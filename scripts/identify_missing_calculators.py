#!/usr/bin/env python3
"""
scripts/identify_missing_calculators.py
Examines all 1,061 queries to pinpoint distinct missing tools and intent gaps.
"""

import json
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent

with open(REPO_ROOT / "data" / "gsc_full_report.json") as f:
    data = json.load(f)

queries = data["queries"]
query_pages = data["query_pages"]

qp_map = {}
for qp in query_pages:
    qp_map.setdefault(qp["keys"][0], []).append(qp)

missing_opportunities = []

# List of queries landing on hubs
for q in queries:
    qs = q["keys"][0]
    imp = q["impressions"]
    pos = q["position"]
    clk = q["clicks"]
    pages = [urlparse(p["keys"][1]).path for p in qp_map.get(qs, [])]
    
    # Check if all pages are hubs
    is_hub_landing = False
    for p in pages:
        parts = [x for x in p.strip("/").split("/") if x]
        if len(parts) == 1 or (len(parts) == 2 and parts[0] == "geometry" and parts[1] in ["2d", "3d", "shapes"]):
            is_hub_landing = True
            missing_opportunities.append({
                "type": "HUB_LANDING",
                "query": qs,
                "landing_page": p,
                "impressions": imp,
                "position": pos,
                "clicks": clk
            })
            break

print("=" * 90)
print(f"IDENTIFIED {len(missing_opportunities)} DIRECT MISSING TOOL QUERIES (LANDING ON HUBS):")
print("=" * 90)
for m in sorted(missing_opportunities, key=lambda x: -x["impressions"]):
    print(f"[{m['impressions']:2d} imp | pos {m['position']:5.1f}] '{m['query']}' -> landed on hub: {m['landing_page']}")

# Also check for other specific queries in the dataset:
print("\n" + "=" * 90)
print("ADDITIONAL HIGH-INTENT QUERIES TO VERIFY COVERAGE:")
print("=" * 90)

special_queries = [
    "slant height", "cone", "frustum", "cylinder", "dihedral angle", "rhombus",
    "lcl", "freight volume", "container load",
    "relative potency", "rrf", "aet", "chromatography", "injection rate", "trp", "um to ng",
    "slenderness", "overturning", "beam path", "closed end displacement", "haunch bar", "flow fill", "soling", "unistrut", "hydraulic",
    "peak shaving", "incremental borrowing", "aerodynamic", "circumferential speed"
]

for sq in special_queries:
    matches = [q for q in queries if sq in q["keys"][0].lower()]
    if matches:
        print(f"\nKeyword: '{sq}' ({len(matches)} queries):")
        for m in sorted(matches, key=lambda x: -x["impressions"]):
            pages = [urlparse(p["keys"][1]).path for p in qp_map.get(m["keys"][0], [])]
            print(f"  [{m['impressions']} imp, pos {m['position']:.1f}] '{m['keys'][0]}' -> {', '.join(pages)}")
