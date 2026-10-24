/**
 * assets/js/embed-modal.js
 * OmniOperand Viral Embed Widget Modal & 1-Click Code Exporter
 * Injects the "Embed Tool" modal and copyable iframe snippets onto all calculator pages.
 */

(function () {
  'use strict';

  function initEmbedModal() {
    // If running inside an iframe embed already, don't show embed button
    if (window.location.pathname.startsWith('/embed/') || window.parent !== window) {
      return;
    }

    const cleanPath = window.location.pathname.replace(/^\/|\/$/g, '');
    const embedUrl = `https://omnioperand.com/embed/${cleanPath}/`;
    const canonicalUrl = `https://omnioperand.com/${cleanPath}/`;
    const toolTitle = document.querySelector('h1')?.innerText?.trim() || document.title.split('—')[0].split('|')[0].trim();

    // Create Embed Modal HTML
    const modalHTML = `
<div id="omni-embed-modal" class="omni-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.75); z-index:10000; align-items:center; justify-content:center; backdrop-filter:blur(4px);">
  <div class="omni-modal-card" style="background:#0f172a; border:1px solid #334155; border-radius:16px; width:90%; max-width:580px; padding:24px; box-shadow:0 25px 50px -12px rgba(0,0,0,0.5); color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:12px; font-weight:700; padding:4px 8px; border-radius:6px; text-transform:uppercase;">Widget</span>
        <h3 style="margin:0; font-size:1.15rem; font-weight:700;">Embed This Calculator</h3>
      </div>
      <button id="omni-close-embed" style="background:none; border:none; color:#94a3b8; font-size:24px; cursor:pointer; line-height:1;">&times;</button>
    </div>

    <p style="font-size:0.88rem; color:#94a3b8; margin:0 0 16px 0; line-height:1.5;">
      Copy and paste this HTML snippet into your WordPress, Ghost, Substack, React, or custom website. The widget is 100% free, responsive, and updates live.
    </p>

    <div style="margin-bottom:16px;">
      <label style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; color:#cbd5e1; font-weight:600; display:block; margin-bottom:6px;">HTML Embed Code</label>
      <div style="position:relative;">
        <textarea id="omni-embed-code-textarea" readonly rows="4" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; font-family:Consolas,monospace; font-size:0.8rem; color:#7dd3fc; resize:none;">&lt;iframe src="${embedUrl}" width="100%" height="520" frameborder="0" style="border: 1px solid #334155; border-radius: 12px; max-width: 100%;"&gt;&lt;/iframe&gt;
&lt;p style="font-size: 11px; color: #64748b; font-family: sans-serif; margin-top: 6px;"&gt;Calculator powered by &lt;a href="${canonicalUrl}" target="_blank" rel="noopener" style="color: #38bdf8; text-decoration: none;"&gt;OmniOperand ${toolTitle}&lt;/a&gt;&lt;/p&gt;</textarea>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
      <div style="font-size:0.8rem; color:#64748b;">
        Includes auto-resizing and HTTPS encryption
      </div>
      <button id="omni-copy-embed-btn" style="background:#0284c7; color:#fff; border:none; padding:10px 20px; border-radius:8px; font-weight:600; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; gap:6px; transition:background 0.2s;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        <span id="omni-copy-btn-text">Copy HTML Snippet</span>
      </button>
    </div>
  </div>
</div>
`;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const modal = document.getElementById('omni-embed-modal');
    const closeBtn = document.getElementById('omni-close-embed');
    const copyBtn = document.getElementById('omni-copy-embed-btn');
    const copyText = document.getElementById('omni-copy-btn-text');
    const textarea = document.getElementById('omni-embed-code-textarea');

    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.style.display = 'none';
    });

    copyBtn.addEventListener('click', () => {
      textarea.select();
      navigator.clipboard.writeText(textarea.value).then(() => {
        copyText.innerText = 'Copied to Clipboard!';
        copyBtn.style.background = '#10b981';
        setTimeout(() => {
          copyText.innerText = 'Copy HTML Snippet';
          copyBtn.style.background = '#0284c7';
        }, 2500);
      });
    });

    // Wire up any buttons with class .btn-open-embed or id #btn-embed
    document.querySelectorAll('.btn-open-embed, #btn-embed, [data-action="embed"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.display = 'flex';
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmbedModal);
  } else {
    initEmbedModal();
  }
})();
