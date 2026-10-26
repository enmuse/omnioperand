#!/usr/bin/env python3
"""
scripts/build_batch3_calculators.py
Production-grade builder for the 5 GSC gap calculators:
1. construction/polymeric-sand
2. construction/rafter-birdsmouth-cut
3. construction/gutter-downspout-sizing
4. engineering/three-phase-transformer-kva
5. finance/crypto-tax-hifo

Features:
- Exact Unicode mathematical typography (zero raw LaTeX backslash commands)
- Master Bidirectional Solver Matrix with parameter cards, sliders, and output metrics
- Embed Calculator Modal trigger in toolbar
- Dual AI Integration Box (human prompt + programmatic REST API)
- Contextual related solvers cluster
- Schema.org WebApplication & FAQPage JSON-LD
"""

import os
import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from unify_headers import build_uniform_header
from data_batch3_gap_calculators import BATCH3_CALCULATORS

CLUSTERS = {
    "construction": [
        {"title": "Polymeric Sand Calculator", "slug": "construction/polymeric-sand", "desc": "Paver joint sand bags, void volume, and 1-inch bedding base.", "icon": "🏛️"},
        {"title": "Rafter Length & Birdsmouth Cut", "slug": "construction/rafter-birdsmouth-cut", "desc": "Common rafter length, seat cuts, heel plumb depth, and overhang.", "icon": "📐"},
        {"title": "Gutter & Downspout Sizing", "slug": "construction/gutter-downspout-sizing", "desc": "Roof drainage flow rate, 5\"/6\" gutter sizing, and downspout capacity.", "icon": "🌧️"},
        {"title": "Brick Soling & Flat Masonry Area", "slug": "construction/brick-soling", "desc": "Flat and herringbone brick soling with joint mortar.", "icon": "🧱"},
        {"title": "Lean-To Roof Pitch & Rafters", "slug": "geometry/2d/lean-to-roof-pitch", "desc": "X:12 pitch ratio, rafter length, and plumb cuts.", "icon": "🏠"},
        {"title": "Concrete Volume Calculator", "slug": "construction/concrete-volume", "desc": "Slab, footing & column volume with 10% waste buffer.", "icon": "🧱"}
    ],
    "engineering": [
        {"title": "3-Phase Transformer kVA & Amps", "slug": "engineering/three-phase-transformer-kva", "desc": "Apparent power kVA, primary/secondary FLA, and NEC 450 sizing.", "icon": "⚡"},
        {"title": "Generator Sizing Calculator", "slug": "engineering/generator-sizing", "desc": "Running watts, peak surge kVA, and generator rating.", "icon": "⚡"},
        {"title": "Wire Gauge & Voltage Drop (NEC)", "slug": "engineering/wire-gauge-voltage-drop", "desc": "NEC 3% limit, conductor size AWG/mm², and drop %.", "icon": "🔌"},
        {"title": "Column Slenderness & Critical Buckling", "slug": "engineering/column-slenderness-buckling", "desc": "Euler critical buckling load, effective length K, and AISC 360.", "icon": "🏛️"},
        {"title": "Hydraulic Cylinder Force & Fluid Flow", "slug": "engineering/hydraulic-cylinder-flow", "desc": "Push/pull force, rod velocity, and pump flow GPM.", "icon": "💧"}
    ],
    "finance": [
        {"title": "Crypto Capital Gains & HIFO Tax", "slug": "finance/crypto-tax-hifo", "desc": "Compare HIFO, FIFO, and LIFO cost basis to minimize crypto taxes.", "icon": "🪙"},
        {"title": "ROAS & Breakeven Calculator", "slug": "finance/roas", "desc": "Return on ad spend, breakeven margin, and net ad profit.", "icon": "📊"},
        {"title": "SEPP 72(t) Early Distribution", "slug": "finance/sepp-72t-distribution", "desc": "Penalty-free early retirement withdrawal methods.", "icon": "💰"},
        {"title": "HECM Reverse Mortgage Calculator", "slug": "finance/reverse-mortgage", "desc": "Principal Limit Factor (PLF) and net proceeds (no info required).", "icon": "🏡"},
        {"title": "Mortgage Amortization Schedule", "slug": "finance/mortgage-amortization", "desc": "Principal, interest, and payoff acceleration breakdown.", "icon": "🏦"}
    ]
}

