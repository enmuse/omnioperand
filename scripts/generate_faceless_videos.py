#!/usr/bin/env python3
"""
OmniOperand Faceless Video Production Engine
Generates high-retention 9:16 vertical short-form videos (1080x1920) for the top 10 most profitable calculators.
Uses macOS Samantha TTS voice, Pillow high-res frame rendering, and FFmpeg H.264/AAC encoding.
"""

import os
import sys
import json
import math
import shutil
import tempfile
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Output directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "videos", "faceless")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# System fonts
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = "/System/Library/Fonts/Helvetica.ttc"
    FONT_REGULAR_PATH = "/System/Library/Fonts/Helvetica.ttc"

# Video Configuration
WIDTH = 1080
HEIGHT = 1920
FPS = 30

VIDEOS_CONFIG = [
    {
        "id": "dscr-loan",
        "title": "DSCR Investor Loan: Qualify With $0 Tax Returns",
        "category": "NON-QM REAL ESTATE",
        "cpl": "$250 – $500 CPL",
        "target_url": "/calculators/dscr-loan/",
        "accent": (16, 185, 129),  # Emerald
        "accent_hex": "#10b981",
        "social_tags": ["#realestateinvesting", "#dscrloan", "#passiveincome", "#mortgagetips", "#realestatelife", "#wealthbuilding"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Stop giving banks two years of personal tax returns to buy rental properties.",
                "badge": "🔥 REAL ESTATE FINANCING HACK",
                "headline": "QUALIFY WITH\nZERO TAX RETURNS",
                "card_title": "NON-QM DEBT SERVICE UNDERWRITING",
                "lines": [
                    "• No Personal W-2 Paystubs",
                    "• No Tax Return Scrutiny",
                    "• Unlimited Portfolio Scaling"
                ],
                "metric_label": "MAX BORROWING CEILING",
                "metric_val": "$2,500,000",
                "status": "BORROWER DTI EXEMPT"
            },
            {
                "type": "problem",
                "narration": "Traditional mortgage lenders look at your personal DTI. If you write off expenses on your taxes, banks claim you make zero dollars.",
                "badge": "⚠️ THE CONVENTIONAL LENDER TRAP",
                "headline": "WHY WRITE-OFFS\nKILL YOUR LOAN",
                "card_title": "SCHEDULE C TAX PENALTY",
                "lines": [
                    "❌ Write-offs reduce taxable income",
                    "❌ Personal DTI capped at 43%",
                    "❌ Portfolio capped at 4-10 properties"
                ],
                "metric_label": "CONVENTIONAL BORROWING LIMIT",
                "metric_val": "CAPPED OUT",
                "status": "DENIED BY FANNIE MAE"
            },
            {
                "type": "formula",
                "narration": "Instead, smart investors use a DSCR loan. The formula is: Gross Monthly Rent divided by the monthly PITIA mortgage payment.",
                "badge": "📐 THE UNDERWRITING FORMULA",
                "headline": "HOW DSCR IS\nCALCULATED",
                "card_title": "DEBT SERVICE COVERAGE RATIO",
                "lines": [
                    "DSCR = Gross Rent ÷ Monthly PITIA",
                    "Gross Monthly Rent = $4,500",
                    "Monthly PITIA Payment = $3,600",
                    "➔ 4,500 ÷ 3,600 = 1.25"
                ],
                "metric_label": "CALCULATED DSCR",
                "metric_val": "1.25x",
                "status": "INSTANT APPROVAL (≥ 1.20)"
            },
            {
                "type": "results",
                "narration": "If a fourplex rents for 4,500 dollars and the mortgage is 3,600, your DSCR is 1.25. That is an instant approval, with closing in as little as 21 days.",
                "badge": "📊 BOTTOM LINE EXECUTION",
                "headline": "THE INVESTOR\nADVANTAGE",
                "card_title": "LOAN TERMS & APPROVAL",
                "lines": [
                    "✓ 80% LTV Purchase & Cash-Out",
                    "✓ 30-Year Fixed or Interest-Only",
                    "✓ Entity Title (LLC / Trust Allowed)"
                ],
                "metric_label": "QUALIFYING PERSONAL INCOME",
                "metric_val": "$0 REQUIRED",
                "status": "100% ASSET-BASED UNDERWRITING"
            },
            {
                "type": "cta",
                "narration": "Calculate your exact DSCR, monthly cash flow, and borrowing power for free at omnioperand.com.",
                "badge": "🚀 FREE INTERACTIVE CALCULATOR",
                "headline": "MODEL YOUR DEAL\nIN SECONDS",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Instant Bidirectional Solving",
                    "• LTV & Interest-Only Toggles",
                    "• Exact Amortization & Cash Flow"
                ],
                "metric_label": "ACCESS ENGINE",
                "metric_val": "omnioperand.com",
                "status": "FREE • NO SIGNUP REQUIRED"
            }
        ]
    },
    {
        "id": "cost-segregation",
        "title": "Cost Segregation: The $184,000 Real Estate Tax Shield",
        "category": "IRS TAX CODE §168(k)",
        "cpl": "$300 – $750 CPL",
        "target_url": "/calculators/cost-segregation/",
        "accent": (56, 189, 248),  # Sky Blue
        "accent_hex": "#38bdf8",
        "social_tags": ["#costsegregation", "#taxstrategy", "#realestatetax", "#depreciation", "#cpa", "#wealthpreservation"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Did you know you can legally wipe out over one hundred thousand dollars in income taxes in year one of buying real estate?",
                "badge": "💡 IRS WEALTH SECRET",
                "headline": "WIPE OUT $100K+\nIN INCOME TAXES",
                "card_title": "COST SEGREGATION ACCELERATION",
                "lines": [
                    "• Front-load 27.5-year depreciation",
                    "• Deduct carpets, lighting, HVAC",
                    "• 100% legal IRS tax code strategy"
                ],
                "metric_label": "YEAR 1 ACCELERATED DEDUCTION",
                "metric_val": "$184,000",
                "status": "IRS §168(k) APPROVED"
            },
            {
                "type": "problem",
                "narration": "Normally, the IRS forces you to depreciate commercial buildings over 39 years, or residential rentals over 27.5 years. That gives you tiny tax deductions.",
                "badge": "⏳ THE 39-YEAR TRICKLE",
                "headline": "WHY NORMAL\nDEPRECIATION SUCKS",
                "card_title": "STANDARD STRAIGHT-LINE MACRS",
                "lines": [
                    "❌ 27.5 Years: Residential Rentals",
                    "❌ 39 Years: Commercial Property",
                    "❌ Tiny 2.5% to 3.6% deduction/year"
                ],
                "metric_label": "STANDARD ANNUAL DEDUCTION",
                "metric_val": "ONLY 2.5%",
                "status": "LOSING VALUE TO INFLATION"
            },
            {
                "type": "formula",
                "narration": "With a Cost Segregation study, you carve out five-year and fifteen-year assets. Reclassifying 25% of an eight-hundred-thousand-dollar building yields a 184,000 dollar first-year write-off.",
                "badge": "📐 THE RECLASSIFICATION MATH",
                "headline": "HOW ASSETS ARE\nRECLASSIFIED",
                "card_title": "ASSET ALLOCATION ENGINE",
                "lines": [
                    "Building Basis (Ex-Land): $800,000",
                    "5-Year Personal Property: 15% ($120k)",
                    "15-Year Land Improvements: 10% ($80k)",
                    "Bonus Depreciation Shield: $184,000"
                ],
                "metric_label": "FIRST-YEAR WRITE-OFF",
                "metric_val": "$184,000",
                "status": "MACRS 5 & 15 YEAR RECLASS"
            },
            {
                "type": "results",
                "narration": "At a 37% tax bracket, that puts 68,000 dollars of pure cash back in your pocket right now. That is capital you can reinvest into your next deal.",
                "badge": "💰 PURE CASH RECOVERY",
                "headline": "NET CASH IN\nYOUR POCKET",
                "card_title": "TAX LIABILITY SHIELD",
                "lines": [
                    "✓ 37% Federal Bracket: $68,080 saved",
                    "✓ Real Estate Professional (REPS) Shield",
                    "✓ Offsets W-2 or active business income"
                ],
                "metric_label": "YEAR 1 HARD CASH SAVED",
                "metric_val": "+$68,080",
                "status": "CASH SAVED ON DAY ONE"
            },
            {
                "type": "cta",
                "narration": "Model your property's 5-year and 15-year tax shield on the OmniOperand Cost Segregation calculator.",
                "badge": "🚀 RUN YOUR PROPERTY",
                "headline": "CALCULATE YOUR\nTAX SHIELD",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Full Bonus Depreciation Schedule",
                    "• Tax Bracket Impact Analysis",
                    "• Engineering Study ROI Estimator"
                ],
                "metric_label": "CALCULATE FREE",
                "metric_val": "omnioperand.com",
                "status": "INSTANT ACCELERATION MODEL"
            }
        ]
    },
    {
        "id": "1031-exchange",
        "title": "Section 1031 Exchange: Sell Real Estate & Pay $0 Capital Gains",
        "category": "IRS CODE §1031",
        "cpl": "$300 – $800 CPL",
        "target_url": "/calculators/1031-exchange/",
        "accent": (245, 158, 11),  # Amber
        "accent_hex": "#f59e0b",
        "social_tags": ["#1031exchange", "#capitalgains", "#realestatesales", "#taxdeferral", "#multifamily", "#commercialre"],
        "scenes": [
            {
                "type": "hook",
                "narration": "If you sell an investment property, the IRS could take up to 40% of your profits in capital gains and depreciation recapture.",
                "badge": "⚠️ TAX CRUNCH ALERT",
                "headline": "DON'T LOSE 40%\nTO CAPITAL GAINS",
                "card_title": "LIKE-KIND TAX DEFERRAL",
                "lines": [
                    "• 20% Federal Long-Term Capital Gains",
                    "• 25% Section 1250 Depreciation Recapture",
                    "• 3.8% Net Investment Income Tax (NIIT)"
                ],
                "metric_label": "POTENTIAL TAX EROSION",
                "metric_val": "UP TO 40%",
                "status": "EROSION OF COMPOUND WEALTH"
            },
            {
                "type": "problem",
                "narration": "On a 500,000 dollar gain, federal capital gains, state taxes, and 25% depreciation recapture can eat 160,000 dollars of your hard-earned equity.",
                "badge": "💸 THE PROFIT DRAIN",
                "headline": "A $160,000 TAX\nSURPRISE",
                "card_title": "SALE TAX LIQUIDATION TRAP",
                "lines": [
                    "Relinquished Sale: $1,200,000",
                    "Realized Capital Gain: $500,000",
                    "Depreciation Recaptured: $120,000",
                    "Tax Bill Owed: -$160,000"
                ],
                "metric_label": "LOST INVESTMENT CAPITAL",
                "metric_val": "-$160,000",
                "status": "OUT-OF-POCKET CASH PAYMENT"
            },
            {
                "type": "formula",
                "narration": "Under IRS Section 1031, you can legally defer 100% of the tax by rolling your full net proceeds into a like-kind replacement property. You have 45 days to identify and 180 days to close.",
                "badge": "📜 THE LIKE-KIND MECHANISM",
                "headline": "DEFER 100% OF\nTHE TAX BILL",
                "card_title": "SECTION 1031 RULES",
                "lines": [
                    "45-Day Identification Window",
                    "180-Day Final Closing Deadline",
                    "Reinvest 100% of Net Cash Equity",
                    "Acquire Equal or Greater Debt"
                ],
                "metric_label": "CAPITAL GAINS DEFERRED",
                "metric_val": "100%",
                "status": "ZERO CURRENT TAX LIABILITY"
            },
            {
                "type": "results",
                "narration": "You keep 100% of your equity compounding into larger, cash-flowing commercial assets instead of handing it to the government.",
                "badge": "📈 COMPOUNDING POWER",
                "headline": "REINVEST THE\nFULL $160,000",
                "card_title": "WEALTH COMPOUNDING IMPACT",
                "lines": [
                    "✓ Buy $2,000,000+ Replacement Asset",
                    "✓ Boost Cash Flow & Tax Deductions",
                    "✓ Swap 'Til You Drop Step-Up in Basis"
                ],
                "metric_label": "LEVERAGED BUYING POWER",
                "metric_val": "+$640,000",
                "status": "4X LEVERAGE PRESERVED"
            },
            {
                "type": "cta",
                "narration": "Calculate your exact tax savings, boot exposure, and 45-day deadlines for free at omnioperand.com.",
                "badge": "🚀 1031 EXCHANGE SOLVER",
                "headline": "CALCULATE YOUR\nDEADLINES & BOOT",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Full Depreciation Recapture Breakdown",
                    "• Cash Boot & Mortgage Boot Calculator",
                    "• 45-Day & 180-Day Calendar Timelines"
                ],
                "metric_label": "RUN CALCULATIONS",
                "metric_val": "omnioperand.com",
                "status": "INSTANT 1031 ANALYSIS"
            }
        ]
    },
    {
        "id": "section-179-equipment",
        "title": "Section 179: Write Off Up to $1.22M in Equipment Today",
        "category": "IRS CODE §179",
        "cpl": "$300 – $600 CPL",
        "target_url": "/calculators/section-179-equipment/",
        "accent": (239, 68, 68),  # Red / Coral
        "accent_hex": "#ef4444",
        "social_tags": ["#section179", "#taxwriteoff", "#equipmentfinancing", "#smallbiztips", "#trucking", "#contractorlife"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Business owners: stop waiting seven years to write off your machinery, vehicles, and tech hardware.",
                "badge": "⚡ SMALL BIZ TAX SHIELD",
                "headline": "WRITE OFF $1,220,000\nIN YEAR ONE",
                "card_title": "FIRST-YEAR EQUIPMENT EXPENSING",
                "lines": [
                    "• Heavy Trucks & Construction Machinery",
                    "• Manufacturing & Medical Equipment",
                    "• Computers, Servers, Software & Tech"
                ],
                "metric_label": "MAX EXPENSING DEDUCTION",
                "metric_val": "$1,220,000",
                "status": "IRS SECTION 179 CAP"
            },
            {
                "type": "problem",
                "narration": "Traditional MACRS depreciation trickles tax deductions out over 5 to 7 years while you pay the full equipment invoice today.",
                "badge": "🛑 THE DEPRECIATION DRAG",
                "headline": "WHY TRADITIONAL\nWRITE-OFFS FAIL",
                "card_title": "STANDARD 7-YEAR SCHEDULE",
                "lines": [
                    "❌ 100% Cash Paid on Day One",
                    "❌ Deductions delayed over 7 years",
                    "❌ Inflation erodes tax shield value"
                ],
                "metric_label": "AVERAGE YEAR 1 WRITE-OFF",
                "metric_val": "ONLY 14.3%",
                "status": "CASH DRAIN FOR BUSINESS"
            },
            {
                "type": "formula",
                "narration": "Under Section 179, you can write off up to 1,220,000 dollars in qualified equipment in year one. Even better: if you finance the equipment with zero down, the tax shield puts immediate net cash in your pocket.",
                "badge": "📐 THE FINANCED CASH ARBITRAGE",
                "headline": "HOW EQUIPMENT\nPAYS YOU CASH",
                "card_title": "THE FINANCING CASH SHIELD",
                "lines": [
                    "Equipment Purchase: $100,000",
                    "Year 1 Financed Payments: $22,000",
                    "Tax Savings (35% Bracket): $35,000",
                    "➔ Net Cash in Pocket: +$13,000"
                ],
                "metric_label": "NET CASH IN POCKET",
                "metric_val": "+$13,000",
                "status": "POSITIVE CASH ON DAY ONE"
            },
            {
                "type": "results",
                "narration": "Buy 100,000 dollars of equipment, finance it, and save 35,000 dollars on your taxes. You literally make 13,000 dollars in net cash in year one.",
                "badge": "🏆 THE BOTTOM LINE",
                "headline": "TAX SAVINGS EXCEED\nYEAR 1 PAYMENTS",
                "card_title": "YEAR ONE ARBITRAGE SUMMARY",
                "lines": [
                    "✓ 100% Tax Write-Off in Year Placed in Service",
                    "✓ Zero Out-of-Pocket Down Payment",
                    "✓ Boost Productivity & Revenue Immediately"
                ],
                "metric_label": "TOTAL TAX SAVED",
                "metric_val": "$35,000",
                "status": "IMMEDIATE CASH ARBITRAGE"
            },
            {
                "type": "cta",
                "narration": "Calculate your net equipment cash-flow shield at omnioperand.com.",
                "badge": "🚀 FREE SECTION 179 SOLVER",
                "headline": "CALCULATE YOUR\nCASH SHIELD",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Full Section 179 & Bonus Depr Matrix",
                    "• Phase-Out Threshold Calculator ($3.05M)",
                    "• Financed vs Cash Purchase Comparison"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "INSTANT TAX CALCULATION"
            }
        ]
    },
    {
        "id": "sba-loan",
        "title": "SBA 7(a) & 504: Buy a Multi-Million Dollar Business With 10% Down",
        "category": "COMMERCIAL ACQUISITION",
        "cpl": "$250 – $500 CPL",
        "target_url": "/calculators/sba-loan/",
        "accent": (168, 85, 247),  # Purple
        "accent_hex": "#a855f7",
        "social_tags": ["#sbaloan", "#buyabusiness", "#acquisitionentrepreneurship", "#eta", "#mergersandacquisitions", "#smb"],
        "scenes": [
            {
                "type": "hook",
                "narration": "How do entrepreneurs buy multi-million dollar cash-flowing businesses with only 10% cash down?",
                "badge": "💼 BUSINESS ACQUISITION",
                "headline": "BUY A $2,000,000\nBIZ WITH 10% DOWN",
                "card_title": "GOVERNMENT-BACKED LEVERAGE",
                "lines": [
                    "• Up to $5,000,000 SBA 7(a) Loan Cap",
                    "• Only 10% Equity Injection Required",
                    "• Cash Flow Pays Off the Debt"
                ],
                "metric_label": "MAX SBA 7(a) LOAN CEILING",
                "metric_val": "$5,000,000",
                "status": "SBA 75% FEDERAL GUARANTY"
            },
            {
                "type": "problem",
                "narration": "Conventional commercial banks demand 25% to 35% down and strict real estate collateral before they lend on business acquisitions.",
                "badge": "🛑 CONVENTIONAL BANK ROADBLOCK",
                "headline": "THE 30% CASH DOWN\nBARRIER",
                "card_title": "CONVENTIONAL BANK CRITERIA",
                "lines": [
                    "❌ 25% to 35% Cash Down Required ($600k+)",
                    "❌ Strict 100% Real Estate Collateral",
                    "❌ 5-Year Short Amortization Balloon"
                ],
                "metric_label": "CONVENTIONAL CASH DOWN",
                "metric_val": "$600,000+",
                "status": "OUT OF REACH FOR MOST BUYERS"
            },
            {
                "type": "formula",
                "narration": "The SBA 7(a) program backs up to 75% of the loan. You put down 10%, seller financing can cover up to 10%, and the bank finances the rest. As long as company cash flows support a 1.25 DSCR, the business pays off its own debt.",
                "badge": "📐 THE CAPITAL STACK",
                "headline": "HOW THE DEAL IS\nSTRUCTURED",
                "card_title": "$2M ACQUISITION CAPITAL STACK",
                "lines": [
                    "Buyer Equity (10%): $200,000",
                    "Seller Note on Standby (10%): $200,000",
                    "SBA 7(a) Senior Loan (80%): $1,600,000",
                    "Annual EBITDA / SDE: $500,000"
                ],
                "metric_label": "DEBT SERVICE COVERAGE",
                "metric_val": "1.85x DSCR",
                "status": "WELL ABOVE 1.25x MINIMUM"
            },
            {
                "type": "results",
                "narration": "Control a 500,000 dollar a year cash-flowing enterprise with just 200,000 dollars in equity. That is an explosive return on capital.",
                "badge": "🏆 RETURN ON EQUITY",
                "headline": "EXPLOSIVE CASH\nON CASH RETURN",
                "card_title": "ACQUISITION CASH FLOW",
                "lines": [
                    "✓ SDE Cash Flow: $500,000 / year",
                    "✓ Debt Service: -$270,000 / year",
                    "✓ Net Post-Debt Cash: $230,000 / year"
                ],
                "metric_label": "YEAR 1 CASH-ON-CASH ROI",
                "metric_val": "115% ROI",
                "status": "FULL PAYBACK IN 10.4 MONTHS"
            },
            {
                "type": "cta",
                "narration": "Model SBA 7(a) payments, guaranty fees, and debt service coverage at omnioperand.com.",
                "badge": "🚀 SBA 7(a) & 504 SOLVER",
                "headline": "TEST YOUR DEAL\nCASH FLOWS",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Variable Prime + 2.75% Spread Models",
                    "• SBA Upfront Guaranty Fee Schedule",
                    "• Complete 10-Year Amortization Table"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "INSTANT ACQUISITION MODEL"
            }
        ]
    },
    {
        "id": "hard-money-loan",
        "title": "The 70% Fix-and-Flip Rule: How Private Lenders Fund Flips",
        "category": "PRIVATE LENDING & FLIPS",
        "cpl": "$250 – $500 CPL",
        "target_url": "/calculators/hard-money-loan/",
        "accent": (234, 179, 8),  # Yellow
        "accent_hex": "#eab308",
        "social_tags": ["#hardmoney", "#houseflipping", "#fixandflip", "#realestateinvestor", "#wholesaling", "#brrrr"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Never buy a house flip without running the hard money 70% rule first.",
                "badge": "🔨 FIX-AND-FLIP FORMULA",
                "headline": "THE 70% RULE\nFOR HOUSE FLIPS",
                "card_title": "MAXIMUM ALLOWABLE OFFER (MAO)",
                "lines": [
                    "• The formula private lenders enforce",
                    "• Protects against market price drops",
                    "• Guarantees healthy flip profit margins"
                ],
                "metric_label": "PRIVATE LENDER CEILING",
                "metric_val": "70% OF ARV",
                "status": "MAXIMUM ALLOWABLE OFFER"
            },
            {
                "type": "problem",
                "narration": "Most amateur flippers overpay for distressed houses because they forget to account for holding costs, points, and lender ARV caps.",
                "badge": "⚠️ THE AMATEUR FLIPPER TRAP",
                "headline": "WHY 80% OF FLIPPERS\nLOSE MONEY",
                "card_title": "HIDDEN HOLDING COST SHOCK",
                "lines": [
                    "❌ 2 to 3 Lender Origination Points",
                    "❌ 11% to 13% Interest-Only Carry",
                    "❌ 6% Realtor Sales Commissions"
                ],
                "metric_label": "AVERAGE UNPLANNED COSTS",
                "metric_val": "$35,000+",
                "status": "EATS ENTIRE PROFIT MARGIN"
            },
            {
                "type": "formula",
                "narration": "The Maximum Allowable Offer formula is: After Repair Value times 70%, minus Rehab Costs. On a 400,000 dollar ARV with 60,000 dollars in rehab, your maximum buy price is 220,000 dollars.",
                "badge": "📐 THE EXACT MAO MATH",
                "headline": "HOW TO CALCULATE\nYOUR MAXIMUM OFFER",
                "card_title": "THE 70% MAO CALCULATION",
                "lines": [
                    "ARV (After Repair Value): $400,000",
                    "70% ARV Benchmark: $280,000",
                    "Less Estimated Rehab: -$60,000",
                    "➔ Maximum Allowable Offer: $220,000"
                ],
                "metric_label": "MAX BUY PRICE",
                "metric_val": "$220,000",
                "status": "LENDER APPROVED ENTRY PRICE"
            },
            {
                "type": "results",
                "narration": "Lock in a guaranteed 45,000 dollar net profit while protecting yourself from market downturns. Private lenders will fund 90% of purchase and 100% of rehab.",
                "badge": "💰 PROFIT & LEVERAGE",
                "headline": "GUARANTEED FLIP\nPROFIT MARGIN",
                "card_title": "NET FLIP PROFIT SUMMARY",
                "lines": [
                    "✓ Resale Revenue: $400,000",
                    "✓ Purchase + Rehab + Carry: -$355,000",
                    "✓ Net Flip Profit: $45,000"
                ],
                "metric_label": "NET CASH PROFIT",
                "metric_val": "+$45,000",
                "status": "PROTECTED RISK-ADJUSTED RETURN"
            },
            {
                "type": "cta",
                "narration": "Run our bidirectional hard money calculator at omnioperand.com before putting an offer in.",
                "badge": "🚀 HARD MONEY SOLVER",
                "headline": "RUN YOUR FLIP\nNUMBERS NOW",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Dual LTC (90%) and LTARV (70%) Caps",
                    "• Monthly Carry Cost Breakdown",
                    "• Return on Capital & Equity Multiplier"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "FREE • NO SIGNUP REQUIRED"
            }
        ]
    },
    {
        "id": "bank-statement-mortgage",
        "title": "Bank Statement Mortgage: Buy a Home Without Tax Returns",
        "category": "SELF-EMPLOYED HOME LOANS",
        "cpl": "$250 – $450 CPL",
        "target_url": "/calculators/bank-statement-mortgage/",
        "accent": (20, 184, 166),  # Teal
        "accent_hex": "#14b8a6",
        "social_tags": ["#bankstatementloan", "#selfemployed", "#mortgagebroker", "#homebuying", "#businessowner", "#nonqm"],
        "scenes": [
            {
                "type": "hook",
                "narration": "If you're a business owner or 1099 freelancer, your tax write-offs are probably disqualifying you from buying a house.",
                "badge": "🏠 1099 & OWNER HACK",
                "headline": "BUY A HOME WITH\nZERO TAX RETURNS",
                "card_title": "BANK STATEMENT UNDERWRITING",
                "lines": [
                    "• 12 to 24 Months Business Bank Deposits",
                    "• Zero W-2 Forms or Tax Returns Required",
                    "• Qualify Based on Actual Cash Flow"
                ],
                "metric_label": "MAX HOME PURCHASE PRICE",
                "metric_val": "$3,000,000+",
                "status": "NON-QM SELF-EMPLOYED LOAN"
            },
            {
                "type": "problem",
                "narration": "Traditional mortgage underwriters look at line 31 of your Schedule C. If you write off expenses to lower taxes, your qualifying income shows as zero.",
                "badge": "🛑 THE UNDERWRITING TRAP",
                "headline": "LINE 31 KILLS\nYOUR MORTGAGE",
                "card_title": "CONVENTIONAL TAX AUDIT",
                "lines": [
                    "❌ Gross Revenue: $500,000 / year",
                    "❌ Tax Write-Offs: -$460,000 / year",
                    "❌ Net Qualifying Income: $40,000 / year"
                ],
                "metric_label": "QUALIFYING HOME LOAN",
                "metric_val": "DENIED",
                "status": "UNDERWRITTEN AS 'POOR'"
            },
            {
                "type": "formula",
                "narration": "With a 12-Month Bank Statement mortgage, lenders calculate qualifying income directly from your business deposits. They total 12 months of gross deposits, apply an industry expense ratio like 50%, and divide by 12.",
                "badge": "📐 THE DEPOSIT FORMULA",
                "headline": "HOW DEPOSITS BECOME\nQUALIFYING INCOME",
                "card_title": "DEPOSIT UNDERWRITING MATRIX",
                "lines": [
                    "Total 12-Month Deposits: $480,000",
                    "Underwriting Expense Ratio: 50%",
                    "Eligible Net Cash Flow: $240,000",
                    "➔ Monthly Qualifying Income: $20,000/mo"
                ],
                "metric_label": "MONTHLY QUALIFYING INCOME",
                "metric_val": "$20,000/MO",
                "status": "APPROVED AT 50% DTI"
            },
            {
                "type": "results",
                "narration": "A business owner depositing 40,000 dollars a month qualifies for a 1,200,000 dollar mortgage, even with zero net tax return income.",
                "badge": "🏆 PURCHASING POWER",
                "headline": "APPROVE A $1.2M\nMORTGAGE TODAY",
                "card_title": "APPROVED HOME PURCHASE",
                "lines": [
                    "✓ Maximum Purchase Power: $1,250,000",
                    "✓ Down Payment: 10% to 20%",
                    "✓ Primary, Second Home, or Investment"
                ],
                "metric_label": "MAX MORTGAGE APPROVED",
                "metric_val": "$1,250,000",
                "status": "ZERO TAX RETURNS NEEDED"
            },
            {
                "type": "cta",
                "narration": "Calculate your exact bank statement qualifying income on OmniOperand.",
                "badge": "🚀 BANK STATEMENT SOLVER",
                "headline": "CALCULATE YOUR\nBORROWING POWER",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• 12 vs 24 Month Deposit Schedules",
                    "• Industry Expense Ratio Sliders (30%-60%)",
                    "• Backsolve Required Monthly Deposits"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "FREE • NO SIGNUP REQUIRED"
            }
        ]
    },
    {
        "id": "commercial-solar-tax-credit",
        "title": "Commercial Solar Tax Credit: 30% ITC + 5-Year Depreciation Shield",
        "category": "CLEAN ENERGY TAX CREDITS",
        "cpl": "$350 – $700 CPL",
        "target_url": "/calculators/commercial-solar-tax-credit/",
        "accent": (249, 115, 22),  # Orange
        "accent_hex": "#f97316",
        "social_tags": ["#solartaxcredit", "#commercialsolar", "#taxequity", "#cleanenergy", "#sustainability", "#commercialre"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Commercial building owners: solar is no longer just green energy, it is an IRS tax shield engine.",
                "badge": "⚡ TAX SHIELD ENGINE",
                "headline": "WIPE OUT 52% OF\nSOLAR COST DAY 1",
                "card_title": "SECTION 48 ENERGY TAX CREDIT",
                "lines": [
                    "• 30% Federal Investment Tax Credit (ITC)",
                    "• 5-Year MACRS Accelerated Depreciation",
                    "• 60% First-Year Bonus Depreciation"
                ],
                "metric_label": "FIRST-YEAR INCENTIVE VALUE",
                "metric_val": "52.4% OF COST",
                "status": "IRS §48 & §168(k) SHIELD"
            },
            {
                "type": "problem",
                "narration": "High commercial utility bills and corporate taxes eat directly into net operating income and building valuation.",
                "badge": "📉 THE EXPENSE DRAIN",
                "headline": "ELECTRICITY BILLS\nDRAIN VALUE",
                "card_title": "COMMERCIAL OPERATING DRAG",
                "lines": [
                    "❌ $3,500/Month Utility Power Bills",
                    "❌ Utility rates rising 6% to 9% annually",
                    "❌ Lowers Net Operating Income (NOI)"
                ],
                "metric_label": "25-YEAR UTILITY BLEED",
                "metric_val": "$1,450,000",
                "status": "PERMANENT CASH BLEED"
            },
            {
                "type": "formula",
                "narration": "Under Section 48, commercial solar earns an immediate 30% federal tax credit. Furthermore, you depreciate 85% of the system value across 5-year MACRS with 60% bonus depreciation in Year 1.",
                "badge": "📐 THE TAX REDUCTION FORMULA",
                "headline": "THE 30% ITC +\nMACRS STACK",
                "card_title": "$250,000 SYSTEM INCENTIVE STACK",
                "lines": [
                    "System Gross Cost: $250,000",
                    "30% Federal ITC Credit: -$75,000",
                    "Depreciable Basis (85%): $212,500",
                    "Year 1 Depr Tax Savings: -$56,000"
                ],
                "metric_label": "YEAR 1 TOTAL TAX BENEFIT",
                "metric_val": "$131,000",
                "status": "52.4% RECOVERED IN MONTH 12"
            },
            {
                "type": "results",
                "narration": "On a 250,000 dollar system, tax incentives pay for over 52% of the project in year one, yielding a rapid 3.8-year payback.",
                "badge": "🏆 RAPID PAYBACK ROI",
                "headline": "3.8-YEAR FULL\nPAYBACK PERIOD",
                "card_title": "CASH FLOW SUMMARY",
                "lines": [
                    "✓ Net Out-of-Pocket Cost: $119,000",
                    "✓ Annual Power Savings: $31,500 / year",
                    "✓ 25-Year Net ROI: 412%"
                ],
                "metric_label": "PAYBACK TIMELINE",
                "metric_val": "3.8 YEARS",
                "status": "21.2 YEARS OF FREE POWER"
            },
            {
                "type": "cta",
                "narration": "Model your commercial solar tax credit and payback timeline at omnioperand.com.",
                "badge": "🚀 COMMERCIAL SOLAR SOLVER",
                "headline": "CALCULATE YOUR\nTAX INCENTIVES",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• 30% ITC Base + Domestic Content Adders",
                    "• 5-Year MACRS Amortization Schedule",
                    "• Internal Rate of Return (IRR) & LCOE"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "INSTANT SOLAR TAX MODEL"
            }
        ]
    },
    {
        "id": "structured-settlement-lump-sum",
        "title": "Structured Settlement Lump Sum: Don't Let Factoring Firms Rob You",
        "category": "ANNUITY & SETTLEMENT FACTORING",
        "cpl": "$500 – $1,500 CPL",
        "target_url": "/calculators/structured-settlement-lump-sum/",
        "accent": (236, 72, 153),  # Pink
        "accent_hex": "#ec4899",
        "social_tags": ["#structuredsettlement", "#annuity", "#lumpsum", "#legalfinance", "#personalinjury", "#settlement"],
        "scenes": [
            {
                "type": "hook",
                "narration": "If you have a structured settlement or legal annuity, factoring companies are trying to take 60% of your money.",
                "badge": "⚖️ DON'T GET ROBBED",
                "headline": "FACTORING FIRMS\nSTEAL 60% OF CASH",
                "card_title": "IRC §5891 ANNUITY VALUATION",
                "lines": [
                    "• Predatory Late-Night TV Commercials",
                    "• Sky-High 14% to 22% Discount Rates",
                    "• Court Approval Required by Law"
                ],
                "metric_label": "PREDATORY DISCOUNT RATE",
                "metric_val": "18.0% APR",
                "status": "ROBBING SETTLEMENT HOLDERS"
            },
            {
                "type": "problem",
                "narration": "Commercial TV commercials offer fast cash for settlements, but they slip in predatory discount rates between 14% and 22%.",
                "badge": "🛑 THE TV COMMERCIAL SCAM",
                "headline": "THE 18% DISCOUNT\nRATE TRAP",
                "card_title": "ANATOMY OF A BAD DEAL",
                "lines": [
                    "❌ Future Payments Owed: $250,000",
                    "❌ Predatory Discount Rate: 18.0%",
                    "❌ Factoring Cash Offer: $98,000"
                ],
                "metric_label": "TOTAL DISCOUNT LOST",
                "metric_val": "-$152,000",
                "status": "60.8% EQUITY FORFEITED"
            },
            {
                "type": "formula",
                "narration": "Under IRC Section 5891, your payout must be discounted to net present value. 250,000 dollars paid over 10 years at a fair 9% rate is worth 157,000 dollars. At an 18% rate, they only give you 98,000 dollars. That is a 59,000 dollar rip-off.",
                "badge": "📐 THE ACTUARIAL DISCOUNT MATH",
                "headline": "FAIR VALUE VS\nPREDATORY OFFERS",
                "card_title": "$250K OVER 10 YEARS COMPARISON",
                "lines": [
                    "Actuarial Fair Value (9% Rate): $157,000",
                    "Predatory Offer (18% Rate): $98,000",
                    "➔ Hidden Broker Fee Spread: $59,000"
                ],
                "metric_label": "PREDATORY BROKER PROFIT",
                "metric_val": "$59,000",
                "status": "MONEY TAKEN FROM YOUR POCKET"
            },
            {
                "type": "results",
                "narration": "Know your actuarial fair market value before talking to factoring brokers so you can negotiate a competitive discount rate under 9%.",
                "badge": "🛡️ PROTECT YOUR PAYOUT",
                "headline": "NEGOTIATE A FAIR\n9% TO 10% RATE",
                "card_title": "LEGAL PROTECTIONS & STANDARDS",
                "lines": [
                    "✓ Judicial 'Best Interest' Hearing Rule",
                    "✓ Demand Competitive Factoring Bids",
                    "✓ Save $59,000+ in Lump Sum Payout"
                ],
                "metric_label": "PROTECTED CASH PROCEEDS",
                "metric_val": "+$59,000",
                "status": "NEVER ACCEPT FIRST OFFER"
            },
            {
                "type": "cta",
                "narration": "Calculate your true lump-sum present value for free on OmniOperand.",
                "badge": "🚀 LUMP SUM SOLVER",
                "headline": "CHECK YOUR FAIR\nMARKET VALUE",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Discount Rate Sensitivity Slider (6%-22%)",
                    "• IRC §5891 Compliance Audit",
                    "• Full Monthly Discount Amortization"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "FREE • INDEPENDENT VALUATION"
            }
        ]
    },
    {
        "id": "commercial-real-estate-cap-rate",
        "title": "Cap Rate & Debt Yield: How Commercial Banks Value Buildings",
        "category": "COMMERCIAL SYNDICATION",
        "cpl": "$300 – $600 CPL",
        "target_url": "/calculators/commercial-real-estate-cap-rate/",
        "accent": (99, 102, 241),  # Indigo
        "accent_hex": "#6366f1",
        "social_tags": ["#caprate", "#debtyield", "#commercialrealestate", "#apartmentbuilding", "#syndication", "#cre"],
        "scenes": [
            {
                "type": "hook",
                "narration": "Want to know how commercial banks and syndicators price 10-million-dollar apartment buildings?",
                "badge": "🏢 INSTITUTIONAL CRE",
                "headline": "HOW BANKS PRICE\n$10M APARTMENTS",
                "card_title": "UNDERWRITING TWIN ENGINES",
                "lines": [
                    "• Cap Rate Determines Valuation",
                    "• Debt Yield Sizes the Maximum Loan",
                    "• DSCR Ensures Solvency"
                ],
                "metric_label": "INSTITUTIONAL BENCHMARK",
                "metric_val": "10.0% DEBT YIELD",
                "status": "COMMERCIAL UNDERWRITING STANDARD"
            },
            {
                "type": "problem",
                "narration": "Beginners only look at Cap Rate. But institutional lenders don't care about cap rate; they size loans using Debt Yield and DSCR.",
                "badge": "⚠️ THE AMATEUR CRE MISTAKE",
                "headline": "CAP RATE DOES NOT\nGUARANTEE A LOAN",
                "card_title": "THE REFINANCE SHORTFALL",
                "lines": [
                    "❌ Low 5% Cap Rate inflates price",
                    "❌ Bank requires 10% minimum Debt Yield",
                    "❌ Loan slashed by $800,000 at closing"
                ],
                "metric_label": "FINANCING SHORTFALL",
                "metric_val": "-$800,000",
                "status": "FORCED CASH RECTIFICATION"
            },
            {
                "type": "formula",
                "narration": "Cap Rate equals Net Operating Income divided by Purchase Price. But lenders require a minimum 9.5% to 10% Debt Yield, calculated as NOI divided by Loan Amount. Even if your Cap Rate is 6%, a low debt yield will slash your loan proceeds by hundreds of thousands of dollars.",
                "badge": "📐 THE DUAL FORMULAS",
                "headline": "CAP RATE VS\nDEBT YIELD MATH",
                "card_title": "CRITICAL UNDERWRITING RATIOS",
                "lines": [
                    "Cap Rate = NOI ÷ Property Price",
                    "Debt Yield = NOI ÷ Loan Amount",
                    "NOI: $500,000 | Price: $8,000,000 (6.25% Cap)",
                    "Max Loan at 10% Debt Yield: $5,000,000"
                ],
                "metric_label": "MAX SENIOR DEBT SIZED",
                "metric_val": "$5,000,000",
                "status": "DEBT YIELD SIZING APPLIED"
            },
            {
                "type": "results",
                "narration": "Accurately forecast loan proceeds, cash-on-cash yield, and valuation before signing a purchase agreement.",
                "badge": "🏆 DEAL CERTAINTY",
                "headline": "ELIMINATE CLOSING\nSURPRISES",
                "card_title": "UNDERWRITING ASSURANCE",
                "lines": [
                    "✓ Exact Maximum Loan Proceeds Known",
                    "✓ True Cash-on-Cash Return Modeled",
                    "✓ Secure Financing with Zero Capital Gaps"
                ],
                "metric_label": "PREDICTABLE CLOSING",
                "metric_val": "100% CERTAINTY",
                "status": "BANK-READY UNDERWRITING"
            },
            {
                "type": "cta",
                "narration": "Run institutional CRE underwriting calculations for free at omnioperand.com.",
                "badge": "🚀 CRE CAP RATE SOLVER",
                "headline": "MODEL YOUR CRE\nDEAL PROCEEDS",
                "card_title": "OMNIOPERAND SOLVER SUITE",
                "lines": [
                    "• Bidirectional Cap Rate & NOI Inversion",
                    "• Debt Yield & DSCR Sensitivity Matrix",
                    "• Levered Cash-on-Cash Return Schedule"
                ],
                "metric_label": "RUN CALCULATOR",
                "metric_val": "omnioperand.com",
                "status": "INSTANT CRE VALUATION"
            }
        ]
    }
]

