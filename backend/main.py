from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import onnxruntime as ort
import numpy as np
import json
import os
from pathlib import Path
from feast import FeatureStore
from backend.auction_engine.mechanism import GSP, VCG

app = FastAPI(title="AdEcon Real-time Auction")

# Paths and configuration
BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_REPO_PATH = os.getenv("FEATURE_REPO_PATH", str(BASE_DIR / "feature_store"))
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "model_training" / "ad_model.onnx"))
FEATURE_MAPPING_PATH = os.getenv(
    "FEATURE_MAPPING_PATH", str(BASE_DIR / "model_training" / "feature_mapping.json")
)
ALLOWED_ORIGINS = [
    origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
]

# CORS for browser clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Resources
print("Loading resources...")
# 1. Feature Store
fs = FeatureStore(repo_path=FEATURE_REPO_PATH)

# 2. ONNX Model
ort_session = ort.InferenceSession(MODEL_PATH)

# 3. Feature Mappings
with open(FEATURE_MAPPING_PATH, "r") as f:
    feature_mapping = json.load(f)

# Define Request Models
class AdCandidate(BaseModel):
    ad_id: str
    bid: float
    # In real world, ad properties might come from DB, here we accept some or fetch from Feast
    # We'll fetch ad features from Feast using ad_id

class RecommendRequest(BaseModel):
    user_id: str
    candidates: List[AdCandidate]
    mechanism: str = "gsp" # gsp or vcg

@app.post("/recommend")
async def recommend(request: RecommendRequest):
    try:
        # 1. Fetch Features
        user_id = request.user_id
        ad_ids = [c.ad_id for c in request.candidates]
        
        # Feast: get_online_features
        # We need to construct the entity rows
        entity_rows = [{"user_id": user_id, "ad_id": ad_id} for ad_id in ad_ids]
        
        features = fs.get_online_features(
            features=[
                "user_features:device_model",
                "user_features:device_type",
                "user_features:device_conn_type",
                "ad_features:site_id",
                "ad_features:site_domain",
                "ad_features:site_category",
                "ad_features:app_id",
                "ad_features:app_domain",
                "ad_features:app_category",
                "ad_features:banner_pos",
            ],
            entity_rows=entity_rows
        ).to_dict()
        
        # 2. Preprocess for Model
        # We need to convert features to indices using feature_mapping
        # And construct the input tensor
        
        # Define the order of features as expected by the model (same as training)
        sparse_features = ['C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'time_of_day']
        
        # Note: Our Feast features don't cover all training features (C1, C14-C21, time_of_day are missing or need to be inferred/mocked)
        # For Demo, we will mock missing features with default values (e.g. 0 or mode)
        # time_of_day can be inferred from current time, but let's mock it.
        
        batch_size = len(ad_ids)
        input_data = []
        
        for i in range(batch_size):
            row = []
            for feat in sparse_features:
                val = None
                # Map Feast feature names to training feature names
                # Feast: device_model -> Train: device_model
                # Feast: banner_pos -> Train: banner_pos
                
                if feat in features:
                    raw_val = features[feat][i]
                    # Convert to string for mapping lookup
                    raw_val_str = str(raw_val)
                    
                    if feat in feature_mapping:
                        if raw_val_str in feature_mapping[feat]:
                            val = feature_mapping[feat][raw_val_str]
                        else:
                            # Handle OOV - use a default or 0? 
                            # If 0 is in mapping, use it, else 0
                            val = 0 
                    else:
                        val = 0
                else:
                    # Missing feature (C1, C14...)
                    val = 0 # Default index
                
                row.append(val)
            input_data.append(row)
            
        input_tensor = np.array(input_data, dtype=np.float32)
        
        # 3. Inference
        ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}
        ort_outs = ort_session.run(None, ort_inputs)
        pctrs = ort_outs[0].flatten().tolist()
        
        # 4. Auction
        auction_candidates = []
        for i, cand in enumerate(request.candidates):
            auction_candidates.append({
                "ad_id": cand.ad_id,
                "bid": cand.bid,
                "pctr": pctrs[i],
                "user_id": user_id
            })
            
        if request.mechanism.lower() == "vcg":
            mech = VCG()
        else:
            mech = GSP()
            
        results = mech.run(auction_candidates)
        
        return {"results": results}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
