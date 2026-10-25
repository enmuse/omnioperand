#!/usr/bin/env python3
"""
scripts/fix_embed_button_placement.py
Fixes improper nesting of .calculator-actions-toolbar where it was mistakenly
injected inside .hero-badge instead of at the bottom of the hero section.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TOOLBAR_BLOCK = '''      <div class="calculator-actions-toolbar">
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      </div>'''

def fix_file(html_path: Path):
    content = html_path.read_text(encoding="utf-8")
    original = content
    
    # Pattern where toolbar was injected inside hero-badge
    # e.g.:
    # <div class="hero-badge">Badge text
    # <div class="calculator-actions-toolbar">...</div>
    # </div>
    nested_pattern = re.compile(
        r'(<div class="hero-badge">[\s\S]*?)\s*<div class="calculator-actions-toolbar">[\s\S]*?</div>\s*</div>',
        re.MULTILINE
    )
    
    match = nested_pattern.search(content)
    if match:
        badge_header = match.group(1).strip()
        # Clean the badge tag so it closes properly
        cleaned_badge = badge_header + "</div>"
        
        # Replace the entire broken badge block with cleaned badge
        content = nested_pattern.sub(cleaned_badge, content, count=1)
        
        # Now insert the toolbar at the proper location: after hero-subtext or before </section>
        # Look for the hero section
        if '</section>' in content and ('solver-hero' in content or 'calculator-hero' in content):
            # Place after </p> of hero-subtext if available
            if '<p class="hero-subtext">' in content:
                content = re.sub(
                    r'(<p class="hero-subtext">[\s\S]*?</p>)',
                    r'\1\n' + TOOLBAR_BLOCK,
                    content,
                    count=1
                )
            else:
                # Otherwise right before </section> of hero
                content = re.sub(
                    r'(<(?:section|div)[^>]*class="[^"]*(?:solver-hero|calculator-hero)[^"]*"[^>]*>[\s\S]*?)(</(?:section|div)>)',
                    r'\1\n' + TOOLBAR_BLOCK + r'\n\2',
                    content,
                    count=1
                )
    else:
        # Check if button is missing entirely
        if 'id="btn-embed"' not in content and 'btn-embed-calculator' not in content:
            if '<p class="hero-subtext">' in content and ('solver-hero' in content or 'calculator-hero' in content):
                content = re.sub(
                    r'(<p class="hero-subtext">[\s\S]*?</p>)',
                    r'\1\n' + TOOLBAR_BLOCK,
                    content,
                    count=1
                )
            elif '<div class="calculator-grid"' in content:
                content = content.replace(
                    '<div class="calculator-grid"',
                    TOOLBAR_BLOCK + '\n\n    <div class="calculator-grid"',
                    1
                )

    if content != original:
        html_path.write_text(content, encoding="utf-8")
        return True
    return False

def run():
    print("Fixing embed button placement across all calculator pages...")
    fixed = 0
    for p in REPO_ROOT.glob("**/*.html"):
        if any(x in p.parts for x in ['.git', '.gemini', 'node_modules', 'dist', 'api']):
            continue
        if fix_file(p):
            fixed += 1
            if fixed <= 10 or fixed % 100 == 0:
                print(f"  Fixed [{fixed}]: {p.relative_to(REPO_ROOT)}")
    print(f"✅ Successfully corrected embed button placement in {fixed} files!")

if __name__ == "__main__":
    run()
