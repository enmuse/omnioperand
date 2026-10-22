/**
 * functions/api/restoration-scope.js
 * Cloudflare Pages Function: POST /api/restoration-scope
 * Deterministic Insurance Disaster Restoration & Claim Supplement Auditor
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

    const peril = String(body.damage_peril || "tree_strike_structural");
    const area = parseFloat(body.affected_area_sqft) || 1800;
    const carrierOffer = parseFloat(body.carrier_initial_scope_usd) || 18500;
    const caliper = parseFloat(body.tree_caliper_inches) || 32;

    let directCost = 0;
    let lineItems = [];

    if (peril === 'tree_strike_structural') {
      const craneCost = 2800;
      const treeRemoval = 1200 + (caliper * 65);
      const shoringTarp = Math.max(1500, area * 0.40 * 12.50);
      const framingTruss = (Math.sqrt(area) * 2) * 95;
      const deckingUnderlay = area * 0.40 * 4.20;
      const metalRoofing = area * 0.40 * 15.00;
      const interiorCeiling = area * 0.35 * 7.50;

      directCost = craneCost + treeRemoval + shoringTarp + framingTruss + deckingUnderlay + metalRoofing + interiorCeiling;

      lineItems = [
        { item: "100-Ton Heavy Crane Mobilization & Rigging", cost_usd: craneCost },
        { item: "Tree Extraction & Sectioning (" + caliper + "-inch caliper)", cost_usd: Math.round(treeRemoval) },
        { item: "Emergency Structural Shoring & Weatherproof Tarping", cost_usd: Math.round(shoringTarp) },
        { item: "Engineered Truss / Rafter Structural Replacement", cost_usd: Math.round(framingTruss) },
        { item: "24-Ga Commercial Standing Seam Metal Roof & CDX Decking", cost_usd: Math.round(metalRoofing + deckingUnderlay) },
        { item: "Interior Ceiling Sheetrock, Thermal Insulation & Paint", cost_usd: Math.round(interiorCeiling) }
      ];
    } else if (peril === 'flash_flood_crawlspace') {
      const cat3Extraction = area * 0.95;
      const mudMucking = area * 2.40;
      const vaporBarrier = area * 1.25;
      const antimicrobialFog = area * 0.75;
      const dehumRent = 3 * 5 * 185;
      const ductwork = (Math.sqrt(area) * 2.5) * 45;
      const insulationBatt = area * 2.60;
      const frenchDrain = (Math.sqrt(area) * 2) * 42;

      directCost = cat3Extraction + mudMucking + vaporBarrier + antimicrobialFog + dehumRent + ductwork + insulationBatt + frenchDrain;

      lineItems = [
        { item: "Cat 3 Black Water Extraction & Manual Mud Mucking", cost_usd: Math.round(cat3Extraction + mudMucking) },
        { item: "Contaminated Subfloor Batt Insulation & Vapor Barrier Tear-Out", cost_usd: Math.round(vaporBarrier + insulationBatt) },
        { item: "Antimicrobial Biocidal Fogging & HEPA Scrubbing", cost_usd: Math.round(antimicrobialFog) },
        { item: "Industrial LGR Commercial Dehumidifiers (3 units x 5 days)", cost_usd: dehumRent },
        { item: "Submerged R-8 Flexible HVAC Ductwork Replacement", cost_usd: Math.round(ductwork) },
        { item: "Interior Perimeter French Drain with Submersible Sump Pump", cost_usd: Math.round(frenchDrain) }
      ];
    } else if (peril === 'slope_failure_landslide') {
      const massExcavation = area * 1.5 * 28;
      const wallReplacement = (Math.sqrt(area) * 1.5 * 8) * 85;
      const foundationUnderpinning = (Math.sqrt(area) * 1.2) * 175;
      const drainageSwale = 6500;

      directCost = massExcavation + wallReplacement + foundationUnderpinning + drainageSwale;
      lineItems = [
        { item: "Mass Landslide Mud & Debris Excavation", cost_usd: Math.round(massExcavation) },
        { item: "Engineered Segmental Retaining Wall Reconstruction", cost_usd: Math.round(wallReplacement) },
        { item: "Helical Pier Foundation Underpinning & Stabilization", cost_usd: Math.round(foundationUnderpinning) },
        { item: "Engineered Mountain Drainage Swales & Geotextile", cost_usd: drainageSwale }
      ];
    } else {
      const tearOff = area * 3.50;
      const substrateRepair = area * 2.20;
      const newStandingSeam = area * 15.00;
      const interiorRepairs = area * 0.25 * 18.00;

      directCost = tearOff + substrateRepair + newStandingSeam + interiorRepairs;
      lineItems = [
        { item: "Metal Roof Tear-Off & Substrate Decking Preparation", cost_usd: Math.round(tearOff + substrateRepair) },
        { item: "24-Gauge Standing Seam Architectural Metal Installation", cost_usd: Math.round(newStandingSeam) },
        { item: "Interior Water Penetration Mitigation & Drywall Repairs", cost_usd: Math.round(interiorRepairs) }
      ];
    }

    // Mandatory 10/10 Overhead & Profit (21% compounded)
    const overhead = directCost * 0.10;
    const profit = (directCost + overhead) * 0.10;
    const totalOp = overhead + profit;
    const trueCost = Math.round(directCost + totalOp);

    const variance = Math.max(0, trueCost - carrierOffer);
    const variancePct = carrierOffer > 0 ? Math.round(((variance / carrierOffer) * 100) * 10) / 10 : 0;

    return new Response(JSON.stringify({
      success: true,
      tool: "insurance_disaster_restoration",
      damage_peril: peril,
      affected_area_sqft: area,
      carrier_initial_scope_usd: carrierOffer,
      true_structural_restoration_cost_usd: trueCost,
      direct_remediation_scope_usd: Math.round(directCost),
      mandatory_overhead_and_profit: {
        overhead_10pct_usd: Math.round(overhead),
        profit_10pct_compounded_usd: Math.round(profit),
        total_op_usd: Math.round(totalOp),
        legal_doctrine: "Gilderman v. State Farm mandatory multi-trade general contractor O&P"
      },
      carrier_underpayment_variance_usd: Math.round(variance),
      variance_percentage: variancePct,
      xactimate_proof_of_loss_line_items: lineItems,
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
