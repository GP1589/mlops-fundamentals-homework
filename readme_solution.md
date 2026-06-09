# Solución: Spotify Genre Classification & Drift Monitoring

Este documento detalla las instrucciones de instalación, ejecución y pruebas del proyecto utilizando los comandos y ajustes adaptados (con `uv` y `mlflow artifacts`).

---

## 1. Configuración del Entorno e Instalación

Para instalar todas las dependencias del monorepositorio utilizando `uv` como gestor de paquetes de alto rendimiento, ejecuta los siguientes comandos desde la raíz del proyecto:

```bash
# Instalar dependencias de cada componente
uv pip install -r data_pipeline/requirements.txt
uv pip install -r model_serving/requirements.txt
uv pip install -r drift_monitoring/requirements.txt

# Instalar framework de pruebas
uv pip install pytest
```

---

## 2. Servidor de MLflow (Model Registry)

Para habilitar el registro de modelos (**Model Registry**), el servidor de MLflow debe iniciarse utilizando una base de datos relacional (como SQLite). Ejecuta el siguiente comando desde la raíz del proyecto para iniciar el servidor de MLflow apuntando a la base de datos de la raíz:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```
*Mantén esta terminal abierta corriendo el servidor de MLflow.*

---

## 3. Ejecución del Pipeline de Datos (DVC)

Para procesar el dataset original de Spotify (`songs.csv`), entrenar los modelos de clasificación (Logistic Regression y XGBoost) y registrar el mejor en MLflow, muévete a la carpeta `data_pipeline` y ejecuta el pipeline de DVC:

```bash
cd data_pipeline

# Forzar la reproducción de todas las etapas
dvc repro --force
```

Este comando:
1. Carga los datos crudos en `data/raw.csv`.
2. Realiza la partición temporal por el año 2010 generando `data/train.csv` (entrenamiento) y `data/prod_sim.csv` (simulación de producción).
3. Entrena ambos modelos de clasificación y los registra en MLflow.
4. Evalúa las métricas, registra el modelo con mejor precisión como `spotify-genre-classifier` y le asigna el alias `@champion`.

---

## 4. Servir el Modelo (FastAPI)

### Descarga del Modelo para Pruebas Locales
Para poder realizar pruebas locales y validaciones rápidas fuera de Docker, descarga el modelo campeón desde el servidor de MLflow a la carpeta local de `model_serving/models`:

```bash
# Ejecutar desde la raíz del proyecto
MLFLOW_TRACKING_URI=http://localhost:5000 mlflow artifacts download \
  --artifact-uri "models:/spotify-genre-classifier@champion" \
  --dst-path model_serving/models
```

### Iniciar el Servidor de FastAPI
Para levantar la API localmente en modo desarrollo con recarga automática:

```bash
# Moverse al directorio de serving
cd model_serving

# Iniciar la API con uv
uv run uvicorn app.main:app --reload --port 8000
```

---

## 5. Pruebas Unitarias

Para correr las pruebas unitarias y verificar el funcionamiento de las etapas de datos y la API de serving, ejecuta:

```bash
# Pruebas del pipeline de datos
pytest data_pipeline/tests -v

# Pruebas de la API de serving
pytest model_serving/tests -v
```

---

## 6. Monitoreo de Deriva de Datos (Drift Monitoring)

Para ejecutar el análisis estadístico de Kolmogorov-Smirnov sobre las variables de audio y detectar desviaciones de distribución, utiliza los siguientes comandos:

### Modo Batch (Compara datos de entrenamiento vs simulación de producción)
```bash
uv run drift_monitoring/src/analyze_drift.py \
  --mode batch \
  --train_data data_pipeline/data/train.csv \
  --prod_data data_pipeline/data/prod_sim.csv \
  --output drift_monitoring/batch_drift_report.json
```

### Modo Online (Compara datos de entrenamiento vs logs de peticiones reales de la API)
```bash
uv run drift_monitoring/src/analyze_drift.py \
  --mode online \
  --train_data data_pipeline/data/train.csv \
  --api_logs model_serving/logs/api_requests.jsonl \
  --output drift_monitoring/online_drift_report.json
```

---

## 7. Construcción y Despliegue en Docker

Para encapsular la API en un contenedor de Docker autocontenido (que descargará el modelo campeón en tiempo de construcción):

```bash
# Moverse al directorio del serving
cd model_serving

# Construir la imagen de Docker usando la red local para conectarse al servidor de MLflow
docker build --network=host -t spotify-api:latest .

# Correr el contenedor de Docker mapeando el puerto de API
docker run -p 8000:8000 spotify-api:latest
```
