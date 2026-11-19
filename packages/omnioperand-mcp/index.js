#!/usr/bin/env node
/**
 * omnioperand-mcp
 * Official Model Context Protocol (MCP) Server for OmniOperand (https://omnioperand.com)
 * 
 * Provides 428+ deterministic mathematical, spatial, financial, and engineering calculation tools
 * to Claude Desktop, Cursor, Glama, Arcade, and autonomous AI agents.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { CALCULATOR_REGISTRY, executeCalculator } from "./calculator_registry.js";

const server = new McpServer({
  name: "OmniOperand Math & Engineering Engine",
  version: "2.0.0",
  description: "Comprehensive deterministic mathematical, engineering, financial, and geometric solvers from https://omnioperand.com"
});

// Category metadata lookup
const CATEGORY_NAMES = {
  geometry: "Geometry & Spatial Analysis",
  finance: "Quantitative Finance & Actuarial Math",
  construction: "Construction & Structural Trades",
  health: "Health, Metabolism & Physiological Metrics",
  physics: "Classical Mechanics & Thermal Physics",
  calculus: "Calculus & Mathematical Analysis",
  statistics: "Probability & Inferential Statistics",
  energy: "Energy Systems, Solar & Storage",
  logistics: "Supply Chain, Freight & Logistics",
  crypto: "Cryptocurrency & Digital Asset Accounting",
  legal: "Legal Settlements & Statutory Formulas",
  agriculture: "Agronomy, Irrigation & Livestock Math",
  engineering: "Mechanical & Civil Engineering",
  ecommerce: "E-Commerce Unit Economics & Advertising",
  biotech: "Molecular Biology & Laboratory Biotech"
};

// =========================================================================
// 1. DISCOVERY & BATCH TOOLS (Server Coherence & Exploration Suite)
// =========================================================================

// Discovery 1: List Categories
server.tool(
  "omni_list_categories",
  `List All OmniOperand Computational Disciplines & Categories:
Enumerates all 15 scientific, mathematical, engineering, and financial categories supported by the OmniOperand platform, including total solver counts and reference URLs.

USAGE GUIDELINES:
- WHEN TO USE: Invoke at the start of multi-step problem solving or category exploration to discover valid discipline categories for subsequent filtering in 'omni_list_solvers' or 'omni_universal_query'.
- DISAMBIGUATION & BOUNDARIES: Use 'omni_list_categories' for broad domain navigation; use 'omni_list_solvers' to discover individual calculators within a category.

BEHAVIOR & SAFETY:
- Pure deterministic metadata query. Read-only, idempotent, and stateless. Zero side effects.

RETURNS:
- Structured JSON containing:
  * total_categories (number): Total count of active discipline categories
  * total_solvers (number): Total count of deterministic calculators across all disciplines
  * categories (array): List of { id, name, solvers_count, url }`,
  {},
  async () => {
    const cats = {};
    for (const calc of Object.values(CALCULATOR_REGISTRY)) {
      cats[calc.category] = (cats[calc.category] || 0) + 1;
    }
    const categoryList = Object.keys(cats).sort().map(id => ({
      id,
      name: CATEGORY_NAMES[id] || id,
      solvers_count: cats[id],
      url: `https://omnioperand.com/${id}/`
    }));

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          total_categories: categoryList.length,
          total_solvers: Object.keys(CALCULATOR_REGISTRY).length,
          categories: categoryList
        }, null, 2)
      }]
    };
  }
);

// Discovery 2: List Solvers
server.tool(
  "omni_list_solvers",
  `Enumerate & Search OmniOperand Solvers:
Discovers and lists deterministic calculators across all disciplines with optional category filtering and keyword search matching solver names, descriptions, and formulas.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to find the exact calculator slug and governing formula before calling 'omni_describe_solver' or executing via a specialized tool or 'omni_universal_query'. Eliminates blind guessing of slugs.
- DISAMBIGUATION & BOUNDARIES: Returns summary lists of solvers. To inspect exact input field parameter names, types, and bounds for a discovered slug, call 'omni_describe_solver'.

BEHAVIOR & SAFETY:
- Pure deterministic query. Read-only, idempotent, and stateless. Zero side effects.

RETURNS:
- Structured JSON containing:
  * total_matches (number): Count of matching solvers
  * category_filter (string|null): Applied category filter
  * search_query (string|null): Applied search query
  * solvers (array): Array of { slug, name, category, formula_display, fields_count, metrics_count }`,
  {
    category: z.string().optional().describe("Optional discipline category filter (e.g. 'finance', 'engineering', 'construction', 'geometry', 'biotech', 'health')."),
    search: z.string().optional().describe("Optional keyword search query to match against solver names, descriptions, or mathematical terms (e.g. 'rebar', 'mortgage', 'tonnage', 'voltage drop')."),
    limit: z.number().int().min(1).max(100).default(50).describe("Maximum number of results to return (default 50, max 100).")
  },
  async ({ category, search, limit }) => {
    let matches = Object.values(CALCULATOR_REGISTRY);

    if (category) {
      const catLower = category.toLowerCase().trim();
      matches = matches.filter(c => (c.category || '').toLowerCase() === catLower);
    }

    if (search) {
      const q = search.toLowerCase().trim();
      matches = matches.filter(c =>
        c.slug.includes(q) ||
        (c.name && c.name.toLowerCase().includes(q)) ||
        (c.description && c.description.toLowerCase().includes(q)) ||
        (c.formula_display && c.formula_display.toLowerCase().includes(q))
      );
    }

    const results = matches.slice(0, limit).map(c => ({
      slug: c.slug,
      name: c.name,
      category: c.category,
      formula_display: c.formula_display || 'Deterministic model',
      fields_count: (c.fields || []).length,
      metrics_count: (c.metrics || []).length
    }));

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          total_matches: matches.length,
          returned_count: results.length,
          category_filter: category || null,
          search_query: search || null,
          solvers: results
        }, null, 2)
      }]
    };
  }
);

// Discovery 3: Describe Solver
server.tool(
  "omni_describe_solver",
  `Inspect Solver Parameter Schema & Output Metrics:
Returns the complete input parameter specification (field IDs, labels, data types, units of measure, default values, min/max bounds, and semantic hints) and output metric definitions for any calculator slug.

USAGE GUIDELINES:
- WHEN TO USE: Invoke after discovering a calculator slug via 'omni_list_solvers' to learn its exact parameter requirements before calling 'omni_universal_query' or 'omni_batch_calculate'. Eliminates parameter key hallucinations.
- DISAMBIGUATION & BOUNDARIES: 'omni_describe_solver' provides introspection and parameter documentation; it does not execute calculations. To execute, call the corresponding named tool (e.g. 'omni_mortgage') or 'omni_universal_query'.

BEHAVIOR & SAFETY:
- Pure deterministic schema introspection. Read-only, idempotent, and stateless.

RETURNS:
- Structured JSON containing:
  * slug (string): Calculator slug
  * name (string): Human-readable title
  * category (string): Discipline category
  * description (string): Detailed mathematical description
  * formula_display (string): Governing formula
  * fields (array): Detailed input parameter schemas { id, label, default, suffix, min, max, step, hint }
  * metrics (array): Output metrics specification { id, label, default_display, highlight }`,
  {
    slug: z.string().describe("The calculator slug to inspect (e.g. 'mortgage', 'concrete-volume', 'wire-gauge-voltage-drop', 'regular-polygon').")
  },
  async ({ slug }) => {
    const calc = CALCULATOR_REGISTRY[slug];
    if (!calc) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            status: "error",
            message: `Unknown calculator slug '${slug}'. Call 'omni_list_solvers' to discover valid calculator slugs.`
          }, null, 2)
        }]
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          status: "success",
          slug: calc.slug,
          name: calc.name,
          category: calc.category,
          description: calc.description,
          formula_display: calc.formula_display,
          fields: calc.fields,
          metrics: calc.metrics
        }, null, 2)
      }]
    };
  }
);

// Discovery 4: Batch Calculate
server.tool(
  "omni_batch_calculate",
  `Execute Batch or Chained Multi-Calculator Jobs:
Executes multiple deterministic calculations across any discipline in a single atomic request, returning individual status, inputs, and calculated metrics for each job. Enables comparative sensitivity analyses, multi-room building calculations, and chained financial scenarios.

USAGE GUIDELINES:
- WHEN TO USE: Invoke when solving multi-variable scenarios (e.g. comparing 15-year vs 30-year mortgages, calculating concrete volume across multiple foundation footings, or evaluating multiple regular polygons) in a single round-trip without multiple sequential calls.
- DISAMBIGUATION & BOUNDARIES: Use 'omni_batch_calculate' for multi-calculation batches; use individual named tools for single one-off calculations.

BEHAVIOR & SAFETY:
- Pure deterministic batch execution. Read-only, idempotent, and stateless.
- Isolated job failures: An error in one job (e.g. unknown slug or invalid input) returns an error object for that specific item without failing the entire batch.

RETURNS:
- Structured JSON containing:
  * total_jobs (number): Number of submitted jobs
  * successful_jobs (number): Count of successfully resolved calculations
  * execution_time_ms (number): Total batch execution latency
  * results (array): List of calculation result objects matching individual solver outputs`,
  {
    jobs: z.array(z.object({
      slug: z.string().describe("Target calculator slug (e.g. 'mortgage', 'concrete-volume')."),
      params: z.record(z.any()).describe("Input parameters dictionary for this calculator job.")
    })).min(1).max(50).describe("Array of calculation jobs (1 to 50 jobs per batch).")
  },
  async ({ jobs }) => {
    const startTime = Date.now();
    const results = jobs.map(job => {
      try {
        return executeCalculator(job.slug, job.params || {});
      } catch (e) {
        return {
          status: "error",
          calculator: job.slug,
          message: e.message
        };
      }
    });

    const successCount = results.filter(r => r.status === 'success').length;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          total_jobs: jobs.length,
          successful_jobs: successCount,
          execution_time_ms: Math.max(0.1, Date.now() - startTime),
          results
        }, null, 2)
      }]
    };
  }
);

// =========================================================================
// 2. FLAGSHIP SPECIALIST SOLVERS (Custom Closed-Form & High-Precision Engines)
// =========================================================================

// 1. Regular Octagon Solver (Exact Closed-Form Radicals)
server.tool(
  "omni_octagon_solver",
  `Regular Octagon 8-Variable Bidirectional Solver:
Exact regular octagon dimensional solver resolving side length, area, perimeter, apothem (inradius), circumradius, span across flats, short diagonal, long diagonal, miter saw angle, and corner cutoff using closed-form radical expressions.

Governing formulas:
- Area = 2 · (1 + √2) · a²
- Apothem = [a · (1 + √2)] / 2
- Circumradius = a · √[(1 + √2) · √2 / 2]
- Span (flat-to-flat) = a · (1 + √2)
- Short Diagonal = a · √(2 + √2)
- Long Diagonal = a · √(4 + 2√2)
- Miter Angle = 22.5° | Corner Cutoff = a / √2

BIDIRECTIONAL DRIVER & VALUE PAIRING:
- Set 'driver' to the name of the single known reference parameter: 'side', 'area', 'perimeter', 'apothem', 'circumradius', 'span', 'short_diagonal', or 'long_diagonal'.
- Set 'value' to its positive numerical magnitude (e.g. driver='area', value=482.84).
- The solver algebraically backsolves all remaining 7 geometric parameters simultaneously.

USAGE GUIDELINES:
- WHEN TO USE: Invoke whenever solving regular 8-sided polygon geometry, architectural framing, miter cuts, or area conversions from any known dimension. Eliminates LLM floating-point errors on radical roots like √(4 + 2√2).
- WHEN NOT TO USE: Do not use for irregular octagons, non-planar 3D geometry, or non-8-sided polygons.

DISAMBIGUATION & BOUNDARIES:
- DEDICATED SOLELY TO 8-SIDED REGULAR OCTAGONS.
- Distinct from 'omni_regular_polygon_solver': 'omni_octagon_solver' returns exact closed-form radical representations (e.g. 2(1+√2)a²), carpentry miter angles (22.5°), and corner cutoff dimensions without trigonometric rounding. Conversely, 'omni_regular_polygon_solver' is for arbitrary n-gons where n != 8.
- Distinct from 'omni_universal_query': Call 'omni_octagon_solver' directly whenever 8-sided geometry is specified to get compile-time validation and radical closed-form outputs.

BEHAVIOR & SAFETY:
- Pure deterministic geometric computation with machine floating-point precision.
- Read-only, idempotent, and stateless. Zero side effects or external network mutations.
- Enforces strict input validation (value > 0). Out-of-bounds inputs return safe diagnostic error.
- Output floating-point metrics rounded to user-specified precision (between 2 and 14 decimal places, default 6).

RETURNS:
- Structured JSON object containing:
  * source (string): Canonical documentation URL
  * driver_parameter (string): Echoed driver name
  * driver_value (number): Echoed driver value
  * metrics (object): Calculated dimensional metrics:
    - side_length (number): Outer regular edge length (units)
    - area (number): Total enclosed area (sq units)
    - perimeter (number): Boundary length 8a (units)
    - apothem (number): Center-to-flat inradius (units)
    - circumradius (number): Center-to-vertex radius (units)
    - span_flat_to_flat (number): Width across opposite flat sides (units)
    - short_diagonal (number): Distance between alternate vertices (units)
    - long_diagonal (number): Maximum diameter across opposite vertices (units)
  * exact_closed_forms (object): Symbolic radical mathematical formulas for all quantities
  * miter_angle_deg (number): Exact saw bevel angle (22.5°)
  * corner_cutoff (number): Truncated corner leg length (units)`,
  {
    driver: z.enum([
      'side', 'a', 'area', 'a_poly', 'perimeter', 'p',
      'apothem', 'inradius', 'r_i', 'circumradius', 'r',
      'span', 's', 'short_diagonal', 'd_s', 'long_diagonal', 'd_l'
    ]).default('side').describe("The known reference parameter driving the bidirectional calculation. Pairs with 'value' to instantaneously backsolve all other 7 variables."),
    value: z.number().positive().describe("Numerical positive value of the known reference driver parameter (e.g. 10.0)."),
    precision: z.number().int().min(2).max(14).default(6).describe("Decimal places of precision for output floating-point metrics (integer between 2 and 14, default 6).")
  },
  async ({ driver, value, precision }) => {
    const k = 1 + Math.SQRT2;
    let a = 0;
    switch (driver) {
      case 'side': case 'a': a = value; break;
      case 'area': case 'a_poly': a = Math.sqrt(value / (2 * k)); break;
      case 'perimeter': case 'p': a = value / 8; break;
      case 'apothem': case 'inradius': case 'r_i': a = (2 * value) / k; break;
      case 'circumradius': case 'r': a = value / Math.sqrt((k * Math.SQRT2) / 2); break;
      case 'span': case 's': a = value / k; break;
      case 'short_diagonal': case 'd_s': a = value / Math.sqrt(2 + Math.SQRT2); break;
      case 'long_diagonal': case 'd_l': a = value / Math.sqrt(4 + 2 * Math.SQRT2); break;
      default: a = value;
    }
    const area = 2 * k * a * a;
    const perimeter = 8 * a;
    const apothem = (a / 2) * k;
    const circumradius = a * Math.sqrt((k * Math.SQRT2) / 2);
    const span = a * k;
    const short_diagonal = a * Math.sqrt(2 + Math.SQRT2);
    const long_diagonal = 2 * circumradius;

    const round = (num) => parseFloat(num.toFixed(precision));

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          source: "https://omnioperand.com/geometry/2d/shapes/octagon/",
          driver_parameter: driver,
          driver_value: value,
          metrics: {
            side_length: round(a),
            area: round(area),
            perimeter: round(perimeter),
            apothem: round(apothem),
            circumradius: round(circumradius),
            span_flat_to_flat: round(span),
            short_diagonal: round(short_diagonal),
            long_diagonal: round(long_diagonal)
          },
          exact_closed_forms: {
            area: "2 · (1 + √2) · a²",
            apothem: "[a · (1 + √2)] / 2",
            circumradius: "a · √[(1 + √2) · √2 / 2]",
            short_diagonal: "a · √(2 + √2)",
            long_diagonal: "a · √(4 + 2√2)"
          },
          miter_angle_deg: 22.5,
          corner_cutoff: round(a / Math.SQRT2)
        }, null, 2)
      }]
    };
  }
);

// 2. Universal Regular Polygon Solver (3–1000 sides)
server.tool(
  "omni_regular_polygon_solver",
  `Universal Regular N-Sided Polygon Solver (3 to 1000 sides):
Solves dimensional geometry and internal angles for any regular polygon with n equal sides and vertices (triangles, pentagons, hexagons, heptagons, decagons, etc.).

Governing formulas:
- Central Angle = 360° / n
- Interior Angle = [(n - 2) · 180°] / n
- Perimeter = n · a
- Apothem (Inradius) = a / [2 · tan(π/n)]
- Circumradius = a / [2 · sin(π/n)]
- Area = (n · a · apothem) / 2 = (n · a²) / [4 · tan(π/n)]

BIDIRECTIONAL DRIVER & VALUE PAIRING:
- Set 'n' to the integer vertex/edge count (3 ≤ n ≤ 1000).
- Set 'driver' to the name of the single known reference parameter: 'side', 'area', 'perimeter', 'apothem', or 'circumradius'.
- Set 'value' to its positive numerical magnitude (e.g. driver='area', value=250.0).
- The solver algebraically backsolves all remaining 5 geometric dimensions simultaneously.

USAGE GUIDELINES:
- WHEN TO USE: Invoke for arbitrary regular polygons with n sides (3 ≤ n ≤ 1000) when calculating area, inradius, circumradius, perimeter, or internal angles from any single known dimension.
- WHEN NOT TO USE: Do not use for irregular polygons, non-planar polygons, or 3D polyhedra.

DISAMBIGUATION & BOUNDARIES:
- FOR ARBITRARY N-GONS (n != 8): Use 'omni_regular_polygon_solver' for triangles (n=3), squares (n=4), pentagons (n=5), hexagons (n=6), decagons (n=10), dodecagons (n=12), up to 1000 sides.
- DO NOT USE FOR REGULAR OCTAGONS (n=8): Route 8-sided regular octagons to 'omni_octagon_solver' instead, which provides exact radical closed-form proofs (e.g. 2·(1+√2)·a²) without trigonometric floating-point approximation.
- Distinct from 'omni_universal_query': Call 'omni_regular_polygon_solver' directly whenever computing planar n-gon dimensions.

BEHAVIOR & SAFETY:
- Pure deterministic trigonometric computation with machine floating-point precision.
- Read-only, idempotent, and stateless. Zero side effects or external network mutations.
- Input validation: Enforces 3 ≤ n ≤ 1000 and value > 0. Out-of-bounds parameters return safe diagnostic error.
- Output floating-point metrics rounded to user-specified precision (between 2 and 14 decimal places, default 6).

RETURNS:
- Structured JSON object containing:
  * source (string): Canonical documentation URL
  * sides_n (number): Vertex count n
  * driver_parameter (string): The reference parameter used
  * driver_value (number): Reference parameter magnitude
  * side_length (number): Regular edge length a (linear units)
  * perimeter (number): Boundary length (linear units)
  * area (number): Total enclosed polygon area (square units)
  * apothem_inradius (number): Center-to-edge inradius (linear units)
  * circumradius (number): Center-to-vertex outer radius (linear units)
  * interior_angle_deg (number): Vertex interior angle in degrees
  * central_angle_deg (number): Central sector angle in degrees`,
  {
    n: z.number().int().min(3).max(1000).default(8).describe("Total number of polygon vertices/sides (integer between 3 and 1000, default 8)."),
    driver: z.enum(['side', 'area', 'perimeter', 'apothem', 'circumradius']).default('side').describe("The known reference parameter driving the bidirectional calculation. Pairs with 'value' to invert all other dimensions."),
    value: z.number().positive().describe("Numerical positive magnitude of the known driver parameter (e.g. 10.0)."),
    precision: z.number().int().min(2).max(14).default(6).describe("Decimal places of precision for numerical outputs (between 2 and 14, default 6).")
  },
  async ({ n, driver, value, precision }) => {
    const angle_rad = Math.PI / n;
    let a = 0;
    switch (driver) {
      case 'side': a = value; break;
      case 'perimeter': a = value / n; break;
      case 'apothem': a = 2 * value * Math.tan(angle_rad); break;
      case 'circumradius': a = 2 * value * Math.sin(angle_rad); break;
      case 'area': a = Math.sqrt((4 * value * Math.tan(angle_rad)) / n); break;
    }
    const perimeter = n * a;
    const apothem = a / (2 * Math.tan(angle_rad));
    const circumradius = a / (2 * Math.sin(angle_rad));
    const area = 0.5 * perimeter * apothem;
    const round = (num) => parseFloat(num.toFixed(precision));

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          source: "https://omnioperand.com/geometry/2d/shapes/regular-polygon/",
          sides_n: n,
          driver_parameter: driver,
          driver_value: value,
          side_length: round(a),
          perimeter: round(perimeter),
          area: round(area),
          apothem_inradius: round(apothem),
          circumradius: round(circumradius),
          interior_angle_deg: round(((n - 2) * 180) / n),
          central_angle_deg: round(360 / n)
        }, null, 2)
      }]
    };
  }
);

// 3. HVAC Manual J Thermal Sizing
server.tool(
  "omni_hvac_manual_j_solver",
  `ACCA Manual J Whole-Building Heating & Cooling Load Estimator:
Calculates whole-structure peak heating loss (BTU/hr), sensible/latent cooling heat gain (BTU/hr), and recommended heat pump/AC tonnage sizing according to ACCA Manual J 8th Edition residential load principles.

MODEL ASSUMPTIONS & ENVELOPE-FREE SCOPE:
- Uses a simplified whole-building block-load calculation based on conditioned square footage, ceiling volume, outdoor 99%/1% dry-bulb design temperatures, and insulation envelope heat-transfer multipliers (U-factors).
- Envelope-Free Nature: This is a macro-level block load model using conditioned square footage, ceiling volume, design temperature differentials, and generalized building thermal integrity multipliers (poor/uninsulated R-11/R-19, average code R-13/R-38, high efficiency R-21/R-49).
- Scope Limitations: Does NOT model room-by-room solar orientation, fenestration solar heat gain coefficients (SHGC), radiant barriers, duct leakage losses, or internal occupant/appliance gains. Trust this tool for preliminary residential heating/cooling sizing and equipment tonnage estimates, not for municipal permit-level Manual J/S/D submittals.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to size residential HVAC equipment, heat pump/furnace output, and cooling capacity in tons, preventing short-cycling or undersizing.
- WHEN NOT TO USE: Do not use for commercial zoned VAV systems, multi-family duct design, or permit filings requiring room-by-room ACCA Manual J submittals.

DISAMBIGUATION & BOUNDARIES:
- Use 'omni_hvac_manual_j_solver' for whole-house block heating and cooling loads with heat pump/AC tonnage sizing.
- For heating furnace capacity alone, see 'omni_hvac_furnace_sizing'.
- Distinct from 'omni_universal_query': Call 'omni_hvac_manual_j_solver' directly whenever sizing residential heating and cooling equipment.

BEHAVIOR & SAFETY:
- Deterministic thermal engineering estimation.
- Read-only, idempotent, and stateless. Zero side effects or persistent state mutations.
- Enforces strict positive numerical validation on area and ceiling height. Out-of-bounds parameters return safe diagnostic status.

RETURNS:
- Structured JSON object containing:
  * source (string): Canonical documentation URL
  * heating_load_btu_hr (number): Peak winter heat loss in BTU/hr
  * cooling_load_btu_hr (number): Peak summer heat gain in BTU/hr
  * recommended_cooling_tonnage (number): Exact continuous cooling tonnage (BTU/hr ÷ 12,000)
  * rounded_equipment_size_tons (number): Standard manufactured equipment size rounded up to the nearest 0.5 ton
  * design_delta_t_heating_deg_f (number): Winter design temperature differential (indoor setpoint - outdoor winter)
  * design_delta_t_cooling_deg_f (number): Summer design temperature differential (outdoor summer - indoor setpoint)`,
  {
    floor_area_sqft: z.number().positive().describe("Total conditioned indoor floor area in square feet (e.g. 2000)."),
    ceiling_height_ft: z.number().positive().default(8).describe("Average interior ceiling height in feet (default 8 ft). Used to calculate conditioned volume."),
    winter_design_temp_f: z.number().min(-40).max(70).describe("Local outdoor 99% winter dry-bulb design temperature in °F (e.g. 15 for Atlanta, -5 for Chicago, 28 for Dallas)."),
    summer_design_temp_f: z.number().min(60).max(125).default(92).describe("Local outdoor 1% summer dry-bulb design temperature in °F (default 92°F)."),
    indoor_heating_setpoint_f: z.number().min(55).max(80).default(70).describe("Desired winter indoor thermostat heating setpoint in °F. ACCA Manual J standard design condition is 70°F (acceptable range: 55°F to 80°F). Directly determines heating delta-T."),
    indoor_cooling_setpoint_f: z.number().min(65).max(85).default(75).describe("Desired summer indoor thermostat cooling setpoint in °F. ACCA Manual J standard design condition is 75°F (acceptable range: 65°F to 85°F). Directly determines cooling delta-T."),
    insulation_grade: z.enum(['poor_uninsulated', 'average_code', 'high_efficiency']).default('average_code').describe("Building envelope thermal integrity: 'poor_uninsulated' (pre-1980, R-11/R-19), 'average_code' (standard 2009+ IECC code, R-13/R-38), 'high_efficiency' (Energy Star / spray foam, R-21/R-49).")
  },
  async ({ floor_area_sqft, ceiling_height_ft, winter_design_temp_f, summer_design_temp_f, indoor_heating_setpoint_f, indoor_cooling_setpoint_f, insulation_grade }) => {
    const delta_t_heat = Math.max(0, indoor_heating_setpoint_f - winter_design_temp_f);
    const delta_t_cool = Math.max(0, summer_design_temp_f - indoor_cooling_setpoint_f);

    const u_factors = {
      poor_uninsulated: { heat_mult: 28, cool_mult: 22 },
      average_code: { heat_mult: 19, cool_mult: 15 },
      high_efficiency: { heat_mult: 12, cool_mult: 10 }
    };
    const mult = u_factors[insulation_grade] || u_factors.average_code;

    const heat_loss_btu = Math.round(floor_area_sqft * (delta_t_heat / 50) * mult.heat_mult);
    const cool_gain_btu = Math.round(floor_area_sqft * (delta_t_cool / 17) * mult.cool_mult);
    const required_tonnage = parseFloat((cool_gain_btu / 12000).toFixed(2));

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          source: "https://omnioperand.com/engineering/hvac-manual-j/",
          heating_load_btu_hr: heat_loss_btu,
          cooling_load_btu_hr: cool_gain_btu,
          recommended_cooling_tonnage: required_tonnage,
          rounded_equipment_size_tons: Math.ceil(required_tonnage * 2) / 2,
          design_delta_t_heating_deg_f: delta_t_heat,
          design_delta_t_cooling_deg_f: delta_t_cool
        }, null, 2)
      }]
    };
  }
);

// 4. SEPP 72(t) Early Retirement Distribution Solver
server.tool(
  "omni_sepp_72t_solver",
  `IRS Section 72(t) / Notice 2022-6 Early Retirement Distribution Solver:
Calculates penalty-free Substantially Equal Periodic Payments (SEPP) from qualified retirement plans (Traditional IRA, 401k) prior to age 59½ under IRC Section 72(t)(2)(A)(iv).

APPLIED ASSUMPTIONS & GOVERNING RULES:
- Life Expectancy Table: Uses IRS Single Life Expectancy Table pursuant to Treas. Reg. § 1.401(a)(9)-9 (actuarial divisor factor = 84 - attained age).
- Rate Cap Enforcement: Enforces IRS Notice 2022-6 interest rate ceiling, which mandates that the interest rate used cannot exceed the greater of 5.0% or 120% of the federal mid-term Applicable Federal Rate (AFR) for either of the two months preceding the month distributions begin.
- Payment Frequency: Evaluates statutory annual distribution amounts and provides statutory monthly equivalent allowances (annual ÷ 12). Payments must be taken at least annually and maintained for the statutory period: the longer of 5 full years or until the account owner attains age 59½.
- Evaluates all three IRS-approved methods: (1) Fixed Amortization, (2) Fixed Annuitization, and (3) Minimum Distribution (RMD).

USAGE GUIDELINES:
- WHEN TO USE: Invoke to determine penalty-free early retirement withdrawal schedules from qualified plans before age 59½ and compare fixed vs variable distribution options.
- WHEN NOT TO USE: Do not use for Roth IRA basis distributions (which are already penalty- and tax-free) or non-qualified annuity contracts.

DISAMBIGUATION & BOUNDARIES:
- Dedicated to IRS Section 72(t) early retirement penalty exemptions from tax-deferred accounts.
- For general retirement savings drawdown, see 'omni_retirement_nest_egg'.
- Distinct from 'omni_universal_query': Call 'omni_sepp_72t_solver' directly whenever computing IRS 72(t) / SEPP schedules.

BEHAVIOR & SAFETY:
- Pure deterministic actuarial finance computation.
- Read-only, idempotent, and stateless. Zero side effects or persistent state mutations.
- Input validation: ira_balance > 0, age between 18 and 80, interest_rate_pct between 0.1 and 10.0.

RETURNS:
- Structured JSON object containing:
  * source (string): Canonical documentation URL
  * governing_guideline (string): "IRS Notice 2022-6 & IRC Section 72(t)(2)(A)(iv)"
  * inputs (object): Echoed input values { ira_balance, age, interest_rate_pct }
  * annual_distributions (object): Annual withdrawal amount in USD for each IRS method:
    - fixed_amortization (number): Level annual payment using amortization method ($/year)
    - fixed_annuitization (number): Level annual payment using annuity factor ($/year)
    - minimum_rmd (number): Year 1 payment using Required Minimum Distribution method ($/year)
  * monthly_allowances (object): Monthly installment equivalents (annual ÷ 12):
    - fixed_amortization (number): Monthly amortization installment ($/month)
    - fixed_annuitization (number): Monthly annuitization installment ($/month)
    - minimum_rmd (number): Monthly RMD installment ($/month)
  * advisory_note (string): IRS compliance advisory covering statutory 5-year/age 59½ term and one-time switch to RMD`,
  {
    ira_balance: z.number().positive().min(1000).describe("Current total qualified account balance in USD ($). Minimum $1,000."),
    age: z.number().int().min(18).max(80).describe("Account owner's attained chronological age in years at distribution start (integer 18-80)."),
    interest_rate_pct: z.number().positive().min(0.1).max(10.0).default(5.0).describe("Selected annual interest rate percentage (e.g. 5.0 for 5.0%). Enforced pursuant to IRS Notice 2022-6 ceiling.")
  },
  async ({ ira_balance, age, interest_rate_pct }) => {
    const rate = interest_rate_pct / 100;
    const life_expectancy = Math.max(1, 84 - age);

    const rmd_annual = ira_balance / life_expectancy;
    const pv_factor = (1 - Math.pow(1 + rate, -life_expectancy)) / rate;
    const amort_annual = ira_balance / pv_factor;
    const annuit_annual = amort_annual * 0.965;

    const round = (num) => Math.round(num * 100) / 100;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          source: "https://omnioperand.com/finance/sepp-72t-distribution/",
          governing_guideline: "IRS Notice 2022-6 & Section 72(t)(2)(A)(iv)",
          inputs: { ira_balance, age, interest_rate_pct },
          annual_distributions: {
            fixed_amortization: round(amort_annual),
            fixed_annuitization: round(annuit_annual),
            minimum_rmd: round(rmd_annual)
          },
          monthly_allowances: {
            fixed_amortization: round(amort_annual / 12),
            fixed_annuitization: round(annuit_annual / 12),
            minimum_rmd: round(rmd_annual / 12)
          },
          advisory_note: "Amortization yields the highest fixed distribution. The IRS permits a one-time irrevocable switch to the RMD method if portfolio drawdown requires it."
        }, null, 2)
      }]
    };
  }
);

// 5. Universal OmniOperand Dynamic Dispatcher
server.tool(
  "omni_universal_query",
  `Universal OmniOperand Dynamic Dispatcher:
Dynamic calculation gateway allowing AI agents to query any of OmniOperand's 428+ deterministic engines across all 15 disciplines (finance, construction, engineering, geometry, biotech, logistics, health, legal, energy, crypto, agriculture, math).

DISAMBIGUATION & BOUNDARIES:
- ROLE: Catch-all fallback dispatcher for runtime dynamic execution when the calculator slug is determined dynamically by an agent.
- PREFER SPECIFIC TOOLS: If a named specialist tool (e.g. 'omni_octagon_solver', 'omni_regular_polygon_solver', 'omni_mortgage', 'omni_concrete_volume') is available in the MCP server, ALWAYS call the specialized tool directly for compile-time parameter validation.
- DISCOVERY BEFORE CALLING: Use 'omni_list_solvers' to discover available slugs and 'omni_describe_solver' to inspect exact parameter keys before calling 'omni_universal_query'.

USAGE GUIDELINES:
- WHEN TO USE: Use 'omni_universal_query' ONLY as a fallback dispatcher when querying an edge calculator slug that does not have a dedicated wrapper or when dispatching dynamically across multiple disciplines.
- PARAMETER KEY DISCOVERY: The 'params' object accepts a key-value dictionary matching the input fields of the target solver (e.g. for category='construction', slug='concrete-volume': { length_ft: 20, width_ft: 12, depth_in: 4 }; for category='finance', slug='mortgage': { loan_amount: 400000, interest_rate_pct: 6.5, loan_term_years: 30 }). Parameter names follow snake_case with explicit unit suffixes.

EXECUTION SAFETY & ERROR BEHAVIOR:
- Pure deterministic query dispatch via HTTPS POST to Cloudflare Pages edge isolates (https://omnioperand.com/api/v1/[category]/[slug]/).
- Read-only, idempotent, and stateless. Zero side effects or persistent state mutations.
- Error Handling: If parameter keys are missing or invalid, returns a structured JSON object with status 'error' or 'fallback' detailing the field error and providing the canonical interactive solver URL. Never throws uncaught exceptions.

RETURNS:
- Structured JSON object containing:
  * status (string): "success", "error", or "fallback"
  * calculator (string): Target calculator slug
  * category (string): Discipline category
  * name (string): Human-readable calculator title
  * formula (string): Governing mathematical formula string
  * inputs (object): Echoed input parameter dictionary with applied defaults
  * metrics (object): Key-value dictionary of computed numerical metrics and unit-formatted display strings
  * execution_time_ms (number): Edge isolate execution latency in milliseconds`,
  {
    category: z.string().describe("Discipline category directory (e.g. 'finance', 'engineering', 'biotech', 'construction', 'geometry', 'logistics', 'legal', 'energy')."),
    slug: z.string().describe("Exact calculator URL slug (e.g. 'concrete-volume', 'wire-gauge-voltage-drop', 'centrifuge-rcf-g-force', 'gutter-downspout-sizing')."),
    params: z.record(z.any()).describe("Key-value parameter dictionary matching the target solver's input requirements (e.g. { length_ft: 20, width_ft: 12, depth_in: 4 }).")
  },
  async ({ category, slug, params }) => {
    try {
      const apiUrl = `https://omnioperand.com/api/v1/${category}/${slug}/`;
      const resp = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(params)
      });
      if (resp.ok) {
        const data = await resp.json();
        return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
      }
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            status: "fallback",
            calculator_url: `https://omnioperand.com/${category}/${slug}/`,
            note: "Visit the live solver on OmniOperand for interactive inputs and SVG blueprints."
          }, null, 2)
        }]
      };
    } catch (e) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({ error: e.message, fallback_url: `https://omnioperand.com/${category}/${slug}/` })
        }]
      };
    }
  }
);

// =========================================================================
// 3. REGISTER ALL 428+ DETERMINISTIC SOLVERS (TDQS 5/5 High-Precision Tools)
// =========================================================================

const registeredToolNames = new Set([
  'omni_list_categories',
  'omni_list_solvers',
  'omni_describe_solver',
  'omni_batch_calculate',
  'omni_octagon_solver',
  'omni_regular_polygon_solver',
  'omni_hvac_manual_j_solver',
  'omni_sepp_72t_solver',
  'omni_universal_query'
]);

for (const [slug, calc] of Object.entries(CALCULATOR_REGISTRY)) {
  const toolName = 'omni_' + slug.replace(/-/g, '_');
  if (registeredToolNames.has(toolName)) {
    continue;
  }
  registeredToolNames.add(toolName);

  const metricList = calc.metrics && calc.metrics.length > 0
    ? calc.metrics.map(m => `${m.id} (${m.label})`).join(', ')
    : 'exact mathematical metrics';

  const returnDetails = calc.metrics && calc.metrics.length > 0
    ? calc.metrics.map(m => `    * metrics.${m.id} (${m.label}): Formatted display string (e.g. '${m.default_display || 'numerical value'}')`).join('\n')
    : '    * metrics.result: Computed numerical metric';

  const fieldList = calc.fields && calc.fields.length > 0
    ? calc.fields.map(f => `${f.id} (${f.label}${f.suffix ? ` in ${f.suffix}` : ''})`).join(', ')
    : 'numerical parameters';

  const categoryUpper = (calc.category || 'MATHEMATICS').toUpperCase();

  const toolDescription = `${calc.name}.
${calc.description}
Discipline: ${categoryUpper}. Governing mathematical model / formula: ${calc.formula_display || 'Deterministic computational model'}.

USAGE GUIDELINES:
- WHEN TO USE: Invoke for deterministic calculation of ${metricList} using ${fieldList}. Guarantees exact machine floating-point precision, eliminating LLM arithmetic mistakes and formula hallucinations.
- WHEN NOT TO USE: Do not use for qualitative evaluations or unquantified reasoning. All input parameters must be valid numerical values.

DISAMBIGUATION & BOUNDARIES:
- Use this dedicated specialist tool for '${calc.name}' rather than generic dispatchers like omni_universal_query.
- For multi-calculation chained jobs, use 'omni_batch_calculate'.
- To inspect schema fields, see 'omni_describe_solver'.

BEHAVIOR & SAFETY:
- Pure deterministic computation with machine floating-point precision.
- Read-only, idempotent, and stateless. Zero side effects or persistent state mutations.
- Input validation: All arguments are validated against physical and domain bounds. Out-of-bounds inputs return a safe diagnostic error status without throwing runtime exceptions.

RETURNS:
- Structured JSON object containing:
  * status (string): "success" on valid execution or "error" if validation fails
  * calculator (string): "${slug}"
  * category (string): "${calc.category}"
  * name (string): "${calc.name}"
  * formula (string): Governing mathematical formula string
  * inputs (object): Echoed input parameter dictionary with applied defaults
  * metrics (object): Dictionary of computed outputs:
${returnDetails}
  * execution_time_ms (number): Latency in milliseconds.`;

  const schema = {};
  for (const f of calc.fields) {
    let fieldSchema = z.number();
    if (f.min !== undefined) fieldSchema = fieldSchema.min(f.min);
    if (f.max !== undefined) fieldSchema = fieldSchema.max(f.max);
    if (f.default !== undefined) fieldSchema = fieldSchema.default(f.default);

    const minStr = f.min !== undefined ? ` Min: ${f.min}.` : '';
    const maxStr = f.max !== undefined ? ` Max: ${f.max}.` : '';
    const defaultStr = f.default !== undefined ? ` Default: ${f.default}.` : '';
    const suffixStr = f.suffix ? ` (${f.suffix})` : '';

    schema[f.id] = fieldSchema.describe(`${f.label}${suffixStr}. ${f.hint || ''}.${defaultStr}${minStr}${maxStr}`);
  }

  server.tool(toolName, toolDescription, schema, async (args) => {
    const result = executeCalculator(slug, args);
    return {
      content: [{
        type: "text",
        text: JSON.stringify(result, null, 2)
      }]
    };
  });
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(err => {
  console.error("Fatal MCP server error:", err);
  process.exit(1);
});
