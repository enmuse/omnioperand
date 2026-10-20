/**
 * functions/api/v1/auth/keys.js
 * API Key Management Endpoint
 * POST /api/v1/auth/keys -> Create a new API key with tier quota
 * GET /api/v1/auth/keys -> Verify active key or inspect tier limits
 */

import { apiKeyRegistry, TIERS, formatSuccessResponse, formatErrorResponse } from '../../../../api/gateway/index.js';
import { CreateApiKeySchema } from '../../../../api/schemas/validation.js';

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

    const parsed = CreateApiKeySchema.safeParse(body);
    if (!parsed.success) {
      const errMs = performance.now() - start;
      return new Response(JSON.stringify(formatErrorResponse({
        code: "VALIDATION_ERROR",
        message: "Invalid key creation parameters",
        executionTimeMs: errMs,
        details: parsed.error.format()
      }), null, 2), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const { tier, name, email } = parsed.data;
    const keyRecord = await apiKeyRegistry.createKey(tier, name, email);

    const execMs = performance.now() - start;
    const responsePayload = formatSuccessResponse({
      calculator: "auth_key_service",
      inputs: { tier, name },
      result: {
        api_key: keyRecord.apiKey,
        key_hash: keyRecord.keyHash,
        consumer_id: keyRecord.consumerId,
        tier: keyRecord.tier,
        name: keyRecord.name,
        created_at: keyRecord.createdAt,
        quota: keyRecord.quota,
        instructions: "Include 'Authorization: Bearer <api_key>' or 'x-api-key: <api_key>' on all subsequent API requests."
      },
      executionTimeMs: execMs
    });

    return new Response(JSON.stringify(responsePayload, null, 2), {
      status: 201,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatErrorResponse({
      code: "INTERNAL_ERROR",
      message: err.message,
      executionTimeMs: execMs
    }), null, 2), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

export async function onRequestGet(context) {
  const start = performance.now();
  const execMs = performance.now() - start;

  return new Response(JSON.stringify(formatSuccessResponse({
    calculator: "auth_key_service",
    inputs: {},
    result: {
      available_tiers: TIERS,
      demo_keys: {
        free: "omni_live_free_demo_key_123",
        pro: "omni_live_pro_demo_key_456",
        enterprise: "omni_live_enterprise_demo_key_789"
      },
      documentation: "https://omnioperand.com/api/",
      openapi_spec: "https://omnioperand.com/api/v1/openapi.json"
    },
    executionTimeMs: execMs
  }), null, 2), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}
