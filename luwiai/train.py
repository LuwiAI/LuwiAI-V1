"""Train LuwiAI-V1 from random initialization on reviewed JSONL data.

The current task generator emits one User/Assistant exchange per record. The
trainer preserves each complete prompt and computes loss on assistant answers,
not on the predictable user prompt text. This remains a narrow research model.
"""
import argparse
import json
import random
from pathlib import Path

import torch

from .model import LuwiConfig, LuwiLM, encode


def load_examples(path: Path, block_size: int):
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    result = []
    for row in rows:
        text = row.get("text")
        if not isinstance(text, str) or "\nAssistant:" not in text:
            continue
        prefix, answer = text.split("\nAssistant:", 1)
        prefix += "\nAssistant:"
        tokens = encode(text + "\n")
        answer_start = len(encode(prefix))
        if len(tokens) - 1 > block_size:
            raise ValueError(f"example {row.get('id')} exceeds max_seq_len; increase model context")
        if answer_start >= len(tokens) - 1:
            continue
        result.append((tokens, answer_start))
    if not result:
        raise ValueError(f"no usable User/Assistant records found in {path}")
    return result


def sample_batch(examples, batch_size, block_size, device, rng):
    xs, ys = [], []
    for tokens, answer_start in rng.choices(examples, k=batch_size):
        x = tokens[:-1]
        y = tokens[1:]
        # y[j] is the token at original position j+1. Only score answer bytes.
        mask_before = max(0, answer_start - 1)
        y = [-100] * mask_before + y[mask_before:]
        pad = block_size - len(x)
        xs.append(x + [0] * pad)
        ys.append(y + [-100] * pad)
    return (torch.tensor(xs, dtype=torch.long, device=device),
            torch.tensor(ys, dtype=torch.long, device=device))


@torch.no_grad()
def estimate_loss(model, examples, batch_size, block_size, device, rng, batches=32):
    model.eval()
    losses = []
    for _ in range(batches):
        x, y = sample_batch(examples, batch_size, block_size, device, rng)
        _, loss = model(x, y)
        losses.append(float(loss.item()))
    model.train()
    return sum(losses) / len(losses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True, help="training JSONL")
    parser.add_argument("--validation", type=Path, help="optional held-out JSONL")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--resume", type=Path, help="checkpoint to resume")
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    seed = int(cfg.get("seed", 7))
    torch.manual_seed(seed)
    rng = random.Random(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    config = LuwiConfig(**cfg["model"])
    model = LuwiLM(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(cfg.get("learning_rate", 3e-4)),
                                  weight_decay=float(cfg.get("weight_decay", 0.1)))
    start_step = 0
    if args.resume:
        state = torch.load(args.resume, map_location=device, weights_only=False)
        model.load_state_dict(state["model"])
        if "optimizer" in state:
            optimizer.load_state_dict(state["optimizer"])
        start_step = int(state.get("step", 0))

    train_data = load_examples(args.data, config.max_seq_len)
    validation_data = load_examples(args.validation, config.max_seq_len) if args.validation else None
    batch_size = int(cfg.get("batch_size", 8))
    block_size = config.max_seq_len
    steps = int(cfg.get("steps", 100))
    log_every = max(1, int(cfg.get("log_every", 25)))
    model.train()
    for step in range(start_step, start_step + steps):
        x, y = sample_batch(train_data, batch_size, block_size, device, rng)
        optimizer.zero_grad(set_to_none=True)
        _, loss = model(x, y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg.get("grad_clip", 1.0)))
        optimizer.step()
        if (step + 1) % log_every == 0 or step == start_step + steps - 1:
            line = f"step={step + 1} train_answer_loss={loss.item():.4f}"
            if validation_data:
                val_loss = estimate_loss(model, validation_data, batch_size, block_size,
                                         device, rng, int(cfg.get("eval_batches", 32)))
                line += f" validation_answer_loss={val_loss:.4f}"
            print(line, flush=True)
            args.out.mkdir(parents=True, exist_ok=True)
            torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                        "config": model.config.to_dict(), "step": step + 1,
                        "seed": seed, "training_data": str(args.data),
                        "objective": "assistant answer bytes only"}, args.out / "checkpoint.pt")

    print(f"Saved randomly initialized and locally trained research checkpoint: {args.out / 'checkpoint.pt'} ({device})")
    print("This checkpoint is not benchmark validated and is not evidence of general-purpose competence.")


if __name__ == "__main__":
    main()