def synthesize_audio(text, output_path):
    """Synthesizes text using macOS say with Samantha voice."""
    temp_aiff = output_path + ".aiff"
    subprocess.run(["/usr/bin/say", "-v", "Samantha", "-r", "172", text, "-o", temp_aiff], check=True)
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_aiff, "-c:a", "aac", "-b:a", "192k", output_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(temp_aiff):
        os.remove(temp_aiff)

def get_audio_duration(file_path):
    """Returns audio duration in seconds."""
    cmd = [
        "/opt/homebrew/bin/ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_background(accent_color):
    """Creates a sleek blueprint gradient background with subtle grid lines."""
    bg = Image.new("RGB", (WIDTH, HEIGHT), (7, 10, 19))
    draw = ImageDraw.Draw(bg)

    # Subtle grid lines
    grid_spacing = 60
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=(16, 26, 46), width=1)
    for y in range(0, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=(16, 26, 46), width=1)

    # Accent radial glow at center
    glow_center = (WIDTH // 2, HEIGHT // 2 - 100)
    glow_radius = 450
    glow_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)

    r_col, g_col, b_col = accent_color
    for r in range(glow_radius, 0, -15):
        alpha = int(24 * (1 - r / glow_radius))
        glow_draw.ellipse(
            [(glow_center[0] - r, glow_center[1] - r), (glow_center[0] + r, glow_center[1] + r)],
            fill=(r_col, g_col, b_col, alpha)
        )
    bg.paste(glow_overlay, (0, 0), glow_overlay)
    return bg

