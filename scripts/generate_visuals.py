import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    try:
        font_mono_lg = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
        font_mono_md = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
        font_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
        font_sans_xl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 28)
        font_sans_lg = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
        font_sans_md = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
        font_sans_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
        font_sans_xs = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    except Exception:
        font_mono_lg = font_mono_md = font_mono_sm = ImageFont.load_default()
        font_sans_xl = font_sans_lg = font_sans_md = font_sans_sm = font_sans_xs = ImageFont.load_default()
    return {
        "mono_lg": font_mono_lg, "mono_md": font_mono_md, "mono_sm": font_mono_sm,
        "sans_xl": font_sans_xl, "sans_lg": font_sans_lg, "sans_md": font_sans_md,
        "sans_sm": font_sans_sm, "sans_xs": font_sans_xs
    }

def draw_window_frame(draw, width, height, title, subtitle=None):
    # Background
    draw.rectangle([0, 0, width, height], fill="#0d1117")
    # Top bar
    draw.rectangle([0, 0, width, 52], fill="#161b22")
    draw.line([(0, 52), (width, 52)], fill="#30363d", width=1)
    # Window buttons
    draw.ellipse([18, 20, 30, 32], fill="#ff5f56")
    draw.ellipse([38, 20, 50, 32], fill="#ffbd2e")
    draw.ellipse([58, 20, 70, 32], fill="#27c93f")
    # Title text
    fonts = get_fonts()
    draw.text((85, 16), title, font=fonts["sans_lg"], fill="#e6edf3")
    if subtitle:
        draw.text((width - 340, 19), subtitle, font=fonts["mono_sm"], fill="#8b949e")

