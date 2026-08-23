"""
parsers/copybook_schema.py — COBOL COPYBOOK -> JSON schema (Open 1, atomic unit).

The Rosetta stone reads a COBOL COPYBOOK (a batch record layout) and emits a
JSON schema the A2A agent layer can reason over. This is the "water-pipe" step:
the overnight batch instruction becomes a routable, verifiable object.

Measurement, not certification. Deterministic, offline, no LLM in the parse.
"""

import re

# A minimal COPYBOOK field:  10  SETTLE-DATE      PIC X(8)  and  20  AMOUNT  PIC 9(12)V99.
FIELD_RE = re.compile(
    r"^\s*(\d+)\s+([A-Z0-9][A-Z0-9-]*)\s+PIC\s+([A-Z0-9()V]+)\s*\.?\s*$"
)


def parse_copybook(text):
    """Parse a COBOL COPYBOOK into an ordered list of field dicts."""
    fields = []
    for line in text.splitlines():
        m = FIELD_RE.match(line)
        if not m:
            continue
        level, name, pic = int(m.group(1)), m.group(2), m.group(3)
        fields.append(_field(level, name, pic))
    return fields


def _field(level, name, pic):
    """Infer a JSON type + width from a PIC clause."""
    numeric = "9" in pic
    is_signed = pic.startswith("S")
    digits = sum(int(d) for d in re.findall(r"\d+", pic))
    return {
        "field": name,
        "level": level,
        "pic": pic,
        "type": "number" if numeric else "string",
        "nullable": level > 0,
        "width": digits if digits else None,
        "signed": is_signed,
        "cobol_field": name,
    }


def to_json_schema(fields):
    """Render the parsed fields as a JSON-schema object (the A2A contract)."""
    props = {}
    required = []
    for f in fields:
        props[f["field"]] = {"type": f["type"], "description": f"PIC {f['pic']}"}
        if not f["nullable"]:
            required.append(f["field"])
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "COPYBOOK-batch",
        "type": "object",
        "properties": props,
        "required": required,
    }


if __name__ == "__main__":
    sample = """\
       01 SETTLEMENT-RECORD.
          10 SETTLE-DATE       PIC X(8).
          10 CURRENCY          PIC X(3).
          10 NOTIONAL          PIC 9(12)V99.
          10 COUNTERPARTY      PIC X(24).
          10 STATUS            PIC X(8)."""
    fields = parse_copybook(sample)
    print(f"parsed {len(fields)} fields")
    for f in fields:
        print(" ", f["field"], f["type"], f["pic"])
    print(to_json_schema(fields))
