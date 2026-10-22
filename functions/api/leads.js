/**
 * functions/api/leads.js
 * OmniOperand Machine & Trade Lead Dispatch Webhook
 * Performs two-tier geo-routing for Western North Carolina vs National inquiries.
 */

const WNC_COUNTIES = new Set([
  "cherokee", "clay", "graham", "swain", "macon", "jackson", "haywood",
  "transylvania", "henderson", "buncombe", "madison", "polk", "rutherford",
  "mcdowell", "yancey", "mitchell", "avery", "watauga", "ashe", "alleghany",
  "wilkes", "surry", "yadkin"
]);

function isWncLocation(zip, state, county) {
  const cleanZip = String(zip || "").trim();
  if (/^(287|288|286|289)\d{2}$/.test(cleanZip)) {
    return true;
  }
  const cleanState = String(state || "").trim().toUpperCase();
  const cleanCounty = String(county || "").trim().toLowerCase().replace(/\s+county$/, "");
  if (cleanState === "NC" && WNC_COUNTIES.has(cleanCounty)) {
    return true;
  }
  return false;
}

export async function onRequestPost(context) {
  try {
    let body = {};
    const ct = context.request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      body = await context.request.json();
    } else {
      const form = await context.request.formData();
      body = Object.fromEntries(form.entries());
    }

    const zip = body.zip || body.zipcode || "";
    const state = body.state || "";
    const county = body.county || "";
    const isWnc = isWncLocation(zip, state, county);

    const leadId = `disp_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    if (isWnc) {
      return new Response(JSON.stringify({
        success: true,
        tier: 1,
        zone: "Western North Carolina",
        corridor: "Southern Plateau & Metro Asheville",
        dispatch_id: leadId,
        message: "Project matched to on-call mountain crews in the Southern Plateau & Metro Asheville corridors."
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    } else {
      return new Response(JSON.stringify({
        success: true,
        tier: 2,
        zone: "National / Out-of-Market",
        dispatch_id: leadId,
        message: "OmniOperand Dispatch is currently at peak capacity for heavy civil machinery outside the Appalachian Southeastern corridor. Click below to view vetted regional contractors in your area.",
        referral_url: `https://www.networx.com/?ref=omnioperand&zip=${encodeURIComponent(zip)}`
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }
  } catch (err) {
    return new Response(JSON.stringify({ success: false, error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
