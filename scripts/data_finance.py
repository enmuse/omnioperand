"""
scripts/data_finance.py
40 High-Value Finance, Debt, Lending & Real Estate Calculators.
Clean mathematical Unicode only (Zero raw LaTeX).
"""

FINANCE_CALCULATORS = [
    {
        "slug": "refinance",
        "category": "finance",
        "name": "Mortgage Refinance & Breakeven Calculator",
        "description": "Calculate monthly payment savings, lifetime interest reduction, and closing cost breakeven horizon when refinancing a home mortgage.",
        "hero_badge": "Mortgage Refinancing • Breakeven Analysis",
        "formula_display": "Breakeven Months = Total Closing Costs / (Current Payment - New Payment)",
        "fields": [
            {"id": "balance", "label": "Remaining Balance", "default": 350000, "prefix": "$", "min": 10000, "max": 2000000, "step": 5000, "hint": "Current outstanding mortgage loan balance"},
            {"id": "curr_rate", "label": "Current Interest Rate (%)", "default": 6.875, "suffix": "%", "min": 1, "max": 15, "step": 0.125, "hint": "Your current mortgage note rate"},
            {"id": "curr_term", "label": "Remaining Years", "default": 27, "suffix": "yrs", "min": 1, "max": 30, "step": 1, "hint": "Number of years left on existing mortgage"},
            {"id": "new_rate", "label": "New Refinance Rate (%)", "default": 5.75, "suffix": "%", "min": 1, "max": 15, "step": 0.125, "hint": "Offered new interest rate"},
            {"id": "new_term", "label": "New Loan Term (Years)", "default": 30, "suffix": "yrs", "min": 10, "max": 30, "step": 5, "hint": "Term of the new replacement mortgage"},
            {"id": "closing_costs", "label": "Total Closing Costs", "default": 5500, "prefix": "$", "min": 0, "max": 25000, "step": 500, "hint": "Origination, appraisal, title, and lender fees"}
        ],
        "metrics": [
            {"id": "monthly_savings", "label": "Monthly Payment Savings", "default_display": "$214.50", "highlight": True},
            {"id": "breakeven_months", "label": "Breakeven Timeline", "default_display": "25.6 months"},
            {"id": "new_monthly_payment", "label": "New Monthly Payment (P&I)", "default_display": "$2,042.80"},
            {"id": "lifetime_savings", "label": "Net Lifetime Savings", "default_display": "$48,220.00"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Amortization Derivation", "step_text": "Monthly payments M are computed using the annuity equation: M = P · [i(1 + i)ⁿ] / [(1 + i)ⁿ - 1], where i = r / 12 and n = years × 12."},
            {"step_title": "Monthly Cash Flow Differential", "step_text": "Monthly payment savings ΔM = M_current - M_new. If ΔM > 0, the homeowner captures immediate monthly liquidity."},
            {"step_title": "Capital Recovery & Breakeven Horizon", "step_text": "The exact time in months to recover closing costs C is: T_breakeven = C / ΔM. If the homeowner remains in the home longer than T_breakeven, refinancing yields positive economic surplus."},
            {"step_title": "Net Lifetime Wealth Impact", "step_text": "Net lifetime savings = (Total remaining payments under old loan) - (Total payments under new loan + closing costs)."}
        ],
        "faqs": [
            {"q": "What is considered a good breakeven period for refinancing?", "a": "Financial planners typically target a breakeven timeline of under 36 months (3 years). If you plan to remain in the property longer than the breakeven threshold, refinancing is financially accretive."},
            {"q": "Should I roll closing costs into the loan balance?", "a": "Rolling closing costs into the new principal avoids out-of-pocket expenses, but increases the principal balance P, raising both your monthly payment and total lifetime interest paid."},
            {"q": "Can refinancing to a 15-year loan save more money?", "a": "Yes! While a 15-year term increases your monthly payment due to faster principal amortization, it significantly reduces total lifetime interest by cutting interest accrual time in half."}
        ],
        "js_logic": """
          const P = getNum('balance');
          const rOld = (getNum('curr_rate') / 100) / 12;
          const nOld = getNum('curr_term') * 12;
          const rNew = (getNum('new_rate') / 100) / 12;
          const nNew = getNum('new_term') * 12;
          const costs = getNum('closing_costs');

          const oldM = rOld === 0 ? P / nOld : P * (rOld * Math.pow(1 + rOld, nOld)) / (Math.pow(1 + rOld, nOld) - 1);
          const newM = rNew === 0 ? P / nNew : P * (rNew * Math.pow(1 + rNew, nNew)) / (Math.pow(1 + rNew, nNew) - 1);
          const savingsMo = oldM - newM;
          const breakeven = savingsMo > 0 ? (costs / savingsMo) : 0;
          const oldTotal = oldM * nOld;
          const newTotal = (newM * nNew) + costs;
          const netLifetime = oldTotal - newTotal;

          setDisp('monthly_savings', '$' + Math.max(0, savingsMo).toFixed(2));
          setDisp('breakeven_months', savingsMo > 0 ? breakeven.toFixed(1) + ' months' : 'No savings');
          setDisp('new_monthly_payment', '$' + newM.toFixed(2));
          setDisp('lifetime_savings', '$' + Math.round(netLifetime).toLocaleString());
        """
    },
    {
        "slug": "heloc",
        "category": "finance",
        "name": "HELOC (Home Equity Line of Credit) Payment Calculator",
        "description": "Calculate interest-only draw period payments and fully amortizing repayment installments for a Home Equity Line of Credit.",
        "hero_badge": "Home Equity • Revolving Credit Matrix",
        "formula_display": "Interest-Only Payment = (Balance · Annual Rate) / 12",
        "fields": [
            {"id": "line_amount", "label": "Drawn HELOC Balance", "default": 75000, "prefix": "$", "min": 5000, "max": 500000, "step": 2500, "hint": "Amount drawn against home equity line"},
            {"id": "heloc_rate", "label": "Variable Interest Rate (%)", "default": 8.5, "suffix": "%", "min": 2, "max": 18, "step": 0.25, "hint": "Current annual variable percentage rate (APR)"},
            {"id": "draw_years", "label": "Draw Period (Years)", "default": 10, "suffix": "yrs", "min": 5, "max": 15, "step": 1, "hint": "Initial interest-only draw period"},
            {"id": "repay_years", "label": "Repayment Period (Years)", "default": 20, "suffix": "yrs", "min": 5, "max": 20, "step": 5, "hint": "Subsequent principal + interest repayment term"}
        ],
        "metrics": [
            {"id": "draw_payment", "label": "Draw Period Monthly Payment", "default_display": "$531.25", "highlight": True},
            {"id": "repay_payment", "label": "Repayment Monthly Payment", "default_display": "$650.84"},
            {"id": "total_interest_draw", "label": "Total Draw Period Interest", "default_display": "$63,750.00"},
            {"id": "total_cost", "label": "Total Cumulative Cost", "default_display": "$156,201.60"}
        ],
        "proof_steps": [
            {"step_title": "Interest-Only Cash Flow During Draw Period", "step_text": "During the draw period (typically years 1–10), the borrower pays strictly accrued interest: M_draw = B · (r / 12), where B is drawn balance and r is variable APR."},
            {"step_title": "Payment Reset Upon Amortization Period", "step_text": "At month (draw_years × 12) + 1, the draw period closes and the loan resets into full principal amortization: M_repay = B · [i(1 + i)ᵐ] / [(1 + i)ᵐ - 1], where m = repay_years × 12."},
            {"step_title": "Payment Shock Sensitivity", "step_text": "Payment shock is defined as ΔM_reset = M_repay - M_draw. Borrowers must anticipate this mandatory jump when the draw window concludes."}
        ],
        "faqs": [
            {"q": "What causes HELOC payments to increase?", "a": "HELOC payments increase if variable index rates (e.g. Wall Street Journal Prime Rate) rise, or when the 10-year interest-only draw period ends and mandatory principal repayment begins."},
            {"q": "Can I pay principal during the draw period?", "a": "Yes! Paying voluntary principal during the draw period reduces your daily average balance, directly decreasing your monthly interest charges."}
        ],
        "js_logic": """
          const B = getNum('line_amount');
          const r = (getNum('heloc_rate') / 100) / 12;
          const drawM = B * r;
          const mRepay = getNum('repay_years') * 12;
          const repayM = r === 0 ? B / mRepay : B * (r * Math.pow(1 + r, mRepay)) / (Math.pow(1 + r, mRepay) - 1);
          const totalDrawInt = drawM * (getNum('draw_years') * 12);
          const totalRepay = repayM * mRepay;

          setDisp('draw_payment', '$' + drawM.toFixed(2));
          setDisp('repay_payment', '$' + repayM.toFixed(2));
          setDisp('total_interest_draw', '$' + Math.round(totalDrawInt).toLocaleString());
          setDisp('total_cost', '$' + Math.round(totalDrawInt + totalRepay).toLocaleString());
        """
    },
    {
        "slug": "dti",
        "category": "finance",
        "name": "Debt-to-Income (DTI) Ratio Calculator",
        "description": "Calculate front-end and back-end debt-to-income ratios and determine your maximum qualified home purchase price for mortgage underwriting.",
        "hero_badge": "Underwriting Invariants • DTI Matrix",
        "formula_display": "Back-End DTI = (Total Monthly Debt Obligations / Gross Monthly Income) × 100%",
        "fields": [
            {"id": "annual_income", "label": "Gross Annual Income", "default": 110000, "prefix": "$", "min": 20000, "max": 1000000, "step": 5000, "hint": "Pre-tax total annual household income"},
            {"id": "proposed_housing", "label": "Proposed Housing Payment", "default": 2400, "prefix": "$", "min": 500, "max": 15000, "step": 100, "hint": "Principal, interest, taxes, insurance (PITI) and HOA"},
            {"id": "auto_payments", "label": "Monthly Auto Loans", "default": 450, "prefix": "$", "min": 0, "max": 3000, "step": 50, "hint": "Total minimum car loan or lease payments"},
            {"id": "student_loans", "label": "Monthly Student Loans", "default": 250, "prefix": "$", "min": 0, "max": 3000, "step": 25, "hint": "Monthly student debt obligation"},
            {"id": "credit_cards", "label": "Credit Card Minimums", "default": 150, "prefix": "$", "min": 0, "max": 5000, "step": 25, "hint": "Sum of all minimum monthly revolving payments"}
        ],
        "metrics": [
            {"id": "back_end_dti", "label": "Back-End DTI Ratio", "default_display": "35.5%", "highlight": True},
            {"id": "front_end_dti", "label": "Front-End Housing DTI", "default_display": "26.2%"},
            {"id": "underwriting_status", "label": "Underwriting Qualification", "default_display": "Fannie Mae Approved (<= 36%)"},
            {"id": "max_housing_budget", "label": "Max Allowed Housing Payment", "default_display": "$3,083.33"}
        ],
        "proof_steps": [
            {"step_title": "Gross Monthly Income Derivation", "step_text": "Gross Monthly Income GMI = Gross Annual Income / 12."},
            {"step_title": "Front-End Housing Ratio", "step_text": "Front-End DTI = (Proposed Housing Payment PITI / GMI) × 100%. Conventional lending benchmarks target <= 28%."},
            {"step_title": "Back-End Total Debt Ratio", "step_text": "Back-End DTI = [(Housing PITI + Auto + Student + Credit Cards) / GMI] × 100%. Qualified Mortgage (QM) limits set the strict upper bound at 43% to 45%."}
        ],
        "faqs": [
            {"q": "What is the maximum DTI allowed for a conventional mortgage?", "a": "Conventional loans backed by Fannie Mae and Freddie Mac generally require a back-end DTI of 36% or less, though automated underwriting systems (DU/LP) allow up to 45% or 50% with strong compensating credit scores and cash reserves."},
            {"q": "Do utility bills and car insurance count toward DTI?", "a": "No. Living expenses like groceries, cell phone bills, car insurance, and utilities are not considered contractual debt obligations and are excluded from DTI underwriting."}
        ],
        "js_logic": """
          const gmi = getNum('annual_income') / 12;
          const housing = getNum('proposed_housing');
          const debts = getNum('auto_payments') + getNum('student_loans') + getNum('credit_cards');
          const totalDebt = housing + debts;
          const frontDti = gmi > 0 ? (housing / gmi) * 100 : 0;
          const backDti = gmi > 0 ? (totalDebt / gmi) * 100 : 0;
          const maxHousing43 = Math.max(0, (gmi * 0.43) - debts);

          setDisp('back_end_dti', backDti.toFixed(1) + '%');
          setDisp('front_end_dti', frontDti.toFixed(1) + '%');
          setDisp('max_housing_budget', '$' + Math.round(maxHousing43).toLocaleString());

          let status = 'Excellent (<= 36%)';
          if (backDti > 50) status = 'High Risk (> 50%)';
          else if (backDti > 43) status = 'FHA / Non-QM Only (44-50%)';
          else if (backDti > 36) status = 'Conventional Approved (37-43%)';
          setDisp('underwriting_status', status);
        """
    },
    {
        "slug": "ltv",
        "category": "finance",
        "name": "Loan-to-Value (LTV) Ratio & PMI Calculator",
        "description": "Determine your exact Loan-to-Value (LTV) ratio, required private mortgage insurance (PMI) thresholds, and equity milestones.",
        "hero_badge": "Equity Analysis • PMI Invariants",
        "formula_display": "LTV = (Loan Balance / Appraised Property Value) × 100%",
        "fields": [
            {"id": "property_value", "label": "Appraised Home Value", "default": 450000, "prefix": "$", "min": 50000, "max": 3000000, "step": 5000, "hint": "Fair market appraised valuation"},
            {"id": "mortgage_balance", "label": "Current Loan Balance", "default": 382500, "prefix": "$", "min": 10000, "max": 3000000, "step": 2500, "hint": "Total outstanding mortgage principal"}
        ],
        "metrics": [
            {"id": "ltv_percentage", "label": "Loan-to-Value (LTV)", "default_display": "85.0%", "highlight": True},
            {"id": "home_equity", "label": "Total Home Equity ($)", "default_display": "$67,500.00"},
            {"id": "pmi_status", "label": "Private Mortgage Insurance", "default_display": "PMI Required (LTV > 80%)"},
            {"id": "pmi_elimination_target", "label": "Paydown Needed to Remove PMI", "default_display": "$22,500.00"}
        ],
        "proof_steps": [
            {"step_title": "LTV Mathematical Definition", "step_text": "LTV = (Mortgage Principal / Appraised Value) × 100%."},
            {"step_title": "Homeowner Protection Act Statutory Threshold", "step_text": "Under the federal Homeowners Protection Act of 1998, borrowers may request PMI cancellation at 80% LTV, and lenders must automatically terminate PMI at 78% LTV on the original amortization schedule."},
            {"step_title": "Capital Required for PMI Removal", "step_text": "Paydown Target = Current Balance - (Appraised Value × 0.80)."}
        ],
        "faqs": [
            {"q": "How can I lower my LTV without paying extra principal?", "a": "Home price appreciation or substantial renovations can increase your home's appraised fair market value, thereby driving down your LTV ratio and allowing you to petition for early PMI removal via a new appraisal."},
            {"q": "What is the difference between LTV and CLTV?", "a": "LTV measures only the primary first mortgage. Combined Loan-to-Value (CLTV) includes all liens secured by the property, including second mortgages and HELOCs."}
        ],
        "js_logic": """
          const V = getNum('property_value');
          const L = getNum('mortgage_balance');
          const ltv = V > 0 ? (L / V) * 100 : 0;
          const equity = Math.max(0, V - L);
          const target80 = V * 0.80;
          const paydown80 = Math.max(0, L - target80);

          setDisp('ltv_percentage', ltv.toFixed(1) + '%');
          setDisp('home_equity', '$' + Math.round(equity).toLocaleString());
          setDisp('pmi_elimination_target', '$' + Math.round(paydown80).toLocaleString());

          let pmiMsg = 'No PMI Required (LTV <= 80%)';
          if (ltv > 80) pmiMsg = 'PMI Required (LTV > 80%)';
          setDisp('pmi_status', pmiMsg);
        """
    },
    {
        "slug": "fha-loan",
        "category": "finance",
        "name": "FHA Loan & Mortgage Insurance (MIP) Calculator",
        "description": "Calculate monthly FHA payments including upfront (UFMIP) and annual monthly mortgage insurance premiums with minimum 3.5% down payment.",
        "hero_badge": "Government Lending • FHA Formula",
        "formula_display": "Total Financed Loan = Purchase Price - Down Payment + (Base Loan × 1.75% UFMIP)",
        "fields": [
            {"id": "purchase_price", "label": "Home Purchase Price", "default": 320000, "prefix": "$", "min": 50000, "max": 1500000, "step": 5000, "hint": "Agreed home purchase price"},
            {"id": "down_payment_pct", "label": "Down Payment (%)", "default": 3.5, "suffix": "%", "min": 3.5, "max": 20, "step": 0.5, "hint": "Minimum 3.5% down payment"},
            {"id": "interest_rate", "label": "Interest Rate (%)", "default": 6.25, "suffix": "%", "min": 2, "max": 12, "step": 0.125, "hint": "30-year fixed FHA note rate"}
        ],
        "metrics": [
            {"id": "total_monthly", "label": "Total Monthly FHA Payment", "default_display": "$2,069.45", "highlight": True},
            {"id": "base_payment", "label": "Base Principal & Interest", "default_display": "$1,927.85"},
            {"id": "monthly_mip", "label": "Monthly FHA MIP (0.55%)", "default_display": "$141.60"},
            {"id": "upfront_mip", "label": "Upfront MIP Financed (1.75%)", "default_display": "$5,404.00"}
        ],
        "proof_steps": [
            {"step_title": "Down Payment & Base Loan", "step_text": "Down Payment = Price × Down_Pct. Base Loan = Price - Down Payment."},
            {"step_title": "Upfront Mortgage Insurance Premium (UFMIP)", "step_text": "FHA requires an upfront premium of 1.75%: UFMIP = Base Loan × 0.0175. This is customarily financed directly into the loan."},
            {"step_title": "Annual Monthly MIP", "step_text": "For LTV > 95% on 30-year terms, annual MIP is 0.55%: Monthly MIP = (Total Financed × 0.0055) / 12."}
        ],
        "faqs": [
            {"q": "Can FHA mortgage insurance be canceled?", "a": "For FHA loans with less than 10% down payment, annual MIP lasts for the entire duration of the loan term. To remove MIP, homeowners typically refinance into a conventional loan once their equity reaches 20%."},
            {"q": "What is the minimum credit score for 3.5% down on an FHA loan?", "a": "HUD regulations require a minimum FICO score of 580 to qualify for the 3.5% down payment program. Borrowers with scores between 500 and 579 require a minimum 10% down payment."}
        ],
        "js_logic": """
          const price = getNum('purchase_price');
          const downPct = getNum('down_payment_pct') / 100;
          const downAmt = price * downPct;
          const baseLoan = price - downAmt;
          const ufmip = baseLoan * 0.0175;
          const totalLoan = baseLoan + ufmip;

          const r = (getNum('interest_rate') / 100) / 12;
          const n = 360;
          const pi = r === 0 ? totalLoan / n : totalLoan * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const monthlyMip = (totalLoan * 0.0055) / 12;

          setDisp('base_payment', '$' + pi.toFixed(2));
          setDisp('monthly_mip', '$' + monthlyMip.toFixed(2));
          setDisp('upfront_mip', '$' + Math.round(ufmip).toLocaleString());
          setDisp('total_monthly', '$' + (pi + monthlyMip).toFixed(2));
        """
    },
    {
        "slug": "va-loan",
        "category": "finance",
        "name": "VA Loan Payment & Funding Fee Calculator",
        "description": "Calculate 0% down VA home loan monthly payments, tiered VA funding fees, and total interest with zero monthly private mortgage insurance.",
        "hero_badge": "Military Benefits • 0% Down Invariant",
        "formula_display": "Total Financed Loan = Purchase Price + (Purchase Price × Funding Fee %)",
        "fields": [
            {"id": "purchase_price", "label": "Home Purchase Price", "default": 400000, "prefix": "$", "min": 50000, "max": 2000000, "step": 5000, "hint": "Agreed purchase price"},
            {"id": "interest_rate", "label": "Interest Rate (%)", "default": 6.125, "suffix": "%", "min": 2, "max": 12, "step": 0.125, "hint": "30-year fixed VA rate"},
            {"id": "down_payment", "label": "Down Payment ($)", "default": 0, "prefix": "$", "min": 0, "max": 200000, "step": 5000, "hint": "Optional down payment (0% is standard)"},
            {"id": "service_type", "label": "VA Funding Fee Tier", "default": 2.15, "suffix": "%", "min": 0, "max": 3.3, "step": 0.15, "hint": "First-time use (2.15%), Subsequent (3.3%), or Exempt (0%)"}
        ],
        "metrics": [
            {"id": "monthly_pi", "label": "Monthly Payment (P&I)", "default_display": "$2,481.94", "highlight": True},
            {"id": "funding_fee_amt", "label": "VA Funding Fee Financed", "default_display": "$8,600.00"},
            {"id": "total_loan", "label": "Total Amount Financed", "default_display": "$408,600.00"},
            {"id": "pmi_savings", "label": "Monthly PMI Saved (vs FHA)", "default_display": "$187.00"}
        ],
        "proof_steps": [
            {"step_title": "Zero Down Payment Benefit", "step_text": "VA loans provide 100% financing with zero down payment requirement: Base Loan = Price - Down Payment."},
            {"step_title": "Statutory VA Funding Fee", "step_text": "VA Funding Fee = Base Loan × Fee_Rate (2.15% for first-time use with 0% down; 0% for service-connected disability)."},
            {"step_title": "Monthly PMI Exemption", "step_text": "Unlike conventional and FHA mortgages, VA loans carry zero monthly mortgage insurance premiums, delivering substantial monthly savings."}
        ],
        "faqs": [
            {"q": "Who is exempt from the VA funding fee?", "a": "Veterans receiving VA compensation for a service-connected disability, surviving spouses eligible for Dependency and Indemnity Compensation (DIC), and active-duty Purple Heart recipients are exempt from paying the funding fee."},
            {"q": "Is there a maximum limit on a VA loan?", "a": "For veterans with full entitlement, there is no conforming loan limit; borrowers can obtain 0% down financing up to whatever loan amount their income qualifies for."}
        ],
        "js_logic": """
          const price = getNum('purchase_price');
          const down = getNum('down_payment');
          const base = Math.max(0, price - down);
          const feePct = getNum('service_type') / 100;
          const fee = base * feePct;
          const total = base + fee;
          const r = (getNum('interest_rate') / 100) / 12;
          const n = 360;
          const pi = r === 0 ? total / n : total * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

          setDisp('monthly_pi', '$' + pi.toFixed(2));
          setDisp('funding_fee_amt', '$' + Math.round(fee).toLocaleString());
          setDisp('total_loan', '$' + Math.round(total).toLocaleString());
          setDisp('pmi_savings', '$' + Math.round((total * 0.0055) / 12).toLocaleString());
        """
    },
    {
        "slug": "reverse-mortgage",
        "category": "finance",
        "name": "Reverse Mortgage (HECM) Calculator",
        "description": "Estimate Home Equity Conversion Mortgage (HECM) borrowing power, principal limits, and tenure monthly payout streams for homeowners 62+.",
        "hero_badge": "Retirement Equity • HECM Formulas",
        "formula_display": "Principal Limit = Home Value × Principal Limit Factor (Age, Rate)",
        "fields": [
            {"id": "home_value", "label": "Appraised Home Value", "default": 550000, "prefix": "$", "min": 100000, "max": 1500000, "step": 10000, "hint": "Current fair market home value"},
            {"id": "youngest_age", "label": "Age of Youngest Borrower", "default": 68, "suffix": "yrs", "min": 62, "max": 95, "step": 1, "hint": "Must be at least 62 years old"},
            {"id": "existing_mortgage", "label": "Existing Mortgage Balance", "default": 85000, "prefix": "$", "min": 0, "max": 500000, "step": 5000, "hint": "Must be paid off by reverse mortgage proceeds"}
        ],
        "metrics": [
            {"id": "net_principal_limit", "label": "Net Available Cash Proceeds", "default_display": "$178,500.00", "highlight": True},
            {"id": "gross_principal_limit", "label": "Gross Principal Limit", "default_display": "$263,500.00"},
            {"id": "monthly_tenure", "label": "Lifetime Monthly Tenure Payout", "default_display": "$1,120.00"},
            {"id": "fha_hecm_limit", "label": "FHA Maximum Claim Limit", "default_display": "$1,149,825.00"}
        ],
        "proof_steps": [
            {"step_title": "Maximum Claim Amount (MCA)", "step_text": "MCA = min(Appraised Home Value, FHA National HECM Lending Limit $1,149,825)."},
            {"step_title": "Principal Limit Factor (PLF)", "step_text": "The actuarial factor PLF is determined by HUD tables based on the age of the youngest borrower and the expected interest rate. (Approx. 40% at age 62 up to 65% at age 85)."},
            {"step_title": "Net Proceeds Resolution", "step_text": "Net Available = (MCA × PLF) - Mandatory Existing Mortgage Payoff - Closing Costs."}
        ],
        "faqs": [
            {"q": "Does the bank take ownership of the house in a reverse mortgage?", "a": "No. The homeowner retains complete title and ownership of the home. The loan is non-recourse, meaning you or your heirs will never owe more than the home is worth when sold."},
            {"q": "Are reverse mortgage proceeds taxable?", "a": "No. Money received from a reverse mortgage is considered loan proceeds rather than earned income, making it completely exempt from federal and state income taxes."}
        ],
        "js_logic": """
          const V = Math.min(getNum('home_value'), 1149825);
          const age = getNum('youngest_age');
          const existing = getNum('existing_mortgage');
          const plf = Math.min(0.68, Math.max(0.38, 0.38 + (age - 62) * 0.012));
          const gross = V * plf;
          const net = Math.max(0, gross - existing - 6000);
          const tenureMonthly = net > 0 ? (net / (12 * (100 - age))) : 0;

          setDisp('gross_principal_limit', '$' + Math.round(gross).toLocaleString());
          setDisp('net_principal_limit', '$' + Math.round(net).toLocaleString());
          setDisp('monthly_tenure', '$' + Math.round(tenureMonthly).toLocaleString() + '/mo');
        """
    },
    {
        "slug": "personal-loan",
        "category": "finance",
        "name": "Personal Loan & Debt Consolidation Calculator",
        "description": "Calculate fixed monthly installments, total interest, and consolidation savings for unsecured personal loans.",
        "hero_badge": "Unsecured Credit • Amortization Matrix",
        "formula_display": "M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]",
        "fields": [
            {"id": "loan_amount", "label": "Loan Amount", "default": 25000, "prefix": "$", "min": 1000, "max": 100000, "step": 1000, "hint": "Requested personal borrowing amount"},
            {"id": "interest_rate", "label": "Interest Rate (%)", "default": 11.5, "suffix": "%", "min": 5, "max": 36, "step": 0.25, "hint": "Fixed APR based on credit tier"},
            {"id": "term_months", "label": "Loan Term (Months)", "default": 36, "suffix": "mo", "min": 12, "max": 84, "step": 12, "hint": "Repayment duration"}
        ],
        "metrics": [
            {"id": "monthly_installment", "label": "Monthly Installment", "default_display": "$824.62", "highlight": True},
            {"id": "total_interest", "label": "Total Cumulative Interest", "default_display": "$4,686.32"},
            {"id": "total_repayment", "label": "Total Overall Repayment", "default_display": "$29,686.32"}
        ],
        "proof_steps": [
            {"step_title": "Fixed Installment Math", "step_text": "Using standard fixed amortization: M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1], where r = APR / 1200."},
            {"step_title": "Total Cost of Borrowing", "step_text": "Total Outlay = M × n. Total Interest = (M × n) - P."}
        ],
        "faqs": [
            {"q": "Can I pay off a personal loan early to save interest?", "a": "Yes! Most top-tier personal loan lenders carry zero prepayment penalties, meaning extra payments directly decrease remaining principal and stop future interest accrual."}
        ],
        "js_logic": """
          const P = getNum('loan_amount');
          const r = (getNum('interest_rate') / 100) / 12;
          const n = getNum('term_months');
          const m = r === 0 ? P / n : P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const total = m * n;
          const interest = total - P;

          setDisp('monthly_installment', '$' + m.toFixed(2));
          setDisp('total_interest', '$' + Math.round(interest).toLocaleString());
          setDisp('total_repayment', '$' + Math.round(total).toLocaleString());
        """
    },
    {
        "slug": "student-loan-refinance",
        "category": "finance",
        "name": "Student Loan Refinancing Calculator",
        "description": "Calculate interest savings and monthly payment changes when refinancing federal or private student debt into lower private interest rates.",
        "hero_badge": "Education Debt • Refi Yields",
        "formula_display": "Total Interest Saved = Lifetime Old Interest - Lifetime Refinanced Interest",
        "fields": [
            {"id": "balance", "label": "Student Loan Balance", "default": 65000, "prefix": "$", "min": 5000, "max": 300000, "step": 2500, "hint": "Total balance of student loans to refinance"},
            {"id": "curr_rate", "label": "Current Weighted APR (%)", "default": 7.2, "suffix": "%", "min": 2, "max": 14, "step": 0.1, "hint": "Average current interest rate"},
            {"id": "curr_term", "label": "Remaining Term (Years)", "default": 10, "suffix": "yrs", "min": 2, "max": 25, "step": 1, "hint": "Years remaining on standard plan"},
            {"id": "new_rate", "label": "New Refinanced APR (%)", "default": 5.1, "suffix": "%", "min": 2, "max": 12, "step": 0.1, "hint": "Offered private refi interest rate"},
            {"id": "new_term", "label": "New Term (Years)", "default": 10, "suffix": "yrs", "min": 5, "max": 20, "step": 5, "hint": "Target repayment term"}
        ],
        "metrics": [
            {"id": "total_savings", "label": "Total Lifetime Interest Saved", "default_display": "$8,540.00", "highlight": True},
            {"id": "monthly_diff", "label": "Monthly Payment Savings", "default_display": "$71.17"},
            {"id": "new_monthly", "label": "New Monthly Payment", "default_display": "$691.83"}
        ],
        "proof_steps": [
            {"step_title": "Current Loan Stream", "step_text": "M_old = P · [r₁(1 + r₁)ⁿ¹] / [(1 + r₁)ⁿ¹ - 1]. Total_old = M_old × n₁."},
            {"step_title": "Refinanced Stream", "step_text": "M_new = P · [r₂(1 + r₂)ⁿ²] / [(1 + r₂)ⁿ² - 1]. Total_new = M_new × n₂."},
            {"step_title": "Net Interest Reduction", "step_text": "Savings = Total_old - Total_new."}
        ],
        "faqs": [
            {"q": "Do I lose federal student loan benefits if I refinance?", "a": "Yes. Refinancing federal loans with a private lender permanently forfeits federal protections like Income-Driven Repayment (IDR), Public Service Loan Forgiveness (PSLF), and federal forbearance options."}
        ],
        "js_logic": """
          const P = getNum('balance');
          const r1 = (getNum('curr_rate') / 100) / 12;
          const n1 = getNum('curr_term') * 12;
          const r2 = (getNum('new_rate') / 100) / 12;
          const n2 = getNum('new_term') * 12;

          const m1 = r1 === 0 ? P / n1 : P * (r1 * Math.pow(1 + r1, n1)) / (Math.pow(1 + r1, n1) - 1);
          const m2 = r2 === 0 ? P / n2 : P * (r2 * Math.pow(1 + r2, n2)) / (Math.pow(1 + r2, n2) - 1);
          const tot1 = m1 * n1;
          const tot2 = m2 * n2;
          const savings = tot1 - tot2;

          setDisp('new_monthly', '$' + m2.toFixed(2));
          setDisp('monthly_diff', '$' + Math.max(0, m1 - m2).toFixed(2));
          setDisp('total_savings', '$' + Math.round(savings).toLocaleString());
        """
    },
    {
        "slug": "credit-card-payoff",
        "category": "finance",
        "name": "Credit Card Payoff & Interest Snowball Calculator",
        "description": "Calculate exact debt-free payoff timelines, total compound interest charges, and monthly payment requirements for high-interest revolving credit.",
        "hero_badge": "Consumer Debt • Exponential Decay",
        "formula_display": "Months to Pay Off = -ln[1 - (P · i / M)] / ln(1 + i)",
        "fields": [
            {"id": "cc_balance", "label": "Credit Card Balance", "default": 14000, "prefix": "$", "min": 500, "max": 100000, "step": 500, "hint": "Total balance on card"},
            {"id": "cc_apr", "label": "Annual Percentage Rate (APR)", "default": 24.5, "suffix": "%", "min": 10, "max": 36, "step": 0.5, "hint": "Revolving interest rate"},
            {"id": "monthly_pay", "label": "Monthly Payment Plan", "default": 500, "prefix": "$", "min": 50, "max": 5000, "step": 50, "hint": "Fixed monthly cash dedicated to card"}
        ],
        "metrics": [
            {"id": "payoff_months", "label": "Time to Debt Freedom", "default_display": "39 months (3.3 yrs)", "highlight": True},
            {"id": "total_cc_interest", "label": "Total Interest Accrued", "default_display": "$5,482.00"},
            {"id": "total_cc_paid", "label": "Total Principal + Interest Paid", "default_display": "$19,482.00"}
        ],
        "proof_steps": [
            {"step_title": "Logarithmic Payoff Inversion", "step_text": "From B_(t+1) = B_t(1 + i) - M, solving for n yields: n = -ln[1 - (B · i) / M] / ln(1 + i), where i = APR / 12."},
            {"step_title": "Minimum Threshold Invariant", "step_text": "If M <= B · i, monthly payments fail to cover interest accrual, causing infinite debt expansion."}
        ],
        "faqs": [
            {"q": "Why does making only minimum payments take decades?", "a": "Minimum payments are often calculated as only 1% to 2% of the principal plus monthly interest, meaning the majority of your payment goes to bank interest rather than retiring principal."}
        ],
        "js_logic": """
          const B = getNum('cc_balance');
          const i = (getNum('cc_apr') / 100) / 12;
          const M = getNum('monthly_pay');

          if (M <= B * i) {
            setDisp('payoff_months', 'Never (Under-funded)');
            setDisp('total_cc_interest', 'Infinite');
            setDisp('total_cc_paid', 'Infinite');
          } else {
            const n = -Math.log(1 - (B * i) / M) / Math.log(1 + i);
            const total = M * n;
            const interest = total - B;
            const yrs = (n / 12).toFixed(1);
            setDisp('payoff_months', Math.ceil(n) + ' mos (' + yrs + ' yrs)');
            setDisp('total_cc_interest', '$' + Math.round(interest).toLocaleString());
            setDisp('total_cc_paid', '$' + Math.round(total).toLocaleString());
          }
        """
    },
    {
        "slug": "boat-loan",
        "category": "finance",
        "name": "Boat Loan Financing & Payment Calculator",
        "description": "Calculate marine loan monthly payments, required down payments (10-20%), and total financing costs for new and used boats and yachts.",
        "hero_badge": "Marine Lending • Fixed Installments",
        "formula_display": "Financed Principal = Boat Price - Down Payment + Sales Tax",
        "fields": [
            {"id": "boat_price", "label": "Boat Purchase Price", "default": 65000, "prefix": "$", "min": 5000, "max": 500000, "step": 2500, "hint": "Agreed price of vessel"},
            {"id": "down_pct", "label": "Down Payment (%)", "default": 15, "suffix": "%", "min": 0, "max": 50, "step": 5, "hint": "10-20% standard marine down payment"},
            {"id": "loan_rate", "label": "Interest Rate (%)", "default": 7.99, "suffix": "%", "min": 4, "max": 18, "step": 0.25, "hint": "Annual marine APR"},
            {"id": "loan_term_yrs", "label": "Loan Term (Years)", "default": 15, "suffix": "yrs", "min": 5, "max": 20, "step": 5, "hint": "Marine loan durations typically 10 to 20 years"}
        ],
        "metrics": [
            {"id": "boat_payment", "label": "Monthly Marine Payment", "default_display": "$528.40", "highlight": True},
            {"id": "down_amt", "label": "Required Down Payment", "default_display": "$9,750.00"},
            {"id": "total_boat_interest", "label": "Total Marine Interest", "default_display": "$39,862.00"}
        ],
        "proof_steps": [
            {"step_title": "Marine Down Payment Deduction", "step_text": "P = Boat Price × (1 - Down_Pct / 100)."},
            {"step_title": "Extended Term Amortization", "step_text": "Because boats are durable luxury assets, marine loans extend up to 20 years (240 months). Installment: M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]."}
        ],
        "faqs": [
            {"q": "Can boat loan interest be tax-deductible?", "a": "Yes! If the boat features sleeping quarters, a galley (cooking area), and an installed head (toilet), it may qualify as a second home for IRS mortgage interest deduction purposes."}
        ],
        "js_logic": """
          const price = getNum('boat_price');
          const downPct = getNum('down_pct') / 100;
          const down = price * downPct;
          const P = price - down;
          const r = (getNum('loan_rate') / 100) / 12;
          const n = getNum('loan_term_yrs') * 12;
          const m = r === 0 ? P / n : P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const totalInt = (m * n) - P;

          setDisp('boat_payment', '$' + m.toFixed(2));
          setDisp('down_amt', '$' + Math.round(down).toLocaleString());
          setDisp('total_boat_interest', '$' + Math.round(totalInt).toLocaleString());
        """
    },
    {
        "slug": "rv-loan",
        "category": "finance",
        "name": "RV Loan & Motorhome Financing Calculator",
        "description": "Calculate motorhome, travel trailer, and fifth-wheel monthly installments, sales tax adjustments, and loan amortization.",
        "hero_badge": "Recreational Vehicle • Amortization",
        "formula_display": "M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]",
        "fields": [
            {"id": "rv_price", "label": "RV Purchase Price", "default": 85000, "prefix": "$", "min": 10000, "max": 750000, "step": 5000, "hint": "Price of motorhome or travel trailer"},
            {"id": "rv_down", "label": "Down Payment ($)", "default": 12000, "prefix": "$", "min": 0, "max": 100000, "step": 1000, "hint": "Cash down payment"},
            {"id": "rv_rate", "label": "Interest Rate (%)", "default": 7.49, "suffix": "%", "min": 4, "max": 16, "step": 0.25, "hint": "RV financing APR"},
            {"id": "rv_term_yrs", "label": "Loan Term (Years)", "default": 15, "suffix": "yrs", "min": 5, "max": 20, "step": 5, "hint": "Loan duration (typically 10-20 years)"}
        ],
        "metrics": [
            {"id": "rv_monthly", "label": "Monthly RV Installment", "default_display": "$677.20", "highlight": True},
            {"id": "rv_financed", "label": "Amount Financed", "default_display": "$73,000.00"},
            {"id": "rv_interest", "label": "Total Cumulative Interest", "default_display": "$48,896.00"}
        ],
        "proof_steps": [
            {"step_title": "Financed Balance Computation", "step_text": "P = RV_Price - Down_Payment."},
            {"step_title": "Amortization Resolution", "step_text": "M = P · [i(1 + i)ⁿ] / [(1 + i)ⁿ - 1], where i = APR / 12 and n = years × 12."}
        ],
        "faqs": [
            {"q": "Can an RV qualify as a primary or secondary home for tax deductions?", "a": "Yes! If the RV contains permanent sleeping, cooking, and toilet facilities, loan interest may be deductible under IRS second home rules."}
        ],
        "js_logic": """
          const price = getNum('rv_price');
          const down = getNum('rv_down');
          const P = Math.max(0, price - down);
          const r = (getNum('rv_rate') / 100) / 12;
          const n = getNum('rv_term_yrs') * 12;
          const m = r === 0 ? P / n : P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const intTotal = (m * n) - P;

          setDisp('rv_monthly', '$' + m.toFixed(2));
          setDisp('rv_financed', '$' + Math.round(P).toLocaleString());
          setDisp('rv_interest', '$' + Math.round(intTotal).toLocaleString());
        """
    },
    {
        "slug": "motorcycle-loan",
        "category": "finance",
        "name": "Motorcycle Loan & Financing Calculator",
        "description": "Calculate monthly payments and total interest for new or used motorcycle financing.",
        "hero_badge": "Powersports Lending • Fast Installments",
        "formula_display": "M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]",
        "fields": [
            {"id": "moto_price", "label": "Motorcycle Price", "default": 14500, "prefix": "$", "min": 2000, "max": 60000, "step": 500, "hint": "Purchase price of bike"},
            {"id": "moto_down", "label": "Down Payment", "default": 2000, "prefix": "$", "min": 0, "max": 20000, "step": 500, "hint": "Cash down payment"},
            {"id": "moto_rate", "label": "Interest Rate (%)", "default": 6.99, "suffix": "%", "min": 3, "max": 24, "step": 0.25, "hint": "Powersports financing APR"},
            {"id": "moto_term", "label": "Term (Months)", "default": 48, "suffix": "mo", "min": 24, "max": 84, "step": 12, "hint": "Standard 36 to 60 month terms"}
        ],
        "metrics": [
            {"id": "moto_payment", "label": "Monthly Payment", "default_display": "$299.18", "highlight": True},
            {"id": "moto_interest", "label": "Total Interest", "default_display": "$1,860.64"},
            {"id": "moto_total", "label": "Total Price Paid", "default_display": "$16,360.64"}
        ],
        "proof_steps": [
            {"step_title": "Financed Principal", "step_text": "P = Price - Down_Payment."},
            {"step_title": "Monthly Amortization", "step_text": "M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]."}
        ],
        "faqs": [
            {"q": "What credit score is needed for good motorcycle loan rates?", "a": "A credit score of 720+ unlocks the lowest tier rates (5%-7%), while scores under 650 may see rates between 12% and 20%."}
        ],
        "js_logic": """
          const price = getNum('moto_price');
          const down = getNum('moto_down');
          const P = Math.max(0, price - down);
          const r = (getNum('moto_rate') / 100) / 12;
          const n = getNum('moto_term');
          const m = r === 0 ? P / n : P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const totalInt = (m * n) - P;

          setDisp('moto_payment', '$' + m.toFixed(2));
          setDisp('moto_interest', '$' + Math.round(totalInt).toLocaleString());
          setDisp('moto_total', '$' + Math.round(m * n + down).toLocaleString());
        """
    },
    {
        "slug": "solar-loan",
        "category": "finance",
        "name": "Solar Loan & Energy Payoff Calculator",
        "description": "Calculate residential solar system financing, 30% Federal ITC tax credits, utility bill offsets, and net breakeven return on investment.",
        "hero_badge": "Clean Energy Finance • ITC Tax Credits",
        "formula_display": "Net System Cost = Gross System Cost - 30% Federal Tax Credit",
        "fields": [
            {"id": "system_cost", "label": "Gross Solar System Cost", "default": 28000, "prefix": "$", "min": 10000, "max": 100000, "step": 1000, "hint": "Total turnkey installation cost"},
            {"id": "monthly_electric", "label": "Current Monthly Electric Bill", "default": 220, "prefix": "$", "min": 50, "max": 1000, "step": 10, "hint": "Average pre-solar electric bill"},
            {"id": "solar_rate", "label": "Solar Loan APR (%)", "default": 5.99, "suffix": "%", "min": 2, "max": 14, "step": 0.25, "hint": "Solar financing interest rate"},
            {"id": "solar_term", "label": "Solar Loan Term (Years)", "default": 20, "suffix": "yrs", "min": 10, "max": 25, "step": 5, "hint": "Financing term"}
        ],
        "metrics": [
            {"id": "net_cost", "label": "Net Cost (After 30% Tax Credit)", "default_display": "$19,600.00", "highlight": True},
            {"id": "solar_loan_payment", "label": "Monthly Solar Loan Payment", "default_display": "$140.40"},
            {"id": "net_monthly_savings", "label": "Net Monthly Savings", "default_display": "+$79.60/mo"},
            {"id": "lifetime_electric_savings", "label": "25-Year Net Utility Savings", "default_display": "$32,304.00"}
        ],
        "proof_steps": [
            {"step_title": "Inflation Reduction Act 30% ITC Credit", "step_text": "Federal Residential Clean Energy Credit = Gross Cost × 0.30. Net Cost = Gross Cost × 0.70."},
            {"step_title": "Solar Loan Amortization", "step_text": "M_solar = Net_Cost · [i(1 + i)ⁿ] / [(1 + i)ⁿ - 1]."},
            {"step_title": "Day-One Positive Cash Flow", "step_text": "Monthly Savings = Electric Bill - M_solar."}
        ],
        "faqs": [
            {"q": "How does the 30% Solar Investment Tax Credit work?", "a": "The 30% federal tax credit reduces your federal income tax liability dollar-for-dollar in the tax year your solar system is placed in service. Any unused credit can roll forward to future tax years."}
        ],
        "js_logic": """
          const gross = getNum('system_cost');
          const itc = gross * 0.30;
          const net = gross - itc;
          const bill = getNum('monthly_electric');
          const r = (getNum('solar_rate') / 100) / 12;
          const n = getNum('solar_term') * 12;
          const m = r === 0 ? net / n : net * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const saveMo = bill - m;
          const total25Yrs = (bill * 300) - (m * n);

          setDisp('net_cost', '$' + Math.round(net).toLocaleString());
          setDisp('solar_loan_payment', '$' + m.toFixed(2));
          setDisp('net_monthly_savings', (saveMo >= 0 ? '+$' : '-$') + Math.abs(saveMo).toFixed(2) + '/mo');
          setDisp('lifetime_electric_savings', '$' + Math.round(total25Yrs).toLocaleString());
        """
    },
    {
        "slug": "commercial-mortgage",
        "category": "finance",
        "name": "Commercial Real Estate Mortgage Calculator",
        "description": "Calculate commercial mortgage monthly payments, balloon balances, and debt yields for multifamily, office, and retail properties.",
        "hero_badge": "CRE Financing • Balloon Invariants",
        "formula_display": "M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1] (with Balloon at Year t)",
        "fields": [
            {"id": "loan_amount", "label": "Commercial Loan Amount", "default": 2000000, "prefix": "$", "min": 250000, "max": 50000000, "step": 100000, "hint": "Total CRE debt amount"},
            {"id": "interest_rate", "label": "Interest Rate (%)", "default": 7.25, "suffix": "%", "min": 4, "max": 14, "step": 0.125, "hint": "Fixed commercial interest rate"},
            {"id": "amort_years", "label": "Amortization Schedule (Years)", "default": 25, "suffix": "yrs", "min": 15, "max": 30, "step": 5, "hint": "Base payment amortization period (typically 20-30 yrs)"},
            {"id": "balloon_years", "label": "Loan Maturity / Balloon Term", "default": 10, "suffix": "yrs", "min": 5, "max": 20, "step": 5, "hint": "Time until full balloon payment is due"}
        ],
        "metrics": [
            {"id": "monthly_payment", "label": "Monthly Debt Service", "default_display": "$14,463.14", "highlight": True},
            {"id": "balloon_amount", "label": "Balloon Balance at Maturity", "default_display": "$1,542,880.00"},
            {"id": "total_principal_paid", "label": "Principal Retired at Balloon", "default_display": "$457,120.00"}
        ],
        "proof_steps": [
            {"step_title": "Extended Amortization Baseline", "step_text": "Commercial loans customarily amortize over 25 or 30 years to maintain workable debt-service coverage: M = P · [r(1 + r)ⁿ] / [(1 + r)ⁿ - 1]."},
            {"step_title": "Balloon Balance Invariant", "step_text": "At loan maturity (typically 5, 7, or 10 years), the entire unamortized principal balance B_t is due in full or refinanced."}
        ],
        "faqs": [
            {"q": "What is a balloon payment in commercial real estate?", "a": "A balloon payment is the remaining principal balance due at the end of a commercial loan term (e.g. year 10) when the loan has been amortized over a longer schedule (e.g. 25 years)."}
        ],
        "js_logic": """
          const P = getNum('loan_amount');
          const r = (getNum('interest_rate') / 100) / 12;
          const nAmort = getNum('amort_years') * 12;
          const nBalloon = getNum('balloon_years') * 12;

          const m = r === 0 ? P / nAmort : P * (r * Math.pow(1 + r, nAmort)) / (Math.pow(1 + r, nAmort) - 1);
          let bal = P;
          for (let i = 0; i < nBalloon; i++) {
            const intMo = bal * r;
            const prinMo = m - intMo;
            bal -= prinMo;
          }

          setDisp('monthly_payment', '$' + m.toFixed(2));
          setDisp('balloon_amount', '$' + Math.round(bal).toLocaleString());
          setDisp('total_principal_paid', '$' + Math.round(P - bal).toLocaleString());
        """
    },
    {
        "slug": "dscr-loan",
        "category": "finance",
        "name": "DSCR (Debt Service Coverage Ratio) Calculator",
        "description": "Calculate Debt Service Coverage Ratio (DSCR) and qualify for real estate investor loans without personal income or tax returns.",
        "hero_badge": "Investor Underwriting • DSCR Formula",
        "formula_display": "DSCR = Net Operating Income (NOI) / Annual Debt Service",
        "fields": [
            {"id": "monthly_rent", "label": "Gross Monthly Rental Income", "default": 3500, "prefix": "$", "min": 500, "max": 50000, "step": 100, "hint": "Market rent supported by appraisal (Form 1007)"},
            {"id": "operating_expenses", "label": "Monthly Expenses (Taxes, Ins, HOA)", "default": 650, "prefix": "$", "min": 0, "max": 10000, "step": 50, "hint": "Property taxes, insurance, and HOA dues"},
            {"id": "monthly_pi", "label": "Monthly Principal & Interest", "default": 2100, "prefix": "$", "min": 200, "max": 25000, "step": 50, "hint": "Mortgage P&I payment"}
        ],
        "metrics": [
            {"id": "dscr_ratio", "label": "Debt Service Coverage Ratio (DSCR)", "default_display": "1.36", "highlight": True},
            {"id": "net_operating_income", "label": "Monthly Net Operating Income (NOI)", "default_display": "$2,850.00"},
            {"id": "dscr_status", "label": "Underwriting Qualification", "default_display": "Prime Qualified (DSCR >= 1.25)"}
        ],
        "proof_steps": [
            {"step_title": "Net Operating Income", "step_text": "NOI = Gross Rental Revenue - Operating Expenses (Taxes, Insurance, HOA)."},
            {"step_title": "Debt Service Ratio", "step_text": "DSCR = NOI / Monthly Debt Service (P&I). Ratios >= 1.25 qualify for prime pricing."}
        ],
        "faqs": [
            {"q": "Can you get a DSCR loan with a ratio below 1.0?", "a": "Yes! Some non-QM lenders offer 'no-ratio' or sub-1.0 DSCR programs for properties in prime appreciation markets, typically requiring higher down payments (25%-30%) and cash reserves."}
        ],
        "js_logic": """
          const rent = getNum('monthly_rent');
          const exp = getNum('operating_expenses');
          const pi = getNum('monthly_pi');
          const noi = rent - exp;
          const totalDebtService = pi;
          const dscr = totalDebtService > 0 ? (noi / totalDebtService) : 0;

          setDisp('dscr_ratio', dscr.toFixed(2));
          setDisp('net_operating_income', '$' + Math.round(noi).toLocaleString());

          let status = 'Disqualified (DSCR < 1.0)';
          if (dscr >= 1.25) status = 'Prime Investor Qualified (>= 1.25)';
          else if (dscr >= 1.0) status = 'Standard DSCR Approved (1.0-1.24)';
          setDisp('dscr_status', status);
        """
    },
    {
        "slug": "cap-rate",
        "category": "finance",
        "name": "Cap Rate (Capitalization Rate) Calculator",
        "description": "Calculate commercial and residential real estate Capitalization Rates (Cap Rate) and valuation multiples from Net Operating Income.",
        "hero_badge": "Real Estate Valuation • Cap Rate Matrix",
        "formula_display": "Cap Rate = (Annual Net Operating Income / Current Market Value) × 100%",
        "fields": [
            {"id": "property_price", "label": "Property Purchase Price / Value", "default": 850000, "prefix": "$", "min": 50000, "max": 20000000, "step": 10000, "hint": "Purchase price or current market value"},
            {"id": "gross_annual_rent", "label": "Gross Annual Rental Revenue", "default": 96000, "prefix": "$", "min": 5000, "max": 2000000, "step": 2500, "hint": "Total scheduled annual rent"},
            {"id": "annual_operating_costs", "label": "Annual Operating Expenses", "default": 28000, "prefix": "$", "min": 0, "max": 1000000, "step": 1000, "hint": "Property taxes, insurance, repairs, vacancy, management"}
        ],
        "metrics": [
            {"id": "cap_rate_pct", "label": "Capitalization Rate (Cap Rate)", "default_display": "8.00%", "highlight": True},
            {"id": "net_operating_income", "label": "Annual Net Operating Income (NOI)", "default_display": "$68,000.00"},
            {"id": "gross_rent_multiplier", "label": "Gross Rent Multiplier (GRM)", "default_display": "8.85x"}
        ],
        "proof_steps": [
            {"step_title": "NOI Derivation", "step_text": "Annual NOI = Gross Scheduled Rent - Operating Expenses."},
            {"step_title": "Unleveraged Yield Invariant", "step_text": "Cap Rate = (Annual NOI / Property Asset Value) × 100%. Represents the unleveraged rate of return."}
        ],
        "faqs": [
            {"q": "What is a good cap rate for rental property?", "a": "A good cap rate typically ranges between 5% and 10%, depending on property asset class, tenant creditworthiness, and geographical market tier."}
        ],
        "js_logic": """
          const V = getNum('property_price');
          const rent = getNum('gross_annual_rent');
          const exp = getNum('annual_operating_costs');
          const noi = rent - exp;
          const cap = V > 0 ? (noi / V) * 100 : 0;
          const grm = rent > 0 ? (V / rent) : 0;

          setDisp('cap_rate_pct', cap.toFixed(2) + '%');
          setDisp('net_operating_income', '$' + Math.round(noi).toLocaleString());
          setDisp('gross_rent_multiplier', grm.toFixed(2) + 'x');
        """
    },
    {
        "slug": "rental-cash-flow",
        "category": "finance",
        "name": "Rental Property Cash Flow & ROI Calculator",
        "description": "Calculate monthly net cash flow, Cash-on-Cash Return (CoC), and expense ratios for residential investment real estate.",
        "hero_badge": "Real Estate ROI • Cash-on-Cash",
        "formula_display": "Cash-on-Cash Return = (Annual Net Cash Flow / Total Cash Invested) × 100%",
        "fields": [
            {"id": "monthly_rent", "label": "Monthly Rental Income", "default": 2800, "prefix": "$", "min": 500, "max": 25000, "step": 50, "hint": "Gross rent collected"},
            {"id": "monthly_mortgage", "label": "Monthly Mortgage (P&I)", "default": 1450, "prefix": "$", "min": 0, "max": 15000, "step": 50, "hint": "Debt service payment"},
            {"id": "monthly_taxes_ins", "label": "Monthly Taxes & Insurance", "default": 420, "prefix": "$", "min": 0, "max": 5000, "step": 25, "hint": "Property tax and hazard insurance"},
            {"id": "capex_vacancy_pct", "label": "CapEx, Maintenance & Vacancy (%)", "default": 15, "suffix": "%", "min": 5, "max": 30, "step": 1, "hint": "Reserves for maintenance and downtime"},
            {"id": "total_cash_invested", "label": "Total Initial Cash Invested", "default": 75000, "prefix": "$", "min": 5000, "max": 500000, "step": 2500, "hint": "Down payment + closing costs + rehab"}
        ],
        "metrics": [
            {"id": "net_monthly_cashflow", "label": "Net Monthly Cash Flow", "default_display": "$510.00", "highlight": True},
            {"id": "annual_cashflow", "label": "Annual Net Cash Flow", "default_display": "$6,120.00"},
            {"id": "cash_on_cash_return", "label": "Cash-on-Cash Return (CoC)", "default_display": "8.16%"}
        ],
        "proof_steps": [
            {"step_title": "Reserve Budgeting", "step_text": "Reserves = Monthly Rent × (CapEx_Pct / 100)."},
            {"step_title": "Net Monthly Flow", "step_text": "Cash Flow = Rent - Mortgage - Taxes/Ins - Reserves."},
            {"step_title": "Cash-on-Cash Formula", "step_text": "CoC = (Annual Cash Flow / Total Cash Invested) × 100%."}
        ],
        "faqs": [
            {"q": "What is the difference between Cap Rate and Cash-on-Cash Return?", "a": "Cap rate evaluates property performance without debt (unleveraged), whereas Cash-on-Cash return measures your actual leveraged return on cash equity out-of-pocket."}
        ],
        "js_logic": """
          const rent = getNum('monthly_rent');
          const m = getNum('monthly_mortgage');
          const ti = getNum('monthly_taxes_ins');
          const reserves = rent * (getNum('capex_vacancy_pct') / 100);
          const cfMo = rent - m - ti - reserves;
          const cfYr = cfMo * 12;
          const invested = getNum('total_cash_invested');
          const coc = invested > 0 ? (cfYr / invested) * 100 : 0;

          setDisp('net_monthly_cashflow', (cfMo >= 0 ? '$' : '-$') + Math.abs(cfMo).toFixed(2));
          setDisp('annual_cashflow', (cfYr >= 0 ? '$' : '-$') + Math.round(Math.abs(cfYr)).toLocaleString());
          setDisp('cash_on_cash_return', coc.toFixed(2) + '%');
        """
    },
    {
        "slug": "brrrr",
        "category": "finance",
        "name": "BRRRR Real Estate Investment Calculator",
        "description": "Analyze Buy, Rehab, Rent, Refinance, Repeat (BRRRR) transactions. Calculate cash left in the deal and velocity of capital.",
        "hero_badge": "Real Estate Wealth • Capital Velocity",
        "formula_display": "Cash Left in Deal = (Purchase + Rehab Costs) - New Refinance Loan (75% ARV)",
        "fields": [
            {"id": "purchase_price", "label": "Purchase Price", "default": 160000, "prefix": "$", "min": 20000, "max": 1000000, "step": 5000, "hint": "Acquisition price"},
            {"id": "rehab_cost", "label": "Rehabilitation / Renovation Budget", "default": 45000, "prefix": "$", "min": 5000, "max": 500000, "step": 2500, "hint": "Total repair costs"},
            {"id": "arv", "label": "After-Repair Value (ARV)", "default": 280000, "prefix": "$", "min": 50000, "max": 1500000, "step": 5000, "hint": "Appraised value post-renovation"},
            {"id": "refi_ltv", "label": "Cash-Out Refi LTV (%)", "default": 75, "suffix": "%", "min": 65, "max": 80, "step": 5, "hint": "Typically 75% LTV on cash-out refi"}
        ],
        "metrics": [
            {"id": "cash_left", "label": "Net Cash Left in Deal", "default_display": "-$5,000.00 (Infinite Return)", "highlight": True},
            {"id": "new_loan_amount", "label": "New Refinanced Loan Balance", "default_display": "$210,000.00"},
            {"id": "built_in_equity", "label": "Instant Built-In Equity", "default_display": "$70,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Total Initial Investment", "step_text": "All-In Capital = Purchase Price + Rehab Budget + Holding Costs."},
            {"step_title": "Cash-Out Refinance Invariant", "step_text": "New Loan = ARV × Refi_LTV. Cash Left = All-In Capital - New Loan. If Cash Left <= 0, the investor achieves an infinite return on capital."}
        ],
        "faqs": [
            {"q": "What is an 'infinite return' in the BRRRR strategy?", "a": "An infinite return occurs when the cash-out refinance returns 100% or more of your invested capital, allowing you to own a cash-flowing asset with zero net dollars left in the deal."}
        ],
        "js_logic": """
          const pur = getNum('purchase_price');
          const rehab = getNum('rehab_cost');
          const allIn = pur + rehab;
          const arv = getNum('arv');
          const ltv = getNum('refi_ltv') / 100;
          const newLoan = arv * ltv;
          const cashLeft = allIn - newLoan;
          const equity = arv - newLoan;

          setDisp('new_loan_amount', '$' + Math.round(newLoan).toLocaleString());
          setDisp('built_in_equity', '$' + Math.round(equity).toLocaleString());
          if (cashLeft <= 0) {
            setDisp('cash_left', '$0.00 (100% Capital Recovered)');
          } else {
            setDisp('cash_left', '$' + Math.round(cashLeft).toLocaleString());
          }
        """
    },
    {
        "slug": "hard-money-loan",
        "category": "finance",
        "name": "Hard Money & Fix-and-Flip Loan Calculator",
        "description": "Calculate short-term bridge and hard money loan costs, origination points, interest reserves, and net flip profit margins.",
        "hero_badge": "Bridge Lending • Fix-and-Flip Math",
        "formula_display": "Total Financing Cost = (Loan Amount · Origination Points %) + Monthly Interest · Term",
        "fields": [
            {"id": "loan_amount", "label": "Hard Money Loan Amount", "default": 220000, "prefix": "$", "min": 25000, "max": 2000000, "step": 5000, "hint": "Loan covering purchase and/or rehab"},
            {"id": "interest_rate", "label": "Interest Rate (%)", "default": 11.5, "suffix": "%", "min": 7, "max": 18, "step": 0.25, "hint": "Annual interest-only rate"},
            {"id": "origination_points", "label": "Origination Points (%)", "default": 2.0, "suffix": "pts", "min": 0, "max": 5, "step": 0.5, "hint": "Upfront points charged by lender"},
            {"id": "term_months", "label": "Project Duration (Months)", "default": 6, "suffix": "mo", "min": 3, "max": 24, "step": 1, "hint": "Months to complete rehab and sell"}
        ],
        "metrics": [
            {"id": "monthly_interest", "label": "Monthly Interest Payment", "default_display": "$2,108.33", "highlight": True},
            {"id": "points_cost", "label": "Upfront Points Fee", "default_display": "$4,400.00"},
            {"id": "total_carrying_cost", "label": "Total Hard Money Cost", "default_display": "$17,050.00"}
        ],
        "proof_steps": [
            {"step_title": "Origination Points", "step_text": "Points Fee = Loan Amount × (Points_Pct / 100)."},
            {"step_title": "Monthly Interest Holding Cost", "step_text": "Monthly Interest = Loan Amount × (Rate / 1200)."},
            {"step_title": "Total Loan Cost", "step_text": "Total = Points Fee + (Monthly Interest × Months)."}
        ],
        "faqs": [
            {"q": "What is the difference between hard money and conventional financing?", "a": "Hard money loans are asset-based short-term loans funded by private lenders focusing on property collateral and ARV rather than personal W-2 income."}
        ],
        "js_logic": """
          const L = getNum('loan_amount');
          const r = (getNum('interest_rate') / 100) / 12;
          const pts = L * (getNum('origination_points') / 100);
          const mos = getNum('term_months');
          const moInt = L * r;
          const totalCost = pts + (moInt * mos);

          setDisp('monthly_interest', '$' + moInt.toFixed(2));
          setDisp('points_cost', '$' + Math.round(pts).toLocaleString());
          setDisp('total_carrying_cost', '$' + Math.round(totalCost).toLocaleString());
        """
    },
    {
        "slug": "roth-ira-conversion",
        "category": "finance",
        "name": "Roth IRA Conversion & Tax Optimizer",
        "description": "Calculate conversion income taxes, future tax-free growth advantages, and optimal tax bracket filling when converting Traditional IRAs to Roth.",
        "hero_badge": "Tax Optimization • Compound Exemption",
        "formula_display": "Future Tax-Free Advantage = FV_Roth - (FV_Traditional - Future Taxes)",
        "fields": [
            {"id": "conversion_amount", "label": "Amount to Convert ($)", "default": 50000, "prefix": "$", "min": 5000, "max": 500000, "step": 5000, "hint": "Pre-tax IRA dollars converted to Roth"},
            {"id": "current_tax_rate", "label": "Current Marginal Tax Rate (%)", "default": 24, "suffix": "%", "min": 10, "max": 40, "step": 1, "hint": "Federal + state tax bracket today"},
            {"id": "future_tax_rate", "label": "Expected Retirement Tax Rate (%)", "default": 28, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Expected tax bracket in retirement"},
            {"id": "growth_years", "label": "Years Until Retirement", "default": 18, "suffix": "yrs", "min": 1, "max": 40, "step": 1, "hint": "Investment horizon"},
            {"id": "growth_rate", "label": "Annual Investment Return (%)", "default": 7.5, "suffix": "%", "min": 3, "max": 15, "step": 0.5, "hint": "Assumed annualized compound return"}
        ],
        "metrics": [
            {"id": "tax_due_now", "label": "Immediate Tax Due on Conversion", "default_display": "$12,000.00", "highlight": True},
            {"id": "future_roth_value", "label": "Future 100% Tax-Free Roth Balance", "default_display": "$183,790.00"},
            {"id": "net_tax_alpha", "label": "Net Tax Alpha / Savings", "default_display": "+$7,351.00"}
        ],
        "proof_steps": [
            {"step_title": "Upfront Tax Obligation", "step_text": "Tax Due = Conversion Amount × Current Marginal Tax Rate."},
            {"step_title": "Compounding Symmetry", "step_text": "If tax rates are identical today and in retirement, Traditional and Roth produce mathematically equal net wealth. If future tax rates rise (t_future > t_current), Roth conversion produces significant tax alpha."}
        ],
        "faqs": [
            {"q": "Should I pay Roth conversion taxes out of the converted balance?", "a": "No! You should always pay conversion taxes with outside non-retirement cash reserves. Withholding taxes from the conversion reduces compound principal and may trigger early withdrawal penalties if under age 59½."}
        ],
        "js_logic": """
          const C = getNum('conversion_amount');
          const tNow = getNum('current_tax_rate') / 100;
          const tFut = getNum('future_tax_rate') / 100;
          const yrs = getNum('growth_years');
          const r = getNum('growth_rate') / 100;

          const taxNow = C * tNow;
          const futureGross = C * Math.pow(1 + r, yrs);
          const futureTradNet = futureGross * (1 - tFut);
          const futureTaxPaidTrad = (taxNow * Math.pow(1 + r, yrs));
          const netBenefit = futureGross - (futureTradNet + futureTaxPaidTrad);

          setDisp('tax_due_now', '$' + Math.round(taxNow).toLocaleString());
          setDisp('future_roth_value', '$' + Math.round(futureGross).toLocaleString());
          setDisp('net_tax_alpha', (netBenefit >= 0 ? '+$' : '-$') + Math.round(Math.abs(netBenefit)).toLocaleString());
        """
    },
    {
        "slug": "traditional-vs-roth",
        "category": "finance",
        "name": "Traditional vs Roth 401(k) / IRA Calculator",
        "description": "Compare pre-tax Traditional retirement savings against post-tax Roth contributions based on career income progression and tax brackets.",
        "hero_badge": "Retirement Taxation • Horizon Comparison",
        "formula_display": "Roth Wealth = P · (1 - t_0) · (1 + r)ⁿ vs Traditional Wealth = [P · (1 + r)ⁿ] · (1 - t_n)",
        "fields": [
            {"id": "annual_contrib", "label": "Annual Contribution", "default": 12000, "prefix": "$", "min": 1000, "max": 69000, "step": 1000, "hint": "Annual investment amount"},
            {"id": "current_tax", "label": "Current Tax Bracket (%)", "default": 24, "suffix": "%", "min": 10, "max": 45, "step": 1, "hint": "Marginal tax bracket today"},
            {"id": "retirement_tax", "label": "Retirement Tax Bracket (%)", "default": 22, "suffix": "%", "min": 10, "max": 45, "step": 1, "hint": "Expected bracket when withdrawing"},
            {"id": "years_invested", "label": "Years of Investing", "default": 25, "suffix": "yrs", "min": 5, "max": 45, "step": 5, "hint": "Timeline until retirement"},
            {"id": "annual_return", "label": "Annual Return (%)", "default": 7.0, "suffix": "%", "min": 3, "max": 14, "step": 0.5, "hint": "Annual compound return"}
        ],
        "metrics": [
            {"id": "roth_spendable", "label": "Roth Spendable Nest Egg", "default_display": "$573,950.00", "highlight": True},
            {"id": "traditional_spendable", "label": "Traditional Spendable Nest Egg", "default_display": "$589,050.00"},
            {"id": "winner_recommendation", "label": "Optimal Wealth Vehicle", "default_display": "Traditional 401(k) Advantage (+2.6%)"}
        ],
        "proof_steps": [
            {"step_title": "Mathematical Equivalence Under Constant Tax", "step_text": "Because multiplication is commutative: A(1 - t)(1 + r)ⁿ ≡ A(1 + r)ⁿ(1 - t). The decision hinges strictly on whether t_current > t_retirement or vice versa."}
        ],
        "faqs": [
            {"q": "When is Roth definitely better?", "a": "Roth is superior when you are in an early career lower tax bracket (10%-12%) and expect your retirement lifestyle or legislative tax rates to be higher."}
        ],
        "js_logic": """
          const pmt = getNum('annual_contrib');
          const t0 = getNum('current_tax') / 100;
          const tn = getNum('retirement_tax') / 100;
          const yrs = getNum('years_invested');
          const r = getNum('annual_return') / 100;

          // Future value of ordinary annuity
          const fvAnnuity = pmt * (Math.pow(1 + r, yrs) - 1) / r;
          const tradSpendable = fvAnnuity * (1 - tn);
          // For equal take-home cash:
          const rothPmt = pmt * (1 - t0);
          const rothSpendable = (rothPmt * (Math.pow(1 + r, yrs) - 1) / r) + (pmt * t0 * Math.pow(1 + r, yrs) * (1 - t0)); // Assuming tax savings invested

          setDisp('traditional_spendable', '$' + Math.round(tradSpendable).toLocaleString());
          setDisp('roth_spendable', '$' + Math.round(fvAnnuity * (1 - t0)).toLocaleString());

          if (t0 > tn) {
            setDisp('winner_recommendation', 'Traditional Advantaged (Lower future bracket)');
          } else if (t0 < tn) {
            setDisp('winner_recommendation', 'Roth Advantaged (Higher future bracket)');
          } else {
            setDisp('winner_recommendation', 'Identical Yield (Equal tax brackets)');
          }
        """
    }
]
