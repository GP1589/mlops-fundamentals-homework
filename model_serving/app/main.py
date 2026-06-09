from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
import logging
import os
from pathlib import Path
import mlflow

app = FastAPI(title="Spotify Genre Classifier API", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpotifyFeatures(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int


class PredictionResponse(BaseModel):
    genre: str
    confidence: float = 0.0


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming /predict requests to logs/api_requests.jsonl.
    """
    if request.method == "POST" and request.url.path == "/predict":
        body_bytes = await request.body()
        try:
            body_json = json.loads(body_bytes)
        except json.JSONDecodeError:
            body_json = {}

        from datetime import datetime, timezone
        body_json["timestamp"] = datetime.now(timezone.utc).isoformat()

        base_dir = Path(__file__).resolve().parent.parent
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

        with open(logs_dir / "api_requests.jsonl", "a") as f:
            f.write(json.dumps(body_json) + "\n")

        async def receive():
            return {"type": "http.request", "body": body_bytes}

        request = Request(request.scope, receive)

    response = await call_next(request)
    return response


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: SpotifyFeatures) -> PredictionResponse:
    """Predict Spotify track genre from audio features."""
    try:
        prediction = predict_genre(features)
        return prediction
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")


# Global variable to cache the loaded model
loaded_model = None
GENRES = ['Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Hip-Hop', 'Jazz', 'Pop', 'R&B', 'Rock']

def load_champion_model():
    global loaded_model
    if loaded_model is not None:
        return loaded_model

    model_path = "./models/model"
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

    import mlflow
    try:
        import mlflow.sklearn
        loaded_model = mlflow.sklearn.load_model(model_path)
        logger.info("Loaded champion model using mlflow.sklearn")
    except Exception as e:
        logger.warning(f"Failed to load model as sklearn: {e}")
        try:
            import mlflow.xgboost
            loaded_model = mlflow.xgboost.load_model(model_path)
            logger.info("Loaded champion model using mlflow.xgboost")
        except Exception as e2:
            logger.warning(f"Failed to load model as xgboost: {e2}")
            try:
                import mlflow.pyfunc
                loaded_model = mlflow.pyfunc.load_model(model_path)
                logger.info("Loaded champion model using mlflow.pyfunc")
            except Exception as e3:
                logger.error(f"Failed to load champion model: {e3}")
                raise e3
    return loaded_model

def predict_genre(features: SpotifyFeatures) -> PredictionResponse:
    model = load_champion_model()

    feature_names = [
        "danceability", "energy", "key", "loudness", "mode", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms"
    ]
    feature_vector = [getattr(features, name) for name in feature_names]

    # Perform inference
    pred = model.predict([feature_vector])[0]

    # Handle confidence score
    confidence = 0.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([feature_vector])
        confidence = float(probabilities[0].max())
    else:
        # If the model wrapper is a pyfunc model, it might not have predict_proba directly,
        # but we can try to call it on the underlying model if exposed, or fallback to 1.0.
        try:
            underlying_model = model._model_impl.python_model
            if hasattr(underlying_model, "predict_proba"):
                probabilities = underlying_model.predict_proba([feature_vector])
                confidence = float(probabilities[0].max())
            else:
                confidence = 1.0
        except Exception:
            confidence = 1.0

    # Decode class index back to genre name
    try:
        predicted_genre = GENRES[int(pred)]
    except (ValueError, IndexError, TypeError):
        predicted_genre = str(pred)

    return PredictionResponse(genre=predicted_genre, confidence=confidence)
