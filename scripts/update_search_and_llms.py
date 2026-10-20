#!/usr/bin/env python3
"""
scripts/update_search_and_llms.py
Updates:
1. assets/js/omni-search.js with full searchable index of all 118+ calculators
2. llms.txt and llms-full.txt with complete directory of endpoints and mathematical references
3. index.html with Construction, Health, and API/Pricing cards
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

from calculator_data import CALCULATORS_DATA, HUB_DATA

def update_search_js():
    print("🔍 Updating assets/js/omni-search.js search index...")
    search_file = REPO_ROOT / "assets" / "js" / "omni-search.js"
    content = search_file.read_text(encoding="utf-8")

    index_items = [
        {
            "title": "OmniOperand Computational REST API & OpenAPI Schema",
            "category": "Developer & Machine Protocols",
            "url": "/api/",
            "keywords": ["api", "rest", "openapi", "json", "developer", "mcp", "postman", "sdk"]
        },
        {
            "title": "OmniOperand Commercial API & MCP Pricing",
            "category": "Commercial & Subscriptions",
            "url": "/pricing/",
            "keywords": ["pricing", "pro", "enterprise", "stripe", "checkout", "api key", "tokens", "subscription"]
        },
        {
            "title": "Embeddable Calculator Widgets (CaaS)",
            "category": "Developer & Webmasters",
            "url": "/embed/",
            "keywords": ["embed", "widget", "iframe", "webmaster", "caas", "calculator widget", "white label"]
        },
        {
            "title": "Universal Regular Polygon Calculator",
            "category": "Geometry > 2D Geometry > Shapes",
            "url": "/geometry/2d/shapes/regular-polygon/",
            "keywords": ["regular polygon", "n-gon", "n-sided", "polygon", "triangle", "square", "pentagon", "hexagon", "octagon", "apothem", "circumradius", "diagonals", "area"]
        },
        {
            "title": "Regular Octagon Calculator",
            "category": "Geometry > 2D Geometry > Shapes",
            "url": "/geometry/2d/shapes/octagon/",
            "keywords": ["octagon", "polygon", "8-sided", "apothem", "circumradius", "diagonal", "stop sign", "area", "perimeter"]
        },
        {
            "title": "Regular Hexagon Calculator",
            "category": "Geometry > 2D Geometry > Shapes",
            "url": "/geometry/2d/shapes/hexagon/",
            "keywords": ["hexagon", "polygon", "6-sided", "honeycomb", "apothem", "circumradius", "diagonal", "area"]
        },
        {
            "title": "Regular Pentagon Calculator",
            "category": "Geometry > 2D Geometry > Shapes",
            "url": "/geometry/2d/shapes/pentagon/",
            "keywords": ["pentagon", "polygon", "5-sided", "golden ratio", "phi", "pentagram", "diagonal", "apothem", "area"]
        },
        {
            "title": "Regular Decagon Calculator",
            "category": "Geometry > 2D Geometry > Shapes",
            "url": "/geometry/2d/shapes/decagon/",
            "keywords": ["decagon", "polygon", "10-sided", "golden ratio", "phi", "apothem", "circumradius", "diagonal", "area"]
        }
    ]

    # Add all Category Hubs
    for cat, hub in HUB_DATA.items():
        index_items.append({
            "title": hub["title"],
            "category": f"Domain Hub > {cat.capitalize()}",
            "url": f"/{cat}/",
            "keywords": [cat, "hub", "calculators", "overview", "formulas"]
        })

    # Add all calculators
    for c in CALCULATORS_DATA:
        cat = c["category"]
        slug = c["slug"]
        name = c["name"]
        desc = c["description"]
        
        # Extract keywords
        raw_words = re.findall(r"[A-Za-z0-9\-]+", f"{name} {desc} {slug}")
        keywords = list(dict.fromkeys([w.lower() for w in raw_words if len(w) > 2]))[:12]

        index_items.append({
            "title": name,
            "category": f"{cat.capitalize()} > {c.get('hero_badge', 'Calculators')}",
            "url": f"/{cat}/{slug}/",
            "keywords": keywords
        })

    json_str = json.dumps(index_items, indent=2, ensure_ascii=False)
    new_index_block = f"  // Calculator & Hub Index Database\n  const SEARCH_INDEX = {json_str};"

    # Replace SEARCH_INDEX definition
    pattern = re.compile(r"  // Calculator & Hub Index Database\s+const SEARCH_INDEX = \[[\s\S]*?\n  \];", re.MULTILINE)
    if pattern.search(content):
        updated_content = pattern.sub(new_index_block, content)
        search_file.write_text(updated_content, encoding="utf-8")
        print(f"  ✅ Updated omni-search.js with {len(index_items)} searchable entries!")
    else:
        print("  ⚠️ Could not find SEARCH_INDEX pattern in omni-search.js")

def update_llms_manifests():
    print("🤖 Updating llms.txt and llms-full.txt manifests...")
    
    # Build llms.txt
    lines = [
        "# OmniOperand (omnioperand.com)",
        "> High-precision quantitative computing engine, bidirectional geometric solvers, and exact radical mathematical derivations.",
        "",
        "## Overview",
        "OmniOperand provides rigorously verified computational solvers across Pure and Applied Mathematics, Quantitative Finance, Construction Engineering, and Physiological Bio-Quant. Each tool offers closed-form algebraic solutions, exact radical constants, step-by-step proofs, zero floating-point approximation drift, and automated machine API endpoints.",
        "",
        "## Commercial API & Autonomous AI Agent Services",
        "- [REST API & OpenAPI 3.1 Schema](https://omnioperand.com/api/): Full machine-readable schema for ChatGPT Custom Actions, Claude MCP, and autonomous AI agents.",
        "- [Model Context Protocol (MCP) Server](https://omnioperand.com/mcp/schemas.json): Stdio and HTTP MCP server exposing deterministic mathematical tools with explicit system prompts.",
        "- [Developer & Enterprise Pricing](https://omnioperand.com/pricing/): Metered API tiers (Free: 500 req/mo, Pro: 50,000 req/mo at $29/mo, Enterprise: $199/mo).",
        "- [Embeddable Widgets (CaaS)](https://omnioperand.com/embed/): Standalone zero-dependency calculator widget engine with isolated Shadow DOM.",
        "",
        "## Domain Hubs"
    ]

    for cat, hub in HUB_DATA.items():
        lines.append(f"- [{hub['title']}](https://omnioperand.com/{cat}/): {hub['description']}")

    # Group calculators by category
    cats = {}
    for c in CALCULATORS_DATA:
        cat = c["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(c)

    for cat, calcs in cats.items():
        cat_title = HUB_DATA.get(cat, {}).get("title", cat.capitalize() + " Solvers")
        lines.append(f"\n### {cat_title}")
        for c in calcs:
            slug = c["slug"]
            name = c["name"]
            desc = c["description"]
            lines.append(f"- [{name}](https://omnioperand.com/{cat}/{slug}/): {desc}")

    llms_path = REPO_ROOT / "llms.txt"
    llms_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  ✅ Updated llms.txt ({len(lines)} lines)")

    # Build llms-full.txt
    full_lines = list(lines)
    full_lines.append("\n## Mathematical Invariants & Analytical Formulas\n")
    for c in CALCULATORS_DATA:
        name = c["name"]
        cat = c["category"]
        slug = c["slug"]
        formula = c.get("formula_display", "")
        proofs = c.get("proof_steps", [])
        
        full_lines.append(f"### {name} (`https://omnioperand.com/{cat}/{slug}/`)")
        full_lines.append(f"- Governing Formula: `{formula}`")
        for p in proofs:
            full_lines.append(f"  - **{p['step_title']}**: {p['step_text']}")
        full_lines.append("")

    full_path = REPO_ROOT / "llms-full.txt"
    full_path.write_text("\n".join(full_lines) + "\n", encoding="utf-8")
    print(f"  ✅ Updated llms-full.txt ({len(full_lines)} lines)")

def update_homepage():
    print("🏠 Updating index.html navigation and hub cards...")
    index_file = REPO_ROOT / "index.html"
    content = index_file.read_text(encoding="utf-8")

    # Update header nav to include all hubs + pricing
    new_nav = """      <nav class="header-nav">
        <a href="/geometry/" class="nav-link">Geometry</a>
        <a href="/calculus/" class="nav-link">Calculus</a>
        <a href="/finance/" class="nav-link">Finance</a>
        <a href="/construction/" class="nav-link">Construction</a>
        <a href="/health/" class="nav-link">Health</a>
        <a href="/physics/" class="nav-link">Physics</a>
        <a href="/statistics/" class="nav-link">Statistics</a>
        <a href="/pricing/" class="nav-link">Pricing</a>
      </nav>"""
    
    nav_pattern = re.compile(r'<nav class="header-nav">[\s\S]*?</nav>')
    if nav_pattern.search(content):
        content = nav_pattern.sub(new_nav, content)

    # Check if Construction and Health cards are in hub-grid
    if "/construction/" not in content:
        # Insert Construction and Health cards before </div class="hub-grid">
        construction_card = """
        <!-- Construction Hub Card -->
        <div class="hub-card" style="--card-accent: #f59e0b;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#f59e0b;">🏗️</div>
              <span class="hub-badge">Active Domain</span>
            </div>
            <h3 class="hub-card-title"><a href="/construction/">Construction & Trades Engineering</a></h3>
            <p class="hub-card-desc">
              High-precision civil and trade engineering solvers. Ready-mix concrete cubic yards, framing, aggregate tonnage, roofing squares, HVAC thermal loads, and electrical drop.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/construction/concrete-slab/"><strong>Concrete Slab & Footings →</strong></a></li>
            <li><a href="/construction/drywall/">Drywall Sheets & Mud →</a></li>
            <li><a href="/construction/ac-btu-tonnage/">HVAC BTU & Tonnage →</a></li>
            <li><a href="/construction/">Explore All 27 Construction Solvers →</a></li>
          </ul>
        </div>

        <!-- Health Hub Card -->
        <div class="hub-card" style="--card-accent: #10b981;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#10b981;">🩺</div>
              <span class="hub-badge">Active Domain</span>
            </div>
            <h3 class="hub-card-title"><a href="/health/">Health, Nutrition & Bio-Quant</a></h3>
            <p class="hub-card-desc">
              Clinical and physiological bio-quant solvers. Basal Metabolic Rate (BMR), TDEE, macronutrient distributions, US Navy body fat, hydration kinetics, and cardiovascular reserve.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/health/bmr/"><strong>Basal Metabolic Rate (BMR) →</strong></a></li>
            <li><a href="/health/tdee/">Total Daily Energy (TDEE) →</a></li>
            <li><a href="/health/macro/">Macronutrient Split →</a></li>
            <li><a href="/health/">Explore All 25 Health Solvers →</a></li>
          </ul>
        </div>

        <!-- Commercial API & MCP Card -->
        <div class="hub-card" style="--card-accent: #8b5cf6;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#8b5cf6;">⚡</div>
              <span class="hub-badge">Commercial API</span>
            </div>
            <h3 class="hub-card-title"><a href="/pricing/">Developer API & Model Context Protocol</a></h3>
            <p class="hub-card-desc">
              Deterministic, sub-15ms mathematical edge endpoints and MCP server for Claude, ChatGPT, and AI agents. Self-service API keys, metered tiers, and embeddable widgets.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/pricing/"><strong>View API Subscription Tiers ($29/mo) →</strong></a></li>
            <li><a href="/api/">REST API Documentation & OpenAPI →</a></li>
            <li><a href="/embed/">Embeddable Widgets (CaaS) →</a></li>
          </ul>
        </div>
"""
        # Find closing tag of hub-grid
        # Replace the first instance of </div> that closes hub-grid
        content = content.replace('<!-- 5. Statistics -->\n        <div class="hub-card"', '<!-- 5. Statistics -->\n        <div class="hub-card"')
        # Insert before </section> that closes master disciplines
        disc_end = content.find('</section>\n\n    <!-- PageSpeed & Architecture Mandates Section -->')
        if disc_end != -1:
            # find last </div> before this </section>
            last_div = content.rfind('</div>', 0, disc_end)
            if last_div != -1:
                content = content[:last_div] + construction_card + content[last_div:]
        index_file.write_text(content, encoding="utf-8")
        print("  ✅ Updated index.html with Construction, Health, and API cards!")
    else:
        index_file.write_text(content, encoding="utf-8")
        print("  ✅ Updated index.html navigation links!")

if __name__ == "__main__":
    update_search_js()
    update_llms_manifests()
    update_homepage()
