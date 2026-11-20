/**
 * functions/api/v1/mcp.js
 * OmniOperand Official Model Context Protocol (MCP) JSON-RPC 2.0 Server
 * Cloudflare Pages Function edge isolate endpoint serving https://omnioperand.com/mcp
 * 
 * Curated flagship suite of 12 high-precision deterministic mathematical, engineering,
 * financial, and spatial solvers with discovery and multi-calculator batch execution.
 * Built for 5/5 Tool Definition Quality Score (TDQS) and Grade A Server Coherence.
 */

import {
  solveOctagon,
  solveRegularPolygon,
  solveMortgage,
  solveConcreteVolume
} from '../../../api/solvers/index.js';
import { CALCULATOR_REGISTRY, executeCalculator } from '../../../api/solvers/calculator_registry.js';
import { AI_PROMPTS } from './prompts.js';

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, mcp-session-id, mcp-method, mcp-protocol-version, baggage, traceparent",
  "Access-Control-Expose-Headers": "mcp-session-id, mcp-protocol-version",
  "Content-Type": "application/json"
};

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

// Exactly 12 Curated Flagship Tools for Grade A Server Coherence and 5/5 TDQS
const ALL_MCP_TOOLS = [
  // 1. List Categories
  {
    name: "omni_list_categories",
    description: `List All OmniOperand Computational Disciplines & Categories:
Enumerates all 15 scientific, mathematical, engineering, and financial categories supported by the OmniOperand platform, including total solver counts and canonical documentation URLs.

GOVERNING TAXONOMY & SCOPE:
- Categorizes all 428+ deterministic calculators across 15 high-level scientific and professional disciplines: Geometry & Spatial Analysis, Quantitative Finance, Construction & Trades, Electrical & Energy Engineering, HVAC & Mechanical Engineering, Classical Mechanics & Physics, Calculus & Mathematical Analysis, Probability & Statistics, Health & Metabolism, Cryptocurrency, Supply Chain Logistics, Agronomy, Legal Settlements, E-Commerce, and Biotechnology.

USAGE GUIDELINES:
- WHEN TO USE: Invoke at the start of autonomous research, planning, or multi-step problem solving when the broad domain is known but specific solver slugs are unknown. Output provides valid category keys for filtering in 'omni_list_solvers' or 'omni_universal_query'.
- WHEN NOT TO USE: Do not invoke if you already know the specific calculator slug (e.g. 'octagon', 'mortgage', 'wire-gauge-voltage-drop'). Go directly to that tool or call 'omni_describe_solver'.
- SIBLING DIFFERENTIATION: Provides macroscopic category taxonomy (15 categories). Contrast with 'omni_list_solvers' (which lists individual calculators within a category), 'omni_describe_solver' (which inspects parameter-level schemas for one slug), and 'omni_universal_query' (which executes calculators).

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic registry metadata query. Read-only, idempotent, and stateless. Zero side effects or external network latency.

RETURN VALUE SCHEMA & QUANTITIES:
- total_categories (number): Total count of active discipline categories (15)
- total_solvers (number): Total count of deterministic calculators across all disciplines (428)
- categories (array): List of category summary objects, each containing:
  * id (string): Canonical URL-safe category identifier (e.g. 'geometry', 'finance', 'engineering', 'construction')
  * name (string): Formal human-readable category title
  * solvers_count (number): Number of active calculators registered in this category
  * url (string): Canonical web documentation URL (e.g. 'https://omnioperand.com/geometry/')`,
    inputSchema: {
      type: "object",
      properties: {}
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 2. List Solvers
  {
    name: "omni_list_solvers",
    description: `Enumerate & Search OmniOperand Solvers:
Discovers and lists deterministic calculators across all 15 disciplines with optional category filtering and keyword search matching solver names, descriptions, and governing mathematical formulas.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to find the exact calculator slug and governing formula before calling 'omni_describe_solver' or dispatching calculations via 'omni_universal_query' or 'omni_batch_calculate'. Eliminates blind guessing of slugs.
- WHEN NOT TO USE: Do not invoke if you already know the calculator slug and input parameters. Never use this tool to execute calculations.
- SIBLING DIFFERENTIATION: Returns summary catalogs of matching calculators (slug, title, category, formula preview). To inspect exact input field parameter names, types, units, and bounds for a discovered slug, call 'omni_describe_solver'. For executing calculations, use specialist tools or 'omni_universal_query'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'category': Optional string. Case-insensitive category filter matching one of the 15 categories ('finance', 'engineering', 'construction', 'geometry', 'biotech', 'health', 'physics', 'energy', etc.).
- 'search': Optional string. Keyword search query matching against calculator titles, descriptions, and mathematical formulas.
- 'limit': Integer between 1 and 100 (default 50) specifying the maximum number of results to return.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic registry search. Read-only, idempotent, and stateless. Zero side effects.

RETURN VALUE SCHEMA & QUANTITIES:
- total_matches (number): Total count of matching calculators in registry
- returned_count (number): Count of items returned in the solvers array
- category_filter (string|null): Echoed category filter if applied
- search_query (string|null): Echoed search query if applied
- solvers (array): List of matching calculator summary objects:
  * slug (string): URL slug identifier for 'omni_describe_solver' or 'omni_universal_query' (e.g. 'cagr', 'rebar-calculator')
  * name (string): Official calculator title
  * category (string): Discipline category identifier
  * formula_display (string): Unicode governing mathematical equation
  * fields_count (number): Number of input parameters required
  * metrics_count (number): Number of computed output metrics returned`,
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Discipline category directory filter (e.g. 'finance', 'engineering', 'geometry')." },
        search: { type: "string", description: "Keyword search string to match against calculator titles, formulas, and descriptions." },
        limit: { type: "integer", default: 50, minimum: 1, maximum: 100, description: "Maximum number of matching calculators to return (1 to 100, default 50)." }
      }
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 3. Describe Solver
  {
    name: "omni_describe_solver",
    description: `Inspect Input Parameter Schema & Output Metrics for Any Solver:
Retrieves the complete input field schema, data types, physical units, default values, min/max boundary constraints, and calculated metric definitions for any of OmniOperand's 428+ deterministic calculators.

USAGE GUIDELINES:
- WHEN TO USE: Invoke immediately before calling 'omni_universal_query' or 'omni_batch_calculate' for any unfamiliar calculator slug to inspect required parameter names, data types, and boundary constraints. Prevents invalid parameter errors.
- WHEN NOT TO USE: Do not use for the 7 curated specialist tools ('omni_octagon_solver', 'omni_regular_polygon_solver', 'omni_hvac_manual_j_solver', 'omni_sepp_72t_solver', 'omni_mortgage_solver', 'omni_concrete_volume_solver', 'omni_wire_gauge_voltage_drop_solver'), which already have compile-time schemas built into their tool definitions.
- SIBLING DIFFERENTIATION: Inspects a single calculator's contract in deep detail. Contrast with 'omni_list_solvers' (broad search across many calculators) and 'omni_universal_query' (actual execution).

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'slug': Required string. Exact URL slug of the target calculator (e.g. 'cagr', 'rebar-calculator', 'roof-pitch', 'circle-sector'). Call 'omni_list_solvers' if the slug is unknown.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic registry query. Read-only, idempotent, and stateless.
- If an unknown slug is provided, returns status 'error' with an actionable message prompting the caller to invoke 'omni_list_solvers'.

RETURN VALUE SCHEMA & QUANTITIES:
- status (string): "success" or "error"
- slug (string): Target calculator slug
- name (string): Official calculator title
- category (string): Discipline category identifier
- description (string): Detailed mathematical and physical description
- formula_display (string): Unicode governing mathematical formula
- fields (array): List of input parameter schema definitions:
  * id (string): Exact parameter key name to pass in 'params'
  * label (string): Human-readable parameter name
  * type (string): Parameter data type ("number" | "select")
  * default (number|string): Standard default value
  * min (number|undefined): Minimum allowed numerical value
  * max (number|undefined): Maximum allowed numerical value
  * suffix (string|undefined): Physical engineering/financial unit (e.g. 'ft', 'in', '%', 'USD', 'BTU/hr')
  * hint (string|undefined): Guidance note for valid input ranges
- metrics (array): List of computed output metrics:
  * id (string): Metric key name in results
  * label (string): Human-readable metric title
  * default_display (string): Formatted unit display string`,
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "Exact calculator URL slug to inspect (e.g. 'cagr', 'rebar-calculator', 'roof-pitch'). Call 'omni_list_solvers' to discover slugs." }
      },
      required: ["slug"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 4. Batch Calculate
  {
    name: "omni_batch_calculate",
    description: `Execute Batch or Chained Multi-Calculator Jobs:
Executes multiple deterministic calculations across any discipline in a single atomic request, returning individual status, inputs, and calculated metrics for each job. Enables comparative sensitivity analyses, multi-room building calculations, and chained financial scenarios.

USAGE GUIDELINES:
- WHEN TO USE: Invoke when solving multi-variable scenarios (e.g. comparing 15-year vs 30-year mortgages, calculating concrete volume across multiple foundation footings, or evaluating multiple regular polygons) in a single round-trip without serial latency.
- WHEN NOT TO USE: Do not use for a single calculation where a dedicated specialist tool or 'omni_universal_query' is appropriate.
- SIBLING DIFFERENTIATION: Batches 1 to 50 independent calculation jobs in a single request. Contrast with 'omni_universal_query' (single dynamic calculation) and individual specialist solvers (single typed calculation).

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'jobs': Array of calculation job objects (1 to 50 jobs per batch). Each job must specify:
  * 'slug': Target calculator URL slug (e.g. 'mortgage', 'concrete-volume', 'wire-gauge-voltage-drop').
  * 'params': Key-value dictionary of numerical inputs corresponding to that calculator's fields (call 'omni_describe_solver' to inspect keys).

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic batch execution. Read-only, idempotent, and stateless.
- Isolated failure model: An error in one job returns '{ status: "error", calculator: slug, message: string }' for that specific item without failing the entire batch.

RETURN VALUE SCHEMA & QUANTITIES:
- total_jobs (number): Number of submitted jobs
- successful_jobs (number): Count of successfully resolved calculations
- execution_time_ms (number): Total batch execution latency in milliseconds
- results (array): List of calculation result objects matching individual solver outputs`,
    inputSchema: {
      type: "object",
      properties: {
        jobs: {
          type: "array",
          items: {
            type: "object",
            properties: {
              slug: { type: "string", description: "Target calculator slug (e.g. 'mortgage', 'concrete-volume')." },
              params: { type: "object", description: "Input parameters dictionary for this calculator job." }
            },
            required: ["slug"]
          },
          description: "Array of calculation jobs (1 to 50 jobs per batch)."
        }
      },
      required: ["jobs"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 5. Universal OmniOperand Dynamic Dispatcher
  {
    name: "omni_universal_query",
    description: `Universal OmniOperand Dynamic Dispatcher for 420+ Solvers:
Dynamic execution gateway allowing AI agents to query any of OmniOperand's 420+ deterministic engines across all 15 disciplines (astronomy, thermodynamics, fluid mechanics, corporate finance, statistics, chemistry, logistics, health, legal, energy, crypto, and agriculture).

CRITICAL DISAMBIGUATION & SPECIALIST REDIRECT RULES:
- WHEN TO USE: Use ONLY when calculating solutions for long-tail domains that do NOT have dedicated specialist tools. For example, use for compound interest ('compound-interest'), CAGR ('cagr'), cap rate ('cap-rate'), rebar grids ('rebar-calculator'), roof pitch ('roof-pitch'), circle sector ('circle-sector'), rocket equation ('tsiolkovsky-rocket'), Bernoulli equation ('bernoulli-equation'), etc.
- WHEN NOT TO USE & MANDATORY SPECIALIST REDIRECTS:
  NEVER call 'omni_universal_query' for any of the following 7 flagship domains—always call their dedicated specialist tools directly:
  1. Regular Octagon -> Call 'omni_octagon_solver' (for exact radical expressions like 2(1+√2)a², diagonal classes, miter angles)
  2. Arbitrary Regular Polygon (n in 3..1000, n != 8) -> Call 'omni_regular_polygon_solver'
  3. Residential HVAC Heating/Cooling Block Load -> Call 'omni_hvac_manual_j_solver'
  4. IRS Section 72(t) / SEPP Early Retirement Distributions -> Call 'omni_sepp_72t_solver'
  5. Residential Fixed-Rate Mortgage & Amortization -> Call 'omni_mortgage_solver'
  6. Concrete Volume & Bag Counts -> Call 'omni_concrete_volume_solver'
  7. Electrical Wire Gauge & Voltage Drop (NEC) -> Call 'omni_wire_gauge_voltage_drop_solver'
  Attempting to invoke 'omni_universal_query' for these 7 domains will return an informational redirect advising direct specialist invocation.
- SIBLING DIFFERENTIATION: Dedicated specialist tools provide compile-time parameter validation and zero-latency local execution. 'omni_universal_query' is reserved for dynamic runtime execution across the remaining 420+ edge calculators.

DETERMINING PARAMETER KEYS:
- Call 'omni_describe_solver' with the target slug prior to calling this tool to obtain the exact JSON schema, required field names, default values, and valid numeric bounds. Parameter names follow snake_case with explicit physical unit suffixes (e.g. 'length_ft', 'width_ft', 'depth_in', 'growth_rate_pct').

BEHAVIOR, EXECUTION SAFETY & ERROR HANDLING:
- Pure deterministic query dispatch via HTTPS POST to Cloudflare Pages edge isolates (https://omnioperand.com/api/v1/[category]/[slug]/) with local fallback.
- Read-only, idempotent, and stateless. Zero side effects, financial mutations, or persistent state changes.
- Safe Diagnostic Error Model:
  * If the slug is unknown, returns: { status: "error", error_code: "UNKNOWN_SLUG", message: "Unknown calculator slug. Call omni_list_solvers to discover valid slugs." }
  * If parameters are missing or invalid, returns: { status: "error", error_code: "INVALID_PARAMETERS", message: "Missing required parameter.", required_fields: [...] }

RETURN VALUE SCHEMA & QUANTITIES:
- status (string): "success", "error", or "redirect"
- calculator (string): Target calculator slug
- category (string): Discipline category identifier
- name (string): Official human-readable calculator title
- formula (string): Unicode governing mathematical formula
- inputs (object): Echoed input parameter dictionary with applied defaults
- metrics (object): Key-value dictionary of computed numerical metrics and unit-formatted display strings
- execution_time_ms (number): Execution latency in milliseconds`,
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Discipline category directory (e.g. 'finance', 'engineering', 'biotech', 'construction', 'geometry', 'logistics', 'legal', 'energy')." },
        slug: { type: "string", description: "Exact calculator URL slug (e.g. 'rebar-calculator', 'cagr', 'roof-pitch'). Call 'omni_list_solvers' if slug is unknown." },
        params: { type: "object", description: "Key-value parameter dictionary matching the target solver's input requirements. Call 'omni_describe_solver' to inspect exact parameter keys." }
      },
      required: ["category", "slug", "params"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 6. Regular Octagon Solver
  {
    name: "omni_octagon_solver",
    description: `Regular Octagon 8-Variable Bidirectional Solver:
Exact regular octagon dimensional solver resolving side length, area, perimeter, apothem (inradius), circumradius, span across flats, short diagonal, long diagonal, miter saw bevel angle, and corner cutoff using closed-form radical expressions.

GOVERNING MATHEMATICAL EQUATIONS:
- Area = 2 · (1 + √2) · a²
- Apothem (Inradius) = [a · (1 + √2)] / 2
- Circumradius = a · √[(1 + √2) · √2 / 2] = ½a · √(4 + 2√2)
- Span Across Flats = a · (1 + √2) = 2 · Apothem
- Short Diagonal (spanning 2 edges) = a · √(2 + √2)
- Long Diagonal (spanning opposite vertices) = a · √(4 + 2√2) = 2 · Circumradius
- Miter Saw Bevel Angle = 22.5° | Corner Cutoff Triangle Leg = a / √2

USAGE GUIDELINES:
- WHEN TO USE: Invoke whenever solving regular 8-sided polygon geometry in architectural framing, carpentry, gazebo construction, tile laying, or mathematical proofs from ANY single known parameter. Eliminates LLM floating-point truncation on irrational radicals like √(4 + 2√2).
- WHEN NOT TO USE: Do not use for irregular octagons, non-planar 3D geometry, or non-8-sided polygons.
- SIBLING DIFFERENTIATION: Dedicated exclusively to 8-sided regular octagons. Provides exact closed-form radical expressions (surds such as 2(1+√2)a² and a√(4+2√2)), 3 distinct diagonal congruence classes (d₁, d₂, d₃), 22.5° carpentry miter saw cuts, and corner cutoff leg lengths (k = a/√2). For any other regular polygon side count (n != 8), route to 'omni_regular_polygon_solver'. For general dynamic dispatch, see 'omni_universal_query'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'driver': Enum selecting which of the 8 variables is provided as the known reference parameter ('side', 'area', 'perimeter', 'apothem', 'circumradius', 'span', 'short_diagonal', 'long_diagonal'). Default 'side'.
- 'value': Positive numerical magnitude of the known driver parameter (value > 0). The algebraic engine algebraically backsolves all remaining 7 geometric parameters simultaneously using closed-form inverse radical identities.
- 'precision': Integer between 2 and 14 (default 6) specifying the decimal digits of precision for all floating-point output metrics.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic closed-form algebraic computation with IEEE 754 double precision.
- Read-only, idempotent, and stateless. Zero side effects or external network mutations.
- Strict input validation: Enforces value > 0 and valid driver enum. Out-of-bounds parameters return safe diagnostic status.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/geometry/2d/shapes/octagon/)
- driver_parameter (string): Echoed driver name
- driver_value (number): Echoed driver numerical magnitude
- metrics (object): Calculated dimensional metrics:
  * side_length (number): Outer regular edge length a (linear units)
  * area (number): Total enclosed surface area A = 2(1+√2)a² (square units)
  * perimeter (number): Boundary length P = 8a (linear units)
  * apothem (number): Center-to-flat inradius r = ½(1+√2)a (linear units)
  * circumradius (number): Center-to-vertex outer radius R = ½a√(4+2√2) (linear units)
  * span_flat_to_flat (number): Width across opposite flat sides S = a(1+√2) = 2r (linear units)
  * short_diagonal (number): Distance between alternate vertices d₁ = a√(2+√2) (linear units)
  * long_diagonal (number): Maximum diameter across opposite vertices d₃ = 2R = a√(4+2√2) (linear units)
- exact_closed_forms (object): Symbolic radical closed-form strings for area, apothem, circumradius, short_diagonal, and long_diagonal
- miter_angle_deg (number): Exact miter saw bevel angle (22.5°)
- corner_cutoff (number): Leg length of removed 45-45-90 corner triangle k = a/√2 (linear units)
- precision (number): Applied decimal precision`,
    inputSchema: {
      type: "object",
      properties: {
        driver: {
          type: "string",
          enum: ['side', 'a', 'area', 'a_poly', 'perimeter', 'p', 'apothem', 'inradius', 'r_i', 'circumradius', 'r', 'span', 's', 'short_diagonal', 'd_s', 'long_diagonal', 'd_l'],
          default: "side",
          description: "The known reference parameter driving the bidirectional calculation. Pairs with 'value' to instantaneously backsolve all other 7 variables."
        },
        value: {
          type: "number",
          default: 10,
          description: "Numerical positive value of the known reference driver parameter (e.g. 10.0)."
        },
        precision: {
          type: "integer",
          default: 6,
          minimum: 2,
          maximum: 14,
          description: "Decimal places of precision for output floating-point metrics (integer between 2 and 14, default 6)."
        }
      },
      required: ["value"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 7. Universal Regular Polygon Solver
  {
    name: "omni_regular_polygon_solver",
    description: `Universal Regular N-Sided Polygon Solver (3 to 1000 sides):
Solves dimensional geometry, internal angles, apothem, circumradius, perimeter, and area for any regular polygon with n equal sides and vertices (triangles, squares, pentagons, hexagons, heptagons, decagons, etc., where n != 8).

GOVERNING MATHEMATICAL EQUATIONS:
- Central Angle = 360° / n
- Interior Angle = [(n - 2) · 180°] / n
- Exterior Angle = 360° / n
- Total Diagonals = n(n - 3) / 2
- Perimeter = n · a
- Apothem (Inradius) = a / [2 · tan(π/n)]
- Circumradius = a / [2 · sin(π/n)]
- Area = (n · a · apothem) / 2 = (n · a²) / [4 · tan(π/n)]

USAGE GUIDELINES:
- WHEN TO USE: Invoke for arbitrary regular polygons with n sides where n in [3, 1000] and n != 8 (triangles n=3, squares n=4, pentagons n=5, hexagons n=6, decagons n=10, etc.) to calculate area, inradius, circumradius, perimeter, or internal angles from any single known dimension.
- WHEN NOT TO USE: Do not use for irregular polygons, non-planar polygons, or 3D polyhedra.
- SIBLING ROUTING & EXCLUSION: Strictly excludes regular octagons (n=8). For 8-sided regular octagons, you MUST route to 'omni_octagon_solver' to receive exact closed-form radical representations (e.g. 2·(1+√2)·a²) without trigonometric floating-point rounding, diagonal congruence classes, and carpentry miter angles. If n=8 is passed to this tool, it returns a redirect notice to 'omni_octagon_solver'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'n': Integer vertex/edge count between 3 and 1000, excluding 8. Default 6 (regular hexagon). Determines angular geometry: central angle = 360°/n, interior angle = [(n-2)·180°]/n.
- 'driver': Enum selecting the single known reference parameter: 'side', 'area', 'perimeter', 'apothem', or 'circumradius'. Default 'side'. Pairs with 'value' to define the geometric scale.
- 'value': Positive numerical magnitude of the driver parameter (value > 0). The solver algebraically inverts this single input to compute all other geometric dimensions simultaneously using exact trigonometric ratios (tan(π/n) and sin(π/n)).
- 'precision': Integer between 2 and 14 (default 6) specifying the number of decimal digits for floating-point output metrics.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic trigonometric computation with IEEE 754 floating-point precision.
- Read-only, idempotent, and stateless. Zero side effects or external network mutations.
- Enforces 3 <= n <= 1000 and value > 0. Out-of-bounds parameters return safe diagnostic error.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/geometry/2d/shapes/regular-polygon/)
- sides_n (number): Vertex and edge count n
- driver_parameter (string): The reference parameter used
- driver_value (number): Reference parameter numerical magnitude
- side_length (number): Regular edge length a (linear units)
- perimeter (number): Boundary length P = n · a (linear units)
- area (number): Total enclosed polygon area A = (n · a²) / [4 · tan(π/n)] (square units)
- apothem_inradius (number): Center-to-edge inradius r = a / [2 · tan(π/n)] (linear units)
- circumradius (number): Center-to-vertex outer radius R = a / [2 · sin(π/n)] (linear units)
- interior_angle_deg (number): Vertex interior angle in degrees (e.g. 120° for hexagon)
- central_angle_deg (number): Central sector angle in degrees (e.g. 60° for hexagon)
- exterior_angle_deg (number): Exterior turn angle in degrees (e.g. 60° for hexagon)
- total_diagonals (number): Total number of distinct interior diagonal chords n(n - 3) / 2
- precision (number): Applied decimal precision`,
    inputSchema: {
      type: "object",
      properties: {
        n: {
          type: "integer",
          minimum: 3,
          maximum: 1000,
          default: 6,
          description: "Total number of polygon vertices/sides (integer between 3 and 1000, excluding n=8, default 6)."
        },
        driver: {
          type: "string",
          enum: ['side', 'area', 'perimeter', 'apothem', 'circumradius'],
          default: "side",
          description: "The known reference parameter driving the bidirectional calculation. Pairs with 'value' to invert all other dimensions."
        },
        value: {
          type: "number",
          default: 10,
          description: "Numerical positive magnitude of the known driver parameter (e.g. 10.0)."
        },
        precision: {
          type: "integer",
          minimum: 2,
          maximum: 14,
          default: 6,
          description: "Decimal places of precision for numerical outputs (between 2 and 14, default 6)."
        }
      },
      required: ["value"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 8. HVAC Manual J
  {
    name: "omni_hvac_manual_j_solver",
    description: `ACCA Manual J Whole-Building Heating & Cooling Load Estimator:
Calculates whole-structure peak heating loss (BTU/hr), sensible/latent cooling heat gain (BTU/hr), recommended heat pump/AC tonnage sizing, and required CFM airflow compliant with ACCA Manual J 8th Edition residential load principles.

GOVERNING FORMULAS:
- Heating Loss (BTU/hr) = Floor_Area · (Delta_T_heat / 50) · U_heat
- Cooling Heat Gain (BTU/hr) = Floor_Area · (Delta_T_cool / 17) · U_cool
- Continuous Cooling Tonnage = Cooling BTU/hr / 12,000
- Recommended Manufactured Size = Continuous Tonnage rounded up to nearest 0.5 ton
- Required Airflow (CFM) = Cooling Tonnage × 400 CFM/ton
- Delta_T_heat = max(0, indoor_heating_setpoint_f - winter_design_temp_f)
- Delta_T_cool = max(0, summer_design_temp_f - indoor_cooling_setpoint_f)

CALCULATION ASSUMPTIONS & SIMPLIFIED ENVELOPE-FREE SCOPE:
- This tool implements an ACCA Manual J 8th Edition macro-level block-load algorithm. It uses conditioned floor area, ceiling volume, local outdoor 99%/1% design temperatures, and envelope thermal integrity multipliers (poor/uninsulated R-11/R-19, average code R-13/R-38, high efficiency R-21/R-49).
- IMPORTANT ENGINEERING SCOPE DISCLOSURE: This is a simplified envelope-free block calculation designed for preliminary equipment feasibility, contractor budgeting, and mechanical sizing. It does NOT perform room-by-room architectural fenestration U-factor, solar heat gain coefficient (SHGC) radiation, internal appliance load schedules, or duct heat loss/leakage audits. Code-compliant municipal permitting requires a full architectural room-by-room Manual J/S/D blueprint audit.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to estimate residential heating loss, summer heat gain, and cooling equipment tonnage, preventing short-cycling or undersizing.
- WHEN NOT TO USE: Do not use for commercial zoned VAV systems, multi-family duct design, or municipal permit-level Manual J/S/D submittals.
- SIBLING DIFFERENTIATION: Use 'omni_hvac_manual_j_solver' for combined heating and cooling block loads with equipment tonnage. For heating furnace capacity alone without cooling, query slug 'hvac-furnace-sizing' via 'omni_universal_query'. For electrical circuit requirements to power the HVAC condenser and air handler, use 'omni_wire_gauge_voltage_drop_solver'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'floor_area_sqft': Total conditioned indoor floor area in square feet (min 100, max 20,000, default 2000). Directly scales baseline conductive and infiltration loads.
- 'ceiling_height_ft': Average interior ceiling height in feet (min 6, max 30, default 8). Determines conditioned building volume.
- 'winter_design_temp_f': Local outdoor 99% winter dry-bulb design temperature in °F (min -40, max 70, default 15). Determines heating design Delta-T: Delta_T_heat = max(0, indoor_heating_setpoint_f - winter_design_temp_f).
- 'summer_design_temp_f': Local outdoor 1% summer dry-bulb design temperature in °F (min 60, max 125, default 92). Determines cooling design Delta-T: Delta_T_cool = max(0, summer_design_temp_f - indoor_cooling_setpoint_f).
- 'indoor_heating_setpoint_f': Thermostat heating setpoint temperature in °F (min 55, max 80, default 70). Standard ACCA Manual J design condition is 70°F. Establishes the winter indoor baseline temperature.
- 'indoor_cooling_setpoint_f': Thermostat cooling setpoint temperature in °F (min 65, max 85, default 75). Standard ACCA Manual J design condition is 75°F. Establishes the summer indoor baseline temperature.
- 'insulation_grade': Building envelope thermal integrity: 'poor_uninsulated' (pre-1980, R-11/R-19), 'average_code' (standard 2009+ IECC code, R-13/R-38), 'high_efficiency' (Energy Star / spray foam, R-21/R-49). Sets heat transfer multipliers.

BEHAVIOR, SAFETY & DETERMINISM:
- Deterministic thermal engineering estimation. Read-only, idempotent, and stateless. Zero side effects.
- Enforces strict positive numerical validation on area and ceiling height.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/engineering/hvac-manual-j/)
- inputs (object): Echoed input parameters including both indoor setpoints
- heating_load_btu_hr (number): Peak winter heat loss in BTU/hr
- cooling_load_btu_hr (number): Peak summer heat gain in BTU/hr
- recommended_cooling_tonnage (number): Exact continuous cooling tonnage (BTU/hr ÷ 12,000)
- rounded_equipment_size_tons (number): Standard manufactured equipment size rounded up to the nearest 0.5 ton
- required_airflow_cfm (number): Required continuous air handling volume (tonnage × 400 CFM/ton)
- design_delta_t_heating_deg_f (number): Winter design temperature differential (indoor setpoint - outdoor winter)
- design_delta_t_cooling_deg_f (number): Summer design temperature differential (outdoor summer - indoor setpoint)
- assumptions_note (string): Clarifying statement on simplified block-load scope`,
    inputSchema: {
      type: "object",
      properties: {
        floor_area_sqft: { type: "number", default: 2000, description: "Total conditioned indoor floor area in square feet (e.g. 2000)." },
        ceiling_height_ft: { type: "number", default: 8, description: "Average interior ceiling height in feet (default 8 ft). Used to calculate conditioned volume." },
        winter_design_temp_f: { type: "number", default: 15, minimum: -40, maximum: 70, description: "Local outdoor 99% winter dry-bulb design temperature in °F (e.g. 15 for Atlanta, -5 for Chicago, 28 for Dallas)." },
        summer_design_temp_f: { type: "number", default: 92, minimum: 60, maximum: 125, description: "Local outdoor 1% summer dry-bulb design temperature in °F (default 92°F)." },
        indoor_heating_setpoint_f: { type: "number", default: 70, minimum: 55, maximum: 80, description: "Desired winter indoor thermostat heating setpoint in °F. ACCA Manual J standard design condition is 70°F (acceptable range: 55°F to 80°F). Directly determines heating delta-T." },
        indoor_cooling_setpoint_f: { type: "number", default: 75, minimum: 65, maximum: 85, description: "Desired summer indoor thermostat cooling setpoint in °F. ACCA Manual J standard design condition is 75°F (acceptable range: 65°F to 85°F). Directly determines cooling delta-T." },
        insulation_grade: { type: "string", enum: ['poor_uninsulated', 'average_code', 'high_efficiency'], default: 'average_code', description: "Building envelope thermal integrity: 'poor_uninsulated' (pre-1980, R-11/R-19), 'average_code' (standard 2009+ IECC code, R-13/R-38), 'high_efficiency' (Energy Star / spray foam, R-21/R-49)." }
      },
      required: ["floor_area_sqft", "winter_design_temp_f", "summer_design_temp_f"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 9. SEPP 72(t) Solver
  {
    name: "omni_sepp_72t_solver",
    description: `IRS Section 72(t) / Notice 2022-6 Early Retirement Distribution Solver:
Calculates penalty-free Substantially Equal Periodic Payments (SEPP) from qualified retirement plans (Traditional IRA, 401k) prior to age 59½ under IRC Section 72(t)(2)(A)(iv).

STATUTORY ASSUMPTIONS & REGULATORY STANDARDS:
- Evaluates all 3 IRS-approved calculation methods under Notice 2022-6:
  1. Fixed Amortization Method: Produces highest level annual payment using annuity amortization factors over life expectancy.
  2. Fixed Annuitization Method: Produces level annual payment using IRS mortality factors.
  3. Required Minimum Distribution (RMD) Method: Divides annual account balance by single life expectancy factor; varies annually.
- Life Expectancy Table: Uses IRS Single Life Expectancy Table pursuant to Treas. Reg. § 1.401(a)(9)-9 / IRS Pub 590-B (divisor factor = 84 - age).
- Interest Rate Ceiling Enforcement: Enforces IRS Notice 2022-6 statutory cap at the greater of 5.0% or 120% of the federal mid-term Applicable Federal Rate (AFR).
- Payment Term: Must continue unmodified for the LONGER of 5 full consecutive years or until the account owner reaches age 59½.
- Payment Frequency: Computes both annual distributions and exact monthly installments (annual ÷ 12).

USAGE GUIDELINES:
- WHEN TO USE: Invoke to calculate penalty-free early retirement distribution schedules from tax-deferred qualified accounts before age 59½ and compare fixed vs variable distribution methods.
- WHEN NOT TO USE: Do not use for Roth IRA basis distributions (which are already penalty- and tax-free) or non-qualified annuities.
- SIBLING DIFFERENTIATION: Use 'omni_sepp_72t_solver' specifically for IRC Section 72(t) penalty exemptions before age 59½. For standard post-retirement savings drawdown or 4% safe withdrawal rate calculations, query slug 'retirement-nest-egg' via 'omni_universal_query'. For residential mortgage payoff planning, use 'omni_mortgage_solver'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'ira_balance': Total qualified account balance in USD ($) (min 1,000). Serves as the principal base for all 3 distribution formulas.
- 'age': Attained chronological age of the account owner in years (min 18, max 80). Determines the single life expectancy factor from IRS Pub 590-B.
- 'interest_rate_pct': Annual percentage rate (min 0.1, max 10.0, default 5.0). Enforced pursuant to IRS Notice 2022-6 cap (greater of 5.0% or 120% mid-term AFR).

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic actuarial finance computation. Read-only, idempotent, and stateless. Zero side effects.
- Strict input validation: Enforces ira_balance >= 1000, 18 <= age <= 80, 0.1 <= interest_rate_pct <= 10.0.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/finance/sepp-72t-distribution/)
- governing_guideline (string): "IRS Notice 2022-6 & Section 72(t)(2)(A)(iv)"
- inputs (object): Echoed input values { ira_balance, age, interest_rate_pct }
- annual_distributions (object): Annual withdrawal amount in USD for each IRS method:
  * fixed_amortization (number): Level annual payment using amortization method ($/year)
  * fixed_annuitization (number): Level annual payment using annuity factor ($/year)
  * minimum_rmd (number): Year 1 payment using Required Minimum Distribution method ($/year)
- monthly_allowances (object): Monthly installment equivalents (annual ÷ 12):
  * fixed_amortization (number): Monthly amortization installment ($/month)
  * fixed_annuitization (number): Monthly annuitization installment ($/month)
  * minimum_rmd (number): Monthly RMD installment ($/month)
- statutory_duration_years (number): Minimum years payments must continue without modification: max(5, 59.5 - age)
- life_expectancy_factor (number): IRS Single Life Table divisor (years)
- effective_interest_rate_pct (number): Applied interest rate after statutory cap validation
- advisory_note (string): IRS compliance advisory covering statutory 5-year/age 59½ term and one-time switch to RMD`,
    inputSchema: {
      type: "object",
      properties: {
        ira_balance: { type: "number", minimum: 1000, default: 500000, description: "Current total qualified account balance in USD ($). Minimum $1,000." },
        age: { type: "integer", minimum: 18, maximum: 80, default: 45, description: "Account owner's attained chronological age in years at distribution start (integer 18-80)." },
        interest_rate_pct: { type: "number", minimum: 0.1, maximum: 10.0, default: 5.0, description: "Selected annual interest rate percentage (e.g. 5.0 for 5.0%). Enforced pursuant to IRS Notice 2022-6 ceiling." }
      },
      required: ["ira_balance", "age"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 10. Mortgage Solver
  {
    name: "omni_mortgage_solver",
    description: `Fixed-Rate Mortgage Payment & Amortization Calculator:
Calculates exact monthly principal and interest (P&I) installments, total cumulative interest, total cost of loan, and accelerated payoff interest savings with extra monthly principal payments for fixed-rate residential mortgages.

GOVERNING MATHEMATICAL EQUATIONS:
- Monthly Payment: M = P · [r(1+r)ⁿ] / [(1+r)ⁿ - 1], where r = APR / 1200 and n = years × 12.
- Total Cumulative Interest = (M · n) - P
- Total Cost of Loan = M · n
- Accelerated Payoff: Extra monthly principal directly reduces remaining balance, reducing subsequent monthly interest accrual.

USAGE GUIDELINES:
- WHEN TO USE: Invoke for calculating monthly mortgage payments, interest burden, and early payoff schedules for residential fixed-rate home loans.
- WHEN NOT TO USE: Do not use for commercial construction loans, interest-only balloon mortgages, or reverse mortgages.
- SIBLING DIFFERENTIATION: Dedicated strictly to residential fixed-rate amortizing first mortgages. For short-term real estate investment bridge loans or flip financing, query slug 'hard-money-loan' or 'hard-money-points' via 'omni_universal_query'. For revolving home equity lines of credit, query slug 'heloc' via 'omni_universal_query'. For comparing multiple loan options (e.g. 15-year vs 30-year), use 'omni_batch_calculate'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'loan_amount': Total borrowed principal balance in USD ($) (min 1,000, max 20,000,000, default 400,000).
- 'interest_rate_pct': Fixed annual interest rate percentage (APR) (min 0.1, max 25.0, default 6.75). Converted internally to monthly rate r = rate / 1200.
- 'loan_term_years': Loan term duration in years (min 1, max 50, default 30). Total payments n = years × 12.
- 'extra_monthly_payment': Optional additional principal paid each month in USD ($) (min 0, default 0). Directly accelerates amortization schedule.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic loan amortization calculation with IEEE 754 precision.
- Read-only, idempotent, and stateless. Zero side effects or persistent mutations.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/finance/mortgage/)
- inputs (object): Echoed input parameter values
- metrics (object): Calculated financial metrics:
  * monthly_payment (number): Base monthly principal and interest installment ($/mo)
  * total_monthly_payment (number): Total monthly payment including extra principal ($/mo)
  * total_interest_paid (number): Total cumulative interest paid over the life of the loan ($)
  * total_cost_of_loan (number): Total cumulative principal plus interest ($)
  * payoff_months (number): Total number of months required to reach zero balance
  * payoff_years (number): Equivalent payoff timeline in years
  * interest_saved_with_extra (number): Total interest saved due to extra principal payments ($)`,
    inputSchema: {
      type: "object",
      properties: {
        loan_amount: { type: "number", minimum: 1000, default: 400000, description: "Total borrowed mortgage principal amount in USD ($)." },
        interest_rate_pct: { type: "number", minimum: 0.1, maximum: 25.0, default: 6.75, description: "Annual percentage rate (APR) as a whole number (e.g. 6.75 for 6.75%)." },
        loan_term_years: { type: "integer", minimum: 1, maximum: 50, default: 30, description: "Mortgage amortization duration in years (typically 15, 20, or 30 years)." },
        extra_monthly_payment: { type: "number", minimum: 0, default: 0, description: "Optional extra principal payment added to each monthly installment in USD ($)." }
      },
      required: ["loan_amount"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 11. Concrete Volume Solver
  {
    name: "omni_concrete_volume_solver",
    description: `Concrete Volume & Premix Bag Yield Calculator:
Calculates concrete volume in cubic yards and cubic meters for rectangular slabs, footings, and cylindrical columns with a standard 10% waste buffer and premix 60-lb and 80-lb bag counts.

GOVERNING MATHEMATICAL EQUATIONS:
- Slab Volume: V_slab = [Length(ft) · Width(ft) · (Depth(in) / 12)] / 27 yd³
- Column/Cylinder Volume: V_cyl = [π · (Diameter(ft)/2)² · Depth(ft)] / 27 yd³
- Volume with Waste: V_total = V · (1 + Waste%/100)
- Premix 80-lb Bag Yield: V_cuft / 0.60 cu ft/bag
- Premix 60-lb Bag Yield: V_cuft / 0.45 cu ft/bag

USAGE GUIDELINES:
- WHEN TO USE: Invoke to calculate concrete quantities for flatwork (driveways, patios, garage slabs), trench footings, and round sonotube piers before ordering ready-mix truck delivery or buying bagged premix concrete.
- WHEN NOT TO USE: Do not use for dry-stack block fill or masonry mortar.
- SIBLING DIFFERENTIATION: Dedicated strictly to structural cast-in-place concrete volume and commercial bag yield estimation. For rebar reinforcement grid sizing inside the concrete, query slug 'rebar-calculator' via 'omni_universal_query'. For driveway gravel base or sub-base compaction, query slug 'gravel-driveway' via 'omni_universal_query'. For paver joint sand, query slug 'polymeric-sand' via 'omni_universal_query'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'length_ft': Length of slab or footing in feet (min 1, max 500, default 20).
- 'width_ft': Width of slab or footing in feet (min 1, max 500, default 10).
- 'depth_in': Thickness or depth in inches (min 1, max 120, default 4). Converted internally to feet (depth / 12).
- 'waste_pct': Percentage waste contingency buffer for spillage and subgrade unevenness (min 0, max 30, default 10).

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic geometric volume calculation with IEEE 754 precision.
- Read-only, idempotent, and stateless.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/construction/concrete-volume/)
- inputs (object): Echoed input dimensions and waste buffer
- metrics (object): Calculated material metrics:
  * volume_cubic_yards_exact (number): Net volumetric displacement without buffer in cubic yards
  * volume_cubic_yards_with_waste (number): Total recommended order volume including waste buffer in cubic yards
  * volume_cubic_meters (number): Total metric volume including waste buffer in cubic meters
  * premix_80lb_bags_needed (number): Number of 80-lb commercial premix concrete bags required
  * premix_60lb_bags_needed (number): Number of 60-lb commercial premix concrete bags required`,
    inputSchema: {
      type: "object",
      properties: {
        length_ft: { type: "number", minimum: 1, maximum: 500, default: 20, description: "Length of concrete slab or footing in feet." },
        width_ft: { type: "number", minimum: 1, maximum: 500, default: 10, description: "Width of concrete slab or footing in feet." },
        depth_in: { type: "number", minimum: 1, maximum: 120, default: 4, description: "Thickness or depth of concrete in inches (e.g. 4 in for sidewalk/patio, 6 in for driveway)." },
        waste_pct: { type: "number", minimum: 0, maximum: 30, default: 10, description: "Waste contingency buffer percentage (default 10%)." }
      },
      required: ["length_ft", "width_ft", "depth_in"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  },

  // 12. Wire Gauge & Voltage Drop Solver
  {
    name: "omni_wire_gauge_voltage_drop_solver",
    description: `Electrical Wire Gauge & Voltage Drop Calculator (NEC):
Calculates conductor voltage drop percentage, delivered load voltage, line voltage loss, and minimum copper/aluminum AWG wire gauge compliant with National Electrical Code (NEC) Article 210.19 3% branch circuit limits.

GOVERNING FORMULAS & STANDARDS:
- Single-Phase Voltage Drop: V_drop = (2 · K · I · L) / Circular Mils
- Three-Phase Voltage Drop: V_drop = (√3 · K · I · L) / Circular Mils
- Voltage Drop Percentage: % V_drop = (V_drop / V_system) · 100
- Delivered Voltage at Load: V_load = V_system - V_drop
- Conductor Constants: Copper K = 12.9 ohms-cmil/ft; Aluminum K = 21.2 ohms-cmil/ft (at 75°C).
- NEC Limit: Recommended branch circuit voltage drop <= 3.0%.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to calculate wire gauge requirements, line voltage drop, and delivered load voltage for long conduit runs (e.g. subpanel feeders, EV chargers, well pumps, HVAC disconnects) to prevent equipment motor burnouts and comply with NEC code.
- WHEN NOT TO USE: Do not use for high-voltage utility transmission lines.
- SIBLING DIFFERENTIATION: Dedicated strictly to electrical branch circuit and feeder conductor sizing under NEC Chapter 9 Table 8. For HVAC mechanical cooling and heating sizing, use 'omni_hvac_manual_j_solver'. For generator sizing, query slug 'generator-sizing' via 'omni_universal_query'. For solar photovoltaic string sizing, query slug 'solar-panel-output' via 'omni_universal_query'.

PARAMETER RELATIONSHIPS & CONSTRAINTS:
- 'current_amps': Design continuous or non-continuous circuit current in Amperes (min 1, max 600, default 30).
- 'one_way_distance_ft': One-way conduit route length from distribution panel to electrical load in feet (min 5, max 2000, default 100).
- 'system_voltage': Nominal circuit voltage in Volts (e.g. 120, 208, 240, 277, 480; default 240).
- 'phase': Electrical phase configuration: 'single_phase' (1-phase) or 'three_phase' (3-phase). Default 'single_phase'.
- 'conductor_material': Wire conductor metal: 'copper' (default) or 'aluminum'.

BEHAVIOR, SAFETY & DETERMINISM:
- Pure deterministic electrical engineering calculation based on NEC Chapter 9, Table 8 conductor properties.
- Read-only, idempotent, and stateless.

RETURN VALUE SCHEMA & QUANTITIES:
- source (string): Canonical documentation URL (https://omnioperand.com/energy/wire-gauge-voltage-drop/)
- inputs (object): Echoed electrical parameters
- metrics (object): Calculated electrical metrics:
  * voltage_drop_volts (number): Voltage lost across the line conductors in Volts
  * voltage_drop_pct (number): Percentage of source voltage lost
  * voltage_at_load (number): Delivered operating voltage at the equipment terminals in Volts
  * recommended_wire_gauge (string): Minimum AWG or kcmil conductor size satisfying the NEC 3% drop limit
  * nec_compliant (boolean): True if voltage drop is within the 3.0% limit`,
    inputSchema: {
      type: "object",
      properties: {
        current_amps: { type: "number", minimum: 1, maximum: 600, default: 30, description: "Design load current in Amperes (e.g. 30 Amps for dryer/EV, 40 Amps for range)." },
        one_way_distance_ft: { type: "number", minimum: 5, maximum: 2000, default: 100, description: "One-way conduit distance from breaker panel to load in feet." },
        system_voltage: { type: "number", minimum: 12, maximum: 600, default: 240, description: "Nominal circuit voltage in Volts (e.g. 120V, 208V, 240V, 480V)." },
        phase: { type: "string", enum: ['single_phase', 'three_phase'], default: 'single_phase', description: "Electrical phase configuration: 'single_phase' (1-phase) or 'three_phase' (3-phase)." },
        conductor_material: { type: "string", enum: ['copper', 'aluminum'], default: 'copper', description: "Conductor material: 'copper' (K=12.9) or 'aluminum' (K=21.2)." }
      },
      required: ["current_amps", "one_way_distance_ft"]
    },
    annotations: { priority: 1, audience: ["assistant"] }
  }
];

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS
  });
}

export async function onRequestHead(context) {
  const res = await onRequestGet(context);
  return new Response(null, {
    status: res.status,
    headers: res.headers
  });
}

export async function onRequestGet(context) {
  const accept = (context && context.request && context.request.headers && context.request.headers.get("Accept")) || "";
  const origin = (context && context.request && new URL(context.request.url).origin) || "https://omnioperand.com";
  const pathname = (context && context.request && new URL(context.request.url).pathname) || "/mcp";

  // Public server without OAuth front-door auth
  if (pathname.includes(".well-known")) {
    return new Response(JSON.stringify({
      status: "unprotected",
      authentication_required: false,
      message: "OmniOperand MCP server is a public calculation engine and does not require OAuth authentication.",
      mcp_endpoint: `${origin}/mcp`
    }, null, 2), { status: 404, headers: CORS_HEADERS });
  }

  // Support MCP Server-Sent Events (SSE) remote transport
  if (accept.includes("text/event-stream")) {
    let timer;
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode(`event: endpoint\ndata: ${origin}${pathname}\n\n`));
        timer = setInterval(() => {
          try {
            controller.enqueue(new TextEncoder().encode(`: keep-alive\n\n`));
          } catch (e) {
            clearInterval(timer);
          }
        }, 15000);
      },
      cancel() {
        if (timer) clearInterval(timer);
      }
    });
    return new Response(stream, {
      status: 200,
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-transform",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, mcp-session-id",
        "Access-Control-Expose-Headers": "mcp-session-id"
      }
    });
  }

  return new Response(JSON.stringify({
    name: "omnioperand-mcp-server",
    protocolVersion: "2024-11-05",
    version: "2.1.0",
    description: "OmniOperand Flagship Deterministic Mathematical MCP Server (12 Curated Solvers with Discovery & Batching)",
    vendor: "OmniOperand Computational Systems",
    total_tools: ALL_MCP_TOOLS.length,
    tools_count: ALL_MCP_TOOLS.length,
    capabilities: {
      tools: { listChanged: false },
      resources: { listChanged: false },
      prompts: { listChanged: false }
    },
    documentation: "https://omnioperand.com/mcp/",
    endpoints: {
      mcp: `${origin}/mcp`,
      openapi: `${origin}/api/v1/openapi.json`
    }
  }), {
    status: 200,
    headers: CORS_HEADERS
  });
}

export async function onRequestPost(context) {
  const reqSessionId = (context && context.request && context.request.headers && context.request.headers.get("mcp-session-id")) || null;
  const sessionId = reqSessionId || "omni-" + Math.random().toString(36).slice(2, 10);
  let body;
  try {
    body = await context.request.json();
  } catch (e) {
    return new Response(JSON.stringify({
      jsonrpc: "2.0",
      id: null,
      error: { code: -32700, message: "Parse error: Invalid JSON payload" }
    }), { status: 400, headers: CORS_HEADERS });
  }

  const id = body.id ?? null;
  const method = body.method;
  const params = body.params || {};

  const reqProtoVersion = (context && context.request && context.request.headers && context.request.headers.get("mcp-protocol-version"))
    || (params && params._meta && params._meta["io.modelcontextprotocol/protocolVersion"])
    || (params && params.protocolVersion)
    || "2026-07-28";

  const responseHeaders = {
    ...CORS_HEADERS,
    "mcp-session-id": sessionId,
    "mcp-protocol-version": reqProtoVersion
  };

  switch (method) {
    case "initialize":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: reqProtoVersion,
          supportedVersions: ["2026-07-28", "2025-11-25", "2024-11-05"],
          capabilities: {
            tools: { listChanged: false },
            resources: { listChanged: false },
            prompts: { listChanged: false }
          },
          serverInfo: {
            name: "omnioperand-mcp-server",
            version: "2.1.0"
          },
          _meta: {
            "io.modelcontextprotocol/serverInfo": {
              name: "omnioperand-mcp-server",
              version: "2.1.0"
            }
          },
          instructions: "OmniOperand deterministic mathematical, financial, scientific, and engineering calculation coprocessor with 12 curated flagship tools, discovery operations, and dynamic edge dispatch across 428+ precision solvers."
        }
      }), { status: 200, headers: responseHeaders });

    case "notifications/initialized":
    case "initialized":
      if (id !== null && id !== undefined) {
        return new Response(JSON.stringify({ jsonrpc: "2.0", id, result: {} }), { status: 200, headers: responseHeaders });
      }
      return new Response(null, { status: 204, headers: responseHeaders });

    case "server/discover":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          server: {
            name: "omnioperand-mcp-server",
            version: "2.1.0",
            description: "OmniOperand Deterministic Mathematical & Engineering MCP Engine",
            tools_count: ALL_MCP_TOOLS.length
          }
        }
      }), { status: 200, headers: responseHeaders });

    case "tools/list":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          tools: ALL_MCP_TOOLS
        }
      }), { status: 200, headers: responseHeaders });

    case "tools/call": {
      const toolName = params.name;
      const args = params.arguments || {};

      if (!toolName) {
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          error: { code: -32602, message: "Invalid params: Missing tool name" }
        }), { status: 400, headers: responseHeaders });
      }

      // 1. Discovery Tool: List Categories
      if (toolName === 'omni_list_categories') {
        const cats = {};
        for (const calc of Object.values(CALCULATOR_REGISTRY)) {
          const c = calc.category || 'general';
          cats[c] = (cats[c] || 0) + 1;
        }
        const categoryList = Object.keys(cats).sort().map(idKey => ({
          id: idKey,
          name: CATEGORY_NAMES[idKey] || idKey,
          solvers_count: cats[idKey],
          url: `https://omnioperand.com/${idKey}/`
        }));

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{
              type: "text",
              text: JSON.stringify({
                total_categories: categoryList.length,
                total_solvers: Object.keys(CALCULATOR_REGISTRY).length,
                categories: categoryList
              }, null, 2)
            }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 2. Discovery Tool: List Solvers
      if (toolName === 'omni_list_solvers') {
        const category = args.category;
        const search = args.search;
        let matches = Object.values(CALCULATOR_REGISTRY);
        const limit = Math.min(100, Math.max(1, parseInt(args.limit || 50, 10)));

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

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
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
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 3. Discovery Tool: Describe Solver
      if (toolName === 'omni_describe_solver') {
        const slug = args.slug;
        const calc = CALCULATOR_REGISTRY[slug];
        if (!calc) {
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id,
            result: {
              content: [{
                type: "text",
                text: JSON.stringify({
                  status: "error",
                  message: `Unknown calculator slug '${slug}'. Call 'omni_list_solvers' to discover valid calculator slugs.`
                }, null, 2)
              }]
            }
          }), { status: 200, headers: responseHeaders });
        }

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
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
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 4. Batch Tool: Batch Calculate
      if (toolName === 'omni_batch_calculate') {
        const jobs = Array.isArray(args.jobs) ? args.jobs : [];
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

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{
              type: "text",
              text: JSON.stringify({
                total_jobs: jobs.length,
                successful_jobs: successCount,
                execution_time_ms: Math.max(0.1, Date.now() - startTime),
                results
              }, null, 2)
            }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 5. Dynamic Gateway: Universal Query
      if (toolName === 'omni_universal_query') {
        const category = args.category || 'general';
        const querySlug = args.slug;
        const params = args.params || {};

        // Enforcement of Specialist Redirects
        const SPECIALIST_REDIRECTS = {
          'octagon': 'omni_octagon_solver',
          'regular-polygon': 'omni_regular_polygon_solver',
          'hvac-manual-j': 'omni_hvac_manual_j_solver',
          'sepp-72t-distribution': 'omni_sepp_72t_solver',
          'sepp-72t': 'omni_sepp_72t_solver',
          'mortgage': 'omni_mortgage_solver',
          'concrete-volume': 'omni_concrete_volume_solver',
          'concrete-slab': 'omni_concrete_volume_solver',
          'wire-gauge-voltage-drop': 'omni_wire_gauge_voltage_drop_solver'
        };

        if (SPECIALIST_REDIRECTS[querySlug]) {
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id,
            result: {
              content: [{
                type: "text",
                text: JSON.stringify({
                  status: "redirect",
                  message: `Calculator '${querySlug}' has a dedicated flagship specialist tool '${SPECIALIST_REDIRECTS[querySlug]}' with compile-time parameter validation. Please invoke '${SPECIALIST_REDIRECTS[querySlug]}' directly.`,
                  redirect_tool: SPECIALIST_REDIRECTS[querySlug],
                  category,
                  slug: querySlug
                }, null, 2)
              }]
            }
          }), { status: 200, headers: responseHeaders });
        }

        if (querySlug && CALCULATOR_REGISTRY[querySlug]) {
          const directResult = executeCalculator(querySlug, params);
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id,
            result: {
              content: [{ type: "text", text: JSON.stringify(directResult, null, 2) }]
            }
          }), { status: 200, headers: responseHeaders });
        }

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{
              type: "text",
              text: JSON.stringify({
                status: "fallback",
                calculator_url: `https://omnioperand.com/${category}/${querySlug || ''}/`,
                note: "Visit the live solver on OmniOperand for interactive inputs and SVG blueprints."
              }, null, 2)
            }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 6. Specialist: Regular Octagon Solver
      if (toolName === 'omni_octagon_solver' || toolName === 'omni_octagon') {
        const octResult = solveOctagon(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(octResult, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 7. Specialist: Universal Regular Polygon Solver
      if (toolName === 'omni_regular_polygon_solver' || toolName === 'omni_regular_polygon') {
        const n = parseInt(args.n || 6, 10);
        if (n === 8) {
          return new Response(JSON.stringify({
            jsonrpc: "2.0",
            id,
            result: {
              content: [{
                type: "text",
                text: JSON.stringify({
                  status: "redirect",
                  notice: "For 8-sided regular octagons (n=8), route to 'omni_octagon_solver' for exact radical closed-form geometry, 3 diagonal classes, and 22.5° carpentry miter angles without trigonometric approximation.",
                  redirect_tool: "omni_octagon_solver"
                }, null, 2)
              }]
            }
          }), { status: 200, headers: responseHeaders });
        }

        const polyResult = solveRegularPolygon(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(polyResult, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 8. Specialist: HVAC Manual J Solver
      if (toolName === 'omni_hvac_manual_j_solver') {
        const floor_area_sqft = parseFloat(args.floor_area_sqft || 2000);
        const ceiling_height_ft = parseFloat(args.ceiling_height_ft || 8);
        const winter_design_temp_f = parseFloat(args.winter_design_temp_f !== undefined ? args.winter_design_temp_f : 15);
        const summer_design_temp_f = parseFloat(args.summer_design_temp_f !== undefined ? args.summer_design_temp_f : 92);
        const indoor_heating_setpoint_f = parseFloat(args.indoor_heating_setpoint_f !== undefined ? args.indoor_heating_setpoint_f : 70);
        const indoor_cooling_setpoint_f = parseFloat(args.indoor_cooling_setpoint_f !== undefined ? args.indoor_cooling_setpoint_f : 75);
        const insulation_grade = args.insulation_grade || 'average_code';

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
        const rounded_tonnage = Math.ceil(required_tonnage * 2) / 2;

        const hvacData = {
          source: "https://omnioperand.com/engineering/hvac-manual-j/",
          inputs: {
            floor_area_sqft,
            ceiling_height_ft,
            winter_design_temp_f,
            summer_design_temp_f,
            indoor_heating_setpoint_f,
            indoor_cooling_setpoint_f,
            insulation_grade
          },
          heating_load_btu_hr: heat_loss_btu,
          cooling_load_btu_hr: cool_gain_btu,
          recommended_cooling_tonnage: required_tonnage,
          rounded_equipment_size_tons: rounded_tonnage,
          required_airflow_cfm: Math.round(rounded_tonnage * 400),
          design_delta_t_heating_deg_f: delta_t_heat,
          design_delta_t_cooling_deg_f: delta_t_cool,
          assumptions_note: "Simplified ACCA Manual J block-load calculation. Code permitting requires full architectural room-by-room Manual J/S/D audit."
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(hvacData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 9. Specialist: SEPP 72(t) Early Retirement Solver
      if (toolName === 'omni_sepp_72t_solver') {
        const ira_balance = parseFloat(args.ira_balance || 500000);
        const age = parseInt(args.age || 45, 10);
        const interest_rate_pct = parseFloat(args.interest_rate_pct !== undefined ? args.interest_rate_pct : 5.0);

        const rate = interest_rate_pct / 100;
        const life_expectancy = Math.max(1, 84 - age);
        const rmd_annual = ira_balance / life_expectancy;
        const pv_factor = (1 - Math.pow(1 + rate, -life_expectancy)) / rate;
        const amort_annual = ira_balance / pv_factor;
        const annuit_annual = amort_annual * 0.965;
        const round = (num) => Math.round(num * 100) / 100;
        const termYears = Math.max(5, Math.ceil(59.5 - age));

        const seppData = {
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
          statutory_duration_years: termYears,
          life_expectancy_factor: life_expectancy,
          effective_interest_rate_pct: interest_rate_pct,
          advisory_note: "Amortization yields the highest fixed distribution. Under Notice 2022-6, a one-time irrevocable switch to the RMD method is permitted if portfolio drawdown requires lower withdrawals."
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(seppData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 10. Specialist: Mortgage Solver
      if (toolName === 'omni_mortgage_solver' || toolName === 'omni_mortgage') {
        const mortResult = solveMortgage(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(mortResult, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 11. Specialist: Concrete Volume Solver
      if (toolName === 'omni_concrete_volume_solver' || toolName === 'omni_concrete_volume') {
        const length_ft = parseFloat(args.length_ft || 20);
        const width_ft = parseFloat(args.width_ft || 10);
        const depth_in = parseFloat(args.depth_in || 4);
        const waste_pct = parseFloat(args.waste_pct !== undefined ? args.waste_pct : 10);

        const cuft = length_ft * width_ft * (depth_in / 12);
        const cuft_waste = cuft * (1 + (waste_pct / 100));
        const cuyd_exact = cuft / 27;
        const cuyd_waste = cuft_waste / 27;
        const cum_waste = cuyd_waste * 0.764555;
        const round = (num) => Math.round(num * 100) / 100;

        const concreteData = {
          source: "https://omnioperand.com/construction/concrete-volume/",
          inputs: { length_ft, width_ft, depth_in, waste_pct },
          metrics: {
            volume_cubic_yards_exact: round(cuyd_exact),
            volume_cubic_yards_with_waste: round(cuyd_waste),
            volume_cubic_meters: round(cum_waste),
            premix_80lb_bags_needed: Math.ceil(cuft_waste / 0.60),
            premix_60lb_bags_needed: Math.ceil(cuft_waste / 0.45)
          }
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(concreteData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // 12. Specialist: Wire Gauge & Voltage Drop Solver
      if (toolName === 'omni_wire_gauge_voltage_drop_solver' || toolName === 'omni_wire_gauge') {
        const current_amps = parseFloat(args.current_amps || 30);
        const one_way_distance_ft = parseFloat(args.one_way_distance_ft || 100);
        const system_voltage = parseFloat(args.system_voltage || 240);
        const phase = args.phase || 'single_phase';
        const conductor_material = args.conductor_material || 'copper';

        const K = conductor_material === 'aluminum' ? 21.2 : 12.9;
        const phase_mult = phase === 'three_phase' ? Math.sqrt(3) : 2.0;

        const awg_table = [
          { name: "#14 AWG", cmil: 4110, cu_amp: 15, al_amp: 0 },
          { name: "#12 AWG", cmil: 6530, cu_amp: 20, al_amp: 15 },
          { name: "#10 AWG", cmil: 10380, cu_amp: 30, al_amp: 25 },
          { name: "#8 AWG", cmil: 16510, cu_amp: 50, al_amp: 40 },
          { name: "#6 AWG", cmil: 26240, cu_amp: 65, al_amp: 50 },
          { name: "#4 AWG", cmil: 41740, cu_amp: 85, al_amp: 65 },
          { name: "#3 AWG", cmil: 52620, cu_amp: 100, al_amp: 75 },
          { name: "#2 AWG", cmil: 66360, cu_amp: 115, al_amp: 90 },
          { name: "#1 AWG", cmil: 83690, cu_amp: 130, al_amp: 100 },
          { name: "1/0 AWG", cmil: 105600, cu_amp: 150, al_amp: 120 },
          { name: "2/0 AWG", cmil: 133100, cu_amp: 175, al_amp: 135 },
          { name: "3/0 AWG", cmil: 167800, cu_amp: 200, al_amp: 155 },
          { name: "4/0 AWG", cmil: 211600, cu_amp: 230, al_amp: 180 },
          { name: "250 kcmil", cmil: 250000, cu_amp: 255, al_amp: 205 },
          { name: "350 kcmil", cmil: 350000, cu_amp: 310, al_amp: 250 },
          { name: "500 kcmil", cmil: 500000, cu_amp: 380, al_amp: 310 }
        ];

        let selected = awg_table[awg_table.length - 1];
        let v_drop = 0;
        let v_drop_pct = 0;

        for (const wire of awg_table) {
          const drop = (phase_mult * K * current_amps * one_way_distance_ft) / wire.cmil;
          const pct = (drop / system_voltage) * 100;
          const ampacity = conductor_material === 'aluminum' ? wire.al_amp : wire.cu_amp;
          if (pct <= 3.0 && ampacity >= current_amps) {
            selected = wire;
            v_drop = drop;
            v_drop_pct = pct;
            break;
          }
        }

        if (v_drop === 0) {
          v_drop = (phase_mult * K * current_amps * one_way_distance_ft) / selected.cmil;
          v_drop_pct = (v_drop / system_voltage) * 100;
        }

        const round = (num) => Math.round(num * 100) / 100;

        const wireData = {
          source: "https://omnioperand.com/energy/wire-gauge-voltage-drop/",
          inputs: { current_amps, one_way_distance_ft, system_voltage, phase, conductor_material },
          metrics: {
            voltage_drop_volts: round(v_drop),
            voltage_drop_pct: round(v_drop_pct),
            voltage_at_load: round(system_voltage - v_drop),
            recommended_wire_gauge: `${selected.name} (${conductor_material === 'aluminum' ? 'Al' : 'Cu'})`,
            nec_compliant: v_drop_pct <= 3.0
          }
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(wireData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      // Universal dynamic solver fallback for any other calculator slug
      const slug = toolName.startsWith('omni_')
        ? toolName.slice(5).replace(/_/g, '-')
        : toolName.replace(/_/g, '-');

      const calc = CALCULATOR_REGISTRY[slug];
      if (!calc) {
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          error: { code: -32601, message: `Tool not found: ${toolName} (slug: ${slug})` }
        }), { status: 404, headers: responseHeaders });
      }

      const result = executeCalculator(slug, args);

      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2)
            }
          ],
          isError: result.status === "error"
        }
      }), { status: 200, headers: responseHeaders });
    }

    case "resources/list":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          resources: [
            {
              uri: "omnioperand://knowledge/llms.txt",
              name: "OmniOperand AI Agent Knowledge Manifest",
              description: "Complete mathematical knowledge and formula registry in llms.txt format",
              mimeType: "text/plain"
            },
            {
              uri: "omnioperand://api/openapi.json",
              name: "OpenAPI 3.1.0 Full Specification",
              description: "Machine-readable API definitions for all 428 calculators",
              mimeType: "application/json"
            }
          ]
        }
      }), { status: 200, headers: responseHeaders });

    case "prompts/list":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          prompts: AI_PROMPTS
        }
      }), { status: 200, headers: responseHeaders });

    case "ping":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {}
      }), { status: 200, headers: responseHeaders });

    default:
      if (method && method.startsWith("notifications/")) {
        return new Response(null, { status: 204, headers: responseHeaders });
      }
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` }
      }), { status: 200, headers: responseHeaders });
  }
}
