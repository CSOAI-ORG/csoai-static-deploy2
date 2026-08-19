# ENTITY ANCHORS — ROR + Wikidata requests (N-SITES THIS-WEEK #7)
**2026-08-19 · JEEVES · verified: no ROR ID, no Wikidata item exist yet — both are free, self-serve**

---

## Why entity anchors matter
Every scholarly/agent surface keys on ROR + Wikidata + ORCID. Without them, our Zenodo DOIs float unattached — no research-org graph links CSOAI's records to the company. The spray-sheet's propagation chain (Zenodo→OpenAIRE→OpenAlex→data.europa.eu) resolves *better* with entity anchors.

## Verified current state (checked live, never assumed)
| Anchor | Status |
|---|---|
| ROR | ❌ **no ID** (search "CSOAI" → 0 hits) |
| Wikidata | ❌ **no item** (search "CSOAI" → 0 hits) |
| ORCID | ❌ **no Nicholas Templeman record** (37 Templemans, none matching) |
| Zenodo concept DOI | ✅ 10.5281/zenodo.21991105 (GSPC Methodology, created 2026-08-18) |
| OAI-PMH | ✅ live (`oai:zenodo.org:21991105`) — propagation trigger armed |

## ROR curation request (draft — free, submit at ror.org/community)
> **Name:** CSOAI Ltd (t/a Council of AI)
> **Type:** Company
> **Country:** GB
> **URL:** https://councilof.ai
> **Linked identifiers:** UK Companies House 16939677; Crossref Funder ID (request); DOI 10.5281/zenodo.21991105
> **Acronym:** CSOAI
> **Request type:** New organization

## Wikidata item (draft — free, create via wikidata.org)
- **Label:** Council of AI / CSOAI Ltd
- **Instance of:** company (Q783794)
- **Country:** United Kingdom (Q145)
- **Official website:** https://councilof.ai
- **UK Companies House ID:** 16939677 (P5123)
- **DOI:** 10.5281/zenodo.21991105 (P356)

## ORCID (draft — Nick creates, free)
- Register at orcid.org (name: Nicholas Templeman; email: nicholas@csoai.org)
- Link works: the GSPC methodology DOI, this estate's HF/kaggle profiles

## SIGIL
`entity-anchors-2026-08-19-jeeves`
