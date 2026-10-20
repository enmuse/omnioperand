/**
 * functions/api/v1/stripe/webhook.js
 * Stripe Webhook Handler Endpoint
 * POST /api/v1/stripe/webhook
 * Ingests Stripe lifecycle events to automatically provision and manage API keys.
 */

import { apiKeyRegistry, formatSuccessResponse, formatErrorResponse } from '../../../../api/gateway/index.js';

export async function onRequestPost(context) {
  const start = performance.now();
  try {
    let event = null;
    try {
      event = await context.request.json();
    } catch (_) {
      const execMs = performance.now() - start;
      return new Response(JSON.stringify(formatErrorResponse({
        code: "INVALID_JSON_PAYLOAD",
        message: "Failed to parse webhook JSON body",
        executionTimeMs: execMs
      }), null, 2), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const eventType = event.type || 'unknown';
    let provisionedKey = null;

    if (eventType === 'checkout.session.completed') {
      const session = event.data?.object || {};
      const customerEmail = session.customer_details?.email || session.customer_email || 'subscriber@omnioperand.com';
      const tier = session.metadata?.tier || 'pro';
      const customerId = session.customer || `cus_${Math.random().toString(36).substring(2, 10)}`;

      // Automatically provision production API key for this subscriber
      provisionedKey = await apiKeyRegistry.createKey(tier, `Stripe Key (${customerEmail})`, customerEmail);

      console.log(`[Stripe Webhook] Successfully provisioned ${tier.toUpperCase()} key for ${customerEmail} (Customer: ${customerId})`);
    }

    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatSuccessResponse({
      calculator: "stripe_webhook",
      inputs: { event_type: eventType },
      result: {
        received: true,
        event_id: event.id || null,
        event_type: eventType,
        ...(provisionedKey ? {
          provisioned_key_preview: provisionedKey.apiKey ? `${provisionedKey.apiKey.slice(0, 10)}...` : null,
          tier: provisionedKey.tier
        } : {})
      },
      executionTimeMs: execMs
    }), null, 2), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    const execMs = performance.now() - start;
    return new Response(JSON.stringify(formatErrorResponse({
      code: "WEBHOOK_PROCESSING_ERROR",
      message: err.message,
      executionTimeMs: execMs
    }), null, 2), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
