/**
 * assets/js/dscr-loan-solver.js
 * OmniOperand DSCR Rental Property Investor Loan Client Engine
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

  function solveDSCR() {
    const price = getNum('param-property_price', 400000);
    const downPct = getNum('param-down_payment_pct', 20) / 100;
    const rate = getNum('param-interest_rate', 7.25) / 100;
    const termYears = getNum('param-loan_term_years', 30);
    const grossRent = getNum('param-gross_monthly_rent', 3200);
    const annualTaxes = getNum('param-annual_property_taxes', 4800);
    const annualInsurance = getNum('param-annual_insurance', 1800);
    const monthlyHoa = getNum('param-monthly_hoa', 0);

    const downAmount = price * downPct;
    const loanAmount = Math.max(0, price - downAmount);
    const n = Math.max(1, termYears * 12);
    const r = rate / 12;

    let monthlyPI = 0;
    if (loanAmount > 0) {
      if (r === 0) {
        monthlyPI = loanAmount / n;
      } else {
        const f = Math.pow(1 + r, n);
        monthlyPI = loanAmount * (r * f) / (f - 1);
      }
    }

    const monthlyTaxes = annualTaxes / 12;
    const monthlyInsurance = annualInsurance / 12;
    const totalPitia = monthlyPI + monthlyTaxes + monthlyInsurance + monthlyHoa;

    const dscrRatio = totalPitia > 0 ? (grossRent / totalPitia) : 0;
    const monthlyCashFlow = grossRent - totalPitia;
    const annualCashFlow = monthlyCashFlow * 12;

    const maxPitia100 = grossRent > 0 ? grossRent / 1.00 : 0;
    const maxPitia120 = grossRent > 0 ? grossRent / 1.20 : 0;
    const maxPitia125 = grossRent > 0 ? grossRent / 1.25 : 0;

    // Badge styling & classification
    const badgeEl = document.getElementById('res-dscr_badge');
    let tierText = 'Deficit (< 1.00x)';
    let tierBg = 'rgba(239, 68, 68, 0.15)';
    let tierColor = '#ef4444';

    if (dscrRatio >= 1.50) {
      tierText = 'Strong Prime (1.50x+)';
      tierBg = 'rgba(16, 185, 129, 0.2)';
      tierColor = '#34d399';
    } else if (dscrRatio >= 1.20) {
      tierText = 'Standard Qualified (1.20x–1.49x)';
      tierBg = 'rgba(16, 185, 129, 0.15)';
      tierColor = '#10b981';
    } else if (dscrRatio >= 1.00) {
      tierText = 'Tight Coverage (1.00x–1.19x)';
      tierBg = 'rgba(245, 158, 11, 0.15)';
      tierColor = '#f59e0b';
    }

    if (badgeEl) {
      badgeEl.innerText = tierText;
      badgeEl.style.backgroundColor = tierBg;
      badgeEl.style.color = tierColor;
    }

    setMetric('res-dscr_ratio', formatDec(dscrRatio, 2) + 'x');
    setMetric('res-monthly_pitia', formatUSD(totalPitia));
    setMetric('res-monthly_pi', formatUSD(monthlyPI));
    setMetric('res-monthly_cash_flow', (monthlyCashFlow >= 0 ? '+' : '') + formatUSD(monthlyCashFlow) + '/mo');
    setMetric('res-annual_cash_flow', (annualCashFlow >= 0 ? '+' : '') + formatUSD(annualCashFlow) + '/yr');
    setMetric('res-loan_amount', formatUSD(loanAmount));
    setMetric('res-down_payment', formatUSD(downAmount) + ` (${(downPct * 100).toFixed(0)}%)`);
    setMetric('res-max_pitia_100', formatUSD(maxPitia100) + '/mo');
    setMetric('res-max_pitia_120', formatUSD(maxPitia120) + '/mo');
    setMetric('res-max_pitia_125', formatUSD(maxPitia125) + '/mo');

    const cashFlowMetric = document.getElementById('res-monthly_cash_flow');
    if (cashFlowMetric) {
      cashFlowMetric.style.color = monthlyCashFlow >= 0 ? 'var(--accent-emerald, #10b981)' : '#ef4444';
    }

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand DSCR Underwriting Engine Verification]
Property Purchase Price: $${price.toLocaleString()}
Down Payment: ${(downPct * 100).toFixed(0)}% ($${Math.round(downAmount).toLocaleString()})
Loan Principal: $${Math.round(loanAmount).toLocaleString()} @ ${(rate * 100).toFixed(2)}% (${termYears} Yrs)
Monthly Principal & Interest (P&I): $${monthlyPI.toFixed(2)}
Taxes ($${(annualTaxes/12).toFixed(2)}) + Insurance ($${(annualInsurance/12).toFixed(2)}) + HOA ($${monthlyHoa})
Total Monthly PITIA: $${totalPitia.toFixed(2)}
Gross Monthly Rental Income: $${grossRent.toLocaleString()}
Resulting DSCR: ${dscrRatio.toFixed(4)}x (${tierText})
Monthly Net Cash Flow: $${monthlyCashFlow.toFixed(2)}/mo
Threshold Allowable PITIA: 1.00x: $${maxPitia100.toFixed(2)} | 1.20x: $${maxPitia120.toFixed(2)} | 1.25x: $${maxPitia125.toFixed(2)}`;
    }
  }

  function copySummary() {
    const dscr = document.getElementById('res-dscr_ratio')?.innerText || 'N/A';
    const pitia = document.getElementById('res-monthly_pitia')?.innerText || 'N/A';
    const cashFlow = document.getElementById('res-monthly_cash_flow')?.innerText || 'N/A';
    const rent = document.getElementById('param-gross_monthly_rent')?.value || '0';
    const price = document.getElementById('param-property_price')?.value || '0';

    const text = `OmniOperand DSCR Loan Analysis:\n• Property Price: $${Number(price).toLocaleString()}\n• Gross Monthly Rent: $${Number(rent).toLocaleString()}\n• Total Monthly PITIA: ${pitia}\n• DSCR Ratio: ${dscr}\n• Net Cash Flow: ${cashFlow}\nSource: https://omnioperand.com/calculators/dscr-loan/`;

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
    const calc = document.getElementById('dscr-loan-calculator');
    if (calc) {
      // Connect inputs & sliders
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveDSCR);
        el.addEventListener('change', solveDSCR);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveDSCR();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
