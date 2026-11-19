/**
 * functions/.well-known/[[path]].js
 * OmniOperand Universal Discovery Router
 *
 * Implements:
 * 1. RFC 9728: OAuth 2.0 Protected Resource Metadata (oauth-protected-resource)
 * 2. RFC 8414: OAuth 2.0 Authorization Server Metadata (oauth-authorization-server)
 * 3. OpenID Connect Discovery 1.0 (openid-configuration)
 * 4. Model Context Protocol Discovery (mcp, mcp.json, server-card.json)
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, mcp-session-id",
  "Access-Control-Expose-Headers": "mcp-session-id",
  "Content-Type": "application/json",
  "Cache-Control": "public, max-age=3600, s-maxage=86400"
};

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
  const url = new URL(context.request.url);
  const origin = url.origin || "https://omnioperand.com";
  const path = url.pathname.toLowerCase();

  // 1. OAuth / OIDC Discovery: Public server without front-door auth
  if (path.includes("oauth-protected-resource") || path.includes("oauth-authorization-server") || path.includes("openid-configuration")) {
    return new Response(JSON.stringify({
      status: "unprotected",
      authentication_required: false,
      message: "OmniOperand MCP server is a public calculation engine and does not require OAuth authentication.",
      mcp_endpoint: `${origin}/mcp`
    }, null, 2), {
      status: 404,
      headers: CORS_HEADERS
    });
  }

  // 4. MCP Discovery Card (mcp, mcp.json, server-card.json)
  if (path.includes("mcp")) {
    const mcpCardPayload = {
      mcp_version: "2024-11-05",
      server_name: "omnioperand-mcp-server",
      server_version: "2.0.0",
      description: "OmniOperand Multi-Domain Deterministic Mathematical MCP Server with 446 tools",
      endpoints: {
        streamable_http: `${origin}/mcp`,
        sse: `${origin}/mcp`,
        http: `${origin}/mcp`,
        openapi: `${origin}/api/v1/openapi.json`
      },
      capabilities: {
        tools: { listChanged: false },
        resources: { listChanged: false },
        prompts: { listChanged: false }
      },
      authentication: {
        required: false,
        methods: ["none"]
      }
    };
    return new Response(JSON.stringify(mcpCardPayload, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // Default fallback for any other .well-known probe
  return new Response(JSON.stringify({
    service: "omnioperand-mcp",
    status: "healthy",
    mcp_endpoint: `${origin}/mcp`
  }), {
    status: 200,
    headers: CORS_HEADERS
  });
}