def render_related_tools_html(cluster_key: str, current_slug: str) -> str:
    tools = CLUSTERS.get(cluster_key, [])
    filtered = [t for t in tools if t["slug"] != current_slug][:4]
    if not filtered:
        return ""
    
    cards = []
    for t in filtered:
        card = f'''
        <a href="/{t['slug']}/" class="related-tool-card" style="display:flex; flex-direction:column; padding:1.25rem; background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:12px; text-decoration:none; transition:all 0.15s ease;">
          <div style="font-size:1.5rem; margin-bottom:0.5rem;">{t['icon']}</div>
          <strong style="color:var(--text-bright); font-size:0.95rem; margin-bottom:0.35rem;">{t['title']}</strong>
          <span style="color:var(--text-secondary); font-size:0.825rem; line-height:1.4;">{t['desc']}</span>
        </a>
        '''
        cards.append(card)
        
    return f'''
    <section class="related-tools-section" style="margin-top:3.5rem; padding-top:2.5rem; border-top:1px solid var(--border-subtle);">
      <h2 style="font-size:1.35rem; margin-bottom:1.25rem; color:var(--text-bright);">Related High-Precision Solvers</h2>
      <div class="related-tools-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:1rem;">
        {''.join(cards)}
      </div>
    </section>
    '''

