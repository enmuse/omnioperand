#!/usr/bin/env python3
"""
scripts/build_batch2_calculators.py
Production-grade builder for 22 GSC High-Intent Missing Calculators:
1. Slant Height (Cone, Pyramid, Frustum)
2. LCL Freight & CBM (Ocean/Air Dimensional Weight & Volume)
3. Tubular Reabsorption of Phosphate (%TRP) & TmP/GFR
4. Brick Soling & Flat Masonry Area
5. Ultrasonic Angle Beam Path & Sound Path Distance
6. Drill Pipe & Casing Well Displacement
7. Aerodynamic Drag & Downforce Force
8. Commercial Battery Peak Shaving & Demand Charge
9. Flowable Fill (CLSM) Volume & Mix
10. Retaining Wall Overturning & Sliding Safety Factor
11. Column Slenderness Ratio & Critical Buckling Load
12. Unistrut Channel Beam Load & Deflection
13. Relative Response Factor (RRF) HPLC
14. Micromolar to ng/mL Mass-Molar Concentration Converter
15. Concrete Haunch & Chamfer Reinforcement
16. Analytical Evaluation Threshold (AET)
17. Relative Potency Bioassay
18. HPLC Column Theoretical Plates & Resolution
19. Syringe Pump & Microfluidic Flow Rate
20. ASC 842 / IFRS 16 Incremental Borrowing Rate (IBR)
21. Circumferential & Surface Cutting Speed
22. Hydraulic Cylinder Force & Fluid Flow

Features:
- Exact Unicode mathematical typography (zero raw LaTeX backslash commands)
- Master Bidirectional Solver Matrix with parameter cards, sliders, and output metrics
- Embed Calculator Modal trigger in toolbar
- Dual AI Integration Box:
  * Copy Prompt for AI with live parameter insertion & verification directives
  * Copy API Endpoint with direct URL & llms.txt reference
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
from data_batch2_gsc import BATCH2_CALCULATORS
from data_batch2_part2_gsc import BATCH2_PART2_CALCULATORS

ALL_NEW_CALCULATORS = BATCH2_CALCULATORS + BATCH2_PART2_CALCULATORS

CLUSTERS = {
    "biotech": [
        {"title": "Tubular Reabsorption of Phosphate (%TRP)", "slug": "biotech/tubular-reabsorption-phosphate-trp", "desc": "%TRP, tubular maximum TmP/GFR, and renal threshold.", "icon": "🧪"},
        {"title": "Relative Response Factor (RRF) HPLC", "slug": "biotech/relative-response-factor-rrf", "desc": "Chromatographic detector response and impurity %.", "icon": "🔬"},
        {"title": "HPLC Column Theoretical Plates & Resolution", "slug": "biotech/chromatography-resolution", "desc": "USP plate count N and peak resolution Rs.", "icon": "📊"},
        {"title": "AET Extractables & Leachables Threshold", "slug": "biotech/analytical-evaluation-threshold-aet", "desc": "Safety Concern Threshold SCT to analytical limit.", "icon": "🛡️"},
        {"title": "Relative Potency Bioassay Calculator", "slug": "biotech/relative-potency-bioassay", "desc": "Parallel line bioassay potency and 95% CI.", "icon": "🧫"},
        {"title": "Syringe Pump & Microfluidic Flow Rate", "slug": "biotech/syringe-pump-injection-rate", "desc": "Inner diameter, linear pusher speed, and volumetric rate.", "icon": "💉"},
        {"title": "Centrifuge RCF to RPM Converter", "slug": "biotech/centrifuge-rcf-g-force", "desc": "Convert RPM to RCF g-force with rotor radius.", "icon": "🧪"},
        {"title": "qPCR Primer Tm Calculator", "slug": "biotech/qpcr-primer-tm", "desc": "Nearest-neighbor melting temperature and annealing Ta.", "icon": "🧬"}
    ],
    "construction": [
        {"title": "Brick Soling & Flat Masonry Area", "slug": "construction/brick-soling", "desc": "Flat and herringbone brick soling with joint mortar.", "icon": "🧱"},
        {"title": "Flowable Fill (CLSM) Volume & Mix", "slug": "construction/flowable-fill-clsm", "desc": "Excavation trench backfill cubic yards and cement bags.", "icon": "🏗️"},
        {"title": "Unistrut Channel Beam Load & Deflection", "slug": "construction/unistrut-load-capacity", "desc": "P1000/P5000 uniform and point load bending capacity.", "icon": "⚙️"},
        {"title": "Concrete Volume Calculator", "slug": "construction/concrete-volume", "desc": "Slab, footing & column volume with 10% waste buffer.", "icon": "🧱"},
        {"title": "Rebar Grid & Spacing Calculator", "slug": "construction/rebar-calculator", "desc": "Linear feet, grid weight, and tie wire for slabs.", "icon": "🏗️"},
        {"title": "Drywall & Mud Estimator", "slug": "construction/drywall", "desc": "Sheet count, joint compound buckets, and screws.", "icon": "📐"}
    ],
    "engineering": [
        {"title": "Ultrasonic Angle Beam Path & Sound Path", "slug": "engineering/ultrasonic-beam-path", "desc": "Wedge refraction angle, surface distance, and flaw depth.", "icon": "📡"},
        {"title": "Drill Pipe & Casing Displacement", "slug": "engineering/drill-pipe-displacement", "desc": "API steel displacement, internal capacity, and barrel volume.", "icon": "🛢️"},
        {"title": "Retaining Wall Overturning & Sliding Safety", "slug": "engineering/retaining-wall-overturning-safety", "desc": "Rankine active earth pressure, FS overturning, and sliding.", "icon": "🧱"},
        {"title": "Column Slenderness & Critical Buckling", "slug": "engineering/column-slenderness-buckling", "desc": "Euler critical buckling load, effective length K, and radius of gyration.", "icon": "🏛️"},
        {"title": "Concrete Haunch & Chamfer Reinforcement", "slug": "engineering/concrete-haunch-reinforcement", "desc": "Shear friction stirrups and 45° fillet reinforcement.", "icon": "📐"},
        {"title": "Hydraulic Cylinder Force & Fluid Flow", "slug": "engineering/hydraulic-cylinder-flow", "desc": "Push/pull force, rod velocity, and pump flow GPM.", "icon": "💧"},
        {"title": "Generator Sizing Calculator", "slug": "engineering/generator-sizing", "desc": "Running watts, peak surge kVA, and generator rating.", "icon": "⚡"},
        {"title": "Wire Gauge & Voltage Drop (NEC)", "slug": "engineering/wire-gauge-voltage-drop", "desc": "NEC 3% limit, conductor size AWG/mm², and drop %.", "icon": "🔌"}
    ],
    "physics": [
        {"title": "Aerodynamic Drag & Downforce Force", "slug": "physics/aerodynamic-drag-force", "desc": "Drag force, aero downforce, and aerodynamic power loss.", "icon": "🏎️"},
        {"title": "Circumferential & Surface Cutting Speed", "slug": "physics/circumferential-surface-speed", "desc": "Machining SFM, peripheral velocity, and spindle RPM.", "icon": "⚙️"},
        {"title": "Kinetic Energy & Momentum", "slug": "physics/kinetic-energy", "desc": "Translational kinetic energy and linear momentum.", "icon": "⚛️"}
    ],
    "energy": [
        {"title": "Battery Peak Shaving & Demand Charge", "slug": "energy/battery-peak-shaving", "desc": "Commercial kW demand threshold, kWh battery capacity, and ROI.", "icon": "🔋"},
        {"title": "Battery Backup Storage", "slug": "engineering/battery-backup-storage", "desc": "Household kWh autonomy, DoD, and battery bank Ah.", "icon": "⚡"},
        {"title": "Solar Photovoltaic Panel Array", "slug": "energy/solar-panel-payback", "desc": "Solar irradiance yield, panel count, and annual kWh generation.", "icon": "☀️"}
    ],
    "finance": [
        {"title": "Incremental Borrowing Rate (IBR) Lease", "slug": "finance/incremental-borrowing-rate-lease", "desc": "ASC 842 / IFRS 16 lease liability discount rate.", "icon": "📈"},
        {"title": "HECM Reverse Mortgage Calculator", "slug": "finance/reverse-mortgage-hecm", "desc": "Principal Limit Factor (PLF) and net proceeds.", "icon": "🏡"},
        {"title": "Section 199A QBI Deduction", "slug": "finance/section-199a-qbi", "desc": "20% pass-through tax deduction, phaseouts, and wage caps.", "icon": "📊"},
        {"title": "Equity IRR & Real Estate Return", "slug": "finance/equity-irr", "desc": "Levered IRR, Equity Multiple (MOIC), and Net Present Value.", "icon": "💰"}
    ],
    "logistics": [
        {"title": "LCL Freight & CBM Calculator", "slug": "logistics/lcl-freight-cbm", "desc": "Cubic meters CBM, dimensional chargeable weight, and freight cost.", "icon": "🚢"},
        {"title": "Pallet Loading & Cube Optimization", "slug": "logistics/pallet-load", "desc": "Container cube utilization and carton stacking.", "icon": "📦"},
        {"title": "Air Freight Volumetric Weight", "slug": "logistics/air-freight-volumetric", "desc": "IATA 1:6000 ratio and dimensional weight.", "icon": "✈️"}
    ],
    "geometry": [
        {"title": "Slant Height Calculator", "slug": "geometry/slant-height", "desc": "Cone, square pyramid, and frustum slant height.", "icon": "📐"},
        {"title": "Lean-To Roof Pitch Calculator", "slug": "geometry/2d/lean-to-roof-pitch", "desc": "Shed pitch, true rafter length, plumb cuts, and deck area.", "icon": "🏠"},
        {"title": "Universal Regular N-Gon", "slug": "geometry/2d/shapes/regular-polygon", "desc": "Arbitrary polygon solver from 3 to 1000 sides.", "icon": "🛑"},
        {"title": "Right Triangle 12-Variable Solver", "slug": "geometry/2d/right-triangle", "desc": "Pythagoras, altitude, inradius, and acute angles.", "icon": "📐"}
    ]
}

def render_related_tools_html(cluster_key: str, current_slug: str) -> str:
    tools = CLUSTERS.get(cluster_key, [])
    filtered = [t for t in tools if t["slug"] != current_slug][:4]
    if not filtered:
        # Fallback to engineering
        filtered = [t for t in CLUSTERS.get("engineering", []) if t["slug"] != current_slug][:4]
    
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
    api_url = f"https://omnioperand.com/api/v1/{slug}"
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
    hreflangs_html = f'<link rel="alternate" hreflang="x-default" href="{canonical_url}">\n  <link rel="alternate" hreflang="en" href="{canonical_url}">'
    
    # Header
    rel_file = f"{slug}/index.html"
    header_html = build_uniform_header(rel_file)
    
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
<html lang="en" data-theme="dark">
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
      <div class="calculator-actions-toolbar">
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      </div>
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

          <!-- Dual AI Agent & Prompt Integration Box -->
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
          </section>
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

  <div class="search-modal" id="search-modal">
    <div class="search-container">
      <div class="search-input-wrapper">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" class="search-input" id="search-modal-input" placeholder="Search calculators...">
      </div>
      <ul class="search-results" id="search-modal-results"></ul>
    </div>
  </div>

  <script src="/assets/js/omni-search.js?v=2.2"></script>
  <script src="/assets/js/embed-modal.js?v=2.2" defer></script>
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

      function updateLLMPromptText() {{
        const promptEl = document.getElementById('llm-prompt-display');
        if (!promptEl) return;
        const LF = String.fromCharCode(10);
        const inputs = Array.from(document.querySelectorAll('.omni-calc-input')).map(el => {{
          const id = el.getAttribute('data-id');
          const val = el.value;
          const label = el.closest('.param-card')?.querySelector('label')?.textContent || id;
          return '- ' + label + ' (' + id + '): ' + val;
        }}).join(LF);
        
        const outputs = Array.from(document.querySelectorAll('.metric-card')).map(el => {{
          const label = el.querySelector('.metric-label')?.textContent || '';
          const val = el.querySelector('.metric-value')?.textContent || '';
          return '- ' + label + ': ' + val;
        }}).join(LF);

        const promptText = [
          '### SYSTEM DIRECTIVE: {name} Verification',
          'You are an expert computational engine and mathematical validator.',
          'Refer to the following verified parameters from OmniOperand ({canonical_url}):',
          '',
          'INPUT PARAMETERS:',
          inputs,
          '',
          'DERIVED METRICS:',
          outputs,
          '',
          'GOVERNING FORMULA:',
          '{formula_display}',
          '',
          'MATHEMATICAL VERIFICATION DIRECTIVES:',
          '1. Ensure all closed-form calculations match machine precision.',
          '2. Eliminate rounding drift in intermediate variables.',
          '3. Autonomous agent endpoint: {api_url}',
          '4. Return step-by-step reasoning verified against standard proofs.'
        ].join(LF);
        promptEl.textContent = promptText;
      }}

      function recalculate() {{
        try {{
          {calc.get("js_logic", "")}
          updateLLMPromptText();
        }} catch(e) {{
          console.error("Calculation error:", e);
        }}
      }}

      // Bind input events
      document.querySelectorAll('.omni-calc-input').forEach(el => {{
        el.addEventListener('input', (e) => {{
          const id = e.target.getAttribute('data-id');
          sync(id, e.target.value);
          recalculate();
        }});
        el.addEventListener('change', (e) => {{
          const id = e.target.getAttribute('data-id');
          sync(id, e.target.value);
          recalculate();
        }});
      }});

      document.querySelectorAll('.omni-calc-slider').forEach(el => {{
        el.addEventListener('input', (e) => {{
          const id = e.target.getAttribute('data-id');
          sync(id, e.target.value);
          recalculate();
        }});
      }});

      // Copy buttons
      const copyPromptBtn = document.getElementById('copy-llm-prompt-btn');
      if (copyPromptBtn) {{
        copyPromptBtn.addEventListener('click', () => {{
          const promptEl = document.getElementById('llm-prompt-display');
          const textEl = document.getElementById('copy-prompt-text');
          if (promptEl) {{
            navigator.clipboard.writeText(promptEl.textContent).then(() => {{
              if (textEl) textEl.textContent = 'Copied Prompt! ✓';
              setTimeout(() => {{ if (textEl) textEl.textContent = 'Copy Prompt for AI'; }}, 2000);
            }}).catch(() => {{
              const ta = document.createElement('textarea');
              ta.value = promptEl.textContent;
              document.body.appendChild(ta);
              ta.select();
              document.execCommand('copy');
              document.body.removeChild(ta);
              if (textEl) textEl.textContent = 'Copied Prompt! ✓';
              setTimeout(() => {{ if (textEl) textEl.textContent = 'Copy Prompt for AI'; }}, 2000);
            }});
          }}
        }});
      }}

      const copyApiBtn = document.getElementById('copy-api-btn');
      if (copyApiBtn) {{
        copyApiBtn.addEventListener('click', () => {{
          const textEl = document.getElementById('copy-api-text');
          navigator.clipboard.writeText('{api_url}').then(() => {{
            if (textEl) textEl.textContent = 'Copied Endpoint! ✓';
            setTimeout(() => {{ if (textEl) textEl.textContent = 'Copy API Endpoint'; }}, 2000);
          }}).catch(() => {{
            if (textEl) textEl.textContent = 'Copied Endpoint! ✓';
            setTimeout(() => {{ if (textEl) textEl.textContent = 'Copy API Endpoint'; }}, 2000);
          }});
        }});
      }}

      // Share URL state
      const shareBtn = document.getElementById('share-calc-btn');
      if (shareBtn) {{
        shareBtn.addEventListener('click', () => {{
          const params = new URLSearchParams();
          document.querySelectorAll('.omni-calc-input').forEach(el => {{
            params.set(el.getAttribute('data-id'), el.value);
          }});
          const shareUrl = window.location.origin + window.location.pathname + '?' + params.toString();
          navigator.clipboard.writeText(shareUrl).then(() => {{
            const t = document.getElementById('share-btn-text');
            if (t) t.textContent = 'Copied Link! ✓';
            setTimeout(() => {{ if (t) t.textContent = 'Share Calculation'; }}, 2000);
          }});
        }});
      }}

      // URL parameters hydration
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.forEach((val, key) => {{
        const inp = document.getElementById('param-' + key);
        if (inp) {{
          inp.value = val;
          sync(key, val);
        }}
      }});

      recalculate();
    }})();
  </script>
</body>
</html>
"""
    return html

def build_all():
    print(f"Generating {len(ALL_NEW_CALCULATORS)} high-intent GSC calculators...")
    built = 0
    for calc in ALL_NEW_CALCULATORS:
        slug = calc["slug"]
        out_dir = REPO_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        
        html = build_calculator_html(calc)
        out_file.write_text(html, encoding="utf-8")
        built += 1
        print(f"  [{built:2d}/{len(ALL_NEW_CALCULATORS)}] Generated: {slug}/index.html")

    print(f"✅ Successfully built all {built} calculators!")

if __name__ == "__main__":
    build_all()
