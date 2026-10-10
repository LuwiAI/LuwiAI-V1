"""Validate provenance and content shape of a generated JSONL dataset."""
import argparse
import json
from pathlib import Path

ALLOWED_SOURCE = {"project_synthetic", "project_authored"}
REQUIRED_PROVENANCE = {"source_type", "creation_method", "rights_basis", "review_status", "split"}


def validate(path: Path):
    errors, seen, count = [], set(), 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON ({exc})"); continue
        p = row.get("provenance", {})
        missing = REQUIRED_PROVENANCE - p.keys()
        if missing: errors.append(f"line {line_no}: missing provenance {sorted(missing)}")
        if not isinstance(row.get("text"), str) or not row.get("text", "").strip(): errors.append(f"line {line_no}: text must be non-empty")
        if not row.get("id"): errors.append(f"line {line_no}: missing id")
        if row.get("id") in seen: errors.append(f"line {line_no}: duplicate id {row.get('id')}")
        seen.add(row.get("id"))
        if p.get("source_type") not in ALLOWED_SOURCE: errors.append(f"line {line_no}: unapproved source_type")
        if p.get("rights_basis") != "project_authored": errors.append(f"line {line_no}: rights basis requires explicit review")
        if p.get("review_status") != "reviewed": errors.append(f"line {line_no}: sample is not reviewed")
        if p.get("split") not in {"train", "validation", "test"}: errors.append(f"line {line_no}: invalid split")
        if "benchmark" in json.dumps(row).lower(): errors.append(f"line {line_no}: benchmark-associated data is disallowed")
        count += 1
    return count, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    count, errors = validate(args.path)
    if errors:
        print("INVALID:"); print("\n".join(errors)); raise SystemExit(1)
    print(f"Valid: {count} records; provenance fields present. This is not a legal opinion.")

if __name__ == "__main__":
    main()
