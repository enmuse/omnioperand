/**
 * assets/js/concrete-volume-solver.js
 * High-Precision Concrete Slab, Footing & Column Volume / Bag Count Engine
 * OmniOperand Math Engine (omnioperand.com)
 */

(function () {
  'use strict';

  const state = {
    shapeType: 'slab', // 'slab', 'column', 'footing'
    lengthFt: 20,
    widthFt: 10,
    thicknessIn: 4,
    columnDiameterIn: 12,
    columnHeightFt: 8,
    columnCount: 1,
    wasteMarginPct: 10,
    costPerYard: 150,
    precision: 3
  };

  // DOM Elements
  const elShapeType = document.getElementById('param-shape-type');
  const elLength = document.getElementById('param-length');
  const elWidth = document.getElementById('param-width');
  const elThickness = document.getElementById('param-thickness');
  const elColDiam = document.getElementById('param-col-diam');
  const elColHeight = document.getElementById('param-col-height');
  const elColCount = document.getElementById('param-col-count');
  const elWaste = document.getElementById('param-waste');
  const elCost = document.getElementById('param-cost');
  const elPrecision = document.getElementById('precision-select');

  // Input row containers
  const rowSlabInputs = document.getElementById('row-slab-inputs');
  const rowColInputs = document.getElementById('row-column-inputs');

  // Metric displays
  const dispYardsNet = document.getElementById('disp-yards-net');
  const dispYardsTotal = document.getElementById('disp-yards-total');
  const dispCubicFeet = document.getElementById('disp-cubic-feet');
  const dispCubicMeters = document.getElementById('disp-cubic-meters');
  const dispBags60 = document.getElementById('disp-bags-60');
  const dispBags80 = document.getElementById('disp-bags-80');
  const dispEstCost = document.getElementById('disp-est-cost');
  const dispLlmPrompt = document.getElementById('llm-prompt-display');
  const blueprintSvg = document.getElementById('concrete-blueprint-svg');

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

  function fmtCurrency(val, dec = 2) {
    return '$' + round(val, dec).toLocaleString('en-US', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec
    });
  }

  function computeVolume() {
    let cuFtNet = 0;

    if (state.shapeType === 'slab' || state.shapeType === 'footing') {
      const lengthFt = state.lengthFt;
      const widthFt = state.widthFt;
      const thicknessFt = state.thicknessIn / 12;
      cuFtNet = lengthFt * widthFt * thicknessFt;
    } else if (state.shapeType === 'column') {
      const radiusFt = (state.columnDiameterIn / 2) / 12;
      const heightFt = state.columnHeightFt;
      const count = state.columnCount;
      const singleVol = Math.PI * radiusFt * radiusFt * heightFt;
      cuFtNet = singleVol * count;
    }

    const cuYdNet = cuFtNet / 27;
    const wasteMultiplier = 1 + (state.wasteMarginPct / 100);
    const cuYdTotal = cuYdNet * wasteMultiplier;
    const cuFtTotal = cuFtNet * wasteMultiplier;
    const cuMetersTotal = cuFtTotal * 0.0283168;

    // Premix bag yields:
    // 60-lb bag = 0.45 cu ft
    // 80-lb bag = 0.60 cu ft
    const bags60 = Math.ceil(cuFtTotal / 0.45);
    const bags80 = Math.ceil(cuFtTotal / 0.60);
    const estCost = cuYdTotal * state.costPerYard;

    return {
      cuFtNet: cuFtNet,
      cuYdNet: cuYdNet,
      cuYdTotal: cuYdTotal,
      cuFtTotal: cuFtTotal,
      cuMetersTotal: cuMetersTotal,
      bags60: bags60,
      bags80: bags80,
      estCost: estCost
    };
  }

  function renderBlueprint() {
    if (!blueprintSvg) return;
    const w = 400;
    const h = 260;

    if (state.shapeType === 'slab' || state.shapeType === 'footing') {
      // 3D Isometric Rectangular Slab
      const ox = 70;
      const oy = 110;
      const sx = 180;
      const sy = 40;
      const sz = 70;
      const slabDepth = 25;

      // Top face
      const pTop = [
        `${ox},${oy}`,
        `${ox + sx},${oy - sy}`,
        `${ox + sx + sz},${oy - sy + 30}`,
        `${ox + sz},${oy + 30}`
      ].join(' ');

      // Front face
      const pFront = [
        `${ox},${oy}`,
        `${ox + sz},${oy + 30}`,
        `${ox + sz},${oy + 30 + slabDepth}`,
        `${ox},${oy + slabDepth}`
      ].join(' ');

      // Right face
      const pRight = [
        `${ox + sz},${oy + 30}`,
        `${ox + sx + sz},${oy - sy + 30}`,
        `${ox + sx + sz},${oy - sy + 30 + slabDepth}`,
        `${ox + sz},${oy + 30 + slabDepth}`
      ].join(' ');

      blueprintSvg.innerHTML = `
        <defs>
          <linearGradient id="slabTopGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#475569"/>
            <stop offset="100%" stop-color="#334155"/>
          </linearGradient>
          <linearGradient id="slabSideGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#1e293b"/>
            <stop offset="100%" stop-color="#0f172a"/>
          </linearGradient>
        </defs>
        <polygon points="${pTop}" fill="url(#slabTopGrad)" stroke="#64748b" stroke-width="1.5"/>
        <polygon points="${pRight}" fill="url(#slabSideGrad)" stroke="#64748b" stroke-width="1.5"/>
        <polygon points="${pFront}" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
        
        <!-- Dimension Callouts -->
        <text x="${ox + sx / 2 + 10}" y="${oy - sy - 8}" font-size="11" fill="var(--accent-cyan)" font-weight="600" text-anchor="middle">Length: ${state.lengthFt} ft</text>
        <text x="${ox - 10}" y="${oy + 25}" font-size="11" fill="var(--accent-amber)" font-weight="600" text-anchor="end">Width: ${state.widthFt} ft</text>
        <text x="${ox + sz + 8}" y="${oy + 30 + slabDepth / 2 + 4}" font-size="11" fill="var(--accent-emerald)" font-weight="600">Depth: ${state.thicknessIn} in</text>
      `;
    } else {
      // 3D Isometric Cylinder Column
      const cx = 200;
      const cyTop = 70;
      const rx = 80;
      const ry = 25;
      const colHeight = 120;

      blueprintSvg.innerHTML = `
        <defs>
          <linearGradient id="colBodyGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#334155"/>
            <stop offset="50%" stop-color="#64748b"/>
            <stop offset="100%" stop-color="#1e293b"/>
          </linearGradient>
        </defs>
        <!-- Bottom Ellipse -->
        <ellipse cx="${cx}" cy="${cyTop + colHeight}" rx="${rx}" ry="${ry}" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
        <!-- Body -->
        <rect x="${cx - rx}" y="${cyTop}" width="${rx * 2}" height="${colHeight}" fill="url(#colBodyGrad)"/>
        <!-- Bottom Outline -->
        <path d="M ${cx - rx} ${cyTop + colHeight} A ${rx} ${ry} 0 0 0 ${cx + rx} ${cyTop + colHeight}" fill="none" stroke="#64748b" stroke-width="1.5"/>
        <!-- Top Ellipse -->
        <ellipse cx="${cx}" cy="${cyTop}" rx="${rx}" ry="${ry}" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
        <!-- Dimension Callouts -->
        <line x1="${cx - rx}" y1="${cyTop - 12}" x2="${cx + rx}" y2="${cyTop - 12}" stroke="var(--accent-cyan)" stroke-width="1" stroke-dasharray="3"/>
        <text x="${cx}" y="${cyTop - 18}" font-size="11" fill="var(--accent-cyan)" font-weight="600" text-anchor="middle">Diameter: ${state.columnDiameterIn} in</text>
        <text x="${cx + rx + 12}" y="${cyTop + colHeight / 2 + 4}" font-size="11" fill="var(--accent-emerald)" font-weight="600">Height: ${state.columnHeightFt} ft</text>
      `;
    }
  }

  function update() {
    const res = computeVolume();
    const dec = state.precision;

    if (dispYardsNet) dispYardsNet.textContent = `${fmtNumber(res.cuYdNet, dec)} yd³`;
    if (dispYardsTotal) dispYardsTotal.textContent = `${fmtNumber(res.cuYdTotal, dec)} yd³`;
    if (dispCubicFeet) dispCubicFeet.textContent = `${fmtNumber(res.cuFtTotal, 1)} ft³`;
    if (dispCubicMeters) dispCubicMeters.textContent = `${fmtNumber(res.cuMetersTotal, 2)} m³`;
    if (dispBags60) dispBags60.textContent = `${res.bags60.toLocaleString()} Bags`;
    if (dispBags80) dispBags80.textContent = `${res.bags80.toLocaleString()} Bags`;
    if (dispEstCost) dispEstCost.textContent = fmtCurrency(res.estCost, 0);

    renderBlueprint();

    if (dispLlmPrompt) {
      dispLlmPrompt.textContent = `SYSTEM DIRECTIVE: Verified Concrete Volume & Material Order Context
Shape Geometry: ${state.shapeType.toUpperCase()}
${state.shapeType === 'column'
  ? `Column Diameter: ${state.columnDiameterIn} inches | Height: ${state.columnHeightFt} feet | Quantity: ${state.columnCount}`
  : `Dimensions: ${state.lengthFt} ft Length × ${state.widthFt} ft Width × ${state.thicknessIn} in Depth`}
Waste Margin Factor: ${state.wasteMarginPct}%
--------------------------------------------------
DERIVED VOLUMETRIC METRICS:
Net Volume: ${round(res.cuYdNet, dec)} cubic yards (${round(res.cuFtNet, 2)} ft³)
Order Volume (with ${state.wasteMarginPct}% waste): ${round(res.cuYdTotal, dec)} cubic yards (${round(res.cuFtTotal, 2)} ft³ / ${round(res.cuMetersTotal, 3)} m³)
60-lb Premix Quikrete Bags Required: ${res.bags60} bags (yield 0.45 ft³/bag)
80-lb Premix Quikrete Bags Required: ${res.bags80} bags (yield 0.60 ft³/bag)
Estimated Ready-Mix Concrete Cost (@ $${state.costPerYard}/yd³): $${round(res.estCost, 2)}
--------------------------------------------------
GOVERNING VOLUMETRIC IDENTITIES:
Cubic Yards = (Length_ft * Width_ft * (Thickness_in / 12)) / 27
Cylinder Vol = [π * (Diameter_in / 24)^2 * Height_ft * Count] / 27
1 Cubic Yard ≡ 27 Cubic Feet ≡ 46,656 Cubic Inches ≡ 0.7645549 Cubic Meters
Verification: Machine-calculated by OmniOperand Engine (omnioperand.com)`;
    }
  }

  // Event Listeners
  if (elShapeType) {
    elShapeType.addEventListener('change', (e) => {
      state.shapeType = e.target.value;
      if (rowSlabInputs && rowColInputs) {
        if (state.shapeType === 'column') {
          rowSlabInputs.style.display = 'none';
          rowColInputs.style.display = 'grid';
        } else {
          rowSlabInputs.style.display = 'grid';
          rowColInputs.style.display = 'none';
        }
      }
      update();
    });
  }

  if (elLength) {
    elLength.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.lengthFt = v;
        update();
      }
    });
  }

  if (elWidth) {
    elWidth.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.widthFt = v;
        update();
      }
    });
  }

  if (elThickness) {
    elThickness.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.thicknessIn = v;
        update();
      }
    });
  }

  if (elColDiam) {
    elColDiam.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.columnDiameterIn = v;
        update();
      }
    });
  }

  if (elColHeight) {
    elColHeight.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v > 0) {
        state.columnHeightFt = v;
        update();
      }
    });
  }

  if (elColCount) {
    elColCount.addEventListener('input', (e) => {
      const v = parseInt(e.target.value, 10);
      if (!isNaN(v) && v > 0) {
        state.columnCount = v;
        update();
      }
    });
  }

  if (elWaste) {
    elWaste.addEventListener('change', (e) => {
      state.wasteMarginPct = parseFloat(e.target.value) || 0;
      update();
    });
  }

  if (elCost) {
    elCost.addEventListener('input', (e) => {
      const v = parseFloat(e.target.value);
      if (!isNaN(v) && v >= 0) {
        state.costPerYard = v;
        update();
      }
    });
  }

  if (elPrecision) {
    elPrecision.addEventListener('change', (e) => {
      state.precision = parseInt(e.target.value, 10) || 3;
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
