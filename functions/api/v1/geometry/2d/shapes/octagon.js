/**
 * OmniOperand REST API — Regular Octagon 8-Variable Bidirectional Solver
 * Route: GET /api/v1/geometry/2d/shapes/octagon
 *        POST /api/v1/geometry/2d/shapes/octagon
 */

const SQRT2 = Math.SQRT2;

function roundPrec(val, prec) {
  if (typeof val !== 'number' || isNaN(val)) return 0;
  return Number(val.toFixed(prec));
}

function solveSide(driver, value) {
  if (value <= 0 || isNaN(value)) return 10.0;
  switch (driver.toLowerCase()) {
    case 'side':
    case 'a':
      return value;
    case 'area':
    case 'a_poly':
      return Math.sqrt(value / (2 * (1 + SQRT2)));
    case 'perimeter':
    case 'p':
      return value / 8;
    case 'apothem':
    case 'inradius':
    case 'r_i':
    case 'ri':
      return (2 * value) / (1 + SQRT2);
    case 'circumradius':
    case 'r':
      return (2 * value) / Math.sqrt(4 + 2 * SQRT2);
    case 'span':
    case 's':
      return value / (1 + SQRT2);
    case 'short_diagonal':
    case 'short_diag':
    case 'd_s':
    case 'ds':
      return value / Math.sqrt(2 + SQRT2);
    case 'long_diagonal':
    case 'long_diag':
    case 'd_l':
    case 'dl':
      return value / Math.sqrt(4 + 2 * SQRT2);
    default:
      return value;
  }
}

function computeOctagon(side, prec) {
  const a = side;
  const p = 8 * a;
  const r_i = (a * (1 + SQRT2)) / 2;
  const R = (a * Math.sqrt(4 + 2 * SQRT2)) / 2;
  const area = 2 * (1 + SQRT2) * a * a;
  const S = a * (1 + SQRT2);
  const d_S = a * Math.sqrt(2 + SQRT2);
  const d_L = a * Math.sqrt(4 + 2 * SQRT2);
  const corner_cut = a / SQRT2;

  return {
    shape: "Regular Octagon",
    symmetry_group: "D8 (Dihedral order 16)",
    parameters: {
      side_length_a: {
        value: roundPrec(a, prec),
        exact_radical: "a",
        symbol: "a"
      },
      area: {
        value: roundPrec(area, prec),
        exact_radical: "2(1 + √2)a²",
        multiplier_approx: 4.8284271247,
        symbol: "A"
      },
      perimeter: {
        value: roundPrec(p, prec),
        exact_radical: "8a",
        symbol: "P"
      },
      apothem_inradius: {
        value: roundPrec(r_i, prec),
        exact_radical: "[a(1 + √2)] / 2",
        multiplier_approx: 1.2071067812,
        symbol: "r_i"
      },
      circumradius: {
        value: roundPrec(R, prec),
        exact_radical: "[a√(4 + 2√2)] / 2",
        multiplier_approx: 1.3065629649,
        symbol: "R"
      },
      span_flat_to_flat: {
        value: roundPrec(S, prec),
        exact_radical: "a(1 + √2)",
        multiplier_approx: 2.4142135624,
        symbol: "S"
      },
      short_diagonal: {
        value: roundPrec(d_S, prec),
        exact_radical: "a√(2 + √2)",
        multiplier_approx: 1.847759065,
        symbol: "d_S"
      },
      long_diagonal: {
        value: roundPrec(d_L, prec),
        exact_radical: "a√(4 + 2√2)",
        multiplier_approx: 2.6131259298,
        symbol: "d_L"
      }
    },
    carpentry_and_fabrication: {
      corner_cutoff_leg: roundPrec(corner_cut, prec),
      corner_cutoff_formula: "a / √2 = [a√2] / 2",
      miter_saw_angle_deg: 22.5,
      corner_joint_angle_deg: 135.0,
      bounding_square_side: roundPrec(S, prec)
    },
    angles: {
      interior_deg: 135.0,
      exterior_deg: 45.0,
      central_deg: 45.0,
      sum_interior_deg: 1080.0
    },
    algebraic_proofs: {
      method_1_triangles: "A = 8 × (½ · a · r_i) = 2(1 + √2)a²",
      method_2_square_subtraction: "A = S² - 4(½ x²) = a²(3 + 2√2) - a² = 2(1 + √2)a²",
      method_3_span_form: "A = 2(√2 - 1)S² ≈ 0.82842712 · S²"
    }
  };
}

function handleOctagonRequest(params) {
  const driver = (params.driver || params.input || 'side').toLowerCase();
  let val = parseFloat(params.value || params.val || (driver === 'side' ? (params.side || params.a || '10') : '10'));
  if (isNaN(val) || val <= 0) val = 10;

  let prec = parseInt(params.precision || params.prec || '8', 10);
  if (isNaN(prec) || prec < 2) prec = 2;
  if (prec > 14) prec = 14;

  const units = params.units || params.unit || 'units';

  const side = solveSide(driver, val);
  const result = computeOctagon(side, prec);

  return {
    meta: {
      api_version: "v1",
      platform: "OmniOperand High-Precision Math Engine",
      canonical_url: "https://omnioperand.com/geometry/2d/shapes/octagon/",
      docs: "https://omnioperand.com/api/",
      openapi_spec: "https://omnioperand.com/api/v1/openapi.json",
      timestamp_utc: new Date().toISOString()
    },
    query: {
      driver,
      input_value: val,
      units,
      precision: prec
    },
    result
  };
}

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "public, max-age=3600, s-maxage=86400",
  "X-Robots-Tag": "all",
  "X-Powered-By": "OmniOperand Edge Compute"
};

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const params = Object.fromEntries(url.searchParams.entries());
  const responseData = handleOctagonRequest(params);

  return new Response(JSON.stringify(responseData, null, 2), {
    status: 200,
    headers: CORS_HEADERS
  });
}

export async function onRequestPost(context) {
  try {
    let body = {};
    const contentType = context.request.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      body = await context.request.json();
    } else {
      const form = await context.request.formData();
      body = Object.fromEntries(form.entries());
    }
    const responseData = handleOctagonRequest(body);
    return new Response(JSON.stringify(responseData, null, 2), {
      status: 200,
      headers: CORS_HEADERS
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: "Invalid request payload", details: err.message }, null, 2), {
      status: 400,
      headers: CORS_HEADERS
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS
  });
}
