#!/usr/bin/env python3
"""
scripts/deep_gsc_analyzer.py
Performs deep analysis of data/gsc_full_report.json:
- Examines all 1,061 queries and their landing pages
- Classifies landing pages: Dedicated Calculator, Category Hub, Generic / Root
- Detects intent mismatches (e.g. query is about "cylinder", page is "circle-sector")
- Identifies missing calculators that searchers are actively looking for
"""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

with open(REPO_ROOT / "data" / "gsc_full_report.json") as f:
    data = json.load(f)

queries = data["queries"]
query_pages = data["query_pages"]

# Map query -> list of landing pages
qp_map = {}
for qp in query_pages:
    q = qp["keys"][0]
    p = qp["keys"][1]
    qp_map.setdefault(q, []).append({
        "page": p,
        "impressions": qp["impressions"],
        "clicks": qp["clicks"],
        "position": qp["position"],
        "ctr": qp["ctr"]
    })

print(f"Total queries: {len(queries)}")
print(f"Total query-page pairs: {len(query_pages)}")

# Check which existing files exist
def page_exists(url):
    clean = url.replace("https://omnioperand.com", "")
    if clean.endswith("/"):
        p = REPO_ROOT / clean.lstrip("/") / "index.html"
    else:
        p = REPO_ROOT / clean.lstrip("/")
    return p.exists()

# Analyze by category / intent
hub_landings = []
root_landings = []
striking_distance = []
high_impression = []

# Detect queries landing on category hubs or homepage
for q in queries:
    q_str = q["keys"][0]
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    
    pages = qp_map.get(q_str, [])
    for p_info in pages:
        p_url = p_info["page"]
        clean_path = p_url.replace("https://omnioperand.com", "")
        
        # Check if landing on root or a category hub
        if clean_path in ["", "/", "/index.html"]:
            root_landings.append((q_str, imp, clk, pos, p_url))
        elif clean_path in [
            "/geometry/", "/geometry/2d/", "/geometry/3d/", "/geometry/2d/shapes/",
            "/calculus/", "/finance/", "/physics/", "/statistics/",
            "/biotech/", "/construction/", "/engineering/", "/agriculture/",
            "/energy/", "/health/", "/ecommerce/", "/logistics/", "/civil/",
            "/legal/", "/crypto/", "/pricing/", "/dispatch/"
        ]:
            hub_landings.append((q_str, imp, clk, pos, p_url))

print(f"\nQueries landing on Homepage (Root): {len(root_landings)}")
for item in root_landings[:20]:
    print(f"  [{item[1]} imp, {item[2]} clk, pos {item[3]:.1f}] '{item[0]}'")

print(f"\nQueries landing on Category Hubs (missing dedicated calculator or index): {len(hub_landings)}")
for item in hub_landings[:30]:
    print(f"  [{item[1]} imp, {item[2]} clk, pos {item[3]:.1f}] '{item[0]}' -> {item[4]}")

# Now let's analyze queries that landed on a page, but the query intent might not match the page slug
mismatches = []
for q in queries:
    q_str = q["keys"][0].lower()
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    pages = qp_map.get(q["keys"][0], [])
    for p_info in pages:
        p_url = p_info["page"]
        slug = p_url.replace("https://omnioperand.com/", "").strip("/")
        
        # check specific keywords in query vs slug
        # e.g., cylinder queries landing on circle-sector or regular-polygon
        if "cylinder" in q_str and "cylinder" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Cylinder Calculator"))
        elif ("bac " in q_str or "bac" == q_str or "blood alcohol" in q_str) and "bac" not in slug and "alcohol" not in slug:
            mismatches.append((q_str, imp, pos, slug, "BAC / Blood Alcohol Calculator"))
        elif ("child tax credit" in q_str) and "child-tax-credit" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Child Tax Credit Calculator"))
        elif ("stopping distance" in q_str) and "stopping-distance" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Stopping Distance Calculator"))
        elif ("vo2" in q_str) and "vo2" not in slug:
            mismatches.append((q_str, imp, pos, slug, "VO2 Max Calculator"))
        elif ("creatin" in q_str) and "creatine" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Creatine Dosing Calculator"))
        elif ("map" in q_str or "arterial pressure" in q_str) and "mean-arterial-pressure" not in slug and "map" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Mean Arterial Pressure (MAP) Calculator"))
        elif ("self storage" in q_str) and "self-storage" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Self Storage Rent/Revenue Calculator"))
        elif ("slant height" in q_str or "frustum" in q_str or "truncated cone" in q_str) and "cone" not in slug and "frustum" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Cone / Frustum / Slant Height Calculator"))
        elif ("auto depreciation" in q_str or "car depreciation" in q_str) and "depreciation" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Vehicle Depreciation Calculator"))
        elif ("2d projectile" in q_str or "projectile motion" in q_str) and "projectile" not in slug:
            mismatches.append((q_str, imp, pos, slug, "2D Projectile Motion Calculator"))
        elif ("amazon fba" in q_str) and "amazon-fba" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Amazon FBA Fee & Profit Calculator"))
        elif ("rsu tax" in q_str) and "rsu" not in slug:
            mismatches.append((q_str, imp, pos, slug, "RSU Tax Calculator"))
        elif ("deck joist" in q_str or "spacing joists" in q_str) and "deck-joist" not in slug and "joist" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Deck Joist Spacing & Span Calculator"))
        elif ("unistrut" in q_str) and "unistrut" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Unistrut Beam Load Capacity Calculator"))
        elif ("section 179" in q_str) and "section-179" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Section 179 Tax Deduction Calculator"))
        elif ("section 1250" in q_str) and "1250" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Section 1250 Depreciation Recapture Calculator"))
        elif ("swale" in q_str) and "swale" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Grass Swale Sizing Calculator"))
        elif ("trailer finance" in q_str) and "trailer" not in slug and "rv-loan" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Trailer Financing Calculator"))
        elif ("yacht fuel" in q_str) and "yacht" not in slug:
            mismatches.append((q_str, imp, pos, slug, "Boat / Yacht Fuel Consumption Calculator"))

print(f"\nPotential Intent Mismatches (Query target vs Actual landing page): {len(mismatches)}")
# deduplicate by query
seen = set()
for q_str, imp, pos, slug, target in mismatches:
    if target not in seen:
        print(f"  Target: {target:35} | Ex: '{q_str}' (imp: {imp}, pos: {pos:.1f}) -> landed on: /{slug}/")
        seen.add(target)
