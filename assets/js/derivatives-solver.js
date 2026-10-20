/**
 * assets/js/derivatives-solver.js
 * High-Precision Derivative, Tangent & Normal Line Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    coeffA: 1.0,  // x^3
    coeffB: -3.0, // x^2
    coeffC: 0.0,  // x^1
    coeffD: 2.0,  // x^0
    x0: 2.0,      // evaluation point
    precision: 4
  };

  // DOM Elements
  const elA = document.getElementById('param-coeff-a');
  const elB = document.getElementById('param-coeff-b');
  const elC = document.getElementById('param-coeff-c');
  const elD = document.getElementById('param-coeff-d');
  const elX0 = document.getElementById('param-x0');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispF0 = document.getElementById('disp-f0');
  const dispFPrime = document.getElementById('disp-f-prime');
  const dispSlope = document.getElementById('disp-slope');
  const dispTangentLine = document.getElementById('disp-tangent-line');
  const dispNormalLine = document.getElementById('disp-normal-line');
  const dispSecondDeriv = document.getElementById('disp-second-deriv');
  const dispConcavity = document.getElementById('disp-concavity');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const plotSvg = document.getElementById('derivative-plot-svg');

  function round(val, dec) {
    if (isNaN(val) || !isFinite(val)) return 0;
    return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
  }

  function fmtNumber(val, dec = 4) {
    return round(val, dec).toLocaleString('en-US', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec
    });
  }

  function f(x) {
    return state.coeffA * Math.pow(x, 3) +
           state.coeffB * Math.pow(x, 2) +
           state.coeffC * x +
           state.coeffD;
  }

  function fPrime(x) {
    return 3 * state.coeffA * Math.pow(x, 2) +
           2 * state.coeffB * x +
           state.coeffC;
  }

  function fDoublePrime(x) {
    return 6 * state.coeffA * x +
           2 * state.coeffB;
  }

  function formatDerivativeFunction() {
    const parts = [];
    const a3 = 3 * state.coeffA;
    const b2 = 2 * state.coeffB;
    const c = state.coeffC;

    if (Math.abs(a3) > 1e-6) parts.push(`${round(a3, 3)}x²`);
    if (Math.abs(b2) > 1e-6) parts.push(`${b2 > 0 && parts.length ? '+ ' : ''}${round(b2, 3)}x`);
    if (Math.abs(c) > 1e-6) parts.push(`${c > 0 && parts.length ? '+ ' : ''}${round(c, 3)}`);

    return parts.length > 0 ? parts.join(' ') : '0';
  }

  function formatLineEquation(m, x0, y0) {
    const b = y0 - m * x0;
    const mStr = Math.abs(m - 1) < 1e-6 ? '' : Math.abs(m + 1) < 1e-6 ? '-' : `${round(m, 3)}`;
    const bStr = Math.abs(b) < 1e-6 ? '' : (b > 0 ? ` + ${round(b, 3)}` : ` - ${round(Math.abs(b), 3)}`);
    return `y = ${mStr}x${bStr}`;
  }

  function renderPlot(x0, y0, m) {
    if (!plotSvg) return;
    const w = 460;
    const h = 240;
    const padX = 45;
    const padY = 25;
    const plotW = w - padX - 25;
    const plotH = h - padY - 25;

    const xMin = x0 - 3;
    const xMax = x0 + 3;
    const xRange = xMax - xMin || 1;

    let yMin = y0;
    let yMax = y0;
    const samples = 80;
    const curvePoints = [];

    for (let i = 0; i <= samples; i++) {
      const curX = xMin + (i / samples) * xRange;
      const curY = f(curX);
      if (curY < yMin) yMin = curY;
      if (curY > yMax) yMax = curY;
      curvePoints.push({ x: curX, y: curY });
    }

    const yMargin = Math.max(2, (yMax - yMin) * 0.2);
    const plotYMin = yMin - yMargin;
    const plotYMax = yMax + yMargin;
    const yRange = plotYMax - plotYMin || 1;

    const toSvgX = (x) => padX + ((x - xMin) / xRange) * plotW;
    const toSvgY = (y) => h - padY - ((y - plotYMin) / yRange) * plotH;

    const zeroY = toSvgY(0);
    const ptX = toSvgX(x0);
    const ptY = toSvgY(y0);

    // Tangent Line Endpoints across domain [xMin, xMax]
    const tanX1 = xMin;
    const tanY1 = y0 + m * (tanX1 - x0);
    const tanX2 = xMax;
    const tanY2 = y0 + m * (tanX2 - x0);

    const curvePathStr = curvePoints.map(p => `${round(toSvgX(p.x), 1)},${round(toSvgY(p.y), 1)}`).join(' ');

    plotSvg.innerHTML = `
      <!-- X-Axis -->
      <line x1="${padX}" y1="${zeroY}" x2="${w - 20}" y2="${zeroY}" stroke="var(--border-subtle)" stroke-width="1.5"/>
      <!-- Tangent Line -->
      <line x1="${toSvgX(tanX1)}" y1="${toSvgY(tanY1)}" x2="${toSvgX(tanX2)}" y2="${toSvgY(tanY2)}" stroke="var(--accent-amber)" stroke-width="2" stroke-dasharray="5"/>
      <!-- Function Curve -->
      <polyline points="${curvePathStr}" fill="none" stroke="var(--accent-blue)" stroke-width="2.5"/>
      <!-- Tangency Point -->
      <circle cx="${ptX}" cy="${ptY}" r="5" fill="var(--accent-rose)"/>
      <circle cx="${ptX}" cy="${ptY}" r="8" fill="none" stroke="var(--accent-rose)" stroke-width="1.5" opacity="0.6"/>
      <!-- Callouts -->
      <text x="${ptX + 10}" y="${ptY - 10}" font-size="11" fill="var(--text-bright)" font-weight="700">(${round(x0, 2)}, ${round(y0, 2)})</text>
      <text x="${w - 30}" y="${padY + 15}" font-size="11" fill="var(--accent-amber)" font-weight="600" text-anchor="end">Slope m = ${round(m, 3)}</text>
    `;
  }

  function update() {
    const x0 = state.x0;
    const dec = state.precision;

    const y0 = f(x0);
    const m = fPrime(x0);
    const fDouble = fDoublePrime(x0);

    const tanEq = formatLineEquation(m, x0, y0);
    let normEq = 'Undefined (Vertical)';
    if (Math.abs(m) > 1e-9) {
      const mNorm = -1 / m;
      normEq = formatLineEquation(mNorm, x0, y0);
    } else {
      normEq = `x = ${round(x0, dec)}`;
    }

    const concavityStr = fDouble > 0 ? 'Concave Upward ∪' : fDouble < 0 ? 'Concave Downward ∩' : 'Inflection Point';

    if (dispF0) dispF0.textContent = fmtNumber(y0, dec);
    if (dispFPrime) dispFPrime.textContent = formatDerivativeFunction();
    if (dispSlope) dispSlope.textContent = fmtNumber(m, dec);
    if (dispTangentLine) dispTangentLine.textContent = tanEq;
    if (dispNormalLine) dispNormalLine.textContent = normEq;
    if (dispSecondDeriv) dispSecondDeriv.textContent = fmtNumber(fDouble, dec);
    if (dispConcavity) dispConcavity.textContent = concavityStr;

    renderPlot(x0, y0, m);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Calculus Derivative & Tangent Line Context
Function: f(x) = ${state.coeffA}x³ + ${state.coeffB}x² + ${state.coeffC}x + ${state.coeffD}
Evaluation Point: x₀ = ${x0} ⟹ f(x₀) = ${round(y0, dec)}
--------------------------------------------------
DERIVED DIFFERENTIAL INVARIANTS:
First Derivative Function f'(x): ${formatDerivativeFunction()}
Instantaneous Rate of Change (Slope m): ${round(m, dec)}
Tangent Line Equation: ${tanEq}
Normal Line Equation: ${normEq}
Second Derivative f''(x₀): ${round(fDouble, dec)} (${concavityStr})
Cubic Inflection Point: x = ${state.coeffA !== 0 ? round(-state.coeffB / (3 * state.coeffA), dec) : 'N/A'}
--------------------------------------------------
GOVERNING THEOREMS:
Limit Definition of Derivative: f'(x) = lim_{h ➔ 0} [f(x + h) - f(x)] / h
Point-Slope Form: y - y₀ = m(x - x₀)
Normal Line Slope: m_⟂ = -1 / m (for m ≠ 0)
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elA) {
    elA.addEventListener('input', (e) => {
      state.coeffA = parseFloat(e.target.value) || 0;
      update();
    });
  }

  if (elB) {
    elB.addEventListener('input', (e) => {
      state.coeffB = parseFloat(e.target.value) || 0;
      update();
    });
  }

  if (elC) {
    elC.addEventListener('input', (e) => {
      state.coeffC = parseFloat(e.target.value) || 0;
      update();
    });
  }

  if (elD) {
    elD.addEventListener('input', (e) => {
      state.coeffD = parseFloat(e.target.value) || 0;
      update();
    });
  }

  if (elX0) {
    elX0.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v)) {
        state.x0 = v;
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
