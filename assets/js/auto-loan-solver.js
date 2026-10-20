/**
 * assets/js/auto-loan-solver.js
 * High-Precision Auto Loan, Payment & Affordability Inversion Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    vehiclePrice: 38000,
    downPayment: 5000,
    tradeIn: 3000,
    taxRate: 7.0,
    fees: 500,
    apr: 5.9,
    termMonths: 60,
    monthlyPayment: 624.49,
    precision: 2,
    activeInput: 'vehiclePrice'
  };

  // DOM Elements
  const elPrice = document.getElementById('param-price');
  const elDown = document.getElementById('param-down');
  const elTrade = document.getElementById('param-trade');
  const elTax = document.getElementById('param-tax');
  const elFees = document.getElementById('param-fees');
  const elApr = document.getElementById('param-apr');
  const elTerm = document.getElementById('param-term');
  const elPayment = document.getElementById('param-payment');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispPayment = document.getElementById('disp-payment');
  const dispFinanced = document.getElementById('disp-financed');
  const dispInterest = document.getElementById('disp-interest');
  const dispTotalCost = document.getElementById('disp-total-cost');
  const dispTaxAmount = document.getElementById('disp-tax-amount');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const chartSvg = document.getElementById('auto-loan-chart-svg');

  function round(val, dec) {
    if (isNaN(val) || !isFinite(val)) return 0;
    return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
  }

  function fmtCurrency(val, dec = 2) {
    return '$' + round(val, dec).toLocaleString('en-US', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec
    });
  }

  function computeFinancedAmount(price, down, trade, taxRate, fees) {
    // Taxable base is usually price minus trade-in (in most US states)
    const taxableBase = Math.max(0, price - trade);
    const tax = taxableBase * (taxRate / 100);
    const totalOutTheDoor = price + tax + fees;
    const netFinanced = Math.max(0, totalOutTheDoor - down - trade);
    return {
      tax: tax,
      totalOutTheDoor: totalOutTheDoor,
      netFinanced: netFinanced
    };
  }

  function computeMonthlyPayment(P, apr, months) {
    const i = (apr / 100) / 12;
    if (i === 0) return P / months;
    const factor = Math.pow(1 + i, months);
    return P * (i * factor) / (factor - 1);
  }

  function invertAffordablePrice(targetM, apr, months, down, trade, taxRate, fees) {
    const i = (apr / 100) / 12;
    let maxP = 0;
    if (i === 0) {
      maxP = targetM * months;
    } else {
      const factor = Math.pow(1 + i, months);
      maxP = targetM * (factor - 1) / (i * factor);
    }

    // Invert out-the-door: maxP = price + (price - trade)*taxRate/100 + fees - down - trade
    // maxP + down + trade - fees = price * (1 + taxRate/100) - trade * (taxRate/100)
    // price * (1 + taxRate/100) = maxP + down + trade*(1 + taxRate/100) - fees
    const tMultiplier = 1 + (taxRate / 100);
    const rhs = maxP + down + trade * tMultiplier - fees;
    const price = rhs / tMultiplier;
    return Math.max(0, price);
  }

  function renderChart(vehicleCost, taxAndFees, totalInterest) {
    if (!chartSvg) return;
    const w = 400;
    const h = 220;
    const total = vehicleCost + taxAndFees + totalInterest;
    if (total <= 0) return;

    const pctVehicle = (vehicleCost / total) * 100;
    const pctTaxes = (taxAndFees / total) * 100;
    const pctInterest = (totalInterest / total) * 100;

    const barW = 320;
    const barH = 34;
    const barX = 40;
    const barY = 50;

    const wVeh = (pctVehicle / 100) * barW;
    const wTax = (pctTaxes / 100) * barW;
    const wInt = (pctInterest / 100) * barW;

    chartSvg.innerHTML = `
      <!-- Segmented Bar -->
      <rect x="${barX}" y="${barY}" width="${wVeh}" height="${barH}" rx="4" fill="var(--accent-blue)"/>
      <rect x="${barX + wVeh}" y="${barY}" width="${wTax}" height="${barH}" rx="4" fill="var(--accent-amber)"/>
      <rect x="${barX + wVeh + wTax}" y="${barY}" width="${wInt}" height="${barH}" rx="4" fill="var(--accent-rose)"/>
      <!-- Legend -->
      <g transform="translate(40, 120)">
        <circle cx="8" cy="8" r="6" fill="var(--accent-blue)"/>
        <text x="24" y="12" font-size="12" fill="var(--text-bright)">Vehicle Base: ${fmtCurrency(vehicleCost, 0)} (${round(pctVehicle, 1)}%)</text>
        
        <circle cx="8" cy="38" r="6" fill="var(--accent-amber)"/>
        <text x="24" y="42" font-size="12" fill="var(--text-bright)">Taxes & Fees: ${fmtCurrency(taxAndFees, 0)} (${round(pctTaxes, 1)}%)</text>
        
        <circle cx="8" cy="68" r="6" fill="var(--accent-rose)"/>
        <text x="24" y="72" font-size="12" fill="var(--text-bright)">Financing Interest: ${fmtCurrency(totalInterest, 0)} (${round(pctInterest, 1)}%)</text>
      </g>
    `;
  }

  function update() {
    const price = state.vehiclePrice;
    const down = state.downPayment;
    const trade = state.tradeIn;
    const taxRate = state.taxRate;
    const fees = state.fees;
    const apr = state.apr;
    const months = state.termMonths;
    const dec = state.precision;

    const fin = computeFinancedAmount(price, down, trade, taxRate, fees);
    const P = fin.netFinanced;
    const payment = computeMonthlyPayment(P, apr, months);
    state.monthlyPayment = payment;

    if (elPayment && state.activeInput !== 'payment') {
      elPayment.value = round(payment, 2);
    }

    const totalLoanPayments = payment * months;
    const totalInterest = Math.max(0, totalLoanPayments - P);
    const totalCostOfVehicle = down + trade + totalLoanPayments;
    const taxAndFees = fin.tax + fees;

    if (dispPayment) dispPayment.textContent = fmtCurrency(payment, dec);
    if (dispFinanced) dispFinanced.textContent = fmtCurrency(P, dec);
    if (dispInterest) dispInterest.textContent = fmtCurrency(totalInterest, dec);
    if (dispTotalCost) dispTotalCost.textContent = fmtCurrency(totalCostOfVehicle, dec);
    if (dispTaxAmount) dispTaxAmount.textContent = fmtCurrency(fin.tax, dec);

    renderChart(price, taxAndFees, totalInterest);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Auto Loan & Affordability Context
Sticker Vehicle Price: $${round(price, 2)}
Down Payment: $${round(down, 2)} | Trade-in Allowance: $${round(trade, 2)}
Sales Tax Rate: ${taxRate}% (Est. Tax: $${round(fin.tax, 2)}) | Dealer Fees: $${round(fees, 2)}
Interest Rate (APR): ${apr}% | Loan Term: ${months} Months (${(months / 12).toFixed(1)} Years)
--------------------------------------------------
DERIVED FINANCING INVARIANTS:
Net Amount Financed (P): $${round(P, 2)}
Monthly Loan Payment (M): $${round(payment, 2)}
Total Loan Interest: $${round(totalInterest, 2)}
Total Out-of-Pocket Vehicle Cost: $${round(totalCostOfVehicle, 2)}
--------------------------------------------------
GOVERNING INVERSION IDENTITIES:
M = P * [i(1+i)^N] / [(1+i)^N - 1]
Affordable Price V = [P_max + Down + Trade*(1+tax) - Fees] / (1+tax)
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elPrice) {
    elPrice.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.vehiclePrice = v;
        state.activeInput = 'vehiclePrice';
        update();
      }
    });
  }

  if (elDown) {
    elDown.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.downPayment = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elTrade) {
    elTrade.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.tradeIn = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elTax) {
    elTax.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.taxRate = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elFees) {
    elFees.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.fees = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elApr) {
    elApr.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.apr = v;
        update();
      }
    });
  }

  if (elTerm) {
    elTerm.addEventListener('change', (e) => {
      state.termMonths = parseInt(e.target.value, 10);
      update();
    });
  }

  if (elPayment) {
    // Inversion: enter desired monthly payment -> compute affordable vehicle price
    elPayment.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.activeInput = 'payment';
        state.monthlyPayment = v;
        const affordablePrice = invertAffordablePrice(v, state.apr, state.termMonths, state.downPayment, state.tradeIn, state.taxRate, state.fees);
        state.vehiclePrice = affordablePrice;
        if (elPrice) elPrice.value = round(affordablePrice, 2);
        update();
      }
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 2;
      update();
    });
  }

  const copyLlmBtn = document.getElementById('copy-llm-prompt-btn');
  if (copyLlmBtn && dispLlmPrompt) {
    copyLlmBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(dispLlmPrompt.textContent).then(() => {
        const orig = copyLlmBtn.textContent;
        copyLlmBtn.textContent = 'Copied!';
        setTimeout(() => copyLlmBtn.textContent = orig, 2000);
      });
    });
  }

  update();
})();
