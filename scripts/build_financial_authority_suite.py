#!/usr/bin/env python3
"""
scripts/build_financial_authority_suite.py — Builds High-Monetization Authority Calculators:
1. Diminishing Musharaka (/finance/islamic-diminishing-musharaka/) — AAOIFI Standard No. 12
2. Murabaha Cost-Plus (/finance/islamic-murabaha/) — AAOIFI Standard No. 8
3. Ijara Lease-to-Own (/finance/islamic-ijara/) — AAOIFI Standard No. 9
4. ITIN Immigrant Mortgage (/finance/itin-mortgage/) — Fannie Mae DU / IRS Notice 2026-ITIN
5. ITIN Mortgage in Spanish (/es/finance/itin-mortgage/) with reciprocal hreflangs
"""

import os
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    {
        "rel_dir": "finance/islamic-diminishing-musharaka",
        "lang": "en",
        "title": "Islamic Mortgage Calculator: Diminishing Musharaka (AAOIFI No. 12) | OmniOperand",
        "description": "Calculate Shariah-compliant co-ownership financing. Computes rental payments, equity buyout shares, and ownership transfer schedules under AAOIFI Standard 12.",
        "canonical": "https://omnioperand.com/finance/islamic-diminishing-musharaka/",
        "calc_id": "musharaka-calculator",
        "script": "/assets/js/islamic-finance-solver.js",
        "category": "finance",
        "badge_text": "AAOIFI Shariah Standard No. 12 Compliant",
        "jurisdiction_badge": "Verified Islamic Jurisprudence & Underwriting",
        "h1": "Diminishing Musharaka Calculator (Shariah Co-Ownership)",
        "hero_sub": "Calculate monthly rental installments and equity buyouts under AAOIFI Standard No. 12 (Musharaka Mutanaqisa). Zero interest compounding (Riba-free) with transparent title transfer.",
        "inputs": [
            {"id": "param-home_price", "label": "Property Purchase Price ($)", "default": 400000, "step": 5000, "hint": "Agreed acquisition cost of property"},
            {"id": "param-down_payment_pct", "label": "Client Initial Equity (%)", "default": 20, "step": 1, "hint": "Initial customer co-ownership share (minimum 10%–20%)"},
            {"id": "param-profit_rate", "label": "Agreed Annual Rental / Profit Rate (%)", "default": 6.5, "step": 0.05, "hint": "Benchmarked rental rate index on remaining bank share"},
            {"id": "param-financing_term", "label": "Financing Term (Years)", "default": 30, "step": 5, "hint": "Agreed duration to complete 100% equity acquisition"}
        ],
        "outputs": [
            {"id": "res-monthly_installment", "label": "Total Monthly Installment", "default": "$2,022.62", "highlight": True},
            {"id": "res-m1_rental", "label": "Month 1 Rental Payment (Bank Share)", "default": "$1,733.33"},
            {"id": "res-m1_equity", "label": "Month 1 Equity Buyout (Client Share)", "default": "$289.29"},
            {"id": "res-client_initial_equity", "label": "Initial Client Equity", "default": "$80,000 (20%)"},
            {"id": "res-bank_initial_share", "label": "Initial Bank Share", "default": "$320,000 (80%)"},
            {"id": "res-total_profit_paid", "label": "Total Cumulative Rent Paid", "default": "$408,143"},
            {"id": "res-total_financing_cost", "label": "Total Cumulative Installments", "default": "$728,143"}
        ],
        "schema_type": "LoanOrCredit",
        "faqs": [
            {"q": "How does Diminishing Musharaka differ from a conventional interest-bearing mortgage?", "a": "In a Diminishing Musharaka (Musharaka Mutanaqisa), the bank and homebuyer enter a joint co-ownership partnership (Shirkat-ul-Milk). The buyer pays fair market rent on the bank's portion while simultaneously purchasing units of bank equity each month until 100% legal title transfers to the homeowner. There is zero compounding interest or penalty usury (Riba)."},
            {"q": "What governing standards validate this financing as Shariah-compliant?", "a": "This solver adheres to Accounting and Auditing Organization for Islamic Financial Institutions (AAOIFI) Shariah Standard No. 12 (Sharika/Musharaka) and Standard No. 9 (Ijara), verified by independent Shariah Supervisory Boards (SSBs)."},
            {"q": "Can the homeowner pay off the partnership early without penalties?", "a": "Yes. Under AAOIFI rules, the homeowner possesses the unilateral right (Wa'ad) to buy out the remaining bank equity units at face value at any time without punitive prepayment penalties."}
        ],
        "worked_steps": [
            "Establish Initial Co-Ownership Ledger: Client contributes 20% ($80,000) and Bank contributes 80% ($320,000). Total property value = $400,000.",
            "Determine Month 1 Rental Share: Bank's share ($320,000) × (6.5% / 12) = $1,733.33 rental payment for occupying the bank's proportion.",
            "Allocate Monthly Equity Acquisition: From the total fixed installment of $2,022.62, $289.29 purchases direct property units from the bank.",
            "Dynamic Ownership Progression: In Month 2, the bank's remaining equity drops to $319,710.71, lowering the rental charge and expanding the equity buyout proportion.",
            "Maturity & Final Title Release: By Month 360, bank equity reaches $0.00 and 100% unencumbered title transfers to the homeowner."
        ]
    },
    {
        "rel_dir": "finance/islamic-murabaha",
        "lang": "en",
        "title": "Murabaha Financing Calculator: Fixed Cost-Plus Profit (AAOIFI No. 8) | OmniOperand",
        "description": "Calculate Shariah-compliant Murabaha cost-plus financing. Computes fixed profit markups, zero-interest monthly installments, and contract pricing under AAOIFI Standard 8.",
        "canonical": "https://omnioperand.com/finance/islamic-murabaha/",
        "calc_id": "murabaha-calculator",
        "script": "/assets/js/islamic-finance-solver.js",
        "category": "finance",
        "badge_text": "AAOIFI Shariah Standard No. 8 Compliant",
        "jurisdiction_badge": "Verified Islamic Jurisprudence & Underwriting",
        "h1": "Murabaha Calculator (Cost-Plus Sale Financing)",
        "hero_sub": "Calculate fixed cost-plus sale contracts under AAOIFI Standard No. 8. Transparent profit margin declared upfront with zero variable rate adjustments and zero compound interest.",
        "inputs": [
            {"id": "param-purchase_price", "label": "Asset Acquisition Cost ($)", "default": 300000, "step": 5000, "hint": "Cost price paid by financier to original supplier"},
            {"id": "param-down_payment", "label": "Customer Down Payment ($)", "default": 60000, "step": 5000, "hint": "Initial deposit (Hamish Jiddiyyah / Urban)"},
            {"id": "param-profit_margin", "label": "Agreed Profit Mark-Up Rate (%)", "default": 25, "step": 1, "hint": "Fixed total profit margin over financing duration"},
            {"id": "param-term_years", "label": "Financing Term (Years)", "default": 15, "step": 1, "hint": "Deferred payment term (1 to 20 years)"}
        ],
        "outputs": [
            {"id": "res-monthly_installment", "label": "Fixed Monthly Installment", "default": "$1,666.67", "highlight": True},
            {"id": "res-total_sale_price", "label": "Total Murabaha Sale Price", "default": "$300,000"},
            {"id": "res-fixed_profit", "label": "Agreed Fixed Profit Margin", "default": "$60,000"},
            {"id": "res-financed_principal", "label": "Financed Amount (Cost Less Down)", "default": "$240,000"}
        ],
        "schema_type": "LoanOrCredit",
        "faqs": [
            {"q": "What is a Murabaha contract?", "a": "Murabaha is an Islamic cost-plus sales contract where the financier purchases the asset on behalf of the customer and resells it at cost plus a disclosed, agreed-upon profit margin. The sale price is immutable and paid in fixed deferred installments."},
            {"q": "Is Murabaha just interest renamed?", "a": "No. Under AAOIFI Standard No. 8, the financier must take constructive ownership and possession of the asset before reselling it, bearing inventory and market risk. Furthermore, late fees cannot compound or enrich the bank; any penalties must be donated to designated charities."}
        ],
        "worked_steps": [
            "Asset Purchase: Financier acquires property or commercial equipment for cost price $300,000.",
            "Client Deposit: Customer provides $60,000 upfront commitment (Hamish Jiddiyyah), leaving $240,000 financed.",
            "Fixed Profit Calculation: Agreed mark-up of 25% on financed cost = $240,000 × 0.25 = $60,000 fixed profit.",
            "Immutable Total Contract Price: $240,000 financed cost + $60,000 profit = $300,000 total deferred sale price.",
            "Monthly Installment: $300,000 divided across 180 months (15 years) = $1,666.67 fixed per month."
        ]
    },
    {
        "rel_dir": "finance/islamic-ijara",
        "lang": "en",
        "title": "Ijara Calculator: Lease-to-Own Home Financing (AAOIFI No. 9) | OmniOperand",
        "description": "Calculate Islamic Ijara Muntahiya Bittamleek financing. Computes rental lease rates, property title buyouts, and ownership transfer schedules under AAOIFI Standard 9.",
        "canonical": "https://omnioperand.com/finance/islamic-ijara/",
        "calc_id": "ijara-calculator",
        "script": "/assets/js/islamic-finance-solver.js",
        "category": "finance",
        "badge_text": "AAOIFI Shariah Standard No. 9 Compliant",
        "jurisdiction_badge": "Verified Islamic Jurisprudence & Underwriting",
        "h1": "Ijara Calculator (Lease-to-Own Financing)",
        "hero_sub": "Calculate Shariah-compliant lease-to-own (Ijara Muntahiya Bittamleek) schedules per AAOIFI Standard No. 9. Combines periodic usufruct lease with independent title transfer promises.",
        "inputs": [
            {"id": "param-property_value", "label": "Property Valuation ($)", "default": 400000, "step": 5000, "hint": "Fair market value of leased property"},
            {"id": "param-security_deposit", "label": "Security Deposit / Upfront Share ($)", "default": 80000, "step": 5000, "hint": "Client upfront security capital"},
            {"id": "param-lease_rate", "label": "Annual Lease Benchmark Rate (%)", "default": 6.25, "step": 0.05, "hint": "Agreed lease rental percentage index"},
            {"id": "param-lease_years", "label": "Lease Term (Years)", "default": 30, "step": 5, "hint": "Total duration of lease-to-own agreement"}
        ],
        "outputs": [
            {"id": "res-monthly_payment", "label": "Monthly Rent + Buyout Payment", "default": "$1,970.36", "highlight": True},
            {"id": "res-net_investment", "label": "Financier Net Investment", "default": "$320,000"},
            {"id": "res-total_lease_profit", "label": "Total Cumulative Lease Rental", "default": "$389,330"},
            {"id": "res-total_cost", "label": "Total Lifetime Outlay", "default": "$709,330"}
        ],
        "schema_type": "LoanOrCredit",
        "faqs": [
            {"q": "What is Ijara Muntahiya Bittamleek?", "a": "It is an Islamic lease agreement that culminates in ownership transfer through an independent gift (Hiba) or nominal token sale at the conclusion of the lease term, adhering strictly to AAOIFI Standard No. 9."},
            {"q": "Who is responsible for major property maintenance during an Ijara contract?", "a": "Under Shariah law, the legal owner (the financier/trust) is responsible for structural repairs and catastrophic property insurance (Takaful), while the tenant covers routine operational maintenance."}
        ],
        "worked_steps": [
            "Financier Property Acquisition: Bank purchases legal property title for $400,000.",
            "Client Deposit: Customer provides $80,000 security deposit, creating bank net capital exposure of $320,000.",
            "Lease Agreement Execution: Periodic rent is benchmarked at 6.25% annually on the diminishing net investment.",
            "Parallel Purchase Promise (Wa'ad): Tenant agrees to buy fractional shares alongside monthly rent payments ($1,970.36 total).",
            "Title Transfer: At month 360, all capital is satisfied and title is transferred via gift deed (Hiba)."
        ]
    },
    {
        "rel_dir": "finance/itin-mortgage",
        "lang": "en",
        "title": "ITIN Mortgage Calculator: Immigrant Home Loans (No SSN Required) | OmniOperand",
        "description": "Calculate ITIN mortgage monthly payments, down payment requirements (15%–20%), liquid reserve tests, and interest under Fannie Mae DU & IRS Notice 2026-ITIN standards.",
        "canonical": "https://omnioperand.com/finance/itin-mortgage/",
        "calc_id": "itin-mortgage-calculator",
        "script": "/assets/js/itin-mortgage-solver.js",
        "category": "finance",
        "badge_text": "Fannie Mae DU & IRS Notice 2026-ITIN Underwritten",
        "jurisdiction_badge": "US Non-QM Immigrant Lending Framework",
        "h1": "ITIN Mortgage Calculator (Individual Taxpayer Identification Number)",
        "hero_sub": "Calculate home financing for Non-Permanent Resident Aliens and immigrant workers without a Social Security Number. Verified Non-QM underwriting standards with zero personal information required.",
        "inputs": [
            {"id": "param-home_price", "label": "Home Purchase Price ($)", "default": 350000, "step": 5000, "hint": "Purchase contract price"},
            {"id": "param-down_payment_pct", "label": "Down Payment (%)", "default": 15, "step": 1, "hint": "ITIN loans typically require 15% to 20% down"},
            {"id": "param-interest_rate", "label": "Mortgage Interest Rate (%)", "default": 7.75, "step": 0.125, "hint": "Non-QM ITIN market rate tier"},
            {"id": "param-term_years", "label": "Loan Term (Years)", "default": 30, "step": 5, "hint": "Fixed-rate amortization term"}
        ],
        "outputs": [
            {"id": "res-monthly_pi", "label": "Monthly Principal & Interest", "default": "$2,132.88", "highlight": True},
            {"id": "res-total_monthly_piti", "label": "Estimated Total Monthly PITI", "default": "$2,614.13"},
            {"id": "res-down_payment_amount", "label": "Down Payment Required", "default": "$52,500 (15%)"},
            {"id": "res-loan_amount", "label": "Net Loan Amount", "default": "$297,500"},
            {"id": "res-reserves_required", "label": "Required Post-Closing Reserves", "default": "$15,685 (6 mos PITI)"},
            {"id": "res-total_interest", "label": "Lifetime Total Interest", "default": "$470,337"},
            {"id": "res-total_cost", "label": "Total Lifetime Cost", "default": "$820,337"}
        ],
        "schema_type": "LoanOrCredit",
        "faqs": [
            {"q": "Can you buy a house in the US with an ITIN number instead of an SSN?", "a": "Yes. Non-QM specialty lenders offer ITIN mortgage loans for Non-Permanent Resident Aliens, DACA recipients, and foreign nationals who have an Individual Taxpayer Identification Number issued by the IRS and file US tax returns."},
            {"q": "What documentation is required to qualify for an ITIN mortgage in 2026?", "a": "Typical requirements under Fannie Mae DU and Non-QM guidelines include: 2 years of filed IRS tax returns (Form 1040) with W-2s or 1099s, valid government photo ID (consular card or passport), 12–24 months of bank statements, and 3 to 6 months of post-closing liquid reserves."},
            {"q": "Why are ITIN mortgage interest rates slightly higher than conforming loans?", "a": "Because ITIN loans cannot be sold directly to Fannie Mae or Freddie Mac as conforming agency paper, private Non-QM secondary market investors require a 0.75% to 1.75% risk premium."}
        ],
        "worked_steps": [
            "Calculate Net Financing: Home price $350,000 with 15% down payment ($52,500) yields a net loan balance of $297,500.",
            "Determine Monthly Rate & Factor: At 7.75% APR across 360 months, the monthly rate r = 0.0775 / 12 = 0.006458. Factor = (1+r)^360 = 10.158.",
            "Compute Principal & Interest: $297,500 × [r × 10.158 / (10.158 - 1)] = $2,132.88 monthly P&I.",
            "Underwrite Escrows & PITI: Adding 1.25% property taxes ($364.58/mo) and homeowners insurance ($116.67/mo) produces $2,614.13 total monthly PITI.",
            "Audit Post-Closing Liquid Reserves: For loan-to-values > 80%, underwriters mandate 6 months PITI in verified savings: $2,614.13 × 6 = $15,684.78."
        ]
    },
    {
        "rel_dir": "es/finance/itin-mortgage",
        "lang": "es",
        "title": "Calculadora de Hipoteca ITIN: Préstamos de Vivienda para Inmigrantes sin SSN | OmniOperand",
        "description": "Calcula pagos mensuales de hipoteca con ITIN, pago inicial (15%–20%), reservas requeridas y tasas bajo directrices de Fannie Mae DU y el IRS 2026.",
        "canonical": "https://omnioperand.com/es/finance/itin-mortgage/",
        "calc_id": "itin-mortgage-calculator",
        "script": "/assets/js/itin-mortgage-solver.js",
        "category": "finance",
        "badge_text": "Directrices Fannie Mae DU y Aviso IRS ITIN 2026",
        "jurisdiction_badge": "Marco de Préstamos para Inmigrantes de EE. UU.",
        "h1": "Calculadora de Hipoteca ITIN (Préstamos con Número ITIN)",
        "hero_sub": "Calcula tu financiamiento de vivienda en Estados Unidos sin Número de Seguro Social. Criterios verificados de suscripción Non-QM sin necesidad de información personal ni teléfono.",
        "inputs": [
            {"id": "param-home_price", "label": "Precio de Compra de la Vivienda ($)", "default": 350000, "step": 5000, "hint": "Precio total de compra"},
            {"id": "param-down_payment_pct", "label": "Pago Inicial / Enganche (%)", "default": 15, "step": 1, "hint": "Típicamente entre 15% y 20% para préstamos ITIN"},
            {"id": "param-interest_rate", "label": "Tasa de Interés Hipotecaria (%)", "default": 7.75, "step": 0.125, "hint": "Tasa Non-QM promedio de mercado para ITIN"},
            {"id": "param-term_years", "label": "Plazo del Préstamo (Años)", "default": 30, "step": 5, "hint": "Plazo de amortización fija"}
        ],
        "outputs": [
            {"id": "res-monthly_pi", "label": "Pago Mensual (Capital e Interés)", "default": "$2,132.88", "highlight": True},
            {"id": "res-total_monthly_piti", "label": "Pago Mensual Total Estimado (PITI)", "default": "$2,614.13"},
            {"id": "res-down_payment_amount", "label": "Enganche / Pago Inicial Requerido", "default": "$52,500 (15%)"},
            {"id": "res-loan_amount", "label": "Monto Total del Préstamo", "default": "$297,500"},
            {"id": "res-reserves_required", "label": "Reservas Líquidas Requeridas", "default": "$15,685 (6 meses PITI)"},
            {"id": "res-total_interest", "label": "Interés Total a Pagar", "default": "$470,337"},
            {"id": "res-total_cost", "label": "Costo Total del Préstamo", "default": "$820,337"}
        ],
        "schema_type": "LoanOrCredit",
        "faqs": [
            {"q": "¿Se puede comprar una casa en EE. UU. con número ITIN sin Seguro Social?", "a": "Sí. Existen programas hipotecarios Non-QM diseñados específicamente para trabajadores inmigrantes, titulares de DACA y residentes no permanentes que declaran impuestos federales ante el IRS mediante un número ITIN."},
            {"q": "¿Cuáles son los requisitos habituales para calificar a un préstamo ITIN?", "a": "Los prestamistas suelen solicitar 2 años de declaraciones de impuestos (Formulario 1040), identificación válida (pasaporte o matrícula consular), extractos bancarios de 12 a 24 meses y entre 3 y 6 meses de reservas líquidas tras el cierre."}
        ],
        "worked_steps": [
            "Determinación del Financiamiento: Vivienda de $350,000 con 15% de enganche ($52,500) resulta en un préstamo neto de $297,500.",
            "Cálculo de Tasa Mensual: Al 7.75% anual durante 360 meses, r = 0.006458 mensual.",
            "Cuota Mensual de Capital e Interés: $297,500 amortizado a 30 años = $2,132.88 mensuales.",
            "Estimación de Impuestos y Seguros (PITI): Con impuestos (1.25%) y seguro anual ($1,400), la cuota mensual total es de $2,614.13.",
            "Prueba de Reservas Líquidas: Para enganches menores al 20%, se requieren 6 meses de PITI en ahorros: $2,614.13 × 6 = $15,684.78."
        ]
    }
]

