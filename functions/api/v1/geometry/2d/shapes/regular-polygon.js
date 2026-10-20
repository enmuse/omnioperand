/**
 * functions/api/v1/geometry/2d/shapes/regular-polygon.js
 * OmniOperand REST API — Universal Regular n-Gon (3-1000) Bidirectional Solver
 * Route: GET /api/v1/geometry/2d/shapes/regular-polygon
 *        POST /api/v1/geometry/2d/shapes/regular-polygon
 */

import { solveRegularPolygon } from '../../../../../../api/solvers/index.js';
import { RegularPolygonInputSchema } from '../../../../../../api/schemas/validation.js';
import { formatSuccessResponse, formatErrorResponse } from '../../../../../../api/gateway/index.js';

export async function onRequestGet(context) {
  const start = performance.now();
  const url = new URL(context.request.url);
  const rawParams = Object.fromEntries(url.searchParams.entries());

  if (!rawParams.value) {
    if (rawParams.val) rawParams.value = rawParams.val;
    else if (rawParams.side) rawParams.value = rawParams.side;
    else if (rawParams.a) rawParams.value = rawParams.a;
  }

  const parsed = RegularPolygonInputSchema.safeParse(rawParams);
  if (!parsed.success) {
    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatErrorResponse({
      code: "VALIDATION_ERROR",
      message: "Invalid regular polygon parameters",
      executionTimeMs: execMs,
      details: parsed.error.format()
    }), null, 2), {
      status: 400,
      headers: { "Content-Type": "application/json; charset=utf-8" }
    });
  }

  const solved = solveRegularPolygon(parsed.data);
  const execMs = performance.now() - start;

  const responsePayload = formatSuccessResponse({
    calculator: solved.calculator,
    inputs: solved.inputs,
    result: solved.result,
    units: solved.units,
    executionTimeMs: execMs,
    meta: {
      exact_radicals: solved.exact_radicals,
      canonical_url: "https://omnioperand.com/geometry/2d/shapes/regular-polygon/",
      docs: "https://omnioperand.com/api/"
    }
  });

  return new Response(JSON.stringify(responsePayload, null, 2), {
    status: 200,
    headers: { "Content-Type": "application/json; charset=utf-8" }
  });
}

export const onRequestHead = onRequestGet;

export async function onRequestPost(context) {
  const start = performance.now();
  try {
    let body = {};
    const ct = context.request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      body = await context.request.json();
    } else {
      const form = await context.request.formData();
      body = Object.fromEntries(form.entries());
    }

    if (!body.value) {
      if (body.val) body.value = body.val;
      else if (body.side) body.value = body.side;
      else if (body.a) body.value = body.a;
    }

    const parsed = RegularPolygonInputSchema.safeParse(body);
    if (!parsed.success) {
      const execMs = performance.now() - start;
      return new Response(JSON.stringify(formatErrorResponse({
        code: "VALIDATION_ERROR",
        message: "Invalid regular polygon parameters",
        executionTimeMs: execMs,
        details: parsed.error.format()
      }), null, 2), {
        status: 400,
        headers: { "Content-Type": "application/json; charset=utf-8" }
      });
    }

    const solved = solveRegularPolygon(parsed.data);
    const execMs = performance.now() - start;

    const responsePayload = formatSuccessResponse({
      calculator: solved.calculator,
      inputs: solved.inputs,
      result: solved.result,
      units: solved.units,
      executionTimeMs: execMs,
      meta: {
        exact_radicals: solved.exact_radicals,
        canonical_url: "https://omnioperand.com/geometry/2d/shapes/regular-polygon/",
        docs: "https://omnioperand.com/api/"
      }
    });

    return new Response(JSON.stringify(responsePayload, null, 2), {
      status: 200,
      headers: { "Content-Type": "application/json; charset=utf-8" }
    });
  } catch (err) {
    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatErrorResponse({
      code: "INVALID_PAYLOAD",
      message: err.message,
      executionTimeMs: execMs
    }), null, 2), {
      status: 400,
      headers: { "Content-Type": "application/json; charset=utf-8" }
    });
  }
}
