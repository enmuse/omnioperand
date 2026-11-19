/**
 * functions/mcp/[[path]].js
 * OmniOperand Root MCP Catch-All Handler
 * 
 * Handles:
 * 1. Subpaths like /mcp/.well-known/openid-configuration and /mcp/.well-known/oauth-protected-resource
 * 2. Aliases to Model Context Protocol JSON-RPC 2.0 Server at /api/v1/mcp
 */

import { onRequestGet as mcpGet, onRequestPost as mcpPost, onRequestOptions as mcpOptions } from '../api/v1/mcp.js';
import { onRequestGet as wellKnownGet, onRequestOptions as wellKnownOptions } from '../.well-known/[[path]].js';

export async function onRequestOptions(context) {
  const path = new URL(context.request.url).pathname;
  if (path.includes(".well-known")) {
    return wellKnownOptions(context);
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
  const path = new URL(context.request.url).pathname;
  if (path.includes(".well-known")) {
    return wellKnownGet(context);
  }
  return mcpGet(context);
}

export async function onRequestPost(context) {
  const path = new URL(context.request.url).pathname;
  if (path.includes(".well-known")) {
    return wellKnownGet(context);
  }
  return mcpPost(context);
}
