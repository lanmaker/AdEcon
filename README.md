# AdEcon: Advertising Economy Simulation

AdEcon is a platform for simulating and analyzing advertising economies. It pairs an auction-driven FastAPI backend with a Vue/Vite frontend, Feast feature store definitions, and DeepFM training utilities.

## Project Structure
- **backend/** – FastAPI service with auction mechanisms (GSP/VCG) and ONNX inference.
- **frontend/** – Vue 3 + Vite UI for configuring and visualizing auctions.
- **feature_store/** – Feast feature definitions and local registry/online store artifacts.
- **model_training/** – DeepFM training/export scripts and model artifacts.
- **data/** – Raw/processed datasets plus generation and preprocess scripts.

## Prerequisites
- Docker Desktop (or Docker Engine) with Compose
- Optional for manual development: Python 3.9+, Node.js 20+, npm

## Quick Start (Docker Compose)
```bash
git clone <repository-url>
cd AdEcon
docker compose up --build -d
```
Access:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

Stop the stack:
```bash
docker compose down
```

## Manual Local Development
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
python -m backend.main
```
The backend serves on http://localhost:8000 (docs at /docs).

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Vite dev server defaults to http://localhost:5173.

## Cloud / Container Deployment
Build and push images to your registry:
```bash
docker build -t <registry>/adecon-backend -f backend/Dockerfile .
docker build -t <registry>/adecon-frontend -f frontend/Dockerfile .
docker push <registry>/adecon-backend
docker push <registry>/adecon-frontend
```
Run on ECS, Cloud Run, Azure Container Apps, etc., mapping:
- Backend: expose port 8000
- Frontend: expose port 80

### Feature Store considerations
The default Feast setup uses local SQLite for the registry/online store. For production/replicas, update `feature_store/feature_store.yaml` to point to a remote registry and online store (e.g., S3/GCS + Redis/DynamoDB/Postgres) and bake or mount updated configs into the backend image.

## Development Notes
- Backend mounts `feature_store` and `model_training` in the container for access to registry and ONNX artifacts.
- Frontend calls the backend at `http://localhost:8000` (see `frontend/src/App.vue`).
- Model artifacts live in `model_training/ad_model.onnx` and `model_training/feature_mapping.json`.

## Maintenance
- Clean generated artifacts: `rm -rf frontend/node_modules **/__pycache__ .DS_Store feature_store/data/*.db feature_store/data/*.parquet`
- Rebuild containers after dependency changes: `docker compose build --no-cache`
