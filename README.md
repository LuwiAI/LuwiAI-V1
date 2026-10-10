# LuwiAI-V1

LuwiAI-V1 is an open research project for building a language model from project-created material. This repository now contains a **real, randomly initialized decoder-only Transformer**, local data generation, PyTorch training, held-out loss measurement, checkpoints, and inference. It remains a small experimental model—not a frontier assistant.

## Honest status

- Model code is trained from random initialization; no pretrained weights or third-party corpus are downloaded.
- Procedural examples are authored in this repository and generated locally. They cover a narrow set of arithmetic and string transformations. This is not broad natural-language knowledge, and synthetic data is not a guarantee against resemblance to protected material.
- The default local run creates a sub-million-parameter model trained on a small toy corpus. That is enough to demonstrate the training lifecycle, **not** to compete with state-of-the-art LLMs.
- No ARC-AGI-3, SWE-Bench, MMLU-Pro, or other benchmark score has been measured. The project makes no 100%, “first,” or “best” claim. See [BENCHMARKS.md](BENCHMARKS.md).
- A minimal allowlisted calculator tool runtime exists for agent experiments, but there is **no autonomous planning/tool-use loop or tool-use-trained checkpoint**. Image/audio/video training is not implemented.

Meaningful general-purpose performance requires orders of magnitude more curated, licensed data, compute, iterations, evaluation, and safety work than this sandbox can provide. Claims must be tied to a reproducible, independently checked evaluation.

The trained research artifact and its measured limitations are documented in [MODEL_CARD.md](MODEL_CARD.md). The code and checkpoint are offered under [Apache-2.0](LICENSE); this does not imply independent review or a guarantee about future generated outputs.

## Run locally

Python 3.10+ and PyTorch 2.2+; CPU is supported. The configuration below is for a modest local research run, not frontier pretraining:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
python -m luwiai.data.generate --out data/generated --count 4096 --seed 7
python -m luwiai.data.validate data/generated/train.jsonl
python -m luwiai.data.validate data/generated/validation.jsonl
python -m luwiai.train \
  --config configs/local_cpu.json \
  --data data/generated/train.jsonl \
  --validation data/generated/validation.jsonl \
  --out runs/local_cpu
python -m luwiai.evaluate --checkpoint runs/local_cpu/checkpoint.pt \
  --data data/generated/validation.jsonl --limit 100
python -m luwiai.chat --checkpoint runs/local_cpu/checkpoint.pt --prompt 'User: Compute 7 + 8.\nAssistant:'
pytest
```

Training supervises assistant answer bytes with complete prompts, prints training and held-out answer loss, and periodically saves a resumable checkpoint. The evaluator reports exact match on this project's own synthetic task split only; it is **not** an external benchmark. Loss and exact match are not evidence of broad knowledge or agent competence. Generated corpora and new training runs are git-ignored; the documented `runs/local_cpu_v2/checkpoint.pt` is the specific reviewed checkpoint release.

`luwiai.agent.ToolRuntime` currently exposes only a bounded integer calculator, using an AST allowlist (no `eval`, shell, or arbitrary Python). It is a guarded building block, not an autonomous agent or a security boundary for deployment.

## Data governance

Every sample includes source/creation metadata, a rights basis, review status, and split. The validator rejects unapproved sources and missing provenance. Before adding any outside text, code, image, video, or audio, review its license/permission and collection terms, record source/version, filter sensitive data, deduplicate, and document removal handling. See [DATA_POLICY.md](DATA_POLICY.md). This is engineering guidance, not legal advice or a guarantee of non-infringement.
