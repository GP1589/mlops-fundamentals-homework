# Grading Rubric: End-to-End MLOps Homework

**Total Points: 20** (includes 2 pts for bonus/advanced features)

---

## 1. Data Pipeline (6 points)

### 1.1 Dataset Integrity (1 point)
- **0.5 pts**: `songs.csv` MD5 matches expected hash (`dvc status songs.csv.dvc` is clean)
- **0.5 pts**: `dvc repro` produces `data/raw.csv` with correct column count

### 1.2 Process Script (1.5 points)
- **0.5 pts**: Temporal split is correct — year ≤ 2010 → train, year > 2010 → prod_sim (exact boundary matters)
- **0.5 pts**: Both `data/train.csv` and `data/prod_sim.csv` are produced
- **0.5 pts**: Audio features and the `genre` column are present in both outputs

### 1.3 Train Script (2 points)
- **0.5 pts**: Loads training data and target (`genre`) correctly
- **0.5 pts**: Trains 2+ different models (Logistic Regression + at least one other)
- **0.5 pts**: Logs parameters and metrics (accuracy) to MLflow for each model
- **0.5 pts**: All runs appear in MLflow UI with proper naming and artifacts

### 1.4 Evaluate Script (1 point)
- **0.5 pts**: Finds best model by accuracy metric
- **0.5 pts**: Registers best model in MLflow Model Registry with `champion` alias

### 1.5 DVC Pipeline (0.5 points)
- **0.5 pts**: `dvc repro` runs without errors and produces expected outputs

---

## 2. Model Serving (5 points)

### 2.1 API Implementation (3 points)
- **1 pt**: `GET /health` endpoint returns correct response
- **1 pt**: `POST /predict` accepts valid `SpotifyFeatures` payload and returns prediction
- **1 pt**: Request logging implemented (writes to `logs/api_requests.jsonl`)

### 2.2 Pydantic Models (1 point)
- **1 pt**: `SpotifyFeatures` includes the audio feature fields with correct types

### 2.3 Dockerfile (1 point)
- **0.5 pts**: Dockerfile builds without errors
- **0.5 pts**: Includes step to download `@champion` model from MLflow

---

## 3. Drift Monitoring (3 points)

### 3.1 Batch Drift Analysis (1.5 points)
- **0.5 pts**: Loads `data/train.csv` and `data/prod_sim.csv` correctly in `--mode batch`
- **0.5 pts**: Kolmogorov-Smirnov test runs for each audio feature (uses `scipy.stats.ks_2samp`)
- **0.5 pts**: `drift_report.json` contains per-feature `ks_statistic`, `p_value`, `drift_detected`, and an overall `status`

### 3.2 Online Drift Analysis (1.5 points)
- **0.5 pts**: Loads `data/train.csv` and `logs/api_requests.jsonl` correctly in `--mode online`
- **0.5 pts**: Parses JSONL line-by-line and builds a DataFrame of production features
- **0.5 pts**: Reuses the same KS analysis logic as batch mode (`run_ks_analysis`)

---

## 4. Testing & CI/CD (4 points)

### 4.1 Unit Tests (2 points)
- **1 pt**: `pytest data_pipeline/tests` passes (all assertions pass)
- **1 pt**: `pytest model_serving/tests` passes (all assertions pass)

### 4.2 Code Quality (1 point)
- **1 pt**: `flake8 .` shows no major style violations (warnings OK, errors not OK)

### 4.3 GitHub Actions (1 point)
- **1 pt**: CI pipeline passes on PR (linter + all tests pass)

---

## 5. Documentation & Code Quality (2 points)

### 5.1 Code Quality (1 point)
- **1 pt**: All TODO comments are addressed; code follows Python style guidelines

### 5.2 README & Setup (1 point)
- **0.5 pts**: README is clear and instructions are followable
- **0.5 pts**: Setup works end-to-end (download → process → train → evaluate)

---

## Point Distribution Summary

| Component | Points |
|-----------|--------|
| Data Pipeline | 6 |
| Model Serving | 5 |
| Drift Monitoring | 3 |
| Testing & CI/CD | 4 |
| Documentation | 2 |
| **TOTAL** | **20** |


---

## Common Pitfalls (Don't lose points!)

❌ **Off by one errors in temporal split**: Ensure year ≤ 2010 for train, not < 2010  
❌ **Forgetting to encode genre**: Models need numeric labels, not strings  
❌ **Missing MLflow logging**: Parameters and metrics must be logged, not just in code  
❌ **Pydantic field mismatches**: API fields must match expected payload in tests  
❌ **Git not tracking files**: Ensure all code is committed before CI runs
