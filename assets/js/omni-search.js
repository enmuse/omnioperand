/**
 * OmniOperand — Global Search & Navigation Controller (omni-search.js)
 * Instant fuzzy matching, keyboard navigation (Cmd+K / '/'), and Theme Toggle
 */

(function () {
  'use strict';

  // Immediate iframe / embed mode detection (0ms FOUC)
  if (typeof window !== 'undefined') {
    if (window.location.search.includes('embed=true') || (window.parent !== window && !window.location.pathname.startsWith('/embed/'))) {
      document.documentElement.classList.add('is-embed');
      if (document.body) {
        document.body.classList.add('is-embed');
      } else {
        document.addEventListener('DOMContentLoaded', () => {
          if (document.body) document.body.classList.add('is-embed');
        });
      }
    }
  }

  // Calculator & Hub Index Database
  const SEARCH_INDEX = [
  {
    "title": "OmniOperand Computational REST API & OpenAPI Schema",
    "category": "Developer & Machine Protocols",
    "url": "/api/",
    "keywords": [
      "api",
      "rest",
      "openapi",
      "json",
      "developer",
      "mcp",
      "postman",
      "sdk"
    ]
  },
  {
    "title": "OmniOperand Commercial API & MCP Pricing",
    "category": "Commercial & Subscriptions",
    "url": "/pricing/",
    "keywords": [
      "pricing",
      "pro",
      "enterprise",
      "stripe",
      "checkout",
      "api key",
      "tokens",
      "subscription"
    ]
  },
  {
    "title": "Embeddable Calculator Widgets (CaaS)",
    "category": "Developer & Webmasters",
    "url": "/embed/",
    "keywords": [
      "embed",
      "widget",
      "iframe",
      "webmaster",
      "caas",
      "calculator widget",
      "white label"
    ]
  },
  {
    "title": "Universal Regular Polygon Calculator",
    "category": "Geometry > 2D Geometry > Shapes",
    "url": "/geometry/2d/shapes/regular-polygon/",
    "keywords": [
      "regular polygon",
      "n-gon",
      "n-sided",
      "polygon",
      "triangle",
      "square",
      "pentagon",
      "hexagon",
      "octagon",
      "apothem",
      "circumradius",
      "diagonals",
      "area"
    ]
  },
  {
    "title": "Regular Octagon Calculator",
    "category": "Geometry > 2D Geometry > Shapes",
    "url": "/geometry/2d/shapes/octagon/",
    "keywords": [
      "octagon",
      "polygon",
      "8-sided",
      "apothem",
      "circumradius",
      "diagonal",
      "stop sign",
      "area",
      "perimeter"
    ]
  },
  {
    "title": "Regular Hexagon Calculator",
    "category": "Geometry > 2D Geometry > Shapes",
    "url": "/geometry/2d/shapes/hexagon/",
    "keywords": [
      "hexagon",
      "polygon",
      "6-sided",
      "honeycomb",
      "apothem",
      "circumradius",
      "diagonal",
      "area"
    ]
  },
  {
    "title": "Regular Pentagon Calculator",
    "category": "Geometry > 2D Geometry > Shapes",
    "url": "/geometry/2d/shapes/pentagon/",
    "keywords": [
      "pentagon",
      "polygon",
      "5-sided",
      "golden ratio",
      "phi",
      "pentagram",
      "diagonal",
      "apothem",
      "area"
    ]
  },
  {
    "title": "Regular Decagon Calculator",
    "category": "Geometry > 2D Geometry > Shapes",
    "url": "/geometry/2d/shapes/decagon/",
    "keywords": [
      "decagon",
      "polygon",
      "10-sided",
      "golden ratio",
      "phi",
      "apothem",
      "circumradius",
      "diagonal",
      "area"
    ]
  },
  {
    "title": "Quantitative Finance & Lending Hub",
    "category": "Domain Hub > Finance",
    "url": "/finance/",
    "keywords": [
      "finance",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Construction & Trades Engineering Hub",
    "category": "Domain Hub > Construction",
    "url": "/construction/",
    "keywords": [
      "construction",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Health, Nutrition & Bio-Quant Hub",
    "category": "Domain Hub > Health",
    "url": "/health/",
    "keywords": [
      "health",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Geometry & Spatial Analysis Hub",
    "category": "Domain Hub > Geometry",
    "url": "/geometry/",
    "keywords": [
      "geometry",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Physics & Engineering Mechanics Hub",
    "category": "Domain Hub > Physics",
    "url": "/physics/",
    "keywords": [
      "physics",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Calculus & Mathematical Analysis Hub",
    "category": "Domain Hub > Calculus",
    "url": "/calculus/",
    "keywords": [
      "calculus",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Probability & Statistics Hub",
    "category": "Domain Hub > Statistics",
    "url": "/statistics/",
    "keywords": [
      "statistics",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Energy, Solar & Clean Tech Engineering Hub",
    "category": "Domain Hub > Energy",
    "url": "/energy/",
    "keywords": [
      "energy",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Logistics, Supply Chain & Freight Operations Hub",
    "category": "Domain Hub > Logistics",
    "url": "/logistics/",
    "keywords": [
      "logistics",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Cryptocurrency, DeFi & Fintech Mechanics Hub",
    "category": "Domain Hub > Crypto",
    "url": "/crypto/",
    "keywords": [
      "crypto",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Legal, Insurance & Actuarial Risk Hub",
    "category": "Domain Hub > Legal",
    "url": "/legal/",
    "keywords": [
      "legal",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Agricultural Science, Crop & Precision Farming Hub",
    "category": "Domain Hub > Agriculture",
    "url": "/agriculture/",
    "keywords": [
      "agriculture",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Civil, Structural, Geotechnical & Hydraulic Engineering Hub",
    "category": "Domain Hub > Engineering",
    "url": "/engineering/",
    "keywords": [
      "engineering",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "E-Commerce, Direct-to-Consumer & Retail Operations Hub",
    "category": "Domain Hub > Ecommerce",
    "url": "/ecommerce/",
    "keywords": [
      "ecommerce",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Biotechnology, Pharmacology & Laboratory Medicine Hub",
    "category": "Domain Hub > Biotech",
    "url": "/biotech/",
    "keywords": [
      "biotech",
      "hub",
      "calculators",
      "overview",
      "formulas"
    ]
  },
  {
    "title": "Mortgage Refinance & Breakeven Calculator",
    "category": "Finance > Mortgage Refinancing • Breakeven Analysis",
    "url": "/finance/refinance/",
    "keywords": [
      "mortgage",
      "refinance",
      "breakeven",
      "calculator",
      "calculate",
      "monthly",
      "payment",
      "savings",
      "lifetime",
      "interest",
      "reduction",
      "and"
    ]
  },
  {
    "title": "HELOC (Home Equity Line of Credit) Payment Calculator",
    "category": "Finance > Home Equity • Revolving Credit Matrix",
    "url": "/finance/heloc/",
    "keywords": [
      "heloc",
      "home",
      "equity",
      "line",
      "credit",
      "payment",
      "calculator",
      "calculate",
      "interest-only",
      "draw",
      "period",
      "payments"
    ]
  },
  {
    "title": "Debt-to-Income (DTI) Ratio Calculator",
    "category": "Finance > Underwriting Invariants • DTI Matrix",
    "url": "/finance/dti/",
    "keywords": [
      "debt-to-income",
      "dti",
      "ratio",
      "calculator",
      "calculate",
      "front-end",
      "and",
      "back-end",
      "ratios",
      "determine",
      "your",
      "maximum"
    ]
  },
  {
    "title": "Loan-to-Value (LTV) Ratio & PMI Calculator",
    "category": "Finance > Equity Analysis • PMI Invariants",
    "url": "/finance/ltv/",
    "keywords": [
      "loan-to-value",
      "ltv",
      "ratio",
      "pmi",
      "calculator",
      "determine",
      "your",
      "exact",
      "required",
      "private",
      "mortgage",
      "insurance"
    ]
  },
  {
    "title": "FHA Loan & Mortgage Insurance (MIP) Calculator",
    "category": "Finance > Government Lending • FHA Formula",
    "url": "/finance/fha-loan/",
    "keywords": [
      "fha",
      "loan",
      "mortgage",
      "insurance",
      "mip",
      "calculator",
      "calculate",
      "monthly",
      "payments",
      "including",
      "upfront",
      "ufmip"
    ]
  },
  {
    "title": "VA Loan Payment & Funding Fee Calculator",
    "category": "Finance > Military Benefits • 0% Down Invariant",
    "url": "/finance/va-loan/",
    "keywords": [
      "loan",
      "payment",
      "funding",
      "fee",
      "calculator",
      "calculate",
      "down",
      "home",
      "monthly",
      "payments",
      "tiered",
      "fees"
    ]
  },
  {
    "title": "Reverse Mortgage (HECM) Calculator",
    "category": "Finance > Retirement Equity • HECM Formulas",
    "url": "/finance/reverse-mortgage/",
    "keywords": [
      "reverse",
      "mortgage",
      "hecm",
      "calculator",
      "estimate",
      "home",
      "equity",
      "conversion",
      "borrowing",
      "power",
      "principal",
      "limits"
    ]
  },
  {
    "title": "Personal Loan & Debt Consolidation Calculator",
    "category": "Finance > Unsecured Credit • Amortization Matrix",
    "url": "/finance/personal-loan/",
    "keywords": [
      "personal",
      "loan",
      "debt",
      "consolidation",
      "calculator",
      "calculate",
      "fixed",
      "monthly",
      "installments",
      "total",
      "interest",
      "and"
    ]
  },
  {
    "title": "Student Loan Refinancing Calculator",
    "category": "Finance > Education Debt • Refi Yields",
    "url": "/finance/student-loan-refinance/",
    "keywords": [
      "student",
      "loan",
      "refinancing",
      "calculator",
      "calculate",
      "interest",
      "savings",
      "and",
      "monthly",
      "payment",
      "changes",
      "when"
    ]
  },
  {
    "title": "Credit Card Payoff & Interest Snowball Calculator",
    "category": "Finance > Consumer Debt • Exponential Decay",
    "url": "/finance/credit-card-payoff/",
    "keywords": [
      "credit",
      "card",
      "payoff",
      "interest",
      "snowball",
      "calculator",
      "calculate",
      "exact",
      "debt-free",
      "timelines",
      "total",
      "compound"
    ]
  },
  {
    "title": "Boat Loan Financing & Payment Calculator",
    "category": "Finance > Marine Lending • Fixed Installments",
    "url": "/finance/boat-loan/",
    "keywords": [
      "boat",
      "loan",
      "financing",
      "payment",
      "calculator",
      "calculate",
      "marine",
      "monthly",
      "payments",
      "required",
      "down",
      "10-20"
    ]
  },
  {
    "title": "RV Loan & Motorhome Financing Calculator",
    "category": "Finance > Recreational Vehicle • Amortization",
    "url": "/finance/rv-loan/",
    "keywords": [
      "loan",
      "motorhome",
      "financing",
      "calculator",
      "calculate",
      "travel",
      "trailer",
      "and",
      "fifth-wheel",
      "monthly",
      "installments",
      "sales"
    ]
  },
  {
    "title": "Motorcycle Loan & Financing Calculator",
    "category": "Finance > Powersports Lending • Fast Installments",
    "url": "/finance/motorcycle-loan/",
    "keywords": [
      "motorcycle",
      "loan",
      "financing",
      "calculator",
      "calculate",
      "monthly",
      "payments",
      "and",
      "total",
      "interest",
      "for",
      "new"
    ]
  },
  {
    "title": "Solar Loan & Energy Payoff Calculator",
    "category": "Finance > Clean Energy Finance • ITC Tax Credits",
    "url": "/finance/solar-loan/",
    "keywords": [
      "solar",
      "loan",
      "energy",
      "payoff",
      "calculator",
      "calculate",
      "residential",
      "system",
      "financing",
      "federal",
      "itc",
      "tax"
    ]
  },
  {
    "title": "Commercial Real Estate Mortgage Calculator",
    "category": "Finance > CRE Financing • Balloon Invariants",
    "url": "/finance/commercial-mortgage/",
    "keywords": [
      "commercial",
      "real",
      "estate",
      "mortgage",
      "calculator",
      "calculate",
      "monthly",
      "payments",
      "balloon",
      "balances",
      "and",
      "debt"
    ]
  },
  {
    "title": "DSCR (Debt Service Coverage Ratio) Calculator",
    "category": "Finance > Investor Underwriting • DSCR Formula",
    "url": "/finance/dscr-loan/",
    "keywords": [
      "dscr",
      "debt",
      "service",
      "coverage",
      "ratio",
      "calculator",
      "calculate",
      "and",
      "qualify",
      "for",
      "real",
      "estate"
    ]
  },
  {
    "title": "Cap Rate (Capitalization Rate) Calculator",
    "category": "Finance > Real Estate Valuation • Cap Rate Matrix",
    "url": "/finance/cap-rate/",
    "keywords": [
      "cap",
      "rate",
      "capitalization",
      "calculator",
      "calculate",
      "commercial",
      "and",
      "residential",
      "real",
      "estate",
      "rates",
      "valuation"
    ]
  },
  {
    "title": "Rental Property Cash Flow & ROI Calculator",
    "category": "Finance > Real Estate ROI • Cash-on-Cash",
    "url": "/finance/rental-cash-flow/",
    "keywords": [
      "rental",
      "property",
      "cash",
      "flow",
      "roi",
      "calculator",
      "calculate",
      "monthly",
      "net",
      "cash-on-cash",
      "return",
      "coc"
    ]
  },
  {
    "title": "BRRRR Real Estate Investment Calculator",
    "category": "Finance > Real Estate Wealth • Capital Velocity",
    "url": "/finance/brrrr/",
    "keywords": [
      "brrrr",
      "real",
      "estate",
      "investment",
      "calculator",
      "analyze",
      "buy",
      "rehab",
      "rent",
      "refinance",
      "repeat",
      "transactions"
    ]
  },
  {
    "title": "Hard Money & Fix-and-Flip Loan Calculator",
    "category": "Finance > Bridge Lending • Fix-and-Flip Math",
    "url": "/finance/hard-money-loan/",
    "keywords": [
      "hard",
      "money",
      "fix-and-flip",
      "loan",
      "calculator",
      "calculate",
      "short-term",
      "bridge",
      "and",
      "costs",
      "origination",
      "points"
    ]
  },
  {
    "title": "Roth IRA Conversion & Tax Optimizer",
    "category": "Finance > Tax Optimization • Compound Exemption",
    "url": "/finance/roth-ira-conversion/",
    "keywords": [
      "roth",
      "ira",
      "conversion",
      "tax",
      "optimizer",
      "calculate",
      "income",
      "taxes",
      "future",
      "tax-free",
      "growth",
      "advantages"
    ]
  },
  {
    "title": "Traditional vs Roth 401(k) / IRA Calculator",
    "category": "Finance > Retirement Taxation • Horizon Comparison",
    "url": "/finance/traditional-vs-roth/",
    "keywords": [
      "traditional",
      "roth",
      "401",
      "ira",
      "calculator",
      "compare",
      "pre-tax",
      "retirement",
      "savings",
      "against",
      "post-tax",
      "contributions"
    ]
  },
  {
    "title": "Required Minimum Distribution (RMD) Calculator",
    "category": "Finance > IRS Mandates • Uniform Lifetime Table",
    "url": "/finance/rmd/",
    "keywords": [
      "required",
      "minimum",
      "distribution",
      "rmd",
      "calculator",
      "calculate",
      "irs",
      "mandatory",
      "annual",
      "withdrawals",
      "from",
      "traditional"
    ]
  },
  {
    "title": "Dividend Reinvestment (DRIP) Calculator",
    "category": "Finance > Equity Compounding • DRIP Engine",
    "url": "/finance/drip/",
    "keywords": [
      "dividend",
      "reinvestment",
      "drip",
      "calculator",
      "simulate",
      "exponential",
      "compounding",
      "through",
      "automatic",
      "growth",
      "rates",
      "and"
    ]
  },
  {
    "title": "FIRE Calculator (Financial Independence, Retire Early)",
    "category": "Finance > Financial Independence • 4% Rule",
    "url": "/finance/fire/",
    "keywords": [
      "fire",
      "calculator",
      "financial",
      "independence",
      "retire",
      "early",
      "calculate",
      "your",
      "exact",
      "number",
      "lean",
      "fat"
    ]
  },
  {
    "title": "Social Security Benefit & Age Optimizer",
    "category": "Finance > Actuarial Retirement • Social Security",
    "url": "/finance/social-security/",
    "keywords": [
      "social",
      "security",
      "benefit",
      "age",
      "optimizer",
      "determine",
      "your",
      "optimal",
      "claiming",
      "breakeven",
      "life",
      "expectancy"
    ]
  },
  {
    "title": "Pension Annuity vs Lump Sum Calculator",
    "category": "Finance > Actuarial Science • Pension Decisions",
    "url": "/finance/pension-vs-lump-sum/",
    "keywords": [
      "pension",
      "annuity",
      "lump",
      "sum",
      "calculator",
      "evaluate",
      "defined",
      "benefit",
      "options",
      "determine",
      "the",
      "internal"
    ]
  },
  {
    "title": "Certificate of Deposit (CD) Calculator",
    "category": "Finance > Fixed Income • Compound Yield",
    "url": "/finance/cd-calculator/",
    "keywords": [
      "certificate",
      "deposit",
      "calculator",
      "calculate",
      "compounding",
      "yields",
      "early",
      "withdrawal",
      "penalties",
      "and",
      "fixed",
      "returns"
    ]
  },
  {
    "title": "High-Yield Savings Account (HYSA) Calculator",
    "category": "Finance > Cash Management • Liquid Compounding",
    "url": "/finance/hysa/",
    "keywords": [
      "high-yield",
      "savings",
      "account",
      "hysa",
      "calculator",
      "calculate",
      "compound",
      "growth",
      "with",
      "monthly",
      "deposits",
      "daily"
    ]
  },
  {
    "title": "Inflation & Purchasing Power Calculator",
    "category": "Finance > Monetary Economics • Purchasing Power",
    "url": "/finance/inflation/",
    "keywords": [
      "inflation",
      "purchasing",
      "power",
      "calculator",
      "calculate",
      "the",
      "erosion",
      "over",
      "time",
      "future",
      "cost",
      "living"
    ]
  },
  {
    "title": "Rule of 72 Investment Doubling Calculator",
    "category": "Finance > Mental Math • Logarithmic Approximation",
    "url": "/finance/rule-of-72/",
    "keywords": [
      "rule",
      "investment",
      "doubling",
      "calculator",
      "calculate",
      "exact",
      "and",
      "heuristic",
      "periods",
      "using",
      "the",
      "logarithmic"
    ]
  },
  {
    "title": "Stock Option & RSU Vesting Calculator",
    "category": "Finance > Equity Compensation • Tax Withholding",
    "url": "/finance/stock-option-rsu/",
    "keywords": [
      "stock",
      "option",
      "rsu",
      "vesting",
      "calculator",
      "calculate",
      "equity",
      "compensation",
      "value",
      "vested",
      "shares",
      "tax"
    ]
  },
  {
    "title": "Crypto Profit & Capital Gains Tax Calculator",
    "category": "Finance > Digital Assets • Tax Accounting",
    "url": "/finance/crypto-profit-tax/",
    "keywords": [
      "crypto",
      "profit",
      "capital",
      "gains",
      "tax",
      "calculator",
      "calculate",
      "cryptocurrency",
      "trading",
      "profits",
      "short-term",
      "long-term"
    ]
  },
  {
    "title": "Capital Gains Tax Calculator",
    "category": "Finance > Tax Optimization • Statutory Brackets",
    "url": "/finance/capital-gains-tax/",
    "keywords": [
      "capital",
      "gains",
      "tax",
      "calculator",
      "calculate",
      "federal",
      "and",
      "state",
      "taxes",
      "stocks",
      "real",
      "estate"
    ]
  },
  {
    "title": "1099 Self-Employment Tax (SECA) Calculator",
    "category": "Finance > 1099 Contracting • SECA Matrix",
    "url": "/finance/self-employment-tax/",
    "keywords": [
      "1099",
      "self-employment",
      "tax",
      "seca",
      "calculator",
      "calculate",
      "social",
      "security",
      "medicare",
      "above-the-line",
      "deduction",
      "and"
    ]
  },
  {
    "title": "Salary to Hourly Wage Calculator",
    "category": "Finance > Compensation • Wage Conversion",
    "url": "/finance/salary-to-hourly/",
    "keywords": [
      "salary",
      "hourly",
      "wage",
      "calculator",
      "convert",
      "annual",
      "into",
      "equivalent",
      "daily",
      "weekly",
      "and",
      "bi-weekly"
    ]
  },
  {
    "title": "Hourly to Salary Wage Calculator",
    "category": "Finance > Payroll Math • Overtime Invariant",
    "url": "/finance/hourly-to-salary/",
    "keywords": [
      "hourly",
      "salary",
      "wage",
      "calculator",
      "convert",
      "pay",
      "into",
      "gross",
      "annual",
      "accounting",
      "for",
      "overtime"
    ]
  },
  {
    "title": "Sales Commission & Quota Calculator",
    "category": "Finance > Sales Compensation • Tier Accelerators",
    "url": "/finance/commission/",
    "keywords": [
      "sales",
      "commission",
      "quota",
      "calculator",
      "calculate",
      "tiered",
      "payouts",
      "accelerated",
      "accelerator",
      "tiers",
      "and",
      "on-target"
    ]
  },
  {
    "title": "Break-Even Point Analysis Calculator",
    "category": "Finance > Corporate Finance • Breakeven Invariant",
    "url": "/finance/break-even/",
    "keywords": [
      "break-even",
      "point",
      "analysis",
      "calculator",
      "calculate",
      "exact",
      "unit",
      "and",
      "revenue",
      "points",
      "contribution",
      "margins"
    ]
  },
  {
    "title": "Margin vs Markup Multiplier Calculator",
    "category": "Finance > Pricing Strategy • Margin-Markup Dual",
    "url": "/finance/margin-markup/",
    "keywords": [
      "margin",
      "markup",
      "multiplier",
      "calculator",
      "convert",
      "between",
      "gross",
      "profit",
      "and",
      "percentage",
      "calculate",
      "target"
    ]
  },
  {
    "title": "Square Footage & Area Calculator",
    "category": "Construction > Construction Math • Precision Area Solver",
    "url": "/construction/square-footage/",
    "keywords": [
      "square",
      "footage",
      "area",
      "calculator",
      "calculate",
      "for",
      "single",
      "rooms",
      "multi-room",
      "floorplans",
      "and",
      "landscaping"
    ]
  },
  {
    "title": "Concrete Slab & Footing Volume Calculator",
    "category": "Construction > Ready-Mix Concrete • Volume & Bag Matrix",
    "url": "/construction/concrete-slab/",
    "keywords": [
      "concrete",
      "slab",
      "footing",
      "volume",
      "calculator",
      "calculate",
      "cubic",
      "yards",
      "ready-mix",
      "60lb",
      "80lb",
      "bag"
    ]
  },
  {
    "title": "Paint Coverage & Gallons Calculator",
    "category": "Construction > Painting & Coatings • Coverage Matrix",
    "url": "/construction/paint-coverage/",
    "keywords": [
      "paint",
      "coverage",
      "gallons",
      "calculator",
      "calculate",
      "exact",
      "and",
      "primer",
      "requirements",
      "for",
      "walls",
      "ceilings"
    ]
  },
  {
    "title": "Flooring & Tile Quantity Calculator",
    "category": "Construction > Flooring Solutions • Waste & Box Matrix",
    "url": "/construction/flooring/",
    "keywords": [
      "flooring",
      "tile",
      "quantity",
      "calculator",
      "calculate",
      "hardwood",
      "planks",
      "laminate",
      "vinyl",
      "plank",
      "lvp",
      "and"
    ]
  },
  {
    "title": "Drywall Sheet & Joint Compound Calculator",
    "category": "Construction > Drywall & Sheetrock • Wall & Ceiling Matrix",
    "url": "/construction/drywall/",
    "keywords": [
      "drywall",
      "sheet",
      "joint",
      "compound",
      "calculator",
      "calculate",
      "and",
      "panels",
      "buckets",
      "screws",
      "paper",
      "tape"
    ]
  },
  {
    "title": "Gravel & Crushed Stone Tonnage Calculator",
    "category": "Construction > Civil Engineering • Aggregate Tonnage Matrix",
    "url": "/construction/gravel/",
    "keywords": [
      "gravel",
      "crushed",
      "stone",
      "tonnage",
      "calculator",
      "calculate",
      "cubic",
      "yards",
      "and",
      "metric",
      "tons",
      "crush-and-run"
    ]
  },
  {
    "title": "Mulch & Soil Volume Calculator",
    "category": "Construction > Landscaping • Landscape Mulch Matrix",
    "url": "/construction/mulch/",
    "keywords": [
      "mulch",
      "soil",
      "volume",
      "calculator",
      "calculate",
      "cubic",
      "yards",
      "and",
      "bag",
      "counts",
      "hardwood",
      "bark"
    ]
  },
  {
    "title": "Patio Paver & Polymeric Sand Calculator",
    "category": "Construction > Hardscaping • Paver & Base Solver",
    "url": "/construction/pavers/",
    "keywords": [
      "patio",
      "paver",
      "polymeric",
      "sand",
      "calculator",
      "calculate",
      "stone",
      "pavers",
      "bedding",
      "crushed",
      "base",
      "and"
    ]
  },
  {
    "title": "Sod & Turf Pallet Calculator",
    "category": "Construction > Turfgrass • Pallet & Roll Matrix",
    "url": "/construction/sod-turf/",
    "keywords": [
      "sod",
      "turf",
      "pallet",
      "calculator",
      "calculate",
      "rolls",
      "square",
      "feet",
      "counts",
      "and",
      "soil",
      "prep"
    ]
  },
  {
    "title": "Retaining Wall Block & Backfill Calculator",
    "category": "Construction > Structural Masonry • Block & Drainage Matrix",
    "url": "/construction/retaining-wall/",
    "keywords": [
      "retaining",
      "wall",
      "block",
      "backfill",
      "calculator",
      "calculate",
      "blocks",
      "capstones",
      "gravel",
      "drainage",
      "and",
      "perforated"
    ]
  },
  {
    "title": "Deck Framing & Joist Spacing Calculator",
    "category": "Construction > Carpentry & Framing • Deck Structural Matrix",
    "url": "/construction/deck-framing/",
    "keywords": [
      "deck",
      "framing",
      "joist",
      "spacing",
      "calculator",
      "calculate",
      "pressure-treated",
      "floor",
      "joists",
      "rim",
      "support",
      "beams"
    ]
  },
  {
    "title": "Fence Post, Rail & Picket Calculator",
    "category": "Construction > Fencing Solutions • Post & Picket Matrix",
    "url": "/construction/fence-post/",
    "keywords": [
      "fence",
      "post",
      "rail",
      "picket",
      "calculator",
      "calculate",
      "posts",
      "horizontal",
      "rails",
      "dog-ear",
      "pickets",
      "and"
    ]
  },
  {
    "title": "Asphalt Driveway Tonnage & Cost Calculator",
    "category": "Construction > Civil Paving • Hot Mix Asphalt Matrix",
    "url": "/construction/asphalt-driveway/",
    "keywords": [
      "asphalt",
      "driveway",
      "tonnage",
      "cost",
      "calculator",
      "calculate",
      "hot",
      "mix",
      "hma",
      "square",
      "footage",
      "and"
    ]
  },
  {
    "title": "Brick & Mortar Quantity Calculator",
    "category": "Construction > Masonry Infrastructure • Brick & Mortar Matrix",
    "url": "/construction/brick-mortar/",
    "keywords": [
      "brick",
      "mortar",
      "quantity",
      "calculator",
      "calculate",
      "modular",
      "standard",
      "and",
      "queen",
      "quantities",
      "plus",
      "type"
    ]
  },
  {
    "title": "Board Feet (FBM) & Lumber Price Calculator",
    "category": "Construction > Hardwood & Forestry • Board Foot Solver",
    "url": "/construction/lumber-board-feet/",
    "keywords": [
      "board",
      "feet",
      "fbm",
      "lumber",
      "price",
      "calculator",
      "calculate",
      "footage",
      "and",
      "total",
      "pricing",
      "for"
    ]
  },
  {
    "title": "Roofing Shingles & Bundles Calculator",
    "category": "Construction > Roofing Systems • Pitch & Shingle Matrix",
    "url": "/construction/roofing-shingles/",
    "keywords": [
      "roofing",
      "shingles",
      "bundles",
      "calculator",
      "calculate",
      "squares",
      "3-tab",
      "and",
      "architectural",
      "shingle",
      "underlayment",
      "rolls"
    ]
  },
  {
    "title": "HVAC Air Conditioner BTU & Tonnage Calculator",
    "category": "Construction > HVAC Engineering • Manual J Sizing Solver",
    "url": "/construction/ac-btu-tonnage/",
    "keywords": [
      "hvac",
      "air",
      "conditioner",
      "btu",
      "tonnage",
      "calculator",
      "calculate",
      "residential",
      "cooling",
      "requirements",
      "and",
      "condenser"
    ]
  },
  {
    "title": "Heating BTU & Furnace Sizing Calculator",
    "category": "Construction > Thermal Systems • Furnace Sizing Matrix",
    "url": "/construction/heating-btu/",
    "keywords": [
      "heating",
      "btu",
      "furnace",
      "sizing",
      "calculator",
      "calculate",
      "output",
      "and",
      "thermal",
      "efficiency",
      "ratings",
      "based"
    ]
  },
  {
    "title": "Solar Panel Array Sizing & kWh Calculator",
    "category": "Construction > Renewable Energy • Photovoltaic Matrix",
    "url": "/construction/solar-sizing/",
    "keywords": [
      "solar",
      "panel",
      "array",
      "sizing",
      "kwh",
      "calculator",
      "calculate",
      "system",
      "size",
      "required",
      "roof",
      "panels"
    ]
  },
  {
    "title": "Tankless Water Heater GPM & Sizing Calculator",
    "category": "Construction > Plumbing Engineering • Flow & Thermal Rise Matrix",
    "url": "/construction/tankless-water-heater/",
    "keywords": [
      "tankless",
      "water",
      "heater",
      "gpm",
      "sizing",
      "calculator",
      "calculate",
      "required",
      "gallons",
      "per",
      "minute",
      "incoming"
    ]
  },
  {
    "title": "Electricity Cost & Appliance kWh Calculator",
    "category": "Construction > Electrical Economics • kWh Cost Matrix",
    "url": "/construction/electricity-cost/",
    "keywords": [
      "electricity",
      "cost",
      "appliance",
      "kwh",
      "calculator",
      "calculate",
      "daily",
      "monthly",
      "and",
      "annual",
      "operating",
      "costs"
    ]
  },
  {
    "title": "Voltage Drop & Wire Gauge (AWG) Calculator",
    "category": "Construction > Electrical Engineering • NEC Voltage Drop Matrix",
    "url": "/construction/wire-gauge-drop/",
    "keywords": [
      "voltage",
      "drop",
      "wire",
      "gauge",
      "awg",
      "calculator",
      "calculate",
      "electrical",
      "percentage",
      "loss",
      "and",
      "proper"
    ]
  },
  {
    "title": "Generator Sizing & Starting Watts Calculator",
    "category": "Construction > Emergency Power • Generator Sizing Matrix",
    "url": "/construction/generator-sizing/",
    "keywords": [
      "generator",
      "sizing",
      "starting",
      "watts",
      "calculator",
      "calculate",
      "running",
      "and",
      "surge",
      "for",
      "whole-home",
      "portable"
    ]
  },
  {
    "title": "Insulation R-Value & Batt Roll Calculator",
    "category": "Construction > Thermal Envelope • R-Value & Batt Matrix",
    "url": "/construction/insulation-r-value/",
    "keywords": [
      "insulation",
      "r-value",
      "batt",
      "roll",
      "calculator",
      "calculate",
      "thermal",
      "resistance",
      "fiberglass",
      "and",
      "quantities",
      "blow-in"
    ]
  },
  {
    "title": "Concrete Rebar Grid & Weight Calculator",
    "category": "Construction > Reinforced Concrete • Rebar Grid Solver",
    "url": "/construction/rebar-calculator/",
    "keywords": [
      "concrete",
      "rebar",
      "grid",
      "weight",
      "calculator",
      "calculate",
      "sticks",
      "layout",
      "spacing",
      "overlap",
      "splices",
      "and"
    ]
  },
  {
    "title": "Rain Gutter & Downspout Sizing Calculator",
    "category": "Construction > Stormwater Engineering • Gutter Capacity Matrix",
    "url": "/construction/gutter-sizing/",
    "keywords": [
      "rain",
      "gutter",
      "downspout",
      "sizing",
      "calculator",
      "calculate",
      "roof",
      "drainage",
      "watershed",
      "5-inch",
      "6-inch",
      "seamless"
    ]
  },
  {
    "title": "Trench Excavation & Soil Swell Calculator",
    "category": "Construction > Earthwork & Excavation • Soil Swell Matrix",
    "url": "/construction/excavation-trench/",
    "keywords": [
      "trench",
      "excavation",
      "soil",
      "swell",
      "calculator",
      "calculate",
      "volume",
      "cubic",
      "yards",
      "bank",
      "bcy",
      "loose"
    ]
  },
  {
    "title": "Basal Metabolic Rate (BMR) Calculator",
    "category": "Health > Bio-Quant • Metabolic Invariants",
    "url": "/health/bmr/",
    "keywords": [
      "basal",
      "metabolic",
      "rate",
      "bmr",
      "calculator",
      "calculate",
      "daily",
      "calories",
      "burned",
      "rest",
      "using",
      "the"
    ]
  },
  {
    "title": "Total Daily Energy Expenditure (TDEE) Calculator",
    "category": "Health > Thermodynamics • Energy Expenditure Solver",
    "url": "/health/tdee/",
    "keywords": [
      "total",
      "daily",
      "energy",
      "expenditure",
      "tdee",
      "calculator",
      "calculate",
      "calorie",
      "based",
      "bmr",
      "and",
      "physical"
    ]
  },
  {
    "title": "Body Mass Index (BMI) & Weight Category Calculator",
    "category": "Health > Anthropometry • WHO BMI Invariants",
    "url": "/health/bmi/",
    "keywords": [
      "body",
      "mass",
      "index",
      "bmi",
      "weight",
      "category",
      "calculator",
      "calculate",
      "prime",
      "and",
      "healthy",
      "range"
    ]
  },
  {
    "title": "US Navy Body Fat Percentage Calculator",
    "category": "Health > Body Composition • US Navy Circumference Method",
    "url": "/health/body-fat/",
    "keywords": [
      "navy",
      "body",
      "fat",
      "percentage",
      "calculator",
      "calculate",
      "and",
      "fat-free",
      "lean",
      "mass",
      "using",
      "the"
    ]
  },
  {
    "title": "Macronutrient Split (Carbs, Protein, Fats) Calculator",
    "category": "Health > Nutritional Biochemistry • Macronutrient Gram Matrix",
    "url": "/health/macro/",
    "keywords": [
      "macronutrient",
      "split",
      "carbs",
      "protein",
      "fats",
      "calculator",
      "calculate",
      "daily",
      "targets",
      "grams",
      "and",
      "calories"
    ]
  },
  {
    "title": "Calorie Deficit & Fat Loss Timeline Calculator",
    "category": "Health > Thermodynamics • Fat Loss Vector",
    "url": "/health/calorie-deficit/",
    "keywords": [
      "calorie",
      "deficit",
      "fat",
      "loss",
      "timeline",
      "calculator",
      "calculate",
      "daily",
      "caloric",
      "weekly",
      "rate",
      "and"
    ]
  },
  {
    "title": "Ideal Body Weight (IBW) Calculator",
    "category": "Health > Clinical Pharmacokinetics • IBW Formula Suite",
    "url": "/health/ideal-weight/",
    "keywords": [
      "ideal",
      "body",
      "weight",
      "ibw",
      "calculator",
      "calculate",
      "clinical",
      "using",
      "devine",
      "robinson",
      "miller",
      "and"
    ]
  },
  {
    "title": "Daily Water Intake & Hydration Calculator",
    "category": "Health > Fluid Dynamics • Hydration Solver",
    "url": "/health/water-intake/",
    "keywords": [
      "daily",
      "water",
      "intake",
      "hydration",
      "calculator",
      "calculate",
      "requirements",
      "ounces",
      "liters",
      "and",
      "standard",
      "glasses"
    ]
  },
  {
    "title": "Target Heart Rate & Training Zones Calculator",
    "category": "Health > Cardiovascular Physiology • Karvonen Matrix",
    "url": "/health/target-heart-rate/",
    "keywords": [
      "target",
      "heart",
      "rate",
      "training",
      "zones",
      "calculator",
      "calculate",
      "cardiovascular",
      "zone",
      "recovery",
      "vo2",
      "max"
    ]
  },
  {
    "title": "One Rep Max (1RM) Calculator",
    "category": "Health > Biomechanics • Strength 1RM Matrix",
    "url": "/health/one-rep-max/",
    "keywords": [
      "one",
      "rep",
      "max",
      "1rm",
      "calculator",
      "calculate",
      "estimated",
      "and",
      "percentage",
      "load",
      "working",
      "sets"
    ]
  },
  {
    "title": "Running Pace & Race Finish Time Calculator",
    "category": "Health > Athletic Kinetics • Running Pace Matrix",
    "url": "/health/running-pace/",
    "keywords": [
      "running",
      "pace",
      "race",
      "finish",
      "time",
      "calculator",
      "calculate",
      "speed",
      "mph",
      "splits",
      "per",
      "mile"
    ]
  },
  {
    "title": "VO2 Max & Aerobic Fitness Calculator",
    "category": "Health > Cardiopulmonary • VO2 Max Matrix",
    "url": "/health/vo2-max/",
    "keywords": [
      "vo2",
      "max",
      "aerobic",
      "fitness",
      "calculator",
      "calculate",
      "maximal",
      "oxygen",
      "uptake",
      "min",
      "and",
      "cardio"
    ]
  },
  {
    "title": "Intermittent Fasting & Autophagy Schedule Calculator",
    "category": "Health > Circadian Biology • Fasting Protocol Matrix",
    "url": "/health/intermittent-fasting/",
    "keywords": [
      "intermittent",
      "fasting",
      "autophagy",
      "schedule",
      "calculator",
      "calculate",
      "and",
      "feeding",
      "windows",
      "for",
      "omad",
      "schedules"
    ]
  },
  {
    "title": "Sleep Cycle & Optimal Bedtime Calculator",
    "category": "Health > Neuro-Physiology • 90-Min Sleep Architecture",
    "url": "/health/sleep-cycles/",
    "keywords": [
      "sleep",
      "cycle",
      "optimal",
      "bedtime",
      "calculator",
      "calculate",
      "exact",
      "bedtimes",
      "and",
      "wake",
      "times",
      "aligned"
    ]
  },
  {
    "title": "Pregnancy Due Date & Gestational Age Calculator",
    "category": "Health > Obstetrics • Naegele's Rule EDD Matrix",
    "url": "/health/pregnancy-due-date/",
    "keywords": [
      "pregnancy",
      "due",
      "date",
      "gestational",
      "age",
      "calculator",
      "calculate",
      "estimated",
      "delivery",
      "edd",
      "current",
      "weeks"
    ]
  },
  {
    "title": "Ovulation & Fertile Window Calculator",
    "category": "Health > Reproductive Endocrinology • Ovulation Matrix",
    "url": "/health/ovulation/",
    "keywords": [
      "ovulation",
      "fertile",
      "window",
      "calculator",
      "calculate",
      "peak",
      "day",
      "days",
      "prior",
      "and",
      "luteal",
      "phase"
    ]
  },
  {
    "title": "Blood Alcohol Concentration (BAC) Calculator",
    "category": "Health > Toxicology • Widmark Pharmacokinetic Matrix",
    "url": "/health/bac/",
    "keywords": [
      "blood",
      "alcohol",
      "concentration",
      "bac",
      "calculator",
      "calculate",
      "and",
      "hours",
      "until",
      "sober",
      "using",
      "the"
    ]
  },
  {
    "title": "Caffeine Half-Life & Sleep Clearance Calculator",
    "category": "Health > Pharmacokinetics • CYP1A2 Degradation Matrix",
    "url": "/health/caffeine-half-life/",
    "keywords": [
      "caffeine",
      "half-life",
      "sleep",
      "clearance",
      "calculator",
      "calculate",
      "remaining",
      "active",
      "bloodstream",
      "and",
      "timeline",
      "based"
    ]
  },
  {
    "title": "Keto Net Carbs & Ketogenic Ratio Calculator",
    "category": "Health > Biochemistry • Ketogenic Ratio Matrix",
    "url": "/health/keto-carb-limit/",
    "keywords": [
      "keto",
      "net",
      "carbs",
      "ketogenic",
      "ratio",
      "calculator",
      "calculate",
      "daily",
      "carbohydrate",
      "limits",
      "total",
      "fiber"
    ]
  },
  {
    "title": "Daily Protein Requirement & Muscle Synthesis Calculator",
    "category": "Health > Sports Nutrition • Protein Synthesis Matrix",
    "url": "/health/daily-protein/",
    "keywords": [
      "daily",
      "protein",
      "requirement",
      "muscle",
      "synthesis",
      "calculator",
      "calculate",
      "optimal",
      "intake",
      "grams",
      "and",
      "meals"
    ]
  },
  {
    "title": "Smoking Cost & Pack-Years Health Calculator",
    "category": "Health > Public Health & Finance • Pack-Year Matrix",
    "url": "/health/smoking-cost/",
    "keywords": [
      "smoking",
      "cost",
      "pack-years",
      "health",
      "calculator",
      "calculate",
      "lifetime",
      "financial",
      "lost",
      "investment",
      "compound",
      "interest"
    ]
  },
  {
    "title": "Bench Press Pyramid & Warm-Up Set Calculator",
    "category": "Health > Barbell Biomechanics • Pyramid Set Matrix",
    "url": "/health/bench-press-pyramid/",
    "keywords": [
      "bench",
      "press",
      "pyramid",
      "warm-up",
      "set",
      "calculator",
      "calculate",
      "ascending",
      "and",
      "descending",
      "strength",
      "sets"
    ]
  },
  {
    "title": "Creatine Monohydrate Dosing & Saturation Calculator",
    "category": "Health > Ergogenic Bio-Quant • Creatine Saturation Matrix",
    "url": "/health/creatine-dosing/",
    "keywords": [
      "creatine",
      "monohydrate",
      "dosing",
      "saturation",
      "calculator",
      "calculate",
      "loading",
      "protocol",
      "20g",
      "day",
      "maintenance",
      "and"
    ]
  },
  {
    "title": "Total Blood Volume (Nadler) Calculator",
    "category": "Health > Hematology • Nadler Hemodynamic Matrix",
    "url": "/health/blood-volume/",
    "keywords": [
      "total",
      "blood",
      "volume",
      "nadler",
      "calculator",
      "calculate",
      "circulating",
      "tbv",
      "plasma",
      "and",
      "red",
      "cell"
    ]
  },
  {
    "title": "Mean Arterial Pressure (MAP) Calculator",
    "category": "Health > Hemodynamics • Perfusion Pressure Matrix",
    "url": "/health/mean-arterial-pressure/",
    "keywords": [
      "mean",
      "arterial",
      "pressure",
      "map",
      "calculator",
      "calculate",
      "and",
      "organ",
      "perfusion",
      "adequacy",
      "from",
      "systolic"
    ]
  },
  {
    "title": "Ellipse Area, Perimeter & Eccentricity Calculator",
    "category": "Geometry > Conic Sections • Ramanujan Elliptic Matrix",
    "url": "/geometry/ellipse/",
    "keywords": [
      "ellipse",
      "area",
      "perimeter",
      "eccentricity",
      "calculator",
      "calculate",
      "exact",
      "ramanujan",
      "high-precision",
      "approximation",
      "semi-axes",
      "focal"
    ]
  },
  {
    "title": "Trapezoid Area, Median & Perimeter Calculator",
    "category": "Geometry > Planar Geometry • Trapezoid Solver",
    "url": "/geometry/trapezoid/",
    "keywords": [
      "trapezoid",
      "area",
      "median",
      "perimeter",
      "calculator",
      "calculate",
      "trapezium",
      "midline",
      "and",
      "diagonal",
      "lengths",
      "from"
    ]
  },
  {
    "title": "Rhombus Area, Side & Diagonals Calculator",
    "category": "Geometry > Equilateral Quadrilateral • Rhombus Matrix",
    "url": "/geometry/rhombus/",
    "keywords": [
      "rhombus",
      "area",
      "side",
      "diagonals",
      "calculator",
      "calculate",
      "perimeter",
      "length",
      "incircle",
      "radius",
      "and",
      "internal"
    ]
  },
  {
    "title": "Parallelogram Area & Diagonals Calculator",
    "category": "Geometry > Affine Geometry • Parallelogram Matrix",
    "url": "/geometry/parallelogram/",
    "keywords": [
      "parallelogram",
      "area",
      "diagonals",
      "calculator",
      "calculate",
      "perimeter",
      "internal",
      "and",
      "heights",
      "using",
      "base",
      "side"
    ]
  },
  {
    "title": "Kite Geometry & Area Calculator",
    "category": "Geometry > Deltoid Geometry • Kite Area Matrix",
    "url": "/geometry/kite/",
    "keywords": [
      "kite",
      "geometry",
      "area",
      "calculator",
      "calculate",
      "perimeter",
      "side",
      "pairs",
      "and",
      "internal",
      "diagonal",
      "lengths"
    ]
  },
  {
    "title": "Cylinder Volume & Surface Area Calculator",
    "category": "Geometry > Solid Geometry • Cylinder Volumetric Matrix",
    "url": "/geometry/cylinder/",
    "keywords": [
      "cylinder",
      "volume",
      "surface",
      "area",
      "calculator",
      "calculate",
      "lateral",
      "curved",
      "total",
      "and",
      "base",
      "perimeter"
    ]
  },
  {
    "title": "Right Circular Cone Volume & Slant Height Calculator",
    "category": "Geometry > Conical Geometry • Right Cone Matrix",
    "url": "/geometry/cone/",
    "keywords": [
      "right",
      "circular",
      "cone",
      "volume",
      "slant",
      "height",
      "calculator",
      "calculate",
      "lateral",
      "area",
      "total",
      "surface"
    ]
  },
  {
    "title": "Sphere Volume & Surface Area Calculator",
    "category": "Geometry > Spherical Geometry • Archimedean Sphere Matrix",
    "url": "/geometry/sphere/",
    "keywords": [
      "sphere",
      "volume",
      "surface",
      "area",
      "calculator",
      "calculate",
      "exact",
      "radius",
      "diameter",
      "and",
      "circumscribed",
      "cylinder"
    ]
  },
  {
    "title": "Torus Volume & Surface Area (Donut) Calculator",
    "category": "Geometry > Topology & Solids • Pappus Toroid Matrix",
    "url": "/geometry/torus/",
    "keywords": [
      "torus",
      "volume",
      "surface",
      "area",
      "donut",
      "calculator",
      "calculate",
      "and",
      "using",
      "pappus",
      "centroid",
      "theorems"
    ]
  },
  {
    "title": "Triangular Prism Volume & Surface Area Calculator",
    "category": "Geometry > Polyhedral Geometry • Triangular Prism Matrix",
    "url": "/geometry/triangular-prism/",
    "keywords": [
      "triangular",
      "prism",
      "volume",
      "surface",
      "area",
      "calculator",
      "calculate",
      "lateral",
      "face",
      "base",
      "and",
      "total"
    ]
  },
  {
    "title": "Square Pyramid Volume & Slant Height Calculator",
    "category": "Geometry > Pyramidal Geometry • Square Pyramid Matrix",
    "url": "/geometry/pyramid/",
    "keywords": [
      "square",
      "pyramid",
      "volume",
      "slant",
      "height",
      "calculator",
      "calculate",
      "and",
      "rectangular",
      "lateral",
      "face",
      "area"
    ]
  },
  {
    "title": "Frustum of a Cone (Truncated Cone) Calculator",
    "category": "Geometry > Truncated Solids • Conical Frustum Matrix",
    "url": "/geometry/frustum-cone/",
    "keywords": [
      "frustum",
      "cone",
      "truncated",
      "calculator",
      "calculate",
      "volume",
      "lateral",
      "surface",
      "area",
      "slant",
      "height",
      "and"
    ]
  },
  {
    "title": "Frustum of a Pyramid (Truncated Pyramid) Calculator",
    "category": "Geometry > Ancient Egyptian Geometry • Moscow Papyrus Matrix",
    "url": "/geometry/frustum-pyramid/",
    "keywords": [
      "frustum",
      "pyramid",
      "truncated",
      "calculator",
      "calculate",
      "volume",
      "slant",
      "height",
      "and",
      "surface",
      "area",
      "square"
    ]
  },
  {
    "title": "Ellipsoid Volume & Surface Area Calculator",
    "category": "Geometry > Triaxial Geometry • Ellipsoid Volumetric Solver",
    "url": "/geometry/ellipsoid/",
    "keywords": [
      "ellipsoid",
      "volume",
      "surface",
      "area",
      "calculator",
      "calculate",
      "and",
      "using",
      "the",
      "knud",
      "thomsen",
      "p-norm"
    ]
  },
  {
    "title": "Arc Length, Sector Area & Chord Calculator",
    "category": "Geometry > Trigonometry • Circular Arc & Sector Matrix",
    "url": "/geometry/arc-length/",
    "keywords": [
      "arc",
      "length",
      "sector",
      "area",
      "chord",
      "calculator",
      "calculate",
      "circular",
      "segment",
      "and",
      "from",
      "circle"
    ]
  },
  {
    "title": "Projectile Motion & Ballistic Trajectory Calculator",
    "category": "Physics > Classical Kinematics • Ballistic Vector Matrix",
    "url": "/physics/projectile-motion/",
    "keywords": [
      "projectile",
      "motion",
      "ballistic",
      "trajectory",
      "calculator",
      "calculate",
      "flight",
      "maximum",
      "apogee",
      "height",
      "total",
      "hang"
    ]
  },
  {
    "title": "Kinetic Energy & Linear Momentum Calculator",
    "category": "Physics > Newtonian Mechanics • Kinetic Energy Matrix",
    "url": "/physics/kinetic-energy/",
    "keywords": [
      "kinetic",
      "energy",
      "linear",
      "momentum",
      "calculator",
      "calculate",
      "translational",
      "joules",
      "ft-lbs",
      "and",
      "relativistic",
      "velocity"
    ]
  },
  {
    "title": "Ohm's Law & Electrical Power (PIVR) Calculator",
    "category": "Physics > Electromagnetism • Four-Quadrant Ohm's Wheel",
    "url": "/physics/ohms-law/",
    "keywords": [
      "ohm",
      "law",
      "electrical",
      "power",
      "pivr",
      "calculator",
      "calculate",
      "voltage",
      "current",
      "resistance",
      "and",
      "with"
    ]
  },
  {
    "title": "Density, Mass & Volume Calculator",
    "category": "Physics > Continuum Mechanics • Density Invariant Matrix",
    "url": "/physics/density-mass-volume/",
    "keywords": [
      "density",
      "mass",
      "volume",
      "calculator",
      "calculate",
      "material",
      "total",
      "and",
      "displacement",
      "with",
      "bidirectional",
      "inversions"
    ]
  },
  {
    "title": "Quadratic Formula & Parabola Vertex Calculator",
    "category": "Calculus > Algebraic Analysis • Quadratic Discriminant Matrix",
    "url": "/calculus/quadratic-formula/",
    "keywords": [
      "quadratic",
      "formula",
      "parabola",
      "vertex",
      "calculator",
      "calculate",
      "real",
      "and",
      "complex",
      "roots",
      "discriminant",
      "4ac"
    ]
  },
  {
    "title": "Standard Deviation & Variance Calculator",
    "category": "Statistics > Statistical Inference • Variance & Dispersion Matrix",
    "url": "/statistics/standard-deviation/",
    "keywords": [
      "standard",
      "deviation",
      "variance",
      "calculator",
      "calculate",
      "sample",
      "and",
      "population",
      "arithmetic",
      "mean",
      "sum",
      "squared"
    ]
  },
  {
    "title": "Z-Score & Standard Normal Distribution Calculator",
    "category": "Statistics > Gaussian Statistics • Standard Normal Matrix",
    "url": "/statistics/z-score/",
    "keywords": [
      "z-score",
      "standard",
      "normal",
      "distribution",
      "calculator",
      "calculate",
      "score",
      "cumulative",
      "probability",
      "two-tailed",
      "p-value",
      "and"
    ]
  },
  {
    "title": "Permutations & Combinations (nPr & nCr) Calculator",
    "category": "Statistics > Combinatorics • Discrete Math Matrix",
    "url": "/statistics/permutations-combinations/",
    "keywords": [
      "permutations",
      "combinations",
      "npr",
      "ncr",
      "calculator",
      "calculate",
      "factorials",
      "ordered",
      "and",
      "unordered",
      "binomial",
      "coefficients"
    ]
  },
  {
    "title": "Bayes' Theorem & Conditional Probability Calculator",
    "category": "Statistics > Epistemology & Probability • Bayesian Update Matrix",
    "url": "/statistics/bayes-theorem/",
    "keywords": [
      "bayes",
      "theorem",
      "conditional",
      "probability",
      "calculator",
      "calculate",
      "posterior",
      "prior",
      "odds",
      "likelihood",
      "ratio",
      "and"
    ]
  },
  {
    "title": "2×2 Matrix Determinant & Inverse Calculator",
    "category": "Calculus > Linear Algebra • Matrix Determinant Matrix",
    "url": "/calculus/matrix-multiplication/",
    "keywords": [
      "matrix",
      "determinant",
      "inverse",
      "calculator",
      "calculate",
      "det",
      "trace",
      "characteristic",
      "polynomial",
      "and",
      "eigenvalues",
      "matrix-multiplication"
    ]
  },
  {
    "title": "Simple Pendulum Period & Harmonic Frequency Calculator",
    "category": "Physics > Harmonic Oscillations • Pendulum Dynamics Matrix",
    "url": "/physics/pendulum-period/",
    "keywords": [
      "simple",
      "pendulum",
      "period",
      "harmonic",
      "frequency",
      "calculator",
      "calculate",
      "natural",
      "angular",
      "rad",
      "and",
      "local"
    ]
  },
  {
    "title": "Customer Acquisition Cost (CAC) Calculator",
    "category": "Finance > B2B SaaS Metrics • CAC Unit Economics",
    "url": "/finance/cac/",
    "keywords": [
      "customer",
      "acquisition",
      "cost",
      "cac",
      "calculator",
      "calculate",
      "blended",
      "and",
      "paid",
      "from",
      "total",
      "sales"
    ]
  },
  {
    "title": "Customer Lifetime Value (LTV / CLV) Calculator",
    "category": "Finance > SaaS Unit Economics • LTV Vector Matrix",
    "url": "/finance/clv-ltv/",
    "keywords": [
      "customer",
      "lifetime",
      "value",
      "ltv",
      "clv",
      "calculator",
      "calculate",
      "from",
      "average",
      "revenue",
      "per",
      "account"
    ]
  },
  {
    "title": "LTV:CAC Ratio & Payback Period Calculator",
    "category": "Finance > Venture Capital • Capital Efficiency Matrix",
    "url": "/finance/ltv-cac-ratio/",
    "keywords": [
      "ltv",
      "cac",
      "ratio",
      "payback",
      "period",
      "calculator",
      "calculate",
      "the",
      "gold-standard",
      "saas",
      "unit",
      "economics"
    ]
  },
  {
    "title": "Customer & Revenue Churn Rate Calculator",
    "category": "Finance > Retention Engineering • Churn Matrix",
    "url": "/finance/churn-rate/",
    "keywords": [
      "customer",
      "revenue",
      "churn",
      "rate",
      "calculator",
      "calculate",
      "logo",
      "gross",
      "net",
      "retention",
      "nrr",
      "and"
    ]
  },
  {
    "title": "MRR to ARR & Net New MRR Calculator",
    "category": "Finance > Subscription Economics • Recurring Revenue Matrix",
    "url": "/finance/mrr-arr/",
    "keywords": [
      "mrr",
      "arr",
      "net",
      "new",
      "calculator",
      "calculate",
      "annual",
      "recurring",
      "revenue",
      "run",
      "rate",
      "expansion"
    ]
  },
  {
    "title": "Startup Cash Runway & Burn Rate Calculator",
    "category": "Finance > Startup Treasury • Cash Runway Vector",
    "url": "/finance/runway-burn/",
    "keywords": [
      "startup",
      "cash",
      "runway",
      "burn",
      "rate",
      "calculator",
      "calculate",
      "net",
      "monthly",
      "gross",
      "outflows",
      "and"
    ]
  },
  {
    "title": "SaaS Magic Number & Sales Efficiency Calculator",
    "category": "Finance > Growth Engineering • Magic Number Matrix",
    "url": "/finance/saas-magic-number/",
    "keywords": [
      "saas",
      "magic",
      "number",
      "sales",
      "efficiency",
      "calculator",
      "calculate",
      "the",
      "measuring",
      "net",
      "new",
      "arr"
    ]
  },
  {
    "title": "SaaS Rule of 40 Calculator",
    "category": "Finance > Public SaaS Valuation • Rule of 40 Matrix",
    "url": "/finance/saas-rule-of-40/",
    "keywords": [
      "saas",
      "rule",
      "calculator",
      "calculate",
      "the",
      "score",
      "balancing",
      "yoy",
      "arr",
      "revenue",
      "growth",
      "rate"
    ]
  },
  {
    "title": "Net Promoter Score (NPS) Calculator",
    "category": "Finance > Customer Experience • NPS Matrix",
    "url": "/finance/net-promoter-score/",
    "keywords": [
      "net",
      "promoter",
      "score",
      "nps",
      "calculator",
      "calculate",
      "promoters",
      "9-10",
      "passives",
      "7-8",
      "detractors",
      "0-6"
    ]
  },
  {
    "title": "Average Revenue Per User (ARPU / ARPA) Calculator",
    "category": "Finance > Monetization Analytics • ARPU Solver",
    "url": "/finance/arpu/",
    "keywords": [
      "average",
      "revenue",
      "per",
      "user",
      "arpu",
      "arpa",
      "calculator",
      "calculate",
      "and",
      "account",
      "across",
      "monthly"
    ]
  },
  {
    "title": "Viral Coefficient (K-Factor) & Growth Calculator",
    "category": "Finance > Growth Loops • K-Factor Matrix",
    "url": "/finance/viral-coefficient/",
    "keywords": [
      "viral",
      "coefficient",
      "k-factor",
      "growth",
      "calculator",
      "calculate",
      "expansion",
      "cycle",
      "time",
      "customer",
      "compounding",
      "multiplier"
    ]
  },
  {
    "title": "Employee Turnover & Replacement Cost Calculator",
    "category": "Finance > HR Economics • Turnover Cost Matrix",
    "url": "/finance/employee-turnover-cost/",
    "keywords": [
      "employee",
      "turnover",
      "replacement",
      "cost",
      "calculator",
      "calculate",
      "true",
      "financial",
      "and",
      "organizational",
      "recruiting",
      "fees"
    ]
  },
  {
    "title": "Return on Ad Spend (ROAS) & Breakeven Calculator",
    "category": "Finance > Performance Marketing • ROAS Matrix",
    "url": "/finance/roas/",
    "keywords": [
      "return",
      "spend",
      "roas",
      "breakeven",
      "calculator",
      "calculate",
      "from",
      "product",
      "profit",
      "margin",
      "net",
      "advertising"
    ]
  },
  {
    "title": "Cost Per Acquisition (CPA) from CPC Calculator",
    "category": "Finance > Digital Advertising • CPA Unit Economics",
    "url": "/finance/cpa-cpc/",
    "keywords": [
      "cost",
      "per",
      "acquisition",
      "cpa",
      "from",
      "cpc",
      "calculator",
      "calculate",
      "click",
      "and",
      "landing",
      "page"
    ]
  },
  {
    "title": "Email Marketing Campaign ROI Calculator",
    "category": "Finance > Direct Response • Email ROI Matrix",
    "url": "/finance/email-marketing-roi/",
    "keywords": [
      "email",
      "marketing",
      "campaign",
      "roi",
      "calculator",
      "calculate",
      "open",
      "rates",
      "click-through",
      "ctr",
      "conversion",
      "yields"
    ]
  },
  {
    "title": "Sales Pipeline Velocity Calculator",
    "category": "Finance > Enterprise Sales • Pipeline Velocity Matrix",
    "url": "/finance/sales-pipeline-velocity/",
    "keywords": [
      "sales",
      "pipeline",
      "velocity",
      "calculator",
      "calculate",
      "revenue",
      "generated",
      "per",
      "day",
      "and",
      "forecast",
      "monthly"
    ]
  },
  {
    "title": "Working Capital & Current Ratio Calculator",
    "category": "Finance > Corporate Treasury • Liquidity Solvency Matrix",
    "url": "/finance/working-capital-ratio/",
    "keywords": [
      "working",
      "capital",
      "current",
      "ratio",
      "calculator",
      "calculate",
      "net",
      "nwc",
      "and",
      "short-term",
      "corporate",
      "liquidity"
    ]
  },
  {
    "title": "Quick Ratio (Acid-Test) Calculator",
    "category": "Finance > Balance Sheet Analysis • Acid-Test Matrix",
    "url": "/finance/quick-ratio/",
    "keywords": [
      "quick",
      "ratio",
      "acid-test",
      "calculator",
      "calculate",
      "the",
      "isolating",
      "liquid",
      "cash",
      "marketable",
      "securities",
      "and"
    ]
  },
  {
    "title": "Corporate DSCR & Interest Coverage Calculator",
    "category": "Finance > Credit Underwriting • Commercial Debt Coverage",
    "url": "/finance/debt-service-coverage/",
    "keywords": [
      "corporate",
      "dscr",
      "interest",
      "coverage",
      "calculator",
      "calculate",
      "debt",
      "service",
      "ratio",
      "and",
      "times",
      "earned"
    ]
  },
  {
    "title": "Economic Order Quantity (EOQ) & Reorder Point Calculator",
    "category": "Finance > Supply Chain & Operations • Ford-Harris EOQ Model",
    "url": "/finance/economic-order-quantity/",
    "keywords": [
      "economic",
      "order",
      "quantity",
      "eoq",
      "reorder",
      "point",
      "calculator",
      "calculate",
      "optimal",
      "inventory",
      "batch",
      "size"
    ]
  },
  {
    "title": "Bessemer Burn Multiple Calculator",
    "category": "Finance > Venture Efficiency • Bessemer Burn Multiple",
    "url": "/finance/burn-multiple/",
    "keywords": [
      "bessemer",
      "burn",
      "multiple",
      "calculator",
      "calculate",
      "the",
      "venture",
      "partners",
      "measuring",
      "net",
      "cash",
      "burned"
    ]
  },
  {
    "title": "Freemium to Paid Conversion Calculator",
    "category": "Finance > Product-Led Growth • PLG Funnel Matrix",
    "url": "/finance/freemium-conversion/",
    "keywords": [
      "freemium",
      "paid",
      "conversion",
      "calculator",
      "calculate",
      "user",
      "rates",
      "free-to-paid",
      "funnel",
      "velocity",
      "monthly",
      "recurring"
    ]
  },
  {
    "title": "Gross Revenue Retention (GRR) vs NRR Calculator",
    "category": "Finance > Retention Analytics • GRR Foundation Matrix",
    "url": "/finance/gross-revenue-retention/",
    "keywords": [
      "gross",
      "revenue",
      "retention",
      "grr",
      "nrr",
      "calculator",
      "calculate",
      "isolating",
      "core",
      "churn",
      "and",
      "contraction"
    ]
  },
  {
    "title": "SaaS CAC Payback Period Calculator",
    "category": "Finance > Unit Economics • Payback Horizon Matrix",
    "url": "/finance/cac-payback/",
    "keywords": [
      "saas",
      "cac",
      "payback",
      "period",
      "calculator",
      "calculate",
      "exact",
      "customer",
      "acquisition",
      "cost",
      "months",
      "accounting"
    ]
  },
  {
    "title": "Inventory Turnover & Days Sales of Inventory (DSI) Calculator",
    "category": "Finance > Working Capital • Inventory Velocity",
    "url": "/finance/inventory-turnover/",
    "keywords": [
      "inventory",
      "turnover",
      "days",
      "sales",
      "dsi",
      "calculator",
      "calculate",
      "ratio",
      "dio",
      "and",
      "capital",
      "tied"
    ]
  },
  {
    "title": "Car Lease vs Buy Financial Comparison Calculator",
    "category": "Finance > Automotive Finance • Lease vs Purchase Matrix",
    "url": "/finance/lease-vs-buy/",
    "keywords": [
      "car",
      "lease",
      "buy",
      "financial",
      "comparison",
      "calculator",
      "compare",
      "the",
      "total",
      "multi-year",
      "cost",
      "leasing"
    ]
  },
  {
    "title": "Electric Vehicle (EV) Charging Cost & Range Calculator",
    "category": "Physics > Electric Mobility • EV Energy Economics",
    "url": "/physics/ev-charging-cost/",
    "keywords": [
      "electric",
      "vehicle",
      "charging",
      "cost",
      "range",
      "calculator",
      "calculate",
      "exact",
      "dollar",
      "fully",
      "charge",
      "car"
    ]
  },
  {
    "title": "Electric Vehicle vs Gas Savings Calculator",
    "category": "Finance > Fleet Decarbonization • EV vs ICE Fuel Economics",
    "url": "/finance/ev-vs-gas-savings/",
    "keywords": [
      "electric",
      "vehicle",
      "gas",
      "savings",
      "calculator",
      "calculate",
      "annual",
      "fuel",
      "maintenance",
      "and",
      "brake",
      "pad"
    ]
  },
  {
    "title": "Car Depreciation & Future Value Curve Calculator",
    "category": "Finance > Automotive Asset Valuation • Depreciation Curve Matrix",
    "url": "/finance/car-depreciation/",
    "keywords": [
      "car",
      "depreciation",
      "future",
      "value",
      "curve",
      "calculator",
      "calculate",
      "multi-year",
      "vehicle",
      "curves",
      "month-by-month",
      "residual"
    ]
  },
  {
    "title": "5-Year True Cost to Own (TCO) Calculator",
    "category": "Finance > Fleet Economics • Full Vehicle TCO Matrix",
    "url": "/finance/true-cost-to-own/",
    "keywords": [
      "5-year",
      "true",
      "cost",
      "own",
      "tco",
      "calculator",
      "calculate",
      "full",
      "vehicle",
      "over",
      "years",
      "combining"
    ]
  },
  {
    "title": "Vehicle Towing Capacity & Tongue Weight Calculator",
    "category": "Physics > Vehicle Dynamics • Safe Towing Matrix",
    "url": "/physics/towing-capacity/",
    "keywords": [
      "vehicle",
      "towing",
      "capacity",
      "tongue",
      "weight",
      "calculator",
      "calculate",
      "safe",
      "legal",
      "gross",
      "combined",
      "rating"
    ]
  },
  {
    "title": "Truck Payload Capacity & Cargo Safety Margin Calculator",
    "category": "Physics > Truck Engineering • Payload GVWR Matrix",
    "url": "/physics/payload-capacity/",
    "keywords": [
      "truck",
      "payload",
      "capacity",
      "cargo",
      "safety",
      "margin",
      "calculator",
      "calculate",
      "actual",
      "remaining",
      "from",
      "gross"
    ]
  },
  {
    "title": "Gas Mileage (MPG / L/100km) & Fuel Cost Calculator",
    "category": "Physics > Fuel Economy • Multi-Standard Metric Matrix",
    "url": "/physics/gas-mileage-mpg/",
    "keywords": [
      "gas",
      "mileage",
      "mpg",
      "100km",
      "fuel",
      "cost",
      "calculator",
      "calculate",
      "exact",
      "imperial",
      "and",
      "liters"
    ]
  },
  {
    "title": "Tire Size Comparison & Speedometer Error Calculator",
    "category": "Physics > Tire Dynamics • Speedometer Calibration Matrix",
    "url": "/physics/tire-size-speedometer/",
    "keywords": [
      "tire",
      "size",
      "comparison",
      "speedometer",
      "error",
      "calculator",
      "calculate",
      "diameter",
      "sidewall",
      "height",
      "revolutions",
      "per"
    ]
  },
  {
    "title": "Horsepower & Torque Conversion Calculator",
    "category": "Physics > Mechanical Power • Drivetrain Physics Matrix",
    "url": "/physics/horsepower-torque/",
    "keywords": [
      "horsepower",
      "torque",
      "conversion",
      "calculator",
      "convert",
      "between",
      "rotational",
      "lb-ft",
      "and",
      "mechanical",
      "any",
      "engine"
    ]
  },
  {
    "title": "Quarter-Mile Elapsed Time (ET) & Trap Speed Calculator",
    "category": "Physics > Motorsports Dynamics • 1/4 Mile ET Matrix",
    "url": "/physics/quarter-mile-speed/",
    "keywords": [
      "quarter-mile",
      "elapsed",
      "time",
      "trap",
      "speed",
      "calculator",
      "calculate",
      "drag",
      "racing",
      "mile",
      "and",
      "finish"
    ]
  },
  {
    "title": "Engine Displacement & Cylinder Volume Calculator",
    "category": "Physics > Engine Building • Displacement Geometry",
    "url": "/physics/engine-displacement/",
    "keywords": [
      "engine",
      "displacement",
      "cylinder",
      "volume",
      "calculator",
      "calculate",
      "total",
      "internal",
      "combustion",
      "cubic",
      "centimeters",
      "liters"
    ]
  },
  {
    "title": "Engine Static Compression Ratio Calculator",
    "category": "Physics > Combustion Engineering • Static CR Matrix",
    "url": "/physics/compression-ratio/",
    "keywords": [
      "engine",
      "static",
      "compression",
      "ratio",
      "calculator",
      "calculate",
      "from",
      "cylinder",
      "swept",
      "volume",
      "combustion",
      "chamber"
    ]
  },
  {
    "title": "Transmission Gear Ratio & Vehicle Speed at RPM Calculator",
    "category": "Physics > Drivetrain Kinematics • Gear Speed Matrix",
    "url": "/physics/gear-ratio-speed/",
    "keywords": [
      "transmission",
      "gear",
      "ratio",
      "vehicle",
      "speed",
      "rpm",
      "calculator",
      "calculate",
      "road",
      "mph",
      "any",
      "engine"
    ]
  },
  {
    "title": "Marine Boat Fuel Burn & Range Calculator",
    "category": "Physics > Marine Engineering • Boat Fuel Matrix",
    "url": "/physics/boat-fuel-burn/",
    "keywords": [
      "marine",
      "boat",
      "fuel",
      "burn",
      "range",
      "calculator",
      "calculate",
      "rate",
      "gallons",
      "per",
      "hour",
      "gph"
    ]
  },
  {
    "title": "Aviation Crosswind & Headwind Component Calculator",
    "category": "Physics > Flight Operations • Crosswind Component Matrix",
    "url": "/physics/aviation-crosswind/",
    "keywords": [
      "aviation",
      "crosswind",
      "headwind",
      "component",
      "calculator",
      "calculate",
      "exact",
      "runway",
      "and",
      "tailwind",
      "from",
      "wind"
    ]
  },
  {
    "title": "Aircraft Rate of Climb & Climb Gradient Calculator",
    "category": "Physics > Aviation Engineering • Climb Gradient Matrix",
    "url": "/physics/aircraft-climb-rate/",
    "keywords": [
      "aircraft",
      "rate",
      "climb",
      "gradient",
      "calculator",
      "convert",
      "between",
      "vertical",
      "speed",
      "feet",
      "per",
      "minute"
    ]
  },
  {
    "title": "RV & Marine Battery Amp Hour & Inverter Runtime Calculator",
    "category": "Physics > Off-Grid Power • Battery Capacity Matrix",
    "url": "/physics/battery-amp-hours/",
    "keywords": [
      "marine",
      "battery",
      "amp",
      "hour",
      "inverter",
      "runtime",
      "calculator",
      "calculate",
      "deep",
      "cycle",
      "hours",
      "from"
    ]
  },
  {
    "title": "Vehicle Vinyl Wrap Material & Roll Calculator",
    "category": "Physics > Automotive Aesthetics • Vinyl Film Roll Matrix",
    "url": "/physics/car-wrap-vinyl/",
    "keywords": [
      "vehicle",
      "vinyl",
      "wrap",
      "material",
      "roll",
      "calculator",
      "calculate",
      "exact",
      "linear",
      "feet",
      "and",
      "square"
    ]
  },
  {
    "title": "Vehicle Braking & Stopping Distance Physics Calculator",
    "category": "Physics > Accident Reconstruction • Braking Distance Matrix",
    "url": "/physics/brake-stopping-distance/",
    "keywords": [
      "vehicle",
      "braking",
      "stopping",
      "distance",
      "physics",
      "calculator",
      "calculate",
      "total",
      "feet",
      "from",
      "initial",
      "speed"
    ]
  },
  {
    "title": "Vehicle Sales Tax & Trade-In Credit Calculator",
    "category": "Finance > Automotive Tax • Trade-In Deduction Matrix",
    "url": "/finance/car-sales-tax/",
    "keywords": [
      "vehicle",
      "sales",
      "tax",
      "trade-in",
      "credit",
      "calculator",
      "calculate",
      "state",
      "county",
      "and",
      "local",
      "registration"
    ]
  },
  {
    "title": "Auto Loan Refinance Savings Calculator",
    "category": "Finance > Consumer Lending • Auto Loan Refinance Matrix",
    "url": "/finance/auto-refinance-savings/",
    "keywords": [
      "auto",
      "loan",
      "refinance",
      "savings",
      "calculator",
      "calculate",
      "monthly",
      "payment",
      "reduction",
      "and",
      "lifetime",
      "interest"
    ]
  },
  {
    "title": "Auto GAP Insurance Need & Negative Equity Calculator",
    "category": "Finance > Risk Underwriting • GAP Insurance Matrix",
    "url": "/finance/gap-insurance-need/",
    "keywords": [
      "auto",
      "gap",
      "insurance",
      "need",
      "negative",
      "equity",
      "calculator",
      "calculate",
      "exposure",
      "underwater",
      "loan",
      "comparing"
    ]
  },
  {
    "title": "Motor Oil Change Interval & Maintenance Cost Calculator",
    "category": "Physics > Fleet Maintenance • Lubrication Schedule Matrix",
    "url": "/physics/oil-change-interval/",
    "keywords": [
      "motor",
      "oil",
      "change",
      "interval",
      "maintenance",
      "cost",
      "calculator",
      "calculate",
      "optimal",
      "intervals",
      "based",
      "mileage"
    ]
  },
  {
    "title": "RV Travel Trailer Tongue & Hitch Distribution Calculator",
    "category": "Physics > RV Dynamics • Weight Distribution Matrix",
    "url": "/physics/rv-payload-hitch/",
    "keywords": [
      "travel",
      "trailer",
      "tongue",
      "hitch",
      "distribution",
      "calculator",
      "calculate",
      "weight",
      "transfer",
      "front",
      "steer",
      "axles"
    ]
  },
  {
    "title": "Commercial Real Estate IRR & Equity Multiple Calculator",
    "category": "Finance > Private Equity • Real Estate IRR Matrix",
    "url": "/finance/internal-rate-of-return/",
    "keywords": [
      "commercial",
      "real",
      "estate",
      "irr",
      "equity",
      "multiple",
      "calculator",
      "calculate",
      "property",
      "internal",
      "rate",
      "return"
    ]
  },
  {
    "title": "Commercial Real Estate NPV & DCF Calculator",
    "category": "Finance > Institutional Underwriting • Real Estate DCF Matrix",
    "url": "/finance/net-present-value/",
    "keywords": [
      "commercial",
      "real",
      "estate",
      "npv",
      "dcf",
      "calculator",
      "calculate",
      "net",
      "present",
      "value",
      "and",
      "discounted"
    ]
  },
  {
    "title": "Cash-on-Cash Return & Pre-Tax Yield Calculator",
    "category": "Finance > Real Estate Investing • Cash-on-Cash Matrix",
    "url": "/finance/cash-on-cash-return/",
    "keywords": [
      "cash-on-cash",
      "return",
      "pre-tax",
      "yield",
      "calculator",
      "calculate",
      "coc",
      "percentage",
      "measuring",
      "annual",
      "cash",
      "flow"
    ]
  },
  {
    "title": "Gross Rent Multiplier (GRM) & Valuation Calculator",
    "category": "Finance > Multifamily Screening • GRM Metric Matrix",
    "url": "/finance/gross-rent-multiplier/",
    "keywords": [
      "gross",
      "rent",
      "multiplier",
      "grm",
      "valuation",
      "calculator",
      "calculate",
      "and",
      "estimate",
      "fair",
      "market",
      "multifamily"
    ]
  },
  {
    "title": "Section 1031 Like-Kind Exchange & Tax Deferral Calculator",
    "category": "Finance > Tax Deferral • Section 1031 Matrix",
    "url": "/finance/exchange-1031/",
    "keywords": [
      "section",
      "1031",
      "like-kind",
      "exchange",
      "tax",
      "deferral",
      "calculator",
      "calculate",
      "deferred",
      "federal",
      "capital",
      "gains"
    ]
  },
  {
    "title": "Cap Rate Sensitivity & Valuation Matrix Calculator",
    "category": "Finance > Valuation Engineering • Cap Rate Sensitivity Matrix",
    "url": "/finance/cap-rate-sensitivity/",
    "keywords": [
      "cap",
      "rate",
      "sensitivity",
      "valuation",
      "matrix",
      "calculator",
      "calculate",
      "commercial",
      "property",
      "asset",
      "across",
      "varying"
    ]
  },
  {
    "title": "Commercial Rent Roll & Economic Vacancy Calculator",
    "category": "Finance > Property Management • Rent Roll Underwriting",
    "url": "/finance/rent-roll-analysis/",
    "keywords": [
      "commercial",
      "rent",
      "roll",
      "economic",
      "vacancy",
      "calculator",
      "analyze",
      "rolls",
      "gross",
      "potential",
      "gpr",
      "physical"
    ]
  },
  {
    "title": "Cost Segregation & Accelerated Depreciation Calculator",
    "category": "Finance > Tax Engineering • Cost Segregation Shield",
    "url": "/finance/cost-segregation/",
    "keywords": [
      "cost",
      "segregation",
      "accelerated",
      "depreciation",
      "calculator",
      "estimate",
      "year",
      "bonus",
      "tax",
      "deductions",
      "segregating",
      "commercial"
    ]
  },
  {
    "title": "Syndication Preferred Return & Waterfall Equity Calculator",
    "category": "Finance > Syndication Structuring • Equity Waterfall Matrix",
    "url": "/finance/preferred-return-waterfall/",
    "keywords": [
      "syndication",
      "preferred",
      "return",
      "waterfall",
      "equity",
      "calculator",
      "calculate",
      "private",
      "distributions",
      "between",
      "general",
      "partners"
    ]
  },
  {
    "title": "Triple Net (NNN) vs Full Service Gross Lease Calculator",
    "category": "Finance > Commercial Leasing • NNN vs Gross Matrix",
    "url": "/finance/commercial-lease-nnn/",
    "keywords": [
      "triple",
      "net",
      "nnn",
      "full",
      "service",
      "gross",
      "lease",
      "calculator",
      "compare",
      "commercial",
      "structures",
      "versus"
    ]
  },
  {
    "title": "Tenant Improvement (TI) Allowance & Amortization Calculator",
    "category": "Finance > Commercial Underwriting • TI Amortization Matrix",
    "url": "/finance/tenant-improvement/",
    "keywords": [
      "tenant",
      "improvement",
      "allowance",
      "amortization",
      "calculator",
      "calculate",
      "build-out",
      "costs",
      "landlord",
      "allowances",
      "per",
      "square"
    ]
  },
  {
    "title": "Short-Term Rental (Airbnb) Cash Flow & ADR Calculator",
    "category": "Finance > Hospitality Economics • STR Cash Flow Matrix",
    "url": "/finance/str-airbnb-cashflow/",
    "keywords": [
      "short-term",
      "rental",
      "airbnb",
      "cash",
      "flow",
      "adr",
      "calculator",
      "calculate",
      "str",
      "vrbo",
      "net",
      "monthly"
    ]
  },
  {
    "title": "Closing Day Property Tax Proration Calculator",
    "category": "Finance > Closing Escrow • Tax Proration Matrix",
    "url": "/finance/property-tax-proration/",
    "keywords": [
      "closing",
      "day",
      "property",
      "tax",
      "proration",
      "calculator",
      "calculate",
      "exact",
      "real",
      "estate",
      "prorations",
      "daily"
    ]
  },
  {
    "title": "House Flipping 70% Rule & MAO Calculator",
    "category": "Finance > Real Estate Wholesaling • 70% Rule Matrix",
    "url": "/finance/house-flip-profit/",
    "keywords": [
      "house",
      "flipping",
      "rule",
      "mao",
      "calculator",
      "calculate",
      "maximum",
      "allowable",
      "offer",
      "for",
      "fix-and-flip",
      "real"
    ]
  },
  {
    "title": "Land Subdivision & Development Lot Yield Calculator",
    "category": "Finance > Civil Engineering • Land Subdivision Matrix",
    "url": "/finance/land-development-yield/",
    "keywords": [
      "land",
      "subdivision",
      "development",
      "lot",
      "yield",
      "calculator",
      "calculate",
      "residential",
      "yields",
      "infrastructure",
      "loss",
      "deductions"
    ]
  },
  {
    "title": "Self-Storage Facility Feasibility & Revenue Calculator",
    "category": "Finance > Commercial Feasibility • Self-Storage Matrix",
    "url": "/finance/self-storage-roi/",
    "keywords": [
      "self-storage",
      "facility",
      "feasibility",
      "revenue",
      "calculator",
      "calculate",
      "rental",
      "net",
      "rentable",
      "square",
      "footage",
      "nrsf"
    ]
  },
  {
    "title": "Mobile Home Park (MHP) Lot Rent & Cap Rate Calculator",
    "category": "Finance > Affordable Housing • MHP Valuation Matrix",
    "url": "/finance/mobile-home-park/",
    "keywords": [
      "mobile",
      "home",
      "park",
      "mhp",
      "lot",
      "rent",
      "cap",
      "rate",
      "calculator",
      "calculate",
      "manufactured",
      "housing"
    ]
  },
  {
    "title": "Mezzanine Debt & Subordinated Financing Blended Cost Calculator",
    "category": "Finance > Capital Stack Structuring • Mezzanine Debt Matrix",
    "url": "/finance/mezzanine-debt/",
    "keywords": [
      "mezzanine",
      "debt",
      "subordinated",
      "financing",
      "blended",
      "cost",
      "calculator",
      "calculate",
      "weighted",
      "average",
      "capital",
      "wacc"
    ]
  },
  {
    "title": "Hard Money Loan Cost & Points Calculator",
    "category": "Finance > Private Lending • Hard Money APR Matrix",
    "url": "/finance/hard-money-points/",
    "keywords": [
      "hard",
      "money",
      "loan",
      "cost",
      "points",
      "calculator",
      "calculate",
      "total",
      "financing",
      "fees",
      "upfront",
      "origination"
    ]
  },
  {
    "title": "Commercial Bridge Loan Interest Reserve Calculator",
    "category": "Finance > Bridge Financing • Interest Reserve Matrix",
    "url": "/finance/bridge-loan-interest/",
    "keywords": [
      "commercial",
      "bridge",
      "loan",
      "interest",
      "reserve",
      "calculator",
      "calculate",
      "escrows",
      "floating",
      "sofr",
      "spreads",
      "and"
    ]
  },
  {
    "title": "Qualified Opportunity Zone (QOZ) Tax Incentive Calculator",
    "category": "Finance > Tax Policy • Opportunity Zone Matrix",
    "url": "/finance/opportunity-zone/",
    "keywords": [
      "qualified",
      "opportunity",
      "zone",
      "qoz",
      "tax",
      "incentive",
      "calculator",
      "calculate",
      "capital",
      "gains",
      "deferral",
      "and"
    ]
  },
  {
    "title": "HOA Reserve Fund Adequacy & Percent Funded Calculator",
    "category": "Finance > Condo Governance • Reserve Fund Matrix",
    "url": "/finance/hoa-reserve-fund/",
    "keywords": [
      "hoa",
      "reserve",
      "fund",
      "adequacy",
      "percent",
      "funded",
      "calculator",
      "calculate",
      "homeowners",
      "association",
      "condominium",
      "metric"
    ]
  },
  {
    "title": "Section 1250 Depreciation Recapture Tax Calculator",
    "category": "Finance > Tax Accounting • Section 1250 Matrix",
    "url": "/finance/depreciation-recapture/",
    "keywords": [
      "section",
      "1250",
      "depreciation",
      "recapture",
      "tax",
      "calculator",
      "calculate",
      "irs",
      "unrecaptured",
      "rate",
      "versus",
      "long-term"
    ]
  },
  {
    "title": "Real Estate GP Promoted Interest (Carried Interest) Calculator",
    "category": "Finance > Private Equity Structuring • GP Promote Matrix",
    "url": "/finance/promoted-interest-carry/",
    "keywords": [
      "real",
      "estate",
      "promoted",
      "interest",
      "carried",
      "calculator",
      "calculate",
      "general",
      "partner",
      "promote",
      "compensation",
      "across"
    ]
  },
  {
    "title": "Blended Mortgage Interest Rate & Second Loan Calculator",
    "category": "Finance > Debt Architecture • Blended APR Matrix",
    "url": "/finance/blended-mortgage-rate/",
    "keywords": [
      "blended",
      "mortgage",
      "interest",
      "rate",
      "second",
      "loan",
      "calculator",
      "calculate",
      "effective",
      "combining",
      "low-rate",
      "first"
    ]
  },
  {
    "title": "W-2 Employee vs 1099 Contractor Net Pay Calculator",
    "category": "Finance > Tax Optimization • W-2 vs 1099 Matrix",
    "url": "/finance/w2-vs-1099/",
    "keywords": [
      "w-2",
      "employee",
      "1099",
      "contractor",
      "net",
      "pay",
      "calculator",
      "compare",
      "take-home",
      "between",
      "employment",
      "and"
    ]
  },
  {
    "title": "Federal Paycheck Withholding & Net Pay Calculator",
    "category": "Finance > Payroll Engineering • Net Paycheck Matrix",
    "url": "/finance/paycheck-withholding/",
    "keywords": [
      "federal",
      "paycheck",
      "withholding",
      "net",
      "pay",
      "calculator",
      "calculate",
      "exact",
      "take-home",
      "after",
      "income",
      "tax"
    ]
  },
  {
    "title": "S-Corporation Reasonable Salary & Tax Savings Calculator",
    "category": "Finance > Corporate Tax Strategy • S-Corp FICA Matrix",
    "url": "/finance/s-corp-reasonable-salary/",
    "keywords": [
      "s-corporation",
      "reasonable",
      "salary",
      "tax",
      "savings",
      "calculator",
      "calculate",
      "annual",
      "fica",
      "self-employment",
      "from",
      "electing"
    ]
  },
  {
    "title": "Section 199A Qualified Business Income (QBI) Calculator",
    "category": "Finance > Pass-Through Tax Policy • Section 199A Matrix",
    "url": "/finance/qbi-deduction/",
    "keywords": [
      "section",
      "199a",
      "qualified",
      "business",
      "income",
      "qbi",
      "calculator",
      "calculate",
      "the",
      "deduction",
      "for",
      "pass-through"
    ]
  },
  {
    "title": "401(k) Employer Match & True Compensation Calculator",
    "category": "Finance > Retirement Planning • 401(k) Match Matrix",
    "url": "/finance/401k-employer-match/",
    "keywords": [
      "401",
      "employer",
      "match",
      "true",
      "compensation",
      "calculator",
      "calculate",
      "matching",
      "dollars",
      "required",
      "employee",
      "contribution"
    ]
  },
  {
    "title": "Mega Backdoor Roth IRA Contribution Calculator",
    "category": "Finance > High Net Worth • Mega Backdoor Roth Matrix",
    "url": "/finance/mega-backdoor-roth/",
    "keywords": [
      "mega",
      "backdoor",
      "roth",
      "ira",
      "contribution",
      "calculator",
      "calculate",
      "maximum",
      "allowable",
      "after-tax",
      "401",
      "contributions"
    ]
  },
  {
    "title": "Health Savings Account (HSA) Triple Tax Calculator",
    "category": "Finance > Tax Alpha • HSA Triple Tax Shield",
    "url": "/finance/hsa-triple-tax/",
    "keywords": [
      "health",
      "savings",
      "account",
      "hsa",
      "triple",
      "tax",
      "calculator",
      "calculate",
      "tax-deductible",
      "contributions",
      "tax-free",
      "investment"
    ]
  },
  {
    "title": "Healthcare FSA Contribution & Forfeiture Calculator",
    "category": "Finance > Healthcare Benefits • FSA Optimization Matrix",
    "url": "/finance/fsa-use-it-or-lose-it/",
    "keywords": [
      "healthcare",
      "fsa",
      "contribution",
      "forfeiture",
      "calculator",
      "calculate",
      "flexible",
      "spending",
      "account",
      "tax",
      "savings",
      "optimal"
    ]
  },
  {
    "title": "Child Tax Credit (CTC) & Phase-Out Calculator",
    "category": "Finance > Family Tax Policy • CTC Phase-Out Matrix",
    "url": "/finance/child-tax-credit/",
    "keywords": [
      "child",
      "tax",
      "credit",
      "ctc",
      "phase-out",
      "calculator",
      "calculate",
      "the",
      "federal",
      "000",
      "per",
      "refundable"
    ]
  },
  {
    "title": "Standard Deduction vs Itemized (Schedule A) Calculator",
    "category": "Finance > Tax Optimization • Schedule A Matrix",
    "url": "/finance/standard-vs-itemized/",
    "keywords": [
      "standard",
      "deduction",
      "itemized",
      "schedule",
      "calculator",
      "compare",
      "the",
      "against",
      "deductions",
      "mortgage",
      "interest",
      "10k"
    ]
  },
  {
    "title": "Marginal vs Effective Tax Rate Calculator",
    "category": "Finance > Tax Literacy • Progressive Bracket Matrix",
    "url": "/finance/marginal-vs-effective-tax/",
    "keywords": [
      "marginal",
      "effective",
      "tax",
      "rate",
      "calculator",
      "calculate",
      "progressive",
      "federal",
      "bracket",
      "tiers",
      "top",
      "versus"
    ]
  },
  {
    "title": "State Income Tax Relocation Comparison Calculator",
    "category": "Finance > Tax Migration • State Tax Arbitrage Matrix",
    "url": "/finance/state-income-tax-comparison/",
    "keywords": [
      "state",
      "income",
      "tax",
      "relocation",
      "comparison",
      "calculator",
      "compare",
      "annual",
      "liabilities",
      "between",
      "high-tax",
      "states"
    ]
  },
  {
    "title": "Tax-Loss Harvesting & Capital Gains Offset Calculator",
    "category": "Finance > Tax Alpha • Loss Harvesting Matrix",
    "url": "/finance/capital-gains-harvesting/",
    "keywords": [
      "tax-loss",
      "harvesting",
      "capital",
      "gains",
      "offset",
      "calculator",
      "calculate",
      "realized",
      "offsets",
      "using",
      "the",
      "irs"
    ]
  },
  {
    "title": "Section 179 Equipment Depreciation Calculator",
    "category": "Finance > Capital Expenditure • Section 179 Tax Shield",
    "url": "/finance/section-179-deduction/",
    "keywords": [
      "section",
      "179",
      "equipment",
      "depreciation",
      "calculator",
      "calculate",
      "immediate",
      "first-year",
      "expensing",
      "deductions",
      "220",
      "000"
    ]
  },
  {
    "title": "Section 168(k) Bonus Depreciation Phase-Down Calculator",
    "category": "Finance > Tax Accounting • Bonus Depreciation Schedule",
    "url": "/finance/bonus-depreciation/",
    "keywords": [
      "section",
      "168",
      "bonus",
      "depreciation",
      "phase-down",
      "calculator",
      "calculate",
      "under",
      "the",
      "tcja",
      "schedule",
      "2024"
    ]
  },
  {
    "title": "Restricted Stock Unit (RSU) Vesting Tax Calculator",
    "category": "Finance > Equity Compensation • RSU Vesting Matrix",
    "url": "/finance/rsu-vesting-tax/",
    "keywords": [
      "restricted",
      "stock",
      "unit",
      "rsu",
      "vesting",
      "tax",
      "calculator",
      "calculate",
      "income",
      "mandatory",
      "supplemental",
      "withholding"
    ]
  },
  {
    "title": "Employee Stock Purchase Plan (ESPP) Calculator",
    "category": "Finance > Equity Compensation • ESPP Alpha Matrix",
    "url": "/finance/espp-discount/",
    "keywords": [
      "employee",
      "stock",
      "purchase",
      "plan",
      "espp",
      "calculator",
      "calculate",
      "returns",
      "with",
      "discount",
      "and",
      "lookback"
    ]
  },
  {
    "title": "Net Unrealized Appreciation (NUA) 401(k) Stock Calculator",
    "category": "Finance > Retirement Distribution • NUA Strategy Matrix",
    "url": "/finance/nua-company-stock/",
    "keywords": [
      "net",
      "unrealized",
      "appreciation",
      "nua",
      "401",
      "stock",
      "calculator",
      "calculate",
      "tax",
      "savings",
      "employer",
      "inside"
    ]
  },
  {
    "title": "Rule 72(t) SEPP Early IRA Withdrawal Calculator",
    "category": "Finance > Early Retirement • Rule 72(t) SEPP Matrix",
    "url": "/finance/sepp-72t-distribution/",
    "keywords": [
      "rule",
      "sepp",
      "early",
      "ira",
      "withdrawal",
      "calculator",
      "calculate",
      "penalty-free",
      "retirement",
      "withdrawals",
      "from",
      "traditional"
    ]
  },
  {
    "title": "Charitable Remainder Unitrust (CRUT) Tax Calculator",
    "category": "Finance > High Net Worth • Philanthropic Tax Shield",
    "url": "/finance/charitable-remainder-trust/",
    "keywords": [
      "charitable",
      "remainder",
      "unitrust",
      "crut",
      "tax",
      "calculator",
      "calculate",
      "immediate",
      "upfront",
      "income",
      "deductions",
      "tax-free"
    ]
  },
  {
    "title": "Federal Estate & Lifetime Gift Tax Exemption Calculator",
    "category": "Finance > Wealth Preservation • Estate Tax Matrix",
    "url": "/finance/estate-gift-tax/",
    "keywords": [
      "federal",
      "estate",
      "lifetime",
      "gift",
      "tax",
      "exemption",
      "calculator",
      "calculate",
      "and",
      "exposure",
      "rate",
      "unified"
    ]
  },
  {
    "title": "Inherited IRA 10-Year Rule & RMD Calculator",
    "category": "Finance > Estate Distribution • SECURE Act 10-Year Matrix",
    "url": "/finance/inherited-ira-10-year/",
    "keywords": [
      "inherited",
      "ira",
      "10-year",
      "rule",
      "rmd",
      "calculator",
      "calculate",
      "secure",
      "act",
      "mandatory",
      "withdrawal",
      "schedules"
    ]
  },
  {
    "title": "Social Security Benefits Taxation Calculator",
    "category": "Finance > Retirement Taxation • Social Security Matrix",
    "url": "/finance/social-security-taxation/",
    "keywords": [
      "social",
      "security",
      "benefits",
      "taxation",
      "calculator",
      "calculate",
      "how",
      "much",
      "your",
      "retirement",
      "benefit",
      "subject"
    ]
  },
  {
    "title": "Medicare IRMAA Surcharge & Surtax Calculator",
    "category": "Finance > Healthcare Policy • Medicare IRMAA Matrix",
    "url": "/finance/medicare-irmaa-surcharge/",
    "keywords": [
      "medicare",
      "irmaa",
      "surcharge",
      "surtax",
      "calculator",
      "calculate",
      "part",
      "and",
      "income-related",
      "monthly",
      "adjustment",
      "amount"
    ]
  },
  {
    "title": "Employer FUTA & SUTA Unemployment Tax Calculator",
    "category": "Finance > Employer Payroll • Unemployment Tax Matrix",
    "url": "/finance/futa-suta-payroll/",
    "keywords": [
      "employer",
      "futa",
      "suta",
      "unemployment",
      "tax",
      "calculator",
      "calculate",
      "federal",
      "act",
      "net",
      "and",
      "state"
    ]
  },
  {
    "title": "Solar PV System Payback & ROI Calculator",
    "category": "Energy > Clean Energy • Solar Economics Matrix",
    "url": "/energy/solar-payback/",
    "keywords": [
      "solar",
      "system",
      "payback",
      "roi",
      "calculator",
      "calculate",
      "exact",
      "simple",
      "period",
      "net",
      "present",
      "value"
    ]
  },
  {
    "title": "Solar PV System Sizing & DC kW Array Calculator",
    "category": "Energy > Photovoltaic Sizing • System Capacity",
    "url": "/energy/solar-pv-sizing/",
    "keywords": [
      "solar",
      "system",
      "sizing",
      "array",
      "calculator",
      "determine",
      "the",
      "exact",
      "kilowatt",
      "rating",
      "and",
      "number"
    ]
  },
  {
    "title": "Home Battery Backup Duration & Storage Calculator",
    "category": "Energy > Energy Storage • Runtime Matrix",
    "url": "/energy/battery-backup-storage/",
    "keywords": [
      "home",
      "battery",
      "backup",
      "duration",
      "storage",
      "calculator",
      "calculate",
      "run-time",
      "hours",
      "and",
      "days",
      "for"
    ]
  },
  {
    "title": "Heat Pump Seasonal COP & HSPF2 Energy Savings Calculator",
    "category": "Energy > Thermal Efficiency • Heat Pump Matrix",
    "url": "/energy/heat-pump-cop-efficiency/",
    "keywords": [
      "heat",
      "pump",
      "seasonal",
      "cop",
      "hspf2",
      "energy",
      "savings",
      "calculator",
      "calculate",
      "operating",
      "electricity",
      "cost"
    ]
  },
  {
    "title": "EV Charging Load, Time & Electrical Panel Capacity Calculator",
    "category": "Energy > E-Mobility • Electrical Infrastructure",
    "url": "/energy/ev-charging-load/",
    "keywords": [
      "charging",
      "load",
      "time",
      "electrical",
      "panel",
      "capacity",
      "calculator",
      "calculate",
      "speed",
      "miles",
      "per",
      "hour"
    ]
  },
  {
    "title": "Solar Inverter Sizing & DC-to-AC Overload Clipping Ratio",
    "category": "Energy > Power Electronics • Inverter Optimization",
    "url": "/energy/solar-inverter-clipping/",
    "keywords": [
      "solar",
      "inverter",
      "sizing",
      "dc-to-ac",
      "overload",
      "clipping",
      "ratio",
      "calculate",
      "loading",
      "ilr",
      "annual",
      "energy"
    ]
  },
  {
    "title": "Commercial HVAC Chiller Tonnage & Cooling Load Calculator",
    "category": "Energy > Commercial HVAC • Hydronic Cooling",
    "url": "/energy/chiller-tonnage-cooling/",
    "keywords": [
      "commercial",
      "hvac",
      "chiller",
      "tonnage",
      "cooling",
      "load",
      "calculator",
      "calculate",
      "chilled",
      "water",
      "capacity",
      "refrigeration"
    ]
  },
  {
    "title": "3-Phase Power Factor Correction & Capacitor Sizing Calculator",
    "category": "Energy > Industrial Power • Reactive Compensation",
    "url": "/energy/power-factor-correction/",
    "keywords": [
      "3-phase",
      "power",
      "factor",
      "correction",
      "capacitor",
      "sizing",
      "calculator",
      "calculate",
      "required",
      "kvar",
      "bank",
      "size"
    ]
  },
  {
    "title": "Solar Net Metering & Utility Feed-in Tariff Calculator",
    "category": "Energy > Grid Economics • Solar Compensation",
    "url": "/energy/net-metering-credits/",
    "keywords": [
      "solar",
      "net",
      "metering",
      "utility",
      "feed-in",
      "tariff",
      "calculator",
      "calculate",
      "annual",
      "financial",
      "compensation",
      "under"
    ]
  },
  {
    "title": "Solar Panel Tilt & Azimuth Irradiance Optimizer",
    "category": "Energy > Solar Geometry • Irradiance Optimization",
    "url": "/energy/solar-tilt-azimuth/",
    "keywords": [
      "solar",
      "panel",
      "tilt",
      "azimuth",
      "irradiance",
      "optimizer",
      "calculate",
      "optimal",
      "fixed",
      "angle",
      "and",
      "orientation"
    ]
  },
  {
    "title": "Wind Turbine Power Curve & Betz Limit Kinetic Yield Calculator",
    "category": "Energy > Wind Energy • Fluid Dynamics",
    "url": "/energy/wind-turbine-power/",
    "keywords": [
      "wind",
      "turbine",
      "power",
      "curve",
      "betz",
      "limit",
      "kinetic",
      "yield",
      "calculator",
      "calculate",
      "theoretical",
      "and"
    ]
  },
  {
    "title": "3-Phase & Single-Phase Transformer kVA Rating Calculator",
    "category": "Energy > Electrical Distribution • Transformer Sizing",
    "url": "/energy/transformer-kva-rating/",
    "keywords": [
      "3-phase",
      "single-phase",
      "transformer",
      "kva",
      "rating",
      "calculator",
      "calculate",
      "full-load",
      "secondary",
      "current",
      "fla",
      "primary"
    ]
  },
  {
    "title": "Electrical Wire Gauge & Voltage Drop Calculator (NEC)",
    "category": "Energy > NEC Electrical Code • Conductor Sizing",
    "url": "/energy/wire-gauge-voltage-drop/",
    "keywords": [
      "electrical",
      "wire",
      "gauge",
      "voltage",
      "drop",
      "calculator",
      "nec",
      "calculate",
      "conductor",
      "percentage",
      "terminal",
      "and"
    ]
  },
  {
    "title": "Geothermal Heat Pump Ground Loop Borehole Length Calculator",
    "category": "Energy > Geothermal Energy • Borehole Engineering",
    "url": "/energy/geothermal-ground-loop/",
    "keywords": [
      "geothermal",
      "heat",
      "pump",
      "ground",
      "loop",
      "borehole",
      "length",
      "calculator",
      "calculate",
      "required",
      "vertical",
      "depth"
    ]
  },
  {
    "title": "Compressed Air CFM Leak Cost & Pneumatic Audit Calculator",
    "category": "Energy > Industrial Efficiency • Pneumatic Systems",
    "url": "/energy/compressed-air-leak-cfm/",
    "keywords": [
      "compressed",
      "air",
      "cfm",
      "leak",
      "cost",
      "pneumatic",
      "audit",
      "calculator",
      "calculate",
      "lost",
      "flow",
      "rate"
    ]
  },
  {
    "title": "Industrial Boiler Combustion Efficiency & Flue Heat Loss Calculator",
    "category": "Energy > Thermal Systems • Combustion Diagnostics",
    "url": "/energy/boiler-combustion-efficiency/",
    "keywords": [
      "industrial",
      "boiler",
      "combustion",
      "efficiency",
      "flue",
      "heat",
      "loss",
      "calculator",
      "calculate",
      "thermal",
      "dry",
      "gas"
    ]
  },
  {
    "title": "Standby Generator kW vs Starting kVA Sizing Calculator",
    "category": "Energy > Emergency Power • Standby Generation",
    "url": "/energy/generator-kw-kva-sizing/",
    "keywords": [
      "standby",
      "generator",
      "starting",
      "kva",
      "sizing",
      "calculator",
      "calculate",
      "emergency",
      "accounting",
      "for",
      "locked",
      "rotor"
    ]
  },
  {
    "title": "Commercial LED Lighting Lumen-to-Watt Retrofit ROI Calculator",
    "category": "Energy > Energy Efficiency • Lighting Systems",
    "url": "/energy/led-lighting-retrofit/",
    "keywords": [
      "commercial",
      "led",
      "lighting",
      "lumen-to-watt",
      "retrofit",
      "roi",
      "calculator",
      "calculate",
      "electrical",
      "energy",
      "savings",
      "hvac"
    ]
  },
  {
    "title": "Variable Frequency Drive (VFD) Pump Affinity Law Savings Calculator",
    "category": "Energy > Fluid Machinery • Affinity Laws",
    "url": "/energy/vfd-pump-savings/",
    "keywords": [
      "variable",
      "frequency",
      "drive",
      "vfd",
      "pump",
      "affinity",
      "law",
      "savings",
      "calculator",
      "calculate",
      "electrical",
      "energy"
    ]
  },
  {
    "title": "Solar Thermal Domestic Water Heating Collector BTU Sizing",
    "category": "Energy > Solar Thermal • Hydronic Engineering",
    "url": "/energy/solar-thermal-water-heater/",
    "keywords": [
      "solar",
      "thermal",
      "domestic",
      "water",
      "heating",
      "collector",
      "btu",
      "sizing",
      "calculate",
      "required",
      "flat",
      "plate"
    ]
  },
  {
    "title": "Heating & Cooling Degree Days (HDD / CDD) Thermal Audit Calculator",
    "category": "Energy > Building Physics • Climatological Modeling",
    "url": "/energy/degree-days-energy-audit/",
    "keywords": [
      "heating",
      "cooling",
      "degree",
      "days",
      "hdd",
      "cdd",
      "thermal",
      "audit",
      "calculator",
      "calculate",
      "weather-normalized",
      "annual"
    ]
  },
  {
    "title": "Battery Cycle Life vs Depth of Discharge (DoD) Degradation Calculator",
    "category": "Energy > Battery Science • Degradation Modeling",
    "url": "/energy/battery-cycle-life-dod/",
    "keywords": [
      "battery",
      "cycle",
      "life",
      "depth",
      "discharge",
      "dod",
      "degradation",
      "calculator",
      "calculate",
      "total",
      "lifetime",
      "kilowatt-hour"
    ]
  },
  {
    "title": "Off-Grid Diesel & Propane Generator Fuel Consumption Calculator",
    "category": "Energy > Off-Grid Power • Fuel Logistics",
    "url": "/energy/offgrid-generator-fuel/",
    "keywords": [
      "off-grid",
      "diesel",
      "propane",
      "generator",
      "fuel",
      "consumption",
      "calculator",
      "calculate",
      "hourly",
      "gallons",
      "run-time",
      "tank"
    ]
  },
  {
    "title": "Electrical Power Quality Total Harmonic Distortion (THD) Calculator",
    "category": "Energy > Power Quality • IEEE 519 Standards",
    "url": "/energy/harmonic-distortion-thd/",
    "keywords": [
      "electrical",
      "power",
      "quality",
      "total",
      "harmonic",
      "distortion",
      "thd",
      "calculator",
      "calculate",
      "for",
      "voltage",
      "and"
    ]
  },
  {
    "title": "Data Center Power Usage Effectiveness (PUE) & Efficiency Calculator",
    "category": "Energy > Cloud Infrastructure • Data Center Energy",
    "url": "/energy/data-center-pue/",
    "keywords": [
      "data",
      "center",
      "power",
      "usage",
      "effectiveness",
      "pue",
      "efficiency",
      "calculator",
      "calculate",
      "infrastructure",
      "dcie",
      "wasted"
    ]
  },
  {
    "title": "Dimensional Weight (DIM Factor 139 / 166) Calculator",
    "category": "Logistics > Parcel Logistics • Volumetric Rating",
    "url": "/logistics/dim-weight-calculator/",
    "keywords": [
      "dimensional",
      "weight",
      "dim",
      "factor",
      "139",
      "166",
      "calculator",
      "calculate",
      "volumetric",
      "billable",
      "and",
      "carrier"
    ]
  },
  {
    "title": "Pallet Ti-Hi & Carton Stacking Pattern Calculator",
    "category": "Logistics > Warehousing • Palletization Matrix",
    "url": "/logistics/pallet-ti-hi-optimizer/",
    "keywords": [
      "pallet",
      "ti-hi",
      "carton",
      "stacking",
      "pattern",
      "calculator",
      "calculate",
      "optimal",
      "tie",
      "cases",
      "per",
      "layer"
    ]
  },
  {
    "title": "Freight Density & NMFC Freight Class Calculator",
    "category": "Logistics > LTL Freight • NMFC Classification",
    "url": "/logistics/freight-density-nmfc/",
    "keywords": [
      "freight",
      "density",
      "nmfc",
      "class",
      "calculator",
      "calculate",
      "shipment",
      "pounds",
      "per",
      "cubic",
      "foot",
      "pcf"
    ]
  },
  {
    "title": "Full Truckload (FTL) vs Less-Than-Truckload (LTL) Cost Breakeven",
    "category": "Logistics > Freight Procurement • Breakeven Analysis",
    "url": "/logistics/ftl-vs-ltl-freight/",
    "keywords": [
      "full",
      "truckload",
      "ftl",
      "less-than-truckload",
      "ltl",
      "cost",
      "breakeven",
      "calculate",
      "whether",
      "shipping",
      "high-volume",
      "palletized"
    ]
  },
  {
    "title": "Ocean Shipping Container CBM Volume & Payload Calculator",
    "category": "Logistics > Ocean Freight • Container Utilization",
    "url": "/logistics/container-cbm-utilization/",
    "keywords": [
      "ocean",
      "shipping",
      "container",
      "cbm",
      "volume",
      "payload",
      "calculator",
      "calculate",
      "cubic",
      "meter",
      "metric",
      "ton"
    ]
  },
  {
    "title": "Reorder Point (ROP) & Safety Stock Volatility Calculator",
    "category": "Logistics > Inventory Science • Demand Volatility",
    "url": "/logistics/reorder-point-safety-stock/",
    "keywords": [
      "reorder",
      "point",
      "rop",
      "safety",
      "stock",
      "volatility",
      "calculator",
      "calculate",
      "statistical",
      "and",
      "inventory",
      "buffers"
    ]
  },
  {
    "title": "Economic Order Quantity (EOQ) & Annual Holding Cost Calculator",
    "category": "Logistics > Inventory Optimization • EOQ Formulation",
    "url": "/logistics/economic-order-quantity-eoq/",
    "keywords": [
      "economic",
      "order",
      "quantity",
      "eoq",
      "annual",
      "holding",
      "cost",
      "calculator",
      "calculate",
      "optimal",
      "purchasing",
      "batch"
    ]
  },
  {
    "title": "Warehouse Aisle Width & Forklift Turning Radius Calculator",
    "category": "Logistics > Facility Engineering • Aisle Clearances",
    "url": "/logistics/forklift-aisle-turning-radius/",
    "keywords": [
      "warehouse",
      "aisle",
      "width",
      "forklift",
      "turning",
      "radius",
      "calculator",
      "calculate",
      "minimum",
      "clear",
      "rack-to-rack",
      "for"
    ]
  },
  {
    "title": "Air Freight Volumetric vs Gross Chargeable Weight Calculator",
    "category": "Logistics > Aviation Logistics • IATA Standards",
    "url": "/logistics/air-freight-chargeable-weight/",
    "keywords": [
      "air",
      "freight",
      "volumetric",
      "gross",
      "chargeable",
      "weight",
      "calculator",
      "calculate",
      "iata",
      "international",
      "6000",
      "ratio"
    ]
  },
  {
    "title": "Shipping Port Demurrage & Container Detention Fee Calculator",
    "category": "Logistics > Maritime Logistics • Supply Chain Penalties",
    "url": "/logistics/demurrage-detention-fees/",
    "keywords": [
      "shipping",
      "port",
      "demurrage",
      "container",
      "detention",
      "fee",
      "calculator",
      "calculate",
      "daily",
      "escalating",
      "inside",
      "terminal"
    ]
  },
  {
    "title": "Semi-Truck Axle Weight Distribution & DOT Bridge Formula Calculator",
    "category": "Logistics > Highway Transport • DOT Axle Compliance",
    "url": "/logistics/truck-axle-weight-distribution/",
    "keywords": [
      "semi-truck",
      "axle",
      "weight",
      "distribution",
      "dot",
      "bridge",
      "formula",
      "calculator",
      "calculate",
      "individual",
      "group",
      "loadings"
    ]
  },
  {
    "title": "Deadhead Trucking Mileage Cost & Lane Profitability Calculator",
    "category": "Logistics > Trucking Economics • Lane Profitability",
    "url": "/logistics/deadhead-trucking-cost/",
    "keywords": [
      "deadhead",
      "trucking",
      "mileage",
      "cost",
      "lane",
      "profitability",
      "calculator",
      "calculate",
      "true",
      "per",
      "loaded",
      "mile"
    ]
  },
  {
    "title": "Supply Chain Bullwhip Effect Variance Amplification Calculator",
    "category": "Logistics > Supply Chain Dynamics • Demand Amplification",
    "url": "/logistics/inventory-bullwhip-effect/",
    "keywords": [
      "supply",
      "chain",
      "bullwhip",
      "effect",
      "variance",
      "amplification",
      "calculator",
      "calculate",
      "order",
      "ratio",
      "across",
      "echelons"
    ]
  },
  {
    "title": "Warehouse Cubic Storage Density & Floor Space Utilization Calculator",
    "category": "Logistics > Facility Optimization • Cubic Utilization",
    "url": "/logistics/warehouse-storage-density/",
    "keywords": [
      "warehouse",
      "cubic",
      "storage",
      "density",
      "floor",
      "space",
      "utilization",
      "calculator",
      "calculate",
      "honeycombing",
      "loss",
      "and"
    ]
  },
  {
    "title": "Freight Fuel Surcharge (FSC) Sliding Scale Calculator",
    "category": "Logistics > Trucking Tariffs • Fuel Surcharge",
    "url": "/logistics/freight-fuel-surcharge/",
    "keywords": [
      "freight",
      "fuel",
      "surcharge",
      "fsc",
      "sliding",
      "scale",
      "calculator",
      "calculate",
      "carrier",
      "percentage",
      "and",
      "per-mile"
    ]
  },
  {
    "title": "Fleet Total Cost of Ownership (TCO) & Operating Cost Per Mile",
    "category": "Logistics > Fleet Management • Operating Cost Per Mile",
    "url": "/logistics/fleet-tco-per-mile/",
    "keywords": [
      "fleet",
      "total",
      "cost",
      "ownership",
      "tco",
      "operating",
      "per",
      "mile",
      "calculate",
      "and",
      "marginal",
      "mcpm"
    ]
  },
  {
    "title": "Intermodal Rail vs Over-The-Road (OTR) Trucking Breakeven",
    "category": "Logistics > Intermodal Freight • Modal Conversion",
    "url": "/logistics/intermodal-rail-vs-truck/",
    "keywords": [
      "intermodal",
      "rail",
      "over-the-road",
      "otr",
      "trucking",
      "breakeven",
      "compare",
      "cost",
      "per",
      "container",
      "transit",
      "lead"
    ]
  },
  {
    "title": "Last-Mile Delivery Route Stop Density & Cost Per Drop Calculator",
    "category": "Logistics > Last-Mile Logistics • Route Density",
    "url": "/logistics/last-mile-route-stop-density/",
    "keywords": [
      "last-mile",
      "delivery",
      "route",
      "stop",
      "density",
      "cost",
      "per",
      "drop",
      "calculator",
      "calculate",
      "driver",
      "metrics"
    ]
  },
  {
    "title": "Warehouse Pick-and-Pack Labor Productivity Rate Calculator",
    "category": "Logistics > Fulfillment Operations • Labor Engineering",
    "url": "/logistics/pick-and-pack-productivity/",
    "keywords": [
      "warehouse",
      "pick-and-pack",
      "labor",
      "productivity",
      "rate",
      "calculator",
      "calculate",
      "order",
      "picker",
      "units-per-hour",
      "uph",
      "cost"
    ]
  },
  {
    "title": "Cross-Dock Logistics Throughput & Staging Transfer Time Calculator",
    "category": "Logistics > Distribution Networks • Cross-Docking",
    "url": "/logistics/cross-dock-throughput/",
    "keywords": [
      "cross-dock",
      "logistics",
      "throughput",
      "staging",
      "transfer",
      "time",
      "calculator",
      "calculate",
      "daily",
      "pallet",
      "capacity",
      "dock"
    ]
  },
  {
    "title": "Import Customs Duty, Ad Valorem Tariff & De Minimis Calculator",
    "category": "Logistics > Global Trade • Customs Compliance",
    "url": "/logistics/customs-duty-tariff/",
    "keywords": [
      "import",
      "customs",
      "duty",
      "valorem",
      "tariff",
      "minimis",
      "calculator",
      "calculate",
      "commercial",
      "duties",
      "section",
      "301"
    ]
  },
  {
    "title": "Pallet Stretch Wrap Film Yield & Containment Force Calculator",
    "category": "Logistics > Packaging Engineering • Load Containment",
    "url": "/logistics/pallet-stretch-wrap-yield/",
    "keywords": [
      "pallet",
      "stretch",
      "wrap",
      "film",
      "yield",
      "containment",
      "force",
      "calculator",
      "calculate",
      "weight",
      "per",
      "pre-stretch"
    ]
  },
  {
    "title": "Cold Chain Mean Kinetic Temperature (MKT) Shelf-Life Calculator",
    "category": "Logistics > Cold Chain Logistics • FDA/USP Compliance",
    "url": "/logistics/cold-chain-mkt/",
    "keywords": [
      "cold",
      "chain",
      "mean",
      "kinetic",
      "temperature",
      "mkt",
      "shelf-life",
      "calculator",
      "calculate",
      "across",
      "excursion",
      "logs"
    ]
  },
  {
    "title": "Dry Ice Sublimation Rate & Cold Box Duration Calculator",
    "category": "Logistics > Cold Chain • Cryogenic Logistics",
    "url": "/logistics/dry-ice-sublimation-shipping/",
    "keywords": [
      "dry",
      "ice",
      "sublimation",
      "rate",
      "cold",
      "box",
      "duration",
      "calculator",
      "calculate",
      "loss",
      "lbs",
      "day"
    ]
  },
  {
    "title": "Reverse Logistics Return Rate & Restocking Recovery Margin Calculator",
    "category": "Logistics > E-Commerce Logistics • Reverse Logistics",
    "url": "/logistics/reverse-logistics-recovery/",
    "keywords": [
      "reverse",
      "logistics",
      "return",
      "rate",
      "restocking",
      "recovery",
      "margin",
      "calculator",
      "calculate",
      "true",
      "financial",
      "cost"
    ]
  },
  {
    "title": "Proof-of-Work Bitcoin Mining Profitability & Hash Rate Calculator",
    "category": "Crypto > Proof of Work • Mining Economics",
    "url": "/crypto/crypto-mining-profitability/",
    "keywords": [
      "proof-of-work",
      "bitcoin",
      "mining",
      "profitability",
      "hash",
      "rate",
      "calculator",
      "calculate",
      "daily",
      "net",
      "profit",
      "break-even"
    ]
  },
  {
    "title": "Proof-of-Stake Validator Staking Yield (APR vs APY) Calculator",
    "category": "Crypto > Proof of Stake • Validator Economics",
    "url": "/crypto/staking-rewards-apr-apy/",
    "keywords": [
      "proof-of-stake",
      "validator",
      "staking",
      "yield",
      "apr",
      "apy",
      "calculator",
      "calculate",
      "annual",
      "returns",
      "commission",
      "deduction"
    ]
  },
  {
    "title": "Automated Market Maker (AMM) Impermanent Loss Calculator",
    "category": "Crypto > DeFi • AMM Mathematics",
    "url": "/crypto/impermanent-loss-amm/",
    "keywords": [
      "automated",
      "market",
      "maker",
      "amm",
      "impermanent",
      "loss",
      "calculator",
      "calculate",
      "exact",
      "for",
      "liquidity",
      "providers"
    ]
  },
  {
    "title": "Liquidity Pool Swap Fee APR & LP Capital Efficiency Calculator",
    "category": "Crypto > DeFi • Fee Monetization",
    "url": "/crypto/liquidity-pool-fee-yield/",
    "keywords": [
      "liquidity",
      "pool",
      "swap",
      "fee",
      "apr",
      "capital",
      "efficiency",
      "calculator",
      "calculate",
      "annual",
      "income",
      "daily"
    ]
  },
  {
    "title": "Crypto Futures Liquidation Price & Maintenance Margin Calculator",
    "category": "Crypto > Derivatives • Liquidation Risk",
    "url": "/crypto/futures-liquidation-price/",
    "keywords": [
      "crypto",
      "futures",
      "liquidation",
      "price",
      "maintenance",
      "margin",
      "calculator",
      "calculate",
      "exact",
      "call",
      "threshold",
      "and"
    ]
  },
  {
    "title": "Crypto Dollar-Cost Averaging (DCA) Accumulation Calculator",
    "category": "Crypto > Wealth Building • Systematic DCA",
    "url": "/crypto/dollar-cost-averaging-dca/",
    "keywords": [
      "crypto",
      "dollar-cost",
      "averaging",
      "dca",
      "accumulation",
      "calculator",
      "simulate",
      "historical",
      "and",
      "projected",
      "recurring",
      "cryptocurrency"
    ]
  },
  {
    "title": "Ethereum Gas Fee Estimator (Gwei, EIP-1559 & USD Cost)",
    "category": "Crypto > Ethereum • EIP-1559 Gas Economics",
    "url": "/crypto/gas-fee-gwei-usd/",
    "keywords": [
      "ethereum",
      "gas",
      "fee",
      "estimator",
      "gwei",
      "eip-1559",
      "usd",
      "cost",
      "calculate",
      "exact",
      "dollar",
      "transaction"
    ]
  },
  {
    "title": "Collateralized Debt Position (CDP) LTV & Liquidation Health Factor",
    "category": "Crypto > DeFi Lending • Liquidation Health",
    "url": "/crypto/cdp-health-factor-ltv/",
    "keywords": [
      "collateralized",
      "debt",
      "position",
      "cdp",
      "ltv",
      "liquidation",
      "health",
      "factor",
      "calculate",
      "loan-to-value",
      "and",
      "collateral"
    ]
  },
  {
    "title": "Perpetual Swap Funding Rate Arbitrage Annualized Yield (Cash & Carry)",
    "category": "Crypto > Quantitative Trading • Market-Neutral Alpha",
    "url": "/crypto/funding-rate-arbitrage/",
    "keywords": [
      "perpetual",
      "swap",
      "funding",
      "rate",
      "arbitrage",
      "annualized",
      "yield",
      "cash",
      "carry",
      "calculate",
      "market-neutral",
      "return"
    ]
  },
  {
    "title": "Token Vesting Cliff, Unlock Schedule & Circulating Inflation Model",
    "category": "Crypto > Tokenomics • Supply Dilution",
    "url": "/crypto/token-vesting-inflation/",
    "keywords": [
      "token",
      "vesting",
      "cliff",
      "unlock",
      "schedule",
      "circulating",
      "inflation",
      "model",
      "calculate",
      "monthly",
      "volume",
      "supply"
    ]
  },
  {
    "title": "Crypto Capital Gains Tax Lot (FIFO vs LIFO vs HIFO) Calculator",
    "category": "Crypto > Tax Optimization • Crypto Accounting",
    "url": "/crypto/crypto-fifo-lifo-tax/",
    "keywords": [
      "crypto",
      "capital",
      "gains",
      "tax",
      "lot",
      "fifo",
      "lifo",
      "hifo",
      "calculator",
      "calculate",
      "realized",
      "short-term"
    ]
  },
  {
    "title": "Zero-Knowledge (ZK) Rollup Calldata Compression & L2 Gas Savings",
    "category": "Crypto > Layer 2 Scaling • ZK Compression",
    "url": "/crypto/zk-rollup-gas-compression/",
    "keywords": [
      "zero-knowledge",
      "rollup",
      "calldata",
      "compression",
      "gas",
      "savings",
      "calculate",
      "batch",
      "ratios",
      "state",
      "diff",
      "costs"
    ]
  },
  {
    "title": "DEX Slippage Tolerance & Price Impact Calculator",
    "category": "Crypto > DEX Mechanics • Price Impact",
    "url": "/crypto/slippage-tolerance-price-impact/",
    "keywords": [
      "dex",
      "slippage",
      "tolerance",
      "price",
      "impact",
      "calculator",
      "calculate",
      "percentage",
      "minimum",
      "received",
      "tokens",
      "and"
    ]
  },
  {
    "title": "Continuous Token Bonding Curve Price & Minting Cost Model",
    "category": "Crypto > Tokenomics • Automated Market Curves",
    "url": "/crypto/bonding-curve-token-mint/",
    "keywords": [
      "continuous",
      "token",
      "bonding",
      "curve",
      "price",
      "minting",
      "cost",
      "model",
      "calculate",
      "instantaneous",
      "buy",
      "sell"
    ]
  },
  {
    "title": "Stablecoin Peg Deviation & Mint/Redeem Arbitrage Spread Calculator",
    "category": "Crypto > DeFi Arbitrage • Stablecoin Pegs",
    "url": "/crypto/stablecoin-depeg-arbitrage/",
    "keywords": [
      "stablecoin",
      "peg",
      "deviation",
      "mint",
      "redeem",
      "arbitrage",
      "spread",
      "calculator",
      "calculate",
      "net",
      "profit",
      "margin"
    ]
  },
  {
    "title": "Cross-Chain Token Bridge Fee & Gas Slippage Optimizer",
    "category": "Crypto > Interoperability • Bridge Analytics",
    "url": "/crypto/cross-chain-bridge-fee/",
    "keywords": [
      "cross-chain",
      "token",
      "bridge",
      "fee",
      "gas",
      "slippage",
      "optimizer",
      "calculate",
      "total",
      "cost",
      "operator",
      "destination"
    ]
  },
  {
    "title": "NFT Marketplace Creator Royalty Split & Net Secondary Proceeds",
    "category": "Crypto > Digital Collectibles • Creator Royalties",
    "url": "/crypto/nft-royalty-split/",
    "keywords": [
      "nft",
      "marketplace",
      "creator",
      "royalty",
      "split",
      "net",
      "secondary",
      "proceeds",
      "calculate",
      "splits",
      "fees",
      "opensea"
    ]
  },
  {
    "title": "Algorithmic Lending Supply & Borrow APY (Aave / Compound Model)",
    "category": "Crypto > DeFi • Interest Rate Curves",
    "url": "/crypto/algorithmic-lending-apy/",
    "keywords": [
      "algorithmic",
      "lending",
      "supply",
      "borrow",
      "apy",
      "aave",
      "compound",
      "model",
      "calculate",
      "interest",
      "rate",
      "curves"
    ]
  },
  {
    "title": "Bitcoin Mining Difficulty Adjustment & Block Time Estimator",
    "category": "Crypto > Consensus Dynamics • Difficulty Adjustment",
    "url": "/crypto/mining-difficulty-adjustment/",
    "keywords": [
      "bitcoin",
      "mining",
      "difficulty",
      "adjustment",
      "block",
      "time",
      "estimator",
      "calculate",
      "upcoming",
      "epoch",
      "percentage",
      "estimated"
    ]
  },
  {
    "title": "Crypto Payment Gateway vs Credit Card Interchange Processing Fees",
    "category": "Crypto > Fintech • Merchant Processing",
    "url": "/crypto/crypto-payment-processor-fees/",
    "keywords": [
      "crypto",
      "payment",
      "gateway",
      "credit",
      "card",
      "interchange",
      "processing",
      "fees",
      "calculate",
      "annual",
      "dollar",
      "savings"
    ]
  },
  {
    "title": "Smart Contract EVM Opcode Gas Execution Cost Analyzer",
    "category": "Crypto > Solidity Engineering • EVM Gas Optimization",
    "url": "/crypto/smart-contract-gas-limit/",
    "keywords": [
      "smart",
      "contract",
      "evm",
      "opcode",
      "gas",
      "execution",
      "cost",
      "analyzer",
      "calculate",
      "granular",
      "sstore",
      "sload"
    ]
  },
  {
    "title": "Optimal Compounding Frequency for DeFi Yield Farming Calculator",
    "category": "Crypto > DeFi Yield Optimization • Game Theory",
    "url": "/crypto/yield-farming-reinvest-frequency/",
    "keywords": [
      "optimal",
      "compounding",
      "frequency",
      "for",
      "defi",
      "yield",
      "farming",
      "calculator",
      "calculate",
      "the",
      "mathematically",
      "reinvestment"
    ]
  },
  {
    "title": "DeFi Flash Loan Arbitrage Spread vs Net Profitability Calculator",
    "category": "Crypto > DeFi Engineering • Flash Loans",
    "url": "/crypto/flash-loan-arbitrage-net/",
    "keywords": [
      "defi",
      "flash",
      "loan",
      "arbitrage",
      "spread",
      "net",
      "profitability",
      "calculator",
      "calculate",
      "uncollateralized",
      "protocol",
      "fees"
    ]
  },
  {
    "title": "Multi-Route DEX Aggregator Optimal Trade Split Calculator",
    "category": "Crypto > DEX Aggregation • Split Routing",
    "url": "/crypto/dex-aggregator-split-routing/",
    "keywords": [
      "multi-route",
      "dex",
      "aggregator",
      "optimal",
      "trade",
      "split",
      "calculator",
      "calculate",
      "splitting",
      "across",
      "multiple",
      "liquidity"
    ]
  },
  {
    "title": "Crypto Portfolio Sharpe Ratio & Value at Risk (VaR 95%) Calculator",
    "category": "Crypto > Quantitative Risk • Portfolio Analytics",
    "url": "/crypto/crypto-portfolio-sharpe-ratio/",
    "keywords": [
      "crypto",
      "portfolio",
      "sharpe",
      "ratio",
      "value",
      "risk",
      "var",
      "calculator",
      "calculate",
      "risk-adjusted",
      "downside",
      "sortino"
    ]
  },
  {
    "title": "Personal Injury Settlement Multiplier Calculator",
    "category": "Legal > Personal Injury • Settlement Valuation",
    "url": "/legal/personal-injury-multiplier/",
    "keywords": [
      "personal",
      "injury",
      "settlement",
      "multiplier",
      "calculator",
      "calculate",
      "estimated",
      "car",
      "accident",
      "and",
      "bodily",
      "insurance"
    ]
  },
  {
    "title": "Pain and Suffering Damages Valuation Calculator (Per Diem vs Multiplier)",
    "category": "Legal > Tort Law • Non-Economic Damages",
    "url": "/legal/pain-and-suffering-valuation/",
    "keywords": [
      "pain",
      "and",
      "suffering",
      "damages",
      "valuation",
      "calculator",
      "per",
      "diem",
      "multiplier",
      "calculate",
      "non-economic",
      "using"
    ]
  },
  {
    "title": "Structured Settlement Annuity Lump-Sum Present Value (NPV)",
    "category": "Legal > Settlement Finance • Present Value",
    "url": "/legal/structured-settlement-npv/",
    "keywords": [
      "structured",
      "settlement",
      "annuity",
      "lump-sum",
      "present",
      "value",
      "npv",
      "calculate",
      "fair",
      "market",
      "cash",
      "and"
    ]
  },
  {
    "title": "Wrongful Death Economic Loss & Future Earning Capacity Calculator",
    "category": "Legal > Forensic Economics • Wrongful Death",
    "url": "/legal/wrongful-death-damages/",
    "keywords": [
      "wrongful",
      "death",
      "economic",
      "loss",
      "future",
      "earning",
      "capacity",
      "calculator",
      "calculate",
      "present",
      "value",
      "decedent"
    ]
  },
  {
    "title": "Attorney Contingency Fee Net Payout & Medical Lien Deduction Calculator",
    "category": "Legal > Legal Ethics • Client Settlement Distribution",
    "url": "/legal/contingency-fee-net-payout/",
    "keywords": [
      "attorney",
      "contingency",
      "fee",
      "net",
      "payout",
      "medical",
      "lien",
      "deduction",
      "calculator",
      "calculate",
      "exact",
      "client"
    ]
  },
  {
    "title": "Car Accident Diminished Value Formula (17c Rule) Calculator",
    "category": "Legal > Auto Insurance • Diminished Value",
    "url": "/legal/car-accident-diminished-value/",
    "keywords": [
      "car",
      "accident",
      "diminished",
      "value",
      "formula",
      "17c",
      "rule",
      "calculator",
      "calculate",
      "inherent",
      "for",
      "repaired"
    ]
  },
  {
    "title": "Workers' Comp Permanent Partial Disability (PPD) Rating & Schedule",
    "category": "Legal > Workers' Compensation • Scheduled Loss",
    "url": "/legal/workers-comp-ppd-rating/",
    "keywords": [
      "workers",
      "comp",
      "permanent",
      "partial",
      "disability",
      "ppd",
      "rating",
      "schedule",
      "calculate",
      "scheduled",
      "body",
      "member"
    ]
  },
  {
    "title": "Lost Wages, Overtime & Fringe Benefits Economic Loss Calculator",
    "category": "Legal > Damages • Economic Compensation",
    "url": "/legal/lost-wages-economic-loss/",
    "keywords": [
      "lost",
      "wages",
      "overtime",
      "fringe",
      "benefits",
      "economic",
      "loss",
      "calculator",
      "calculate",
      "past",
      "and",
      "future"
    ]
  },
  {
    "title": "Bodily Injury Liability Umbrella Policy Limit Exhaustion Calculator",
    "category": "Legal > Insurance Coverage • Layered Liability",
    "url": "/legal/umbrella-policy-limit-exhaustion/",
    "keywords": [
      "bodily",
      "injury",
      "liability",
      "umbrella",
      "policy",
      "limit",
      "exhaustion",
      "calculator",
      "calculate",
      "claim",
      "allocation",
      "across"
    ]
  },
  {
    "title": "Prejudgment Interest Statutory Damages Calculator",
    "category": "Legal > Civil Procedure • Statutory Interest",
    "url": "/legal/prejudgment-interest-statutory/",
    "keywords": [
      "prejudgment",
      "interest",
      "statutory",
      "damages",
      "calculator",
      "calculate",
      "accrued",
      "from",
      "the",
      "date",
      "injury",
      "formal"
    ]
  },
  {
    "title": "Child Support Statutory Guidelines (Income Shares Model) Calculator",
    "category": "Legal > Family Law • Income Shares Guidelines",
    "url": "/legal/child-support-income-shares/",
    "keywords": [
      "child",
      "support",
      "statutory",
      "guidelines",
      "income",
      "shares",
      "model",
      "calculator",
      "calculate",
      "monthly",
      "obligation",
      "using"
    ]
  },
  {
    "title": "Spousal Maintenance & Alimony Duration & Payment Formula Calculator",
    "category": "Legal > Family Law • Alimony Guidelines",
    "url": "/legal/spousal-maintenance-alimony/",
    "keywords": [
      "spousal",
      "maintenance",
      "alimony",
      "duration",
      "payment",
      "formula",
      "calculator",
      "calculate",
      "monthly",
      "payments",
      "and",
      "support"
    ]
  },
  {
    "title": "Commercial General Liability (CGL) Audit Payroll Premium Adjustment",
    "category": "Legal > Commercial Insurance • Premium Audit",
    "url": "/legal/cgl-general-liability-audit/",
    "keywords": [
      "commercial",
      "general",
      "liability",
      "cgl",
      "audit",
      "payroll",
      "premium",
      "adjustment",
      "calculate",
      "annual",
      "insurance",
      "adjustments"
    ]
  },
  {
    "title": "Business Interruption Loss & Gross Earnings Formula Calculator",
    "category": "Legal > Commercial Property • Business Interruption",
    "url": "/legal/business-interruption-insurance/",
    "keywords": [
      "business",
      "interruption",
      "loss",
      "gross",
      "earnings",
      "formula",
      "calculator",
      "calculate",
      "insurance",
      "recovery",
      "net",
      "profit"
    ]
  },
  {
    "title": "Life Insurance Human Life Value (HLV) Capital Needs Calculator",
    "category": "Legal > Actuarial Science • Human Life Value",
    "url": "/legal/life-insurance-human-life-value/",
    "keywords": [
      "life",
      "insurance",
      "human",
      "value",
      "hlv",
      "capital",
      "needs",
      "calculator",
      "calculate",
      "optimal",
      "term",
      "permanent"
    ]
  },
  {
    "title": "Long-Term Care Insurance Elimination Period & Benefit Pool Calculator",
    "category": "Legal > Actuarial • Long-Term Care",
    "url": "/legal/long-term-care-benefit-pool/",
    "keywords": [
      "long-term",
      "care",
      "insurance",
      "elimination",
      "period",
      "benefit",
      "pool",
      "calculator",
      "calculate",
      "lifetime",
      "out-of-pocket",
      "costs"
    ]
  },
  {
    "title": "Property Casualty Co-Insurance Penalty (80% Rule) Calculator",
    "category": "Legal > Property Insurance • Coinsurance Clause",
    "url": "/legal/property-casualty-coinsurance/",
    "keywords": [
      "property",
      "casualty",
      "co-insurance",
      "penalty",
      "rule",
      "calculator",
      "calculate",
      "insurance",
      "payout",
      "and",
      "coinsurance",
      "penalties"
    ]
  },
  {
    "title": "Title Insurance Premium & Refinance Reissue Rate Calculator",
    "category": "Legal > Real Estate Law • Title Insurance",
    "url": "/legal/title-insurance-reissue-rate/",
    "keywords": [
      "title",
      "insurance",
      "premium",
      "refinance",
      "reissue",
      "rate",
      "calculator",
      "calculate",
      "lender",
      "and",
      "owner",
      "policy"
    ]
  },
  {
    "title": "Health Insurance Subrogation Lien Reduction (Common Fund Doctrine) Calculator",
    "category": "Legal > Healthcare Subrogation • Lien Resolution",
    "url": "/legal/subrogation-lien-reduction/",
    "keywords": [
      "health",
      "insurance",
      "subrogation",
      "lien",
      "reduction",
      "common",
      "fund",
      "doctrine",
      "calculator",
      "calculate",
      "mandatory",
      "legal"
    ]
  },
  {
    "title": "Breach of Contract Expectation & Consequential Damages Calculator",
    "category": "Legal > Contract Law • Commercial Litigation",
    "url": "/legal/breach-of-contract-damages/",
    "keywords": [
      "breach",
      "contract",
      "expectation",
      "consequential",
      "damages",
      "calculator",
      "calculate",
      "incidental",
      "losses",
      "lost",
      "profits",
      "hadley"
    ]
  },
  {
    "title": "Medical Malpractice Noneconomic Damages Cap Adjustment Calculator",
    "category": "Legal > Health Law • Malpractice Tort Reform",
    "url": "/legal/medical-malpractice-damages-cap/",
    "keywords": [
      "medical",
      "malpractice",
      "noneconomic",
      "damages",
      "cap",
      "adjustment",
      "calculator",
      "calculate",
      "verdict",
      "reductions",
      "applying",
      "state"
    ]
  },
  {
    "title": "Law Firm Billing Realization & Collection Rate Productivity Calculator",
    "category": "Legal > Law Firm Practice Management • Financial Metrics",
    "url": "/legal/legal-billing-realization-rate/",
    "keywords": [
      "law",
      "firm",
      "billing",
      "realization",
      "collection",
      "rate",
      "productivity",
      "calculator",
      "calculate",
      "write-down",
      "write-off",
      "leakage"
    ]
  },
  {
    "title": "Punitive-to-Compensatory Damages Ratio Compliance (SCOTUS Due Process)",
    "category": "Legal > Constitutional Tort Law • SCOTUS Precedent",
    "url": "/legal/punitive-compensatory-ratio/",
    "keywords": [
      "punitive-to-compensatory",
      "damages",
      "ratio",
      "compliance",
      "scotus",
      "due",
      "process",
      "calculate",
      "ratios",
      "and",
      "test",
      "constitutional"
    ]
  },
  {
    "title": "USPTO Trademark Filing Fees & Multi-Class Madrid Protocol Calculator",
    "category": "Legal > Intellectual Property • Trademark Filing",
    "url": "/legal/trademark-registration-fees/",
    "keywords": [
      "uspto",
      "trademark",
      "filing",
      "fees",
      "multi-class",
      "madrid",
      "protocol",
      "calculator",
      "calculate",
      "united",
      "states",
      "patent"
    ]
  },
  {
    "title": "Workers' Comp Experience Modification Rate (EMR) Premium Impact",
    "category": "Legal > Risk Management • EMR Modifiers",
    "url": "/legal/workers-comp-emr-modifier/",
    "keywords": [
      "workers",
      "comp",
      "experience",
      "modification",
      "rate",
      "emr",
      "premium",
      "impact",
      "calculate",
      "mod",
      "financial",
      "compensation"
    ]
  },
  {
    "title": "Crop Yield Estimator (Corn, Soybeans & Wheat Bushels Per Acre)",
    "category": "Agriculture > Agronomy • Yield Forecasting",
    "url": "/agriculture/crop-yield-estimator/",
    "keywords": [
      "crop",
      "yield",
      "estimator",
      "corn",
      "soybeans",
      "wheat",
      "bushels",
      "per",
      "acre",
      "calculate",
      "pre-harvest",
      "grain"
    ]
  },
  {
    "title": "N-P-K Fertilizer Application & Nutrient Blending Rate (lbs/acre)",
    "category": "Agriculture > Soil Fertility • Nutrient Management",
    "url": "/agriculture/npk-fertilizer-blending/",
    "keywords": [
      "n-p-k",
      "fertilizer",
      "application",
      "nutrient",
      "blending",
      "rate",
      "lbs",
      "acre",
      "calculate",
      "commercial",
      "rates",
      "for"
    ]
  },
  {
    "title": "Cattle Stocking Rate & Animal Unit Months (AUM) Grazing Capacity",
    "category": "Agriculture > Rangeland Ecology • Grazing Capacity",
    "url": "/agriculture/cattle-stocking-rate-aum/",
    "keywords": [
      "cattle",
      "stocking",
      "rate",
      "animal",
      "unit",
      "months",
      "aum",
      "grazing",
      "capacity",
      "calculate",
      "pasture",
      "allowable"
    ]
  },
  {
    "title": "Grain Silo & Cylindrical Grain Bin Bushel Capacity Calculator",
    "category": "Agriculture > Grain Storage • Silo Engineering",
    "url": "/agriculture/grain-bin-bushel-capacity/",
    "keywords": [
      "grain",
      "silo",
      "cylindrical",
      "bin",
      "bushel",
      "capacity",
      "calculator",
      "calculate",
      "struck",
      "and",
      "peaked",
      "volume"
    ]
  },
  {
    "title": "Center Pivot Irrigation Flow Rate & Water Application Depth Calculator",
    "category": "Agriculture > Irrigation Engineering • Center Pivot",
    "url": "/agriculture/center-pivot-irrigation/",
    "keywords": [
      "center",
      "pivot",
      "irrigation",
      "flow",
      "rate",
      "water",
      "application",
      "depth",
      "calculator",
      "calculate",
      "system",
      "pumping"
    ]
  },
  {
    "title": "Timber Board Foot Volume Estimator (Doyle, Scribner & International 1/4)",
    "category": "Agriculture > Forestry • Timber Scaling",
    "url": "/agriculture/timber-volume-doyle-scribner/",
    "keywords": [
      "timber",
      "board",
      "foot",
      "volume",
      "estimator",
      "doyle",
      "scribner",
      "international",
      "calculate",
      "sawtimber",
      "standing",
      "trees"
    ]
  },
  {
    "title": "Round Hay Bale Weight & Winter Livestock Forage Requirement",
    "category": "Agriculture > Livestock Management • Winter Forage",
    "url": "/agriculture/hay-bale-livestock-forage/",
    "keywords": [
      "round",
      "hay",
      "bale",
      "weight",
      "winter",
      "livestock",
      "forage",
      "requirement",
      "calculate",
      "estimated",
      "from",
      "diameter"
    ]
  },
  {
    "title": "Seed Planting Population & Row Spacing Seed Count Per Acre",
    "category": "Agriculture > Planting Technology • Seeding Density",
    "url": "/agriculture/seed-planting-population/",
    "keywords": [
      "seed",
      "planting",
      "population",
      "row",
      "spacing",
      "count",
      "per",
      "acre",
      "calculate",
      "seeds",
      "foot",
      "bag"
    ]
  },
  {
    "title": "Livestock Feed Conversion Ratio (FCR) & Cost of Gain Calculator",
    "category": "Agriculture > Animal Science • Feed Efficiency",
    "url": "/agriculture/feed-conversion-ratio-fcr/",
    "keywords": [
      "livestock",
      "feed",
      "conversion",
      "ratio",
      "fcr",
      "cost",
      "gain",
      "calculator",
      "calculate",
      "efficiency",
      "lbs",
      "per"
    ]
  },
  {
    "title": "Agricultural Soil Lime Requirement & CCE Neutralization Calculator",
    "category": "Agriculture > Agronomy • Soil Chemistry",
    "url": "/agriculture/soil-lime-requirement-cce/",
    "keywords": [
      "agricultural",
      "soil",
      "lime",
      "requirement",
      "cce",
      "neutralization",
      "calculator",
      "calculate",
      "tons",
      "limestone",
      "needed",
      "per"
    ]
  },
  {
    "title": "Herbicide / Pesticide Tank Mix Spray Dilution Rate Calculator",
    "category": "Agriculture > Crop Protection • Sprayer Calibration",
    "url": "/agriculture/pesticide-tank-mix-dilution/",
    "keywords": [
      "herbicide",
      "pesticide",
      "tank",
      "mix",
      "spray",
      "dilution",
      "rate",
      "calculator",
      "calculate",
      "chemical",
      "ounces",
      "add"
    ]
  },
  {
    "title": "Dairy Cow Fat-Corrected Milk (4% FCM) & Energy-Corrected Milk (ECM)",
    "category": "Agriculture > Dairy Science • Milk Equivalency",
    "url": "/agriculture/dairy-cow-fat-corrected-milk/",
    "keywords": [
      "dairy",
      "cow",
      "fat-corrected",
      "milk",
      "fcm",
      "energy-corrected",
      "ecm",
      "calculate",
      "and",
      "from",
      "bulk",
      "tank"
    ]
  },
  {
    "title": "Combine Harvester Field Grain Loss & Bushel Dockage Rate Calculator",
    "category": "Agriculture > Harvest Operations • Loss Quantification",
    "url": "/agriculture/combine-harvester-grain-loss/",
    "keywords": [
      "combine",
      "harvester",
      "field",
      "grain",
      "loss",
      "bushel",
      "dockage",
      "rate",
      "calculator",
      "calculate",
      "harvesting",
      "bushels"
    ]
  },
  {
    "title": "Agricultural Subsurface Drainage Tile Spacing & Sizing Calculator",
    "category": "Agriculture > Agricultural Drainage • Water Management",
    "url": "/agriculture/drainage-tile-spacing/",
    "keywords": [
      "agricultural",
      "subsurface",
      "drainage",
      "tile",
      "spacing",
      "sizing",
      "calculator",
      "calculate",
      "corrugated",
      "hdpe",
      "lateral",
      "feet"
    ]
  },
  {
    "title": "Greenhouse Daily Light Integral (DLI) & Supplemental LED PPFD Calculator",
    "category": "Agriculture > Controlled Environment Agriculture • Photobiology",
    "url": "/agriculture/greenhouse-dli-lighting/",
    "keywords": [
      "greenhouse",
      "daily",
      "light",
      "integral",
      "dli",
      "supplemental",
      "led",
      "ppfd",
      "calculator",
      "calculate",
      "mol",
      "day"
    ]
  },
  {
    "title": "Swine Nursery Feed Intake & Average Daily Gain (ADG) Calculator",
    "category": "Agriculture > Swine Production • Growth Kinetics",
    "url": "/agriculture/pig-average-daily-gain/",
    "keywords": [
      "swine",
      "nursery",
      "feed",
      "intake",
      "average",
      "daily",
      "gain",
      "adg",
      "calculator",
      "calculate",
      "days",
      "market"
    ]
  },
  {
    "title": "Poultry Broiler Flock European Production Efficiency Factor (EPEF) Calculator",
    "category": "Agriculture > Poultry Science • Broiler Performance",
    "url": "/agriculture/broiler-flock-epef-efficiency/",
    "keywords": [
      "poultry",
      "broiler",
      "flock",
      "european",
      "production",
      "efficiency",
      "factor",
      "epef",
      "calculator",
      "calculate",
      "epi",
      "index"
    ]
  },
  {
    "title": "Silage Bunker Trench Dry Matter Density & Packing Loss Calculator",
    "category": "Agriculture > Forage Preservation • Silage Compaction",
    "url": "/agriculture/silage-bunker-density/",
    "keywords": [
      "silage",
      "bunker",
      "trench",
      "dry",
      "matter",
      "density",
      "packing",
      "loss",
      "calculator",
      "calculate",
      "tractor",
      "weight"
    ]
  },
  {
    "title": "Livestock Manure N-P-K Nutrient Fertilizer Value Credit Per Ton",
    "category": "Agriculture > Nutrient Economics • Manure Valuation",
    "url": "/agriculture/manure-nutrient-fertilizer-credit/",
    "keywords": [
      "livestock",
      "manure",
      "n-p-k",
      "nutrient",
      "fertilizer",
      "value",
      "credit",
      "per",
      "ton",
      "calculate",
      "commercial",
      "dollar"
    ]
  },
  {
    "title": "Farm Tractor Diesel Fuel Consumption Per Acre (PTO Horsepower) Calculator",
    "category": "Agriculture > Machinery Economics • Field Efficiency",
    "url": "/agriculture/tractor-fuel-consumption-pto/",
    "keywords": [
      "farm",
      "tractor",
      "diesel",
      "fuel",
      "consumption",
      "per",
      "acre",
      "pto",
      "horsepower",
      "calculator",
      "calculate",
      "hourly"
    ]
  },
  {
    "title": "Pasture Weed Eradication Herbicide Rate & Boom Sprayer Calibration",
    "category": "Agriculture > Rangeland Management • Weed Control",
    "url": "/agriculture/pasture-weed-herbicide-coverage/",
    "keywords": [
      "pasture",
      "weed",
      "eradication",
      "herbicide",
      "rate",
      "boom",
      "sprayer",
      "calibration",
      "calculate",
      "nozzle",
      "flow",
      "gpm"
    ]
  },
  {
    "title": "Beehive Honey Harvest Yield & Fall Sugar Syrup Feeding Calculator",
    "category": "Agriculture > Apiculture • Apiary Management",
    "url": "/agriculture/beehive-honey-yield-feeding/",
    "keywords": [
      "beehive",
      "honey",
      "harvest",
      "yield",
      "fall",
      "sugar",
      "syrup",
      "feeding",
      "calculator",
      "calculate",
      "harvestable",
      "surplus"
    ]
  },
  {
    "title": "Aquaponics Fish-to-Plant Biomass Ratio & Biofilter Media Sizing",
    "category": "Agriculture > Aquaculture • Controlled Systems",
    "url": "/agriculture/aquaponics-biofilter-fish-plant/",
    "keywords": [
      "aquaponics",
      "fish-to-plant",
      "biomass",
      "ratio",
      "biofilter",
      "media",
      "sizing",
      "calculate",
      "daily",
      "fish",
      "feed",
      "rate"
    ]
  },
  {
    "title": "Vineyard Grape Yield to Finished Wine Gallons & Bottles Calculator",
    "category": "Agriculture > Viticulture & Enology • Wine Yield",
    "url": "/agriculture/vineyard-grape-yield-wine/",
    "keywords": [
      "vineyard",
      "grape",
      "yield",
      "finished",
      "wine",
      "gallons",
      "bottles",
      "calculator",
      "calculate",
      "harvest",
      "tonnage",
      "per"
    ]
  },
  {
    "title": "Farmland Cash Rent Equivalent vs Crop Share Lease Calculator",
    "category": "Agriculture > Agricultural Real Estate • Farm Leases",
    "url": "/agriculture/farmland-cash-rent-equivalent/",
    "keywords": [
      "farmland",
      "cash",
      "rent",
      "equivalent",
      "crop",
      "share",
      "lease",
      "calculator",
      "compare",
      "fixed",
      "per",
      "acre"
    ]
  },
  {
    "title": "Beam Deflection & Maximum Bending Moment Calculator",
    "category": "Engineering > Structural Mechanics • Beam Analysis",
    "url": "/engineering/beam-deflection-bending-moment/",
    "keywords": [
      "beam",
      "deflection",
      "maximum",
      "bending",
      "moment",
      "calculator",
      "calculate",
      "shear",
      "force",
      "and",
      "mid-span",
      "elastic"
    ]
  },
  {
    "title": "Soil Compaction Dry Density & Optimum Moisture (Proctor Test)",
    "category": "Engineering > Geotechnical Engineering • Soil Compaction",
    "url": "/engineering/proctor-soil-compaction/",
    "keywords": [
      "soil",
      "compaction",
      "dry",
      "density",
      "optimum",
      "moisture",
      "proctor",
      "test",
      "calculate",
      "from",
      "wet",
      "bulk"
    ]
  },
  {
    "title": "Darcy-Weisbach Pipe Friction Head Loss & Pressure Drop Calculator",
    "category": "Engineering > Hydraulic Engineering • Pipe Networks",
    "url": "/engineering/darcy-weisbach-head-loss/",
    "keywords": [
      "darcy-weisbach",
      "pipe",
      "friction",
      "head",
      "loss",
      "pressure",
      "drop",
      "calculator",
      "calculate",
      "feet",
      "psi",
      "and"
    ]
  },
  {
    "title": "Manning's Open Channel Flow Velocity & Discharge Capacity Calculator",
    "category": "Engineering > Hydraulics • Open Channel Flow",
    "url": "/engineering/mannings-open-channel-flow/",
    "keywords": [
      "manning",
      "open",
      "channel",
      "flow",
      "velocity",
      "discharge",
      "capacity",
      "calculator",
      "calculate",
      "cfs",
      "fps",
      "and"
    ]
  },
  {
    "title": "ASCE 7 Wind Load Velocity Pressure on Building Envelopes Calculator",
    "category": "Engineering > Structural Engineering • ASCE 7 Standards",
    "url": "/engineering/asce7-wind-load-pressure/",
    "keywords": [
      "asce",
      "wind",
      "load",
      "velocity",
      "pressure",
      "building",
      "envelopes",
      "calculator",
      "calculate",
      "design",
      "psf",
      "based"
    ]
  },
  {
    "title": "Reinforced Concrete Slab One-Way & Two-Way Punching Shear Capacity (ACI 318)",
    "category": "Engineering > Structural Concrete • ACI 318 Standard",
    "url": "/engineering/concrete-slab-shear-capacity/",
    "keywords": [
      "reinforced",
      "concrete",
      "slab",
      "one-way",
      "two-way",
      "punching",
      "shear",
      "capacity",
      "aci",
      "318",
      "calculate",
      "nominal"
    ]
  },
  {
    "title": "Earthwork Cut and Fill Volume Calculator (Average End Area Method)",
    "category": "Engineering > Civil Site Design • Earthwork Volumes",
    "url": "/engineering/earthwork-cut-and-fill/",
    "keywords": [
      "earthwork",
      "cut",
      "and",
      "fill",
      "volume",
      "calculator",
      "average",
      "end",
      "area",
      "method",
      "calculate",
      "excavation"
    ]
  },
  {
    "title": "Retaining Wall Rankine Lateral Earth Pressure (Active & Passive) Calculator",
    "category": "Engineering > Geotechnical • Retaining Wall Mechanics",
    "url": "/engineering/retaining-wall-rankine-earth/",
    "keywords": [
      "retaining",
      "wall",
      "rankine",
      "lateral",
      "earth",
      "pressure",
      "active",
      "passive",
      "calculator",
      "calculate",
      "and",
      "coefficients"
    ]
  },
  {
    "title": "Stormwater Runoff Peak Discharge Calculator (Rational Method Q = C·I·A)",
    "category": "Engineering > Civil Hydrology • Stormwater Runoff",
    "url": "/engineering/rational-method-stormwater/",
    "keywords": [
      "stormwater",
      "runoff",
      "peak",
      "discharge",
      "calculator",
      "rational",
      "method",
      "calculate",
      "watershed",
      "cubic",
      "feet",
      "per"
    ]
  },
  {
    "title": "Asphalt Pavement Structural Number & AASHTO ESAL Design Life Calculator",
    "category": "Engineering > Highway Engineering • AASHTO Pavement",
    "url": "/engineering/pavement-structural-number-esal/",
    "keywords": [
      "asphalt",
      "pavement",
      "structural",
      "number",
      "aashto",
      "esal",
      "design",
      "life",
      "calculator",
      "calculate",
      "flexible",
      "layer"
    ]
  },
  {
    "title": "Steel Column Euler Critical Buckling Load & Slenderness Ratio Calculator",
    "category": "Engineering > Mechanics of Materials • Buckling",
    "url": "/engineering/euler-column-buckling-load/",
    "keywords": [
      "steel",
      "column",
      "euler",
      "critical",
      "buckling",
      "load",
      "slenderness",
      "ratio",
      "calculator",
      "calculate",
      "elastic",
      "kips"
    ]
  },
  {
    "title": "Shallow Foundation Bearing Capacity Calculator (Terzaghi Equation)",
    "category": "Engineering > Geotechnical • Foundation Bearing",
    "url": "/engineering/terzaghi-bearing-capacity/",
    "keywords": [
      "shallow",
      "foundation",
      "bearing",
      "capacity",
      "calculator",
      "terzaghi",
      "equation",
      "calculate",
      "ultimate",
      "and",
      "allowable",
      "soil"
    ]
  },
  {
    "title": "Highway Culvert Hydraulics (Inlet vs Outlet Control Headwater Depth)",
    "category": "Engineering > Highway Drainage • Culvert Hydraulics",
    "url": "/engineering/culvert-headwater-inlet-outlet/",
    "keywords": [
      "highway",
      "culvert",
      "hydraulics",
      "inlet",
      "outlet",
      "control",
      "headwater",
      "depth",
      "calculate",
      "ratio",
      "flow",
      "regime"
    ]
  },
  {
    "title": "Stormwater Detention Basin Storage Volume & Settling Inflow Calculator",
    "category": "Engineering > Water Resources • Stormwater Detention",
    "url": "/engineering/detention-pond-settling-volume/",
    "keywords": [
      "stormwater",
      "detention",
      "basin",
      "storage",
      "volume",
      "settling",
      "inflow",
      "calculator",
      "calculate",
      "required",
      "active",
      "flood"
    ]
  },
  {
    "title": "Truss Member Axial Tension & Compression (Method of Joints) Calculator",
    "category": "Engineering > Structural Mechanics • Truss Statics",
    "url": "/engineering/truss-method-of-joints/",
    "keywords": [
      "truss",
      "member",
      "axial",
      "tension",
      "compression",
      "method",
      "joints",
      "calculator",
      "calculate",
      "internal",
      "forces",
      "kips"
    ]
  },
  {
    "title": "Concrete Curing Compressive Strength Maturity Index (Nurse-Saul Method)",
    "category": "Engineering > Materials Engineering • Concrete Maturity",
    "url": "/engineering/concrete-maturity-index/",
    "keywords": [
      "concrete",
      "curing",
      "compressive",
      "strength",
      "maturity",
      "index",
      "nurse-saul",
      "method",
      "calculate",
      "temperature-time",
      "ttf",
      "c-hours"
    ]
  },
  {
    "title": "Water Hammer Joukowsky Shockwave Pressure Surge & Wave Speed Calculator",
    "category": "Engineering > Fluid Transient Dynamics • Water Hammer",
    "url": "/engineering/water-hammer-joukowsky-surge/",
    "keywords": [
      "water",
      "hammer",
      "joukowsky",
      "shockwave",
      "pressure",
      "surge",
      "wave",
      "speed",
      "calculator",
      "calculate",
      "rapid",
      "valve"
    ]
  },
  {
    "title": "Soil Slope Stability Safety Factor (Ordinary / Bishop Method)",
    "category": "Engineering > Geotechnical • Slope Stability",
    "url": "/engineering/slope-stability-safety-factor/",
    "keywords": [
      "soil",
      "slope",
      "stability",
      "safety",
      "factor",
      "ordinary",
      "bishop",
      "method",
      "calculate",
      "against",
      "deep",
      "rotational"
    ]
  },
  {
    "title": "Geotextile Fabric Tensile Modulus for Subgrade Stabilization Calculator",
    "category": "Engineering > Geosynthetics • Highway Subgrades",
    "url": "/engineering/geotextile-roadbed-stabilization/",
    "keywords": [
      "geotextile",
      "fabric",
      "tensile",
      "modulus",
      "for",
      "subgrade",
      "stabilization",
      "calculator",
      "calculate",
      "aggregate",
      "base",
      "reduction"
    ]
  },
  {
    "title": "Seismic Equivalent Lateral Force Base Shear Calculator (ASCE 7 / IBC)",
    "category": "Engineering > Earthquake Engineering • Seismic Base Shear",
    "url": "/engineering/seismic-base-shear-asce7/",
    "keywords": [
      "seismic",
      "equivalent",
      "lateral",
      "force",
      "base",
      "shear",
      "calculator",
      "asce",
      "ibc",
      "calculate",
      "total",
      "design"
    ]
  },
  {
    "title": "Wastewater BOD Removal Efficiency & Aeration Tank Sizing Calculator",
    "category": "Engineering > Environmental Engineering • Wastewater Treatment",
    "url": "/engineering/wastewater-bod-aeration-tank/",
    "keywords": [
      "wastewater",
      "bod",
      "removal",
      "efficiency",
      "aeration",
      "tank",
      "sizing",
      "calculator",
      "calculate",
      "municipal",
      "and",
      "industrial"
    ]
  },
  {
    "title": "Deep Foundation Driven Pile Static Axial Skin Friction & End Bearing Capacity",
    "category": "Engineering > Deep Foundations • Pile Dynamics",
    "url": "/engineering/pile-axial-capacity-bearing/",
    "keywords": [
      "deep",
      "foundation",
      "driven",
      "pile",
      "static",
      "axial",
      "skin",
      "friction",
      "end",
      "bearing",
      "capacity",
      "calculate"
    ]
  },
  {
    "title": "Pre-Stressed Concrete Post-Tension Tendon Elongation & Friction Loss Calculator",
    "category": "Engineering > Structural Concrete • Post-Tensioning",
    "url": "/engineering/prestressed-concrete-elongation/",
    "keywords": [
      "pre-stressed",
      "concrete",
      "post-tension",
      "tendon",
      "elongation",
      "friction",
      "loss",
      "calculator",
      "calculate",
      "theoretical",
      "inches",
      "jack"
    ]
  },
  {
    "title": "Bridge Superstructure Thermal Expansion & Expansion Joint Sizing Calculator",
    "category": "Engineering > Bridge Engineering • Expansion Joints",
    "url": "/engineering/thermal-expansion-bridge-joints/",
    "keywords": [
      "bridge",
      "superstructure",
      "thermal",
      "expansion",
      "joint",
      "sizing",
      "calculator",
      "calculate",
      "total",
      "movement",
      "and",
      "contraction"
    ]
  },
  {
    "title": "Roadway Horizontal Alignment Minimum Curve Radius & Superelevation Calculator",
    "category": "Engineering > Transportation • Highway Geometric Design",
    "url": "/engineering/highway-horizontal-curve-radius/",
    "keywords": [
      "roadway",
      "horizontal",
      "alignment",
      "minimum",
      "curve",
      "radius",
      "superelevation",
      "calculator",
      "calculate",
      "min",
      "feet",
      "maximum"
    ]
  },
  {
    "title": "Total Landed Cost & Gross Margin Calculator",
    "category": "Ecommerce > DTC Supply Chain • Unit Economics",
    "url": "/ecommerce/landed-cost-unit-margin/",
    "keywords": [
      "total",
      "landed",
      "cost",
      "gross",
      "margin",
      "calculator",
      "calculate",
      "true",
      "per-unit",
      "factoring",
      "fob",
      "factory"
    ]
  },
  {
    "title": "Inventory Turnover Ratio & Days Sales of Inventory (DSI) Calculator",
    "category": "Ecommerce > Working Capital • Inventory Velocity",
    "url": "/ecommerce/inventory-turnover-days-sales/",
    "keywords": [
      "inventory",
      "turnover",
      "ratio",
      "days",
      "sales",
      "dsi",
      "calculator",
      "evaluate",
      "retail",
      "merchandising",
      "velocity",
      "and"
    ]
  },
  {
    "title": "Shopping Cart Abandonment & Recovery Opportunity Calculator",
    "category": "Ecommerce > Conversion Rate Optimization • Abandonment",
    "url": "/ecommerce/cart-abandonment-revenue-loss/",
    "keywords": [
      "shopping",
      "cart",
      "abandonment",
      "recovery",
      "opportunity",
      "calculator",
      "quantify",
      "uncaptured",
      "revenue",
      "lost",
      "abandoned",
      "online"
    ]
  },
  {
    "title": "Gross Margin Return on Investment (GMROI) Calculator",
    "category": "Ecommerce > Merchandising Finance • Inventory ROI",
    "url": "/ecommerce/gmroi-retail-merchandising/",
    "keywords": [
      "gross",
      "margin",
      "return",
      "investment",
      "gmroi",
      "calculator",
      "calculate",
      "measure",
      "how",
      "many",
      "profit",
      "dollars"
    ]
  },
  {
    "title": "Amazon FBA Fulfillment Fee & Net Profit Margin Calculator",
    "category": "Ecommerce > Amazon Marketplace • Seller Economics",
    "url": "/ecommerce/amazon-fba-fee-margin/",
    "keywords": [
      "amazon",
      "fba",
      "fulfillment",
      "fee",
      "net",
      "profit",
      "margin",
      "calculator",
      "calculate",
      "exact",
      "seller",
      "central"
    ]
  },
  {
    "title": "Safety Stock & Inventory Reorder Point (ROP) Calculator",
    "category": "Ecommerce > Inventory Operations • Stockout Prevention",
    "url": "/ecommerce/safety-stock-reorder-point/",
    "keywords": [
      "safety",
      "stock",
      "inventory",
      "reorder",
      "point",
      "rop",
      "calculator",
      "calculate",
      "optimal",
      "buffer",
      "units",
      "and"
    ]
  },
  {
    "title": "Customer Lifetime Value (LTV) to CAC & Payback Calculator",
    "category": "Ecommerce > Growth Analytics • Unit Economics",
    "url": "/ecommerce/ltv-cac-payback-period/",
    "keywords": [
      "customer",
      "lifetime",
      "value",
      "ltv",
      "cac",
      "payback",
      "calculator",
      "calculate",
      "ratio",
      "and",
      "cash",
      "period"
    ]
  },
  {
    "title": "Free Shipping Threshold & AOV Optimization Calculator",
    "category": "Ecommerce > Cart Optimization • Shipping Economics",
    "url": "/ecommerce/free-shipping-threshold-aov/",
    "keywords": [
      "free",
      "shipping",
      "threshold",
      "aov",
      "optimization",
      "calculator",
      "calculate",
      "the",
      "mathematically",
      "optimal",
      "lift",
      "average"
    ]
  },
  {
    "title": "Retail Shrinkage & Loss Prevention Calculator",
    "category": "Ecommerce > Store Operations • Loss Prevention",
    "url": "/ecommerce/retail-shrinkage-loss/",
    "keywords": [
      "retail",
      "shrinkage",
      "loss",
      "prevention",
      "calculator",
      "calculate",
      "total",
      "annual",
      "inventory",
      "analyze",
      "root",
      "causes"
    ]
  },
  {
    "title": "Customer Cohort Retention & Churn Rate Calculator",
    "category": "Ecommerce > Subscription Analytics • Retention",
    "url": "/ecommerce/cohort-retention-churn/",
    "keywords": [
      "customer",
      "cohort",
      "retention",
      "churn",
      "rate",
      "calculator",
      "analyze",
      "multi-month",
      "curves",
      "across",
      "acquisition",
      "cohorts"
    ]
  },
  {
    "title": "Payment Gateway Processing Fee & Effective Merchant Discount Rate (MDR) Calculator",
    "category": "Ecommerce > Fintech & Payments • Processing Overhead",
    "url": "/ecommerce/merchant-discount-rate-stripe/",
    "keywords": [
      "payment",
      "gateway",
      "processing",
      "fee",
      "effective",
      "merchant",
      "discount",
      "rate",
      "mdr",
      "calculator",
      "calculate",
      "total"
    ]
  },
  {
    "title": "Target ROAS & Break-Even Return on Ad Spend Calculator",
    "category": "Ecommerce > Paid Media Strategy • ROAS Optimization",
    "url": "/ecommerce/target-roas-break-even/",
    "keywords": [
      "target",
      "roas",
      "break-even",
      "return",
      "spend",
      "calculator",
      "calculate",
      "exact",
      "for",
      "desired",
      "profit",
      "margins"
    ]
  },
  {
    "title": "Return Merchandise Authorization (RMA) & Reverse Logistics Cost Calculator",
    "category": "Ecommerce > Reverse Logistics • Margin Protection",
    "url": "/ecommerce/rma-reverse-logistics-cost/",
    "keywords": [
      "return",
      "merchandise",
      "authorization",
      "rma",
      "reverse",
      "logistics",
      "cost",
      "calculator",
      "calculate",
      "total",
      "true",
      "financial"
    ]
  },
  {
    "title": "Product Bundle Pricing & Elasticity Calculator",
    "category": "Ecommerce > Merchandising Strategy • Bundle Pricing",
    "url": "/ecommerce/product-bundle-pricing-elasticity/",
    "keywords": [
      "product",
      "bundle",
      "pricing",
      "elasticity",
      "calculator",
      "model",
      "promotional",
      "discounts",
      "against",
      "single-item",
      "sales",
      "forecast"
    ]
  },
  {
    "title": "Retail Markdown & Clearance Discount Optimization Calculator",
    "category": "Ecommerce > Inventory Liquidation • Markdown Pricing",
    "url": "/ecommerce/retail-markdown-optimization/",
    "keywords": [
      "retail",
      "markdown",
      "clearance",
      "discount",
      "optimization",
      "calculator",
      "calculate",
      "optimal",
      "tiers",
      "clear",
      "slow-moving",
      "inventory"
    ]
  },
  {
    "title": "Open-to-Buy (OTB) Retail Inventory Budget Calculator",
    "category": "Ecommerce > Merchandise Planning • OTB Budgeting",
    "url": "/ecommerce/open-to-buy-otb-budget/",
    "keywords": [
      "open-to-buy",
      "otb",
      "retail",
      "inventory",
      "budget",
      "calculator",
      "calculate",
      "exact",
      "monthly",
      "purchasing",
      "budgets",
      "and"
    ]
  },
  {
    "title": "Email Marketing Revenue Per Recipient (RPR) & Campaign ROI Calculator",
    "category": "Ecommerce > Retention Marketing • Email Economics",
    "url": "/ecommerce/email-revenue-per-recipient/",
    "keywords": [
      "email",
      "marketing",
      "revenue",
      "per",
      "recipient",
      "rpr",
      "campaign",
      "roi",
      "calculator",
      "evaluate",
      "broadcast",
      "and"
    ]
  },
  {
    "title": "Average Order Value (AOV) Expansion & Cross-Sell Uplift Calculator",
    "category": "Ecommerce > Conversion Rate Optimization • Cart Expansion",
    "url": "/ecommerce/aov-expansion-elasticity/",
    "keywords": [
      "average",
      "order",
      "value",
      "aov",
      "expansion",
      "cross-sell",
      "uplift",
      "calculator",
      "calculate",
      "incremental",
      "top-line",
      "and"
    ]
  },
  {
    "title": "Dropshipping vs 3PL Warehousing Profitability Calculator",
    "category": "Ecommerce > Fulfillment Strategy • 3PL vs Dropship",
    "url": "/ecommerce/dropshipping-vs-3pl-margin/",
    "keywords": [
      "dropshipping",
      "3pl",
      "warehousing",
      "profitability",
      "calculator",
      "compare",
      "net",
      "profit",
      "margins",
      "between",
      "direct",
      "supplier"
    ]
  },
  {
    "title": "Net Promoter Score (NPS) & Customer Sentiment Index Calculator",
    "category": "Ecommerce > Customer Loyalty • NPS Sentiment",
    "url": "/ecommerce/nps-customer-satisfaction/",
    "keywords": [
      "net",
      "promoter",
      "score",
      "nps",
      "customer",
      "sentiment",
      "index",
      "calculator",
      "calculate",
      "your",
      "store",
      "from"
    ]
  },
  {
    "title": "Tiered Affiliate Marketing Commission & Payout Calculator",
    "category": "Ecommerce > Partner Marketing • Affiliate Economics",
    "url": "/ecommerce/tiered-affiliate-commission/",
    "keywords": [
      "tiered",
      "affiliate",
      "marketing",
      "commission",
      "payout",
      "calculator",
      "calculate",
      "blended",
      "payouts",
      "network",
      "platform",
      "tracking"
    ]
  },
  {
    "title": "Monthly Recurring Revenue (MRR) Net Expansion & Contraction Calculator",
    "category": "Ecommerce > SaaS & Subscriptions • MRR Velocity",
    "url": "/ecommerce/mrr-expansion-contraction/",
    "keywords": [
      "monthly",
      "recurring",
      "revenue",
      "mrr",
      "net",
      "expansion",
      "contraction",
      "calculator",
      "calculate",
      "new",
      "retention",
      "nrr"
    ]
  },
  {
    "title": "BOGO (Buy One Get One) Promotional Profit Margin Calculator",
    "category": "Ecommerce > Promotional Pricing • BOGO Economics",
    "url": "/ecommerce/bogo-buy-one-get-one-margin/",
    "keywords": [
      "bogo",
      "buy",
      "one",
      "get",
      "promotional",
      "profit",
      "margin",
      "calculator",
      "calculate",
      "the",
      "real",
      "dilution"
    ]
  },
  {
    "title": "E-Commerce Return Reserve & Allowance Fund Calculator",
    "category": "Ecommerce > Financial Accounting • Return Reserves",
    "url": "/ecommerce/ecommerce-return-reserve/",
    "keywords": [
      "e-commerce",
      "return",
      "reserve",
      "allowance",
      "fund",
      "calculator",
      "calculate",
      "gaap",
      "ifrs",
      "compliant",
      "reserves",
      "prevent"
    ]
  },
  {
    "title": "Influencer Marketing Campaign ROAS & EMV Calculator",
    "category": "Ecommerce > Influencer Partnerships • Campaign ROAS",
    "url": "/ecommerce/influencer-marketing-roas/",
    "keywords": [
      "influencer",
      "marketing",
      "campaign",
      "roas",
      "emv",
      "calculator",
      "calculate",
      "return",
      "spend",
      "customer",
      "acquisition",
      "cost"
    ]
  },
  {
    "title": "Deadstock Holding Cost & Liquidation Cashflow Calculator",
    "category": "Ecommerce > Warehouse Operations • Deadstock Recovery",
    "url": "/ecommerce/deadstock-liquidation-cashflow/",
    "keywords": [
      "deadstock",
      "holding",
      "cost",
      "liquidation",
      "cashflow",
      "calculator",
      "calculate",
      "true",
      "monthly",
      "carrying",
      "losses",
      "inventory"
    ]
  },
  {
    "title": "Retail Store Sales Per Square Foot & Space Productivity Calculator",
    "category": "Ecommerce > Brick & Mortar • Space Productivity",
    "url": "/ecommerce/retail-sales-per-square-foot/",
    "keywords": [
      "retail",
      "store",
      "sales",
      "per",
      "square",
      "foot",
      "space",
      "productivity",
      "calculator",
      "calculate",
      "analyze",
      "selling"
    ]
  },
  {
    "title": "Direct Mail Postcard & Catalog Campaign ROI Calculator",
    "category": "Ecommerce > Offline Marketing • Direct Mail ROI",
    "url": "/ecommerce/direct-mail-catalog-roi/",
    "keywords": [
      "direct",
      "mail",
      "postcard",
      "catalog",
      "campaign",
      "roi",
      "calculator",
      "calculate",
      "customer",
      "acquisition",
      "cost",
      "cpa"
    ]
  },
  {
    "title": "Customs Import Duty & Section 301 Tariff Calculator",
    "category": "Ecommerce > International Trade • Customs Tariffs",
    "url": "/ecommerce/customs-import-duty-hts/",
    "keywords": [
      "customs",
      "import",
      "duty",
      "section",
      "301",
      "tariff",
      "calculator",
      "calculate",
      "duties",
      "china",
      "trade",
      "tariffs"
    ]
  },
  {
    "title": "Economic Order Quantity (EOQ) & Total Cost of Inventory Calculator",
    "category": "Ecommerce > Supply Chain Operations • EOQ Model",
    "url": "/ecommerce/retail-replenishment-lead-time-eoq/",
    "keywords": [
      "economic",
      "order",
      "quantity",
      "eoq",
      "total",
      "cost",
      "inventory",
      "calculator",
      "calculate",
      "the",
      "mathematically",
      "optimal"
    ]
  },
  {
    "title": "Pharmacokinetics Drug Elimination Half-Life (t½) & Clearance Calculator",
    "category": "Biotech > Pharmacokinetics • Drug Metabolism",
    "url": "/biotech/drug-elimination-half-life/",
    "keywords": [
      "pharmacokinetics",
      "drug",
      "elimination",
      "half-life",
      "clearance",
      "calculator",
      "calculate",
      "rate",
      "constant",
      "systemic",
      "and",
      "time"
    ]
  },
  {
    "title": "Cockcroft-Gault Creatinine Clearance (CrCl) & Renal Dosing Calculator",
    "category": "Biotech > Clinical Pharmacology • Renal Function",
    "url": "/biotech/cockcroft-gault-crcl/",
    "keywords": [
      "cockcroft-gault",
      "creatinine",
      "clearance",
      "crcl",
      "renal",
      "dosing",
      "calculator",
      "calculate",
      "estimated",
      "via",
      "the",
      "standard"
    ]
  },
  {
    "title": "IV Drip Rate & Infusion Velocity Calculator",
    "category": "Biotech > Clinical Nursing • IV Pharmacology",
    "url": "/biotech/iv-drip-infusion-rate/",
    "keywords": [
      "drip",
      "rate",
      "infusion",
      "velocity",
      "calculator",
      "calculate",
      "electronic",
      "pump",
      "rates",
      "and",
      "gravity",
      "drops"
    ]
  },
  {
    "title": "PCR Primer Melting Temperature (Tm) & Annealing Calculator",
    "category": "Biotech > Molecular Biology • PCR Design",
    "url": "/biotech/pcr-primer-tm/",
    "keywords": [
      "pcr",
      "primer",
      "melting",
      "temperature",
      "annealing",
      "calculator",
      "calculate",
      "dna",
      "oligonucleotide",
      "via",
      "the",
      "wallace"
    ]
  },
  {
    "title": "Michaelis-Menten Enzyme Kinetics & Lineweaver-Burk Calculator",
    "category": "Biotech > Enzymology • Enzyme Kinetics",
    "url": "/biotech/michaelis-menten-kinetics/",
    "keywords": [
      "michaelis-menten",
      "enzyme",
      "kinetics",
      "lineweaver-burk",
      "calculator",
      "calculate",
      "steady-state",
      "reaction",
      "velocity",
      "maximum",
      "vmax",
      "michaelis"
    ]
  },
  {
    "title": "Body Surface Area (BSA) Calculator (Mosteller & Du Bois Formulas)",
    "category": "Biotech > Clinical Oncology • BSA Dosing",
    "url": "/biotech/body-surface-area-mosteller/",
    "keywords": [
      "body",
      "surface",
      "area",
      "bsa",
      "calculator",
      "mosteller",
      "bois",
      "formulas",
      "calculate",
      "adult",
      "and",
      "pediatric"
    ]
  },
  {
    "title": "Laboratory Serial Dilution & Stock Solution Concentration (C₁V₁ = C₂V₂) Calculator",
    "category": "Biotech > Wet Lab Chemistry • Dilution Math",
    "url": "/biotech/serial-dilution-c1v1/",
    "keywords": [
      "laboratory",
      "serial",
      "dilution",
      "stock",
      "solution",
      "concentration",
      "calculator",
      "calculate",
      "volume",
      "buffer",
      "diluent",
      "required"
    ]
  },
  {
    "title": "In Vitro Cell Culture Doubling Time & Specific Growth Rate Calculator",
    "category": "Biotech > Cell Biology • Cell Proliferation",
    "url": "/biotech/cell-culture-doubling-time/",
    "keywords": [
      "vitro",
      "cell",
      "culture",
      "doubling",
      "time",
      "specific",
      "growth",
      "rate",
      "calculator",
      "calculate",
      "mammalian",
      "and"
    ]
  },
  {
    "title": "Beer-Lambert Law Spectrophotometry & Protein Concentration Calculator",
    "category": "Biotech > Biochemistry • UV-Vis Spectroscopy",
    "url": "/biotech/beer-lambert-spectrophotometry/",
    "keywords": [
      "beer-lambert",
      "law",
      "spectrophotometry",
      "protein",
      "concentration",
      "calculator",
      "calculate",
      "solute",
      "molar",
      "absorbance",
      "and",
      "percent"
    ]
  },
  {
    "title": "Hemocytometer Cell Count & Trypan Blue Viability Calculator",
    "category": "Biotech > Laboratory Protocols • Cell Counting",
    "url": "/biotech/hemocytometer-cell-viability/",
    "keywords": [
      "hemocytometer",
      "cell",
      "count",
      "trypan",
      "blue",
      "viability",
      "calculator",
      "calculate",
      "total",
      "concentration",
      "cells",
      "percentage"
    ]
  },
  {
    "title": "Henderson-Hasselbalch Buffer pH & Acid-Base Equilibrium Calculator",
    "category": "Biotech > Physical Biochemistry • Buffer Systems",
    "url": "/biotech/henderson-hasselbalch-ph/",
    "keywords": [
      "henderson-hasselbalch",
      "buffer",
      "acid-base",
      "equilibrium",
      "calculator",
      "calculate",
      "aqueous",
      "solution",
      "conjugate",
      "ratios",
      "and",
      "capacity"
    ]
  },
  {
    "title": "Centrifuge Relative Centrifugal Force (RCF / g-Force) & RPM Calculator",
    "category": "Biotech > Laboratory Centrifugation • RCF Math",
    "url": "/biotech/centrifuge-rcf-g-force/",
    "keywords": [
      "centrifuge",
      "relative",
      "centrifugal",
      "force",
      "rcf",
      "g-force",
      "rpm",
      "calculator",
      "convert",
      "between",
      "rotational",
      "speed"
    ]
  },
  {
    "title": "Clinical Trial Sample Size & Statistical Power Calculator",
    "category": "Biotech > Biostatistics • Clinical Trial Design",
    "url": "/biotech/clinical-trial-sample-size/",
    "keywords": [
      "clinical",
      "trial",
      "sample",
      "size",
      "statistical",
      "power",
      "calculator",
      "calculate",
      "required",
      "patient",
      "per",
      "treatment"
    ]
  },
  {
    "title": "Hazard Ratio (HR), Relative Risk (RR) & Odds Ratio (OR) Calculator",
    "category": "Biotech > Evidence-Based Medicine • Clinical Epidemiology",
    "url": "/biotech/hazard-ratio-relative-risk/",
    "keywords": [
      "hazard",
      "ratio",
      "relative",
      "risk",
      "odds",
      "calculator",
      "calculate",
      "clinical",
      "evidence",
      "metrics",
      "including",
      "reduction"
    ]
  },
  {
    "title": "Clinical Diagnostic Test Sensitivity, Specificity & Predictive Value (PPV/NPV) Calculator",
    "category": "Biotech > Diagnostic Medicine • Test Performance",
    "url": "/biotech/diagnostic-sensitivity-specificity/",
    "keywords": [
      "clinical",
      "diagnostic",
      "test",
      "sensitivity",
      "specificity",
      "predictive",
      "value",
      "ppv",
      "npv",
      "calculator",
      "calculate",
      "positive"
    ]
  },
  {
    "title": "Solution Molarity, Molality & Normality Preparation Calculator",
    "category": "Biotech > Analytical Chemistry • Solution Prep",
    "url": "/biotech/molarity-normality-solution/",
    "keywords": [
      "solution",
      "molarity",
      "molality",
      "normality",
      "preparation",
      "calculator",
      "calculate",
      "chemical",
      "solute",
      "mass",
      "required",
      "grams"
    ]
  },
  {
    "title": "Radioactive Isotope Exponential Decay & Specific Activity Calculator",
    "category": "Biotech > Nuclear Medicine • Radiobiology",
    "url": "/biotech/radioisotope-decay-law/",
    "keywords": [
      "radioactive",
      "isotope",
      "exponential",
      "decay",
      "specific",
      "activity",
      "calculator",
      "calculate",
      "residual",
      "radioactivity",
      "constants",
      "remaining"
    ]
  },
  {
    "title": "Diabetes Insulin-to-Carb Ratio (ICR) & Insulin Sensitivity Factor (ISF) Calculator",
    "category": "Biotech > Endocrinology • Diabetes Pharmacotherapy",
    "url": "/biotech/insulin-carb-ratio-isf/",
    "keywords": [
      "diabetes",
      "insulin-to-carb",
      "ratio",
      "icr",
      "insulin",
      "sensitivity",
      "factor",
      "isf",
      "calculator",
      "calculate",
      "individualized",
      "rapid-acting"
    ]
  },
  {
    "title": "Arterial Blood Gas (ABG) & Serum Anion Gap Calculator",
    "category": "Biotech > Critical Care Medicine • ABG Diagnostics",
    "url": "/biotech/arterial-blood-gas-anion-gap/",
    "keywords": [
      "arterial",
      "blood",
      "gas",
      "abg",
      "serum",
      "anion",
      "gap",
      "calculator",
      "interpret",
      "acid-base",
      "disorders",
      "calculate"
    ]
  },
  {
    "title": "Quantitative Real-Time PCR (qPCR) 2^(-ΔΔCt) Relative Gene Expression Calculator",
    "category": "Biotech > Genomics • qPCR Quantification",
    "url": "/biotech/qpcr-delta-delta-ct/",
    "keywords": [
      "quantitative",
      "real-time",
      "pcr",
      "qpcr",
      "relative",
      "gene",
      "expression",
      "calculator",
      "calculate",
      "fold",
      "change",
      "rt-qpcr"
    ]
  },
  {
    "title": "Recombinant Protein Fermentation Yield & Specific Productivity Calculator",
    "category": "Biotech > Bioprocessing • Fermentation Scale-Up",
    "url": "/biotech/recombinant-protein-yield/",
    "keywords": [
      "recombinant",
      "protein",
      "fermentation",
      "yield",
      "specific",
      "productivity",
      "calculator",
      "calculate",
      "total",
      "cellular",
      "volumetric",
      "and"
    ]
  },
  {
    "title": "Maintenance IV Fluid Requirements (Holliday-Segar 4-2-1 Rule) Calculator",
    "category": "Biotech > Pediatric Critical Care • Fluid Maintenance",
    "url": "/biotech/maintenance-fluid-pediatric/",
    "keywords": [
      "maintenance",
      "fluid",
      "requirements",
      "holliday-segar",
      "4-2-1",
      "rule",
      "calculator",
      "calculate",
      "daily",
      "and",
      "hourly",
      "for"
    ]
  },
  {
    "title": "Apparent Volume of Distribution (Vd) & Loading Dose Calculator",
    "category": "Biotech > Clinical Pharmacokinetics • Loading Dose",
    "url": "/biotech/drug-volume-of-distribution/",
    "keywords": [
      "apparent",
      "volume",
      "distribution",
      "loading",
      "dose",
      "calculator",
      "calculate",
      "and",
      "determine",
      "exact",
      "intravenous",
      "oral"
    ]
  },
  {
    "title": "Biostatistical Cohen's d Effect Size & Standardized Mean Difference Calculator",
    "category": "Biotech > Meta-Analysis • Statistical Effect Size",
    "url": "/biotech/cohen-d-effect-size/",
    "keywords": [
      "biostatistical",
      "cohen",
      "effect",
      "size",
      "standardized",
      "mean",
      "difference",
      "calculator",
      "calculate",
      "hedges",
      "unbiased",
      "small-sample"
    ]
  },
  {
    "title": "Toxicology Therapeutic Index (TI) & Margin of Safety (MOS) Calculator",
    "category": "Biotech > Preclinical Toxicology • Drug Safety",
    "url": "/biotech/ld50-therapeutic-index/",
    "keywords": [
      "toxicology",
      "therapeutic",
      "index",
      "margin",
      "safety",
      "mos",
      "calculator",
      "calculate",
      "certain",
      "factor",
      "and",
      "drug"
    ]
  },
  {
    "title": "Generator Sizing Calculator",
    "category": "Engineering > Electrical Engineering • IEEE 446 Invariants",
    "url": "/engineering/generator-sizing/",
    "keywords": [
      "generator",
      "sizing",
      "calculator",
      "calculate",
      "required",
      "home",
      "size",
      "running",
      "watts",
      "peak",
      "surge",
      "and"
    ]
  },
  {
    "title": "Wire Gauge & Voltage Drop Calculator",
    "category": "Engineering > Electrical Engineering • NFPA 70 / NEC Standard",
    "url": "/engineering/wire-gauge-voltage-drop/",
    "keywords": [
      "wire",
      "gauge",
      "voltage",
      "drop",
      "calculator",
      "calculate",
      "and",
      "minimum",
      "awg",
      "for",
      "circuits",
      "compliant"
    ]
  },
  {
    "title": "Home Battery Backup Storage Calculator",
    "category": "Engineering > Renewable Energy & Storage • IEEE 2030 Invariants",
    "url": "/engineering/battery-backup-storage/",
    "keywords": [
      "home",
      "battery",
      "backup",
      "storage",
      "calculator",
      "calculate",
      "bank",
      "capacity",
      "kwh",
      "and",
      "amp-hours",
      "for"
    ]
  },
  {
    "title": "HECM Reverse Mortgage Calculator",
    "category": "Finance > Actuarial Finance • HUD / FHA Invariants",
    "url": "/finance/reverse-mortgage-hecm/",
    "keywords": [
      "hecm",
      "reverse",
      "mortgage",
      "calculator",
      "calculate",
      "fha",
      "proceeds",
      "principal",
      "limit",
      "factors",
      "and",
      "net"
    ]
  },
  {
    "title": "Section 199A QBI Calculator",
    "category": "Finance > Tax Law & Quantitative Accounting • IRC § 199A Invariants",
    "url": "/finance/section-199a-qbi/",
    "keywords": [
      "section",
      "199a",
      "qbi",
      "calculator",
      "calculate",
      "your",
      "irs",
      "deduction",
      "phase-out",
      "limits",
      "w-2",
      "wage"
    ]
  },
  {
    "title": "RV & Camper Loan Calculator",
    "category": "Finance > Consumer Lending & Asset Finance • Amortization Invariants",
    "url": "/finance/rv-loan/",
    "keywords": [
      "camper",
      "loan",
      "calculator",
      "calculate",
      "and",
      "motorhome",
      "monthly",
      "payments",
      "interest",
      "cost",
      "amortization",
      "schedules"
    ]
  },
  {
    "title": "Equity IRR & Real Estate Return Calculator",
    "category": "Finance > Quantitative Finance & Private Equity • Cash Flow Invariants",
    "url": "/finance/equity-irr/",
    "keywords": [
      "equity",
      "irr",
      "real",
      "estate",
      "return",
      "calculator",
      "calculate",
      "levered",
      "internal",
      "rate",
      "multiple",
      "moic"
    ]
  },
  {
    "title": "qPCR Primer Tm & Annealing Calculator",
    "category": "Biotech > Molecular Biology & Genomics • SantaLucia Invariants",
    "url": "/biotech/qpcr-primer-tm/",
    "keywords": [
      "qpcr",
      "primer",
      "annealing",
      "calculator",
      "calculate",
      "exact",
      "and",
      "pcr",
      "melting",
      "temperature",
      "using",
      "santalucia"
    ]
  },
  {
    "title": "US Navy Body Fat Calculator",
    "category": "Health > Military Physiology • DoD Instruction 1308.3 Standard",
    "url": "/health/navy-body-fat/",
    "keywords": [
      "navy",
      "body",
      "fat",
      "calculator",
      "calculate",
      "percentage",
      "using",
      "the",
      "official",
      "circumference",
      "formula",
      "dod"
    ]
  },
  {
    "title": "Smoking Cost & Lifetime Wealth Calculator",
    "category": "Health > Public Health & Actuarial Wealth • Compounding Invariants",
    "url": "/health/cost-of-smoking/",
    "keywords": [
      "smoking",
      "cost",
      "lifetime",
      "wealth",
      "calculator",
      "calculate",
      "the",
      "true",
      "including",
      "annual",
      "out-of-pocket",
      "expenses"
    ]
  },
  {
    "title": "Concrete Volume Calculator",
    "category": "Construction > Trades & Civil Engineering • ASTM C94 Invariants",
    "url": "/construction/concrete-volume/",
    "keywords": [
      "concrete",
      "volume",
      "calculator",
      "calculate",
      "exact",
      "cubic",
      "yards",
      "and",
      "meters",
      "for",
      "slabs",
      "footings"
    ]
  },
  {
    "title": "Rebar Grid & Spacing Calculator",
    "category": "Construction > Structural Engineering • ACI 318 Standard",
    "url": "/construction/rebar-calculator/",
    "keywords": [
      "rebar",
      "grid",
      "spacing",
      "calculator",
      "calculate",
      "total",
      "linear",
      "footage",
      "bar",
      "count",
      "weight",
      "and"
    ]
  },
  {
    "title": "Drywall & Mud/Fastener Estimator",
    "category": "Construction > Trades & Residential Remodeling • Finish Invariants",
    "url": "/construction/drywall/",
    "keywords": [
      "drywall",
      "mud",
      "fastener",
      "estimator",
      "calculate",
      "sheets",
      "joint",
      "compound",
      "buckets",
      "tape",
      "and",
      "screws"
    ]
  },
  {
    "title": "HVAC Furnace & Heating BTU Calculator",
    "category": "Engineering > Mechanical Engineering • ASHRAE Fundamentals",
    "url": "/engineering/hvac-furnace-sizing/",
    "keywords": [
      "hvac",
      "furnace",
      "heating",
      "btu",
      "calculator",
      "calculate",
      "required",
      "capacity",
      "btus",
      "and",
      "tons",
      "based"
    ]
  },
  {
    "title": "Lean-To Roof Pitch & Rafter Calculator",
    "category": "Geometry > Applied Geometry & Carpentry • Trigonometric Invariants",
    "url": "/geometry/2d/lean-to-roof-pitch/",
    "keywords": [
      "lean-to",
      "roof",
      "pitch",
      "rafter",
      "calculator",
      "calculate",
      "shed",
      "ratio",
      "angle",
      "degrees",
      "true",
      "length"
    ]
  },
  {
    "title": "Slant Height Calculator",
    "category": "Geometry > 3D Euclidean Geometry • Pythagorean Invariants",
    "url": "/geometry/slant-height/",
    "keywords": [
      "slant",
      "height",
      "calculator",
      "calculate",
      "surface",
      "area",
      "and",
      "lateral",
      "pitch",
      "for",
      "right",
      "circular"
    ]
  },
  {
    "title": "LCL Freight & CBM Calculator",
    "category": "Logistics > Ocean Freight & Global Logistics • Incoterms 2026 Invariants",
    "url": "/logistics/lcl-freight-cbm/",
    "keywords": [
      "lcl",
      "freight",
      "cbm",
      "calculator",
      "calculate",
      "ocean",
      "chargeable",
      "weight",
      "rule",
      "volumetric",
      "container",
      "packing"
    ]
  },
  {
    "title": "Tubular Reabsorption of Phosphate (%TRP) & TmP/GFR Calculator",
    "category": "Biotech > Clinical Nephrology & Endocrinology • Walton-Bijvoet Invariants",
    "url": "/biotech/tubular-reabsorption-phosphate-trp/",
    "keywords": [
      "tubular",
      "reabsorption",
      "phosphate",
      "trp",
      "tmp",
      "gfr",
      "calculator",
      "calculate",
      "and",
      "ratio",
      "using",
      "serum"
    ]
  },
  {
    "title": "Brick Soling & Flat Masonry Area Calculator",
    "category": "Construction > Civil Construction & Pavements • IS 2212 / ASTM C902",
    "url": "/construction/brick-soling/",
    "keywords": [
      "brick",
      "soling",
      "flat",
      "masonry",
      "area",
      "calculator",
      "calculate",
      "count",
      "bedding",
      "sand",
      "volume",
      "and"
    ]
  },
  {
    "title": "Ultrasonic Angle Beam Path & Sound Path Distance Calculator",
    "category": "Engineering > Non-Destructive Testing (NDT) • ASME Sec V / AWS D1.1",
    "url": "/engineering/ultrasonic-beam-path/",
    "keywords": [
      "ultrasonic",
      "angle",
      "beam",
      "path",
      "sound",
      "distance",
      "calculator",
      "calculate",
      "ndt",
      "shear",
      "wave",
      "surface"
    ]
  },
  {
    "title": "Drill Pipe & Casing Well Displacement Calculator",
    "category": "Engineering > Petroleum & Drilling Engineering • API RP 13B Invariants",
    "url": "/engineering/drill-pipe-displacement/",
    "keywords": [
      "drill",
      "pipe",
      "casing",
      "well",
      "displacement",
      "calculator",
      "calculate",
      "collar",
      "and",
      "bbl",
      "pit",
      "volume"
    ]
  },
  {
    "title": "Aerodynamic Drag & Downforce Force Calculator",
    "category": "Physics > Fluid Dynamics & Aerodynamics • Navier-Stokes Invariants",
    "url": "/physics/aerodynamic-drag-force/",
    "keywords": [
      "aerodynamic",
      "drag",
      "downforce",
      "force",
      "calculator",
      "calculate",
      "lbf",
      "power",
      "required",
      "overcome",
      "and",
      "terminal"
    ]
  },
  {
    "title": "Commercial Battery Peak Shaving & Demand Charge Calculator",
    "category": "Energy > Power Systems & Energy Storage • IEEE 1547 / C&I Energy",
    "url": "/energy/battery-peak-shaving/",
    "keywords": [
      "commercial",
      "battery",
      "peak",
      "shaving",
      "demand",
      "charge",
      "calculator",
      "calculate",
      "energy",
      "storage",
      "capacity",
      "kwh"
    ]
  },
  {
    "title": "Flowable Fill (CLSM) Volume & Mix Calculator",
    "category": "Construction > Civil Infrastructure & Utilities • ACI 229R / ASTM D6103",
    "url": "/construction/flowable-fill-clsm/",
    "keywords": [
      "flowable",
      "fill",
      "clsm",
      "volume",
      "mix",
      "calculator",
      "calculate",
      "controlled",
      "low-strength",
      "material",
      "cubic",
      "yards"
    ]
  },
  {
    "title": "Retaining Wall Overturning & Sliding Safety Factor Calculator",
    "category": "Engineering > Geotechnical & Structural Engineering • Rankine / IBC 1807",
    "url": "/engineering/retaining-wall-overturning-safety/",
    "keywords": [
      "retaining",
      "wall",
      "overturning",
      "sliding",
      "safety",
      "factor",
      "calculator",
      "calculate",
      "factors",
      "against",
      "and",
      "for"
    ]
  },
  {
    "title": "Column Slenderness Ratio & Critical Buckling Load Calculator",
    "category": "Engineering > Structural Mechanics & Steel Design • AISC 360-22 Standard",
    "url": "/engineering/column-slenderness-buckling/",
    "keywords": [
      "column",
      "slenderness",
      "ratio",
      "critical",
      "buckling",
      "load",
      "calculator",
      "calculate",
      "effective",
      "euler",
      "stress",
      "and"
    ]
  },
  {
    "title": "Unistrut Channel Beam Load & Deflection Calculator",
    "category": "Construction > Structural Framing & MEP Supports • MFMA-4 Standards",
    "url": "/construction/unistrut-load-capacity/",
    "keywords": [
      "unistrut",
      "channel",
      "beam",
      "load",
      "deflection",
      "calculator",
      "calculate",
      "maximum",
      "allowable",
      "and",
      "for",
      "standard"
    ]
  },
  {
    "title": "Relative Response Factor (RRF) HPLC Calculator",
    "category": "Biotech > Pharmaceutical Analytical Chemistry • ICH Q3A/B & USP <621>",
    "url": "/biotech/relative-response-factor-rrf/",
    "keywords": [
      "relative",
      "response",
      "factor",
      "rrf",
      "hplc",
      "calculator",
      "calculate",
      "factors",
      "and",
      "true",
      "impurity",
      "weight"
    ]
  },
  {
    "title": "Micromolar to ng/mL Mass-Molar Concentration Converter",
    "category": "Biotech > Quantitative Biochemistry & Pharmacology • IUPAC Invariants",
    "url": "/biotech/molar-mass-concentration-converter/",
    "keywords": [
      "micromolar",
      "mass-molar",
      "concentration",
      "converter",
      "convert",
      "molarity",
      "mass",
      "with",
      "molecular",
      "weight",
      "precision",
      "pharmacology"
    ]
  },
  {
    "title": "Concrete Haunch & Chamfer Reinforcement Calculator",
    "category": "Engineering > Structural Concrete Design • ACI 318-19 / AASHTO LRFD",
    "url": "/engineering/concrete-haunch-reinforcement/",
    "keywords": [
      "concrete",
      "haunch",
      "chamfer",
      "reinforcement",
      "calculator",
      "calculate",
      "dimensions",
      "bevel",
      "angle",
      "diagonal",
      "rebar",
      "lengths"
    ]
  },
  {
    "title": "Analytical Evaluation Threshold (AET) Calculator",
    "category": "Biotech > Extractables & Leachables (E&L) • PQRI & ISO 10993-18",
    "url": "/biotech/analytical-evaluation-threshold-aet/",
    "keywords": [
      "analytical",
      "evaluation",
      "threshold",
      "aet",
      "calculator",
      "calculate",
      "the",
      "for",
      "extractables",
      "and",
      "leachables",
      "testing"
    ]
  },
  {
    "title": "Relative Potency Bioassay Calculator",
    "category": "Biotech > Biopharmaceutical Bioassays • USP <1032>/<1034> & Ph. Eur. 5.3",
    "url": "/biotech/relative-potency-bioassay/",
    "keywords": [
      "relative",
      "potency",
      "bioassay",
      "calculator",
      "calculate",
      "and",
      "fieller",
      "confidence",
      "intervals",
      "for",
      "parallel-line",
      "4-parameter"
    ]
  },
  {
    "title": "HPLC Column Theoretical Plates & Resolution Calculator",
    "category": "Biotech > Chromatography & Quality Control • USP <621> / EP 2.2.46",
    "url": "/biotech/chromatography-resolution/",
    "keywords": [
      "hplc",
      "column",
      "theoretical",
      "plates",
      "resolution",
      "calculator",
      "calculate",
      "usp",
      "plate",
      "count",
      "chromatographic",
      "peak"
    ]
  },
  {
    "title": "Syringe Pump & Microfluidic Flow Rate Calculator",
    "category": "Biotech > Laboratory Automation & Microfluidics • ISO 7886 Standard",
    "url": "/biotech/syringe-pump-injection-rate/",
    "keywords": [
      "syringe",
      "pump",
      "microfluidic",
      "flow",
      "rate",
      "calculator",
      "calculate",
      "volumetric",
      "linear",
      "stepper",
      "motor",
      "pusher"
    ]
  },
  {
    "title": "ASC 842 / IFRS 16 Incremental Borrowing Rate (IBR) Calculator",
    "category": "Finance > Lease Accounting Standards • GAAP ASC 842 & IFRS 16",
    "url": "/finance/incremental-borrowing-rate-lease/",
    "keywords": [
      "asc",
      "842",
      "ifrs",
      "incremental",
      "borrowing",
      "rate",
      "ibr",
      "calculator",
      "calculate",
      "corporate",
      "lease",
      "rates"
    ]
  },
  {
    "title": "Circumferential & Surface Cutting Speed Calculator",
    "category": "Physics > Machining & Kinematics • ISO 3002 Cutting Tool Standard",
    "url": "/physics/circumferential-surface-speed/",
    "keywords": [
      "circumferential",
      "surface",
      "cutting",
      "speed",
      "calculator",
      "calculate",
      "tangential",
      "sfm",
      "min",
      "and",
      "from",
      "rpm"
    ]
  },
  {
    "title": "Hydraulic Cylinder Force & Fluid Flow Calculator",
    "category": "Engineering > Fluid Power & Mobile Hydraulics • ISO 3320 / NFPA Invariants",
    "url": "/engineering/hydraulic-cylinder-flow/",
    "keywords": [
      "hydraulic",
      "cylinder",
      "force",
      "fluid",
      "flow",
      "calculator",
      "calculate",
      "extension",
      "and",
      "retraction",
      "lbs",
      "stroke"
    ]
  }
];

  // Theme Management
  function initTheme() {
    const savedTheme = localStorage.getItem('omni-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      toggleBtn.setAttribute('title', savedTheme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme');

      toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('omni-theme', next);
        toggleBtn.innerHTML = next === 'dark' ? '☀️' : '🌙';
        toggleBtn.setAttribute('title', next === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme');
      });
    }
  }

  // Search Modal Management
  function initSearch() {
    const modal = document.getElementById('search-modal');
    const input = document.getElementById('search-modal-input');
    const resultsContainer = document.getElementById('search-modal-results');
    const triggerBtns = document.querySelectorAll('.search-btn-trigger');

    if (!modal || !input || !resultsContainer) return;

    function openModal() {
      modal.classList.add('active');
      input.value = '';
      renderResults(SEARCH_INDEX.slice(0, 5));
      setTimeout(() => input.focus(), 50);
    }

    function closeModal() {
      modal.classList.remove('active');
    }

    triggerBtns.forEach(btn => btn.addEventListener('click', openModal));

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        modal.classList.contains('active') ? closeModal() : openModal();
      } else if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });

    input.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        renderResults(SEARCH_INDEX.slice(0, 5));
        return;
      }

      const matches = SEARCH_INDEX.filter(item => {
        return item.title.toLowerCase().includes(q) ||
               item.category.toLowerCase().includes(q) ||
               item.keywords.some(k => k.toLowerCase().includes(q));
      });

      renderResults(matches);
    });

    function renderResults(items) {
      if (!items || items.length === 0) {
        resultsContainer.innerHTML = `<li style="padding:1.5rem; text-align:center; color:var(--text-muted);">No calculators found matching your query.</li>`;
        return;
      }

      resultsContainer.innerHTML = items.map(item => `
        <li class="search-result-item">
          <a href="${item.url}">
            <span class="search-result-title">${item.title}</span>
            <span class="search-result-category">${item.category}</span>
          </a>
        </li>
      `).join('');
    }
  }

  // Global FAQ Accordion Toggle Delegation (Capture Phase to avoid legacy inline listener collisions)
  function initFaqToggles() {
    document.addEventListener('click', (e) => {
      const question = e.target.closest('.faq-question');
      if (!question) return;

      // Stop propagation so legacy direct element click listeners do not execute and double-toggle!
      e.stopPropagation();
      e.stopImmediatePropagation();

      const item = question.closest('.faq-item') || question.parentElement;
      if (item) {
        item.classList.toggle('open');
      }
    }, true); // true = Capturing phase!
  }

  // Universal Calculator Embed Modal & 1-Click Code Exporter
  window.openOmniEmbedModal = function () {
    let modal = document.getElementById('omni-embed-modal');
    if (!modal) {
      modal = createModalDOM();
    }
    if (modal) {
      updateEmbedCode(modal);
      modal.classList.add('is-open', 'active');
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  };
  window.closeOmniEmbedModal = function () {
    const modal = document.getElementById('omni-embed-modal');
    if (modal) {
      modal.classList.remove('is-open', 'active');
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  };
  window.openEmbedModal = window.openOmniEmbedModal;

  function getCleanUrls() {
    const rawPath = window.location.pathname.replace(/^\/embed\//, '').replace(/\/$/, '').replace(/^\//, '');
    const canonicalLink = document.querySelector('link[rel="canonical"]');
    const canonicalUrl = canonicalLink ? canonicalLink.href : ('https://omnioperand.com/' + (rawPath ? rawPath + '/' : ''));
    const embedUrl = 'https://omnioperand.com/embed/' + (rawPath ? rawPath + '/' : '');
    const toolTitle = document.querySelector('h1')?.textContent?.trim() || document.title.split('—')[0].split('|')[0].trim() || 'Calculator';
    return { canonicalUrl, embedUrl, toolTitle };
  }

  function getIframeSnippet(embedUrl, canonicalUrl, toolTitle) {
    return `<iframe src="${embedUrl}" width="100%" height="720" frameborder="0" style="border:1px solid #1e293b;border-radius:12px;width:100%;max-width:100%;box-shadow:0 8px 30px rgba(0,0,0,0.3);"></iframe>\n<p style="font-size:12px;color:#64748b;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin-top:6px;text-align:right;">Calculator powered by <a href="${canonicalUrl}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;font-weight:600;">OmniOperand ${toolTitle}</a></p>`;
  }

  function getBacklinkSnippet(canonicalUrl, toolTitle) {
    return `<a href="${canonicalUrl}" target="_blank" rel="noopener" style="font-family:sans-serif;color:#0284c7;font-weight:600;text-decoration:none;">Interactive ${toolTitle} by OmniOperand</a>`;
  }

  function updateEmbedCode(modal) {
    const { canonicalUrl, embedUrl, toolTitle } = getCleanUrls();
    const textarea = modal.querySelector('#omni-embed-code-textarea');
    const activeTab = modal.querySelector('.omni-tab-active');
    const isIframe = !activeTab || activeTab.id === 'tab-embed-iframe';
    if (textarea) {
      textarea.value = isIframe ? getIframeSnippet(embedUrl, canonicalUrl, toolTitle) : getBacklinkSnippet(canonicalUrl, toolTitle);
    }
  }

  function createModalDOM() {
    let existing = document.getElementById('omni-embed-modal');
    if (existing) return existing;

    const { canonicalUrl, embedUrl, toolTitle } = getCleanUrls();
    const iframeCode = getIframeSnippet(embedUrl, canonicalUrl, toolTitle);

    const modalHtml = `
      <div id="omni-embed-modal" class="omni-modal-overlay" style="display:none; position:fixed; inset:0; width:100%; height:100%; background:rgba(3,7,18,0.85); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); z-index:99999; align-items:center; justify-content:center; padding:1rem; box-sizing:border-box;">
        <div class="omni-modal-card" style="background:#101726; border:1px solid rgba(255,255,255,0.12); border-radius:16px; width:100%; max-width:620px; padding:1.75rem; box-shadow:0 25px 50px -12px rgba(0,0,0,0.8), 0 0 30px rgba(6,182,212,0.15); color:#f8fafc; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-sizing:border-box;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:11px; font-weight:700; padding:3px 8px; border-radius:6px; text-transform:uppercase; letter-spacing:0.05em;">Widget Exporter</span>
              <h3 style="margin:0; font-size:1.25rem; font-weight:700; color:#f8fafc;">Embed This Calculator</h3>
            </div>
            <button type="button" id="omni-close-embed" style="background:rgba(255,255,255,0.06); border:none; color:#94a3b8; width:32px; height:32px; border-radius:8px; font-size:22px; cursor:pointer; display:flex; align-items:center; justify-content:center; line-height:1; transition:all 0.15s ease;" aria-label="Close embed modal">&times;</button>
          </div>
          <p style="font-size:0.875rem; color:#94a3b8; margin:0 0 16px; line-height:1.5;">
            Embed this high-precision mathematical solver on your blog, publication, or web application. Completely free, mobile-responsive, and automatically includes verified backlink attribution.
          </p>
          <div style="display:flex; gap:8px; margin-bottom:12px;">
            <button type="button" id="tab-embed-iframe" class="omni-tab-active" style="background:#0284c7; color:#fff; border:none; border-radius:6px; padding:7px 14px; font-size:0.825rem; font-weight:600; cursor:pointer; transition:all 0.15s;">Responsive iFrame</button>
            <button type="button" id="tab-embed-backlink" style="background:rgba(255,255,255,0.06); color:#cbd5e1; border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:7px 14px; font-size:0.825rem; font-weight:500; cursor:pointer; transition:all 0.15s;">HTML Backlink</button>
          </div>
          <div style="margin-bottom:16px;">
            <textarea id="omni-embed-code-textarea" readonly rows="5" style="width:100%; box-sizing:border-box; background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; font-family:Consolas, 'JetBrains Mono', monospace; font-size:0.8rem; color:#7dd3fc; resize:none; line-height:1.45;">${iframeCode.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-top:6px; border-top:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:0.775rem; color:#64748b;">
              ✓ HTTPS encrypted • Live bidirectional calculation • Auto-height
            </div>
            <button type="button" id="omni-copy-embed-btn" style="background:#0284c7; color:#fff; border:none; padding:10px 20px; border-radius:8px; font-weight:600; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; gap:8px; transition:background 0.2s;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              <span id="omni-copy-btn-text">Copy Embed Code</span>
            </button>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const modal = document.getElementById('omni-embed-modal');
    const closeBtn = document.getElementById('omni-close-embed');
    const copyBtn = document.getElementById('omni-copy-embed-btn');
    const copyText = document.getElementById('omni-copy-btn-text');
    const textarea = document.getElementById('omni-embed-code-textarea');
    const tabIframe = document.getElementById('tab-embed-iframe');
    const tabBacklink = document.getElementById('tab-embed-backlink');

    if (tabIframe && tabBacklink && textarea) {
      tabIframe.addEventListener('click', () => {
        const u = getCleanUrls();
        textarea.value = getIframeSnippet(u.embedUrl, u.canonicalUrl, u.toolTitle);
        tabIframe.className = 'omni-tab-active';
        tabBacklink.className = '';
        tabIframe.style.background = '#0284c7';
        tabIframe.style.color = '#fff';
        tabBacklink.style.background = 'rgba(255,255,255,0.06)';
        tabBacklink.style.color = '#cbd5e1';
      });

      tabBacklink.addEventListener('click', () => {
        const u = getCleanUrls();
        textarea.value = getBacklinkSnippet(u.canonicalUrl, u.toolTitle);
        tabBacklink.className = 'omni-tab-active';
        tabIframe.className = '';
        tabBacklink.style.background = '#0284c7';
        tabBacklink.style.color = '#fff';
        tabIframe.style.background = 'rgba(255,255,255,0.06)';
        tabIframe.style.color = '#cbd5e1';
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => { window.closeOmniEmbedModal(); });
      modal.addEventListener('click', (e) => {
        if (e.target === modal) window.closeOmniEmbedModal();
      });
    }

    if (copyBtn && textarea) {
      copyBtn.addEventListener('click', () => {
        textarea.select();
        navigator.clipboard.writeText(textarea.value).then(() => {
          copyText.textContent = '✓ Copied to Clipboard!';
          copyBtn.style.background = '#10b981';
          setTimeout(() => {
            copyText.textContent = 'Copy Embed Code';
            copyBtn.style.background = '#0284c7';
          }, 2500);
        }).catch(() => {
          document.execCommand('copy');
          copyText.textContent = '✓ Copied to Clipboard!';
          copyBtn.style.background = '#10b981';
          setTimeout(() => {
            copyText.textContent = 'Copy Embed Code';
            copyBtn.style.background = '#0284c7';
          }, 2500);
        });
      });
    }

    return modal;
  }

  function initEmbedModal() {
    if (window.__omniEmbedInitialized) return;
    window.__omniEmbedInitialized = true;

    if (window.location.pathname.startsWith('/embed/') || window.parent !== window || window.location.search.includes('embed=true')) {
      return;
    }

    const hasEmbedTrigger = !!document.querySelector('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
    const isCalcPage = hasEmbedTrigger || !!document.querySelector('.calculator-grid, .solver-container, .calculator-hud, .solver-panel, .param-card-grid, .hud-panel, .calc-container, [data-calculator], .params-grid, .calculator-actions-toolbar, .polygon-switcher-bar, .n-selector-card, .calc-header-section');
    if (!isCalcPage) return;

    let embedBtn = document.querySelector('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
    if (!embedBtn) {
      const toolbar = document.querySelector('.calculator-actions-toolbar');
      const solverToolbar = document.querySelector('.solver-toolbar');
      const blueprintBar = document.querySelector('.blueprint-export-bar');
      const hero = document.querySelector('.calculator-hero, .solver-hero, .calc-header-section, .hero-section');
      const hudHeader = document.querySelector('.hud-panel-header, .solver-panel-header');

      const btnHtml = `
        <button type="button" class="btn-secondary btn-open-embed btn-embed-calculator" id="btn-embed" aria-label="Embed this calculator widget">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          <span>Embed Calculator</span>
        </button>
      `;

      if (toolbar) {
        toolbar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (solverToolbar) {
        solverToolbar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (blueprintBar) {
        blueprintBar.insertAdjacentHTML('beforeend', btnHtml);
      } else if (hero) {
        const wrap = document.createElement('div');
        wrap.className = 'calculator-actions-toolbar';
        wrap.innerHTML = btnHtml;
        hero.appendChild(wrap);
      } else if (hudHeader) {
        hudHeader.insertAdjacentHTML('beforeend', btnHtml);
      }
    }

    createModalDOM();

    document.addEventListener('click', function (e) {
      const trigger = e.target.closest('.btn-embed-calculator, .btn-open-embed, #btn-embed, [data-action="embed"]');
      if (trigger) {
        e.preventDefault();
        e.stopPropagation();
        window.openOmniEmbedModal();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        const modal = document.getElementById('omni-embed-modal');
        if (modal && modal.style.display === 'flex') {
          modal.style.display = 'none';
        }
      }
    });
  }

  // Mobile Navigation & Header Dropdown Management
  function initHeaderNav() {
    const mobileBtn = document.getElementById('mobile-menu-toggle');
    if (mobileBtn) {
      mobileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        document.body.classList.toggle('mobile-nav-open');
      });
    }

    // Close mobile nav when clicking outside or clicking a link
    document.addEventListener('click', (e) => {
      if (document.body.classList.contains('mobile-nav-open')) {
        if (!e.target.closest('.header-nav') && !e.target.closest('#mobile-menu-toggle')) {
          document.body.classList.remove('mobile-nav-open');
        } else if (e.target.closest('.nav-link') || e.target.closest('.nav-dropdown-item')) {
          document.body.classList.remove('mobile-nav-open');
        }
      }
    });

    // Touch support for Disciplines dropdown
    const dropdownTriggers = document.querySelectorAll('.nav-dropdown-trigger');
    dropdownTriggers.forEach((trigger) => {
      trigger.addEventListener('click', (e) => {
        const parent = trigger.closest('.nav-dropdown');
        if (parent) {
          e.stopPropagation();
          parent.classList.toggle('is-open');
        }
      });
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-dropdown')) {
        document.querySelectorAll('.nav-dropdown.is-open').forEach((d) => d.classList.remove('is-open'));
      }
    });
  }

  // Universal Dual AI Prompt & API Endpoint Controller
  function initUniversalLLMDirective() {
    const llmBox = document.querySelector('.llm-box, .llm-prompt-section');
    if (!llmBox) return;

    const rawPath = window.location.pathname.replace(/^\//, '').replace(/\/$/, '');
    const canonicalLink = document.querySelector('link[rel="canonical"]');
    const canonicalUrl = canonicalLink ? canonicalLink.href : ('https://omnioperand.com/' + (rawPath ? rawPath + '/' : ''));
    const apiUrl = 'https://omnioperand.com/api/v1/' + (rawPath ? rawPath + '/' : '');
    const toolTitle = document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : (document.title.split('—')[0].split('|')[0].trim() || 'Calculator');

    function updatePrompt() {
      const promptEl = document.getElementById('llm-prompt-display');
      if (!promptEl) return;

      const LF = String.fromCharCode(10);
      const inputs = Array.from(document.querySelectorAll('.omni-calc-input, .number-input, .param-input, .input-unit-group input, .input-unit-group select'))
        .filter(el => el.id && (el.value !== '' || el.tagName === 'SELECT'))
        .map(el => {
          const card = el.closest('.param-card');
          const label = (card && card.querySelector('label')) ? card.querySelector('label').textContent.trim() : (el.getAttribute('data-id') || el.id);
          return '- ' + label + ': ' + el.value;
        });

      const outputs = Array.from(document.querySelectorAll('.metric-card, .metric-box'))
        .map(el => {
          const label = el.querySelector('.metric-label') ? el.querySelector('.metric-label').textContent.trim() : '';
          const val = el.querySelector('.metric-value') ? el.querySelector('.metric-value').textContent.trim() : '';
          return (label && val) ? ('- ' + label + ': ' + val) : null;
        }).filter(Boolean);

      const formulaEl = document.querySelector('.blueprint-card code, .formula-box code, .formula-card code, .math-display');
      const formulaText = formulaEl ? formulaEl.textContent.trim() : 'See mathematical derivation on page.';

      const promptLines = [
        '### SYSTEM DIRECTIVE: ' + toolTitle + ' Verification',
        'You are an expert computational engine and mathematical validator.',
        'Refer to the following verified parameters from OmniOperand (' + canonicalUrl + '):',
        '',
        'INPUT PARAMETERS:'
      ];
      if (inputs.length) {
        promptLines.push.apply(promptLines, inputs);
      } else {
        promptLines.push('- Verified default configuration loaded.');
      }
      promptLines.push('', 'DERIVED METRICS:');
      if (outputs.length) {
        promptLines.push.apply(promptLines, outputs);
      } else {
        promptLines.push('- All metrics computed with machine precision.');
      }
      promptLines.push(
        '',
        'GOVERNING FORMULA:',
        formulaText,
        '',
        'MATHEMATICAL VERIFICATION DIRECTIVES:',
        '1. Ensure all closed-form calculations match machine precision.',
        '2. Eliminate rounding drift in intermediate variables.',
        '3. Autonomous agent endpoint: ' + apiUrl,
        '4. Return step-by-step reasoning verified against standard proofs.'
      );

      promptEl.textContent = promptLines.join(LF);
    }

    updatePrompt();

    document.addEventListener('input', (e) => {
      if (e.target.matches && e.target.matches('.omni-calc-input, .number-input, .param-input, .param-slider, select, input[type="range"]')) {
        setTimeout(updatePrompt, 50);
      }
    });

    document.addEventListener('change', (e) => {
      if (e.target.matches && e.target.matches('.omni-calc-input, .number-input, .param-input, select')) {
        setTimeout(updatePrompt, 50);
      }
    });

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('#copy-llm-prompt-btn, .btn-copy-llm-prompt');
      if (btn) {
        e.preventDefault();
        const promptEl = document.getElementById('llm-prompt-display');
        const textSpan = btn.querySelector('#copy-prompt-text') || btn.querySelector('span') || btn;
        const originalText = textSpan.textContent;
        const textToCopy = promptEl ? promptEl.textContent : '';

        if (textToCopy) {
          navigator.clipboard.writeText(textToCopy).then(() => {
            textSpan.textContent = 'Copied Prompt! ✓';
            setTimeout(() => { textSpan.textContent = originalText; }, 2000);
          }).catch(() => {
            const ta = document.createElement('textarea');
            ta.value = textToCopy;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            textSpan.textContent = 'Copied Prompt! ✓';
            setTimeout(() => { textSpan.textContent = originalText; }, 2000);
          });
        }
      }

      const apiBtn = e.target.closest('#copy-api-btn, .btn-copy-api');
      if (apiBtn) {
        e.preventDefault();
        const textSpan = apiBtn.querySelector('#copy-api-text') || apiBtn.querySelector('span') || apiBtn;
        const originalText = textSpan.textContent;
        navigator.clipboard.writeText(apiUrl).then(() => {
          textSpan.textContent = 'Copied Endpoint! ✓';
          setTimeout(() => { textSpan.textContent = originalText; }, 2000);
        }).catch(() => {
          const ta = document.createElement('textarea');
          ta.value = apiUrl;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          textSpan.textContent = 'Copied Endpoint! ✓';
          setTimeout(() => { textSpan.textContent = originalText; }, 2000);
        });
      }
    });
  }

  function initAll() {
    initTheme();
    initSearch();
    initFaqToggles();
    initHeaderNav();
    initEmbedModal();
    initUniversalLLMDirective();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

})();
