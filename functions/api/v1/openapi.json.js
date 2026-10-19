/**
 * OmniOperand REST API — OpenAPI 3.1.0 Endpoint
 * Route: GET /api/v1/openapi.json
 */

export async function onRequestGet(context) {
  // Fetch static openapi.json or return embedded definition
  const url = new URL(context.request.url);
  const openapiUrl = new URL('/api/v1/openapi.json', url.origin);
  
  try {
    const res = await context.env.ASSETS.fetch(openapiUrl);
    const data = await res.json();
    return new Response(JSON.stringify(data, null, 2), {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Cache-Control": "public, max-age=86400, s-maxage=604800"
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: "Failed to load openapi.json" }), {
      status: 500,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}
