/**
 * functions/embed/[[catchall]].js
 * Cloudflare Pages Function: Universal Embed Route Engine
 * Serves zero-clutter, responsive, iframe-embeddable calculator views with auto-resizing
 * and permanent attribution backlinking.
 */

export async function onRequest(context) {
  const url = new URL(context.request.url);
  // URL format: /embed/category/tool-slug/
  const embedPath = url.pathname.replace(/^\/embed\//, '').replace(/\/$/, '');
  
  if (!embedPath) {
    // If /embed/ is requested with no subpath, pass to /embed/index.html showcase
    return context.next();
  }

  // Construct target canonical calculator URL
  const targetCanonicalUrl = new URL(`/${embedPath}/`, url.origin);
  targetCanonicalUrl.search = url.search; // Preserve query parameters

  let canonicalResponse;
  try {
    canonicalResponse = await context.env.ASSETS.fetch(targetCanonicalUrl);
  } catch (err) {
    // Fallback to direct fetch
    canonicalResponse = await fetch(targetCanonicalUrl);
  }

  if (!canonicalResponse.ok) {
    return new Response(
      `<!DOCTYPE html><html><body style="font-family:sans-serif;background:#0f172a;color:#f8fafc;padding:2rem;text-align:center;">
        <h3>OmniOperand Embed Widget</h3>
        <p>Calculator tool <code>${embedPath}</code> not found.</p>
        <p><a href="https://omnioperand.com/" target="_blank" style="color:#38bdf8;">Browse all OmniOperand calculators &rarr;</a></p>
      </body></html>`,
      { status: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }

  let html = await canonicalResponse.text();

  // Extract clean tool title for attribution
  const titleMatch = html.match(/<title>([^<—|]+)/i);
  const toolTitle = titleMatch ? titleMatch[1].trim() : 'Calculator';

  // 1. Strip site header, site footer, breadcrumbs, and floating search buttons
  html = html.replace(/<header\b[^>]*class="[^"]*site-header[^"]*"[^>]*>[\s\S]*?<\/header>/gi, '');
  html = html.replace(/<footer\b[^>]*class="[^"]*site-footer[^"]*"[^>]*>[\s\S]*?<\/footer>/gi, '');
  html = html.replace(/<nav\b[^>]*aria-label="breadcrumb"[^>]*>[\s\S]*?<\/nav>/gi, '');
  html = html.replace(/<div\b[^>]*class="[^"]*theme-switch[^"]*"[^>]*>[\s\S]*?<\/div>/gi, '');

  // 2. Inject auto-resize postMessage script & sticky attribution footer
  const embedEnhancements = `
<style>
  body {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .calculator-hud, .solver-hud, main {
    padding-top: 8px !important;
    padding-bottom: 8px !important;
    max-width: 100% !important;
    box-shadow: none !important;
  }
  .omni-embed-attribution {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    font-size: 11.5px;
    color: #94a3b8;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    background: rgba(15, 23, 42, 0.95);
    border-top: 1px solid rgba(56, 189, 248, 0.2);
    position: sticky;
    bottom: 0;
    z-index: 9999;
    backdrop-filter: blur(8px);
  }
  .omni-embed-attribution a {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
  }
  .omni-embed-attribution a:hover {
    text-decoration: underline;
  }
  .omni-embed-badge {
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    padding: 2px 8px;
    border-radius: 9999px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
</style>

<div class="omni-embed-attribution">
  <div>
    <span>Powered by </span>
    <a href="https://omnioperand.com/${embedPath}/" target="_blank" rel="noopener">OmniOperand &mdash; ${toolTitle}</a>
  </div>
  <a href="https://omnioperand.com/${embedPath}/" target="_blank" rel="noopener" class="omni-embed-badge">
    Open Full Tool &nearr;
  </a>
</div>

<script>
  (function() {
    function notifyParentResize() {
      if (window.parent && window.parent !== window) {
        var h = document.documentElement.scrollHeight || document.body.scrollHeight;
        window.parent.postMessage({ type: 'omni:resize', height: h }, '*');
      }
    }
    window.addEventListener('load', notifyParentResize);
    window.addEventListener('resize', notifyParentResize);
    window.addEventListener('omni:calculated', notifyParentResize);
    if (typeof MutationObserver !== 'undefined') {
      new MutationObserver(notifyParentResize).observe(document.body, { childList: true, subtree: true, attributes: true });
    }
    setTimeout(notifyParentResize, 300);
    setTimeout(notifyParentResize, 1000);
  })();
</script>
`;

  html = html.replace('</body>', `${embedEnhancements}\n</body>`);

  // Allow iframe embedding from any domain (removes X-Frame-Options blocking)
  return new Response(html, {
    status: 200,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'X-Frame-Options': 'ALLOWALL',
      'Content-Security-Policy': "frame-ancestors *",
      'Cache-Control': 'public, max-age=3600, s-maxage=86400'
    }
  });
}
