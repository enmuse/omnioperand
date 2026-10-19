/**
 * OmniOperand — Regular Hexagon Bidirectional Solver Engine
 * 8-Variable High-Precision Analytic Geometry Solver
 */

(function () {
  'use strict';

  const SQRT3 = Math.sqrt(3);
  const PI = Math.PI;

  // Factor constants relative to side length 'a'
  const K_APOTHEM = SQRT3 / 2;             // ~0.8660254037844386
  const K_CIRCUMRADIUS = 1.0;              // Exactly 1.0 * a
  const K_PERIMETER = 6;
  const K_AREA = (3 * SQRT3) / 2;          // ~2.598076211353316
  const K_SHORT_DIAG = SQRT3;              // ~1.7320508075688772
  const K_SPAN = SQRT3;                    // ~1.7320508075688772 (Flat-to-flat span = 2 * Apothem)
  const K_LONG_DIAG = 2.0;                 // 2 * a (Maximal vertex diameter)

  let currentDriver = 'side';
  let precision = 4;
  let currentUnit = 'cm';
  let currentValues = {
    side: 10,
    apothem: 10 * K_APOTHEM,
    circumradius: 10 * K_CIRCUMRADIUS,
    perimeter: 10 * K_PERIMETER,
    area: 100 * K_AREA,
    short_diag: 10 * K_SHORT_DIAG,
    span: 10 * K_SPAN,
    long_diag: 10 * K_LONG_DIAG
  };

  function solveSideFromDriver(driver, value) {
    if (value <= 0 || isNaN(value)) return 0;
    switch (driver) {
      case 'side': return value;
      case 'apothem': return (2 * value) / SQRT3;
      case 'circumradius': return value;
      case 'perimeter': return value / 6;
      case 'area': return Math.sqrt((2 * value) / (3 * SQRT3));
      case 'short_diag': return value / SQRT3;
      case 'span': return value / SQRT3;
      case 'long_diag': return value / 2;
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
      short_diag: safeA * K_SHORT_DIAG,
      span: safeA * K_SPAN,
      long_diag: safeA * K_LONG_DIAG
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
    setExact('apothem', `r<sub>i</sub> = (${aStr} · √3) / 2`);
    setExact('circumradius', `R = a = ${aStr}`);
    setExact('perimeter', `P = 6 · (${aStr})`);
    setExact('area', `A = (3√3 / 2) · (${aStr})<sup>2</sup>`);
    setExact('short_diag', `d<sub>S</sub> = (${aStr}) · √3`);
    setExact('span', `S = 2r<sub>i</sub> = (${aStr}) · √3`);
    setExact('long_diag', `d<sub>L</sub> = 2 · (${aStr})`);
  }

  function updateSVGCanvas(vals) {
    const polygonEl = document.getElementById('svg-hexagon-polygon');
    const verticesGroup = document.getElementById('svg-vertices-group');
    if (!polygonEl || !verticesGroup) return;

    const cx = 200;
    const cy = 200;
    const maxRadius = 150;

    // Hexagon vertices with horizontal top and bottom:
    // Angles at 30°, 90°, 150°, 210°, 270°, 330° or rotated so vertices align symmetrically
    // For flat top/bottom edges, vertices are at angles: 0, 60, 120, 180, 240, 300 (or shifted 30°)
    // With 30° shift: top edge is horizontal between (150-30 = 60° and 120°)
    const points = [];
    const coords = [];

    for (let k = 0; k < 6; k++) {
      const angle = (PI / 6) + (k * PI / 3); // 30, 90, 150, 210, 270, 330 deg
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
      circle.setAttribute('r', '4.5');
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

    const apothem_px = R_px * (SQRT3 / 2);

    // Midpoint of top edge between V0 (30°) and V1 (90°)
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

      <!-- Long Diagonal (V0 to V3 through center) -->
      <line id="dim-long_diag" class="svg-dimension-line" x1="${coords[0].x.toFixed(2)}" y1="${coords[0].y.toFixed(2)}" x2="${coords[3].x.toFixed(2)}" y2="${coords[3].y.toFixed(2)}" stroke="#f59e0b" stroke-dasharray="4 4" />

      <!-- Short Diagonal (V5 to V1 across 2 edges) -->
      <line id="dim-short_diag" class="svg-dimension-line" x1="${coords[5].x.toFixed(2)}" y1="${coords[5].y.toFixed(2)}" x2="${coords[1].x.toFixed(2)}" y2="${coords[1].y.toFixed(2)}" stroke="#ec4899" stroke-dasharray="3 3" />

      <!-- Span (Flat to flat distance) -->
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
    const promptText = `### SYSTEM DIRECTIVE: Regular Hexagon Geometric Verification
You are an expert computational geometer and mathematical reasoning engine.
Refer to the following verified exact parameters for a Regular Hexagon:

- Known Input Variable: ${currentDriver.toUpperCase()} = ${formatNum(vals[currentDriver])} ${currentDriver === 'area' ? u + '²' : u}
- Side Length (a): ${formatNum(vals.side)} ${u}
- Inradius / Apothem (r_i): ${formatNum(vals.apothem)} ${u}  [Exact: (a * √3) / 2 ≈ 0.866025 * a]
- Circumradius (R): ${formatNum(vals.circumradius)} ${u}  [Exact: R = a]
- Perimeter (P): ${formatNum(vals.perimeter)} ${u}  [Exact: 6a]
- Area (A): ${formatNum(vals.area)} ${u}²  [Exact: (3√3 / 2)a² ≈ 2.598076 * a²]
- Short Diagonal (d_S): ${formatNum(vals.short_diag)} ${u}  [Exact: a * √3 ≈ 1.732051 * a]
- Medium Diagonal / Span (S): ${formatNum(vals.span)} ${u}  [Exact: 2 * r_i = a * √3 ≈ 1.732051 * a]
- Long Diagonal (d_L): ${formatNum(vals.long_diag)} ${u}  [Exact: 2a = 2R]
- Interior Angle: 120° (2π/3 rad) | Exterior / Central Angle: 60° (π/3 rad)
- Number of Diagonals: 9 (6 short, 3 long)

When answering questions about regular hexagons:
1. Note the unique property: The circumradius R is always strictly equal to side length a.
2. The regular hexagon uniquely tiles the 2D Euclidean plane (hexagonal tessellation / honeycomb conjecture).
3. Area equals 6 equilateral triangles: A = 6 * (a²√3 / 4) = (3√3 / 2)a².`;

    promptEl.textContent = promptText;
  }

  function initEvents() {
    ['side', 'apothem', 'circumradius', 'perimeter', 'area', 'short_diag', 'span', 'long_diag'].forEach(key => {
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
          const val = parseFloat(e.target.value);
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
          const val = parseFloat(e.target.value);
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

    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => {
        const item = q.closest('.faq-item');
        item.classList.toggle('open');
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
          calculator: "regular_hexagon",
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
