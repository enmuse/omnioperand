#!/usr/bin/env python3
"""
scripts/generate_calculators.py — Programmatic Calculator Generator & Taxonomy Builder

OmniOperand Scalable Architecture:
Defines categories, subcategories, hubs, and individual calculators.
Can rebuild the static hierarchy, generate new calculator templates,
and maintain the XML sitemap and llms.txt index.
"""

import os
import sys
import json
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Master Taxonomy Registry
TAXONOMY = {
    "geometry": {
        "title": "Geometry & Spatial Analysis",
        "description": "Euclidean, analytic, and differential geometry solvers.",
        "icon": "📐",
        "accent": "var(--accent-cyan)",
        "subcategories": {
            "2d": {
                "title": "Two-Dimensional (2D) Geometry",
                "description": "Planar figures including regular polygons, triangles, quadrilaterals, circles, and conic curves.",
                "icon": "📐",
                "calculators": [
                    {
                        "slug": "right-triangle",
                        "name": "Right Triangle & Pythagorean Solver",
                        "description": "12-variable right triangle solver for legs, hypotenuse, altitude, inradius, and acute angles.",
                        "status": "active"
                    },
                    {
                        "slug": "circle-sector",
                        "name": "Circle Sector & Segment Solver",
                        "description": "Circle curve solver for arc length, chord length, sagitta height, sector area, and segment area.",
                        "status": "active"
                    },
                    {
                        "slug": "roof-pitch",
                        "name": "Roof Pitch & Rafter Length Solver",
                        "description": "Carpentry roof slope solver for pitch-in-12, degrees, rafter length, plumb cuts, and birdsmouth cuts.",
                        "status": "active"
                    }
                ],
                "subhubs": {
                    "shapes": {
                        "title": "Polygons & Geometric Shapes",
                        "description": "Regular and equilateral polygon solvers with exact radical expressions and live Cartesian blueprints.",
                        "icon": "🛑",
                        "calculators": [
                            {
                                "slug": "regular-polygon",
                                "name": "Universal Regular Polygon Calculator",
                                "description": "Arbitrary n-sided regular polygon solver for side length, area, perimeter, apothem, circumradius, and Archimedean convergence.",
                                "status": "active"
                            },
                            {
                                "slug": "octagon",
                                "name": "Regular Octagon Calculator",
                                "description": "8-sided regular polygon solver for side length, area, perimeter, apothem, circumradius, and 3 distinct diagonals.",
                                "status": "active"
                            },
                            {
                                "slug": "hexagon",
                                "name": "Regular Hexagon Calculator",
                                "description": "6-sided regular polygon solver with minimal/maximal diameters, circumradius R=a, and honeycomb metrics.",
                                "status": "active"
                            },
                            {
                                "slug": "pentagon",
                                "name": "Regular Pentagon Calculator",
                                "description": "5-sided regular polygon governed by the golden ratio and pentagram diagonals.",
                                "status": "active"
                            },
                            {
                                "slug": "decagon",
                                "name": "Regular Decagon Calculator",
                                "description": "10-sided regular polygon with circumradius R=a·ϕ, flat-to-flat span, and 4 diagonal classes.",
                                "status": "active"
                            }
                        ]
                    }
                }
            },
            "3d": {
                "title": "Three-Dimensional (3D) Geometry",
                "description": "Spatial polyhedra, cylinders, prisms, and civil engineering volumetric calculations.",
                "icon": "🧊",
                "calculators": [
                    {
                        "slug": "concrete-volume",
                        "name": "Concrete Volume & Bag Count Calculator",
                        "description": "Cubic yards, cubic feet, cubic meters, and 60lb/80lb premix bags for slabs, footings, and cylindrical columns.",
                        "status": "active"
                    }
                ],
                "subhubs": {}
            }
        }
    },
    "calculus": {
        "title": "Calculus & Mathematical Analysis",
        "description": "Differential, integral, and multivariable calculus solvers.",
        "icon": "∫",
        "accent": "var(--accent-emerald)",
        "calculators": [
            {
                "slug": "integrals",
                "name": "Definite & Indefinite Integral Calculator",
                "description": "Evaluates exact closed-form antiderivatives, definite integrals, and Simpson's/Trapezoidal Riemann sums.",
                "status": "active"
            },
            {
                "slug": "derivatives",
                "name": "Derivative & Tangent Line Calculator",
                "description": "Computes polynomial derivatives, instantaneous slope, tangent lines, normal lines, and concavity.",
                "status": "active"
            }
        ],
        "subcategories": {}
    },
    "finance": {
        "title": "Quantitative Finance & Actuarial Math",
        "description": "Options pricing, compound yields, amortization matrices, and discounted cash flows.",
        "icon": "📈",
        "accent": "var(--accent-violet)",
        "calculators": [
            {
                "slug": "mortgage-amortization",
                "name": "Mortgage Amortization & Early Payoff Calculator",
                "description": "Fixed-rate mortgage payment matrix, borrowing capacity inversion, and accelerated payoff savings.",
                "status": "active"
            },
            {
                "slug": "compound-interest",
                "name": "Compound Interest & Investment Growth Calculator",
                "description": "Discrete and continuous compounding, periodic deposits, APY conversions, and savings goal inversions.",
                "status": "active"
            },
            {
                "slug": "cagr",
                "name": "Compound Annual Growth Rate (CAGR) Calculator",
                "description": "Geometric mean growth rate, portfolio doubling periods via Rule of 72, and target valuation inversions.",
                "status": "active"
            },
            {
                "slug": "auto-loan",
                "name": "Auto Loan & Car Affordability Calculator",
                "description": "Car loan installment payments, trade-in sales tax credits, dealer fees, and affordability inversion.",
                "status": "active"
            }
        ],
        "subcategories": {}
    },
    "physics": {
        "title": "Physics & Engineering Mechanics",
        "description": "Kinematics, thermodynamics, fluid dynamics, and electrical circuits.",
        "icon": "⚡",
        "accent": "var(--accent-amber)",
        "calculators": [],
        "subcategories": {}
    },
    "statistics": {
        "title": "Probability & Statistics",
        "description": "Stochastic distributions, hypothesis tests, and linear regressions.",
        "icon": "📊",
        "accent": "var(--accent-blue)",
        "calculators": [],
        "subcategories": {}
    }
}

