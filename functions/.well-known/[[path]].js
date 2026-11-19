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

  // 1. RFC 9728: Protected Resource Metadata
  if (path.includes("oauth-protected-resource")) {
    const resourcePayload = {
      resource: `${origin}/mcp`,
      authorization_servers: [
        "https://auth.arcade.dev",
        origin
      ],
      scopes_supported: [
        "tools:read",
        "tools:call",
        "resources:read",
        "prompts:read",
        "mcp",
        "read",
        "write"
      ],
      bearer_methods_supported: [
        "header"
      ],
      resource_documentation: `${origin}/mcp`
    };
    return new Response(JSON.stringify(resourcePayload, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // 2. RFC 8414: OAuth Authorization Server Metadata
  if (path.includes("oauth-authorization-server")) {
    const authServerPayload = {
      issuer: origin,
      authorization_endpoint: "https://auth.arcade.dev/oauth2/auth",
      device_authorization_endpoint: "https://auth.arcade.dev/oauth2/device/auth",
      token_endpoint: "https://auth.arcade.dev/oauth2/token",
      userinfo_endpoint: "https://auth.arcade.dev/userinfo",
      revocation_endpoint: "https://auth.arcade.dev/oauth2/revoke",
      jwks_uri: "https://auth.arcade.dev/.well-known/jwks.json",
      response_types_supported: ["code", "token"],
      subject_types_supported: ["public"],
      grant_types_supported: ["authorization_code", "client_credentials", "refresh_token"],
      token_endpoint_auth_methods_supported: ["client_secret_post", "client_secret_basic", "none"],
      scopes_supported: ["openid", "offline_access", "tools", "mcp"],
      code_challenge_methods_supported: ["S256"]
    };
    return new Response(JSON.stringify(authServerPayload, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // 3. OpenID Connect Discovery 1.0 (openid-configuration)
  if (path.includes("openid-configuration")) {
    const oidcPayload = {
      issuer: origin,
      authorization_endpoint: "https://auth.arcade.dev/oauth2/auth",
      device_authorization_endpoint: "https://auth.arcade.dev/oauth2/device/auth",
      token_endpoint: "https://auth.arcade.dev/oauth2/token",
      userinfo_endpoint: "https://auth.arcade.dev/userinfo",
      jwks_uri: "https://auth.arcade.dev/.well-known/jwks.json",
      response_types_supported: ["code", "id_token", "token id_token"],
      subject_types_supported: ["public"],
      id_token_signing_alg_values_supported: ["RS256"],
      scopes_supported: ["openid", "offline_access", "tools", "mcp"],
      token_endpoint_auth_methods_supported: ["client_secret_post", "client_secret_basic", "none"],
      claims_supported: ["sub", "iss", "aud", "exp", "iat"],
      code_challenge_methods_supported: ["S256"]
    };
    return new Response(JSON.stringify(oidcPayload, null, 2), {
      status: 200,
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
        methods: ["none", "oauth2"],
        oauth2: {
          authorization_endpoint: "https://auth.arcade.dev/oauth2/auth",
          token_endpoint: "https://auth.arcade.dev/oauth2/token",
          scopes_supported: ["tools", "mcp"]
        }
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
