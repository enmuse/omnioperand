# OmniOperand MCP Server — Model Context Protocol

[![npm version](https://img.shields.io/badge/npm-v2.1.0-blue?logo=npm)](https://www.npmjs.com)
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Cursor%20%7C%20Antigravity-purple)](https://omnioperand.com/mcp/)
[![OmniOperand Engine](https://img.shields.io/badge/OmniOperand-428%20Solvers-cyan)](https://omnioperand.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Official **Model Context Protocol (MCP)** server for [OmniOperand](https://omnioperand.com) — a high-authority computational platform providing **428+ deterministic, bidirectional solvers** across finance, engineering, HVAC, construction, biotechnology, and geometry.

---

## ⚡ Why Use OmniOperand MCP?

Large Language Models (LLMs) frequently hallucinate or accumulate compounding floating-point errors when performing:
* **Recursive 360-month loan amortizations** with extra principal payments.
* **Complex radical geometry proofs** (such as regular octagon diagonal formulations like $\sqrt{4+2\sqrt{2}}$).
* **Thermal HVAC load equations** (ACCA Manual J heating loss and sensible/latent heat gain).
* **IRS Section 72(t) / Notice 2022-6** early retirement distributions across multiple methods.
* **National Electrical Code (NEC)** conductor ampacity and voltage drop constraints.
* **Structural concrete order quantities** with commercial bag yields and contractor waste buffers.

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

## 🛠️ Curated Flagship MCP Tools (12 Tools)

The server exposes 12 carefully curated, non-overlapping tools featuring discovery operations, batch execution, and specialized domain solvers:

### Discovery & Multi-Job Suite
| Tool Name | Purpose | Output Metrics / Returns |
| :--- | :--- | :--- |
| `omni_list_categories` | Enumerate all 15 scientific and computational disciplines with active calculator counts. | Array of categories with counts, IDs, and URLs. |
| `omni_list_solvers` | Discover and keyword-search across all 428+ deterministic calculators. | Array of solver summaries with formulas and parameter counts. |
| `omni_describe_solver` | Inspect exact parameter schema, field names, data types, units, and metrics for any solver. | Complete input schema (names, types, defaults, min/max, units) and output metrics. |
| `omni_batch_calculate` | Execute multi-scenario parameter sweeps or chained calculations in a single atomic request. | Batch results array with execution latency and individual statuses. |

### Dynamic Gateway
| Tool Name | Purpose | Scope |
| :--- | :--- | :--- |
| `omni_universal_query` | Dynamic edge gateway connecting to 420+ long-tail solvers across OmniOperand's catalog. | Astronomy, chemistry, physics, statistics, logistics, and legal math. |

### Flagship Domain Solvers
| Tool Name | Discipline | Governing Standard / Formula | Web Solver Link |
| :--- | :--- | :--- | :--- |
| `omni_octagon_solver` | Geometry & Carpentry | Exact closed-form radicals ($2(1+\sqrt{2})a^2$, $\sqrt{4+2\sqrt{2}}$), 8-variable bidirectional solver, 22.5° miter cuts. | [Octagon Solver](https://omnioperand.com/geometry/2d/shapes/octagon/) |
| `omni_regular_polygon_solver` | Geometry & Polygons | Universal regular $n$-gon solver for arbitrary $n$ (3 to 1000 sides, $n \ne 8$), resolving apothem, circumradius, and area. | [Universal N-Gon](https://omnioperand.com/geometry/2d/shapes/regular-polygon/) |
| `omni_hvac_manual_j_solver` | Mechanical & HVAC | ACCA Manual J 8th Edition whole-building heating loss, cooling gain, and equipment tonnage sizing. | [HVAC Manual J](https://omnioperand.com/engineering/hvac-manual-j/) |
| `omni_sepp_72t_solver` | Actuarial & Finance | IRS Notice 2022-6 / IRC § 72(t) early retirement distributions (Amortization, Annuitization, RMD) with statutory caps. | [72(t) SEPP Solver](https://omnioperand.com/finance/sepp-72t-distribution/) |
| `omni_mortgage_solver` | Real Estate Finance | Fixed-rate residential mortgage P&I amortization calculator with accelerated payoff savings. | [Mortgage Calculator](https://omnioperand.com/finance/mortgage/) |
| `omni_concrete_volume_solver` | Construction & Civil | Structural concrete slab and column volume in cubic yards with 60-lb/80-lb bag counts and 10% waste buffer. | [Concrete Volume](https://omnioperand.com/construction/concrete-volume/) |
| `omni_wire_gauge_voltage_drop_solver` | Electrical Engineering | National Electrical Code (NEC) Article 210.19 3% branch circuit wire gauge and voltage drop calculator. | [Wire Gauge Solver](https://omnioperand.com/energy/wire-gauge-voltage-drop/) |

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
* **MCP Edge Endpoint:** [`https://omnioperand.com/mcp`](https://omnioperand.com/mcp)

---

## 📄 License

MIT License — Copyright (c) 2026 OmniOperand (enmuse). See [LICENSE](LICENSE) for details.
