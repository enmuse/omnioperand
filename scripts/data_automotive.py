"""
scripts/data_automotive.py
25 High-Value Automotive, Fleet, Transport, Marine & Mechanical Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

AUTOMOTIVE_CALCULATORS = [
    {
        "slug": "lease-vs-buy",
        "category": "finance",
        "name": "Car Lease vs Buy Financial Comparison Calculator",
        "description": "Compare the total multi-year financial cost of leasing versus purchasing a new vehicle, accounting for depreciation, money factor, and equity at lease end.",
        "hero_badge": "Automotive Finance • Lease vs Purchase Matrix",
        "formula_display": "Total Lease Cost = Down Payment + (Monthly Lease × Term) + Disposition Fee | Total Loan Cost = Down Payment + (Monthly Loan × Term) - Resale Equity",
        "fields": [
            {"id": "vehicle_price", "label": "Vehicle Negotiated Price (MSRP / Cap Cost)", "default": 42000, "prefix": "$", "min": 5000, "max": 250000, "step": 1000, "hint": "Agreed selling price before fees"},
            {"id": "down_payment", "label": "Cash Down Payment", "default": 4000, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Upfront capital applied"},
            {"id": "lease_term_months", "label": "Lease Term (Months)", "default": 36, "suffix": "months", "min": 24, "max": 48, "step": 12, "hint": "Standard lease duration"},
            {"id": "lease_monthly", "label": "Quoted Monthly Lease Payment", "default": 480, "prefix": "$", "min": 100, "max": 5000, "step": 10, "hint": "Monthly lease bill including sales tax"},
            {"id": "loan_apr_pct", "label": "Purchase Loan APR (%)", "default": 6.5, "suffix": "%", "min": 0.0, "max": 25.0, "step": 0.1, "hint": "Financing interest rate"},
            {"id": "residual_value_pct", "label": "Estimated Resale Value after 3 Years", "default": 55, "suffix": "%", "min": 20, "max": 85, "step": 1, "hint": "Expected market resale value %"}
        ],
        "metrics": [
            {"id": "net_lease_cost", "label": "Net 3-Year Lease Outflow", "default_display": "$21,680.00", "highlight": True},
            {"id": "net_buy_cost", "label": "Net 3-Year Purchase Cost (After Equity)", "default_display": "$17,450.00", "highlight": True},
            {"id": "financial_winner", "label": "Cost-Effective Strategy", "default_display": "Purchasing Saves ~$4,230.00", "highlight": True},
            {"id": "equity_retained", "label": "Residual Vehicle Equity Retained", "default_display": "$23,100.00"}
        ],
        "proof_steps": [
            {"step_title": "Gross Capital Outflow Modeling", "step_text": "Leasing Outflow = Down Payment + (Monthly Lease × Term) + Disposition Fee ($400). Loan Outflow = Down Payment + (Monthly Payment × Term)."},
            {"step_title": "Residual Equity Valuation", "step_text": "At month 36, the lessee walks away with $0 equity. The purchaser retains an asset worth: Equity = Vehicle Price × (Resale Value% / 100)."},
            {"step_title": "Net Economic Depreciation Cost", "step_text": "Net Purchase Cost = Total Loan Cash Outflows - Residual Equity Asset Value. Buying almost always beats leasing unless the vehicle depreciates catastrophically faster than manufacturer residual estimates."}
        ],
        "faqs": [
            {"q": "Is it financially better to lease or buy a car?", "a": "From a pure wealth-building standpoint, buying and holding a vehicle for 6 to 10 years is vastly superior. Leasing provides lower monthly payments and warranty peace of mind, but costs significantly more over time because you pay the steepest part of the depreciation curve repeatedly."},
            {"q": "What is a car lease Money Factor?", "a": "Money factor is lease interest expressed in decimal form. Multiply the money factor by 2,400 to find the equivalent annual percentage rate (APR). For example: 0.0025 × 2,400 = 6.0% APR."}
        ],
        "js_logic": """
          const price = getNum('vehicle_price');
          const down = getNum('down_payment');
          const term = getNum('lease_term_months') || 36;
          const leaseMo = getNum('lease_monthly');
          const apr = (getNum('loan_apr_pct') || 6.5) / 100;
          const resPct = (getNum('residual_value_pct') || 55) / 100;

          const totalLease = down + (leaseMo * term) + 400;

          const loanPrin = Math.max(0, price - down);
          const r = apr / 12;
          const buyMo = r > 0 ? (loanPrin * (r * Math.pow(1 + r, term)) / (Math.pow(1 + r, term) - 1)) : (loanPrin / term);
          const totalBuyPayments = down + (buyMo * term);
          const residualEquity = price * resPct;
          const netBuyCost = totalBuyPayments - residualEquity;

          const diff = Math.abs(totalLease - netBuyCost);
          let winner = totalLease < netBuyCost ? ('Leasing Saves ~$' + Math.round(diff).toLocaleString()) : ('Purchasing Saves ~$' + Math.round(diff).toLocaleString());

          setDisp('net_lease_cost', '$' + totalLease.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_buy_cost', '$' + netBuyCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('financial_winner', winner);
          setDisp('equity_retained', '$' + residualEquity.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "ev-charging-cost",
        "category": "physics",
        "name": "Electric Vehicle (EV) Charging Cost & Range Calculator",
        "description": "Calculate exact dollar cost to fully charge an electric car at home versus public DC fast chargers, cost per mile, and monthly charging expense.",
        "hero_badge": "Electric Mobility • EV Energy Economics",
        "formula_display": "Full Charge Cost = Battery Capacity (kWh) × Electricity Rate ($/kWh) / Charging Efficiency",
        "fields": [
            {"id": "battery_kwh", "label": "Usable Battery Pack Capacity (kWh)", "default": 75, "suffix": "kWh", "min": 15, "max": 220, "step": 1, "hint": "Tesla Model 3/Y ≈ 75-82 kWh, F-150 Lightning ≈ 131 kWh"},
            {"id": "home_kwh_rate", "label": "Home Electric Rate ($/kWh)", "default": 0.16, "prefix": "$", "min": 0.04, "max": 0.70, "step": 0.01, "hint": "US national average: ~$0.16/kWh"},
            {"id": "public_kwh_rate", "label": "Public DC Fast Charge Rate ($/kWh)", "default": 0.42, "prefix": "$", "min": 0.15, "max": 0.85, "step": 0.01, "hint": "Tesla Supercharger / Electrify America: ~$0.35 - $0.48/kWh"},
            {"id": "rated_range_miles", "label": "Full Battery Driving Range", "default": 310, "suffix": "miles", "min": 80, "max": 600, "step": 5, "hint": "EPA estimated range on full charge"},
            {"id": "monthly_miles_driven", "label": "Monthly Driving Distance", "default": 1200, "suffix": "miles/mo", "min": 100, "max": 10000, "step": 50, "hint": "Average commute and road trips"}
        ],
        "metrics": [
            {"id": "home_full_charge", "label": "Home Full 0-100% Charge Cost", "default_display": "$13.33", "highlight": True},
            {"id": "public_full_charge", "label": "Public Fast 0-100% Charge Cost", "default_display": "$35.00", "highlight": True},
            {"id": "home_cost_per_mile", "label": "Home Electricity Cost per Mile", "default_display": "$0.043 / mile", "highlight": True},
            {"id": "monthly_home_bill", "label": "Estimated Monthly Home EV Electric Bill", "default_display": "$51.60 / mo"}
        ],
        "proof_steps": [
            {"step_title": "AC Charging Efficiency Adjustment", "step_text": "AC home charging incurs 10% thermal and inverter energy loss (efficiency η ≈ 90%). Energy drawn from grid = Battery Capacity / 0.90."},
            {"step_title": "Direct Full Recharge Cost", "step_text": "Cost_home = (Battery kWh / 0.90) × Rate_home. Cost_public = (Battery kWh / 0.90) × Rate_public."},
            {"step_title": "Distance Energy Intensity (Wh/mi)", "step_text": "Efficiency = (Battery kWh × 1000) / Range Miles. Cost per Mile = Cost_home / Range Miles."}
        ],
        "faqs": [
            {"q": "How much does it cost to charge a Tesla at home?", "a": "For a standard 75 kWh battery pack at the US average residential electricity rate of $0.16/kWh, a full charge costs approximately $13.30, providing roughly 300 miles of range ($0.044 per mile)."},
            {"q": "Is DC fast charging more expensive than gasoline?", "a": "DC fast charging ($0.40-$0.50/kWh) works out to roughly $0.10 to $0.13 per mile, which is still cheaper than a 25 MPG gas car ($0.14/mile at $3.50/gal), but roughly 3× more expensive than charging overnight at home."}
        ],
        "js_logic": """
          const kwh = getNum('battery_kwh');
          const homeRate = getNum('home_kwh_rate');
          const pubRate = getNum('public_kwh_rate');
          const range = getNum('rated_range_miles') || 1;
          const miles = getNum('monthly_miles_driven');

          const eff = 0.90;
          const gridKwh = kwh / eff;
          const homeFull = gridKwh * homeRate;
          const pubFull = gridKwh * pubRate;

          const costPerMile = homeFull / range;
          const monthlyBill = miles * costPerMile;

          setDisp('home_full_charge', '$' + homeFull.toFixed(2));
          setDisp('public_full_charge', '$' + pubFull.toFixed(2));
          setDisp('home_cost_per_mile', '$' + costPerMile.toFixed(3) + ' / mile');
          setDisp('monthly_home_bill', '$' + monthlyBill.toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "ev-vs-gas-savings",
        "category": "finance",
        "name": "Electric Vehicle vs Gas Savings Calculator",
        "description": "Calculate annual fuel, maintenance, and brake pad cost savings switching from an internal combustion engine (ICE) car to an EV.",
        "hero_badge": "Fleet Decarbonization • EV vs ICE Fuel Economics",
        "formula_display": "Annual Savings = (Gas Gallons × Price/Gal + ICE Maint) - (EV kWh × Price/kWh + EV Maint)",
        "fields": [
            {"id": "annual_miles", "label": "Annual Driving Mileage", "default": 13500, "suffix": "miles/yr", "min": 2000, "max": 100000, "step": 500, "hint": "US driver average: ~13,500 miles/yr"},
            {"id": "gas_car_mpg", "label": "Current Gas Car Fuel Economy (MPG)", "default": 27, "suffix": "MPG", "min": 10, "max": 65, "step": 1, "hint": "Combined city/highway miles per gallon"},
            {"id": "gas_price_gallon", "label": "Local Gasoline Price ($/Gallon)", "default": 3.65, "prefix": "$", "min": 2.00, "max": 7.50, "step": 0.05, "hint": "Price per gallon of regular unleaded"},
            {"id": "ev_efficiency_mi_kwh", "label": "EV Efficiency (Miles per kWh)", "default": 3.6, "suffix": "mi/kWh", "min": 1.5, "max": 5.0, "step": 0.1, "hint": "Standard EV: 3.2 to 4.0 miles/kWh"},
            {"id": "electric_rate", "label": "Electricity Rate ($/kWh)", "default": 0.16, "prefix": "$", "min": 0.05, "max": 0.60, "step": 0.01, "hint": "Overnight home charging utility rate"}
        ],
        "metrics": [
            {"id": "annual_total_savings", "label": "Annual Total Operating Savings", "default_display": "$1,725.00 / yr", "highlight": True},
            {"id": "five_year_savings", "label": "5-Year Cumulative Savings", "default_display": "$8,625.00", "highlight": True},
            {"id": "annual_gas_fuel_cost", "label": "Annual Gasoline Expenditure", "default_display": "$1,825.00 / yr"},
            {"id": "annual_ev_fuel_cost", "label": "Annual EV Electricity Expenditure", "default_display": "$600.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Internal Combustion Energy Expense", "step_text": "Annual Gas Cost = (Annual Miles / MPG) × Gas Price/Gallon. Annual ICE Maintenance ≈ $0.06/mile (oil changes, spark plugs, belts, transmissions)."},
            {"step_title": "Electric Drivetrain Energy Expense", "step_text": "Annual EV Power Cost = (Annual Miles / mi/kWh) × Electricity Rate. Annual EV Maintenance ≈ $0.02/mile (cabin filters, tire rotations; no motor oil or transmission fluid)."},
            {"step_title": "Compound Economic Differential", "step_text": "Net Annual Savings = (Gas Fuel + ICE Maintenance) - (EV Electricity + EV Maintenance). Over a 5-year ownership horizon, fuel and maintenance differentials frequently surpass $8,000 to $12,000."}
        ],
        "faqs": [
            {"q": "Do EVs really require less maintenance than gas cars?", "a": "Yes. An electric vehicle drivetrain has approximately 20 moving parts compared to over 2,000 in an internal combustion engine and multi-speed automatic transmission. EVs require zero oil changes, no spark plugs, no oxygen sensors, and regenerative braking preserves brake pads for 100,000+ miles."},
            {"q": "What about battery degradation replacement costs?", "a": "Modern EV lithium-ion battery packs are engineered to last 300,000 to 500,000 miles with less than 15-20% degradation and are protected by federally mandated 8-year / 100,000-mile manufacturer warranties."}
        ],
        "js_logic": """
          const miles = getNum('annual_miles');
          const mpg = getNum('gas_car_mpg') || 27;
          const gasPrice = getNum('gas_price_gallon');
          const miKwh = getNum('ev_efficiency_mi_kwh') || 3.6;
          const elRate = getNum('electric_rate');

          const annualGasFuel = (miles / mpg) * gasPrice;
          const annualIceMaint = miles * 0.06;
          const totalIceCost = annualGasFuel + annualIceMaint;

          const annualEvFuel = (miles / miKwh) * elRate;
          const annualEvMaint = miles * 0.02;
          const totalEvCost = annualEvFuel + annualEvMaint;

          const annualSavings = totalIceCost - totalEvCost;
          const fiveYrSavings = annualSavings * 5;

          setDisp('annual_total_savings', '$' + Math.round(annualSavings).toLocaleString() + ' / yr');
          setDisp('five_year_savings', '$' + Math.round(fiveYrSavings).toLocaleString());
          setDisp('annual_gas_fuel_cost', '$' + Math.round(annualGasFuel).toLocaleString() + ' / yr');
          setDisp('annual_ev_fuel_cost', '$' + Math.round(annualEvFuel).toLocaleString() + ' / yr');
        """
    },
    {
        "slug": "car-depreciation",
        "category": "finance",
        "name": "Car Depreciation & Future Value Curve Calculator",
        "description": "Calculate multi-year vehicle depreciation curves, month-by-month residual value, dollar loss per mile driven, and optimal trade-in horizons.",
        "hero_badge": "Automotive Asset Valuation • Depreciation Curve Matrix",
        "formula_display": "Value(t) = Purchase Price × (1 - Depreciation Rate)^t",
        "fields": [
            {"id": "initial_purchase_price", "label": "Vehicle Purchase Price", "default": 45000, "prefix": "$", "min": 5000, "max": 250000, "step": 1000, "hint": "Original out-the-door price paid"},
            {"id": "vehicle_age_years", "label": "Ownership Horizon (Years)", "default": 5, "suffix": "years", "min": 1, "max": 15, "step": 1, "hint": "Years you plan to keep vehicle"},
            {"id": "depreciation_profile", "label": "Depreciation Category (0.85 Low/Toyota, 1.0 Normal, 1.25 Luxury/German)", "default": 1.0, "min": 0.7, "max": 1.6, "step": 0.05, "hint": "Trucks/Hondas hold value; luxury sedans drop fast"}
        ],
        "metrics": [
            {"id": "residual_future_value", "label": "Projected Future Resale Value", "default_display": "$18,000.00", "highlight": True},
            {"id": "total_dollar_depreciation", "label": "Total Cumulative Dollar Loss", "default_display": "-$27,000.00", "highlight": True},
            {"id": "first_year_drop", "label": "Year 1 Immediate Depreciation", "default_display": "$9,000.00 (20%)", "highlight": True},
            {"id": "monthly_depreciation_cost", "label": "Average Monthly Depreciation Drag", "default_display": "$450.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Year 1 Drive-Off Steeper Loss", "step_text": "New vehicles lose an immediate 10% when driving off the dealer lot and ~20% by the end of year 1: V_1 = Price × (1 - 0.20 × Profile)."},
            {"step_title": "Compound Annual Resale Decay", "step_text": "In years 2 through 5, vehicles depreciate by approximately 15% of their remaining balance annually: V_t = V_1 × (1 - 0.15 × Profile)^(t - 1)."},
            {"step_title": "The 5-Year Residual Benchmark", "step_text": "By year 5, average vehicles retain approximately 40% of initial MSRP (luxury sedans retain ~30-35%; Toyota Tacomas retain ~55-60%)."}
        ],
        "faqs": [
            {"q": "What vehicles have the lowest depreciation rates?", "a": "Midsize trucks, sports cars, and Japanese brands (Toyota Tacoma, Jeep Wrangler, Porsche 911, Honda Civic) consistently lead the industry with the highest 5-year resale value retention."},
            {"q": "How can I avoid severe car depreciation?", "a": "Buy 2 to 3-year-old certified pre-owned (CPO) vehicles. The initial owner absorbs the steep 30-40% year 1-3 depreciation drop, leaving you with stable, gradual curve loss."}
        ],
        "js_logic": """
          const price = getNum('initial_purchase_price');
          const years = getNum('vehicle_age_years') || 5;
          const profile = getNum('depreciation_profile') || 1.0;

          const yr1Rate = Math.min(0.35, 0.20 * profile);
          const yr1Val = price * (1 - yr1Rate);

          let currentVal = yr1Val;
          const subsequentRate = Math.min(0.25, 0.15 * profile);
          for (let y = 2; y <= years; y++) {
            currentVal *= (1 - subsequentRate);
          }

          const totalDrop = price - currentVal;
          const yr1Drop = price - yr1Val;
          const monthlyDrag = totalDrop / (years * 12);

          setDisp('residual_future_value', '$' + Math.round(currentVal).toLocaleString());
          setDisp('total_dollar_depreciation', '-$' + Math.round(totalDrop).toLocaleString());
          setDisp('first_year_drop', '$' + Math.round(yr1Drop).toLocaleString() + ' (' + (yr1Rate * 100).toFixed(0) + '%)');
          setDisp('monthly_depreciation_cost', '$' + Math.round(monthlyDrag).toLocaleString() + ' / mo');
        """
    },
    {
        "slug": "true-cost-to-own",
        "category": "finance",
        "name": "5-Year True Cost to Own (TCO) Calculator",
        "description": "Calculate true full cost to own a vehicle over 5 years combining depreciation, financing interest, fuel, insurance, maintenance, and state taxes.",
        "hero_badge": "Fleet Economics • Full Vehicle TCO Matrix",
        "formula_display": "5-Yr TCO = Depreciation + Financing + Insurance + Fuel + Maintenance + Taxes/Fees",
        "fields": [
            {"id": "purchase_price_tco", "label": "Vehicle Purchase Price", "default": 40000, "prefix": "$", "min": 5000, "max": 250000, "step": 1000, "hint": "Total negotiated price"},
            {"id": "monthly_fuel_cost", "label": "Estimated Monthly Fuel / Power Cost", "default": 175, "prefix": "$", "min": 20, "max": 1500, "step": 10, "hint": "Gas or electricity expenditure"},
            {"id": "monthly_insurance", "label": "Monthly Auto Insurance Premium", "default": 160, "prefix": "$", "min": 30, "max": 1000, "step": 5, "hint": "Full coverage insurance premium"},
            {"id": "loan_interest_total", "label": "Total 5-Year Financing Interest Paid", "default": 4500, "prefix": "$", "min": 0, "max": 40000, "step": 100, "hint": "Interest accrued on auto loan"}
        ],
        "metrics": [
            {"id": "total_5yr_tco", "label": "Total 5-Year True Cost to Own", "default_display": "$52,600.00", "highlight": True},
            {"id": "monthly_effective_tco", "label": "Effective Monthly Cost of Ownership", "default_display": "$876.67 / mo", "highlight": True},
            {"id": "cost_per_mile_tco", "label": "True Cost per Mile (13.5k mi/yr)", "default_display": "$0.78 / mile", "highlight": True},
            {"id": "depreciation_share", "label": "Depreciation Share of Total Cost", "default_display": "$24,000.00 (45.6%)"}
        ],
        "proof_steps": [
            {"step_title": "Six Pillars of Vehicle Cost Breakdown", "step_text": "TCO = 1) Depreciation (typically 60% drop in 5 yrs) + 2) Fuel (60 mo) + 3) Insurance (60 mo) + 4) Financing Interest + 5) Maintenance & Repairs ($1,000/yr) + 6) Registration/Fees ($300/yr)."},
            {"step_title": "Hidden Depreciation Primacy", "step_text": "Depreciation is the single largest hidden expense of vehicle ownership, frequently exceeding fuel and insurance combined."},
            {"step_title": "Per-Mile Amortization Metric", "step_text": "Total 5-year miles = 5 × 13,500 = 67,500 miles. Cost per Mile = TCO / 67,500."}
        ],
        "faqs": [
            {"q": "What is the true cost of owning an average new car?", "a": "According to AAA's annual 'Your Driving Costs' study, the average cost to own and operate a new car in the United States exceeds $12,000 per year ($1,000+ per month or ~$0.75 to $0.85 per mile) when including all depreciation and insurance."},
            {"q": "How can I cut my vehicle TCO by half?", "a": "Buy reliable 4-year-old used vehicles in cash, shop auto insurance annually, maintain vehicles proactively to prevent catastrophic repairs, and hold cars for 8 to 10 years."}
        ],
        "js_logic": """
          const price = getNum('purchase_price_tco');
          const fuelMo = getNum('monthly_fuel_cost');
          const insMo = getNum('monthly_insurance');
          const interest = getNum('loan_interest_total');

          const dep = price * 0.60;
          const fuel5Yr = fuelMo * 60;
          const ins5Yr = insMo * 60;
          const maint5Yr = 5000;
          const fees5Yr = 1500;

          const totalTco = dep + fuel5Yr + ins5Yr + interest + maint5Yr + fees5Yr;
          const monthlyTco = totalTco / 60;
          const costPerMile = totalTco / (5 * 13500);
          const depShare = (dep / totalTco) * 100;

          setDisp('total_5yr_tco', '$' + Math.round(totalTco).toLocaleString());
          setDisp('monthly_effective_tco', '$' + monthlyTco.toFixed(2) + ' / mo');
          setDisp('cost_per_mile_tco', '$' + costPerMile.toFixed(2) + ' / mile');
          setDisp('depreciation_share', '$' + Math.round(dep).toLocaleString() + ' (' + depShare.toFixed(1) + '%)');
        """
    },
    {
        "slug": "towing-capacity",
        "category": "physics",
        "name": "Vehicle Towing Capacity & Tongue Weight Calculator",
        "description": "Calculate safe legal towing capacity, Gross Combined Weight Rating (GCWR), allowable trailer weight, and mandatory 10-15% tongue weight.",
        "hero_badge": "Vehicle Dynamics • Safe Towing Matrix",
        "formula_display": "Max Safe Tow = GCWR - Vehicle Curb Weight - Passenger/Cargo Payload",
        "fields": [
            {"id": "gcwr_lbs", "label": "Gross Combined Weight Rating (GCWR)", "default": 15000, "suffix": "lbs", "min": 3000, "max": 45000, "step": 250, "hint": "Maximum allowed weight of truck + trailer combined"},
            {"id": "curb_weight_lbs", "label": "Vehicle Curb Weight (Empty)", "default": 5400, "suffix": "lbs", "min": 2000, "max": 15000, "step": 100, "hint": "Weight of empty tow vehicle"},
            {"id": "payload_passengers_lbs", "label": "Passengers & Cargo in Vehicle", "default": 850, "suffix": "lbs", "min": 150, "max": 5000, "step": 50, "hint": "Driver, passengers, luggage, and tools inside truck"},
            {"id": "trailer_gvwr_target", "label": "Loaded Trailer Weight (Target)", "default": 6500, "suffix": "lbs", "min": 500, "max": 35000, "step": 250, "hint": "Dry trailer weight plus water, propane, and gear"}
        ],
        "metrics": [
            {"id": "max_allowable_trailer", "label": "True Real-World Max Tow Capacity", "default_display": "8,750 lbs", "highlight": True},
            {"id": "tongue_weight_range", "label": "Safe Tongue Weight Window (10-15%)", "default_display": "650 - 975 lbs", "highlight": True},
            {"id": "remaining_gcwr_buffer", "label": "Remaining GCWR Safety Buffer", "default_display": "2,250 lbs (15.0%)", "highlight": True},
            {"id": "safety_status", "label": "Towing Safety Assessment", "default_display": "Safe (Within All Legal Limits)"}
        ],
        "proof_steps": [
            {"step_title": "The Real-World Towing Capacity Law", "step_text": "Advertised 'maximum tow rating' assumes an empty truck with only a 150 lb driver. Real-world capacity: Max Allowable Trailer = GCWR - Vehicle Curb Weight - Passenger Payload - Cargo."},
            {"step_title": "Tongue Weight Physics Stability", "step_text": "To prevent lethal high-speed trailer sway, 10% to 15% of total loaded trailer weight must press down directly on the hitch ball: Tongue Weight = Trailer Weight × [0.10 to 0.15]."},
            {"step_title": "Payload Overload Trap", "step_text": "Tongue weight counts against vehicle GVWR payload! Most trucks exceed their payload rating long before hitting maximum tow capacity."}
        ],
        "faqs": [
            {"q": "Why is tongue weight so critical for trailer towing?", "a": "If tongue weight is under 10%, the trailer becomes back-heavy, inducing violent aerodynamic fishtailing and sway at highway speeds that can flip both truck and trailer. If tongue weight exceeds 15%, the rear truck axle is overloaded, unloading front steer tires and compromising braking."},
            {"q": "What is the difference between GVWR and GCWR?", "a": "GVWR (Gross Vehicle Weight Rating) is the maximum legal weight of the tow vehicle alone (including tongue weight). GCWR (Gross Combined Weight Rating) is the maximum legal weight of truck AND trailer combined."}
        ],
        "js_logic": """
          const gcwr = getNum('gcwr_lbs');
          const curb = getNum('curb_weight_lbs');
          const payload = getNum('payload_passengers_lbs');
          const trailer = getNum('trailer_gvwr_target');

          const trueMaxTow = Math.max(0, gcwr - curb - payload);
          const minTongue = trailer * 0.10;
          const maxTongue = trailer * 0.15;
          const totalCombined = curb + payload + trailer;
          const buffer = gcwr - totalCombined;
          const bufferPct = gcwr > 0 ? (buffer / gcwr) * 100 : 0;

          let status = 'Safe (Within All Legal Limits)';
          if (totalCombined > gcwr) status = 'DANGER: Overloaded GCWR by ' + Math.abs(buffer).toLocaleString() + ' lbs';
          else if (bufferPct < 10) status = 'Caution: Near Capacity (< 10% safety margin)';

          setDisp('max_allowable_trailer', trueMaxTow.toLocaleString() + ' lbs');
          setDisp('tongue_weight_range', Math.round(minTongue).toLocaleString() + ' - ' + Math.round(maxTongue).toLocaleString() + ' lbs');
          setDisp('remaining_gcwr_buffer', buffer.toLocaleString() + ' lbs (' + bufferPct.toFixed(1) + '%)');
          setDisp('safety_status', status);
        """
    },
    {
        "slug": "payload-capacity",
        "category": "physics",
        "name": "Truck Payload Capacity & Cargo Safety Margin Calculator",
        "description": "Calculate actual remaining payload capacity from Gross Vehicle Weight Rating (GVWR), curb weight, aftermarket accessories, and passenger weight.",
        "hero_badge": "Truck Engineering • Payload GVWR Matrix",
        "formula_display": "Available Payload = GVWR - Vehicle Curb Weight - Driver & Passengers - Tongue Weight",
        "fields": [
            {"id": "gvwr_sticker", "label": "Door Jamb GVWR Rating", "default": 7100, "suffix": "lbs", "min": 2000, "max": 20000, "step": 100, "hint": "Gross Vehicle Weight Rating on tire placard"},
            {"id": "curb_weight_actual", "label": "Vehicle Base Curb Weight", "default": 5150, "suffix": "lbs", "min": 1500, "max": 15000, "step": 50, "hint": "Weight with full tank of gas, empty cargo"},
            {"id": "occupant_weight", "label": "Driver & Passengers Total Weight", "default": 550, "suffix": "lbs", "min": 100, "max": 2500, "step": 25, "hint": "Weight of all people in cab"},
            {"id": "accessories_cargo", "label": "Truck Bed Cargo & Accessories", "default": 400, "suffix": "lbs", "min": 0, "max": 5000, "step": 25, "hint": "Toolbox, bed cover, winch, luggage, coolers"}
        ],
        "metrics": [
            {"id": "net_payload_remaining", "label": "Remaining Available Payload", "default_display": "1,000 lbs", "highlight": True},
            {"id": "total_gvwr_payload", "label": "Original Maximum Payload Rating", "default_display": "1,950 lbs", "highlight": True},
            {"id": "gvwr_utilization_pct", "label": "Gross Weight Capacity Used", "default_display": "85.9%", "highlight": True},
            {"id": "payload_verdict", "label": "Weight Rating Compliance", "default_display": "Legal & Safe (1,000 lbs headroom)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Vehicle Weight Rating Constraint", "step_text": "GVWR is the absolute legal operating ceiling established by the chassis, suspension, tire load indexes, and brake engineers."},
            {"step_title": "Maximum Static Payload Formula", "step_text": "Sticker Payload = GVWR - Base Curb Weight."},
            {"step_title": "Real-World Usable Headroom", "step_text": "Remaining Usable Payload = Sticker Payload - Cab Occupants - Bed Accessories - Tongue Weight. Exceeding GVWR compromises emergency braking and voids auto insurance liability coverage."}
        ],
        "faqs": [
            {"q": "Does towing a trailer reduce truck payload capacity?", "a": "Yes! Trailer tongue weight rests directly on the truck hitch ball and must be subtracted pound-for-pound from available payload capacity. An 800 lb tongue weight consumes 800 lbs of your truck's payload capacity."},
            {"q": "Can helper springs or air bags increase payload capacity?", "a": "No! Air bags and helper springs level the vehicle and prevent rear suspension sag, but they do NOT legally or mechanically increase the manufacturer GVWR, which is limited by axles, wheel bearings, frames, and brakes."}
        ],
        "js_logic": """
          const gvwr = getNum('gvwr_sticker');
          const curb = getNum('curb_weight_actual');
          const occ = getNum('occupant_weight');
          const cargo = getNum('accessories_cargo');

          const origPayload = gvwr - curb;
          const currentWeight = curb + occ + cargo;
          const remaining = gvwr - currentWeight;
          const utilPct = gvwr > 0 ? (currentWeight / gvwr) * 100 : 0;

          let verdict = 'Legal & Safe (' + remaining.toLocaleString() + ' lbs headroom)';
          if (remaining < 0) verdict = 'ILLEGAL OVERLOAD by ' + Math.abs(remaining).toLocaleString() + ' lbs (Safety Hazard)';
          else if (remaining < 200) verdict = 'Warning: At Critical Limit (< 200 lbs margin)';

          setDisp('net_payload_remaining', remaining.toLocaleString() + ' lbs');
          setDisp('total_gvwr_payload', origPayload.toLocaleString() + ' lbs');
          setDisp('gvwr_utilization_pct', utilPct.toFixed(1) + '%');
          setDisp('payload_verdict', verdict);
        """
    },
    {
        "slug": "gas-mileage-mpg",
        "category": "physics",
        "name": "Gas Mileage (MPG / L/100km) & Fuel Cost Calculator",
        "description": "Calculate exact gas mileage in US MPG, Imperial MPG, and Liters per 100km, cost per mile, and annual fuel expense.",
        "hero_badge": "Fuel Economy • Multi-Standard Metric Matrix",
        "formula_display": "US MPG = Miles Driven / Gallons Consumed | L/100km = 235.215 / US MPG",
        "fields": [
            {"id": "trip_odometer_miles", "label": "Miles Driven Between Fill-ups", "default": 345, "suffix": "miles", "min": 20, "max": 1500, "step": 5, "hint": "Miles on trip odometer when refueling"},
            {"id": "gallons_pumped", "label": "Gallons Pumped into Tank", "default": 12.8, "suffix": "gallons", "min": 1, "max": 100, "step": 0.1, "hint": "Exact fuel gallons from gas station receipt"},
            {"id": "fuel_price_per_gal", "label": "Fuel Price per Gallon", "default": 3.65, "prefix": "$", "min": 1.50, "max": 9.00, "step": 0.05, "hint": "Current pump price per gallon"}
        ],
        "metrics": [
            {"id": "us_mpg_result", "label": "Fuel Economy (US MPG)", "default_display": "26.95 MPG", "highlight": True},
            {"id": "metric_fuel_economy", "label": "Metric Consumption (L/100km)", "default_display": "8.73 L/100km", "highlight": True},
            {"id": "cost_per_mile_fuel", "label": "Fuel Cost per Mile", "default_display": "$0.135 / mile", "highlight": True},
            {"id": "fillup_total_cost", "label": "Total Fill-Up Cost", "default_display": "$46.72"}
        ],
        "proof_steps": [
            {"step_title": "Direct Volumetric Consumption", "step_text": "MPG = Distance (Miles) / Volume (Gallons). For example: 345 miles / 12.8 gallons = 26.95 MPG."},
            {"step_title": "Metric Inverse Representation", "step_text": "In Europe and Canada, fuel consumption is measured inversely as Liters consumed per 100 km: L/100km = 235.215 / US MPG."},
            {"step_title": "Cost per Distance Traveled", "step_text": "Cost/Mile = Fuel Price / MPG. At $3.65/gal and 26.95 MPG: 3.65 / 26.95 = $0.135/mile."}
        ],
        "faqs": [
            {"q": "Why is L/100km better for comparing efficiency than MPG?", "a": "MPG is non-linear. Upgrading from 10 MPG to 20 MPG saves 50 gallons every 1,000 miles. Upgrading from 40 MPG to 50 MPG saves only 5 gallons. L/100km represents consumption linearly, accurately reflecting fuel saved."},
            {"q": "How can I improve my car's gas mileage by 15%?", "a": "Maintain correct tire inflation pressures (+2-3 PSI), eliminate excess cargo weight from trunk, replace clogged air filters, and avoid rapid jackrabbit acceleration."}
        ],
        "js_logic": """
          const miles = getNum('trip_odometer_miles');
          const gal = getNum('gallons_pumped') || 1;
          const price = getNum('fuel_price_per_gal');

          const mpg = miles / gal;
          const l100km = mpg > 0 ? (235.215 / mpg) : 0;
          const costMile = mpg > 0 ? (price / mpg) : 0;
          const totalCost = gal * price;

          setDisp('us_mpg_result', mpg.toFixed(2) + ' MPG');
          setDisp('metric_fuel_economy', l100km.toFixed(2) + ' L/100km');
          setDisp('cost_per_mile_fuel', '$' + costMile.toFixed(3) + ' / mile');
          setDisp('fillup_total_cost', '$' + totalCost.toFixed(2));
        """
    },
    {
        "slug": "tire-size-speedometer",
        "category": "physics",
        "name": "Tire Size Comparison & Speedometer Error Calculator",
        "description": "Calculate tire diameter, sidewall height, revolutions per mile, and exact speedometer error when changing tire sizes.",
        "hero_badge": "Tire Dynamics • Speedometer Calibration Matrix",
        "formula_display": "Tire Diameter = 2 × (Width × Aspect Ratio / 25.4) + Rim Diameter | Actual Speed = Indicated Speed × (New Diameter / Old Diameter)",
        "fields": [
            {"id": "orig_width", "label": "Original Tire Width (mm)", "default": 245, "suffix": "mm", "min": 135, "max": 405, "step": 10, "hint": "e.g. 245/45R18"},
            {"id": "orig_aspect", "label": "Original Aspect Ratio (%)", "default": 45, "suffix": "%", "min": 25, "max": 90, "step": 5, "hint": "Sidewall height as % of width"},
            {"id": "orig_rim", "label": "Original Wheel Rim Diameter", "default": 18, "suffix": "in", "min": 12, "max": 28, "step": 1, "hint": "Wheel diameter in inches"},
            {"id": "new_width", "label": "New Tire Width (mm)", "default": 275, "suffix": "mm", "min": 135, "max": 405, "step": 10, "hint": "e.g. 275/40R19"},
            {"id": "new_aspect", "label": "New Aspect Ratio (%)", "default": 40, "suffix": "%", "min": 25, "max": 90, "step": 5, "hint": "New sidewall %"},
            {"id": "new_rim", "label": "New Wheel Rim Diameter", "default": 19, "suffix": "in", "min": 12, "max": 28, "step": 1, "hint": "New rim diameter in inches"}
        ],
        "metrics": [
            {"id": "actual_speed_at_65", "label": "Actual Speed when Speedometer Reads 65 MPH", "default_display": "67.1 MPH", "highlight": True},
            {"id": "diameter_difference_pct", "label": "Overall Diameter Variance", "default_display": "+3.2% (+0.85 in)", "highlight": True},
            {"id": "orig_diameter_in", "label": "Original Tire Diameter", "default_display": "26.68 inches"},
            {"id": "new_diameter_in", "label": "New Tire Diameter", "default_display": "27.53 inches"}
        ],
        "proof_steps": [
            {"step_title": "Metric to Imperial Tire Geometry", "step_text": "Sidewall Height = Width (mm) × (Aspect Ratio / 100) / 25.4. Total Diameter = (2 × Sidewall) + Rim Diameter."},
            {"step_title": "Rolling Circumference and Revolutions", "step_text": "Circumference C = π × Diameter. Revolutions per Mile = 63,360 / Circumference."},
            {"step_title": "Speedometer Kinematic Coupling", "step_text": "Because the vehicle speed sensor reads transmission/wheel rotation frequency, changing tire circumference alters actual road speed: Actual Speed = Indicated Speed × (New Diameter / Old Diameter)."}
        ],
        "faqs": [
            {"q": "What is the maximum safe tire size change without recalibration?", "a": "Automotive engineers recommend keeping overall tire diameter changes within ±3.0% of factory specifications to prevent anti-lock brake (ABS), traction control, and speedometer calibration malfunctions."},
            {"q": "Will larger tires make my car faster or slower?", "a": "Larger diameter tires increase your top speed at a given engine RPM, but decrease off-the-line wheel torque and acceleration because they effectively create a taller final drive gear ratio."}
        ],
        "js_logic": """
          const w1 = getNum('orig_width');
          const a1 = (getNum('orig_aspect') || 45) / 100;
          const r1 = getNum('orig_rim');

          const w2 = getNum('new_width');
          const a2 = (getNum('new_aspect') || 40) / 100;
          const r2 = getNum('new_rim');

          const d1 = (2 * (w1 * a1 / 25.4)) + r1;
          const d2 = (2 * (w2 * a2 / 25.4)) + r2;

          const ratio = d2 / d1;
          const diffIn = d2 - d1;
          const diffPct = ((d2 - d1) / d1) * 100;
          const actualSpeed = 65 * ratio;

          setDisp('actual_speed_at_65', actualSpeed.toFixed(1) + ' MPH');
          setDisp('diameter_difference_pct', (diffPct >= 0 ? '+' : '') + diffPct.toFixed(1) + '% (' + (diffIn >= 0 ? '+' : '') + diffIn.toFixed(2) + ' in)');
          setDisp('orig_diameter_in', d1.toFixed(2) + ' inches');
          setDisp('new_diameter_in', d2.toFixed(2) + ' inches');
        """
    },
    {
        "slug": "horsepower-torque",
        "category": "physics",
        "name": "Horsepower & Torque Conversion Calculator",
        "description": "Convert between rotational Torque (lb-ft or N·m) and Mechanical Horsepower (HP / kW) at any engine RPM, proving the 5,252 RPM crossover law.",
        "hero_badge": "Mechanical Power • Drivetrain Physics Matrix",
        "formula_display": "Horsepower = (Torque in lb-ft × Engine RPM) / 5,252 | kW = HP × 0.7457",
        "fields": [
            {"id": "torque_input_lbft", "label": "Engine Torque (lb-ft)", "default": 400, "suffix": "lb-ft", "min": 10, "max": 2500, "step": 10, "hint": "Torque measured at flywheel or dyno"},
            {"id": "engine_rpm_point", "label": "Engine Speed (RPM)", "default": 5500, "suffix": "RPM", "min": 500, "max": 18000, "step": 100, "hint": "Revolutions per minute"},
            {"id": "mechanical_metric_nm", "label": "Metric Torque Equivalence (N·m)", "default": 542.3, "suffix": "N·m", "min": 10, "max": 3500, "step": 10, "hint": "Metric Newton-meters"}
        ],
        "metrics": [
            {"id": "horsepower_calculated", "label": "Calculated Horsepower (HP)", "default_display": "418.89 HP", "highlight": True},
            {"id": "kilowatts_output", "label": "Metric Power Output (kW)", "default_display": "312.37 kW", "highlight": True},
            {"id": "torque_hp_crossover_note", "label": "5,252 RPM Crossover Status", "default_display": "Above 5,252 RPM (HP exceeds Torque)", "highlight": True},
            {"id": "foot_pounds_work", "label": "Rotational Work per Second", "default_display": "230,388 ft-lb / sec"}
        ],
        "proof_steps": [
            {"step_title": "James Watt Horsepower Definition", "step_text": "One mechanical horsepower HP = 33,000 foot-pounds of work per minute = 550 ft-lb/sec."},
            {"step_title": "Rotational Work Angular Velocity", "step_text": "Power = Torque × Angular Velocity = Torque (lb-ft) × [2π × RPM / 60] / 550. Combining constants: 550 × 60 / (2π) = 33,000 / 2π = 5,252.113."},
            {"step_title": "The 5,252 RPM Dyno Invariant", "step_text": "On every dyno chart on Earth plotting horsepower and torque in lb-ft on identical scales, the curves MUST cross precisely at 5,252 RPM: HP ≡ Torque at 5,252 RPM."}
        ],
        "faqs": [
            {"q": "Why do horsepower and torque curves always cross at 5,252 RPM?", "a": "Because of unit definitions! Since 1 HP is defined as 33,000 ft-lb/min, and one revolution equals 2π radians, the constant is 33,000 / 2π = 5,252. At 5,252 RPM, HP = (Torque × 5,252) / 5,252 = Torque."},
            {"q": "What is the difference between horsepower and torque?", "a": "Torque is instantaneous twisting force (how much work the engine can do). Horsepower is how rapidly that twisting force is applied over time (how fast work gets done). Torque gives you acceleration off the line; horsepower delivers top-end speed."}
        ],
        "js_logic": """
          const tq = getNum('torque_input_lbft');
          const rpm = getNum('engine_rpm_point');

          const hp = (tq * rpm) / 5252;
          const kw = hp * 0.745699872;
          const workSec = hp * 550;

          let crossNote = 'At 5,252 RPM Crossover (HP == Torque)';
          if (rpm > 5252) crossNote = 'Above 5,252 RPM (HP exceeds Torque)';
          else if (rpm < 5252) crossNote = 'Below 5,252 RPM (Torque exceeds HP)';

          setDisp('horsepower_calculated', hp.toFixed(2) + ' HP');
          setDisp('kilowatts_output', kw.toFixed(2) + ' kW');
          setDisp('torque_hp_crossover_note', crossNote);
          setDisp('foot_pounds_work', Math.round(workSec).toLocaleString() + ' ft-lb / sec');
        """
    },
    {
        "slug": "quarter-mile-speed",
        "category": "physics",
        "name": "Quarter-Mile Elapsed Time (ET) & Trap Speed Calculator",
        "description": "Calculate drag racing 1/4 mile elapsed time (ET) and finish trap speed from vehicle curb weight and wheel horsepower using the iconic Hale and Fox formulas.",
        "hero_badge": "Motorsports Dynamics • 1/4 Mile ET Matrix",
        "formula_display": "ET = 5.825 × ∛(Weight / Horsepower) | Trap Speed = 234 × ∛(Horsepower / Weight)",
        "fields": [
            {"id": "curb_weight_race_lbs", "label": "Total Race Weight (Car + Driver)", "default": 3400, "suffix": "lbs", "min": 1000, "max": 8000, "step": 50, "hint": "Vehicle weight on track scales with driver in seat"},
            {"id": "flywheel_horsepower", "label": "Flywheel Horsepower (BHP)", "default": 450, "suffix": "HP", "min": 50, "max": 3500, "step": 10, "hint": "Engine horsepower at crank"},
            {"id": "drivetrain_layout", "label": "Drivetrain Loss Factor (0.85 RWD/FWD, 0.80 AWD)", "default": 0.85, "min": 0.70, "max": 0.95, "step": 0.05, "hint": "Wheel horsepower transfer efficiency"}
        ],
        "metrics": [
            {"id": "quarter_mile_et", "label": "Estimated 1/4 Mile Elapsed Time (ET)", "default_display": "11.75 sec", "highlight": True},
            {"id": "trap_speed_mph", "label": "Quarter-Mile Trap Speed", "default_display": "116.8 MPH", "highlight": True},
            {"id": "wheel_horsepower", "label": "Effective Wheel Horsepower (WHP)", "default_display": "382.5 WHP"},
            {"id": "power_to_weight", "label": "Power-to-Weight Ratio", "default_display": "7.56 lbs / HP"}
        ],
        "proof_steps": [
            {"step_title": "Wheel Horsepower Derivation", "step_text": "WHP = Crank HP × Drivetrain Transfer Efficiency (manual RWD: 15% loss; AWD: 20-22% loss)."},
            {"step_title": "Hale and Fox Empirical Dynamic Laws", "step_text": "Elapsed Time ET = 5.825 × (Weight / HP)^(1/3). Trap Speed = 234 × (HP / Weight)^(1/3)."},
            {"step_title": "Tire Traction and 60-Foot Sensitivity", "step_text": "These formulas assume optimal launch traction on a prepped NHRA drag strip surface. Street tires on unprepped asphalt typically add 0.3 to 0.6 seconds to ET."}
        ],
        "faqs": [
            {"q": "How accurate are drag racing quarter-mile formulas?", "a": "The Fox and Hale formulas are remarkably accurate (typically within ±0.2 seconds) for typical passenger and sports cars with competent drivers on drag radial or slick tires."},
            {"q": "Why does reducing vehicle weight lower ET faster than adding power?", "a": "Reducing weight improves every phase of vehicle physics simultaneously: launch grip, 60-foot sprint, braking, and rotational tire acceleration without adding heat or drivetrain stress."}
        ],
        "js_logic": """
          const wt = getNum('curb_weight_race_lbs');
          const crankHp = getNum('flywheel_horsepower');
          const eff = getNum('drivetrain_layout') || 0.85;

          const whp = crankHp * eff;
          const ratio = wt / crankHp;

          const et = 5.825 * Math.cbrt(ratio);
          const trap = 234 * Math.cbrt(crankHp / wt);

          setDisp('quarter_mile_et', et.toFixed(2) + ' sec');
          setDisp('trap_speed_mph', trap.toFixed(1) + ' MPH');
          setDisp('wheel_horsepower', whp.toFixed(1) + ' WHP');
          setDisp('power_to_weight', ratio.toFixed(2) + ' lbs / HP');
        """
    },
    {
        "slug": "engine-displacement",
        "category": "physics",
        "name": "Engine Displacement & Cylinder Volume Calculator",
        "description": "Calculate total internal combustion engine displacement in Cubic Centimeters (cc), Liters (L), and Cubic Inches (CID) from bore, stroke, and cylinder count.",
        "hero_badge": "Engine Building • Displacement Geometry",
        "formula_display": "Displacement = π × (Bore / 2)² × Stroke × Cylinders",
        "fields": [
            {"id": "cylinder_bore_mm", "label": "Cylinder Bore Diameter (mm)", "default": 86.0, "suffix": "mm", "min": 40.0, "max": 150.0, "step": 0.5, "hint": "Internal diameter of cylinder bore"},
            {"id": "piston_stroke_mm", "label": "Piston Stroke Length (mm)", "default": 86.0, "suffix": "mm", "min": 40.0, "max": 150.0, "step": 0.5, "hint": "Crankshaft throw travel distance"},
            {"id": "number_of_cylinders", "label": "Number of Cylinders", "default": 4, "min": 1, "max": 16, "step": 1, "hint": "e.g. 4 (Inline-4), 6 (V6), 8 (V8)"}
        ],
        "metrics": [
            {"id": "displacement_cc", "label": "Engine Displacement (cc)", "default_display": "1,998 cc", "highlight": True},
            {"id": "displacement_liters", "label": "Engine Displacement (Liters)", "default_display": "2.0 Liters", "highlight": True},
            {"id": "displacement_cid", "label": "Cubic Inches (CID)", "default_display": "121.9 CID", "highlight": True},
            {"id": "bore_stroke_ratio", "label": "Bore-to-Stroke Ratio Profile", "default_display": "1.00 (Square Engine)"}
        ],
        "proof_steps": [
            {"step_title": "Cylinder Swept Volume Geometry", "step_text": "Swept Volume V_cyl = π × r² × h = π × (Bore / 2)² × Stroke."},
            {"step_title": "Total Multi-Cylinder Displacement", "step_text": "Total Displacement = V_cyl × Number of Cylinders. Convert mm³ to cm³ (cc) by dividing by 1,000."},
            {"step_title": "Bore / Stroke Mechanical Classification", "step_text": "Bore / Stroke > 1.0 = Over-square (high-revving racing engines); = 1.0 = Square engine (balanced torque/revs); < 1.0 = Under-square (long-stroke low-end diesel torque)."}
        ],
        "faqs": [
            {"q": "What is the difference between a square and over-square engine?", "a": "An over-square engine has a bore larger than its stroke, permitting larger intake valves and higher safe redline RPMs (e.g. Ferrari, Formula 1). An under-square engine has a longer stroke, favoring low-RPM torque for towing and trucks."},
            {"q": "How do you convert cc to cubic inches?", "a": "Multiply cubic centimeters by 0.0610237, or divide by 16.387. For example: 5,000 cc × 0.0610237 = 305 CID (Chevy 305)."}
        ],
        "js_logic": """
          const bore = getNum('cylinder_bore_mm');
          const stroke = getNum('piston_stroke_mm');
          const cyl = getNum('number_of_cylinders') || 4;

          const singleVolMm3 = Math.PI * Math.pow(bore / 2, 2) * stroke;
          const totalCc = (singleVolMm3 * cyl) / 1000;
          const liters = totalCc / 1000;
          const cid = totalCc * 0.0610237441;
          const bsRatio = bore / stroke;

          let bsClass = 'Square Engine (Bore == Stroke)';
          if (bsRatio > 1.05) bsClass = bsRatio.toFixed(2) + ' (Over-Square / High-Revving)';
          else if (bsRatio < 0.95) bsClass = bsRatio.toFixed(2) + ' (Under-Square / Long-Stroke Torque)';

          setDisp('displacement_cc', Math.round(totalCc).toLocaleString() + ' cc');
          setDisp('displacement_liters', liters.toFixed(1) + ' Liters (' + liters.toFixed(3) + 'L)');
          setDisp('displacement_cid', cid.toFixed(1) + ' CID');
          setDisp('bore_stroke_ratio', bsClass);
        """
    },
    {
        "slug": "compression-ratio",
        "category": "physics",
        "name": "Engine Static Compression Ratio Calculator",
        "description": "Calculate static compression ratio (CR) from cylinder swept volume, combustion chamber cc, head gasket thickness/bore, and piston dome/dish volume.",
        "hero_badge": "Combustion Engineering • Static CR Matrix",
        "formula_display": "Compression Ratio = (Swept Volume + Clearance Volume) / Clearance Volume",
        "fields": [
            {"id": "cyl_swept_vol_cc", "label": "Cylinder Swept Volume (cc)", "default": 500, "suffix": "cc", "min": 50, "max": 2000, "step": 10, "hint": "Single cylinder displacement in cc"},
            {"id": "chamber_cc", "label": "Cylinder Head Chamber Volume (cc)", "default": 58, "suffix": "cc", "min": 20, "max": 150, "step": 1, "hint": "Measured combustion chamber volume"},
            {"id": "gasket_cc", "label": "Compressed Head Gasket Volume (cc)", "default": 6.5, "suffix": "cc", "min": 1, "max": 25, "step": 0.5, "hint": "Volume occupied by head gasket bore/thickness"},
            {"id": "piston_net_cc", "label": "Piston Dome (+) or Dish/Deck (-) Volume (cc)", "default": -4.0, "suffix": "cc", "min": -50, "max": 50, "step": 0.5, "hint": "Dish adds volume (-); dome reduces clearance (+)"}
        ],
        "metrics": [
            {"id": "static_cr_result", "label": "Static Compression Ratio", "default_display": "9.27 : 1.0", "highlight": True},
            {"id": "total_clearance_vol", "label": "Total Clearance Volume", "default_display": "60.50 cc", "highlight": True},
            {"id": "octane_guidance", "label": "Recommended Fuel Octane", "default_display": "Regular 87 AKI Unleaded", "highlight": True},
            {"id": "total_cylinder_volume", "label": "Total BDC Volume", "default_display": "560.50 cc"}
        ],
        "proof_steps": [
            {"step_title": "Clearance Volume Consolidation", "step_text": "Clearance Volume V_clear = Chamber Volume + Gasket Volume + Piston-to-Deck Volume - Piston Dome Volume (+ Dish Volume)."},
            {"step_title": "Compression Ratio Definition", "step_text": "CR = (Swept Volume + Clearance Volume) / Clearance Volume. Measures gas volumetric compression from Bottom Dead Center (BDC) to Top Dead Center (TDC)."},
            {"step_title": "Knock and Octane Thresholds", "step_text": "Naturally aspirated engines with CR > 10.5:1 require premium 91-93 octane fuel to prevent destructive pre-ignition knock (detonation)."}
        ],
        "faqs": [
            {"q": "What is the difference between static and dynamic compression ratio?", "a": "Static CR is purely geometric based on piston travel from bottom to top dead center. Dynamic CR accounts for the intake valve closing (IVC) point, calculating compression only after the intake valve fully seals."},
            {"q": "Can you lower compression ratio with a thicker head gasket?", "a": "Yes! Adding a thicker head gasket increases clearance volume, effectively lowering the compression ratio, which is a common technique when adding a turbocharger to a high-compression engine."}
        ],
        "js_logic": """
          const swept = getNum('cyl_swept_vol_cc');
          const chamber = getNum('chamber_cc');
          const gasket = getNum('gasket_cc');
          const piston = getNum('piston_net_cc');

          const clearance = chamber + gasket - piston;
          const cr = clearance > 0 ? ((swept + clearance) / clearance) : 0;
          const totalBdc = swept + clearance;

          let octane = 'Regular 87 AKI Unleaded';
          if (cr > 11.5) octane = 'Race Gas (100+ AKI) / E85';
          else if (cr >= 10.5) octane = 'Premium 93 AKI Unleaded';
          else if (cr >= 9.5) octane = 'Mid-Grade 89-91 AKI Unleaded';

          setDisp('static_cr_result', cr.toFixed(2) + ' : 1.0');
          setDisp('total_clearance_vol', clearance.toFixed(2) + ' cc');
          setDisp('octane_guidance', octane);
          setDisp('total_cylinder_volume', totalBdc.toFixed(2) + ' cc');
        """
    },
    {
        "slug": "gear-ratio-speed",
        "category": "physics",
        "name": "Transmission Gear Ratio & Vehicle Speed at RPM Calculator",
        "description": "Calculate vehicle road speed (MPH / km/h) at any engine RPM for each transmission gear, axle final drive ratio, and tire diameter.",
        "hero_badge": "Drivetrain Kinematics • Gear Speed Matrix",
        "formula_display": "Speed (MPH) = (Engine RPM × Tire Diameter in inches) / (Trans Ratio × Axle Ratio × 336)",
        "fields": [
            {"id": "engine_rpm_cruise", "label": "Engine Speed (RPM)", "default": 2500, "suffix": "RPM", "min": 800, "max": 10000, "step": 100, "hint": "Target highway cruising RPM"},
            {"id": "trans_gear_ratio", "label": "Transmission Gear Ratio", "default": 0.68, "min": 0.40, "max": 6.00, "step": 0.01, "hint": "Top overdrive gear (e.g. 0.68:1)"},
            {"id": "axle_final_drive", "label": "Differential Axle Ratio", "default": 3.73, "min": 2.00, "max": 6.50, "step": 0.05, "hint": "Differential ring & pinion ratio"},
            {"id": "tire_diameter_inches", "label": "Tire Overall Diameter (inches)", "default": 28.5, "suffix": "in", "min": 18.0, "max": 45.0, "step": 0.5, "hint": "Outer tire diameter in inches"}
        ],
        "metrics": [
            {"id": "vehicle_speed_mph", "label": "Vehicle Road Speed (MPH)", "default_display": "83.6 MPH", "highlight": True},
            {"id": "vehicle_speed_kmh", "label": "Vehicle Road Speed (km/h)", "default_display": "134.5 km/h", "highlight": True},
            {"id": "overall_drivetrain_ratio", "label": "Total Overall Gear Reduction", "default_display": "2.54 : 1.0"},
            {"id": "driveshaft_rpm", "label": "Driveshaft Rotational Speed", "default_display": "3,676 RPM"}
        ],
        "proof_steps": [
            {"step_title": "Total Drivetrain Ratio", "step_text": "Overall Gear Ratio R_total = Transmission Ratio × Axle Final Drive Ratio. For example: 0.68 × 3.73 = 2.536:1."},
            {"step_title": "Wheel Rotational Frequency", "step_text": "Wheel RPM = Engine RPM / R_total."},
            {"step_title": "Road Linear Velocity Constant", "step_text": "Speed MPH = (Wheel RPM × π × Diameter × 60) / 63,360 = (Engine RPM × Diameter) / (R_total × 336.135)."}
        ],
        "faqs": [
            {"q": "Where does the 336 constant come from in the gear ratio formula?", "a": "The constant derives from converting units: 1 mile = 63,360 inches, 1 hour = 60 minutes, and circumference = π × D: 63,360 / (60 × π) = 336.135."},
            {"q": "How does changing axle gear ratio from 3.23 to 4.10 affect cruising RPM?", "a": "Installing shorter (numerically higher) 4.10 gears increases wheel torque and acceleration by ~27%, but raises highway engine RPM at any given speed by 27%, increasing cabin drone and fuel consumption."}
        ],
        "js_logic": """
          const rpm = getNum('engine_rpm_cruise');
          const trans = getNum('trans_gear_ratio') || 1;
          const axle = getNum('axle_final_drive') || 1;
          const diam = getNum('tire_diameter_inches');

          const totalRatio = trans * axle;
          const mph = totalRatio > 0 ? ((rpm * diam) / (totalRatio * 336.1355)) : 0;
          const kmh = mph * 1.609344;
          const driveshaftRpm = trans > 0 ? (rpm / trans) : 0;

          setDisp('vehicle_speed_mph', mph.toFixed(1) + ' MPH');
          setDisp('vehicle_speed_kmh', kmh.toFixed(1) + ' km/h');
          setDisp('overall_drivetrain_ratio', totalRatio.toFixed(2) + ' : 1.0');
          setDisp('driveshaft_rpm', Math.round(driveshaftRpm).toLocaleString() + ' RPM');
        """
    },
    {
        "slug": "boat-fuel-burn",
        "category": "physics",
        "name": "Marine Boat Fuel Burn & Range Calculator",
        "description": "Calculate marine boat fuel burn rate in Gallons Per Hour (GPH), cruising range in nautical miles (NM), and fuel costs with safe reserves.",
        "hero_badge": "Marine Engineering • Boat Fuel Matrix",
        "formula_display": "Cruising Range (NM) = Usable Fuel (Gallons) × (Speed in Knots / GPH)",
        "fields": [
            {"id": "cruise_speed_knots", "label": "Cruising Speed (Knots)", "default": 24, "suffix": "knots", "min": 4, "max": 65, "step": 1, "hint": "Cruising speed in nautical knots"},
            {"id": "fuel_burn_gph", "label": "Combined Fuel Burn (GPH)", "default": 18, "suffix": "GPH", "min": 0.5, "max": 150, "step": 0.5, "hint": "Total gallons per hour at cruising RPM"},
            {"id": "fuel_tank_capacity", "label": "Total Fuel Tank Capacity", "default": 120, "suffix": "gallons", "min": 10, "max": 2000, "step": 10, "hint": "Full fuel capacity"},
            {"id": "fuel_price_marina", "label": "Marina Fuel Price per Gallon", "default": 4.85, "prefix": "$", "min": 2.50, "max": 10.00, "step": 0.10, "hint": "Marina dockside fuel rate"}
        ],
        "metrics": [
            {"id": "safe_cruising_range", "label": "Safe Cruising Range (10% Reserve)", "default_display": "144.0 NM", "highlight": True},
            {"id": "statute_miles_range", "label": "Range in Statute Miles", "default_display": "165.7 Miles", "highlight": True},
            {"id": "fuel_economy_nmpg", "label": "Marine Fuel Economy (NMPG)", "default_display": "1.33 NM / gal"},
            {"id": "hourly_boating_cost", "label": "Operating Fuel Cost per Hour", "default_display": "$87.30 / hr"}
        ],
        "proof_steps": [
            {"step_title": "Marine Fuel Efficiency NMPG", "step_text": "Nautical Miles per Gallon NMPG = Speed (Knots) / Fuel Burn (GPH). For example: 24 knots / 18 GPH = 1.33 NMPG."},
            {"step_title": "Coast Guard 10% Reserve Rule", "step_text": "Mariners must maintain at least a 10% (daytime coastal) to 33% (offshore passage) fuel safety reserve: Usable Fuel = Tank Capacity × 0.90."},
            {"step_title": "Safe Range Formulation", "step_text": "Safe Range (NM) = Usable Gallons × NMPG. Converting to Statute Miles: Statute Miles = NM × 1.15078."}
        ],
        "faqs": [
            {"q": "What is the Rule of Thirds in marine fuel planning?", "a": "The offshore Rule of Thirds states: 1/3 of fuel for the trip out, 1/3 for the return voyage, and 1/3 held in reserve for unexpected headwinds, heavy seas, or navigation diversions."},
            {"q": "How does boat hull type affect fuel burn?", "a": "Planing hulls burn substantial fuel while climbing over their bow wave, achieving maximum efficiency once fully up on plane. Displacement hulls have low drag at low speeds, but encounter an impenetrable hull speed barrier where fuel burn spikes exponentially."}
        ],
        "js_logic": """
          const kts = getNum('cruise_speed_knots');
          const gph = getNum('fuel_burn_gph') || 1;
          const tank = getNum('fuel_tank_capacity');
          const price = getNum('fuel_price_marina');

          const nmpg = kts / gph;
          const usable = tank * 0.90;
          const rangeNm = usable * nmpg;
          const rangeMiles = rangeNm * 1.150779;
          const costHr = gph * price;

          setDisp('safe_cruising_range', rangeNm.toFixed(1) + ' NM');
          setDisp('statute_miles_range', rangeMiles.toFixed(1) + ' Miles');
          setDisp('fuel_economy_nmpg', nmpg.toFixed(2) + ' NM / gal');
          setDisp('hourly_boating_cost', '$' + costHr.toFixed(2) + ' / hr');
        """
    },
    {
        "slug": "aviation-crosswind",
        "category": "physics",
        "name": "Aviation Crosswind & Headwind Component Calculator",
        "description": "Calculate exact runway crosswind component and headwind/tailwind component from wind speed, wind direction, and magnetic runway heading.",
        "hero_badge": "Flight Operations • Crosswind Component Matrix",
        "formula_display": "Crosswind = Wind Speed × sin(Wind Angle - Runway Heading) | Headwind = Wind Speed × cos(Wind Angle - Runway Heading)",
        "fields": [
            {"id": "runway_heading_deg", "label": "Runway Magnetic Heading (°)", "default": 270, "suffix": "°", "min": 10, "max": 360, "step": 10, "hint": "e.g. Runway 27 = 270°"},
            {"id": "wind_direction_deg", "label": "Wind Direction from ATC / METAR (°)", "default": 310, "suffix": "°", "min": 1, "max": 360, "step": 5, "hint": "Direction wind is blowing FROM"},
            {"id": "wind_speed_knots", "label": "Wind Speed (Knots)", "default": 18, "suffix": "knots", "min": 1, "max": 80, "step": 1, "hint": "Sustained wind velocity in knots"}
        ],
        "metrics": [
            {"id": "crosswind_component", "label": "Crosswind Component", "default_display": "11.6 knots (Right Crosswind)", "highlight": True},
            {"id": "headwind_component", "label": "Headwind Component", "default_display": "13.8 knots (Headwind)", "highlight": True},
            {"id": "wind_angle_delta", "label": "Relative Wind Angle", "default_display": "40° off runway heading"},
            {"id": "crosswind_safety", "label": "Cessna 172 Max Demonstrated Limit (15 kts)", "default_display": "Within Demonstrated Limits (11.6 < 15 kts)"}
        ],
        "proof_steps": [
            {"step_title": "Relative Angular Delta", "step_text": "Angular Offset θ = |Wind Direction - Runway Heading|."},
            {"step_title": "Trigonometric Vector Decomposition", "step_text": "Crosswind = Wind Speed × sin(θ). Headwind = Wind Speed × cos(θ)."},
            {"step_title": "Tailwind Safety Hazard", "step_text": "If θ > 90°, cos(θ) becomes negative, representing a dangerous tailwind that dramatically increases landing rollout distance and stall risk."}
        ],
        "faqs": [
            {"q": "What is the difference between maximum demonstrated crosswind and an operating limitation?", "a": "For FAA Part 23 general aviation aircraft, maximum demonstrated crosswind is not an airworthiness limitation; it is simply the maximum crosswind tested by the factory test pilot during certification. However, exceeding it during an accident invites FAA negligence enforcement."},
            {"q": "How do pilots correct for crosswinds on landing?", "a": "Pilots utilize either the crab technique (heading pointed into wind until flare) or the wing-low slip technique (aileron into wind to prevent drift, opposite rudder to align fuselage with runway centerline)."}
        ],
        "js_logic": """
          const rwy = getNum('runway_heading_deg');
          const windDir = getNum('wind_direction_deg');
          const speed = getNum('wind_speed_knots');

          let diff = (windDir - rwy) % 360;
          if (diff > 180) diff -= 360;
          if (diff < -180) diff += 360;

          const rad = Math.abs(diff) * (Math.PI / 180);
          const cross = speed * Math.sin(rad);
          const head = speed * Math.cos(diff * (Math.PI / 180));

          const side = diff >= 0 ? 'Right Crosswind' : 'Left Crosswind';
          const headType = head >= 0 ? 'Headwind' : 'TAILWIND (Caution)';

          setDisp('crosswind_component', cross.toFixed(1) + ' knots (' + side + ')');
          setDisp('headwind_component', Math.abs(head).toFixed(1) + ' knots (' + headType + ')');
          setDisp('wind_angle_delta', Math.abs(diff).toFixed(0) + '° off runway heading');
          setDisp('crosswind_safety', cross <= 15 ? 'Within Demonstrated Limits (' + cross.toFixed(1) + ' < 15 kts)' : 'EXCEEDS Standard 15 kt GA Limit');
        """
    },
    {
        "slug": "aircraft-climb-rate",
        "category": "physics",
        "name": "Aircraft Rate of Climb & Climb Gradient Calculator",
        "description": "Convert between Vertical Speed Rate of Climb (Feet Per Minute - FPM) and Climb Gradient in feet per nautical mile (ft/NM) and percent slope.",
        "hero_badge": "Aviation Engineering • Climb Gradient Matrix",
        "formula_display": "Climb Gradient (ft/NM) = (FPM × 60) / Groundspeed (Knots) | Gradient % = ft/NM / 60.76",
        "fields": [
            {"id": "climb_rate_fpm", "label": "Vertical Speed (Rate of Climb)", "default": 850, "suffix": "FPM", "min": 100, "max": 10000, "step": 50, "hint": "Feet per minute on vertical speed indicator (VSI)"},
            {"id": "groundspeed_knots", "label": "Groundspeed during Climb (Knots)", "default": 110, "suffix": "knots", "min": 40, "max": 500, "step": 5, "hint": "Aircraft speed over ground (accounting for wind)"}
        ],
        "metrics": [
            {"id": "climb_gradient_ft_nm", "label": "Climb Gradient (ft / NM)", "default_display": "463.6 ft / NM", "highlight": True},
            {"id": "climb_gradient_pct", "label": "Climb Gradient Percentage (%)", "default_display": "7.63% slope", "highlight": True},
            {"id": "standard_departure_status", "label": "FAA Standard Departure Clearance (200 ft/NM)", "default_display": "Passes Standard (463.6 > 200 ft/NM)", "highlight": True},
            {"id": "time_to_10k_feet", "label": "Time to Climb 10,000 Feet", "default_display": "11.8 minutes"}
        ],
        "proof_steps": [
            {"step_title": "Kinematic Motion Across Ground", "step_text": "One nautical mile equals 6,076.12 feet. At groundspeed GS knots, an aircraft travels GS / 60 nautical miles per minute."},
            {"step_title": "Climb Gradient Formulation", "step_text": "Gradient (ft/NM) = Vertical Speed (FPM) / Nautical Miles per Minute = (FPM × 60) / GS."},
            {"step_title": "Obstacle Clearance Standard", "step_text": "Standard instrument departure procedures (TERPS) mandate a minimum climb gradient of 200 ft/NM (3.3%) to ensure obstacle clearance."}
        ],
        "faqs": [
            {"q": "Why does a headwind increase your climb gradient?", "a": "A headwind reduces your groundspeed without changing your aerodynamic rate of climb (FPM). Since you are moving forward across the ground more slowly, you gain more altitude per nautical mile, clearing runway obstacles more easily."},
            {"q": "What is the standard FAA climb gradient?", "a": "Unless published otherwise, the standard FAA climb gradient is 200 feet per nautical mile (approximately 3.3% gradient)."}
        ],
        "js_logic": """
          const fpm = getNum('climb_rate_fpm');
          const gs = getNum('groundspeed_knots') || 1;

          const ftNm = (fpm * 60) / gs;
          const pct = ftNm / 60.7612;
          const timeTo10k = 10000 / fpm;

          setDisp('climb_gradient_ft_nm', ftNm.toFixed(1) + ' ft / NM');
          setDisp('climb_gradient_pct', pct.toFixed(2) + '% slope');
          setDisp('standard_departure_status', ftNm >= 200 ? 'Passes Standard (' + ftNm.toFixed(1) + ' > 200 ft/NM)' : 'WARNING: Below 200 ft/NM TERPS Minimum');
          setDisp('time_to_10k_feet', timeTo10k.toFixed(1) + ' minutes');
        """
    },
    {
        "slug": "battery-amp-hours",
        "category": "physics",
        "name": "RV & Marine Battery Amp Hour & Inverter Runtime Calculator",
        "description": "Calculate deep cycle battery runtime in hours from total appliance AC watt load, battery voltage, amp hour capacity, and depth of discharge (DoD).",
        "hero_badge": "Off-Grid Power • Battery Capacity Matrix",
        "formula_display": "Runtime (Hours) = (Battery Volts × Amp Hours × DoD %) / (Inverter Load Watts / Inverter Efficiency)",
        "fields": [
            {"id": "battery_voltage", "label": "Battery System Nominal Voltage", "default": 12, "suffix": "V", "min": 12, "max": 48, "step": 12, "hint": "12V, 24V, or 48V battery bank"},
            {"id": "battery_capacity_ah", "label": "Battery Bank Capacity (Amp Hours)", "default": 200, "suffix": "Ah", "min": 20, "max": 2000, "step": 20, "hint": "Total battery Ah rating"},
            {"id": "dod_allowable_pct", "label": "Safe Depth of Discharge (DoD %)", "default": 80, "suffix": "%", "min": 30, "max": 95, "step": 5, "hint": "Lead-acid/AGM = 50%, Lithium LiFePO4 = 80-90%"},
            {"id": "appliance_load_watts", "label": "Continuous AC Appliance Load", "default": 350, "suffix": "Watts", "min": 10, "max": 5000, "step": 25, "hint": "Fridge, laptop, TV, microwave combined"}
        ],
        "metrics": [
            {"id": "battery_runtime_hours", "label": "Estimated Battery Runtime", "default_display": "4.9 hours", "highlight": True},
            {"id": "usable_watt_hours", "label": "Usable Energy Storage", "default_display": "1,920 Wh (1.92 kWh)", "highlight": True},
            {"id": "dc_current_draw", "label": "DC Battery Current Draw", "default_display": "34.3 Amps", "highlight": True},
            {"id": "chemistry_guidance", "label": "Battery Chemistry Recommendation", "default_display": "Lithium LiFePO4 (80% Safe DoD)"}
        ],
        "proof_steps": [
            {"step_title": "Total Stored Energy", "step_text": "Watt-Hours Wh = Voltage × Amp-Hours. For a 12V 200Ah bank: 12 × 200 = 2,400 Wh."},
            {"step_title": "Depth of Discharge and Usable Energy", "step_text": "Usable Energy = Total Wh × (DoD% / 100). Lead-acid batteries degrade rapidly if discharged past 50%; LiFePO4 lithium batteries can be discharged to 85-90%."},
            {"step_title": "Inverter Inefficiency Loss", "step_text": "DC-to-AC inverters have 85-90% conversion efficiency: Real DC Load = AC Load / 0.88. Runtime = Usable Wh / Real DC Load."}
        ],
        "faqs": [
            {"q": "Why should lead-acid batteries not be discharged below 50%?", "a": "Discharging lead-acid (flooded or AGM) batteries past 50% causes irreversible lead-sulfate crystallization on the plates, slashing battery lifespan from 1,000 cycles down to under 250 cycles."},
            {"q": "What size inverter do I need for a 1,000-watt appliance?", "a": "Choose an inverter rated for at least 1,200 to 1,500 watts continuous to handle startup surge spikes and maintain cool operating temperatures."}
        ],
        "js_logic": """
          const volts = getNum('battery_voltage');
          const ah = getNum('battery_capacity_ah');
          const dod = (getNum('dod_allowable_pct') || 80) / 100;
          const watts = getNum('appliance_load_watts') || 1;

          const totalWh = volts * ah;
          const usableWh = totalWh * dod;
          const inverterEff = 0.88;
          const dcLoad = watts / inverterEff;
          const hours = dcLoad > 0 ? (usableWh / dcLoad) : 0;
          const dcAmps = dcLoad / volts;

          setDisp('battery_runtime_hours', hours.toFixed(1) + ' hours (' + (hours * 60).toFixed(0) + ' min)');
          setDisp('usable_watt_hours', Math.round(usableWh).toLocaleString() + ' Wh (' + (usableWh / 1000).toFixed(2) + ' kWh)');
          setDisp('dc_current_draw', dcAmps.toFixed(1) + ' Amps');
          setDisp('chemistry_guidance', dod > 0.6 ? 'Lithium LiFePO4 (' + (dod*100).toFixed(0) + '% Safe DoD)' : 'Lead-Acid / AGM (50% Safe DoD)');
        """
    },
    {
        "slug": "car-wrap-vinyl",
        "category": "physics",
        "name": "Vehicle Vinyl Wrap Material & Roll Calculator",
        "description": "Calculate exact linear feet and square feet of vinyl wrap film required for full vehicle wraps, accounting for bumpers, roof, and 20% waste margin.",
        "hero_badge": "Automotive Aesthetics • Vinyl Film Roll Matrix",
        "formula_display": "Roll Length (Feet) = [(Vehicle Length × 3) + Roof + Bumpers] × 1.20 Waste Factor",
        "fields": [
            {"id": "vehicle_length_inches", "label": "Vehicle Bumper-to-Bumper Length (in)", "default": 195, "suffix": "in", "min": 100, "max": 300, "step": 5, "hint": "Midsize sedan ≈ 190 in, Full-size truck ≈ 230 in"},
            {"id": "roll_width_inches", "label": "Vinyl Wrap Roll Width (Standard 60 in)", "default": 60, "suffix": "in", "min": 48, "max": 72, "step": 6, "hint": "Industry standard 3M / Avery roll width = 60 inches"},
            {"id": "vehicle_body_type", "label": "Body Style Category (1.0 Coupe, 1.15 Sedan, 1.30 SUV/Truck)", "default": 1.15, "min": 0.8, "max": 2.0, "step": 0.05, "hint": "Surface area complexity multiplier"}
        ],
        "metrics": [
            {"id": "recommended_roll_length", "label": "Recommended Vinyl Roll Length", "default_display": "58.0 linear feet", "highlight": True},
            {"id": "total_wrap_area_sqft", "label": "Total Surface Area to Cover", "default_display": "290 sq ft", "highlight": True},
            {"id": "standard_box_purchase", "label": "Industry Box Order Size", "default_display": "Buy 60' × 5' Roll (300 sq ft Box)", "highlight": True},
            {"id": "estimated_material_cost", "label": "Estimated Film Material Cost ($750)", "default_display": "~$650 - $850 (Premium Cast Vinyl)"}
        ],
        "proof_steps": [
            {"step_title": "The 3x Length Wrap Heuristic", "step_text": "Professional wrap installers estimate base coverage using the Rule of Three: (Length × 3) covers left side, right side, and top horizontal hood/roof/trunk surfaces."},
            {"step_title": "Waste and Complex Curve Overhead", "step_text": "Bumpers, mirrors, door handles, and deep recesses require stretching margins, adding 20% material buffer."},
            {"step_title": "Roll Sizing Conversion", "step_text": "Rolls are sold in 60-inch (5-foot) widths. A 5-foot × 60-foot roll provides 300 square feet, which accommodates 95% of standard cars."}
        ],
        "faqs": [
            {"q": "What size roll of vinyl wrap do I need for a full car wrap?", "a": "For compacts and sports coupes, a 50-foot × 5-foot roll is usually sufficient. For mid-size sedans and crossovers, buy a 60-foot × 5-foot roll (300 sq ft). Full-size trucks and large SUVs require 75 feet."},
            {"q": "What is the difference between Cast and Calendered vinyl?", "a": "Always use Cast vinyl (3M 2080, Avery Dennison SW900) for vehicles! Cast vinyl has no memory and will not shrink, peel, or pop out of deep body contours like cheap calendered film."}
        ],
        "js_logic": """
          const lengthIn = getNum('vehicle_length_inches');
          const widthIn = getNum('roll_width_inches') || 60;
          const bodyMult = getNum('vehicle_body_type') || 1.15;

          const lengthFt = lengthIn / 12;
          const linearFt = (lengthFt * 3.2 * bodyMult);
          const rollFt = Math.ceil(linearFt / 5) * 5;
          const sqFt = rollFt * (widthIn / 12);

          let box = "Buy 50' × 5' Roll (250 sq ft Box)";
          if (rollFt > 65) box = "Buy 75' × 5' Roll (375 sq ft Box)";
          else if (rollFt > 50) box = "Buy 60' × 5' Roll (300 sq ft Box)";

          setDisp('recommended_roll_length', linearFt.toFixed(1) + ' linear feet');
          setDisp('total_wrap_area_sqft', Math.round(sqFt) + ' sq ft');
          setDisp('standard_box_purchase', box);
          setDisp('estimated_material_cost', '~$' + Math.round(sqFt * 2.50).toLocaleString() + ' - $' + Math.round(sqFt * 3.20).toLocaleString() + ' (Premium Cast Vinyl)');
        """
    },
    {
        "slug": "brake-stopping-distance",
        "category": "physics",
        "name": "Vehicle Braking & Stopping Distance Physics Calculator",
        "description": "Calculate total stopping distance in feet from initial speed, driver perception-reaction time, and road friction coefficient (dry, wet, snow, ice).",
        "hero_badge": "Accident Reconstruction • Braking Distance Matrix",
        "formula_display": "Stopping Distance = (Speed × Reaction Time) + (Speed² / [2 × g × Friction Coefficient μ])",
        "fields": [
            {"id": "vehicle_speed_mph_brake", "label": "Initial Vehicle Speed (MPH)", "default": 65, "suffix": "MPH", "min": 10, "max": 160, "step": 5, "hint": "Speed prior to emergency braking"},
            {"id": "reaction_time_sec", "label": "Driver Perception-Reaction Time", "default": 1.5, "suffix": "seconds", "min": 0.5, "max": 4.0, "step": 0.1, "hint": "AASHTO standard reaction time: 1.5 - 2.5 sec"},
            {"id": "road_surface_friction", "label": "Road Surface Friction (0.80 Dry, 0.50 Wet, 0.20 Snow, 0.10 Ice)", "default": 0.80, "min": 0.05, "max": 1.10, "step": 0.05, "hint": "Coefficient of friction μ"}
        ],
        "metrics": [
            {"id": "total_stopping_distance", "label": "Total Stopping Distance", "default_display": "319.4 feet", "highlight": True},
            {"id": "reaction_distance_feet", "label": "Distance Traveled Before Brakes Applied", "default_display": "143.0 feet", "highlight": True},
            {"id": "pure_braking_distance", "label": "Pure Mechanical Braking Distance", "default_display": "176.4 feet", "highlight": True},
            {"id": "car_lengths_equivalent", "label": "Equivalent Car Lengths (15 ft/car)", "default_display": "21.3 Car Lengths"}
        ],
        "proof_steps": [
            {"step_title": "Driver Perception-Reaction Distance", "step_text": "Converting speed to feet per second: v (ft/s) = MPH × 1.46667. Reaction Distance d_react = v × Reaction Time."},
            {"step_title": "Kinetic Energy Dissipation Braking", "step_text": "Braking Distance d_brake = v² / (2 · g · μ), where g = 32.174 ft/s² and μ is the tire-to-road friction coefficient."},
            {"step_title": "Quadratic Velocity Scaling", "step_text": "Braking distance scales with the SQUARE of speed: doubling your speed quadruples your braking distance."}
        ],
        "faqs": [
            {"q": "Why is stopping distance so much longer on wet roads?", "a": "Wet asphalt drops tire friction coefficient μ from ~0.80 down to ~0.45, nearly doubling the mechanical braking distance. On packed snow (μ ≈ 0.20), stopping distance increases four-fold."},
            {"q": "What is the 3-second following distance rule?", "a": "At 65 MPH, you travel 95 feet every single second. A 3-second gap provides 285 feet of safety buffer, allowing enough space for perception, reaction, and smooth braking."}
        ],
        "js_logic": """
          const mph = getNum('vehicle_speed_mph_brake');
          const tReact = getNum('reaction_time_sec');
          const mu = getNum('road_surface_friction') || 0.8;

          const vFps = mph * 1.466667;
          const dReact = vFps * tReact;
          const g = 32.174;
          const dBrake = Math.pow(vFps, 2) / (2 * g * mu);
          const dTotal = dReact + dBrake;

          setDisp('total_stopping_distance', dTotal.toFixed(1) + ' feet');
          setDisp('reaction_distance_feet', dReact.toFixed(1) + ' feet');
          setDisp('pure_braking_distance', dBrake.toFixed(1) + ' feet');
          setDisp('car_lengths_equivalent', (dTotal / 15).toFixed(1) + ' Car Lengths');
        """
    },
    {
        "slug": "car-sales-tax",
        "category": "finance",
        "name": "Vehicle Sales Tax & Trade-In Credit Calculator",
        "description": "Calculate state, county, and local vehicle sales tax, registration fees, and tax credit savings from trading in an existing vehicle.",
        "hero_badge": "Automotive Tax • Trade-In Deduction Matrix",
        "formula_display": "Net Taxable Base = Purchase Price - Trade-In Value | Sales Tax = Net Taxable Base × Tax Rate %",
        "fields": [
            {"id": "purchase_price_tax", "label": "New Vehicle Purchase Price", "default": 42000, "prefix": "$", "min": 2000, "max": 250000, "step": 1000, "hint": "Agreed vehicle purchase price"},
            {"id": "trade_in_allowance", "label": "Trade-In Vehicle Allowance", "default": 14000, "prefix": "$", "min": 0, "max": 150000, "step": 500, "hint": "Dealer trade-in credit"},
            {"id": "state_sales_tax_pct", "label": "Combined State & County Sales Tax Rate", "default": 7.0, "suffix": "%", "min": 0.0, "max": 13.0, "step": 0.1, "hint": "Local vehicle sales tax rate"}
        ],
        "metrics": [
            {"id": "total_sales_tax_due", "label": "Vehicle Sales Tax Due", "default_display": "$1,960.00", "highlight": True},
            {"id": "trade_in_tax_savings", "label": "Sales Tax Saved from Trade-In", "default_display": "$980.00 Saved", "highlight": True},
            {"id": "net_taxable_amount", "label": "Net Taxable Amount", "default_display": "$28,000.00", "highlight": True},
            {"id": "total_out_the_door", "label": "Net Price After Tax & Trade", "default_display": "$29,960.00"}
        ],
        "proof_steps": [
            {"step_title": "State Trade-In Tax Credit Offset", "step_text": "In 43 out of 50 US states, sales tax is assessed only on the net difference: Taxable Base = Purchase Price - Trade-In Allowance."},
            {"step_title": "Direct Tax Calculation", "step_text": "Sales Tax = Taxable Base × (Tax Rate% / 100)."},
            {"step_title": "Trade-In Hidden Financial Bonus", "step_text": "Trading in a $14,000 car in a 7% tax state saves an extra $980 in cash sales tax, making a $14,000 trade-in effectively worth $14,980 compared to a private sale."}
        ],
        "faqs": [
            {"q": "Do all states allow a sales tax credit for vehicle trade-ins?", "a": "Most states do, but California, Hawaii, Kentucky, Maryland, Michigan, Montana, and Virginia do not allow full trade-in deductions or have specific state restrictions."},
            {"q": "Should I sell my car privately or trade it in to save tax?", "a": "If private sale market value exceeds dealer trade-in offer by more than the sales tax savings (e.g. more than 7-8%), private sale yields more cash even after paying full tax on the new vehicle."}
        ],
        "js_logic": """
          const price = getNum('purchase_price_tax');
          const trade = getNum('trade_in_allowance');
          const rate = (getNum('state_sales_tax_pct') || 7.0) / 100;

          const taxable = Math.max(0, price - trade);
          const tax = taxable * rate;
          const taxSaved = trade * rate;
          const otd = taxable + tax;

          setDisp('total_sales_tax_due', '$' + tax.toFixed(2));
          setDisp('trade_in_tax_savings', '$' + taxSaved.toFixed(2) + ' Saved');
          setDisp('net_taxable_amount', '$' + taxable.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('total_out_the_door', '$' + otd.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "auto-refinance-savings",
        "category": "finance",
        "name": "Auto Loan Refinance Savings Calculator",
        "description": "Calculate monthly payment reduction and lifetime interest savings from refinancing an auto loan to a lower APR interest rate.",
        "hero_badge": "Consumer Lending • Auto Loan Refinance Matrix",
        "formula_display": "Monthly Payment = P × [r(1+r)ⁿ] / [(1+r)ⁿ - 1] | Lifetime Savings = Current Remaining Payments - New Refinance Payments",
        "fields": [
            {"id": "loan_payoff_balance", "label": "Current Loan Payoff Balance", "default": 24000, "prefix": "$", "min": 2000, "max": 150000, "step": 500, "hint": "Principal payoff amount on current loan"},
            {"id": "remaining_months_old", "label": "Remaining Term (Months)", "default": 48, "suffix": "months", "min": 12, "max": 84, "step": 6, "hint": "Months left on current loan"},
            {"id": "current_loan_apr", "label": "Current Loan APR (%)", "default": 9.5, "suffix": "%", "min": 1.0, "max": 29.0, "step": 0.1, "hint": "Existing interest rate"},
            {"id": "new_refinance_apr", "label": "New Refinanced APR (%)", "default": 5.75, "suffix": "%", "min": 1.0, "max": 20.0, "step": 0.1, "hint": "Lower APR from credit union or online lender"}
        ],
        "metrics": [
            {"id": "total_lifetime_interest_saved", "label": "Total Lifetime Interest Saved", "default_display": "$2,080.00", "highlight": True},
            {"id": "monthly_payment_savings", "label": "Monthly Payment Reduction", "default_display": "$43.33 / mo", "highlight": True},
            {"id": "new_monthly_payment", "label": "New Lower Monthly Payment", "default_display": "$560.85 / mo"},
            {"id": "old_monthly_payment", "label": "Current Monthly Payment", "default_display": "$604.18 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Current Loan Cash Outflow", "step_text": "Monthly Payment M = P · [r(1+r)ⁿ] / [(1+r)ⁿ - 1]. Total Remaining Cash Outflow = M_old × n."},
            {"step_title": "Refinanced Amortization Schedule", "step_text": "Re-amortize current payoff balance P at new lower interest rate r_new across remaining term n."},
            {"step_title": "Pure Financial Arbitrage", "step_text": "Net Lifetime Savings = Total Old Payments - Total New Payments. Refinancing from 9.5% to 5.75% puts over $2,000 directly back into your pocket."}
        ],
        "faqs": [
            {"q": "When does it make sense to refinance an auto loan?", "a": "Refinancing makes sense if your credit score has improved by 50+ points since purchasing, if interest rates have dropped, or if you initially financed through a dealership with a high marked-up interest rate."},
            {"q": "Does auto refinancing hurt your credit score?", "a": "Applying triggers a minor hard inquiry (temporarily lowering credit by 3-5 points). All inquiries within a 14-45 day window count as a single inquiry under FICO rate-shopping rules."}
        ],
        "js_logic": """
          const p = getNum('loan_payoff_balance');
          const n = getNum('remaining_months_old') || 48;
          const rOld = ((getNum('current_loan_apr') || 9.5) / 100) / 12;
          const rNew = ((getNum('new_refinance_apr') || 5.75) / 100) / 12;

          const mOld = rOld > 0 ? (p * (rOld * Math.pow(1 + rOld, n)) / (Math.pow(1 + rOld, n) - 1)) : (p / n);
          const mNew = rNew > 0 ? (p * (rNew * Math.pow(1 + rNew, n)) / (Math.pow(1 + rNew, n) - 1)) : (p / n);

          const totalOld = mOld * n;
          const totalNew = mNew * n;
          const totalSavings = Math.max(0, totalOld - totalNew);
          const moSavings = Math.max(0, mOld - mNew);

          setDisp('total_lifetime_interest_saved', '$' + totalSavings.toFixed(2));
          setDisp('monthly_payment_savings', '$' + moSavings.toFixed(2) + ' / mo');
          setDisp('new_monthly_payment', '$' + mNew.toFixed(2) + ' / mo');
          setDisp('old_monthly_payment', '$' + mOld.toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "gap-insurance-need",
        "category": "finance",
        "name": "Auto GAP Insurance Need & Negative Equity Calculator",
        "description": "Calculate negative equity exposure ('underwater loan') comparing outstanding auto loan balance against actual cash value (ACV) after depreciation.",
        "hero_badge": "Risk Underwriting • GAP Insurance Matrix",
        "formula_display": "GAP Exposure = Outstanding Loan Balance - Vehicle Actual Cash Value (ACV)",
        "fields": [
            {"id": "current_loan_payoff", "label": "Outstanding Auto Loan Payoff", "default": 32000, "prefix": "$", "min": 2000, "max": 150000, "step": 500, "hint": "Current balance owed to bank or lender"},
            {"id": "market_value_acv", "label": "Vehicle Actual Cash Value (ACV / KBB)", "default": 25500, "prefix": "$", "min": 1000, "max": 150000, "step": 500, "hint": "Insurance total loss payout value"},
            {"id": "insurance_deductible", "label": "Insurance Comprehensive/Collision Deductible", "default": 500, "prefix": "$", "min": 0, "max": 2500, "step": 100, "hint": "Deductible owed on total loss claim"}
        ],
        "metrics": [
            {"id": "net_gap_exposure", "label": "Out-of-Pocket GAP Risk if Totaled", "default_display": "$7,000.00", "highlight": True},
            {"id": "equity_status", "label": "Loan-to-Value (LTV) Ratio", "default_display": "125.5% (Underwater / Negative Equity)", "highlight": True},
            {"id": "gap_recommendation", "label": "GAP Insurance Recommendation", "default_display": "CRITICAL: Purchase GAP Insurance", "highlight": True},
            {"id": "insurance_shortfall", "label": "Primary Insurance Payout Shortfall", "default_display": "$6,500.00"}
        ],
        "proof_steps": [
            {"step_title": "Total Loss Payout Rule", "step_text": "If a vehicle is totaled or stolen, standard auto insurance pays ONLY Actual Cash Value (ACV) minus your deductible, NOT what you owe on the loan."},
            {"step_title": "The Negative Equity Gap", "step_text": "GAP Shortfall = Loan Payoff - (ACV - Deductible). If you owe $32,000 and ACV is $25,500, you must write a $7,000 check to the lender for a car that no longer exists."},
            {"step_title": "Purchasing Heuristic", "step_text": "GAP insurance is essential whenever loan-to-value (LTV) exceeds 105-110%, typically occurring on loans with under 15% down payment or terms over 60 months."}
        ],
        "faqs": [
            {"q": "What happens if my car is totaled and I do not have GAP insurance?", "a": "Your auto insurer pays market value to the lender. The remaining balance (frequently $3,000 to $8,000+) remains your personal legal debt, which the bank will demand in full immediately."},
            {"q": "Where should I buy GAP insurance?", "a": "Never buy GAP from the dealership (where it costs $800 to $1,200). Buy it from your primary auto insurance company (State Farm, Geico, Progressive), where it typically costs only $20 to $40 per year."}
        ],
        "js_logic": """
          const payoff = getNum('current_loan_payoff');
          const acv = getNum('market_value_acv');
          const ded = getNum('insurance_deductible');

          const ltv = acv > 0 ? (payoff / acv) * 100 : 0;
          const shortfall = Math.max(0, payoff - acv);
          const totalGapExposure = Math.max(0, payoff - (acv - ded));

          let rec = 'GAP Insurance NOT Needed (Positive Equity)';
          if (totalGapExposure > 3000) rec = 'CRITICAL: Purchase GAP Insurance';
          else if (totalGapExposure > 1000) rec = 'Recommended: GAP Insurance Advised';

          setDisp('net_gap_exposure', '$' + totalGapExposure.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('equity_status', ltv.toFixed(1) + '% ' + (ltv > 100 ? '(Underwater / Negative Equity)' : '(Positive Equity)'));
          setDisp('gap_recommendation', rec);
          setDisp('insurance_shortfall', '$' + shortfall.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "oil-change-interval",
        "category": "physics",
        "name": "Motor Oil Change Interval & Maintenance Cost Calculator",
        "description": "Calculate optimal motor oil change intervals based on mileage, synthetic vs conventional oil, operating duty cycle, and annual maintenance budget.",
        "hero_badge": "Fleet Maintenance • Lubrication Schedule Matrix",
        "formula_display": "Annual Oil Cost = (Annual Miles / Change Interval) × Cost per Service",
        "fields": [
            {"id": "annual_driving_miles", "label": "Annual Miles Driven", "default": 14000, "suffix": "miles/yr", "min": 2000, "max": 100000, "step": 500, "hint": "Miles driven per calendar year"},
            {"id": "oil_type_interval", "label": "Oil Type Interval (5000 Conventional, 7500 Blend, 10000 Full Synthetic)", "default": 10000, "suffix": "miles", "min": 3000, "max": 15000, "step": 1000, "hint": "Manufacturer recommended interval"},
            {"id": "service_cost_per_change", "label": "Cost per Oil & Filter Service", "default": 85, "prefix": "$", "min": 25, "max": 350, "step": 5, "hint": "DIY (~$35) vs quick lube (~$85) vs dealer (~$140)"}
        ],
        "metrics": [
            {"id": "changes_per_year", "label": "Services Required per Year", "default_display": "1.4 changes / yr", "highlight": True},
            {"id": "annual_oil_cost", "label": "Annual Oil Maintenance Cost", "default_display": "$119.00 / yr", "highlight": True},
            {"id": "days_between_changes", "label": "Days Between Oil Changes", "default_display": "261 days (~8.7 months)"},
            {"id": "oil_cost_per_mile", "label": "Lubrication Cost per Mile", "default_display": "$0.0085 / mile"}
        ],
        "proof_steps": [
            {"step_title": "Duty Cycle Degradation Factors", "step_text": "Short trips under 5 miles, severe stop-and-go traffic, and heavy towing classify as 'Severe Service', requiring 25% shorter intervals due to fuel dilution and moisture accumulation."},
            {"step_title": "Full Synthetic Economic Superiority", "step_text": "While full synthetic oil costs 40% more per change, its 10,000-mile interval cuts service frequency in half compared to 5,000-mile conventional oil, reducing annual cost and time."},
            {"step_title": "Lubrication Cost per Mile", "step_text": "Cost/Mile = Service Cost / Interval. At $85 per 10,000 miles, clean oil costs less than 1 cent ($0.0085) per mile—the cheapest insurance for an engine."}
        ],
        "faqs": [
            {"q": "Do modern cars really need oil changes every 3,000 miles?", "a": "No! The 3,000-mile rule was created by quick-lube chains in the 1970s for non-detergent mineral oil. Modern synthetic motor oils and precision engines easily last 7,500 to 10,000 miles between changes."},
            {"q": "Can you switch back to conventional oil after using synthetic?", "a": "Yes. It is a persistent myth that once you switch to synthetic oil you can never go back. Synthetic and conventional oils are completely miscible and compatible."}
        ],
        "js_logic": """
          const miles = getNum('annual_driving_miles');
          const interval = getNum('oil_type_interval') || 10000;
          const cost = getNum('service_cost_per_change');

          const changes = miles / interval;
          const annualCost = changes * cost;
          const daysBetween = (interval / miles) * 365;
          const costMile = cost / interval;

          setDisp('changes_per_year', changes.toFixed(1) + ' changes / yr');
          setDisp('annual_oil_cost', '$' + annualCost.toFixed(2) + ' / yr');
          setDisp('days_between_changes', Math.round(daysBetween) + ' days (~' + (daysBetween / 30.4).toFixed(1) + ' months)');
          setDisp('oil_cost_per_mile', '$' + costMile.toFixed(4) + ' / mile');
        """
    },
    {
        "slug": "rv-payload-hitch",
        "category": "physics",
        "name": "RV Travel Trailer Tongue & Hitch Distribution Calculator",
        "description": "Calculate travel trailer hitch weight distribution, weight transfer to front steer axles, and prevention of trailer fishtailing.",
        "hero_badge": "RV Dynamics • Weight Distribution Matrix",
        "formula_display": "Hitch Weight % = (Tongue Weight / Total Loaded Trailer Weight) × 100",
        "fields": [
            {"id": "trailer_dry_weight", "label": "Trailer Dry Weight (Unloaded)", "default": 5500, "suffix": "lbs", "min": 1000, "max": 25000, "step": 100, "hint": "Manufacturer shipping weight"},
            {"id": "camping_cargo_gear", "label": "Water, Propane, Food & Gear", "default": 1200, "suffix": "lbs", "min": 200, "max": 8000, "step": 50, "hint": "Fresh water (8.3 lb/gal), batteries, gear"},
            {"id": "tongue_weight_measured", "label": "Measured Tongue Weight on Ball", "default": 800, "suffix": "lbs", "min": 100, "max": 3500, "step": 25, "hint": "Hitch weight measured on tongue scale"}
        ],
        "metrics": [
            {"id": "hitch_weight_pct", "label": "Tongue Weight Percentage", "default_display": "11.94%", "highlight": True},
            {"id": "total_loaded_trailer", "label": "Total Loaded Trailer Weight", "default_display": "6,700 lbs", "highlight": True},
            {"id": "stability_verdict", "label": "Towing Stability Assessment", "default_display": "Optimal Stability (10% - 15% Window)", "highlight": True},
            {"id": "wdh_recommendation", "label": "Weight Distribution Hitch (WDH)", "default_display": "WDH Strongly Recommended (> 5,000 lbs)"}
        ],
        "proof_steps": [
            {"step_title": "Total Loaded Weight Integration", "step_text": "Total Loaded Trailer = Dry Weight + Water + Propane + Batteries + Camping Gear."},
            {"step_title": "Tongue Ratio Dynamic Stability", "step_text": "Tongue % = (Tongue Weight / Total Trailer Weight) × 100. Target stability window is strictly 10.0% to 15.0%."},
            {"step_title": "Weight Distribution Hitch (WDH) Leverage", "step_text": "For trailers over 5,000 lbs, a Weight Distribution Hitch with spring bars acts as a lever, transferring tongue weight forward onto the truck's front steering axle and rearward onto trailer axles."}
        ],
        "faqs": [
            {"q": "What happens if travel trailer tongue weight is 8%?", "a": "At 8% tongue weight, the trailer is dangerously tail-heavy. When passing a semi-truck or encountering a crosswind, aerodynamic side forces will initiate violent, uncontrollable fishtailing that can roll the tow vehicle."},
            {"q": "How does fresh water affect tongue weight?", "a": "Fresh water tanks are rarely centered over trailer axles. If the tank is in front of the axle, 50 gallons of water adds 415 lbs of tongue weight. If behind the axle, water unloads the tongue, creating instability."}
        ],
        "js_logic": """
          const dry = getNum('trailer_dry_weight');
          const cargo = getNum('camping_cargo_gear');
          const tongue = getNum('tongue_weight_measured');

          const total = dry + cargo;
          const pct = total > 0 ? (tongue / total) * 100 : 0;

          let verdict = 'Optimal Stability (10% - 15% Window)';
          if (pct < 10) verdict = 'DANGEROUS: Tail-Heavy Sway Risk (< 10%)';
          else if (pct > 15) verdict = 'CAUTION: Nose-Heavy Rear Axle Overload (> 15%)';

          let wdh = total >= 5000 ? 'WDH Strongly Recommended (> 5,000 lbs)' : 'Weight Carrying Hitch Acceptable (< 5,000 lbs)';

          setDisp('hitch_weight_pct', pct.toFixed(2) + '%');
          setDisp('total_loaded_trailer', total.toLocaleString() + ' lbs');
          setDisp('stability_verdict', verdict);
          setDisp('wdh_recommendation', wdh);
        """
    }
]
