/**
 * functions/_middleware.js
 * Root Cloudflare Pages Edge Middleware
 * 
 * 1. Normalizes www.omnioperand.com -> omnioperand.com (301 Permanent Redirect)
 * 2. Normalizes duplicate slashes (e.g. // -> /)
 * 3. 301 Redirects translated slug variants to canonical paths (resolves GSC 404 validation)
 * 4. 301 Redirects untranslated localized category paths to canonical English paths
 * 5. Intercepts downstream 404 responses for localized routes and redirects to canonical English
 */

const UNTRANSLATED_CATEGORIES = new Set([
  "agriculture", "biotech", "civil", "crypto", "dispatch",
  "ecommerce", "energy", "health", "legal", "logistics"
]);

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

  // 3. Normalize legacy /calculators/ prefix
  if (url.pathname.startsWith("/calculators/")) {
    const normalized = url.pathname.replace(/^\/calculators/, "");
    return Response.redirect(`${url.origin}${normalized || "/"}${url.search}`, 301);
  }

  // 4. Specific slug typo redirects
  if (url.pathname.includes("/solar-panel-payback")) {
    return Response.redirect(`${url.origin}/energy/solar-payback/`, 301);
  }
  if (url.pathname.includes("/pallet-load")) {
    return Response.redirect(`${url.origin}/logistics/pallet-ti-hi-optimizer/`, 301);
  }
  if (url.pathname.includes("/air-freight-volumetric")) {
    return Response.redirect(`${url.origin}/logistics/air-freight-chargeable-weight/`, 301);
  }
  if (url.pathname.startsWith("/ingegneria/dimensionamento-gruppo-elettrogeno")) {
    return Response.redirect(`${url.origin}/engineering/generator-sizing/`, 301);
  }

  // 5. Translated finance slugs normalization
  if (/rule-(?:de|di|av|z|van|von|n)-72/.test(url.pathname)) {
    return Response.redirect(`${url.origin}/finance/rule-of-72/`, 301);
  }
  if (/saas-rule-(?:de|di|av|z|van|von|n)-40/.test(url.pathname)) {
    return Response.redirect(`${url.origin}/finance/saas-rule-of-40/`, 301);
  }
  if (/internal-rate-(?:de|di|av|z|van|von|n)-return/.test(url.pathname)) {
    return Response.redirect(`${url.origin}/finance/internal-rate-of-return/`, 301);
  }
  if (/fsa-use-it-(?:o|ou|eller|oder|lub|tai|sau|van)-lose-it/.test(url.pathname)) {
    return Response.redirect(`${url.origin}/finance/fsa-use-it-or-lose-it/`, 301);
  }

  // 6. Fast-path redirect for untranslated category routes under language codes
  const langCategoryMatch = url.pathname.match(/^\/(de|es|fi|fr|it|nl|no|pl|pt|ro|sv)\/([^\/]+)(\/.*)?$/);
  if (langCategoryMatch) {
    const [, lang, category, rest] = langCategoryMatch;
    if (UNTRANSLATED_CATEGORIES.has(category) || (category === "engineering" && lang !== "it")) {
      const canonicalPath = `/${category}${rest || "/"}`;
      return Response.redirect(`${url.origin}${canonicalPath}${url.search}`, 301);
    }
  }

  // Execute downstream handlers
  const response = await context.next();

  // 7. 404 Interceptor: Fallback localized 404s to canonical English equivalents
  if (response.status === 404) {
    const localizedMatch = url.pathname.match(/^\/(de|es|fi|fr|it|nl|no|pl|pt|ro|sv)\/(.+)$/);
    if (localizedMatch) {
      const strippedPath = `/${localizedMatch[2]}`;
      return Response.redirect(`${url.origin}${strippedPath}${url.search}`, 301);
    }
  }

  return response;
}
