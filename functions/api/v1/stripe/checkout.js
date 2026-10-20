/**
 * functions/api/v1/stripe/checkout.js
 * Stripe Checkout Session Creation Endpoint
 * POST /api/v1/stripe/checkout
 * Generates hosted Stripe Checkout sessions for Pro ($29/mo) and Enterprise ($199/mo) tiers.
 */

import { formatSuccessResponse, formatErrorResponse } from '../../../../api/gateway/index.js';

const DEFAULT_STRIPE_SECRET_KEY = "";

const TIER_PRICING = {
  pro: {
    price_id: "price_1USiRmAhO4PtNxeltaIxNgHz",
    name: "OmniOperand Pro Tier (API, MCP & White-Label CaaS)",
    unit_amount: 2900, // $29.00
    currency: "usd",
    description: "50,000 requests/mo, 60 req/min, Model Context Protocol (MCP) server access, white-label widget embedding, and commercial license."
  },
  enterprise: {
    price_id: "price_1USiRmAhO4PtNxel0aPnsnLr",
    name: "OmniOperand Enterprise Tier (AI Clusters & Custom SLA)",
    unit_amount: 19900, // $199.00
    currency: "usd",
    description: "1,000,000 requests/mo, 300 req/min, priority edge routing, unlimited lead-capture webhooks, and dedicated prompt engineering."
  }
};

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

    const tier = (body.tier || 'pro').toLowerCase();
    const pricing = TIER_PRICING[tier] || TIER_PRICING.pro;
    const email = body.email ? String(body.email).trim() : null;

    const origin = new URL(context.request.url).origin;
    const successUrl = body.success_url || `${origin}/pricing/?session_id={CHECKOUT_SESSION_ID}&status=success`;
    const cancelUrl = body.cancel_url || `${origin}/pricing/?status=cancelled`;

    const stripeKey = context.env?.STRIPE_SECRET_KEY || DEFAULT_STRIPE_SECRET_KEY;

    // Direct Stripe API call with URLSearchParams body
    const params = new URLSearchParams();
    params.append('mode', 'subscription');
    params.append('success_url', successUrl);
    params.append('cancel_url', cancelUrl);
    // Note: payment_method_types omitted to enable Stripe Dynamic Payment Methods (Apple Pay, Google Pay, Cards, Link)

    if (email) {
      params.append('customer_email', email);
    }

    // Line item configuration: use dedicated price ID if configured, else dynamic price_data
    const activePriceId = (tier === 'enterprise' ? context.env?.STRIPE_ENTERPRISE_PRICE_ID : context.env?.STRIPE_PRO_PRICE_ID) || pricing.price_id;
    if (activePriceId) {
      params.append('line_items[0][price]', activePriceId);
      params.append('line_items[0][quantity]', '1');
    } else {
      params.append('line_items[0][price_data][currency]', pricing.currency);
      params.append('line_items[0][price_data][unit_amount]', String(pricing.unit_amount));
      params.append('line_items[0][price_data][recurring][interval]', 'month');
      params.append('line_items[0][price_data][product_data][name]', pricing.name);
      params.append('line_items[0][price_data][product_data][description]', pricing.description);
      params.append('line_items[0][quantity]', '1');
    }

    // Metadata
    params.append('metadata[tier]', tier);
    params.append('metadata[service]', 'omnioperand');

    const stripeRes = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${stripeKey}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    });

    const sessionData = await stripeRes.json();
    const execMs = performance.now() - start;

    if (!stripeRes.ok) {
      return new Response(JSON.stringify(formatErrorResponse({
        code: "STRIPE_CHECKOUT_ERROR",
        message: sessionData.error?.message || "Failed to create checkout session with Stripe",
        executionTimeMs: execMs,
        details: sessionData.error
      }), null, 2), {
        status: stripeRes.status,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify(formatSuccessResponse({
      calculator: "stripe_checkout",
      inputs: { tier, email },
      result: {
        session_id: sessionData.id,
        checkout_url: sessionData.url,
        tier,
        amount_usd: pricing.unit_amount / 100,
        billing_interval: "monthly"
      },
      executionTimeMs: execMs
    }), null, 2), {
      status: 200,
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