def build_calculator_html(calc):
    slug = calc["slug"]
    category = calc["category"]
    name = calc["name"]
    title = calc["title"]
    description = calc["description"]
    canonical_url = f"https://omnioperand.com/{slug}/"
    hero_badge = calc.get("hero_badge", f"{category.capitalize()} Engine • Verified Invariants")
    hero_subtext = calc.get("hero_subtext", description)
    jurisdiction = calc.get("governing_jurisdiction")
    has_dual_units = calc.get("has_dual_units", False)
    cluster = calc.get("cluster", category)
    
    # Breadcrumbs
    path_segments = slug.split('/')
    breadcrumbs_ld = [
        {"@type": "ListItem", "position": 1, "name": "OmniOperand", "item": "https://omnioperand.com/"}
    ]
    accum = ""
    for idx, seg in enumerate(path_segments):
        accum += f"{seg}/"
        is_last = (idx == len(path_segments) - 1)
        seg_name = name if is_last else seg.replace('-', ' ').title()
        breadcrumbs_ld.append({
            "@type": "ListItem",
            "position": idx + 2,
            "name": seg_name,
            "item": f"https://omnioperand.com/{accum}"
        })
        
    # FAQs Schema
    faq_ld = []
    for f in calc.get("faqs", []):
        faq_ld.append({
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f["a"]
            }
        })
        
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "@id": f"{canonical_url}#app",
                "name": name,
                "url": canonical_url,
                "applicationCategory": f"{category.capitalize()}Application",
                "operatingSystem": "All",
                "browserRequirements": "Requires JavaScript",
                "description": description,
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumbs",
                "itemListElement": breadcrumbs_ld
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": faq_ld
            }
        ]
    }
    
    # Header
    nav_html = build_uniform_header(f"{slug}/index.html")
    
    # Unit toggle HTML
    unit_toggle_html = ""
    if has_dual_units:
        unit_toggle_html = '''
        <div class="unit-toggle-group" style="display:flex; align-items:center; gap:0.5rem; background:var(--bg-card); padding:0.25rem 0.5rem; border-radius:8px; border:1px solid var(--border-subtle);">
          <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">UNITS:</span>
          <button type="button" class="unit-pill active" id="unit-btn-imperial" onclick="setUnits('imperial')">Imperial (US)</button>
          <button type="button" class="unit-pill" id="unit-btn-metric" onclick="setUnits('metric')">Metric (SI)</button>
        </div>
        '''
        
    toolbar_html = f'''
    <div class="solver-toolbar" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; padding-bottom:1.25rem; margin-bottom:1.5rem; border-bottom:1px solid var(--border-subtle);">
      {unit_toggle_html}
      <div class="toolbar-group" style="display:flex; gap:0.5rem; margin-left:auto;">
        <button type="button" class="btn-action" id="btn-embed" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 0.8rem; background:rgba(168,85,247,0.1); border:1px solid rgba(168,85,247,0.3); border-radius:6px; color:var(--accent-purple); font-size:0.85rem; font-weight:600; cursor:pointer; transition:all 0.15s ease;">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
          <span>Embed Calculator</span>
        </button>
        <button type="button" class="btn-action" id="share-calc-btn" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 0.8rem; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); border-radius:6px; color:var(--accent-cyan); font-size:0.85rem; font-weight:600; cursor:pointer; transition:all 0.15s ease;">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
          <span id="share-btn-text">Share</span>
        </button>
      </div>
    </div>
    '''
    
    # Input parameter cards
    inputs_html = []
    for inp in calc.get("inputs", []):
        inp_id = inp["id"]
        label = inp["label"]
        inp_type = inp.get("type", "number")
        hint = inp.get("hint", "")
        unit = inp.get("unit", "")
        metric_unit = inp.get("metric_unit", unit)
        
        if inp_type == "select":
            opts = "".join([f'<option value="{val}" {"selected" if str(val) == str(inp["default"]) else ""}>{txt}</option>' for val, txt in inp["options"]])
            card = f'''
            <div class="param-card">
              <div class="param-label-row">
                <label for="param-{inp_id}">{label}</label>
                <span class="param-symbol">{inp_id}</span>
              </div>
              <div class="input-unit-group">
                <select id="param-{inp_id}" class="number-input omni-calc-input" data-id="{inp_id}" style="width:100%; cursor:pointer;">
                  {opts}
                </select>
              </div>
              {f'<div class="param-hint">{hint}</div>' if hint else ''}
            </div>
            '''
        else:
            val = inp["default"]
            min_v = inp.get("min", 0)
            max_v = inp.get("max", 100)
            step = inp.get("step", 1)
            card = f'''
            <div class="param-card">
              <div class="param-label-row">
                <label for="param-{inp_id}">{label}</label>
                <span class="param-symbol">{inp_id}</span>
              </div>
              <div class="input-unit-group">
                <input type="number" id="param-{inp_id}" class="number-input omni-calc-input" data-id="{inp_id}" value="{val}" step="{step}" min="{min_v}" max="{max_v}">
                <span class="input-suffix" id="unit-suffix-{inp_id}" data-imp="{unit}" data-met="{metric_unit}">{unit}</span>
              </div>
              <input type="range" id="slider-{inp_id}" class="param-slider omni-calc-slider" data-id="{inp_id}" min="{min_v}" max="{max_v}" step="{step}" value="{val}">
              {f'<div class="param-hint">{hint}</div>' if hint else ''}
            </div>
            '''
        inputs_html.append(card)
        
    # Output metric cards
    outputs_html = []
    for out in calc.get("outputs", []):
        out_id = out["id"]
        label = out["label"]
        color = out.get("color", "var(--text-bright)")
        m_box = f'''
        <div class="metric-card">
          <span class="metric-label">{label}</span>
          <span class="metric-value" id="disp-{out_id}" style="color:{color};">—</span>
        </div>
        '''
        outputs_html.append(m_box)
        
    # Proof Steps HTML
    proofs_html = []
    for idx, p in enumerate(calc.get("proof_steps", [])):
        p_box = f'''
        <div class="proof-step">
          <div class="step-num">{idx + 1}</div>
          <div class="step-content">
            <strong>{p["step_title"]}</strong>
            <p>{p["step_text"]}</p>
          </div>
        </div>
        '''
        proofs_html.append(p_box)
        
    # FAQs Accordion HTML
    faqs_html = []
    for f in calc.get("faqs", []):
        f_box = f'''
        <div class="faq-item">
          <button type="button" class="faq-question">
            <span>{f["q"]}</span>
            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div class="faq-answer">
            <p>{f["a"]}</p>
          </div>
        </div>
        '''
        faqs_html.append(f_box)
        
    related_html = render_related_tools_html(cluster, slug)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">

  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="website">

  <link rel="stylesheet" href="/assets/css/omni-core.css?v=2.2">
  <link rel="stylesheet" href="/assets/css/calculator.css?v=1.3">
  <link rel="icon" type="image/png" href="/assets/images/logo.png">
  <link rel="apple-touch-icon" href="/assets/images/logo.png">

  <script type="application/ld+json">
{json.dumps(json_ld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body class="calculator-page">
  <a href="#main-content" class="skip-link">Skip to main content</a>
  {nav_html}

  <main id="main-content" class="calc-main">
    <div class="container">
      <header class="calc-header">
        <div class="hero-badge">{hero_badge}</div>
        <h1>{name}</h1>
        <p class="calc-subtext">{hero_subtext}</p>
        {f'<div class="authority-badge" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.25rem 0.6rem; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); border-radius:6px; font-size:0.75rem; color:var(--accent-emerald); font-weight:600; margin-top:0.5rem;"><svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>Governed by {jurisdiction}</div>' if jurisdiction else ''}
      </header>

      <section class="solver-interface" aria-label="Interactive Calculator HUD">
        {toolbar_html}
        
        <div class="solver-grid">
          <div class="params-column">
            <h2 class="section-title">Input Parameters</h2>
            <div class="params-grid">
              {''.join(inputs_html)}
            </div>
          </div>

          <div class="results-column">
            <h2 class="section-title">Calculated Outputs</h2>
            <div class="metrics-grid">
              {''.join(outputs_html)}
            </div>

            <div class="blueprint-card" style="margin-top:1.5rem; background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:12px; padding:1.25rem;">
              <h3 style="font-size:0.95rem; font-weight:700; color:var(--text-bright); margin-bottom:0.75rem;">Verified Mathematical Identity</h3>
              <div class="formula-box" style="font-family:var(--font-mono); font-size:0.85rem; line-height:1.5; color:var(--accent-cyan); background:var(--bg-card); padding:0.75rem; border-radius:8px; border:1px solid var(--border-subtle);">
                {calc.get("formula_display", "")}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Step-by-Step Proofs & Derivations -->
      <section class="proof-section" style="margin-top:3.5rem;">
        <h2 style="font-size:1.35rem; color:var(--text-bright); margin-bottom:1.25rem;">Analytical Derivation &amp; Methodology</h2>
        <div class="proof-steps-container">
          {''.join(proofs_html)}
        </div>
      </section>

      <!-- Dual AI Prompt & REST API Integration Box -->
      <section class="ai-box" style="margin-top:3.5rem; background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:16px; padding:2rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
          <span style="font-size:1.5rem;">🤖</span>
          <h2 style="font-size:1.25rem; color:var(--text-bright); margin:0;">AI Agent &amp; LLM Integration</h2>
        </div>
        <p style="color:var(--text-secondary); font-size:0.9rem; line-height:1.5; margin-bottom:1.5rem;">
          Feed verified mathematical context directly into ChatGPT, Claude, and Gemini, or call our programmatic REST endpoint.
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem;">
          <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:12px; padding:1.25rem; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="font-weight:700; color:var(--text-bright); font-size:0.95rem; margin-bottom:0.4rem;">Human Chat Prompt</div>
              <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.4; margin-bottom:0.75rem;">Copy active parameters and system instructions to eliminate model hallucinations.</p>
            </div>
            <button type="button" class="btn-action" id="copy-ai-prompt-btn" style="width:100%; display:inline-flex; align-items:center; justify-content:center; gap:0.5rem; padding:0.6rem; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); border-radius:8px; color:var(--accent-cyan); font-weight:600; font-size:0.85rem; cursor:pointer;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span>Copy Prompt for AI</span>
            </button>
          </div>

          <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:12px; padding:1.25rem; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <div style="font-weight:700; color:var(--text-bright); font-size:0.95rem; margin-bottom:0.4rem;">Programmatic REST API</div>
              <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.4; margin-bottom:0.75rem;">Sub-15ms edge compute endpoint returning floating-point &amp; radical invariants.</p>
            </div>
            <button type="button" class="btn-action" id="copy-api-url-btn" style="width:100%; display:inline-flex; align-items:center; justify-content:center; gap:0.5rem; padding:0.6rem; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:8px; color:var(--accent-emerald); font-weight:600; font-size:0.85rem; cursor:pointer;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
              <span>Copy API Endpoint</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Frequently Asked Questions -->
      <section class="faq-section" style="margin-top:3.5rem;">
        <h2 style="font-size:1.35rem; color:var(--text-bright); margin-bottom:1.25rem;">Frequently Asked Questions</h2>
        <div class="faq-accordion">
          {''.join(faqs_html)}
        </div>
      </section>

      <!-- Related Solvers -->
      {related_html}
    </div>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
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
  </footer>

  <script src="/assets/js/omni-search.js?v=2.4" defer></script>
  <script src="/assets/js/embed-modal.js?v=1.1" defer></script>
  <script>
    function getNum(id) {{
      const el = document.getElementById('param-' + id);
      return el ? parseFloat(el.value) || 0 : 0;
    }}
    function setDisp(id, val) {{
      const el = document.getElementById('disp-' + id);
      if (el) el.textContent = val;
    }}
    function fmt(num, dec = 2) {{
      return Number(num).toLocaleString('en-US', {{ minimumFractionDigits: dec, maximumFractionDigits: dec }});
    }}

    function calculate() {{
{calc.get("js_logic", "")}
    }}

    // Sync input and sliders
    document.querySelectorAll('.omni-calc-input').forEach(input => {{
      const id = input.dataset.id;
      const slider = document.getElementById('slider-' + id);
      input.addEventListener('input', () => {{
        if (slider) slider.value = input.value;
        calculate();
      }});
      if (slider) {{
        slider.addEventListener('input', () => {{
          input.value = slider.value;
          calculate();
        }});
      }}
    }});

    // URL parameter sharing
    function getShareUrl() {{
      const params = new URLSearchParams();
      document.querySelectorAll('.omni-calc-input').forEach(inp => {{
        params.set(inp.dataset.id, inp.value);
      }});
      return window.location.origin + window.location.pathname + '?' + params.toString();
    }}

    const shareBtn = document.getElementById('share-calc-btn');
    if (shareBtn) {{
      shareBtn.addEventListener('click', () => {{
        navigator.clipboard.writeText(getShareUrl()).then(() => {{
          const txt = document.getElementById('share-btn-text');
          txt.textContent = 'Link Copied!';
          setTimeout(() => txt.textContent = 'Share', 2000);
        }});
      }});
    }}

    // AI Prompt Copy
    const copyPromptBtn = document.getElementById('copy-ai-prompt-btn');
    if (copyPromptBtn) {{
      copyPromptBtn.addEventListener('click', () => {{
        const LF = String.fromCharCode(10);
        let promptLines = ['Problem Context for {name}:'];
        document.querySelectorAll('.omni-calc-input').forEach(inp => {{
          promptLines.push('- ' + inp.dataset.id + ': ' + inp.value);
        }});
        promptLines.push('');
        promptLines.push('Please verify using exact formulas: {calc.get('formula_display', '').replace('"', "'")}' );
        const promptText = promptLines.join(LF);
        navigator.clipboard.writeText(promptText).then(() => {{
          const span = copyPromptBtn.querySelector('span');
          span.textContent = 'Prompt Copied!';
          setTimeout(() => span.textContent = 'Copy Prompt for AI', 2000);
        }});
      }});
    }}

    // API URL Copy
    const copyApiBtn = document.getElementById('copy-api-url-btn');
    if (copyApiBtn) {{
      copyApiBtn.addEventListener('click', () => {{
        navigator.clipboard.writeText('https://omnioperand.com/api/v1/{slug}').then(() => {{
          const span = copyApiBtn.querySelector('span');
          span.textContent = 'Endpoint Copied!';
          setTimeout(() => span.textContent = 'Copy API Endpoint', 2000);
        }});
      }});
    }}

    // FAQ Accordion
    document.querySelectorAll('.faq-question').forEach(q => {{
      q.addEventListener('click', () => {{
        const item = q.closest('.faq-item');
        item.classList.toggle('active');
      }});
    }});

    window.addEventListener('DOMContentLoaded', calculate);
  </script>
</body>
</html>
'''

def main():
    print("=========================================================")
    print("🚀 Building GSC Batch 3 Gap Calculators")
    print(f"Total to build: {len(BATCH3_CALCULATORS)}")
    print("=========================================================\n")
    
    for calc in BATCH3_CALCULATORS:
        slug = calc["slug"]
        out_dir = REPO_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        
        html = build_calculator_html(calc)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ Built: {slug} (file://{out_file})")
        
    print("\n🎉 All 5 gap calculators built successfully!")

if __name__ == "__main__":
    main()
