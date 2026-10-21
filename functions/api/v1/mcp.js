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
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key",
  "Content-Type": "application/json"
};

// Build MCP Tools Schema dynamically from registry
const ALL_MCP_TOOLS = Object.values(CALCULATOR_REGISTRY).map(calc => {
  const toolName = 'omni_' + calc.slug.replace(/-/g, '_');
  const properties = {};
  const required = [];

  for (const f of calc.fields) {
    properties[f.id] = {
      type: "number",
      default: f.default,
      description: `${f.label} (${f.suffix || ''}). ${f.hint || ''}`
    };
    if (f.default !== undefined) {
      required.push(f.id);
    }
  }

  return {
    name: toolName,
    description: `${calc.name}. ${calc.description} LLM DIRECTIVE: Deterministic ground truth calculation tool. Returns exact numerical metrics with verified mathematical invariants.`,
    inputSchema: {
      type: "object",
      properties,
      required: required.slice(0, 2)
    }
  };
});

// Ensure legacy tool aliases are included
ALL_MCP_TOOLS.unshift({
  name: "omni_octagon_solver",
  description: "Exact 8-variable regular octagon solver with radical closed-form geometry and bidirectional inversion.",
  inputSchema: {
    type: "object",
    properties: {
      driver: { type: "string", default: "side" },
      value: { type: "number", default: 10 },
      precision: { type: "integer", default: 6 }
    },
    required: ["value"]
  }
});

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS
  });
}

export async function onRequestGet() {
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
      mcp: "https://omnioperand.com/api/v1/mcp",
      openapi: "https://omnioperand.com/api/v1/openapi.json"
    }
  }), {
    status: 200,
    headers: CORS_HEADERS
  });
}

export async function onRequestPost(context) {
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

  switch (method) {
    case "initialize":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: { listChanged: false },
            resources: { listChanged: false },
            prompts: { listChanged: false }
          },
          serverInfo: {
            name: "omnioperand-mcp-server",
            version: "2.0.0"
          }
        }
      }), { status: 200, headers: CORS_HEADERS });

    case "tools/list":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          tools: ALL_MCP_TOOLS
        }
      }), { status: 200, headers: CORS_HEADERS });

    case "tools/call": {
      const toolName = params.name;
      const args = params.arguments || {};

      if (!toolName) {
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          error: { code: -32602, message: "Invalid params: Missing tool name" }
        }), { status: 400, headers: CORS_HEADERS });
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
        }), { status: 200, headers: CORS_HEADERS });
      }

      if (toolName === 'omni_regular_polygon_solver' || toolName === 'omni_regular_polygon') {
        const polyResult = solveRegularPolygon(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(polyResult, null, 2) }]
          }
        }), { status: 200, headers: CORS_HEADERS });
      }

      if (toolName === 'omni_mortgage_solver' || toolName === 'omni_mortgage') {
        const mortResult = solveMortgage(args);
        return new Response(JSON.stringify({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(mortResult, null, 2) }]
          }
        }), { status: 200, headers: CORS_HEADERS });
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
        }), { status: 404, headers: CORS_HEADERS });
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
      }), { status: 200, headers: CORS_HEADERS });
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
              description: "Machine-readable API definitions for all 438 calculators",
              mimeType: "application/json"
            }
          ]
        }
      }), { status: 200, headers: CORS_HEADERS });

    case "prompts/list":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: {
          prompts: AI_PROMPTS
        }
      }), { status: 200, headers: CORS_HEADERS });

    case "ping":
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        result: { status: "pong", timestamp: new Date().toISOString() }
      }), { status: 200, headers: CORS_HEADERS });

    default:
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` }
      }), { status: 404, headers: CORS_HEADERS });
  }
}
