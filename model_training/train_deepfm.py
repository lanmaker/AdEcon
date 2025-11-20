import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, log_loss
import numpy as np
from deepfm import DeepFM
import json

def train_model():
    print("Loading data...")
    data = pd.read_parquet('data/processed_data.parquet')

    # 1. Feature Engineering
    # Only using sparse features for simplicity in this custom implementation
    sparse_features = ['C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'time_of_day']
    target = ['click']

    # Label Encoding and Save Mapping
    lbe_dict = {}
    feat_sizes = []
    for feat in sparse_features:
        lbe = LabelEncoder()
        data[feat] = lbe.fit_transform(data[feat])
        lbe_dict[feat] = {str(k): int(v) for k, v in zip(lbe.classes_, lbe.transform(lbe.classes_))}
        feat_sizes.append(data[feat].max() + 1)
    
    with open('model_training/feature_mapping.json', 'w') as f:
        json.dump(lbe_dict, f)
    print("Feature mappings saved.")

    # Train/Test Split
    train, test = train_test_split(data, test_size=0.2, random_state=2022)
    
    # Convert to tensors
    train_x = torch.tensor(train[sparse_features].values, dtype=torch.float32)
    train_y = torch.tensor(train[target].values, dtype=torch.float32)
    test_x = torch.tensor(test[sparse_features].values, dtype=torch.float32)
    test_y = torch.tensor(test[target].values, dtype=torch.float32)

    # 2. Define Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeepFM(feat_sizes=feat_sizes).to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 3. Training Loop
    print("Training model...")
    batch_size = 256
    epochs = 3
    
    train_dataset = torch.utils.data.TensorDataset(train_x, train_y)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

    # 4. Evaluation
    model.eval()
    with torch.no_grad():
        preds = model(test_x.to(device)).cpu().numpy()
        auc = roc_auc_score(test_y.numpy(), preds)
        ll = log_loss(test_y.numpy(), preds)
        print(f"Test AUC: {auc:.4f}, LogLoss: {ll:.4f}")

    # 5. Export to ONNX
    print("Exporting to ONNX...")
    # Use randint to ensure valid indices (0 is always valid)
    dummy_input = torch.randint(0, 1, (1, len(sparse_features))).float().to(device)
    torch.onnx.export(model, dummy_input, "model_training/ad_model.onnx", 
                      input_names=['input'], output_names=['probability'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'probability': {0: 'batch_size'}})
    print("Model exported to model_training/ad_model.onnx")

if __name__ == "__main__":
    train_model()
