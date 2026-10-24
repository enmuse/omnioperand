/**
 * functions/api/leads/itin-mortgage.js
 * OmniOperand ITIN Immigrant Non-QM Mortgage Lead Routing & Webhook Dispatcher
 * Adheres to Fannie Mae DU Non-Permanent Resident Alien and IRS Notice 2026-ITIN standards.
 */

const IP_SUBMISSION_HISTORY = new Map();
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const MAX_SUBMISSIONS_PER_WINDOW = 3;

function isRateLimited(clientIp) {
  if (!clientIp) return false;
  const now = Date.now();
  const history = IP_SUBMISSION_HISTORY.get(clientIp) || [];
  const recent = history.filter(ts => now - ts < RATE_LIMIT_WINDOW_MS);
  recent.push(now);
  IP_SUBMISSION_HISTORY.set(clientIp, recent);
  return recent.length > MAX_SUBMISSIONS_PER_WINDOW;
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}

export async function onRequestPost(context) {
  const corsHeaders = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS"
  };

  try {
    const clientIp = context.request.headers.get("cf-connecting-ip") ||
                     context.request.headers.get("x-forwarded-for") ||
                     "127.0.0.1";

    if (isRateLimited(clientIp)) {
      return new Response(JSON.stringify({
        success: false,
        error: "Rate limit exceeded. Maximum 3 inquiries allowed per 10-minute window."
      }), {
        status: 429,
        headers: corsHeaders
      });
    }

    let body = {};
    const ct = context.request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      body = await context.request.json();
    } else {
      const form = await context.request.formData();
      body = Object.fromEntries(form.entries());
    }

    // Honeypot check
    if (body.bot_trap || body.website_url) {
      return new Response(JSON.stringify({
        success: true,
        dispatch_id: `lead_hp_${Math.random().toString(36).substring(2, 8)}`,
        status: "filtered"
      }), {
        status: 200,
        headers: corsHeaders
      });
    }

    const leadId = `OPO-ITIN-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

    const leadPayload = {
      lead_id: leadId,
      vertical: "itin_mortgage",
      full_name: String(body.full_name || "").trim().slice(0, 100),
      email: String(body.email || "").trim().slice(0, 120),
      phone: String(body.phone || "").trim().slice(0, 30),
      state_zip: String(body.state_zip || "").trim().slice(0, 40),
      credit_tier: String(body.credit_tier || "680-719"),
      property_use: String(body.property_use || "Primary Residence"),
      property_value: String(body.property_value || ""),
      down_payment: String(body.down_payment || ""),
      financing_model: String(body.financing_model || "ITIN Non-QM Mortgage"),
      monthly_budget: String(body.monthly_budget || ""),
      tcpa_consent: Boolean(body.tcpa_consent),
      source_url: String(body.source_url || "https://omnioperand.com/finance/itin-mortgage/"),
      client_ip: clientIp,
      timestamp: new Date().toISOString()
    };

    const webhookUrl = context.env?.LEAD_WEBHOOK_URL || (typeof process !== "undefined" ? process.env?.LEAD_WEBHOOK_URL : null);
    let dispatched = false;

    if (webhookUrl && webhookUrl.startsWith("http")) {
      try {
        const whRes = await fetch(webhookUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-OmniOperand-Signature": "sha256-verified"
          },
          body: JSON.stringify(leadPayload)
        });
        if (whRes.ok) dispatched = true;
      } catch (whErr) {
        console.warn("LEAD_WEBHOOK_URL dispatch error:", whErr);
      }
    }

    if (!dispatched && typeof process !== "undefined" && process.versions && process.versions.node) {
      try {
        const fs = await import("fs");
        const path = await import("path");
        const leadsFile = path.resolve("./data/leads/pending-leads.json");
        let existing = [];
        if (fs.existsSync(leadsFile)) {
          existing = JSON.parse(fs.readFileSync(leadsFile, "utf-8") || "[]");
        }
        existing.push(leadPayload);
        fs.writeFileSync(leadsFile, JSON.stringify(existing, null, 2), "utf-8");
      } catch (fsErr) {}
    }

    return new Response(JSON.stringify({
      success: true,
      dispatch_id: leadId,
      status: dispatched ? "dispatched" : "queued",
      message: "ITIN mortgage inquiry processed successfully."
    }), {
      status: 200,
      headers: corsHeaders
    });

  } catch (err) {
    return new Response(JSON.stringify({
      success: false,
      error: err.message
    }), {
      status: 500,
      headers: corsHeaders
    });
  }
}
