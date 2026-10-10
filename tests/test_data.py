import json
from luwiai.data.generate import examples
from luwiai.data.validate import validate

def test_generated_examples_are_reproducible_and_valid(tmp_path):
    rows=list(examples(20,13)); assert rows==list(examples(20,13))
    path=tmp_path/"data.jsonl"; path.write_text("".join(json.dumps(x)+"\n" for x in rows))
    count,errors=validate(path); assert count==20 and errors==[]

def test_validator_rejects_missing_rights(tmp_path):
    path=tmp_path/"bad.jsonl"; path.write_text(json.dumps({"id":"x","text":"hello","provenance":{"source_type":"project_synthetic"}})+"\n")
    assert validate(path)[1]
