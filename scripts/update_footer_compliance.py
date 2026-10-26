#!/usr/bin/env python3
"""
scripts/update_footer_compliance.py
Updates the global footer across all HTML pages and template generators to the
standardized two-tier trust and compliance footer (Platform + Legal & Trust).
"""

import glob
import os
import re

NEW_FOOTER = """<footer class="site-footer">
  <div class="container footer-content" style="display:flex; flex-wrap:wrap; justify-content:space-between; gap:1.5rem; padding:2rem 0; border-top:1px solid var(--border-subtle);">
    <div class="footer-brand">
      <div style="font-weight:700; color:var(--text-bright); margin-bottom:0.5rem;">OmniOperand</div>
      <p style="font-size:0.8rem; color:var(--text-muted); max-width:320px; line-height:1.4;">
        Deterministic computational engines, verified mathematical proofs, and programmatic APIs for technical professionals.
      </p>
    </div>
    <div class="footer-links-grid" style="display:flex; gap:2.5rem; font-size:0.85rem;">
      <div class="footer-col" style="display:flex; flex-direction:column; gap:0.4rem;">
        <span style="font-weight:600; color:var(--text-primary); margin-bottom:4px;">Platform</span>
        <a href="/about/" style="color:var(--text-secondary); text-decoration:none;">About &amp; Methodology</a>
        <a href="/mcp/" style="color:var(--text-secondary); text-decoration:none;">MCP Server</a>
        <a href="/api/" style="color:var(--text-secondary); text-decoration:none;">REST API</a>
      </div>
      <div class="footer-col" style="display:flex; flex-direction:column; gap:0.4rem;">
        <span style="font-weight:600; color:var(--text-primary); margin-bottom:4px;">Legal &amp; Trust</span>
        <a href="/privacy/" style="color:var(--text-secondary); text-decoration:none;">Privacy Policy</a>
        <a href="/terms/" style="color:var(--text-secondary); text-decoration:none;">Terms of Service</a>
        <a href="/disclaimer/" style="color:var(--text-secondary); text-decoration:none;">Affiliate Disclosure</a>
      </div>
    </div>
  </div>
  <div class="container footer-bottom" style="display:flex; justify-content:space-between; align-items:center; padding:1rem 0; border-top:1px solid rgba(255,255,255,0.05); font-size:0.75rem; color:var(--text-muted);">
    <div>© 2026 OmniOperand. All mathematical proofs and calculations verified.</div>
    <div>Hosted on Cloudflare Edge • Pure Client-Side Math</div>
  </div>
</footer>"""

FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.DOTALL)

def update_html_files():
    total_updated = 0
    total_skipped = 0
    total_scanned = 0

    for root, dirs, files in os.walk('.'):
        # Skip .git and node_modules
        if '.git' in root or 'node_modules' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                total_scanned += 1
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if FOOTER_RE.search(content):
                    new_content, count = FOOTER_RE.subn(NEW_FOOTER, content, count=1)
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        total_updated += 1
                    else:
                        total_skipped += 1
                else:
                    print(f"Warning: No footer found in {path}")

    print(f"Scanned {total_scanned} HTML files: {total_updated} updated, {total_skipped} unchanged.")

def update_template_scripts():
    scripts = [
        'scripts/build_batch2_calculators.py',
        'scripts/build_financial_authority_suite.py',
        'scripts/build_gsc_suite.py',
        'scripts/build_full_calculator_suite.py'
    ]
    for s in scripts:
        if not os.path.exists(s):
            continue
        with open(s, 'r', encoding='utf-8') as f:
            c = f.read()
        new_c, count = FOOTER_RE.subn(NEW_FOOTER, c)
        if count > 0 and new_c != c:
            with open(s, 'w', encoding='utf-8') as f:
                f.write(new_c)
            print(f"Updated footer in template script: {s} ({count} replacements)")

if __name__ == '__main__':
    update_html_files()
    update_template_scripts()
