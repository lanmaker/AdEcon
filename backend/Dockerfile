FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# We need to create requirements.txt first or list them here
# Using inline pip install for simplicity of this file, but better to use requirements.txt
RUN pip install --no-cache-dir \
    fastapi uvicorn onnxruntime feast pandas numpy scikit-learn torch

# Copy backend code
COPY backend /app/backend
COPY feature_store /app/feature_store
COPY model_training /app/model_training

# Expose port
EXPOSE 8000

# Run command
# We need to be in /app to run python -m backend.main
CMD ["python", "-m", "backend.main"]
