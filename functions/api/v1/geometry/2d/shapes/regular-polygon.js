/**
 * OmniOperand REST API — Universal Regular n-Sided Polygon Solver
 * Route: GET /api/v1/geometry/2d/shapes/regular-polygon
 *        POST /api/v1/geometry/2d/shapes/regular-polygon
 */

const SHAPE_NAMES = {
  3: 'Equilateral Triangle',
  4: 'Square (Tetragon)',
  5: 'Regular Pentagon',
  6: 'Regular Hexagon',
  7: 'Regular Heptagon',
  8: 'Regular Octagon',
  9: 'Regular Nonagon',
  10: 'Regular Decagon',
  11: 'Regular Hendecagon',
  12: 'Regular Dodecagon',
  15: 'Regular Pentadecagon',
  16: 'Regular Hexadecagon',
  20: 'Regular Icosagon',
  24: 'Regular Icositetragon',
  50: 'Regular Pentecontagon',
  100: 'Regular Hectagon',
  1000: 'Regular Chiliagon'
};

function roundPrec(val, prec) {
  if (typeof val !== 'number' || isNaN(val)) return 0;
  return Number(val.toFixed(prec));
}

function solveSideFromDriver(driver, value, n) {
  if (value <= 0 || isNaN(value)) return 0;
  const anglePiN = Math.PI / n;
  const tanPiN = Math.tan(anglePiN);
  const sinPiN = Math.sin(anglePiN);

  switch (driver.toLowerCase()) {
    case 'side':
    case 'a':
      return value;
    case 'perimeter':
    case 'p':
      return value / n;
    case 'apothem':
    case 'inradius':
    case 'r_i':
    case 'ri':
      return 2 * value * tanPiN;
    case 'circumradius':
    case 'r':
      return 2 * value * sinPiN;
    case 'area':
    case 'a_poly':
      return Math.sqrt((4 * value * tanPiN) / n);
    case 'span':
    case 's':
      return n % 2 === 0 ? (value * tanPiN) : (2 * value * sinPiN * tanPiN) / (sinPiN + tanPiN);
    default:
      return value;
  }
}

function computeMetrics(n, side, prec) {
  const anglePiN = Math.PI / n;
  const tanPiN = Math.tan(anglePiN);
  const sinPiN = Math.sin(anglePiN);
  const cosPiN = Math.cos(anglePiN);

  const perimeter = n * side;
  const apothem = side / (2 * tanPiN);
  const circumradius = side / (2 * sinPiN);
  const area = (n * side * side) / (4 * tanPiN);
  const span = n % 2 === 0 ? 2 * apothem : circumradius + apothem;
  const totalDiagonals = (n * (n - 3)) / 2;

  const interiorAngleDeg = ((n - 2) * 180) / n;
  const exteriorAngleDeg = 360 / n;
  const centralAngleDeg = 360 / n;
  const sumInteriorAnglesDeg = (n - 2) * 180;

  // Diagonals classes
  const diagonalClasses = [];
  const maxK = Math.floor(n / 2);
  for (let k = 2; k <= maxK; k++) {
    const chordLen = 2 * circumradius * Math.sin((k * Math.PI) / n);
    diagonalClasses.push({
      skip_edges: k,
      name: k === 2 ? 'Shortest Diagonal (d₂)' : k === maxK ? (n % 2 === 0 ? 'Main Diameter (d_max)' : `Long Diagonal (d_${k})`) : `Diagonal Class d_${k}`,
      length: roundPrec(chordLen, prec),
      formula: `2R · sin(${k}π / ${n})`
    });
  }

  // Archimedean Limit Metrics
  const perimeterCircleRatio = perimeter / (2 * circumradius);
  const areaCircleRatio = area / (circumradius * circumradius);

  // Invariance check
  const actualRatio = apothem / circumradius;
  const expectedRatio = cosPiN;
  const invarianceVerified = Math.abs(actualRatio - expectedRatio) < 1e-12;

  return {
    n,
    name: SHAPE_NAMES[n] || `Regular ${n}-sided Polygon (${n}-gon)`,
    side: roundPrec(side, prec),
    perimeter: roundPrec(perimeter, prec),
    apothem: roundPrec(apothem, prec),
    circumradius: roundPrec(circumradius, prec),
    area: roundPrec(area, prec),
    span_flat_to_flat: roundPrec(span, prec),
    total_diagonals: totalDiagonals,
    diagonal_classes: diagonalClasses,
    angles: {
      interior_deg: roundPrec(interiorAngleDeg, prec),
      exterior_deg: roundPrec(exteriorAngleDeg, prec),
      central_deg: roundPrec(centralAngleDeg, prec),
      sum_interior_deg: sumInteriorAnglesDeg,
      interior_rad: roundPrec(((n - 2) * Math.PI) / n, prec)
    },
    archimedean_convergence: {
      limit_pi_approximation: roundPrec(perimeterCircleRatio, prec),
      pi_deviation_abs: roundPrec(Math.abs(Math.PI - perimeterCircleRatio), prec),
      area_convergence_ratio: roundPrec(areaCircleRatio, prec)
    },
    verification: {
      invariance: "r_i / R === cos(π / n)",
      actual_ratio: roundPrec(actualRatio, 10),
      expected_cos: roundPrec(expectedRatio, 10),
      is_valid: invarianceVerified
    }
  };
}

function handleRequest(params) {
  let n = parseInt(params.n || params.sides || '8', 10);
  if (isNaN(n) || n < 3) n = 3;
  if (n > 1000) n = 1000;

  const driver = (params.driver || params.input || 'side').toLowerCase();
  let val = parseFloat(params.value || params.val || (driver === 'side' ? (params.side || params.a || '10') : '10'));
  if (isNaN(val) || val <= 0) val = 10;

  let prec = parseInt(params.precision || params.prec || '8', 10);
  if (isNaN(prec) || prec < 2) prec = 2;
  if (prec > 14) prec = 14;

  const units = params.units || params.unit || 'units';

  const side = solveSideFromDriver(driver, val, n);
  const metrics = computeMetrics(n, side, prec);

  return {
    meta: {
      api_version: "v1",
      platform: "OmniOperand High-Precision Math Engine",
      canonical_url: `https://omnioperand.com/geometry/2d/shapes/regular-polygon/?n=${n}`,
      docs: "https://omnioperand.com/api/",
      openapi_spec: "https://omnioperand.com/api/v1/openapi.json",
      timestamp_utc: new Date().toISOString()
    },
    query: {
      n,
      driver,
      input_value: val,
      units,
      precision: prec
    },
    result: metrics
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
  const responseData = handleRequest(params);

  return new Response(JSON.stringify(responseData, null, 2), {
    status: 200,
    headers: CORS_HEADERS
  });
}

export const onRequestHead = onRequestGet;

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
    const responseData = handleRequest(body);
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
