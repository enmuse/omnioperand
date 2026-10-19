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
                "subhubs": {
                    "shapes": {
                        "title": "Polygons & Geometric Shapes",
                        "description": "Regular and equilateral polygon solvers with exact radical expressions and live Cartesian blueprints.",
                        "icon": "🛑",
                        "calculators": [
                            {
                                "slug": "octagon",
                                "name": "Regular Octagon Calculator",
                                "description": "8-sided regular polygon solver for side length, area, perimeter, apothem, circumradius, and 3 distinct diagonals.",
                                "status": "active",
                                "inputs": ["side", "area", "perimeter", "apothem", "circumradius", "span", "short_diag", "long_diag"]
                            },
                            {
                                "slug": "hexagon",
                                "name": "Regular Hexagon Calculator",
                                "description": "6-sided regular polygon solver with minimal/maximal diameters and tessellation metrics.",
                                "status": "roadmap",
                                "inputs": ["side", "area", "perimeter", "apothem", "circumradius"]
                            },
                            {
                                "slug": "pentagon",
                                "name": "Regular Pentagon Calculator",
                                "description": "5-sided regular polygon governed by the golden ratio and pentagram diagonals.",
                                "status": "roadmap",
                                "inputs": ["side", "area", "perimeter", "apothem", "circumradius"]
                            }
                        ]
                    }
                }
            }
        }
    },
    "calculus": {
        "title": "Calculus & Mathematical Analysis",
        "description": "Differential, integral, and multivariable calculus solvers.",
        "icon": "∫",
        "accent": "var(--accent-emerald)",
        "subcategories": {}
    },
    "finance": {
        "title": "Quantitative Finance & Actuarial Math",
        "description": "Options pricing, compound yields, amortization matrices, and discounted cash flows.",
        "icon": "📈",
        "accent": "var(--accent-violet)",
        "subcategories": {}
    },
    "physics": {
        "title": "Physics & Engineering Mechanics",
        "description": "Kinematics, thermodynamics, fluid dynamics, and electrical circuits.",
        "icon": "⚡",
        "accent": "var(--accent-amber)",
        "subcategories": {}
    },
    "statistics": {
        "title": "Probability & Statistics",
        "description": "Stochastic distributions, hypothesis tests, and linear regressions.",
        "icon": "📊",
        "accent": "var(--accent-blue)",
        "subcategories": {}
    }
}

def generate_sitemap():
    """Generates canonical sitemap.xml from taxonomy."""
    urls = [
        ("https://omnioperand.com/", "1.0", "weekly"),
    ]

    for cat_slug, cat_data in TAXONOMY.items():
        urls.append((f"https://omnioperand.com/{cat_slug}/", "0.9", "weekly"))
        for sub_slug, sub_data in cat_data.get("subcategories", {}).items():
            urls.append((f"https://omnioperand.com/{cat_slug}/{sub_slug}/", "0.9", "weekly"))
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
        for sub_slug, sub_data in cat_data.get("subcategories", {}).items():
            print(f"   └── 📂 {sub_data['title']} (/{cat_slug}/{sub_slug}/)")
            for hub_slug, hub_data in sub_data.get("subhubs", {}).items():
                print(f"       └── 📂 {hub_data['title']} (/{cat_slug}/{sub_slug}/{hub_slug}/)")
                for calc in hub_data.get("calculators", []):
                    total_calcs += 1
                    status_badge = "🟢 LIVE" if calc["status"] == "active" else "🟡 ROADMAP"
                    if calc["status"] == "active":
                        active_calcs += 1
                    print(f"           └── {status_badge} {calc['name']} (/{calc['slug']}/)")

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
        parser.print_help()

if __name__ == "__main__":
    main()
