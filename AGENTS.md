# AGENTS.md — OmniOperand Architecture & AI Engineering Mandates

> Production Architecture, Mathematical Precision Standards & Operational Protocols for `enmuse/omnioperand`  
> Domain: **omnioperand.com**  
> Operational Lead: **Brandon** (Hendersonville, NC)

---

## 1. Executive Summary & Vision

**OmniOperand** (`omnioperand.com`) is a high-authority computational platform engineered for students, engineers, researchers, and autonomous AI agents. Unlike legacy calculation websites that feature static one-way inputs, outdated UI, and intrusive advertisements, OmniOperand provides:

1. **Unified Bidirectional Solvers:** Enter *any* single known parameter (or combination of parameters), and the mathematical engine instantaneously resolves all other variables with machine precision.
2. **Exact Analytical & Radical Derivations:** Numerical answers are always paired with exact closed-form radical representations (e.g. $2(1+\sqrt{2})a^2$) and step-by-step algebraic proofs.
3. **Live Interactive Cartesian Blueprints:** Dynamic SVG rendering on a coordinate plane with responsive dimension lines, vertex callouts, and tactile feedback.
4. **Native AI Agent Integration (`llms.txt`):** Structured system prompts, prompt engineering rubrics, and machine-readable endpoints eliminating hallucination for LLMs (ChatGPT, Claude, Gemini).
5. **100/100 Google PageSpeed Mandate:** Zero render-blocking frameworks, zero external font round-trips, sub-50ms TTFB on Cloudflare's global edge network.

```mermaid
graph TD
  Root["OmniOperand Root (/)<br/>Global Search, Disciplines Directory, llms.txt"] --> Domain["Level 2 Domain Hub<br/>/geometry/, /calculus/, /finance/, etc."]
  Domain --> SubDomain["Level 3 Sub-Domain Hub<br/>/geometry/2d/, /geometry/3d/, etc."]
  SubDomain --> SubHub["Level 4 Shape/Topic Hub<br/>/geometry/2d/shapes/"]
  SubHub --> Solver["Level 5 Precision Solver<br/>/geometry/2d/shapes/octagon/<br/>8-Variable Bidirectional Engine"]
```

---

## 2. Directory Layout & Architecture

```text
/
├── .env                              # Cloudflare, GitHub, and PageSpeed API credentials (Git-ignored)
├── .gitignore                        # Git exclusion rules
├── AGENTS.md                         # AI agent system memory & operational mandates (this file)
├── HUMAN.md                          # Human operator action punch list for Brandon
├── README.md                         # Public repository overview
├── 404.html                          # Mathematical 404 error page
├── index.html                        # Homepage & global discipline explorer
├── robots.txt                        # Search engine and AI crawler directives
├── sitemap.xml                       # Canonical XML sitemap
├── llms.txt                          # Standardized AI agent manifest (Answer.AI spec)
├── llms-full.txt                     # Comprehensive mathematical knowledge base for LLMs
├── assets/
│   ├── css/
│   │   ├── omni-core.css             # Math design system (glassmorphism, typography, grid)
│   │   └── calculator.css           # Calculator HUD, parameter cards, sliders, SVG canvas
│   └── js/
│       ├── omni-search.js            # Client-side fuzzy search & theme management
│       ├── blueprint-engine.js       # Vector SVG, High-Res PNG & LaTeX TikZ blueprint exporter
│       ├── octagon-solver.js         # Flagship regular octagon 8-variable bidirectional solver
│       └── regular-polygon-solver.js # Universal n-sided polygon (3-1000) solver engine
├── api/
│   ├── index.html                    # REST API Interactive Playground & Documentation
│   └── v1/
│       └── openapi.json              # OpenAPI 3.1.0 schema for AI agents and developer tooling
├── functions/
│   └── api/
│       └── v1/
│           ├── openapi.json.js       # Cloudflare Pages Function serving OpenAPI spec with CORS
│           └── geometry/
│               └── 2d/
│                   └── shapes/
│                       ├── regular-polygon.js # GET/POST endpoint for arbitrary n-gons
│                       └── octagon.js         # GET/POST endpoint for 8-variable octagon solver
├── geometry/
│   ├── index.html                    # Level 2 Hub: Geometry & Spatial Analysis
│   └── 2d/
│       ├── index.html                # Level 3 Hub: Two-Dimensional Geometry
│       └── shapes/
│           ├── index.html            # Level 4 Hub: Polygons & Shapes Directory
│           └── octagon/
│               └── index.html        # Level 5 Tool: Regular Octagon Calculator & Proofs
├── calculus/
│   └── index.html                    # Level 2 Hub: Calculus & Mathematical Analysis
├── finance/
│   └── index.html                    # Level 2 Hub: Quantitative Finance & Actuarial Math
├── physics/
│   └── index.html                    # Level 2 Hub: Physics & Engineering Mechanics
├── statistics/
│   └── index.html                    # Level 2 Hub: Probability & Statistics
└── scripts/
    ├── generate_calculators.py       # Programmatic generator & taxonomy builder
    ├── deploy.py                     # Programmatic Cloudflare Pages deployment script
    └── test_site.py                  # Automated test suite (formula invariants, SEO, file integrity)
```

