/**
 * functions/api/v1/solve/[[path]].js
 * Universal Cloudflare Pages Function Router for all OmniOperand Deterministic Solvers.
 * 
 * Routes:
 *   GET  /api/v1/solve                    -> Index of all solvers
 *   GET  /api/v1/solve/:category/:slug   -> Solver schema & metadata
 *   POST /api/v1/solve/:category/:slug   -> Execute calculation
 *   POST /api/v1/solve                   -> Dispatch calculation via { calculator, inputs }
 */

import { CALCULATOR_REGISTRY, executeCalculator } from '../../../../api/solvers/calculator_registry.js';

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key",
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "public, max-age=3600, s-maxage=86400"
};

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS
  });
}

export async function onRequestGet(context) {
  const params = context.params.path || [];
  
  // Case 1: GET /api/v1/solve -> Return directory index
  if (params.length === 0) {
    const list = Object.values(CALCULATOR_REGISTRY).map(c => ({
      slug: c.slug,
      category: c.category,
      name: c.name,
      description: c.description,
      formula: c.formula_display,
      endpoint: `/api/v1/solve/${c.category}/${c.slug}`
    }));

    return new Response(JSON.stringify({
      status: "success",
      total_calculators: list.length,
      solvers: list
    }, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  }

  // Case 2: GET /api/v1/solve/:category/:slug or /api/v1/solve/:slug
  let slug = params.length >= 2 ? params[1] : params[0];
  const calc = CALCULATOR_REGISTRY[slug];

  if (!calc) {
    return new Response(JSON.stringify({
      status: "error",
      message: `Calculator '${slug}' not found`
    }), {
      status: 404,
      headers: CORS_HEADERS
    });
  }

  return new Response(JSON.stringify({
    status: "success",
    slug: calc.slug,
    category: calc.category,
    name: calc.name,
    description: calc.description,
    formula: calc.formula_display,
    fields: calc.fields,
    metrics: calc.metrics
  }, null, 2), {
    status: 200,
    headers: CORS_HEADERS
  });
}

export async function onRequestPost(context) {
  const params = context.params.path || [];
  let slug = params.length >= 2 ? params[1] : (params.length === 1 ? params[0] : null);

  let body = {};
  try {
    body = await context.request.json();
  } catch (e) {
    body = {};
  }

  if (!slug && body.calculator) {
    slug = body.calculator;
  }

  if (!slug) {
    return new Response(JSON.stringify({
      status: "error",
      message: "Missing calculator slug in URL path or request payload"
    }), {
      status: 400,
      headers: CORS_HEADERS
    });
  }

  const inputs = body.inputs || body;
  const result = executeCalculator(slug, inputs);

  const status = result.status === "error" ? 400 : 200;
  return new Response(JSON.stringify(result, null, 2), {
    status,
    headers: CORS_HEADERS
  });
}
