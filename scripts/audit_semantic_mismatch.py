#!/usr/bin/env python3
"""
scripts/audit_semantic_mismatch.py
Checks whether queries landing on calculators have high semantic divergence from the page.
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

candidates = []

for q in queries:
    qs = q["keys"][0].lower()
    imp = q["impressions"]
    pos = q["position"]
    pages = [urlparse(p["keys"][1]).path for p in qp_map.get(q["keys"][0], [])]
    
    for p in pages:
        slug = p.strip("/").split("/")[-1]
        parent = p.strip("/").split("/")[0] if "/" in p.strip("/") else ""
        
        # Check specific intent divergences
        # e.g., query has terms not present in slug or synonyms
        words = [w for w in qs.split() if len(w) > 3 and w not in ["calculator", "calculate", "formula", "omni", "what", "with", "from", "that", "this", "which", "free", "best", "online", "chart", "rate"]]
        
        # Check if words match slug
        slug_clean = slug.replace("-", " ")
        overlap = [w for w in words if w in slug_clean]
        
        # If very low overlap and not a hub
        if len(words) >= 2 and len(overlap) == 0 and parent not in ["de", "es", "fr", "it", "fi", "nl", "no", "pl", "pt", "ro", "sv"]:
            candidates.append({
                "query": q["keys"][0],
                "page": p,
                "impressions": imp,
                "position": pos,
                "words": words,
                "slug": slug
            })

print(f"Total potential semantic divergence candidates: {len(candidates)}")
# Sort by impressions desc
for c in sorted(candidates, key=lambda x: -x["impressions"])[:40]:
    print(f"[{c['impressions']} imp, pos {c['position']:.1f}] '{c['query']}' -> {c['page']}")

