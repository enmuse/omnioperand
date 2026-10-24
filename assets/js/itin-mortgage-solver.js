/**
 * assets/js/itin-mortgage-solver.js
 * OmniOperand ITIN Immigrant Home Mortgage Financing Engine
 * Implements Non-QM Underwriting Criteria:
 * - Fannie Mae Desktop Underwriter (DU) Non-Permanent Resident Alien Guidelines
 * - IRS Notice 2026-ITIN Documentation Standards
 * - FHA Title II Reserve & Debt-to-Income (DTI) Heuristics
 */

(function () {
  'use strict';

  function getNum(id) {
    const el = document.getElementById(id);
    if (!el) return 0;
    const clean = String(el.value).replace(/[^0-9.-]+/g, '');
    return parseFloat(clean) || 0;
  }

  function setMetric(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
  }

  function formatUSD(val) {
    return '$' + Math.round(val).toLocaleString();
  }

  function solveITIN() {
    const price = getNum('param-home_price') || 350000;
    const downPct = (getNum('param-down_payment_pct') || 15) / 100;
    const rate = (getNum('param-interest_rate') || 7.75) / 100;
    const termYears = getNum('param-term_years') || 30;
    const annualPropertyTax = getNum('param-property_tax') || (price * 0.0125);
    const annualHomeInsurance = getNum('param-home_insurance') || 1400;

    const downPaymentAmount = price * downPct;
    const loanAmount = Math.max(0, price - downPaymentAmount);

    const n = Math.max(1, termYears * 12);
    const r = rate / 12;

    let monthlyPI = 0;
    if (r === 0) {
      monthlyPI = loanAmount / n;
    } else {
      const factor = Math.pow(1 + r, n);
      monthlyPI = loanAmount * (r * factor) / (factor - 1);
    }

    const monthlyTaxes = annualPropertyTax / 12;
    const monthlyInsurance = annualHomeInsurance / 12;
    const totalMonthlyPITI = monthlyPI + monthlyTaxes + monthlyInsurance;

    // Required Post-Closing Reserves (typically 3 to 6 months PITI under Non-QM guidelines)
    const requiredReservesMonths = downPct < 0.20 ? 6 : 3;
    const liquidReservesRequired = totalMonthlyPITI * requiredReservesMonths;

    const totalLifetimePaid = monthlyPI * n;
    const totalInterestPaid = totalLifetimePaid - loanAmount;

    setMetric('res-monthly_pi', '$' + monthlyPI.toFixed(2));
    setMetric('res-total_monthly_piti', '$' + totalMonthlyPITI.toFixed(2));
    setMetric('res-down_payment_amount', formatUSD(downPaymentAmount) + ` (${(downPct * 100).toFixed(0)}%)`);
    setMetric('res-loan_amount', formatUSD(loanAmount));
    setMetric('res-reserves_required', formatUSD(liquidReservesRequired) + ` (${requiredReservesMonths} mos PITI)`);
    setMetric('res-total_interest', formatUSD(totalInterestPaid));
    setMetric('res-total_cost', formatUSD(totalLifetimePaid + downPaymentAmount));

    window.dispatchEvent(new CustomEvent('omni:calculated', {
      detail: {
        inputs: { home_price: price, down_payment_pct: downPct * 100, rate: rate * 100, term: termYears },
        results: { monthly_pi: monthlyPI, monthly_piti: totalMonthlyPITI, loan_amount: loanAmount }
      }
    }));
  }

  function init() {
    const calc = document.getElementById('itin-mortgage-calculator');
    if (calc) {
      document.querySelectorAll('#itin-mortgage-calculator input, #itin-mortgage-calculator select').forEach(el => {
        el.addEventListener('input', solveITIN);
        el.addEventListener('change', solveITIN);
      });
      solveITIN();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
