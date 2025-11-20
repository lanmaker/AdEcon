FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and artifacts
COPY backend /app/backend
COPY feature_store /app/feature_store
COPY model_training /app/model_training
COPY data /app/data

ENV FEATURE_REPO_PATH=/app/feature_store \
    MODEL_PATH=/app/model_training/ad_model.onnx \
    FEATURE_MAPPING_PATH=/app/model_training/feature_mapping.json \
    PROCESSED_DATA_PATH=/app/data/processed_data.parquet \
    FEAST_USAGE=False

# Expose port
EXPOSE 8000

# Run command
# Apply/materialize Feast repo then start API
CMD ["/bin/sh", "-c", "feast -c ${FEATURE_REPO_PATH} apply && feast -c ${FEATURE_REPO_PATH} materialize-incremental \"$(date +%Y-%m-%d)\" && python -m backend.main"]
