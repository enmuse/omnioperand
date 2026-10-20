/**
 * functions/api/v1/stripe/portal.js
 * Stripe Customer Billing Portal Session Endpoint
 * POST /api/v1/stripe/portal
 * Allows subscribed customers to manage subscriptions, update cards, and view invoices.
 */

import { formatSuccessResponse, formatErrorResponse } from '../../../../api/gateway/index.js';

const DEFAULT_STRIPE_SECRET_KEY = "";

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

    const customerId = body.customer_id;
    if (!customerId) {
      const execMs = performance.now() - start;
      return new Response(JSON.stringify(formatErrorResponse({
        code: "MISSING_CUSTOMER_ID",
        message: "A valid Stripe customer_id is required to open the billing portal",
        executionTimeMs: execMs
      }), null, 2), {
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const origin = new URL(context.request.url).origin;
    const returnUrl = body.return_url || `${origin}/pricing/`;
    const stripeKey = context.env?.STRIPE_SECRET_KEY || DEFAULT_STRIPE_SECRET_KEY;

    const params = new URLSearchParams();
    params.append('customer', customerId);
    params.append('return_url', returnUrl);

    const stripeRes = await fetch('https://api.stripe.com/v1/billing_portal/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${stripeKey}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    });

    const portalData = await stripeRes.json();
    const execMs = performance.now() - start;

    if (!stripeRes.ok) {
      return new Response(JSON.stringify(formatErrorResponse({
        code: "STRIPE_PORTAL_ERROR",
        message: portalData.error?.message || "Failed to create customer portal session",
        executionTimeMs: execMs,
        details: portalData.error
      }), null, 2), {
        status: stripeRes.status,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify(formatSuccessResponse({
      calculator: "stripe_portal",
      inputs: { customer_id: customerId },
      result: {
        portal_url: portalData.url
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
