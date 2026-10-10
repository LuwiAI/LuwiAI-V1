"""Run autoregressive inference with a locally trained checkpoint."""
import argparse
from pathlib import Path
import torch
from .model import LuwiConfig, LuwiLM, decode, encode


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--new-tokens", type=int, default=160)
    p.add_argument("--temperature", type=float, default=0.8)
    a = p.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    saved = torch.load(a.checkpoint, map_location=device, weights_only=False)
    config = LuwiConfig(**saved["config"])
    model = LuwiLM(config).to(device)
    model.load_state_dict(saved["model"])
    model.eval()
    prompt = torch.tensor([encode(a.prompt)], dtype=torch.long, device=device)
    result = model.generate(prompt, max_new_tokens=a.new_tokens, temperature=a.temperature)
    print(decode(result[0].tolist()))

if __name__ == "__main__":
    main()
