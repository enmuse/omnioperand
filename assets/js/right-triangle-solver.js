/**
 * assets/js/right-triangle-solver.js
 * High-Precision Right Triangle Master Bidirectional Solver
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    legA: 3,
    legB: 4,
    hypotenuseC: 5,
    angleAlpha: 36.8699,
    angleBeta: 53.1301,
    altitudeH: 2.4,
    segP: 1.8,
    segQ: 3.2,
    area: 6.0,
    perimeter: 12.0,
    inradius: 1.0,
    circumradius: 2.5,
    precision: 4,
    activeInput: 'legs'
  };

  // DOM Elements
  const elLegA = document.getElementById('param-leg-a');
  const elLegB = document.getElementById('param-leg-b');
  const elHypotenuse = document.getElementById('param-hypotenuse');
  const elAngleAlpha = document.getElementById('param-alpha');
  const elAngleBeta = document.getElementById('param-beta');
  const elArea = document.getElementById('param-area');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispLegA = document.getElementById('disp-leg-a');
  const dispLegB = document.getElementById('disp-leg-b');
  const dispHyp = document.getElementById('disp-hypotenuse');
  const dispAlpha = document.getElementById('disp-alpha');
  const dispBeta = document.getElementById('disp-beta');
  const dispAltitude = document.getElementById('disp-altitude');
  const dispSegP = document.getElementById('disp-seg-p');
  const dispSegQ = document.getElementById('disp-seg-q');
  const dispArea = document.getElementById('disp-area');
  const dispPerimeter = document.getElementById('disp-perimeter');
  const dispInradius = document.getElementById('disp-inradius');
  const dispCircumradius = document.getElementById('disp-circumradius');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const blueprintSvg = document.getElementById('triangle-blueprint-svg');

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

  function solveFromLegs(a, b) {
    const c = Math.sqrt(a * a + b * b);
    const alphaRad = Math.atan(a / b);
    const betaRad = Math.atan(b / a);
    const alphaDeg = alphaRad * (180 / Math.PI);
    const betaDeg = betaRad * (180 / Math.PI);
    const area = 0.5 * a * b;
    const perimeter = a + b + c;
    const h = (a * b) / c;
    const p = (a * a) / c; // projection of a on c
    const q = (b * b) / c; // projection of b on c
    const inradius = (a + b - c) / 2;
    const circumradius = c / 2;

    return {
      a, b, c,
      alphaDeg, betaDeg,
      alphaRad, betaRad,
      area, perimeter,
      h, p, q,
      inradius, circumradius
    };
  }

  function renderBlueprint(m) {
    if (!blueprintSvg) return;
    const w = 400;
    const h = 240;
    const ox = 70;
    const oy = 190;

    // Scale to fit canvas
    const maxPlotW = 260;
    const maxPlotH = 150;
    const scale = Math.min(maxPlotW / m.b, maxPlotH / m.a);

    const pxB = m.b * scale; // horizontal leg b
    const pxA = m.a * scale; // vertical leg a

    // Right angle vertex is at (ox, oy)
    // Top vertex (A) is at (ox, oy - pxA)
    // Right vertex (B) is at (ox + pxB, oy)
    const Ax = ox;
    const Ay = oy - pxA;
    const Bx = ox + pxB;
    const By = oy;
    const Cx = ox;
    const Cy = oy;

    // Altitude foot on hypotenuse AB:
    // Altitude vector from C perpendicular to AB
    const footX = ox + (m.q / m.c) * (Ax - Bx) + pxB;
    const footY = oy - (m.p / m.c) * pxA;

    // Incircle center: (Cx + r, Cy - r)
    const incenterPx = m.inradius * scale;
    const icX = ox + incenterPx;
    const icY = oy - incenterPx;

    blueprintSvg.innerHTML = `
      <!-- Right Angle Square -->
      <polyline points="${ox},${oy - 16} ${ox + 16},${oy - 16} ${ox + 16},${oy}" fill="none" stroke="#64748b" stroke-width="1.5"/>
      <!-- Triangle Fill & Outline -->
      <polygon points="${Cx},${Cy} ${Bx},${By} ${Ax},${Ay}" fill="rgba(59, 130, 246, 0.12)" stroke="var(--accent-blue)" stroke-width="2.5"/>
      <!-- Altitude line -->
      <line x1="${Cx}" y1="${Cy}" x2="${footX}" y2="${footY}" stroke="var(--accent-amber)" stroke-width="1.5" stroke-dasharray="4"/>
      <!-- Inscribed Circle -->
      <circle cx="${icX}" cy="${icY}" r="${incenterPx}" fill="rgba(16, 185, 129, 0.15)" stroke="var(--accent-emerald)" stroke-width="1.5"/>
      
      <!-- Labels -->
      <!-- Leg a (vertical) -->
      <text x="${ox - 15}" y="${oy - pxA / 2 + 4}" font-size="12" fill="var(--accent-cyan)" font-weight="600" text-anchor="end">a = ${round(m.a, 2)}</text>
      <!-- Leg b (horizontal) -->
      <text x="${ox + pxB / 2}" y="${oy + 22}" font-size="12" fill="var(--accent-cyan)" font-weight="600" text-anchor="middle">b = ${round(m.b, 2)}</text>
      <!-- Hypotenuse c -->
      <text x="${ox + pxB / 2 + 10}" y="${oy - pxA / 2 - 10}" font-size="12" fill="var(--accent-blue)" font-weight="700">c = ${round(m.c, 2)}</text>
      <!-- Angle Alpha at vertex A -->
      <text x="${Ax + 8}" y="${Ay + 25}" font-size="10" fill="var(--text-bright)">α = ${round(m.alphaDeg, 1)}°</text>
      <!-- Angle Beta at vertex B -->
      <text x="${Bx - 40}" y="${By - 8}" font-size="10" fill="var(--text-bright)">β = ${round(m.betaDeg, 1)}°</text>
    `;
  }

  function update() {
    const a = state.legA;
    const b = state.legB;
    const dec = state.precision;

    const m = solveFromLegs(a, b);

    state.hypotenuseC = m.c;
    state.angleAlpha = m.alphaDeg;
    state.angleBeta = m.betaDeg;
    state.altitudeH = m.h;
    state.segP = m.p;
    state.segQ = m.q;
    state.area = m.area;
    state.perimeter = m.perimeter;
    state.inradius = m.inradius;
    state.circumradius = m.circumradius;

    if (elHypotenuse && state.activeInput !== 'hyp') elHypotenuse.value = round(m.c, dec);
    if (elAngleAlpha && state.activeInput !== 'alpha') elAngleAlpha.value = round(m.alphaDeg, 2);
    if (elAngleBeta && state.activeInput !== 'beta') elAngleBeta.value = round(m.betaDeg, 2);
    if (elArea && state.activeInput !== 'area') elArea.value = round(m.area, dec);

    if (dispLegA) dispLegA.textContent = fmtNumber(m.a, dec);
    if (dispLegB) dispLegB.textContent = fmtNumber(m.b, dec);
    if (dispHyp) dispHyp.textContent = fmtNumber(m.c, dec);
    if (dispAlpha) dispAlpha.textContent = `${fmtNumber(m.alphaDeg, 2)}°`;
    if (dispBeta) dispBeta.textContent = `${fmtNumber(m.betaDeg, 2)}°`;
    if (dispAltitude) dispAltitude.textContent = fmtNumber(m.h, dec);
    if (dispSegP) dispSegP.textContent = fmtNumber(m.p, dec);
    if (dispSegQ) dispSegQ.textContent = fmtNumber(m.q, dec);
    if (dispArea) dispArea.textContent = fmtNumber(m.area, dec);
    if (dispPerimeter) dispPerimeter.textContent = fmtNumber(m.perimeter, dec);
    if (dispInradius) dispInradius.textContent = fmtNumber(m.inradius, dec);
    if (dispCircumradius) dispCircumradius.textContent = fmtNumber(m.circumradius, dec);

    renderBlueprint(m);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Right Triangle Geometric Invariant Context
Leg a: ${round(m.a, dec)} | Leg b: ${round(m.b, dec)} | Hypotenuse c: ${round(m.c, dec)}
Acute Angles: α = ${round(m.alphaDeg, 4)}° | β = ${round(m.betaDeg, 4)}° (Sum α + β = 90°)
--------------------------------------------------
DERIVED EUCLIDEAN INVARIANTS:
Altitude to Hypotenuse (h_c): ${round(m.h, dec)}
Hypotenuse Projections: p = ${round(m.p, dec)} | q = ${round(m.q, dec)} (Check p + q = c: ${round(m.p + m.q, dec)})
Triangle Area: ${round(m.area, dec)} (Check: (1/2)*a*b = (1/2)*c*h_c)
Perimeter: ${round(m.perimeter, dec)}
Inscribed Circle Radius (r_i): ${round(m.inradius, dec)}
Circumscribed Circle Radius (R = c/2): ${round(m.circumradius, dec)}
--------------------------------------------------
GOVERNING IDENTITIES:
a² + b² = c² (Pythagorean Theorem)
h_c = (a * b) / c
Geometric Mean Theorem: h_c² = p * q
Cathetus Theorem: a² = c * p and b² = c * q
Inradius r_i = (a + b - c) / 2
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elLegA) {
    elLegA.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.legA = v;
        state.activeInput = 'legs';
        update();
      }
    });
  }

  if (elLegB) {
    elLegB.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.legB = v;
        state.activeInput = 'legs';
        update();
      }
    });
  }

  if (elHypotenuse) {
    // Inversion: enter hypotenuse c and solve leg b given current a
    elHypotenuse.addEventListener('input', (e) => {
      const c = parseFloat(e.target.value);
      const a = state.legA;
      if (!isNaN(c) && c > a) {
        state.activeInput = 'hyp';
        const b = Math.sqrt(c * c - a * a);
        state.legB = b;
        if (elLegB) elLegB.value = round(b, 3);
        update();
      }
    });
  }

  if (elAngleAlpha) {
    // Inversion: enter angle alpha and solve leg b = a / tan(alpha)
    elAngleAlpha.addEventListener('input', (e) => {
      const deg = parseFloat(e.target.value);
      if (!isNaN(deg) && deg > 0 && deg < 90) {
        state.activeInput = 'alpha';
        const rad = deg * (Math.PI / 180);
        const b = state.legA / Math.tan(rad);
        state.legB = b;
        if (elLegB) elLegB.value = round(b, 3);
        update();
      }
    });
  }

  if (elArea) {
    // Inversion: enter target area and solve leg b = 2*Area / a
    elArea.addEventListener('input', (e) => {
      const area = parseFloat(e.target.value);
      if (!isNaN(area) && area > 0 && state.legA > 0) {
        state.activeInput = 'area';
        const b = (2 * area) / state.legA;
        state.legB = b;
        if (elLegB) elLegB.value = round(b, 3);
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

  // Preset buttons (3-4-5, 5-12-13, 8-15-17, 1-1-√2)
  document.querySelectorAll('[data-preset-triple]').forEach(btn => {
    btn.addEventListener('click', () => {
      const triple = btn.getAttribute('data-preset-triple').split(',').map(Number);
      if (triple.length === 2 && elLegA && elLegB) {
        elLegA.value = triple[0];
        elLegB.value = triple[1];
        state.legA = triple[0];
        state.legB = triple[1];
        update();
      }
    });
  });

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
