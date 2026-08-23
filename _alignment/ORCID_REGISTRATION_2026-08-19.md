# ORCID Registration — prepared, [N] to complete
## 2026-08-19 · the USENIX/S&P hard gate

**Status:** Nicholas Templeman (the sole named creator on the Zenodo spine DOI 10.5281/zenodo.21991105) has **no ORCID iD** (pub.orcid.org search: num-found 0). ORCID registration is a free, self-serve, ~30-min account creation that requires the owner's email + password — an [N] action this lane cannot complete.

## Why it's a gate
- USENIX Security '27 (Cycle 2, reg 19 Jan 2027) **mandates ORCID + artifacts**
- ICLR 2027 (abstract 18 Sep) and FAccT 2027 (abstract 27 Oct) prefer linked ORCID
- Zenodo creators without ORCID don't propagate into the scholarly graphs

## Exact steps for [N] (10 minutes)
1. Go to https://orcid.org/register (verified 200, free)
2. Name: Nicholas Templeman
3. Email: nicholas@csoai.org (or personal)
4. Password + visibility defaults (public for the iD, private for email)
5. Verify email → get iD (16-digit, e.g. 0000-0002-XXXX-XXXX)
6. Add affiliation: CSOAI Ltd (UK Companies House 16939677)
7. Link the Zenodo DOI 10.5281/zenodo.21991104 to the profile (works section)
8. Give the lane the iD → we add it to the Zenodo record creators + llms.txt author line

## After registration
- Zenodo record 21991105 creators get `person_or_org.identifiers` = [{scheme: "orcid", identifier: "<ID>"}]
- ROR #39061 (just opened) cross-references the ORCID
- OpenAlex author profile becomes claimable

**Prepared by: Sim World lane · blocks: USENIX (Jan), ICLR (Sep), FAccT (Oct)**
