/**
 * assets/js/compound-interest-solver.js
 * High-Precision Compound Interest, APY & Inversion Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    principal: 10000,
    annualRate: 8.0,
    years: 20,
    contribution: 500,
    contribFrequency: 12, // 12 times a year
    compoundFrequency: 12, // 12 = monthly, 1 = annually, 4 = quarterly, 365 = daily, 0 = continuous
    depositTiming: 'end', // 'end' or 'beginning'
    precision: 2,
    activeMode: 'fv' // 'fv', 'pmt', 'principal', 'time'
  };

  // DOM Elements
  const elPrincipal = document.getElementById('param-principal');
  const elRate = document.getElementById('param-rate');
  const elYears = document.getElementById('param-years');
  const elContribution = document.getElementById('param-contribution');
  const elCompoundFreq = document.getElementById('param-compound-freq');
  const elTiming = document.getElementById('param-timing');
  const elTargetFv = document.getElementById('param-target-fv');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispFv = document.getElementById('disp-fv');
  const dispTotalContrib = document.getElementById('disp-total-contrib');
  const dispTotalInterest = document.getElementById('disp-total-interest');
  const dispTotalPrincipal = document.getElementById('disp-total-principal');
  const dispApy = document.getElementById('disp-apy');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const chartSvg = document.getElementById('compound-chart-svg');

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

  function calculateAPY(rAnnual, m) {
    const r = rAnnual / 100;
    if (m === 0) { // Continuous
      return (Math.exp(r) - 1) * 100;
    }
    return (Math.pow(1 + r / m, m) - 1) * 100;
  }

  function calculateFutureValue(P, rAnnual, t, PMT, m, contribPerYear, timing) {
    const r = rAnnual / 100;
    const isBeginning = (timing === 'beginning');

    if (m === 0) { // Continuous compounding
      const lumpSumFV = P * Math.exp(r * t);
      // For continuous compounding with continuous cash flows: PMT_yr * (e^(rt) - 1) / r
      const annualPMT = PMT * contribPerYear;
      const annuityFV = r > 0 ? annualPMT * (Math.exp(r * t) - 1) / r : annualPMT * t;
      return lumpSumFV + annuityFV;
    }

    // Effective rate per deposit period
    // If compounding freq equals deposit freq:
    let i = r / m;
    let n = m * t;

    // Lump sum growth
    const lumpSumFV = P * Math.pow(1 + i, n);

    // Annuity growth (monthly contributions)
    let annuityFV = 0;
    if (PMT > 0 && contribPerYear > 0) {
      // Nominal rate per payment period
      const ratePerPayment = Math.pow(1 + r / m, m / contribPerYear) - 1;
      const totalPayments = contribPerYear * t;
      if (ratePerPayment === 0) {
        annuityFV = PMT * totalPayments;
      } else {
        annuityFV = PMT * (Math.pow(1 + ratePerPayment, totalPayments) - 1) / ratePerPayment;
        if (isBeginning) {
          annuityFV *= (1 + ratePerPayment);
        }
      }
    }

    return lumpSumFV + annuityFV;
  }

  function calculateRequiredPMT(targetFV, P, rAnnual, t, m, contribPerYear, timing) {
    const r = rAnnual / 100;
    const isBeginning = (timing === 'beginning');
    const lumpSumFV = m === 0 ? P * Math.exp(r * t) : P * Math.pow(1 + r / m, m * t);
    const neededFromAnnuity = targetFV - lumpSumFV;
    if (neededFromAnnuity <= 0) return 0;

    if (m === 0) {
      const factor = r > 0 ? (Math.exp(r * t) - 1) / r : t;
      return (neededFromAnnuity / factor) / contribPerYear;
    }

    const ratePerPayment = Math.pow(1 + r / m, m / contribPerYear) - 1;
    const totalPayments = contribPerYear * t;
    let factor = (Math.pow(1 + ratePerPayment, totalPayments) - 1) / ratePerPayment;
    if (isBeginning) factor *= (1 + ratePerPayment);

    return neededFromAnnuity / factor;
  }

  function renderChart(history, targetYear) {
    if (!chartSvg) return;
    const w = 600;
    const h = 260;
    const padX = 65;
    const padY = 30;
    const plotW = w - padX - 30;
    const plotH = h - padY - 30;

    if (!history || history.length === 0) return;

    const maxVal = history[history.length - 1].total;
    if (maxVal <= 0) return;

    const getX = (yr) => padX + (yr / targetYear) * plotW;
    const getY = (val) => h - padY - (val / maxVal) * plotH;

    // Build stacked area points
    const ptsPrincipal = history.map(d => `${round(getX(d.year), 1)},${round(getY(d.principal), 1)}`);
    const ptsDeposits = history.map(d => `${round(getX(d.year), 1)},${round(getY(d.principal + d.contributions), 1)}`);
    const ptsTotal = history.map(d => `${round(getX(d.year), 1)},${round(getY(d.total), 1)}`);

    const areaTotal = [
      `${round(getX(0), 1)},${h - padY}`,
      ...ptsTotal,
      `${round(getX(targetYear), 1)},${h - padY}`
    ].join(' ');

    const areaDeposits = [
      `${round(getX(0), 1)},${h - padY}`,
      ...ptsDeposits,
      `${round(getX(targetYear), 1)},${h - padY}`
    ].join(' ');

    const areaPrincipal = [
      `${round(getX(0), 1)},${h - padY}`,
      ...ptsPrincipal,
      `${round(getX(targetYear), 1)},${h - padY}`
    ].join(' ');

    chartSvg.innerHTML = `
      <defs>
        <linearGradient id="interestGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#10b981" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#10b981" stop-opacity="0.1"/>
        </linearGradient>
        <linearGradient id="contribGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.1"/>
        </linearGradient>
      </defs>
      <!-- Grid -->
      <line x1="${padX}" y1="${h - padY}" x2="${w - 20}" y2="${h - padY}" stroke="var(--border-subtle)" stroke-width="1"/>
      <line x1="${padX}" y1="${padY}" x2="${w - 20}" y2="${padY}" stroke="var(--border-subtle)" stroke-dasharray="4" stroke-width="1"/>
      <line x1="${padX}" y1="${padY + plotH / 2}" x2="${w - 20}" y2="${padY + plotH / 2}" stroke="var(--border-subtle)" stroke-dasharray="4" stroke-width="1"/>
      <!-- Labels -->
      <text x="${padX - 8}" y="${padY + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">${fmtCurrency(maxVal, 0)}</text>
      <text x="${padX - 8}" y="${padY + plotH / 2 + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">${fmtCurrency(maxVal / 2, 0)}</text>
      <text x="${padX - 8}" y="${h - padY + 4}" font-size="10" fill="var(--text-muted)" text-anchor="end">$0</text>
      <text x="${padX}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr 0</text>
      <text x="${padX + plotW / 2}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${round(targetYear / 2, 0)}</text>
      <text x="${padX + plotW}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${targetYear}</text>
      <!-- Stacked Areas -->
      <polygon points="${areaTotal}" fill="url(#interestGrad)"/>
      <polygon points="${areaDeposits}" fill="url(#contribGrad)"/>
      <polygon points="${areaPrincipal}" fill="rgba(168, 85, 247, 0.4)"/>
      <!-- Outlines -->
      <polyline points="${ptsTotal.join(' ')}" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5"/>
    `;
  }

  function update() {
    const P = state.principal;
    const r = state.annualRate;
    const t = state.years;
    const PMT = state.contribution;
    const m = state.compoundFrequency;
    const contribFreq = state.contribFrequency;
    const timing = state.depositTiming;
    const dec = state.precision;

    const fv = calculateFutureValue(P, r, t, PMT, m, contribFreq, timing);
    const totalDeposits = PMT * contribFreq * t;
    const totalInvested = P + totalDeposits;
    const totalInterest = Math.max(0, fv - totalInvested);
    const apy = calculateAPY(r, m);

    if (elTargetFv && state.activeMode !== 'targetFv') {
      elTargetFv.value = round(fv, 2);
    }

    if (dispFv) dispFv.textContent = fmtCurrency(fv, dec);
    if (dispTotalPrincipal) dispTotalPrincipal.textContent = fmtCurrency(P, dec);
    if (dispTotalContrib) dispTotalContrib.textContent = fmtCurrency(totalDeposits, dec);
    if (dispTotalInterest) dispTotalInterest.textContent = fmtCurrency(totalInterest, dec);
    if (dispApy) dispApy.textContent = `${round(apy, 4)}% APY`;

    // Yearly trajectory data
    const history = [];
    for (let yr = 0; yr <= t; yr++) {
      const yrFV = calculateFutureValue(P, r, yr, PMT, m, contribFreq, timing);
      const yrDeposits = PMT * contribFreq * yr;
      history.push({
        year: yr,
        principal: P,
        contributions: yrDeposits,
        total: yrFV
      });
    }

    renderChart(history, t);

    // Dynamic LLM prompt
    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Compound Interest & Future Value Context
Initial Principal (P): $${round(P, 2)}
Annual Interest Rate (r): ${r}%
Investment Horizon (t): ${t} Years
Periodic Contribution (PMT): $${round(PMT, 2)} (${contribFreq} times/year, ${timing} of period)
Compounding Frequency: ${m === 0 ? 'Continuous' : `${m} times/year`}
--------------------------------------------------
DERIVED FINANCIAL INVARIANTS:
Future Value (FV): $${round(fv, 2)}
Total Contributed Cash: $${round(totalInvested, 2)} (Principal: $${round(P, 2)} + Deposits: $${round(totalDeposits, 2)})
Total Compound Interest Earned: $${round(totalInterest, 2)}
Effective Annual Percentage Yield (APY): ${round(apy, 4)}%
Interest-to-Principal Ratio: ${round((totalInterest / totalInvested) * 100, 2)}%
--------------------------------------------------
GOVERNING CLOSED-FORM IDENTITIES:
Discrete: FV = P(1 + r/m)^(mt) + PMT * [((1 + i_p)^N - 1) / i_p]
Continuous: FV = P * e^(rt) + PMT_ann * [(e^(rt) - 1) / r]
APY = (1 + r/m)^m - 1
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elPrincipal) {
    elPrincipal.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.principal = v;
        update();
      }
    });
  }

  if (elRate) {
    elRate.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.annualRate = v;
        update();
      }
    });
  }

  if (elYears) {
    elYears.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.years = v;
        update();
      }
    });
  }

  if (elContribution) {
    elContribution.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.contribution = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elCompoundFreq) {
    elCompoundFreq.addEventListener('change', (e) => {
      state.compoundFrequency = parseInt(e.target.value, 10);
      update();
    });
  }

  if (elTiming) {
    elTiming.addEventListener('change', (e) => {
      state.depositTiming = e.target.value;
      update();
    });
  }

  if (elTargetFv) {
    // Inversion: calculate required monthly deposit from target future value
    elTargetFv.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.activeMode = 'targetFv';
        const reqPMT = calculateRequiredPMT(v, state.principal, state.annualRate, state.years, state.compoundFrequency, state.contribFrequency, state.depositTiming);
        state.contribution = Math.max(0, reqPMT);
        if (elContribution) elContribution.value = round(state.contribution, 2);
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
