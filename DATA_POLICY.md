# Data governance and provenance policy

## Default rule

The project does not ingest third-party datasets by default. Training examples currently come only from the project's procedural generator, whose templates and algorithms are authored in-repository. No public benchmark question/answer data is used for training.

## Required manifest fields

Each JSONL record must include `id`, `text`, and `provenance` with:

- `source_type`: `project_synthetic`, `project_authored`, or an explicitly approved source category.
- `creation_method`: reproducible description of how the sample was created.
- `rights_basis`: `project_authored` for original project material, or a recorded license/permission identifier for future material.
- `review_status`: `reviewed` or `pending`.
- `split`: `train`, `validation`, or `test`.

The current validator accepts only project-authored/project-synthetic data with `review_status=reviewed`, and refuses benchmark-labeled material. Do not label a third-party-derived or unreviewed sample as synthetic to bypass this rule.

## Future data additions

Before adding any external text, code, image, video, or audio source: record the exact source and version, rights basis and terms, collection date, transformations, attribution obligations, and removal contact/process. Obtain the necessary rights, filter sensitive personal data and malware/secrets, deduplicate, document provenance, and get legal review where appropriate. Respect robots/access terms and applicable privacy law. “Publicly accessible” does not mean public domain or permission to train.

For generated data, preserve generator version and seed; screen for memorized/reproduced content, personally identifying information, unsafe instructions, and quality failures. Synthetic data can still infringe or reproduce protected material. Keep raw sources, derived data, validation sets, and benchmark sets separated and access-controlled.

This policy is an engineering baseline, not legal advice or a guarantee that a model/output is non-infringing or safe.
