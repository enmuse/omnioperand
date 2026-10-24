#!/usr/bin/env python3
"""
scripts/register_authority_solvers.py — Registers the 4 new financial authority calculators in calculator_registry.json
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REG_PATH = REPO_ROOT / "api" / "solvers" / "calculator_registry.json"

NEW_SOLVERS = {
    "islamic-diminishing-musharaka": {
        "slug": "islamic-diminishing-musharaka",
        "category": "finance",
        "name": "Diminishing Musharaka Calculator (AAOIFI Standard No. 12)",
        "description": "Calculate Shariah-compliant co-ownership financing with rental rates and progressive equity buyouts.",
        "formula_display": "M = P · [r(1+r)ⁿ] / [(1+r)ⁿ - 1], R_t = P_t · (r/12), E_t = M - R_t",
        "fields": [
            {"id": "home_price", "label": "Property Purchase Price ($)", "default": 400000, "suffix": "$", "min": 50000, "max": 10000000, "step": 5000, "hint": "Agreed acquisition cost"},
            {"id": "down_payment_pct", "label": "Client Initial Equity (%)", "default": 20, "suffix": "%", "min": 5, "max": 90, "step": 1, "hint": "Initial customer share"},
            {"id": "profit_rate", "label": "Agreed Annual Rental Rate (%)", "default": 6.5, "suffix": "%", "min": 1, "max": 20, "step": 0.125, "hint": "Rental rate index"},
            {"id": "financing_term", "label": "Financing Term (Years)", "default": 30, "suffix": "years", "min": 5, "max": 40, "step": 5, "hint": "Duration of contract"}
        ],
        "metrics": [
            {"id": "monthly_installment", "label": "Total Monthly Installment", "default_display": "$2,022.62", "highlight": True},
            {"id": "m1_rental", "label": "Month 1 Rental Payment", "default_display": "$1,733.33", "highlight": True},
            {"id": "m1_equity", "label": "Month 1 Equity Buyout", "default_display": "$289.29", "highlight": True},
            {"id": "total_profit_paid", "label": "Total Cumulative Rent Paid", "default_display": "$408,143", "highlight": True}
        ],
        "js_logic": "const price = getNum('home_price'); const downPct = getNum('down_payment_pct') / 100; const bankEquity = price * (1 - downPct); const r = (getNum('profit_rate') / 100) / 12; const n = getNum('financing_term') * 12; const factor = Math.pow(1 + r, n); const m = bankEquity * (r * factor) / (factor - 1); setMetric('monthly_installment', '$' + m.toFixed(2)); setMetric('m1_rental', '$' + (bankEquity * r).toFixed(2)); setMetric('m1_equity', '$' + (m - bankEquity * r).toFixed(2)); setMetric('total_profit_paid', '$' + Math.round(m * n - bankEquity).toLocaleString());"
    },
    "islamic-murabaha": {
        "slug": "islamic-murabaha",
        "category": "finance",
        "name": "Murabaha Cost-Plus Financing Calculator (AAOIFI Standard No. 8)",
        "description": "Calculate Shariah-compliant Murabaha cost-plus deferred sale financing with transparent fixed mark-up.",
        "formula_display": "Total Price = Financed Amount · (1 + Profit Margin %)",
        "fields": [
            {"id": "purchase_price", "label": "Asset Acquisition Cost ($)", "default": 300000, "suffix": "$", "min": 10000, "max": 10000000, "step": 5000, "hint": "Cost price paid to supplier"},
            {"id": "down_payment", "label": "Customer Deposit ($)", "default": 60000, "suffix": "$", "min": 0, "max": 5000000, "step": 5000, "hint": "Upfront commitment"},
            {"id": "profit_margin", "label": "Agreed Profit Mark-Up (%)", "default": 25, "suffix": "%", "min": 1, "max": 100, "step": 1, "hint": "Total profit markup"},
            {"id": "term_years", "label": "Financing Term (Years)", "default": 15, "suffix": "years", "min": 1, "max": 30, "step": 1, "hint": "Deferred installment term"}
        ],
        "metrics": [
            {"id": "monthly_installment", "label": "Fixed Monthly Installment", "default_display": "$1,666.67", "highlight": True},
            {"id": "total_sale_price", "label": "Total Murabaha Sale Price", "default_display": "$300,000", "highlight": True},
            {"id": "fixed_profit", "label": "Agreed Fixed Profit Margin", "default_display": "$60,000", "highlight": True}
        ],
        "js_logic": "const cost = getNum('purchase_price'); const down = getNum('down_payment'); const financed = cost - down; const profit = financed * (getNum('profit_margin') / 100); const total = financed + profit; const m = total / (getNum('term_years') * 12); setMetric('monthly_installment', '$' + m.toFixed(2)); setMetric('total_sale_price', '$' + Math.round(total).toLocaleString()); setMetric('fixed_profit', '$' + Math.round(profit).toLocaleString());"
    },
    "islamic-ijara": {
        "slug": "islamic-ijara",
        "category": "finance",
        "name": "Ijara Lease-to-Own Financing Calculator (AAOIFI Standard No. 9)",
        "description": "Calculate Shariah-compliant lease-to-own (Ijara Muntahiya Bittamleek) financing with independent gift title transfer.",
        "formula_display": "Monthly Rent = P_net · [r(1+r)ⁿ] / [(1+r)ⁿ - 1]",
        "fields": [
            {"id": "property_value", "label": "Property Valuation ($)", "default": 400000, "suffix": "$", "min": 50000, "max": 10000000, "step": 5000, "hint": "Property market value"},
            {"id": "security_deposit", "label": "Security Deposit ($)", "default": 80000, "suffix": "$", "min": 10000, "max": 5000000, "step": 5000, "hint": "Client upfront security capital"},
            {"id": "lease_rate", "label": "Annual Lease Benchmark (%)", "default": 6.25, "suffix": "%", "min": 1, "max": 20, "step": 0.05, "hint": "Annual lease index"},
            {"id": "lease_years", "label": "Lease Term (Years)", "default": 30, "suffix": "years", "min": 5, "max": 40, "step": 5, "hint": "Lease-to-own duration"}
        ],
        "metrics": [
            {"id": "monthly_payment", "label": "Monthly Rent + Buyout", "default_display": "$1,970.36", "highlight": True},
            {"id": "net_investment", "label": "Financier Net Investment", "default_display": "$320,000", "highlight": True},
            {"id": "total_lease_profit", "label": "Total Cumulative Lease Rental", "default_display": "$389,330", "highlight": True}
        ],
        "js_logic": "const val = getNum('property_value'); const dep = getNum('security_deposit'); const net = val - dep; const r = (getNum('lease_rate') / 100) / 12; const n = getNum('lease_years') * 12; const factor = Math.pow(1 + r, n); const m = net * (r * factor) / (factor - 1); setMetric('monthly_payment', '$' + m.toFixed(2)); setMetric('net_investment', '$' + Math.round(net).toLocaleString()); setMetric('total_lease_profit', '$' + Math.round(m * n - net).toLocaleString());"
    },
    "itin-mortgage": {
        "slug": "itin-mortgage",
        "category": "finance",
        "name": "ITIN Immigrant Home Mortgage Calculator",
        "description": "Calculate ITIN home loans for Non-Permanent Resident Aliens under Fannie Mae DU & IRS Notice 2026-ITIN standards.",
        "formula_display": "P&I = Loan · [r(1+r)ⁿ] / [(1+r)ⁿ - 1], Reserves = 6 · PITI",
        "fields": [
            {"id": "home_price", "label": "Home Purchase Price ($)", "default": 350000, "suffix": "$", "min": 50000, "max": 10000000, "step": 5000, "hint": "Purchase contract price"},
            {"id": "down_payment_pct", "label": "Down Payment (%)", "default": 15, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Typically 15% to 20%"},
            {"id": "interest_rate", "label": "Mortgage Interest Rate (%)", "default": 7.75, "suffix": "%", "min": 3, "max": 15, "step": 0.125, "hint": "Non-QM ITIN rate tier"},
            {"id": "term_years", "label": "Loan Term (Years)", "default": 30, "suffix": "years", "min": 10, "max": 30, "step": 5, "hint": "Amortization term"}
        ],
        "metrics": [
            {"id": "monthly_pi", "label": "Monthly Principal & Interest", "default_display": "$2,132.88", "highlight": True},
            {"id": "total_monthly_piti", "label": "Estimated Total Monthly PITI", "default_display": "$2,614.13", "highlight": True},
            {"id": "reserves_required", "label": "Required Post-Closing Reserves", "default_display": "$15,685", "highlight": True}
        ],
        "js_logic": "const price = getNum('home_price'); const down = price * (getNum('down_payment_pct') / 100); const loan = price - down; const r = (getNum('interest_rate') / 100) / 12; const n = getNum('term_years') * 12; const factor = Math.pow(1 + r, n); const pi = loan * (r * factor) / (factor - 1); const piti = pi + (price * 0.0125 / 12) + (1400 / 12); const reserves = piti * (getNum('down_payment_pct') < 20 ? 6 : 3); setMetric('monthly_pi', '$' + pi.toFixed(2)); setMetric('total_monthly_piti', '$' + piti.toFixed(2)); setMetric('reserves_required', '$' + Math.round(reserves).toLocaleString());"
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

    with open(REG_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print(f"✅ Registered {added} new financial authority calculators. Total solvers in registry: {len(registry)}")

if __name__ == "__main__":
    main()
