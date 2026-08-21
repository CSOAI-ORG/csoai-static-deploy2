#!/usr/bin/env python3.11
"""
witness_api.py — the Sovereign Witness FastAPI HTTP API.

Endpoints:
- GET /api/v1/witness/sigil/recent?limit=100
- GET /api/v1/witness/sigil/verify/{hash}
- GET /api/v1/witness/bft/proposals?limit=50
- GET /api/v1/witness/bft/proposal/{id}
- GET /api/v1/witness/audit/recent?limit=1000&actor_type=&action=
- GET /api/v1/witness/oscal/components
- GET /api/v1/witness/crosswalk/cells?framework=
- GET /api/v1/witness/watchdogs?limit=100
- GET /api/v1/witness/health
- GET /api/v1/witness/stats
- POST /api/v1/witness/sigil/append
- POST /api/v1/witness/audit
- POST /api/v1/witness/bft/propose
- POST /api/v1/witness/bft/{id}/vote
- POST /api/v1/witness/watchdog
- POST /api/v1/witness/oscal/register
- POST /api/v1/witness/crosswalk/register
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from witness_store import SovereignWitness

app = FastAPI(
    title="Sovereign Witness API",
    version="1.0.0",
    description="The public Witness API. L0.8 of the 8-layer physical substrate.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

w = SovereignWitness()


class SigilAppend(BaseModel):
    actor: str
    action: str
    payload: Optional[dict] = None
    bft_vote: Optional[dict] = None


class AuditEntry(BaseModel):
    actor: str
    actor_type: str
    action: str
    status: str = "success"
    details: Optional[dict] = None


class BftPropose(BaseModel):
    title: str
    proposer: str
    action: dict


class BftVote(BaseModel):
    voter: str
    choice: str  # for / against / abstain


class WatchdogReport(BaseModel):
    lat: float
    lon: float
    severity: str
    type: str


class OscalRegister(BaseModel):
    sha256: str
    name: str
    category: str
    description: str = ""


class CrosswalkRegister(BaseModel):
    framework: str
    article: str
    covered_by: str


@app.get("/api/v1/witness/health")
def health():
    return {"status": "ok", "service": "witness", "version": "1.0.0"}


@app.get("/api/v1/witness/stats")
def stats():
    return w.stats()


@app.get("/api/v1/witness/sigil/recent")
def sigil_recent(limit: int = Query(default=100, ge=1, le=1000)):
    return {"events": w.recent_sigil(limit=limit), "count": min(limit, len(w.recent_sigil(limit=limit)))}


@app.get("/api/v1/witness/sigil/verify/{hash_}")
def sigil_verify(hash_: str):
    result = w.verify_sigil(hash_)
    if not result['verified']:
        raise HTTPException(status_code=404, detail=f"Hash not found: {hash_}")
    return result


@app.get("/api/v1/witness/bft/proposals")
def bft_proposals_list(limit: int = Query(default=50, ge=1, le=500)):
    return {"proposals": w.bft_proposals(limit=limit), "count": min(limit, len(w.bft_proposals(limit=limit)))}


@app.get("/api/v1/witness/bft/proposal/{proposal_id}")
def bft_proposal_get(proposal_id: int):
    proposals = w.bft_proposals(limit=1000)
    for p in proposals:
        if p['id'] == proposal_id:
            return p
    raise HTTPException(status_code=404, detail=f"Proposal not found: {proposal_id}")


@app.get("/api/v1/witness/audit/recent")
def audit_recent(limit: int = Query(default=1000, ge=1, le=10000), actor_type: Optional[str] = None, action: Optional[str] = None):
    return {"entries": w.recent_audit(limit=limit, actor_type=actor_type, action=action), "count": limit}


@app.get("/api/v1/witness/oscal/components")
def oscal_components():
    return {"components": w.oscal_components(), "count": len(w.oscal_components())}


@app.get("/api/v1/witness/crosswalk/cells")
def crosswalk_cells(framework: Optional[str] = None):
    return {"cells": w.crosswalk_cells(framework=framework), "count": len(w.crosswalk_cells(framework=framework))}


@app.get("/api/v1/witness/watchdogs")
def watchdogs_list(limit: int = Query(default=100, ge=1, le=1000)):
    return {"reports": w.watchdogs(limit=limit), "count": min(limit, len(w.watchdogs(limit=limit)))}


@app.post("/api/v1/witness/sigil/append")
def sigil_append(req: SigilAppend):
    event = w.append_sigil(actor=req.actor, action=req.action, payload=req.payload, bft_vote=req.bft_vote)
    w.audit(actor=req.actor, actor_type='human', action=req.action, status='success', details={'sigil': event['hash']})
    return event


@app.post("/api/v1/witness/audit")
def audit_post(req: AuditEntry):
    return w.audit(actor=req.actor, actor_type=req.actor_type, action=req.action, status=req.status, details=req.details)


@app.post("/api/v1/witness/bft/propose")
def bft_propose(req: BftPropose):
    return w.propose_bft(title=req.title, proposer=req.proposer, action=req.action)


@app.post("/api/v1/witness/bft/{proposal_id}/vote")
def bft_vote_post(proposal_id: int, req: BftVote):
    return w.vote_bft(proposal_id=proposal_id, voter=req.voter, choice=req.choice)


@app.post("/api/v1/witness/watchdog")
def watchdog_post(req: WatchdogReport):
    return w.log_watchdog(lat=req.lat, lon=req.lon, severity=req.severity, type_=req.type)


@app.post("/api/v1/witness/oscal/register")
def oscal_register(req: OscalRegister):
    return w.register_oscal(sha256=req.sha256, name=req.name, category=req.category, description=req.description)


@app.post("/api/v1/witness/crosswalk/register")
def crosswalk_register(req: CrosswalkRegister):
    return w.register_crosswalk(framework=req.framework, article=req.article, covered_by=req.covered_by)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8042, log_level='info')
