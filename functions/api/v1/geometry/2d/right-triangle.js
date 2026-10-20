/**
 * functions/api/v1/geometry/2d/right-triangle.js
 * OmniOperand REST API — Right Triangle Engine
 */

import { solveRightTriangle } from '../../../../../api/solvers/index.js';
import { RightTriangleInputSchema } from '../../../../../api/schemas/validation.js';
import { formatSuccessResponse, formatErrorResponse } from '../../../../../api/gateway/index.js';

export async function onRequestGet(context) {
  const start = performance.now();
  const url = new URL(context.request.url);
  const rawParams = Object.fromEntries(url.searchParams.entries());

  const parsed = RightTriangleInputSchema.safeParse(rawParams);
  if (!parsed.success) {
    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatErrorResponse({
      code: "VALIDATION_ERROR",
      message: "Invalid right triangle parameters",
      executionTimeMs: execMs,
      details: parsed.error.format()
    }), null, 2), {
      status: 400,
      headers: { "Content-Type": "application/json; charset=utf-8" }
    });
  }

  const solved = solveRightTriangle(parsed.data);
  const execMs = performance.now() - start;

  return new Response(JSON.stringify(formatSuccessResponse({
    calculator: solved.calculator,
    inputs: solved.inputs,
    result: solved.result,
    units: solved.units,
    executionTimeMs: execMs
  }), null, 2), {
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

    const parsed = RightTriangleInputSchema.safeParse(body);
    if (!parsed.success) {
      const execMs = performance.now() - start;
      return new Response(JSON.stringify(formatErrorResponse({
        code: "VALIDATION_ERROR",
        message: "Invalid right triangle parameters",
        executionTimeMs: execMs,
        details: parsed.error.format()
      }), null, 2), {
        status: 400,
        headers: { "Content-Type": "application/json; charset=utf-8" }
      });
    }

    const solved = solveRightTriangle(parsed.data);
    const execMs = performance.now() - start;

    return new Response(JSON.stringify(formatSuccessResponse({
      calculator: solved.calculator,
      inputs: solved.inputs,
      result: solved.result,
      units: solved.units,
      executionTimeMs: execMs
    }), null, 2), {
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
