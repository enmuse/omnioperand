/**
 * OmniOperand — Global Search & Navigation Controller (omni-search.js)
 * Instant fuzzy matching, keyboard navigation (Cmd+K / '/'), and Theme Toggle
 */

(function () {
  'use strict';

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

  // Global FAQ Accordion Toggle Delegation
  function initFaqToggles() {
    document.addEventListener('click', (e) => {
      const question = e.target.closest('.faq-question');
      if (question) {
        const item = question.closest('.faq-item');
        if (item) {
          item.classList.toggle('open');
        }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSearch();
    initFaqToggles();
  });

})();
