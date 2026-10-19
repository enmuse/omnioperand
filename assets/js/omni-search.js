/**
 * OmniOperand — Global Search & Navigation Controller (omni-search.js)
 * Instant fuzzy matching, keyboard navigation (Cmd+K / '/'), and Theme Toggle
 */

(function () {
  'use strict';

  // Calculator & Hub Index Database
  const SEARCH_INDEX = [
    {
      title: "Universal Regular Polygon Calculator",
      category: "Geometry > 2D Geometry > Shapes",
      url: "/geometry/2d/shapes/regular-polygon/",
      keywords: ["regular polygon", "n-gon", "n-sided", "polygon", "triangle", "square", "pentagon", "hexagon", "heptagon", "octagon", "nonagon", "decagon", "dodecagon", "icosagon", "apothem", "circumradius", "diagonals", "area", "archimedes"]
    },
    {
      title: "Regular Octagon Calculator",
      category: "Geometry > 2D Geometry > Shapes",
      url: "/geometry/2d/shapes/octagon/",
      keywords: ["octagon", "polygon", "8-sided", "apothem", "circumradius", "diagonal", "stop sign", "area", "perimeter"]
    },
    {
      title: "Regular Hexagon Calculator",
      category: "Geometry > 2D Geometry > Shapes",
      url: "/geometry/2d/shapes/hexagon/",
      keywords: ["hexagon", "polygon", "6-sided", "honeycomb", "apothem", "circumradius", "diagonal", "hex bolt", "area"]
    },
    {
      title: "Regular Pentagon Calculator",
      category: "Geometry > 2D Geometry > Shapes",
      url: "/geometry/2d/shapes/pentagon/",
      keywords: ["pentagon", "polygon", "5-sided", "golden ratio", "phi", "pentagram", "diagonal", "apothem", "area"]
    },
    {
      title: "Regular Decagon Calculator",
      category: "Geometry > 2D Geometry > Shapes",
      url: "/geometry/2d/shapes/decagon/",
      keywords: ["decagon", "polygon", "10-sided", "golden ratio", "phi", "apothem", "circumradius", "diagonal", "area"]
    },
    {
      title: "2D Geometry Hub",
      category: "Geometry",
      url: "/geometry/2d/",
      keywords: ["2d", "two dimensional", "polygons", "triangles", "quadrilaterals", "circles", "shapes"]
    },
    {
      title: "Polygons & Geometric Shapes Hub",
      category: "Geometry > 2D Geometry",
      url: "/geometry/2d/shapes/",
      keywords: ["shapes", "polygons", "hexagon", "pentagon", "octagon", "decagon", "regular polygons"]
    },
    {
      title: "Geometry Master Hub",
      category: "Mathematics",
      url: "/geometry/",
      keywords: ["geometry", "euclidean", "coordinate", "3d", "angles", "trigonometry", "surfaces"]
    },
    {
      title: "Calculus & Analysis Hub",
      category: "Mathematics",
      url: "/calculus/",
      keywords: ["calculus", "derivatives", "integrals", "limits", "differential equations", "taylor series"]
    },
    {
      title: "Finance & Quantitative Hub",
      category: "Applied Math",
      url: "/finance/",
      keywords: ["finance", "compound interest", "amortization", "loan", "present value", "black scholes", "annuity"]
    },
    {
      title: "Physics & Engineering Hub",
      category: "Physical Sciences",
      url: "/physics/",
      keywords: ["physics", "mechanics", "kinematics", "thermodynamics", "electrical", "fluids", "circuits"]
    },
    {
      title: "Statistics & Probability Hub",
      category: "Data Science",
      url: "/statistics/",
      keywords: ["statistics", "probability", "distributions", "normal", "binomial", "standard deviation", "regression"]
    }
  ];

  // Theme Management
  function initTheme() {
    const savedTheme = localStorage.getItem('omni-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      toggleBtn.setAttribute('title', savedTheme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme');

      toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('omni-theme', next);
        toggleBtn.innerHTML = next === 'dark' ? '☀️' : '🌙';
        toggleBtn.setAttribute('title', next === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme');
      });
    }
  }

  // Search Modal Management
  function initSearch() {
    const modal = document.getElementById('search-modal');
    const input = document.getElementById('search-modal-input');
    const resultsContainer = document.getElementById('search-modal-results');
    const triggerBtns = document.querySelectorAll('.search-btn-trigger');

    if (!modal || !input || !resultsContainer) return;

    function openModal() {
      modal.classList.add('active');
      input.value = '';
      renderResults(SEARCH_INDEX.slice(0, 5));
      setTimeout(() => input.focus(), 50);
    }

    function closeModal() {
      modal.classList.remove('active');
    }

    triggerBtns.forEach(btn => btn.addEventListener('click', openModal));

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        modal.classList.contains('active') ? closeModal() : openModal();
      } else if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });

    input.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        renderResults(SEARCH_INDEX.slice(0, 5));
        return;
      }

      const matches = SEARCH_INDEX.filter(item => {
        return item.title.toLowerCase().includes(q) ||
               item.category.toLowerCase().includes(q) ||
               item.keywords.some(k => k.toLowerCase().includes(q));
      });

      renderResults(matches);
    });

    function renderResults(items) {
      if (!items || items.length === 0) {
        resultsContainer.innerHTML = `<li style="padding:1.5rem; text-align:center; color:var(--text-muted);">No calculators found matching your query.</li>`;
        return;
      }

      resultsContainer.innerHTML = items.map(item => `
        <li class="search-result-item">
          <a href="${item.url}">
            <span class="search-result-title">${item.title}</span>
            <span class="search-result-category">${item.category}</span>
          </a>
        </li>
      `).join('');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSearch();
  });

})();
