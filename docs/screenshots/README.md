# Visual Assets and Interface Showcase

This directory contains visual documentation for **CivicFund Radar**. All assets depict the modern, light-themed web application and architecture designed for community climate organizations.

---

## Visual Catalog

### 1. `01-main-screen.png` — Main Web Dashboard & Grant Discovery Overview
- **Path:** `docs/screenshots/01-main-screen.png`
- **Interface Screen:** Web Application Main Dashboard (`https://app.civicfundradar.org/`)
- **Key Elements:**
  - Clean light SaaS theme with emerald green (`#059669`) and slate navy typography.
  - Three real-time KPI metric cards: **Verified Active Grants (24)**, **Total Available Funding ($14.2M)**, and **Average Match Rate (88%)**.
  - Interactive search header with focus-area filtering and live query input.
  - Discovered opportunity cards with 'Likely Fit' and 'Possible Fit' badges, verified funder links, and 'Inspect Evidence' triggers.
- **Role:** Demonstrates the primary working interface for community organizations discovering verified climate grants.

---

### 2. `02-organization-profile.png` — Organization Profile & Matching Criteria Intake
- **Path:** `docs/screenshots/02-organization-profile.png`
- **Interface Screen:** Organization Intake Portal (`https://app.civicfundradar.org/organization`)
- **Profile Demonstrated:** *Harbor Community Climate Alliance*, a frontline 501(c)(3) environmental justice coalition.
- **Key Elements:**
  - Left Column: Organization name, verified 501(c)(3) entity badge, Great Lakes/Coastal region selection, and **Justice40 Disadvantaged Community Entity** active toggle.
  - Right Column: Targeted focus area tags (*Community Microgrids*, *Urban Heat Island Mitigation*, *Clean Energy Transition*, *Environmental Justice*, *Nature-Based Solutions*).
  - Funding Constraints: Non-dilutive only, exclusion of commercial equity/SBIR requirements, minimum award threshold ($250,000).
  - Action Trigger: **Run AI Radar Discovery (TinyFish Live Engine)** button.
- **Role:** Illustrates the structured intake pipeline that configures deterministic matching rules.

---

### 3. `03-opportunity-shortlist.png` — Discovered Opportunity Shortlist & AI Fit Analysis
- **Path:** `docs/screenshots/03-opportunity-shortlist.png`
- **Interface Screen:** Shortlist View (`https://app.civicfundradar.org/shortlist`)
- **Key Elements:**
  - Filter tabs: **All Matches (18)**, **Likely Fit (8)**, **Possible Fit (6)**, **Under Review (4)**.
  - Sort by **Fit Score (Highest)**.
  - Multi-card grid displaying:
    1. *EPA Environmental Justice Community Change Grant (EJCPS)* — **Likely Fit • 96% Match**, Deadline Nov 21, 2026, $500K – $2M, 0% cost-share.
    2. *DOE Clean Energy to Communities (C2C)* — **Likely Fit • 91% Match**, Deadline Dec 15, 2026, $250K – $1M.
    3. *NOAA Climate Resilience Regional Challenge* — **Possible Fit • 78% Match**, Jan 10, 2027, with amber note: *“Cost-share requirement ambiguous in notice”*.
    4. *USDA Forest Service Urban Community Forestry* — **Likely Fit • 89% Match**, Mar 1, 2027, $100K – $500K.
  - Provenance timestamps (*“Checked 12m ago via TinyFish Fetch”*).
- **Role:** Demonstrates the ranked opportunity shortlist with transparent eligibility indicators.

---

### 4. `04-evidence-detail.png` — Official Evidence & Provenance Audit Drawer
- **Path:** `docs/screenshots/04-evidence-detail.png`
- **Interface Screen:** Slide-Out Evidence Drawer
- **Grant Audited:** *EPA Environmental Justice Community Change Grant (EJCPS)* (NOFO #EPA-R-OAR-EJ-24-01)
- **Key Elements:**
  - Verification Badge: **Authoritative Source Verified via TinyFish Fetch**.
  - Source Information: Official EPA link, opportunity number, checked timestamp (Oct 22, 2026 09:14 UTC).
  - Verbatim NOFO Evidence Spans:
    - *Nonprofit Status:* Quoted excerpt from EPA NOFO Sec. III.A.1 (Eligible Applicants, p. 8).
    - *Justice40 Priority:* 100% allocation to disadvantaged communities verified from NOFO Sec. I.B.
    - *Cost-Share Requirement:* Confirmed 0% required for Track II community awards.
  - Next Action Guidance: Funder portal link and *Export Evidence Brief (PDF/Markdown)*.
- **Role:** Proves how CivicFund Radar eliminates hallucinations by grounding every eligibility claim in official text.

---

### 5. `05-architecture-flow.png` — System Architecture & Data Flow Infographic
- **Path:** `docs/assets/05-architecture-flow.png`
- **Asset Type:** End-to-End System Architecture Infographic
- **Pipeline Breakdown:**
  1. *Intake & Profile:* Organization context, 501(c)(3) status, Justice40 criteria, focus areas.
  2. *Live Web Discovery & Verification Engine:* TinyFish Search API for live discovery, TinyFish Fetch API for structured NOFO retrieval, Grants.gov and Federal Register integration.
  3. *Deterministic Match & Provenance Engine:* High-performance Go CLI core, SQLite FTS5 ledger, rule-based date math, nonprofit constraints, and negative evidence detection.
  4. *Decision Support & Shortlist:* Source-linked shortlist, Likely/Possible fit ranking, evidence drawer, PDF/Markdown export.
- **Role:** Provides technical reviewers and evaluators with a complete, publication-grade architectural overview.
