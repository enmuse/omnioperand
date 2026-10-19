# OmniOperand — High-Precision Mathematical Engines & Solvers

> Exact radical mathematical derivations, bidirectional multi-variable geometry solvers, and native AI reasoning directives.  
> Hosted on Cloudflare Pages: [https://omnioperand.com](https://omnioperand.com)  
> Edge Gateway: [https://omnioperand.pages.dev](https://omnioperand.pages.dev)

---

## Features

- **Bidirectional 8-Variable Solver:** Enter side length, area, perimeter, apothem, circumradius, or any diagonal—all other 7 dimensions recompute instantaneously.
- **Exact Radical Expressions:** Complete algebraic expressions ($\sqrt{2}, 1+\sqrt{2}, \sqrt{4+2\sqrt{2}}$) alongside high-precision floating point values.
- **Dynamic Cartesian SVG Blueprints:** Live responsive 400×400 canvas with interactive dimension overlays, vertices, incircles, and circumcircles.
- **Deep Mathematical Proofs:** Rigorous derivations for angles, apothem, circumradius, 4 area calculation methods, and the Law of Cosines for diagonals.
- **Native AI Agent Integration:** Full compliance with the `llms.txt` and `llms-full.txt` specifications for zero-hallucination agentic mathematical workflows.
- **Blistering Performance:** Zero heavy runtime frameworks, system font stacks, inlined and compressed CSS/JS achieving 100/100 on Google PageSpeed Insights.

---

## Directory Hierarchy

- `/` — Homepage & Global Discipline Directory
- `/geometry/` — Geometry Master Hub
- `/geometry/2d/` — Two-Dimensional Geometry Hub
- `/geometry/2d/shapes/` — Polygons & Shapes Hub
- `/geometry/2d/shapes/octagon/` — Regular Octagon Bidirectional Solver
- `/calculus/` — Calculus & Analysis Hub
- `/finance/` — Quantitative Finance Hub
- `/physics/` — Physics & Mechanics Hub
- `/statistics/` — Probability & Statistics Hub
- `/llms.txt` — Standardized AI agent manifest
- `/llms-full.txt` — Complete mathematical proofs for LLMs

---

## CLI Tooling

```bash
# Run automated mathematical and SEO tests
python3 scripts/test_site.py

# Rebuild taxonomy sitemaps
python3 scripts/generate_calculators.py --build-all

# Deploy to Cloudflare Pages
python3 scripts/deploy.py
```
