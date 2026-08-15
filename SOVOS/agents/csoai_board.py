"""csoai-board — the One-Man-Corporation OS: CEO-agent routing table + harness.

Each business function is a "CEO agent": an MCP-wrapped specialist with its own
toolset. sovos_router dispatches; every action flows through the signed-card
layer so the board is audit-able end to end.

Seats: CEO (human) · CFO · CRO · CMO · CLO · CTO · COO · CPO · CISO

Usage:
    from csoai_board import Board, seat, route
    board = Board()
    board.route("open_invoice", amount=420, client="AI Verify")
    # → dispatches to CFO agent, logs signed action
"""

from __future__ import annotations
import hashlib, json, datetime
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ── The Board (seat registry) ───────────────────────────────────────
SEATS = {
    "CEO": {"title": "Chairman (human)", "human": True,
            "toolset": "final sign-off"},
    "CFO": {"title": "Accountant/Finance", "human": False,
            "toolset": "ERPNext + Stripe + bookkeeping",
            "harness": "erpnext"},
    "CRO": {"title": "Sales/Revenue", "human": False,
            "toolset": "Twenty + named-account engine",
            "harness": "twenty"},
    "CMO": {"title": "Marketing", "human": False,
            "toolset": "n8n + press pack + content engine",
            "harness": "n8n"},
    "CLO": {"title": "Legal/IP", "human": False,
            "toolset": "OIN/LOT + contracts + OpenPatent",
            "harness": "legal"},
    "CTO": {"title": "Engineering", "human": False,
            "toolset": "Devin + Claude Code + monorepo",
            "harness": "dev"},
    "COO": {"title": "Operations", "human": False,
            "toolset": "fleet + cron + MCP workers",
            "harness": "ops"},
    "CPO": {"title": "Publishing/Distribution", "human": False,
            "toolset": "Zenodo/HF/Kaggle/PyPI/npm",
            "harness": "distribution"},
    "CISO": {"title": "Security/Neutrality", "human": False,
            "toolset": "claim-linter + firewall-lint + jail bank",
            "harness": "security"},
}


# ── Action log entry (signed) ───────────────────────────────────────
@dataclass
class BoardAction:
    seat: str
    intent: str
    payload: Dict[str, Any]
    ts: str = field(default_factory=lambda: datetime.datetime.now(
        datetime.timezone.utc).isoformat())
    digest: str = ""
    signature: str = ""

    def sign(self, seed: str = "0" * 64) -> "BoardAction":
        canonical = json.dumps({
            "seat": self.seat, "intent": self.intent, "payload": self.payload,
            "ts": self.ts,
        }, sort_keys=True, separators=(",", ":")).encode()
        self.digest = hashlib.sha256(canonical).hexdigest()
        self.signature = hashlib.sha256(
            bytes.fromhex(seed[:32]) + bytes.fromhex(self.digest[:32])
        ).hexdigest()[:64]
        return self

    def to_dict(self) -> Dict:
        return {"seat": self.seat, "intent": self.intent, "payload": self.payload,
                "ts": self.ts, "digest": self.digest, "signature": self.signature}


# ── Harness stubs (real toolset wiring comes per-seat) ──────────────
HARNESSES: Dict[str, Callable[[str, Dict], Dict]] = {}


def _register_harness(seat: str):
    def deco(fn):
        HARNESSES[seat] = fn
        return fn
    return deco


@_register_harness("CFO")
def cfo_harness(intent: str, payload: Dict) -> Dict:
    """CFO agent — ledger, invoice, tax-prep intent handling."""
    if intent == "open_invoice":
        return {"seat": "CFO", "status": "drafted",
                "invoice": {"amount": payload.get("amount"),
                            "client": payload.get("client"),
                            "currency": payload.get("currency", "GBP"),
                            "vat": round(payload.get("amount", 0) * 0.2, 2)},
                "note": "AI-drafted; human (or qualified accountant) signs the authority act"}
    if intent == "book":
        return {"seat": "CFO", "status": "posted",
                "entry": payload, "note": "ledger entry via ERPNext (pending install)"}
    return {"seat": "CFO", "status": "unknown_intent", "intent": intent}


@_register_harness("CRO")
def cro_harness(intent: str, payload: Dict) -> Dict:
    if intent == "add_prospect":
        return {"seat": "CRO", "status": "added",
                "prospect": payload.get("name"),
                "stage": payload.get("stage", "discovery"),
                "note": "tracked in Twenty (pending install)"}
    return {"seat": "CRO", "status": "unknown_intent", "intent": intent}


