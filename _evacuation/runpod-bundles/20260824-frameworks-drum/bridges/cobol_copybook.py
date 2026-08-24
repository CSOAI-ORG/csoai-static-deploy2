#!/usr/bin/env python3
"""COBOL COPYBOOK → JSON parser — the "proof of weave" (doctrine-clean).

Reads a COBOL COPYBOOK (an 01-level record with PIC field definitions) and parses fixed-width
COBOL records into JSON. This is the *wrap-not-replace* proof: legacy COBOL batch data becomes
machine-readable without migrating or touching the mainframe. It is a parser and nothing more —
no money, no token, no settlement. Doctrine: [BUILT] parser; the settlement/bridge layers built
on top are Phase 2 (crypto, compliance-gated).

PIC handling (COBOL DISPLAY, the standard that dominates legacy batch):
  X / X(n)   alphanumeric — left-justified, space-padded, width n
  9(n)       unsigned integer — n digit bytes (leading zeros)
  9(n)Vmm    unsigned w/ implied decimal — (n+mm) digit bytes, no 'V' in the record
  S9(n)Vmm   signed w/ implied decimal — same byte count as unsigned (the sign is packed
             into the last byte's zone; this parser detects a trailing '-' or overpunch
             {D}=neg/}+pos conservatively, and NEVER assumes zoned/SWIFT)

Stdlib-only. Run: python3 bridges/cobol_copybook.py --selftest
"""
import json
import re
import sys

FIELD_RE = re.compile(
    r"^\s*(?P<level>\d{2})\s+(?P<name>[A-Z0-9][A-Z0-9_-]*)\s+PIC\s+(?P<pic>[SX9V()0-9]+)\.?", re.IGNORECASE)


def classify_pic(pic):
    """Return {pic_type, width, decimals, signed} for a PIC clause."""
    pic = pic.upper().replace(" ", "")
    base = pic.replace("S", "", 1)          # strip a leading sign indicator
    signed = base != pic
    # split integer / fractional on the implied-decimal marker V
    if "V" in base:
        int_part, frac_part = base.split("V", 1)
    else:
        int_part, frac_part = base, ""
    int_digits = digits_of(int_part)
    frac_digits = digits_of(frac_part)
    width = int_digits + frac_digits
    if width == 0:
        xm = re.match(r"^X(?:\((\d+)\))?$", base)
        w = int(xm.group(1)) if xm and xm.group(1) else 1
        return {"pic_type": "ALPHA", "width": w, "decimals": 0, "signed": False}
    return {"pic_type": "NUMERIC", "width": width, "decimals": frac_digits, "signed": signed}


def parse_copybook(copybook_text):
    """Parse a COPYBOOK into field defs (order preserved)."""
    fields = []
    for line in copybook_text.splitlines():
        m = FIELD_RE.match(line)
        if not m:
            continue
        pic = m.group("pic")
        fields.append({"name": m.group("name").upper(), "pic": pic.upper(), **classify_pic(pic)})
    return fields


def digits_of(part):
    """Count the digit positions in a PIC fragment like '9(5)' or '99'."""
    if not part or not part.startswith("9"):
        return 0
    m = re.match(r"^9\((\d+)\)$", part)
    if m:
        return int(m.group(1))
    return len(re.sub(r"[^9]", "", part))


def offset_layout(fields):
    """Assign a byte offset to each field (fixed-width, concatenated). Return (fields, total)."""
    off = 0
    for f in fields:
        f["offset"] = off
        off += f["width"]
    return fields, off


def parse_record(record_bytes, fields):
    """Parse a fixed-width COBOL record into a dict using the field layout."""
    if isinstance(record_bytes, str):
        record_bytes = record_bytes.encode("latin-1")
    out = {}
    for f in fields:
        chunk = record_bytes[f["offset"]: f["offset"] + f["width"]]
        raw = chunk.decode("latin-1")
        out[f["name"]] = (raw.strip() if f["pic_type"] == "ALPHA" else numeric_value(raw, f))
    return out


def numeric_value(raw, f):
    """Convert a fixed-width COBOL numeric field (digit bytes) to a python number."""
    neg = False
    if f.get("signed") and raw:
        last = raw[-1]
        if last in "-D}":        # trailing minus / overpunch D} == negative
            neg = True
    digits = re.sub(r"[^0-9]", "", raw)
    if digits == "":
        return None
    val = int(digits) / (10 ** f.get("decimals", 0))
    return -val if neg else val


SAMPLE_BOOK = """       01  CUSTOMER-RECORD.
           05  CUSTOMER-ID       PIC X(10).
           05  CUSTOMER-NAME     PIC X(16).
           05  BALANCE           PIC 9(5)V99.
           05  STATUS            PIC X(1).
"""
# layout: 10 + 16 + 7 + 1 = 34 bytes
SAMPLE_RECORD = "CUST000123" + "ACME CORPORATION" + "1234567" + "A"


def main():
    if "--selftest" in sys.argv:
        fields = offset_layout(parse_copybook(SAMPLE_BOOK))[0]
        total = sum(f["width"] for f in fields)
        assert total == 34, f"layout width {total} != 34"
        rec = parse_record(SAMPLE_RECORD, fields)
        assert rec["CUSTOMER-ID"] == "CUST000123", rec
        assert rec["CUSTOMER-NAME"] == "ACME CORPORATION", rec
        # 9(5)V99 = 7 digit bytes, implied decimal after the 5th -> 1234567 / 100
        assert rec["BALANCE"] == 12345.67, rec
        assert rec["STATUS"] == "A", rec
        print(f"COBOL COPYBOOK parser: PASS (layout {total} bytes, {len(fields)} fields)")
        print(json.dumps(rec, indent=1))
        return 0
    print("usage: python3 bridges/cobol_copybook.py --selftest")
    return 1


if __name__ == "__main__":
    sys.exit(main())
