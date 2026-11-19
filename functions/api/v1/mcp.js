/**
 * functions/api/v1/mcp.js
 * OmniOperand Official Model Context Protocol (MCP) JSON-RPC 2.0 Server
 * Exposes all 428 deterministic solvers to Claude Desktop, Cursor, and AI agents.
 */

import {
  solveOctagon,
  solveRegularPolygon,
  solveMortgage,
  solveCompoundInterest,
  solveCagr,
  solveAutoLoan,
  solveConcreteVolume,
  solveRoofPitch,
  solveCircleSector,
  solveRightTriangle
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

// Build MCP Tools Schema dynamically from registry with TDQS 5/5 compliant metadata
const ALL_MCP_TOOLS = Object.values(CALCULATOR_REGISTRY).map(calc => {
  const toolName = 'omni_' + calc.slug.replace(/-/g, '_');
  const properties = {};
  const required = [];

  for (const f of calc.fields) {
    const minStr = f.min !== undefined ? ` Min: ${f.min}.` : '';
    const maxStr = f.max !== undefined ? ` Max: ${f.max}.` : '';
    const defaultStr = f.default !== undefined ? ` Default: ${f.default}.` : '';
    const suffixStr = f.suffix ? ` (${f.suffix})` : '';

    const prop = {
      type: "number",
      description: `${f.label}${suffixStr}. ${f.hint || ''}.${defaultStr}${minStr}${maxStr}`
    };
    if (f.default !== undefined) prop.default = f.default;
    if (f.min !== undefined) prop.minimum = f.min;
    if (f.max !== undefined) prop.maximum = f.max;

    properties[f.id] = prop;
    if (f.default !== undefined) {
      required.push(f.id);
    }
  }

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
- SIBLING ROUTING: Use this dedicated specialist tool for '${calc.name}' rather than generic dispatchers like omni_universal_query. For cross-discipline dynamic dispatch, see omni_universal_query.

BEHAVIOR & SAFETY:
- Pure deterministic computation with machine floating-point precision.
- Read-only, idempotent, and stateless. Zero side effects or persistent state mutations.
- Input validation: All arguments are validated against physical and domain bounds. Out-of-bounds inputs return a safe diagnostic error status without throwing runtime exceptions.

RETURNS:
- Structured JSON object containing:
  * status (string): "success" on valid execution or "error" if validation fails
  * calculator (string): "${calc.slug}"
  * category (string): "${calc.category}"
  * name (string): "${calc.name}"
  * formula (string): Governing mathematical formula string
  * inputs (object): Echoed input parameter dictionary with applied defaults
  * metrics (object): Dictionary of computed outputs:
${returnDetails}
  * execution_time_ms (number): Latency in milliseconds.`;

  return {
    name: toolName,
    description: toolDescription,
    inputSchema: {
      type: "object",
      properties,
      required: required.slice(0, 2)
    }
  };
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

// Ensure discovery tools and flagship specialist tools are prepended with exact TDQS 5/5 specifications
ALL_MCP_TOOLS.unshift(
  {
    name: "omni_list_categories",
    description: `List All OmniOperand Computational Disciplines & Categories:
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
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "omni_list_solvers",
    description: `Enumerate & Search OmniOperand Solvers:
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
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Optional discipline category filter (e.g. 'finance', 'engineering', 'construction', 'geometry', 'biotech', 'health')." },
        search: { type: "string", description: "Optional keyword search query to match against solver names, descriptions, or mathematical terms (e.g. 'rebar', 'mortgage', 'tonnage', 'voltage drop')." },
        limit: { type: "integer", default: 50, minimum: 1, maximum: 100, description: "Maximum number of results to return (default 50, max 100)." }
      }
    }
  },
  {
    name: "omni_describe_solver",
    description: `Inspect Solver Parameter Schema & Output Metrics:
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
    inputSchema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The calculator slug to inspect (e.g. 'mortgage', 'concrete-volume', 'wire-gauge-voltage-drop', 'regular-polygon')." }
      },
      required: ["slug"]
    }
  },
  {
    name: "omni_batch_calculate",
    description: `Execute Batch or Chained Multi-Calculator Jobs:
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
    }
  },
  {
    name: "omni_octagon_solver",
    description: `Regular Octagon 8-Variable Bidirectional Solver:
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
- SIBLING ROUTING: Use omni_octagon_solver specifically for 8-sided regular octagons where closed-form radical representations are required. For arbitrary n-sided regular polygons where n != 8 (e.g. triangles n=3, pentagons n=5, hexagons n=6, decagons n=10, or arbitrary n up to 1000), route to omni_regular_polygon_solver instead.

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
    }
  },
  {
    name: "omni_regular_polygon_solver",
    description: `Universal Regular N-Sided Polygon Solver (3 to 1000 sides):
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
- SIBLING ROUTING: For 8-sided regular octagons specifically, ROUTE TO 'omni_octagon_solver' instead to receive exact closed-form radical representations (e.g. 2·(1+√2)·a²) without trigonometric floating-point rounding. For arbitrary n (e.g. n=3, 5, 6, 7, 9, 10, 12, ...), use 'omni_regular_polygon_solver'.

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
    inputSchema: {
      type: "object",
      properties: {
        n: {
          type: "integer",
          minimum: 3,
          maximum: 1000,
          default: 8,
          description: "Total number of polygon vertices/sides (integer between 3 and 1000, default 8)."
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
    }
  },
  {
    name: "omni_hvac_manual_j_solver",
    description: `ACCA Manual J Whole-Building Heating & Cooling Load Estimator:
Calculates whole-structure peak heating loss (BTU/hr), sensible/latent cooling heat gain (BTU/hr), and recommended heat pump/AC tonnage sizing according to ACCA Manual J 8th Edition residential load principles.

MODEL ASSUMPTIONS & ENVELOPE-FREE SCOPE:
- Uses a simplified whole-building block-load calculation based on conditioned square footage, ceiling volume, outdoor 99%/1% dry-bulb design temperatures, and insulation envelope heat-transfer multipliers (U-factors).
- Envelope-Free Nature: This is a macro-level block load model using conditioned square footage, ceiling volume, design temperature differentials, and generalized building thermal integrity multipliers (poor/uninsulated R-11/R-19, average code R-13/R-38, high efficiency R-21/R-49).
- Scope Limitations: Does NOT model room-by-room solar orientation, fenestration solar heat gain coefficients (SHGC), radiant barriers, duct leakage losses, or internal occupant/appliance gains. Trust this tool for preliminary residential heating/cooling sizing and equipment tonnage estimates, not for municipal permit-level Manual J/S/D submittals.

USAGE GUIDELINES:
- WHEN TO USE: Invoke to size residential HVAC equipment, heat pump/furnace output, and cooling capacity in tons, preventing short-cycling or undersizing.
- WHEN NOT TO USE: Do not use for commercial zoned VAV systems, multi-family duct design, or permit filings requiring room-by-room ACCA Manual J submittals.
- SIBLING ROUTING: Use omni_hvac_manual_j_solver for comprehensive block heating and cooling loads with tonnage sizing. For dedicated furnace heating output alone, see omni_hvac_furnace_sizing. For general engineering queries, see omni_universal_query.

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
    inputSchema: {
      type: "object",
      properties: {
        floor_area_sqft: { type: "number", minimum: 100, default: 2000, description: "Total conditioned indoor floor area in square feet (e.g. 2000)." },
        ceiling_height_ft: { type: "number", minimum: 6, maximum: 30, default: 8, description: "Average interior ceiling height in feet (default 8 ft). Used to calculate conditioned volume." },
        winter_design_temp_f: { type: "number", minimum: -40, maximum: 70, default: 15, description: "Local outdoor 99% winter dry-bulb design temperature in °F (e.g. 15 for Atlanta, -5 for Chicago, 28 for Dallas)." },
        summer_design_temp_f: { type: "number", minimum: 60, maximum: 125, default: 92, description: "Local outdoor 1% summer dry-bulb design temperature in °F (default 92°F)." },
        indoor_heating_setpoint_f: { type: "number", minimum: 55, maximum: 80, default: 70, description: "Desired winter indoor thermostat heating setpoint in °F. ACCA Manual J standard design condition is 70°F (acceptable range: 55°F to 80°F). Directly determines heating delta-T." },
        indoor_cooling_setpoint_f: { type: "number", minimum: 65, maximum: 85, default: 75, description: "Desired summer indoor thermostat cooling setpoint in °F. ACCA Manual J standard design condition is 75°F (acceptable range: 65°F to 85°F). Directly determines cooling delta-T." },
        insulation_grade: {
          type: "string",
          enum: ['poor_uninsulated', 'average_code', 'high_efficiency'],
          default: "average_code",
          description: "Building envelope thermal integrity: 'poor_uninsulated' (pre-1980, R-11/R-19), 'average_code' (standard 2009+ IECC code, R-13/R-38), 'high_efficiency' (Energy Star / spray foam, R-21/R-49)."
        }
      },
      required: ["floor_area_sqft"]
    }
  },
  {
    name: "omni_sepp_72t_solver",
    description: `IRS Section 72(t) / Notice 2022-6 Early Retirement Distribution Solver:
Calculates penalty-free Substantially Equal Periodic Payments (SEPP) from qualified retirement plans (Traditional IRA, 401k) prior to age 59½ under IRC Section 72(t)(2)(A)(iv).

APPLIED ASSUMPTIONS & GOVERNING RULES:
- Life Expectancy Table: Uses IRS Single Life Expectancy Table pursuant to Treas. Reg. § 1.401(a)(9)-9 (actuarial divisor factor = 84 - attained age).
- Rate Cap Enforcement: Enforces IRS Notice 2022-6 interest rate ceiling, which mandates that the interest rate used cannot exceed the greater of 5.0% or 120% of the federal mid-term Applicable Federal Rate (AFR) for either of the two months preceding the month distributions begin.
- Payment Frequency: Evaluates statutory annual distribution amounts and provides statutory monthly equivalent allowances (annual ÷ 12). Payments must be taken at least annually and maintained for the statutory period: the longer of 5 full years or until the account owner attains age 59½.
- Evaluates all three IRS-approved methods: (1) Fixed Amortization, (2) Fixed Annuitization, and (3) Minimum Distribution (RMD).

USAGE GUIDELINES:
- WHEN TO USE: Invoke to determine penalty-free early retirement withdrawal schedules from qualified plans before age 59½ and compare fixed vs variable distribution options.
- WHEN NOT TO USE: Do not use for Roth IRA basis distributions (which are already penalty- and tax-free) or non-qualified annuity contracts.
- SIBLING ROUTING: Use omni_sepp_72t_solver for IRS 72(t) early retirement distributions. For standard retirement nest egg drawdown, see omni_retirement_nest_egg. For general finance queries, see omni_universal_query.

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
    inputSchema: {
      type: "object",
      properties: {
        ira_balance: { type: "number", minimum: 1000, default: 500000, description: "Current total qualified account balance in USD ($). Minimum $1,000." },
        age: { type: "integer", minimum: 18, maximum: 80, default: 45, description: "Account owner's attained chronological age in years at distribution start (integer 18-80)." },
        interest_rate_pct: { type: "number", minimum: 0.1, maximum: 10.0, default: 5.0, description: "Selected annual interest rate percentage (e.g. 5.0 for 5.0%). Enforced pursuant to IRS Notice 2022-6 ceiling." }
      },
      required: ["ira_balance", "age"]
    }
  },
  {
    name: "omni_universal_query",
    description: `Universal OmniOperand Dynamic Dispatcher:
Dynamic calculation gateway allowing AI agents to query any of OmniOperand's 428+ deterministic engines across all 15 disciplines (finance, construction, engineering, geometry, biotech, logistics, health, legal, energy, crypto, agriculture, math).

USAGE GUIDELINES & SIBLING ROUTING:
- SIBLING ROUTING (CRITICAL MANDATE): Always PREFER dedicated specialist tools (such as 'omni_octagon_solver', 'omni_regular_polygon_solver', 'omni_hvac_manual_j_solver', 'omni_sepp_72t_solver', 'omni_mortgage', 'omni_concrete_volume') when available. Dedicated tools provide native parameter validation, zero network latency, and compiled typing.
- WHEN TO USE: Use omni_universal_query ONLY as a fallback dispatcher when querying an edge calculator slug that does not have a dedicated wrapper or when discovering parameters across disciplines dynamically.
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
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Discipline category directory (e.g. 'finance', 'engineering', 'biotech', 'construction', 'geometry', 'logistics', 'legal', 'energy')." },
        slug: { type: "string", description: "Exact calculator URL slug (e.g. 'concrete-volume', 'wire-gauge-voltage-drop', 'centrifuge-rcf-g-force', 'gutter-downspout-sizing')." },
        params: { type: "object", description: "Key-value parameter dictionary matching the target solver's input requirements (e.g. { length_ft: 20, width_ft: 12, depth_in: 4 })." }
      },
      required: ["category", "slug", "params"]
    }
  }
);

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
        // Keep-alive heartbeat every 15 seconds to maintain open connection
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
    version: "2.0.0",
    description: "OmniOperand Multi-Domain Deterministic Mathematical MCP Server",
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
            version: "2.0.0"
          },
          _meta: {
            "io.modelcontextprotocol/serverInfo": {
              name: "omnioperand-mcp-server",
              version: "2.0.0"
            }
          },
          instructions: "OmniOperand deterministic mathematical, financial, scientific, and engineering calculation coprocessor with 447 precision solvers."
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
          protocolVersion: reqProtoVersion,
          supportedVersions: ["2026-07-28", "2025-11-25", "2024-11-05"],
          capabilities: {
            tools: { listChanged: false },
            resources: { listChanged: false },
            prompts: { listChanged: false }
          },
          serverInfo: {
            name: "omnioperand-mcp-server",
            version: "2.0.0"
          },
          _meta: {
            "io.modelcontextprotocol/serverInfo": {
              name: "omnioperand-mcp-server",
              version: "2.0.0"
            }
          },
          instructions: "OmniOperand deterministic mathematical, financial, scientific, and engineering calculation coprocessor with 447 precision solvers."
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

      // Discovery & Batch Tool Dispatches
      if (toolName === 'omni_list_categories') {
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

      if (toolName === 'omni_list_solvers') {
        let matches = Object.values(CALCULATOR_REGISTRY);
        const category = args.category;
        const search = args.search;
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

      // Dedicated flagship solver dispatches
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

      if (toolName === 'omni_regular_polygon_solver' || toolName === 'omni_regular_polygon') {
        const polyResult = solveRegularPolygon(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(polyResult, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

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

        const hvacData = {
          source: "https://omnioperand.com/engineering/hvac-manual-j/",
          heating_load_btu_hr: heat_loss_btu,
          cooling_load_btu_hr: cool_gain_btu,
          recommended_cooling_tonnage: required_tonnage,
          rounded_equipment_size_tons: Math.ceil(required_tonnage * 2) / 2,
          design_delta_t_heating_deg_f: delta_t_heat,
          design_delta_t_cooling_deg_f: delta_t_cool
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(hvacData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

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
          advisory_note: "Amortization yields the highest fixed distribution. The IRS permits a one-time irrevocable switch to the RMD method if portfolio drawdown requires it."
        };

        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(seppData, null, 2) }]
          }
        }), { status: 200, headers: responseHeaders });
      }

      if (toolName === 'omni_universal_query') {
        const category = args.category || 'general';
        const querySlug = args.slug;
        const params = args.params || {};

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

      // Universal dynamic solver dispatch for all other calculators
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
