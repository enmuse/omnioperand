/**
 * assets/js/circle-sector-solver.js
 * High-Precision Circle Sector, Arc Length & Segment Area Inversion Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    radius: 10,
    angleDeg: 60,
    arcLength: 10.472,
    chordLength: 10.0,
    sagitta: 1.340,
    sectorArea: 52.360,
    segmentArea: 9.059,
    precision: 4,
    activeInput: 'angle'
  };

  // DOM Elements
  const elRadius = document.getElementById('param-radius');
  const elAngle = document.getElementById('param-angle');
  const elArc = document.getElementById('param-arc');
  const elChord = document.getElementById('param-chord');
  const elSagitta = document.getElementById('param-sagitta');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispRadius = document.getElementById('disp-radius');
  const dispAngleDeg = document.getElementById('disp-angle-deg');
  const dispAngleRad = document.getElementById('disp-angle-rad');
  const dispArcLength = document.getElementById('disp-arc-length');
  const dispChordLength = document.getElementById('disp-chord-length');
  const dispSagitta = document.getElementById('disp-sagitta');
  const dispSectorArea = document.getElementById('disp-sector-area');
  const dispSegmentArea = document.getElementById('disp-segment-area');
  const dispPerimeter = document.getElementById('disp-perimeter');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const blueprintSvg = document.getElementById('sector-blueprint-svg');

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

  function computeFromRadiusAndAngle(R, thetaDeg) {
    const thetaRad = thetaDeg * (Math.PI / 180);
    const arc = R * thetaRad;
    const chord = 2 * R * Math.sin(thetaRad / 2);
    const sagitta = R * (1 - Math.cos(thetaRad / 2));
    const sectorArea = 0.5 * R * R * thetaRad;
    const triangleArea = 0.5 * R * R * Math.sin(thetaRad);
    const segmentArea = sectorArea - triangleArea;
    const perimeter = 2 * R + arc;

    return {
      radius: R,
      angleDeg: thetaDeg,
      angleRad: thetaRad,
      arcLength: arc,
      chordLength: chord,
      sagitta: sagitta,
      sectorArea: sectorArea,
      segmentArea: segmentArea,
      perimeter: perimeter
    };
  }

  function renderBlueprint(m) {
    if (!blueprintSvg) return;
    const cx = 200;
    const cy = 180;
    const scaleR = 120;

    const halfAngleRad = (m.angleDeg / 2) * (Math.PI / 180);
    const startAngleRad = -Math.PI / 2 - halfAngleRad;
    const endAngleRad = -Math.PI / 2 + halfAngleRad;

    const x1 = cx + scaleR * Math.cos(startAngleRad);
    const y1 = cy + scaleR * Math.sin(startAngleRad);
    const x2 = cx + scaleR * Math.cos(endAngleRad);
    const y2 = cy + scaleR * Math.sin(endAngleRad);

    const largeArcFlag = m.angleDeg > 180 ? 1 : 0;

    // Sector path: center -> p1 -> arc -> p2 -> z
    const sectorPathD = `M ${cx} ${cy} L ${x1} ${y1} A ${scaleR} ${scaleR} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;

    // Segment path: p1 -> arc -> p2 -> z
    const segmentPathD = `M ${x1} ${y1} A ${scaleR} ${scaleR} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;

    // Midpoint on chord
    const midChordX = (x1 + x2) / 2;
    const midChordY = (y1 + y2) / 2;

    // Midpoint on arc
    const midArcX = cx;
    const midArcY = cy - scaleR;

    blueprintSvg.innerHTML = `
      <defs>
        <radialGradient id="secGrad" cx="50%" cy="100%" r="100%">
          <stop offset="0%" stop-color="var(--accent-blue)" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="var(--accent-blue)" stop-opacity="0.35"/>
        </radialGradient>
      </defs>
      <!-- Shaded Sector -->
      <path d="${sectorPathD}" fill="url(#secGrad)" stroke="var(--accent-blue)" stroke-width="2"/>
      <!-- Shaded Segment -->
      <path d="${segmentPathD}" fill="rgba(16, 185, 129, 0.35)" stroke="var(--accent-emerald)" stroke-width="1.5"/>
      <!-- Chord Line -->
      <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="var(--accent-amber)" stroke-width="2"/>
      <!-- Sagitta Height Line -->
      <line x1="${midChordX}" y1="${midChordY}" x2="${midArcX}" y2="${midArcY}" stroke="var(--accent-rose)" stroke-width="2" stroke-dasharray="3"/>
      <!-- Center Point -->
      <circle cx="${cx}" cy="${cy}" r="4" fill="var(--text-bright)"/>
      <text x="${cx}" y="${cy + 18}" font-size="11" fill="var(--text-muted)" text-anchor="middle">Center (Origin)</text>

      <!-- Radius Callout -->
      <line x1="${cx}" y1="${cy}" x2="${x1}" y2="${y1}" stroke="var(--accent-cyan)" stroke-width="2"/>
      <text x="${(cx + x1) / 2 - 15}" y="${(cy + y1) / 2 + 5}" font-size="11" fill="var(--accent-cyan)" font-weight="600">R = ${m.radius}</text>

      <!-- Labels -->
      <text x="${midArcX}" y="${midArcY - 10}" font-size="11" fill="var(--accent-emerald)" font-weight="600" text-anchor="middle">Arc Length: s = ${round(m.arcLength, 2)}</text>
      <text x="${(x1 + x2) / 2}" y="${midChordY + 16}" font-size="11" fill="var(--accent-amber)" font-weight="600" text-anchor="middle">Chord: c = ${round(m.chordLength, 2)}</text>
      <text x="${cx}" y="${cy - 30}" font-size="12" fill="var(--text-bright)" font-weight="700" text-anchor="middle">θ = ${round(m.angleDeg, 1)}°</text>
    `;
  }

  function update() {
    const R = state.radius;
    const deg = state.angleDeg;
    const dec = state.precision;

    const m = computeFromRadiusAndAngle(R, deg);

    state.arcLength = m.arcLength;
    state.chordLength = m.chordLength;
    state.sagitta = m.sagitta;
    state.sectorArea = m.sectorArea;
    state.segmentArea = m.segmentArea;

    if (elArc && state.activeInput !== 'arc') elArc.value = round(m.arcLength, 3);
    if (elChord && state.activeInput !== 'chord') elChord.value = round(m.chordLength, 3);
    if (elSagitta && state.activeInput !== 'sagitta') elSagitta.value = round(m.sagitta, 3);

    if (dispRadius) dispRadius.textContent = fmtNumber(m.radius, dec);
    if (dispAngleDeg) dispAngleDeg.textContent = `${fmtNumber(m.angleDeg, dec)}°`;
    if (dispAngleRad) dispAngleRad.textContent = `${fmtNumber(m.angleRad, dec)} rad`;
    if (dispArcLength) dispArcLength.textContent = fmtNumber(m.arcLength, dec);
    if (dispChordLength) dispChordLength.textContent = fmtNumber(m.chordLength, dec);
    if (dispSagitta) dispSagitta.textContent = fmtNumber(m.sagitta, dec);
    if (dispSectorArea) dispSectorArea.textContent = fmtNumber(m.sectorArea, dec);
    if (dispSegmentArea) dispSegmentArea.textContent = fmtNumber(m.segmentArea, dec);
    if (dispPerimeter) dispPerimeter.textContent = fmtNumber(m.perimeter, dec);

    renderBlueprint(m);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Circle Sector & Segment Geometry Context
Circle Radius (R): ${m.radius}
Central Angle (θ): ${round(m.angleDeg, dec)}° (${round(m.angleRad, 6)} radians)
--------------------------------------------------
DERIVED GEOMETRIC INVARIANTS:
Arc Length (s): ${round(m.arcLength, dec)}
Chord Length (c): ${round(m.chordLength, dec)}
Sagitta Height (h): ${round(m.sagitta, dec)}
Sector Area (A_sec): ${round(m.sectorArea, dec)}
Segment Area (A_seg): ${round(m.segmentArea, dec)}
Sector Perimeter: ${round(m.perimeter, dec)}
--------------------------------------------------
GOVERNING EXACT FORMULATIONS:
Arc s = R * θ_rad
Chord c = 2R * sin(θ_rad / 2)
Sagitta h = R * (1 - cos(θ_rad / 2))
Sector Area = (1/2) * R² * θ_rad
Segment Area = (1/2) * R² * (θ_rad - sin(θ_rad))
Chord-Sagitta Inversion: R = (c² / (8h)) + (h / 2)
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elRadius) {
    elRadius.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.radius = v;
        state.activeInput = 'radius';
        update();
      }
    });
  }

  if (elAngle) {
    elAngle.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0 && v <= 360) {
        state.angleDeg = v;
        state.activeInput = 'angle';
        update();
      }
    });
  }

  if (elArc) {
    // Inversion: solve angle from arc length
    elArc.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.activeInput = 'arc';
        state.arcLength = v;
        const rad = v / state.radius;
        const deg = rad * (180 / Math.PI);
        if (deg <= 360) {
          state.angleDeg = deg;
          if (elAngle) elAngle.value = round(deg, 2);
          update();
        }
      }
    });
  }

  if (elChord) {
    // Inversion: solve angle from chord length
    elChord.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0 && v <= 2 * state.radius) {
        state.activeInput = 'chord';
        state.chordLength = v;
        const halfRad = Math.asin(v / (2 * state.radius));
        const deg = (2 * halfRad) * (180 / Math.PI);
        state.angleDeg = deg;
        if (elAngle) elAngle.value = round(deg, 2);
        update();
      }
    });
  }

  if (elSagitta) {
    // Inversion: solve radius & angle from chord and sagitta
    elSagitta.addEventListener('input', (e) => {
      const h = parseFloat(e.target.value);
      const c = state.chordLength;
      if (!isNaN(h) && h > 0 && c > 0) {
        state.activeInput = 'sagitta';
        state.sagitta = h;
        // Inversion formula: R = c^2 / (8h) + h / 2
        const R = (c * c) / (8 * h) + (h / 2);
        state.radius = R;
        if (elRadius) elRadius.value = round(R, 3);
        const halfRad = Math.asin(c / (2 * R));
        const deg = (2 * halfRad) * (180 / Math.PI);
        state.angleDeg = deg;
        if (elAngle) elAngle.value = round(deg, 2);
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
