/**
 * assets/js/embed-modal.js
 * OmniOperand Viral Embed Widget Modal & 1-Click Code Exporter
 * Injects the "Embed Calculator" modal and copyable iframe snippets onto all calculator pages.
 */

(function () {
  'use strict';

  // Global function to open the embed modal from anywhere
  window.openOmniEmbedModal = function () {
    let modal = document.getElementById('omni-embed-modal');
    if (!modal) {
      modal = createModalDOM();
    }
    if (modal) {
      updateEmbedCode(modal);
      modal.classList.add('is-open', 'active');
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  };
  window.closeOmniEmbedModal = function () {
    const modal = document.getElementById('omni-embed-modal');
    if (modal) {
      modal.classList.remove('is-open', 'active');
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  };
  window.openEmbedModal = window.openOmniEmbedModal;

  function getCleanUrls() {
    const rawPath = window.location.pathname.replace(/^\/embed\//, '').replace(/\/$/, '').replace(/^\//, '');
    const canonicalLink = document.querySelector('link[rel="canonical"]');
    const canonicalUrl = canonicalLink ? canonicalLink.href : ('https://omnioperand.com/' + (rawPath ? rawPath + '/' : ''));
    const embedUrl = 'https://omnioperand.com/embed/' + (rawPath ? rawPath + '/' : '');
    const toolTitle = document.querySelector('h1')?.textContent?.trim() || document.title.split('—')[0].split('|')[0].trim() || 'Calculator';
    return { canonicalUrl, embedUrl, toolTitle };
  }

  function getIframeSnippet(embedUrl, canonicalUrl, toolTitle) {
    return `<iframe src="${embedUrl}" width="100%" height="720" frameborder="0" style="border:1px solid #1e293b;border-radius:12px;width:100%;max-width:100%;box-shadow:0 8px 30px rgba(0,0,0,0.3);"></iframe>\n<p style="font-size:12px;color:#64748b;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin-top:6px;text-align:right;">Calculator powered by <a href="${canonicalUrl}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;font-weight:600;">OmniOperand ${toolTitle}</a></p>`;
  }

  function getBacklinkSnippet(canonicalUrl, toolTitle) {
    return `<a href="${canonicalUrl}" target="_blank" rel="noopener" style="font-family:sans-serif;color:#0284c7;font-weight:600;text-decoration:none;">Interactive ${toolTitle} by OmniOperand</a>`;
  }

  function updateEmbedCode(modal) {
    const { canonicalUrl, embedUrl, toolTitle } = getCleanUrls();
    const textarea = modal.querySelector('#omni-embed-code-textarea');
    const activeTab = modal.querySelector('.omni-tab-active');
    const isIframe = !activeTab || activeTab.id === 'tab-embed-iframe';
    if (textarea) {
      textarea.value = isIframe ? getIframeSnippet(embedUrl, canonicalUrl, toolTitle) : getBacklinkSnippet(canonicalUrl, toolTitle);
    }
  }

  function createModalDOM() {
    let existing = document.getElementById('omni-embed-modal');
    if (existing) return existing;

    const { canonicalUrl, embedUrl, toolTitle } = getCleanUrls();
    const iframeCode = getIframeSnippet(embedUrl, canonicalUrl, toolTitle);

    const modalHtml = `
      <div id="omni-embed-modal" class="omni-modal-overlay" style="display:none; position:fixed; inset:0; width:100%; height:100%; background:rgba(3,7,18,0.85); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); z-index:99999; align-items:center; justify-content:center; padding:1rem; box-sizing:border-box;">
        <div class="omni-modal-card" style="background:#101726; border:1px solid rgba(255,255,255,0.12); border-radius:16px; width:100%; max-width:620px; padding:1.75rem; box-shadow:0 25px 50px -12px rgba(0,0,0,0.8), 0 0 30px rgba(6,182,212,0.15); color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-sizing:border-box;">
          
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:11px; font-weight:700; padding:3px 8px; border-radius:6px; text-transform:uppercase; letter-spacing:0.05em;">Widget Exporter</span>
              <h3 style="margin:0; font-size:1.25rem; font-weight:700; color:#f8fafc;">Embed This Calculator</h3>
            </div>
            <button type="button" id="omni-close-embed" style="background:rgba(255,255,255,0.06); border:none; color:#94a3b8; width:32px; height:32px; border-radius:8px; font-size:22px; cursor:pointer; display:flex; align-items:center; justify-content:center; line-height:1; transition:all 0.15s ease;" aria-label="Close embed modal">&times;</button>
          </div>

          <p style="font-size:0.875rem; color:#94a3b8; margin:0 0 16px; line-height:1.5;">
            Embed this high-precision mathematical solver on your blog, publication, or web application. Completely free, mobile-responsive, and automatically includes verified backlink attribution.
          </p>

          <div style="display:flex; gap:8px; margin-bottom:12px;">
            <button type="button" id="tab-embed-iframe" class="omni-tab-active" style="background:#0284c7; color:#fff; border:none; border-radius:6px; padding:7px 14px; font-size:0.825rem; font-weight:600; cursor:pointer; transition:all 0.15s;">Responsive iFrame</button>
            <button type="button" id="tab-embed-backlink" style="background:rgba(255,255,255,0.06); color:#cbd5e1; border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:7px 14px; font-size:0.825rem; font-weight:500; cursor:pointer; transition:all 0.15s;">HTML Backlink</button>
          </div>

          <div style="margin-bottom:16px;">
            <textarea id="omni-embed-code-textarea" readonly rows="5" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; font-family:Consolas, 'JetBrains Mono', monospace; font-size:0.8rem; color:#7dd3fc; resize:none; line-height:1.45;">${iframeCode.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-top:6px; border-top:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:0.775rem; color:#64748b;">
              ✓ HTTPS encrypted • Live bidirectional calculation • Auto-height
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

    const modal = document.getElementById('omni-embed-modal');
    const closeBtn = document.getElementById('omni-close-embed');
    const copyBtn = document.getElementById('omni-copy-embed-btn');
    const copyText = document.getElementById('omni-copy-btn-text');
    const textarea = document.getElementById('omni-embed-code-textarea');
    const tabIframe = document.getElementById('tab-embed-iframe');
    const tabBacklink = document.getElementById('tab-embed-backlink');

    if (tabIframe && tabBacklink && textarea) {
      tabIframe.addEventListener('click', () => {
        const u = getCleanUrls();
        textarea.value = getIframeSnippet(u.embedUrl, u.canonicalUrl, u.toolTitle);
        tabIframe.className = 'omni-tab-active';
        tabBacklink.className = '';
        tabIframe.style.background = '#0284c7';
        tabIframe.style.color = '#fff';
        tabBacklink.style.background = 'rgba(255,255,255,0.06)';
        tabBacklink.style.color = '#cbd5e1';
      });

      tabBacklink.addEventListener('click', () => {
        const u = getCleanUrls();
        textarea.value = getBacklinkSnippet(u.canonicalUrl, u.toolTitle);
        tabBacklink.className = 'omni-tab-active';
        tabIframe.className = '';
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
        }).catch(() => {
          document.execCommand('copy');
          copyText.textContent = '✓ Copied to Clipboard!';
          copyBtn.style.background = '#10b981';
          setTimeout(() => {
            copyText.textContent = 'Copy Embed Code';
            copyBtn.style.background = '#0284c7';
          }, 2500);
        });
      });
    }

    return modal;
  }

  function initEmbedModal() {
    if (window.__omniEmbedInitialized) return;
    window.__omniEmbedInitialized = true;

    // If running inside an iframe embed already or on /embed/, don't inject button
    if (window.location.pathname.startsWith('/embed/') || window.parent !== window || window.location.search.includes('embed=true')) {
      return;
    }

    // Check if this page is a calculator / solver page
    const isCalcPage = !!document.querySelector('.calculator-grid, .solver-container, .calculator-hud, .solver-panel, .param-card-grid, .hud-panel, .calc-container, [data-calculator], .params-grid, .calculator-actions-toolbar');
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

    // Pre-create the modal DOM
    createModalDOM();

    // Wire up global click listener on document for maximum reliability
    document.addEventListener('click', function (e) {
      const trigger = e.target.closest('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
      if (trigger) {
        e.preventDefault();
        e.stopPropagation();
        window.openOmniEmbedModal();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        const modal = document.getElementById('omni-embed-modal');
        if (modal && modal.style.display === 'flex') {
          modal.style.display = 'none';
        }
      }
    });
  }

  window.initOmniEmbedModal = initEmbedModal;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmbedModal);
  } else {
    initEmbedModal();
  }
})();
