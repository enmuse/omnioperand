/**
 * assets/js/islamic-finance-solver.js
 * OmniOperand Shariah-Compliant Financing Engine
 * Implements AAOIFI Standards:
 * - Standard No. 12: Diminishing Musharaka (Musharaka Mutanaqisa)
 * - Standard No. 8: Murabaha (Cost-Plus Sale)
 * - Standard No. 9: Ijara (Lease-to-Own / Ijara Muntahiya Bittamleek)
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

  // 1. Diminishing Musharaka Engine
  function solveMusharaka() {
    const price = getNum('param-home_price') || 400000;
    const downPct = (getNum('param-down_payment_pct') || 20) / 100;
    const profitRate = (getNum('param-profit_rate') || 6.5) / 100;
    const years = getNum('param-financing_term') || 30;

    const clientInitialEquity = price * downPct;
    const bankInitialEquity = price - clientInitialEquity;

    const n = Math.max(1, years * 12);
    const r = profitRate / 12;

    // Monthly installment M (rental + equity buyout)
    let monthlyTotal = 0;
    if (r === 0) {
      monthlyTotal = bankInitialEquity / n;
    } else {
      const factor = Math.pow(1 + r, n);
      monthlyTotal = bankInitialEquity * (r * factor) / (factor - 1);
    }

    // Month 1 breakdown
    const m1Rental = bankInitialEquity * r;
    const m1EquityBuyout = monthlyTotal - m1Rental;

    // Year 1 equity acquired
    let bankBal = bankInitialEquity;
    let y1RentalTotal = 0;
    let y1EquityTotal = 0;
    for (let m = 0; m < 12; m++) {
      const rent = bankBal * r;
      const equity = monthlyTotal - rent;
      y1RentalTotal += rent;
      y1EquityTotal += equity;
      bankBal -= equity;
    }

    const totalPaidOverLife = monthlyTotal * n;
    const totalProfitPaid = totalPaidOverLife - bankInitialEquity;

    setMetric('res-monthly_installment', '$' + monthlyTotal.toFixed(2));
    setMetric('res-m1_rental', '$' + m1Rental.toFixed(2));
    setMetric('res-m1_equity', '$' + m1EquityBuyout.toFixed(2));
    setMetric('res-client_initial_equity', formatUSD(clientInitialEquity) + ` (${(downPct * 100).toFixed(0)}%)`);
    setMetric('res-bank_initial_share', formatUSD(bankInitialEquity) + ` (${((1 - downPct) * 100).toFixed(0)}%)`);
    setMetric('res-total_profit_paid', formatUSD(totalProfitPaid));
    setMetric('res-total_financing_cost', formatUSD(totalPaidOverLife));

    // Dispatch calculated event
    window.dispatchEvent(new CustomEvent('omni:calculated', {
      detail: {
        inputs: { home_price: price, down_payment_pct: downPct * 100, profit_rate: profitRate * 100, term: years },
        results: { monthly_installment: monthlyTotal, total_profit: totalProfitPaid }
      }
    }));
  }

  // 2. Murabaha Engine
  function solveMurabaha() {
    const costPrice = getNum('param-purchase_price') || 300000;
    const downPayment = getNum('param-down_payment') || 60000;
    const profitMarginPct = (getNum('param-profit_margin') || 25) / 100;
    const termYears = getNum('param-term_years') || 15;

    const financedAmount = Math.max(0, costPrice - downPayment);
    const fixedProfit = financedAmount * profitMarginPct;
    const totalMurabahaSalePrice = financedAmount + fixedProfit;
    const months = termYears * 12;
    const monthlyInstallment = totalMurabahaSalePrice / months;

    setMetric('res-monthly_installment', '$' + monthlyInstallment.toFixed(2));
    setMetric('res-total_sale_price', formatUSD(totalMurabahaSalePrice));
    setMetric('res-fixed_profit', formatUSD(fixedProfit));
    setMetric('res-financed_principal', formatUSD(financedAmount));

    window.dispatchEvent(new CustomEvent('omni:calculated', {
      detail: {
        inputs: { purchase_price: costPrice, down_payment: downPayment, profit_margin: profitMarginPct * 100, term: termYears },
        results: { monthly_installment: monthlyInstallment, fixed_profit: fixedProfit }
      }
    }));
  }

  // 3. Ijara Engine
  function solveIjara() {
    const propertyValue = getNum('param-property_value') || 400000;
    const securityDeposit = getNum('param-security_deposit') || 80000;
    const annualLeaseRate = (getNum('param-lease_rate') || 6.25) / 100;
    const leaseYears = getNum('param-lease_years') || 30;

    const bankNetInvestment = propertyValue - securityDeposit;
    const months = leaseYears * 12;
    const monthlyRate = annualLeaseRate / 12;

    const factor = Math.pow(1 + monthlyRate, months);
    const monthlyRentPlusOwnership = bankNetInvestment * (monthlyRate * factor) / (factor - 1);
    const totalLeasePayments = monthlyRentPlusOwnership * months;
    const totalLeaseRentProfit = totalLeasePayments - bankNetInvestment;

    setMetric('res-monthly_payment', '$' + monthlyRentPlusOwnership.toFixed(2));
    setMetric('res-net_investment', formatUSD(bankNetInvestment));
    setMetric('res-total_lease_profit', formatUSD(totalLeaseRentProfit));
    setMetric('res-total_cost', formatUSD(totalLeasePayments));

    window.dispatchEvent(new CustomEvent('omni:calculated', {
      detail: {
        inputs: { property_value: propertyValue, security_deposit: securityDeposit, lease_rate: annualLeaseRate * 100, term: leaseYears },
        results: { monthly_payment: monthlyRentPlusOwnership, lease_profit: totalLeaseRentProfit }
      }
    }));
  }

  function init() {
    const isMusharaka = document.getElementById('musharaka-calculator');
    const isMurabaha = document.getElementById('murabaha-calculator');
    const isIjara = document.getElementById('ijara-calculator');

    if (isMusharaka) {
      document.querySelectorAll('#musharaka-calculator input, #musharaka-calculator select').forEach(el => {
        el.addEventListener('input', solveMusharaka);
        el.addEventListener('change', solveMusharaka);
      });
      solveMusharaka();
    } else if (isMurabaha) {
      document.querySelectorAll('#murabaha-calculator input, #murabaha-calculator select').forEach(el => {
        el.addEventListener('input', solveMurabaha);
        el.addEventListener('change', solveMurabaha);
      });
      solveMurabaha();
    } else if (isIjara) {
      document.querySelectorAll('#ijara-calculator input, #ijara-calculator select').forEach(el => {
        el.addEventListener('input', solveIjara);
        el.addEventListener('change', solveIjara);
      });
      solveIjara();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
