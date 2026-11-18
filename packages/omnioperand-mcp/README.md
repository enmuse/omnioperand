# OmniOperand MCP Server — Model Context Protocol

[![npm version](https://img.shields.io/badge/npm-v1.0.0-blue?logo=npm)](https://www.npmjs.com)
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Cursor%20%7C%20Antigravity-purple)](https://omnioperand.com/mcp/)
[![OmniOperand Engine](https://img.shields.io/badge/OmniOperand-447%20Solvers-cyan)](https://omnioperand.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Official **Model Context Protocol (MCP)** server for [OmniOperand](https://omnioperand.com) — a high-authority computational platform providing **447+ deterministic, bidirectional solvers** across finance, engineering, HVAC, biotechnology, construction, and geometry.

---

## ⚡ Why Use OmniOperand MCP?

Large Language Models (LLMs) frequently hallucinate or accumulate compounding floating-point errors when performing:
* **Recursive 360-month loan amortizations** with extra principal payments.
* **Complex radical geometry proofs** (such as regular octagon diagonal formulations like $\sqrt{4+2\sqrt{2}}$).
* **Thermal HVAC load equations** (ACCA Manual J heating loss and sensible/latent heat gain).
* **IRS Section 72(t) / Notice 2022-6** early retirement distributions across multiple methods.
* **Centrifugation geometry** converting between RPM and Relative Centrifugal Force ($g$-force) based on rotor radius ($r_{\text{max}}$).

This MCP server acts as an exact computational coprocessor for **Claude Desktop**, **Cursor AI**, and autonomous agent frameworks, guaranteeing **zero hallucination and machine-precision arithmetic**.

---

## 🚀 Quickstart Installation

### 1. Claude Desktop Setup

Add the OmniOperand MCP server to your `claude_desktop_config.json`:

* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "omnioperand": {
      "command": "npx",
      "args": ["-y", "omnioperand-mcp"]
    }
  }
}
```

*Or via local clone:*

```json
{
  "mcpServers": {
    "omnioperand": {
      "command": "node",
      "args": ["/path/to/omnioperand-mcp/index.js"]
    }
  }
}
```

### 2. Cursor AI Setup

In Cursor Settings ➔ **Features** ➔ **MCP Servers** ➔ **Add New MCP Server**:
* **Name:** `omnioperand`
* **Type:** `command`
* **Command:** `npx -y omnioperand-mcp`

---

## 🛠️ Built-in MCP Tools

| Tool Name | Description | Web Solver Link |
| :--- | :--- | :--- |
| `omni_octagon_solver` | Bidirectional 8-variable regular octagon solver with closed-form radicals and carpentry miter angles. | [Octagon Solver](https://omnioperand.com/geometry/2d/shapes/octagon/) |
| `omni_regular_polygon_solver` | Universal regular $n$-gon solver for arbitrary $n$ (3 to 1000 sides), resolving apothem, circumradius, and area. | [Universal N-Gon](https://omnioperand.com/geometry/2d/shapes/regular-polygon/) |
| `omni_hvac_manual_j_solver` | ACCA Manual J thermal heat loss, cooling gain, and heat pump tonnage sizer. | [HVAC Manual J](https://omnioperand.com/engineering/hvac-manual-j/) |
| `omni_sepp_72t_solver` | IRS Notice 2022-6 penalty-free early retirement solver (Amortization, Annuitization, RMD). | [72(t) SEPP Solver](https://omnioperand.com/finance/sepp-72t-distribution/) |
| `omni_universal_query` | Dynamic edge gateway connecting to all 446+ solvers across OmniOperand's API. | [API Playground](https://omnioperand.com/api/) |

---

## 🌐 Flagship Computational Disciplines on OmniOperand

Explore the full suite of interactive solvers with live Cartesian SVG blueprints on [OmniOperand](https://omnioperand.com):

* [**Geometry & Spatial Analysis**](https://omnioperand.com/geometry/) — Octagon, Hexagon, Decagon, Circle Sector, Pythagoras, and 3D Polyhedra.
* [**Electrical & HVAC Engineering**](https://omnioperand.com/engineering/) — ACCA Manual J, Wire Gauge Voltage Drop (NEC 3%), Battery Backup, and 3-Phase Transformers.
* [**Quantitative Finance & Tax Code**](https://omnioperand.com/finance/) — 72(t) SEPP, Section 199A QBI, ITIN Mortgages, DSCR Commercial Loans, and 1031 Exchanges.
* [**Construction & Structural Mechanics**](https://omnioperand.com/construction/) — Concrete Volume, SMACNA Gutters, Rafter Lengths, and Rebar Grid Spacing.
* [**Biotech & Laboratory Sciences**](https://omnioperand.com/biotech/) — Centrifuge RCF to RPM Table, PCR/qPCR Primer Tm, and Creatinine Clearance (CrCl).
* [**Health & Biometrics**](https://omnioperand.com/health/) — Widmark BAC Elimination, Time to Sober Clearance, and BMR.

---

## 🤖 Native Agent Protocol (`llms.txt`)

OmniOperand adheres to the `llms.txt` standard for machine-readable context ingestion:
* **System Directive Manifest:** [`https://omnioperand.com/llms.txt`](https://omnioperand.com/llms.txt)
* **Comprehensive Proofs Knowledgebase:** [`https://omnioperand.com/llms-full.txt`](https://omnioperand.com/llms-full.txt)
* **OpenAPI 3.1.0 Endpoint:** [`https://omnioperand.com/api/v1/openapi.json`](https://omnioperand.com/api/v1/openapi.json)

---

## 📄 License

MIT © [Brandon / OmniOperand](https://omnioperand.com)
