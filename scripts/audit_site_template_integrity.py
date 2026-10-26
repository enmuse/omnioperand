#!/usr/bin/env python3
"""
scripts/audit_site_template_integrity.py
Comprehensive template, functionality, and feature integrity audit across all pages.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def audit_site():
    html_files = sorted(list(REPO_ROOT.glob("**/*.html")))
    html_files = [f for f in html_files if not any(x in f.parts for x in ['.git', '.gemini', 'node_modules', 'dist'])]
    print(f"Auditing {len(html_files)} HTML files...")

    results = {
        "old_omni_core_css": [],
        "old_search_js": [],
        "missing_header_nav": [],
        "missing_lang_dropdown": [],
        "missing_search_btn": [],
        "missing_theme_btn": [],
        "missing_embed_modal_script": [],
        "calc_missing_embed_btn": [],
        "calc_missing_llm_box": [],
        "calc_missing_api_btn": [],
        "calc_missing_faq": [],
        "broken_script_src": set(),
        "raw_latex_found": [],
        "missing_canonical": [],
        "missing_title": [],
        "missing_description": [],
        "missing_viewport": [],
        "missing_og_tags": [],
        "shape_missing_switcher": []
    }

    script_pattern = re.compile(r'<script[^>]+src=["\']([^"\']+)["\']')
    latex_pattern = re.compile(r'\\(frac|alpha|theta|beta|pi|sum|lim|sqrt|cdot|implies|le|ge)\b')

    shape_slugs = {"regular-polygon", "octagon", "hexagon", "pentagon", "decagon"}

    for f in html_files:
        rel = f.relative_to(REPO_ROOT)
        rel_str = str(rel).replace('\\', '/')
        content = f.read_text(encoding="utf-8", errors="ignore")

        # 1. Base SEO tags
        if '<title>' not in content or '</title>' not in content:
            results["missing_title"].append(rel_str)
        if '<meta name="description"' not in content and '<meta name=\'description\'' not in content:
            results["missing_description"].append(rel_str)
        if '<link rel="canonical"' not in content and '<link rel=\'canonical\'' not in content:
            results["missing_canonical"].append(rel_str)
        if '<meta name="viewport"' not in content:
            results["missing_viewport"].append(rel_str)
        if '<meta property="og:title"' not in content:
            results["missing_og_tags"].append(rel_str)

        # 2. CSS & JS cache-busting
        if 'omni-core.css' in content and 'omni-core.css?v=2.2' not in content:
            results["old_omni_core_css"].append(rel_str)
        if 'omni-search.js' in content and 'omni-search.js?v=2.4' not in content:
            results["old_search_js"].append(rel_str)

        # 3. Header & Navigation checks (skip 404.html, embed iframes)
        if '<header' in content and '404.html' not in rel_str and 'embed' not in rel.parts:
            if 'nav-dropdown' not in content and 'Disciplines' not in content:
                results["missing_header_nav"].append(rel_str)
            if 'lang-dropdown' not in content:
                results["missing_lang_dropdown"].append(rel_str)
            if 'global-search-trigger' not in content:
                results["missing_search_btn"].append(rel_str)
            if 'theme-toggle-btn' not in content:
                results["missing_theme_btn"].append(rel_str)

        # 4. Check for broken script tags
        for src in script_pattern.findall(content):
            clean_src = src.split('?')[0]
            if clean_src.startswith('/'):
                local_path = REPO_ROOT / clean_src.lstrip('/')
                if not local_path.exists():
                    results["broken_script_src"].add((clean_src, rel_str))

        # 5. Calculators checks
        is_calc = any(marker in content for marker in ['calculator-grid', 'solver-column', 'hud-panel', 'calculator-hud'])
        if is_calc and '404.html' not in rel_str and 'embed' not in rel.parts:
            if 'btn-embed' not in content and 'btn-open-embed' not in content and 'btn-embed-calculator' not in content:
                results["calc_missing_embed_btn"].append(rel_str)
            if 'embed-modal.js' not in content:
                results["missing_embed_modal_script"].append(rel_str)
            if 'llm-box' not in content:
                results["calc_missing_llm_box"].append(rel_str)
            elif 'copy-api-btn' not in content:
                results["calc_missing_api_btn"].append(rel_str)
            if not any(faq_marker in content for faq_marker in ['faq-section', 'faq-accordion', 'Frequently Asked Questions', 'FAQ', 'faq-item']):
                results["calc_missing_faq"].append(rel_str)

        # 6. Shape Polygon Switcher Bar check (AGENTS.md § 3.7)
        parts = rel.parts
        # check if it is one of the shape calculators
        if len(parts) >= 2 and any(parts[-2] == s for s in shape_slugs):
            if 'Polygon Switcher Bar' not in content and 'polygon-switcher' not in content and 'Universal N-Gon' not in content:
                results["shape_missing_switcher"].append(rel_str)

        # 7. Raw LaTeX check
        if latex_pattern.search(content):
            # Exclude TikZ templates in blueprint-engine.js or json specs
            results["raw_latex_found"].append(rel_str)

    print("\n" + "="*50)
    print("SITE-WIDE AUDIT RESULTS")
    print("="*50)
    for k, v in results.items():
        if isinstance(v, (list, set)):
            count = len(v)
            status = "✅ PASS" if count == 0 else f"⚠️  {count} files"
            print(f"{k.ljust(30)}: {status}")
            if count > 0 and count <= 15:
                for item in v:
                    print(f"    - {item}")
            elif count > 15:
                for item in list(v)[:5]:
                    print(f"    - {item}")
                print(f"    ... and {count - 5} more")

    return results

if __name__ == "__main__":
    audit_site()
