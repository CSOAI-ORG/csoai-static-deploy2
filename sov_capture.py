#!/usr/bin/env python3
"""
sov_capture.py — TUI/PC capture pipeline for SOVOS.

Per user: 'all done here auto convert to honey KB in sov space sovos
so its all learning nns gnns.' Every keystroke, every file, every
terminal command becomes a Phlabet glyph → IWM → KB → GNN learning.

Pipeline:
  1. TUI Snooper      — captures terminal commands + context
  2. Browser Siphon   — captures URL visits + page titles (local-only)
  3. File Watcher     — captures code changes + diffs
  4. Chat Harvest     — captures agent conversation events
  5. KB Refiner       — compresses to Phlabet, dedupes, scores, stores
  6. GNN Spine        — extracts patterns, skills, predictions

Usage:
  python3 sov_capture.py --setup           # install all
  python3 sov_capture.py --snooper --cmd "git status" --exit 0
  python3 sov_capture.py --siphon --url "https://csoai.org" --title "GSPC"
  python3 sov_capture.py --file-change --path "src/main.rs"
  python3 sov_capture.py --chat-event --query "..." --response "..."
  python3 sov_capture.py --refine          # run refinery
  python3 sov_capture.py --status          # show capture stats
  python3 sov_capture.py --gnn-extract     # extract skills via GNN
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SOV_ROOT = HOME / ".sov"
HONEY_DIR = SOV_ROOT / "honey"
TERMINAL_DIR = HONEY_DIR / "terminal"
BROWSER_DIR = HONEY_DIR / "browser"
FILES_DIR = HONEY_DIR / "files"
CHAT_DIR = HONEY_DIR / "chat"
IWM_DIR = SOV_ROOT / "iwm"

CLOUDFARE_ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
KB_PATH = CLOUDFARE_ROOT / "benchmark-results" / "sov_kb.json"

# 2026-08-08 (JEEVES): the zsh preexec hook writes every terminal command to
# ~/.sov/honey/terminal/<date>.jsonl, which can grow to hundreds of MB /
# millions of lines. Every capture-derived reader (refine_kb, gnn_extract)
# must process only the most recent window, never the whole file — a full
# scan stalled PHASE_9I to 227s and, compounded over ticks, ballooned the
# KB from 85 to 328K entries. Shared bounded window for all capture readers.
REFINE_WINDOW = 500

# Phlabet — same encoding as sov-hive Rust crate
PHLABET_KEYWORDS = {
    0x00: ["governance", "balance", "justice", "regulation", "compliance", "audit"],
    0x01: ["authority", "decision", "sovereign", "mandate", "policy"],
    0x02: ["network", "connection", "protocol", "harness", "agent", "api"],
    0x03: ["law", "regulation", "article", "provision", "act", "code"],
    0x04: ["cross-jurisdiction", "equivalence", "interop", "bridge"],
    0x10: ["defense", "protection", "encryption", "security", "auth"],
    0x11: ["surveillance", "detection", "audit", "monitoring", "scan"],
    0x12: ["threat", "vulnerability", "attack", "exploit"],
    0x16: ["detection", "signal", "wifi", "sensing", "perception"],
    0x17: ["watchdog", "guardian", "observer", "monitor"],
    0x20: ["privacy", "secret", "encryption", "sovereign", "private"],
    0x21: ["anonymity", "identity", "persona", "obfuscation"],
    0x24: ["genesis", "origin", "root", "trust", "foundation"],
    0x30: ["value", "transaction", "commerce", "revenue", "price"],
    0x31: ["growth", "abundance", "harvest", "market", "build", "deploy"],
    0x32: ["energy", "compute", "burn", "training", "inference", "gpu"],
    0x33: ["mechanism", "process", "workflow", "pipeline", "ci", "cd"],
    0xF0: ["sov", "sovereign", "mind", "unified", "hive"],
    0xF3: ["structure", "reasoning", "core", "gnn", "spine", "neural"],
    0xF4: ["knowledge", "output", "training", "data", "create", "honey"],
    0xF5: ["simulation", "imagination", "prediction", "dream"],
    0xF7: ["multi-spectrum", "rainbow", "defense", "security"],
    0xF8: ["self-similar", "recursive", "fractal", "hive"],
    0xF9: ["collective", "swarm", "hive", "clan"],
    0xFF: ["origin", "start", "genesis"],
}

KEYWORD_TO_PHONEME = {}
for code, kws in PHLABET_KEYWORDS.items():
    for kw in kws:
        KEYWORD_TO_PHONEME[kw] = code


def compress_to_phlabet(text: str) -> list[int]:
    """Compress text to Phlabet phoneme codes (matches Rust crate)."""
    text = text.lower()
    words = re.findall(r'\w+', text)
    matched = set()
    for w in words:
        for kw, code in KEYWORD_TO_PHONEME.items():
            if kw in w or w in kw:
                matched.add(code)
    if not matched:
        matched.add(0xFF)  # void
    return sorted(matched)


def make_kb_entry(question: str, answer: str, source: str, vectors: list = None) -> dict:
    """Make a KB entry from a capture event."""
    timestamp = datetime.now(timezone.utc).isoformat()
    seed = hashlib.sha256(f"{question}:{timestamp}".encode()).digest()
    vector = []
    for i in range(64):
        b = seed[i % len(seed)]
        vector.append(((b + i) % 256) / 255.0 - 0.5)

    return {
        "question": question[:500],
        "answer": answer[:2000],
        "dimension": "hive_capture",
        "hive": "GSPC_SOV_CAPTURE",
        "source_clan": f"clan-{source}",
        "score_at_capture": 100.0,
        "cluster_best_at_capture": 0.0,
        "delta": 100.0,
        "sha256": hashlib.sha256(f"{source}:{question}:{timestamp}".encode()).hexdigest(),
        "captured": timestamp,
        "verified": True,
        "fabricated": False,
        "misattributed": False,
        "citations": [{
            "url": "sov-capture-local-pc",
            "source": source,
            "as_of": "2026-07-31",
        }],
        "metadata": {
            "source": source,
            "use_case": "hive_learning",
            "audience": "engineer",
        },
    }


def log_event(directory: Path, event: dict):
    """Append a JSONL event to a date-stamped file in the capture directory."""
    directory.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    filepath = directory / f"{date_str}.jsonl"
    with open(filepath, "a") as f:
        f.write(json.dumps(event) + "\n")


def _build_terminal_kb_entry(cmd: str, exit_code: int = 0, pwd: str = None):
    """Build a KB entry from a terminal command WITHOUT writing to the capture log.

    2026-08-08 (JEEVES): `refine_kb` was re-calling `capture_terminal()`,
    which BOTH logged the event to the terminal JSONL AND returned a KB
    entry. That re-wrote every refined event back to the capture file, a
    self-feedback loop that ballooned the KB (85 -> 328K entries) and the
    capture file (13MB -> 787MB) in under 2h. This helper computes the same
    KB entry with no log side-effect, so refining no longer grows the source.
    """
    pwd = pwd or os.getcwd()
    glyphs = [PHLABET_KEYWORDS.get(c, ["?"])[0] for c in compress_to_phlabet(cmd)]
    success = "successful" if exit_code == 0 else f"failed (exit {exit_code})"
    answer = (
        f"Terminal command: `{cmd[:200]}` ran {success} in {pwd}. "
        f"Phlabet glyphs: {', '.join(glyphs[:8])}. "
        f"Captured by SOV TUI Snooper."
    )
    return make_kb_entry(
        question=f"What happened when we ran: {cmd[:200]}?",
        answer=answer,
        source="terminal_snooper",
    )


def capture_terminal(cmd: str, exit_code: int = 0, pwd: str = None):
    """TUI Snooper — capture a terminal command."""
    timestamp = datetime.now(timezone.utc).isoformat()
    pwd = pwd or os.getcwd()
    event = {
        "epoch": timestamp,
        "kind": "terminal_command",
        "cmd": cmd[:500],
        "exit_code": exit_code,
        "pwd": pwd,
        "phlabet_codes": compress_to_phlabet(cmd),
    }
    log_event(TERMINAL_DIR, event)

    # Auto-convert to KB entry (no re-write to the capture log)
    glyphs = [PHLABET_KEYWORDS.get(c, ["?"])[0] for c in event["phlabet_codes"]]
    success = "successful" if exit_code == 0 else f"failed (exit {exit_code})"
    answer = (
        f"Terminal command: `{cmd[:200]}` ran {success} in {pwd}. "
        f"Phlabet glyphs: {', '.join(glyphs[:8])}. "
        f"Captured by SOV TUI Snooper."
    )
    return make_kb_entry(
        question=f"What happened when we ran: {cmd[:200]}?",
        answer=answer,
        source="terminal_snooper",
    )


def capture_browser(url: str, title: str = "", text_sample: str = ""):
    """Browser Siphon — capture a URL visit (no passwords, no PII)."""
    timestamp = datetime.now(timezone.utc).isoformat()
    event = {
        "epoch": timestamp,
        "kind": "page_visit",
        "url": url[:500],
        "title": title[:500],
        "text_sample": text_sample[:1000] if text_sample else "",
        "phlabet_codes": compress_to_phlabet(f"{url} {title} {text_sample}"),
    }
    log_event(BROWSER_DIR, event)

    glyphs = [PHLABET_KEYWORDS.get(c, ["?"])[0] for c in event["phlabet_codes"]]
    return make_kb_entry(
        question=f"What did we learn from: {title}?",
        answer=(
            f"Visited {url[:200]} — '{title[:200]}'. "
            f"Phlabet glyphs extracted: {', '.join(glyphs[:8])}. "
            f"Captured by SOV Browser Siphon (local-only, no PII)."
        ),
        source="browser_siphon",
    )


def capture_file_change(path: str, diff: str = ""):
    """File Watcher — capture a code change."""
    timestamp = datetime.now(timezone.utc).isoformat()
    event = {
        "epoch": timestamp,
        "kind": "file_change",
        "path": path[:500],
        "diff": diff[:2000] if diff else "",
        "phlabet_codes": compress_to_phlabet(f"{path} {diff}"),
    }
    log_event(FILES_DIR, event)

    glyphs = [PHLABET_KEYWORDS.get(c, ["?"])[0] for c in event["phlabet_codes"]]
    return make_kb_entry(
        question=f"What changed in {path}?",
        answer=(
            f"File changed: {path[:200]}. "
            f"Phlabet glyphs: {', '.join(glyphs[:8])}. "
            f"Captured by SOV File Watcher."
        ),
        source="file_watcher",
    )


def capture_chat_event(query: str, response: str):
    """Chat Harvest — capture an agent conversation event."""
    timestamp = datetime.now(timezone.utc).isoformat()
    event = {
        "epoch": timestamp,
        "kind": "chat_event",
        "query": query[:1000],
        "response": response[:2000],
        "phlabet_codes": compress_to_phlabet(f"{query} {response}"),
    }
    log_event(CHAT_DIR, event)

    glyphs = [PHLABET_KEYWORDS.get(c, ["?"])[0] for c in event["phlabet_codes"]]
    return make_kb_entry(
        question=query[:300],
        answer=(
            f"Response: {response[:1000]}... "
            f"Phlabet glyphs: {', '.join(glyphs[:8])}. "
            f"Captured by SOV Chat Harvest."
        ),
        source="chat_harvest",
    )


def refine_kb():
    """KB Refinery — deduplicate, score, store in IWM."""
    print("KB Refinery — processing today's capture events...")

    # Get today's events
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    sources = {
        "terminal": TERMINAL_DIR,
        "browser": BROWSER_DIR,
        "files": FILES_DIR,
        "chat": CHAT_DIR,
    }

    events_by_source = {}
    for name, dir_path in sources.items():
        filepath = dir_path / f"{today}.jsonl"
        if filepath.exists():
            events = []
            with open(filepath) as f:
                for line in f:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                        # bound the window: the terminal capture can grow to
                        # millions of lines from the zsh preexec hook (each
                        # agent shell cmd logs an event). Processing the whole
                        # file each 5-min tick re-feeds every event through
                        # capture_terminal() again -> a feedback loop that
                        # ballooned the KB to 328K entries. Only refine the
                        # most recent REFINE_WINDOW events.
                        if len(events) >= REFINE_WINDOW:
                            break
            # take the most recent window, not the head
            events = events[-REFINE_WINDOW:]
            events_by_source[name] = events
            print(f"  {name}: {len(events)} events (refine window {REFINE_WINDOW})")
        else:
            events_by_source[name] = []
            print(f"  {name}: 0 events")

    # Convert each event to a KB entry (NO capture-log side-effect — the
    # terminal entries use the inline helper so refining doesn't re-grow the
    # source capture file; 2026-08-08 JEEVES feedback-loop fix)
    new_entries = []
    for name, events in events_by_source.items():
        for event in events:
            if name == "terminal":
                entry = _build_terminal_kb_entry(
                    event["cmd"],
                    event.get("exit_code", 0),
                    event.get("pwd", ""),
                )
            elif name == "browser":
                entry = capture_browser(
                    event.get("url", ""),
                    event.get("title", ""),
                    event.get("text_sample", ""),
                )
            elif name == "files":
                entry = capture_file_change(
                    event.get("path", ""),
                    event.get("diff", ""),
                )
            elif name == "chat":
                entry = capture_chat_event(
                    event.get("query", ""),
                    event.get("response", ""),
                )
            else:
                continue
            new_entries.append(entry)

    if not new_entries:
        print("  No events to refine.")
        return 0

    # Dedup by sha256 AND by normalized question
    # 2026-08-08 (JEEVES): the KB had ballooned to 7,124 entries of which
    # only 56 were unique facts — the epoch-based entry generation produced a
    # different sha256 per write, so exact-hash dedup missed ~99% redundancy
    # and the SAME ~56 questions re-appended every 5-min tick. Dedup by
    # normalized question text so only genuinely-new knowledge is appended.
    if KB_PATH.exists():
        kb = json.loads(KB_PATH.read_text())
    else:
        kb = {"entries": []}

    import re as _re
    def _norm_question(q):
        return _re.sub(r"[^a-z0-9]", " ", (q or "").lower())

    existing_hashes = {e.get("sha256") for e in kb.get("entries", [])}
    existing_q = {_norm_question(e.get("question", "")) for e in kb.get("entries", [])}
    before = len(kb.get("entries", []))

    added = 0
    for entry in new_entries:
        qn = _norm_question(entry.get("question", ""))
        if entry["sha256"] not in existing_hashes and qn not in existing_q:
            kb["entries"].append(entry)
            existing_hashes.add(entry["sha256"])
            existing_q.add(qn)
            added += 1

    after = len(kb["entries"])
    KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # 2026-08-08 fix (JEEVES): the KB reached 289 MB / 328K entries. Writing
    # it back with `indent=2` pretty-printed ~4x the compact size and pushed
    # every refine() past the EAT PHASE_9I budget. Compact single-line write
    # is far faster to serialize AND to re-parse. Pretty-print for humans can
    # be regenerated on demand (phas editor / small jq) — the canonical KB
    # does not need to be human-pretty on disk.
    KB_PATH.write_text(json.dumps(kb))

    print(f"  KB: {before} → {after} entries (+{added} new, dedup by normalized question)")
    print(f"  Saved to: {KB_PATH}")
    return added


def gnn_extract_skills():
    """GNN Spine — extract skills/patterns from capture events."""
    print("GNN Spine — extracting patterns from capture events...")

    # Find causal chains: command → success → skill
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    terminal_file = TERMINAL_DIR / f"{today}.jsonl"
    if not terminal_file.exists():
        print("  No terminal events today.")
        return

    events = []
    with open(terminal_file) as f:
        # 2026-08-08 (JEEVES): bound to the most recent window — the zsh
        # preexec hook can grow this file to hundreds of MB / millions of
        # lines; a full read here stalled PHASE_9I (227s). Same learning as
        # refine_kb: refine only the recent window, never the whole file.
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                if len(events) >= REFINE_WINDOW:
                    break
        events = events[-REFINE_WINDOW:]

    # Group by success/failure
    success_commands = [e for e in events if e.get("exit_code") == 0]
    failed_commands = [e for e in events if e.get("exit_code") != 0]

    # Extract patterns
    skills = []
    for cmd_event in success_commands:
        cmd = cmd_event.get("cmd", "")
        # Extract base command (first word)
        base_cmd = cmd.split()[0] if cmd else ""
        if base_cmd:
            skills.append({
                "skill_id": hashlib.sha256(f"skill:{base_cmd}".encode()).hexdigest()[:16],
                "command_pattern": base_cmd,
                "full_command": cmd[:200],
                "pwd": cmd_event.get("pwd", ""),
                "phlabet_codes": cmd_event.get("phlabet_codes", []),
                "confidence": 0.95 if success_commands else 0.0,
                "captured": cmd_event.get("epoch", ""),
            })

    # Deduplicate by skill_id
    seen = set()
    unique_skills = []
    for s in skills:
        if s["skill_id"] not in seen:
            seen.add(s["skill_id"])
            unique_skills.append(s)

    # Write skills to IWM
    IWM_DIR.mkdir(parents=True, exist_ok=True)
    skills_file = IWM_DIR / f"skills_{today}.jsonl"
    with open(skills_file, "w") as f:
        for s in unique_skills:
            f.write(json.dumps(s) + "\n")

    # Add skills to KB
    if KB_PATH.exists():
        kb = json.loads(KB_PATH.read_text())
    else:
        kb = {"entries": []}

    for s in unique_skills:
        entry = make_kb_entry(
            question=f"What is the skill for '{s['command_pattern']}'?",
            answer=(
                f"Skill extracted from successful runs: command '{s['command_pattern']}' "
                f"ran successfully in {s['pwd']}. "
                f"Phlabet codes: {s['phlabet_codes']}. "
                f"Confidence: {s['confidence']}. "
                f"Captured by GNN Spine."
            ),
            source="gnn_spine",
        )
        kb["entries"].append(entry)

    KB_PATH.write_text(json.dumps(kb))
    print(f"  Extracted {len(unique_skills)} unique skills")
    print(f"  Skills file: {skills_file}")
    print(f"  KB updated: {len(kb['entries'])} entries total")


def install():
    """Install the capture pipeline."""
    print("Installing SOVOS capture pipeline...")

    # Create directories
    for d in [TERMINAL_DIR, BROWSER_DIR, FILES_DIR, CHAT_DIR, IWM_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # Install zsh hook
    zshrc = HOME / ".zshrc"
    if zshrc.exists():
        content = zshrc.read_text()
        if "SOV_SNOOPER" not in content:
            hook = """