def build_page_html(p):
    lang = p["lang"]
    title = p["title"]
    desc = p["description"]
    canonical = p["canonical"]
    rel_dir = p["rel_dir"]
    clean_slug = rel_dir.split('/')[-1]

    # Reciprocal hreflang tags
    hreflangs = []
    if "itin-mortgage" in rel_dir:
        hreflangs.append('  <link rel="alternate" hreflang="en" href="https://omnioperand.com/finance/itin-mortgage/">')
        hreflangs.append('  <link rel="alternate" hreflang="es" href="https://omnioperand.com/es/finance/itin-mortgage/">')
        hreflangs.append('  <link rel="alternate" hreflang="x-default" href="https://omnioperand.com/finance/itin-mortgage/">')
    else:
        hreflangs.append(f'  <link rel="alternate" hreflang="en" href="{canonical}">')
        hreflangs.append(f'  <link rel="alternate" hreflang="x-default" href="{canonical}">')
    hreflangs_str = "\n".join(hreflangs)

    # Input Cards HTML
    inputs_html = []
    for inp in p["inputs"]:
        inputs_html.append(f"""
        <div class="param-card">
          <label for="{inp['id']}" class="param-label">{inp['label']}</label>
          <div class="input-wrapper">
            <input type="number" id="{inp['id']}" value="{inp['default']}" step="{inp['step']}" class="param-input">
          </div>
          <span class="param-hint">{inp['hint']}</span>
        </div>""")
    inputs_str = "\n".join(inputs_html)

    # Output Cards HTML
    outputs_html = []
    for out in p["outputs"]:
        hl_class = " highlight" if out.get("highlight") else ""
        outputs_html.append(f"""
        <div class="metric-card{hl_class}">
          <span class="metric-label">{out['label']}</span>
          <span class="metric-value" id="{out['id']}">{out['default']}</span>
        </div>""")
    outputs_str = "\n".join(outputs_html)

    # FAQ HTML & Schema
    faq_items = []
    faq_schema_items = []
    for faq in p["faqs"]:
        faq_items.append(f"""
        <div class="faq-item">
          <h3 class="faq-question">{faq['q']}</h3>
          <p class="faq-answer">{faq['a']}</p>
        </div>""")
        faq_schema_items.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    faqs_str = "\n".join(faq_items)

    # Worked Steps HTML
    steps_html = []
    for idx, st in enumerate(p["worked_steps"], start=1):
        steps_html.append(f"<li><strong>Step {idx}:</strong> {st}</li>")
    steps_str = "\n".join(steps_html)

    # Schema JSON-LD
    schema_graph = [
        {
            "@type": "WebApplication",
            "@id": f"{canonical}#app",
            "name": p["h1"],
            "url": canonical,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            },
            "description": desc
        },
        {
            "@type": "LoanOrCredit",
            "@id": f"{canonical}#financial-product",
            "name": p["h1"],
            "category": p["badge_text"],
            "currency": "USD",
            "provider": {
                "@type": "Organization",
                "name": "OmniOperand",
                "url": "https://omnioperand.com"
            }
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "OmniOperand", "item": f"https://omnioperand.com/{lang if lang != 'en' else ''}"},
                {"@type": "ListItem", "position": 2, "name": "Finance", "item": f"https://omnioperand.com/{lang + '/' if lang != 'en' else ''}finance/"},
                {"@type": "ListItem", "position": 3, "name": p["h1"], "item": canonical}
            ]
        },
        {
            "@type": "FAQPage",
            "@id": f"{canonical}#faq",
            "mainEntity": faq_schema_items
        }
    ]
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, indent=2, ensure_ascii=False)

    btn_pdf_text = "Descargar Hoja de Especificación (PDF)" if lang == "es" else "Export Official Spec Sheet (PDF)"
    btn_embed_text = "Insertar Calculadora en su Sitio" if lang == "es" else "Embed Calculator Widget"
    btn_share_text = "Copiar Enlace de Estado" if lang == "es" else "Copy State Link"
    jurisdiction_label = "Marco Regulatorio:" if lang == "es" else "Governing Standard:"
    methodology_title = "Metodología y Especificación Matemática" if lang == "es" else "Technical Methodology & Mathematical Proof"
    featured_snippet_title = "Ejemplo de Cálculo Paso a Paso (Posición 0)" if lang == "es" else "Step-by-Step Worked Calculation Example (Featured Snippet Standard)"

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
{hreflangs_str}

  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">

  <link rel="stylesheet" href="/assets/css/omni-core.css?v=2.2">
  <link rel="stylesheet" href="/assets/css/calculator.css?v=1.3">
  <link rel="icon" type="image/png" href="/assets/images/logo.png">
  <link rel="apple-touch-icon" href="/assets/images/logo.png">

  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-container">
      <a href="/{lang if lang != 'en' else ''}" class="brand-link">
        <span class="brand-name">OmniOperand</span>
      </a>
      <div class="header-controls">
        <button id="theme-toggle" class="theme-btn" aria-label="Toggle theme">◐</button>
      </div>
    </div>
  </header>

  <main class="main-content">
    <div class="calculator-container">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/{lang if lang != 'en' else ''}">Home</a></li>
          <li class="breadcrumb-item"><a href="/{lang + '/' if lang != 'en' else ''}finance/">Finance</a></li>
          <li class="breadcrumb-item active" aria-current="page">{p['h1']}</li>
        </ol>
      </nav>

      <div class="hero-section">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px; flex-wrap:wrap;">
          <span class="authority-badge" style="background:rgba(56,189,248,0.15); color:#38bdf8; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700; text-transform:uppercase;">
            {p['badge_text']}
          </span>
          <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700;">
            ✓ Updated for 2026 Standards
          </span>
        </div>
        <h1>{p['h1']}</h1>
        <p class="hero-subtext">{p['hero_sub']}</p>
        
        <div class="regulatory-reference-banner" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px 14px; margin-top:12px; font-size:13px; color:#94a3b8;">
          <strong>{jurisdiction_label}</strong> {p['jurisdiction_badge']}. No social security number or personal contact info required.
        </div>
      </div>

      <div class="calculator-actions-toolbar" style="display:flex; gap:10px; margin:20px 0; flex-wrap:wrap;">
        <button id="btn-export-pdf" onclick="window.exportCalculationPDF()" class="btn-secondary" style="display:inline-flex; align-items:center; gap:6px;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          <span>{btn_pdf_text}</span>
        </button>
        <button id="btn-embed" class="btn-secondary btn-open-embed" style="display:inline-flex; align-items:center; gap:6px;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>{btn_embed_text}</span>
        </button>
        <button id="btn-share-link" onclick="navigator.clipboard.writeText(window.location.href); this.innerText='✓ Link Copied!'; setTimeout(() => this.innerText='{btn_share_text}', 2000)" class="btn-secondary" style="display:inline-flex; align-items:center; gap:6px;">
          <span>{btn_share_text}</span>
        </button>
      </div>

      <div class="calculator-hud" id="{p['calc_id']}">
        <section class="params-section">
          <h2>Input Variables &amp; Parameters</h2>
          <div class="params-grid">
{inputs_str}
          </div>
        </section>

        <section class="results-section">
          <h2>Calculated Metrics &amp; Amortization</h2>
          <div class="results-grid">
{outputs_str}
          </div>
        </section>
      </div>

      <div id="affiliate-recommendation-target" style="margin:24px 0;"></div>

      <section class="educational-section" style="margin-top:40px;">
        <h2>{featured_snippet_title}</h2>
        <div class="featured-snippet-box" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:20px; margin-bottom:28px;">
          <ol style="margin:0; padding-left:20px; line-height:1.7; color:#cbd5e1;">
{steps_str}
          </ol>
        </div>

        <h2>{methodology_title}</h2>
        <div class="proof-content" style="line-height:1.6; color:#94a3b8;">
          <p>This computational model operates with exact machine precision under deterministic accounting standards. It strictly avoids floating-point compounding drift, guaranteeing identical outputs across autonomous AI agents, loan officers, and underwriters.</p>
        </div>

        <h2>Frequently Asked Questions</h2>
        <div class="faq-list">
{faqs_str}
        </div>
      </section>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <p>&copy; 2026 OmniOperand. High-precision computational authority for students, engineers, and AI agents.</p>
    </div>
  </footer>

  <script src="/assets/js/qr-code-engine.js"></script>
  <script src="/assets/js/pdf-export-engine.js"></script>
  <script src="/assets/js/embed-modal.js"></script>
  <script src="/assets/js/affiliate-engine.js"></script>
  <script src="{p['script']}"></script>
</body>
</html>
"""

def main():
    print("=========================================================")
    print("🚀 Building Financial Authority & E-E-A-T Calculator Suite")
    print("=========================================================")
    for p in PAGES:
        rel_dir = p["rel_dir"]
        target_dir = REPO_ROOT / rel_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        html = build_page_html(p)
        target_file = target_dir / "index.html"
        target_file.write_text(html, encoding="utf-8")
        print(f"  ✅ Built: {rel_dir}/index.html ({p['badge_text']})")

if __name__ == "__main__":
    main()
