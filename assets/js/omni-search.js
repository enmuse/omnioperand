/**
 * OmniOperand — Global Search & Navigation Controller (omni-search.js)
 * Instant fuzzy matching, keyboard navigation (Cmd+K / '/'), and Theme Toggle
 */

(function () {
  'use strict';

  // Calculator & Hub Index Database
  const SEARCH_INDEX = [
    {
      title: "OmniOperand Computational REST API & OpenAPI Schema",
      category: "Developer & Machine Protocols",
      url: "/api/",
      keywords: ["api", "rest", "rest api", "openapi", "json", "curl", "python", "developer", "programmatic", "endpoints", "chatgpt action", "llm", "agents", "mcp"]
    },
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
      title: "Mortgage Amortization & Early Payoff Calculator",
      category: "Finance > Debt & Real Estate",
      url: "/finance/mortgage-amortization/",
      keywords: ["mortgage", "amortization", "loan", "home loan", "interest", "monthly payment", "early payoff", "principal", "extra payment", "borrowing power", "interest savings", "fixed rate"]
    },
    {
      title: "Compound Interest & Investment Growth Calculator",
      category: "Finance > Wealth Growth",
      url: "/finance/compound-interest/",
      keywords: ["compound interest", "interest", "apy", "future value", "investing", "stocks", "savings", "monthly contribution", "continuous compounding", "annuity", "rule of 72"]
    },
    {
      title: "Compound Annual Growth Rate (CAGR) Calculator",
      category: "Finance > Valuation",
      url: "/finance/cagr/",
      keywords: ["cagr", "compound annual growth rate", "growth rate", "portfolio return", "doubling time", "geometric mean", "valuation", "investment return", "annualized"]
    },
    {
      title: "Auto Loan & Car Affordability Calculator",
      category: "Finance > Consumer Lending",
      url: "/finance/auto-loan/",
      keywords: ["auto loan", "car loan", "car payment", "car affordability", "trade-in", "sales tax", "vehicle price", "apr", "financing", "monthly car payment"]
    },
    {
      title: "Concrete Volume & Bag Count Calculator",
      category: "Geometry > 3D Geometry > Civil Engineering",
      url: "/geometry/3d/concrete-volume/",
      keywords: ["concrete", "cubic yards", "quikrete", "bag count", "80lb bag", "60lb bag", "slab", "footing", "column", "pier", "patio", "driveway", "cement", "ready mix"]
    },
    {
      title: "Roof Pitch, Rafter Length & Slope Calculator",
      category: "Geometry > 2D Geometry > Carpentry",
      url: "/geometry/2d/roof-pitch/",
      keywords: ["roof pitch", "pitch in 12", "rafter length", "slope", "degrees", "roof angle", "carpentry", "framing", "plumb cut", "birdsmouth", "truss", "overhang"]
    },
    {
      title: "Circle Sector, Arc Length & Segment Area Calculator",
      category: "Geometry > 2D Geometry > Curves",
      url: "/geometry/2d/circle-sector/",
      keywords: ["circle sector", "sector area", "arc length", "chord length", "sagitta", "segment area", "circular segment", "radius", "central angle"]
    },
    {
      title: "Right Triangle & Pythagorean Theorem Calculator",
      category: "Geometry > 2D Geometry > Triangles",
      url: "/geometry/2d/right-triangle/",
      keywords: ["right triangle", "pythagorean theorem", "hypotenuse", "altitude", "inradius", "circumradius", "cathetus", "triangle area", "trigonometry", "sine", "cosine", "tangent"]
    },
    {
      title: "Definite & Indefinite Integral Calculator",
      category: "Calculus > Integrals",
      url: "/calculus/integrals/",
      keywords: ["integral", "antiderivative", "definite integral", "indefinite integral", "riemann sum", "simpsons rule", "trapezoidal rule", "area under curve", "fundamental theorem of calculus"]
    },
    {
      title: "Derivative & Tangent Line Equation Calculator",
      category: "Calculus > Derivatives",
      url: "/calculus/derivatives/",
      keywords: ["derivative", "tangent line", "normal line", "slope", "instantaneous rate of change", "concavity", "second derivative", "inflection point", "differentiation"]
    },
    {
      title: "3D Geometry Hub",
      category: "Geometry",
      url: "/geometry/3d/",
      keywords: ["3d", "three dimensional", "spatial", "volume", "concrete", "polyhedra", "prisms", "cylinders"]
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
      keywords: ["finance", "mortgage", "compound interest", "cagr", "auto loan", "amortization", "loan", "present value"]
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

  // Global FAQ Accordion Toggle Delegation
  function initFaqToggles() {
    document.addEventListener('click', (e) => {
      const question = e.target.closest('.faq-question');
      if (question) {
        const item = question.closest('.faq-item');
        if (item) {
          item.classList.toggle('open');
        }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSearch();
    initFaqToggles();
  });

})();
