/**
 * assets/js/structured-settlement-solver.js
 * OmniOperand Structured Settlement & Annuity Factoring Client Engine
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

  function solveSettlement() {
    const pmt = getNum('param-monthly_payment', 2500);
    const years = Math.max(0.5, getNum('param-remaining_years', 10));
    const colaPct = getNum('param-annual_cola', 0) / 100;
    const discountRate = Math.max(0.01, getNum('param-discount_rate', 12) / 100);
    const adminFee = getNum('param-admin_fee', 2500);

    const totalMonths = Math.round(years * 12);
    const monthlyDiscount = discountRate / 12;

    let nominalTotal = 0;
    let grossPv = 0;

    for (let m = 1; m <= totalMonths; m++) {
      const yearIndex = Math.floor((m - 1) / 12);
      const adjustedPmt = pmt * Math.pow(1 + colaPct, yearIndex);
      nominalTotal += adjustedPmt;
      const pv = adjustedPmt / Math.pow(1 + monthlyDiscount, m);
      grossPv += pv;
    }

    const netOffer = Math.max(0, grossPv - adminFee);
    const discountSurrendered = Math.max(0, nominalTotal - netOffer);
    const payoutPct = nominalTotal > 0 ? (netOffer / nominalTotal) * 100 : 0;

    setMetric('res-net_cash_offer', formatUSD(netOffer));
    setMetric('res-dollar_discount', formatUSD(discountSurrendered));
    setMetric('res-nominal_future_value', formatUSD(nominalTotal));
    setMetric('res-effective_payout_pct', formatDec(payoutPct, 1) + '% Payout');
    setMetric('res-total_payments', totalMonths + ' Payments');
    setMetric('res-gross_pv', formatUSD(grossPv));

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Structured Settlement Factoring Verification]
Guaranteed Annuity Stream: $${pmt.toLocaleString()}/month for ${years} Years (${totalMonths} Total Payments)
COLA Escalation: ${(colaPct * 100).toFixed(1)}% Annual
Total Future Contract Nominal Value: $${Math.round(nominalTotal).toLocaleString()}
Market Factoring Discount Rate: ${(discountRate * 100).toFixed(2)}% | Legal & Filing Fees: $${adminFee.toLocaleString()}
Fair Market Gross Present Value: $${Math.round(grossPv).toLocaleString()}
Estimated Cash-in-Hand Lump Sum Offer: $${Math.round(netOffer).toLocaleString()}
Effective Realization Rate: ${payoutPct.toFixed(1)}% of Future Nominal Dollars
Cost of Immediate Liquidity (Discount Surrendered): -$${Math.round(discountSurrendered).toLocaleString()}`;
    }
  }

  function copySummary() {
    const offer = document.getElementById('res-net_cash_offer')?.innerText || 'N/A';
    const nominal = document.getElementById('res-nominal_future_value')?.innerText || 'N/A';
    const discount = document.getElementById('res-dollar_discount')?.innerText || 'N/A';
    const pmt = document.getElementById('param-monthly_payment')?.value || '0';

    const text = `OmniOperand Structured Settlement Analysis:\n• Monthly Payment: $${Number(pmt).toLocaleString()}\n• Future Nominal Sum: ${nominal}\n• Immediate Lump Sum Offer: ${offer}\n• Discount Surrendered: ${discount}\nSource: https://omnioperand.com/calculators/structured-settlement-lump-sum/`;

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
    const calc = document.getElementById('structured-settlement-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveSettlement);
        el.addEventListener('change', solveSettlement);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveSettlement();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
