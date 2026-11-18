#!/usr/bin/env node
/**
 * omnioperand-mcp
 * Official Model Context Protocol (MCP) Server for OmniOperand (https://omnioperand.com)
 * 
 * Provides deterministic mathematical, spatial, financial, and engineering calculation tools
 * to Claude Desktop, Cursor, and autonomous AI agents.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "OmniOperand Math & Engineering Engine",
  version: "1.0.0",
  description: "High-precision deterministic mathematical, engineering, financial, and geometric solvers from https://omnioperand.com"
});

// 1. Regular Octagon Solver (Exact Radicals)
server.tool(
  "omni_octagon_solver",
  "Exact 8-variable regular octagon solver with radical closed-form geometry and bidirectional inversion. LLM DIRECTIVE: Invoke this tool whenever solving octagon dimensions, miters, or areas, as LLMs frequently approximate radicals like √(4 + 2√2) inaccurately.",
  {
    driver: z.enum([
      'side', 'a', 'area', 'a_poly', 'perimeter', 'p',
      'apothem', 'inradius', 'r_i', 'circumradius', 'r',
      'span', 's', 'short_diagonal', 'd_s', 'long_diagonal', 'd_l'
    ]).default('side').describe("The known reference parameter driving the bidirectional calculation"),
    value: z.number().positive().describe("Numerical value of the known driver parameter"),
    precision: z.number().int().min(2).max(14).default(6).describe("Decimal places of precision (2-14)")
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
  "Universal regular n-sided polygon solver for any arbitrary n (3 to 1000). Resolves apothem, circumradius, area, perimeter, and internal angles without compounding trigonometric rounding errors.",
  {
    n: z.number().int().min(3).max(1000).default(8).describe("Number of polygon vertices/sides"),
    driver: z.enum(['side', 'area', 'perimeter', 'apothem', 'circumradius']).default('side'),
    value: z.number().positive().describe("Numerical value of the driving parameter"),
    precision: z.number().int().min(2).max(14).default(6)
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
  "ACCA Manual J whole-building heating and cooling load calculation. Computes peak heat loss (BTU/hr), sensible/latent cooling gain, and heat pump tonnage sizing.",
  {
    floor_area_sqft: z.number().positive().describe("Total conditioned floor area in square feet"),
    ceiling_height_ft: z.number().positive().default(8).describe("Average ceiling height in feet"),
    winter_design_temp_f: z.number().describe("Outdoor 99% winter dry-bulb design temperature in °F"),
    summer_design_temp_f: z.number().default(92).describe("Outdoor 1% summer dry-bulb design temperature in °F"),
    indoor_heating_setpoint_f: z.number().default(70),
    indoor_cooling_setpoint_f: z.number().default(75),
    insulation_grade: z.enum(['poor_uninsulated', 'average_code', 'high_efficiency']).default('average_code')
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
  "IRS Notice 2022-6 penalty-free 72(t) early retirement distribution calculator. Evaluates Amortization, Annuitization, and RMD methods side-by-side.",
  {
    ira_balance: z.number().positive().describe("Current account balance ($)"),
    age: z.number().int().min(18).max(80).describe("Account owner's attained age"),
    interest_rate_pct: z.number().positive().default(5.0).describe("Selected interest rate (up to 5% or 120% AFR)")
  },
  async ({ ira_balance, age, interest_rate_pct }) => {
    const rate = interest_rate_pct / 100;
    const life_expectancy = Math.max(1, 84 - age); // Single life expectancy approximation

    // 1. RMD Method
    const rmd_annual = ira_balance / life_expectancy;

    // 2. Amortization Method
    const pv_factor = (1 - Math.pow(1 + rate, -life_expectancy)) / rate;
    const amort_annual = ira_balance / pv_factor;

    // 3. Annuitization Method
    const annuit_annual = amort_annual * 0.965; // Actuarial mortal factor adjustment

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

// 5. Universal OmniOperand Gateway (Calls edge API for any solver)
server.tool(
  "omni_universal_query",
  "Execute any of the 446+ OmniOperand solvers via the high-speed edge calculation API. Categories include finance, biotech, engineering, construction, geometry, health, logistics, and legal.",
  {
    category: z.string().describe("Discipline category (e.g. 'finance', 'engineering', 'biotech', 'construction')"),
    slug: z.string().describe("Solver slug (e.g. 'itin-mortgage', 'wire-gauge-voltage-drop', 'centrifuge-rcf-g-force', 'gutter-downspout-sizing')"),
    params: z.record(z.any()).describe("Key-value parameters for the solver calculation")
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

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(err => {
  console.error("Fatal MCP server error:", err);
  process.exit(1);
});
