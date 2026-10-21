"""
scripts/calculator_data.py
Aggregated repository of 423 commercial-grade, high-profit calculators.
Categories: finance, construction, health, geometry, physics, calculus, statistics,
energy, logistics, crypto, legal, agriculture, engineering, ecommerce, biotech.
"""

from data_finance import FINANCE_CALCULATORS
from data_finance_2 import FINANCE_CALCULATORS_2
from data_construction import CONSTRUCTION_CALCULATORS
from data_health import HEALTH_CALCULATORS
from data_stem import STEM_CALCULATORS
from data_b2b_saas import B2B_SAAS_CALCULATORS
from data_automotive import AUTOMOTIVE_CALCULATORS
from data_real_estate_pro import REAL_ESTATE_PRO_CALCULATORS
from data_tax_payroll import TAX_PAYROLL_CALCULATORS

# New expansion modules (205 calculators)
from data_energy_solar import ENERGY_CALCULATORS
from data_logistics_freight import LOGISTICS_CALCULATORS
from data_crypto_fintech import CRYPTO_CALCULATORS
from data_legal_insurance import LEGAL_CALCULATORS
from data_agriculture_farming import AGRICULTURE_CALCULATORS
from data_engineering_civil import ENGINEERING_CALCULATORS
from data_ecommerce_retail import ECOMMERCE_CALCULATORS
from data_biotech_pharma import BIOTECH_CALCULATORS

CALCULATORS_DATA = (
    FINANCE_CALCULATORS
    + FINANCE_CALCULATORS_2
    + CONSTRUCTION_CALCULATORS
    + HEALTH_CALCULATORS
    + STEM_CALCULATORS
    + B2B_SAAS_CALCULATORS
    + AUTOMOTIVE_CALCULATORS
    + REAL_ESTATE_PRO_CALCULATORS
    + TAX_PAYROLL_CALCULATORS
    + ENERGY_CALCULATORS
    + LOGISTICS_CALCULATORS
    + CRYPTO_CALCULATORS
    + LEGAL_CALCULATORS
    + AGRICULTURE_CALCULATORS
    + ENGINEERING_CALCULATORS
    + ECOMMERCE_CALCULATORS
    + BIOTECH_CALCULATORS
)

HUB_DATA = {
    "finance": {
        "title": "Quantitative Finance & Lending Hub",
        "description": "Calculators for mortgages, debt refinancing, HELOCs, real estate underwriting, tax liabilities, and compound interest models.",
        "badge": "Domain Hub • Quantitative Finance",
        "icon": "💵"
    },
    "construction": {
        "title": "Construction & Trades Engineering Hub",
        "description": "High-precision solvers for concrete volumes, framing, aggregate tonnage, roofing squares, HVAC thermal loads, and electrical circuits.",
        "badge": "Domain Hub • Construction & Trades",
        "icon": "🏗️"
    },
    "health": {
        "title": "Health, Nutrition & Bio-Quant Hub",
        "description": "Clinical and athletic physiological engines: BMR, TDEE, macronutrients, body fat percentages, hydration, and pharmacokinetics.",
        "badge": "Domain Hub • Bio-Quant & Health",
        "icon": "🩺"
    },
    "geometry": {
        "title": "Geometry & Spatial Analysis Hub",
        "description": "2D and 3D geometric solvers: regular polygons, conic sections, polyhedra, surfaces of revolution, and radical closed-form proofs.",
        "badge": "Domain Hub • Geometry & Spatial Analysis",
        "icon": "📐"
    },
    "physics": {
        "title": "Physics & Engineering Mechanics Hub",
        "description": "Classical Newtonian kinematics, ballistics, electromagnetism, Ohm's law, fluid mechanics, and harmonic oscillation solvers.",
        "badge": "Domain Hub • Physics & Mechanics",
        "icon": "⚡"
    },
    "calculus": {
        "title": "Calculus & Mathematical Analysis Hub",
        "description": "Computational engines for differentiation, integration, quadratic roots, linear systems, and algebraic structures.",
        "badge": "Domain Hub • Infinitesimal Calculus",
        "icon": "∫"
    },
    "statistics": {
        "title": "Probability & Statistics Hub",
        "description": "Stochastic models, probability mass/density functions, parameter estimation, z-scores, combinatorics, and Bayesian inference.",
        "badge": "Domain Hub • Probability & Statistics",
        "icon": "📊"
    },
    "energy": {
        "title": "Energy, Solar & Clean Tech Engineering Hub",
        "description": "Advanced computational solvers for solar PV generation, battery energy storage (BESS), heat pumps, LCOE, grid arbitrage, and wind power mechanics.",
        "badge": "Domain Hub • Energy & Clean Tech",
        "icon": "☀️"
    },
    "logistics": {
        "title": "Logistics, Supply Chain & Freight Operations Hub",
        "description": "Calculators for ocean container TEUs, dimensional freight weight, truckload ton-miles, customs demurrage, route fuel consumption, and warehouse pallet geometry.",
        "badge": "Domain Hub • Logistics & Freight",
        "icon": "🚢"
    },
    "crypto": {
        "title": "Cryptocurrency, DeFi & Fintech Mechanics Hub",
        "description": "Deterministic financial models for AMM impermanent loss, crypto staking APY, ASIC mining profitability, gas fees, perp liquidation thresholds, and funding rates.",
        "badge": "Domain Hub • Crypto & DeFi",
        "icon": "🪙"
    },
    "legal": {
        "title": "Legal, Insurance & Actuarial Risk Hub",
        "description": "Calculators for personal injury settlement multipliers, lost earning capacity, life insurance mortality reserves, litigation contingency fees, and workers' compensation.",
        "badge": "Domain Hub • Legal & Actuarial Risk",
        "icon": "⚖️"
    },
    "agriculture": {
        "title": "Agricultural Science, Crop & Precision Farming Hub",
        "description": "Solvers for center-pivot irrigation, NPK fertilizer blending, grain bin storage volume, cattle feed conversion, seed population planting rates, and soil CEC.",
        "badge": "Domain Hub • Agricultural Science",
        "icon": "🌾"
    },
    "engineering": {
        "title": "Civil, Structural, Geotechnical & Hydraulic Engineering Hub",
        "description": "Rigorous solvers for beam elastic deflection, Manning open channel flow, reinforced concrete rebar ratio, retaining wall lateral earth pressure, and column buckling.",
        "badge": "Domain Hub • Civil & Structural Engineering",
        "icon": "🌉"
    },
    "ecommerce": {
        "title": "E-Commerce, Direct-to-Consumer & Retail Operations Hub",
        "description": "Comprehensive unit economics models: true landed costs, inventory turnover DSI, cart abandonment recovery, Amazon FBA fee margins, GMROI, and LTV:CAC.",
        "badge": "Domain Hub • E-Commerce & Retail",
        "icon": "🛒"
    },
    "biotech": {
        "title": "Biotechnology, Pharmacology & Laboratory Medicine Hub",
        "description": "Clinical pharmacology and molecular biology solvers: drug elimination half-life, Cockcroft-Gault CrCl, PCR primer Tm, Michaelis-Menten kinetics, and qPCR 2^(-ΔΔCt).",
        "badge": "Domain Hub • Biotech & Pharmacology",
        "icon": "🧬"
    }
}
