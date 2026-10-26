#!/usr/bin/env python3
"""
scripts/register_batch3_gap_solvers.py
Registers the 5 new GSC gap calculators in api/solvers/calculator_registry.json:
1. polymeric-sand
2. rafter-birdsmouth-cut
3. gutter-downspout-sizing
4. three-phase-transformer-kva
5. crypto-tax-hifo
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REG_PATH = REPO_ROOT / "api" / "solvers" / "calculator_registry.json"

NEW_SOLVERS = {
    "polymeric-sand": {
        "slug": "polymeric-sand",
        "category": "construction",
        "name": "Polymeric Sand & Paver Joint Calculator",
        "description": "Calculate exact 50lb bags of polymeric sand and cubic yards of bedding sand for pavers, patio stones, and flagstone joints compliant with ICPI standards.",
        "formula_display": "V_j = Area · [ 1 - (L · W) / ((L + W_j) · (W + W_j)) ] · (D_j / 12) | Bags = ⌈ (V_j · 100 lbs/cuft) / 50 ⌉",
        "fields": [
            {"id": "patio_area_sqft", "label": "Total Patio Area (sq ft)", "default": 300, "suffix": "sq ft", "min": 10, "max": 50000, "step": 10, "hint": "Total area to be paved"},
            {"id": "paver_length_in", "label": "Paver Length (in)", "default": 8, "suffix": "in", "min": 2, "max": 48, "step": 0.25, "hint": "Length of individual paver"},
            {"id": "paver_width_in", "label": "Paver Width (in)", "default": 4, "suffix": "in", "min": 2, "max": 48, "step": 0.25, "hint": "Width of individual paver"},
            {"id": "joint_width_in", "label": "Joint Width (in)", "default": 0.25, "suffix": "in", "min": 0.0625, "max": 2, "step": 0.0625, "hint": "Average joint width between pavers"},
            {"id": "joint_depth_in", "label": "Joint Depth (in)", "default": 2.0, "suffix": "in", "min": 0.5, "max": 6, "step": 0.125, "hint": "Depth of sand fill in joint"}
        ],
        "metrics": [
            {"id": "poly_sand_bags", "label": "50-lb Polymeric Sand Bags Needed", "default_display": "9 Bags", "highlight": True},
            {"id": "joint_volume_cuft", "label": "Total Joint Void Volume", "default_display": "4.24 cu ft", "highlight": True},
            {"id": "bedding_sand_cuyd", "label": "1-Inch Bedding Sand Base", "default_display": "1.02 cu yd", "highlight": False}
        ],
        "js_logic": "const area = getNum('patio_area_sqft'); const l = getNum('paver_length_in'); const w = getNum('paver_width_in'); const wj = getNum('joint_width_in'); const dj = getNum('joint_depth_in'); const faceSqFt = (l * w) / 144; const totalFootprint = ((l + wj) * (w + wj)) / 144; const jointRatio = 1 - (faceSqFt / totalFootprint); const cuft = area * jointRatio * (dj / 12) * 1.10; const bags = Math.ceil((cuft * 100) / 50); const bedding = ((area * (1/12)) / 27) * 1.10; setMetric('poly_sand_bags', bags + ' Bags'); setMetric('joint_volume_cuft', cuft.toFixed(2) + ' cu ft'); setMetric('bedding_sand_cuyd', bedding.toFixed(2) + ' cu yd');"
    },
    "rafter-birdsmouth-cut": {
        "slug": "rafter-birdsmouth-cut",
        "category": "construction",
        "name": "Rafter Length & Birdsmouth Cut Calculator",
        "description": "Calculate common rafter line length, plumb cut angle, birdsmouth seat cut width, heel cut depth, and overhang tail compliant with IRC R802.4.1.",
        "formula_display": "Run = (Span - Ridge) / 2 | L_line = Run · √[ 1 + (Pitch/12)² ] | HeelCut = Seat · (Pitch/12) ≤ Depth / 3",
        "fields": [
            {"id": "building_span_ft", "label": "Building Span (ft)", "default": 24, "suffix": "ft", "min": 4, "max": 100, "step": 0.5, "hint": "Out-to-out framing width"},
            {"id": "roof_pitch_in", "label": "Roof Pitch (Rise in 12)", "default": 6, "suffix": "in/12", "min": 1, "max": 24, "step": 0.5, "hint": "Pitch slope"},
            {"id": "rafter_depth_in", "label": "Rafter Depth (in)", "default": 7.25, "suffix": "in", "min": 3.5, "max": 16, "step": 0.25, "hint": "Actual timber depth (7.25 for 2x8)"},
            {"id": "wall_thickness_in", "label": "Wall Top Plate Width (in)", "default": 3.5, "suffix": "in", "min": 3.5, "max": 12, "step": 0.5, "hint": "Width of wall plate"},
            {"id": "overhang_run_in", "label": "Overhang Horizontal Run (in)", "default": 12, "suffix": "in", "min": 0, "max": 60, "step": 1, "hint": "Eave overhang past wall"}
        ],
        "metrics": [
            {"id": "line_rafter_length", "label": "Rafter Line Length", "default_display": "13.35 ft", "highlight": True},
            {"id": "pitch_angle_deg", "label": "Plumb Cut Angle", "default_display": "26.57°", "highlight": True},
            {"id": "heel_cut_depth", "label": "Birdsmouth Heel Cut", "default_display": "1.75 in (Safe)", "highlight": True}
        ],
        "js_logic": "const span = getNum('building_span_ft'); const pitch = getNum('roof_pitch_in'); const depth = getNum('rafter_depth_in'); const wall = getNum('wall_thickness_in'); const run = (span - (1.5 / 12)) / 2; const factor = Math.sqrt(1 + Math.pow(pitch / 12, 2)); const lineLen = run * factor; const deg = Math.atan(pitch / 12) * (180 / Math.PI); const heel = wall * (pitch / 12); const maxHeel = depth / 3; setMetric('line_rafter_length', lineLen.toFixed(2) + ' ft'); setMetric('pitch_angle_deg', deg.toFixed(2) + '°'); setMetric('heel_cut_depth', heel.toFixed(2) + ' in' + (heel <= maxHeel ? ' (Safe)' : ' (Exceeds 1/3)'));"
    },
    "gutter-downspout-sizing": {
        "slug": "gutter-downspout-sizing",
        "category": "construction",
        "name": "Gutter & Downspout Sizing Calculator",
        "description": "Calculate roof runoff flow rate (GPM), effective drainage area, gutter sizing (5\" or 6\"), and downspout capacity under SMACNA and IPC 1106 standards.",
        "formula_display": "A_eff = (L · W) · Factor_B | Q = A_eff · I · 0.01039 GPM | A_ds = (A_eff / N) · (I / 100)",
        "fields": [
            {"id": "roof_length_ft", "label": "Gutter Run Length (ft)", "default": 50, "suffix": "ft", "min": 10, "max": 300, "step": 1, "hint": "Length of gutter run"},
            {"id": "roof_width_ft", "label": "Rafter Rake Width (ft)", "default": 20, "suffix": "ft", "min": 5, "max": 150, "step": 1, "hint": "Distance from ridge to gutter"},
            {"id": "rainfall_intensity_in_hr", "label": "Rainfall Intensity (in/hr)", "default": 4.0, "suffix": "in/hr", "min": 1.0, "max": 10.0, "step": 0.25, "hint": "Design rainfall intensity"},
            {"id": "downspout_count", "label": "Number of Downspouts", "default": 2, "suffix": "outlets", "min": 1, "max": 10, "step": 1, "hint": "Number of drainage outlets"}
        ],
        "metrics": [
            {"id": "design_flow_gpm", "label": "Peak Storm Runoff Flow", "default_display": "45.7 GPM", "highlight": True},
            {"id": "recommended_gutter_size", "label": "Recommended Gutter Size", "default_display": "6-Inch K-Style", "highlight": True},
            {"id": "recommended_downspout_type", "label": "Standard Downspout Recommendation", "default_display": "2x3 Rectangular", "highlight": False}
        ],
        "js_logic": "const l = getNum('roof_length_ft'); const w = getNum('roof_width_ft'); const i = getNum('rainfall_intensity_in_hr'); const n = getNum('downspout_count'); const effArea = l * w * 1.10; const q = effArea * i * 0.010389; const dsArea = (effArea / n) * (i / 100); setMetric('design_flow_gpm', q.toFixed(1) + ' GPM'); setMetric('recommended_gutter_size', q > 45 ? '6-Inch K-Style' : '5-Inch K-Style'); setMetric('recommended_downspout_type', dsArea > 5.7 ? '3x4 Rectangular' : '2x3 Rectangular');"
    },
    "three-phase-transformer-kva": {
        "slug": "three-phase-transformer-kva",
        "category": "engineering",
        "name": "3-Phase Transformer kVA & Amps Calculator",
        "description": "Calculate 3-phase transformer apparent power (kVA), primary and secondary full-load amperes (FLA), and standard rating selection compliant with NEC 450.",
        "formula_display": "kVA = kW / PF | FLA = (kVA · 1,000) / (√3 · V_LL) | S_std selected from NEC NEMA steps",
        "fields": [
            {"id": "primary_voltage_v", "label": "Primary Voltage (V)", "default": 480, "suffix": "V", "min": 120, "max": 34500, "step": 10, "hint": "Primary supply voltage"},
            {"id": "secondary_voltage_v", "label": "Secondary Voltage (V)", "default": 208, "suffix": "V", "min": 120, "max": 4800, "step": 10, "hint": "Secondary utilization voltage"},
            {"id": "load_kw", "label": "Connected Active Load (kW)", "default": 60, "suffix": "kW", "min": 1, "max": 5000, "step": 5, "hint": "Total real power"},
            {"id": "power_factor", "label": "Power Factor (cos θ)", "default": 0.85, "suffix": "PF", "min": 0.5, "max": 1.0, "step": 0.05, "hint": "Load power factor"}
        ],
        "metrics": [
            {"id": "standard_nec_kva", "label": "Standard NEC Transformer Rating", "default_display": "112.5 kVA", "highlight": True},
            {"id": "primary_fla", "label": "Primary Full-Load Amps (FLA)", "default_display": "135.3 A", "highlight": True},
            {"id": "secondary_fla", "label": "Secondary Full-Load Amps (FLA)", "default_display": "312.3 A", "highlight": True}
        ],
        "js_logic": "const v1 = getNum('primary_voltage_v'); const v2 = getNum('secondary_voltage_v'); const kw = getNum('load_kw'); const pf = getNum('power_factor') || 0.85; const designKva = (kw / pf) * 1.25; const std = [15, 30, 45, 75, 112.5, 150, 225, 300, 500, 750, 1000]; let rating = 1500; for (const s of std) { if (s >= designKva) { rating = s; break; } } const sqrt3 = Math.sqrt(3); const pri = (rating * 1000) / (sqrt3 * v1); const sec = (rating * 1000) / (sqrt3 * v2); setMetric('standard_nec_kva', rating + ' kVA'); setMetric('primary_fla', pri.toFixed(1) + ' A'); setMetric('secondary_fla', sec.toFixed(1) + ' A');"
    },
    "crypto-tax-hifo": {
        "slug": "crypto-tax-hifo",
        "category": "finance",
        "name": "Crypto Capital Gains & HIFO Tax Calculator",
        "description": "Compare HIFO, FIFO, and LIFO cost basis accounting methods for cryptocurrency disposals to minimize IRS capital gains taxes under IRS Notice 2014-21.",
        "formula_display": "Proceeds = Units · P_sale | Gain = Proceeds - CostBasis | HIFO sorts lots by max(Price)",
        "fields": [
            {"id": "disposal_amount", "label": "Crypto Units Sold", "default": 1.5, "suffix": "units", "min": 0.01, "max": 10000, "step": 0.1, "hint": "Total coins/tokens sold"},
            {"id": "sale_price_usd", "label": "Sale Price per Unit ($)", "default": 65000, "suffix": "$", "min": 1, "max": 1000000, "step": 500, "hint": "Execution sale price"},
            {"id": "highest_cost_basis", "label": "Highest Lot Cost Basis ($)", "default": 68000, "suffix": "$", "min": 1, "max": 1000000, "step": 500, "hint": "Cost of highest purchase lot"},
            {"id": "first_cost_basis", "label": "First Lot Cost Basis ($)", "default": 30000, "suffix": "$", "min": 1, "max": 1000000, "step": 500, "hint": "Cost of earliest purchase lot"}
        ],
        "metrics": [
            {"id": "tax_savings_hifo", "label": "Immediate Tax Savings with HIFO", "default_display": "$5,700 Saved", "highlight": True},
            {"id": "hifo_taxable_gain", "label": "HIFO Capital Gain / (Loss)", "default_display": "-$4,500 (Loss)", "highlight": True},
            {"id": "fifo_taxable_gain", "label": "FIFO Taxable Capital Gain", "default_display": "+$52,500 Gain", "highlight": False}
        ],
        "js_logic": "const units = getNum('disposal_amount'); const sale = getNum('sale_price_usd'); const hifoCost = getNum('highest_cost_basis'); const fifoCost = getNum('first_cost_basis'); const proceeds = units * sale; const hifoGain = proceeds - (units * hifoCost); const fifoGain = proceeds - (units * fifoCost); const savings = Math.max(0, (fifoGain - hifoGain) * 0.20); setMetric('tax_savings_hifo', '$' + Math.round(savings).toLocaleString() + ' Saved'); setMetric('hifo_taxable_gain', (hifoGain >= 0 ? '+$' : '-$') + Math.round(Math.abs(hifoGain)).toLocaleString()); setMetric('fifo_taxable_gain', (fifoGain >= 0 ? '+$' : '-$') + Math.round(Math.abs(fifoGain)).toLocaleString());"
    }
}

def main():
    with open(REG_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    added = 0
    for slug, solver_data in NEW_SOLVERS.items():
        if slug not in registry:
            registry[slug] = solver_data
            added += 1
            print(f"  ✅ Added {slug} to calculator_registry.json")
        else:
            print(f"  ℹ️ {slug} already in registry, updating definition")
            registry[slug] = solver_data

    with open(REG_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print(f"\n🎉 Finished: {added} new solvers added. Total solvers in registry: {len(registry)}")

if __name__ == "__main__":
    main()
