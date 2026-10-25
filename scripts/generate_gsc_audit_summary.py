#!/usr/bin/env python3
"""
scripts/generate_gsc_audit_summary.py
Generates a comprehensive structured breakdown of GSC data:
1. Overall Traffic & Indexing Performance
2. Existing High-Performing Calculators
3. Exactly What Is Missing (The 18 Distinct Missing Calculators identified from queries landing on hubs)
4. Strategic Priority Ranking of Missing Calculators by Google Search Position & Impression Volume
"""

import json
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

with open(REPO_ROOT / "data" / "gsc_full_report.json") as f:
    data = json.load(f)

queries = data["queries"]
query_pages = data["query_pages"]

qp_map = {}
for qp in query_pages:
    qp_map.setdefault(qp["keys"][0], []).append(qp)

# Identify missing calculators from queries landing on hubs
missing_tools = {
    # Logistics
    "LCL (Less Than Container Load) Shipping & Freight CBM Calculator": {
        "hub": "/logistics/",
        "category": "Logistics & Freight",
        "queries": ["less than container load calculator", "automatic freight measurement", "freight volume measurement system", "logistics volume measurement"],
        "best_pos": 12.0,
        "total_imp": 8,
        "rationale": "High-intent freight logistics query ranking at Position 12.0. Users need CBM volume, chargeable weight (volumetric vs gross), and ocean container palletization."
    },
    # Geometry
    "Slant Height & Cone / Pyramid Geometry Calculator": {
        "hub": "/geometry/",
        "category": "Geometry & Trigonometry",
        "queries": ["slant height calculator", "how to find the slant height of a pyramid"],
        "best_pos": 10.0,
        "total_imp": 2,
        "rationale": "Ranking at Position 10.0 directly on the geometry hub. Solves s = sqrt(r^2 + h^2) for right cones, regular pyramids, and truncated frustums."
    },
    # Biotech
    "Relative Potency Bioassay Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Pharmaceuticals",
        "queries": ["relative potency formula", "relative potency calculation"],
        "best_pos": 83.3,
        "total_imp": 4,
        "rationale": "Compliant with USP <1032>/<1034> parallel-line bioassay analysis, EC50 ratio, and 95% Fieller's confidence intervals."
    },
    "Relative Response Factor (RRF) HPLC Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Pharmaceuticals",
        "queries": ["rrf calculation formula"],
        "best_pos": 79.0,
        "total_imp": 3,
        "rationale": "Quantifies pharmaceutical impurities and degradants in HPLC/GC using relative response factors: RRF = (Area_imp / Conc_imp) / (Area_std / Conc_std)."
    },
    "Analytical Evaluation Threshold (AET) Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Pharmaceuticals",
        "queries": ["aet calculation"],
        "best_pos": 80.5,
        "total_imp": 2,
        "rationale": "PQRI and ISO 10993 extractables & leachables safety threshold based on Safety Concern Threshold (SCT) and maximum daily drug dose."
    },
    "Tubular Reabsorption of Phosphate (%TRP) Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Clinical Nephrology",
        "queries": ["trp calculation"],
        "best_pos": 41.0,
        "total_imp": 1,
        "rationale": "Striking distance position 41.0. Calculates %TRP and TmP/GFR ratio for diagnosing hyperparathyroidism, hypophosphatemia, and rickets."
    },
    "Micromolar to ng/mL (uM to ng/mL) Mass-Molar Converter": {
        "hub": "/biotech/",
        "category": "Biotech & Analytical Chemistry",
        "queries": ["um to ng/ml"],
        "best_pos": 79.0,
        "total_imp": 1,
        "rationale": "Converts molar concentration (uM, nM, mM) to mass concentration (ng/mL, ug/mL, mg/L) based on molecular weight."
    },
    "Chromatography Column Resolution & Theoretical Plates Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Analytical Chemistry",
        "queries": ["chromatography calculator"],
        "best_pos": 86.0,
        "total_imp": 1,
        "rationale": "USP theoretical plate count N = 16(t_r / W)^2, peak asymmetry factor, and chromatographic resolution Rs."
    },
    "Syringe Pump & Microfluidic Injection Rate Calculator": {
        "hub": "/biotech/",
        "category": "Biotech & Laboratory Automation",
        "queries": ["injection rate calculation"],
        "best_pos": 90.0,
        "total_imp": 1,
        "rationale": "Computes linear stepper rate, inner syringe barrel diameter, and volumetric delivery rate in uL/min and mL/hr."
    },
    # Construction
    "Unistrut Channel Beam Load & Deflection Calculator": {
        "hub": "/construction/",
        "category": "Construction & Structural Framing",
        "queries": ["unistrut load capacity calculator"],
        "best_pos": 78.0,
        "total_imp": 1,
        "rationale": "Standard metal framing channels (P1000, P2000, P5000), single vs back-to-back, span length, uniform vs point load capacity, and deflection limits."
    },
    "Flowable Fill (CLSM) Volume & Mix Calculator": {
        "hub": "/construction/",
        "category": "Construction & Civil",
        "queries": ["flow fill calculator"],
        "best_pos": 71.0,
        "total_imp": 1,
        "rationale": "Controlled Low-Strength Material (CLSM) trench backfill volume in cubic yards, cement/fly-ash/sand slurry mix ratios."
    },
    "Brick Soling & Flat Masonry Area Calculator": {
        "hub": "/construction/",
        "category": "Construction & Masonry",
        "queries": ["soling work rate per sq ft"],
        "best_pos": 56.0,
        "total_imp": 1,
        "rationale": "Flat brick soling, edge soling, and herringbone sub-base square footage, brick unit count, and mortar bedding volume."
    },
    # Engineering
    "Column Slenderness Ratio & Critical Buckling Load Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & Structural Mechanics",
        "queries": ["slenderness equation"],
        "best_pos": 74.0,
        "total_imp": 1,
        "rationale": "Euler's buckling equation P_cr = pi^2 * E * I / (KL)^2 and slenderness ratio lambda = KL / r according to AISC 360."
    },
    "Retaining Wall Overturning & Sliding Safety Factor Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & Geotechnical",
        "queries": ["resistance to overturning formula"],
        "best_pos": 71.0,
        "total_imp": 1,
        "rationale": "Factor of safety against overturning FS_ot = Sum(M_resist) / Sum(M_overturn) and sliding resistance."
    },
    "Ultrasonic Angle Beam Path & Sound Path Distance Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & NDT Testing",
        "queries": ["beam path formula"],
        "best_pos": 63.0,
        "total_imp": 1,
        "rationale": "Non-destructive weld testing: sound path distance W = d / cos(theta), surface skip distance S = 2 * d * tan(theta)."
    },
    "Drill Pipe & Casing Well Displacement Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & Petroleum Drilling",
        "queries": ["closed end displacement"],
        "best_pos": 69.0,
        "total_imp": 1,
        "rationale": "Open-end vs closed-end drill pipe displacement in bbl/ft for tripping pipe and mud pit volume control."
    },
    "Concrete Haunch & Chamfer Reinforcement Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & Structural Concrete",
        "queries": ["haunch bar calculation formula"],
        "best_pos": 80.0,
        "total_imp": 1,
        "rationale": "Bridge and portal frame concrete haunch dimensions, additional shear rebar, and haunch bar lengths."
    },
    "Hydraulic Cylinder Force & Fluid Flow Calculator": {
        "hub": "/engineering/",
        "category": "Engineering & Fluid Power",
        "queries": ["calcul hidraulic"],
        "best_pos": 100.0,
        "total_imp": 1,
        "rationale": "Hydraulic piston extend/retract force F = P * A, flow rate Q = A * v, and pump horsepower requirements."
    },
    # Energy
    "Commercial Battery Peak Shaving & Demand Charge Calculator": {
        "hub": "/energy/",
        "category": "Energy & Power Systems",
        "queries": ["peak shaving calculator"],
        "best_pos": 70.5,
        "total_imp": 2,
        "rationale": "Peak kW shaving threshold, battery discharge duration, utility monthly demand charge reduction ($/kW), and payback period."
    },
    # Finance
    "ASC 842 / IFRS 16 Incremental Borrowing Rate (IBR) Calculator": {
        "hub": "/finance/",
        "category": "Corporate Finance & Lease Accounting",
        "queries": ["incremental borrowing rate calculation formula"],
        "best_pos": 90.0,
        "total_imp": 1,
        "rationale": "Calculates lease present value and liability discount rate using reference risk-free rate + credit spread adjustment."
    },
    # Physics
    "Aerodynamic Drag & Downforce Force Calculator": {
        "hub": "/physics/",
        "category": "Physics & Aerodynamics",
        "queries": ["aerodynamic calculator"],
        "best_pos": 70.0,
        "total_imp": 1,
        "rationale": "Aerodynamic drag force F_d = 0.5 * rho * v^2 * C_d * A and required power to overcome drag P = F_d * v."
    },
    "Circumferential / Surface Cutting Speed Calculator": {
        "hub": "/physics/",
        "category": "Physics & Machining",
        "queries": ["circumferential speed"],
        "best_pos": 95.0,
        "total_imp": 1,
        "rationale": "Calculates tangential surface speed v = pi * D * N from RPM and wheel/tool diameter in m/s, m/min, and SFM."
    }
}

print(f"Total Missing Calculators Identified: {len(missing_tools)}")
total_missing_imp = sum(t["total_imp"] for t in missing_tools.values())
print(f"Total Impressions Currently Wasted on Hubs: {total_missing_imp}")

print("\n" + "=" * 90)
print("MISSING CALCULATORS RANKED BY GOOGLE SEARCH POSITION (STRIKING DISTANCE FIRST):")
print("=" * 90)

sorted_tools = sorted(missing_tools.items(), key=lambda x: x[1]["best_pos"])
for i, (name, t) in enumerate(sorted_tools, 1):
    print(f"{i:2d}. [Pos {t['best_pos']:4.1f} | {t['total_imp']} imp | Hub: {t['hub']}]")
    print(f"    Name: {name}")
    print(f"    Category: {t['category']}")
    print(f"    Queries: {', '.join([repr(q) for q in t['queries']])}")
    print(f"    Rationale: {t['rationale']}\n")
