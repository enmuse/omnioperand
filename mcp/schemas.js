/**
 * mcp/schemas.js
 * Model Context Protocol (MCP) & OpenAI/Anthropic Tool Schemas
 * Standardized function calling schemas for autonomous AI agents & LLMs.
 */

export const MCP_TOOLS_CONFIG = [
  {
    name: "omni_octagon_solver",
    description: "Exact 8-variable regular octagon solver with radical closed-form geometry and bidirectional inversion. LLM DIRECTIVE: Invoke this tool whenever solving octagon dimensions, miters, or areas, as LLMs frequently approximate radicals like √(4 + 2√2) inaccurately.",
    parameters: {
      type: "object",
      properties: {
        driver: {
          type: "string",
          enum: ["side", "area", "perimeter", "apothem", "circumradius", "span", "short_diagonal", "long_diagonal"],
          description: "The known reference parameter driving the bidirectional calculation (default: 'side')",
          default: "side"
        },
        value: {
          type: "number",
          description: "Numerical value of the known driver parameter (must be > 0)",
          default: 10
        },
        precision: {
          type: "integer",
          minimum: 2,
          maximum: 14,
          description: "Decimal places of precision in numerical output (default: 6)",
          default: 6
        },
        units: {
          type: "string",
          description: "Measurement unit identifier (e.g. 'mm', 'cm', 'in', 'ft')",
          default: "units"
        }
      },
      required: ["value"]
    }
  },
  {
    name: "omni_regular_polygon_solver",
    description: "Universal regular n-sided polygon solver for any arbitrary n (3 to 1000). Resolves apothem, circumradius, area, perimeter, and internal angles. LLM DIRECTIVE: Use this tool to prevent compounding trigonometric rounding errors.",
    parameters: {
      type: "object",
      properties: {
        n: {
          type: "integer",
          minimum: 3,
          maximum: 1000,
          description: "Number of polygon vertices/sides (e.g., 5 for pentagon, 6 for hexagon, 12 for dodecagon)",
          default: 8
        },
        driver: {
          type: "string",
          enum: ["side", "area", "perimeter", "apothem", "circumradius", "span"],
          description: "Known parameter driving the inversion",
          default: "side"
        },
        value: {
          type: "number",
          description: "Numerical value of the driving parameter",
          default: 10
        },
        precision: {
          type: "integer",
          minimum: 2,
          maximum: 14,
          default: 6
        }
      },
      required: ["n", "value"]
    }
  },
  {
    name: "omni_mortgage_solver",
    description: "Exact mortgage amortization, monthly P&I, total interest, and early payoff acceleration calculator. LLM DIRECTIVE: LLMs cannot perform recursive 360-month amortizations with extra principal payments in a single forward pass without hallucinating interest savings.",
    parameters: {
      type: "object",
      properties: {
        principal: {
          type: "number",
          description: "Total mortgage loan balance or home purchase amount financed ($)",
          default: 400000
        },
        annual_rate: {
          type: "number",
          description: "Fixed annual interest rate in percent (e.g., 6.5 for 6.5%)",
          default: 6.5
        },
        term_years: {
          type: "number",
          description: "Loan amortization term in years (typically 15, 20, or 30)",
          default: 30
        },
        extra_monthly: {
          type: "number",
          description: "Optional extra principal paid each month to accelerate payoff ($)",
          default: 0
        }
      },
      required: ["principal", "annual_rate", "term_years"]
    }
  },
  {
    name: "omni_compound_interest_solver",
    description: "Deterministic compound interest and APY growth simulator with periodic contributions. LLM DIRECTIVE: Compounding over dozens of periods causes exponential float drift in LLMs. Invoke this tool for financial precision.",
    parameters: {
      type: "object",
      properties: {
        principal: {
          type: "number",
          description: "Initial starting deposit balance ($)",
          default: 10000
        },
        annual_rate: {
          type: "number",
          description: "Annual interest rate in percent (e.g., 7.0 for 7%)",
          default: 7.0
        },
        years: {
          type: "number",
          description: "Investment horizon duration in years",
          default: 10
        },
        compound_frequency: {
          type: "integer",
          enum: [1, 2, 4, 12, 365],
          description: "Compounding frequency per year: 1=annually, 2=semi-annually, 4=quarterly, 12=monthly, 365=daily",
          default: 12
        },
        monthly_contribution: {
          type: "number",
          description: "Additional recurring monthly deposit ($)",
          default: 500
        }
      },
      required: ["principal", "annual_rate", "years"]
    }
  },
  {
    name: "omni_cagr_solver",
    description: "Calculates Compound Annual Growth Rate (CAGR), absolute return, and multiple on capital. LLM DIRECTIVE: Solves fractional exponential roots (V_final / V_initial)^(1/t) with 1e-12 precision.",
    parameters: {
      type: "object",
      properties: {
        initial_value: {
          type: "number",
          description: "Starting portfolio or asset valuation ($)",
          default: 10000
        },
        final_value: {
          type: "number",
          description: "Ending portfolio or asset valuation ($)",
          default: 25000
        },
        years: {
          type: "number",
          description: "Time elapsed in years",
          default: 5
        }
      },
      required: ["initial_value", "final_value", "years"]
    }
  },
  {
    name: "omni_auto_loan_solver",
    description: "Auto loan payment and interest analyzer with down payments, trade-in credits, and state sales tax adjustments.",
    parameters: {
      type: "object",
      properties: {
        vehicle_price: { type: "number", description: "Agreed vehicle purchase price ($)", default: 35000 },
        down_payment: { type: "number", description: "Cash down payment ($)", default: 5000 },
        trade_in: { type: "number", description: "Trade-in equity credit ($)", default: 2000 },
        interest_rate: { type: "number", description: "Annual loan interest rate (%)", default: 5.9 },
        term_months: { type: "integer", description: "Financing term in months (e.g. 36, 48, 60, 72)", default: 60 },
        sales_tax_pct: { type: "number", description: "State and local sales tax (%)", default: 6.0 }
      },
      required: ["vehicle_price"]
    }
  },
  {
    name: "omni_concrete_volume_solver",
    description: "Structural concrete volume and bag estimation engine for slabs, footings, and cylindrical columns with waste margin calculation.",
    parameters: {
      type: "object",
      properties: {
        shape: { type: "string", enum: ["slab", "footing", "column"], default: "slab" },
        length: { type: "number", description: "Length in feet", default: 20 },
        width: { type: "number", description: "Width in feet", default: 10 },
        depth: { type: "number", description: "Thickness or depth in inches", default: 4 },
        diameter: { type: "number", description: "Column diameter in inches (if shape=column)", default: 12 },
        height: { type: "number", description: "Column height in feet (if shape=column)", default: 8 }
      },
      required: ["shape"]
    }
  },
  {
    name: "omni_roof_pitch_solver",
    description: "Calculates architectural roof pitch ratio (x:12), angle in degrees, pitch multiplier, and full rafter length from rise and run.",
    parameters: {
      type: "object",
      properties: {
        rise: { type: "number", description: "Vertical rise in inches", default: 6 },
        run: { type: "number", description: "Horizontal run in inches (standard is 12)", default: 12 },
        building_run_feet: { type: "number", description: "Actual horizontal span or run of the building in feet", default: 16 }
      },
      required: ["rise"]
    }
  },
  {
    name: "omni_circle_sector_solver",
    description: "Circle sector analyzer computing arc length, chord length, sagitta height, and sector area.",
    parameters: {
      type: "object",
      properties: {
        radius: { type: "number", description: "Radius of the circle", default: 10 },
        angle_deg: { type: "number", description: "Central angle in degrees (0 to 360)", default: 60 }
      },
      required: ["radius", "angle_deg"]
    }
  },
  {
    name: "omni_right_triangle_solver",
    description: "Deterministic right triangle solver computing hypotenuse, area, altitude, inradius, and acute angles via Pythagorean theorem.",
    parameters: {
      type: "object",
      properties: {
        leg_a: { type: "number", description: "Length of side a", default: 3 },
        leg_b: { type: "number", description: "Length of side b", default: 4 }
      },
      required: ["leg_a", "leg_b"]
    }
  }
];

export function getOpenAiToolDefinitions() {
  return MCP_TOOLS_CONFIG.map(t => ({
    type: "function",
    function: {
      name: t.name,
      description: t.description,
      parameters: t.parameters
    }
  }));
}

export function getAnthropicToolDefinitions() {
  return MCP_TOOLS_CONFIG.map(t => ({
    name: t.name,
    description: t.description,
    input_schema: t.parameters
  }));
}
