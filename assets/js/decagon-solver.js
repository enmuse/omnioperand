/**
 * OmniOperand — Regular Decagon Bidirectional Solver Engine
 * 9-Variable High-Precision Analytic Geometry Solver with Golden Ratio Invariants
 */

(function () {
  'use strict';

  const SQRT5 = Math.sqrt(5);
  const PHI = (1 + SQRT5) / 2; // ~1.618033988749895 (Golden Ratio)
  const PI = Math.PI;

  // Factor constants relative to side length 'a'
  const K_CIRCUMRADIUS = PHI;                                              // R = a * ϕ ≈ 1.618033988749895
  const K_APOTHEM = Math.sqrt(5 + 2 * SQRT5) / 2;                          // r_i ≈ 1.5388417685876266
  const K_SPAN = Math.sqrt(5 + 2 * SQRT5);                                 // S = 2 * r_i ≈ 3.077683537175253
  const K_PERIMETER = 10;
  const K_AREA = (5 / 2) * Math.sqrt(5 + 2 * SQRT5);                       // ~7.694208842938133
  const K_DIAG_1 = Math.sqrt((5 + SQRT5) / 2);                             // Short diag d1 ≈ 1.902113032590307
  const K_DIAG_2 = PHI * PHI;                                              // Medium diag d2 = a * ϕ² ≈ 2.618033988749895
  const K_DIAG_3 = Math.sqrt(5 + 2 * SQRT5);                               // Long diag d3 = S ≈ 3.077683537175253
  const K_MAIN_DIAMETER = 2 * PHI;                                         // Main diameter d4 = 2R = 2aϕ ≈ 3.23606797749979

  let currentDriver = 'side';
  let precision = 4;
  let currentUnit = 'cm';
  let currentValues = {
    side: 10,
    apothem: 10 * K_APOTHEM,
    circumradius: 10 * K_CIRCUMRADIUS,
    perimeter: 10 * K_PERIMETER,
    area: 100 * K_AREA,
    span: 10 * K_SPAN,
    diag_1: 10 * K_DIAG_1,
    diag_2: 10 * K_DIAG_2,
    main_diameter: 10 * K_MAIN_DIAMETER
  };

  function solveSideFromDriver(driver, value) {
    if (value <= 0 || isNaN(value)) return 0;
    switch (driver) {
      case 'side': return value;
      case 'apothem': return value / K_APOTHEM;
      case 'circumradius': return value / PHI;
      case 'perimeter': return value / 10;
      case 'area': return Math.sqrt(value / K_AREA);
      case 'span': return value / K_SPAN;
      case 'diag_1': return value / K_DIAG_1;
      case 'diag_2': return value / K_DIAG_2;
      case 'main_diameter': return value / K_MAIN_DIAMETER;
      default: return value;
    }
  }

  function computeAllFromSide(a) {
    const safeA = Math.max(0.000001, a);
    return {
      side: safeA,
      apothem: safeA * K_APOTHEM,
      circumradius: safeA * K_CIRCUMRADIUS,
      perimeter: safeA * K_PERIMETER,
      area: safeA * safeA * K_AREA,
      span: safeA * K_SPAN,
      diag_1: safeA * K_DIAG_1,
      diag_2: safeA * K_DIAG_2,
      main_diameter: safeA * K_MAIN_DIAMETER
    };
  }

  function formatNum(num) {
    if (isNaN(num)) return '0';
    if (num >= 1e9 || (num < 1e-4 && num > 0)) {
      return num.toExponential(precision);
    }
    return Number(num.toFixed(precision)).toString();
  }

  function updateDOM(activeKey) {
    const areaUnit = `${currentUnit}²`;

    for (const [key, val] of Object.entries(currentValues)) {
      const inputEl = document.getElementById(`input-${key}`);
      const sliderEl = document.getElementById(`slider-${key}`);
      const unitEl = document.getElementById(`unit-${key}`);
      const cardEl = document.getElementById(`card-${key}`);
      const statusTag = document.getElementById(`status-${key}`);

      if (unitEl) unitEl.textContent = (key === 'area') ? areaUnit : currentUnit;
      if (inputEl && key !== activeKey) inputEl.value = formatNum(val);

      if (sliderEl) {
        const maxVal = Math.max(100, Math.ceil(val * 2));
        sliderEl.max = maxVal;
        sliderEl.value = val;
      }

      if (cardEl && statusTag) {
        if (key === currentDriver) {
          cardEl.classList.add('is-driver');
          statusTag.textContent = 'Input (Driver)';
          statusTag.className = 'param-status-tag input';
        } else {
          cardEl.classList.remove('is-driver');
          statusTag.textContent = 'Calculated';
          statusTag.className = 'param-status-tag calculated';
        }
      }
    }

    updateExactBadges(currentValues.side);
    updateSVGCanvas(currentValues);
    updateLLMPrompt(currentValues);
  }

  function updateExactBadges(a) {
    const aStr = formatNum(a);
    const setExact = (id, str) => {
      const el = document.getElementById(`exact-${id}`);
      if (el) el.innerHTML = str;
    };

    setExact('side', `a = ${aStr}`);
    setExact('apothem', `r<sub>i</sub> = [(${aStr}) · √(5 + 2√5)] / 2`);
    setExact('circumradius', `R = a · ϕ = (${aStr}) · <sup>(1 + √5)</sup>/<sub>2</sub>`);
    setExact('perimeter', `P = 10 · (${aStr})`);
    setExact('area', `A = [5 · (${aStr})<sup>2</sup> / 2] · √(5 + 2√5)`);
    setExact('span', `S = 2r<sub>i</sub> = (${aStr}) · √(5 + 2√5)`);
    setExact('diag_1', `d<sub>1</sub> = (${aStr}) · √[(5 + √5) / 2]`);
    setExact('diag_2', `d<sub>2</sub> = a · ϕ<sup>2</sup> = (${aStr}) · <sup>(3 + √5)</sup>/<sub>2</sub>`);
    setExact('main_diameter', `d<sub>4</sub> = 2R = (${aStr}) · (1 + √5)`);
  }

  function updateSVGCanvas(vals) {
    const polygonEl = document.getElementById('svg-decagon-polygon');
    const verticesGroup = document.getElementById('svg-vertices-group');
    if (!polygonEl || !verticesGroup) return;

    const cx = 200;
    const cy = 200;
    const maxRadius = 150;

    // Decagon with horizontal top and bottom:
    // Angles offset by 18° so top edge is horizontal between (90-18=72°) and (90+18=108°)
    const points = [];
    const coords = [];

    for (let k = 0; k < 10; k++) {
      const angle = (PI / 10) + (k * 2 * PI / 10);
      const vx = cx + maxRadius * Math.cos(angle);
      const vy = cy - maxRadius * Math.sin(angle);
      points.push(`${vx.toFixed(2)},${vy.toFixed(2)}`);
      coords.push({ x: vx, y: vy, angle: angle });
    }

    polygonEl.setAttribute('points', points.join(' '));

    verticesGroup.innerHTML = '';
    coords.forEach((pt, idx) => {
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', pt.x.toFixed(2));
      circle.setAttribute('cy', pt.y.toFixed(2));
      circle.setAttribute('r', '4');
      circle.setAttribute('class', 'svg-vertex-dot');
      circle.setAttribute('data-vertex', idx + 1);

      const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
      title.textContent = `Vertex V${idx + 1} (${pt.x.toFixed(1)}, ${pt.y.toFixed(1)})`;
      circle.appendChild(title);
      verticesGroup.appendChild(circle);
    });

    updateDimensionOverlays(cx, cy, maxRadius, coords, vals);
  }

  function updateDimensionOverlays(cx, cy, R_px, coords, vals) {
    const overlayGroup = document.getElementById('svg-dimension-overlay');
    if (!overlayGroup) return;

    const apothem_px = R_px * Math.cos(PI / 10); // cos(18°)

    // Top horizontal edge midpoint between V0 and V1
    const topMidX = (coords[0].x + coords[1].x) / 2;
    const topMidY = (coords[0].y + coords[1].y) / 2;

    overlayGroup.innerHTML = `
      <circle id="svg-incircle" class="svg-incircle" cx="${cx}" cy="${cy}" r="${apothem_px.toFixed(2)}" />
      <circle id="svg-circumcircle" class="svg-circumcircle" cx="${cx}" cy="${cy}" r="${R_px.toFixed(2)}" />
      <circle cx="${cx}" cy="${cy}" r="3" fill="#38bdf8" />

      <!-- Apothem Line -->
      <line id="dim-apothem" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${topMidX.toFixed(2)}" y2="${topMidY.toFixed(2)}" stroke="#10b981" stroke-dasharray="3 3" />

      <!-- Circumradius Line (to V0) -->
      <line id="dim-circumradius" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#a855f7" stroke-dasharray="3 3" />

      <!-- Main Diameter Line (V0 to V5 through center) -->
      <line id="dim-main_diameter" class="svg-dimension-line" x1="${coords[0].x.toFixed(2)}" y1="${coords[0].y.toFixed(2)}" x2="${coords[5].x.toFixed(2)}" y2="${coords[5].y.toFixed(2)}" stroke="#f59e0b" stroke-dasharray="4 4" />

      <!-- Short Diagonal d1 (V9 to V1 across 2 edges) -->
      <line id="dim-diag_1" class="svg-dimension-line" x1="${coords[9].x.toFixed(2)}" y1="${coords[9].y.toFixed(2)}" x2="${coords[1].x.toFixed(2)}" y2="${coords[1].y.toFixed(2)}" stroke="#ec4899" stroke-dasharray="3 3" />

      <!-- Medium Diagonal d2 (V9 to V2 across 3 edges) -->
      <line id="dim-diag_2" class="svg-dimension-line" x1="${coords[9].x.toFixed(2)}" y1="${coords[9].y.toFixed(2)}" x2="${coords[2].x.toFixed(2)}" y2="${coords[2].y.toFixed(2)}" stroke="#6366f1" stroke-dasharray="3 3" />

      <!-- Span (Flat to flat) -->
      <line id="dim-span" class="svg-dimension-line" x1="${cx}" y1="${cy - apothem_px}" x2="${cx}" y2="${cy + apothem_px}" stroke="#38bdf8" stroke-dasharray="3 2" />

      <!-- Side Length (V1 to V0) -->
      <line id="dim-side" class="svg-dimension-line" x1="${coords[1].x.toFixed(2)}" y1="${coords[1].y.toFixed(2)}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#06b6d4" />
    `;
  }

  function highlightDimension(key) {
    document.querySelectorAll('.svg-dimension-line').forEach(el => el.classList.remove('active'));
    const targetLine = document.getElementById(`dim-${key}`);
    if (targetLine) targetLine.classList.add('active');
  }

  function updateLLMPrompt(vals) {
    const promptEl = document.getElementById('llm-prompt-display');
    if (!promptEl) return;

    const u = currentUnit;
    const promptText = `### SYSTEM DIRECTIVE: Regular Decagon Geometric Verification
You are an expert computational geometer and mathematical reasoning engine.
Refer to the following verified exact parameters for a Regular Decagon:

- Known Input Variable: ${currentDriver.toUpperCase()} = ${formatNum(vals[currentDriver])} ${currentDriver === 'area' ? u + '²' : u}
- Side Length (a): ${formatNum(vals.side)} ${u}
- Inradius / Apothem (r_i): ${formatNum(vals.apothem)} ${u}  [Exact: (a / 2) * √(5 + 2√5) ≈ 1.538842 * a]
- Circumradius (R): ${formatNum(vals.circumradius)} ${u}  [Exact: a * ϕ = a * (1 + √5) / 2 ≈ 1.618034 * a]
- Perimeter (P): ${formatNum(vals.perimeter)} ${u}  [Exact: 10a]
- Area (A): ${formatNum(vals.area)} ${u}²  [Exact: (5/2)a² * √(5 + 2√5) ≈ 7.694209 * a²]
- Span (S): ${formatNum(vals.span)} ${u}  [Exact: 2 * r_i = a * √(5 + 2√5) ≈ 3.077684 * a]
- Short Diagonal (d_1): ${formatNum(vals.diag_1)} ${u}  [Exact: a * √[(5 + √5)/2] ≈ 1.902113 * a]
- Medium Diagonal (d_2): ${formatNum(vals.diag_2)} ${u}  [Exact: a * ϕ² = a * (3 + √5) / 2 ≈ 2.618034 * a]
- Main Diameter (d_4): ${formatNum(vals.main_diameter)} ${u}  [Exact: 2R = a * (1 + √5) ≈ 3.236068 * a]
- Interior Angle: 144° (4π/5 rad) | Exterior / Central Angle: 36° (π/5 rad)
- Number of Diagonals: 35 (10 short d1, 10 medium d2, 10 long d3, 5 main diameters d4)

When answering questions about regular decagons:
1. Note the fundamental identity: The circumradius strictly equals side length times the golden ratio R = a · ϕ.
2. The medium diagonal across 3 edges equals a · ϕ² = a · (1 + ϕ).
3. The flat-to-flat span S equals the diagonal across 4 edges d3 = a · √(5 + 2√5).`;

    promptEl.textContent = promptText;
  }

  function initEvents() {
    ['side', 'apothem', 'circumradius', 'perimeter', 'area', 'span', 'diag_1', 'diag_2', 'main_diameter'].forEach(key => {
      const inputEl = document.getElementById(`input-${key}`);
      const sliderEl = document.getElementById(`slider-${key}`);
      const cardEl = document.getElementById(`card-${key}`);
      const copyBtn = document.getElementById(`copy-${key}`);

      if (inputEl) {
        inputEl.addEventListener('focus', () => {
          setDriver(key);
          highlightDimension(key);
        });

        inputEl.addEventListener('input', (e) => {
          const raw = String(e.target.value).trim().replace(',', '.');
          const val = parseFloat(raw);
          if (!isNaN(val) && val > 0) {
            currentDriver = key;
            const newSide = solveSideFromDriver(key, val);
            currentValues = computeAllFromSide(newSide);
            updateDOM(key);
          }
        });
      }

      if (sliderEl) {
        sliderEl.addEventListener('input', (e) => {
          const raw = String(e.target.value).trim().replace(',', '.');
          const val = parseFloat(raw);
          if (!isNaN(val) && val > 0) {
            setDriver(key);
            const newSide = solveSideFromDriver(key, val);
            currentValues = computeAllFromSide(newSide);
            updateDOM();
          }
        });
      }

      if (cardEl) {
        cardEl.addEventListener('mouseenter', () => highlightDimension(key));
        cardEl.addEventListener('click', (e) => {
          if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
            setDriver(key);
            inputEl?.focus();
          }
        });
      }

      if (copyBtn) {
        copyBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          const val = currentValues[key];
          const text = `${formatNum(val)} ${key === 'area' ? currentUnit + '²' : currentUnit}`;
          navigator.clipboard.writeText(text).then(() => {
            const orig = copyBtn.textContent;
            copyBtn.textContent = '✓ Copied';
            setTimeout(() => copyBtn.textContent = orig, 1500);
          });
        });
      }
    });

    const driverSelect = document.getElementById('driver-select');
    if (driverSelect) {
      driverSelect.addEventListener('change', (e) => setDriver(e.target.value));
    }

    document.querySelectorAll('.unit-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.unit-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentUnit = e.target.getAttribute('data-unit');
        updateDOM();
      });
    });

    document.querySelectorAll('.prec-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.prec-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        precision = parseInt(e.target.getAttribute('data-prec'), 10);
        updateDOM();
      });
    });

    document.querySelectorAll('.proof-header').forEach(header => {
      header.addEventListener('click', () => {
        const card = header.closest('.proof-card');
        card.classList.toggle('open');
      });
    });

    const copyPromptBtn = document.getElementById('copy-llm-prompt-btn');
    if (copyPromptBtn) {
      copyPromptBtn.addEventListener('click', () => {
        const promptEl = document.getElementById('llm-prompt-display');
        if (promptEl) {
          navigator.clipboard.writeText(promptEl.textContent).then(() => {
            const orig = copyPromptBtn.textContent;
            copyPromptBtn.textContent = '✓ Copied Prompt for LLM';
            setTimeout(() => copyPromptBtn.textContent = orig, 2000);
          });
        }
      });
    }

    const copyJsonBtn = document.getElementById('copy-json-btn');
    if (copyJsonBtn) {
      copyJsonBtn.addEventListener('click', () => {
        const payload = {
          calculator: "regular_decagon",
          units: currentUnit,
          input_driver: currentDriver,
          precision: precision,
          parameters: currentValues
        };
        navigator.clipboard.writeText(JSON.stringify(payload, null, 2)).then(() => {
          const orig = copyJsonBtn.textContent;
          copyJsonBtn.textContent = '✓ Copied JSON Data';
          setTimeout(() => copyJsonBtn.textContent = orig, 2000);
        });
      });
    }
  }

  function setDriver(key) {
    currentDriver = key;
    const driverSelect = document.getElementById('driver-select');
    if (driverSelect && driverSelect.value !== key) {
      driverSelect.value = key;
    }
    updateDOM();
  }

  document.addEventListener('DOMContentLoaded', () => {
    initEvents();
    currentValues = computeAllFromSide(10);
    updateDOM();
  });

})();
