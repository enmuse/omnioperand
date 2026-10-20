/**
 * assets/js/mortgage-solver.js
 * High-Precision Mortgage Amortization, Early Payoff & Inversion Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  // State
  const state = {
    principal: 400000,
    annualRate: 6.5,
    termYears: 30,
    monthlyPayment: 2528.27,
    extraMonthly: 200,
    precision: 2,
    activeInput: 'principal'
  };

  // DOM Elements
  const elPrincipal = document.getElementById('param-principal');
  const elRate = document.getElementById('param-rate');
  const elTerm = document.getElementById('param-term');
  const elPayment = document.getElementById('param-payment');
  const elExtra = document.getElementById('param-extra');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispBasePayment = document.getElementById('disp-base-payment');
  const dispTotalPayment = document.getElementById('disp-total-payment');
  const dispTotalInterest = document.getElementById('disp-total-interest');
  const dispTotalPaid = document.getElementById('disp-total-paid');
  const dispPayoffMonths = document.getElementById('disp-payoff-months');
  const dispInterestSaved = document.getElementById('disp-interest-saved');
  const dispTimeSaved = document.getElementById('disp-time-saved');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const scheduleBody = document.getElementById('amortization-schedule-body');
  const chartSvg = document.getElementById('mortgage-chart-svg');

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

  function calculateBaseMonthlyPayment(P, rAnnual, years) {
    const i = (rAnnual / 100) / 12;
    const n = years * 12;
    if (i === 0) return P / n;
    const factor = Math.pow(1 + i, n);
    return P * (i * factor) / (factor - 1);
  }

  function calculatePrincipalFromPayment(M, rAnnual, years) {
    const i = (rAnnual / 100) / 12;
    const n = years * 12;
    if (i === 0) return M * n;
    const factor = Math.pow(1 + i, n);
    return M * (factor - 1) / (i * factor);
  }

  function calculateTermFromPayment(P, M, rAnnual) {
    const i = (rAnnual / 100) / 12;
    if (i === 0) return (P / M) / 12;
    if (M <= P * i) return Infinity; // Payment doesn't cover interest
    const n = -Math.log(1 - (P * i) / M) / Math.log(1 + i);
    return n / 12;
  }

  function buildAmortization(P, rAnnual, years, extra) {
    const i = (rAnnual / 100) / 12;
    const nStandard = years * 12;
    const standardM = calculateBaseMonthlyPayment(P, rAnnual, years);
    const standardTotalInterest = (standardM * nStandard) - P;

    let balance = P;
    let totalInterestPaid = 0;
    let totalPaid = 0;
    let month = 0;
    const schedule = [];
    const yearlyData = [];
    let currentYearInterest = 0;
    let currentYearPrincipal = 0;

    const actualMonthlyPayment = standardM + extra;

    while (balance > 0.001 && month < 1200) { // Safety cap 100 years
      month++;
      const interestPayment = balance * i;
      let principalPayment = actualMonthlyPayment - interestPayment;

      if (principalPayment > balance) {
        principalPayment = balance;
      }

      balance -= principalPayment;
      totalInterestPaid += interestPayment;
      totalPaid += (interestPayment + principalPayment);

      currentYearInterest += interestPayment;
      currentYearPrincipal += principalPayment;

      if (month <= 12 || month % 12 === 0 || balance <= 0.001) {
        schedule.push({
          month: month,
          payment: interestPayment + principalPayment,
          principalPayment: principalPayment,
          interestPayment: interestPayment,
          totalInterest: totalInterestPaid,
          balance: Math.max(0, balance)
        });
      }

      if (month % 12 === 0 || balance <= 0.001) {
        yearlyData.push({
          year: Math.ceil(month / 12),
          yearInterest: currentYearInterest,
          yearPrincipal: currentYearPrincipal,
          balance: Math.max(0, balance)
        });
        currentYearInterest = 0;
        currentYearPrincipal = 0;
      }
    }

    const interestSaved = Math.max(0, standardTotalInterest - totalInterestPaid);
    const monthsSaved = Math.max(0, nStandard - month);

    return {
      standardPayment: standardM,
      actualPayment: actualMonthlyPayment,
      totalMonths: month,
      standardMonths: nStandard,
      monthsSaved: monthsSaved,
      totalInterest: totalInterestPaid,
      standardTotalInterest: standardTotalInterest,
      interestSaved: interestSaved,
      totalPaid: totalPaid,
      schedule: schedule,
      yearlyData: yearlyData
    };
  }

  function renderChart(yearlyData, initialP) {
    if (!chartSvg) return;
    const w = 600;
    const h = 260;
    const padX = 50;
    const padY = 30;
    const plotW = w - padX - 30;
    const plotH = h - padY - 30;

    if (!yearlyData || yearlyData.length === 0) return;

    const maxYear = yearlyData[yearlyData.length - 1].year;
    const points = yearlyData.map(d => {
      const x = padX + (d.year / maxYear) * plotW;
      const y = h - padY - (d.balance / initialP) * plotH;
      return `${round(x, 1)},${round(y, 1)}`;
    });

    const startX = padX;
    const startY = h - padY - plotH;
    const areaPoints = [`${startX},${h - padY}`, ...points, `${padX + plotW},${h - padY}`].join(' ');
    const linePath = points.join(' ');

    chartSvg.innerHTML = `
      <defs>
        <linearGradient id="balanceGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.02"/>
        </linearGradient>
      </defs>
      <!-- Grid -->
      <line x1="${padX}" y1="${h - padY}" x2="${w - 20}" y2="${h - padY}" stroke="var(--border-subtle)" stroke-width="1"/>
      <line x1="${padX}" y1="${padY}" x2="${w - 20}" y2="${padY}" stroke="var(--border-subtle)" stroke-dasharray="4" stroke-width="1"/>
      <line x1="${padX}" y1="${padY + plotH / 2}" x2="${w - 20}" y2="${padY + plotH / 2}" stroke="var(--border-subtle)" stroke-dasharray="4" stroke-width="1"/>
      <!-- Y Axis Labels -->
      <text x="${padX - 8}" y="${padY + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">${fmtCurrency(initialP, 0)}</text>
      <text x="${padX - 8}" y="${padY + plotH / 2 + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">${fmtCurrency(initialP / 2, 0)}</text>
      <text x="${padX - 8}" y="${h - padY + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">$0</text>
      <!-- X Axis Labels -->
      <text x="${padX}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Year 0</text>
      <text x="${padX + plotW / 2}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${round(maxYear / 2, 0)}</text>
      <text x="${padX + plotW}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${maxYear}</text>
      <!-- Area & Line -->
      <polygon points="${areaPoints}" fill="url(#balanceGrad)"/>
      <polyline points="${linePath}" fill="none" stroke="var(--accent-blue)" stroke-width="2.5" stroke-linecap="round"/>
    `;
  }

  function renderScheduleTable(schedule) {
    if (!scheduleBody) return;
    scheduleBody.innerHTML = schedule.map(row => `
      <tr>
        <td style="font-weight:600; font-family:var(--font-mono);">M ${row.month}</td>
        <td>${fmtCurrency(row.payment)}</td>
        <td style="color:var(--accent-emerald);">${fmtCurrency(row.principalPayment)}</td>
        <td style="color:var(--accent-rose);">${fmtCurrency(row.interestPayment)}</td>
        <td>${fmtCurrency(row.totalInterest)}</td>
        <td style="font-weight:600;">${fmtCurrency(row.balance)}</td>
      </tr>
    `).join('');
  }

  function update() {
    const P = state.principal;
    const r = state.annualRate;
    const years = state.termYears;
    const extra = state.extraMonthly;
    const dec = state.precision;

    const basePayment = calculateBaseMonthlyPayment(P, r, years);
    state.monthlyPayment = basePayment;
    if (elPayment && state.activeInput !== 'payment') {
      elPayment.value = round(basePayment, 2);
    }

    const res = buildAmortization(P, r, years, extra);

    if (dispBasePayment) dispBasePayment.textContent = fmtCurrency(basePayment, dec);
    if (dispTotalPayment) dispTotalPayment.textContent = fmtCurrency(basePayment + extra, dec);
    if (dispTotalInterest) dispTotalInterest.textContent = fmtCurrency(res.totalInterest, dec);
    if (dispTotalPaid) dispTotalPaid.textContent = fmtCurrency(res.totalPaid, dec);

    const yrs = Math.floor(res.totalMonths / 12);
    const remM = res.totalMonths % 12;
    if (dispPayoffMonths) {
      dispPayoffMonths.textContent = `${yrs} yrs, ${remM} mos (${res.totalMonths} total)`;
    }

    if (dispInterestSaved) dispInterestSaved.textContent = fmtCurrency(res.interestSaved, dec);

    const savedYrs = Math.floor(res.monthsSaved / 12);
    const savedM = res.monthsSaved % 12;
    if (dispTimeSaved) {
      dispTimeSaved.textContent = res.monthsSaved > 0 ? `${savedYrs} yrs, ${savedM} mos earlier` : 'Standard schedule';
    }

    renderChart(res.yearlyData, P);
    renderScheduleTable(res.schedule);

    // Update LLM prompt
    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Mortgage Amortization Context
Loan Principal (P): $${round(P, 2)}
Annual Interest Rate (r): ${r}% (Monthly i = ${(r / 12).toFixed(6)}%)
Standard Loan Term: ${years} Years (${years * 12} Months)
Extra Monthly Principal (E): $${round(extra, 2)}
--------------------------------------------------
DERIVED AMORTIZATION INVARIANTS:
Base Monthly Payment (M): $${round(basePayment, 2)}
Actual Monthly Payment (M + E): $${round(basePayment + extra, 2)}
Actual Payoff Horizon: ${res.totalMonths} months (${yrs} yrs, ${remM} mos)
Total Interest with Extra Payments: $${round(res.totalInterest, 2)}
Total Interest under Standard Schedule: $${round(res.standardTotalInterest, 2)}
Total Interest Savings: $${round(res.interestSaved, 2)}
Total Accelerated Time Saved: ${res.monthsSaved} months (${savedYrs} yrs, ${savedM} mos)
--------------------------------------------------
CLOSED-FORM PROOF IDENTITY:
M = P * [i(1+i)^n] / [(1+i)^n - 1]
P = M * [(1+i)^n - 1] / [i(1+i)^n]
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elPrincipal) {
    elPrincipal.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.principal = v;
        state.activeInput = 'principal';
        update();
      }
    });
  }

  if (elRate) {
    elRate.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.annualRate = v;
        state.activeInput = 'rate';
        update();
      }
    });
  }

  if (elTerm) {
    elTerm.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.termYears = v;
        state.activeInput = 'term';
        update();
      }
    });
  }

  if (elExtra) {
    elExtra.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.extraMonthly = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elPayment) {
    // Inversion: solve for principal given target payment
    elPayment.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.activeInput = 'payment';
        state.monthlyPayment = v;
        const invertedP = calculatePrincipalFromPayment(v, state.annualRate, state.termYears);
        if (invertedP > 0 && isFinite(invertedP)) {
          state.principal = invertedP;
          if (elPrincipal) elPrincipal.value = round(invertedP, 2);
          update();
        }
      }
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 2;
      update();
    });
  }

  // Quick preset buttons
  document.querySelectorAll('[data-preset-term]').forEach(btn => {
    btn.addEventListener('click', () => {
      const term = parseFloat(btn.getAttribute('data-preset-term'));
      if (term && elTerm) {
        elTerm.value = term;
        state.termYears = term;
        update();
      }
    });
  });

  // Copy LLM prompt
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

  // Initial calculation
  update();
})();
