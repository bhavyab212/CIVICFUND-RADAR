# CivicFund Radar — System Architecture & Implementation Specifications

## 1. System Overview

**CivicFund Radar** is an evidence-first funding discovery assistant and intelligent web platform tailored for small non-profits, community organizations, and grassroots climate coalitions. The system solves the chronic challenge of finding non-dilutive climate funding across disparate federal, state, and foundation sources while eliminating hallucinations, outdated deadlines, and disqualifying eligibility traps.

CivicFund Radar combines:
1. **Live Web Intelligence:** **TinyFish Search** discovers active candidate opportunities across public agencies, and **TinyFish Fetch** extracts structured NOFO facts and quote spans.
2. **Deterministic Ledger & Verification:** A pure-Go SQLite FTS5 store indexes opportunities, runs date math (`AssessActivity`), enforces applicant and geographic constraints (`AssessFit`), and tracks negative evidence (`BuildCoverage`).
3. **Responsive Web Dashboard:** A clean, accessible light-themed interface (`web/index.html`) served directly by the built-in HTTP server (`civicfund-radar serve`), featuring live KPI cards, interactive opportunity cards, and a slide-out evidence audit drawer.
4. **Upstream Agent Integration:** OpenProse and AI coding agents can consume structured `ResearchPacket` JSON payloads for automated executive briefings.

---

