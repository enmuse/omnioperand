#!/usr/bin/env python3
"""
scripts/remediate_internal_links.py — Fix broken localized dropdowns, translated slug typos, and missing category indices.

Resolves GSC 404 validation failure on omnioperand.com by eliminating all internal links to phantom URLs.
"""

import os
import glob
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LANGS = ['de', 'es', 'fi', 'fr', 'it', 'nl', 'no', 'pl', 'pt', 'ro', 'sv']

def build_valid_path_index():
    """Maps all existing files and virtual directory index paths."""
    valid_paths = set()
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # Ignore git, node_modules, wrangler
        if any(ignored in dirpath for ignored in ['.git', 'node_modules', '.wrangler']):
            continue
        rel_dir = os.path.relpath(dirpath, REPO_ROOT)
        if rel_dir == '.':
            rel_dir = ''
        for fn in filenames:
            rel_file = os.path.join(rel_dir, fn) if rel_dir else fn
            valid_paths.add('/' + rel_file)
            if fn == 'index.html':
                if rel_dir:
                    valid_paths.add('/' + rel_dir + '/')
                    valid_paths.add('/' + rel_dir)
                else:
                    valid_paths.add('/')
            elif fn.endswith('.html'):
                valid_paths.add('/' + rel_file[:-5])
                valid_paths.add('/' + rel_file[:-5] + '/')
    return valid_paths

def create_italian_engineering_hub(valid_paths):
    """Creates it/ingegneria/index.html to serve as a category landing page for Italian engineering solvers."""
    hub_path = os.path.join(REPO_ROOT, "it", "ingegneria", "index.html")
    if os.path.exists(hub_path):
        return
    
    os.makedirs(os.path.dirname(hub_path), exist_ok=True)
    hub_html = """<!DOCTYPE html>
<html lang="it" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ingegneria Elettrica & Industriale | OmniOperand</title>
  <meta name="description" content="Calcolatori avanzati per ingegneria elettrica e meccanica: dimensionamento gruppi elettrogeni, caduta di tensione e potenza.">
  <link rel="canonical" href="https://omnioperand.com/it/ingegneria/">
  <link rel="alternate" hreflang="en" href="https://omnioperand.com/engineering/">
  <link rel="alternate" hreflang="it" href="https://omnioperand.com/it/ingegneria/">
  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com/engineering/">

  <meta property="og:title" content="Ingegneria Elettrica & Industriale | OmniOperand">
  <meta property="og:description" content="Calcolatori avanzati per ingegneria elettrica e meccanica: dimensionamento gruppi elettrogeni, caduta di tensione e potenza.">
  <meta property="og:url" content="https://omnioperand.com/it/ingegneria/">
  <meta property="og:type" content="website">

  <link rel="stylesheet" href="/assets/css/omni-core.css?v=2.2">
  <link rel="stylesheet" href="/assets/css/calculator.css?v=1.3">
  <link rel="icon" type="image/png" href="/assets/images/logo.png">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CollectionPage",
        "@id": "https://omnioperand.com/it/ingegneria/#hub",
        "name": "Ingegneria Elettrica & Industriale",
        "url": "https://omnioperand.com/it/ingegneria/",
        "inLanguage": "it"
      }
    ]
  }
  </script>
</head>
<body>
  <header class="header">
    <div class="container header-container">
      <a href="/it/" class="logo">
        <span class="logo-icon">📐</span>
        <span class="logo-text">Omni<span>Operand</span> <span class="logo-lang-badge">IT</span></span>
      </a>
      <nav class="nav">
        <a href="/it/">Home</a>
        <a href="/it/finance/">Finanza</a>
        <a href="/it/construction/">Edilizia</a>
        <a href="/it/geometry/">Geometria</a>
        <a href="/it/physics/">Fisica</a>
        <a href="/it/statistics/">Statistica</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <div class="container">
      <nav class="breadcrumb-wrapper" aria-label="Breadcrumb">
        <ol class="breadcrumbs">
          <li class="breadcrumb-item"><a href="/it/">Inizio</a></li>
          <li class="breadcrumb-separator">/</li>
          <li class="breadcrumb-item active" aria-current="page">Ingegneria</li>
        </ol>
      </nav>

      <section class="category-hero">
        <h1 class="category-title">Ingegneria Elettrica & Meccanica</h1>
        <p class="category-description">Solutori e calcolatori ad alta precisione con conformità alle normative CEI ed industriali europee.</p>
      </section>

      <div class="calculator-grid">
        <article class="calculator-card">
          <div class="card-icon">⚡</div>
          <h2 class="card-title">Dimensionamento Gruppo Elettrogeno</h2>
          <p class="card-description">Calcola kW continui, kVA di spunto induttivo e potenza nominale del generatore con margine del 20%.</p>
          <a href="/it/ingegneria/dimensionamento-gruppo-elettrogeno/" class="card-link">Apri Solutore →</a>
        </article>
      </div>
    </div>
  </main>

  <footer class="footer">
    <div class="container footer-bottom">
      <p>&copy; 2026 OmniOperand. Tutti i diritti riservati.</p>
    </div>
  </footer>
</body>
</html>
"""
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("✅ Created it/ingegneria/index.html")
    valid_paths.add("/it/ingegneria/")
    valid_paths.add("/it/ingegneria")