---

## 3. Core Architectural & Engineering Standards

### 1. Bidirectional Solver Philosophy (Never Silo Inputs)
- **Do NOT create fragmented one-way pages** (e.g. separate pages for "octagon area from side" and "octagon side from area"). This creates thin doorway pages vulnerable to Google penalties.
- **Implement a Master Bidirectional Solver Matrix:** Every parameter card is interactive. Selecting any variable immediately computes all other variables through algebraic inversions.
- Provide deep semantic anchor IDs (`#area-from-side`, `#diagonals`, `#apothem`, etc.) and structured FAQ blocks so targeted search queries land directly on relevant explanations.

### 2. Mathematical Rigor & Proof Structure
Every single calculation page MUST provide:
- Exact closed-form formulas with irrational radicals ($\sqrt{2}, \sqrt{3}, \pi, \phi$) before decimal rounding.
- Minimum 4 decimal digits of precision by default, configurable up to 10 decimal digits.
- Step-by-step proofs covering:
  - Coordinate definitions and symmetry groups (e.g. $D_8$).
  - Angle derivations (interior, exterior, central).
  - Multiple distinct area derivations (triangulation, bounding square subtraction, radius/apothem forms).
  - Law of Cosines proofs for all diagonal congruence classes.
  - Practical carpentry/engineering heuristics (e.g. miter saw angles, corner cutoff distances).

### 3. SEO & Structured Data Requirements
Every calculator and hub page MUST include:
- A descriptive, keyword-rich `<title>` and `<meta name="description">`.
- Canonical link `<link rel="canonical" href="https://omnioperand.com/...">`.
- Fully populated OpenGraph and Twitter cards.
- Complete Schema.org JSON-LD tags:
  - `WebApplication` (defining inputs, outputs, application category).
  - `BreadcrumbList` (tracking complete hierarchy back to root).
  - `FAQPage` (high-intent question-and-answer pairs matching organic search queries).

### 4. 100/100 PageSpeed & Performance Guardrail
- **Zero Heavy JavaScript Frameworks:** No React, Next.js, Vue, or heavy charting libraries.
- **Zero External Font Calls:** Do NOT import Google Fonts or external webfonts. Use the native mathematical system font stack:
  `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "JetBrains Mono", Consolas, monospace;`
- **Pure SVG Blueprints:** Technical diagrams and dimension callouts must use responsive, lightweight vector SVGs.

### 5. AI Agent & LLM Native Directives (`llms.txt`)
- Always maintain root `/llms.txt` and `/llms-full.txt`.
- Every calculator must include a copyable "Prompt for LLMs" with explicit system directives and verification checks so users can feed verified problem context into ChatGPT, Claude, and Gemini without hallucination.

### 6. Strict Zero-Raw-LaTeX Mandate (Clean Mathematical Unicode Typography)
- **Hard Prohibition on Raw LaTeX in HTML:** AI agents must **NEVER** write raw LaTeX backslash commands (e.g. `\frac`, `\alpha`, `\theta`, `\beta`, `\pi`, `\sum`, `\lim`, `\sqrt`, `\cdot`, `\implies`, `\le`, `\ge`, `\text{...}`) inside user-facing HTML files.
- **Why:** OmniOperand maintains 100/100 Google PageSpeed scores by eliminating heavy 200KB+ client libraries (MathJax, KaTeX) and external web fonts. Placing raw LaTeX backslashes into HTML causes them to render as ugly, broken, unparsed code to the user.
- **Mandated Mathematical Typography Standard:**
  - **Greek Symbols:** Use native Unicode characters: `α`, `β`, `γ`, `θ`, `π`, `ϕ`, `φ`, `λ`, `σ`, `ω`, `Δ`, `∑`.
  - **Arithmetic & Logic Operators:** Use standard mathematical Unicode: `·` (middle dot), `×`, `÷`, `±`, `∓`, `√`, `∛`, `≈`, `≠`, `≤`, `≥`, `⟹`, `➔`, `→`, `∞`, `∠`, `⊥`.
  - **Powers, Roots & Indices:** Use semantic HTML `<sup>` and `<sub>` (e.g. `r<sub>i</sub>`, `V<sub>j</sub>`, `S²`, `a³`, `aⁿ`).
  - **Fractions:** Use typographic fractions `½`, `¼`, `¾`, or clean inline bracketed forms: `[(n - 2) · 180°] / n` or `a / [2 tan(π/n)]`.
  - **Limits & Summations:** Format cleanly: `lim (n ➔ ∞) P = 2πR` and `∑ (Interior Angles) = (n - 2) · 180°`.
