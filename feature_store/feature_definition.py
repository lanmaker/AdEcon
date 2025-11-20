import os
from datetime import timedelta
from pathlib import Path
from feast import Entity, Field, FeatureView, FileSource, ValueType
from feast.types import Int64, String, Float32

BASE_DIR = Path(__file__).resolve().parent.parent
# Allow overriding via env for containerized deployments
processed_data_path = os.getenv(
    "PROCESSED_DATA_PATH", str(BASE_DIR / "data" / "processed_data.parquet")
)

# Define Entities
user = Entity(name="user_id", join_keys=["user_id"])
ad = Entity(name="ad_id", join_keys=["ad_id"])

# Define Data Source (local file store for demo)
offline_source = FileSource(
    path=processed_data_path,
    timestamp_field="event_timestamp",
)

# Define Feature Views

# User Features: We will just take some device properties as "User Features" for this demo
# In reality, these would be aggregated stats (e.g. average CTR).
user_fv = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=365), # Long TTL for demo
    schema=[
        Field(name="device_model", dtype=String),
        Field(name="device_type", dtype=Int64),
        Field(name="device_conn_type", dtype=Int64),
    ],
    source=offline_source,
)

# Ad Features: Site/App info as "Ad Features"
ad_fv = FeatureView(
    name="ad_features",
    entities=[ad],
    ttl=timedelta(days=365),
    schema=[
        Field(name="site_id", dtype=String),
        Field(name="site_domain", dtype=String),
        Field(name="site_category", dtype=String),
        Field(name="app_id", dtype=String),
        Field(name="app_domain", dtype=String),
        Field(name="app_category", dtype=String),
        Field(name="banner_pos", dtype=Int64),
    ],
    source=offline_source,
)

# Context Features? 
# Usually context features (time_of_day) are passed in the request, not retrieved from Feast.
# But we can store them if we want to log them.
