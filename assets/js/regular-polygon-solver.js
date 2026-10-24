/**
 * OmniOperand — Universal Regular n-Sided Polygon Bidirectional Solver Engine
 * Dynamic Analytic Geometry, Inversion Invariants, and Archimedean Convergence
 */

(function () {
  'use strict';

  const PI = Math.PI;

  // State
  let currentN = 8;
  let currentDriver = 'side';
  let precision = 4;
  let currentUnit = 'cm';

  let currentValues = {
    n: 8,
    side: 10,
    apothem: 0,
    circumradius: 0,
    perimeter: 0,
    area: 0,
    span: 0,
    diagonals_count: 20,
    interior_angle: 135,
    central_angle: 45
  };

  const SHAPE_NAMES = {
    3: 'Equilateral Triangle',
    4: 'Square (Tetragon)',
    5: 'Regular Pentagon',
    6: 'Regular Hexagon',
    7: 'Regular Heptagon',
    8: 'Regular Octagon',
    9: 'Regular Nonagon',
    10: 'Regular Decagon',
    11: 'Regular Hendecagon',
    12: 'Regular Dodecagon',
    15: 'Regular Pentadecagon',
    16: 'Regular Hexadecagon',
    20: 'Regular Icosagon',
    24: 'Regular Icositetragon',
    50: 'Regular Pentecontagon',
    100: 'Regular Hectagon',
    1000: 'Regular Chiliagon'
  };

  function solveSideFromDriver(driver, value, n) {
    if (value <= 0 || isNaN(value)) return 0;
    const anglePiN = PI / n;
    const tanPiN = Math.tan(anglePiN);
    const sinPiN = Math.sin(anglePiN);

    switch (driver) {
      case 'side':
        return value;
      case 'perimeter':
        return value / n;
      case 'apothem':
        return 2 * value * tanPiN;
      case 'circumradius':
        return 2 * value * sinPiN;
      case 'area':
        return Math.sqrt((4 * value * tanPiN) / n);
      case 'span':
        if (n % 2 === 0) {
          // Span is 2 * apothem for even n
          return value * tanPiN;
        } else {
          // Height from vertex to base for odd n: H = a / (2 * tan(pi / (2n)))
          return 2 * value * Math.tan(PI / (2 * n));
        }
      default:
        return value;
    }
  }

  function computeAll(n, a) {
    const safeN = Math.max(3, Math.min(1000, Math.round(n)));
    const safeA = Math.max(0.000001, a);

    const anglePiN = PI / safeN;
    const tanPiN = Math.tan(anglePiN);
    const sinPiN = Math.sin(anglePiN);

    const apothem = safeA / (2 * tanPiN);
    const circumradius = safeA / (2 * sinPiN);
    const perimeter = safeN * safeA;
    const area = (safeN * safeA * safeA) / (4 * tanPiN);

    let span = 0;
    if (safeN % 2 === 0) {
      span = 2 * apothem; // Flat-to-flat span
    } else {
      span = apothem + circumradius; // Total height (vertex to base) = safeA / (2 * Math.tan(PI / (2 * safeN)))
    }

    const diagCount = (safeN * (safeN - 3)) / 2;
    const centralAngleDeg = 360 / safeN;
    const interiorAngleDeg = ((safeN - 2) * 180) / safeN;

    return {
      n: safeN,
      side: safeA,
      apothem: apothem,
      circumradius: circumradius,
      perimeter: perimeter,
      area: area,
      span: span,
      diagonals_count: diagCount,
      interior_angle: interiorAngleDeg,
      central_angle: centralAngleDeg
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

    // 1. Update Name & Subtitle
    const nameEl = document.getElementById('polygon-name-display');
    const nDisplay = document.getElementById('n-badge-display');
    const shapeTitle = SHAPE_NAMES[currentN] || `Regular ${currentN}-gon`;
    if (nameEl) nameEl.textContent = shapeTitle;
    if (nDisplay) nDisplay.textContent = `n = ${currentN}`;

    // 2. Update n input & slider
    const inputN = document.getElementById('input-n');
    const sliderN = document.getElementById('slider-n');
    if (inputN && activeKey !== 'n') inputN.value = currentN;
    if (sliderN && activeKey !== 'n') sliderN.value = Math.min(100, currentN);

    // 3. Update Span Label (Span vs Height depending on parity)
    const spanTitleEl = document.getElementById('title-span');
    if (spanTitleEl) {
      spanTitleEl.innerHTML = (currentN % 2 === 0)
        ? `Span (Flat-to-Flat) <span class="param-symbol">S</span>`
        : `Height (Vertex-to-Base) <span class="param-symbol">H</span>`;
    }

    // 4. Update Parameter Cards
    for (const [key, val] of Object.entries(currentValues)) {
      if (key === 'n') continue;
      const inputEl = document.getElementById(`input-${key}`);
      const sliderEl = document.getElementById(`slider-${key}`);
      const unitEl = document.getElementById(`unit-${key}`);
      const cardEl = document.getElementById(`card-${key}`);
      const statusTag = document.getElementById(`status-${key}`);

      if (unitEl) {
        if (key === 'area') unitEl.textContent = areaUnit;
        else if (key === 'interior_angle' || key === 'central_angle') unitEl.textContent = '°';
        else if (key === 'diagonals_count') unitEl.textContent = '';
        else unitEl.textContent = currentUnit;
      }

      if (inputEl && key !== activeKey) {
        inputEl.value = (key === 'diagonals_count') ? Math.round(val) : formatNum(val);
      }

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

    // 5. Update Exact Radical / Trigonometric Badges
    updateExactBadges(currentN, currentValues.side);

    // 6. Update Archimedean Efficiency Convergence
    updateArchimedeanEfficiency(currentValues);

    // 7. Update Dynamic SVG Canvas
    updateSVGCanvas(currentValues);

    // 8. Update LLM System Prompt
    updateLLMPrompt(currentValues);
  }

  function updateExactBadges(n, a) {
    const aStr = formatNum(a);
    const setExact = (id, str) => {
      const el = document.getElementById(`exact-${id}`);
      if (el) el.innerHTML = str;
    };

    setExact('side', `a = ${aStr}`);
    setExact('perimeter', `P = ${n} · (${aStr})`);
    setExact('diagonals_count', `N<sub>d</sub> = ${n}(${n - 3})/2 = ${(n * (n - 3)) / 2}`);
    setExact('central_angle', `β = 360° / ${n} = ${formatNum(360 / n)}°`);
    setExact('interior_angle', `α = (${n} - 2)·180° / ${n} = ${formatNum(((n - 2) * 180) / n)}°`);

    // Special constructible radicals
    if (n === 3) {
      setExact('apothem', `r<sub>i</sub> = (${aStr}) · √3 / 6`);
      setExact('circumradius', `R = (${aStr}) · √3 / 3`);
      setExact('area', `A = (√3 / 4) · (${aStr})<sup>2</sup>`);
      setExact('span', `H = (${aStr}) · √3 / 2`);
    } else if (n === 4) {
      setExact('apothem', `r<sub>i</sub> = (${aStr}) / 2`);
      setExact('circumradius', `R = (${aStr}) · √2 / 2`);
      setExact('area', `A = (${aStr})<sup>2</sup>`);
      setExact('span', `S = (${aStr})`);
    } else if (n === 5) {
      setExact('apothem', `r<sub>i</sub> = [(${aStr}) / 10] · √(25 + 10√5)`);
      setExact('circumradius', `R = [(${aStr}) / 10] · √(50 + 10√5)`);
      setExact('area', `A = [(${aStr})<sup>2</sup> / 4] · √(25 + 10√5)`);
      setExact('span', `H = [(${aStr}) / 2] · √(5 + 2√5)`);
    } else if (n === 6) {
      setExact('apothem', `r<sub>i</sub> = (${aStr}) · √3 / 2`);
      setExact('circumradius', `R = a = ${aStr}`);
      setExact('area', `A = [3√3 / 2] · (${aStr})<sup>2</sup>`);
      setExact('span', `S = (${aStr}) · √3`);
    } else if (n === 8) {
      setExact('apothem', `r<sub>i</sub> = [(${aStr}) · (1 + √2)] / 2`);
      setExact('circumradius', `R = [(${aStr}) · √(4 + 2√2)] / 2`);
      setExact('area', `A = 2(1 + √2) · (${aStr})<sup>2</sup>`);
      setExact('span', `S = (${aStr}) · (1 + √2)`);
    } else if (n === 10) {
      setExact('apothem', `r<sub>i</sub> = [(${aStr}) / 2] · √(5 + 2√5)`);
      setExact('circumradius', `R = (${aStr}) · <sup>(1 + √5)</sup>/<sub>2</sub>`);
      setExact('area', `A = [5 · (${aStr})<sup>2</sup> / 2] · √(5 + 2√5)`);
      setExact('span', `S = (${aStr}) · √(5 + 2√5)`);
    } else if (n === 12) {
      setExact('apothem', `r<sub>i</sub> = [(${aStr}) · (2 + √3)] / 2`);
      setExact('circumradius', `R = (${aStr}) · √(2 + √3)`);
      setExact('area', `A = 3(2 + √3) · (${aStr})<sup>2</sup>`);
      setExact('span', `S = (${aStr}) · (2 + √3)`);
    } else {
      // General Trigonometric Exact Form
      setExact('apothem', `r<sub>i</sub> = (${aStr}) / [2 · tan(π/${n})]`);
      setExact('circumradius', `R = (${aStr}) / [2 · sin(π/${n})]`);
      setExact('area', `A = [${n} · (${aStr})<sup>2</sup>] / [4 · tan(π/${n})]`);
      if (n % 2 === 0) {
        setExact('span', `S = (${aStr}) / tan(π/${n})`);
      } else {
        setExact('span', `H = (${aStr}) / [2 · tan(π/${2 * n})]`);
      }
    }
  }

  function updateArchimedeanEfficiency(vals) {
    const effAreaEl = document.getElementById('archimedes-area-ratio');
    const effPerimEl = document.getElementById('archimedes-perim-ratio');
    const progressEl = document.getElementById('archimedes-progress-bar');

    if (!effAreaEl || !effPerimEl) return;

    // Circumcircle area and circumference
    const circleArea = PI * vals.circumradius * vals.circumradius;
    const circlePerim = 2 * PI * vals.circumradius;

    const areaRatio = (vals.area / circleArea) * 100;
    const perimRatio = (vals.perimeter / circlePerim) * 100;

    effAreaEl.textContent = `${areaRatio.toFixed(3)}% of Circle`;
    effPerimEl.textContent = `${perimRatio.toFixed(3)}% of Circle`;

    if (progressEl) {
      progressEl.style.width = `${Math.min(100, areaRatio)}%`;
    }
  }

  function updateSVGCanvas(vals) {
    const polygonEl = document.getElementById('svg-polygon-shape-body');
    const verticesGroup = document.getElementById('svg-vertices-group');
    if (!polygonEl || !verticesGroup) return;

    const cx = 200;
    const cy = 200;
    const maxRadius = 150;
    const n = vals.n;

    // Orientation: for even n, orient flat top/bottom; for odd n, point upwards
    let startAngle = (n % 2 === 0) ? (PI / n) : (PI / 2);

    const points = [];
    const coords = [];

    for (let k = 0; k < n; k++) {
      const angle = startAngle + (k * 2 * PI) / n;
      const vx = cx + maxRadius * Math.cos(angle);
      const vy = cy - maxRadius * Math.sin(angle);
      points.push(`${vx.toFixed(2)},${vy.toFixed(2)}`);
      coords.push({ x: vx, y: vy, angle: angle });
    }

    polygonEl.setAttribute('points', points.join(' '));

    // Render vertex circles (limit rendering dots to n <= 40 for performance)
    verticesGroup.innerHTML = '';
    if (n <= 40) {
      coords.forEach((pt, idx) => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', pt.x.toFixed(2));
        circle.setAttribute('cy', pt.y.toFixed(2));
        circle.setAttribute('r', n > 20 ? '3' : '4');
        circle.setAttribute('class', 'svg-vertex-dot');
        circle.setAttribute('data-vertex', idx + 1);

        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        title.textContent = `Vertex V${idx + 1} (${pt.x.toFixed(1)}, ${pt.y.toFixed(1)})`;
        circle.appendChild(title);
        verticesGroup.appendChild(circle);
      });
    }

    updateDimensionOverlays(cx, cy, maxRadius, coords, vals);
  }

  function updateDimensionOverlays(cx, cy, R_px, coords, vals) {
    const overlayGroup = document.getElementById('svg-dimension-overlay');
    if (!overlayGroup) return;

    const n = vals.n;
    const apothem_px = R_px * Math.cos(PI / n);

    let overlayHTML = `
      <circle id="svg-incircle" class="svg-incircle" cx="${cx}" cy="${cy}" r="${apothem_px.toFixed(2)}" />
      <circle id="svg-circumcircle" class="svg-circumcircle" cx="${cx}" cy="${cy}" r="${R_px.toFixed(2)}" />
      <circle cx="${cx}" cy="${cy}" r="3" fill="#38bdf8" />
    `;

    // Apothem line to first edge midpoint
    if (coords.length >= 2) {
      const edgeMidX = (coords[0].x + coords[1].x) / 2;
      const edgeMidY = (coords[0].y + coords[1].y) / 2;

      overlayHTML += `
        <!-- Apothem Line -->
        <line id="dim-apothem" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${edgeMidX.toFixed(2)}" y2="${edgeMidY.toFixed(2)}" stroke="#10b981" stroke-dasharray="3 3" />
        
        <!-- Circumradius Line -->
        <line id="dim-circumradius" class="svg-dimension-line" x1="${cx}" y1="${cy}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#a855f7" stroke-dasharray="3 3" />

        <!-- Side Edge Line -->
        <line id="dim-side" class="svg-dimension-line" x1="${coords[1].x.toFixed(2)}" y1="${coords[1].y.toFixed(2)}" x2="${coords[0].x.toFixed(2)}" y2="${coords[0].y.toFixed(2)}" stroke="#06b6d4" />
      `;

      // Span line
      if (n % 2 === 0) {
        // Flat to flat vertical
        overlayHTML += `
          <line id="dim-span" class="svg-dimension-line" x1="${cx}" y1="${cy - apothem_px}" x2="${cx}" y2="${cy + apothem_px}" stroke="#38bdf8" stroke-dasharray="3 2" />
        `;
      } else {
        // Top vertex to bottom base
        overlayHTML += `
          <line id="dim-span" class="svg-dimension-line" x1="${cx}" y1="${cy - R_px}" x2="${cx}" y2="${cy + apothem_px}" stroke="#38bdf8" stroke-dasharray="3 2" />
        `;
      }
    }

    overlayGroup.innerHTML = overlayHTML;
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
    const n = vals.n;
    const name = SHAPE_NAMES[n] || `Regular ${n}-gon`;

    const promptText = `### SYSTEM DIRECTIVE: Universal Regular Polygon Verification (${name}, n = ${n})
You are an expert computational geometer and mathematical reasoning engine.
Refer to the following verified exact parameters:

- Polygon Order: n = ${n} sides (${name})
- Known Driver: ${currentDriver.toUpperCase()} = ${formatNum(vals[currentDriver])} ${currentDriver === 'area' ? u + '²' : u}
- Side Length (a): ${formatNum(vals.side)} ${u}
- Inradius / Apothem (r_i): ${formatNum(vals.apothem)} ${u}  [Formula: a / (2 · tan(π/${n}))]
- Circumradius (R): ${formatNum(vals.circumradius)} ${u}  [Formula: a / (2 · sin(π/${n}))]
- Perimeter (P): ${formatNum(vals.perimeter)} ${u}  [Formula: ${n} · a]
- Area (A): ${formatNum(vals.area)} ${u}²  [Formula: (${n} · a²) / (4 · tan(π/${n}))]
- ${n % 2 === 0 ? 'Flat-to-Flat Span (S)' : 'Vertex-to-Base Height (H)'}: ${formatNum(vals.span)} ${u}
- Total Diagonals: ${vals.diagonals_count}  [Formula: n(n - 3) / 2]
- Central / Exterior Angle: ${(360 / n).toFixed(4)}° (2π/${n} rad)
- Interior Angle: ${(((n - 2) * 180) / n).toFixed(4)}° (π(1 - 2/${n}) rad)
- Archimedean Circle Area Coverage: ${((vals.area / (PI * vals.circumradius * vals.circumradius)) * 100).toFixed(3)}%

Mathematical Verification Directives:
1. All regular n-gons are cyclic (inscribed in radius R) and tangential (circumscribed around inradius r_i).
2. The ratio r_i / R strictly equals cos(π/n).
3. The k-th diagonal chord skipping k edges strictly satisfies d_k = 2R · sin(kπ/n) = a · sin(kπ/n) / sin(π/n).
4. As n ➔ ∞, Area ➔ πR² and Perimeter ➔ 2πR.`;

    promptEl.textContent = promptText;
  }

  function initEvents() {
    // 1. Presets Buttons
    document.querySelectorAll('.preset-n-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const nVal = parseInt(e.target.getAttribute('data-n'), 10);
        if (nVal >= 3) {
          document.querySelectorAll('.preset-n-btn').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
          currentN = nVal;
          const currentA = solveSideFromDriver(currentDriver, currentValues[currentDriver], currentN);
          currentValues = computeAll(currentN, currentA);
          updateDOM();
        }
      });
    });

    // 2. N Input and Slider
    const inputN = document.getElementById('input-n');
    const sliderN = document.getElementById('slider-n');

    if (inputN) {
      inputN.addEventListener('input', (e) => {
        let val = parseInt(e.target.value, 10);
        if (!isNaN(val) && val >= 3) {
          currentN = Math.min(1000, val);
          const currentA = solveSideFromDriver(currentDriver, currentValues[currentDriver], currentN);
          currentValues = computeAll(currentN, currentA);
          updateDOM('n');
        }
      });
    }

    if (sliderN) {
      sliderN.addEventListener('input', (e) => {
        let val = parseInt(e.target.value, 10);
        if (!isNaN(val) && val >= 3) {
          currentN = val;
          const currentA = solveSideFromDriver(currentDriver, currentValues[currentDriver], currentN);
          currentValues = computeAll(currentN, currentA);
          updateDOM();
        }
      });
    }

    // 3. Parameter Inputs & Sliders
    ['side', 'apothem', 'circumradius', 'perimeter', 'area', 'span'].forEach(key => {
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
            const newSide = solveSideFromDriver(key, val, currentN);
            currentValues = computeAll(currentN, newSide);
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
            const newSide = solveSideFromDriver(key, val, currentN);
            currentValues = computeAll(currentN, newSide);
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

    // 4. Driver Dropdown
    const driverSelect = document.getElementById('driver-select');
    if (driverSelect) {
      driverSelect.addEventListener('change', (e) => setDriver(e.target.value));
    }

    // 5. Units & Precision Segmented Controls
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

    // 6. Accordion Proof Cards & FAQs
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

    // 7. Copy LLM Prompt & JSON Buttons
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
          calculator: "universal_regular_polygon",
          n: currentN,
          shape_name: SHAPE_NAMES[currentN] || `Regular ${currentN}-gon`,
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

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    initEvents();

    // Check for URL query parameter ?n=
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const nParam = parseInt(urlParams.get('n'), 10);
      if (!isNaN(nParam) && nParam >= 3 && nParam <= 1000) {
        currentN = nParam;
        const nInput = document.getElementById('input-n');
        if (nInput) nInput.value = currentN;
      }
    } catch (e) {
      // Fallback to default
    }

    currentValues = computeAll(currentN, 10);
    updateDOM();
  });

})();
