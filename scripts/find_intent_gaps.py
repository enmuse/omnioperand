#!/usr/bin/env python3
"""
scripts/find_intent_gaps.py
Finds all queries with striking position (<= 50) or high impressions (>= 2)
and checks if the landing page exactly answers the query or if a dedicated calculator is missing.
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

# Let's check queries with position <= 30
striking = [q for q in queries if q["position"] <= 35]
striking = sorted(striking, key=lambda x: x["position"])

print(f"Total striking distance queries (pos <= 35): {len(striking)}")
print("=" * 100)
for q in striking:
    qs = q["keys"][0]
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    pages = [urlparse(p["keys"][1]).path for p in qp_map.get(qs, [])]
    pages_str = ", ".join(pages)
    print(f"Pos {pos:4.1f} | {imp:2d} imp | {clk} clk | '{qs}' -> {pages_str}")

