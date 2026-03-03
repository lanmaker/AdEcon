from __future__ import annotations

import hashlib
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.auction_engine.mechanism import GSP, VCG

try:
    from feast import FeatureStore
except Exception:  # pragma: no cover - optional dependency path
    FeatureStore = None


def _parse_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _parse_non_negative_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(0, value)


def api_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message},
    )


BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_REPO_PATH = os.getenv("FEATURE_REPO_PATH", str(BASE_DIR / "feature_store"))
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "model_training" / "ad_model.onnx"))
FEATURE_MAPPING_PATH = os.getenv(
    "FEATURE_MAPPING_PATH", str(BASE_DIR / "model_training" / "feature_mapping.json")
)

FEAST_USAGE = _parse_bool_env("FEAST_USAGE", False)
MAX_CANDIDATES_PER_REQUEST = _parse_non_negative_int_env("MAX_CANDIDATES_PER_REQUEST", 200)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
if not ALLOWED_ORIGINS:
    ALLOWED_ORIGINS = ["*"]
ALLOW_CREDENTIALS = "*" not in ALLOWED_ORIGINS

SPARSE_FEATURES = [
    "C1",
    "banner_pos",
    "site_id",
    "site_domain",
    "site_category",
    "app_id",
    "app_domain",
    "app_category",
    "device_model",
    "device_type",
    "device_conn_type",
    "C14",
    "C15",
    "C16",
    "C17",
    "C18",
    "C19",
    "C20",
    "C21",
    "time_of_day",
]

ONLINE_TO_TRAIN_FEATURES = {
    "user_features:device_model": "device_model",
    "user_features:device_type": "device_type",
    "user_features:device_conn_type": "device_conn_type",
    "ad_features:site_id": "site_id",
    "ad_features:site_domain": "site_domain",
    "ad_features:site_category": "site_category",
    "ad_features:app_id": "app_id",
    "ad_features:app_domain": "app_domain",
    "ad_features:app_category": "app_category",
    "ad_features:banner_pos": "banner_pos",
}


def _fallback_feature_index(user_id: str, ad_id: str, feat_name: str, mapping_size: int) -> int:
    if mapping_size <= 0:
        return 0
    key = f"{user_id}:{ad_id}:{feat_name}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return int.from_bytes(digest[:8], "big") % mapping_size


def _build_model_input(
    *,
    user_id: str,
    ad_ids: List[str],
    raw_features: Dict[str, List],
    feature_mapping: Dict[str, Dict[str, int]],
) -> np.ndarray:
    input_data: List[List[int]] = []
    for index, ad_id in enumerate(ad_ids):
        row: List[int] = []
        for feature_name in SPARSE_FEATURES:
            mapping = feature_mapping.get(feature_name, {})
            if feature_name in raw_features and index < len(raw_features[feature_name]):
                raw_value = str(raw_features[feature_name][index])
                value = int(mapping.get(raw_value, 0))
            else:
                if FEAST_USAGE:
                    value = 0
                else:
                    value = _fallback_feature_index(
                        user_id=user_id,
                        ad_id=ad_id,
                        feat_name=feature_name,
                        mapping_size=len(mapping),
                    )
            row.append(value)
        input_data.append(row)
    return np.array(input_data, dtype=np.float32)


def _fetch_online_features(fs: Optional["FeatureStore"], user_id: str, ad_ids: List[str]) -> Dict[str, List]:
    if not FEAST_USAGE or fs is None:
        return {}
    entity_rows = [{"user_id": user_id, "ad_id": ad_id} for ad_id in ad_ids]
    raw = fs.get_online_features(
        features=list(ONLINE_TO_TRAIN_FEATURES.keys()),
        entity_rows=entity_rows,
    ).to_dict()

    features: Dict[str, List] = {}
    for online_feature, train_feature in ONLINE_TO_TRAIN_FEATURES.items():
        short_name = online_feature.split(":")[-1]
        if short_name in raw:
            features[train_feature] = raw[short_name]
        elif online_feature in raw:
            features[train_feature] = raw[online_feature]
    return features