def generate_sitemap():
    """Generates canonical sitemap.xml from taxonomy."""
    urls = [
        ("https://omnioperand.com/", "1.0", "weekly"),
        ("https://omnioperand.com/api/", "0.9", "weekly")
    ]

    for cat_slug, cat_data in TAXONOMY.items():
        urls.append((f"https://omnioperand.com/{cat_slug}/", "0.9", "weekly"))
        # Direct category calculators
        for calc in cat_data.get("calculators", []):
            if calc.get("status") == "active":
                urls.append((f"https://omnioperand.com/{cat_slug}/{calc['slug']}/", "1.0", "daily"))

        for sub_slug, sub_data in cat_data.get("subcategories", {}).items():
            urls.append((f"https://omnioperand.com/{cat_slug}/{sub_slug}/", "0.9", "weekly"))
            # Subcategory calculators
            for calc in sub_data.get("calculators", []):
                if calc.get("status") == "active":
                    urls.append((f"https://omnioperand.com/{cat_slug}/{sub_slug}/{calc['slug']}/", "1.0", "daily"))

            for hub_slug, hub_data in sub_data.get("subhubs", {}).items():
                urls.append((f"https://omnioperand.com/{cat_slug}/{sub_slug}/{hub_slug}/", "0.9", "weekly"))
                for calc in hub_data.get("calculators", []):
                    if calc.get("status") == "active":
                        urls.append((f"https://omnioperand.com/{cat_slug}/{sub_slug}/{hub_slug}/{calc['slug']}/", "1.0", "daily"))

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url, prio, freq in urls:
        sitemap_lines.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-10-19</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>')
    sitemap_lines.append('</urlset>')

    sitemap_path = REPO_ROOT / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines) + "\n")
    print(f"✅ Generated sitemap.xml with {len(urls)} URLs")

def list_inventory():
    """Prints the current taxonomy tree and calculator statuses."""
    print("=========================================================")
    print("📐 OmniOperand Calculator Inventory & Hub Tree")
    print("=========================================================")
    total_calcs = 0
    active_calcs = 0

    for cat_slug, cat_data in TAXONOMY.items():
        print(f"\n📁 [{cat_data['icon']}] {cat_data['title']} (/{cat_slug}/)")
        for calc in cat_data.get("calculators", []):
            total_calcs += 1
            status_badge = "🟢 LIVE" if calc["status"] == "active" else "🟡 ROADMAP"
            if calc["status"] == "active":
                active_calcs += 1
            print(f"   └── {status_badge} {calc['name']} (/{cat_slug}/{calc['slug']}/)")

        for sub_slug, sub_data in cat_data.get("subcategories", {}).items():
            print(f"   └── 📂 {sub_data['title']} (/{cat_slug}/{sub_slug}/)")
            for calc in sub_data.get("calculators", []):
                total_calcs += 1
                status_badge = "🟢 LIVE" if calc["status"] == "active" else "🟡 ROADMAP"
                if calc["status"] == "active":
                    active_calcs += 1
                print(f"       └── {status_badge} {calc['name']} (/{cat_slug}/{sub_slug}/{calc['slug']}/)")

            for hub_slug, hub_data in sub_data.get("subhubs", {}).items():
                print(f"       └── 📂 {hub_data['title']} (/{cat_slug}/{sub_slug}/{hub_slug}/)")
                for calc in hub_data.get("calculators", []):
                    total_calcs += 1
                    status_badge = "🟢 LIVE" if calc["status"] == "active" else "🟡 ROADMAP"
                    if calc["status"] == "active":
                        active_calcs += 1
                    print(f"           └── {status_badge} {calc['name']} (/{cat_slug}/{sub_slug}/{hub_slug}/{calc['slug']}/)")

    print("\n---------------------------------------------------------")
    print(f"Total Defined Calculators: {total_calcs} | Active Production Solvers: {active_calcs}")
    print("=========================================================\n")

def main():
    parser = argparse.ArgumentParser(description="OmniOperand Calculator Generator")
    parser.add_argument("--list", action="store_true", help="List all taxonomy hubs and calculators")
    parser.add_argument("--sitemap", action="store_true", help="Regenerate canonical sitemap.xml")
    parser.add_argument("--build-all", action="store_true", help="Rebuild and verify all taxonomy assets")
    args = parser.parse_args()

    if args.list:
        list_inventory()
    elif args.sitemap:
        generate_sitemap()
    elif args.build_all:
        print("🚀 Rebuilding OmniOperand taxonomy and sitemaps...")
        generate_sitemap()
        list_inventory()
        print("✨ Build completed successfully!")
    else:
        list_inventory()
        generate_sitemap()

if __name__ == "__main__":
    main()
