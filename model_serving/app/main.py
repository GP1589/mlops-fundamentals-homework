from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import logging
import os
from pathlib import Path

app = FastAPI(title="Spotify Genre Classifier API", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpotifyFeatures(BaseModel):
    """
    Spotify audio features for genre classification.

    Based on the 550k Spotify Songs dataset from Kaggle.
    All values are normalized by Spotify to ranges [0, 1] except where noted.
    """
    danceability: float  # 0-1: How suitable for dancing
    energy: float  # 0-1: Intensity and activity
    key: int  # 0-11: Pitch class (C to B)
    loudness: float  # dB: Overall loudness
    mode: int  # 0-1: Major (1) or Minor (0)
    speechiness: float  # 0-1: Presence of spoken words
    acousticness: float  # 0-1: How acoustic
    instrumentalness: float  # 0-1: Likelihood of instrumental
    liveness: float  # 0-1: Presence of audience
    valence: float  # 0-1: Musical positiveness
    tempo: float  # BPM: Beats per minute
    duration_ms: int  # Milliseconds: Song length


class PredictionResponse(BaseModel):
    genre: str
    confidence: float = 0.0


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: SpotifyFeatures) -> PredictionResponse:
    """
    Predict Spotify track genre from audio features.

    Logs incoming requests to logs/api_requests.jsonl for drift monitoring.
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    request_log_path = logs_dir / "api_requests.jsonl"

    request_data = {
        **features.model_dump(),
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }

    with open(request_log_path, "a") as f:
        f.write(json.dumps(request_data) + "\n")

    logger.info(f"Logged prediction request: {request_data}")

    try:
        prediction = predict_genre(features)
        return prediction
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")


def predict_genre(features: SpotifyFeatures) -> PredictionResponse:
    """
    **IMPORTANT: This is an intentionally incomplete skeleton for students to implement.**
    
    Students must:
    1. Load the MLflow model registered with the @champion alias
       - The model is baked into the Docker container at ./models/
       - Use: mlflow.sklearn.load_model("models:/champion@champion/production")
    2. Convert SpotifyFeatures to the format expected by the model
       - Extract feature values in the correct order (order matters for sklearn models)
       - Must match the 12 audio features used during training
    3. Perform inference on the 12 audio features
    4. Map the predicted class index back to genre name
    5. Return a PredictionResponse with the genre and confidence score

    Example implementation structure:
        import mlflow
        from sklearn.preprocessing import LabelEncoder
        
        # Load model once (consider caching for performance)
        model = mlflow.sklearn.load_model("models:/champion@champion/production")
        
        # Extract features in correct order matching training data
        feature_names = [
            'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'
        ]
        feature_vector = [getattr(features, name) for name in feature_names]
        
        # Make prediction
        prediction = model.predict([feature_vector])
        
        # Get confidence (probability of predicted class)
        # For probability estimates: model.predict_proba([feature_vector])
        
        # Map class index to genre name
        genres = ['Rock', 'Pop', 'Electronic', 'Folk', 'Country', 'Hip-Hop', 'R&B', 'Jazz', 'Blues', 'Classical']
        predicted_genre = genres[prediction[0]]
        
        return PredictionResponse(genre=predicted_genre, confidence=confidence)
    
    For now, returns a placeholder response so API tests pass:
    """
    return PredictionResponse(genre="Pop", confidence=0.85)
