/**
 * functions/api/leads/_dispatcher.js
 * OmniOperand High-Intent Lead Alerting & Webhook Dispatch Engine
 * 
 * Supports:
 * - Discord / Slack / Zapier / Custom Webhooks (via LEAD_WEBHOOK_URL or DISCORD_WEBHOOK_URL)
 * - Instant Email Alerts via Resend (RESEND_API_KEY) or SendGrid (SENDGRID_API_KEY)
 * - Cloudflare KV Storage (LEADS_KV binding)
 * - Guaranteed non-blocking edge dispatch via context.waitUntil()
 */

export async function dispatchLeadAlerts(structuredLead, context) {
  const env = context.env || {};
  const promises = [];

  // 1. Webhook Dispatch (Discord, Slack, Zapier, Make)
  const webhookUrls = new Set();
  if (env.DISCORD_WEBHOOK_URL) webhookUrls.add(env.DISCORD_WEBHOOK_URL);
  if (env.LEAD_WEBHOOK_URL) webhookUrls.add(env.LEAD_WEBHOOK_URL);

  for (const url of webhookUrls) {
    if (url && url.startsWith("http")) {
      promises.push(sendWebhookAlert(url, structuredLead));
    }
  }

  // 2. Email Alert via Resend
  const resendKey = env.RESEND_API_KEY || env.RESEND_API_TOKEN;
  if (resendKey) {
    promises.push(sendResendEmailAlert(resendKey, env.LEAD_ALERT_EMAIL || "brandon@omnioperand.com", structuredLead));
  } else if (env.SENDGRID_API_KEY) {
    promises.push(sendSendGridEmailAlert(env.SENDGRID_API_KEY, env.LEAD_ALERT_EMAIL || "brandon@omnioperand.com", structuredLead));
  }

  // 3. Cloudflare KV Lead Archival
  if (env.LEADS_KV && typeof env.LEADS_KV.put === "function") {
    promises.push(
      env.LEADS_KV.put(`lead:${structuredLead.dispatch_id}`, JSON.stringify(structuredLead), {
        expirationTtl: 60 * 60 * 24 * 90 // 90 days retention
      })
    );
  }

  // Run in background without holding up the HTTP response
  if (promises.length > 0) {
    if (context.waitUntil) {
      context.waitUntil(Promise.allSettled(promises));
    } else {
      await Promise.allSettled(promises);
    }
  }
}

async function sendWebhookAlert(url, lead) {
  try {
    const isDiscord = url.includes("discord.com/api/webhooks");
    let payload = {};

    if (isDiscord) {
      payload = {
        username: "OmniOperand Lead Dispatcher",
        avatar_url: "https://omnioperand.com/assets/images/logo.png",
        embeds: [
          {
            title: `🚨 High-Intent Lead: ${lead.niche.toUpperCase()}`,
            description: `**Inquiry ID:** \`${lead.dispatch_id}\`\n**Calculator:** [View Source Page](${lead.source_url})`,
            color: 0x0284c7, // Sky Blue
            fields: [
              { name: "👤 Full Name", value: lead.full_name || "N/A", inline: true },
              { name: "📧 Email", value: lead.email || "N/A", inline: true },
              { name: "📱 Mobile Phone", value: lead.phone || "N/A", inline: true },
              { name: "📍 Location", value: lead.state_zip || "N/A", inline: true },
              { name: "💳 Credit Tier", value: lead.credit_tier || "N/A", inline: true },
              { name: "🏛️ Deal / Basis Value", value: lead.scenario_summary?.property_value || "$0", inline: true },
              { name: "💰 Equity / Down Payment", value: lead.scenario_summary?.down_payment || "$0", inline: true },
              { name: "📈 Financing Model", value: lead.scenario_summary?.financing_model || "Standard", inline: true },
              { name: "💵 Est. Cash / Monthly", value: lead.scenario_summary?.monthly_budget || "$0", inline: true }
            ],
            footer: {
              text: `OmniOperand Edge Ingestion • ${new Date().toISOString()}`
            }
          }
        ]
      };
    } else {
      // Standard JSON Webhook (Slack / Zapier / Make / Internal CRM)
      payload = {
        event: "lead.created",
        lead_id: lead.dispatch_id,
        niche: lead.niche,
        contact: {
          name: lead.full_name,
          email: lead.email,
          phone: lead.phone,
          state_zip: lead.state_zip
        },
        scenario: lead.scenario_summary,
        source_url: lead.source_url,
        ip: lead.ip,
        timestamp: lead.timestamp
      };
    }

    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    console.warn("[Lead Alert] Webhook dispatch error:", err.message);
  }
}

