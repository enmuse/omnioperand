/**
 * embed/embed.js
 * OmniOperand Embeddable Calculator Widget Engine (Calculator-as-a-Service / CaaS)
 * Pure vanilla JavaScript, zero dependencies, isolated Shadow DOM.
 */

(function () {
  'use strict';

  // Partner Tier Registry (Known Pro/White-label Partners)
  const WHITE_LABEL_PARTNERS = new Set([
    'pro_partner',
    'pro_demo',
    'enterprise_client',
    'whitelabel_corp',
    'bank_partner_alpha'
  ]);

  function isWhiteLabel(partnerId) {
    if (!partnerId) return false;
    const clean = partnerId.toLowerCase().trim();
    if (WHITE_LABEL_PARTNERS.has(clean)) return true;
    if (clean.startsWith('pro_') || clean.startsWith('ent_') || clean.startsWith('wl_')) return true;
    return false;
  }

  // Pure Math Engines for Real-Time Offline Client Compute
  const ENGINES = {
    mortgage: function (inputs) {
      const P = parseFloat(inputs.principal || 400000);
      const rate = parseFloat(inputs.rate || 6.5);
      const years = parseFloat(inputs.term || 30);
      const r = (rate / 100) / 12;
      const n = years * 12;
      let monthly = 0;
      if (r === 0) monthly = P / n;
      else {
        const factor = Math.pow(1 + r, n);
        monthly = P * (r * factor) / (factor - 1);
      }
      const totalPaid = monthly * n;
      const totalInterest = totalPaid - P;
      return {
        metrics: [
          { label: "Monthly Payment (P&I)", value: "$" + monthly.toFixed(2), highlight: true },
          { label: "Total Interest Paid", value: "$" + Math.round(totalInterest).toLocaleString() },
          { label: "Total Financing Cost", value: "$" + Math.round(totalPaid).toLocaleString() }
        ],
        details: `30-year fixed loan of $${P.toLocaleString()} at ${rate}% APR requires $${monthly.toFixed(2)} monthly.`
      };
    },

    octagon: function (inputs) {
      const a = parseFloat(inputs.side || 10);
      const sqrt2 = Math.SQRT2;
      const area = 2 * (1 + sqrt2) * a * a;
      const perimeter = 8 * a;
      const span = a * (1 + sqrt2);
      const apothem = (a * (1 + sqrt2)) / 2;
      return {
        metrics: [
          { label: "Total Area", value: area.toFixed(2) + " sq units", highlight: true },
          { label: "Flat-to-Flat Span", value: span.toFixed(2) + " units" },
          { label: "Apothem (Inradius)", value: apothem.toFixed(2) + " units" },
          { label: "Perimeter", value: perimeter.toFixed(2) + " units" }
        ],
        details: `Closed form area: 2(1 + √2)a² ≈ ${(4.828427 * a * a).toFixed(2)}. Miter saw cut angle: 22.5°.`
      };
    },

    "compound-interest": function (inputs) {
      const P = parseFloat(inputs.principal || 10000);
      const rate = parseFloat(inputs.rate || 7.0);
      const years = parseFloat(inputs.years || 10);
      const monthly = parseFloat(inputs.monthly || 500);

      const r = rate / 100;
      const mRate = Math.pow(1 + r / 12, 1) - 1;
      let balance = P;
      let totalDeposited = P;
      const months = years * 12;
      for (let i = 0; i < months; i++) {
        balance = balance * (1 + mRate) + monthly;
        totalDeposited += monthly;
      }
      const interestEarned = balance - totalDeposited;
      return {
        metrics: [
          { label: "Future Valuation", value: "$" + Math.round(balance).toLocaleString(), highlight: true },
          { label: "Total Contributions", value: "$" + Math.round(totalDeposited).toLocaleString() },
          { label: "Compound Interest Earned", value: "$" + Math.round(interestEarned).toLocaleString() }
        ],
        details: `Initial $${P.toLocaleString()} with $${monthly}/mo grows to $${Math.round(balance).toLocaleString()} over ${years} years.`
      };
    },

    cagr: function (inputs) {
      const initial = parseFloat(inputs.initial || 10000);
      const finalVal = parseFloat(inputs.final || 25000);
      const years = parseFloat(inputs.years || 5);
      const cagr = Math.pow(finalVal / initial, 1 / years) - 1;
      const growthPct = ((finalVal - initial) / initial) * 100;
      return {
        metrics: [
          { label: "Annual Growth Rate (CAGR)", value: (cagr * 100).toFixed(2) + "%", highlight: true },
          { label: "Total Absolute Return", value: growthPct.toFixed(1) + "%" },
          { label: "Multiple on Invested Capital", value: (finalVal / initial).toFixed(2) + "x" }
        ],
        details: `Asset increased from $${initial.toLocaleString()} to $${finalVal.toLocaleString()} over ${years} years.`
      };
    },

    "concrete-volume": function (inputs) {
      const length = parseFloat(inputs.length || 20);
      const width = parseFloat(inputs.width || 10);
      const depth = parseFloat(inputs.depth || 4); // inches
      const cuFt = length * width * (depth / 12);
      const cuYards = cuFt / 27;
      const cuYardsBuffer = cuYards * 1.10;
      const bags80 = Math.ceil(cuFt / 0.60);
      return {
        metrics: [
          { label: "Volume (+10% Waste Buffer)", value: cuYardsBuffer.toFixed(2) + " cu yds", highlight: true },
          { label: "Exact Cubic Yards", value: cuYards.toFixed(2) + " cu yds" },
          { label: "80lb Premix Bags Needed", value: bags80 + " bags" }
        ],
        details: `${length}' × ${width}' slab at ${depth}" depth requires ${cuYardsBuffer.toFixed(2)} cubic yards or ${bags80} bags of 80lb concrete.`
      };
    }
  };

  // Shadow DOM Stylesheet
  function getWidgetStyles(theme, isWhiteLabelMode, customStyles) {
    const isDark = theme === 'dark' || (theme === 'auto' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);

    const primary = customStyles.primary || (isDark ? '#38bdf8' : '#0284c7');
    const accent = customStyles.accent || (isDark ? '#818cf8' : '#6366f1');
    const bg = customStyles.bg || (isDark ? '#0f172a' : '#ffffff');
    const surface = isDark ? '#1e293b' : '#f8fafc';
    const border = isDark ? '#334155' : '#e2e8f0';
    const text = isDark ? '#f8fafc' : '#0f172a';
    const textMuted = isDark ? '#94a3b8' : '#64748b';
    const font = customStyles.font || '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif';

    return `
      :host {
        display: block;
        width: 100%;
        max-width: 680px;
        margin: 0 auto;
        font-family: ${font};
        color: ${text};
        box-sizing: border-box;
      }
      *, *::before, *::after {
        box-sizing: border-box;
      }
      .omni-widget-card {
        background: ${bg};
        border: 1px solid ${border};
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, ${isDark ? '0.5' : '0.05'}), 0 8px 10px -6px rgba(0, 0, 0, ${isDark ? '0.5' : '0.03'});
      }
      .omni-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid ${border};
      }
      .omni-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
        color: ${text};
      }
      .omni-badge {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 8px;
        border-radius: 9999px;
        background: ${isDark ? 'rgba(56, 189, 248, 0.15)' : 'rgba(2, 132, 199, 0.1)'};
        color: ${primary};
      }
      .omni-form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
      }
      .omni-field {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .omni-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: ${textMuted};
      }
      .omni-input {
        background: ${surface};
        border: 1px solid ${border};
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 0.95rem;
        font-weight: 600;
        color: ${text};
        outline: none;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
      }
      .omni-input:focus {
        border-color: ${primary};
        box-shadow: 0 0 0 3px ${isDark ? 'rgba(56, 189, 248, 0.2)' : 'rgba(2, 132, 199, 0.15)'};
      }
      .omni-results-card {
        background: ${surface};
        border: 1px solid ${border};
        border-radius: 12px;
        padding: 18px;
        position: relative;
        overflow: hidden;
      }
      .omni-metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 16px;
        margin-bottom: 12px;
      }
      .omni-metric-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      .omni-metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: ${textMuted};
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }
      .omni-metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: ${text};
        font-feature-settings: "tnum" 1;
      }
      .omni-metric-value.highlight {
        color: ${primary};
      }
      .omni-details {
        font-size: 0.85rem;
        color: ${textMuted};
        line-height: 1.4;
        margin: 0;
        padding-top: 8px;
        border-top: 1px dashed ${border};
      }
      /* Lead Capture Gate Overlay */
      .omni-lead-gate {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 24px 16px;
        background: ${isDark ? 'rgba(15, 23, 42, 0.88)' : 'rgba(255, 255, 255, 0.92)'};
        backdrop-filter: blur(8px);
        border-radius: 12px;
        border: 1px dashed ${primary};
        margin-top: 12px;
      }
      .omni-gate-title {
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: ${text};
      }
      .omni-gate-desc {
        font-size: 0.82rem;
        color: ${textMuted};
        max-width: 380px;
        margin: 0 0 16px 0;
      }
      .omni-gate-form {
        display: flex;
        gap: 8px;
        width: 100%;
        max-width: 360px;
      }
      .omni-gate-input {
        flex: 1;
        padding: 9px 12px;
        border-radius: 8px;
        border: 1px solid ${border};
        background: ${surface};
        color: ${text};
        font-size: 0.88rem;
        outline: none;
      }
      .omni-gate-btn {
        background: ${primary};
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 0.88rem;
        font-weight: 600;
        cursor: pointer;
        transition: opacity 0.15s ease, transform 0.1s ease;
      }
      .omni-gate-btn:hover {
        opacity: 0.92;
        transform: translateY(-1px);
      }
      /* Footer & Attribution */
      .omni-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 16px;
        font-size: 0.75rem;
        color: ${textMuted};
      }
      .omni-powered-by {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: ${textMuted};
        text-decoration: none;
        font-weight: 500;
        transition: color 0.15s ease;
      }
      .omni-powered-by:hover {
        color: ${primary};
      }
      .omni-powered-by strong {
        color: ${primary};
        font-weight: 700;
      }
      .omni-badge-icon {
        width: 14px;
        height: 14px;
      }
    `;
  }

  // Calculator Form Templates
  const FORM_CONFIGS = {
    mortgage: {
      title: "Mortgage Amortization & Payment Calculator",
      badge: "Financial Engine",
      fields: [
        { id: "principal", label: "Loan Amount ($)", type: "number", default: 400000, step: 5000 },
        { id: "rate", label: "Interest Rate (%)", type: "number", default: 6.5, step: 0.125 },
        { id: "term", label: "Loan Term (Years)", type: "number", default: 30, step: 5 }
      ]
    },
    octagon: {
      title: "Regular Octagon Precision Solver",
      badge: "Exact Radical Geometry",
      fields: [
        { id: "side", label: "Side Length (a)", type: "number", default: 10, step: 1 }
      ]
    },
    "compound-interest": {
      title: "Compound Interest & APY Growth",
      badge: "Wealth Compounder",
      fields: [
        { id: "principal", label: "Initial Deposit ($)", type: "number", default: 10000, step: 1000 },
        { id: "rate", label: "Annual Rate (%)", type: "number", default: 7.0, step: 0.25 },
        { id: "years", label: "Timeline (Years)", type: "number", default: 10, step: 1 },
        { id: "monthly", label: "Monthly Deposit ($)", type: "number", default: 500, step: 50 }
      ]
    },
    cagr: {
      title: "CAGR & Annualized Growth Calculator",
      badge: "Actuarial Metric",
      fields: [
        { id: "initial", label: "Initial Value ($)", type: "number", default: 10000, step: 1000 },
        { id: "final", label: "Final Value ($)", type: "number", default: 25000, step: 1000 },
        { id: "years", label: "Duration (Years)", type: "number", default: 5, step: 1 }
      ]
    },
    "concrete-volume": {
      title: "Concrete Slab & Footing Volume Estimator",
      badge: "Structural Math",
      fields: [
        { id: "length", label: "Length (Feet)", type: "number", default: 20, step: 1 },
        { id: "width", label: "Width (Feet)", type: "number", default: 10, step: 1 },
        { id: "depth", label: "Thickness (Inches)", type: "number", default: 4, step: 0.5 }
      ]
    }
  };

  // Render Widget Instance Inside Shadow DOM
  function renderWidget(container) {
    const calcType = (container.getAttribute('data-calculator') || 'mortgage').toLowerCase();
    const partnerId = container.getAttribute('data-partner-id') || 'direct';
    const theme = container.getAttribute('data-theme') || 'auto';
    const requireLeadCapture = container.getAttribute('data-lead-capture') === 'true';

    const customStyles = {
      primary: container.getAttribute('data-primary-color'),
      accent: container.getAttribute('data-accent-color'),
      bg: container.getAttribute('data-bg-color'),
      font: container.getAttribute('data-font-family')
    };

    const isWhiteLabelPartner = isWhiteLabel(partnerId);
    const config = FORM_CONFIGS[calcType] || FORM_CONFIGS.mortgage;
    const engine = ENGINES[calcType] || ENGINES.mortgage;

    // Check if this partner/user has already unlocked results
    const unlockKey = `omni_unlocked_${calcType}_${partnerId}`;
    let isUnlocked = !requireLeadCapture || localStorage.getItem(unlockKey) === 'true';

    // Attach Shadow DOM
    const shadow = container.attachShadow({ mode: 'open' });

    // Build Styles
    const styleEl = document.createElement('style');
    styleEl.textContent = getWidgetStyles(theme, isWhiteLabelPartner, customStyles);
    shadow.appendChild(styleEl);

    // Build Card Element
    const cardEl = document.createElement('div');
    cardEl.className = 'omni-widget-card';

    // Header
    let headerHtml = `
      <div class="omni-header">
        <h3 class="omni-title">
          <span>${config.title}</span>
        </h3>
        <span class="omni-badge">${config.badge}</span>
      </div>
    `;

    // Input fields
    let formHtml = `<div class="omni-form-grid">`;
    for (const f of config.fields) {
      formHtml += `
        <div class="omni-field">
          <label class="omni-label" for="omni-${f.id}">${f.label}</label>
          <input 
            type="${f.type}" 
            class="omni-input" 
            id="omni-${f.id}" 
            data-param="${f.id}" 
            value="${f.default}" 
            step="${f.step || 1}" 
          />
        </div>
      `;
    }
    formHtml += `</div>`;

    // Results container
    const resultsContainerHtml = `
      <div class="omni-results-card" id="omni-results-box">
        <div class="omni-metrics-grid" id="omni-metrics-target"></div>
        <p class="omni-details" id="omni-details-target"></p>
        <div id="omni-lead-gate-container"></div>
      </div>
    `;

    // Attribution footer (suppressed on Pro/White-label)
    let footerHtml = '';
    if (!isWhiteLabelPartner) {
      const referralUrl = `https://omnioperand.com/?ref=embed-${encodeURIComponent(partnerId)}&calc=${encodeURIComponent(calcType)}`;
      footerHtml = `
        <div class="omni-footer">
          <span>Deterministic Edge Compute</span>
          <a href="${referralUrl}" target="_blank" rel="noopener" class="omni-powered-by" title="Powered by OmniOperand Computational Platform">
            <svg class="omni-badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
            <span>Powered by <strong>OmniOperand</strong></span>
          </a>
        </div>
      `;
    }

    cardEl.innerHTML = headerHtml + formHtml + resultsContainerHtml + footerHtml;
    shadow.appendChild(cardEl);

    // Update function
    function updateCalculations() {
      const inputs = {};
      const inputElements = shadow.querySelectorAll('.omni-input');
      inputElements.forEach(inp => {
        inputs[inp.getAttribute('data-param')] = parseFloat(inp.value) || 0;
      });

      const outcome = engine(inputs);
      const metricsTarget = shadow.getElementById('omni-metrics-target');
      const detailsTarget = shadow.getElementById('omni-details-target');
      const gateContainer = shadow.getElementById('omni-lead-gate-container');

      if (!metricsTarget || !detailsTarget) return;

      if (requireLeadCapture && !isUnlocked) {
        // Blur metrics or show teaser
        metricsTarget.innerHTML = outcome.metrics.map((m, idx) => `
          <div class="omni-metric-item">
            <span class="omni-metric-label">${m.label}</span>
            <span class="omni-metric-value ${m.highlight ? 'highlight' : ''}">${idx === 0 ? m.value : '••••••'}</span>
          </div>
        `).join('');

        detailsTarget.style.display = 'none';

        gateContainer.innerHTML = `
          <div class="omni-lead-gate">
            <h4 class="omni-gate-title">Unlock Full Breakdown & Analytical Schedule</h4>
            <p class="omni-gate-desc">Enter your email to reveal all calculations, amortization schedules, and radical proofs.</p>
            <form class="omni-gate-form" id="omni-gate-form">
              <input type="email" class="omni-gate-input" id="omni-gate-email" placeholder="name@company.com" required />
              <button type="submit" class="omni-gate-btn">Unlock Results</button>
            </form>
          </div>
        `;

        const gateForm = shadow.getElementById('omni-gate-form');
        if (gateForm) {
          gateForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const emailInput = shadow.getElementById('omni-gate-email');
            const email = emailInput ? emailInput.value.trim() : '';
            if (email && email.includes('@')) {
              isUnlocked = true;
              localStorage.setItem(unlockKey, 'true');

              // Asynchronous lead capture beacon back to OmniOperand API
              try {
                fetch('/api/v1/leads', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    email,
                    calculator: calcType,
                    partner_id: partnerId,
                    inputs,
                    timestamp: new Date().toISOString()
                  })
                }).catch(() => {});
              } catch (_) {}

              // Dispatch custom event for host site
              container.dispatchEvent(new CustomEvent('omni:lead-captured', {
                bubbles: true,
                composed: true,
                detail: { email, calculator: calcType, partner_id: partnerId, inputs }
              }));

              updateCalculations();
            }
          });
        }
      } else {
        // Full un-gated display
        metricsTarget.innerHTML = outcome.metrics.map(m => `
          <div class="omni-metric-item">
            <span class="omni-metric-label">${m.label}</span>
            <span class="omni-metric-value ${m.highlight ? 'highlight' : ''}">${m.value}</span>
          </div>
        `).join('');

        detailsTarget.style.display = 'block';
        detailsTarget.textContent = outcome.details;
        gateContainer.innerHTML = '';
      }
    }

    // Attach live change listeners
    const inputElements = shadow.querySelectorAll('.omni-input');
    inputElements.forEach(inp => {
      inp.addEventListener('input', updateCalculations);
      inp.addEventListener('change', updateCalculations);
    });

    // Initial calculation
    updateCalculations();
  }

  // Scan and Initialize All Widgets on DOM Ready
  function initAllWidgets() {
    const widgets = document.querySelectorAll('div[data-calculator]');
    widgets.forEach(w => {
      if (!w.hasAttribute('data-omni-initialized')) {
        w.setAttribute('data-omni-initialized', 'true');
        renderWidget(w);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAllWidgets);
  } else {
    initAllWidgets();
  }

  // Expose global for manual hydration
  window.OmniOperandWidget = {
    init: initAllWidgets,
    render: renderWidget
  };
})();