## 2. High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph Intake["1. Intake & Profiling"]
        A[Community Climate Organization] --> B[Organization Profile Intake\nweb/index.html & ProfileRequest]
        B --> C[Research Assignment JSON\nschemas/research-assignment.schema.json]
    end

    subgraph Discovery["2. Live Web Discovery & Harvesting Engine"]
        C --> D[TinyFish Search API\nLive Query Generation & Discovery]
        D --> E[TinyFish Fetch API\nOfficial NOFO Page & Quote Extraction]
        
        C --> F[Federal Registry Collectors]
        F --> F1[Grants.gov REST API & Daily XML Extract]
        F --> F2[Federal Register Notices API]
        F --> F3[137 Embedded Agency Feeds & Sources]
    end

    subgraph Core["3. Deterministic Go Core & SQLite Ledger"]
        E --> G[DedupeKey Normalizer & Store]
        F1 --> G
        F2 --> G
        F3 --> G
        G --> H[(SQLite FTS5 Local Ledger\nmodernc.org/sqlite)]
        
        H --> I[Hybrid Retrieval Engine\nSQLite FTS5 + usearch vector fallback]
        I --> J[Deterministic Evaluation Rules (no_llm: true)]
        
        subgraph Rules["Evaluation Suite"]
            J1[AssessActivity: Excludes Past Deadlines]
            J2[AssessFit: 501c3 & Justice40 Priority Matching]
            J3[EstimateEffort: Application Complexity Heuristics]
            J4[BuildCoverage: Explicit Negative Evidence]
            J5[SQL AST Guard: query_only = ON]
        end
        J --> Rules
    end

    subgraph Output["4. User Interfaces & Decision Support"]
        Rules --> K[Interactive Web Dashboard\nhttp://localhost:8080/ & /shortlist]
        Rules --> L[Research Packet JSON\nschemas/research-packet.schema.json]
        
        K --> M[Evidence Audit Drawer\nVerbatim Citations & Grants.gov Links]
        L --> N[Upstream Agent Synthesis\nOpenProse Executive Briefing Memo]
    end

    classDef core fill:#e8f5e9,stroke:#059669,stroke-width:2px;
    classDef storage fill:#e3f2fd,stroke:#0284c7,stroke-width:2px;
    classDef web fill:#f0fdf4,stroke:#10b981,stroke-width:2px;

    class A,B,C,D,E,F,F1,F2,F3,G,I,J,Rules,J1,J2,J3,J4,J5,K,L,M,N core;
    class H storage;
    class K,M web;
```

---

## 3. Subsystem Specifications

### 3.1 Web Dashboard & Application Server
- **Frontend Layer:** Built with clean HTML5, CSS3, and ES6+ (`web/index.html`). Implements an accessible light theme (#F8FAFC background, #059669 emerald primary, slate typography) with zero external build step dependencies.
- **Embedded Web Server:** `internal/civicfundradar/webserver.go` provides:
  - `GET /`: Serves the responsive single-page web dashboard.
  - `POST /api/opportunities/search`: Ingests `ProfileRequest` JSON, executes live discovery and rule matching, and returns typed `DiscoveryResponse`.
  - `GET /api/health`: Provides self-diagnostic telemetry (feeds count, sources count, active mode).
- **CLI Command:** `civicfund-radar serve --port 8080` launches the local web server and opens immediate browser access.

### 3.2 TinyFish Live Engine
- **Module:** `internal/civicfundradar/tinyfish.go`
- **Search Capabilities:** Constructs targeted keyword queries based on organization focus areas, geographic boundaries, and project summaries; queries the TinyFish Search API for live solicitation URLs.
- **Fetch & Extraction:** Calls the TinyFish Fetch API to retrieve structured markdown of official funder NOFOs; extracts verified deadline spans, eligible entity categories, and cost-share requirements.
- **Graceful Fallback:** When a `TINYFISH_API_KEY` is not set in the environment, the client gracefully falls back to the embedded public registry and official government endpoints (Grants.gov API and Federal Register), ensuring zero-downtime offline execution.

### 3.3 Deterministic Rule Evaluation (no_llm: true)
Located in `internal/civicfundradar/research.go` and `tinyfish.go`:
1. **`AssessActivity`:** Performs date math against `time.Now().UTC()`. Past-due opportunities are marked `inactive` and excluded by default unless `--include-inactive` is specified.
2. **`AssessFit`:** Calculates preliminary fit scores (0–100) and maps them to:
   - **`likely_fit`:** Verified 501(c)(3) applicant eligibility + direct focus area alignment + 0% cost-share or verified waivers.
   - **`possible_fit`:** Project theme aligns, but cost-share or sub-tier partner criteria require funder confirmation.
   - **`mismatch`:** Explicit constraint exclusion (e.g., commercial equity or for-profit requirement).
   - **`unknown`:** Insufficient published evidence in the notice text.
3. **`BuildCoverage` & Negative Evidence:** Verifies not just what matched, but explicitly records monitored lanes with zero hits (e.g., `"ARPA-E: checked_no_match"`), preventing false assumptions.

### 3.4 Local SQLite FTS5 Ledger
- **Driver:** Pure Go `modernc.org/sqlite v1.50.0` (zero CGO dependencies).
- **Full-Text Indexing:** SQLite FTS5 virtual tables index program titles, summaries, and eligibility statements.
- **Deduplication:** `DedupeKey` hashing ensures multiple feed entries or repeated search hits for the same grant number are unified into a single revisioned opportunity record.

### 3.5 Security Controls & Hardening
- **SQL AST Injection Guard:** `internal/cli/helpers.go` and `sql.go` enforce `PRAGMA query_only = ON;` and parse tokens outside string literals to reject all mutating keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `REPLACE`), preventing CTE DML write bypasses.
- **Secret Isolation:** API keys remain strictly server-side (`.env` excluded via `.gitignore`) and are never leaked into browser bundles or client-side responses.
- **Bounded Resource Consumption:** HTTP client requests are capped at 20-second timeouts, and ZIP/XML ingestion streams are bounded to prevent memory exhaustion.

---

## 4. Architecture Decision Records (ADRs)

### ADR-0001: Evidence-First Non-Dilutive Grant Engine
- **Status:** Accepted (2026-05)
- **Decision:** Never execute LLM inference inside the core CLI or data ledger. All retrieval and rule matching must be deterministic, auditable, and reproducible.

### ADR-0002: CivicFund Radar Full-Stack Implementation
- **Status:** Accepted (2026-10)
- **Decision:** Build a complete, functional full-stack solution featuring a native light-themed web interface (`web/index.html`), embedded Go HTTP server (`civicfund-radar serve`), real TinyFish Search & Fetch client, and climate non-profit specialization.
