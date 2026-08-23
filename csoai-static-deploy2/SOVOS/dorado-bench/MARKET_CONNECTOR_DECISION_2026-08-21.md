# Council Ledger — Market-Connector Decision (2026-08-21, research-verified)

## The finding that matters
Redistribution licensing is the constraint, not availability. Every free/standard tier
prohibits public redistribution. PLUS a two-layer trap: vendor licence ≠ index-owner rights
(S&P 500 © S&P DJI, FTSE © FTSE Russell, DAX © STOXX, Nikkei © Nikkei Inc, HSI © HSI Co,
KOSPI © KRX, ASX © S&P/ASX, STI © FTSE Russell/SGX/SPH, SSE © SSE) + exchange display fees
for realtime/15-min data.

## Current state (honest)
- dorado_bench.py uses Yahoo v8 (free, no auth, 9 indices, 18 pair-gaps live) — DEV SHIM ONLY.
  Grants NO redistribution rights. Fine for internal measurement; NOT publishable as a signed
  dataset without a licence.

## Decision (research-verified: subagent + sources cited)
- PRODUCTION: Twelve Data (Business tier, first-party MCP, 84 markets incl. East+West) OR
  FMP Enterprise (only vendor documenting the redistribution path) + signed Data Display &
  Licensing Agreement naming the 9 indices explicitly.
- DISQUALIFIED: Polygon/Massive (US-only indices), Financial Datasets (fundamentals not quotes),
  EODHD (OTC/VWAP provenance red flag).
- STRUCTURE: delayed/EOD snapshots (shed real-time exchange fees); parallel legal clearance on
  index-owner rights; keep Yahoo as the internal dev/measurement feed.

## What stays public now
- The pair-gap METRIC (log_return delta) is our derived measurement — but index VALUES in a
  signed public dataset need the licence. Until then: publish gaps + methodology, keep raw
  quotes internal (register: MEASURED-internal / REPORTED-derived).

## REFINEMENT (2026-08-21, full research pass — sources cited)
- PRIMARY: **Twelve Data Business tier** — first-party MCP (mcp.twelvedata.com), 84 markets incl.
  East+West headline indices, explicit "For Business" track. Individual plans = non-commercial;
  must move to Business + get redistribution in writing.
- SECONDARY: **FMP Enterprise** + signed Data Display & Licensing Agreement (only vendor documenting
  the redistribution path); MCP is community-built.
- DISQUALIFIED (hard): Polygon/Massive (indices only CME/CBOE/Nasdaq = US-only, no HSI/Nikkei/SSE/
  KOSPI/ASX/STI/FTSE/DAX) · Financial Datasets (fundamentals, not index quotes) · EODHD (OTC/VWAP-
  aggregated prices — NOT exchange-licensed; unacceptable provenance for audit-grade signed output).
- THREE-LAYER LICENSING (the real constraint): (1) vendor plan terms (all free/standard = personal/
  non-commercial, redistribution forbidden); (2) index-owner IP (S&P DJI, FTSE Russell, STOXX, Nikkei
  Inc, HSI Co, KRX, SGX, SSE — vendor licence does NOT transfer); (3) exchange display/redistribution
  fees for realtime/15-min.
- ACTION: adopt Twelve Data Business; name the 9 indices explicitly in the agreement; parallel legal
  clearance on index-owner rights; publish DELAYED/EOD snapshots (sheds exchange realtime fees);
  Yahoo stays internal dev-only.
- Sources: twelvedata.com/pricing · github.com/twelvedata/mcp · site.financialmodelingprep.com/developer/
  docs/pricing · massive.com (rebrand + index sources) · financialdatasets.ai/mcp-server · eodhd.com.
