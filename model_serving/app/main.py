from fastapi import FastAPI
import json

# TODO: Load model from local artifact (baked during Docker build)

app = FastAPI()

@app.post("/predict")
def predict(payload: dict):
    # TODO: Log the incoming feature payload to 'logs/api_requests.jsonl'
    # TODO: Perform inference
    
    # Placeholder return
    return {"genre": "Pop"}
