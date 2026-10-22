/**
 * functions/api/feasibility.js
 * Cloudflare Pages Function: POST /api/feasibility
 * Deterministic Mountain Steep-Slope & Municipal Permitting Feasibility Engine
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

    const acres = parseFloat(body.parcel_acres) || 2.5;
    const slope = parseFloat(body.slope_gradient_pct) || 28;
    const elev = parseFloat(body.elevation_ft) || 3250;
    const soil = String(body.soil_profile || "shallow_granite_ledge");
    const footprint = parseFloat(body.proposed_footprint_sqft) || 3800;

    const parcelSqft = acres * 43560;

    // 1. Steep Slope Tier & Impervious Cap
    let imperviousPct = 50;
    let slopeCategory = "Standard Mountain Review (<15%)";
    let alerts = [];
    let permits = [
      "Local Building & Zoning Plan Review",
      "NCDEQ Sedimentation & Erosion Control Plan (>1 acre disturbance)"
    ];

    if (slope >= 35) {
      imperviousPct = 15;
      slopeCategory = "Critical Steep Slope Restriction (>35%)";
      alerts.push("CRITICAL SLOPE (>35%): Mandatory geotechnical borehole analysis, global slope stability factor of safety (FS >= 1.5), and PE civil seal required. Side-cast fill prohibited.");
      permits.push("County Hillside Major Development Special Use Permit");
      permits.push("Registered Geotechnical PE Borehole & Global Stability Seal");
      permits.push("Engineered Retaining Wall Structural Drawings");
    } else if (slope >= 25) {
      imperviousPct = 30;
      slopeCategory = "Severe Steep Slope Ordinance Enforced (25%–35%)";
      alerts.push("SEVERE STEEP SLOPE: 30% maximum impervious surface cap enforced. Side-cast fill prohibited. Engineered retaining walls required.");
      permits.push("County Steep Slope Minor Review Permit");
      permits.push("Engineered Retaining Wall & Drainage Plan");
    } else if (slope >= 15) {
      imperviousPct = 40;
      slopeCategory = "Moderate Slope Review (15%–25%)";
      permits.push("Minor Slope Disturbance Review & Revegetation Plan");
    }

    const maxImperviousSqft = Math.round(parcelSqft * (imperviousPct / 100));

    // 2. Elevation / Mountain Ridge Protection
    let mrpaApplies = false;
    if (elev >= 3000) {
      mrpaApplies = true;
      alerts.push("MOUNTAIN RIDGE PROTECTION ACT (Elev >= 3,000'): 35-foot maximum structural height limit from natural grade. Clearing buffer capped at 15 feet beyond foundation perimeter. ASCE 7-22 Exposure C wind engineering mandated.");
      permits.push("NC Mountain Ridge Protection Act Compliance Certification");
    }

    // 3. Cut-and-Fill Mass Balance
    const benchWidth = Math.sqrt(footprint) * 1.25;
    const benchLength = footprint / (benchWidth * 0.8);
    const cutDepth = (benchWidth * (slope / 100) / 2) * 1.15;
    const rawCutYards = Math.round((0.5 * benchWidth * cutDepth * benchLength) / 27);
    const fillYards = Math.round(rawCutYards * 0.75 * 1.15); // 15% compaction shrink

    // 4. Retaining Wall & Cost Itemization
    let wallSqft = 0;
    let wallCostLow = 0;
    let wallCostHigh = 0;
    if (slope >= 25) {
      const wallHeight = cutDepth * 0.85;
      wallSqft = Math.round(benchLength * wallHeight);
      wallCostLow = wallSqft * 75;
      wallCostHigh = wallSqft * 105;
    }

    let rockCost = 0;
    if (slope >= 25 && soil === 'shallow_granite_ledge') {
      const rockYards = rawCutYards * 0.40;
      rockCost = Math.round(rockYards * 28 + 3500);
      alerts.push("SHALLOW BEDROCK REFUSAL: 5,000 ft-lb hydraulic rock breaker mobilization required for uphill bench excavation.");
    }

    const clearingCost = Math.round(Math.min(acres, 1.5) * 4500);
    const gradingCostLow = Math.round(rawCutYards * 22);
    const gradingCostHigh = Math.round(rawCutYards * 32);
    const drivewayCost = 14500;
    const engPermitCost = slope >= 25 ? 9500 : 4500;

    const totalLow = clearingCost + gradingCostLow + wallCostLow + rockCost + drivewayCost + engPermitCost;
    const totalHigh = Math.round(clearingCost + gradingCostHigh + wallCostHigh + (rockCost * 1.3) + (drivewayCost * 1.4) + (engPermitCost * 1.3));

    return new Response(JSON.stringify({
      success: true,
      tool: "steep_slope_feasibility",
      parcel_acres: acres,
      slope_gradient_pct: slope,
      elevation_ft: elev,
      soil_profile: soil,
      proposed_footprint_sqft: footprint,
      slope_category: slopeCategory,
      impervious_surface_cap_sqft: maxImperviousSqft,
      impervious_surface_cap_pct: imperviousPct,
      mountain_ridge_protection_act: {
        applies: mrpaApplies,
        max_structural_height_ft: 35,
        clearing_buffer_ft: 15,
        wind_exposure_category: "C"
      },
      cut_fill_mass_balance_yds: {
        cut_volume_raw: rawCutYards,
        fill_volume_compacted: fillYards,
        compaction_shrink_factor: 1.15
      },
      retaining_wall: {
        required: slope >= 25,
        wall_face_sqft: wallSqft,
        cost_range_usd: [wallCostLow, wallCostHigh]
      },
      rock_breaker_contingency_usd: rockCost,
      estimated_civil_budget_usd: {
        low: totalLow,
        high: totalHigh
      },
      mandatory_permits: permits,
      regulatory_alerts: alerts,
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
