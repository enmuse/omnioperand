#!/usr/bin/env python3
"""
scripts/audit_routing_comprehensive.py
Comprehensive routing, redirect chain, sitemap, canonical, and link integrity audit for OmniOperand.
Verifies zero 301->404 loops, zero sitemap redirect leaks, and zero broken canonical tags.
"""

import os
import re
import sys
import glob
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent

def main():
    print("=" * 65)
    print("🔍 OMNIOPERAND COMPREHENSIVE ROUTING & REDIRECT AUDIT")
    print("=" * 65)

    errors = []
    warnings = []

    # 1. Index all static HTML routes on disk
    html_routes = set()
    file_map = {}
    for p in REPO_ROOT.rglob("*.html"):
        rel = p.relative_to(REPO_ROOT)
        rel_str = str(rel)
        if rel_str.startswith(".wrangler") or rel_str.startswith(".git") or rel_str.startswith("scratch"):
            continue
        
        if rel_str.endswith("index.html"):
            base = "/" + rel_str[:-10]
            route = base if base.endswith("/") else base + "/"
            html_routes.add(route)
            html_routes.add(route.rstrip("/"))
            file_map[route] = p
            file_map[route.rstrip("/")] = p
        else:
            route = "/" + rel_str
            html_routes.add(route)
            file_map[route] = p

    print(f"📁 Indexed {len(html_routes)} valid static route variations on disk.")

    # 2. Audit _redirects file
    redirects_file = REPO_ROOT / "_redirects"
    redirect_rules = []
    if redirects_file.exists():
        with open(redirects_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                clean = line.strip()
                if not clean or clean.startswith("#"):
                    continue
                parts = clean.split()
                if len(parts) >= 2:
                    src = parts[0]
                    dst = parts[1]
                    status = parts[2] if len(parts) >= 3 else "301"
                    redirect_rules.append((src, dst, status, line_no))

    print(f"📋 Auditing {len(redirect_rules)} rules in _redirects...")
    for src, dst, status, line_no in redirect_rules:
        # Check if dst is external
        if dst.startswith("http://") or dst.startswith("https://"):
            continue
        
        # Strip splat or wildcard from dst
        target_path = dst.replace(":splat", "").rstrip("*")
        if not target_path.endswith("/") and not "." in target_path.split("/")[-1]:
            target_path += "/"

        # Check if target exists on disk
        if target_path not in html_routes and target_path.rstrip("/") not in html_routes:
            errors.append(f"[_redirects L{line_no}] 301 Target 404: {src} -> {dst} (Path '{target_path}' does not exist on disk!)")

    # 3. Audit functions/_middleware.js hardcoded redirects
    middleware_file = REPO_ROOT / "functions" / "_middleware.js"
    print("⚙️ Auditing functions/_middleware.js redirect targets...")
    if middleware_file.exists():
        with open(middleware_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check explicit redirect paths
        explicit_redirects = [
            "/energy/solar-payback/",
            "/logistics/pallet-ti-hi-optimizer/",
            "/logistics/air-freight-chargeable-weight/",
            "/engineering/generator-sizing/",
            "/finance/rule-of-72/",
            "/finance/saas-rule-of-40/",
            "/finance/internal-rate-of-return/",
            "/finance/fsa-use-it-or-lose-it/"
        ]
        for path in explicit_redirects:
            if path not in html_routes:
                errors.append(f"[_middleware.js] Hardcoded redirect target 404: '{path}' does not exist on disk!")

        # Check UNTRANSLATED_CATEGORIES
        categories = re.findall(r'"([a-z0-9_-]+)"', content.split("UNTRANSLATED_CATEGORIES = new Set([")[1].split("]);")[0])
        for cat in categories:
            cat_path = f"/{cat}/"
            if cat_path not in html_routes:
                errors.append(f"[_middleware.js] Untranslated category redirect target 404: '{cat_path}' does not exist on disk!")

        # Check VALID_CALCULATORS_PATHS
        if "VALID_CALCULATORS_PATHS" in content:
            calc_paths = re.findall(r'"([a-z0-9_-]*)"', content.split("VALID_CALCULATORS_PATHS = new Set([")[1].split("]);")[0])
            for cp in calc_paths:
                if cp:
                    expected = f"/calculators/{cp}/"
                    if expected not in html_routes:
                        errors.append(f"[_middleware.js] Whitelisted calculator path missing on disk: '{expected}'!")

    # 4. Audit all Sitemaps
    sitemap_files = list(REPO_ROOT.glob("sitemap*.xml"))
    print(f"🗺️ Auditing {len(sitemap_files)} sitemap files...")
    all_sitemap_urls = set()
    for sm in sitemap_files:
        with open(sm, "r", encoding="utf-8") as f:
            sm_content = f.read()
        locs = re.findall(r"<loc>(.*?)</loc>", sm_content)
        for loc in locs:
            clean_loc = loc.strip()
            parsed = urlparse(clean_loc)
            path = parsed.path
            if not path.endswith("/") and not "." in path.split("/")[-1]:
                path += "/"
            all_sitemap_urls.add((clean_loc, path, sm.name))

            # Sitemap URLs should never 404
            if path not in html_routes and not path.endswith(".xml"):
                errors.append(f"[{sm.name}] Sitemap URL 404 on disk: {clean_loc} (Path: {path})")

            # Sitemap URLs should NEVER be caught by a 301 in _redirects
            for src, dst, status, line_no in redirect_rules:
                if src == path or (src.endswith("/*") and path.startswith(src[:-2])):
                    errors.append(f"[{sm.name}] Sitemap URL is 301 redirected by _redirects L{line_no}: {clean_loc} -> {dst}")

            # Sitemap URLs should NEVER be caught by legacy prefix redirection in middleware
            if path.startswith("/calculators/") and path != "/calculators/":
                sub = path.replace("/calculators/", "").split("/")[0]
                if sub not in calc_paths:
                    errors.append(f"[{sm.name}] Sitemap URL redirected by middleware /calculators/ rule: {clean_loc}")

    # 5. Audit Canonical Tags in HTML Files
    print(f"🏷️ Auditing canonical tags across HTML files...")
    canonical_count = 0
    for path, fpath in file_map.items():
        if not str(fpath).endswith("index.html"):
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        canon_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
        if canon_match:
            canonical_count += 1
            canon_url = canon_match.group(1).strip()
            parsed_canon = urlparse(canon_url)
            canon_path = parsed_canon.path
            if not canon_path.endswith("/"):
                canon_path += "/"

            # Normalize path
            norm_path = path if path.endswith("/") else path + "/"

            # Canonical path must exist on disk
            if canon_path not in html_routes:
                errors.append(f"[{fpath.relative_to(REPO_ROOT)}] Canonical URL points to 404: {canon_url} (Path: {canon_path})")

            # Canonical path should not mismatch own directory path (except for intended aliases)
            if canon_path != norm_path:
                warnings.append(f"[{fpath.relative_to(REPO_ROOT)}] Canonical mismatch: page={norm_path} vs canonical={canon_path}")

    # Summary Output
    print("\n" + "=" * 65)
    print("📊 AUDIT RESULTS SUMMARY")
    print("=" * 65)
    print(f"Total HTML files audited: {len(file_map)}")
    print(f"Total sitemap URLs audited: {len(all_sitemap_urls)}")
    print(f"Total _redirects rules audited: {len(redirect_rules)}")
    print(f"Total canonical tags audited: {canonical_count}")
    print(f"Errors found: {len(errors)}")
    print(f"Warnings found: {len(warnings)}")

    if warnings:
        print("\n⚠️ WARNINGS (Review for context):")
        for w in warnings[:15]:
            print(f"  - {w}")
        if len(warnings) > 15:
            print(f"  ... and {len(warnings) - 15} more warnings.")

    if errors:
        print("\n❌ CRITICAL ROUTING ERRORS (301 -> 404 or Sitemap 404):")
        for e in errors:
            print(f"  🚨 {e}")
        print("\nFix these errors immediately to prevent GSC indexation drops.")
        sys.exit(1)
    else:
        print("\n🎉 ZERO ROUTING ISSUES DETECTED! All redirects, sitemaps, and canonicals resolve to valid 200 OK paths.")

if __name__ == "__main__":
    main()
