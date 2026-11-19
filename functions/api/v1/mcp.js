/**
 * functions/api/v1/mcp.js
 * OmniOperand Official Model Context Protocol (MCP) JSON-RPC 2.0 Server
 * Exposes all 446 deterministic solvers to Claude Desktop, Cursor, and AI agents.
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
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, mcp-session-id",
  "Access-Control-Expose-Headers": "mcp-session-id",
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
  const responseHeaders = {
    ...CORS_HEADERS,
    "mcp-session-id": sessionId
  };

  let body;
  try {
    body = await context.request.json();
  } catch (e) {
    return new Response(JSON.stringify({
      jsonrpc: "2.0",
      id: null,
      error: { code: -32700, message: "Parse error: Invalid JSON payload" }
    }), { status: 400, headers: responseHeaders });
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
          protocolVersion: (params && params.protocolVersion) || "2024-11-05",
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
          protocolVersion: "2024-11-05",
          serverInfo: {
            name: "omnioperand-mcp-server",
            version: "2.0.0"
          },
          capabilities: {
            tools: { listChanged: false },
            resources: { listChanged: false },
            prompts: { listChanged: false }
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
              description: "Machine-readable API definitions for all 446 calculators",
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
