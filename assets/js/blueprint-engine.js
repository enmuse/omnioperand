/**
 * OmniOperand — Interactive Blueprint Engine & Attribution Asset Exporter
 * Provides high-res PNG/SVG rendering, layer toggles, LaTeX/TikZ generation,
 * and academic/commercial backlink attribution tools.
 */

(function () {
  'use strict';

  // State
  let activeTheme = 'dark'; // 'dark' | 'blueprint'
  let layers = {
    grid: true,
    circles: true,
    dims: true,
    labels: true
  };

  function getShapeInfo() {
    const canonicalEl = document.querySelector('link[rel="canonical"]');
    const canonicalUrl = canonicalEl ? canonicalEl.href : window.location.href;
    const titleEl = document.querySelector('title');
    const rawTitle = titleEl ? titleEl.textContent.split('|')[0].trim() : 'Geometric Blueprint';

    // Detect shape from URL, input-n, or title
    let shapeName = 'regular-polygon';
    let n = 8;
    const inputN = document.getElementById('input-n');
    if (inputN && inputN.value) {
      n = parseInt(inputN.value, 10) || 8;
      shapeName = `regular-${n}-gon`;
    } else if (canonicalUrl.includes('octagon')) { shapeName = 'octagon'; n = 8; }
    else if (canonicalUrl.includes('hexagon')) { shapeName = 'hexagon'; n = 6; }
    else if (canonicalUrl.includes('pentagon')) { shapeName = 'pentagon'; n = 5; }
    else if (canonicalUrl.includes('decagon')) { shapeName = 'decagon'; n = 10; }

    return { shapeName, n, canonicalUrl, rawTitle };
  }

  function initBlueprintControls() {
    const svg = document.querySelector('.omni-blueprint-svg') || 
                document.querySelector('.octagon-svg') || 
                document.querySelector('svg[id$="-canvas"]');
    if (!svg) return;

    const wrapper = document.getElementById('blueprint-canvas-wrapper') || svg.closest('.canvas-wrapper');
    const coordDisplay = document.getElementById('blueprint-coord-display');

    // 1. Layer Toggles
    ['grid', 'circles', 'dims', 'labels'].forEach(layerKey => {
      const btn = document.getElementById(`toggle-layer-${layerKey}`);
      if (!btn) return;

      btn.addEventListener('click', () => {
        layers[layerKey] = !layers[layerKey];
        btn.classList.toggle('active', layers[layerKey]);
        applyLayerVisibility(svg, layerKey, layers[layerKey]);
      });
    });

    // Theme Toggle (Dark Grid / Technical Blueprint Cyan)
    const themeBtn = document.getElementById('toggle-blueprint-theme');
    if (themeBtn && wrapper) {
      themeBtn.addEventListener('click', () => {
        activeTheme = (activeTheme === 'dark') ? 'blueprint' : 'dark';
        wrapper.classList.toggle('blueprint-theme-active', activeTheme === 'blueprint');
        themeBtn.classList.toggle('active', activeTheme === 'blueprint');
      });
    }

    // 2. Interactive Coordinate Readouts
    svg.addEventListener('mousemove', (e) => {
      const dot = e.target.closest('.svg-vertex-dot');
      if (dot && coordDisplay) {
        const vNum = dot.getAttribute('data-vertex') || '1';
        const cx = parseFloat(dot.getAttribute('cx') || '200');
        const cy = parseFloat(dot.getAttribute('cy') || '200');
        // Convert canvas (cx, cy) to Cartesian relative to origin (200, 200)
        const cartX = (cx - 200).toFixed(1);
        const cartY = (200 - cy).toFixed(1);
        const angleDeg = Math.round((Math.atan2(200 - cy, cx - 200) * 180 / Math.PI + 360) % 360);

        coordDisplay.textContent = `V${vNum}: (${cartX}, ${cartY})px • ${angleDeg}°`;
        coordDisplay.style.borderColor = 'var(--accent-amber)';
        coordDisplay.style.color = 'var(--accent-amber)';
      }
    });

    svg.addEventListener('mouseleave', () => {
      if (coordDisplay) {
        coordDisplay.textContent = 'Hover vertex for coordinates';
        coordDisplay.style.borderColor = '';
        coordDisplay.style.color = '';
      }
    });

    // 3. Export Buttons
    initExportActions(svg);
    initAttributionActions();
  }

  function applyLayerVisibility(svg, layerKey, isVisible) {
    if (layerKey === 'grid') {
      const gridRect = svg.querySelector('rect[fill*="Grid"]');
      const axes = svg.querySelectorAll('.svg-axis');
      if (gridRect) gridRect.classList.toggle('layer-hidden', !isVisible);
      axes.forEach(a => a.classList.toggle('layer-hidden', !isVisible));
    } else if (layerKey === 'circles') {
      const circles = svg.querySelectorAll('.svg-incircle, .svg-circumcircle, #svg-incircle, #svg-circumcircle');
      circles.forEach(c => c.classList.toggle('layer-hidden', !isVisible));
    } else if (layerKey === 'dims') {
      const dimOverlay = svg.querySelector('#svg-dimension-overlay');
      if (dimOverlay) dimOverlay.classList.toggle('layer-hidden', !isVisible);
    } else if (layerKey === 'labels') {
      const verticesGroup = svg.querySelector('#svg-vertices-group');
      if (verticesGroup) verticesGroup.classList.toggle('layer-hidden', !isVisible);
    }
  }

  function initExportActions(svg) {
    const pngBtn = document.getElementById('btn-export-png');
    const svgBtn = document.getElementById('btn-export-svg');
    const tikzBtn = document.getElementById('btn-export-tikz');
    const { shapeName, n, canonicalUrl } = getShapeInfo();

    // Export PNG (2000x2000 High-Res)
    if (pngBtn) {
      pngBtn.addEventListener('click', () => {
        const origText = pngBtn.innerHTML;
        pngBtn.innerHTML = 'Rendering...';
        exportHighResPNG(svg, `omnioperand-${shapeName}-blueprint.png`, () => {
          pngBtn.innerHTML = '✓ Downloaded!';
          setTimeout(() => pngBtn.innerHTML = origText, 2000);
        });
      });
    }

    // Export Vector SVG
    if (svgBtn) {
      svgBtn.addEventListener('click', () => {
        exportVectorSVG(svg, `omnioperand-${shapeName}-blueprint.svg`);
        const origText = svgBtn.innerHTML;
        svgBtn.innerHTML = '✓ Downloaded!';
        setTimeout(() => svgBtn.innerHTML = origText, 2000);
      });
    }

    // Export LaTeX / TikZ
    if (tikzBtn) {
      tikzBtn.addEventListener('click', () => {
        const tikzCode = generateTikZ(shapeName, n, canonicalUrl);
        navigator.clipboard.writeText(tikzCode).then(() => {
          const origText = tikzBtn.innerHTML;
          tikzBtn.innerHTML = '✓ Copied TikZ!';
          setTimeout(() => tikzBtn.innerHTML = origText, 2000);
        });
      });
    }

    // Scroll to Attribution
    const citeBtn = document.getElementById('btn-open-attribution');
    if (citeBtn) {
      citeBtn.addEventListener('click', () => {
        const licenseBox = document.querySelector('.blueprint-license-box');
        if (licenseBox) {
          licenseBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
          licenseBox.style.boxShadow = '0 0 20px rgba(6, 182, 212, 0.4)';
          setTimeout(() => licenseBox.style.boxShadow = '', 2500);
        }
      });
    }
  }

  function exportHighResPNG(svg, filename, callback) {
    const canvas = document.createElement('canvas');
    const size = 2000;
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    // 1. Fill blueprint dark background
    ctx.fillStyle = (activeTheme === 'blueprint') ? '#040d1c' : '#070a12';
    ctx.fillRect(0, 0, size, size);

    // 2. Draw high-resolution coordinate grid
    ctx.strokeStyle = (activeTheme === 'blueprint') ? 'rgba(56, 189, 248, 0.08)' : 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1.5;
    const step = 50; // 40 grid units across 2000px
    for (let x = 0; x <= size; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, size);
      ctx.stroke();
    }
    for (let y = 0; y <= size; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(size, y);
      ctx.stroke();
    }

    // 3. Serialize SVG with inline CSS definitions
    const serializedSvg = serializeSvgWithStyles(svg);
    const svgBlob = new Blob([serializedSvg], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);
    const img = new Image();

    img.onload = function () {
      // Draw SVG onto canvas
      ctx.drawImage(img, 0, 0, size, size);
      URL.revokeObjectURL(url);

      // 4. Overlay High-DPI Watermark and Attribution Banner at Footer
      ctx.fillStyle = 'rgba(7, 10, 18, 0.85)';
      ctx.fillRect(0, size - 70, size, 70);

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 26px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace';
      ctx.fillText('OMNIOPERAND', 40, size - 26);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '22px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace';
      ctx.fillText('• omnioperand.com • Free for commercial & academic use with backlink attribution', 250, size - 26);

      // 5. Trigger download
      canvas.toBlob((blob) => {
        if (!blob) return;
        const link = document.createElement('a');
        link.download = filename;
        link.href = URL.createObjectURL(blob);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
        if (callback) callback();
      }, 'image/png');
    };

    img.onerror = function () {
      URL.revokeObjectURL(url);
      if (callback) callback();
    };

    img.src = url;
  }

  function exportVectorSVG(svg, filename) {
    const serializedSvg = serializeSvgWithStyles(svg, true);
    const blob = new Blob([serializedSvg], { type: 'image/svg+xml;charset=utf-8' });
    const link = document.createElement('a');
    link.download = filename;
    link.href = URL.createObjectURL(blob);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  }

  function serializeSvgWithStyles(svg, includeLicenseHeader = false) {
    const clone = svg.cloneNode(true);

    // Embed standalone styles inside SVG defs
    let defs = clone.querySelector('defs');
    if (!defs) {
      defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
      clone.insertBefore(defs, clone.firstChild);
    }

    const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
    styleEl.textContent = `
      .svg-axis { stroke: rgba(56, 189, 248, 0.4); stroke-width: 1.5; stroke-dasharray: 4 4; }
      .svg-polygon-shape { fill: rgba(6, 182, 212, 0.12); stroke: #06b6d4; stroke-width: 2.5; stroke-linejoin: round; }
      .svg-incircle { fill: none; stroke: rgba(16, 185, 129, 0.6); stroke-width: 1.5; stroke-dasharray: 5 4; }
      .svg-circumcircle { fill: none; stroke: rgba(168, 85, 247, 0.6); stroke-width: 1.5; stroke-dasharray: 5 4; }
      .svg-dimension-line { stroke-width: 2; }
      .svg-vertex-dot { fill: #06b6d4; stroke: #ffffff; stroke-width: 1.5; }
      .svg-blueprint-meta { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 8px; fill: rgba(148, 163, 184, 0.7); font-weight: 600; }
      .svg-blueprint-watermark { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 8.5px; fill: rgba(56, 189, 248, 0.85); font-weight: 600; }
    `;
    defs.appendChild(styleEl);

    // Ensure watermark is present
    if (!clone.querySelector('.svg-blueprint-watermark')) {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.innerHTML = `
        <text x="14" y="22" class="svg-blueprint-meta">OMNIOPERAND ANALYTIC BLUEPRINT</text>
        <text x="386" y="388" text-anchor="end" class="svg-blueprint-watermark">OmniOperand • omnioperand.com</text>
      `;
      clone.appendChild(g);
    }

    const serializer = new XMLSerializer();
    let xml = serializer.serializeToString(clone);

    if (includeLicenseHeader) {
      const header = `<!--\n` +
        `  OmniOperand Analytic Geometry Blueprint\n` +
        `  Generated by https://omnioperand.com\n` +
        `  License: Creative Commons Attribution 4.0 International (CC BY 4.0)\n` +
        `  Free to use in commercial projects, academia, and research with backlink attribution.\n` +
        `-->\n`;
      xml = header + xml;
    }

    return xml;
  }

  function generateTikZ(shapeName, n, url) {
    const angleStep = 360 / n;
    // Compute starting rotation angle to match site layout
    const offset = (n === 8) ? 22.5 : (n === 6) ? 30 : (n === 5) ? 90 : 18;

    return `% =========================================================================
% OmniOperand Analytic Blueprint — Regular ${shapeName.charAt(0).toUpperCase() + shapeName.slice(1)} (n = ${n})
% Source: ${url}
% License: CC BY 4.0 (Free to use in academia and commerce with attribution)
% Required Attribution: Diagram via OmniOperand (https://omnioperand.com)
% =========================================================================

\\documentclass[tikz, border=10pt]{standalone}
\\usepackage{tikz}

\\begin{document}
\\begin{tikzpicture}[scale=1.2, >=stealth]
  % Coordinate Grid & Axes
  \\draw[step=1cm, gray!20, very thin] (-4,-4) grid (4,4);
  \\draw[->, thick, cyan!70] (-4.2,0) -- (4.2,0) node[right] {$x$};
  \\draw[->, thick, cyan!70] (0,-4.2) -- (0,4.2) node[above] {$y$};

  % Regular ${shapeName.charAt(0).toUpperCase() + shapeName.slice(1)} Polygon
  \\draw[cyan!90!black, very thick, fill=cyan!10]
    (${offset}:3.5cm)
    \\foreach \\k in {1,...,${n - 1}} {
      -- ({${offset} + \\k * ${angleStep}}:3.5cm)
    } -- cycle;

  % Circumcircle & Incircle
  \\draw[dashed, purple!70, thick] (0,0) circle (3.5cm);
  \\draw[dashed, teal!80, thick] (0,0) circle ({3.5 * cos(${180 / n})});

  % Vertices & Center Origin
  \\fill[cyan] (0,0) circle (2pt) node[below right, font=\\tiny] {$O(0,0)$};
  \\foreach \\k in {0,...,${n - 1}} {
    \\fill[cyan!90!black] ({${offset} + \\k * ${angleStep}}:3.5cm) circle (2.5pt);
  }

  % Scale & Attribution Note
  \\node[align=center, font=\\tiny\\sffamily, gray!60] at (0,-4.5) {Generated by OmniOperand • omnioperand.com • CC BY 4.0};
\\end{tikzpicture}
\\end{document}`;
  }

  function initAttributionActions() {
    const { shapeName, canonicalUrl, rawTitle } = getShapeInfo();

    // 1. Copy Web Backlink (HTML)
    const copyHtmlBtn = document.getElementById('copy-backlink-html');
    if (copyHtmlBtn) {
      const htmlSnippet = `<a href="${canonicalUrl}" target="_blank" rel="noopener">Diagram courtesy of OmniOperand</a>`;
      const codeEl = document.getElementById('snippet-backlink-html');
      if (codeEl) codeEl.textContent = htmlSnippet;

      copyHtmlBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(htmlSnippet).then(() => {
          const orig = copyHtmlBtn.textContent;
          copyHtmlBtn.textContent = '✓ Copied HTML';
          setTimeout(() => copyHtmlBtn.textContent = orig, 1800);
        });
      });
    }

    // 2. Copy Academic Citation (BibTeX)
    const copyBibtexBtn = document.getElementById('copy-backlink-bibtex');
    if (copyBibtexBtn) {
      const bibtexSnippet = `@misc{omnioperand_${shapeName},
  title = {${rawTitle}},
  author = {{OmniOperand}},
  year = {2026},
  url = {${canonicalUrl}}
}`;
      const codeEl = document.getElementById('snippet-backlink-bibtex');
      if (codeEl) codeEl.textContent = bibtexSnippet.replace(/\n\s+/g, ' ');

      copyBibtexBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(bibtexSnippet).then(() => {
          const orig = copyBibtexBtn.textContent;
          copyBibtexBtn.textContent = '✓ Copied BibTeX';
          setTimeout(() => copyBibtexBtn.textContent = orig, 1800);
        });
      });
    }
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBlueprintControls);
  } else {
    initBlueprintControls();
  }

})();
