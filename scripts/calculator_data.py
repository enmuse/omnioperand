"""
scripts/calculator_data.py
Aggregated repository of 109 commercial-grade, high-profit calculators.
Categories: finance, construction, health, geometry, physics, calculus, statistics.
"""

from data_finance import FINANCE_CALCULATORS
from data_finance_2 import FINANCE_CALCULATORS_2
from data_construction import CONSTRUCTION_CALCULATORS
from data_health import HEALTH_CALCULATORS
from data_stem import STEM_CALCULATORS

CALCULATORS_DATA = (
    FINANCE_CALCULATORS
    + FINANCE_CALCULATORS_2
    + CONSTRUCTION_CALCULATORS
    + HEALTH_CALCULATORS
    + STEM_CALCULATORS
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
    }
}
