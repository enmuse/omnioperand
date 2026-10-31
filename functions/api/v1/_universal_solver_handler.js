/**
 * functions/api/v1/_universal_solver_handler.js
 * Universal Cloudflare Pages Function Router & 301 Resolver for all OmniOperand Deterministic Solvers.
 * 
 * 1. Web Crawlers & HTML Browsers (Googlebot, Bingbot, standard browser GET):
 *    Returns HTTP 301 Moved Permanently redirecting to https://omnioperand.com/:category/:slug/
 *    This eliminates 361 GSC 404 crawl errors and funnels all link equity to the canonical HTML calculators.
 * 
 * 2. API Clients & AI Agents (Accept: application/json, POST, or query params):
 *    Executes the calculation via CALCULATOR_REGISTRY or returns solver JSON schema.
 */

import { CALCULATOR_REGISTRY, executeCalculator } from '../../../../api/solvers/calculator_registry.js';

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key",
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "public, max-age=3600, s-maxage=86400",
  "X-Robots-Tag": "noindex, nofollow"
};

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS
  });
}

export async function handleUniversalApiRequest(context, category, slugParts) {
  const request = context.request;
  const url = new URL(request.url);
  const acceptHeader = (request.headers.get("accept") || "").toLowerCase();
  const userAgent = (request.headers.get("user-agent") || "").toLowerCase();

  // Extract clean slug
  let slug = "";
  if (Array.isArray(slugParts)) {
    slug = slugParts.filter(Boolean).pop() || "";
  } else if (typeof slugParts === "string") {
    slug = slugParts;
  }

  // Fallback: extract slug from pathname if empty
  if (!slug) {
    const segments = url.pathname.split("/").filter(Boolean);
    slug = segments[segments.length - 1] || "";
  }

  // Find in registry if available
  const calc = CALCULATOR_REGISTRY[slug];
  const targetCategory = category || (calc ? calc.category : "") || "";
  const canonicalWebUrl = `https://omnioperand.com/${targetCategory ? targetCategory + "/" : ""}${slug}/`;

  // 1. Check if caller is a search bot, crawler, or browser requesting HTML
  const isSearchBot = /googlebot|bingbot|yandex|duckduckbot|slurp|baiduspider|crawler|spider|bot|facebookexternalhit|twitterbot/i.test(userAgent);
  const isBrowserHtml = acceptHeader.includes("text/html");
  const isExplicitJson = acceptHeader.includes("application/json") || url.searchParams.get("format") === "json";

  // If GET request from browser or crawler, or anything not explicitly asking for JSON:
  if (request.method === "GET" && (isSearchBot || isBrowserHtml || !isExplicitJson)) {
    // 301 Permanent Redirect to canonical HTML solver page!
    return Response.redirect(canonicalWebUrl, 301);
  }

  // 2. Handle API Clients (JSON requests)
  if (!calc) {
    // If not in registry and it is a GET, 301 redirect to canonical web URL
    if (request.method === "GET") {
      return Response.redirect(canonicalWebUrl, 301);
    }
    return new Response(JSON.stringify({
      status: "error",
      message: `Calculator '${slug}' not found`
    }, null, 2), {
      status: 404,
      headers: CORS_HEADERS
    });
  }

  if (request.method === "GET") {
    // If query params are provided, execute calculation
    const paramsCount = Array.from(url.searchParams.keys()).filter(k => k !== "format" && k !== "api_key").length;
    if (paramsCount > 0) {
      const inputs = Object.fromEntries(url.searchParams.entries());
      const result = executeCalculator(slug, inputs);
      const status = result.status === "error" ? 400 : 200;
      return new Response(JSON.stringify(result, null, 2), {
        status,
        headers: CORS_HEADERS
      });
    }

    // Return metadata schema
    return new Response(JSON.stringify({
      status: "success",
      slug: calc.slug,
      category: calc.category,
      name: calc.name,
      description: calc.description,
      formula: calc.formula_display,
      fields: calc.fields,
      metrics: calc.metrics,
      web_url: canonicalWebUrl
    }, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  if (request.method === "POST") {
    let body = {};
    try {
      const ct = request.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        body = await request.json();
      } else {
        const form = await request.formData();
        body = Object.fromEntries(form.entries());
      }
    } catch (e) {
      body = {};
    }

    const inputs = body.inputs || body;
    const result = executeCalculator(slug, inputs);
    const status = result.status === "error" ? 400 : 200;
    return new Response(JSON.stringify(result, null, 2), {
      status,
      headers: CORS_HEADERS
    });
  }

  return new Response("Method Not Allowed", { status: 405, headers: CORS_HEADERS });
}
