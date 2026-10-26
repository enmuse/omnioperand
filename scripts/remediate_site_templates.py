#!/usr/bin/env python3
"""
scripts/remediate_site_templates.py
Remediates all template, feature, and functionality gaps identified in the site-wide audit.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SEARCH_MODAL_HTML = '''  <div class="search-modal" id="search-modal">
    <div class="search-container">
      <div class="search-input-wrapper">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" class="search-input" id="search-modal-input" placeholder="Search calculators...">
      </div>
      <ul class="search-results" id="search-modal-results"></ul>
    </div>
  </div>'''

TOOLBAR_HTML = '''      <div class="calculator-actions-toolbar">
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      </div>'''

STATUTORY_PAGES = {
    "engineering/hvac-manual-j/index.html": {
        "slug": "engineering/hvac-manual-j",
        "title": "ACCA Manual J Heat Pump & Cold-Climate Sizing",
        "api_endpoint": "https://omnioperand.com/api/hvac-manual-j",
        "api_method": "POST",
        "faq": [
            ("What is ACCA Manual J?", "ACCA Manual J is the American National Standards Institute (ANSI) recognized standard for calculating heating and cooling equipment loads in residential structures. It computes building heat loss and heat gain using architectural dimensions, insulation U-values, window SHGC, and regional 99% climatic design temperatures."),
            ("Why is low-ambient heat pump derating critical?", "Inverter-driven cold-climate heat pumps lose thermodynamic heating capacity as outdoor ambient temperatures fall below freezing. Derating models the compressor capacity retention (typically 70–85% at 0°F to 14°F) to accurately size auxiliary electric heat strips and prevent winter freeze-outs."),
            ("What is the thermal balance point?", "The thermal balance point is the outdoor temperature at which building envelope heat loss precisely matches the maximum heating capacity of the heat pump compressor without supplementary resistance heat.")
        ]
    },
    "engineering/nec-load/index.html": {
        "slug": "engineering/nec-load",
        "title": "NEC 220 Residential Electrical Service Load",
        "api_endpoint": "https://omnioperand.com/api/nec-load",
        "api_method": "POST",
        "faq": [
            ("What is the NEC Article 220.82 Optional Method?", "NEC 220.82 provides a simplified demand-factor calculation for single-family residential dwellings with a minimum 100A service. It combines general lighting at 3 VA/sq ft with small appliance circuits, takes the first 10,000 VA at 100%, and derates the remainder at 40%."),
            ("How are EV chargers calculated under the National Electrical Code?", "Under NEC 625.41, electric vehicle supply equipment (EVSE) is classified as a continuous duty load, requiring conductors and overcurrent protection to be sized at 125% of the nameplate rating."),
            ("What copper and aluminum wire sizes correspond to 200A service?", "Per NEC Table 310.16 and 310.12, a standard single-phase 200-amp residential service requires 2/0 AWG Copper (Cu) or 4/0 AWG Aluminum (Al) conductors rated at 75°C.")
        ]
    },
    "civil/insurance-restoration/index.html": {
        "slug": "civil/insurance-restoration",
        "title": "Insurance Disaster Restoration & Supplement Auditor",
        "api_endpoint": "https://omnioperand.com/api/restoration-scope",
        "api_method": "POST",
        "faq": [
            ("What is statutory 10/10 Overhead & Profit (O&P)?", "Standard insurance restoration contracts entitle general contractors managing three or more distinct construction trades to 10% general contractor overhead and 10% net profit on gross mitigation and rebuild scopes."),
            ("What distinguishes IICRC Category 1, 2, and 3 water losses?", "Category 1 is clean sanitary water (broken supply lines). Category 2 is grey water with chemical or physical contaminants (dishwasher/washing machine discharge). Category 3 is black water with pathogenic contaminants (sewage backups, river flooding, or standing Category 2 water after 48 hours)."),
            ("How does Xactimate pricing affect restoration claim supplements?", "Xactimate publishes monthly localized labor, equipment, and material price lists for thousands of geographic zones across North America. Scope supplements document missed line items (such as negative air HEPA filtration and content manipulation) to establish fair market settlement.")
        ]
    },
    "civil/steep-slope/index.html": {
        "slug": "civil/steep-slope",
        "title": "Mountain Steep-Slope Feasibility & Permitting Engine",
        "api_endpoint": "https://omnioperand.com/api/feasibility",
        "api_method": "POST",
        "faq": [
            ("What constitutes a steep slope under mountain ordinances?", "Most county Unified Development Ordinances (such as Buncombe, Henderson, and Haywood County, NC) define steep slopes as natural ground slopes exceeding 15% to 25%, with severe slope protections applying above 30% or 35%."),
            ("When is a licensed geotechnical engineer required?", "Building sites with average slopes above 25% or containing mapped colluvial slide hazards require stamped site-specific geotechnical investigations and engineered retaining wall plans before zoning permits are granted."),
            ("How does cut-and-fill mass balance reduce site development costs?", "Balancing soil excavation (cut) with structural embankment placement (fill) minimizes expensive off-site trucking fees, export disposal permits, and imported structural backfill.")
        ]
    },
    "health/telehealth-prescribing/index.html": {
        "slug": "health/telehealth-prescribing",
        "title": "Telehealth Psychiatric Triage & Medication Router",
        "api_endpoint": "https://omnioperand.com/api/clinical-triage",
        "api_method": "POST",
        "faq": [
            ("What is the Ryan Haight Online Pharmacy Consumer Protection Act?", "The Ryan Haight Act (21 U.S.C. § 829(e)) requires healthcare providers to conduct at least one in-person medical evaluation prior to prescribing Schedule II-V controlled substances, subject to temporary DEA telemedicine waivers."),
            ("How are PHQ-9 and GAD-7 scores interpreted?", "PHQ-9 measures depression severity: 0–4 minimal, 5–9 mild, 10–14 moderate, 15–19 moderately severe, and 20–27 severe. GAD-7 measures anxiety: 0–4 minimal, 5–9 mild, 10–14 moderate, and 15–21 severe."),
            ("When is urgent crisis protocol mandated?", "Any positive affirmative response on the Columbia-Suicide Severity Rating Scale (C-SSRS) or PHQ-9 Question 9 indicating active intent immediately mandates 24/7 crisis protocol triage (988 Lifeline) and precludes routine asynchronous telehealth.")
        ]
    }
}

FINANCE_PAGES = {
    "finance/islamic-diminishing-musharaka/index.html": {
        "slug": "finance/islamic-diminishing-musharaka",
        "title": "Diminishing Musharaka Calculator (AAOIFI No. 12)",
        "api_endpoint": "https://omnioperand.com/api/v1/finance/islamic-diminishing-musharaka",
        "api_method": "GET"
    },
    "finance/islamic-ijara/index.html": {
        "slug": "finance/islamic-ijara",
        "title": "Islamic Ijara Home Lease & Buyout Calculator (AAOIFI No. 9)",
        "api_endpoint": "https://omnioperand.com/api/v1/finance/islamic-ijara",
        "api_method": "GET"
    },
    "finance/islamic-murabaha/index.html": {
        "slug": "finance/islamic-murabaha",
        "title": "Islamic Murabaha Cost-Plus Financing Calculator (AAOIFI No. 8)",
        "api_endpoint": "https://omnioperand.com/api/v1/finance/islamic-murabaha",
        "api_method": "GET"
    },
    "finance/itin-mortgage/index.html": {
        "slug": "finance/itin-mortgage",
        "title": "ITIN Mortgage Calculator (Non-SSN Home Loan)",
        "api_endpoint": "https://omnioperand.com/api/v1/finance/itin-mortgage",
        "api_method": "GET"
    },
    "es/finance/itin-mortgage/index.html": {
        "slug": "es/finance/itin-mortgage",
        "title": "Calculadora de Préstamos Hipotecarios ITIN",
        "api_endpoint": "https://omnioperand.com/api/v1/finance/itin-mortgage",
        "api_method": "GET"
    }
}

def generate_llm_box(slug: str, title: str, api_url: str, method: str) -> str:
    return f'''    <!-- Dual AI Agent & Prompt Integration Box -->
    <section class="llm-box" style="margin-top:2rem;">
      <div class="llm-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:0.75rem;">
        <div>
          <span class="llm-badge" style="background:rgba(56,189,248,0.15); color:var(--accent-cyan); font-size:0.75rem; font-weight:700; text-transform:uppercase; padding:3px 8px; border-radius:4px; letter-spacing:0.5px;">LLM Directive &amp; API Spec</span>
          <h3 style="margin:0.35rem 0 0 0; font-size:1.25rem; color:var(--text-bright);">Artificial Intelligence &amp; Prompt Integration</h3>
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
        <span><span style="color:var(--accent-cyan); font-weight:700;">{method}</span> {api_url}</span>
        <span style="color:var(--text-muted); font-size:0.75rem;">JSON Invariants</span>
      </div>

      <pre class="llm-prompt-code" id="llm-prompt-display" style="background:var(--bg-canvas); border:1px solid var(--border-subtle); border-radius:6px; padding:10px 14px; font-size:0.8rem; color:var(--text-secondary); font-family:monospace; white-space:pre-wrap; max-height:160px; overflow-y:auto; line-height:1.45;">Generating verified mathematical prompt for {title}...</pre>

      <div style="font-size:0.75rem; color:var(--text-muted); display:flex; align-items:center; gap:1rem; flex-wrap:wrap; margin-top:0.75rem;">
        <span>✓ Standardized for <code>llms.txt</code></span>
        <span>✓ Deterministic Statutory Models</span>
        <span>✓ Machine-Readable Edge API</span>
      </div>
    </section>'''

def generate_faq_section(faq_list):
    items = []
    for q, a in faq_list:
        items.append(f'''      <div class="faq-item open">
        <div class="faq-question">
          <span>{q}</span>
          <span class="faq-icon">+</span>
        </div>
        <div class="faq-answer">
          {a}
        </div>
      </div>''')
    items_html = "\n\n".join(items)
    return f'''    <!-- FAQ Section -->
    <section class="faq-section" style="margin-top:2.5rem;">
      <h2 style="font-size:1.75rem; margin-bottom:1rem;">Frequently Asked Questions</h2>
{items_html}
    </section>'''

def fix_statutory_pages():
    print("Fixing 5 statutory engineering compliance pages...")
    for rel_path, data in STATUTORY_PAGES.items():
        file_path = REPO_ROOT / rel_path
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")

        # 1. Fix the broken badge nesting
        # Replace:
        # <div class="calc-title-badge">Title
        # <div class="calculator-actions-toolbar">...</div>
        # </div>
        broken_badge_pattern = re.compile(
            r'<div class="calc-title-badge">([^<]+)\s*<div class="calculator-actions-toolbar">[\s\S]*?</div>\s*</div>',
            re.MULTILINE
        )
        match = broken_badge_pattern.search(content)
        if match:
            badge_text = match.group(1).strip()
            fixed_badge = f'<div class="calc-title-badge">{badge_text}</div>'
            content = broken_badge_pattern.sub(fixed_badge, content, count=1)

        # Ensure actions toolbar is after hero-subtext or before </section>
        if 'id="btn-embed"' not in content:
            if '<p style="font-size: 1.05rem;' in content:
                content = re.sub(
                    r'(<p style="font-size: 1.05rem;[\s\S]*?</p>)',
                    r'\1\n' + TOOLBAR_HTML,
                    content,
                    count=1
                )
            elif '</section>' in content:
                content = content.replace('</section>', TOOLBAR_HTML + '\n    </section>', 1)

        # 2. Add LLM Box before </main>
        if 'class="llm-box"' not in content and '</main>' in content:
            llm_box_html = generate_llm_box(data["slug"], data["title"], data["api_endpoint"], data["api_method"])
            content = content.replace('</main>', llm_box_html + '\n  </main>', 1)

        # 3. Add FAQ Section before </main>
        if 'class="faq-section"' not in content and '</main>' in content:
            faq_html = generate_faq_section(data["faq"])
            content = content.replace('</main>', faq_html + '\n  </main>', 1)

        # 4. Add Search modal and scripts before </body>
        if 'id="search-modal"' not in content:
            content = content.replace('</body>', SEARCH_MODAL_HTML + '\n\n</body>', 1)

        scripts_to_add = []
        if 'omni-search.js' not in content:
            scripts_to_add.append('  <script src="/assets/js/omni-search.js?v=2.4"></script>')
        if 'embed-modal.js' not in content:
            scripts_to_add.append('  <script src="/assets/js/embed-modal.js?v=2.2" defer></script>')

        if scripts_to_add:
            script_block = "\n".join(scripts_to_add)
            content = content.replace('</body>', script_block + '\n</body>', 1)

        file_path.write_text(content, encoding="utf-8")
        print(f"  ✓ Remediated {rel_path}")

def fix_finance_pages():
    print("Fixing Islamic finance and ITIN mortgage pages...")
    for rel_path, data in FINANCE_PAGES.items():
        file_path = REPO_ROOT / rel_path
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")

        # 1. Add LLM Box before </main>
        if 'class="llm-box"' not in content and '</main>' in content:
            llm_box_html = generate_llm_box(data["slug"], data["title"], data["api_endpoint"], data["api_method"])
            content = content.replace('</main>', llm_box_html + '\n  </main>', 1)

        # 2. Add Search modal and search script
        if 'id="search-modal"' not in content:
            content = content.replace('</body>', SEARCH_MODAL_HTML + '\n\n</body>', 1)

        if 'omni-search.js' not in content:
            content = content.replace('</body>', '  <script src="/assets/js/omni-search.js?v=2.4"></script>\n</body>', 1)

        file_path.write_text(content, encoding="utf-8")
        print(f"  ✓ Remediated {rel_path}")

def fix_multilingual_regular_polygon():
    print("Fixing multilingual regular polygon pages...")
    langs = ['de', 'es', 'fi', 'fr', 'it', 'nl', 'no', 'pl', 'pt', 'ro', 'sv']
    for lang in langs:
        rel_path = f"{lang}/geometry/2d/shapes/regular-polygon/index.html"
        file_path = REPO_ROOT / rel_path
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")

        modified = False
        if 'id="btn-embed"' not in content and 'btn-embed-calculator' not in content:
            # Insert after hero description
            if '<p class="hero-subtext">' in content:
                content = re.sub(
                    r'(<p class="hero-subtext">[\s\S]*?</p>)',
                    r'\1\n' + TOOLBAR_HTML,
                    content,
                    count=1
                )
                modified = True
            elif '</section>' in content:
                content = content.replace('</section>', TOOLBAR_HTML + '\n    </section>', 1)
                modified = True

        if 'embed-modal.js' not in content:
            content = content.replace('</body>', '  <script src="/assets/js/embed-modal.js?v=2.2" defer></script>\n</body>', 1)
            modified = True

        if modified:
            file_path.write_text(content, encoding="utf-8")
            print(f"  ✓ Remediated {rel_path}")

def fix_404():
    print("Fixing 404.html tags...")
    p = REPO_ROOT / "404.html"
    if p.exists():
        content = p.read_text(encoding="utf-8")
        if '<meta name="description"' not in content:
            content = content.replace(
                '<title>',
                '<meta name="description" content="Mathematical 404: The requested coordinate or computational route does not exist on OmniOperand.">\n  <link rel="canonical" href="https://omnioperand.com/404.html">\n  <meta property="og:title" content="404 — Coordinate Undefined | OmniOperand">\n  <meta property="og:description" content="The requested computational route is undefined.">\n  <meta property="og:url" content="https://omnioperand.com/404.html">\n  <title>',
                1
            )
            p.write_text(content, encoding="utf-8")
            print("  ✓ Remediated 404.html")

def fix_missing_og_tags():
    print("Fixing missing OpenGraph tags on category hubs...")
    hub_files = sorted(list(REPO_ROOT.glob("**/index.html")))
    for p in hub_files:
        if any(x in p.parts for x in ['.git', 'node_modules', 'dist']):
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        if '<meta property="og:title"' not in content:
            rel = p.relative_to(REPO_ROOT)
            rel_str = str(rel).replace('\\', '/')
            # Derive title and desc
            title_m = re.search(r'<title>([^<]+)</title>', content)
            title = title_m.group(1).strip() if title_m else "OmniOperand High-Precision Computational Engine"
            desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
            desc = desc_m.group(1).strip() if desc_m else "High-precision computational solvers and mathematical authority."
            url = f"https://omnioperand.com/{rel_str.replace('index.html', '')}"

            og_block = f'''  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">'''

            if '<link rel="canonical"' in content:
                content = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1\n' + og_block, content, count=1)
                p.write_text(content, encoding="utf-8")
                print(f"  ✓ Added OG tags to {rel_str}")

def main():
    fix_statutory_pages()
    fix_finance_pages()
    fix_multilingual_regular_polygon()
    fix_404()
    fix_missing_og_tags()
    print("✅ All remediation tasks completed successfully.")

if __name__ == "__main__":
    main()
