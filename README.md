# AdEcon: Advertising Economy Simulation

AdEcon is a comprehensive platform for simulating and analyzing advertising economies. It combines a machine learning-powered backend with a modern frontend to demonstrate auction mechanisms, feature stores, and model training.

## Project Structure

- **backend/**: Python-based backend service (FastAPI/Flask).
- **frontend/**: Vue.js + Vite frontend application.
- **feature_store/**: Feast feature store configuration and definitions.
- **model_training/**: Scripts and models for ad prediction (DeepFM).
- **data/**: Raw data and preprocessing scripts.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AdEcon
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    - Frontend: [http://localhost:80](http://localhost:80)
    - Backend API: [http://localhost:8000](http://localhost:8000)

## Development

### Backend
The backend handles the auction logic and serves the machine learning models. It is containerized and mounts the `feature_store` and `model_training` directories for easy access to data and models.

### Frontend
The frontend is built with Vue 3 and Vite, providing an interactive interface to visualize the auction mechanisms and ad performance.

### Feature Store & Model Training
The project uses Feast for feature serving and DeepFM for click-through rate (CTR) prediction.
