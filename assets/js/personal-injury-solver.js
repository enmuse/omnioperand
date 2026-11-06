/**
 * assets/js/personal-injury-solver.js
 * OmniOperand Personal Injury Settlement Value & Multiplier Client Engine
 */

(function () {
  'use strict';

  function getNum(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback !== undefined ? fallback : 0;
    const clean = String(el.value).replace(/[^0-9.-]+/g, '');
    const val = parseFloat(clean);
    return isNaN(val) ? (fallback !== undefined ? fallback : 0) : val;
  }

  function setMetric(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
  }

  function formatUSD(val) {
    return '$' + Math.round(val).toLocaleString('en-US');
  }

  function formatDec(val, dec) {
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  function solvePI() {
    const pastMed = getNum('param-past_medical', 35000);
    const futureMed = getNum('param-future_medical', 15000);
    const lostWages = getNum('param-lost_wages', 10000);
    const futureWages = getNum('param-future_wages', 0);
    const severityTier = document.getElementById('param-severity_tier')?.value || 'moderate';
    const customMultiplier = getNum('param-custom_multiplier', 0);
    const faultPct = getNum('param-fault_pct', 0) / 100;
    const feePct = getNum('param-attorney_fee_pct', 33.333) / 100;
    const liens = getNum('param-medical_liens', 12000);

    const totalSpecials = pastMed + futureMed + lostWages + futureWages;

    let defaultMult = 2.0;
    if (severityTier === 'minor') defaultMult = 1.75;
    else if (severityTier === 'moderate') defaultMult = 2.75;
    else if (severityTier === 'severe') defaultMult = 4.0;
    else if (severityTier === 'catastrophic') defaultMult = 5.0;

    const multiplier = customMultiplier > 0 ? customMultiplier : defaultMult;
    const painAndSuffering = totalSpecials * multiplier;
    const grossSettlement = totalSpecials + painAndSuffering;

    const faultReduction = grossSettlement * faultPct;
    const adjustedGross = Math.max(0, grossSettlement - faultReduction);
    const attorneyFee = adjustedGross * feePct;
    const liensPaid = Math.min(liens, Math.max(0, adjustedGross - attorneyFee));
    const netClientRecovery = Math.max(0, adjustedGross - attorneyFee - liensPaid);
    const takeHomePct = grossSettlement > 0 ? (netClientRecovery / grossSettlement) * 100 : 0;

    setMetric('res-net_client_recovery', formatUSD(netClientRecovery));
    setMetric('res-gross_settlement', formatUSD(grossSettlement));
    setMetric('res-pain_and_suffering', formatUSD(painAndSuffering));
    setMetric('res-attorney_fee', formatUSD(attorneyFee));
    setMetric('res-economic_specials', formatUSD(totalSpecials));
    setMetric('res-multiplier_display', formatDec(multiplier, 2) + 'x Multiplier');
    setMetric('res-take_home_pct', formatDec(takeHomePct, 1) + '% Take-Home');

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Personal Injury Settlement Valuation Verification]
Special Economic Damages: $${totalSpecials.toLocaleString()}
  • Past/Future Medical Expenses: $${(pastMed + futureMed).toLocaleString()}
  • Past/Future Lost Income: $${(lostWages + futureWages).toLocaleString()}
General Damages (Pain & Suffering): $${Math.round(painAndSuffering).toLocaleString()} (${multiplier.toFixed(2)}x ${severityTier} severity multiplier)
Gross Pre-Fault Case Valuation: $${Math.round(grossSettlement).toLocaleString()}
Comparative Fault Adjustment (${(faultPct * 100).toFixed(0)}%): -$${Math.round(faultReduction).toLocaleString()}
Attorney Contingency Fee (${(feePct * 100).toFixed(1)}%): -$${Math.round(attorneyFee).toLocaleString()}
Medical Liens & Health Insurance Subrogation: -$${Math.round(liensPaid).toLocaleString()}
Net Client In-Pocket Recovery: $${Math.round(netClientRecovery).toLocaleString()} (${takeHomePct.toFixed(1)}% of Gross)`;
    }
  }

  function copySummary() {
    const recovery = document.getElementById('res-net_client_recovery')?.innerText || 'N/A';
    const gross = document.getElementById('res-gross_settlement')?.innerText || 'N/A';
    const mult = document.getElementById('res-multiplier_display')?.innerText || 'N/A';

    const text = `OmniOperand Personal Injury Settlement Analysis:\n• Gross Settlement Value: ${gross}\n• Severity Multiplier: ${mult}\n• Net In-Pocket Recovery: ${recovery}\nSource: https://omnioperand.com/calculators/personal-injury-settlement/`;

    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('btn-copy-summary');
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = '<span>✓ Summary Copied!</span>';
        setTimeout(() => { btn.innerHTML = orig; }, 2000);
      }
    });
  }

  function init() {
    const calc = document.getElementById('personal-injury-calculator');
    if (calc) {
      calc.querySelectorAll('input, select').forEach(el => {
        el.addEventListener('input', solvePI);
        el.addEventListener('change', solvePI);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solvePI();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

