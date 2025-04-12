# lightzoo/models/transformer.py

import torch
import torch.nn as nn
from .base import BaseModel

class Transformer(BaseModel):
    def __init__(self, input_dim=512, num_tokens=10000, max_len=128, num_heads=8, num_layers=6, num_classes=10):
        super(Transformer, self).__init__()

        self.token_emb = nn.Embedding(num_tokens, input_dim)
        self.pos_emb = nn.Parameter(torch.zeros(1, max_len, input_dim))

        encoder_layer = nn.TransformerEncoderLayer(d_model=input_dim, nhead=num_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.classifier = nn.Sequential(
            nn.Linear(input_dim, num_classes)
        )

    def forward(self, x):
        # x shape: (batch_size, seq_len)
        token_embeddings = self.token_emb(x)                  # (B, L, D)
        embeddings = token_embeddings + self.pos_emb[:, :x.size(1), :]  # Add positional encoding

        transformed = self.transformer(embeddings.transpose(0, 1))      # (L, B, D)
        cls_token = transformed[0]                                      # Use first token as CLS
        return self.classifier(cls_token)
