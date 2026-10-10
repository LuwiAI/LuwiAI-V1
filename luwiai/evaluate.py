"""Evaluate exact text answers on LuwiAI's own synthetic held-out split.

This is a task-specific diagnostic only. It is not ARC-AGI-3, SWE-Bench,
MMLU-Pro, or any externally recognized benchmark.
"""
import argparse
import json
import random
from pathlib import Path

import torch

from .model import LuwiConfig, LuwiLM, decode, encode


def evaluate(checkpoint: Path, data: Path, limit: int | None = None, seed: int = 17):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    saved = torch.load(checkpoint, map_location=device, weights_only=False)
    model = LuwiLM(LuwiConfig(**saved["config"])).to(device)
    model.load_state_dict(saved["model"])
    model.eval()
    rows = [json.loads(line) for line in data.read_text(encoding="utf-8").splitlines() if line.strip()]
    rng = random.Random(seed)
    if limit is not None and limit < len(rows):
        rows = rng.sample(rows, limit)
    correct, samples = 0, []
    for row in rows:
        if "\nAssistant:" not in row.get("text", ""):
            continue
        prefix, expected = row["text"].split("\nAssistant:", 1)
        prompt = prefix + "\nAssistant:"
        input_ids = torch.tensor([encode(prompt)], dtype=torch.long, device=device)
        if input_ids.shape[1] > model.config.max_seq_len:
            continue
        with torch.no_grad():
            output = model.generate(input_ids, max_new_tokens=min(96, model.config.max_seq_len - input_ids.shape[1]), temperature=0)
        prediction = decode(output[0, input_ids.shape[1]:].tolist()).split("\n", 1)[0].strip()
        target = expected.strip()
        matched = prediction == target
        correct += int(matched)
        if len(samples) < 10:
            samples.append({"prompt": prefix.removeprefix("User: "), "expected": target,
                            "predicted": prediction, "exact_match": matched})
    total = len(rows)
    return {"evaluation": "luwiai_generated_validation_exact_match",
            "is_external_benchmark": False, "checkpoint": str(checkpoint),
            "examples": total, "exact_matches": correct,
            "exact_match_rate": correct / total if total else None,
            "seed": seed, "samples": samples,
            "warning": "Synthetic narrow-task diagnostic only; not evidence of general LLM or benchmark competence."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--out", type=Path, help="optional JSON report path")
    args = p.parse_args()
    result = evaluate(args.checkpoint, args.data, args.limit, args.seed)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
