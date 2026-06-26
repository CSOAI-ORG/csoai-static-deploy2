# LAST 24-48 HOURS Security Intelligence Report -- June 20-21, 2026

**Report Date:** June 21, 2026
**Analyst:** Cybersecurity Intelligence Unit
**Scope:** CVEs, Breaches, AI Safety, Ransomware, Vulnerabilities, M&A, Policy

---

## TABLE OF CONTENTS

1. [CRITICAL: FORTIBLEED - Fortinet Credential Leak (June 16-18, 2026)](#1-fortibleed)
2. [CRITICAL: Klue OAuth Breach / Icarus Extortion (June 12-19, 2026)](#2-klue-oauth-breach)
3. [CVEs DISCLOSED JUNE 20-21, 2026](#3-cves-june-20-21)
4. [AI MODEL JAILBREAK: Anthropic Fable 5 / Pliny (June 9-12, 2026)](#4-fable5-jailbreak)
5. [AI CODING TOOL VULNERABILITY: CVE-2026-35603 (June 17, 2026)](#5-ai-coding-tools-cve)
6. [CISA ALERTS & KEV UPDATES (June 2026)](#6-cisa-alerts)
7. [MICROSOFT PATCH TUESDAY JUNE 2026](#7-patch-tuesday)
8. [AI SECURITY THREATS & PROMPT INJECTION (June 2026)](#8-ai-threats)
9. [RANSOMWARE: Gentlemen RaaS + EDR Killers (June 18, 2026)](#9-ransomware)
10. [M&A / STARTUP NEWS (June 2026)](#10-ma-news)
11. [OTHER BREACHES & INCIDENTS](#11-other-breaches)
12. [POLICY / GOVERNMENT](#12-policy)

---

## 1. FORTIBLEED: Fortinet Mass Credential Leak (DISCLOSED: June 16-18, 2026)

**CSOAI RELEVANCE: CRITICAL - Infrastructure/Edge Device Compromise**

| Field | Detail |
|-------|--------|
| **Event** | FortiBleed - Massive credential compromise campaign targeting Fortinet FortiGate firewalls |
| **Disclosed** | June 16, 2026 (formal); CISA warning June 19, 2026 |
| **Affected Devices** | ~74,000-86,000 Fortinet firewalls/VPNs (approx. 50% of all internet-facing FortiGate devices) |
| **Threat Actor** | Russian-speaking cybercriminal group |
| **Impact** | Cleartext credentials, Kerberos hashes, NTLM hashes harvested; 4 organizations fully compromised including a Turkish NATO defense contractor with classified documents exfiltrated |

**Technical Details:**
- Attackers systematically extracted configuration files from internet-facing FortiGate devices and cracked stored credential hashes
- Operational database included validated credentials organized by country, sector, and organization revenue
- Campaign used 45-GPU cluster managed via Hashtopolis for hash cracking
- Affected major orgs: Samsung, Siemens, Foxconn, Oracle, Accenture, DHL, Infosys, Fortinet itself, government agencies
- Legacy SHA-256 password storage (pre-FortiOS 7.2.11/7.4.8/7.6.1) enabled rapid cracking

**Sources:**
- Huntress: https://support.huntress.io/hc/en-us/articles/52698652545171-2026-June-Fortibleed-Credential-Exposure
- Arctic Wolf: https://arcticwolf.com/resources/blog/active-fortibleed-campaign-impacting-fortinet-devices-across-194-countries/
- Help Net Security: https://www.helpnetsecurity.com/2026/06/18/fortinet-fortibleed-data-leak/
- BleepingComputer: https://www.bleepingcomputer.com/news/security/fortibleed-leak-exposes-fortinet-vpn-credentials-for-73-000-devices/
- HKCERT: https://www.hkcert.org/security-bulletin/security-alert-fortibleed-credential-leak-incident-over-70-000-fortinet-devices-suspected-to-be-affected-by-data-and-credential-exposure-hong-kong-organisations-may-be-affected_20260618

---

## 2. KLUE OAUTH BREACH / ICARUS EXTORTION (June 12-19, 2026)

**CSOAI RELEVANCE: HIGH - SaaS Supply Chain / OAuth Token Abuse**

| Field | Detail |
|-------|--------|
| **Event** | Klue market intelligence platform breached; OAuth tokens stolen for customer Salesforce data theft |
| **Disclosed** | June 18-19, 2026 |
| **Threat Actor** | Icarus extortion group (active since April 2026) |
| **Affected** | Huntress, Recorded Future, Tanium, Jamf, Gong, Sprout Social, Insurity + others |
| **Root Cause** | Compromised legacy credential associated with deprecated integration service |

**Attack Chain:**
1. Attacker gained access via compromised legacy credential (created for prototyping, never revoked)
2. Pushed code update to Klue backend to harvest OAuth tokens from customer integrations
3. Used Python scripts (user-agent: "Python-urllib/3.12", "Python-urllib/3.14") to query Salesforce REST API
4. Exfiltrated business contacts, sales communications, pricing, opportunity notes
5. Extortion emails sent from compromised Australian retail domains via Session Messenger

**Technical Indicators:**
- Salesforce API endpoint: `/services/data/v59.0/query/<STRING>`
- ~900 queries observed in 15-minute bursts
- Attacker IPs: Netherlands, France, Ukraine (138.226.246[.]94 linked to spam)
- Salesforce disabled Klue Battlecards app integration in response

**Sources:**
- BleepingComputer: https://www.bleepingcomputer.com/news/security/klue-oauth-breach-victim-list-grows-as-icarus-hackers-claim-attack/
- The Hacker News: https://thehackernews.com/2026/06/salesforce-disables-klue-app.html
- Huntress: https://www.huntress.com/blog/klue-breach-investigation
- Rescana: https://www.rescana.com/post/klue-oauth-integration-breach-exposes-salesforce-customer-data-in-icarus-supply-chain-attack
- SC World: https://www.scworld.com/brief/icarus-threat-actors-exploit-klue-oauth-breach-to-steal-salesforce-data

---

## 3. CVEs DISCLOSED JUNE 20-21, 2026

### 3.1 CVE-2026-12771 - LiteLLM M2M JWT Handler Improper Authorization
| Field | Detail |
|-------|--------|
| **Severity** | CRITICAL |
| **Product** | BerriAI LiteLLM <= 1.82.2 |
| **File** | `litellm/proxy/auth/user_api_key_auth.py` |
| **Description** | Improper authorization in M2M JWT Handler allows remote attack. Public exploit available. |
| **Published** | June 21, 2026 |
| **CSOAI Relevance** | CRITICAL - AI infrastructure component; affects LLM proxy deployments |

**Source:** https://www.tenable.com/cve/newest | https://cvefeed.io/vuln/detail/CVE-2026-12771

---

### 3.2 CVE-2026-12770 - LiteLLM Admin Key Handler Improper Authorization
| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Product** | BerriAI LiteLLM <= 1.63.1 |
| **File** | `litellm/proxy/management_endpoints/key_management_endpoints.py` |
| **Description** | Improper authorization in Admin Key Handler. Public exploit disclosed. |
| **Published** | June 21, 2026 |
| **CSOAI Relevance** | HIGH - AI infrastructure; admin key management bypass |

**Source:** https://www.tenable.com/cve/newest | https://cvefeed.io/vuln/detail/CVE-2026-12770

---

### 3.3 CVE-2026-56265 - Crawl4AI Authentication Bypass via Hardcoded JWT Key
| Field | Detail |
|-------|--------|
| **Severity** | CRITICAL (CVSS 9.3) |
| **Product** | Crawl4AI >= 0, < 0.8.7 |
| **CWE** | CWE-798 (Use of Hard-coded Credentials) |
| **Description** | Hardcoded default JWT signing key in Docker API server allows attackers to forge valid auth tokens for any user, bypassing authentication completely. |
| **Published** | June 21, 2026 |
| **CSOAI Relevance** | CRITICAL - AI-powered web crawler widely used in LLM pipelines |

**Source:** https://www.vulncheck.com/advisories/crawl4ai-authentication-bypass-via-hardcoded-jwt-signing-key

---

### 3.4 CVE-2026-56397 / CVE-2026-56396 / CVE-2026-56395 - SiYuan RCE via Bazaar Package
| Field | Detail |
|-------|--------|
| **Severity** | CRITICAL (CVSS 9.6) |
| **Product** | SiYuan Note/SiYuan |
| **Description** | Remote code execution via malicious Bazaar package metadata and README. Attack path: Drive-by Compromise -> Command and Scripting Interpreter execution. |
| **Published** | June 21, 2026 |
| **CSOAI Relevance** | HIGH - Note-taking/knowledge management platform with AI features |

**Source:** https://cve.tools/

---

### 3.5 CVE-2026-56345 - AVideo Authorization Bypass (Meet Plugin)
| Field | Detail |
|-------|--------|
| **Severity** | CRITICAL (CVSS 9.2) |
| **Product** | AVideo through 29.0 |
| **Description** | Authorization bypass in Meet plugin uploadRecordedVideo.json.php allows full account takeover including admin session hijacking via crafted filename. |
| **Published** | June 20, 2026 |
| **CSOAI Relevance** | MEDIUM - Video platform; could affect AI-generated video content pipelines |

**Source:** https://feedly.com/cve/severity/9-10

---

### 3.6 CVE-2026-56341 - AVideo Payment Plugin Data Exposure
| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Product** | AVideo through 26.0 |
| **Description** | Multiple unauthenticated list.json.php endpoints expose PayPal tokens, Authorize.Net webhooks, Bitcoin transaction records. |
| **Published** | June 20, 2026 |
| **CSOAI Relevance** | MEDIUM - Payment data exposure in video platforms |

---

### 3.7 CVE-2026-56304 - Picklescan Unsafe Pickle Deserialization
| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Product** | picklescan < 1.0.1 |
| **Description** | Unsafe pickle deserialization allows unauthenticated attackers to create arbitrary zero-byte files via logging.FileHandler. Can bypass RCE blocklists. |
| **Published** | June 20, 2026 |
| **CSOAI Relevance** | HIGH - Picklescan is used to scan pickle files in ML/AI model loading pipelines |

---

### 3.8 CVE-2026-56276 - Flowise Mass Assignment Password Bypass
| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Product** | Flowise < 3.1.2 |
| **Description** | PUT /api/v1/user endpoint allows authenticated users to directly modify credential field without validation, bypassing password change verification. |
| **Published** | June 20, 2026 |
| **CSOAI Relevance** | HIGH - Flowise is a popular open-source LLM workflow builder |

---

### 3.9 CVE-2026-56267 - Flowise Forgot Password PII Exposure
| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Product** | Flowise < 3.0.13 |
| **Description** | POST /api/v1/account/forgot-password returns full user objects including PII to unauthenticated attackers. |
| **Published** | June 20, 2026 |
| **CSOAI Relevance** | HIGH - LLM workflow platform user enumeration and PII leak |

---

### 3.10 Capgo Authorization/Authentication Vulnerabilities (Multiple CVEs)
| CVE | Severity | Description | Published |
|-----|----------|-------------|-----------|
| CVE-2026-56081 | CRITICAL (9.3) | Authentication logic flaw: attacker can pre-register account with victim's email, enable 2FA, lock out legitimate user | June 19, 2026 |
| CVE-2026-56216 | HIGH | App-limited API keys can mint unrestricted keys via empty limits | June 20, 2026 |
| CVE-2026-56215 | HIGH | SSO provisioning email takeover - mutable email used as account-merge key | June 20, 2026 |
| CVE-2026-56214 | HIGH | Unauthenticated org enumeration via billing status endpoints | June 20, 2026 |
| CVE-2026-56227 | MEDIUM | SSRF in webhook URL validation allows loopback/internal addresses | June 20, 2026 |
| CVE-2026-56218 | MEDIUM | EXIF metadata (GPS geolocation) not stripped from uploaded images | June 20, 2026 |
| CVE-2026-56282 | MEDIUM | Unauthenticated /replication endpoint exposes PostgreSQL replication telemetry | June 20, 2026 |
| CVE-2026-56235 | MEDIUM | PostgREST RPC functions allow cross-tenant usage telemetry disclosure | June 20, 2026 |

**CSOAI Relevance:** MEDIUM - Capgo is a mobile app update platform; AI-powered mobile apps may use it

**Source:** https://www.tenable.com/cve/newest

---

### 3.11 Additional CVEs Published June 20, 2026
| CVE | Severity | Product | Description |
|-----|----------|---------|-------------|
| CVE-2026-56355 | LOW | GNU Savannah Savane <=3.17 | Untrusted data used as part of authorization |
| CVE-2026-56347 | MEDIUM | AVideo TopMenu <=26.0 | Stored XSS in menu item rendering |
| CVE-2026-56346 | MEDIUM | AVideo <=25.0 | Authentication bypass in PGP decryption |
| CVE-2026-56342 | MEDIUM | AVideo <=27.0 | SSRF in plugin/Live/test.php |
| CVE-2026-56332 | MEDIUM | Capgo <12.128.2 | Open redirect in confirm-signup |
| CVE-2026-56330 | MEDIUM | Capgo <12.128.2 | Open redirect in Stripe endpoints |
| CVE-2026-56325 | LOW | Capgo <12.128.2 | SQL wildcard confusion via ILIKE |
| CVE-2026-56319 | MEDIUM | Capgo <12.128.2 | App ID enumeration via differential errors |
| CVE-2026-56317 | LOW | Nuxt <4.4.7 | XSS in NoScript component |
| CVE-2026-56307 | MEDIUM | Capgo <12.128.12 | Broken cursor pagination in /private/devices |
| CVE-2026-56295 | MEDIUM | Capgo <12.128.2 | Webhook management auth bypass |
| CVE-2026-56294 | MEDIUM | capacitor-native-biometric <12.128.2 | Biometric auth bypass via CryptoObject hook |
| CVE-2026-12673 | MEDIUM | Liquidfiles <4.2.12 | Admin privilege escalation across domains |

---

## 4. AI MODEL JAILBREAK: ANTHROPIC FABLE 5 / PLINY (June 9-12, 2026)

**CSOAI RELEVANCE: CRITICAL - AI Safety / Model Governance**

| Field | Detail |
|-------|--------|
| **Event** | "Pliny the Liberator" jailbreaks Claude Fable 5 within 48 hours of launch; US government issues export control order |
| **Timeline** | June 9: Fable 5 launches; June 10: Pliny publishes jailbreak; June 12: US government orders shutdown |
| **Technique** | Multi-agent "Pack Hunt" - decomposition/recomposition using Unicode, homoglyphs, Cyrillic substitution, long-context framing |
| **Output** | Stack buffer overflow exploitation guidance, methamphetamine synthesis (Birch reduction), 120K character system prompt leak |

**Key Details:**
- Pliny used decomposition: broke harmful requests into innocuous sub-questions, then reassembled answers
- Published step-by-step stack buffer overflow exploitation for x86 Linux (disabling ASLR, writing vulnerable C code)
- US Commerce Department issued export control order blocking foreign-national access
- Anthropic blocked ALL global access to Fable 5 and Mythos 5 (not just foreign nationals)
- Amazon researchers reportedly found the jailbreak and took it to Commerce Department first (per WSJ)
- Anthropic had been asked to delay launch and refused

**Industry Impact:**
- First time an export control order pulled a commercial AI model offline globally
- Pentagon had already blacklisted Anthropic in March 2026 over supply chain/safety disputes
- Anthropic's annualized revenue hit $47B; IPO planned
- Validates concerns about AI model safety vs. capability tradeoffs

**Sources:**
- SecurityWeek: https://www.securityweek.com/anthropic-disputes-fable-5-ai-jailbreak/
- Gotchaa Lab: https://gotchaa-lab.com/blog/2026-06-13-fable-5-jailbreak-ai-safety-limits
- Meteoraweb: https://meteoraweb.com/en/news/anthropic-blocks-claude-fable-5-and-mythos-5-pliny-the-liberators-jailbreak-triggers-government-order-what-enterprises-must-do
- CNBC/Reuters: Anthropic Executives: Pentagon blacklisting could cut 2026 revenue by multiple billions

---

## 5. AI CODING TOOL VULNERABILITY: CVE-2026-35603 (June 17, 2026)

**CSOAI RELEVANCE: CRITICAL - AI Developer Tools / Privilege Escalation**

| Field | Detail |
|-------|--------|
| **CVE** | CVE-2026-35603 |
| **Severity** | Critical (Privilege Escalation) |
| **Products** | Claude Code (Anthropic), Cursor, OpenAI Codex CLI, Google Gemini CLI |
| **Disclosed** | June 17, 2026 |
| **Root Cause** | World-writable C:\ProgramData\ directories trusted for machine-wide configuration |

**Technical Details:**
- Low-privileged attacker creates malicious config in world-writable ProgramData directory
- When ANY user (including admin) launches the tool, malicious hook/notify command executes in their context
- **Claude Code:** `C:\ProgramData\ClaudeCode\managed-settings.json` with hooks -> CVE-2026-35603 assigned by Anthropic (FIXED)
- **Cursor:** `C:\ProgramData\Cursor\hooks.json` -> UNRESOLVED at publication (no formal reply after 5 months)
- **OpenAI Codex CLI:** `C:\ProgramData\openai\codex\config.toml` -> can disable sandbox + remove approval prompts simultaneously -> UNRESOLVED
- **Google Gemini CLI:** No conclusive response at publication

**Vendor Response Comparison:**
| Vendor | Response | Status |
|--------|----------|--------|
| Anthropic | Assigned CVE, deprecated ProgramData path, moved to protected Program Files, proactively emailed customers | FIXED |
| Cursor | No formal reply, not properly triaged | UNRESOLVED |
| OpenAI | Triaged low severity, moved to Unresolved | UNRESOLVED |
| Google | No conclusive response | UNKNOWN |

**Source:** https://cymulate.com/blog/cve-2026-35603-ai-coding-tools-privilege-escalation/

---

## 6. CISA ALERTS & KEV UPDATES (June 2026)

### 6.1 CISA KEV New Entries (June 16, 2026)
| CVE | Severity | Product | Action Due | Notes |
|-----|----------|---------|------------|-------|
| CVE-2026-48907 | CRITICAL (10.0) | Widget Factory Joomla Content Editor | June 19, 2026 | Unauthenticated PHP code upload |
| CVE-2026-11645 | HIGH (8.8) | Google Chromium V8 | June 23, 2026 | OOB read/write RCE via crafted HTML |
| CVE-2026-7473 | MEDIUM (6.9) | Arista EOS | June 23, 2026 | Tunnel decapsulation vulnerability |
| CVE-2026-20245 | HIGH (7.8) | Cisco Catalyst SD-WAN Manager | June 23, 2026 | Command injection as root |
| CVE-2026-42271 | HIGH (8.8) | BerriAI LiteLLM | June 22, 2026 | Command injection - authenticated user to RCE |
| CVE-2026-50751 | CRITICAL (9.3) | Check Point Security Gateway | June 11, 2026 | IKEv1 auth bypass for VPN - known ransomware use |
| CVE-2026-28318 | HIGH (7.5) | SolarWinds Serv-U | June 19, 2026 | DoS via Content-Encoding: deflate |
| CVE-2026-48027 | CRITICAL (9.8) | Nx Console | June 10, 2026 | Embedded malicious code, credential harvesting |

**Source:** https://cvefeed.io/cisakev/cisa-known-exploited-vulnerability-catalog

### 6.2 CISA/FBI Joint Warning - Fuel Tank Monitoring Systems
- Date: June 4, 2026
- Target: Internet-exposed automatic tank gauge (ATG) systems
- Sectors: Energy, agriculture, transportation
- Agencies: CISA, FBI, NSA, DOE
- **CSOAI Relevance:** HIGH - OT/ICS systems increasingly targeted

---

## 7. MICROSOFT PATCH TUESDAY JUNE 2026 (June 9, 2026)

**Summary:** 206 vulnerabilities patched, including 3 publicly disclosed zero-days and 37 Critical.

### Zero-Day / Publicly Disclosed Vulnerabilities
| CVE | Severity | CVSS | Product | Description |
|-----|----------|------|---------|-------------|
| CVE-2026-45586 | Important | 7.8 | Windows CTFMON | Elevation of Privilege (link following), publicly disclosed, MS assesses exploitation "more likely" |
| CVE-2026-50507 | Important | 6.8 | Windows BitLocker | Security feature bypass, physical access, PoC exists, MS assesses "more likely" |
| CVE-2026-49160 | Important | 7.5 | HTTP.sys | DoS via HTTP/2 uncontrolled resource consumption, publicly disclosed |
| CVE-2026-47291 | Critical | 9.8 | HTTP.sys | RCE via integer overflow + heap buffer overflow. Default MaxRequestBytes=16KB not impacted |

### Critical AI-Related Vulnerabilities
| CVE | Severity | CVSS | Product | Description |
|-----|----------|------|---------|-------------|
| CVE-2026-45497 | Critical | 7.7 | Microsoft M365 Copilot | RCE via command injection. Cloud-fixed, no customer action |
| CVE-2026-42824 | Critical | 6.5 | Microsoft M365 Copilot | Info disclosure via command injection. Cloud-fixed |
| CVE-2026-47644 | Critical | 6.5 | Copilot Chat (Edge) | Info disclosure via injection flaw. Cloud-fixed |
| CVE-2026-47655 | Critical | 6.5 | Microsoft Graph | Info disclosure - exposure of sensitive org data. Cloud-fixed |

### Other Notable Critical CVEs
| CVE | Severity | CVSS | Product |
|-----|----------|------|---------|
| CVE-2026-45657 | Critical | 9.8 | Windows Kernel | RCE via TCP/IP processing (use-after-free + heap overflow) |
| CVE-2026-26142 | Critical | 9.8 | Nuance PowerScribe | RCE via deserialization (healthcare) |
| CVE-2026-45607 | Critical | 8.4 | Windows Hyper-V | RCE via guest-to-host (out-of-bounds read) |
| CVE-2026-45641 | Critical | 8.4 | Windows Hyper-V | RCE via guest-to-host (type confusion) |
| CVE-2026-47288 | Critical | 7.1 | Windows Kerberos KDC | RCE via integer overflow (adjacent network) |
| CVE-2026-45461 | Critical | 8.4 | Microsoft Office | RCE via use-after-free (Preview Pane attack vector) |
| CVE-2026-45463 | Critical | 8.4 | Microsoft Office | RCE via integer underflow (Preview Pane) |
| CVE-2026-42987 | Critical | 8.1 | Windows Deployment Services | RCE via use-after-free (TFTP, race condition) |
| CVE-2026-44803 | Critical | 7.8 | Windows Graphics | RCE via integer overflow (Preview Pane) |

**Source:** https://www.crowdstrike.com/en-us/blog/patch-tuesday-analysis-june-2026/
https://www.thezdi.com/blog/2026/6/9/the-june-2026-security-update-review

---

## 8. AI SECURITY THREATS & PROMPT INJECTION (June 2026)

### 8.1 Fake Context Alignment - Gemini Voice Assistant Attack
- **Date:** Disclosed June 8, 2026 (Check Point Threat Intel Report)
- **Technique:** Notification-based prompt injection manipulating Google's Gemini voice assistant
- **Impact:** Hidden authorization prompts, device control, auto-joining Zoom calls, cross-device memory poisoning
- **Response:** Google deployed classifier updates after disclosure

### 8.2 Meta AI Chatbot Account Takeover
- **Date:** Reported June 8, 2026
- **Attack:** Attackers used Meta's AI support chatbot to seize Instagram accounts
- **Root Cause:** AI agents granted account recovery authority without identity verification checks

### 8.3 OpenClaw AI Agent Phishing Susceptibility
- **Date:** June 10, 2026
- **Finding:** OpenClaw email AI agent found falling for phishing attacks, spilling user data
- **Significance:** AI agents as vulnerable as human users to social engineering

### 8.4 LLM-Driven EDR Evasion Lab
- **Date:** June 8, 2026 (Check Point)
- **Finding:** Researchers demonstrated AI-enabled EDR evasion where threat actors automate malware development and testing against Sophos, CrowdStrike, and Microsoft Defender using LLM agents
- **Significance:** AI-driven autonomous attack development and testing

### 8.5 Prompt Injection in 2026 - OWASP LLM01
- Prompt injection remains #1 on OWASP Top 10 for LLM Applications
- Agentic AI dramatically expands attack surface: agents don't just read text, they act on it
- Indirect prompt injection via emails, documents, web pages, database records
- **Key principle:** "Assume the model will be compromised and design for containment"

**Source:** https://www.kunalganglani.com/blog/prompt-injection-2026-owasp-llm-vulnerability
https://research.checkpoint.com/2026/8th-june-threat-intelligence-report/

---

## 9. RANSOMWARE: Gentlemen RaaS + EDR Killers (June 18, 2026)

**CSOAI RELEVANCE: HIGH - Ransomware Evolution**

| Field | Detail |
|-------|--------|
| **Group** | The Gentlemen ransomware-as-a-service (RaaS) |
| **Disclosed** | June 18, 2026 |
| **Innovation** | Actively developing and maintaining suite of EDR killers |
| **Growth** | Fastest-growing RaaS operation, outcompeting rivals on revenue share |

**Key Technical Details:**
- Multiple EDR killers to disable endpoint detection and response
- Not technically sophisticated but economically innovative
- Revenue share model attracting more affiliates than competitors

**Source:** https://www.bleepingcomputer.com/news/security/gentlemen-ransomware-uses-multiple-edr-killers-to-disable-defenses/

---

## 10. M&A / STARTUP NEWS (June 2026)

### 10.1 Accenture OT Cybersecurity Acquisitions - $4.1B
- **Date:** June 18, 2026
- **Deals:**
  - Majority stake in Dragos (valued at $3.25B) - industrial/OT cybersecurity
  - Full acquisition of runZero - attack surface management
  - Full acquisition of NetRise - OT cybersecurity
- **CSOAI Relevance:** Major consolidation in OT/ICS security for critical infrastructure

### 10.2 Cisco Acquires WideField Security
- **Date:** June 18, 2026
- **Purpose:** Boost Splunk's Agentic SOC with identity lifecycle security
- **Focus:** Human and non-human identity discovery, session intelligence, AI agent security
- **Context:** Cisco's 3rd cybersecurity M&A deal of 2026 (after Galileo and Astrix)

### 10.3 Dream Raises $260M at $3B Valuation
- **Date:** June 18, 2026
- **Company:** Israeli startup providing sovereign AI and cyber defenses for governments and critical infrastructure
- **Significance:** Validates sovereign AI security market

### 10.4 SailPoint to Acquire Entro - ~$200M
- **Date:** Reported June 2026
- **Focus:** Non-human identity secrets management

### 10.5 1Password Acquires Apono - $250M-$300M
- **Date:** Reported June 2026
- **Focus:** Just-in-time access and permissions management

### 10.6 Cisco Warns SD-WAN Zero-Day Exploited
- **Date:** June 19, 2026
- **CVE:** No patch available; command injection vulnerability in SD-WAN actively exploited

**Source:** https://www.securityweek.com/
https://www.cybersecuritydive.com/

---

## 11. OTHER BREACHES & INCIDENTS

### 11.1 Nintendo / TinyPulse Data Theft
- **Date:** June 18, 2026
- **Incident:** Threat actors stole survey data from third-party TinyPulse service used by Nintendo of America
- **Impact:** Internal survey data stolen; Nintendo systems not compromised

### 11.2 SoFi Hong Kong Third-Party Breach
- **Date:** June 9, 2026
- **Incident:** Database breach at third-party vendor containing customer information

### 11.3 ShapedPlugin Supply Chain Attack
- **Date:** June 18, 2026
- **Incident:** Multiple WordPress plugins compromised; update flow hacked to infect paying customers

### 11.4 Red Hat npm Supply Chain Attack
- **Date:** June 2026
- **Incident:** Dozens of Red Hat npm packages targeted; variant of Mini Shai-Hulud involved

### 11.5 Operation Endgame - SocGholish Botnet Takedown
- **Date:** June 18, 2026
- **Result:** 15,000 WordPress sites cleaned, 106 C&C servers/domains taken down, linked to Evil Corp

### 11.6 Splunk Enterprise Actively Exploited
- **CVE:** CVE-2026-20253
- **Severity:** Critical (OS command injection in AI Toolkit)
- **Action:** CISA gave federal agencies 3 days to patch (by Sunday)
- **Status:** Exploited in attacks days after disclosure

### 11.7 DentaQuest / ShinyHunters Breach
- **Date:** Reported June 8, 2026
- **Impact:** 2.6 million accounts exposed (names, emails, government IDs, health insurance)

### 11.8 Dashlane Password Manager Attack
- **Date:** Reported June 8, 2026
- **Method:** Threat actors brute-forced 2FA codes to register unauthorized devices
- **Impact:** <20 users' encrypted password vaults downloaded

### 11.9 UN World Food Programme Gaza Breach
- **Date:** Reported June 8, 2026
- **Impact:** ~600,000 Palestinian households' data exposed (names, IDs, phone numbers, locations)

### 11.10 Hola Browser Supply Chain Compromise
- **Date:** Reported June 8, 2026
- **Impact:** Unauthorized cryptominer pushed to ~0.1% of users via supply chain

---

## 12. POLICY / GOVERNMENT

### 12.1 Trump Memo - National Security Systems Security
- **Date:** June 5, 2026
- **Key Points:**
  - Aggressive timelines for securing sensitive systems
  - NSA designated as National Manager
  - Committee on National Security Systems revived
  - 60 days: CNSS roadmap
  - 90 days: Review/update policies
  - 90 days: Cloud hosting guidance for national security systems

### 12.2 NSPM-11 - AI Adoption for National Security
- **Date:** June 5, 2026
- **Purpose:** Accelerate AI adoption across national security systems
- **Context:** Response to foreign adversaries using AI to speed up cyber campaigns

### 12.3 Trump EO on AI Model Access
- **Date:** June 2026
- **Directive:** Early government access to powerful AI models
- **Context:** Reversal from previous administration's repudiation of government AI reviews

### 12.4 CISA Chief on AI Executive Order
- **Date:** June 19, 2026
- **Statement:** Implementation starting soon despite agency depletion from workforce cuts

### 12.5 French President Macron on AI Regulation
- **Date:** June 18, 2026
- **Call:** Urged wealthy democracies to cooperate on advanced AI regulation; requested US share cutting-edge AI

---

## METHODOLOGY & SOURCES

**Sources Consulted:**
- Tenable CVE Feed (https://www.tenable.com/cve/newest)
- CISA KEV Catalog (https://cvefeed.io/cisakev/)
- VulnCheck Advisories (https://www.vulncheck.com/)
- CrowdStrike Patch Tuesday Analysis
- BleepingComputer
- The Hacker News
- SecurityWeek
- Check Point Research Threat Intelligence
- HKCERT Security News
- Help Net Security
- Cymulate Research Labs
- Various vendor security advisories

**Search Queries Used:**
- CVE disclosed June 2026
- AI security vulnerability June 2026
- data breach June 20 2026
- ransomware attack June 2026
- AI safety incident June 2026
- prompt injection attack June 2026
- CISA alert June 2026
- NVD new CVE June 2026
- major cyber attack June 2026
- AI model jailbreak June 2026
- cybersecurity news June 21 2026
- FortiBleed Fortinet credential leak
- Klue OAuth breach Icarus
- Anthropic Fable 5 jailbreak Pliny

---

*Report compiled: June 21, 2026*
*Next update: As new intelligence emerges*