def fix_html_files(valid_paths):
    html_files = glob.glob(os.path.join(REPO_ROOT, "**/*.html"), recursive=True)
    total_modified = 0
    total_dropdown_fixed = 0
    total_slug_fixed = 0
    total_typos_fixed = 0

    for filepath in html_files:
        # Ignore external/vendor directories
        if any(ignored in filepath for ignored in ['.git', 'node_modules', '.wrangler']):
            continue

        rel_path = os.path.relpath(filepath, REPO_ROOT)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            original = f.read()

        content = original

        # 1. Normalize language dropdown menu
        dropdown_match = re.search(r'(<div class=[\"\']lang-dropdown-menu[\"\']>)(.*?)(</div>)', content, re.DOTALL)
        if dropdown_match:
            prefix = dropdown_match.group(1)
            block = dropdown_match.group(2)
            suffix = dropdown_match.group(3)

            def dropdown_replacer(m):
                nonlocal total_dropdown_fixed
                href = m.group(1)
                rest = m.group(2)

                # Special fix for generator sizing English link inside Italian page
                if "dimensionamento-gruppo-elettrogeno" in href and ('EN' in rest or '🇺🇸' in rest or href.startswith('/ingegneria/')):
                    total_dropdown_fixed += 1
                    return f'<a href="/engineering/generator-sizing/"{rest}'

                # Check if href exists on disk
                if href in valid_paths or (href + '/' in valid_paths) or (href.endswith('/') and href[:-1] in valid_paths):
                    return m.group(0)

                # Check if localized href can fallback to language home
                parts = [p for p in href.split('/') if p]
                if parts and parts[0] in LANGS:
                    total_dropdown_fixed += 1
                    return f'<a href="/{parts[0]}/"{rest}'

                return m.group(0)

            new_block = re.sub(r'<a href=[\"\'](/[^\"\'#?]+)[\"\']([^>]*)', dropdown_replacer, block)
            if new_block != block:
                content = content[:dropdown_match.start()] + prefix + new_block + suffix + content[dropdown_match.end():]

        # 2. Fix translated slug typos in finance hubs and articles
        new_content = re.sub(r'/finance/rule-(?:de|di|av|z|van|von|n)-72/?', '/finance/rule-of-72/', content)
        if new_content != content:
            total_slug_fixed += 1
            content = new_content

        new_content = re.sub(r'/finance/saas-rule-(?:de|di|av|z|van|von|n)-40/?', '/finance/saas-rule-of-40/', content)
        if new_content != content:
            total_slug_fixed += 1
            content = new_content

        new_content = re.sub(r'/finance/internal-rate-(?:de|di|av|z|van|von|n)-return/?', '/finance/internal-rate-of-return/', content)
        if new_content != content:
            total_slug_fixed += 1
            content = new_content

        new_content = re.sub(r'/finance/fsa-use-it-(?:o|ou|eller|oder|lub|tai|sau|van)-lose-it/?', '/finance/fsa-use-it-or-lose-it/', content)
        if new_content != content:
            total_slug_fixed += 1
            content = new_content

        # 3. Fix specific single-file link targets
        if '/energy/solar-panel-payback/' in content:
            content = content.replace('/energy/solar-panel-payback/', '/energy/solar-payback/')
            total_typos_fixed += 1

        if '/logistics/pallet-load/' in content:
            content = content.replace('/logistics/pallet-load/', '/logistics/pallet-ti-hi-optimizer/')
            total_typos_fixed += 1

        if '/logistics/air-freight-volumetric/' in content:
            content = content.replace('/logistics/air-freight-volumetric/', '/logistics/air-freight-chargeable-weight/')
            total_typos_fixed += 1

        if rel_path == 'it/ingegneria/dimensionamento-gruppo-elettrogeno/index.html':
            # Fix breadcrumbs and links
            content = content.replace('href="/ingegneria/dimensionamento-gruppo-elettrogeno/"', 'href="/engineering/generator-sizing/"')
            content = content.replace('https://omnioperand.com/ingegneria/dimensionamento-gruppo-elettrogeno/', 'https://omnioperand.com/engineering/generator-sizing/')

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            total_modified += 1

    print(f"\n📊 Remediation Summary:")
    print(f"  • Files modified: {total_modified}")
    print(f"  • Language dropdown links normalized: {total_dropdown_fixed}")
    print(f"  • Finance translated slug links repaired: {total_slug_fixed}")
    print(f"  • Specific slug typos fixed: {total_typos_fixed}")

if __name__ == "__main__":
    paths = build_valid_path_index()
    create_italian_engineering_hub(paths)
    fix_html_files(paths)

