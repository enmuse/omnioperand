#!/usr/bin/env python3
"""
scripts/build_gsc_suite.py
Production-grade builder for:
1. 15 GSC High-Intent Missing Calculators
2. Italian Localized Page for 'dimensionamento gruppo elettrogeno' (/it/ingegneria/dimensionamento-gruppo-elettrogeno/)
3. Programmatic SEO enhancements for currently ranking pages (pregnancy-due-date, centrifuge-rcf-g-force, sepp-72t-distribution)
4. Contextual related tools cluster cross-linking
5. Instant above-the-fold URL parameter state sharing & dual unit toggling
6. Schema.org WebApplication (Offer price 0) & FAQPage JSON-LD
"""

import os
import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from unify_headers import build_uniform_header
from gsc_calculator_data import GSC_CALCULATORS

CLUSTERS = {
    "biotech": [
        {"title": "Centrifuge RCF to RPM Converter", "slug": "biotech/centrifuge-rcf-g-force", "desc": "Convert RPM to RCF g-force with rotor radius.", "icon": "🧪"},
        {"title": "qPCR Primer Tm Calculator", "slug": "biotech/qpcr-primer-tm", "desc": "Nearest-neighbor melting temperature and annealing Ta.", "icon": "🧬"},
        {"title": "PCR Primer Tm & GC Formula", "slug": "biotech/pcr-primer-tm", "desc": "Thermodynamic salt-corrected primer melting temp.", "icon": "🔬"},
        {"title": "Cockcroft-Gault CrCl Calculator", "slug": "biotech/cockcroft-gault-crcl", "desc": "Creatinine clearance and renal dosing adjustment.", "icon": "💊"},
        {"title": "Cell Culture Doubling Time", "slug": "biotech/cell-culture-doubling-time", "desc": "Cell proliferation kinetics and growth rate.", "icon": "🧫"}
    ],
    "construction": [
        {"title": "Concrete Volume Calculator", "slug": "construction/concrete-volume", "desc": "Slab, footing & column volume with 10% waste buffer.", "icon": "🧱"},
        {"title": "Rebar Grid & Spacing Calculator", "slug": "construction/rebar-calculator", "desc": "Linear feet, grid weight, and tie wire for slabs.", "icon": "🏗️"},
        {"title": "Drywall & Mud Estimator", "slug": "construction/drywall", "desc": "Sheet count, joint compound buckets, and screws.", "icon": "📐"},
        {"title": "Lean-To Roof Pitch & Rafters", "slug": "geometry/2d/lean-to-roof-pitch", "desc": "X:12 pitch ratio, rafter length, and plumb cuts.", "icon": "🏠"},
        {"title": "Paint Coverage Calculator", "slug": "construction/paint-coverage", "desc": "Wall and ceiling surface area in gallons of paint.", "icon": "🎨"},
        {"title": "Patio Paver & Sand Estimator", "slug": "construction/pavers", "desc": "Base gravel, bedding sand, and paver brick count.", "icon": "🏛️"}
    ],
    "engineering": [
        {"title": "Generator Sizing Calculator", "slug": "engineering/generator-sizing", "desc": "Running watts, peak surge kVA, and generator rating.", "icon": "⚡"},
        {"title": "Wire Gauge & Voltage Drop (NEC)", "slug": "engineering/wire-gauge-voltage-drop", "desc": "NEC 3% limit, conductor size AWG/mm², and drop %.", "icon": "🔌"},
        {"title": "Battery Backup Storage", "slug": "engineering/battery-backup-storage", "desc": "Household kWh autonomy, DoD, and battery bank Ah.", "icon": "🔋"},
        {"title": "HVAC Furnace & Heating BTU", "slug": "engineering/hvac-furnace-sizing", "desc": "Home heat loss, climate zone, and furnace tonnage.", "icon": "🔥"},
        {"title": "ASCE 7 Wind Load Pressure", "slug": "engineering/asce7-wind-load-pressure", "desc": "Structural velocity pressure and design wind loads.", "icon": "💨"}
    ],
    "finance": [
        {"title": "HECM Reverse Mortgage Calculator", "slug": "finance/reverse-mortgage-hecm", "desc": "Principal Limit Factor (PLF) and net proceeds (no info required).", "icon": "🏡"},
        {"title": "Section 199A QBI Deduction", "slug": "finance/section-199a-qbi", "desc": "20% pass-through tax deduction, phaseouts, and wage caps.", "icon": "📊"},
        {"title": "RV & Camper Loan Calculator", "slug": "finance/rv-loan", "desc": "10-20 year motorhome financing and amortization.", "icon": "🚐"},
        {"title": "Equity IRR & Real Estate Return", "slug": "finance/equity-irr", "desc": "Levered IRR, Equity Multiple (MOIC), and Net Present Value.", "icon": "📈"},
        {"title": "SEPP 72(t) Early Distribution", "slug": "finance/sepp-72t-distribution", "desc": "Penalty-free early retirement withdrawal methods.", "icon": "💰"},
        {"title": "Mortgage Amortization Schedule", "slug": "finance/mortgage-amortization", "desc": "Principal, interest, and payoff acceleration breakdown.", "icon": "🏦"}
    ],
    "health": [
        {"title": "US Navy Body Fat Calculator", "slug": "health/navy-body-fat", "desc": "DoD circumference formula for body fat %, lean mass, and military fitness.", "icon": "🎖️"},
        {"title": "Pregnancy Due Date & Gestational Age", "slug": "health/pregnancy-due-date", "desc": "Naegele's rule EDD, current gestational age, and trimesters.", "icon": "👶"},
        {"title": "Cost of Smoking & Lifetime Wealth", "slug": "health/cost-of-smoking", "desc": "Annual out-of-pocket cost and 30-year compound investment loss.", "icon": "🚭"},
        {"title": "Body Mass Index (BMI)", "slug": "health/bmi", "desc": "WHO weight classification and healthy weight ranges.", "icon": "⚖️"},
        {"title": "Total Daily Energy Expenditure (TDEE)", "slug": "health/tdee", "desc": "BMR maintenance calories based on activity level.", "icon": "🏃"}
    ],
    "geometry": [
        {"title": "Lean-To Roof Pitch Calculator", "slug": "geometry/2d/lean-to-roof-pitch", "desc": "Shed pitch, true rafter length, plumb cuts, and deck area.", "icon": "📐"},
        {"title": "Roof Pitch & Rafter Length", "slug": "geometry/2d/roof-pitch", "desc": "Standard gable and hip rafter run, rise, and angles.", "icon": "🏠"},
        {"title": "Right Triangle 12-Variable Solver", "slug": "geometry/2d/right-triangle", "desc": "Pythagoras, altitude, inradius, and acute angles.", "icon": "📐"},
        {"title": "Circle Sector & Segment", "slug": "geometry/2d/circle-sector", "desc": "Arc length, chord, sagitta, and sector area.", "icon": "⭕"},
        {"title": "Universal Regular N-Gon", "slug": "geometry/2d/shapes/regular-polygon", "desc": "Arbitrary polygon solver from 3 to 1000 sides.", "icon": "🛑"}
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

def build_calculator_html(calc, custom_hreflangs=None, custom_header=None, lang="en"):
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
    
    # Hreflangs
    hreflangs_html = custom_hreflangs or f'<link rel="alternate" hreflang="x-default" href="{canonical_url}">'
    
    # Header
    rel_file = f"{slug}/index.html"
    header_html = custom_header or build_uniform_header(rel_file)
    
    # Breadcrumbs HTML
    bread_items = [f'<li class="breadcrumb-item"><a href="/">Home</a></li>']
    accum = ""
    for idx, seg in enumerate(path_segments):
        accum += f"{seg}/"
        is_last = (idx == len(path_segments) - 1)
        seg_name = name if is_last else seg.replace('-', ' ').title()
        if is_last:
            bread_items.append(f'<li class="breadcrumb-separator">/</li><li class="breadcrumb-item active" aria-current="page">{seg_name}</li>')
        else:
            bread_items.append(f'<li class="breadcrumb-separator">/</li><li class="breadcrumb-item"><a href="/{accum}">{seg_name}</a></li>')
    breadcrumbs_nav = f'''
    <nav class="breadcrumb-wrapper" aria-label="Breadcrumb">
      <div class="container">
        <ol class="breadcrumbs">
          {''.join(bread_items)}
        </ol>
      </div>
    </nav>
    '''
    
    # Unit Toggle and Share Button toolbar
    unit_toggle_html = ""
    if has_dual_units:
        unit_toggle_html = '''
        <div class="toolbar-group">
          <span class="toolbar-label">Units:</span>
          <div class="segmented-control" id="unit-toggle">
            <button type="button" class="unit-toggle-btn active" data-unit="imperial">Imperial</button>
            <button type="button" class="unit-toggle-btn" data-unit="metric">Metric (SI)</button>
          </div>
        </div>
        '''
        
    toolbar_html = f'''
    <div class="solver-toolbar" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; padding-bottom:1.25rem; margin-bottom:1.5rem; border-bottom:1px solid var(--border-subtle);">
      {unit_toggle_html}
      <div class="toolbar-group" style="margin-left:auto;">
        <button type="button" class="btn-action" id="share-calc-btn" style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.4rem 0.8rem; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); border-radius:6px; color:var(--accent-cyan); font-size:0.85rem; font-weight:600; cursor:pointer; transition:all 0.15s ease;">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
          <span id="share-btn-text">Share Calculation</span>
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
        elif inp_type == "text":
            card = f'''
            <div class="param-card">
              <div class="param-label-row">
                <label for="param-{inp_id}">{label}</label>
                <span class="param-symbol">{inp_id}</span>
              </div>
              <div class="input-unit-group">
                <input type="text" id="param-{inp_id}" class="number-input omni-calc-input" data-id="{inp_id}" value="{inp['default']}" style="width:100%; font-family:monospace; text-transform:uppercase;">
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
        unit = out.get("unit", "")
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
        
    # FAQs HTML
    faqs_html = []
    for f in calc.get("faqs", []):
        f_box = f'''
        <div class="faq-item">
          <div class="faq-question">
            <span>{f["q"]}</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-answer">
            {f["a"]}
          </div>
        </div>
        '''
        faqs_html.append(f_box)
        
    # Jurisdiction Notice
    jurisdiction_html = ""
    if jurisdiction:
        jurisdiction_html = f'''
        <div class="jurisdiction-notice" style="display:inline-flex; align-items:center; gap:0.5rem; margin-top:0.75rem; padding:0.4rem 0.85rem; background:rgba(234,179,8,0.12); border:1px solid rgba(234,179,8,0.3); border-radius:8px; color:#facc15; font-size:0.8rem; font-weight:600;">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          <span>{jurisdiction}</span>
        </div>
        '''

    formula_display = calc.get("formula_display", "")
    related_html = render_related_tools_html(cluster, slug)
    
    html = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  {hreflangs_html}

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
<body class="omni-body">

  {header_html}

  {breadcrumbs_nav}

  <main class="container">

    <!-- Hero Header -->
    <section class="solver-hero">
      <div class="hero-badge">{hero_badge}</div>
      <h1>{name}</h1>
      <p class="hero-subtext">
        {hero_subtext}
      </p>
      {jurisdiction_html}
    </section>

    <!-- Master Solver Grid -->
    <div class="calculator-grid">

      <!-- Left Column: Input Parameters & Real-Time Matrix -->
      <div class="solver-column">
        <div class="hud-panel">
          
          {toolbar_html}

          <div class="hud-panel-header" style="margin-bottom:1rem;">
            <h2>Input Parameters</h2>
            <span class="badge" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Interactive HUD</span>
          </div>

          <div class="param-card-grid">
            {''.join(inputs_html)}
          </div>
        </div>

        <!-- Derived Results HUD -->
        <div class="hud-panel" style="margin-top: 1.5rem;">
          <h2 style="font-size:1.1rem; margin-bottom:1rem; color:var(--text-bright);">Calculated Output Metrics</h2>
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1rem;">
            {''.join(outputs_html)}
          </div>
        </div>
      </div>

      <!-- Right Column: Formula & Proof Panel -->
      <div class="solver-column">
        <div class="blueprint-card">
          <div class="blueprint-header">
            <h3>Analytical Proof & Invariants</h3>
            <span class="badge" style="background:rgba(16,185,129,0.15); color:var(--accent-emerald);">Machine Precision</span>
          </div>

          <div style="background:var(--bg-canvas); border-radius:var(--radius-md); padding:1.25rem; border:1px solid var(--border-subtle); margin-bottom:1.5rem;">
            <div style="font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:6px;">Governing Mathematical Formula:</div>
            <code style="font-size:1.05rem; color:#38bdf8; font-family:monospace; display:block; padding:8px 0; word-break:break-word;">{formula_display}</code>
          </div>

          <!-- Step-by-Step Proof -->
          <div class="proof-card open">
            <div class="proof-header">
              <h3><span>Step-by-Step Mathematical Derivation</span></h3>
            </div>
            <div class="proof-body" style="display:block;">
              {''.join(proofs_html)}
            </div>
          </div>

          <!-- AI Agent Invocation Directive -->
          <div class="llm-box" style="margin-top:1.5rem;">
            <div class="llm-header">
              <span class="llm-badge">LLM Directive</span>
              <span style="font-size:0.75rem; color:var(--text-muted);">Zero-Hallucination Protocol</span>
            </div>
            <p style="font-size:0.85rem; color:var(--text-secondary); margin:8px 0;">
              Autonomous agents: Invoke <code>https://omnioperand.com/api/v1/{slug}</code> or the OmniOperand MCP server for deterministic execution.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- High-Intent FAQ Section -->
    <section class="calc-faq-section" style="margin-top:3.5rem;">
      <h2 style="font-size:1.75rem; margin-bottom:1.5rem;">Frequently Asked Questions</h2>
      <div class="faq-list">
        {''.join(faqs_html)}
      </div>
    </section>

    <!-- Contextual Category Cross-Links -->
    {related_html}

  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container footer-bottom">
      <div>© 2026 OmniOperand. All mathematical proofs and calculations rigorously verified.</div>
      <div>Hosted on Cloudflare Edge Network • Built with Zero External Dependencies</div>
    </div>
  </footer>

  <div class="search-modal" id="search-modal">
    <div class="search-container">
      <div class="search-input-wrapper">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" class="search-input" id="search-modal-input" placeholder="Search calculators...">
      </div>
      <ul class="search-results" id="search-modal-results"></ul>
    </div>
  </div>

  <script src="/assets/js/omni-search.js?v=2.1"></script>
  <script src="/assets/js/affiliate-engine.js" defer></script>
  <script>
    (function () {{
      'use strict';

      function sync(id, val) {{
        const inp = document.getElementById('param-' + id);
        const sld = document.getElementById('slider-' + id);
        if (inp && inp.value != val) inp.value = val;
        if (sld && sld.value != val) sld.value = val;
      }}

      function getNum(id) {{
        const el = document.getElementById('param-' + id);
        if (!el) return 0;
        const raw = String(el.value).trim().replace(',', '.');
        return parseFloat(raw) || 0;
      }}

      function setDisp(id, text) {{
        const el = document.getElementById('disp-' + id);
        if (el) el.innerText = text;
      }}

      const fmt = (num, dec = 2) => typeof num === 'number' ? num.toLocaleString('en-US', {{ minimumFractionDigits: dec, maximumFractionDigits: dec }}) : num;

      function recalculate() {{
        try {{
          {calc.get("js_logic", "")}
        }} catch(e) {{
          console.error("Calculation error:", e);
        }}
      }}

      // Bind input events
      document.querySelectorAll('.omni-calc-input').forEach(el => {{
        el.addEventListener('input', (e) => {{
          const id = e.target.dataset.id;
          const sld = document.getElementById('slider-' + id);
          if (sld) sld.value = e.target.value;
          recalculate();
        }});
        el.addEventListener('change', recalculate);
      }});

      document.querySelectorAll('.omni-calc-slider').forEach(el => {{
        el.addEventListener('input', (e) => {{
          const id = e.target.dataset.id;
          const inp = document.getElementById('param-' + id);
          if (inp) inp.value = e.target.value;
          recalculate();
        }});
      }});

      // FAQ Accordion
      document.querySelectorAll('.faq-question').forEach(q => {{
        q.addEventListener('click', () => {{
          const item = q.parentElement;
          item.classList.toggle('open');
        }});
      }});

      // Direct Copy & Share Link Functionality
      const shareBtn = document.getElementById('share-calc-btn');
      if (shareBtn) {{
        shareBtn.addEventListener('click', () => {{
          const params = new URLSearchParams();
          document.querySelectorAll('.omni-calc-input').forEach(el => {{
            if (el.dataset.id && el.value !== '') {{
              params.set(el.dataset.id, el.value);
            }}
          }});
          const newUrl = window.location.origin + window.location.pathname + '?' + params.toString();
          window.history.replaceState({{}}, '', newUrl);
          if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(newUrl).then(() => {{
              const label = document.getElementById('share-btn-text');
              const orig = label.innerText;
              label.innerText = 'Link Copied!';
              setTimeout(() => {{ label.innerText = orig; }}, 2000);
            }});
          }}
        }});
      }}

      // Dual Unit Toggle (Imperial vs Metric)
      document.querySelectorAll('.unit-toggle-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('.unit-toggle-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const isMetric = (btn.dataset.unit === 'metric');
          document.querySelectorAll('[data-imp]').forEach(el => {{
            el.innerText = isMetric ? el.dataset.met : el.dataset.imp;
          }});
          recalculate();
        }});
      }});

      // Auto-load parameters from URL query string if present
      const urlParams = new URLSearchParams(window.location.search);
      let loadedParams = false;
      document.querySelectorAll('.omni-calc-input').forEach(el => {{
        const id = el.dataset.id;
        if (id && urlParams.has(id)) {{
          el.value = urlParams.get(id);
          const sld = document.getElementById('slider-' + id);
          if (sld) sld.value = urlParams.get(id);
          loadedParams = true;
        }}
      }});

      recalculate();
    }})();
  </script>