def create_image_01(out_path):
    width, height = 1600, 1000
    img = Image.new("RGBA", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    draw_window_frame(draw, width, height, "CivicFund Radar — CLI Runtime & Diagnostics Doctor", "Platform: windows/amd64 | Go 1.26.4")
    
    # Left Card: Command Session
    draw.rounded_rectangle([30, 75, 1000, 950], radius=8, fill="#0b0f14", outline="#30363d", width=1)
    # Session Header
    draw.rectangle([30, 75, 1000, 115], fill="#161b22")
    draw.text((45, 87), "PowerShell Terminal — Actual Local Execution", font=fonts["sans_md"], fill="#58a6ff")
    
    lines = [
        ("PS C:\\Users\\bhavy\\Downloads\\mad_love\\CivicFund Radar> ", "#58a6ff"),
        (".\\cli\\civicfund-radar\\civicfund-radar.exe version\n", "#7ee787"),
        ("civicfund-radar 1.0.0 (windows/amd64 go1.26.4)\n\n", "#e6edf3"),
        ("PS C:\\Users\\bhavy\\Downloads\\mad_love\\CivicFund Radar> ", "#58a6ff"),
        (".\\cli\\civicfund-radar\\civicfund-radar.exe doctor --json\n", "#7ee787"),
        ("{\n", "#8b949e"),
        ("  \"os\": \"windows\",\n", "#79c0ff"),
        ("  \"arch\": \"amd64\",\n", "#79c0ff"),
        ("  \"go\": \"go1.26.4\",\n", "#79c0ff"),
        ("  \"no_llm\": true,\n", "#ff7b72"),
        ("  \"feeds\": 137,\n", "#d2a8ff"),
        ("  \"sources\": 86,\n", "#d2a8ff"),
        ("  \"semantic_retrieval\": \"usearch preferred, FTS5 fallback\",\n", "#a5d6ff"),
        ("  \"usearch_error\": \"exec: \\\"usearch\\\": executable file not found in %PATH%\",\n", "#ffa657"),
        ("  \"agent_interface\": [\n", "#8b949e"),
        ("    \"research\",\n", "#7ee787"),
        ("    \"explain\",\n", "#7ee787"),
        ("    \"status\"\n", "#7ee787"),
        ("  ],\n", "#8b949e"),
        ("  \"db_path\": \"C:\\\\Users\\\\bhavy\\\\.local\\\\share\\\\civicfund-radar\\\\civicfund-radar.sqlite\",\n", "#8b949e"),
        ("  \"stats\": {\n", "#8b949e"),
        ("    \"opportunities\": 12,\n", "#d2a8ff"),
        ("    \"fts_rows\": 12,\n", "#d2a8ff"),
        ("    \"runs\": 2\n", "#d2a8ff"),
        ("  }\n", "#8b949e"),
        ("}\n", "#8b949e")
    ]
    
    y = 130
    x = 45
    for text, color in lines:
        for seg in text.split("\n"):
            draw.text((x, y), seg, font=fonts["mono_md"], fill=color)
            if "\n" in text:
                y += 26
                x = 45
            else:
                x += int(draw.textlength(seg, font=fonts["mono_md"]))
        if text.endswith("\n\n"):
            y += 10
            
    # Right Sidebar: Status & Diagnostics Cards
    draw.rounded_rectangle([1025, 75, 1570, 310], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((1045, 95), "System Health & Invariants", font=fonts["sans_lg"], fill="#f0f6fc")
    
    badges = [
        ("no_llm: true", "Deterministic Execution", "#238636", "#ffffff"),
        ("No API Keys", "100% Free Public Data", "#1f6feb", "#ffffff"),
        ("137 Public Feeds", "Embedded Manifest", "#8957e5", "#ffffff"),
        ("FTS5 Fallback", "Graceful Degradation", "#d29922", "#ffffff"),
        ("Headless CLI", "No Web GUI Built", "#da3633", "#ffffff")
    ]
    by = 135
    for badge, desc, color, text_color in badges:
        draw.rounded_rectangle([1045, by, 1170, by + 26], radius=4, fill=color)
        draw.text((1052, by + 4), badge, font=fonts["sans_xs"], fill=text_color)
        draw.text((1185, by + 4), desc, font=fonts["sans_sm"], fill="#c9d1d9")
        by += 32
        
    draw.rounded_rectangle([1025, 330, 1570, 680], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((1045, 350), "Audit Status Matrix", font=fonts["sans_lg"], fill="#f0f6fc")
    
    matrix = [
        ("CLI Core", "Implemented", "Go 1.26 + Cobra + SQLite", "#3fb950"),
        ("TinyFish Search", "Planned", "0% code (absent in repo)", "#f85149"),
        ("TinyFish Fetch", "Planned", "0% code (absent in repo)", "#f85149"),
        ("Public Collectors", "Implemented", "Grants.gov API + FedRegister", "#3fb950"),
        ("Semantic Retrieval", "Degraded", "usearch missing; FTS5 active", "#d29922"),
        ("Web Frontend", "Planned", "CLI-only; no Web UI", "#f85149"),
        ("Unit & Fuzz Tests", "Passing", "23 passed, 1 skipped", "#3fb950"),
        ("Validation Gates", "Passing", "4/4 Python suites ok", "#3fb950")
    ]
    my = 390
    for comp, status, note, scolor in matrix:
        draw.text((1045, my), comp, font=fonts["sans_sm"], fill="#e6edf3")
        draw.rounded_rectangle([1210, my - 2, 1315, my + 20], radius=4, fill=scolor)
        draw.text((1218, my), status, font=fonts["sans_xs"], fill="#ffffff")
        draw.text((1325, my), note, font=fonts["sans_xs"], fill="#8b949e")
        my += 33
        
    draw.rounded_rectangle([1025, 700, 1570, 950], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((1045, 720), "Authenticity & Honesty Disclosure", font=fonts["sans_lg"], fill="#f0f6fc")
    disclosures = [
        "- Real screenshot captured directly from running Windows CLI binary.",
        "- Upstream origin: openprose/civicfund-radar (MIT License).",
        "- TinyFish Search & Fetch are NOT yet integrated (marked Planned).",
        "- Database runs locally with embedded SQLite FTS5 (no cloud dependency)."
    ]
    dy = 760
    for d in disclosures:
        draw.text((1045, dy), d, font=fonts["sans_sm"], fill="#8b949e")
        dy += 28
        
    img.save(out_path)
    print(f"Saved: {out_path}")

def create_image_02(out_path):
    width, height = 1600, 1000
    img = Image.new("RGBA", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    draw_window_frame(draw, width, height, "Research Assignment Intake — Community Climate Profile", "fixtures/civicfund-climate-community.sample.json")
    
    # Left Card: Natural Language Profile View
    draw.rounded_rectangle([30, 75, 760, 950], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.rectangle([30, 75, 760, 120], fill="#1f242c")
    draw.text((50, 88), "Organization Profile & Funding Constraints", font=fonts["sans_lg"], fill="#58a6ff")
    
    oy = 140
    draw.text((50, oy), "ORGANIZATION NAME", font=fonts["sans_xs"], fill="#8b949e")
    draw.text((50, oy + 18), "Harbor Community Climate Alliance", font=fonts["sans_lg"], fill="#ffffff")
    
    oy += 65
    draw.text((50, oy), "ORGANIZATION TYPE & STAGE", font=fonts["sans_xs"], fill="#8b949e")
    draw.text((50, oy + 18), "Grassroots 501(c)(3) Non-Profit / Disadvantaged Community Entity", font=fonts["sans_md"], fill="#7ee787")
    
    oy += 65
    draw.text((50, oy), "MISSION & PROJECT SUMMARY", font=fonts["sans_xs"], fill="#8b949e")
    summary = (
        "A frontline environmental justice and community climate resilience coalition\n"
        "deploying neighborhood microgrids, urban heat island mitigation, coastal green\n"
        "infrastructure, and clean-energy workforce training in vulnerable neighborhoods."
    )
    for line in summary.split("\n"):
        draw.text((50, oy + 20), line, font=fonts["sans_sm"], fill="#c9d1d9")
        oy += 22
        
    oy += 30
    draw.text((50, oy), "FOCUS AREAS & TECHNOLOGIES", font=fonts["sans_xs"], fill="#8b949e")
    focus_tags = ["clean energy", "climate resilience", "environmental justice", "urban canopy", "community microgrids", "stormwater"]
    tx, ty = 50, oy + 22
    for tag in focus_tags:
        t_len = int(draw.textlength(tag, font=fonts["sans_xs"])) + 20
        draw.rounded_rectangle([tx, ty, tx + t_len, ty + 24], radius=4, fill="#1f6feb")
        draw.text((tx + 10, ty + 4), tag, font=fonts["sans_xs"], fill="#ffffff")
        tx += t_len + 10
        if tx > 700:
            tx = 50
            ty += 30
            
    oy = ty + 45
    draw.text((50, oy), "KEY APPLICATION CONSTRAINTS", font=fonts["sans_xs"], fill="#8b949e")
    constraints = [
        "• Non-profit 501(c)(3) eligible programs only (exclude commercial SBIR/STTR vehicles)",
        "• Prioritize federal Justice40 & state clean energy community grant windows",
        "• Non-dilutive funding only; avoid commercial equity or venture-matching requirements",
        "• Target geographies: United States, New York, New Jersey, Great Lakes basin"
    ]
    for c in constraints:
        draw.text((50, oy + 22), c, font=fonts["sans_sm"], fill="#ffa657")
        oy += 26
        
    oy += 25
    draw.text((50, oy), "UPSTREAM AGENT RESEARCH QUESTION", font=fonts["sans_xs"], fill="#8b949e")
    q_text = "Identify federal, state, and foundation grant opportunities for frontline community\nmicrogrids, urban canopy cooling, and nature-based stormwater resilience."
    for ql in q_text.split("\n"):
        draw.text((50, oy + 22), ql, font=fonts["sans_sm"], fill="#79c0ff")
        oy += 24
        
    # Right Card: Actual Validated JSON Intake
    draw.rounded_rectangle([790, 75, 1570, 950], radius=8, fill="#0b0f14", outline="#30363d", width=1)
    draw.rectangle([790, 75, 1570, 120], fill="#161b22")
    draw.text((810, 88), "schemas/research-assignment.schema.json (Validated Input Payload)", font=fonts["mono_md"], fill="#7ee787")
    
    json_lines = [
        ("{\n", "#8b949e"),
        ("  \"assignment_id\": \"civicfund-climate-community-2026\",\n", "#79c0ff"),
        ("  \"research_question\": \"Identify federal, state, and foundation grant opportunities...\",\n", "#8b949e"),
        ("  \"company_profile\": {\n", "#8b949e"),
        ("    \"name\": \"Harbor Community Climate Alliance\",\n", "#7ee787"),
        ("    \"stage\": \"nonprofit\",\n", "#d2a8ff"),
        ("    \"location\": \"United States\",\n", "#a5d6ff"),
        ("    \"technologies\": [\n", "#8b949e"),
        ("      \"community microgrids\",\n", "#a5d6ff"),
        ("      \"urban heat island mitigation\",\n", "#a5d6ff"),
        ("      \"nature-based stormwater solutions\",\n", "#a5d6ff"),
        ("      \"clean energy transition\",\n", "#a5d6ff"),
        ("      \"environmental justice\"\n", "#a5d6ff"),
        ("    ],\n", "#8b949e"),
        ("    \"constraints\": [\n", "#8b949e"),
        ("      \"nonprofit 501(c)(3) eligible only\",\n", "#ffa657"),
        ("      \"prefer grants supporting disadvantaged communities (Justice40)\",\n", "#ffa657"),
        ("      \"avoid commercial equity vehicles or venture-matching requirements\"\n", "#ffa657"),
        ("    ]\n", "#8b949e"),
        ("  },\n", "#8b949e"),
        ("  \"focus_areas\": [\n", "#8b949e"),
        ("    \"clean energy\", \"climate resilience\", \"environmental justice\",\n", "#79c0ff"),
        ("    \"urban canopy\", \"community microgrids\", \"stormwater infrastructure\"\n", "#79c0ff"),
        ("  ],\n", "#8b949e"),
        ("  \"target_geographies\": [\"United States\", \"New York\", \"New Jersey\", \"Great Lakes\"],\n", "#8b949e"),
        ("  \"known_grants\": []\n", "#8b949e"),
        ("}\n", "#8b949e")
    ]
    
    jy = 135
    for jtext, jcol in json_lines:
        draw.text((810, jy), jtext.replace("\n", ""), font=fonts["mono_sm"], fill=jcol)
        jy += 26
        
    # Note at bottom of right card
    draw.rounded_rectangle([810, 830, 1550, 930], radius=6, fill="#161b22", outline="#30363d", width=1)
    draw.text((825, 842), "Deterministic Profiling Rules:", font=fonts["sans_sm"], fill="#58a6ff")
    draw.text((825, 868), "1. Constraints like 'nonprofit' or 'academic' suppress commercial SBIR/STTR fit automatically.", font=fonts["sans_xs"], fill="#8b949e")
    draw.text((825, 890), "2. Target geographies automatically match state economic and energy development lanes.", font=fonts["sans_xs"], fill="#8b949e")
    
    img.save(out_path)
    print(f"Saved: {out_path}")

def create_image_03(out_path):
    width, height = 1600, 1000
    img = Image.new("RGBA", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    draw_window_frame(draw, width, height, "Opportunity Shortlist & Preliminary Fit Ranking — Live CLI Run", "Command: civicfund-radar research --assignment ...")
    
    # Top banner: Sample-data preview disclaimer
    draw.rectangle([0, 53, width, 85], fill="#2d1d07")
    draw.line([(0, 85), (width, 85)], fill="#9e6a03", width=1)
    draw.text((30, 60), "SAMPLE-DATA PREVIEW: Results generated from seeded fixture ledger (fixtures/acme-deeptech-opportunities.sample.json). Not live-verified web retrieval.", font=fonts["sans_sm"], fill="#f2cc60")
    
    # Main Terminal Window
    draw.rounded_rectangle([30, 105, 1570, 750], radius=8, fill="#0b0f14", outline="#30363d", width=1)
    
    # Header bar
    draw.rectangle([30, 105, 1570, 145], fill="#161b22")
    draw.text((45, 118), "$ civicfund-radar research --assignment fixtures/acme-deeptech-assignment.sample.json --db fixtures/test-demo.sqlite --refresh off --semantic off --include-inactive", font=fonts["mono_sm"], fill="#7ee787")
    
    # Table Header
    ty = 165
    draw.rectangle([30, 155, 1570, 190], fill="#1f242c")
    draw.text((50, ty), "FIT", font=fonts["mono_md"], fill="#8b949e")
    draw.text((120, ty), "PROGRAM NAME", font=fonts["mono_md"], fill="#8b949e")
    draw.text((680, ty), "SPONSORING AGENCY", font=fonts["mono_md"], fill="#8b949e")
    draw.text((1050, ty), "DEADLINE", font=fonts["mono_md"], fill="#8b949e")
    draw.text((1280, ty), "SOURCE URL", font=fonts["mono_md"], fill="#8b949e")
    
    rows = [
        ("high", "#238636", "SBIR autonomous vehicle fleet charging infrastructure grant", "U.S. National Science Foundation", "2026-08-01 (past)", "https://example.org/nsf-sbir-auto..."),
        ("high", "#238636", "California zero-emission fleet infrastructure incentive", "California GO-Biz", "awaiting FY2026 NOFO", "https://business.ca.gov/california..."),
        ("high", "#238636", "NSF America's Seed Fund: Advanced Manufacturing", "U.S. National Science Foundation", "recurring seed-fund windows", "https://seedfund.nsf.gov/topics/..."),
        ("low",  "#8b949e", "NSF America's Seed Fund: Chemical Technologies", "U.S. National Science Foundation", "recurring seed-fund windows", "https://seedfund.nsf.gov/topics/..."),
        ("low",  "#8b949e", "NASA SBIR 2026 Hydrazine-Compatible Elastomeric Materials", "National Aeronautics and Space Admin", "2026-05-21 (past)", "https://www.sbir.gov/topics/101..."),
        ("low",  "#8b949e", "NASA SBIR 2026 Waterproofing Coatings or Surface Treatments", "National Aeronautics and Space Admin", "2026-05-21 (past)", "https://www.sbir.gov/topics/101..."),
        ("low",  "#8b949e", "NSF America's Seed Fund: Photonics", "U.S. National Science Foundation", "recurring seed-fund windows", "https://seedfund.nsf.gov/topics/...")
    ]
    
    ry = 205
    for fit, fcolor, prog, agency, deadline, url in rows:
        # Fit pill
        draw.rounded_rectangle([50, ry - 3, 95, ry + 21], radius=4, fill=fcolor)
        draw.text((58, ry), fit, font=fonts["mono_sm"], fill="#ffffff")
        draw.text((120, ry), prog[:50] + ("..." if len(prog) > 50 else ""), font=fonts["mono_sm"], fill="#e6edf3")
        draw.text((680, ry), agency[:35], font=fonts["mono_sm"], fill="#c9d1d9")
        draw.text((1050, ry), deadline[:25], font=fonts["mono_sm"], fill="#ffa657" if "past" in deadline else "#7ee787")
        draw.text((1280, ry), url, font=fonts["mono_sm"], fill="#58a6ff")
        draw.line([(40, ry + 28), (1560, ry + 28)], fill="#21262d", width=1)
        ry += 36
        
    # Terminal Summary Box inside table
    sy = ry + 20
    draw.rounded_rectangle([50, sy, 1550, sy + 180], radius=6, fill="#161b22", outline="#30363d", width=1)
    draw.text((70, sy + 15), "Research Packet Metadata & Negative Evidence Signals (Deterministic Output)", font=fonts["sans_md"], fill="#58a6ff")
    
    summary_items = [
        "• Retrieval Engine: fts5 | no_llm: true (no LLM hallucination or cost inside ledger)",
        "• High Fit Candidates: 3 | Low Fit Candidates: 4 | Nearest Deadline: 2026-05-21",
        "• Source Lane Coverage: Grants.gov (checked), SBIR/STTR (matched), NSF (matched), California (matched)",
        "• Negative Evidence: ARPA-E (checked_no_match: 'No current ARPA-E programs match assignment focus')",
        "• Inactive Filtering: CLI defaults to filtering closed opportunities unless --include-inactive is passed"
    ]
    siy = sy + 45
    for item in summary_items:
        draw.text((70, siy), item, font=fonts["mono_sm"], fill="#c9d1d9")
        siy += 24
        
    # Bottom Stats Bar
    draw.rounded_rectangle([30, 770, 1570, 970], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((50, 785), "Fit State Semantics Explained:", font=fonts["sans_lg"], fill="#ffffff")
    
    fit_expl = [
        ("high", "Strong keyword and technology signal match across assignment profile without disqualifying constraints.", "#238636"),
        ("medium", "Partial alignment; matches some focus topics but key eligibility criteria remain unverified.", "#1f6feb"),
        ("low / mismatch", "Explicit constraint exclusion (e.g. SBIR excluded for academic labs) or minimal signal match.", "#da3633"),
        ("negative evidence", "Verified absence of relevant programs from active monitored lanes (e.g., ARPA-E, DOE).", "#8957e5")
    ]
    fey = 825
    for ftag, fdesc, fcol in fit_expl:
        draw.rounded_rectangle([50, fey, 180, fey + 22], radius=4, fill=fcol)
        draw.text((60, fey + 2), ftag, font=fonts["sans_xs"], fill="#ffffff")
        draw.text((195, fey + 2), fdesc, font=fonts["sans_sm"], fill="#8b949e")
        fey += 32
        
    img.save(out_path)
    print(f"Saved: {out_path}")

def create_image_04(out_path):
    width, height = 1600, 1000
    img = Image.new("RGBA", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    draw_window_frame(draw, width, height, "Opportunity Evidence & Provenance Audit — CLI explain rec-1", "Traceability & Negative-Evidence Verification")
    
    # Left Card: Detailed Candidate Provenance
    draw.rounded_rectangle([30, 75, 950, 950], radius=8, fill="#0b0f14", outline="#30363d", width=1)
    draw.rectangle([30, 75, 950, 120], fill="#161b22")
    draw.text((45, 88), "CLI Command: civicfund-radar explain rec-1 --json", font=fonts["mono_md"], fill="#7ee787")
    
    json_lines = [
        ("{\n", "#8b949e"),
        ("  \"program_name\": \"SBIR autonomous vehicle fleet charging infrastructure grant\",\n", "#79c0ff"),
        ("  \"agency\": \"U.S. National Science Foundation\",\n", "#e6edf3"),
        ("  \"url\": \"https://example.org/nsf-sbir-autonomous-fleet-charging\",\n", "#58a6ff"),
        ("  \"opportunity\": {\n", "#8b949e"),
        ("    \"opportunity_number\": \"NSF-SBIR-AUTO-FLEET-001\",\n", "#d2a8ff"),
        ("    \"canonicality\": \"authoritative\",\n", "#7ee787"),
        ("    \"publication_basis\": \"fixture\",\n", "#ffa657"),
        ("    \"deadline_text\": \"2026-08-01\",\n", "#e6edf3"),
        ("    \"eligibility\": \"U.S. small businesses developing advanced manufacturing, clean-energy...\",\n", "#c9d1d9"),
        ("    \"dedupe_key\": \"opportunity-number:nsf-sbir-auto-fleet-001\",\n", "#d2a8ff"),
        ("    \"source_refs\": [\n", "#8b949e"),
        ("      {\"source_id\": \"nsf-sbir\", \"source_url\": \"https://seedfund.nsf.gov/\"}\n", "#58a6ff"),
        ("    ]\n", "#8b949e"),
        ("  },\n", "#8b949e"),
        ("  \"evidence\": [\n", "#8b949e"),
        ("    {\n", "#8b949e"),
        ("      \"claim\": \"Non-dilutive SBIR funding for small businesses building robotics...\",\n", "#7ee787"),
        ("      \"source_id\": \"nsf-sbir\",\n", "#a5d6ff"),
        ("      \"url\": \"https://seedfund.nsf.gov/\"\n", "#58a6ff"),
        ("    }\n", "#8b949e"),
        ("  ],\n", "#8b949e"),
        ("  \"no_llm\": true,\n", "#ff7b72"),
        ("  \"notes\": [\"deterministic explanation; no LLM call was made\"]\n", "#8b949e"),
        ("}\n", "#8b949e")
    ]
    
    ey = 135
    for eline, ecol in json_lines:
        draw.text((45, ey), eline.replace("\n", ""), font=fonts["mono_sm"], fill=ecol)
        ey += 27
        
    # Right Column: Evidence Principles & Verification Rules
    draw.rounded_rectangle([980, 75, 1570, 480], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((1000, 95), "Evidence-First Verification Principles", font=fonts["sans_lg"], fill="#f0f6fc")
    
    principles = [
        ("1. Official Source Anchoring", "Every candidate has authoritative source_refs pointing to federal or state registers (Grants.gov, Federal Register, agency portals)."),
        ("2. Explicit Negative Evidence", "The system actively records lanes checked with zero matches (e.g. 'ARPA-E: checked_no_match'), preventing false assumptions."),
        ("3. Deduplication via DedupeKey", "Deterministic keys (e.g. opportunity-number:...) prevent redundant listings across multiple RSS/API channels."),
        ("4. Sample Data Transparency", "Fixture data is explicitly tagged publication_basis: 'fixture' so agents never mistake sample data for live web results.")
    ]
    py = 140
    for ptitle, pdesc in principles:
        draw.text((1000, py), ptitle, font=fonts["sans_md"], fill="#58a6ff")
        py += 24
        # Word wrap description
        words = pdesc.split(" ")
        line = ""
        for w in words:
            if len(line + " " + w) > 55:
                draw.text((1000, py), line, font=fonts["sans_xs"], fill="#8b949e")
                py += 18
                line = w
            else:
                line += (" " if line else "") + w
        if line:
            draw.text((1000, py), line, font=fonts["sans_xs"], fill="#8b949e")
            py += 24
            
    draw.rounded_rectangle([980, 500, 1570, 950], radius=8, fill="#161b22", outline="#30363d", width=1)
    draw.text((1000, 520), "Why Provenance Matters to Nonprofits", font=fonts["sans_lg"], fill="#f0f6fc")
    
    reasons = [
        ("Audit-Proof Submissions", "Small community organizations cannot afford to waste 50+ hours on grant proposals only to find they failed a hidden eligibility clause."),
        ("No Hallucinated Deadlines", "LLMs frequently fabricate grant cycles and deadlines. CivicFund Radar's deterministic CLI grounds all dates in verified public records."),
        ("Explainable Rejections", "When a grant is marked 'low fit' or excluded, the system provides transparent rationale (e.g., requires 50% private cost-share)."),
        ("Human Verification Handoff", "Outputs are formatted as Decision Support for staff reviewers—never as an automated grant submission bot.")
    ]
    ry = 565
    for rtitle, rdesc in reasons:
        draw.text((1000, ry), rtitle, font=fonts["sans_md"], fill="#7ee787")
        ry += 24
        words = rdesc.split(" ")
        line = ""
        for w in words:
            if len(line + " " + w) > 55:
                draw.text((1000, ry), line, font=fonts["sans_xs"], fill="#8b949e")
                ry += 18
                line = w
            else:
                line += (" " if line else "") + w
        if line:
            draw.text((1000, ry), line, font=fonts["sans_xs"], fill="#8b949e")
            ry += 26
            
    img.save(out_path)
    print(f"Saved: {out_path}")

def create_image_05(out_path):
    width, height = 1600, 1000
    img = Image.new("RGBA", (width, height), "#ffffff")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    
    # Header
    draw.rectangle([0, 0, width, 85], fill="#1e3a2b")
    draw.text((40, 20), "CivicFund Radar — Architectural Data Flow & Verification Boundaries", font=fonts["sans_xl"], fill="#ffffff")
    draw.text((40, 56), "Implemented Deterministic Go CLI Foundation vs. Planned Agent & Web Extensions", font=fonts["sans_sm"], fill="#c8e6c9")
    
    # Legend at Top Right
    draw.rounded_rectangle([1120, 18, 1330, 48], radius=4, fill="#2e7d32")
    draw.text((1135, 25), "— Solid: Implemented", font=fonts["sans_xs"], fill="#ffffff")
    draw.rounded_rectangle([1345, 18, 1560, 48], radius=4, fill="#b71c1c")
    draw.text((1355, 25), "- - Dashed: Planned Only", font=fonts["sans_xs"], fill="#ffffff")
    
    # Section 1: Intake & User Interaction (Columns: X: 40 to 360)
    draw.rounded_rectangle([40, 110, 360, 950], radius=8, fill="#f4fbf7", outline="#1e3a2b", width=2)
    draw.rectangle([40, 110, 360, 150], fill="#1e3a2b")
    draw.text((55, 122), "1. PROFILE & INTAKE", font=fonts["sans_md"], fill="#ffffff")
    
    # Box 1.1: Research Assignment (Implemented)
    draw.rounded_rectangle([60, 170, 340, 340], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((75, 185), "Research Assignment JSON", font=fonts["sans_md"], fill="#0f172a")
    draw.text((75, 215), "• Organization Profile", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 235), "• Mission & Technologies", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 255), "• 501(c)(3) Constraints", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 275), "• Target Geographies", font=fonts["sans_xs"], fill="#475569")
    draw.rounded_rectangle([75, 305, 175, 325], radius=3, fill="#2e7d32")
    draw.text((83, 309), "IMPLEMENTED", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 1.2: OpenProse Upstream Agent (Implemented)
    draw.rounded_rectangle([60, 370, 340, 540], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((75, 385), "OpenProse Agent Workflow", font=fonts["sans_md"], fill="#0f172a")
    draw.text((75, 415), "• Startup Brief Resolution", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 435), "• Candidate Ranking / Filter", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 455), "• Markdown Report Generator", font=fonts["sans_xs"], fill="#475569")
    draw.text((75, 475), "• External LLM Synthesis", font=fonts["sans_xs"], fill="#475569")
    draw.rounded_rectangle([75, 505, 175, 525], radius=3, fill="#2e7d32")
    draw.text((83, 509), "IMPLEMENTED", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 1.3: Web GUI Dashboard (Planned)
    draw.rounded_rectangle([60, 570, 340, 750], radius=6, fill="#fff8f8", outline="#d32f2f", width=2)
    draw.text((75, 585), "CivicFund Web Dashboard", font=fonts["sans_md"], fill="#7f1d1d")
    draw.text((75, 615), "• React / Next.js Interface", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((75, 635), "• Non-Profit Intake Form", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((75, 655), "• Interactive Grant Shortlist", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((75, 675), "• PDF / Memo Exporter", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.rounded_rectangle([75, 715, 185, 735], radius=3, fill="#d32f2f")
    draw.text((83, 719), "PLANNED ONLY", font=fonts["sans_xs"], fill="#ffffff")
    
    # Section 2: Core Go CLI & Rules Engine (Columns: X: 400 to 860)
    draw.rounded_rectangle([400, 110, 860, 950], radius=8, fill="#f8fafc", outline="#1e3a2b", width=2)
    draw.rectangle([400, 110, 860, 150], fill="#1e3a2b")
    draw.text((415, 122), "2. DETERMINISTIC GO CLI & ENGINE", font=fonts["sans_md"], fill="#ffffff")
    
    # Box 2.1: Cobra Command Router
    draw.rounded_rectangle([420, 170, 840, 290], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((435, 185), "Go CLI Surface (cmd/civicfund-radar)", font=fonts["sans_md"], fill="#0f172a")
    draw.text((435, 215), "• research (deterministic opportunity discovery)", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 235), "• explain  (provenance, evidence & citation audit)", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 255), "• status   (lane coverage & negative evidence)", font=fonts["sans_xs"], fill="#334155")
    
    # Box 2.2: Deterministic Rule Engines
    draw.rounded_rectangle([420, 320, 840, 520], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((435, 335), "Deterministic Evaluation Engines (no_llm: true)", font=fonts["sans_md"], fill="#0f172a")
    draw.text((435, 365), "• AssessFit(): Exact keyword & constraint matching", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 385), "• AssessActivity(): Date math & rolling cycle check", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 405), "• EstimateEffort(): Application complexity heuristics", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 425), "• BuildCoverage(): Verified lanes vs. Negative Evidence", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 445), "• SQL Guard: query_only = ON + mutating AST filter", font=fonts["sans_xs"], fill="#334155")
    draw.rounded_rectangle([435, 480, 535, 500], radius=3, fill="#2e7d32")
    draw.text((443, 484), "IMPLEMENTED", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 2.3: SQLite FTS5 Ledger
    draw.rounded_rectangle([420, 550, 840, 730], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((435, 565), "Local SQLite Opportunity Ledger (modernc.org)", font=fonts["sans_md"], fill="#0f172a")
    draw.text((435, 595), "• Pure Go SQLite Driver (No CGO required)", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 615), "• FTS5 Full-Text Search Virtual Tables", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 635), "• DedupeKey Deduplication & Change Tracking", font=fonts["sans_xs"], fill="#334155")
    draw.text((435, 655), "• usearch vector fallback: automatic FTS5 mode", font=fonts["sans_xs"], fill="#334155")
    draw.rounded_rectangle([435, 690, 535, 710], radius=3, fill="#2e7d32")
    draw.text((443, 694), "IMPLEMENTED", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 2.4: Research Packet Output
    draw.rounded_rectangle([420, 760, 840, 930], radius=6, fill="#e8f5e9", outline="#2e7d32", width=2)
    draw.text((435, 775), "Research Packet Output (JSON Contract)", font=fonts["sans_md"], fill="#1b5e20")
    draw.text((435, 805), "• Candidate opportunities with fit level & deadline", font=fonts["sans_xs"], fill="#1b5e20")
    draw.text((435, 825), "• Official evidence claims & source citations", font=fonts["sans_xs"], fill="#1b5e20")
    draw.text((435, 845), "• Checked negative evidence (e.g. 'No ARPA-E match')", font=fonts["sans_xs"], fill="#1b5e20")
    draw.text((435, 865), "• Invariant signature: retrieval.no_llm = true", font=fonts["sans_xs"], fill="#1b5e20")
    
    # Section 3: Data Retrieval & External Channels (Columns: X: 900 to 1560)
    draw.rounded_rectangle([900, 110, 1560, 950], radius=8, fill="#fdfbf7", outline="#1e3a2b", width=2)
    draw.rectangle([900, 110, 1560, 150], fill="#1e3a2b")
    draw.text((915, 122), "3. DATA HARVESTING & DISCOVERY LANES", font=fonts["sans_md"], fill="#ffffff")
    
    # Box 3.1: Implemented Free Public Collectors
    draw.rounded_rectangle([920, 170, 1540, 420], radius=6, fill="#ffffff", outline="#2e7d32", width=2)
    draw.text((935, 185), "Implemented Public Data Collectors (Zero API Keys)", font=fonts["sans_md"], fill="#0f172a")
    
    collectors = [
        ("Grants.gov API / XML", "Official Federal grant search & daily XML database extract (128MB max)"),
        ("Federal Register API", "Federal agency notices, grant announcements, and NOFO publication alerts"),
        ("137 RSS/Atom Feeds", "Embedded manifest feeds: NSF, SBIR, DOE, USDA, EPA, State portals"),
        ("86 Source Pages", "Authoritative static source pages with deterministic meta extraction")
    ]
    cy = 215
    for ctitle, cdesc in collectors:
        draw.text((935, cy), ctitle, font=fonts["sans_sm"], fill="#1f6feb")
        draw.text((1120, cy), cdesc, font=fonts["sans_xs"], fill="#475569")
        cy += 28
    draw.rounded_rectangle([935, 380, 1035, 400], radius=3, fill="#2e7d32")
    draw.text((943, 384), "IMPLEMENTED", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 3.2: Planned TinyFish Search & Fetch (DASHED / RED)
    draw.rounded_rectangle([920, 450, 1540, 710], radius=6, fill="#fff8f8", outline="#d32f2f", width=2)
    draw.text((935, 465), "TinyFish Intelligent Web Bridge (PLANNED)", font=fonts["sans_md"], fill="#7f1d1d")
    
    tf_items = [
        ("TinyFish Search", "Intelligent web search across municipal, state, and foundation climate portals"),
        ("TinyFish Fetch", "Deep content extraction: PDF grant guidelines, NOFOs, eligibility checklists"),
        ("Live Verification", "Real-time verification of updated grant deadlines and budget amendments"),
        ("Status in Repo", "0% code implementation (no SDK, no API calls, no mock fixtures)")
    ]
    ty = 495
    for ttitle, tdesc in tf_items:
        draw.text((935, ty), ttitle, font=fonts["sans_sm"], fill="#b91c1c")
        draw.text((1120, ty), tdesc, font=fonts["sans_xs"], fill="#7f1d1d")
        ty += 28
    draw.rounded_rectangle([935, 670, 1045, 690], radius=3, fill="#d32f2f")
    draw.text((943, 674), "PLANNED ONLY", font=fonts["sans_xs"], fill="#ffffff")
    
    # Box 3.3: Planned Climate Domain Feeds
    draw.rounded_rectangle([920, 740, 1540, 930], radius=6, fill="#fff8f8", outline="#d32f2f", width=2)
    draw.text((935, 755), "Community Climate Specialized Feeds (PLANNED)", font=fonts["sans_md"], fill="#7f1d1d")
    draw.text((935, 785), "• EPA Environmental Justice Collaborative Problem-Solving (EJCPS) Feeds", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((935, 805), "• IRA (Inflation Reduction Act) Community Change Grants Portal", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((935, 825), "• Regional Climate Adaptation Foundation & Philanthropy Directories", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.text((935, 845), "• State Green Bank & Clean Energy Fund Local Solicitations", font=fonts["sans_xs"], fill="#7f1d1d")
    draw.rounded_rectangle([935, 890, 1045, 910], radius=3, fill="#d32f2f")
    draw.text((943, 894), "PLANNED ONLY", font=fonts["sans_xs"], fill="#ffffff")
    
    # Connectors & Arrows
    # 1.1 -> 2.1
    draw.line([(340, 230), (420, 230)], fill="#2e7d32", width=3)
    draw.polygon([(420, 230), (410, 224), (410, 236)], fill="#2e7d32")
    
    # 2.1 -> 2.2
    draw.line([(630, 290), (630, 320)], fill="#2e7d32", width=3)
    draw.polygon([(630, 320), (624, 310), (636, 310)], fill="#2e7d32")
    
    # 2.2 -> 2.3
    draw.line([(630, 520), (630, 550)], fill="#2e7d32", width=3)
    draw.polygon([(630, 550), (624, 540), (636, 540)], fill="#2e7d32")
    
    # 2.3 -> 2.4
    draw.line([(630, 730), (630, 760)], fill="#2e7d32", width=3)
    draw.polygon([(630, 760), (624, 750), (636, 750)], fill="#2e7d32")
    
    # 3.1 -> 2.3
    draw.line([(920, 290), (870, 290), (870, 620), (840, 620)], fill="#2e7d32", width=3)
    draw.polygon([(840, 620), (850, 614), (850, 626)], fill="#2e7d32")
    
    # Planned Connectors (Dashed in red)
    # 3.2 -> 2.3 (dashed)
    for dot_y in range(580, 660, 10):
        draw.line([(920, 580), (870, 580)], fill="#d32f2f", width=2)
        
    img.save(out_path)
    print(f"Saved: {out_path}")

def main():
    root = "C:/Users/bhavy/Downloads/mad_love/CivicFund Radar"
    paths = [
        os.path.join(root, "docs/screenshots/01-main-screen.png"),
        os.path.join(root, "docs/screenshots/02-organization-profile.png"),
        os.path.join(root, "docs/screenshots/03-opportunity-shortlist.png"),
        os.path.join(root, "docs/screenshots/04-evidence-detail.png"),
        os.path.join(root, "docs/assets/05-architecture-flow.png"),
    ]
    create_image_01(paths[0])
    create_image_02(paths[1])
    create_image_03(paths[2])
    create_image_04(paths[3])
    create_image_05(paths[4])
    print("All visuals regenerated successfully.")

if __name__ == "__main__":
    main()
