/**
 * assets/js/sba-loan-solver.js
 * OmniOperand SBA 7(a) & SBA 504 Commercial Loan Client Engine
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

  function solveSba() {
    const program = document.getElementById('param-loan_program')?.value || '7a';
    const cost = getNum('param-project_cost', 1000000);
    const downPct = getNum('param-down_payment_pct', 10) / 100;
    const termYears = getNum('param-loan_term_years', 25);
    const primeRate = getNum('param-prime_rate', 8.5) / 100;
    const spread = getNum('param-lender_spread', 2.75) / 100;
    const noi = getNum('param-annual_noi', 150000);

    const downAmount = cost * downPct;
    const financedAmount = Math.max(0, cost - downAmount);
    const n = Math.max(1, termYears * 12);

    let monthlyPI = 0;
    let guaranteeFee = 0;
    let effectiveRatePct = 0;

    if (program === '7a') {
      effectiveRatePct = (primeRate + spread) * 100;
      const r = (primeRate + spread) / 12;

      if (financedAmount <= 150000) {
        guaranteeFee = 0;
      } else if (financedAmount <= 700000) {
        guaranteeFee = financedAmount * 0.0277;
      } else if (financedAmount <= 1000000) {
        guaranteeFee = financedAmount * 0.0327;
      } else {
        guaranteeFee = financedAmount * 0.0375;
      }

      if (financedAmount > 0 && r > 0) {
        const f = Math.pow(1 + r, n);
        monthlyPI = financedAmount * ((r * f) / (f - 1));
      }
    } else {
      // 504 loan: 50% bank @ 7.5%, 40% CDC @ 6.25%
      const seniorAmount = cost * 0.50;
      const cdcAmount = cost * 0.40;
      const bankR = (getNum('param-prime_rate', 7.5) / 100) / 12;
      const cdcR = (getNum('param-cdc_rate', 6.25) / 100) / 12;

      const fBank = Math.pow(1 + bankR, n);
      const bankPI = seniorAmount * ((bankR * fBank) / (fBank - 1));

      const fCdc = Math.pow(1 + cdcR, n);
      const cdcPI = cdcAmount * ((cdcR * fCdc) / (fCdc - 1));

      monthlyPI = bankPI + cdcPI;
      effectiveRatePct = financedAmount > 0
        ? ((seniorAmount * (bankR * 12) + cdcAmount * (cdcR * 12)) / financedAmount) * 100
        : 6.875;
      guaranteeFee = cdcAmount * 0.0215;
    }

    const annualDebtService = monthlyPI * 12;
    const dscr = annualDebtService > 0 ? (noi / annualDebtService) : 0;

    const badgeEl = document.getElementById('res-dscr_badge');
    let tierText = 'Deficit (< 1.15x)';
    let tierBg = 'rgba(239, 68, 68, 0.15)';
    let tierColor = '#ef4444';

    if (dscr >= 1.50) {
      tierText = 'Strong Coverage (1.50x+)';
      tierBg = 'rgba(16, 185, 129, 0.2)';
      tierColor = '#34d399';
    } else if (dscr >= 1.25) {
      tierText = 'Bank Approved (1.25x+)';
      tierBg = 'rgba(16, 185, 129, 0.15)';
      tierColor = '#10b981';
    } else if (dscr >= 1.15) {
      tierText = 'SBA Eligible (1.15x–1.24x)';
      tierBg = 'rgba(245, 158, 11, 0.15)';
      tierColor = '#f59e0b';
    }

    if (badgeEl) {
      badgeEl.innerText = tierText;
      badgeEl.style.backgroundColor = tierBg;
      badgeEl.style.color = tierColor;
    }

    setMetric('res-monthly_pi', formatUSD(monthlyPI) + '/mo');
    setMetric('res-effective_rate', formatDec(effectiveRatePct, 2) + '%');
    setMetric('res-loan_amount', formatUSD(financedAmount));
    setMetric('res-down_payment', formatUSD(downAmount));
    setMetric('res-guarantee_fee', formatUSD(guaranteeFee));
    setMetric('res-annual_debt', formatUSD(annualDebtService) + '/yr');
    setMetric('res-dscr', formatDec(dscr, 2) + 'x');

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand SBA Loan Commercial Underwriting Verification]
Program: SBA ${program === '7a' ? '7(a)' : '504 Certified Development Company'}
Total Project Cost: $${cost.toLocaleString()}
Borrower Equity (Down): $${Math.round(downAmount).toLocaleString()} (${(downPct * 100).toFixed(0)}%)
Financed Amount: $${Math.round(financedAmount).toLocaleString()} @ ${effectiveRatePct.toFixed(2)}% APR (${termYears} Yrs)
Monthly Debt Service: $${monthlyPI.toFixed(2)}/mo ($${annualDebtService.toFixed(2)}/yr)
Annual NOI: $${noi.toLocaleString()} -> Coverage DSCR: ${dscr.toFixed(2)}x (${tierText})
SBA Guaranty Fee: $${Math.round(guaranteeFee).toLocaleString()}`;
    }
  }

  function copySummary() {
    const monthly = document.getElementById('res-monthly_pi')?.innerText || 'N/A';
    const dscr = document.getElementById('res-dscr')?.innerText || 'N/A';
    const rate = document.getElementById('res-effective_rate')?.innerText || 'N/A';
    const cost = document.getElementById('param-project_cost')?.value || '0';

    const text = `OmniOperand SBA Loan Analysis:\n• Project Cost: $${Number(cost).toLocaleString()}\n• Blended APR: ${rate}\n• Monthly Debt Service: ${monthly}\n• Coverage (DSCR): ${dscr}\nSource: https://omnioperand.com/calculators/sba-loan/`;

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
    const calc = document.getElementById('sba-loan-calculator');
    if (calc) {
      calc.querySelectorAll('input, select').forEach(el => {
        el.addEventListener('input', solveSba);
        el.addEventListener('change', solveSba);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveSba();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