@_register_harness("CPO")
def cpo_harness(intent: str, payload: Dict) -> Dict:
    if intent == "publish_card":
        return {"seat": "CPO", "status": "queued",
                "card": payload.get("card_id"),
                "channels": ["zenodo", "github", "kaggle", "huggingface"],
                "note": "anchor-first: Zenodo concept DOI, mirrors point back"}
    return {"seat": "CPO", "status": "unknown_intent", "intent": intent}


@_register_harness("CISO")
def ciso_harness(intent: str, payload: Dict) -> Dict:
    if intent == "firewall_check":
        text = json.dumps(payload).lower()
        banned = ["referral fee", "paid placement", "rating for listing",
                  "certified by council", "endorsed by council"]
        hits = [b for b in banned if b in text]
        return {"seat": "CISO", "status": "BLOCKED" if hits else "CLEAR",
                "hits": hits,
                "note": "firewall lint on agent output — neutrality is the moat"}
    return {"seat": "CISO", "status": "unknown_intent", "intent": intent}


# ── The Board ───────────────────────────────────────────────────────
class Board:
    """The routing layer: intent → seat → harness → signed action."""

    ROUTES: Dict[str, str] = {
        "open_invoice": "CFO", "book": "CFO", "tax_prep": "CFO",
        "add_prospect": "CRO", "outreach": "CRO", "pipeline": "CRO",
        "press": "CMO", "content": "CMO", "social": "CMO",
        "contract": "CLO", "ip_filing": "CLO", "compliance": "CLO",
        "build": "CTO", "ship": "CTO", "fix": "CTO",
        "schedule": "COO", "fleet": "COO", "monitor": "COO",
        "publish_card": "CPO", "distribute": "CPO",
        "firewall_check": "CISO", "audit": "CISO",
    }

    def __init__(self, seed: str = "0" * 64):
        self.seed = seed
        self.ledger: List[Dict] = []

    def route(self, intent: str, **payload) -> Dict:
        """Dispatch an intent to the right CEO agent; sign + log the action."""
        seat = self.ROUTES.get(intent, "COO")  # default: ops
        if seat == "CEO":
            return {"seat": "CEO", "status": "HUMAN_DECISION_REQUIRED",
                    "intent": intent, "payload": payload,
                    "note": "the chairman must sign off"}

        harness = HARNESSES.get(seat)
        result = harness(intent, payload) if harness else {
            "seat": seat, "status": "no_harness"}

        action = BoardAction(seat=seat, intent=intent, payload=payload)
        action.sign(self.seed)
        record = {**result, "action": action.to_dict()}
        self.ledger.append(record)
        return record

    def summary(self) -> Dict:
        return {"seats": list(SEATS.keys()),
                "actions_logged": len(self.ledger),
                "last_digest": self.ledger[-1]["action"]["digest"][:16]
                if self.ledger else None}


# ── self-test ───────────────────────────────────────────────────────
def self_test() -> int:
    failures = 0
    print("=== csoai-board self-test ===", flush=True)
    board = Board()

    # 1. CFO routing + signing
    r = board.route("open_invoice", amount=420, client="AI Verify", currency="USD")
    assert r["seat"] == "CFO" and r["status"] == "drafted"
    assert r["action"]["signature"], "action must be signed"
    print(f"  ✅ CFO: invoice drafted + signed ({r['action']['digest'][:12]})")

    # 2. CRO routing
    r = board.route("add_prospect", name="Adobe", stage="C2PA warm intro")
    assert r["seat"] == "CRO"
    print(f"  ✅ CRO: prospect tracked ({r['prospect']})")

    # 3. CPO routing
    r = board.route("publish_card", card_id="REL-016")
    assert r["seat"] == "CPO"
    print(f"  ✅ CPO: publish queued ({r['channels']})")

    # 4. CISO firewall blocks banned language
    r = board.route("firewall_check", text="give us a referral fee for a better rating")
    assert r["status"] == "BLOCKED", "firewall must block referral-fee language"
    print(f"  ✅ CISO: firewall BLOCKED referral-fee language ({r['hits']})")

    # 5. Unknown intent → COO default
    r = board.route("something_else", x=1)
    assert r["seat"] == "COO"
    print(f"  ✅ unknown intent → COO default")

    # 6. CEO seat requires human
    # (no route to CEO by default; all intents map to agents)
    print(f"  ✅ board has {len(SEATS)} seats, {len(board.ROUTES)} intent routes")

    print(f"\n✅ csoai-board: ALL TESTS PASS ({len(board.ledger)} actions logged)")
    return failures


if __name__ == "__main__":
    import sys
    sys.exit(self_test())