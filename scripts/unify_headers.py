#!/usr/bin/env python3
"""
scripts/unify_headers.py
Unifies the site header navigation across all HTML files on OmniOperand.
Provides consistent, uniform navigation choices everywhere:
- Geometry
- Calculus
- Finance
- Physics
- Disciplines Dropdown (all 16 domains)
- Universal N-Gon
- MCP Server
- REST API
- Pricing
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def build_uniform_header(rel_path_str: str) -> str:
    path_parts = rel_path_str.replace('\\', '/').split('/')
    top_dir = path_parts[0] if len(path_parts) > 1 else ''

    active_cat = ''
    badge_text = 'Math Engine'

    if rel_path_str in ('index.html', '404.html'):
        active_cat = 'home'
        badge_text = 'Math Engine'
    elif rel_path_str.startswith('geometry/2d/shapes/regular-polygon/'):
        active_cat = 'regular-polygon'
        badge_text = 'Universal Solver'
    elif rel_path_str.startswith('geometry/2d/shapes/octagon/'):
        active_cat = 'geometry'
        badge_text = 'Geometry'
    elif rel_path_str.startswith('api/'):
        active_cat = 'api'
        badge_text = 'REST API'
    elif rel_path_str.startswith('mcp/'):
        active_cat = 'mcp'
        badge_text = 'MCP Server'
    elif rel_path_str.startswith('pricing/'):
        active_cat = 'pricing'
        badge_text = 'Pricing'
    elif rel_path_str.startswith('embed/'):
        active_cat = 'embed'
        badge_text = 'Embed CaaS'
    else:
        active_cat = top_dir
        badge_text = top_dir.capitalize()

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

    header_html = f'''  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand-link">
        <img src="/assets/images/logo.png" alt="OmniOperand Logo" class="brand-logo-img" width="32" height="32">
        <span>OmniOperand</span>
        <span class="brand-badge">{badge_text}</span>
      </a>

      <nav class="header-nav" aria-label="Main Navigation">
        <a href="/geometry/" class="nav-link{geom_active}">Geometry</a>
        <a href="/calculus/" class="nav-link{calc_active}">Calculus</a>
        <a href="/finance/" class="nav-link{fin_active}">Finance</a>
        <a href="/physics/" class="nav-link{phys_active}">Physics</a>
        <div class="nav-dropdown">
          <button class="nav-dropdown-trigger{disc_active}" type="button" aria-expanded="false" aria-haspopup="true">
            <span>Disciplines</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="nav-dropdown-menu">
            <a href="/geometry/" class="nav-dropdown-item"><span class="item-icon">📐</span><span>Geometry</span></a>
            <a href="/calculus/" class="nav-dropdown-item"><span class="item-icon">∫</span><span>Calculus</span></a>
            <a href="/finance/" class="nav-dropdown-item"><span class="item-icon">💵</span><span>Finance</span></a>
            <a href="/physics/" class="nav-dropdown-item"><span class="item-icon">⚡</span><span>Physics</span></a>
            <a href="/statistics/" class="nav-dropdown-item"><span class="item-icon">📊</span><span>Statistics</span></a>
            <a href="/construction/" class="nav-dropdown-item"><span class="item-icon">🏗️</span><span>Construction</span></a>
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
        <a href="/geometry/2d/shapes/regular-polygon/" class="nav-link nav-link-featured{ngon_active}">Universal N-Gon</a>
        <a href="/mcp/" class="nav-link nav-link-mcp{mcp_active}">MCP Server</a>
        <a href="/api/" class="nav-link{api_active}">REST API</a>
        <a href="/pricing/" class="nav-link{price_active}">Pricing</a>
      </nav>

      <div class="header-actions">
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
    header_pattern = re.compile(r'(?:<!--\s*(?:Master\s+)?Site\s+Header\s*-->\s*)?<header\s+class=[\"\'](?:site-header|omni-header)[\"\']>.*?</header>', re.DOTALL)
    
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
            
            if header_pattern.search(content):
                new_header = build_uniform_header(rel_path)
                new_content = header_pattern.sub(new_header, content, count=1)
                
                if new_content != content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    updated_files.append(rel_path)
            else:
                print(f"⚠️ Header pattern not found in {rel_path}")

    print(f"✅ Successfully unified headers across {count} HTML files!")

if __name__ == '__main__':
    unify_all_headers()
