/**
 * assets/js/cost-segregation-solver.js
 * OmniOperand Cost Segregation & Bonus Depreciation Client Engine
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

  function solveCostSeg() {
    const price = getNum('param-purchase_price', 2000000);
    const landPct = getNum('param-land_value_pct', 20) / 100;
    const propType = document.getElementById('param-property_type')?.value || 'commercial';
    const fivePct = getNum('param-five_year_pct', 15) / 100;
    const fifteenPct = getNum('param-fifteen_year_pct', 10) / 100;
    const bonusPct = getNum('param-bonus_depreciation_pct', 60) / 100;
    const taxRate = getNum('param-marginal_tax_rate', 37) / 100;

    const landValue = price * landPct;
    const depreciableBasis = Math.max(0, price - landValue);

    const fiveBasis = depreciableBasis * fivePct;
    const fifteenBasis = depreciableBasis * fifteenPct;
    const structuralBasis = Math.max(0, depreciableBasis - fiveBasis - fifteenBasis);

    const recoveryYears = propType === 'residential' ? 27.5 : 39.0;
    const straightLineYr1 = (depreciableBasis / recoveryYears) * (11.5 / 12);

    const fiveBonus = fiveBasis * bonusPct;
    const fiveStd = (fiveBasis - fiveBonus) * 0.20;

    const fifteenBonus = fifteenBasis * bonusPct;
    const fifteenStd = (fifteenBasis - fifteenBonus) * 0.05;

    const structuralYr1 = (structuralBasis / recoveryYears) * (11.5 / 12);

    const costSegYr1 = fiveBonus + fiveStd + fifteenBonus + fifteenStd + structuralYr1;
    const incrementalDeduction = Math.max(0, costSegYr1 - straightLineYr1);
    const immediateTaxSavings = incrementalDeduction * taxRate;
    const studyCost = 4500;
    const roiMultiple = immediateTaxSavings > 0 ? (immediateTaxSavings / studyCost) : 0;

    setMetric('res-year1_tax_savings', formatUSD(immediateTaxSavings));
    setMetric('res-cost_seg_deduction', formatUSD(costSegYr1));
    setMetric('res-incremental_deduction', formatUSD(incrementalDeduction));
    setMetric('res-straight_line_yr1', formatUSD(straightLineYr1));
    setMetric('res-depreciable_basis', formatUSD(depreciableBasis));
    setMetric('res-five_year_basis', formatUSD(fiveBasis));
    setMetric('res-fifteen_year_basis', formatUSD(fifteenBasis));
    setMetric('res-roi_multiple', formatDec(roiMultiple, 1) + 'x ROI');

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Cost Segregation Underwriting Verification]
Property Purchase Price: $${price.toLocaleString()} (Land: $${Math.round(landValue).toLocaleString()} | Depreciable Basis: $${Math.round(depreciableBasis).toLocaleString()})
Property Classification: ${propType === 'residential' ? 'Residential Rental (27.5-Yr)' : 'Commercial Nonresidential (39-Yr)'}
5-Year Personal Property Reclassified: $${Math.round(fiveBasis).toLocaleString()} (${(fivePct * 100).toFixed(0)}%)
15-Year Land Improvements Reclassified: $${Math.round(fifteenBasis).toLocaleString()} (${(fifteenPct * 100).toFixed(0)}%)
§168(k) Bonus Depreciation: ${(bonusPct * 100).toFixed(0)}%
Standard Straight-Line Year 1 Deduction: $${Math.round(straightLineYr1).toLocaleString()}
Cost Segregation Year 1 Deduction: $${Math.round(costSegYr1).toLocaleString()}
Incremental Year 1 Write-Off: +$${Math.round(incrementalDeduction).toLocaleString()}
Immediate Cash Tax Shield @ ${(taxRate * 100).toFixed(0)}%: $${Math.round(immediateTaxSavings).toLocaleString()} (Study ROI: ${roiMultiple.toFixed(1)}x)`;
    }
  }

  function copySummary() {
    const savings = document.getElementById('res-year1_tax_savings')?.innerText || 'N/A';
    const writeoff = document.getElementById('res-cost_seg_deduction')?.innerText || 'N/A';
    const roi = document.getElementById('res-roi_multiple')?.innerText || 'N/A';
    const price = document.getElementById('param-purchase_price')?.value || '0';

    const text = `OmniOperand Cost Segregation Analysis:\n• Property Price: $${Number(price).toLocaleString()}\n• Year 1 Depreciation: ${writeoff}\n• Immediate Year 1 Tax Shield: ${savings}\n• Engineering Study ROI: ${roi}\nSource: https://omnioperand.com/calculators/cost-segregation/`;

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
    const calc = document.getElementById('cost-segregation-calculator');
    if (calc) {
      calc.querySelectorAll('input, select').forEach(el => {
        el.addEventListener('input', solveCostSeg);
        el.addEventListener('change', solveCostSeg);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveCostSeg();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

