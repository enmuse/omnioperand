/**
 * functions/_middleware.js
 * Root Cloudflare Pages Edge Middleware
 * 
 * 1. Normalizes www.omnioperand.com -> omnioperand.com (301 Permanent Redirect)
 *    Eliminates duplicate site crawling and resolves the 264 "Alternate page with proper canonical tag" GSC entries.
 * 2. Normalizes duplicate slashes (e.g. // -> /)
 */

export async function onRequest(context) {
  const url = new URL(context.request.url);

  // 1. WWW to Non-WWW 301 Permanent Redirect
  if (url.hostname.startsWith("www.")) {
    const nonWwwHost = url.hostname.replace(/^www\./, "");
    return Response.redirect(`https://${nonWwwHost}${url.pathname}${url.search}`, 301);
  }

  // 2. Double-slash path normalization
  if (url.pathname.includes("//")) {
    const cleanPath = url.pathname.replace(/\/+/g, "/");
    return Response.redirect(`${url.origin}${cleanPath}${url.search}`, 301);
  }

  return context.next();
}
