/**
 * functions/api/nec-load.js
 * Cloudflare Pages Function: POST /api/nec-load
 * Deterministic NEC Article 220.82 Residential Service Load Calculation Engine
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

    const sqft = parseFloat(body.home_sqft) || 2800;
    const circuits = parseInt(body.small_appliance_circuits) || 3;
    const hvac = String(body.hvac_type || "heat_pump_10kw");
    const evKw = parseFloat(body.ev_charger_kw) || 9.6;
    const waterType = String(body.water_heater_type || "tank_4500");

    const hasRange = body.has_range !== false && body.has_range !== "false";
    const hasDryer = body.has_dryer !== false && body.has_dryer !== "false";
    const hasHotTub = body.has_hottub === true || body.has_hottub === "true";
    const hasWellPump = body.has_wellpump !== false && body.has_wellpump !== "false";

    // 1. General Lighting: 3 VA/sqft per NEC 220.12
    const generalLightingVa = sqft * 3;

    // 2. Small Appliance & Laundry: 1,500 VA each per NEC 220.52
    const smallApplianceVa = circuits * 1500;

    // 3. Appliances
    const rangeVa = hasRange ? 8000 : 0;
    const dryerVa = hasDryer ? 5000 : 0;
    const hotTubVa = hasHotTub ? 5500 : 0;
    const wellPumpVa = hasWellPump ? 2500 : 0;

    let waterVa = 4500;
    if (waterType === 'hybrid_heatpump') waterVa = 1200;
    else if (waterType === 'tankless_18kw') waterVa = 18000;
    else if (waterType === 'tankless_27kw') waterVa = 27000;
    else if (waterType === 'gas_tankless') waterVa = 300;

    const subtotalGeneral = generalLightingVa + smallApplianceVa + rangeVa + dryerVa + hotTubVa + wellPumpVa + waterVa;

    // Derating per NEC 220.82(B)
    const first10k = Math.min(subtotalGeneral, 10000);
    const remainder = Math.max(0, subtotalGeneral - 10000);
    const deratedRemainder = remainder * 0.40;
    const netGeneralVa = first10k + deratedRemainder;

    // 4. EV Continuous Load at 125% per NEC 625
    const evVa = evKw * 1000 * 1.25;

    // 5. HVAC Load per NEC 220.82(C)
    let hvacVa = 0;
    if (hvac === 'heat_pump_10kw') {
      hvacVa = 4320 + (10000 * 0.65);
    } else if (hvac === 'heat_pump_15kw') {
      hvacVa = 4320 + (15000 * 0.65);
    } else if (hvac === 'heat_pump_5kw') {
      hvacVa = 4320 + (5000 * 0.65);
    } else if (hvac === 'electric_furnace_15kw') {
      hvacVa = 15000 * 0.65;
    } else if (hvac === 'ac_gas_heat') {
      hvacVa = 5000;
    }

    const totalVa = Math.round(netGeneralVa + evVa + hvacVa);
    const totalAmps = Math.round((totalVa / 240) * 10) / 10;

    let serviceRating = 200;
    let cuGauge = "2/0 AWG Cu";
    let alGauge = "4/0 AWG Al";

    if (totalAmps <= 100) {
      serviceRating = 100;
      cuGauge = "#4 AWG Cu";
      alGauge = "#2 AWG Al";
    } else if (totalAmps <= 150) {
      serviceRating = 150;
      cuGauge = "#1 AWG Cu";
      alGauge = "2/0 AWG Al";
    } else if (totalAmps <= 200) {
      serviceRating = 200;
      cuGauge = "2/0 AWG Cu";
      alGauge = "4/0 AWG Al";
    } else if (totalAmps <= 300) {
      serviceRating = 300;
      cuGauge = "350 kcmil Cu";
      alGauge = "500 kcmil Al";
    } else {
      serviceRating = 400;
      cuGauge = "Parallel 3/0 AWG Cu (x2)";
      alGauge = "Parallel 250 kcmil Al (x2)";
    }

    return new Response(JSON.stringify({
      success: true,
      tool: "nec_220_residential_load",
      home_sqft: sqft,
      calculated_demand_va: totalVa,
      calculated_demand_amps: totalAmps,
      recommended_service_rating_amps: serviceRating,
      minimum_conductors_75c: {
        copper: cuGauge,
        aluminum: alGauge
      },
      derating_breakdown: {
        raw_general_load_va: subtotalGeneral,
        first_10000_va_at_100pct: first10k,
        remainder_va_at_40pct: Math.round(deratedRemainder),
        net_general_load_va: Math.round(netGeneralVa),
        ev_continuous_load_va: Math.round(evVa),
        hvac_calculated_load_va: Math.round(hvacVa)
      },
      statutory_references: [
        "NEC Article 220.82 (Optional Calculation - Dwelling Unit)",
        "NEC Article 625.42 (Electric Vehicle Branch Circuits 125% Continuous Duty)",
        "NEC Table 310.16 (Allowable Ampacities of Insulated Conductors @ 75°C)"
      ],
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
