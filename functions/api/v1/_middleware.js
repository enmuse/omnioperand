/**
 * functions/api/v1/_middleware.js
 * Cloudflare Pages Functions Gateway Middleware
 * Enforces API Key Auth, Tier Rate Limiting, Usage Metering, and Standardized Envelopes.
 */

import { apiKeyRegistry, rateLimiter, usageTracker, extractApiKey, formatErrorResponse, TIERS } from '../../../api/gateway/index.js';

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, x-api-key",
  "Access-Control-Expose-Headers": "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-Consumer-ID, X-Tier",
  "X-Robots-Tag": "noindex, nofollow",
  "X-Powered-By": "OmniOperand Edge Compute"
};

export async function onRequest(context) {
  const { request } = context;
  const start = performance.now();
  const url = new URL(request.url);
  const path = url.pathname;

  // 1. Handle Preflight CORS
  if (request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: CORS_HEADERS
    });
  }

  // 2. Identify Public Endpoints Exempt from Strict Auth
  const isPublicDocOrPrompt = path.endsWith('/openapi.json') ||
                              path.endsWith('/prompts') ||
                              path.includes('/auth/keys') ||
                              path.includes('/leads');

  // 3. Extract API Key (Header or query param fallback)
  let rawKey = extractApiKey(request);
  if (!rawKey) {
    rawKey = url.searchParams.get('api_key') || url.searchParams.get('apikey');
  }

  let consumerId = 'usr_anonymous';
  let tier = 'free';
  let clientRecord = null;

  if (rawKey) {
    clientRecord = await apiKeyRegistry.validateKey(rawKey);
    if (!clientRecord) {
      const execMs = performance.now() - start;
      const errBody = formatErrorResponse({
        code: "UNAUTHORIZED",
        message: "Invalid or revoked API key. Pass 'Authorization: Bearer <KEY>' or 'x-api-key'. For free key generation, visit /api/v1/auth/keys or use demo key 'omni_live_free_demo_key_123'.",
        executionTimeMs: execMs
      });
      return new Response(JSON.stringify(errBody, null, 2), {
        status: 401,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" }
      });
    }
    consumerId = clientRecord.consumerId;
    tier = clientRecord.tier;
  } else {
    // If endpoint requires auth and no key is provided
    if (!isPublicDocOrPrompt) {
      // Use client IP hash as consumerId on Free tier sandbox
      const clientIp = request.headers.get('cf-connecting-ip') ||
                       request.headers.get('x-forwarded-for') ||
                       '127.0.0.1';
      consumerId = `anon_${clientIp.replace(/[^a-zA-Z0-9]/g, '').slice(0, 16)}`;
      tier = 'free';
    }
  }

  // 4. Rate Limiting Check
  const rateCheck = rateLimiter.checkRateLimit(consumerId, tier);
  const rateHeaders = {
    "X-RateLimit-Limit": String(rateCheck.limit),
    "X-RateLimit-Remaining": String(rateCheck.remaining),
    "X-RateLimit-Reset": String(rateCheck.resetSeconds),
    "X-Consumer-ID": consumerId,
    "X-Tier": tier
  };

  if (!rateCheck.allowed) {
    const execMs = performance.now() - start;
    const errBody = formatErrorResponse({
      code: "RATE_LIMIT_EXCEEDED",
      message: `Rate limit exceeded for tier '${tier}'. Limit: ${rateCheck.limit} req/min. Reset in ${rateCheck.resetSeconds}s. Upgrade to Pro at https://omnioperand.com/pricing`,
      executionTimeMs: execMs,
      details: {
        tier,
        limit_per_minute: rateCheck.limit,
        reset_in_seconds: rateCheck.resetSeconds,
        usage_this_month: rateCheck.currentUsageMonth,
        monthly_quota: rateCheck.monthLimit
      }
    });

    usageTracker.recordRequest({
      consumerId,
      tier,
      path,
      method: request.method,
      status: 429,
      latencyMs: execMs
    });

    return new Response(JSON.stringify(errBody, null, 2), {
      status: 429,
      headers: {
        ...CORS_HEADERS,
        ...rateHeaders,
        "Retry-After": String(rateCheck.resetSeconds),
        "Content-Type": "application/json"
      }
    });
  }

  // Store auth/rate context in data
  context.data = {
    consumerId,
    tier,
    rateCheck,
    startTime: start
  };

  // 5. Proceed to Endpoint Handler
  let response;
  try {
    response = await context.next();
  } catch (err) {
    const execMs = performance.now() - start;
    const errBody = formatErrorResponse({
      code: "INTERNAL_ERROR",
      message: err.message || "An unexpected error occurred processing your calculation request.",
      executionTimeMs: execMs
    });
    return new Response(JSON.stringify(errBody, null, 2), {
      status: 500,
      headers: { ...CORS_HEADERS, ...rateHeaders, "Content-Type": "application/json" }
    });
  }

  const execMs = performance.now() - start;

  // 6. Record Usage Telemetry
  usageTracker.recordRequest({
    consumerId,
    tier,
    path,
    method: request.method,
    status: response.status,
    latencyMs: execMs
  });

  // 7. Inject Rate Limit and CORS Headers into Response
  const newHeaders = new Headers(response.headers);
  for (const [k, v] of Object.entries(CORS_HEADERS)) {
    if (!newHeaders.has(k)) newHeaders.set(k, v);
  }
  for (const [k, v] of Object.entries(rateHeaders)) {
    newHeaders.set(k, v);
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}
