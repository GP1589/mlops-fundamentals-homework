FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Configure MLflow tracking URI
# Students can override this when building the image:
#   docker build --build-arg MLFLOW_TRACKING_URI=http://your-mlflow-server:5000 .
ARG MLFLOW_TRACKING_URI=http://localhost:5000

# Pull the MLflow model with @champion alias and bake it into the image
# This requires either:
# 1. MLflow server running at the MLFLOW_TRACKING_URI during build time, OR
# 2. Override MLFLOW_TRACKING_URI with a running MLflow server when building:
#    docker build --build-arg MLFLOW_TRACKING_URI=http://mlflow-host:5000 .
#
# The command downloads the model registered as "champion" with the @champion alias
RUN mlflow models download -m "models:/champion@champion" -d ./models --no-directory

COPY ./app ./app

# Ensure the app directory is a Python package
RUN touch /app/app/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
