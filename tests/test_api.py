import importlib
import sys

from fastapi.testclient import TestClient


def load_app(monkeypatch, **env):
    monkeypatch.setenv("FEAST_USAGE", "false")
    monkeypatch.setenv("MAX_CANDIDATES_PER_REQUEST", "200")
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    if "backend.main" in sys.modules:
        del sys.modules["backend.main"]
    module = importlib.import_module("backend.main")
    return module.app


def test_recommend_happy_path(monkeypatch):
    app = load_app(monkeypatch)
    with TestClient(app) as client:
        response = client.post(
            "/recommend",
            json={
                "user_id": "dev_1",
                "candidates": [
                    {"ad_id": "ad_1", "bid": 1.2},
                    {"ad_id": "ad_2", "bid": 2.0},
                ],
                "mechanism": "gsp",
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert "results" in payload
    assert len(payload["results"]) == 2


def test_recommend_rejects_empty_candidates(monkeypatch):
    app = load_app(monkeypatch)
    with TestClient(app) as client:
        response = client.post(
            "/recommend",
            json={"user_id": "dev_1", "candidates": [], "mechanism": "gsp"},
        )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_CANDIDATES"


def test_recommend_rejects_duplicate_ad_ids(monkeypatch):
    app = load_app(monkeypatch)
    with TestClient(app) as client:
        response = client.post(
            "/recommend",
            json={
                "user_id": "dev_1",
                "candidates": [
                    {"ad_id": "ad_1", "bid": 1.0},
                    {"ad_id": "ad_1", "bid": 1.1},
                ],
                "mechanism": "gsp",
            },
        )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "DUPLICATE_AD_IDS"


def test_recommend_rejects_invalid_mechanism(monkeypatch):
    app = load_app(monkeypatch)
    with TestClient(app) as client:
        response = client.post(
            "/recommend",
            json={
                "user_id": "dev_1",
                "candidates": [{"ad_id": "ad_1", "bid": 1.2}],
                "mechanism": "invalid",
            },
        )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_MECHANISM"


def test_recommend_rejects_too_many_candidates(monkeypatch):
    app = load_app(monkeypatch, MAX_CANDIDATES_PER_REQUEST="1")
    with TestClient(app) as client:
        response = client.post(
            "/recommend",
            json={
                "user_id": "dev_1",
                "candidates": [
                    {"ad_id": "ad_1", "bid": 1.2},
                    {"ad_id": "ad_2", "bid": 1.1},
                ],
                "mechanism": "gsp",
            },
        )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "TOO_MANY_CANDIDATES"


def test_health_ok(monkeypatch):
    app = load_app(monkeypatch)
    with TestClient(app) as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"ok", "degraded"}
    assert "model_ready" in payload
    assert "startup_error" in payload


def test_health_degraded_when_model_missing(monkeypatch):
    app = load_app(monkeypatch, MODEL_PATH="/tmp/nonexistent-model.onnx")
    with TestClient(app) as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["model_ready"] is False
