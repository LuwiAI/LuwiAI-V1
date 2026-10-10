import torch
from luwiai.model import LuwiConfig, LuwiLM, decode, encode


def test_byte_tokenizer_round_trip():
    text = "LuwiAI: olá 🌍"
    assert decode(encode(text)) == text


def test_model_forward_backward_and_generation():
    torch.manual_seed(1)
    model = LuwiLM(LuwiConfig(d_model=32, n_heads=4, n_layers=1, max_seq_len=16))
    x = torch.randint(0, 256, (2, 8))
    logits, loss = model(x, x)
    assert logits.shape == (2, 8, 256)
    assert loss is not None and torch.isfinite(loss)
    loss.backward()
    generated = model.generate(x[:1, :3], max_new_tokens=2, temperature=0)
    assert generated.shape == (1, 5)
