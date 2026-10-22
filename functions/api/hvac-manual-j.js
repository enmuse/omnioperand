/**
 * functions/api/hvac-manual-j.js
 * Cloudflare Pages Function: POST /api/hvac-manual-j
 * Deterministic ACCA Manual J & Cold-Climate Inverter Heat Pump Sizing Engine
 */

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

    const sqft = parseFloat(body.conditioned_sqft) || 2400;
    const height = parseFloat(body.ceiling_height_ft) || 9;
    const grade = String(body.insulation_grade || "standard_iecc");
    const winterTemp = parseFloat(body.winter_design_temp_f) || 14;
    const windowSqft = parseFloat(body.window_sqft) || 280;

    const deltaT = 70 - winterTemp;

    let uWall = 0.065;
    let uCeil = 0.026;
    let ach = 0.35;
    let uWin = 0.30;

    if (grade === 'historic_uninsulated') {
      uWall = 0.14;
      uCeil = 0.085;
      ach = 0.65;
      uWin = 0.65;
    } else if (grade === 'high_performance_sprayfoam') {
      uWall = 0.040;
      uCeil = 0.020;
      ach = 0.18;
      uWin = 0.26;
    }

    const perimeter = Math.sqrt(sqft) * 4;
    const grossWallArea = perimeter * height;
    const netWallArea = Math.max(grossWallArea - windowSqft, grossWallArea * 0.7);
    const volume = sqft * height;
    const cfm = (volume * ach) / 60;

    const qCeil = uCeil * sqft * deltaT;
    const qWall = uWall * netWallArea * deltaT;
    const qWin = uWin * windowSqft * deltaT;
    const qInfil = 1.08 * cfm * deltaT;

    const totalHeatLoss = Math.round(qCeil + qWall + qWin + qInfil);

    const rawTonnage = totalHeatLoss / 12000;
    let recommendedTons = Math.round(rawTonnage * 2) / 2;
    if (recommendedTons < 1.5) recommendedTons = 1.5;
    if (recommendedTons > 5.0) recommendedTons = 5.0;

    const lowTempFactor = winterTemp <= 0 ? 0.70 : (winterTemp <= 15 ? 0.78 : 0.85);
    const hpOutputAtDesign = recommendedTons * 12000 * lowTempFactor;

    const deficitBtu = Math.max(0, totalHeatLoss - hpOutputAtDesign);
    const rawAuxKw = deficitBtu / 3412.14;
    let auxKw = 5;
    if (rawAuxKw > 10) auxKw = 15;
    else if (rawAuxKw > 5) auxKw = 10;
    else if (rawAuxKw <= 0) auxKw = 0;

    const balancePoint = Math.round(70 - (hpOutputAtDesign / (totalHeatLoss / deltaT)));

    return new Response(JSON.stringify({
      success: true,
      tool: "acca_manual_j_heat_loss",
      conditioned_sqft: sqft,
      winter_design_temp_f: winterTemp,
      total_design_heat_loss_btu: totalHeatLoss,
      recommended_heat_pump_tons: recommendedTons,
      auxiliary_strip_heat_kw: auxKw,
      thermal_balance_point_f: balancePoint,
      component_breakdown_btu: {
        ceiling: Math.round(qCeil),
        walls: Math.round(qWall),
        windows: Math.round(qWin),
        infiltration: Math.round(qInfil)
      },
      low_ambient_capacity_retention_pct: Math.round(lowTempFactor * 100),
      dispatch_endpoint: "/api/leads"
    }, null, 2), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    return new Response(JSON.stringify({ success: false, error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
