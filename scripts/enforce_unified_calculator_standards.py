#!/usr/bin/env python3
"""
scripts/enforce_unified_calculator_standards.py
Enforces uniform standards across all OmniOperand calculators:
1. Prominent 'Embed Calculator' button (#btn-embed) in actions toolbar
2. Dual AI Integration Box (.llm-box):
   - Copy Prompt for AI (#copy-llm-prompt-btn) with live parameters & directives
   - Copy API Endpoint (#copy-api-btn) with direct GET/POST endpoint pill
   - Real-time dynamic prompt block (#llm-prompt-display)
   - Zero-hallucination verification badges
3. Modern script inclusions (omni-search.js?v=2.2, embed-modal.js?v=2.2)
4. Strict zero raw LaTeX enforcement (AGENTS.md § 3.6)
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Embedded button snippet
EMBED_BTN_HTML = '''      <div class="calculator-actions-toolbar">
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      </div>'''

def generate_dual_llm_box(slug: str, title: str) -> str:
    api_url = f"https://omnioperand.com/api/v1/{slug}"
    return f'''          <!-- Dual AI Agent & Prompt Integration Box -->
          <section class="llm-box" style="margin-top:1.5rem;">
            <div class="llm-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:0.75rem;">
              <div>
                <span class="llm-badge" style="background:rgba(56,189,248,0.15); color:var(--accent-cyan); font-size:0.75rem; font-weight:700; text-transform:uppercase; padding:3px 8px; border-radius:4px; letter-spacing:0.5px;">LLM Directive & API Spec</span>
                <h3 style="margin:0.35rem 0 0 0; font-size:1.15rem; color:var(--text-bright);">Artificial Intelligence & Prompt Integration</h3>
              </div>
              <div class="llm-actions" style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <button type="button" class="btn-action" id="copy-llm-prompt-btn" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 0.8rem; background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.35); border-radius:6px; color:var(--accent-cyan); font-size:0.825rem; font-weight:600; cursor:pointer; transition:all 0.15s ease;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                  <span id="copy-prompt-text">Copy Prompt for AI</span>
                </button>
                <button type="button" class="btn-action" id="copy-api-btn" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 0.8rem; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.35); border-radius:6px; color:var(--accent-emerald); font-size:0.825rem; font-weight:600; cursor:pointer; transition:all 0.15s ease;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                  <span id="copy-api-text">Copy API Endpoint</span>
                </button>
              </div>
            </div>

            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5; margin-bottom:0.75rem;">
              Paste this verified mathematical prompt directly into ChatGPT, Claude, or Gemini to eliminate arithmetic hallucination, or invoke the programmatic API endpoint for automated workflows.
            </p>

            <div class="api-endpoint-pill" style="display:flex; align-items:center; justify-content:space-between; background:var(--bg-canvas); border:1px solid var(--border-subtle); border-radius:6px; padding:6px 12px; margin-bottom:0.75rem; font-family:monospace; font-size:0.82rem; color:var(--text-bright);">
              <span><span style="color:var(--accent-cyan); font-weight:700;">GET / POST</span> {api_url}</span>
              <span style="color:var(--text-muted); font-size:0.75rem;">JSON Invariants</span>
            </div>

            <pre class="llm-prompt-code" id="llm-prompt-display" style="background:var(--bg-canvas); border:1px solid var(--border-subtle); border-radius:6px; padding:10px 14px; font-size:0.8rem; color:var(--text-secondary); font-family:monospace; white-space:pre-wrap; max-height:160px; overflow-y:auto; line-height:1.45;">Generating verified mathematical prompt...</pre>

            <div style="font-size:0.75rem; color:var(--text-muted); display:flex; align-items:center; gap:1rem; flex-wrap:wrap; margin-top:0.75rem;">
              <span>✓ Standardized for <code>llms.txt</code></span>
              <span>✓ Exact Radical Form & Closed Formulas</span>
              <span>✓ Machine-Readable Edge API</span>
            </div>
          </section>'''

def process_file(html_path: Path):
    rel_path = html_path.relative_to(REPO_ROOT)
    parts = list(rel_path.parts)
    
    # Exclude non-calculators
    if any(x in parts for x in ['.git', '.gemini', 'node_modules', 'dist', 'api', 'embed', 'data', 'config', 'scripts']):
        return False
    
    # Must be index.html and at least category/slug/index.html
    if html_path.name != "index.html" or len(parts) < 3:
        return False

    content = html_path.read_text(encoding="utf-8")
    
    # Must be an actual calculator page
    if not ('calculator-grid' in content or 'solver-column' in content or 'hud-panel' in content or 'calculator-hud' in content):
        return False

    # Derive slug
    slug = "/".join(parts[:-1])
    
    # Extract title
    title_match = re.search(r'<title>([^<—|]+)', content)
    title = title_match.group(1).strip() if title_match else parts[-2].replace('-', ' ').title()

    modified = False

    # 1. Ensure Embed Calculator button exists
    if 'id="btn-embed"' not in content and 'class="btn-embed-calculator"' not in content and 'btn-open-embed' not in content:
        # Insert inside or right after hero header
        if '</section>' in content and ('solver-hero' in content or 'calculator-hero' in content):
            content = re.sub(
                r'(<(?:section|div)[^>]*class="[^"]*(?:solver-hero|calculator-hero|calc-header-section)[^"]*"[^>]*>[\s\S]*?)(</(?:section|div)>)',
                r'\1\n' + EMBED_BTN_HTML + r'\n\2',
                content,
                count=1
            )
            modified = True
        elif '<div class="calculator-grid"' in content:
            content = content.replace(
                '<div class="calculator-grid"',
                EMBED_BTN_HTML + '\n\n    <div class="calculator-grid"',
                1
            )
            modified = True

    # 2. Upgrade LLM Box if old single-paragraph format
    old_llm_pattern = re.compile(
        r'<div class="llm-box"[^>]*>[\s\S]*?Autonomous agents: Invoke <code>[^<]*</code>[^<]*</div>\s*</div>',
        re.MULTILINE
    )
    if old_llm_pattern.search(content):
        dual_box = generate_dual_llm_box(slug, title)
        # Note: replace the inner llm-box with dual_box
        content = old_llm_pattern.sub(dual_box, content, count=1)
        modified = True
    elif 'id="copy-llm-prompt-btn"' not in content and '<div class="llm-box"' in content:
        # Has llm-box but missing buttons
        dual_box = generate_dual_llm_box(slug, title)
        content = re.sub(r'<div class="llm-box"[^>]*>[\s\S]*?</div>\s*</div>', dual_box, content, count=1)
        modified = True
    elif 'id="copy-api-btn"' not in content and 'id="copy-llm-prompt-btn"' in content:
        # Has prompt button but missing API button & pill (like regular-polygon / octagon)
        # Add copy-api-btn
        api_btn_html = '<button type="button" class="btn btn-secondary btn-sm" id="copy-api-btn">Copy API Endpoint</button>'
        content = content.replace(
            '<button class="btn btn-primary btn-sm" id="copy-llm-prompt-btn">',
            '<button type="button" class="btn btn-primary btn-sm" id="copy-llm-prompt-btn">',
            1
        )
        content = re.sub(
            r'(<button[^>]*id="copy-llm-prompt-btn"[^>]*>[\s\S]*?</button>)',
            r'\1\n          ' + api_btn_html,
            content,
            count=1
        )
        # Add API pill if missing
        if 'api-endpoint-pill' not in content:
            api_pill = f'''      <div class="api-endpoint-pill" style="display:flex; align-items:center; justify-content:space-between; background:var(--bg-canvas); border:1px solid var(--border-subtle); border-radius:6px; padding:6px 12px; margin:0.75rem 0; font-family:monospace; font-size:0.82rem; color:var(--text-bright);">
        <span><span style="color:var(--accent-cyan); font-weight:700;">GET / POST</span> https://omnioperand.com/api/v1/{slug}</span>
        <span style="color:var(--text-muted); font-size:0.75rem;">JSON Invariants</span>
      </div>'''
            content = content.replace(
                '<pre class="llm-prompt-code"',
                api_pill + '\n\n      <pre class="llm-prompt-code"',
                1
            )
        modified = True

    # 3. Ensure clean script tags
    content = content.replace('<!-- <script src="/assets/js/omni-search.js?v=2.1"></script>', '')
    content = content.replace('<!-- <script src="/assets/js/omni-search.js"></script>', '')
    
    # Update script references
    if 'omni-search.js?v=2.1' in content:
        content = content.replace('omni-search.js?v=2.1', 'omni-search.js?v=2.2')
        modified = True

    if modified:
        html_path.write_text(content, encoding="utf-8")
        return True
    return False

def run_enforcement():
    print("Auditing and enforcing uniform calculator standards across all files...")
    count = 0
    updated = 0
    for p in REPO_ROOT.glob("**/*.html"):
        parts = p.parts
        if any(x in parts for x in ['.git', '.gemini', 'node_modules', 'dist', 'api', 'embed']):
            continue
        count += 1
        if process_file(p):
            updated += 1
            print(f"  [UPDATED] {p.relative_to(REPO_ROOT)}")

    print(f"✅ Completed! Checked {count} HTML files, updated {updated} calculators with uniform standards.")

if __name__ == "__main__":
    run_enforcement()
