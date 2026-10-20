# 📋 OmniOperand Operations — Human Action Punch List

**Project:** `enmuse/omnioperand`  
**Brand Domain:** [https://omnioperand.com](https://omnioperand.com)  
**Cloudflare Pages Edge:** [https://omnioperand.pages.dev](https://omnioperand.pages.dev)  
**Operational Lead:** Brandon (Hendersonville, NC)  
**GitHub Repository:** [https://github.com/enmuse/omnioperand](https://github.com/enmuse/omnioperand)  

---

## 🟢 Completed by Antigravity (Automated & Verified)

- [x] **Created GitHub Repository**: Initialized and published public repository [`enmuse/omnioperand`](https://github.com/enmuse/omnioperand) via GitHub REST API with full git tracking.
- [x] **Cloudflare Pages Project Created**: Programmatically created Pages project `omnioperand` on Cloudflare account `2bbe914ca4d82460c51d668407bb3dbd`.
- [x] **Custom Domains Attached**: Added `omnioperand.com` and `www.omnioperand.com` to the Cloudflare Pages project.
- [x] **Cloudflare DNS Configured**: Created proxied CNAME records in Cloudflare Zone `3c5297e2d6de7e4e858fd2679201e85d`:
  - `omnioperand.com` → `omnioperand.pages.dev`
  - `www.omnioperand.com` → `omnioperand.pages.dev`
- [x] **Secure API Credentials Configured**: Created `.env` containing Cloudflare, GitHub, and PageSpeed API keys. Protected by `.gitignore`.
- [x] **Flagship Regular Polygons Suite**:
  - **Universal Regular $n$-Polygon Solver ($n=3$ to $1000$):** Arbitrary $n$-gon bidirectional calculating engine, Archimedean circle exhaustion progress indicators, and dynamic vector morphing.
  - **Regular Octagon ($n=8$):** 8-variable bidirectional solver, $D_8$ symmetry group proofs, interactive blueprint.
  - **Regular Hexagon ($n=6$):** 8-variable bidirectional solver, equilateral triangle tessellation proofs, flat-to-flat and point-to-point diagonals.
  - **Regular Pentagon ($n=5$):** 7-variable bidirectional solver, golden ratio ($\phi$) proofs, exact radical derivations.
  - **Regular Decagon ($n=10$):** 9-variable bidirectional solver, 4 diagonal congruence classes ($d_1, d_2, d_3, d_4=2R$), golden ratio invariants ($R=a\phi$).
- [x] **Clean Mathematical Notation & Typography**: Eliminated all raw LaTeX backslash syntax, adopting standard Unicode notation (`α`, `β`, `θ`, `π`, `ϕ`, `√`, `°`, `²`, `³`) across all solvers and explanations.
- [x] **Enhanced Interactive Blueprints & Export Suite**:
  - Live Cartesian coordinate HUD with dynamic vertex $(X, Y)$ and angle readouts.
  - Interactive layer toggle pills (Cartesian Grid, Incircle/Circumcircle, Dimension Overlays, Vertex Points, Blueprint Theme).
  - High-Resolution PNG export (2000×2000 canvas with crisp anti-aliasing, coordinate grid, and embedded attribution watermark).
  - Standalone Vector SVG download with inline styles and CC BY 4.0 metadata.
  - Automatic LaTeX TikZ generator generating compilable Overleaf/LaTeX vector code.
  - **Commercial & Academic Attribution Box:** All blueprints are declared free to use in commerce, academia, textbooks, and software under CC BY 4.0 with ready-to-copy HTML web backlink and BibTeX citation code.
- [x] **Comprehensive Mathematical Proofs**: Analytical derivations for symmetry groups, angles, exact radicals, area formulas, and diagonal lengths.
- [x] **LLM Integration & Prompt Engineering Suite**:
  - On-page copyable verified prompt for ChatGPT, Claude, and Gemini with system directives and verification heuristics.
  - Machine-readable JSON export button on all solvers.
  - Standardized `/llms.txt` and comprehensive `/llms-full.txt` files at root.
- [x] **Hierarchical Hub-and-Spoke Architecture**:
  - Level 1: Root Homepage (`index.html`) featuring search and all 5 primary mathematical disciplines.
  - Level 2: Geometry Master Hub (`/geometry/index.html`).
  - Level 3: 2D Geometry Hub (`/geometry/2d/index.html`).
  - Level 4: Shapes & Polygons Hub (`/geometry/2d/shapes/index.html`).
  - Level 5: Regular Octagon, Hexagon, Pentagon, and Decagon Calculators.
  - Level 2 Discipline Hubs for Calculus, Finance, Physics, and Statistics.
- [x] **Automated Tooling & Test Suite**:
  - `scripts/test_site.py`: Automated testing suite passing with 1e-12 mathematical precision for all 4 polygon engines and 100% file integrity.
  - `scripts/generate_calculators.py`: Scalable taxonomy builder and sitemap generator.
  - `scripts/deploy.py`: Programmatic Cloudflare Pages deployment script.

---

## 🟡 Human Action Checklist for Brandon

```
┌──────────────────────────────────────────────────────────────┐
│                      REMAINING WORK                          │
│                                                              │
│  1. Check Cloudflare SSL Certificate Status (~1 min) [Done]  │
│  2. Review Initial Live Deployment on Cloudflare (~1 min)    │
│  3. Sign Up for Affiliate Networks (~45-60 mins)             │
│  4. Dedicated Stripe Profile for OmniOperand (~2 mins) [Done]│
└──────────────────────────────────────────────────────────────┘
```

---

### Task 1: Check Cloudflare SSL / TLS Status
The CNAME DNS records have already been set up in Cloudflare DNS for `omnioperand.com` and `www.omnioperand.com` pointing to `omnioperand.pages.dev`. Cloudflare Pages issues an edge SSL certificate (via Google Trust Services or Let's Encrypt).
1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Navigate to **Workers & Pages** → **omnioperand** → **Custom Domains**.
3. Confirm that `omnioperand.com` and `www.omnioperand.com` display status **Active** with a green checkmark. (If it displays *Initializing* or *Pending*, wait a few minutes while Cloudflare completes SSL handshake validation).
Completed - 10/20/26 by Brandon
---

### Task 2: Useful CLI Commands for Local Maintenance

To test all mathematical logic and site files:
```bash
python3 scripts/test_site.py
```

To list current taxonomy inventory or regenerate sitemaps:
```bash
python3 scripts/generate_calculators.py --list
python3 scripts/generate_calculators.py --sitemap
```

To deploy updates to Cloudflare Pages:
```bash
python3 scripts/deploy.py
```

To push changes to GitHub:
```bash
git add .
git commit -m "feat: updates"
git push origin main
```
Noted on 10/20/26 by Brandon
---

### Task 3: Affiliate Network Account Registration (High-Ticket CPA Monetization)

The contextual recommendation engine (`assets/js/affiliate-engine.js`) is fully active on all calculator pages and reads partner URLs from `config/affiliates.json`. To start capturing $50–$300 CPA commissions on human traffic:

1. **Sign up for Major Affiliate Networks**:
   - **Impact.com**: LendingTree, Rocket Mortgage, Marcus by Goldman Sachs, Uber/Lyft.
   - **CJ Affiliate (Commission Junction)**: AutoPay, TurboTax, H&R Block, QuickBooks.
   - **ShareASale / Awin**: Gusto Payroll, Rockler Woodworking, Northern Tool, Home Depot.
   - **Rakuten Advertising**: Financial institutions, retail cards, and trade suppliers.
2. **Update Tracking Links**:
   - Once approved, open `config/affiliates.json` and replace the placeholder `tracking_url` values with your unique affiliate tracking links.
   - The engine automatically routes clicks through your tracking codes with zero layout shift (CLS).

---

### Task 4: Dedicated Stripe Business Profile / Account for OmniOperand (~2 mins)

**Status:** The current live Stripe key has already provisioned the official **OmniOperand Developer Platform (API & MCP)** product (`prod_VTfU6ZCDeAONJq`) with live Pro ($29/mo) and Enterprise ($199/mo) prices, and checkout sessions work out-of-the-box.

**Recommended Separation Step:** To ensure customer bank statements specifically display **`OMNIOPERAND`** (instead of sharing `WNC Trade Network` branding or 1099-K reporting):
1. Go to [dashboard.stripe.com](https://dashboard.stripe.com/).
2. Click your business name dropdown in the top-left corner (`WNC Trade Network`) and click **"+ Add new account"** (or **"Create new account"**).
3. Set the account name to **"OmniOperand"**.
4. Set the Business Profile settings:
   - **Business website:** `https://omnioperand.com`
   - **Statement descriptor:** `OMNIOPERAND`
   - **Support email:** `support@omnioperand.com`
5. Under **Developers** → **API keys**, generate a restricted key (with Products, Prices, and Checkout Sessions write permissions) or copy the Secret key.
6. Replace `STRIPE_SECRET_KEY` in `.env` and in your Cloudflare Pages dashboard under **Settings** → **Environment variables**.
Completed 10/20/26 by Brandon