def load_resources(app: FastAPI) -> None:
    app.state.fs = None
    app.state.ort_session = None
    app.state.feature_mapping = {}
    app.state.startup_error = None

    try:
        app.state.ort_session = ort.InferenceSession(MODEL_PATH)
        with open(FEATURE_MAPPING_PATH, "r", encoding="utf-8") as f:
            app.state.feature_mapping = json.load(f)
    except Exception as exc:
        app.state.startup_error = f"failed to load model resources: {exc}"
        return

    if FEAST_USAGE:
        if FeatureStore is None:
            app.state.startup_error = "FEAST_USAGE=true but feast is not installed"
            return
        try:
            app.state.fs = FeatureStore(repo_path=FEATURE_REPO_PATH)
        except Exception as exc:
            app.state.startup_error = f"failed to initialize feature store: {exc}"
            return


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_resources(app)
    yield


app = FastAPI(title="AdEcon Real-time Auction", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.fs = None
app.state.ort_session = None
app.state.feature_mapping = {}
app.state.startup_error = None


class AdCandidate(BaseModel):
    ad_id: str = Field(..., min_length=1, max_length=128)
    bid: float = Field(..., gt=0)


class RecommendRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=128)
    candidates: List[AdCandidate]
    mechanism: str = Field(default="gsp", min_length=1, max_length=16)


@app.post("/recommend")
async def recommend(request: RecommendRequest):
    if not request.candidates:
        raise api_error(422, "INVALID_CANDIDATES", "candidates must not be empty")
    if MAX_CANDIDATES_PER_REQUEST > 0 and len(request.candidates) > MAX_CANDIDATES_PER_REQUEST:
        raise api_error(
            422,
            "TOO_MANY_CANDIDATES",
            f"candidates exceeds limit: {MAX_CANDIDATES_PER_REQUEST}",
        )

    ad_ids = [candidate.ad_id for candidate in request.candidates]
    if len(ad_ids) != len(set(ad_ids)):
        raise api_error(422, "DUPLICATE_AD_IDS", "candidates must have unique ad_id")

    mechanism = request.mechanism.strip().lower()
    if mechanism not in {"gsp", "vcg"}:
        raise api_error(422, "INVALID_MECHANISM", "mechanism must be one of: gsp, vcg")

    if app.state.ort_session is None:
        raise api_error(
            503,
            "MODEL_NOT_READY",
            app.state.startup_error or "model resources are not ready",
        )
    if FEAST_USAGE and app.state.fs is None:
        raise api_error(
            503,
            "FEATURE_STORE_NOT_READY",
            app.state.startup_error or "feature store is not ready",
        )

    try:
        user_id = request.user_id.strip()
        features = _fetch_online_features(app.state.fs, user_id=user_id, ad_ids=ad_ids)
        input_tensor = _build_model_input(
            user_id=user_id,
            ad_ids=ad_ids,
            raw_features=features,
            feature_mapping=app.state.feature_mapping,
        )
        ort_inputs = {app.state.ort_session.get_inputs()[0].name: input_tensor}
        ort_outs = app.state.ort_session.run(None, ort_inputs)
        pctrs = ort_outs[0].flatten().tolist()

        auction_candidates = [
            {
                "ad_id": candidate.ad_id,
                "bid": candidate.bid,
                "pctr": float(pctrs[index]),
                "user_id": user_id,
            }
            for index, candidate in enumerate(request.candidates)
        ]
        mechanism_impl = VCG() if mechanism == "vcg" else GSP()
        results = mechanism_impl.run(auction_candidates)
        return {"results": results}
    except HTTPException:
        raise
    except Exception as exc:
        raise api_error(500, "RECOMMEND_FAILED", str(exc))


@app.get("/healthz")
async def health():
    model_ready = app.state.ort_session is not None
    feature_store_ready = (not FEAST_USAGE) or (app.state.fs is not None)
    status = "ok" if model_ready and feature_store_ready else "degraded"
    return {
        "status": status,
        "feast_usage": FEAST_USAGE,
        "model_ready": model_ready,
        "feature_store_ready": feature_store_ready,
        "max_candidates_per_request": MAX_CANDIDATES_PER_REQUEST,
        "startup_error": app.state.startup_error,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
