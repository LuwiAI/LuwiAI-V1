"""Small decoder-only Transformer; byte IDs avoid external tokenizer data."""
import torch
from torch import nn

VOCAB_SIZE = 256


def encode(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def decode(tokens) -> str:
    return bytes(int(t) for t in tokens).decode("utf-8", errors="replace")


class LuwiConfig:
    def __init__(self, vocab_size=VOCAB_SIZE, d_model=128, n_heads=4, n_layers=4, max_seq_len=512, dropout=0.0):
        if d_model % n_heads: raise ValueError("d_model must be divisible by n_heads")
        self.vocab_size, self.d_model, self.n_heads = vocab_size, d_model, n_heads
        self.n_layers, self.max_seq_len, self.dropout = n_layers, max_seq_len, dropout

    def to_dict(self):
        return vars(self).copy()


class LuwiLM(nn.Module):
    def __init__(self, config=LuwiConfig()):
        super().__init__()
        self.config = config
        self.token = nn.Embedding(config.vocab_size, config.d_model)
        self.position = nn.Embedding(config.max_seq_len, config.d_model)
        layer = nn.TransformerEncoderLayer(d_model=config.d_model, nhead=config.n_heads,
            dim_feedforward=4 * config.d_model, dropout=config.dropout, batch_first=True, norm_first=True, activation="gelu")
        self.blocks = nn.TransformerEncoder(layer, num_layers=config.n_layers, enable_nested_tensor=False)
        self.norm = nn.LayerNorm(config.d_model)
        self.head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        self.head.weight = self.token.weight

    def forward(self, input_ids, targets=None):
        batch, length = input_ids.shape
        if length > self.config.max_seq_len: raise ValueError("sequence exceeds max_seq_len")
        pos = torch.arange(length, device=input_ids.device)
        x = self.token(input_ids) + self.position(pos)[None, :, :]
        causal_mask = torch.triu(torch.ones(length, length, device=input_ids.device, dtype=torch.bool), diagonal=1)
        logits = self.head(self.norm(self.blocks(x, mask=causal_mask)))
        loss = None
        if targets is not None:
            loss = nn.functional.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1), ignore_index=-100)
        return logits, loss

    @torch.no_grad()
    def generate(self, input_ids, max_new_tokens=64, temperature=0.8):
        self.eval()
        for _ in range(max_new_tokens):
            context = input_ids[:, -self.config.max_seq_len:]
            logits, _ = self(context)
            next_logits = logits[:, -1, :] / max(temperature, 1e-5)
            next_token = torch.multinomial(torch.softmax(next_logits, dim=-1), num_samples=1)
            input_ids = torch.cat((input_ids, next_token), dim=1)
        return input_ids
