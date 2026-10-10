# Evaluation and benchmark integrity

LuwiAI-V1 has **no verified ARC-AGI-3, SWE-Bench, MMLU-Pro, or other benchmark results**. This repository must not be marketed as achieving 100%, first, or state of the art without reproducible independent evidence.

## Protocol for any reported score

1. Identify the exact public benchmark release, split, task subset, evaluator commit/version, and license/terms.
2. Preserve a clean training/evaluation boundary. Do not train on hidden test data, evaluator answers, or benchmark-specific leakage. Track overlap checks and exclusions.
3. Pin checkpoint SHA-256, tokenizer/config, source commit, data manifest hashes, dependency versions, hardware, decoding settings, tool permissions, and random seeds.
4. Run the official evaluator where permitted; retain raw logs and report failures, timeouts, cost, sample count, and uncertainty. Do not substitute a hand-written proxy while presenting it as an official result.
5. Have an independent reviewer reproduce the run before making a public claim.
6. Report exact scores and protocol, including less-than-perfect results. Never turn a tiny smoke test into a benchmark result.

ARC-style reasoning, software engineering, and broad knowledge are distinct capabilities. High performance on one does not establish performance on another. “All benchmarks” is not a defined finite target.

This repository currently supplies no benchmark adapters and intentionally records no scores. Add adapters only after reviewing each benchmark's current rules and evaluator.
