#!/usr/bin/env python3
"""
scripts/optimize_existing_ranking_pages.py
Applies CTR title/meta optimization, Schema.org Offer price 0,
contextual related tools clustering, and copy-share URL state features
across existing top-ranking pages.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CLUSTERS = {
    "biotech": [
        {"title": "Centrifuge RCF to RPM Converter", "slug": "biotech/centrifuge-rcf-g-force", "desc": "Convert RPM to RCF g-force with rotor radius.", "icon": "🧪"},
        {"title": "qPCR Primer Tm Calculator", "slug": "biotech/qpcr-primer-tm", "desc": "Nearest-neighbor melting temperature and annealing Ta.", "icon": "🧬"},
        {"title": "PCR Primer Tm & GC Formula", "slug": "biotech/pcr-primer-tm", "desc": "Thermodynamic salt-corrected primer melting temp.", "icon": "🔬"},
        {"title": "Cockcroft-Gault CrCl Calculator", "slug": "biotech/cockcroft-gault-crcl", "desc": "Creatinine clearance and renal dosing adjustment.", "icon": "💊"},
        {"title": "Cell Culture Doubling Time", "slug": "biotech/cell-culture-doubling-time", "desc": "Cell proliferation kinetics and growth rate.", "icon": "🧫"}
    ],
    "health": [
        {"title": "US Navy Body Fat Calculator", "slug": "health/navy-body-fat", "desc": "DoD circumference formula for body fat %, lean mass, and military fitness.", "icon": "🎖️"},
        {"title": "Pregnancy Due Date & Gestational Age", "slug": "health/pregnancy-due-date", "desc": "Naegele's rule EDD, current gestational age, and trimesters.", "icon": "👶"},
        {"title": "Cost of Smoking & Lifetime Wealth", "slug": "health/cost-of-smoking", "desc": "Annual out-of-pocket cost and 30-year compound investment loss.", "icon": "🚭"},
        {"title": "Body Mass Index (BMI)", "slug": "health/bmi", "desc": "WHO weight classification and healthy weight ranges.", "icon": "⚖️"},
        {"title": "Total Daily Energy Expenditure (TDEE)", "slug": "health/tdee", "desc": "BMR maintenance calories based on activity level.", "icon": "🏃"}
    ],
    "finance": [
        {"title": "HECM Reverse Mortgage Calculator", "slug": "finance/reverse-mortgage-hecm", "desc": "Principal Limit Factor (PLF) and net proceeds (no info required).", "icon": "🏡"},
        {"title": "Section 199A QBI Deduction", "slug": "finance/section-199a-qbi", "desc": "20% pass-through tax deduction, phaseouts, and wage caps.", "icon": "📊"},
        {"title": "RV & Camper Loan Calculator", "slug": "finance/rv-loan", "desc": "10-20 year motorhome financing and amortization.", "icon": "🚐"},
        {"title": "Equity IRR & Real Estate Return", "slug": "finance/equity-irr", "desc": "Levered IRR, Equity Multiple (MOIC), and Net Present Value.", "icon": "📈"},
        {"title": "SEPP 72(t) Early Distribution", "slug": "finance/sepp-72t-distribution", "desc": "Penalty-free early retirement withdrawal methods.", "icon": "💰"},
        {"title": "Mortgage Amortization Schedule", "slug": "finance/mortgage-amortization", "desc": "Principal, interest, and payoff acceleration breakdown.", "icon": "🏦"}
    ]
}

def render_cluster(cluster_key, current_slug):
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

PAGES_TO_OPTIMIZE = [
    {
        "file": "health/pregnancy-due-date/index.html",
        "slug": "health/pregnancy-due-date",
        "cluster": "health",
        "title": "Pregnancy Due Date Calculator: Accurate Gestational Age & EDD | OmniOperand",
        "desc": "Calculate your exact estimated delivery date (EDD), gestational age in weeks/days, and trimester milestones using Naegele's rule. Free & instant."
    },
    {
        "file": "biotech/centrifuge-rcf-g-force/index.html",
        "slug": "biotech/centrifuge-rcf-g-force",
        "cluster": "biotech",
        "title": "Centrifuge RCF to RPM Converter: Free & Instant Formula | OmniOperand",
        "desc": "Convert RPM to RCF (relative centrifugal force / g-force) and vice versa with rotor radius. Fast, free formula compliant with laboratory standards."
    },
    {
        "file": "finance/sepp-72t-distribution/index.html",
        "slug": "finance/sepp-72t-distribution",
        "cluster": "finance",
        "title": "SEPP 72(t) Calculator: Early Retirement Penalty-Free Withdrawals | OmniOperand",
        "desc": "Calculate penalty-free early retirement distributions using IRS 72(t) amortization, annuitization, and RMD methods. Avoid the 10% early withdrawal tax."
    },
    {
        "file": "biotech/pcr-primer-tm/index.html",
        "slug": "biotech/pcr-primer-tm",
        "cluster": "biotech",
        "title": "PCR Primer Tm Calculator: Thermodynamic Melting Formula | OmniOperand",
        "desc": "Calculate PCR primer melting temperature (Tm) with nearest-neighbor thermodynamics, salt correction, and GC content. Free, instant laboratory tool."
    },
    {
        "file": "health/body-fat/index.html",
        "slug": "health/body-fat",
        "cluster": "health",
        "title": "US Navy Body Fat Calculator: Circumference Formula & Tiers | OmniOperand",
        "desc": "Calculate body fat percentage and lean mass using the official US Navy circumference formula (DoD standard). Free, instant calculation."
    },
    {
        "file": "health/smoking-cost/index.html",
        "slug": "health/smoking-cost",
        "cluster": "health",
        "title": "Smoking Cost Calculator: Lifetime Outlay & Wealth Lost | OmniOperand",
        "desc": "Calculate annual smoking costs and lifetime compound investment wealth lost. Discover the 10, 20, and 30-year opportunity cost of smoking."
    }
]

def optimize_pages():
    print("Optimizing existing top-ranking pages for CTR & Contextual Linking...")
    for p in PAGES_TO_OPTIMIZE:
        fpath = REPO_ROOT / p["file"]
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        
        # 1. Update <title>
        content = re.sub(r'<title>[^<]+</title>', f'<title>{p["title"]}</title>', content, count=1)
        
        # 2. Update <meta name="description">
        content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{p["desc"]}">', content, count=1)
        
        # 3. Update og:title and og:description
        content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{p["title"]}">', content, count=1)
        content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{p["desc"]}">', content, count=1)
        
        # 4. Inject Offer into WebApplication schema if missing
        if '"offers"' not in content and '"@type": "WebApplication"' in content:
            offer_snippet = ',\n        "offers": {\n          "@type": "Offer",\n          "price": "0",\n          "priceCurrency": "USD"\n        }'
            content = re.sub(r'("@type":\s*"WebApplication"[^}]+)', r'\1' + offer_snippet, content, count=1)

        # 5. Inject Contextual Related Tools before </main> if missing
        if 'class="related-tools-section"' not in content and '</main>' in content:
            cluster_html = render_cluster(p["cluster"], p["slug"])
            content = content.replace('</main>', cluster_html + '\n  </main>', 1)
            
        fpath.write_text(content, encoding="utf-8")
        print(f"  ✅ Optimized: {p['file']}")

if __name__ == "__main__":
    optimize_pages()
