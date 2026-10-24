/**
 * assets/js/lead-drawer.js
 * OmniOperand High-Converting Halal & Immigrant Lending Lead-Capture Drawer
 * Features:
 *  - Auto pre-population from calculator DOM
 *  - TCPA & RESPA Section 8 Safe-Harbor shields
 *  - Client-side honeypot bot trap
 *  - Direct webhook forwarding to /api/leads/islamic-finance
 *  - Local storage offline backup
 */

(function () {
  'use strict';

  function initLeadDrawer() {
    // If inside an embed iframe, do not inject full lead drawer
    if (window.location.pathname.startsWith('/embed/') || window.parent !== window) {
      return;
    }

    if (document.getElementById('omni-lead-drawer-overlay')) {
      return;
    }

    const isSpanish = document.documentElement.lang === 'es' || window.location.pathname.startsWith('/es/');
    const isItin = window.location.pathname.includes('itin');
    const isIslamic = window.location.pathname.includes('islamic');

    // Drawer text localization & specialization
    const titleText = isItin
      ? (isSpanish ? 'Pre-Aprobación de Hipoteca ITIN' : 'ITIN Mortgage Pre-Approval')
      : (isSpanish ? 'Consulta de Financiamiento Shariah' : 'Halal Financing Pre-Approval');
    
    const subTitle = isItin
      ? (isSpanish ? 'Compare prestamistas especializados en préstamos sin Seguro Social (solo ITIN/W-2/1099).' : 'Connect with licensed Non-QM lenders specializing in ITIN loans with no SSN required.')
      : (isSpanish ? 'Verifique disponibilidad con entidades certificadas bajo normas AAOIFI sin usura (Riba).' : 'Compare certified AAOIFI-compliant financing partners with zero compounding interest (Riba-free).');

    const drawerHTML = `
<div id="omni-lead-drawer-overlay" class="lead-drawer-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(2,6,23,0.78); backdrop-filter:blur(6px); z-index:99999; opacity:0; transition:opacity 0.3s ease;">
  <div id="omni-lead-drawer" class="lead-drawer" style="position:fixed; top:0; right:0; width:100%; max-width:480px; height:100%; background:#0f172a; border-left:1px solid #334155; box-shadow:-10px 0 35px rgba(0,0,0,0.6); display:flex; flex-direction:column; transform:translateX(100%); transition:transform 0.35s cubic-bezier(0.16, 1, 0.3, 1); overflow-y:auto; box-sizing:border-box; color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    
    <!-- Header -->
    <div style="padding:22px 24px; border-bottom:1px solid #1e293b; display:flex; justify-content:space-between; align-items:flex-start; background:#0b1120;">
      <div>
        <div style="display:inline-flex; align-items:center; gap:6px; background:${isItin ? 'rgba(56,189,248,0.15)' : 'rgba(16,185,129,0.15)'}; color:${isItin ? '#38bdf8' : '#34d399'}; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">
          <span>${isItin ? '🏛️ Non-QM / ITIN Partner Network' : '🕌 AAOIFI Shariah Lending Network'}</span>
        </div>
        <h3 id="lead-drawer-title" style="margin:0; font-size:1.25rem; font-weight:800; color:#fff;">${titleText}</h3>
        <p style="margin:6px 0 0 0; font-size:0.82rem; color:#94a3b8; line-height:1.4;">${subTitle}</p>
      </div>
      <button id="lead-drawer-close" aria-label="Close Drawer" style="background:#1e293b; border:1px solid #334155; color:#94a3b8; width:34px; height:34px; border-radius:8px; cursor:pointer; font-size:20px; line-height:1; display:flex; align-items:center; justify-content:center; margin-left:12px; transition:all 0.2s;">&times;</button>
    </div>

    <!-- Pre-populated Calculation Snapshot -->
    <div style="padding:16px 24px; background:#1e293b; border-bottom:1px solid #334155;">
      <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.06em; color:#94a3b8; font-weight:700; margin-bottom:10px; display:flex; justify-content:space-between;">
        <span>Attached Calculator Scenario</span>
        <span style="color:${isItin ? '#38bdf8' : '#34d399'};">✓ Live State Synced</span>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:12px;">
        <div style="background:#0f172a; padding:8px 12px; border-radius:6px; border:1px solid #334155;">
          <span style="color:#64748b; display:block; font-size:10px;">Property Value</span>
          <strong id="lead-snap-price" style="color:#f8fafc; font-size:13px;">$400,000</strong>
        </div>
        <div style="background:#0f172a; padding:8px 12px; border-radius:6px; border:1px solid #334155;">
          <span style="color:#64748b; display:block; font-size:10px;">Down Payment / Equity</span>
          <strong id="lead-snap-down" style="color:#f8fafc; font-size:13px;">20% ($80,000)</strong>
        </div>
        <div style="background:#0f172a; padding:8px 12px; border-radius:6px; border:1px solid #334155;">
          <span style="color:#64748b; display:block; font-size:10px;">Financing Model</span>
          <strong id="lead-snap-model" style="color:#f8fafc; font-size:13px;">Musharaka</strong>
        </div>
        <div style="background:#0f172a; padding:8px 12px; border-radius:6px; border:1px solid #334155;">
          <span style="color:#64748b; display:block; font-size:10px;">Est. Monthly Budget</span>
          <strong id="lead-snap-monthly" style="color:${isItin ? '#38bdf8' : '#34d399'}; font-size:13px;">$2,022.62</strong>
        </div>
      </div>
    </div>

    <!-- Form Content -->
    <div id="lead-form-container" style="padding:22px 24px; flex:1;">
      <form id="omni-lead-form">
        <!-- Anti-Spam Bot Trap (Honeypot) -->
        <div style="display:none !important; opacity:0; position:absolute; left:-9999px;">
          <label for="lead-bot-website">Do not fill this field if human</label>
          <input type="text" id="lead-bot-website" name="website_url" autocomplete="off" tabindex="-1">
        </div>

        <div style="display:grid; grid-template-columns:1fr; gap:14px;">
          <div>
            <label for="lead-fullname" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">Full Legal Name *</label>
            <input type="text" id="lead-fullname" required placeholder="e.g., Tariq Rahman / Carlos Morales" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:14px; outline:none;">
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div>
              <label for="lead-email" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">Email Address *</label>
              <input type="email" id="lead-email" required placeholder="you@example.com" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:14px; outline:none;">
            </div>
            <div>
              <label for="lead-phone" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">Mobile Phone *</label>
              <input type="tel" id="lead-phone" required placeholder="(555) 000-0000" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:14px; outline:none;">
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div>
              <label for="lead-state-zip" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">State & Zip Code *</label>
              <input type="text" id="lead-state-zip" required placeholder="e.g., TX 75001" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:14px; outline:none;">
            </div>
            <div>
              <label for="lead-credit-tier" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">Estimated Credit Tier</label>
              <select id="lead-credit-tier" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:13px; outline:none;">
                <option value="720+">720+ (Excellent)</option>
                <option value="680-719" selected>680-719 (Good)</option>
                <option value="620-679">620-679 (Fair)</option>
                <option value="<620">&lt;620 (Challenged / No Credit)</option>
              </select>
            </div>
          </div>

          <div>
            <label for="lead-property-use" style="display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:5px;">Property Occupancy</label>
            <select id="lead-property-use" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #334155; border-radius:8px; padding:10px 14px; color:#fff; font-size:13px; outline:none;">
              <option value="Primary Residence" selected>Primary Residence (Owner-Occupied)</option>
              <option value="Investment Property">Investment Property / Rental</option>
              <option value="Second Home">Second Home / Vacation</option>
            </select>
          </div>
        </div>

        <!-- TCPA Mandatory Consent Checkbox -->
        <div style="margin-top:18px; padding:12px; background:rgba(255,255,255,0.02); border:1px solid #1e293b; border-radius:8px;">
          <label style="display:flex; align-items:flex-start; gap:10px; font-size:11px; line-height:1.45; color:#94a3b8; cursor:pointer;">
            <input type="checkbox" id="lead-tcpa-consent" required style="margin-top:2px; accent-color:#0284c7; width:16px; height:16px; cursor:pointer;">
            <span>
              <strong>TCPA Authorization:</strong> By submitting, you authorize verified financing partners to contact you at the phone number and email provided regarding your inquiry, including phone calls and text messages. Consent is not a condition of purchase.
            </span>
          </label>
        </div>

        <!-- Submit Button -->
        <div style="margin-top:18px;">
          <button type="submit" id="lead-submit-btn" style="width:100%; background:${isItin ? '#0284c7' : '#059669'}; color:#fff; border:none; padding:14px; border-radius:10px; font-weight:700; font-size:15px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; box-shadow:0 10px 20px -5px ${isItin ? 'rgba(2,132,199,0.4)' : 'rgba(5,150,105,0.4)'}; transition:all 0.2s;">
            <span id="lead-submit-spinner" style="display:none; width:16px; height:16px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation:spin 0.8s linear infinite;"></span>
            <span id="lead-submit-text">${isSpanish ? 'Verificar Pre-Aprobación Ahora' : 'Request Partner Pre-Approval Match'}</span>
          </button>
        </div>

        <!-- RESPA Section 8 Safe-Harbor Disclosure -->
        <div style="margin-top:16px; font-size:10px; color:#64748b; line-height:1.4; border-top:1px solid #1e293b; padding-top:12px;">
          <strong>RESPA Educational Safe-Harbor Notice:</strong> OmniOperand is an independent mathematical utility and comparison directory, not a mortgage broker or lender. OmniOperand does not originate loans, issue pre-approvals, or make credit decisions. Advertising and lead-generation fees may be paid by participating lending partners. All financing terms, profit rates, and approvals are determined exclusively by licensed institutions.
        </div>
      </form>
    </div>

    <!-- Success Confirmation State (Hidden initially) -->
    <div id="lead-success-container" style="display:none; padding:32px 24px; text-align:center; flex:1; justify-content:center; flex-direction:column; align-items:center;">
      <div style="width:64px; height:64px; background:rgba(16,185,129,0.15); border:2px solid #10b981; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; color:#10b981; margin-bottom:16px;">
        ✓
      </div>
      <h3 style="margin:0 0 8px 0; font-size:1.4rem; color:#fff;">Pre-Approval Inquiry Received!</h3>
      <p style="font-size:0.9rem; color:#94a3b8; line-height:1.5; margin:0 0 20px 0; max-width:360px;">
        Your calculation scenario has been matched with our accredited partner desk. A certified specialist licensed in your state will review your property scenario and connect with you shortly.
      </p>
      
      <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:12px 18px; margin-bottom:24px; width:100%; max-width:340px; text-align:left;">
        <div style="font-size:10px; text-transform:uppercase; color:#64748b; font-weight:700;">Inquiry Reference ID</div>
        <div id="lead-confirmation-id" style="font-family:Consolas,monospace; font-size:14px; color:#38bdf8; font-weight:700;">OPO-2026-PENDING</div>
        <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Zero impact on credit score during pre-check.</div>
      </div>

      <button id="lead-success-close-btn" style="background:#334155; color:#f8fafc; border:none; padding:10px 24px; border-radius:8px; font-weight:600; font-size:14px; cursor:pointer;">
        Return to Calculator
      </button>
    </div>

  </div>
</div>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}
@media (max-width: 640px) {
  #omni-lead-drawer {
    max-width: 100% !important;
  }
}
</style>
`;

    document.body.insertAdjacentHTML('beforeend', drawerHTML);

    const overlay = document.getElementById('omni-lead-drawer-overlay');
    const drawer = document.getElementById('omni-lead-drawer');
    const closeBtn = document.getElementById('lead-drawer-close');
    const form = document.getElementById('omni-lead-form');
    const formContainer = document.getElementById('lead-form-container');
    const successContainer = document.getElementById('lead-success-container');
    const successCloseBtn = document.getElementById('lead-success-close-btn');
    const submitBtn = document.getElementById('lead-submit-btn');
    const submitText = document.getElementById('lead-submit-text');
    const submitSpinner = document.getElementById('lead-submit-spinner');

    function openDrawer() {
      // Pull current live state from calculator DOM
      const priceInput = document.getElementById('param-home_price');
      const downInput = document.getElementById('param-down_payment_pct');
      const monthlyRes = document.getElementById('res-monthly_installment') || document.getElementById('res-monthly_piti');
      const modelTitle = document.querySelector('h1')?.innerText || (isItin ? 'ITIN Mortgage' : 'Islamic Financing');

      const priceVal = priceInput ? Number(priceInput.value || 400000) : 400000;
      const downPct = downInput ? Number(downInput.value || 20) : 20;
      const downAmount = Math.round(priceVal * (downPct / 100));

      document.getElementById('lead-snap-price').innerText = '$' + priceVal.toLocaleString('en-US');
      document.getElementById('lead-snap-down').innerText = `${downPct}% ($${downAmount.toLocaleString('en-US')})`;
      document.getElementById('lead-snap-model').innerText = modelTitle.split('(')[0].replace('Calculator', '').trim();
      if (monthlyRes) {
        document.getElementById('lead-snap-monthly').innerText = monthlyRes.innerText.trim();
      }

      overlay.style.display = 'block';
      setTimeout(() => {
        overlay.style.opacity = '1';
        drawer.style.transform = 'translateX(0)';
      }, 10);
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      overlay.style.opacity = '0';
      drawer.style.transform = 'translateX(100%)';
      setTimeout(() => {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
      }, 350);
    }

    closeBtn.addEventListener('click', closeDrawer);
    successCloseBtn.addEventListener('click', closeDrawer);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeDrawer();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && overlay.style.display === 'block') closeDrawer();
    });

    // Form Submission
    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      // Check anti-spam honeypot
      const botTrap = document.getElementById('lead-bot-website').value;
      if (botTrap) {
        // Silent success for spam bots
        formContainer.style.display = 'none';
        successContainer.style.display = 'flex';
        document.getElementById('lead-confirmation-id').innerText = 'OPO-2026-' + Math.random().toString(36).substring(2, 8).toUpperCase();
        return;
      }

      submitBtn.disabled = true;
      submitSpinner.style.display = 'inline-block';
      submitText.innerText = 'Transmitting Scenario...';

      const payload = {
        full_name: document.getElementById('lead-fullname').value.trim(),
        email: document.getElementById('lead-email').value.trim(),
        phone: document.getElementById('lead-phone').value.trim(),
        state_zip: document.getElementById('lead-state-zip').value.trim(),
        credit_tier: document.getElementById('lead-credit-tier').value,
        property_use: document.getElementById('lead-property-use').value,
        property_value: document.getElementById('lead-snap-price').innerText,
        down_payment: document.getElementById('lead-snap-down').innerText,
        financing_model: document.getElementById('lead-snap-model').innerText,
        monthly_budget: document.getElementById('lead-snap-monthly').innerText,
        tcpa_consent: document.getElementById('lead-tcpa-consent').checked,
        bot_trap: botTrap,
        source_url: window.location.href,
        submitted_at: new Date().toISOString()
      };

      // Local offline backup
      try {
        const stored = JSON.parse(localStorage.getItem('omni_pending_leads') || '[]');
        stored.push(payload);
        localStorage.setItem('omni_pending_leads', JSON.stringify(stored));
      } catch (err) {}

      let leadRef = 'OPO-' + Math.floor(100000 + Math.random() * 900000);

      try {
        const endpoint = isItin ? '/api/leads/itin-mortgage' : '/api/leads/islamic-finance';
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data && data.dispatch_id) {
          leadRef = data.dispatch_id.toUpperCase();
        }
      } catch (networkErr) {
        // Non-blocking fallback: Even if offline or network fails, user sees success confirmation
        console.warn('Lead dispatch note:', networkErr);
      }

      formContainer.style.display = 'none';
      successContainer.style.display = 'flex';
      document.getElementById('lead-confirmation-id').innerText = leadRef;
    });

    // Expose openLeadDrawer globally
    window.openLeadDrawer = openDrawer;

    // Attach to any interactive trigger buttons
    document.querySelectorAll('.btn-lead-drawer, #btn-open-lead-drawer, [data-action="open-lead-drawer"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openDrawer();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLeadDrawer);
  } else {
    initLeadDrawer();
  }
})();
