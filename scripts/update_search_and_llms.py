#!/usr/bin/env python3
"""
scripts/update_search_and_llms.py
Updates:
1. assets/js/omni-search.js with full searchable index of all calculators
2. llms.txt and llms-full.txt with complete directory of endpoints and mathematical references
3. index.html with Construction, Health, and API/Pricing cards
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

from calculator_data import CALCULATORS_DATA, HUB_DATA
try:
    from gsc_calculator_data import GSC_CALCULATORS
except ImportError:
    GSC_CALCULATORS = []

try:
    from data_batch2_gsc import BATCH2_CALCULATORS
    from data_batch2_part2_gsc import BATCH2_PART2_CALCULATORS
    ALL_BATCH2 = BATCH2_CALCULATORS + BATCH2_PART2_CALCULATORS
except ImportError:
    ALL_BATCH2 = []

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

    # Add all core calculators
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

    # Add GSC and Batch 2 calculators
    extra_calcs = GSC_CALCULATORS + ALL_BATCH2
    for c in extra_calcs:
        slug = c["slug"]
        cat = c.get("category", slug.split('/')[0])
        name = c["name"]
        desc = c["description"]
        raw_words = re.findall(r"[A-Za-z0-9\-]+", f"{name} {desc} {slug}")
        keywords = list(dict.fromkeys([w.lower() for w in raw_words if len(w) > 2]))[:12]
        index_items.append({
            "title": name,
            "category": f"{cat.capitalize()} > {c.get('hero_badge', 'Calculators')}",
            "url": f"/{slug}/",
            "keywords": keywords
        })

    json_str = json.dumps(index_items, indent=2, ensure_ascii=False)
    new_index_block = f"  // Calculator & Hub Index Database\n  const SEARCH_INDEX = {json_str};"

    # Replace SEARCH_INDEX definition
    pattern = re.compile(r"  // Calculator & Hub Index Database\s+const SEARCH_INDEX = \[[\s\S]*?\n\s*\];", re.MULTILINE)
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
        cats[cat].append((f"/{cat}/{c['slug']}/", c["name"], c["description"], c.get("formula_display", ""), c.get("proof_steps", [])))

    for c in GSC_CALCULATORS + ALL_BATCH2:
        slug = c["slug"]
        cat = c.get("category", slug.split('/')[0])
        if cat not in cats:
            cats[cat] = []
        cats[cat].append((f"/{slug}/", c["name"], c["description"], c.get("formula_display", ""), c.get("proof_steps", [])))

    for cat, calcs in cats.items():
        cat_title = HUB_DATA.get(cat, {}).get("title", cat.capitalize() + " Solvers")
        lines.append(f"\n### {cat_title}")
        for url, name, desc, formula, proofs in calcs:
            lines.append(f"- [{name}](https://omnioperand.com{url}): {desc}")

    llms_path = REPO_ROOT / "llms.txt"
    llms_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  ✅ Updated llms.txt ({len(lines)} lines)")

    # Build llms-full.txt
    full_lines = list(lines)
    full_lines.append("\n## Mathematical Invariants & Analytical Formulas\n")
    for cat, calcs in cats.items():
        for url, name, desc, formula, proofs in calcs:
            full_lines.append(f"### {name} (`https://omnioperand.com{url}`)")
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

    # Update header nav to include key hubs + MCP + API + Pricing
    new_nav = """      <nav class="header-nav">
        <a href="/geometry/" class="nav-link">Geometry</a>
        <a href="/finance/" class="nav-link">Finance</a>
        <a href="/construction/" class="nav-link">Construction</a>
        <a href="/energy/" class="nav-link">Energy</a>
        <a href="/logistics/" class="nav-link">Logistics</a>
        <a href="/crypto/" class="nav-link">Crypto</a>
        <a href="/ecommerce/" class="nav-link">E-Commerce</a>
        <a href="/biotech/" class="nav-link">Biotech</a>
        <a href="/mcp/" class="nav-link" style="color:var(--accent-purple); font-weight:700;">MCP Server</a>
        <a href="/api/" class="nav-link">REST API</a>
        <a href="/pricing/" class="nav-link">Pricing</a>
      </nav>"""
    
    nav_pattern = re.compile(r'<nav class="header-nav">[\s\S]*?</nav>')
    if nav_pattern.search(content):
        content = nav_pattern.sub(new_nav, content)

    # Build comprehensive discipline hub cards
    domain_cards = """
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

        <!-- Energy & Solar Clean Tech Hub -->
        <div class="hub-card" style="--card-accent: #f59e0b;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#f59e0b;">☀️</div>
              <span class="hub-badge">Clean Tech</span>
            </div>
            <h3 class="hub-card-title"><a href="/energy/">Energy, Solar & Clean Tech</a></h3>
            <p class="hub-card-desc">
              Solar PV array sizing, battery storage ESS capacity, heat pump seasonal COP, Levelized Cost of Energy (LCOE), and commercial grid peak demand shaving.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/energy/solar-payback/"><strong>Solar PV Payback & ROI →</strong></a></li>
            <li><a href="/energy/battery-backup-storage/">Battery Backup & Storage Sizing →</a></li>
            <li><a href="/energy/levelized-cost-of-energy/">Levelized Cost of Energy (LCOE) →</a></li>
            <li><a href="/energy/">Explore All 25 Energy Solvers →</a></li>
          </ul>
        </div>

        <!-- Logistics & Freight Hub -->
        <div class="hub-card" style="--card-accent: #0ea5e9;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#0ea5e9;">🚢</div>
              <span class="hub-badge">Supply Chain</span>
            </div>
            <h3 class="hub-card-title"><a href="/logistics/">Logistics, Supply Chain & Freight</a></h3>
            <p class="hub-card-desc">
              Dimensional weight (DIM divisor), ocean container TEU load optimization, NMFC freight class density, drayage demurrage, and truckload ton-mile costs.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/logistics/dim-weight-calculator/"><strong>Dimensional Weight (DIM 139/166) →</strong></a></li>
            <li><a href="/logistics/pallet-ti-hi-optimizer/">Pallet Ti-Hi Unit Load Optimizer →</a></li>
            <li><a href="/logistics/freight-density-nmfc/">NMFC Freight Density & Class →</a></li>
            <li><a href="/logistics/">Explore All 25 Logistics Solvers →</a></li>
          </ul>
        </div>

        <!-- Crypto & Fintech Hub -->
        <div class="hub-card" style="--card-accent: #a855f7;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#a855f7;">🪙</div>
              <span class="hub-badge">Web3 & DeFi</span>
            </div>
            <h3 class="hub-card-title"><a href="/crypto/">Cryptocurrency, DeFi & Fintech</a></h3>
            <p class="hub-card-desc">
              Automated Market Maker (AMM) impermanent loss, crypto staking APY/APR compounding, ASIC mining profitability, gas cost units, and futures liquidation prices.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/crypto/crypto-mining-profitability/"><strong>Bitcoin ASIC Mining Profitability →</strong></a></li>
            <li><a href="/crypto/staking-rewards-apr-apy/">Staking Rewards APR vs APY →</a></li>
            <li><a href="/crypto/impermanent-loss-amm/">AMM Impermanent Loss Model →</a></li>
            <li><a href="/crypto/">Explore All 25 Crypto Solvers →</a></li>
          </ul>
        </div>

        <!-- Legal & Insurance Hub -->
        <div class="hub-card" style="--card-accent: #ef4444;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#ef4444;">⚖️</div>
              <span class="hub-badge">Actuarial Risk</span>
            </div>
            <h3 class="hub-card-title"><a href="/legal/">Legal, Insurance & Actuarial Risk</a></h3>
            <p class="hub-card-desc">
              Personal injury settlement multipliers, pain and suffering valuations, structured settlement NPV discounting, lost future earning capacity, and contingency payouts.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/legal/personal-injury-multiplier/"><strong>Personal Injury Settlement Multiplier →</strong></a></li>
            <li><a href="/legal/structured-settlement-npv/">Structured Settlement Cash NPV →</a></li>
            <li><a href="/legal/lost-earning-capacity/">Future Lost Earning Capacity →</a></li>
            <li><a href="/legal/">Explore All 25 Legal Solvers →</a></li>
          </ul>
        </div>

        <!-- Agricultural Science Hub -->
        <div class="hub-card" style="--card-accent: #84cc16;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#84cc16;">🌾</div>
              <span class="hub-badge">Agronomy</span>
            </div>
            <h3 class="hub-card-title"><a href="/agriculture/">Agricultural Science & Precision Farming</a></h3>
            <p class="hub-card-desc">
              Corn and soybean yield estimators, NPK commercial fertilizer blending, livestock stocking density AUM, grain bin bushel storage, and pesticide tank mixing.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/agriculture/crop-yield-estimator/"><strong>Corn & Grain Crop Yield Estimator →</strong></a></li>
            <li><a href="/agriculture/npk-fertilizer-blending/">NPK Fertilizer Blending & Ratio →</a></li>
            <li><a href="/agriculture/grain-bin-volume-bushels/">Round Grain Bin Bushel Capacity →</a></li>
            <li><a href="/agriculture/">Explore All 25 Ag Solvers →</a></li>
          </ul>
        </div>

        <!-- Civil & Structural Engineering Hub -->
        <div class="hub-card" style="--card-accent: #64748b;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#64748b;">🌉</div>
              <span class="hub-badge">Structures</span>
            </div>
            <h3 class="hub-card-title"><a href="/engineering/">Civil, Structural & Geotechnical</a></h3>
            <p class="hub-card-desc">
              Beam elastic deflection and bending moments, Manning open channel gravity flow, reinforced concrete rebar ratios, Rankine retaining wall lateral pressure, and column buckling.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/engineering/beam-deflection-bending-moment/"><strong>Beam Deflection & Bending Moment →</strong></a></li>
            <li><a href="/engineering/manning-pipe-flow/">Manning Open Channel Gravity Flow →</a></li>
            <li><a href="/engineering/retaining-wall-active-earth-pressure/">Rankine Retaining Wall Earth Pressure →</a></li>
            <li><a href="/engineering/">Explore All 25 Engineering Solvers →</a></li>
          </ul>
        </div>

        <!-- E-Commerce & Retail Hub -->
        <div class="hub-card" style="--card-accent: #ec4899;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#ec4899;">🛒</div>
              <span class="hub-badge">Unit Economics</span>
            </div>
            <h3 class="hub-card-title"><a href="/ecommerce/">E-Commerce & Retail Operations</a></h3>
            <p class="hub-card-desc">
              Total landed unit cost, inventory turnover days sales (DSI), checkout cart abandonment recovery, Amazon FBA fee margins, GMROI, and Customer LTV:CAC ratios.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/ecommerce/landed-cost-unit-margin/"><strong>Total Landed Cost & Gross Margin →</strong></a></li>
            <li><a href="/ecommerce/amazon-fba-fee-margin/">Amazon FBA Fee & Net Margin →</a></li>
            <li><a href="/ecommerce/inventory-turnover-days-sales/">Inventory Turnover & DSI Days →</a></li>
            <li><a href="/ecommerce/">Explore All 30 E-Commerce Solvers →</a></li>
          </ul>
        </div>

        <!-- Biotechnology & Pharmacology Hub -->
        <div class="hub-card" style="--card-accent: #06b6d4;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#06b6d4;">🧬</div>
              <span class="hub-badge">Clinical Medicine</span>
            </div>
            <h3 class="hub-card-title"><a href="/biotech/">Biotechnology, Pharma & Lab Medicine</a></h3>
            <p class="hub-card-desc">
              Pharmacokinetics drug elimination half-life, Cockcroft-Gault CrCl renal dosing, PCR primer melting temperature (Tm), Michaelis-Menten enzyme kinetics, and qPCR 2^(-ΔΔCt).
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/biotech/drug-elimination-half-life/"><strong>Pharmacokinetics Elimination Half-Life (t½) →</strong></a></li>
            <li><a href="/biotech/cockcroft-gault-crcl/">Cockcroft-Gault Creatinine Clearance →</a></li>
            <li><a href="/biotech/pcr-primer-tm/">PCR Primer Melting Temp (Tm) →</a></li>
            <li><a href="/biotech/">Explore All 25 Biotech Solvers →</a></li>
          </ul>
        </div>

        <!-- Commercial API & Model Context Protocol Card -->
        <div class="hub-card" style="--card-accent: #8b5cf6;">
          <div>
            <div class="hub-card-header">
              <div class="hub-card-icon" style="color:#8b5cf6;">⚡</div>
              <span class="hub-badge">AI Protocols</span>
            </div>
            <h3 class="hub-card-title"><a href="/mcp/">Model Context Protocol (MCP) Server</a></h3>
            <p class="hub-card-desc">
              Direct connection for Claude Desktop, Cursor, and AI agents. Exposes all 438 deterministic solvers with zero hallucination and machine verification.
            </p>
          </div>
          <ul class="hub-card-links">
            <li><a href="/mcp/"><strong>Connect Claude Desktop & Cursor (1-Click) →</strong></a></li>
            <li><a href="/api/">REST API Documentation & OpenAPI 3.1 →</a></li>
            <li><a href="/pricing/">Commercial API Keys & Quotas →</a></li>
          </ul>
        </div>
    """

    if "/energy/" not in content:
        disc_end = content.find('</section>\n\n    <!-- Machine-Readable LLM Standards Callout -->')
        if disc_end == -1:
            disc_end = content.find('</section>\n\n    <!-- PageSpeed & Architecture Mandates Section -->')
        if disc_end != -1:
            last_div = content.rfind('</div>', 0, disc_end)
            if last_div != -1:
                content = content[:last_div] + domain_cards + content[last_div:]
        index_file.write_text(content, encoding="utf-8")
        print("  ✅ Updated index.html with all 15 Domain Hubs and MCP Server card!")
    else:
        index_file.write_text(content, encoding="utf-8")
        print("  ✅ Updated index.html navigation links!")

if __name__ == "__main__":
    update_search_js()
    update_llms_manifests()
    update_homepage()
    try:
        from sync_calculator_counts import sync_all
        sync_all()
    except Exception as e:
        print(f"⚠️ Metrics sync notice: {e}")
