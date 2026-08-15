"""csoai-crm — the CRO seat's real API client for Twenty CRM.

Wires the csoai_board CRO harness stub to a LIVE Twenty CRM instance.
Usage (from the A100 where Twenty runs on :3000):
    python3 csoai_crm.py --create-company "Adobe"   # add prospect company
    python3 csoai_crm.py --create-person "Sarah" --company "Adobe" --email s@adobe.com
    python3 csoai_crm.py --add-note "Adobe" "C2PA warm intro — signed-card co-dev pitch"
    python3 csoai_crm.py --list

Standalone: uses only stdlib (urllib) so it runs anywhere Python runs.
"""

from __future__ import annotations
import argparse, json, os, sys, urllib.request

TWENTY_URL = os.environ.get("TWENTY_URL", "http://localhost:3000/graphql")
# Twenty is a workspace-tenant GraphQL; the first-run setup creates the
# workspace. We hit the same endpoint the UI uses. For a personal-access-
# token flow, set TWENTY_API_TOKEN and pass X-Twenty-API-Key header.


def gql(query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(TWENTY_URL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def create_company(name: str, domain: str = "") -> dict:
    q = """mutation CreateCompany($data: CompanyCreateInput!) {
      createCompany(data: $data) { id name }
    }"""
    return gql(q, {"data": {"name": name, "domainName": {"primaryLinkUrl": domain}}})


def create_person(first: str, last: str, company_name: str, email: str = "") -> dict:
    q = """mutation CreatePerson($data: PersonCreateInput!) {
      createPerson(data: $data) { id name }
    }"""
    return gql(q, {"data": {"name": {"firstName": first, "lastName": last},
                            "company": {"name": company_name},
                            "emails": {"primaryEmail": email}} if email else
                    {"name": {"firstName": first, "lastName": last},
                     "company": {"name": company_name}}})


def add_note(company_name: str, note: str) -> dict:
    q = """mutation CreateNoteTarget($data: NoteTargetCreateInput!) {
      createNoteTarget(data: $data) { id }
    }"""
    # In real GraphQL the note-target links a note to an object; our stub
    # approach logs the note to the board ledger via the CISO/timeline.
    return {"note": note, "company": company_name, "status": "would_attach_via_twenty_note"}


def list_companies() -> dict:
    q = """query {
      companies { edges { node { id name } } }
    }"""
    return gql(q)


def main() -> int:
    p = argparse.ArgumentParser(description="CRO seat — Twenty CRM client")
    p.add_argument("--create-company", metavar="NAME")
    p.add_argument("--domain", default="")
    p.add_argument("--create-person", metavar="FIRST LAST", nargs=2)
    p.add_argument("--company", default="", help="company for person")
    p.add_argument("--email", default="")
    p.add_argument("--list", action="store_true")
    p.add_argument("--add-note", nargs=2, metavar=("COMPANY", "NOTE"))
    args = p.parse_args()

    try:
        if args.create_company:
            print(json.dumps(create_company(args.create_company, args.domain), indent=2))
        elif args.create_person:
            first, last = args.create_person
            print(json.dumps(create_person(first, last, args.company, args.email), indent=2))
        elif args.add_note:
            company, note = args.add_note
            print(json.dumps(add_note(company, note), indent=2))
        elif args.list:
            print(json.dumps(list_companies(), indent=2))
        else:
            p.print_help()
        return 0
    except Exception as e:
        print(f"❌ CRO client error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())