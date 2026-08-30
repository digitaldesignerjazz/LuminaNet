#!/usr/bin/env python3
"""Validate LuminaNet schema examples.

Exit 0 only if every file in schema/examples/valid passes and every file
in schema/examples/invalid fails. Form, not trust.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    sys.stderr.write(
        "jsonschema fehlt.\n"
        "  sudo apt install python3-jsonschema\n"
        "  oder: python3 -m pip install -r tools/requirements.txt\n"
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
EX_DIR = SCHEMA_DIR / "examples"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validator(name: str) -> Draft202012Validator:
    schema = load(SCHEMA_DIR / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


ENV = validator("envelope.schema.json")
SCENE = validator("scene.schema.json")
AGENT = validator("agent-message.schema.json")

AGENT_TOPICS = {
    "agent.hello",
    "agent.caps",
    "agent.ask",
    "agent.say",
    "agent.handoff",
    "agent.nack",
}


def topic_of(doc: dict) -> str | None:
    to = doc.get("to") if isinstance(doc, dict) else None
    if isinstance(to, dict):
        topic = to.get("topic")
        if isinstance(topic, str):
            return topic
    frm = doc.get("from") if isinstance(doc, dict) else None
    if isinstance(frm, dict):
        topic = frm.get("topic")
        if isinstance(topic, str):
            return topic
    return None


def looks_like_envelope(doc: dict) -> bool:
    return isinstance(doc, dict) and "v" in doc and "from" in doc and "to" in doc


def looks_like_scene(doc: dict) -> bool:
    return isinstance(doc, dict) and "scene_id" in doc and "channels" in doc and "v" not in doc


def check_document(doc: dict) -> None:
    if looks_like_envelope(doc):
        ENV.validate(doc)
        topic = topic_of(doc)
        body = doc.get("body", {})
        if topic == "scene.set":
            SCENE.validate(body)
        elif topic in AGENT_TOPICS and topic != "agent.caps":
            AGENT.validate(body)
        return
    if looks_like_scene(doc):
        SCENE.validate(doc)
        return
    raise ValidationError("unbekanntes Dokumentformat")


def run_dir(path: Path, must_pass: bool) -> list[str]:
    errors: list[str] = []
    files = sorted(p for p in path.glob("*.json") if p.is_file())
    if not files:
        errors.append(f"keine JSON-Dateien in {path.relative_to(ROOT)}")
        return errors
    for file in files:
        rel = file.relative_to(ROOT)
        try:
            doc = load(file)
            check_document(doc)
        except (ValidationError, json.JSONDecodeError) as exc:
            if must_pass:
                errors.append(f"VALID sollte gelten, gilt nicht: {rel}\n  {exc}")
            else:
                print(f"ok  invalid bricht wie erwartet: {rel}")
        else:
            if must_pass:
                print(f"ok  valid: {rel}")
            else:
                errors.append(f"INVALID sollte scheitern, gilt aber: {rel}")
    return errors


def main() -> int:
    valid = EX_DIR / "valid"
    invalid = EX_DIR / "invalid"
    if not valid.is_dir() or not invalid.is_dir():
        print("examples/valid oder examples/invalid fehlt", file=sys.stderr)
        return 2
    errors = run_dir(valid, must_pass=True) + run_dir(invalid, must_pass=False)
    if errors:
        print("\nKante gebrochen:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("\nKante hält. Form geprüft, Vertrauen nicht.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
