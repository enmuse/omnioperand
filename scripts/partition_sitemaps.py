#!/usr/bin/env python3
"""
scripts/partition_sitemaps.py — OmniOperand Partitioned Sitemap Index Engine
Splits monolithic sitemap into domain & language partitioned XML sitemaps:
- sitemap-index.xml (Master Index)
- sitemap-en.xml (General & Science)
- sitemap-engineering.xml (Engineering, Construction, Energy, Civil)
- sitemap-finance.xml (Mortgage, Lending, Islamic, Wealth)
- sitemap-es.xml, sitemap-fr.xml, sitemap-de.xml, sitemap-it.xml, sitemap-pt.xml,
  sitemap-nl.xml, sitemap-pl.xml, sitemap-sv.xml, sitemap-no.xml, sitemap-fi.xml, sitemap-ro.xml
"""

import os
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent

LANG_CODES = ["es", "fr", "de", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"]

def write_urlset_file(filepath: Path, urls: list, lastmod: str = None):
    if not lastmod:
        lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url, prio, freq in sorted(urls, key=lambda x: x[0]):
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>\n")
    filepath.write_text("\n".join(lines), encoding="utf-8")

def main():
    print("=========================================================")
    print("🗺️ OmniOperand Partitioned Sitemap Generator")
    print("=========================================================")

    # Buckets
    buckets = {
        "en": [],
        "engineering": [],
        "finance": []
    }
    for code in LANG_CODES:
        buckets[code] = []

    # Scan all HTML files
    for p in REPO_ROOT.glob("**/index.html"):
        if ".git" in p.parts or "scratch" in p.parts:
            continue
        rel = p.parent.relative_to(REPO_ROOT)
        rel_str = str(rel)

        if rel_str == ".":
            url = "https://omnioperand.com/"
            prio = "1.0"
            freq = "weekly"
            buckets["en"].append((url, prio, freq))
            continue

        url = f"https://omnioperand.com/{rel_str}/"
        parts = rel_str.split("/")
        first_segment = parts[0]

        if first_segment in LANG_CODES:
            prio = "0.8"
            freq = "weekly"
            buckets[first_segment].append((url, prio, freq))
        else:
            # English pages
            prio = "0.9" if len(parts) <= 2 else "0.85"
            freq = "weekly"
            if first_segment in ("engineering", "construction", "civil", "energy"):
                buckets["engineering"].append((url, prio, freq))
            elif first_segment == "finance":
                buckets["finance"].append((url, prio, freq))
            else:
                buckets["en"].append((url, prio, freq))

    # Write each partition
    sitemap_files = []
    
    # 1. sitemap-en.xml
    p_en = REPO_ROOT / "sitemap-en.xml"
    write_urlset_file(p_en, buckets["en"])
    sitemap_files.append("sitemap-en.xml")
    print(f"  ✅ sitemap-en.xml: {len(buckets['en'])} URLs")

    # 2. sitemap-engineering.xml
    p_eng = REPO_ROOT / "sitemap-engineering.xml"
    write_urlset_file(p_eng, buckets["engineering"])
    sitemap_files.append("sitemap-engineering.xml")
    print(f"  ✅ sitemap-engineering.xml: {len(buckets['engineering'])} URLs")

    # 3. sitemap-finance.xml
    p_fin = REPO_ROOT / "sitemap-finance.xml"
    write_urlset_file(p_fin, buckets["finance"])
    sitemap_files.append("sitemap-finance.xml")
    print(f"  ✅ sitemap-finance.xml: {len(buckets['finance'])} URLs")

    # 4. Localized sitemaps
    for code in LANG_CODES:
        p_lang = REPO_ROOT / f"sitemap-{code}.xml"
        write_urlset_file(p_lang, buckets[code])
        sitemap_files.append(f"sitemap-{code}.xml")
        print(f"  ✅ sitemap-{code}.xml: {len(buckets[code])} URLs")

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 5. Master monolithic sitemap.xml (all URLs across all partitions)
    all_urls = []
    for b_urls in buckets.values():
        all_urls.extend(b_urls)
    p_master = REPO_ROOT / "sitemap.xml"
    write_urlset_file(p_master, all_urls, lastmod=today_str)
    print(f"  ✅ sitemap.xml: {len(all_urls)} URLs (Monolithic Canonical)")

    # Total URLs
    total_urls = len(all_urls)
    print(f"\n📊 Total indexed URLs across partitions: {total_urls}")

    # Build sitemap-index.xml
    index_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for sm in sitemap_files:
        index_lines.append("  <sitemap>")
        index_lines.append(f"    <loc>https://omnioperand.com/{sm}</loc>")
        index_lines.append(f"    <lastmod>{today_str}</lastmod>")
        index_lines.append("  </sitemap>")
    index_lines.append("</sitemapindex>\n")
    
    (REPO_ROOT / "sitemap-index.xml").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"  ✅ sitemap-index.xml generated with {len(sitemap_files)} partitioned sitemaps!")

    # Update robots.txt to declare sitemap-index.xml
    robots_file = REPO_ROOT / "robots.txt"
    robots_content = """User-agent: *
Allow: /

# Canonical Sitemaps & LLM Manifests
Sitemap: https://omnioperand.com/sitemap-index.xml
Sitemap: https://omnioperand.com/sitemap.xml
# LLM-Spec: https://omnioperand.com/llms.txt
# LLM-Full: https://omnioperand.com/llms-full.txt
"""
    robots_file.write_text(robots_content, encoding="utf-8")
    print("  ✅ robots.txt updated with sitemap-index.xml declaration!")

if __name__ == "__main__":
    main()