def render_scene_frame(base_bg, video_conf, scene_idx, scene_progress, total_progress, fonts):
    """Renders a single frame for the video."""
    frame = base_bg.copy()
    draw = ImageDraw.Draw(frame)
    scene = video_conf["scenes"][scene_idx]
    accent = video_conf["accent"]
    r, g, b = accent

    # 1. Top Global Progress Bar (0 to 1080)
    bar_width = int(total_progress * WIDTH)
    draw.rectangle([(0, 0), (WIDTH, 12)], fill=(20, 28, 48))
    if bar_width > 0:
        draw.rectangle([(0, 0), (bar_width, 12)], fill=accent)

    # 2. Top Header Brand Bar
    # Header pill
    pill_box = [(60, 60), (460, 120)]
    draw.rounded_rectangle(pill_box, radius=18, fill=(13, 20, 36), outline=(30, 48, 80), width=2)
    # Emerald live dot
    draw.ellipse([(85, 82), (101, 98)], fill=(16, 185, 129))
    draw.text((115, 75), "OMNIOPERAND", font=fonts["brand"], fill=(255, 255, 255))

    # Category Pill
    cat_text = video_conf["category"]
    cat_bbox = draw.textbbox((0, 0), cat_text, font=fonts["badge"])
    cat_w = cat_bbox[2] - cat_bbox[0] + 40
    cat_box = [(WIDTH - 60 - cat_w, 60), (WIDTH - 60, 120)]
    draw.rounded_rectangle(cat_box, radius=18, fill=(13, 20, 36), outline=accent, width=2)
    draw.text((WIDTH - 60 - cat_w + 20, 78), cat_text, font=fonts["badge"], fill=accent)

    # 3. Scene Badge Pill
    badge_text = scene["badge"]
    badge_bbox = draw.textbbox((0, 0), badge_text, font=fonts["badge"])
    badge_w = badge_bbox[2] - badge_bbox[0] + 48
    badge_x = (WIDTH - badge_w) // 2
    badge_box = [(badge_x, 190), (badge_x + badge_w, 254)]
    draw.rounded_rectangle(badge_box, radius=20, fill=(20, 30, 52), outline=(45, 65, 100), width=2)
    draw.text((badge_x + 24, 208), badge_text, font=fonts["badge"], fill=(240, 246, 255))

    # 4. Big Scene Headline (Centered)
    headline_lines = scene["headline"].split("\n")
    headline_y = 290
    for hl in headline_lines:
        hl_bbox = draw.textbbox((0, 0), hl, font=fonts["headline"])
        hl_w = hl_bbox[2] - hl_bbox[0]
        draw.text(((WIDTH - hl_w) // 2, headline_y), hl, font=fonts["headline"], fill=(255, 255, 255))
        headline_y += 76

    # 5. Main Glassmorphism Central Card
    card_top = 480
    card_bottom = 1420
    card_box = [(60, card_top), (WIDTH - 60, card_bottom)]
    
    # Shadow and border
    draw.rounded_rectangle(card_box, radius=32, fill=(12, 18, 34), outline=(38, 56, 92), width=3)
    
    # Card Header
    card_header_box = [(60, card_top), (WIDTH - 60, card_top + 80)]
    draw.rounded_rectangle(card_header_box, radius=32, fill=(18, 28, 52), outline=(38, 56, 92), width=2)
    draw.rectangle([(60, card_top + 40), (WIDTH - 60, card_top + 80)], fill=(18, 28, 52))
    
    # Card title & icon
    draw.ellipse([(95, card_top + 28), (119, card_top + 52)], fill=accent)
    draw.text((135, card_top + 24), scene["card_title"], font=fonts["subhead"], fill=(255, 255, 255))

    # Card Content: Bullet Lines / Formulas
    content_y = card_top + 120
    for line in scene["lines"]:
        line_color = (255, 255, 255)
        if "❌" in line:
            line_color = (248, 113, 113)  # Red
        elif "✓" in line or "•" in line:
            line_color = (226, 232, 240)
        elif "➔" in line or "=" in line:
            line_color = accent
        
        # Draw background highlight for formula / key lines
        if "➔" in line or "=" in line:
            highlight_box = [(85, content_y - 10), (WIDTH - 85, content_y + 56)]
            draw.rounded_rectangle(highlight_box, radius=16, fill=(20, 32, 58), outline=accent, width=1)
            draw.text((110, content_y + 2), line, font=fonts["formula"], fill=accent)
            content_y += 84
        else:
            draw.text((100, content_y), line, font=fonts["body"], fill=line_color)
            content_y += 66

    # 6. Hero Metric Box inside Card (Bottom Portion of Card)
    metric_box = [(100, card_bottom - 280), (WIDTH - 100, card_bottom - 60)]
    draw.rounded_rectangle(metric_box, radius=24, fill=(18, 28, 52), outline=accent, width=2)
    
    # Metric label
    m_lbl = scene["metric_label"]
    m_bbox = draw.textbbox((0, 0), m_lbl, font=fonts["metric_label"])
    m_w = m_bbox[2] - m_bbox[0]
    draw.text(((WIDTH - m_w) // 2, card_bottom - 260), m_lbl, font=fonts["metric_label"], fill=(148, 163, 184))

    # Metric Value (Big Neon)
    m_val = scene["metric_val"]
    m_vbox = draw.textbbox((0, 0), m_val, font=fonts["metric_val"])
    m_vw = m_vbox[2] - m_vbox[0]
    draw.text(((WIDTH - m_vw) // 2, card_bottom - 225), m_val, font=fonts["metric_val"], fill=accent)

    # Status pill under metric
    st_text = scene["status"]
    st_bbox = draw.textbbox((0, 0), st_text, font=fonts["status"])
    st_w = st_bbox[2] - st_bbox[0]
    draw.text(((WIDTH - st_w) // 2, card_bottom - 110), st_text, font=fonts["status"], fill=(255, 255, 255))

    # 7. Bottom Solver URL Footer
    footer_box = [(60, 1460), (WIDTH - 60, 1580)]
    draw.rounded_rectangle(footer_box, radius=24, fill=(13, 20, 36), outline=(40, 58, 92), width=2)
    draw.text((95, 1485), "FREE COMPUTATIONAL SOLVER", font=fonts["footer_sub"], fill=(148, 163, 184))
    url_text = "omnioperand.com" + video_conf["target_url"]
    draw.text((95, 1520), url_text, font=fonts["footer_url"], fill=(56, 189, 248))

    # 8. Interactive Teleprompter / Subtitle Bubble at very bottom
    sub_box = [(60, 1620), (WIDTH - 60, 1840)]
    draw.rounded_rectangle(sub_box, radius=24, fill=(8, 12, 22), outline=(30, 44, 70), width=2)
    
    # Subtitle header
    draw.text((95, 1640), "NARRATION TRANSCRIPT", font=fonts["trans_label"], fill=accent)
    
    # Wrap narration text into 2-3 lines
    words = scene["narration"].split()
    narration_lines = []
    curr_line = ""
    for w in words:
        test_line = (curr_line + " " + w).strip()
        test_bbox = draw.textbbox((0, 0), test_line, font=fonts["trans_text"])
        if test_bbox[2] - test_bbox[0] > (WIDTH - 200):
            narration_lines.append(curr_line)
            curr_line = w
        else:
            curr_line = test_line
    if curr_line:
        narration_lines.append(curr_line)
    
    trans_y = 1680
    for nl in narration_lines[:3]:
        draw.text((95, trans_y), nl, font=fonts["trans_text"], fill=(240, 246, 255))
        trans_y += 42

    return frame

def generate_video(video_conf):
    """Full pipeline for one faceless video."""
    vid_id = video_conf["id"]
    print(f"\n==========================================")
    print(f"🎬 Generating Faceless Video: {vid_id}")
    print(f"==========================================")
    
    temp_dir = tempfile.mkdtemp(prefix=f"vid_{vid_id}_")
    
    try:
        # Load fonts
        fonts = {
            "brand": ImageFont.truetype(FONT_BOLD_PATH, 28),
            "badge": ImageFont.truetype(FONT_BOLD_PATH, 26),
            "headline": ImageFont.truetype(FONT_BOLD_PATH, 62),
            "subhead": ImageFont.truetype(FONT_BOLD_PATH, 30),
            "body": ImageFont.truetype(FONT_REGULAR_PATH, 32),
            "formula": ImageFont.truetype(FONT_BOLD_PATH, 32),
            "metric_label": ImageFont.truetype(FONT_BOLD_PATH, 24),
            "metric_val": ImageFont.truetype(FONT_BOLD_PATH, 72),
            "status": ImageFont.truetype(FONT_BOLD_PATH, 24),
            "footer_sub": ImageFont.truetype(FONT_BOLD_PATH, 22),
            "footer_url": ImageFont.truetype(FONT_BOLD_PATH, 32),
            "trans_label": ImageFont.truetype(FONT_BOLD_PATH, 22),
            "trans_text": ImageFont.truetype(FONT_REGULAR_PATH, 28)
        }
        
        # 1. Synthesize audio for each scene
        scene_durations = []
        audio_files = []
        for i, scene in enumerate(video_conf["scenes"]):
            sec_audio = os.path.join(temp_dir, f"scene_{i}.m4a")
            synthesize_audio(scene["narration"], sec_audio)
            dur = get_audio_duration(sec_audio)
            scene_durations.append(dur)
            audio_files.append(sec_audio)
            print(f"  🔊 Scene {i+1} ({scene['type']}): {dur:.2f}s")
            
        total_duration = sum(scene_durations)
        print(f"  ⏱️  Total Narration Duration: {total_duration:.2f}s")
        
        # Concatenate audio files into full audio
        full_audio = os.path.join(temp_dir, "full_audio.m4a")
        inputs = []
        for af in audio_files:
            inputs.extend(["-i", af])
        filter_str = "".join(f"[{i}:a]" for i in range(len(audio_files))) + f"concat=n={len(audio_files)}:v=0:a=1[outa]"
        cmd = ["/opt/homebrew/bin/ffmpeg", "-y"] + inputs + ["-filter_complex", filter_str, "-map", "[outa]", "-c:a", "aac", full_audio]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # 2. Setup FFmpeg video encoding pipe
        output_mp4 = os.path.join(OUTPUT_DIR, f"{vid_id}.mp4")
        ffmpeg_cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{WIDTH}x{HEIGHT}",
            "-pix_fmt", "rgb24",
            "-r", str(FPS),
            "-i", "-",
            "-i", full_audio,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "copy",
            "-shortest",
            output_mp4
        ]
        
        pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Render base background
        base_bg = create_background(video_conf["accent"])
        
        # Calculate frame boundaries for each scene
        scene_frame_counts = [int(dur * FPS) for dur in scene_durations]
        total_frames = sum(scene_frame_counts)
        
        # Generate poster image (first frame of Scene 1)
        poster_path = os.path.join(OUTPUT_DIR, f"{vid_id}-poster.png")
        poster_frame = render_scene_frame(base_bg, video_conf, 0, 0.5, 0.1, fonts)
        poster_frame.save(poster_path)
        print(f"  🖼️  Saved Poster: {os.path.basename(poster_path)}")
        
        # 4. Stream frames through pipe
        current_frame = 0
        for s_idx, f_count in enumerate(scene_frame_counts):
            for f in range(f_count):
                scene_progress = f / max(1, f_count - 1)
                total_progress = current_frame / max(1, total_frames - 1)
                
                # Render frame
                frame_img = render_scene_frame(base_bg, video_conf, s_idx, scene_progress, total_progress, fonts)
                pipe.stdin.write(frame_img.tobytes())
                current_frame += 1
                
        pipe.stdin.close()
        pipe.wait()
        
        if pipe.returncode != 0:
            raise RuntimeError(f"FFmpeg encoding failed with code {pipe.returncode}")
            
        file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
        print(f"  ✅ Video Complete: {os.path.basename(output_mp4)} ({file_size_mb:.2f} MB, {total_duration:.1f}s)")
        
        return {
            "id": vid_id,
            "title": video_conf["title"],
            "category": video_conf["category"],
            "cpl": video_conf["cpl"],
            "target_url": video_conf["target_url"],
            "duration": round(total_duration, 1),
            "video_path": f"/assets/videos/faceless/{vid_id}.mp4",
            "poster_path": f"/assets/videos/faceless/{vid_id}-poster.png",
            "accent_hex": video_conf["accent_hex"],
            "social_tags": video_conf["social_tags"],
            "full_script": " ".join(s["narration"] for s in video_conf["scenes"]),
            "scenes": video_conf["scenes"]
        }
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    print("=========================================================")
    print("🚀 OmniOperand Faceless Video Production Suite (10 Top Calculators)")
    print("=========================================================")
    
    results = []
    for vid_conf in VIDEOS_CONFIG:
        res = generate_video(vid_conf)
        results.append(res)
        
    # Write metadata JSON
    meta_path = os.path.join(OUTPUT_DIR, "videos.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n🎉 All 10 Faceless Videos Generated Successfully!")
    print(f"📄 Metadata written to: {meta_path}")

if __name__ == "__main__":
    main()

