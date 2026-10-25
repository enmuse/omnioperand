#!/usr/bin/env python3
"""
scripts/audit_query_coverage.py
Analyzes all 1,061 GSC queries to determine exact calculator coverage:
1. Exact match / Dedicated Calculator: query lands on a dedicated calculator.
2. Category Hub landing: query lands on a hub like /biotech/, /logistics/, /engineering/ because no dedicated calculator exists.
3. Suboptimal / Intent Mismatch landing: query lands on a calculator that does not actually compute what the user wants.
4. Missing high-value calculators based on query search intent.
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

# Let's inspect the 28 hub landing queries first
hub_queries = []
for q in queries:
    q_str = q["keys"][0]
    pages = qp_map.get(q_str, [])
    for p in pages:
        u = urlparse(p["keys"][1]).path
        parts = [x for x in u.strip("/").split("/") if x]
        # Check if landing page is a category hub
        if len(parts) == 1 and parts[0] in [
            "biotech", "construction", "engineering", "agriculture",
            "energy", "health", "ecommerce", "logistics", "civil",
            "legal", "crypto", "calculus", "finance", "physics", "statistics"
        ]:
            hub_queries.append({
                "query": q_str,
                "hub": u,
                "impressions": q["impressions"],
                "position": q["position"],
                "clicks": q["clicks"]
            })
        elif len(parts) == 2 and parts[0] == "geometry" and parts[1] in ["2d", "3d", "shapes"]:
            hub_queries.append({
                "query": q_str,
                "hub": u,
                "impressions": q["impressions"],
                "position": q["position"],
                "clicks": q["clicks"]
            })
        elif len(parts) == 1 and parts[0] == "geometry":
            hub_queries.append({
                "query": q_str,
                "hub": u,
                "impressions": q["impressions"],
                "position": q["position"],
                "clicks": q["clicks"]
            })

print(f"Total Hub Landings: {len(hub_queries)}")
for h in sorted(hub_queries, key=lambda x: (x["hub"], -x["impressions"])):
    print(f"  Hub: {h['hub']:15} | [{h['impressions']} imp, pos {h['position']:.1f}] '{h['query']}'")

# Now let's analyze queries that landed on a specific calculator, but the query is looking for something distinct that may not be directly calculated or answered on that page:
all_calc_pages = set()
for qp in query_pages:
    u = urlparse(qp["keys"][1]).path
    all_calc_pages.add(u)

print("\n" + "=" * 80)
print("DEEP INTENT ANALYSIS OF QUERIES:")
print("=" * 80)

# Let's group queries by theme/intent
themes = {
    "Cylinder Geometry / Slant Height / Frustum": [],
    "Logistics / Freight / Dimensional Weight / Container": [],
    "Structural & Engineering (Unistrut, Slenderness, Overturning, Beam Path, Flow Fill)": [],
    "Biotech & Pharma (Relative Potency, RRF, AET, Chromatography, Injection Rate, uM to ng/mL)": [],
    "Finance / Tax / Leasing (Incremental Borrowing Rate, Section 1250 Recapture, Section 179)": [],
    "Construction & Trades (Soling, Deck Spacing, Asphalt, Swale)": [],
    "Physics & Aerodynamics (Circumferential Speed, Aerodynamics, Stopping Distance)": [],
    "Health / Medical / Fitness (Creatine, VO2 Max, MAP, Blood Alcohol)": []
}

for q in queries:
    qs = q["keys"][0].lower()
    imp = q["impressions"]
    pos = q["position"]
    pages = [urlparse(p["keys"][1]).path for p in qp_map.get(q["keys"][0], [])]
    p_str = ", ".join(pages)
    
    # Categorize
    if any(k in qs for k in ["cyclinder", "cylinder", "frustum", "slant height", "truncated cone", "dihedral angle", "rhombus", "arc calculator", "chord", "sector", "segment"]):
        themes["Cylinder Geometry / Slant Height / Frustum"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["freight", "container load", "dim weight", "ti hi", "warehouse", "logistics volume", "pallet"]):
        themes["Logistics / Freight / Dimensional Weight / Container"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["unistrut", "slenderness", "overturning", "beam path", "flow fill", "haunch bar", "closed end displacement", "calcul hidraulic", "hydraulic", "transformer kva"]):
        themes["Structural & Engineering (Unistrut, Slenderness, Overturning, Beam Path, Flow Fill)"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["potency", "rrf", "aet", "chromatography", "injection rate", "um to ng", "ng/ml", "trp calculation", "annealing temperature", "tm calculator", "doubling time"]):
        themes["Biotech & Pharma (Relative Potency, RRF, AET, Chromatography, Injection Rate, uM to ng/mL)"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["incremental borrowing", "1250", "179", "proration", "tenant improvement", "rsu tax", "child tax credit", "qbi", "sepp", "reverse mortgage"]):
        themes["Finance / Tax / Leasing (Incremental Borrowing Rate, Section 1250 Recapture, Section 179)"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["soling", "deck", "swale", "joist", "paver", "paint", "asphalt", "rebar", "gutter"]):
        themes["Construction & Trades (Soling, Deck Spacing, Asphalt, Swale)"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["aerodynamic", "circumferential speed", "stopping distance", "climb rate", "kinetic energy", "torque"]):
        themes["Physics & Aerodynamics (Circumferential Speed, Aerodynamics, Stopping Distance)"].append((q["keys"][0], imp, pos, p_str))
    elif any(k in qs for k in ["creatin", "vo2", "map", "bac", "alcohol", "body weight", "smoking", "gestational"]):
        themes["Health / Medical / Fitness (Creatine, VO2 Max, MAP, Blood Alcohol)"].append((q["keys"][0], imp, pos, p_str))

for theme_name, q_list in themes.items():
    print(f"\n### {theme_name} ({len(q_list)} queries):")
    for q_str, imp, pos, p_str in sorted(q_list, key=lambda x: -x[1])[:10]:
        print(f"  [{imp:2d} imp | pos {pos:4.1f}] '{q_str}' -> {p_str}")
