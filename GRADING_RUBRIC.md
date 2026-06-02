# Grading Rubric: End-to-End MLOps Homework

**Total Points: 20**

### 1. Data Pipeline & DVC (4 pts)
*   **[1 pt]** `download.py` is parameterized (allows changing the data source path easily).
*   **[1 pt]** Data processing splits the dataset temporally (pre-2018 vs 2018+).
*   **[2 pts]** `dvc.yaml` correctly defines the DAG (download -> process -> train -> evaluate) and tracks data/artifacts.

### 2. Experiment Tracking & Evaluation (5 pts)
*   **[2 pts]** `train.py` successfully logs metrics, parameters, and models to MLflow for at least two different model architectures.
*   **[1 pt]** Hyperparameters are driven by `params.yaml` via DVC.
*   **[2 pts]** `evaluate.py` programmatically identifies the best run and assigns it an alias in the MLflow Model Registry.

### 3. Model Serving & Containerization (5 pts)
*   **[2 pts]** FastAPI `/predict` endpoint works and returns correctly formatted predictions.
*   **[1 pt]** FastAPI service logs incoming feature payloads to a file for drift monitoring.
*   **[2 pts]** `Dockerfile` successfully pulls the aliased model from MLflow during the build process, creating an immutable image.

### 4. Drift Monitoring (3 pts)
*   **[3 pts]** `drift_monitoring` script correctly compares the baseline training data (from DVC) against the simulated production logs and outputs a drift report (e.g., using statistical tests on audio features).

### 5. CI/CD & Testing (3 pts)
*   **[1 pt]** GitHub Actions workflow triggers on PRs and runs tests.
*   **[2 pts]** All provided unit tests in `data_pipeline/tests/` and `model_serving/tests/` pass successfully.