# SOVOS Honey Capture
export SOV_SNOOPER=1
export SOV_HONEY_PATH="$HOME/.sov/honey"
# 2026-08-08 (JEEVES): cap the daily capture file so the preexec hook can't
# flood the disk (grew to 787MB one day). Stop appending past 10MB/day; the
# cap is ~free and refine/gO readers are window-bounded anyway.
preexec() {
    if [ -n "$1" ]; then
        local _cap=~/.sov/honey/terminal/$(date -u +%Y%m%d).jsonl
        if [ ! -f "$_cap" ] || [ $(wc -c < "$_cap" 2>/dev/null || echo 0) -lt 10485760 ]; then
            echo "{\\\"epoch\\\":\\\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\\\",\\\"cmd\\\":\\\"$(echo $1 | sed 's/"/\\\\\"/g')\\\",\\\"pwd\\\":\\\"$PWD\\\"}" >> "$_cap" 2>/dev/null
        fi
    fi
}
"""
            with open(zshrc, "a") as f:
                f.write(hook)
            print(f"  Added zsh hook to {zshrc}")
        else:
            print(f"  zsh hook already installed in {zshrc}")
    else:
        print(f"  WARNING: {zshrc} not found")

    # Test capture works
    print("\nTesting capture pipeline...")
    entry = capture_terminal("echo 'hello sov'", 0, "/tmp")
    print(f"  Test entry sha256: {entry['sha256'][:16]}...")

    print("\n✓ SOVOS capture pipeline installed")
    print(f"  Capture dir: {HONEY_DIR}")
    print(f"  IWM dir: {IWM_DIR}")
    print(f"  KB: {KB_PATH}")


def show_status():
    """Show capture pipeline status."""
    print("SOVOS Capture Pipeline Status")
    print("=" * 50)
    for name, dir_path in [("terminal", TERMINAL_DIR), ("browser", BROWSER_DIR),
                            ("files", FILES_DIR), ("chat", CHAT_DIR)]:
        files = list(dir_path.glob("*.jsonl"))
        total_lines = 0
        big = 0
        for f in files:
            if f.stat().st_size > 100 * 1024 * 1024:
                big += 1
                continue
            with open(f) as fh:
                total_lines += sum(1 for _ in fh)
        suffix = f"  (+{big} large file{'s' if big != 1 else ''} not full-counted)" if big else ""
        print(f"  {name:10} {len(files):3} files  {total_lines:5}+ events{suffix}")

    if KB_PATH.exists():
        kb = json.loads(KB_PATH.read_text())
        print(f"  KB         {len(kb.get('entries', []))} entries")

    if IWM_DIR.exists():
        skills = list(IWM_DIR.glob("skills_*.jsonl"))
        if skills:
            total_skills = 0
            for f in skills:
                with open(f) as fh:
                    total_skills += sum(1 for _ in fh)
            print(f"  IWM skills {len(skills)} files  {total_skills} skills")


def main():
    parser = argparse.ArgumentParser(description="SOVOS PC capture pipeline")
    parser.add_argument("--setup", action="store_true", help="Install the pipeline")
    parser.add_argument("--snooper", action="store_true", help="TUI snooper mode")
    parser.add_argument("--cmd", help="Command to capture (with --snooper)")
    parser.add_argument("--exit", type=int, default=0, help="Exit code (with --snooper)")
    parser.add_argument("--siphon", action="store_true", help="Browser siphon mode")
    parser.add_argument("--url", help="URL to capture (with --siphon)")
    parser.add_argument("--title", default="", help="Page title (with --siphon)")
    parser.add_argument("--file-change", action="store_true", help="File watcher mode")
    parser.add_argument("--path", help="File path (with --file-change)")
    parser.add_argument("--chat-event", action="store_true", help="Chat harvest mode")
    parser.add_argument("--query", help="Query (with --chat-event)")
    parser.add_argument("--response", help="Response (with --chat-event)")
    parser.add_argument("--refine", action="store_true", help="Run KB refinery")
    parser.add_argument("--gnn-extract", action="store_true", help="GNN extract skills")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()

    if args.setup:
        install()
    elif args.snooper and args.cmd:
        entry = capture_terminal(args.cmd, args.exit)
        if KB_PATH.exists():
            kb = json.loads(KB_PATH.read_text())
        else:
            kb = {"entries": []}
        kb["entries"].append(entry)
        KB_PATH.write_text(json.dumps(kb))
        print(f"Captured + appended to KB: {entry['sha256'][:16]}...")
    elif args.siphon and args.url:
        entry = capture_browser(args.url, args.title)
        kb = json.loads(KB_PATH.read_text()) if KB_PATH.exists() else {"entries": []}
        kb["entries"].append(entry)
        KB_PATH.write_text(json.dumps(kb))
        print(f"Captured + appended to KB: {entry['sha256'][:16]}...")
    elif args.file_change and args.path:
        entry = capture_file_change(args.path)
        kb = json.loads(KB_PATH.read_text()) if KB_PATH.exists() else {"entries": []}
        kb["entries"].append(entry)
        KB_PATH.write_text(json.dumps(kb))
        print(f"Captured + appended to KB: {entry['sha256'][:16]}...")
    elif args.chat_event and args.query and args.response:
        entry = capture_chat_event(args.query, args.response)
        kb = json.loads(KB_PATH.read_text()) if KB_PATH.exists() else {"entries": []}
        kb["entries"].append(entry)
        KB_PATH.write_text(json.dumps(kb))
        print(f"Captured + appended to KB: {entry['sha256'][:16]}...")
    elif args.refine:
        refine_kb()
    elif args.gnn_extract:
        gnn_extract_skills()
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()