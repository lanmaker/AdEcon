# AdEcon: Real-time Advertising Auction & Recommendation System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue_3-green.svg)](https://vuejs.org/)
[![Feast](https://img.shields.io/badge/Feature_Store-Feast-orange.svg)](https://docs.feast.dev/)
[![Docker](https://img.shields.io/badge/Deployment-Docker-blue.svg)](https://www.docker.com/)

**AdEcon** is a full-stack ML systems project that simulates a real-time ad economy. It pairs a DeepFM CTR prediction model with a pluggable auction engine to highlight the intersection of Computational Economics and ML Engineering.

![Dashboard Screenshot](docs/dashboard_screenshot.png) <!-- Replace with your actual UI screenshot -->

## 🚀 Key Features
- **Full-Stack MLE Architecture**: End-to-end path from feature definitions to model serving and real-time visualization.
- **Training–Serving Consistency**: Feature retrieval via **Feast** for point-in-time correctness across training and online inference.
- **Auction Mechanisms**: Pluggable **GSP** and **VCG** auctions with cost/revenue/surplus visualization.
- **Real-time Inference**: ONNX-exported DeepFM served through **FastAPI** with low-latency inference.
- **Interactive Dashboard**: Modern **Vue 3 + Vite** UI to configure candidates, switch mechanisms, and inspect outcomes.

## 🛠️ Project Structure
- `backend/` – FastAPI service with auction logic and ONNX inference.
- `frontend/` – Vue 3 + Vite dashboard for simulation and visualization.
- `feature_store/` – Feast configs, feature definitions, and local registry/online store.
- `model_training/` – DeepFM training/export scripts and model artifacts.
- `data/` – Raw/processed datasets plus generation/preprocess scripts.

## 🏁 Quick Start (Docker Compose)
Prerequisite: Docker Desktop (or Docker Engine) with Compose.

```bash
git clone https://github.com/lanmaker/AdEcon.git
cd AdEcon
docker compose up --build -d
```

Access:
- Frontend dashboard: http://localhost (if port 80 is taken, adjust the mapping in `docker-compose.yml`, e.g., `8080:80`)
- Backend API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs

Stop the stack:
```bash
docker compose down
```

## 💻 Manual Local Development
### Backend
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd feature_store
feast apply
feast materialize-incremental "$(date +%Y-%m-%d)"
cd ..

export PYTHONPATH=$PYTHONPATH:.
python -m backend.main  # runs at http://localhost:8000 (docs at /docs)
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # Vite dev server at http://localhost:5173
```

## 📦 Cloud / Container Deployment
Build and push images to your registry (ECR/GCR/Docker Hub):
```bash
docker build -t <registry>/adecon-backend -f backend/Dockerfile .
docker build -t <registry>/adecon-frontend -f frontend/Dockerfile .
docker push <registry>/adecon-backend
docker push <registry>/adecon-frontend
```
Run on ECS, Cloud Run, Azure Container Apps, etc., exposing port 8000 for the backend and port 80 for the frontend.

**Feature store in production:** Update `feature_store/feature_store.yaml` to use remote registry/online stores (e.g., S3/GCS + Redis/Dynamo/Postgres) for multi-replica consistency.  
**Model artifacts:** `model_training/ad_model.onnx` and `model_training/feature_mapping.json` are baked/mounted; in production, version them (MLflow/DVC) and bake or fetch at runtime.

## 🧹 Maintenance
Clean generated artifacts (use with care):
```bash
rm -rf frontend/node_modules **/__pycache__ .DS_Store feature_store/data/*.db feature_store/data/*.parquet
```
