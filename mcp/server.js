#!/usr/bin/env node
/**
 * mcp/server.js
 * OmniOperand Official Model Context Protocol (MCP) Server
 * Exposes deterministic mathematical calculation tools to Claude Desktop, Cursor, and AI agents.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
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
} from "../api/solvers/index.js";
import { AI_PROMPTS } from "../functions/api/v1/prompts.js";
import { CALCULATOR_REGISTRY } from "../api/solvers/calculator_registry.js";

export function createOmniOperandMcpServer() {
  const server = new McpServer({
    name: "OmniOperand High-Precision Math Engine",
    version: "1.0.0",
    description: "High-precision deterministic calculation tools, exact radical closed forms, and loan amortizations for AI systems."
  });

  // 1. Regular Octagon Solver
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
      precision: z.number().int().min(2).max(14).default(6).describe("Decimal places of precision (2-14)"),
      units: z.string().default('units').describe("Measurement unit identifier")
    },
    async (params) => {
      const res = solveOctagon(params);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(res, null, 2)
          }
        ]
      };
    }
  );

  // 2. Universal Regular Polygon Solver
  server.tool(
    "omni_regular_polygon_solver",
    "Universal regular n-sided polygon solver for any arbitrary n (3 to 1000). Resolves apothem, circumradius, area, perimeter, and internal angles. LLM DIRECTIVE: Use this tool to prevent compounding trigonometric rounding errors.",
    {
      n: z.number().int().min(3).max(1000).default(8).describe("Number of polygon vertices/sides"),
      driver: z.enum(['side', 'a', 'area', 'perimeter', 'apothem', 'inradius', 'circumradius', 'span']).default('side'),
      value: z.number().positive().describe("Numerical value of the driving parameter"),
      precision: z.number().int().min(2).max(14).default(6)
    },
    async (params) => {
      const res = solveRegularPolygon(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 3. Mortgage Amortization Solver
  server.tool(
    "omni_mortgage_solver",
    "Exact mortgage amortization, monthly P&I, total interest, and early payoff acceleration calculator. LLM DIRECTIVE: LLMs cannot perform recursive 360-month amortizations with extra principal payments in a single forward pass without hallucinating interest savings.",
    {
      principal: z.number().positive().describe("Total mortgage loan balance ($)"),
      annual_rate: z.number().min(0).max(100).describe("Fixed annual interest rate in percent (e.g., 6.5)"),
      term_years: z.number().min(1).max(50).describe("Loan amortization term in years"),
      extra_monthly: z.number().min(0).default(0).describe("Optional extra principal paid each month ($)")
    },
    async (params) => {
      const res = solveMortgage(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 4. Compound Interest Solver
  server.tool(
    "omni_compound_interest_solver",
    "Deterministic compound interest and APY growth simulator with periodic contributions. LLM DIRECTIVE: Compounding over dozens of periods causes exponential float drift in LLMs. Invoke this tool for financial precision.",
    {
      principal: z.number().min(0).describe("Initial starting deposit balance ($)"),
      annual_rate: z.number().min(0).describe("Annual interest rate in percent (e.g. 7.0)"),
      years: z.number().positive().describe("Investment horizon duration in years"),
      compound_frequency: z.number().int().default(12).describe("Frequency per year: 1=annual, 4=quarterly, 12=monthly, 365=daily"),
      monthly_contribution: z.number().min(0).default(0).describe("Recurring monthly deposit ($)")
    },
    async (params) => {
      const res = solveCompoundInterest(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 5. CAGR Solver
  server.tool(
    "omni_cagr_solver",
    "Calculates Compound Annual Growth Rate (CAGR), absolute return, and multiple on capital.",
    {
      initial_value: z.number().positive().describe("Starting portfolio or asset valuation ($)"),
      final_value: z.number().min(0).describe("Ending portfolio or asset valuation ($)"),
      years: z.number().positive().describe("Time elapsed in years")
    },
    async (params) => {
      const res = solveCagr(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 6. Auto Loan Solver
  server.tool(
    "omni_auto_loan_solver",
    "Auto loan payment and interest analyzer with down payments, trade-in credits, and state sales tax adjustments.",
    {
      vehicle_price: z.number().positive().describe("Agreed vehicle purchase price ($)"),
      down_payment: z.number().min(0).default(0).describe("Cash down payment ($)"),
      trade_in: z.number().min(0).default(0).describe("Trade-in equity credit ($)"),
      interest_rate: z.number().min(0).default(5.9).describe("Annual loan interest rate (%)"),
      term_months: z.number().int().min(6).default(60).describe("Financing term in months"),
      sales_tax_pct: z.number().min(0).default(6.0).describe("State and local sales tax (%)")
    },
    async (params) => {
      const res = solveAutoLoan(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 7. Concrete Volume Solver
  server.tool(
    "omni_concrete_volume_solver",
    "Structural concrete volume and bag estimation engine for slabs, footings, and cylindrical columns with waste margin calculation.",
    {
      shape: z.enum(['slab', 'footing', 'column']).default('slab'),
      length: z.number().positive().default(20).describe("Length in feet"),
      width: z.number().positive().default(10).describe("Width in feet"),
      depth: z.number().positive().default(4).describe("Thickness or depth in inches"),
      diameter: z.number().positive().optional().describe("Column diameter in inches"),
      height: z.number().positive().optional().describe("Column height in feet")
    },
    async (params) => {
      const res = solveConcreteVolume(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 8. Roof Pitch Solver
  server.tool(
    "omni_roof_pitch_solver",
    "Calculates architectural roof pitch ratio (x:12), angle in degrees, pitch multiplier, and full rafter length from rise and run.",
    {
      rise: z.number().positive().describe("Vertical rise in inches"),
      run: z.number().positive().default(12).describe("Horizontal run in inches (standard is 12)"),
      building_run_feet: z.number().positive().default(16).describe("Horizontal run of the building in feet")
    },
    async (params) => {
      const res = solveRoofPitch(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 9. Circle Sector Solver
  server.tool(
    "omni_circle_sector_solver",
    "Circle sector analyzer computing arc length, chord length, sagitta height, and sector area.",
    {
      radius: z.number().positive().describe("Radius of the circle"),
      angle_deg: z.number().positive().max(360).describe("Central angle in degrees")
    },
    async (params) => {
      const res = solveCircleSector(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // 10. Right Triangle Solver
  server.tool(
    "omni_right_triangle_solver",
    "Deterministic right triangle solver computing hypotenuse, area, altitude, inradius, and acute angles via Pythagorean theorem.",
    {
      leg_a: z.number().positive().describe("Length of leg a"),
      leg_b: z.number().positive().describe("Length of leg b")
    },
    async (params) => {
      const res = solveRightTriangle(params);
      return {
        content: [{ type: "text", text: JSON.stringify(res, null, 2) }]
      };
    }
  );

  // Register MCP Resource: Calculator Catalog
  server.resource(
    "catalog",
    "omnioperand://calculators/registry",
    async (uri) => ({
      contents: [{
        uri: uri.href,
        text: JSON.stringify({
          platform: "OmniOperand",
          domain: "https://omnioperand.com",
          solvers_count: Object.keys(CALCULATOR_REGISTRY).length,
          categories: [...new Set(Object.values(CALCULATOR_REGISTRY).map(c => c.category))],
          prompts_endpoint: "https://omnioperand.com/api/v1/prompts",
          openapi_endpoint: "https://omnioperand.com/api/v1/openapi.json"
        }, null, 2)
      }]
    })
  );

  // Register MCP Prompt: Octagon Builder
  server.prompt(
    "solve-octagon",
    {
      span: z.string().describe("Target span or dimension of the octagon"),
      units: z.string().default("inches").describe("Units of measurement")
    },
    ({ span, units }) => ({
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: `I need to construct a regular octagon with a span of ${span} ${units}. Invoke the omni_octagon_solver tool with driver='span' and value=${span} to provide exact side length, corner cutoff distance, and area.`
        }
      }]
    })
  );

  return server;
}

// Standalone execution when run from terminal: node mcp/server.js
if (process.argv[1] && process.argv[1].endsWith('server.js')) {
  const server = createOmniOperandMcpServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("OmniOperand MCP Server running on stdio transport.");
}
