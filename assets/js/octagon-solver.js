/**
 * OmniOperand — Regular Octagon Bidirectional Solver Engine
 * Complete 8-Variable High-Precision Analytic Geometry Solver
 */

(function () {
  'use strict';

  // Mathematical Constants
  const SQRT2 = Math.SQRT2;
  const PI = Math.PI;
  const RAD_22_5 = PI / 8; // 22.5 degrees

  // Factor constants relative to side length 'a'
  const K_APOTHEM = (1 + SQRT2) / 2;                         // ~1.2071067811865475
  const K_CIRCUMRADIUS = Math.sqrt(4 + 2 * SQRT2) / 2;       // ~1.3065629648763766
  const K_PERIMETER = 8;
  const K_AREA = 2 * (1 + SQRT2);                            // ~4.82842712474619
  const K_SHORT_DIAG = Math.sqrt(2 + SQRT2);                 // ~1.8477590650225735
  const K_SPAN = 1 + SQRT2;                                  // ~2.414213562373095 (Medium Diagonal / Height)
  const K_LONG_DIAG = Math.sqrt(4 + 2 * SQRT2);              // ~2.613125929752753 (2 * Circumradius)

  // Current State
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

  // Unit conversion factors relative to meters
  const UNIT_CONVERSIONS = {
    mm: 0.001,
    cm: 0.01,
    m: 1.0,
    in: 0.0254,
    ft: 0.3048,
    yd: 0.9144
  };

  /**
   * Derive fundamental side length 'a' from any chosen driver variable
   */
  function solveSideFromDriver(driver, value) {
    if (value <= 0 || isNaN(value)) return 0;

    switch (driver) {
      case 'side':
        return value;
      case 'apothem':
        return (2 * value) / (1 + SQRT2);
      case 'circumradius':
        return (2 * value) / Math.sqrt(4 + 2 * SQRT2);
      case 'perimeter':
        return value / 8;
      case 'area':
        return Math.sqrt(value / (2 * (1 + SQRT2)));
      case 'short_diag':
        return value / Math.sqrt(2 + SQRT2);
      case 'span':
        return value / (1 + SQRT2);
      case 'long_diag':
        return value / Math.sqrt(4 + 2 * SQRT2);
      default:
        return value;
    }
  }

  /**
   * Recompute all 8 variables given a side length 'a'
   */
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

  /**
   * Format numbers to selected precision
   */
  function formatNum(num) {
    if (isNaN(num)) return '0';
    if (num >= 1e9 || (num < 1e-4 && num > 0)) {
      return num.toExponential(precision);
    }
    return Number(num.toFixed(precision)).toString();
  }

  /**
   * Update all DOM input elements and exact badges
   */
  function updateDOM(activeKey) {
    const areaUnit = `${currentUnit}²`;

    for (const [key, val] of Object.entries(currentValues)) {
      const inputEl = document.getElementById(`input-${key}`);
      const sliderEl = document.getElementById(`slider-${key}`);
      const unitEl = document.getElementById(`unit-${key}`);
      const cardEl = document.getElementById(`card-${key}`);
      const statusTag = document.getElementById(`status-${key}`);

      if (unitEl) {
        unitEl.textContent = (key === 'area') ? areaUnit : currentUnit;
      }

      if (inputEl && key !== activeKey) {
        inputEl.value = formatNum(val);
      }

      if (sliderEl) {
        // Dynamic slider min/max adjustment around current value
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

    // Update exact formula expressions based on side length
    updateExactBadges(currentValues.side);

    // Update SVG Canvas rendering
    updateSVGCanvas(currentValues);

    // Update LLM prompt text
    updateLLMPrompt(currentValues);
  }

  /**
   * Update exact radical expressions in the parameter cards
   */
  function updateExactBadges(a) {
    const aStr = formatNum(a);
    const setExact = (id, str) => {
      const el = document.getElementById(`exact-${id}`);
      if (el) el.innerHTML = str;
    };

    setExact('side', `a = ${aStr}`);
    setExact('apothem', `r<sub>i</sub> = <sup>(${aStr})·(1+√2)</sup>/<sub>2</sub>`);
    setExact('circumradius', `R = <sup>(${aStr})·√(4+2√2)</sup>/<sub>2</sub>`);
    setExact('perimeter', `P = 8 · (${aStr})`);
    setExact('area', `A = 2(1+√2) · (${aStr})<sup>2</sup>`);
    setExact('short_diag', `d<sub>S</sub> = (${aStr})·√(2+√2)`);
    setExact('span', `S = (${aStr})·(1+√2)`);
    setExact('long_diag', `d<sub>L</sub> = (${aStr})·√(4+2√2)`);
  }

  /**
   * Render dynamic SVG Octagon with coordinate geometry
   */
  function updateSVGCanvas(vals) {
    const polygonEl = document.getElementById('svg-octagon-polygon');
    const verticesGroup = document.getElementById('svg-vertices-group');
    if (!polygonEl || !verticesGroup) return;

    const cx = 200;
    const cy = 200;
    const maxRadius = 150; // SVG canvas radius bound

    // Calculate octagon vertices (stop-sign orientation: horizontal top/bottom)
    const points = [];
    const coords = [];

    for (let k = 0; k < 8; k++) {
      // Angle offset so top edge is horizontal: angles at 67.5, 112.5, 157.5, etc.
      const angle = (PI / 8) + (k * PI / 4);
      const vx = cx + maxRadius * Math.cos(angle);
      const vy = cy - maxRadius * Math.sin(angle); // negative because SVG y is downwards
      points.push(`${vx.toFixed(2)},${vy.toFixed(2)}`);
      coords.push({ x: vx, y: vy, angle: angle });
    }

    polygonEl.setAttribute('points', points.join(' '));

    // Render vertex circles
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

    // Update active dimension lines
    updateDimensionOverlays(cx, cy, maxRadius, coords, vals);
  }

  /**
   * Draw dimension callouts for apothem, circumradius, span, diagonals
   */
  function updateDimensionOverlays(cx, cy, R_px, coords, vals) {
    const overlayGroup = document.getElementById('svg-dimension-overlay');
    if (!overlayGroup) return;

    // Apothem in pixels
    const apothem_px = R_px * Math.cos(PI / 8);

    // Top horizontal edge midpoint: midpoint between V0 (index 0) and V1 (index 1)
    const topMidX = (coords[0].x + coords[1].x) / 2;
    const topMidY = (coords[0].y + coords[1].y) / 2;

    overlayGroup.innerHTML = `
      <!-- Incircle (Apothem) -->
      <circle id="svg-incircle" class="svg-incircle" cx="${cx}" cy="${cy}" r="${apothem_px.toFixed(2)}" />
      <!-- Circumcircle -->
      <circle id="svg-circumcircle" class="svg-circumcircle" cx="${cx}" cy="${cy}" r="${R_px.toFixed(2)}" />

      <!-- Center Origin Dot -->
      <circle cx="${cx}" cy="${cy}" r="3" fill="#38bdf8" />

      <!-- Apothem Line (Center to Top Midpoint) -->
      <line id="dim-apothem" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${topMidX.toFixed(2)}" y2="${topMidY.toFixed(2)}" stroke="#10b981" stroke-dasharray="3 3" />

      <!-- Circumradius Line (Center to V0) -->
      <line id="dim-circumradius" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#a855f7" stroke-dasharray="3 3" />

      <!-- Long Diagonal Line (V0 to V4) -->
      <line id="dim-long_diag" class="svg-dimension-line" x1="${coords[0].x.toFixed(2)}" y1="${coords[0].y.toFixed(2)}" x2="${coords[4].x.toFixed(2)}" y2="${coords[4].y.toFixed(2)}" stroke="#f59e0b" stroke-dasharray="4 4" />

      <!-- Span (Height: Flat to Flat) -->
      <line id="dim-span" class="svg-dimension-line" x1="${cx}" y1="${cy - apothem_px}" x2="${cx}" y2="${cy + apothem_px}" stroke="#38bdf8" stroke-dasharray="3 2" />

      <!-- Short Diagonal (V7 to V1 across 2 sides) -->
      <line id="dim-short_diag" class="svg-dimension-line" x1="${coords[7].x.toFixed(2)}" y1="${coords[7].y.toFixed(2)}" x2="${coords[1].x.toFixed(2)}" y2="${coords[1].y.toFixed(2)}" stroke="#ec4899" stroke-dasharray="3 3" />

      <!-- Side Length Dimension (Top edge V1 to V0) -->
      <line id="dim-side" class="svg-dimension-line" x1="${coords[1].x.toFixed(2)}" y1="${coords[1].y.toFixed(2)}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#06b6d4" />
    `;
  }

  /**
   * Highlight SVG dimension when hovering corresponding card
   */
  function highlightDimension(key) {
    document.querySelectorAll('.svg-dimension-line').forEach(el => el.classList.remove('active'));
    const targetLine = document.getElementById(`dim-${key}`);
    if (targetLine) {
      targetLine.classList.add('active');
    }
  }

  /**
   * Update LLM System Prompt and copyable integration text
   */
  function updateLLMPrompt(vals) {
    const promptEl = document.getElementById('llm-prompt-display');
    if (!promptEl) return;

    const u = currentUnit;
    const promptText = `### SYSTEM DIRECTIVE: Regular Octagon Geometric Verification
You are an expert computational geometer and mathematical reasoning engine.
Refer to the following verified exact parameters for a Regular Octagon:

- Known Input Variable: ${currentDriver.toUpperCase()} = ${formatNum(vals[currentDriver])} ${currentDriver === 'area' ? u + '²' : u}
- Derived Side Length (a): ${formatNum(vals.side)} ${u}
- Inradius / Apothem (r_i): ${formatNum(vals.apothem)} ${u}  [Exact: a * (1 + √2) / 2]
- Circumradius (R): ${formatNum(vals.circumradius)} ${u}  [Exact: a * √(4 + 2√2) / 2]
- Perimeter (P): ${formatNum(vals.perimeter)} ${u}  [Exact: 8a]
- Area (A): ${formatNum(vals.area)} ${u}²  [Exact: 2(1 + √2)a² ≈ 4.828427 * a²]
- Short Diagonal (d_S): ${formatNum(vals.short_diag)} ${u}  [Exact: a * √(2 + √2) ≈ 1.847759 * a]
- Medium Diagonal / Span (S): ${formatNum(vals.span)} ${u}  [Exact: a * (1 + √2) ≈ 2.414214 * a]
- Long Diagonal (d_L): ${formatNum(vals.long_diag)} ${u}  [Exact: a * √(4 + 2√2) ≈ 2.613126 * a]
- Interior Angle: 135° (3π/4 rad) | Exterior / Central Angle: 45° (π/4 rad)
- Number of Diagonals: 20 (8 short, 8 medium, 4 long)

When answering questions about regular octagons:
1. Always state whether the polygon is regular.
2. Show the exact radical expression before giving decimal approximations.
3. Validate answers against the law of cosines: d_S² = 2a² - 2a² cos(135°) = a²(2 + √2).
4. For carpentry/framing with given span S, corner cut-out = (S - a) / 2 = a / √2.`;

    promptEl.textContent = promptText;
  }

  /**
   * Event Handlers Setup
   */
  function initEvents() {
    // Input & Slider listeners for all 8 parameters
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

    // Driver Dropdown selector
    const driverSelect = document.getElementById('driver-select');
    if (driverSelect) {
      driverSelect.addEventListener('change', (e) => {
        setDriver(e.target.value);
      });
    }

    // Unit segmented control
    document.querySelectorAll('.unit-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.unit-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentUnit = e.target.getAttribute('data-unit');
        updateDOM();
      });
    });

    // Precision segmented control
    document.querySelectorAll('.prec-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.prec-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        precision = parseInt(e.target.getAttribute('data-prec'), 10);
        updateDOM();
      });
    });

    // Proofs accordion toggles
    document.querySelectorAll('.proof-header').forEach(header => {
      header.addEventListener('click', () => {
        const card = header.closest('.proof-card');
        card.classList.toggle('open');
      });
    });

    // FAQ toggles
    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => {
        const item = q.closest('.faq-item');
        item.classList.toggle('open');
      });
    });

    // Copy LLM Prompt button
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

    // Copy JSON API button
    const copyJsonBtn = document.getElementById('copy-json-btn');
    if (copyJsonBtn) {
      copyJsonBtn.addEventListener('click', () => {
        const payload = {
          calculator: "regular_octagon",
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

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    initEvents();
    currentValues = computeAllFromSide(10);
    updateDOM();
  });

})();
