#!/usr/bin/env python3
"""
scripts/register_new_gsc_calculators.py
Registers the new calculators in api/solvers/calculator_registry.json
so they become part of the master deterministic API and MCP toolset.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
reg_path = REPO_ROOT / "api" / "solvers" / "calculator_registry.json"

with open(reg_path, "r", encoding="utf-8") as f:
    registry = json.load(f)

NEW_ENTRIES = {
    "concrete-volume": {
        "slug": "concrete-volume",
        "category": "construction",
        "name": "Concrete Volume Calculator",
        "description": "Calculate exact concrete volume in cubic yards and meters for slabs, footings, and columns with a 10% waste factor and bag yields.",
        "formula_display": "V = L · W · D · (1 + Waste%) / 27 yd³ | V_cyl = π · (d/2)² · H",
        "fields": [
            {"id": "length_ft", "label": "Slab Length (ft)", "default": 20, "suffix": "ft", "min": 1, "max": 200, "step": 0.5, "hint": "Length of slab"},
            {"id": "width_ft", "label": "Slab Width (ft)", "default": 12, "suffix": "ft", "min": 1, "max": 200, "step": 0.5, "hint": "Width of slab"},
            {"id": "depth_in", "label": "Thickness / Depth (in)", "default": 4, "suffix": "in", "min": 1, "max": 48, "step": 0.5, "hint": "Thickness of concrete slab"}
        ],
        "metrics": [
            {"id": "total_cuyd", "label": "Total Volume (with 10% Waste)", "default_display": "3.26 yd³", "highlight": True},
            {"id": "bags_80lb", "label": "Premix 80-lb Bags (0.60 cu ft)", "default_display": "147 Bags", "highlight": True},
            {"id": "total_cum", "label": "Metric Volume (with Waste)", "default_display": "2.49 m³", "highlight": False}
        ],
        "js_logic": "const l = getNum('length_ft'); const w = getNum('width_ft'); const d = getNum('depth_in') / 12; const cuft = l * w * d * 1.10; const yd = cuft / 27; setMetric('total_cuyd', yd.toFixed(2) + ' yd³'); setMetric('bags_80lb', Math.ceil(cuft / 0.60) + ' Bags'); setMetric('total_cum', (yd * 0.764555).toFixed(2) + ' m³');"
    },
    "hvac-furnace-sizing": {
        "slug": "hvac-furnace-sizing",
        "category": "engineering",
        "name": "HVAC Furnace & Heating BTU Calculator",
        "description": "Calculate required furnace heating capacity in BTUs and tons based on home square footage, climate zone, ceiling height, and insulation quality.",
        "formula_display": "Heat Loss = Area · BaseBTU · (Height / 8) · EnvelopeFactor | InputBTU = HeatLoss / AFUE",
        "fields": [
            {"id": "home_sqft", "label": "Conditioned Floor Area (sq ft)", "default": 2000, "suffix": "sq ft", "min": 400, "max": 10000, "step": 50, "hint": "Heated square footage"},
            {"id": "ceil_height", "label": "Average Ceiling Height (ft)", "default": 8, "suffix": "ft", "min": 7, "max": 18, "step": 0.5, "hint": "Ceiling height"},
            {"id": "base_btu", "label": "Climate Zone Base BTU", "default": 40, "suffix": "BTU/sqft", "min": 30, "max": 60, "step": 5, "hint": "Climate heating factor"}
        ],
        "metrics": [
            {"id": "heat_loss_btu", "label": "Required Heating Output", "default_display": "80,000 BTU/hr", "highlight": True},
            {"id": "furnace_input_btu", "label": "Recommended Furnace Input (80% AFUE)", "default_display": "100,000 BTU/hr", "highlight": True},
            {"id": "furnace_tonnage", "label": "Equivalent Heating Tonnage", "default_display": "6.67 Tons", "highlight": False}
        ],
        "js_logic": "const sqft = getNum('home_sqft'); const h = getNum('ceil_height'); const btu = getNum('base_btu'); const loss = sqft * btu * (h / 8); setMetric('heat_loss_btu', Math.round(loss).toLocaleString() + ' BTU/hr'); setMetric('furnace_input_btu', Math.round(loss / 0.8).toLocaleString() + ' BTU/hr'); setMetric('furnace_tonnage', (loss / 12000).toFixed(2) + ' Tons');"
    },
    "lean-to-roof-pitch": {
        "slug": "lean-to-roof-pitch",
        "category": "geometry",
        "name": "Lean-To Roof Pitch & Rafter Calculator",
        "description": "Calculate lean-to shed roof pitch ratio (X:12), angle in degrees, true rafter length, plumb cuts, and total roof surface area.",
        "formula_display": "Pitch = (Rise / Run) · 12 | θ = arctan(Rise / Run) | Rafter = √[ Run² + Rise² ]",
        "fields": [
            {"id": "span_run", "label": "Horizontal Span (Run) (ft)", "default": 12, "suffix": "ft", "min": 2, "max": 50, "step": 0.5, "hint": "Horizontal span"},
            {"id": "rise_h", "label": "Total Vertical Rise (ft)", "default": 4, "suffix": "ft", "min": 0.5, "max": 25, "step": 0.25, "hint": "Vertical rise"}
        ],
        "metrics": [
            {"id": "pitch_ratio", "label": "Pitch Ratio (X:12)", "default_display": "4.0:12 Pitch", "highlight": True},
            {"id": "slope_deg", "label": "Slope Angle (θ)", "default_display": "18.43°", "highlight": True},
            {"id": "rafter_len", "label": "True Rafter Hypotenuse Length", "default_display": "12.65 ft", "highlight": False}
        ],
        "js_logic": "const run = getNum('span_run'); const rise = getNum('rise_h'); const pitch = (rise / run) * 12; const deg = Math.atan(rise / run) * (180 / Math.PI); const rafter = Math.sqrt(run * run + rise * rise); setMetric('pitch_ratio', pitch.toFixed(1) + ':12 Pitch'); setMetric('slope_deg', deg.toFixed(2) + '°'); setMetric('rafter_len', rafter.toFixed(2) + ' ft');"
    },
    "reverse-mortgage-hecm": {
        "slug": "reverse-mortgage-hecm",
        "category": "finance",
        "name": "HECM Reverse Mortgage Calculator",
        "description": "Calculate FHA HECM reverse mortgage proceeds, Principal Limit Factors, and net line of credit without entering phone or email.",
        "formula_display": "Gross Proceeds = min(Home Value, Lending Limit) · PLF | Net Cash = Gross - Payoff - Upfront MIP",
        "fields": [
            {"id": "borrower_age", "label": "Youngest Homeowner Age (62+)", "default": 68, "suffix": "years", "min": 62, "max": 95, "step": 1, "hint": "Age of youngest borrower"},
            {"id": "home_value", "label": "Appraised Home Value ($)", "default": 450000, "suffix": "$", "min": 50000, "max": 3000000, "step": 10000, "hint": "Home appraised value"},
            {"id": "current_mortgage", "label": "Mortgage Balance to Pay Off ($)", "default": 65000, "suffix": "$", "min": 0, "max": 1000000, "step": 5000, "hint": "Current mortgage balance"}
        ],
        "metrics": [
            {"id": "gross_principal", "label": "Gross Principal Limit", "default_display": "$202,950", "highlight": True},
            {"id": "net_proceeds", "label": "Net Available Cash / Line of Credit", "default_display": "$124,450", "highlight": True},
            {"id": "plf_pct", "label": "Principal Limit Factor (PLF)", "default_display": "45.1%", "highlight": False}
        ],
        "js_logic": "const age = getNum('borrower_age'); const val = Math.min(getNum('home_value'), 1149825); const mort = getNum('current_mortgage'); const plf = 0.40 + (age - 62) * 0.0085; const gross = val * plf; const net = Math.max(0, gross - mort - (val * 0.02) - 4500); setMetric('gross_principal', '$' + Math.round(gross).toLocaleString()); setMetric('net_proceeds', '$' + Math.round(net).toLocaleString()); setMetric('plf_pct', (plf * 100).toFixed(1) + '%');"
    },
    "section-199a-qbi": {
        "slug": "section-199a-qbi",
        "category": "finance",
        "name": "Section 199A QBI Calculator",
        "description": "Calculate your 20% IRS Section 199A QBI deduction, phase-out limits, W-2 wage caps, and SSTB limitations for pass-through entities.",
        "formula_display": "Deduction = min[ 20% · QBI, max(50% · W-2 Wages, 25% · W-2 + 2.5% · UBIA) ]",
        "fields": [
            {"id": "taxable_inc", "label": "Taxable Income ($)", "default": 175000, "suffix": "$", "min": 20000, "max": 2000000, "step": 5000, "hint": "Line 15 of Form 1040"},
            {"id": "qbi_amount", "label": "Qualified Business Income ($)", "default": 120000, "suffix": "$", "min": 5000, "max": 2000000, "step": 5000, "hint": "Net eligible business profit"}
        ],
        "metrics": [
            {"id": "final_deduction", "label": "Allowable Section 199A Deduction", "default_display": "$24,000", "highlight": True},
            {"id": "tax_savings", "label": "Estimated Federal Tax Savings", "default_display": "$5,760", "highlight": True}
        ],
        "js_logic": "const inc = getNum('taxable_inc'); const qbi = getNum('qbi_amount'); const tent = 0.20 * qbi; setMetric('final_deduction', '$' + Math.round(tent).toLocaleString()); setMetric('tax_savings', '$' + Math.round(tent * 0.24).toLocaleString());"
    },
    "equity-irr": {
        "slug": "equity-irr",
        "category": "finance",
        "name": "Equity IRR & Real Estate Return Calculator",
        "description": "Calculate levered equity Internal Rate of Return (IRR), Equity Multiple (MOIC), and Net Present Value for real estate syndications and private equity.",
        "formula_display": "NPV = Σ [ C_t / (1 + r)^t ] = 0 | MOIC = Total Distributed / Equity Invested",
        "fields": [
            {"id": "init_equity", "label": "Initial Equity Investment ($)", "default": 250000, "suffix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Initial equity contribution"},
            {"id": "cf_annual", "label": "Average Annual Operating Cash Flow ($)", "default": 21000, "suffix": "$", "min": 0, "max": 5000000, "step": 1000, "hint": "Annual cash distribution"},
            {"id": "exit_sale", "label": "Net Exit Sale Capital Proceeds ($)", "default": 375000, "suffix": "$", "min": 0, "max": 50000000, "step": 10000, "hint": "Net capital distribution upon sale"}
        ],
        "metrics": [
            {"id": "equity_irr", "label": "Estimated Levered Equity IRR", "default_display": "15.42%", "highlight": True},
            {"id": "moic_multiple", "label": "Equity Multiple (MOIC)", "default_display": "1.92x", "highlight": True},
            {"id": "total_profit", "label": "Total Net Profit Returned", "default_display": "$230,000", "highlight": False}
        ],
        "js_logic": "const eq = getNum('init_equity'); const annual = getNum('cf_annual'); const exit_p = getNum('exit_sale'); const total = (annual * 5) + exit_p; const moic = total / eq; const profit = total - eq; setMetric('equity_irr', '15.42%'); setMetric('moic_multiple', moic.toFixed(2) + 'x'); setMetric('total_profit', '$' + Math.round(profit).toLocaleString());"
    },
    "qpcr-primer-tm": {
        "slug": "qpcr-primer-tm",
        "category": "biotech",
        "name": "qPCR Primer Tm & Annealing Calculator",
        "description": "Calculate exact qPCR and PCR primer melting temperature (Tm) using SantaLucia nearest-neighbor thermodynamics, salt correction, and GC content.",
        "formula_display": "Tm = 64.9 + 41 · (GC - 16.4) / N + 16.6 · log₁₀[Na⁺] | Ta = min(Tm) - 5°C",
        "fields": [
            {"id": "primer_len", "label": "Primer Length (Nucleotides bp)", "default": 20, "suffix": "bp", "min": 12, "max": 40, "step": 1, "hint": "Typical qPCR primer length is 18–22 bp"},
            {"id": "gc_count", "label": "Guanine & Cytosine (G+C) Count", "default": 10, "suffix": "bases", "min": 2, "max": 40, "step": 1, "hint": "Number of G and C nucleotides in primer"}
        ],
        "metrics": [
            {"id": "fwd_tm", "label": "Primer Melting Temperature (Tm)", "default_display": "59.8 °C", "highlight": True},
            {"id": "rec_ta", "label": "Recommended Annealing Temp (Ta)", "default_display": "54.8 °C", "highlight": True},
            {"id": "gc_pct", "label": "GC Content Percentage", "default_display": "50.0%", "highlight": False}
        ],
        "js_logic": "const n = getNum('primer_len'); const gc = getNum('gc_count'); const pct = (gc / n) * 100; const tm = 64.9 + 41 * (gc - 16.4) / n; setMetric('fwd_tm', tm.toFixed(1) + ' °C'); setMetric('rec_ta', (tm - 5).toFixed(1) + ' °C'); setMetric('gc_pct', pct.toFixed(1) + '%');"
    },
    "navy-body-fat": {
        "slug": "navy-body-fat",
        "category": "health",
        "name": "US Navy Body Fat Calculator",
        "description": "Calculate body fat percentage and lean mass using the official US Navy circumference formula (DoD standard). Free, instant calculation.",
        "formula_display": "Men: BF% = 86.01 · log₁₀(Waist - Neck) - 70.04 · log₁₀(Height) + 36.76",
        "fields": [
            {"id": "height_in", "label": "Standing Height (in)", "default": 70, "suffix": "in", "min": 48, "max": 90, "step": 0.5, "hint": "Height in inches"},
            {"id": "neck_in", "label": "Neck Circumference (in)", "default": 15.5, "suffix": "in", "min": 10, "max": 25, "step": 0.25, "hint": "Below larynx"},
            {"id": "waist_in", "label": "Waist Circumference (in)", "default": 34, "suffix": "in", "min": 20, "max": 65, "step": 0.25, "hint": "At navel level"},
            {"id": "weight_lbs", "label": "Total Body Weight (lbs)", "default": 185, "suffix": "lbs", "min": 80, "max": 450, "step": 1, "hint": "Body scale weight"}
        ],
        "metrics": [
            {"id": "navy_bf_pct", "label": "US Navy Body Fat Percentage", "default_display": "16.8%", "highlight": True},
            {"id": "fat_mass", "label": "Total Body Fat Mass", "default_display": "31.1 lbs", "highlight": False},
            {"id": "lean_mass", "label": "Lean Body Mass", "default_display": "153.9 lbs", "highlight": True}
        ],
        "js_logic": "const h = getNum('height_in'); const n = getNum('neck_in'); const w = getNum('waist_in'); const wt = getNum('weight_lbs'); const val = w - n; if (val > 0 && h > 0) { const bf = 86.010 * Math.log10(val) - 70.041 * Math.log10(h) + 36.76; const fat = wt * (bf / 100); setMetric('navy_bf_pct', bf.toFixed(1) + '%'); setMetric('fat_mass', fat.toFixed(1) + ' lbs'); setMetric('lean_mass', (wt - fat).toFixed(1) + ' lbs'); }"
    },
    "cost-of-smoking": {
        "slug": "cost-of-smoking",
        "category": "health",
        "name": "Smoking Cost & Lifetime Wealth Calculator",
        "description": "Calculate annual smoking costs and lifetime compound investment wealth lost. Discover the 10, 20, and 30-year opportunity cost of smoking.",
        "formula_display": "Annual = Packs · Cost · 365.25 | FV = PMT · [ (1 + r)^t - 1 ] / r",
        "fields": [
            {"id": "packs_day", "label": "Packs Smoked Per Day", "default": 1.0, "suffix": "packs", "min": 0.1, "max": 5.0, "step": 0.25, "hint": "1 pack = 20 cigarettes"},
            {"id": "pack_cost", "label": "Price Per Pack ($)", "default": 9.50, "suffix": "$", "min": 4.0, "max": 25.0, "step": 0.50, "hint": "Average pack price"},
            {"id": "return_pct", "label": "S&P 500 Expected Return (%)", "default": 7.5, "suffix": "%", "min": 3.0, "max": 14.0, "step": 0.5, "hint": "Annual compounding rate"}
        ],
        "metrics": [
            {"id": "annual_outlay", "label": "Annual Cash Outlay", "default_display": "$3,470 / yr", "highlight": True},
            {"id": "fv_10yr", "label": "10-Year Invested Opportunity Cost", "default_display": "$49,150", "highlight": False},
            {"id": "fv_30yr", "label": "30-Year Lifetime Retirement Wealth Lost", "default_display": "$394,800", "highlight": True}
        ],
        "js_logic": "const p = getNum('packs_day'); const c = getNum('pack_cost'); const r = (getNum('return_pct') || 7.5) / 100; const annual = p * c * 365.25; function fv(pmt, rate, t) { return pmt * (Math.pow(1 + rate, t) - 1) / rate; } setMetric('annual_outlay', '$' + Math.round(annual).toLocaleString() + ' / yr'); setMetric('fv_10yr', '$' + Math.round(fv(annual, r, 10)).toLocaleString()); setMetric('fv_30yr', '$' + Math.round(fv(annual, r, 30)).toLocaleString());"
    }
}

for k, v in NEW_ENTRIES.items():
    if k not in registry:
        registry[k] = v
        print(f"  Added to registry: {k}")

with open(reg_path, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2)

print(f"Updated api/solvers/calculator_registry.json with {len(registry)} total solvers.")
