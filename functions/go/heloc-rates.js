/**
 * functions/go/heloc-rates.js
 * Cloudflare Pages Function: HELOC Affiliate Dispatch & Tracking Bridge
 * Seamlessly passes through query parameters (subid, draw, utm_*) with HTTP 302
 */

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const targetBase = context.env.HELOC_AFFILIATE_URL || "https://www.lendingtree.com/home-equity/heloc/";
  const targetUrl = new URL(targetBase);

  // Preserve all incoming query parameters for attribution
  for (const [key, value] of url.searchParams.entries()) {
    targetUrl.searchParams.set(key, value);
  }

  return Response.redirect(targetUrl.toString(), 302);
}