async function sendResendEmailAlert(apiKey, recipient, lead) {
  try {
    const html = `
      <div style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; max-width:600px; margin:0 auto; background:#0f172a; color:#f8fafc; border:1px solid #334155; border-radius:12px; overflow:hidden;">
        <div style="padding:24px; background:#0284c7; color:#fff;">
          <h2 style="margin:0 0 4px 0; font-size:20px;">🚨 New High-Intent Lead Ingestion</h2>
          <div style="font-size:13px; opacity:0.9;">OmniOperand Ingestion ID: <strong>${lead.dispatch_id}</strong></div>
        </div>
        <div style="padding:24px;">
          <h3 style="margin:0 0 16px 0; font-size:16px; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Client Contact Profile</h3>
          <table style="width:100%; border-collapse:collapse; margin-bottom:24px; font-size:14px;">
            <tr><td style="padding:8px 0; color:#94a3b8; width:140px;">Full Name:</td><td style="padding:8px 0; font-weight:700;">${lead.full_name}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Email Address:</td><td style="padding:8px 0; font-weight:700;"><a href="mailto:${lead.email}" style="color:#38bdf8;">${lead.email}</a></td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Mobile Phone:</td><td style="padding:8px 0; font-weight:700;"><a href="tel:${lead.phone}" style="color:#38bdf8;">${lead.phone}</a></td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">State / Zip:</td><td style="padding:8px 0; font-weight:700;">${lead.state_zip}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Credit Rating:</td><td style="padding:8px 0; font-weight:700;">${lead.credit_tier}</td></tr>
          </table>

          <h3 style="margin:0 0 16px 0; font-size:16px; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Calculated Scenario Snapshot</h3>
          <table style="width:100%; border-collapse:collapse; margin-bottom:24px; font-size:14px;">
            <tr><td style="padding:8px 0; color:#94a3b8; width:140px;">Vertical / Niche:</td><td style="padding:8px 0; font-weight:700; color:#34d399;">${lead.niche.toUpperCase()}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Property / Deal Value:</td><td style="padding:8px 0; font-weight:700;">${lead.scenario_summary?.property_value || "$0"}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Equity / Down:</td><td style="padding:8px 0; font-weight:700;">${lead.scenario_summary?.down_payment || "$0"}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Est. Cash / Monthly:</td><td style="padding:8px 0; font-weight:700;">${lead.scenario_summary?.monthly_budget || "$0"}</td></tr>
            <tr><td style="padding:8px 0; color:#94a3b8;">Origin URL:</td><td style="padding:8px 0;"><a href="${lead.source_url}" style="color:#38bdf8; font-size:12px;">${lead.source_url}</a></td></tr>
          </table>
        </div>
      </div>
    `;

    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        from: "OmniOperand Lead Desk <alerts@omnioperand.com>",
        to: [recipient],
        subject: `[LEAD: ${lead.niche.toUpperCase()}] ${lead.full_name} (${lead.state_zip}) — ${lead.scenario_summary?.property_value || ""}`,
        html: html
      })
    });
  } catch (err) {
    console.warn("[Lead Alert] Resend dispatch error:", err.message);
  }
}

async function sendSendGridEmailAlert(apiKey, recipient, lead) {
  try {
    const payload = {
      personalizations: [{ to: [{ email: recipient }] }],
      from: { email: "alerts@omnioperand.com", name: "OmniOperand Lead Desk" },
      subject: `[LEAD: ${lead.niche.toUpperCase()}] ${lead.full_name} (${lead.state_zip})`,
      content: [{
        type: "text/plain",
        value: `New High-Intent Lead Ingestion:
Lead ID: ${lead.dispatch_id}
Niche: ${lead.niche}
Name: ${lead.full_name}
Email: ${lead.email}
Phone: ${lead.phone}
Location: ${lead.state_zip}
Deal Size: ${lead.scenario_summary?.property_value}
Source: ${lead.source_url}`
      }]
    };

    await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    console.warn("[Lead Alert] SendGrid dispatch error:", err.message);
  }
}
