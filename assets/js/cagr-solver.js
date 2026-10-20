/**
 * assets/js/cagr-solver.js
 * Compound Annual Growth Rate (CAGR) & Valuation Inverter Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    startVal: 100000,
    endVal: 350000,
    years: 5,
    cagr: 28.47,
    precision: 4,
    activeInput: 'endVal'
  };

  // DOM Elements
  const elStart = document.getElementById('param-start');
  const elEnd = document.getElementById('param-end');
  const elYears = document.getElementById('param-years');
  const elCagr = document.getElementById('param-cagr');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispCagr = document.getElementById('disp-cagr');
  const dispTotalReturn = document.getElementById('disp-total-return');
  const dispDollarGain = document.getElementById('disp-dollar-gain');
  const dispDoublingTime = document.getElementById('disp-doubling-time');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const chartSvg = document.getElementById('cagr-chart-svg');

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

  function calculateCAGR(v0, vn, n) {
    if (v0 <= 0 || vn <= 0 || n <= 0) return 0;
    return (Math.pow(vn / v0, 1 / n) - 1) * 100;
  }

  function calculateEndingValue(v0, cagrPct, n) {
    const g = cagrPct / 100;
    return v0 * Math.pow(1 + g, n);
  }

  function calculateStartingValue(vn, cagrPct, n) {
    const g = cagrPct / 100;
    return vn / Math.pow(1 + g, n);
  }

  function calculateYearsNeeded(v0, vn, cagrPct) {
    const g = cagrPct / 100;
    if (g <= 0 || v0 <= 0 || vn <= 0) return 0;
    return Math.log(vn / v0) / Math.log(1 + g);
  }

  function renderChart(v0, vn, n, cagrPct) {
    if (!chartSvg) return;
    const w = 600;
    const h = 260;
    const padX = 65;
    const padY = 30;
    const plotW = w - padX - 30;
    const plotH = h - padY - 30;

    const g = cagrPct / 100;
    const maxVal = Math.max(v0, vn) * 1.1;
    const minVal = 0;

    const steps = 30;
    const ptsCAGR = [];
    const ptsLinear = [];

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * n;
      const cagrVal = v0 * Math.pow(1 + g, t);
      const linearVal = v0 + (vn - v0) * (t / n);

      const x = padX + (t / n) * plotW;
      const yCAGR = h - padY - (cagrVal / maxVal) * plotH;
      const yLinear = h - padY - (linearVal / maxVal) * plotH;

      ptsCAGR.push(`${round(x, 1)},${round(yCAGR, 1)}`);
      ptsLinear.push(`${round(x, 1)},${round(yLinear, 1)}`);
    }

    const areaCAGR = [
      `${round(padX, 1)},${h - padY}`,
      ...ptsCAGR,
      `${round(padX + plotW, 1)},${h - padY}`
    ].join(' ');

    chartSvg.innerHTML = `
      <defs>
        <linearGradient id="cagrGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.5"/>
          <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.05"/>
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
      <text x="${padX + plotW / 2}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${round(n / 2, 1)}</text>
      <text x="${padX + plotW}" y="${h - 10}" font-size="10" fill="var(--text-muted)" text-anchor="middle">Yr ${n}</text>
      <!-- Trajectories -->
      <polygon points="${areaCAGR}" fill="url(#cagrGrad)"/>
      <polyline points="${ptsLinear.join(' ')}" fill="none" stroke="var(--text-muted)" stroke-dasharray="4" stroke-width="1.5"/>
      <polyline points="${ptsCAGR.join(' ')}" fill="none" stroke="var(--accent-violet)" stroke-width="2.5"/>
    `;
  }

  function update() {
    const v0 = state.startVal;
    const vn = state.endVal;
    const n = state.years;
    const dec = state.precision;

    const cagr = calculateCAGR(v0, vn, n);
    state.cagr = cagr;

    if (elCagr && state.activeInput !== 'cagr') {
      elCagr.value = round(cagr, dec);
    }

    const totalReturn = v0 > 0 ? ((vn - v0) / v0) * 100 : 0;
    const dollarGain = vn - v0;
    const doublingTime = cagr > 0 ? Math.log(2) / Math.log(1 + cagr / 100) : 0;

    if (dispCagr) dispCagr.textContent = `${round(cagr, dec)}%`;
    if (dispTotalReturn) dispTotalReturn.textContent = `${round(totalReturn, 2)}%`;
    if (dispDollarGain) dispDollarGain.textContent = fmtCurrency(dollarGain, 2);
    if (dispDoublingTime) {
      dispDoublingTime.textContent = doublingTime > 0 ? `${round(doublingTime, 2)} Years` : 'N/A';
    }

    renderChart(v0, vn, n, cagr);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Compound Annual Growth Rate (CAGR) Context
Beginning Value (V0): $${round(v0, 2)}
Ending Value (Vn): $${round(vn, 2)}
Time Horizon (n): ${n} Years
--------------------------------------------------
DERIVED FINANCIAL INVARIANTS:
Compound Annual Growth Rate (CAGR): ${round(cagr, dec)}%
Absolute Total Return (AR): ${round(totalReturn, 2)}%
Absolute Dollar Appreciation: $${round(dollarGain, 2)}
Exact Doubling Period: ${round(doublingTime, 2)} years (Rule of 72 est: ${round(72 / cagr, 2)} yrs)
--------------------------------------------------
GOVERNING CLOSED-FORM IDENTITIES:
CAGR = (Vn / V0)^(1/n) - 1
Vn = V0 * (1 + CAGR)^n
V0 = Vn / (1 + CAGR)^n
n = ln(Vn / V0) / ln(1 + CAGR)
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  if (elStart) {
    elStart.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.startVal = v;
        state.activeInput = 'startVal';
        update();
      }
    });
  }

  if (elEnd) {
    elEnd.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.endVal = v;
        state.activeInput = 'endVal';
        update();
      }
    });
  }

  if (elYears) {
    elYears.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.years = v;
        state.activeInput = 'years';
        update();
      }
    });
  }

  if (elCagr) {
    // Inversion: enter target CAGR to compute required Ending Value
    elCagr.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v)) {
        state.activeInput = 'cagr';
        state.cagr = v;
        const newEnd = calculateEndingValue(state.startVal, v, state.years);
        state.endVal = newEnd;
        if (elEnd) elEnd.value = round(newEnd, 2);
        update();
      }
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 4;
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
