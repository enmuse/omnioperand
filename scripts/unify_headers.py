#!/usr/bin/env python3
"""
scripts/unify_headers.py
Unifies the site header navigation and multi-language switcher across all HTML files on OmniOperand.
Provides consistent, uniform navigation choices and internationalization everywhere:
- Language Selector (🇺🇸 EN, 🇪🇸 ES, 🇫🇷 FR, 🇩🇪 DE, 🇸🇪 SV, 🇳🇴 NO, 🇫🇮 FI, 🇷🇴 RO)
- Geometry
- Calculus
- Finance
- Physics
- Disciplines Dropdown (all 16 domains)
- Universal N-Gon
- MCP Server
- REST API
- Pricing

Inlines critical dropdown CSS alongside the header to guarantee 0ms render
and 100% protection against CDN or browser CSS cache staleness.
Also cache-busts /assets/css/omni-core.css?v=2.2 and /assets/js/omni-search.js?v=2.1.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LANGUAGES = [
    {"code": "en", "name": "English", "flag": "🇺🇸", "prefix": ""},
    {"code": "es", "name": "Español", "flag": "🇪🇸", "prefix": "/es"},
    {"code": "fr", "name": "Français", "flag": "🇫🇷", "prefix": "/fr"},
    {"code": "de", "name": "Deutsch", "flag": "🇩🇪", "prefix": "/de"},
    {"code": "it", "name": "Italiano", "flag": "🇮🇹", "prefix": "/it"},
    {"code": "pt", "name": "Português", "flag": "🇵🇹", "prefix": "/pt"},
    {"code": "nl", "name": "Nederlands", "flag": "🇳🇱", "prefix": "/nl"},
    {"code": "pl", "name": "Polski", "flag": "🇵🇱", "prefix": "/pl"},
    {"code": "sv", "name": "Svenska", "flag": "🇸🇪", "prefix": "/sv"},
    {"code": "no", "name": "Norsk", "flag": "🇳🇴", "prefix": "/no"},
    {"code": "fi", "name": "Suomi", "flag": "🇫🇮", "prefix": "/fi"},
    {"code": "ro", "name": "Română", "flag": "🇷🇴", "prefix": "/ro"},
]

LANG_MAP = {l["code"]: l for l in LANGUAGES}
NON_EN_CODES = {l["code"] for l in LANGUAGES if l["code"] != "en"}

def build_uniform_header(rel_path_str: str) -> str:
    norm_path = rel_path_str.replace('\\', '/')
    path_parts = norm_path.split('/')
    
    # Detect language prefix
    if len(path_parts) > 1 and path_parts[0] in NON_EN_CODES:
        current_lang = path_parts[0]
        base_parts = path_parts[1:]
    else:
        current_lang = 'en'
        base_parts = path_parts

    base_rel_path = '/'.join(base_parts)
    top_dir = base_parts[0] if len(base_parts) > 1 else ''

    # Compute base path for language switching
    if base_rel_path in ('index.html', '404.html'):
        base_url_path = ''
    elif base_rel_path.endswith('/index.html'):
        base_url_path = base_rel_path[:-len('index.html')]
    elif base_rel_path.endswith('.html'):
        base_url_path = base_rel_path
    else:
        base_url_path = base_rel_path + '/' if not base_rel_path.endswith('/') else base_rel_path

    # Active category detection
    active_cat = ''
    badge_text = 'Math Engine'

    if base_rel_path in ('index.html', '404.html'):
        active_cat = 'home'
        badge_text = 'Math Engine'
    elif base_rel_path.startswith('geometry/2d/shapes/regular-polygon/'):
        active_cat = 'regular-polygon'
        badge_text = 'Universal Solver'
    elif base_rel_path.startswith('geometry/2d/shapes/octagon/'):
        active_cat = 'geometry'
        badge_text = 'Geometry'
    elif base_rel_path.startswith('api/'):
        active_cat = 'api'
        badge_text = 'REST API'
    elif base_rel_path.startswith('mcp/'):
        active_cat = 'mcp'
        badge_text = 'MCP Server'
    elif base_rel_path.startswith('pricing/'):
        active_cat = 'pricing'
        badge_text = 'Pricing'
    elif base_rel_path.startswith('embed/'):
        active_cat = 'embed'
        badge_text = 'Embed CaaS'
    else:
        active_cat = top_dir
        badge_text = top_dir.capitalize() if top_dir else 'Math Engine'

    geom_active = ' active' if active_cat == 'geometry' else ''
    calc_active = ' active' if active_cat == 'calculus' else ''
    fin_active = ' active' if active_cat == 'finance' else ''
    phys_active = ' active' if active_cat == 'physics' else ''
    ngon_active = ' active' if active_cat == 'regular-polygon' else ''
    mcp_active = ' active' if active_cat == 'mcp' else ''
    api_active = ' active' if active_cat == 'api' else ''
    price_active = ' active' if active_cat == 'pricing' else ''

    other_disciplines = {
        'statistics', 'construction', 'health', 'engineering',
        'energy', 'logistics', 'crypto', 'ecommerce', 'biotech',
        'legal', 'agriculture', 'embed', 'automotive', 'real-estate',
        'tax-payroll', 'b2b-saas'
    }
    disc_active = ' active' if active_cat in other_disciplines else ''

    current_meta = LANG_MAP.get(current_lang, LANG_MAP['en'])
    current_flag = current_meta['flag']
    current_code_upper = current_lang.upper()

    # Build language dropdown items
    lang_items = []
    for l in LANGUAGES:
        code = l['code']
        flag = l['flag']
        name = l['name']
        is_active = ' active' if code == current_lang else ''
        if code == 'en':
            target_url = f"/{base_url_path}" if base_url_path else "/"
        else:
            target_url = f"/{code}/{base_url_path}" if base_url_path else f"/{code}/"
        
        lang_items.append(
            f'<a href="{target_url}" class="lang-dropdown-item{is_active}">'
            f'<span class="lang-flag">{flag}</span>'
            f'<span class="lang-name">{name}</span>'
            f'<span class="lang-code-pill">{code.upper()}</span>'
            f'</a>'
        )

    lang_items_html = '\n            '.join(lang_items)

    # Prefix for nav links if in non-en
    lang_prefix = f"/{current_lang}" if current_lang != 'en' else ""
    home_url = f"/{current_lang}/" if current_lang != 'en' else "/"

    header_html = f'''  <!-- Critical Navigation Dropdown CSS (0ms FOUC & Cache-Proof) -->
  <style id="omni-nav-dropdown-css">
    .nav-dropdown {{ position: relative; display: inline-flex; align-items: center; }}
    .nav-dropdown-trigger {{ display: inline-flex; align-items: center; gap: 0.35rem; color: var(--text-secondary); font-size: 0.925rem; font-weight: 500; padding: 0.4rem 0.6rem; border-radius: var(--radius-sm); background: transparent; border: none; cursor: pointer; font-family: inherit; white-space: nowrap; transition: color 0.15s ease, background 0.15s ease; }}
    .nav-dropdown-trigger:hover, .nav-dropdown-trigger.active, .nav-dropdown:hover .nav-dropdown-trigger, .nav-dropdown:focus-within .nav-dropdown-trigger {{ color: var(--text-primary); background: rgba(56, 189, 248, 0.08); }}
    .nav-dropdown-trigger svg {{ transition: transform 0.2s ease; }}
    .nav-dropdown:hover .nav-dropdown-trigger svg, .nav-dropdown:focus-within .nav-dropdown-trigger svg, .nav-dropdown.is-open .nav-dropdown-trigger svg {{ transform: rotate(180deg); }}
    .nav-dropdown-menu {{ display: none; position: absolute; top: calc(100% + 4px); left: 50%; transform: translateX(-50%); width: 440px; max-width: 90vw; background: #101726; background: var(--bg-surface-elevated, #101726); border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.12)); border-radius: 12px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 24px rgba(6, 182, 212, 0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 0.75rem; grid-template-columns: repeat(2, 1fr); gap: 0.25rem 0.5rem; z-index: 1000; }}
    .nav-dropdown-menu::before {{ content: ''; position: absolute; top: -8px; left: 0; right: 0; height: 8px; }}
    .nav-dropdown:hover .nav-dropdown-menu, .nav-dropdown:focus-within .nav-dropdown-menu, .nav-dropdown.is-open .nav-dropdown-menu {{ display: grid; }}
    .nav-dropdown-item {{ display: flex; align-items: center; gap: 0.6rem; padding: 0.45rem 0.65rem; border-radius: 6px; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; text-decoration: none; transition: all 0.12s ease; }}
    .nav-dropdown-item:hover {{ color: var(--accent-cyan); background: rgba(6, 182, 212, 0.08); transform: translateX(2px); }}
    .nav-dropdown-item .item-icon {{ font-size: 1rem; line-height: 1; width: 1.25rem; text-align: center; }}
    
    /* Internationalization Language Switcher Dropdown */
    .lang-dropdown {{ position: relative; display: inline-flex; align-items: center; }}
    .lang-dropdown-trigger {{ display: inline-flex; align-items: center; gap: 0.35rem; color: var(--text-secondary); font-size: 0.825rem; font-weight: 600; padding: 0.35rem 0.55rem; border-radius: var(--radius-sm); background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.12)); cursor: pointer; font-family: inherit; transition: all 0.15s ease; }}
    .lang-dropdown-trigger:hover, .lang-dropdown-trigger.active, .lang-dropdown:hover .lang-dropdown-trigger, .lang-dropdown:focus-within .lang-dropdown-trigger {{ color: var(--text-primary); background: rgba(56, 189, 248, 0.1); border-color: rgba(56, 189, 248, 0.35); }}
    .lang-dropdown-trigger svg {{ transition: transform 0.2s ease; }}
    .lang-dropdown:hover .lang-dropdown-trigger svg, .lang-dropdown:focus-within .lang-dropdown-trigger svg, .lang-dropdown.is-open .lang-dropdown-trigger svg {{ transform: rotate(180deg); }}
    .lang-dropdown-menu {{ display: none; position: absolute; top: calc(100% + 6px); right: 0; width: 330px; background: #101726; background: var(--bg-surface-elevated, #101726); border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.12)); border-radius: 10px; box-shadow: 0 16px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(6, 182, 212, 0.12); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 0.5rem; z-index: 1000; grid-template-columns: repeat(2, 1fr); gap: 2px 6px; }}
    .lang-dropdown-menu::before {{ content: ''; position: absolute; top: -8px; left: 0; right: 0; height: 8px; }}
    .lang-dropdown:hover .lang-dropdown-menu, .lang-dropdown:focus-within .lang-dropdown-menu, .lang-dropdown.is-open .lang-dropdown-menu {{ display: grid; }}
    .lang-dropdown-item {{ display: flex; align-items: center; justify-content: space-between; gap: 0.4rem; padding: 0.35rem 0.5rem; border-radius: 6px; color: var(--text-secondary); font-size: 0.825rem; font-weight: 500; text-decoration: none; transition: all 0.12s ease; }}
    .lang-dropdown-item:hover {{ color: var(--accent-cyan); background: rgba(6, 182, 212, 0.08); }}
    .lang-dropdown-item.active {{ color: var(--accent-cyan); background: rgba(6, 182, 212, 0.12); font-weight: 600; }}
    .lang-dropdown-item .lang-flag {{ font-size: 0.95rem; line-height: 1; }}
    .lang-code-pill {{ font-size: 0.65rem; font-weight: 700; color: var(--text-muted); padding: 1px 4px; border-radius: 3px; background: rgba(255, 255, 255, 0.06); }}
    .lang-dropdown-item.active .lang-code-pill {{ color: var(--accent-cyan); background: rgba(6, 182, 212, 0.25); }}

    @media (max-width: 768px) {{
      body.mobile-nav-open .nav-dropdown {{ flex-direction: column; align-items: stretch; width: 100%; }}
      body.mobile-nav-open .nav-dropdown-menu {{ position: static; transform: none; width: 100%; max-width: 100%; display: grid; box-shadow: none; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-subtle); margin-top: 0.5rem; }}
      .lang-dropdown-menu {{ right: auto; left: 0; width: 100%; max-width: 310px; }}
    }}
  </style>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="{home_url}" class="brand-link">
        <img src="/assets/images/logo.png" alt="OmniOperand Logo" class="brand-logo-img" width="32" height="32">
        <span>OmniOperand</span>
        <span class="brand-badge">{badge_text}</span>
      </a>

      <nav class="header-nav" aria-label="Main Navigation">
        <a href="{lang_prefix}/geometry/" class="nav-link{geom_active}">Geometry</a>
        <a href="{lang_prefix}/calculus/" class="nav-link{calc_active}">Calculus</a>
        <a href="{lang_prefix}/finance/" class="nav-link{fin_active}">Finance</a>
        <a href="{lang_prefix}/physics/" class="nav-link{phys_active}">Physics</a>
        <div class="nav-dropdown">
          <button class="nav-dropdown-trigger{disc_active}" type="button" aria-expanded="false" aria-haspopup="true">
            <span>Disciplines</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="nav-dropdown-menu">
            <a href="{lang_prefix}/geometry/" class="nav-dropdown-item"><span class="item-icon">📐</span><span>Geometry</span></a>
            <a href="{lang_prefix}/calculus/" class="nav-dropdown-item"><span class="item-icon">∫</span><span>Calculus</span></a>
            <a href="{lang_prefix}/finance/" class="nav-dropdown-item"><span class="item-icon">💵</span><span>Finance</span></a>
            <a href="{lang_prefix}/physics/" class="nav-dropdown-item"><span class="item-icon">⚡</span><span>Physics</span></a>
            <a href="{lang_prefix}/statistics/" class="nav-dropdown-item"><span class="item-icon">📊</span><span>Statistics</span></a>
            <a href="{lang_prefix}/construction/" class="nav-dropdown-item"><span class="item-icon">🏗️</span><span>Construction</span></a>
            <a href="/health/" class="nav-dropdown-item"><span class="item-icon">🩺</span><span>Health</span></a>
            <a href="/engineering/" class="nav-dropdown-item"><span class="item-icon">🌉</span><span>Engineering</span></a>
            <a href="/energy/" class="nav-dropdown-item"><span class="item-icon">☀️</span><span>Energy &amp; Solar</span></a>
            <a href="/logistics/" class="nav-dropdown-item"><span class="item-icon">🚢</span><span>Logistics</span></a>
            <a href="/crypto/" class="nav-dropdown-item"><span class="item-icon">🪙</span><span>Crypto &amp; DeFi</span></a>
            <a href="/ecommerce/" class="nav-dropdown-item"><span class="item-icon">🛒</span><span>E-Commerce</span></a>
            <a href="/biotech/" class="nav-dropdown-item"><span class="item-icon">🧬</span><span>Biotech</span></a>
            <a href="/legal/" class="nav-dropdown-item"><span class="item-icon">⚖️</span><span>Legal &amp; Risk</span></a>
            <a href="/agriculture/" class="nav-dropdown-item"><span class="item-icon">🌾</span><span>Agriculture</span></a>
            <a href="/embed/" class="nav-dropdown-item"><span class="item-icon">🔌</span><span>Embed Widgets</span></a>
          </div>
        </div>
        <a href="{lang_prefix}/geometry/2d/shapes/regular-polygon/" class="nav-link nav-link-featured{ngon_active}">Universal N-Gon</a>
        <a href="/mcp/" class="nav-link nav-link-mcp{mcp_active}">MCP Server</a>
        <a href="/api/" class="nav-link{api_active}">REST API</a>
        <a href="/pricing/" class="nav-link{price_active}">Pricing</a>
      </nav>

      <div class="header-actions">
        <!-- Multi-Language Switcher -->
        <div class="lang-dropdown">
          <button class="lang-dropdown-trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-label="Select Language">
            <span class="lang-flag">{current_flag}</span>
            <span class="lang-code">{current_code_upper}</span>
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="lang-dropdown-menu">
            {lang_items_html}
          </div>
        </div>

        <button class="search-btn-trigger" id="global-search-trigger" aria-label="Search calculators">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <span>Search</span>
          <kbd class="search-kbd">⌘K</kbd>
        </button>
        <button class="btn-icon" id="theme-toggle-btn" aria-label="Toggle Dark/Light Mode">☀️</button>
        <button class="btn-icon mobile-menu-btn" id="mobile-menu-toggle" aria-label="Toggle Navigation Menu">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      </div>
    </div>
  </header>'''
    return header_html

def unify_all_headers():
    header_pattern = re.compile(
        r'(?:<!--\s*Critical\s+Navigation\s+Dropdown\s+CSS[^>]*-->\s*)?'
        r'(?:<style id=[\"\']omni-nav-dropdown-css[\"\']>.*?</style>\s*)?'
        r'(?:<!--\s*(?:Master\s+)?Site\s+Header\s*-->\s*)?'
        r'<header\s+class=[\"\'](?:site-header|omni-header)[\"\']>.*?</header>',
        re.DOTALL
    )
    
    count = 0
    updated_files = []
    
    for root, dirs, files in os.walk(REPO_ROOT):
        if '.git' in root or 'node_modules' in root or '.wrangler' in root:
            continue
        for file in files:
            if not file.endswith('.html'):
                continue
            
            full_path = Path(root) / file
            rel_path = full_path.relative_to(REPO_ROOT).as_posix()
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cache bust omni-core.css?v=2.2 and omni-search.js
            new_content = re.sub(r'href=([\"\'])/assets/css/omni-core\.css(?:\?v=[^\"\']*)?([\"\'])', r'href=\1/assets/css/omni-core.css?v=2.2\2', content)
            new_content = re.sub(r'src=([\"\'])/assets/js/omni-search\.js(?:\?v=[^\"\']*)?([\"\'])', r'src=\1/assets/js/omni-search.js?v=2.1\2', new_content)

            if header_pattern.search(new_content):
                new_header = build_uniform_header(rel_path)
                new_content = header_pattern.sub(new_header, new_content, count=1)
                
                if new_content != content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    updated_files.append(rel_path)
            else:
                if new_content != content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    updated_files.append(rel_path)

    print(f"✅ Successfully unified headers, language switcher, and CSS cache-busting across {count} HTML files!")

if __name__ == '__main__':
    unify_all_headers()
