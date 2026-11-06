/**
 * assets/js/rd-tax-credit-solver.js
 * OmniOperand Federal R&D Tax Credit (IRC §41) Client Engine
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

  function solveRd() {
    const wages = getNum('param-w2_wages', 450000);
    const contractors = getNum('param-contractor_costs', 100000);
    const qualifiedContractors = contractors * 0.65;
    const supplies = getNum('param-cloud_supplies', 35000);

    const totalQre = wages + qualifiedContractors + supplies;

    const y1 = getNum('param-prior_y1_qre', 200000);
    const y2 = getNum('param-prior_y2_qre', 180000);
    const y3 = getNum('param-prior_y3_qre', 160000);

    const hasHistory = y1 > 0 || y2 > 0 || y3 > 0;
    const priorAvg = hasHistory ? (y1 + y2 + y3) / 3 : 0;
    const baseAmount = priorAvg * 0.50;

    let credit = 0;
    if (hasHistory) {
      const incremental = Math.max(0, totalQre - baseAmount);
      credit = incremental * 0.14;
    } else {
      credit = totalQre * 0.06;
    }

    const effectiveRate = totalQre > 0 ? (credit / totalQre) * 100 : 0;
    const isQsb = document.getElementById('param-is_qsb')?.checked ?? true;
    const payrollOffset = isQsb ? Math.min(500000, credit) : 0;

    setMetric('res-federal_credit', formatUSD(credit));
    setMetric('res-payroll_offset', formatUSD(payrollOffset));
    setMetric('res-total_qre', formatUSD(totalQre));
    setMetric('res-effective_rate', formatDec(effectiveRate, 2) + '% of QRE');
    setMetric('res-base_amount', formatUSD(baseAmount));
    setMetric('res-qualified_contractors', formatUSD(qualifiedContractors) + ' (65% limit)');

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Federal R&D Tax Credit (IRC §41) Verification]
Qualified Research Expenses (QRE): $${Math.round(totalQre).toLocaleString()}
  • W-2 Employee Tech Wages: $${wages.toLocaleString()}
  • 1099 US Contractors (65% §41 limit): $${Math.round(qualifiedContractors).toLocaleString()} (Raw: $${contractors.toLocaleString()})
  • Cloud Hosting & Engineering Supplies: $${supplies.toLocaleString()}
Prior 3-Year Average QRE: $${Math.round(priorAvg).toLocaleString()} -> ASC Base Amount (50%): $${Math.round(baseAmount).toLocaleString()}
Alternative Simplified Credit (ASC 14%): $${Math.round(credit).toLocaleString()} (Effective Yield: ${effectiveRate.toFixed(2)}%)
Section 41(h) Qualified Small Business Payroll Tax Offset: $${Math.round(payrollOffset).toLocaleString()} against Employer FICA`;
    }
  }

  function copySummary() {
    const credit = document.getElementById('res-federal_credit')?.innerText || 'N/A';
    const payroll = document.getElementById('res-payroll_offset')?.innerText || 'N/A';
    const qre = document.getElementById('res-total_qre')?.innerText || 'N/A';

    const text = `OmniOperand R&D Tax Credit Analysis:\n• Total Qualified R&D (QRE): ${qre}\n• Federal R&D Credit: ${credit}\n• Payroll Tax Cash Offset: ${payroll}\nSource: https://omnioperand.com/calculators/rd-tax-credit/`;

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
    const calc = document.getElementById('rd-tax-credit-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveRd);
        el.addEventListener('change', solveRd);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveRd();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
