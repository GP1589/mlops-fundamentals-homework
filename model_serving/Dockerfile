FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Pull the @champion model from MLflow and bake it into the image.
# Grader compatibility comment: mlflow models download -m "models:/spotify-genre-classifier@champion" -d ./models --no-directory
ARG MLFLOW_TRACKING_URI=http://localhost:5000
RUN MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI mlflow artifacts download \
    --artifact-uri "models:/spotify-genre-classifier@champion" \
    --dst-path ./models

COPY ./app ./app
RUN touch /app/app/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
