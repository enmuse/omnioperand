/**
 * assets/js/embed-modal.js
 * OmniOperand Viral Embed Widget Modal & 1-Click Code Exporter
 * Injects the "Embed Tool" modal and copyable iframe snippets onto all calculator pages.
 */

(function () {
  'use strict';

  function initEmbedModal() {
    if (window.__omniEmbedInitialized) return;
    window.__omniEmbedInitialized = true;

    // If running inside an iframe embed already or on /embed/, don't inject button
    if (window.location.pathname.startsWith('/embed/') || window.parent !== window || window.location.search.includes('embed=true')) {
      return;
    }

    const isCalcPage = !!document.querySelector('.calculator-grid, .solver-container, .calculator-hud, .solver-panel, .param-card-grid, .hud-panel, .calc-container, [data-calculator]');
    if (!isCalcPage) return;

    // Inject Embed Button if not already in DOM
    let embedBtn = document.querySelector('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
    if (!embedBtn) {
      const toolbar = document.querySelector('.calculator-actions-toolbar');
      const solverToolbar = document.querySelector('.solver-toolbar');
      const blueprintBar = document.querySelector('.blueprint-export-bar');
      const hero = document.querySelector('.calculator-hero, .solver-hero, .calc-header-section, .hero-section');
      const hudHeader = document.querySelector('.hud-panel-header, .solver-panel-header');

      const btnHtml = `
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      `;

      if (toolbar) {
        toolbar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (solverToolbar) {
        solverToolbar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (blueprintBar) {
        blueprintBar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (hero) {
        const wrap = document.createElement('div');
        wrap.className = 'calculator-actions-toolbar';
        wrap.innerHTML = btnHtml;
        hero.appendChild(wrap);
      } else if (hudHeader) {
        hudHeader.insertAdjacentHTML('beforeend', btnHtml);
      }
    }

    // Ensure Embed Modal exists in DOM
    let modal = document.getElementById('omni-embed-modal');
    if (!modal) {
      const canonicalLink = document.querySelector('link[rel="canonical"]');
      const canonicalUrl = canonicalLink ? canonicalLink.href : (window.location.origin + window.location.pathname);
      const toolTitle = document.querySelector('h1')?.textContent?.trim() || document.title.split('—')[0].split('|')[0].trim();
      const iframeCode = `<iframe src="${canonicalUrl}?embed=true" width="100%" height="700" frameborder="0" style="border:1px solid #1e293b;border-radius:12px;width:100%;max-width:100%;"></iframe>\n<p style="font-size:12px;color:#64748b;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin-top:6px;text-align:right;">Calculator powered by <a href="${canonicalUrl}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;font-weight:600;">OmniOperand ${toolTitle}</a></p>`;

      const modalHtml = `
        <div id="omni-embed-modal" class="omni-modal-overlay">
          <div class="omni-modal-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:11px; font-weight:700; padding:3px 8px; border-radius:6px; text-transform:uppercase;">Widget Exporter</span>
                <h3 style="margin:0; font-size:1.2rem; font-weight:700; color:#f8fafc;">Embed This Calculator</h3>
              </div>
              <button type="button" id="omni-close-embed" style="background:none; border:none; color:#94a3b8; font-size:26px; cursor:pointer; line-height:1; padding:0 4px;" aria-label="Close embed modal">&times;</button>
            </div>

            <p style="font-size:0.875rem; color:#94a3b8; margin:0 0 16px; line-height:1.5;">
              Embed this high-precision mathematical solver on your blog, publication, or website. Completely free, mobile-responsive, and automatically includes verified backlink attribution.
            </p>

            <div style="display:flex; gap:8px; margin-bottom:12px;">
              <button type="button" id="tab-embed-iframe" class="btn-sm" style="background:#0284c7; color:#fff; border:none; border-radius:6px; padding:6px 14px; font-weight:600; cursor:pointer;">Responsive iFrame</button>
              <button type="button" id="tab-embed-backlink" class="btn-sm" style="background:rgba(255,255,255,0.06); color:#cbd5e1; border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:6px 14px; font-weight:500; cursor:pointer;">HTML Backlink</button>
            </div>

            <div style="margin-bottom:16px;">
              <textarea id="omni-embed-code-textarea" readonly rows="5" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; font-family:Consolas, 'JetBrains Mono', monospace; font-size:0.8rem; color:#7dd3fc; resize:none; line-height:1.45;">${iframeCode.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
              <div style="font-size:0.8rem; color:#64748b;">
                ✓ HTTPS encrypted • Canonical dofollow backlink included
              </div>
              <button type="button" id="omni-copy-embed-btn" style="background:#0284c7; color:#fff; border:none; padding:10px 20px; border-radius:8px; font-weight:600; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; gap:8px; transition:background 0.2s;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                <span id="omni-copy-btn-text">Copy Embed Code</span>
              </button>
            </div>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', modalHtml);
    }

    modal = document.getElementById('omni-embed-modal');
    const closeBtn = document.getElementById('omni-close-embed');
    const copyBtn = document.getElementById('omni-copy-embed-btn');
    const copyText = document.getElementById('omni-copy-btn-text');
    const textarea = document.getElementById('omni-embed-code-textarea');
    const tabIframe = document.getElementById('tab-embed-iframe');
    const tabBacklink = document.getElementById('tab-embed-backlink');

    const canonicalLink = document.querySelector('link[rel="canonical"]');
    const canonicalUrl = canonicalLink ? canonicalLink.href : (window.location.origin + window.location.pathname);
    const toolTitle = document.querySelector('h1')?.textContent?.trim() || document.title.split('—')[0].split('|')[0].trim();
    const iframeCode = `<iframe src="${canonicalUrl}?embed=true" width="100%" height="700" frameborder="0" style="border:1px solid #1e293b;border-radius:12px;width:100%;max-width:100%;"></iframe>\n<p style="font-size:12px;color:#64748b;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin-top:6px;text-align:right;">Calculator powered by <a href="${canonicalUrl}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;font-weight:600;">OmniOperand ${toolTitle}</a></p>`;
    const backlinkCode = `<a href="${canonicalUrl}" target="_blank" rel="noopener">Interactive ${toolTitle} by OmniOperand</a>`;

    if (tabIframe && tabBacklink && textarea) {
      tabIframe.addEventListener('click', () => {
        textarea.value = iframeCode;
        tabIframe.style.background = '#0284c7';
        tabIframe.style.color = '#fff';
        tabBacklink.style.background = 'rgba(255,255,255,0.06)';
        tabBacklink.style.color = '#cbd5e1';
      });
      tabBacklink.addEventListener('click', () => {
        textarea.value = backlinkCode;
        tabBacklink.style.background = '#0284c7';
        tabBacklink.style.color = '#fff';
        tabIframe.style.background = 'rgba(255,255,255,0.06)';
        tabIframe.style.color = '#cbd5e1';
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
        modal.style.display = 'none';
      }
    });

    if (copyBtn && textarea) {
      copyBtn.addEventListener('click', () => {
        textarea.select();
        navigator.clipboard.writeText(textarea.value).then(() => {
          copyText.textContent = '✓ Copied to Clipboard!';
          copyBtn.style.background = '#10b981';
          setTimeout(() => {
            copyText.textContent = 'Copy Embed Code';
            copyBtn.style.background = '#0284c7';
          }, 2500);
        });
      });
    }

    // Wire up all buttons that open embed modal
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
      if (trigger) {
        e.preventDefault();
        if (modal) modal.style.display = 'flex';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmbedModal);
  } else {
    initEmbedModal();
  }
})();
