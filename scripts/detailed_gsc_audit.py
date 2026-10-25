#!/usr/bin/env python3
"""
scripts/detailed_gsc_audit.py
Detailed analysis of all 1,061 queries from Google Search Console.
"""

import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

with open(REPO_ROOT / "data" / "gsc_full_report.json") as f:
    data = json.load(f)

queries = data["queries"]
query_pages = data["query_pages"]

qp_map = {}
for qp in query_pages:
    q = qp["keys"][0]
    p = qp["keys"][1]
    qp_map.setdefault(q, []).append(qp)

# Let's inspect:
# 1. Top queries by impressions
print("=" * 80)
print("TOP 50 QUERIES BY IMPRESSIONS:")
print("=" * 80)
sorted_queries = sorted(queries, key=lambda x: x["impressions"], reverse=True)
for i, q in enumerate(sorted_queries[:50], 1):
    q_str = q["keys"][0]
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    pages = [p["keys"][1].replace("https://omnioperand.com", "") for p in qp_map.get(q_str, [])]
    pages_str = ", ".join(pages) if pages else "No landing page recorded"
    print(f"{i:2d}. [{imp:3d} imp | {clk:2d} clk | pos {pos:5.1f}] '{q_str}' -> {pages_str}")

# 2. Striking distance queries (position <= 30)
print("\n" + "=" * 80)
print("TOP STRIKING DISTANCE QUERIES (Position <= 30):")
print("=" * 80)
striking = [q for q in queries if q["position"] <= 30]
striking = sorted(striking, key=lambda x: x["position"])
for i, q in enumerate(striking, 1):
    q_str = q["keys"][0]
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    pages = [p["keys"][1].replace("https://omnioperand.com", "") for p in qp_map.get(q_str, [])]
    pages_str = ", ".join(pages) if pages else "No landing page recorded"
    print(f"{i:2d}. [pos {pos:4.1f} | {imp:2d} imp | {clk:1d} clk] '{q_str}' -> {pages_str}")

# 3. Queries with clicks
print("\n" + "=" * 80)
print("QUERIES THAT GENERATED CLICKS:")
print("=" * 80)
clicked = [q for q in queries if q["clicks"] > 0]
for q in clicked:
    q_str = q["keys"][0]
    imp = q["impressions"]
    clk = q["clicks"]
    pos = q["position"]
    pages = [p["keys"][1].replace("https://omnioperand.com", "") for p in qp_map.get(q_str, [])]
    pages_str = ", ".join(pages) if pages else "No landing page recorded"
    print(f"  [{clk} clicks | {imp} imp | pos {pos:4.1f}] '{q_str}' -> {pages_str}")

# 4. Hub landing queries
print("\n" + "=" * 80)
print("QUERIES LANDING ON CATEGORY HUBS (NO DIRECT CALCULATOR):")
print("=" * 80)
hub_queries = []
for q in queries:
    q_str = q["keys"][0]
    pages = qp_map.get(q_str, [])
    for p in pages:
        p_url = p["keys"][1].replace("https://omnioperand.com", "")
        # Hub check
        parts = [x for x in p_url.strip("/").split("/") if x]
        if len(parts) == 1 or (len(parts) == 2 and parts[0] == "geometry" and parts[1] in ["2d", "3d", "shapes"]):
            hub_queries.append((q_str, q["impressions"], q["position"], p_url))

hub_queries = sorted(hub_queries, key=lambda x: x[1], reverse=True)
for q_str, imp, pos, p_url in hub_queries:
    print(f"  [{imp} imp | pos {pos:4.1f}] '{q_str}' -> landed on: {p_url}")

