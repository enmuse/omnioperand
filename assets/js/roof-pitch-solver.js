/**
 * assets/js/roof-pitch-solver.js
 * High-Precision Roof Pitch, Rafter Length & Trigonometric Slope Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    pitchIn12: 6,       // 6:12 pitch
    pitchAngleDeg: 26.565,
    pitchPercent: 50.0,
    spanFt: 30,         // Total building width 30 ft
    overhangIn: 12,     // 12 inch horizontal overhang
    precision: 3,
    activeInput: 'pitch'
  };

  // DOM Elements
  const elPitch = document.getElementById('param-pitch');
  const elAngle = document.getElementById('param-angle');
  const elSpan = document.getElementById('param-span');
  const elOverhang = document.getElementById('param-overhang');
  const elPrecision = document.getElementById('precision-select');

  // Metric displays
  const dispPitchRatio = document.getElementById('disp-pitch-ratio');
  const dispAngleDeg = document.getElementById('disp-angle-deg');
  const dispPitchGrade = document.getElementById('disp-pitch-grade');
  const dispRafterLength = document.getElementById('disp-rafter-length');
  const dispTotalRafter = document.getElementById('disp-total-rafter');
  const dispRafterMultiplier = document.getElementById('disp-rafter-multiplier');
  const dispTotalRise = document.getElementById('disp-total-rise');
  const dispPlumbCut = document.getElementById('disp-plumb-cut');
  const dispSeatCut = document.getElementById('disp-seat-cut');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const blueprintSvg = document.getElementById('roof-blueprint-svg');

  function round(val, dec) {
    if (isNaN(val) || !isFinite(val)) return 0;
    return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
  }

  function fmtNumber(val, dec = 3) {
    return round(val, dec).toLocaleString('en-US', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec
    });
  }

  function toFeetAndInches(totalFeet) {
    const feet = Math.floor(totalFeet);
    const inchesDecimal = (totalFeet - feet) * 12;
    const inches = Math.floor(inchesDecimal);
    const sixteenths = Math.round((inchesDecimal - inches) * 16);
    if (sixteenths === 16) {
      return `${feet}' ${inches + 1}"`;
    }
    if (sixteenths === 0) {
      return `${feet}' ${inches}"`;
    }
    return `${feet}' ${inches} ${sixteenths}/16"`;
  }

  function computeRoofMetrics() {
    const risePer12 = state.pitchIn12;
    const runFt = state.spanFt / 2; // Half span
    const overhangFt = state.overhangIn / 12;

    const angleRad = Math.atan(risePer12 / 12);
    const angleDeg = angleRad * (180 / Math.PI);
    const gradePct = (risePer12 / 12) * 100;
    const rafterMultiplier = Math.sqrt(1 + Math.pow(risePer12 / 12, 2));

    const totalRiseFt = runFt * (risePer12 / 12);
    const rafterLineLengthFt = runFt * rafterMultiplier;
    const overhangRafterLengthFt = overhangFt * rafterMultiplier;
    const totalRafterLengthFt = rafterLineLengthFt + overhangRafterLengthFt;

    // Carpentry Cut Angles
    const plumbCutAngle = 90 - angleDeg; // Angle on speed square / miter saw for vertical cuts
    const seatCutAngle = angleDeg;       // Level cut angle

    return {
      risePer12: risePer12,
      angleDeg: angleDeg,
      gradePct: gradePct,
      rafterMultiplier: rafterMultiplier,
      runFt: runFt,
      totalRiseFt: totalRiseFt,
      rafterLineLengthFt: rafterLineLengthFt,
      totalRafterLengthFt: totalRafterLengthFt,
      plumbCutAngle: plumbCutAngle,
      seatCutAngle: seatCutAngle
    };
  }

  function renderBlueprint(m) {
    if (!blueprintSvg) return;
    const w = 460;
    const h = 240;

    const ox = 50;
    const oy = 190;
    const spanPx = 360;
    const halfSpanPx = spanPx / 2;

    // Scaled height
    const maxPxHeight = 110;
    const riseRatio = Math.min(1.2, m.risePer12 / 12);
    const risePx = Math.max(15, riseRatio * halfSpanPx);
    const clampedRisePx = Math.min(maxPxHeight, risePx);

    const peakX = ox + halfSpanPx;
    const peakY = oy - clampedRisePx;
    const rightX = ox + spanPx;

    blueprintSvg.innerHTML = `
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="var(--accent-blue)"/>
        </marker>
      </defs>
      <!-- Base Plate Tie Beam -->
      <line x1="${ox}" y1="${oy}" x2="${rightX}" y2="${oy}" stroke="#475569" stroke-width="3"/>
      <!-- Left Rafter -->
      <line x1="${ox - 20}" y1="${oy + (20 / halfSpanPx) * clampedRisePx}" x2="${peakX}" y2="${peakY}" stroke="var(--accent-blue)" stroke-width="3.5"/>
      <!-- Right Rafter -->
      <line x1="${peakX}" y1="${peakY}" x2="${rightX + 20}" y2="${oy + (20 / halfSpanPx) * clampedRisePx}" stroke="var(--accent-blue)" stroke-width="3.5"/>
      <!-- King Post (Center Line) -->
      <line x1="${peakX}" y1="${oy}" x2="${peakX}" y2="${peakY}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4"/>
      
      <!-- Right Angle at Center Base -->
      <polyline points="${peakX - 12},${oy} ${peakX - 12},${oy - 12} ${peakX},${oy - 12}" fill="none" stroke="#64748b" stroke-width="1"/>
      
      <!-- Dimension Callouts -->
      <!-- Rise -->
      <line x1="${peakX + 10}" y1="${oy}" x2="${peakX + 10}" y2="${peakY}" stroke="var(--accent-emerald)" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
      <text x="${peakX + 18}" y="${oy - clampedRisePx / 2 + 4}" font-size="11" fill="var(--accent-emerald)" font-weight="600">Rise: ${round(m.totalRiseFt, 2)} ft</text>
      
      <!-- Run -->
      <line x1="${ox}" y1="${oy + 18}" x2="${peakX}" y2="${oy + 18}" stroke="var(--accent-cyan)" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
      <text x="${ox + halfSpanPx / 2}" y="${oy + 34}" font-size="11" fill="var(--accent-cyan)" font-weight="600" text-anchor="middle">Run: ${m.runFt} ft</text>

      <!-- Span -->
      <text x="${ox + halfSpanPx}" y="${oy - clampedRisePx - 15}" font-size="13" fill="var(--text-bright)" font-weight="700" text-anchor="middle">Pitch: ${m.risePer12}:12 (${round(m.angleDeg, 1)}°)</text>

      <!-- Rafter Line Label -->
      <text x="${ox + halfSpanPx / 2 - 25}" y="${oy - clampedRisePx / 2 - 10}" font-size="11" fill="var(--accent-blue)" font-weight="600" transform="rotate(-${round(Math.min(45, m.angleDeg), 0)}, ${ox + halfSpanPx / 2 - 25}, ${oy - clampedRisePx / 2 - 10})">
        Rafter: ${toFeetAndInches(m.rafterLineLengthFt)}
      </text>
    `;
  }

  function update() {
    const m = computeRoofMetrics();
    const dec = state.precision;

    if (dispPitchRatio) dispPitchRatio.textContent = `${round(m.risePer12, 2)} / 12`;
    if (dispAngleDeg) dispAngleDeg.textContent = `${round(m.angleDeg, dec)}°`;
    if (dispPitchGrade) dispPitchGrade.textContent = `${round(m.gradePct, 1)}%`;
    if (dispRafterLength) dispRafterLength.textContent = `${toFeetAndInches(m.rafterLineLengthFt)} (${round(m.rafterLineLengthFt, 3)} ft)`;
    if (dispTotalRafter) dispTotalRafter.textContent = `${toFeetAndInches(m.totalRafterLengthFt)} (${round(m.totalRafterLengthFt, 3)} ft)`;
    if (dispRafterMultiplier) dispRafterMultiplier.textContent = `${round(m.rafterMultiplier, 4)}×`;
    if (dispTotalRise) dispTotalRise.textContent = `${toFeetAndInches(m.totalRiseFt)} (${round(m.totalRiseFt, 2)} ft)`;
    if (dispPlumbCut) dispPlumbCut.textContent = `${round(m.plumbCutAngle, 2)}°`;
    if (dispSeatCut) dispSeatCut.textContent = `${round(m.seatCutAngle, 2)}°`;

    renderBlueprint(m);

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Roof Pitch & Rafter Trigonometry Context
Roof Pitch Ratio: ${round(m.risePer12, 3)}:12 (Rise per 12 inches of horizontal run)
Building Total Span: ${state.spanFt} feet | Half Span (Run): ${m.runFt} feet
Eaves Overhang: ${state.overhangIn} inches
--------------------------------------------------
DERIVED TRIGONOMETRIC METRICS:
Pitch Slope Angle: ${round(m.angleDeg, dec)}° (${round(m.angleDeg * (Math.PI / 180), 5)} radians)
Grade Percentage: ${round(m.gradePct, 2)}%
Rafter Length Multiplier: ${round(m.rafterMultiplier, 5)}
Total Ridge Rise: ${round(m.totalRiseFt, 3)} ft (${toFeetAndInches(m.totalRiseFt)})
Common Rafter Line Length: ${round(m.rafterLineLengthFt, 3)} ft (${toFeetAndInches(m.rafterLineLengthFt)})
Total Rafter Length (with overhang): ${round(m.totalRafterLengthFt, 3)} ft (${toFeetAndInches(m.totalRafterLengthFt)})
Miter Saw Plumb Cut Angle: ${round(m.plumbCutAngle, 2)}° | Level Seat Cut Angle: ${round(m.seatCutAngle, 2)}°
--------------------------------------------------
GOVERNING TRIGONOMETRIC FORMULAS:
Angle θ = arctan(Rise_in / 12)
Rafter Multiplier = √(1 + (Rise_in / 12)²)
Rafter Line Length = Run_ft * Multiplier
Plumb Cut Angle = 90° - θ | Level Cut = θ
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elPitch) {
    elPitch.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.pitchIn12 = v;
        state.activeInput = 'pitch';
        const ang = Math.atan(v / 12) * (180 / Math.PI);
        state.pitchAngleDeg = ang;
        if (elAngle) elAngle.value = round(ang, 2);
        update();
      }
    });
  }

  if (elAngle) {
    // Inversion: enter angle in degrees to compute pitch in 12
    elAngle.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0 && v < 90) {
        state.activeInput = 'angle';
        state.pitchAngleDeg = v;
        const rad = v * (Math.PI / 180);
        const pitch12 = 12 * Math.tan(rad);
        state.pitchIn12 = pitch12;
        if (elPitch) elPitch.value = round(pitch12, 2);
        update();
      }
    });
  }

  if (elSpan) {
    elSpan.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.spanFt = v;
        update();
      }
    });
  }

  if (elOverhang) {
    elOverhang.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      state.overhangIn = (!isNaN(v) && v >= 0) ? v : 0;
      update();
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 3;
      update();
    });
  }

  // Quick Pitch preset buttons (e.g. 4:12, 6:12, 8:12, 12:12)
  document.querySelectorAll('[data-preset-pitch]').forEach(btn => {
    btn.addEventListener('click', () => {
      const p = parseFloat(btn.getAttribute('data-preset-pitch'));
      if (p !== undefined && elPitch) {
        elPitch.value = p;
        state.pitchIn12 = p;
        const ang = Math.atan(p / 12) * (180 / Math.PI);
        state.pitchAngleDeg = ang;
        if (elAngle) elAngle.value = round(ang, 2);
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
