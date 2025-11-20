import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_rows=100000):
    """
    Generates synthetic data mimicking the Avazu CTR Prediction dataset.
    """
    print(f"Generating {num_rows} rows of synthetic data...")
    
    # Fixed seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    # Generate timestamps (last 7 days)
    base_date = datetime.now()
    dates = [base_date - timedelta(days=x) for x in range(7)]
    
    data = {
        'id': [f'{i:010d}' for i in range(num_rows)],
        'click': np.random.choice([0, 1], size=num_rows, p=[0.8, 0.2]), # ~20% CTR
        'hour': [], # YYMMDDHH format
        'C1': np.random.randint(1000, 1010, size=num_rows),
        'banner_pos': np.random.randint(0, 2, size=num_rows),
        'site_id': [f'site_{random.randint(0, 100)}' for _ in range(num_rows)],
        'site_domain': [f'domain_{random.randint(0, 50)}' for _ in range(num_rows)],
        'site_category': [f'cat_{random.randint(0, 20)}' for _ in range(num_rows)],
        'app_id': [f'app_{random.randint(0, 50)}' for _ in range(num_rows)],
        'app_domain': [f'app_domain_{random.randint(0, 20)}' for _ in range(num_rows)],
        'app_category': [f'app_cat_{random.randint(0, 10)}' for _ in range(num_rows)],
        'device_id': [f'dev_{random.randint(0, 1000)}' for _ in range(num_rows)], # User ID proxy
        'device_ip': [f'ip_{random.randint(0, 5000)}' for _ in range(num_rows)],
        'device_model': [f'model_{random.randint(0, 100)}' for _ in range(num_rows)],
        'device_type': np.random.randint(0, 2, size=num_rows),
        'device_conn_type': np.random.randint(0, 4, size=num_rows),
        'C14': np.random.randint(300, 400, size=num_rows),
        'C15': np.random.choice([320, 300], size=num_rows),
        'C16': np.random.choice([50, 250], size=num_rows),
        'C17': np.random.randint(100, 200, size=num_rows),
        'C18': np.random.randint(0, 4, size=num_rows),
        'C19': np.random.randint(30, 40, size=num_rows),
        'C20': np.random.randint(100000, 100010, size=num_rows),
        'C21': np.random.randint(10, 100, size=num_rows),
    }

    # Generate 'hour' column
    for _ in range(num_rows):
        d = random.choice(dates)
        h = random.randint(0, 23)
        data['hour'].append(int(d.strftime('%y%m%d') + f"{h:02d}"))

    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = 'data/train.csv'
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
