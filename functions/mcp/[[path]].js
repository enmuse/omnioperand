/**
 * functions/mcp/[[path]].js
 * OmniOperand Root MCP & Dynamic OAuth Suite
 * 
 * Implements:
 * 1. RFC 7591: Dynamic Client Registration (/mcp/oauth/register)
 * 2. RFC 6749: OAuth 2.0 Token Endpoint (/mcp/oauth/token)
 * 3. RFC 6749: OAuth 2.0 Authorization Endpoint (/mcp/oauth/authorize)
 * 4. Subpaths like /mcp/.well-known/openid-configuration
 * 5. Main Model Context Protocol JSON-RPC 2.0 Server (/mcp)
 */

import { onRequestGet as mcpGet, onRequestPost as mcpPost, onRequestOptions as mcpOptions } from '../api/v1/mcp.js';
import { onRequestGet as wellKnownGet, onRequestOptions as wellKnownOptions } from '../.well-known/[[path]].js';

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, mcp-session-id",
  "Access-Control-Expose-Headers": "mcp-session-id",
  "Content-Type": "application/json"
};

export async function onRequestOptions(context) {
  const path = new URL(context.request.url).pathname;
  if (path.includes(".well-known") || path.includes("/oauth/")) {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  return mcpOptions(context);
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
  const path = url.pathname;

  // 1. OAuth Authorization Endpoint (Redirects with authorization code)
  if (path.includes("/oauth/authorize")) {
    const redirectUri = url.searchParams.get("redirect_uri") || "https://cloud.arcade.dev/api/v1/oauth/callback";
    const state = url.searchParams.get("state") || "";
    const code = "omni-auth-" + Math.random().toString(36).slice(2, 10);
    try {
      const target = new URL(redirectUri);
      target.searchParams.set("code", code);
      if (state) target.searchParams.set("state", state);
      return Response.redirect(target.toString(), 302);
    } catch (e) {
      return new Response(JSON.stringify({ code, status: "authorized" }), {
        status: 200,
        headers: CORS_HEADERS
      });
    }
  }

  // 2. OAuth Userinfo Endpoint
  if (path.includes("/oauth/userinfo")) {
    return new Response(JSON.stringify({
      sub: "omnioperand-public-user",
      name: "OmniOperand Agent",
      preferred_username: "omni-agent",
      email: "agent@omnioperand.com"
    }), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // 3. Subpath .well-known probes
  if (path.includes(".well-known")) {
    return wellKnownGet(context);
  }

  // 4. Fallback to standard MCP server
  return mcpGet(context);
}

export async function onRequestPost(context) {
  const url = new URL(context.request.url);
  const path = url.pathname;

  // 1. RFC 7591: Dynamic Client Registration
  if (path.includes("/oauth/register")) {
    let body = {};
    try {
      body = await context.request.json();
    } catch (e) {}

    const redirectUris = body.redirect_uris || ["https://cloud.arcade.dev/api/v1/oauth/callback"];
    const clientId = "omni-client-" + Math.random().toString(36).slice(2, 10);
    const clientSecret = "omni-secret-" + Math.random().toString(36).slice(2, 16);

    return new Response(JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      client_id_issued_at: Math.floor(Date.now() / 1000),
      client_secret_expires_at: 0,
      redirect_uris: redirectUris,
      grant_types: ["authorization_code", "client_credentials", "refresh_token"],
      response_types: ["code"],
      token_endpoint_auth_method: "client_secret_post"
    }, null, 2), {
      status: 201,
      headers: CORS_HEADERS
    });
  }

  // 2. OAuth 2.0 Token Endpoint
  if (path.includes("/oauth/token")) {
    const accessToken = "omni-token-" + Math.random().toString(36).slice(2, 14);
    return new Response(JSON.stringify({
      access_token: accessToken,
      token_type: "Bearer",
      expires_in: 86400,
      scope: "tools mcp",
      refresh_token: "omni-refresh-" + Math.random().toString(36).slice(2, 14)
    }, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // 3. Subpath .well-known probes
  if (path.includes(".well-known")) {
    return wellKnownGet(context);
  }

  // 4. Fallback to standard MCP server
  return mcpPost(context);
}