- **Allowed Exception:** Only programmatic LaTeX TikZ export templates for downloadable files or inside copyable code blocks (e.g. `blueprint-engine.js` TikZ output) may contain LaTeX backslashes.
- **Automated CI Enforcement:** `scripts/test_site.py` contains `test_zero_raw_latex_in_html()`, which scans all `.html` files in the repository. Any unparsed backslash command will fail the test suite and block Cloudflare deployment.

### 7. Flagship Engine & Cross-Shape Navigation Architecture
- **Discoverability Mandate:** The **Universal Regular Polygon Solver** (`/geometry/2d/shapes/regular-polygon/`) is the master 2D computational engine. It must never be buried or hard to find. It must be prominently linked from:
  1. Root Homepage (`/`): Hero CTA buttons, featured solver showcase, and Geometry hub card.
  2. Level 2 Geometry Hub (`/geometry/`): Top featured item under Two-Dimensional Geometry.
  3. Level 3 2D Hub (`/geometry/2d/`): Top featured item under Polygons & Shapes.
  4. Level 4 Shapes Hub (`/geometry/2d/shapes/`): Full-width master solver showcase banner.
- **Unified Polygon Switcher Bar:** Every shape calculator (`regular-polygon`, `octagon`, `hexagon`, `pentagon`, `decagon`) MUST feature a persistent, responsive **Polygon Switcher Bar** directly above the solver HUD:
  - Quick-switch pills: `[⨁ Universal N-Gon (3–1000)]`, `[▲ Triangle (3)]`, `[■ Square (4)]`, `[⬠ Pentagon (5)]`, `[⬡ Hexagon (6)]`, `[🛑 Octagon (8)]`, `[⯃ Decagon (10)]`, `[📁 All Shapes]`.
  - The current active shape must be styled with an active highlight, and the Universal N-Gon pill must feature an accent badge so users can effortlessly pivot between dedicated radical closed-form solvers and the universal arbitrary $n$ solver in a single click without dead ends.

### 8. Programmatic REST API & Machine Protocol Standards
- **Sub-15ms Serverless Architecture:** All REST endpoints reside in `/functions/api/v1/` powered by Cloudflare Pages Functions (V8 edge isolates).
- **Deterministic Math Engine:** Pure algebraic and trigonometric functions with sub-0.5ms CPU execution time and zero external dependencies.
- **Zero Hallucination Protocol:** Endpoints must return both machine-precision floating-point metrics (up to 14 decimals) and exact algebraic radical representations before rounding.
- **Mathematical Invariance Verification:** Every API response includes a verified identity proof (`is_valid: true`), proving that fundamental invariants (such as $r_i / R \equiv \cos(\pi/n)$) hold true with machine precision.
- **OpenAPI 3.1 & Agent Native:** Maintain `/api/v1/openapi.json` for seamless integration into ChatGPT Custom Actions, Anthropic Claude MCP tools, and autonomous agent frameworks.
- **CORS & Edge Caching:** All endpoints must provide open CORS (`Access-Control-Allow-Origin: *`) and edge cache headers (`Cache-Control: public, max-age=3600, s-maxage=86400`).

---

## 4. Operational Scripts & Automation

All operations are automated via Python scripts in `/scripts/`:

| Script | Purpose | Command |
| :--- | :--- | :--- |
| `scripts/test_site.py` | Validates mathematical invariants, file integrity, and SEO tags | `python3 scripts/test_site.py` |
| `scripts/generate_calculators.py` | Manages taxonomy registry, regenerates sitemap.xml and llms.txt | `python3 scripts/generate_calculators.py --build-all` |
| `scripts/deploy.py` | Deploys site to Cloudflare Pages edge network | `python3 scripts/deploy.py` |

---

## 5. Git & Cloudflare Workflow Protocol

1. **Commit Hygiene:** Use conventional commit messages (`feat:`, `fix:`, `docs:`, `perf:`).
2. **Pre-commit Verification:** Always run `python3 scripts/test_site.py` to ensure all mathematical invariants and file checks pass before pushing.
3. **Deployment:** Push to GitHub remote `origin/main` (`enmuse/omnioperand`) and trigger Cloudflare Pages deployment via `scripts/deploy.py`.

---

# Antigravity Rules for Payment & MCP Implementation
- Use TypeScript with strict null checks.
- Keep wallet secrets strictly in `.env`; never hardcode addresses or keys.
- Use Viem (not Web3.js) for EVM signature verification on Base.
- Mock all on-chain settlements in unit tests to prevent network timeouts during testing.
- Follow the official @modelcontextprotocol/sdk patterns for tool declarations.

