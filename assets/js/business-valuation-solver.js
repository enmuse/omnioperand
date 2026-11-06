/**
 * assets/js/business-valuation-solver.js
 * OmniOperand Business Valuation & SDE / EBITDA Multiple Client Engine
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

  function solveValuation() {
    const revenue = getNum('param-gross_revenue', 1500000);
    const profit = getNum('param-net_profit', 180000);
    const ownerComp = getNum('param-owner_compensation', 140000);
    const perks = getNum('param-discretionary_perks', 25000);
    const dep = getNum('param-depreciation', 35000);
    const interest = getNum('param-interest_expense', 10000);
    const oneTime = getNum('param-one_time_expenses', 0);
    const multiple = Math.max(1.0, getNum('param-target_multiple', 3.5));
    const gmSalary = getNum('param-replacement_gm_salary', 120000);

    const totalAddbacks = ownerComp + perks + dep + interest + oneTime;
    const sde = profit + totalAddbacks;
    const adjustedEbitda = Math.max(0, sde - gmSalary);

    const medianVal = sde * multiple;
    const lowVal = sde * Math.max(1.0, multiple - 0.5);
    const highVal = sde * (multiple + 0.5);

    const cashClosing = medianVal * 0.70;
    const sellerNote = medianVal * 0.15;
    const earnout = medianVal * 0.15;

    const r = 0.08 / 12;
    const n = 60;
    let noteMonthly = 0;
    if (sellerNote > 0) {
      const f = Math.pow(1 + r, n);
      noteMonthly = sellerNote * ((r * f) / (f - 1));
    }

    setMetric('res-median_valuation', formatUSD(medianVal));
    setMetric('res-sde', formatUSD(sde));
    setMetric('res-adjusted_ebitda', formatUSD(adjustedEbitda));
    setMetric('res-valuation_range', `${formatUSD(lowVal)} – ${formatUSD(highVal)}`);
    setMetric('res-total_addbacks', formatUSD(totalAddbacks));
    setMetric('res-cash_closing', formatUSD(cashClosing) + ' (70%)');
    setMetric('res-seller_note', formatUSD(sellerNote) + ' (15%)');
    setMetric('res-earnout', formatUSD(earnout) + ' (15%)');

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Business Valuation Underwriting Verification]
Annual Gross Revenue: $${revenue.toLocaleString()}
Reported Net Profit: $${profit.toLocaleString()}
Discretionary Recast Add-Backs: $${Math.round(totalAddbacks).toLocaleString()}
  • Owner Compensation & Draw: $${ownerComp.toLocaleString()}
  • Personal Perks / Vehicles: $${perks.toLocaleString()}
  • Depreciation ($${dep.toLocaleString()}) + Interest ($${interest.toLocaleString()}) + One-Time ($${oneTime.toLocaleString()})
Seller's Discretionary Earnings (SDE): $${Math.round(sde).toLocaleString()}
Adjusted EBITDA (Less $${gmSalary.toLocaleString()} GM Salary): $${Math.round(adjustedEbitda).toLocaleString()}
Enterprise Valuation @ ${multiple.toFixed(2)}x Multiple: $${Math.round(medianVal).toLocaleString()} (Range: $${Math.round(lowVal).toLocaleString()} – $${Math.round(highVal).toLocaleString()})
Standard Deal Structure:
  • Cash at Closing (70%): $${Math.round(cashClosing).toLocaleString()}
  • 5-Year Seller Note (15% @ 8% APR): $${Math.round(sellerNote).toLocaleString()} ($${noteMonthly.toFixed(2)}/mo)
  • Contingent Earnout (15%): $${Math.round(earnout).toLocaleString()}`;
    }
  }

  function copySummary() {
    const val = document.getElementById('res-median_valuation')?.innerText || 'N/A';
    const sde = document.getElementById('res-sde')?.innerText || 'N/A';
    const range = document.getElementById('res-valuation_range')?.innerText || 'N/A';
    const rev = document.getElementById('param-gross_revenue')?.value || '0';

    const text = `OmniOperand Business Valuation Analysis:\n• Annual Revenue: $${Number(rev).toLocaleString()}\n• Recast SDE: ${sde}\n• Estimated Valuation: ${val}\n• Market Range: ${range}\nSource: https://omnioperand.com/calculators/business-valuation-multiple/`;

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
    const calc = document.getElementById('business-valuation-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveValuation);
        el.addEventListener('change', solveValuation);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveValuation();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

