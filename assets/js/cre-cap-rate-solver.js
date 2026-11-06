/**
 * assets/js/cre-cap-rate-solver.js
 * OmniOperand Commercial Real Estate Cap Rate, NOI & Debt Yield Client Engine
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

  function solveCre() {
    const price = getNum('param-purchase_price', 5000000);
    const gpr = getNum('param-gross_rent', 600000);
    const otherInc = getNum('param-other_income', 25000);
    const vacancyPct = getNum('param-vacancy_pct', 5) / 100;
    const opex = getNum('param-operating_expenses', 225000);
    const ltvPct = getNum('param-ltv_pct', 70) / 100;
    const rate = getNum('param-interest_rate', 6.75) / 100;
    const termYears = getNum('param-amortization_years', 25);

    const vacancyLoss = gpr * vacancyPct;
    const egi = gpr - vacancyLoss + otherInc;
    const noi = Math.max(0, egi - opex);
    const capRatePct = price > 0 ? (noi / price) * 100 : 0;

    const loanAmount = price * ltvPct;
    const equityRequired = Math.max(0, price - loanAmount);
    const n = Math.max(1, termYears * 12);
    const r = rate / 12;

    let monthlyDebt = 0;
    if (loanAmount > 0 && r > 0) {
      const f = Math.pow(1 + r, n);
      monthlyDebt = loanAmount * ((r * f) / (f - 1));
    }
    const annualDebt = monthlyDebt * 12;

    const debtYieldPct = loanAmount > 0 ? (noi / loanAmount) * 100 : 0;
    const dscr = annualDebt > 0 ? (noi / annualDebt) : 0;
    const netCashFlow = noi - annualDebt;
    const cocReturnPct = equityRequired > 0 ? (netCashFlow / equityRequired) * 100 : 0;

    const badgeEl = document.getElementById('res-cre_badge');
    if (badgeEl) {
      if (debtYieldPct >= 9.5 && dscr >= 1.25) {
        badgeEl.innerText = 'Wholesale Institutional Approved';
        badgeEl.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
        badgeEl.style.color = '#34d399';
      } else {
        badgeEl.innerText = 'Sub-Threshold Underwriting Warning';
        badgeEl.style.backgroundColor = 'rgba(245, 158, 11, 0.15)';
        badgeEl.style.color = '#f59e0b';
      }
    }

    setMetric('res-noi', formatUSD(noi) + '/yr');
    setMetric('res-cap_rate', formatDec(capRatePct, 2) + '%');
    setMetric('res-debt_yield', formatDec(debtYieldPct, 2) + '%');
    setMetric('res-dscr', formatDec(dscr, 2) + 'x');
    setMetric('res-net_cash_flow', (netCashFlow >= 0 ? '+' : '') + formatUSD(netCashFlow) + '/yr');
    setMetric('res-coc_return', formatDec(cocReturnPct, 1) + '% CoC');
    setMetric('res-egi', formatUSD(egi));
    setMetric('res-annual_debt_service', formatUSD(annualDebt));

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Commercial Real Estate Underwriting Verification]
Property Valuation: $${price.toLocaleString()}
Effective Gross Income (EGI): $${Math.round(egi).toLocaleString()} (GPR: $${gpr.toLocaleString()} - Vacancy ${(vacancyPct * 100).toFixed(0)}% + Other: $${otherInc.toLocaleString()})
Operating Expenses (OpEx): $${opex.toLocaleString()} (OpEx Ratio: ${((opex / egi) * 100).toFixed(1)}%)
Net Operating Income (NOI): $${Math.round(noi).toLocaleString()}
Resulting Capitalization Rate: ${capRatePct.toFixed(2)}%
Financed Debt: $${Math.round(loanAmount).toLocaleString()} (${(ltvPct * 100).toFixed(0)}% LTV @ ${(rate * 100).toFixed(2)}% ${termYears}-Yr Amort)
Annual Debt Service: $${Math.round(annualDebt).toLocaleString()} ($${monthlyDebt.toFixed(2)}/mo)
Underwriting Invariants: Debt Yield: ${debtYieldPct.toFixed(2)}% (Target >= 9.5%) | DSCR: ${dscr.toFixed(2)}x (Target >= 1.25x)
Net Cash-on-Cash Return: ${cocReturnPct.toFixed(2)}% (+$${Math.round(netCashFlow).toLocaleString()}/yr)`;
    }
  }

  function copySummary() {
    const capRate = document.getElementById('res-cap_rate')?.innerText || 'N/A';
    const noi = document.getElementById('res-noi')?.innerText || 'N/A';
    const debtYield = document.getElementById('res-debt_yield')?.innerText || 'N/A';
    const price = document.getElementById('param-purchase_price')?.value || '0';

    const text = `OmniOperand CRE Underwriting Analysis:\n• Property Price: $${Number(price).toLocaleString()}\n• Net Operating Income: ${noi}\n• Capitalization Rate: ${capRate}\n• Debt Yield: ${debtYield}\nSource: https://omnioperand.com/calculators/commercial-real-estate-cap-rate/`;

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
    const calc = document.getElementById('cre-cap-rate-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveCre);
        el.addEventListener('change', solveCre);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveCre();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

