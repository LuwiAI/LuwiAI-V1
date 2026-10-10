"""Generate original, reproducible toy instructions from authored rules.

This generator uses no downloaded corpora or third-party prompt/answer data.
Synthetic examples are useful for pipeline tests, not a replacement for broad
human-authored training data or evidence of general intelligence.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path


def examples(count: int, seed: int):
    rng = random.Random(seed)
    for i in range(count):
        kind = i % 9
        if kind == 0:
            a, b = rng.randint(-999, 999), rng.randint(-999, 999)
            prompt, answer = f"Compute {a} + {b}.", str(a + b)
        elif kind == 1:
            a, b = rng.randint(-999, 999), rng.randint(-999, 999)
            prompt, answer = f"Compute {a} - {b}.", str(a - b)
        elif kind == 2:
            a, b = rng.randint(-30, 30), rng.randint(-30, 30)
            prompt, answer = f"Compute {a} * {b}.", str(a * b)
        elif kind == 3:
            n = rng.randint(1, 20)
            prompt, answer = f"List the integers from 1 through {n} in ascending order, separated by commas.", ", ".join(map(str, range(1, n + 1)))
        elif kind == 4:
            word = "".join(rng.choice("abcdefg") for _ in range(rng.randint(3, 10)))
            prompt, answer = f"Reverse this string exactly: {word}", word[::-1]
        elif kind == 5:
            word = "".join(rng.choice("abcdefg") for _ in range(rng.randint(3, 10)))
            prompt, answer = f"Count the characters in this string: {word}", str(len(word))
        elif kind == 6:
            values = [rng.randint(-100, 100) for _ in range(4)]
            prompt, answer = f"Sort these integers from smallest to largest: {', '.join(map(str, values))}.", ", ".join(map(str, sorted(values)))
        elif kind == 7:
            x, y = rng.randint(-100, 100), rng.randint(-100, 100)
            prompt = f"Which integer is larger, {x} or {y}?"
            answer = str(max(x, y))
        else:
            word = "".join(rng.choice("abcdefghijklm") for _ in range(rng.randint(3, 10)))
            prompt, answer = f"Convert this string to uppercase: {word}", word.upper()
        text = f"User: {prompt}\nAssistant: {answer}"
        yield {
            "id": hashlib.sha256(f"{seed}:{i}:{text}".encode()).hexdigest()[:16],
            "text": text,
            "provenance": {
                "source_type": "project_synthetic",
                "creation_method": "luwiai.data.generate.examples; deterministic procedural templates authored in this repository",
                "rights_basis": "project_authored",
                "review_status": "reviewed",
                "split": "validation" if i % 10 == 0 else "train",
                "generator_seed": seed,
                "generator_index": i,
            },
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--count", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")
    args.out.mkdir(parents=True, exist_ok=True)
    rows = list(examples(args.count, args.seed))
    file_hashes = {}
    for split in ("train", "validation"):
        path = args.out / f"{split}.jsonl"
        selected = [r for r in rows if r["provenance"]["split"] == split]
        payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in selected)
        path.write_text(payload, encoding="utf-8")
        file_hashes[path.name] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        print(f"{path}: {len(selected)} records")
    manifest = {"generator": "luwiai.data.generate.examples", "seed": args.seed,
                "count": args.count, "files": file_hashes,
                "note": "Procedural project-authored examples; not a broad knowledge corpus."}
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