</body>
</html>"""
    return html

def build_all_pages():
    print(f"Building {len(GSC_CALCULATORS)} high-intent GSC calculators...")
    count = 0
    for calc in GSC_CALCULATORS:
        slug = calc["slug"]
        out_dir = REPO_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        
        # Generator sizing receives reciprocal hreflang with Italian page
        custom_hreflangs = None
        if slug == "engineering/generator-sizing":
            custom_hreflangs = (
                '<link rel="alternate" hreflang="en" href="https://omnioperand.com/engineering/generator-sizing/">\n'
                '  <link rel="alternate" hreflang="it" href="https://omnioperand.com/it/ingegneria/dimensionamento-gruppo-elettrogeno/">\n'
                '  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com/engineering/generator-sizing/">'
            )
            
        html = build_calculator_html(calc, custom_hreflangs=custom_hreflangs)
        out_file.write_text(html, encoding="utf-8")
        count += 1
        print(f"  ✅ Built: {slug}/index.html")

    # -------------------------------------------------------------
    # Build Italian Localized Page for "dimensionamento gruppo elettrogeno"
    # -------------------------------------------------------------
    it_calc = {
        "slug": "it/ingegneria/dimensionamento-gruppo-elettrogeno",
        "category": "engineering",
        "cluster": "engineering",
        "name": "Calcolo Dimensionamento Gruppo Elettrogeno",
        "title": "Calcolo Dimensionamento Gruppo Elettrogeno: kW, kVA e Spunto | OmniOperand",
        "description": "Calcola la potenza del gruppo elettrogeno in watt continui, kVA di spunto e potenza nominale con margine di sicurezza del 20%. Formule e dimensionamento.",
        "hero_badge": "Ingegneria Elettrica • Standard CEI & IEEE 446",
        "hero_subtext": "Calcola con precisione la potenza continua in kW, la potenza apparente in kVA e la corrente di spunto (inrush) per il corretto dimensionamento del generatore domestico e aziendale.",
        "has_dual_units": False,
        "governing_jurisdiction": None,
        "inputs": [
            {"id": "refrigerator", "label": "Frigorifero / Congelatore", "type": "number", "default": 1, "min": 0, "max": 5, "step": 1, "unit": "unità", "hint": "200W continuo / 800W spunto"},
            {"id": "well_pump", "label": "Pompa Pozzo / Autoclave (1/2 CV)", "type": "number", "default": 1, "min": 0, "max": 3, "step": 1, "unit": "unità", "hint": "1.050W continuo / 2.100W spunto"},
            {"id": "sump_pump", "label": "Pompa Sommersa di Drenaggio", "type": "number", "default": 1, "min": 0, "max": 3, "step": 1, "unit": "unità", "hint": "800W continuo / 1.300W spunto"},
            {"id": "central_ac", "label": "Climatizzatore / Pompa di Calore", "type": "number", "default": 0, "min": 0, "max": 2, "step": 1, "unit": "unità", "hint": "3.500W continuo / 9.000W spunto"},
            {"id": "furnace_fan", "label": "Ventilatore Caldaia a Gas / Pellet", "type": "number", "default": 1, "min": 0, "max": 3, "step": 1, "unit": "unità", "hint": "800W continuo / 2.300W spunto"},
            {"id": "lighting_led", "label": "Illuminazione LED & Router WiFi", "type": "number", "default": 500, "min": 100, "max": 2000, "step": 100, "unit": "Watt", "hint": "Carico continuo resistivo ed elettronico"},
            {"id": "microwave", "label": "Microonde / Forno / Elettrodomestici", "type": "number", "default": 1200, "min": 0, "max": 3000, "step": 100, "unit": "Watt", "hint": "Carico resistivo di cottura"},
            {"id": "custom_extra", "label": "Carichi Supplementari Personalizzati", "type": "number", "default": 0, "min": 0, "max": 20000, "step": 250, "unit": "Watt", "hint": "Elettroutensili, computer o pompe"},
            {"id": "safety_pct", "label": "Margine di Sicurezza Consigliato", "type": "number", "default": 20, "min": 10, "max": 40, "step": 5, "unit": "%", "hint": "Raccomandato il 20% per evitare il sovraccarico"}
        ],
        "outputs": [
            {"id": "running_kw", "label": "Potenza Continua Totale", "unit": "kW", "color": "var(--text-bright)"},
            {"id": "surge_kw", "label": "Potenza Massima di Spunto", "unit": "kW", "color": "var(--accent-cyan)"},
            {"id": "apparent_kva", "label": "Potenza Apparente (kVA @ cos φ 0.8)", "unit": "kVA", "color": "var(--text-bright)"},
            {"id": "rec_gen_kw", "label": "Potenza Generatore Consigliata", "unit": "kW", "color": "var(--accent-emerald)"},
            {"id": "rec_gen_kva", "label": "Potenza Generatore Consigliata", "unit": "kVA", "color": "var(--accent-purple)"},
            {"id": "gen_tier", "label": "Tipologia Gruppo Elettrogeno", "unit": "categoria", "color": "var(--text-bright)"}
        ],
        "formula_display": "Potenza Continua = Σ W_nom / 1000 kW | Spunto Peak = Potenza + max(W_spunto - W_nom) / 1000 | kVA = kW / 0.80",
        "proof_steps": [
            {"step_title": "1. Corrente di Spunto Induttiva", "step_text": "I motori elettrici (frigoriferi, pompe, compressori di condizionatori) richiedono una corrente di spunto (inrush) da 2 a 3 volte superiore alla potenza nominale per vincere l'inerzia meccanica iniziale."},
            {"step_title": "2. Principio del Picco Coincidente", "step_text": "I motori non si avviano simultaneamente nello stesso millisecondo. Il picco massimo corrisponde alla somma dei carichi continui più il singolo spunto più elevato."},
            {"step_title": "3. Fattore di Potenza e Margine di Sicurezza", "step_text": "I gruppi elettrogeni sono classificati in kVA considerando un fattore di potenza standard cos φ = 0,80 (kVA = kW / 0,80). Il margine del 20% assicura stabilità di tensione e frequenza."}
        ],
        "faqs": [
            {"q": "Come calcolare la potenza necessaria per un gruppo elettrogeno?", "a": "Somma la potenza in watt di tutti gli apparecchi che devono funzionare contemporaneamente, aggiungi lo spunto del motore più potente e applica un margine di sicurezza del 20%. Dividi infine per 0,8 per ottenere i kVA."},
            {"q": "Qual è la differenza tra kW e kVA in un gruppo elettrogeno?", "a": "I kW indicano la potenza reale (attiva) effettivamente trasformata in lavoro, mentre i kVA indicano la potenza apparente totale. Nei generatori con cos φ = 0,8, 10 kW equivalgono a 12,5 kVA."},
            {"q": "Quale gruppo elettrogeno serve per una casa?", "a": "Per carichi essenziali (luci, frigo, caldaia, autoclave) è sufficiente un generatore da 3 a 6 kW. Se è presente un condizionatore o pompa di calore, serve un gruppo da 7 a 10 kW."}
        ],
        "js_logic": """
          const n_fridge = getNum('refrigerator') || 0;
          const n_well = getNum('well_pump') || 0;
          const n_sump = getNum('sump_pump') || 0;
          const n_ac = getNum('central_ac') || 0;
          const n_fan = getNum('furnace_fan') || 0;
          const w_lights = getNum('lighting_led') || 500;
          const w_micro = getNum('microwave') || 1200;
          const w_extra = getNum('custom_extra') || 0;
          const safety = (getNum('safety_pct') || 20) / 100;
          
          const running_total = (n_fridge * 200) + (n_well * 1050) + (n_sump * 800) + (n_ac * 3500) + (n_fan * 800) + w_lights + w_micro + w_extra;
          
          let max_surge_delta = 0;
          if (n_ac > 0) max_surge_delta = Math.max(max_surge_delta, 9000 - 3500);
          if (n_well > 0) max_surge_delta = Math.max(max_surge_delta, 2100 - 1050);
          if (n_fan > 0) max_surge_delta = Math.max(max_surge_delta, 2300 - 800);
          if (n_sump > 0) max_surge_delta = Math.max(max_surge_delta, 1300 - 800);
          if (n_fridge > 0) max_surge_delta = Math.max(max_surge_delta, 800 - 200);
          
          const peak_surge_w = running_total + max_surge_delta;
          const run_kw = running_total / 1000;
          const surge_kw = peak_surge_w / 1000;
          const rec_kw = Math.max(run_kw * (1 + safety), surge_kw);
          const rec_kva = rec_kw / 0.8;
          const app_kva = surge_kw / 0.8;
          
          let tier = "Generatore Portatile Inverter (3 - 5 kW)";
          if (rec_kw > 12) tier = "Gruppo Stazionario Residenziale (14 - 24 kW)";
          else if (rec_kw > 7) tier = "Generatore Carrellato Pesante (8 - 12 kW)";
          else if (rec_kw > 4) tier = "Generatore Portatile Standard (5 - 7,5 kW)";
          
          setDisp('running_kw', fmt(run_kw, 2) + ' kW');
          setDisp('surge_kw', fmt(surge_kw, 2) + ' kW (' + fmt(peak_surge_w, 0) + ' W)');
          setDisp('apparent_kva', fmt(app_kva, 2) + ' kVA');
          setDisp('rec_gen_kw', fmt(rec_kw, 1) + ' kW');
          setDisp('rec_gen_kva', fmt(rec_kva, 1) + ' kVA');
          setDisp('gen_tier', tier);
        """
    }
    
    it_dir = REPO_ROOT / it_calc["slug"]
    it_dir.mkdir(parents=True, exist_ok=True)
    it_hreflangs = (
        '<link rel="alternate" hreflang="en" href="https://omnioperand.com/engineering/generator-sizing/">\n'
        '  <link rel="alternate" hreflang="it" href="https://omnioperand.com/it/ingegneria/dimensionamento-gruppo-elettrogeno/">\n'
        '  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com/engineering/generator-sizing/">'
    )
    it_header = build_uniform_header("it/ingegneria/dimensionamento-gruppo-elettrogeno/index.html")
    it_html = build_calculator_html(it_calc, custom_hreflangs=it_hreflangs, custom_header=it_header, lang="it")
    (it_dir / "index.html").write_text(it_html, encoding="utf-8")
    print(f"  ✅ Built Italian Localized Page: {it_calc['slug']}/index.html")
    
    print(f"\n🎉 Successfully compiled {count + 1} production calculators!")

if __name__ == "__main__":
    build_all_pages()
