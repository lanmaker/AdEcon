import pandas as pd
import numpy as np

def preprocess_data(input_path='data/train.csv', output_path='data/processed_data.parquet'):
    """
    Preprocesses the raw data:
    1. Handles missing values.
    2. Extracts time_of_day from hour.
    3. Saves as Parquet for Feast.
    """
    print(f"Reading data from {input_path}...")
    df = pd.read_csv(input_path)

    # 1. Handle Missing Values (Simple strategy for demo)
    # For categorical features, fill with 'unknown' or mode
    # For numerical, fill with mean/median
    # In this synthetic dataset, we assume no missing values for simplicity, 
    # but adding a check.
    df.fillna(method='ffill', inplace=True)

    # 2. Extract time_of_day
    # 'hour' format: YYMMDDHH
    df['hour_str'] = df['hour'].astype(str)
    df['time_of_day'] = df['hour_str'].apply(lambda x: int(x[-2:]))
    
    # Create a timestamp column for Feast (event_timestamp)
    # Assuming 'hour' represents the event time.
    # We need a proper datetime object.
    def parse_date(x):
        return pd.to_datetime(x, format='%y%m%d%H')
    
    df['event_timestamp'] = df['hour_str'].apply(parse_date)
    
    # Drop temporary column
    df.drop(columns=['hour_str'], inplace=True)

    # Ensure user_id and ad_id exist for Feast entities
    # Mapping device_id -> user_id
    # Mapping id -> ad_id (or use C1/banner_pos combination as ad proxy, but 'id' is unique impression)
    # For this demo, let's define:
    # User Entity: device_id
    # Ad Entity: id (Impression ID - strictly speaking not reusable 'Ad', but for CTR we predict on impression context)
    # BETTER: Let's create a synthetic 'ad_id' to simulate reusable ads.
    np.random.seed(42)
    df['ad_id'] = [f'ad_{np.random.randint(0, 1000)}' for _ in range(len(df))]
    
    # Rename device_id to user_id for clarity
    df.rename(columns={'device_id': 'user_id'}, inplace=True)

    print(f"Saving processed data to {output_path}...")
    df.to_parquet(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    preprocess_data()
