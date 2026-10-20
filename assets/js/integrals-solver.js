/**
 * assets/js/integrals-solver.js
 * High-Precision Definite/Indefinite Integral & Riemann Sum Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    coeffA: 0.5,   // x^3
    coeffB: -1.5,  // x^2
    coeffC: 2.0,   // x^1
    coeffD: 3.0,   // x^0
    boundLower: 0,
    boundUpper: 4,
    partitions: 20,
    precision: 5
  };

  // DOM Elements
  const elA = document.getElementById('param-coeff-a');
  const elB = document.getElementById('param-coeff-b');
  const elC = document.getElementById('param-coeff-c');
  const elD = document.getElementById('param-coeff-d');
  const elLower = document.getElementById('param-bound-lower');
  const elUpper = document.getElementById('param-bound-upper');
  const elPartitions = document.getElementById('param-partitions');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispExactIntegral = document.getElementById('disp-exact-integral');
  const dispAntiderivative = document.getElementById('disp-antiderivative');
  const dispSimpsons = document.getElementById('disp-simpsons');
  const dispTrapezoid = document.getElementById('disp-trapezoid');
  const dispMidpoint = document.getElementById('disp-midpoint');
  const dispAvgValue = document.getElementById('disp-avg-value');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const plotSvg = document.getElementById('integral-plot-svg');

  function round(val, dec) {
    if (isNaN(val) || !isFinite(val)) return 0;
    return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
  }

  function fmtNumber(val, dec = 5) {
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

  function F(x) {
    // Indefinite integral: (a/4)x^4 + (b/3)x^3 + (c/2)x^2 + dx
    return (state.coeffA / 4) * Math.pow(x, 4) +
           (state.coeffB / 3) * Math.pow(x, 3) +
           (state.coeffC / 2) * Math.pow(x, 2) +
           state.coeffD * x;
  }

  function formatAntiderivative() {
    const parts = [];
    const a4 = state.coeffA / 4;
    const b3 = state.coeffB / 3;
    const c2 = state.coeffC / 2;
    const d = state.coeffD;

    if (Math.abs(a4) > 1e-6) parts.push(`${round(a4, 3)}x⁴`);
    if (Math.abs(b3) > 1e-6) parts.push(`${b3 > 0 && parts.length ? '+ ' : ''}${round(b3, 3)}x³`);
    if (Math.abs(c2) > 1e-6) parts.push(`${c2 > 0 && parts.length ? '+ ' : ''}${round(c2, 3)}x²`);
    if (Math.abs(d) > 1e-6) parts.push(`${d > 0 && parts.length ? '+ ' : ''}${round(d, 3)}x`);

    return parts.length > 0 ? parts.join(' ') + ' + C' : 'C';
  }

  function computeNumericalMethods(a, b, N) {
    if (a === b) return { trap: 0, simp: 0, mid: 0 };
    const dx = (b - a) / N;

    // Trapezoidal Rule
    let trapSum = 0.5 * (f(a) + f(b));
    for (let i = 1; i < N; i++) {
      trapSum += f(a + i * dx);
    }
    const trap = trapSum * dx;

    // Midpoint Rule
    let midSum = 0;
    for (let i = 0; i < N; i++) {
      midSum += f(a + (i + 0.5) * dx);
    }
    const mid = midSum * dx;

    // Simpson's Rule (ensure N is even)
    const nEven = N % 2 === 0 ? N : N + 1;
    const dxSimp = (b - a) / nEven;
    let simpSum = f(a) + f(b);
    for (let i = 1; i < nEven; i++) {
      simpSum += (i % 2 === 1 ? 4 : 2) * f(a + i * dxSimp);
    }
    const simp = (dxSimp / 3) * simpSum;

    return { trap, simp, mid };
  }

  function renderPlot(a, b, exactVal) {
    if (!plotSvg) return;
    const w = 460;
    const h = 240;
    const padX = 45;
    const padY = 25;
    const plotW = w - padX - 25;
    const plotH = h - padY - 25;

    // Domain range with padding
    const xMin = Math.min(a, b) - 1;
    const xMax = Math.max(a, b) + 1;
    const xRange = xMax - xMin || 1;

    // Sample y values
    let yMin = 0;
    let yMax = 0;
    const samples = 100;
    const curvePoints = [];

    for (let i = 0; i <= samples; i++) {
      const curX = xMin + (i / samples) * xRange;
      const curY = f(curX);
      if (curY < yMin) yMin = curY;
      if (curY > yMax) yMax = curY;
      curvePoints.push({ x: curX, y: curY });
    }

    // Add margin to y range
    const yMargin = Math.max(1, (yMax - yMin) * 0.15);
    const plotYMin = yMin - yMargin;
    const plotYMax = yMax + yMargin;
    const yRange = plotYMax - plotYMin || 1;

    const toSvgX = (x) => padX + ((x - xMin) / xRange) * plotW;
    const toSvgY = (y) => h - padY - ((y - plotYMin) / yRange) * plotH;

    const zeroY = toSvgY(0);

    // Build shaded area between [a, b]
    const shadePts = [];
    shadePts.push(`${toSvgX(a)},${zeroY}`);
    const shadeSteps = 50;
    for (let i = 0; i <= shadeSteps; i++) {
      const curX = a + (i / shadeSteps) * (b - a);
      shadePts.push(`${toSvgX(curX)},${toSvgY(f(curX))}`);
    }
    shadePts.push(`${toSvgX(b)},${zeroY}`);

    const curvePathStr = curvePoints.map(p => `${round(toSvgX(p.x), 1)},${round(toSvgY(p.y), 1)}`).join(' ');

    plotSvg.innerHTML = `
      <defs>
        <linearGradient id="intGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#10b981" stop-opacity="0.45"/>
          <stop offset="100%" stop-color="#10b981" stop-opacity="0.08"/>
        </linearGradient>
      </defs>
      <!-- X-Axis Line -->
      <line x1="${padX}" y1="${zeroY}" x2="${w - 20}" y2="${zeroY}" stroke="var(--border-subtle)" stroke-width="1.5"/>
      <!-- Bound Markers -->
      <line x1="${toSvgX(a)}" y1="${padY}" x2="${toSvgX(a)}" y2="${h - padY}" stroke="var(--accent-blue)" stroke-width="1" stroke-dasharray="3"/>
      <line x1="${toSvgX(b)}" y1="${padY}" x2="${toSvgX(b)}" y2="${h - padY}" stroke="var(--accent-blue)" stroke-width="1" stroke-dasharray="3"/>
      <!-- Shaded Area -->
      <polygon points="${shadePts.join(' ')}" fill="url(#intGrad)"/>
      <!-- Curve f(x) -->
      <polyline points="${curvePathStr}" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5"/>
      <!-- Text Labels -->
      <text x="${toSvgX(a)}" y="${h - 8}" font-size="11" fill="var(--accent-blue)" font-weight="600" text-anchor="middle">a = ${a}</text>
      <text x="${toSvgX(b)}" y="${h - 8}" font-size="11" fill="var(--accent-blue)" font-weight="600" text-anchor="middle">b = ${b}</text>
      <text x="${w / 2}" y="${padY + 14}" font-size="12" fill="var(--text-bright)" font-weight="600" text-anchor="middle">
        ∫ f(x) dx = ${round(exactVal, 3)}
      </text>
    `;
  }

  function update() {
    const a = state.boundLower;
    const b = state.boundUpper;
    const N = state.partitions;
    const dec = state.precision;

    const exact = F(b) - F(a);
    const num = computeNumericalMethods(a, b, N);
    const avgVal = (b !== a) ? exact / (b - a) : f(a);

    if (dispExactIntegral) dispExactIntegral.textContent = fmtNumber(exact, dec);
    if (dispAntiderivative) dispAntiderivative.textContent = formatAntiderivative();
    if (dispSimpsons) dispSimpsons.textContent = fmtNumber(num.simp, dec);
    if (dispTrapezoid) dispTrapezoid.textContent = fmtNumber(num.trap, dec);
    if (dispMidpoint) dispMidpoint.textContent = fmtNumber(num.mid, dec);
    if (dispAvgValue) dispAvgValue.textContent = fmtNumber(avgVal, dec);

    renderPlot(a, b, exact);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Calculus Definite Integral Context
Integrand Function: f(x) = ${state.coeffA}x³ + ${state.coeffB}x² + ${state.coeffC}x + ${state.coeffD}
Integration Interval: [${a}, ${b}]
--------------------------------------------------
DERIVED ANALYTIC INVARIANTS:
Exact Definite Integral: ${round(exact, dec)}
Indefinite Antiderivative F(x): ${formatAntiderivative()}
Mean Value of Function (f_avg): ${round(avgVal, dec)}
--------------------------------------------------
NUMERICAL RIEMANN APPROXIMATIONS (N = ${N} partitions):
Simpson's Rule: ${round(num.simp, dec)} (Error: ${Math.abs(exact - num.simp).toExponential(3)})
Trapezoidal Rule: ${round(num.trap, dec)} (Error: ${Math.abs(exact - num.trap).toExponential(3)})
Midpoint Rule: ${round(num.mid, dec)} (Error: ${Math.abs(exact - num.mid).toExponential(3)})
--------------------------------------------------
GOVERNING IDENTITIES:
Fundamental Theorem of Calculus: ∫_a^b f(x) dx = F(b) - F(a)
Power Rule of Integration: ∫ xⁿ dx = [xⁿ⁺¹ / (n + 1)] + C
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

  if (elLower) {
    elLower.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v)) {
        state.boundLower = v;
        update();
      }
    });
  }

  if (elUpper) {
    elUpper.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v)) {
        state.boundUpper = v;
        update();
      }
    });
  }

  if (elPartitions) {
    elPartitions.addEventListener('change', (e) => {
      state.partitions = parseInt(e.target.value, 10) || 20;
      update();
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 5;
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
