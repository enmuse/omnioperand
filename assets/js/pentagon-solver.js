/**
 * OmniOperand — Regular Pentagon Bidirectional Solver Engine
 * 7-Variable High-Precision Analytic Geometry Solver with Golden Ratio Invariants
 */

(function () {
  'use strict';

  const SQRT5 = Math.sqrt(5);
  const PHI = (1 + SQRT5) / 2; // ~1.618033988749895 (Golden Ratio)
  const PI = Math.PI;

  // Factor constants relative to side length 'a'
  const K_APOTHEM = Math.sqrt(25 + 10 * SQRT5) / 10;                // ~0.6881909602355868
  const K_CIRCUMRADIUS = Math.sqrt(50 + 10 * SQRT5) / 10;           // ~0.85065080835204
  const K_PERIMETER = 5;
  const K_AREA = Math.sqrt(25 + 10 * SQRT5) / 4;                    // ~1.720477400588967
  const K_DIAGONAL = PHI;                                           // ~1.618033988749895 (Golden ratio diagonal)
  const K_HEIGHT = Math.sqrt(5 + 2 * SQRT5) / 2;                    // ~1.5388417685876266 (Vertex to flat base)

  let currentDriver = 'side';
  let precision = 4;
  let currentUnit = 'cm';
  let currentValues = {
    side: 10,
    apothem: 10 * K_APOTHEM,
    circumradius: 10 * K_CIRCUMRADIUS,
    perimeter: 10 * K_PERIMETER,
    area: 100 * K_AREA,
    diagonal: 10 * K_DIAGONAL,
    height: 10 * K_HEIGHT
  };

  function solveSideFromDriver(driver, value) {
    if (value <= 0 || isNaN(value)) return 0;
    switch (driver) {
      case 'side': return value;
      case 'apothem': return value / K_APOTHEM;
      case 'circumradius': return value / K_CIRCUMRADIUS;
      case 'perimeter': return value / 5;
      case 'area': return Math.sqrt(value / K_AREA);
      case 'diagonal': return value / PHI;
      case 'height': return value / K_HEIGHT;
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
      diagonal: safeA * K_DIAGONAL,
      height: safeA * K_HEIGHT
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
    setExact('apothem', `r<sub>i</sub> = (${aStr} / 10) · √(25 + 10√5)`);
    setExact('circumradius', `R = (${aStr} / 10) · √(50 + 10√5)`);
    setExact('perimeter', `P = 5 · (${aStr})`);
    setExact('area', `A = [(${aStr})<sup>2</sup> / 4] · √(25 + 10√5)`);
    setExact('diagonal', `d = a · ϕ = (${aStr}) · <sup>(1 + √5)</sup>/<sub>2</sub>`);
    setExact('height', `H = R + r<sub>i</sub> = [(${aStr}) · √(5 + 2√5)] / 2`);
  }

  function updateSVGCanvas(vals) {
    const polygonEl = document.getElementById('svg-pentagon-polygon');
    const verticesGroup = document.getElementById('svg-vertices-group');
    if (!polygonEl || !verticesGroup) return;

    const cx = 200;
    const cy = 200;
    const maxRadius = 150;

    // Pentagon with vertex pointing straight up:
    // Angles at 90°, 90+72=162°, 234°, 306°, 378° (18°)
    const points = [];
    const coords = [];

    for (let k = 0; k < 5; k++) {
      const angle = (PI / 2) + (k * 2 * PI / 5);
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

    const apothem_px = R_px * Math.cos(PI / 5); // cos(36°)

    // Bottom horizontal edge between V2 (234°) and V3 (306°)
    const botMidX = (coords[2].x + coords[3].x) / 2;
    const botMidY = (coords[2].y + coords[3].y) / 2;

    overlayGroup.innerHTML = `
      <circle id="svg-incircle" class="svg-incircle" cx="${cx}" cy="${cy}" r="${apothem_px.toFixed(2)}" />
      <circle id="svg-circumcircle" class="svg-circumcircle" cx="${cx}" cy="${cy}" r="${R_px.toFixed(2)}" />
      <circle cx="${cx}" cy="${cy}" r="3" fill="#38bdf8" />

      <!-- Apothem Line (Center to bottom midpoint) -->
      <line id="dim-apothem" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${botMidX.toFixed(2)}" y2="${botMidY.toFixed(2)}" stroke="#10b981" stroke-dasharray="3 3" />

      <!-- Circumradius Line (Center to top vertex V0) -->
      <line id="dim-circumradius" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#a855f7" stroke-dasharray="3 3" />

      <!-- Golden Ratio Diagonal Line (V1 to V3) -->
      <line id="dim-diagonal" class="svg-dimension-line" x1="${coords[1].x.toFixed(2)}" y1="${coords[1].y.toFixed(2)}" x2="${coords[3].x.toFixed(2)}" y2="${coords[3].y.toFixed(2)}" stroke="#f59e0b" stroke-dasharray="4 4" />

      <!-- Total Height (V0 top vertex to bottom edge midpoint) -->
      <line id="dim-height" class="svg-dimension-line" x1="${cx}" y1="${coords[0].y.toFixed(2)}" x2="${cx}" y2="${botMidY.toFixed(2)}" stroke="#38bdf8" stroke-dasharray="3 2" />

      <!-- Side Length (V2 to V3 on bottom) -->
      <line id="dim-side" class="svg-dimension-line" x1="${coords[2].x.toFixed(2)}" y1="${coords[2].y.toFixed(2)}" x2="${coords[3].x.toFixed(2)}" y2="${coords[3].y.toFixed(2)}" stroke="#06b6d4" />
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
    const promptText = `### SYSTEM DIRECTIVE: Regular Pentagon Geometric Verification
You are an expert computational geometer and mathematical reasoning engine.
Refer to the following verified exact parameters for a Regular Pentagon:

- Known Input Variable: ${currentDriver.toUpperCase()} = ${formatNum(vals[currentDriver])} ${currentDriver === 'area' ? u + '²' : u}
- Side Length (a): ${formatNum(vals.side)} ${u}
- Inradius / Apothem (r_i): ${formatNum(vals.apothem)} ${u}  [Exact: (a / 10) * √(25 + 10√5) ≈ 0.688191 * a]
- Circumradius (R): ${formatNum(vals.circumradius)} ${u}  [Exact: (a / 10) * √(50 + 10√5) ≈ 0.850651 * a]
- Perimeter (P): ${formatNum(vals.perimeter)} ${u}  [Exact: 5a]
- Area (A): ${formatNum(vals.area)} ${u}²  [Exact: (a² / 4) * √(25 + 10√5) ≈ 1.720477 * a²]
- Diagonal (d): ${formatNum(vals.diagonal)} ${u}  [Exact: a * ϕ = a * (1 + √5) / 2 ≈ 1.618034 * a]
- Height / Span (H): ${formatNum(vals.height)} ${u}  [Exact: R + r_i = (a / 2) * √(5 + 2√5) ≈ 1.538842 * a]
- Interior Angle: 108° (3π/5 rad) | Exterior / Central Angle: 72° (2π/5 rad)
- Number of Diagonals: 5 (all congruent, creating the golden pentagram)

When answering questions about regular pentagons:
1. Emphasize the fundamental role of the Golden Ratio ϕ = (1 + √5) / 2 ≈ 1.6180339887.
2. The ratio of diagonal to side length is strictly equal to the golden ratio: d / a = ϕ.
3. The five diagonals intersect to form a smaller inverted central regular pentagon, establishing recursive golden self-similarity.`;

    promptEl.textContent = promptText;
  }

  function initEvents() {
    ['side', 'apothem', 'circumradius', 'perimeter', 'area', 'diagonal', 'height'].forEach(key => {
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
          calculator: "regular_pentagon",
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
