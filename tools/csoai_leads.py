#!/usr/bin/env python3
"""
csoai_leads.py — Create and manage CSOAI leads database.

Usage:
  python3 csoai_leads.py --init          # Create database with schema
  python3 csoai_leads.py --add           # Add sample leads
  python3 csoai_leads.py --list          # List all leads
  python3 csoai_leads.py --report        # Generate Tier 0 report
"""
import json, sys, argparse, os, sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "csoai_leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    organization TEXT,
    sector TEXT,
    tier INTEGER DEFAULT 2,
    status TEXT DEFAULT 'new',
    contact_email TEXT,
    contact_phone TEXT,
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS engagements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    engagement_type TEXT,
    description TEXT,
    value_gbp REAL,
    status TEXT DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    report_type TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);
"""

SAMPLE_LEADS = [
    {"name": "DSTL", "organization": "Defence Science and Technology Laboratory", "sector": "defence", "tier": 1},
    {"name": "NCSC", "organization": "National Cyber Security Centre", "sector": "cyber", "tier": 1},
    {"name": "NHS England", "organization": "NHS England Transformation", "sector": "healthcare", "tier": 1},
    {"name": "Cabinet Office", "organization": "Cabinet Office Commercial", "sector": "government", "tier": 1},
    {"name": "MOD Digital", "organization": "Ministry of Defence Digital", "sector": "defence", "tier": 1},
]

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(SCHEMA)
    print(f"Database created: {DB_PATH}")

def add_leads():
    conn = sqlite3.connect(str(DB_PATH))
    for lead in SAMPLE_LEADS:
        try:
            conn.execute(
                "INSERT INTO leads (name, organization, sector, tier) VALUES (?, ?, ?, ?)",
                (lead["name"], lead["organization"], lead["sector"], lead["tier"])
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    print(f"Added {len(SAMPLE_LEADS)} sample leads")

def list_leads():
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute("SELECT id, name, organization, sector, tier, status FROM leads ORDER BY tier, name").fetchall()
    for row in rows:
        print(f"  [{row[4]}] {row[1]:20s} | {row[2]:30s} | {row[3]:15s} | {row[5]}")

def generate_report():
    conn = sqlite3.connect(str(DB_PATH))
    tier1 = conn.execute("SELECT COUNT(*) FROM leads WHERE tier = 1").fetchone()[0]
    tier2 = conn.execute("SELECT COUNT(*) FROM leads WHERE tier = 2").fetchone()[0]
    tier3 = conn.execute("SELECT COUNT(*) FROM leads WHERE tier = 3").fetchone()[0]
    total = tier1 + tier2 + tier3
    print(f"CSOAI Leads Report — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Total leads: {total}")
    print(f"  Tier 1 (Crown): {tier1}")
    print(f"  Tier 2 (Strategic): {tier2}")
    print(f"  Tier 3 (Pipeline): {tier3}")

def main():
    parser = argparse.ArgumentParser(description="CSOAI Leads Database")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--add", action="store_true", help="Add sample leads")
    parser.add_argument("--list", action="store_true", help="List all leads")
    parser.add_argument("--report", action="store_true", help="Generate report")
    args = parser.parse_args()

    if args.init:
        init_db()
    elif args.add:
        add_leads()
    elif args.list:
        list_leads()
    elif args.report:
        generate_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
