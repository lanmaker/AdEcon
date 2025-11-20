import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepFM(nn.Module):
    def __init__(self, feat_sizes, embedding_size=4, hidden_dims=[32, 16], dropout=0.5):
        super(DeepFM, self).__init__()
        self.feat_sizes = feat_sizes
        self.embedding_size = embedding_size
        self.input_dim = len(feat_sizes) * embedding_size
        
        # FM Part
        self.fm_first_order_embeddings = nn.ModuleList([
            nn.Embedding(size, 1) for size in feat_sizes
        ])
        
        self.fm_second_order_embeddings = nn.ModuleList([
            nn.Embedding(size, embedding_size) for size in feat_sizes
        ])
        
        # DNN Part
        layers = []
        in_dim = self.input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            in_dim = hidden_dim
        layers.append(nn.Linear(in_dim, 1))
        self.dnn = nn.Sequential(*layers)
        
    def forward(self, x):
        # x shape: (batch_size, num_features)
        
        # FM First Order
        fm_first_order = []
        for i, emb in enumerate(self.fm_first_order_embeddings):
            fm_first_order.append(emb(x[:, i].long()))
        fm_first_order = torch.cat(fm_first_order, dim=1) # (batch, num_features)
        fm_first_order_sum = torch.sum(fm_first_order, dim=1, keepdim=True) # (batch, 1)
        
        # FM Second Order
        fm_second_order = []
        for i, emb in enumerate(self.fm_second_order_embeddings):
            fm_second_order.append(emb(x[:, i].long()))
        fm_second_order_emb = torch.stack(fm_second_order, dim=1) # (batch, num_features, k)
        
        # sum_square part
        sum_emb = torch.sum(fm_second_order_emb, 1) # (batch, k)
        sum_emb_square = sum_emb * sum_emb # (batch, k)
        
        # square_sum part
        square_emb = fm_second_order_emb * fm_second_order_emb # (batch, num_features, k)
        square_emb_sum = torch.sum(square_emb, 1) # (batch, k)
        
        fm_second_order_sum = 0.5 * torch.sum(sum_emb_square - square_emb_sum, dim=1, keepdim=True) # (batch, 1)
        
        # DNN
        dnn_input = fm_second_order_emb.view(-1, self.input_dim)
        dnn_output = self.dnn(dnn_input)
        
        # Total
        total_sum = fm_first_order_sum + fm_second_order_sum + dnn_output
        return torch.sigmoid(total_sum)
