# lightzoo/models/modules/attention.py

import torch
import torch.nn as nn

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super(MultiHeadSelfAttention, self).__init__()
        assert embed_dim % num_heads == 0, "Embedding dimension must be divisible by number of heads"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.qkv_proj = nn.Linear(embed_dim, embed_dim * 3)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

        self.scale = self.head_dim ** -0.5

    def forward(self, x):
        B, L, D = x.size()
        qkv = self.qkv_proj(x).reshape(B, L, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]  # Each: (B, num_heads, L, head_dim)

        attn_scores = (q @ k.transpose(-2, -1)) * self.scale  # (B, num_heads, L, L)
        attn_probs = attn_scores.softmax(dim=-1)

        out = (attn_probs @ v).transpose(1, 2).reshape(B, L, D)  # (B, L, D)
        return self.out_proj(out)
