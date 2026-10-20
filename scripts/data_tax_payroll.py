"""
scripts/data_tax_payroll.py
25 High-Value Tax, Payroll, Executive Compensation & Retirement Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

TAX_PAYROLL_CALCULATORS = [
    {
        "slug": "w2-vs-1099",
        "category": "finance",
        "name": "W-2 Employee vs 1099 Contractor Net Pay Calculator",
        "description": "Compare net take-home pay between W-2 employment and 1099 independent contractor arrangements, factoring in 15.3% self-employment tax, benefits, and write-offs.",
        "hero_badge": "Tax Optimization • W-2 vs 1099 Matrix",
        "formula_display": "1099 Breakeven = W-2 Salary × 1.30 (to offset FICA + Health + PTO + Retirement)",
        "fields": [
            {"id": "w2_base_salary", "label": "W-2 Base Annual Salary", "default": 100000, "prefix": "$", "min": 20000, "max": 1000000, "step": 5000, "hint": "Current or offered W-2 compensation"},
            {"id": "offered_1099_rate", "label": "Equivalent 1099 Hourly Rate", "default": 65.00, "prefix": "$", "min": 15.00, "max": 500.00, "step": 5.00, "hint": "Quoted hourly contract consulting rate"},
            {"id": "billable_hours_per_year", "label": "Billable Hours per Year", "default": 1920, "suffix": "hours", "min": 500, "max": 2500, "step": 40, "hint": "Standard full-time: ~1,920 - 2,000 billable hours"},
            {"id": "annual_1099_business_expenses", "label": "Estimated 1099 Business Tax Write-offs", "default": 8500, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Home office, laptop, software, vehicle deductions"}
        ],
        "metrics": [
            {"id": "net_w2_take_home", "label": "W-2 Estimated Net Take-Home Pay", "default_display": "$74,800.00 / yr", "highlight": True},
            {"id": "net_1099_take_home", "label": "1099 Estimated Net Take-Home Pay", "default_display": "$85,420.00 / yr", "highlight": True},
            {"id": "recommended_contract_rate", "label": "1099 Breakeven Hourly Target", "default_display": "$67.71 / hr", "highlight": True},
            {"id": "self_employment_tax_burden", "label": "1099 Self-Employment (FICA) Tax", "default_display": "$16,420.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Self-Employment Tax Disparity", "step_text": "W-2 employees pay 7.65% FICA while their employer pays the matching 7.65%. A 1099 contractor pays both halves: the full 15.3% Self-Employment Tax on net profit."},
            {"step_title": "Fringe Benefits Economic Value", "step_text": "W-2 jobs provide employer-subsidized health insurance ($7,500/yr), paid time off ($6,000 value), and 401(k) matches (~$3,000). Total benefits add 25% to 35% above base salary."},
            {"step_title": "The 1.30x Multiplier Rule", "step_text": "To achieve identical net financial lifestyle parity, a 1099 contractor must bill at least 30% to 40% more than an equivalent W-2 salary."}
        ],
        "faqs": [
            {"q": "What tax write-offs can a 1099 independent contractor claim?", "a": "1099 contractors can deduct business equipment (computers, phones), home office square footage, health insurance premiums, professional travel, client meals (50%), retirement plan contributions (SEP-IRA / Solo 401k), and the 20% Section 199A QBI deduction."},
            {"q": "Why is 1099 hourly rate always higher than W-2 hourly rate?", "a": "1099 contractors must self-fund health insurance, unpaid vacation/sick time, employer FICA taxes, billing software, and accounting overhead."}
        ],
        "js_logic": """
          const w2 = getNum('w2_base_salary');
          const rate1099 = getNum('offered_1099_rate');
          const hours = getNum('billable_hours_per_year') || 1920;
          const expenses = getNum('annual_1099_business_expenses');

          const gross1099 = rate1099 * hours;
          const net1099Profit = Math.max(0, gross1099 - expenses);

          // W2 calculations
          const w2Fica = Math.min(168600, w2) * 0.062 + (w2 * 0.0145);
          const w2FedTax = w2 * 0.175; // average blended
          const netW2 = w2 - w2Fica - w2FedTax;

          // 1099 calculations
          const seTax = (net1099Profit * 0.9235) * 0.153;
          const seDeduction = seTax * 0.50;
          const taxable1099 = Math.max(0, net1099Profit - seDeduction);
          const fedTax1099 = taxable1099 * 0.175;
          const healthSelf = 6000;
          const net1099 = gross1099 - expenses - seTax - fedTax1099 - healthSelf;

          const breakevenGross = (w2 * 1.30);
          const breakevenRate = breakevenGross / hours;

          setDisp('net_w2_take_home', '$' + Math.round(netW2).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('net_1099_take_home', '$' + Math.round(net1099).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('recommended_contract_rate', '$' + breakevenRate.toFixed(2) + ' / hr');
          setDisp('self_employment_tax_burden', '$' + Math.round(seTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    },
    {
        "slug": "paycheck-withholding",
        "category": "finance",
        "name": "Federal Paycheck Withholding & Net Pay Calculator",
        "description": "Calculate exact net paycheck take-home pay after federal income tax, Social Security (6.2%), Medicare (1.45%), and pre-tax deductions.",
        "hero_badge": "Payroll Engineering • Net Paycheck Matrix",
        "formula_display": "Net Paycheck = Gross Pay - Pre-Tax Deductions - FICA Taxes - Federal Withholding",
        "fields": [
            {"id": "annual_gross_pay", "label": "Annual Gross Salary", "default": 85000, "prefix": "$", "min": 15000, "max": 1000000, "step": 2500, "hint": "Base salary before deductions"},
            {"id": "pay_frequency_periods", "label": "Pay Frequency (12 Monthly, 24 Semi-Monthly, 26 Bi-Weekly, 52 Weekly)", "default": 26, "min": 12, "max": 52, "step": 1, "hint": "26 = Bi-weekly (every 2 weeks); 24 = 2x per month"},
            {"id": "pretax_401k_pct", "label": "Pre-Tax 401(k) / HSA Contribution (%)", "default": 6.0, "suffix": "%", "min": 0.0, "max": 50.0, "step": 0.5, "hint": "Pre-tax deduction percentage"},
            {"id": "filing_status_fed", "label": "Tax Filing Status (1 = Single, 2 = Married Filing Jointly)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1 = Single, 2 = Married"}
        ],
        "metrics": [
            {"id": "net_take_home_paycheck", "label": "Net Take-Home Pay per Paycheck", "default_display": "$2,352.40", "highlight": True},
            {"id": "gross_pay_per_period", "label": "Gross Pay per Paycheck", "default_display": "$3,269.23", "highlight": True},
            {"id": "total_annual_fica_tax", "label": "Annual FICA (Social Security + Medicare)", "default_display": "$6,502.50 / yr"},
            {"id": "annual_net_take_home", "label": "Annual Cumulative Net Take-Home", "default_display": "$61,162.40 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Pre-Tax Deductions Shield", "step_text": "Pre-tax 401(k) and health contributions reduce taxable wages for federal income tax, though FICA taxes still apply to gross wages."},
            {"step_title": "FICA Mandatory Payroll Tax", "step_text": "Social Security tax is 6.2% up to the annual wage cap ($168,600). Medicare tax is 1.45% on all earnings uncapped (with 0.9% additional surcharge over $200k)."},
            {"step_title": "Federal Progressive Bracket Withholding", "step_text": "Withholding mirrors federal income tax brackets (10%, 12%, 22%, 24%) after subtracting the standard deduction allowance."}
        ],
        "faqs": [
            {"q": "Why is my bonus taxed at a higher rate than my normal paycheck?", "a": "Bonuses are classified as supplemental wages. The IRS mandates a flat 22% federal withholding rate on bonuses up to $1M (37% over $1M), which may be higher or lower than your actual marginal bracket when filing your annual return."},
            {"q": "What is the 2024 Social Security wage base limit?", "a": "For 2024, the Social Security wage cap is $168,600. Earnings above this amount are exempt from the 6.2% Social Security tax."}
        ],
        "js_logic": """
          const gross = getNum('annual_gross_pay');
          const periods = getNum('pay_frequency_periods') || 26;
          const pretaxPct = (getNum('pretax_401k_pct') || 6.0) / 100;
          const status = getNum('filing_status_fed');

          const grossPeriod = gross / periods;
          const pretaxPeriod = grossPeriod * pretaxPct;
          const ficaSocial = Math.min(168600, gross) * 0.062 / periods;
          const ficaMed = (grossPeriod * 0.0145);
          const totalFicaPeriod = ficaSocial + ficaMed;

          const taxableGrossAnnual = Math.max(0, gross - (gross * pretaxPct));
          const stdDed = status === 2 ? 29200 : 14600;
          const taxableIncome = Math.max(0, taxableGrossAnnual - stdDed);

          // Progressive tax approximation
          let fedAnnualTax = 0;
          if (taxableIncome > 0) {
            fedAnnualTax = taxableIncome * (status === 2 ? 0.12 : 0.145);
          }
          const fedPeriod = fedAnnualTax / periods;

          const netPeriod = grossPeriod - pretaxPeriod - totalFicaPeriod - fedPeriod;
          const netAnnual = netPeriod * periods;

          setDisp('net_take_home_paycheck', '$' + netPeriod.toFixed(2));
          setDisp('gross_pay_per_period', '$' + grossPeriod.toFixed(2));
          setDisp('total_annual_fica_tax', '$' + (totalFicaPeriod * periods).toFixed(2) + ' / yr');
          setDisp('annual_net_take_home', '$' + Math.round(netAnnual).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    },
    {
        "slug": "s-corp-reasonable-salary",
        "category": "finance",
        "name": "S-Corporation Reasonable Salary & Tax Savings Calculator",
        "description": "Calculate annual FICA self-employment tax savings from electing S-Corp status, optimizing reasonable compensation salary versus shareholder distributions.",
        "hero_badge": "Corporate Tax Strategy • S-Corp FICA Matrix",
        "formula_display": "FICA Savings = (Net Business Profit - Reasonable Salary) × 15.3%",
        "fields": [
            {"id": "net_business_profit", "label": "Annual Net Business Profit", "default": 160000, "prefix": "$", "min": 30000, "max": 2000000, "step": 5000, "hint": "Gross revenue minus all operating expenses"},
            {"id": "reasonable_salary_target", "label": "Justifiable Reasonable W-2 Salary", "default": 70000, "prefix": "$", "min": 20000, "max": 500000, "step": 5000, "hint": "Defensible salary for your role under IRS standards"},
            {"id": "corporate_compliance_costs", "label": "Annual Payroll & CPA Filing Fees", "default": 2200, "prefix": "$", "min": 500, "max": 10000, "step": 100, "hint": "Gusto/ADP payroll + Form 1120-S corporate tax return"}
        ],
        "metrics": [
            {"id": "net_annual_tax_savings", "label": "Net Annual Cash Tax Savings", "default_display": "$11,570.00 / yr", "highlight": True},
            {"id": "shareholder_distribution", "label": "FICA-Free Shareholder Distributions", "default_display": "$90,000.00", "highlight": True},
            {"id": "gross_fica_savings", "label": "Gross FICA Self-Employment Tax Saved", "default_display": "$13,770.00 / yr"},
            {"id": "s_corp_threshold_rating", "label": "S-Corp Viability Verdict", "default_display": "Highly Profitable Election (Saves > $5k/yr)"}
        ],
        "proof_steps": [
            {"step_title": "Sole Proprietorship FICA Exposure", "step_text": "In a standard LLC or sole proprietorship, 100% of the $160,000 net profit is subject to the 15.3% self-employment tax ($24,480 total)."},
            {"step_title": "S-Corp Distribution Exemption", "step_text": "Under an S-Corp, FICA taxes apply ONLY to the $70,000 W-2 reasonable salary. The remaining $90,000 is taken as a shareholder profit distribution, which is 100% exempt from FICA taxes."},
            {"step_title": "Net Economic Benefit", "step_text": "Gross Tax Savings = $90,000 × 15.3% = $13,770. Subtracting $2,200 for payroll processing and corporate CPA returns yields $11,570 in clean annual cash tax savings."}
        ],
        "faqs": [
            {"q": "What is the minimum profit where an S-Corp election makes sense?", "a": "An S-Corp election typically makes financial sense once net profit consistently exceeds $80,000 to $100,000 per year, which generates enough FICA tax savings to easily outweigh the $1,500 to $2,500 in added payroll and accounting compliance costs."},
            {"q": "How does the IRS determine 'Reasonable Compensation'?", "a": "The IRS looks at RCReports data, Bureau of Labor Statistics (BLS) wage data for your job title, hours worked, business complexity, and compensation paid to comparable non-owner employees. Paying yourself a $10,000 salary on $200k profit is an immediate audit trigger."}
        ],
        "js_logic": """
          const profit = getNum('net_business_profit');
          const salary = getNum('reasonable_salary_target');
          const fees = getNum('corporate_compliance_costs');

          const distributions = Math.max(0, profit - salary);
          // Social Security cap factor
          const ficaRate = 0.153;
          const grossSavings = distributions * ficaRate;
          const netSavings = Math.max(0, grossSavings - fees);

          let verdict = 'Highly Profitable Election (Saves > $5k/yr)';
          if (netSavings <= 0) verdict = 'NOT Recommended: Profit too low to offset CPA fees';
          else if (netSavings < 3000) verdict = 'Marginal Benefit (Under $3k net savings)';

          setDisp('net_annual_tax_savings', '$' + Math.round(netSavings).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('shareholder_distribution', '$' + Math.round(distributions).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('gross_fica_savings', '$' + Math.round(grossSavings).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('s_corp_threshold_rating', verdict);
        """
    },
    {
        "slug": "qbi-deduction",
        "category": "finance",
        "name": "Section 199A Qualified Business Income (QBI) Calculator",
        "description": "Calculate the 20% Section 199A QBI deduction for pass-through entities (LLCs, S-Corps, partnerships), testing Specified Service Trade or Business (SSTB) thresholds.",
        "hero_badge": "Pass-Through Tax Policy • Section 199A Matrix",
        "formula_display": "QBI Deduction = Qualified Business Income × 20% (Subject to Wage / Property Caps)",
        "fields": [
            {"id": "qualified_business_income", "label": "Qualified Business Income (QBI)", "default": 140000, "prefix": "$", "min": 10000, "max": 5000000, "step": 5000, "hint": "Net domestic profit from eligible pass-through trade/business"},
            {"id": "taxable_income_total", "label": "Total Taxable Income on Form 1040", "default": 165000, "prefix": "$", "min": 20000, "max": 5000000, "step": 5000, "hint": "Total taxable income before QBI deduction"},
            {"id": "sstb_business_flag", "label": "Specified Service Business (Law, Health, Consulting, Finance)", "default": 0, "min": 0, "max": 1, "step": 1, "hint": "0 = Non-SSTB (Real estate, tech, retail); 1 = SSTB (Doctors, lawyers, consultants)"},
            {"id": "filing_status_qbi", "label": "Filing Status (1 = Single, 2 = Married Filing Jointly)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "Determines phase-out threshold"}
        ],
        "metrics": [
            {"id": "qbi_deduction_amount", "label": "Section 199A QBI Tax Deduction", "default_display": "$28,000.00", "highlight": True},
            {"id": "effective_tax_savings_qbi", "label": "Estimated Federal Tax Saved (24% Bracket)", "default_display": "$6,720.00 Cash Saved", "highlight": True},
            {"id": "phaseout_limitation_status", "label": "Threshold & Phase-Out Status", "default_display": "Below Threshold (100% Full Deduction)", "highlight": True},
            {"id": "effective_taxable_qbi", "label": "Taxable Profit After 20% Deduction", "default_display": "$112,000.00"}
        ],
        "proof_steps": [
            {"step_title": "The 20% Pass-Through Deduction Rule", "step_text": "Taxpayers operating sole proprietorships, partnerships, or S-Corps can deduct up to 20% of net qualified business income directly off their personal tax return."},
            {"step_title": "SSTB Threshold Limits", "step_text": "For 2024, the full 20% deduction is available to all businesses below taxable income thresholds ($191,950 Single / $383,900 MFJ)."},
            {"step_title": "High-Income Phase-Out Restrictions", "step_text": "Above the threshold, Specified Service Trades (doctors, lawyers, accountants, consultants) completely phase out. Non-service businesses are limited by W-2 wages paid."}
        ],
        "faqs": [
            {"q": "What businesses are classified as SSTBs under Section 199A?", "a": "Specified Service Trades or Businesses include healthcare (doctors, dentists), law, accounting, actuarial science, performing arts, consulting, athletics, financial services, and brokerage services. Engineers and architects are explicitly excluded from SSTB restrictions."},
            {"q": "Does rental real estate qualify for the 20% QBI deduction?", "a": "Yes! Rental real estate qualifies under IRS safe harbor Rev. Proc. 2019-38 if you maintain separate books, perform at least 250 hours of rental services annually, and maintain contemporaneous service logs."}
        ],
        "js_logic": """
          const qbi = getNum('qualified_business_income');
          const taxable = getNum('taxable_income_total');
          const isSstb = getNum('sstb_business_flag') === 1;
          const status = getNum('filing_status_qbi');

          const threshold = status === 2 ? 383900 : 191950;
          const phaseoutRange = status === 2 ? 100000 : 50000;

          let deduction = qbi * 0.20;
          let phaseStatus = 'Below Threshold (100% Full Deduction)';

          if (taxable > threshold + phaseoutRange) {
            if (isSstb) {
              deduction = 0;
              phaseStatus = 'Fully Phased Out (SSTB over limit)';
            } else {
              phaseStatus = 'Above Threshold (Subject to W-2 Wage Caps)';
            }
          } else if (taxable > threshold) {
            phaseStatus = 'In Phase-Out Range (Partial Reduction)';
            const factor = 1 - ((taxable - threshold) / phaseoutRange);
            if (isSstb) deduction *= factor;
          }

          const taxSaved = deduction * 0.24;

          setDisp('qbi_deduction_amount', '$' + Math.round(deduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('effective_tax_savings_qbi', '$' + Math.round(taxSaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Cash Saved');
          setDisp('phaseout_limitation_status', phaseStatus);
          setDisp('effective_taxable_qbi', '$' + Math.round(qbi - deduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "401k-employer-match",
        "category": "finance",
        "name": "401(k) Employer Match & True Compensation Calculator",
        "description": "Calculate employer 401(k) matching dollars, required employee contribution to maximize match, vesting schedules, and 30-year compound growth.",
        "hero_badge": "Retirement Planning • 401(k) Match Matrix",
        "formula_display": "Employer Match = Salary × min(Employee Contribution %, Max Match Cap %) × Match Rate %",
        "fields": [
            {"id": "employee_base_salary", "label": "Annual Gross Salary", "default": 95000, "prefix": "$", "min": 20000, "max": 500000, "step": 5000, "hint": "Base annual compensation"},
            {"id": "employee_contribution_pct", "label": "Your 401(k) Contribution (%)", "default": 6.0, "suffix": "%", "min": 1.0, "max": 50.0, "step": 0.5, "hint": "Percentage of salary contributed"},
            {"id": "match_rate_pct", "label": "Employer Match Rate (%)", "default": 50, "suffix": "%", "min": 25, "max": 100, "step": 25, "hint": "Standard: 50% match (e.g. $0.50 on the dollar)"},
            {"id": "match_cap_pct", "label": "Match Ceiling Cap (%)", "default": 6.0, "suffix": "%", "min": 1.0, "max": 15.0, "step": 0.5, "hint": "Company matches up to 6% of salary"}
        ],
        "metrics": [
            {"id": "annual_employer_free_money", "label": "Annual Employer Match (Free Money)", "default_display": "+$2,850.00 / yr", "highlight": True},
            {"id": "total_annual_401k_inflow", "label": "Total Combined Annual 401(k) Deposit", "default_display": "$8,550.00 / yr", "highlight": True},
            {"id": "instant_guaranteed_return", "label": "Instant Guaranteed Return on Your Money", "default_display": "50.0% Instant ROI", "highlight": True},
            {"id": "future_value_30yr_match", "label": "30-Year Future Value of Match Alone (8% CAGR)", "default_display": "$323,010.00"}
        ],
        "proof_steps": [
            {"step_title": "Matching Tier Ceiling Constraint", "step_text": "Eligible Match Contribution = min(Your Contribution%, Match Cap%) = min(6.0%, 6.0%) = 6.0%."},
            {"step_title": "Employer Cash Injection", "step_text": "Employer Match = Salary × Eligible% × Match Rate = $95,000 × 6% × 50% = $2,850/yr."},
            {"step_title": "Instant Risk-Free Return", "step_text": "Receiving $0.50 on every dollar contributed represents an immediate, risk-free 50% return before market growth, making capturing the full match the single highest priority in personal finance."}
        ],
        "faqs": [
            {"q": "What happens if I contribute less than the company match cap?", "a": "You are literally declining free salary! If your company matches 50% up to 6% and you only contribute 3%, you forfeit 1.5% of your salary ($1,425/yr on a $95k salary) forever."},
            {"q": "What is a 401(k) vesting schedule?", "a": "Your personal contributions are always 100% vested immediately. A vesting schedule dictates when you own company matching funds (e.g. 20% per year over 5 years or 100% cliff vesting after 3 years)."}
        ],
        "js_logic": """
          const sal = getNum('employee_base_salary');
          const empPct = (getNum('employee_contribution_pct') || 6.0) / 100;
          const matchRate = (getNum('match_rate_pct') || 50) / 100;
          const capPct = (getNum('match_cap_pct') || 6.0) / 100;

          const eligiblePct = Math.min(empPct, capPct);
          const empDollars = sal * empPct;
          const matchDollars = sal * eligiblePct * matchRate;
          const totalInflow = empDollars + matchDollars;
          const instantRoi = empDollars > 0 ? ((matchDollars / empDollars) * 100) : 0;

          // 30-year compound value of match alone at 8%
          const r = 0.08;
          const fv30 = matchDollars * ((Math.pow(1 + r, 30) - 1) / r);

          setDisp('annual_employer_free_money', '+$' + Math.round(matchDollars).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('total_annual_401k_inflow', '$' + Math.round(totalInflow).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('instant_guaranteed_return', instantRoi.toFixed(1) + '% Instant ROI');
          setDisp('future_value_30yr_match', '$' + Math.round(fv30).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "mega-backdoor-roth",
        "category": "finance",
        "name": "Mega Backdoor Roth IRA Contribution Calculator",
        "description": "Calculate maximum allowable after-tax 401(k) contributions and Mega Backdoor Roth capacity under the Section 415(c) overall limit ($69,000 in 2024).",
        "hero_badge": "High Net Worth • Mega Backdoor Roth Matrix",
        "formula_display": "Mega Backdoor Capacity = Section 415(c) Limit ($69,000) - Employee Elective Deferral - Employer Match",
        "fields": [
            {"id": "annual_415c_limit", "label": "IRS Section 415(c) Overall Annual Limit", "default": 69000, "prefix": "$", "min": 60000, "max": 80000, "step": 1000, "hint": "2024 IRS limit = $69,000 (excluding 50+ catch-up)"},
            {"id": "employee_regular_deferral", "label": "Your Employee 401(k) Deferral (Pre-tax or Roth)", "default": 23000, "prefix": "$", "min": 0, "max": 23000, "step": 500, "hint": "2024 elective deferral limit = $23,000"},
            {"id": "employer_total_match_contributions", "label": "Employer Match & Profit Sharing Received", "default": 9500, "prefix": "$", "min": 0, "max": 40000, "step": 500, "hint": "All company match and non-elective contributions"}
        ],
        "metrics": [
            {"id": "max_mega_backdoor_capacity", "label": "Available Mega Backdoor Roth Capacity", "default_display": "$36,500.00 / yr", "highlight": True},
            {"id": "total_annual_roth_shelter", "label": "Total Roth Tax-Free Capital Shelter", "default_display": "$59,500.00 / yr", "highlight": True},
            {"id": "future_30yr_tax_free_wealth", "label": "30-Year Compound Tax-Free Balance (8%)", "default_display": "$4,136,000.00", "highlight": True},
            {"id": "plan_prerequisites_check", "label": "Mandatory Employer Plan Rules", "default_display": "Requires After-Tax 401k + In-Plan Conversion"}
        ],
        "proof_steps": [
            {"step_title": "Section 415(c) Ceiling Law", "step_text": "The IRS limits total annual additions to a defined contribution plan to $69,000 (for 2024). This limit includes employee deferrals, employer matches, and after-tax contributions."},
            {"step_title": "Mega Backdoor Mathematical Residual", "step_text": "After-Tax Capacity = $69,000 - $23,000 Employee Deferral - $9,500 Match = $36,500."},
            {"step_title": "Immediate In-Plan Roth Conversion", "step_text": "By executing an immediate automated In-Plan Roth Conversion, the $36,500 after-tax dollars convert into a Roth 401(k) / Roth IRA with zero taxes on future gains forever."}
        ],
        "faqs": [
            {"q": "What two plan features are required for a Mega Backdoor Roth?", "a": "Your employer's 401(k) plan document MUST permit: 1) Non-Roth after-tax contributions, and 2) In-service distributions to a Roth IRA or In-Plan Roth Conversions. Without these specific provisions, the strategy cannot be executed."},
            {"q": "Can I do a Mega Backdoor Roth if my income is over the Roth IRA income limit?", "a": "Yes! The Mega Backdoor Roth completely bypasses the standard Roth IRA income phase-out limits ($161k Single / $240k MFJ) because contributions are made inside an employer 401(k) plan."}
        ],
        "js_logic": """
          const limit415c = getNum('annual_415c_limit') || 69000;
          const employeeDef = getNum('employee_regular_deferral');
          const employerMatch = getNum('employer_total_match_contributions');

          const capacity = Math.max(0, limit415c - employeeDef - employerMatch);
          const totalRoth = employeeDef + capacity;

          const r = 0.08;
          const fv30 = capacity * ((Math.pow(1 + r, 30) - 1) / r);

          setDisp('max_mega_backdoor_capacity', '$' + Math.round(capacity).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('total_annual_roth_shelter', '$' + Math.round(totalRoth).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('future_30yr_tax_free_wealth', '$' + Math.round(fv30).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('plan_prerequisites_check', 'Requires After-Tax 401k + In-Plan Conversion');
        """
    },
    {
        "slug": "hsa-triple-tax",
        "category": "finance",
        "name": "Health Savings Account (HSA) Triple Tax Calculator",
        "description": "Calculate Health Savings Account (HSA) triple tax savings: tax-deductible contributions, tax-free investment growth, and tax-free medical withdrawals.",
        "hero_badge": "Tax Alpha • HSA Triple Tax Shield",
        "formula_display": "HSA Triple Tax Advantage = Tax Deduction on Contribution + Tax-Free Growth + Tax-Free Withdrawal",
        "fields": [
            {"id": "annual_hsa_contribution", "label": "Annual HSA Contribution (2024 Limit)", "default": 4150, "prefix": "$", "min": 500, "max": 8300, "step": 50, "hint": "$4,150 individual, $8,300 family limit"},
            {"id": "marginal_income_tax_pct", "label": "Your Marginal Income Tax Bracket (%)", "default": 24, "suffix": "%", "min": 10, "max": 45, "step": 1, "hint": "Federal + state tax bracket"},
            {"id": "investment_horizon_years", "label": "Investment Horizon (Years)", "default": 25, "suffix": "years", "min": 5, "max": 45, "step": 1, "hint": "Years until retirement withdrawals"},
            {"id": "hsa_annual_return_pct", "label": "Expected Investment Return (CAGR %)", "default": 8.0, "suffix": "%", "min": 3.0, "max": 14.0, "step": 0.5, "hint": "Index fund return rate"}
        ],
        "metrics": [
            {"id": "future_tax_free_hsa_wealth", "label": "Future Tax-Free HSA Wealth Balance", "default_display": "$302,735.00", "highlight": True},
            {"id": "annual_immediate_tax_savings", "label": "Annual Upfront Tax Savings (Income + FICA)", "default_display": "$1,313.48 / yr", "highlight": True},
            {"id": "total_lifetime_taxes_avoided", "label": "Estimated Lifetime Taxes Completely Eliminated", "default_display": "$98,450.00 Saved", "highlight": True},
            {"id": "fica_payroll_tax_savings", "label": "FICA Payroll Tax Saved Annually (7.65%)", "default_display": "$317.48 / yr"}
        ],
        "proof_steps": [
            {"step_title": "The Triple Tax Exemption", "step_text": "1) Contributions are 100% tax-deductible (and exempt from FICA if made through payroll). 2) Dividends and capital gains compound 100% tax-free. 3) Withdrawals for qualified medical expenses are 100% tax-free."},
            {"step_title": "Payroll FICA Bonus Advantage", "step_text": "Unlike 401(k) and IRA contributions which are subject to 7.65% FICA taxes, payroll HSA deductions bypass FICA taxes completely, saving an extra $317/year."},
            {"step_title": "The Stealth IRA Strategy", "step_text": "Pay current medical out-of-pocket, save receipts digitally, let HSA capital compound in index funds for 25 years, and reimburse yourself tax-free in retirement."}
        ],
        "faqs": [
            {"q": "What happens to HSA funds after age 65?", "a": "After age 65, you can withdraw HSA funds for ANY non-medical purpose penalty-free, paying only ordinary income tax (identical to a traditional IRA). For medical expenses, withdrawals remain 100% tax-free forever."},
            {"q": "Is there a deadline to reimburse myself for medical expenses from an HSA?", "a": "No! There is zero time limit under IRS rules. You can incur a medical expense at age 30, keep the receipt, and reimburse yourself tax-free at age 65 after the funds have compounded for 35 years."}
        ],
        "js_logic": """
          const contrib = getNum('annual_hsa_contribution');
          const taxRate = (getNum('marginal_income_tax_pct') || 24) / 100;
          const years = getNum('investment_horizon_years') || 25;
          const r = (getNum('hsa_annual_return_pct') || 8.0) / 100;

          const ficaRate = 0.0765;
          const annualTaxSaved = contrib * (taxRate + ficaRate);
          const ficaSaved = contrib * ficaRate;

          const futureVal = contrib * ((Math.pow(1 + r, years) - 1) / r);
          const totalContributed = contrib * years;
          const growthGains = futureVal - totalContributed;
          const taxesAvoided = (growthGains * taxRate) + (annualTaxSaved * years);

          setDisp('future_tax_free_hsa_wealth', '$' + Math.round(futureVal).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('annual_immediate_tax_savings', '$' + annualTaxSaved.toFixed(2) + ' / yr');
          setDisp('total_lifetime_taxes_avoided', '$' + Math.round(taxesAvoided).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Saved');
          setDisp('fica_payroll_tax_savings', '$' + ficaSaved.toFixed(2) + ' / yr');
        """
    },
    {
        "slug": "fsa-use-it-or-lose-it",
        "category": "finance",
        "name": "Healthcare FSA Contribution & Forfeiture Calculator",
        "description": "Calculate Healthcare Flexible Spending Account (FSA) tax savings, optimal annual election, and avoid forfeiture under the IRS 'use-it-or-lose-it' rule.",
        "hero_badge": "Healthcare Benefits • FSA Optimization Matrix",
        "formula_display": "Net FSA Benefit = (FSA Contribution × Tax Rate %) - Forfeited Unused Balance",
        "fields": [
            {"id": "annual_fsa_election", "label": "Annual Healthcare FSA Election (Max $3,200)", "default": 2500, "prefix": "$", "min": 250, "max": 3200, "step": 50, "hint": "2024 IRS individual cap = $3,200"},
            {"id": "projected_medical_spend", "label": "Projected Out-of-Pocket Medical Expenses", "default": 2200, "prefix": "$", "min": 100, "max": 5000, "step": 50, "hint": "Copays, prescriptions, dental, vision, braces"},
            {"id": "marginal_tax_bracket_fsa", "label": "Combined Tax Bracket (Income + FICA)", "default": 31.65, "suffix": "%", "min": 15.0, "max": 50.0, "step": 0.5, "hint": "24% income tax + 7.65% FICA = 31.65%"},
            {"id": "employer_rollover_cap", "label": "Employer Plan Rollover Limit ($640 Max)", "default": 640, "prefix": "$", "min": 0, "max": 640, "step": 20, "hint": "IRS allows up to $640 rollover into next plan year"}
        ],
        "metrics": [
            {"id": "net_fsa_tax_savings", "label": "Net Cash Tax Savings Realized", "default_display": "$696.30 Cash Saved", "highlight": True},
            {"id": "forfeited_cash_loss", "label": "Estimated Forfeited Unused Cash", "default_display": "$0.00 (Protected by Rollover)", "highlight": True},
            {"id": "gross_tax_deduction_benefit", "label": "Gross Tax Deduction Value", "default_display": "$791.25"},
            {"id": "fsa_recommendation", "label": "FSA Strategy Guidance", "default_display": "Optimal Election (Full Expenses Covered)"}
        ],
        "proof_steps": [
            {"step_title": "Upfront Pre-Tax Shield", "step_text": "FSA contributions are deducted pre-income-tax and pre-FICA: Gross Tax Savings = FSA Election × Combined Tax Rate% (31.65%)."},
            {"step_title": "The Use-It-or-Lose-It Trap", "step_text": "Unused funds past the rollover limit ($640 in 2024) or 2.5-month grace period are permanently forfeited to your employer."},
            {"step_title": "Net Economic Benefit Invariant", "step_text": "Net Benefit = Gross Tax Savings - Cash Forfeited. Even with a minor $200 unspent balance, the $640 rollover protects you from losing a penny."}
        ],
        "faqs": [
            {"q": "Can you have both an HSA and an FSA?", "a": "You cannot have a general Healthcare FSA and an HSA simultaneously. However, you CAN have an HSA paired with a Limited Purpose FSA (LP-FSA) restricted exclusively to dental and vision expenses."},
            {"q": "What happens if you leave your job with an unspent FSA balance?", "a": "Any unspent FSA balance is forfeited upon termination of employment unless you elect COBRA to continue the FSA through the end of the plan year."}
        ],
        "js_logic": """
          const election = getNum('annual_fsa_election');
          const spend = getNum('projected_medical_spend');
          const taxRate = (getNum('marginal_tax_bracket_fsa') || 31.65) / 100;
          const rolloverCap = getNum('employer_rollover_cap');

          const grossSaved = election * taxRate;
          const unspent = Math.max(0, election - spend);
          const forfeited = Math.max(0, unspent - rolloverCap);
          const netSaved = grossSaved - forfeited;

          setDisp('net_fsa_tax_savings', '$' + netSaved.toFixed(2) + ' Cash Saved');
          setDisp('forfeited_cash_loss', forfeited > 0 ? ('$' + forfeited.toFixed(2) + ' FORFEITED') : '$0.00 (Protected by Rollover)');
          setDisp('gross_tax_deduction_benefit', '$' + grossSaved.toFixed(2));
          setDisp('fsa_recommendation', forfeited > 0 ? 'WARNING: Reduce election by $' + Math.round(forfeited) : 'Optimal Election (Full Expenses Covered)');
        """
    },
    {
        "slug": "child-tax-credit",
        "category": "finance",
        "name": "Child Tax Credit (CTC) & Phase-Out Calculator",
        "description": "Calculate the federal Child Tax Credit ($2,000 per child), refundable Additional Child Tax Credit (ACTC), and high-income phase-outs.",
        "hero_badge": "Family Tax Policy • CTC Phase-Out Matrix",
        "formula_display": "Phase-Out Reduction = $50 for every $1,000 MAGI exceeds $200k (Single) / $400k (MFJ)",
        "fields": [
            {"id": "qualifying_children_count", "label": "Qualifying Children Under Age 17", "default": 2, "min": 1, "max": 10, "step": 1, "hint": "Children with valid SSN under age 17 at year end"},
            {"id": "adjusted_gross_income_magi", "label": "Modified Adjusted Gross Income (MAGI)", "default": 185000, "prefix": "$", "min": 20000, "max": 1000000, "step": 5000, "hint": "Total household MAGI on Form 1040"},
            {"id": "tax_filing_status_ctc", "label": "Filing Status (1 = Single/HoH, 2 = Married Filing Jointly)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "Phase-out threshold: $200k Single / $400k MFJ"},
            {"id": "earned_income_annual", "label": "Annual Earned Income (W-2 / Business)", "default": 185000, "prefix": "$", "min": 0, "max": 1000000, "step": 5000, "hint": "Needed for refundable ACTC calculation"}
        ],
        "metrics": [
            {"id": "total_child_tax_credit", "label": "Total Child Tax Credit Allowed", "default_display": "$4,000.00 Credit", "highlight": True},
            {"id": "refundable_actc_portion", "label": "Refundable Additional Child Tax Credit", "default_display": "Up to $3,400.00 ($1,700/child)", "highlight": True},
            {"id": "phaseout_tax_reduction", "label": "Phase-Out Credit Reduction", "default_display": "$0.00 (Full Credit Retained)", "highlight": True},
            {"id": "direct_dollar_tax_cut", "label": "Direct 1040 Tax Bill Reduction", "default_display": "-$4,000.00 off tax bill"}
        ],
        "proof_steps": [
            {"step_title": "Maximum Statutory Credit", "step_text": "Base Credit = $2,000 per qualifying child under age 17. For 2 children: 2 × $2,000 = $4,000."},
            {"step_title": "High-Income Phase-Out Thresholds", "step_text": "The credit phases out by $50 for every $1,000 (or fraction thereof) that MAGI exceeds $200,000 (Single / Head of Household) or $400,000 (Married Filing Jointly)."},
            {"step_title": "Refundable Additional Child Tax Credit (ACTC)", "step_text": "Up to $1,700 per child (2024 limit) is refundable even if your total income tax liability is zero, calculated as 15% of earned income above $2,500."}
        ],
        "faqs": [
            {"q": "What is the difference between a tax credit and a tax deduction?", "a": "A tax deduction reduces taxable income (e.g. a $2,000 deduction at a 24% tax rate saves $480 in taxes). A tax credit reduces your actual tax bill dollar-for-dollar (a $2,000 tax credit saves a full $2,000 in cash)."},
            {"q": "At what income does the Child Tax Credit phase out completely?", "a": "For married couples with 2 children, the credit begins phasing out at $400,000 MAGI and is completely eliminated at $480,000 MAGI."}
        ],
        "js_logic": """
          const kids = getNum('qualifying_children_count');
          const magi = getNum('adjusted_gross_income_magi');
          const status = getNum('tax_filing_status_ctc');
          const earned = getNum('earned_income_annual');

          const threshold = status === 2 ? 400000 : 200000;
          const maxCredit = kids * 2000;
          const excess = Math.max(0, magi - threshold);
          const reduction = Math.ceil(excess / 1000) * 50;
          const actualCredit = Math.max(0, maxCredit - reduction);

          const refundableLimit = kids * 1700;
          const refundableEarned = Math.max(0, (earned - 2500) * 0.15);
          const actualRefundable = Math.min(actualCredit, Math.min(refundableLimit, refundableEarned));

          setDisp('total_child_tax_credit', '$' + Math.round(actualCredit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Credit');
          setDisp('refundable_actc_portion', 'Up to $' + Math.round(actualRefundable).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('phaseout_tax_reduction', reduction > 0 ? ('-$' + reduction.toLocaleString() + ' Reduction') : '$0.00 (Full Credit Retained)');
          setDisp('direct_dollar_tax_cut', '-$' + Math.round(actualCredit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' off tax bill');
        """
    },
    {
        "slug": "standard-vs-itemized",
        "category": "finance",
        "name": "Standard Deduction vs Itemized (Schedule A) Calculator",
        "description": "Compare the standard deduction against itemized Schedule A deductions: mortgage interest, $10k SALT cap, and charitable contributions.",
        "hero_badge": "Tax Optimization • Schedule A Matrix",
        "formula_display": "Itemized Total = min(State/Local Tax, $10,000) + Mortgage Interest + Charitable Giving + Medical > 7.5%",
        "fields": [
            {"id": "filing_status_std", "label": "Tax Filing Status (1 = Single $14,600, 2 = MFJ $29,200)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "2024 Standard deduction rates"},
            {"id": "state_local_taxes_salt", "label": "State Income & Property Taxes (SALT)", "default": 14500, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Subject to $10,000 TCJA cap"},
            {"id": "mortgage_interest_paid", "label": "Annual Home Mortgage Interest Paid", "default": 16200, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Form 1098 box 1"},
            {"id": "charitable_donations", "label": "Annual Charitable Giving (Cash & Goods)", "default": 5500, "prefix": "$", "min": 0, "max": 100000, "step": 250, "hint": "Tax-exempt 501(c)(3) donations"}
        ],
        "metrics": [
            {"id": "optimal_deduction_strategy", "label": "Recommended Tax Strategy", "default_display": "Itemize Deductions (Schedule A)", "highlight": True},
            {"id": "total_itemized_deductions", "label": "Total Itemized Deductions", "default_display": "$31,700.00", "highlight": True},
            {"id": "standard_deduction_allowance", "label": "Standard Deduction Allowance", "default_display": "$29,200.00"},
            {"id": "extra_taxable_income_saved", "label": "Extra Deductions Above Standard", "default_display": "+$2,500.00 extra deduction"}
        ],
        "proof_steps": [
            {"step_title": "The $10,000 SALT Cap Restriction", "step_text": "Under the Tax Cuts and Jobs Act (TCJA), state and local income taxes plus property taxes are strictly capped at $10,000 ($5,000 MFS): Allowed SALT = min(Actual SALT, $10,000)."},
            {"step_title": "Schedule A Itemization Summation", "step_text": "Total Itemized = Allowed SALT ($10,000) + Mortgage Interest ($16,200) + Charitable Giving ($5,500) = $31,700."},
            {"step_title": "Filing Selection Rule", "step_text": "Because $31,700 itemized exceeds the $29,200 Married Filing Jointly standard deduction by $2,500, itemizing saves an extra $600 in cash taxes."}
        ],
        "faqs": [
            {"q": "What percentage of taxpayers itemize deductions today?", "a": "Prior to 2018, nearly 31% of US taxpayers itemized. Following the TCJA doubling of the standard deduction and the $10,000 SALT cap, fewer than 10% of households benefit from itemizing."},
            {"q": "What is the charitable deduction 'bunching' strategy?", "a": "Taxpayers who fall just short of the standard deduction often 'bunch' two or three years of charitable donations into a single year using a Donor-Advised Fund (DAF), allowing them to itemize in year 1 and take the standard deduction in years 2 and 3."}
        ],
        "js_logic": """
          const status = getNum('filing_status_std');
          const salt = getNum('state_local_taxes_salt');
          const mort = getNum('mortgage_interest_paid');
          const charity = getNum('charitable_donations');

          const stdDed = status === 2 ? 29200 : 14600;
          const saltAllowed = Math.min(10000, salt);
          const itemized = saltAllowed + mort + charity;

          const diff = itemized - stdDed;
          let strategy = 'Take Standard Deduction ($' + stdDed.toLocaleString() + ')';
          if (diff > 0) {
            strategy = 'Itemize Deductions (Schedule A)';
          }

          setDisp('optimal_deduction_strategy', strategy);
          setDisp('total_itemized_deductions', '$' + itemized.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('standard_deduction_allowance', '$' + stdDed.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('extra_taxable_income_saved', (diff > 0 ? '+$' : '$0.00 ') + (diff > 0 ? diff.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' extra deduction' : '(Standard is higher)'));
        """
    },
    {
        "slug": "marginal-vs-effective-tax",
        "category": "finance",
        "name": "Marginal vs Effective Tax Rate Calculator",
        "description": "Calculate progressive federal tax bracket tiers, top marginal tax rate versus true effective (average) tax rate paid on total income.",
        "hero_badge": "Tax Literacy • Progressive Bracket Matrix",
        "formula_display": "Effective Tax Rate % = (Total Federal Tax Paid / Total Gross Income) × 100",
        "fields": [
            {"id": "annual_taxable_income_bracket", "label": "Taxable Income (After Deductions)", "default": 125000, "prefix": "$", "min": 10000, "max": 2000000, "step": 5000, "hint": "Income on Form 1040 line 15"},
            {"id": "filing_status_bracket", "label": "Tax Filing Status (1 = Single, 2 = Married Filing Jointly)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "Select bracket schedule"}
        ],
        "metrics": [
            {"id": "effective_tax_rate_pct", "label": "True Effective (Average) Tax Rate", "default_display": "15.01%", "highlight": True},
            {"id": "marginal_tax_rate_pct", "label": "Top Marginal Tax Bracket", "default_display": "24.00%", "highlight": True},
            {"id": "total_federal_tax_due", "label": "Total Federal Income Tax Due", "default_display": "$18,765.00", "highlight": True},
            {"id": "tax_on_next_dollar", "label": "Tax on Your Next $1.00 Earned", "default_display": "$0.24 (24 cents)"}
        ],
        "proof_steps": [
            {"step_title": "Progressive Tax Bracket Buckets", "step_text": "Federal income tax is progressive: income is divided into buckets taxed at increasing rates (10%, 12%, 22%, 24%, 32%, 35%, 37%)."},
            {"step_title": "Marginal vs Effective Distinction", "step_text": "Your marginal rate (24%) applies ONLY to the last dollar earned in that bucket. Dollars below that bracket are taxed at 10%, 12%, and 22%."},
            {"step_title": "Effective Tax Rate Formulation", "step_text": "Effective Tax Rate = Total Tax Due / Taxable Income = $18,765 / $125,000 = 15.01%. You pay only 15 cents of every dollar to federal tax, not 24 cents."}
        ],
        "faqs": [
            {"q": "Can a raise push me into a higher tax bracket and lower my take-home pay?", "a": "NO! This is the most common myth in personal finance. Moving into a higher tax bracket ONLY taxes the dollars that fall inside the new bracket. You ALWAYS keep more money after a raise."},
            {"q": "What is the difference between taxable income and gross income?", "a": "Gross income is total money earned before any adjustments. Taxable income is gross income MINUS pre-tax deductions (401k, HSA) and the standard deduction ($14,600 Single / $29,200 MFJ)."}
        ],
        "js_logic": """
          const income = getNum('annual_taxable_income_bracket');
          const status = getNum('filing_status_bracket');

          // 2024 brackets (Single vs MFJ)
          const bracketsSingle = [
            {limit: 11600, rate: 0.10},
            {limit: 47150, rate: 0.12},
            {limit: 100525, rate: 0.22},
            {limit: 191950, rate: 0.24},
            {limit: 243725, rate: 0.32},
            {limit: 609350, rate: 0.35},
            {limit: Infinity, rate: 0.37}
          ];

          const bracketsMfj = [
            {limit: 23200, rate: 0.10},
            {limit: 94300, rate: 0.12},
            {limit: 201050, rate: 0.22},
            {limit: 383900, rate: 0.24},
            {limit: 487450, rate: 0.32},
            {limit: 731200, rate: 0.35},
            {limit: Infinity, rate: 0.37}
          ];

          const schedule = status === 2 ? bracketsMfj : bracketsSingle;

          let tax = 0;
          let prevLimit = 0;
          let marginal = 0.10;

          for (let i = 0; i < schedule.length; i++) {
            const b = schedule[i];
            if (income > prevLimit) {
              const taxableInBracket = Math.min(income - prevLimit, b.limit - prevLimit);
              tax += taxableInBracket * b.rate;
              marginal = b.rate;
              prevLimit = b.limit;
            } else {
              break;
            }
          }

          const effective = income > 0 ? (tax / income) * 100 : 0;

          setDisp('effective_tax_rate_pct', effective.toFixed(2) + '%');
          setDisp('marginal_tax_rate_pct', (marginal * 100).toFixed(2) + '%');
          setDisp('total_federal_tax_due', '$' + Math.round(tax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('tax_on_next_dollar', '$' + marginal.toFixed(2) + ' (' + (marginal * 100).toFixed(0) + ' cents)');
        """
    },
    {
        "slug": "state-income-tax-comparison",
        "category": "finance",
        "name": "State Income Tax Relocation Comparison Calculator",
        "description": "Compare annual state income tax liabilities between high-tax states (California, New York, New Jersey) and zero-income-tax states (Florida, Texas, Tennessee).",
        "hero_badge": "Tax Migration • State Tax Arbitrage Matrix",
        "formula_display": "Annual Relocation Savings = Current State Income Tax - Destination State Income Tax",
        "fields": [
            {"id": "annual_gross_household_income", "label": "Annual Household Gross Income", "default": 225000, "prefix": "$", "min": 30000, "max": 10000000, "step": 10000, "hint": "W-2 salary + 1099 profit + capital gains"},
            {"id": "current_state_tax_rate", "label": "Current State Income Tax Rate (%)", "default": 9.3, "suffix": "%", "min": 0.0, "max": 14.0, "step": 0.1, "hint": "CA ≈ 9.3%, NY ≈ 6.5-10.9%, NJ ≈ 8.9%"},
            {"id": "destination_state_tax_rate", "label": "Destination State Income Tax Rate (%)", "default": 0.0, "suffix": "%", "min": 0.0, "max": 14.0, "step": 0.1, "hint": "FL, TX, TN, NV, WA, WY, SD, AK = 0.0%"}
        ],
        "metrics": [
            {"id": "annual_tax_savings_relocation", "label": "Annual State Income Tax Saved", "default_display": "$20,925.00 / yr", "highlight": True},
            {"id": "ten_year_compound_savings", "label": "10-Year Cumulative Savings (7% Growth)", "default_display": "$289,112.00", "highlight": True},
            {"id": "monthly_take_home_boost", "label": "Monthly Take-Home Pay Increase", "default_display": "+$1,743.75 / mo", "highlight": True},
            {"id": "current_state_annual_tax", "label": "Current State Income Tax Bill", "default_display": "$20,925.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Direct State Tax Arbitrage", "step_text": "State Tax Outflow = Taxable Income × State Tax Rate%. Relocating from California (9.3%) to Florida (0.0%) on $225,000 saves $20,925 annually."},
            {"step_title": "Monthly Cash Flow Expansion", "step_text": "Saving $20,925 per year immediately increases monthly household disposable income by $1,743.75."},
            {"step_title": "10-Year Wealth Compounding", "step_text": "Investing that $20,925 annual tax savings into index funds at a 7% CAGR generates $289,112 in pure additional net worth over 10 years."}
        ],
        "faqs": [
            {"q": "What nine US states have zero state income tax?", "a": "Alaska, Florida, Nevada, New Hampshire (dividend/interest tax phasing out in 2027), South Dakota, Tennessee, Texas, Washington (has a 7% high-value capital gains tax), and Wyoming."},
            {"q": "Does moving to a zero-tax state always save money?", "a": "Not always. Zero-income-tax states frequently make up revenue through higher local property taxes (e.g. Texas property taxes average 1.6-2.2%), higher sales taxes, or toll roads."}
        ],
        "js_logic": """
          const inc = getNum('annual_gross_household_income');
          const rOld = (getNum('current_state_tax_rate') || 9.3) / 100;
          const rNew = (getNum('destination_state_tax_rate') || 0.0) / 100;

          const taxOld = inc * rOld;
          const taxNew = inc * rNew;
          const annualSavings = Math.max(0, taxOld - taxNew);
          const monthlyBoost = annualSavings / 12;

          // 10-year FV at 7%
          const r = 0.07;
          const fv10 = annualSavings * ((Math.pow(1 + r, 10) - 1) / r);

          setDisp('annual_tax_savings_relocation', '$' + Math.round(annualSavings).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('ten_year_compound_savings', '$' + Math.round(fv10).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('monthly_take_home_boost', '+$' + monthlyBoost.toFixed(2) + ' / mo');
          setDisp('current_state_annual_tax', '$' + Math.round(taxOld).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    },
    {
        "slug": "capital-gains-harvesting",
        "category": "finance",
        "name": "Tax-Loss Harvesting & Capital Gains Offset Calculator",
        "description": "Calculate realized capital gains offsets using tax-loss harvesting, the IRS $3,000 ordinary income write-off limit, and net tax savings.",
        "hero_badge": "Tax Alpha • Loss Harvesting Matrix",
        "formula_display": "Net Capital Gain/Loss = Realized Gains - Realized Losses | Offset Limit = $3,000 against Ordinary Income",
        "fields": [
            {"id": "realized_capital_gains", "label": "Realized Capital Gains (Stocks/Crypto)", "default": 24000, "prefix": "$", "min": 0, "max": 5000000, "step": 1000, "hint": "Profits locked in from asset sales"},
            {"id": "harvested_capital_losses", "label": "Harvested Capital Losses Available", "default": 32000, "prefix": "$", "min": 0, "max": 5000000, "step": 1000, "hint": "Paper losses realized by selling losing positions"},
            {"id": "ordinary_income_tax_bracket", "label": "Your Marginal Income Tax Bracket (%)", "default": 32, "suffix": "%", "min": 10, "max": 45, "step": 1, "hint": "Federal tax rate on ordinary income"}
        ],
        "metrics": [
            {"id": "net_capital_tax_savings", "label": "Total Cash Taxes Saved", "default_display": "$5,760.00 Saved", "highlight": True},
            {"id": "capital_gains_eliminated", "label": "Capital Gains Wiped Out (Zero Tax)", "default_display": "$24,000.00 (100% Offset)", "highlight": True},
            {"id": "ordinary_income_offset_used", "label": "Ordinary Income Offset Applied", "default_display": "$3,000.00 (Max Annual Limit)", "highlight": True},
            {"id": "loss_carryover_future_years", "label": "Loss Carryforward to Future Tax Years", "default_display": "$5,000.00 Remaining Carryover"}
        ],
        "proof_steps": [
            {"step_title": "Dollar-for-Dollar Capital Gain Erasure", "step_text": "Harvested capital losses offset capital gains dollar-for-dollar without any cap: $24,000 gains - $24,000 losses = $0 taxable capital gains."},
            {"step_title": "The $3,000 Ordinary Income Offset", "step_text": "Under IRC Section 1211, excess losses over gains can offset up to $3,000 of ordinary W-2 income ($1,500 MFS) per tax year."},
            {"step_title": "Indefinite Loss Carryforward", "step_text": "Any remaining unabsorbed losses ($32,000 - $24,000 - $3,000 = $5,000) carry forward indefinitely to offset future gains in subsequent tax years."}
        ],
        "faqs": [
            {"q": "What is the IRS Wash-Sale Rule?", "a": "Under IRC Section 1091, you cannot claim a tax loss if you repurchase the exact same security (or a 'substantially identical' stock or option) within 30 days before or 30 days after the sale date (61-day total window)."},
            {"q": "Can you avoid the wash-sale rule using ETFs?", "a": "Yes! Investors sell a losing index fund (e.g. Vanguard S&P 500 VOO) and immediately purchase a similar but not identical fund (e.g. Schwab US Large-Cap SCHX or Vanguard Total Stock VTI) to harvest the tax loss while remaining 100% invested in the market."}
        ],
        "js_logic": """
          const gains = getNum('realized_capital_gains');
          const losses = getNum('harvested_capital_losses');
          const ordRate = (getNum('ordinary_income_tax_bracket') || 32) / 100;
          const capRate = 0.20; // long-term cap gains rate

          const net = gains - losses;
          let capGainsSaved = 0;
          let ordOffset = 0;
          let carryover = 0;

          if (net >= 0) {
            capGainsSaved = losses * capRate;
          } else {
            capGainsSaved = gains * capRate;
            const excessLoss = Math.abs(net);
            ordOffset = Math.min(3000, excessLoss);
            carryover = Math.max(0, excessLoss - 3000);
          }

          const ordTaxSaved = ordOffset * ordRate;
          const totalSaved = capGainsSaved + ordTaxSaved;

          setDisp('net_capital_tax_savings', '$' + Math.round(totalSaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Saved');
          setDisp('capital_gains_eliminated', '$' + Math.min(gains, losses).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (100% Offset)');
          setDisp('ordinary_income_offset_used', '$' + ordOffset.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (Max Annual Limit)');
          setDisp('loss_carryover_future_years', '$' + carryover.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Remaining Carryover');
        """
    },
    {
        "slug": "section-179-deduction",
        "category": "finance",
        "name": "Section 179 Equipment Depreciation Calculator",
        "description": "Calculate immediate first-year Section 179 equipment expensing deductions ($1,220,000 limit in 2024), phase-out ceilings, and net equipment acquisition cost.",
        "hero_badge": "Capital Expenditure • Section 179 Tax Shield",
        "formula_display": "Section 179 Deduction = min(Equipment Cost, $1,220,000) | Net Equipment Cost = Purchase Price - Cash Tax Saved",
        "fields": [
            {"id": "equipment_purchase_total", "label": "Total Qualifying Equipment Purchased", "default": 240000, "prefix": "$", "min": 5000, "max": 5000000, "step": 10000, "hint": "Machinery, computers, heavy vehicles > 6,000 lbs, software"},
            {"id": "business_tax_bracket_pct", "label": "Business / Owner Marginal Tax Rate (%)", "default": 35, "suffix": "%", "min": 10, "max": 45, "step": 1, "hint": "Federal + state marginal tax bracket"},
            {"id": "annual_business_net_income", "label": "Annual Business Taxable Net Income", "default": 450000, "prefix": "$", "min": 10000, "max": 10000000, "step": 25000, "hint": "Section 179 cannot exceed net business taxable income"}
        ],
        "metrics": [
            {"id": "section_179_deduction_amount", "label": "Year 1 Section 179 Tax Deduction", "default_display": "$240,000.00", "highlight": True},
            {"id": "immediate_cash_tax_savings", "label": "Direct Cash Tax Savings", "default_display": "$84,000.00 Cash Saved", "highlight": True},
            {"id": "net_effective_equipment_cost", "label": "True Out-of-Pocket Equipment Cost", "default_display": "$156,000.00 (35% Effective Discount)", "highlight": True},
            {"id": "phaseout_status_indicator", "label": "Phase-Out Threshold Status ($3,050,000)", "default_display": "Full Deduction (Below Phase-Out Ceiling)"}
        ],
        "proof_steps": [
            {"step_title": "The Section 179 Expensing Rule", "step_text": "Section 179 allows businesses to write off 100% of the purchase price of qualifying equipment in the year placed in service, rather than depreciating it over 5 to 7 years."},
            {"step_title": "2024 Statutory Limits", "step_text": "The 2024 maximum deduction is $1,220,000. The deduction phases out dollar-for-dollar once total equipment purchases exceed $3,050,000."},
            {"step_title": "Cash Flow Cost Reduction", "step_text": "True Equipment Cost = Equipment Price - (Deduction × Tax Bracket%). Buying $240,000 of machinery at a 35% tax rate saves $84,000 in cash taxes, reducing actual equipment cost to $156,000."}
        ],
        "faqs": [
            {"q": "Does a financed or leased piece of equipment qualify for Section 179?", "a": "YES! You can finance 100% of an equipment purchase with $0 down and still claim the full Section 179 tax deduction in Year 1, creating a cash-flow surplus where tax savings exceed your initial lease payments."},
            {"q": "Can Section 179 create a net operating loss (NOL)?", "a": "No. Section 179 cannot exceed your active business taxable income. Any unused Section 179 deduction above net income carries forward to future tax years. (Bonus depreciation, however, CAN create a tax loss)."}
        ],
        "js_logic": """
          const cost = getNum('equipment_purchase_total');
          const taxRate = (getNum('business_tax_bracket_pct') || 35) / 100;
          const income = getNum('annual_business_net_income');

          const cap2024 = 1220000;
          const phaseout2024 = 3050000;

          const excessPhaseout = Math.max(0, cost - phaseout2024);
          const maxDeductionAllowed = Math.max(0, cap2024 - excessPhaseout);
          const eligibleDeduction = Math.min(cost, Math.min(income, maxDeductionAllowed));

          const taxSaved = eligibleDeduction * taxRate;
          const netCost = cost - taxSaved;
          const discountPct = cost > 0 ? (taxSaved / cost) * 100 : 0;

          setDisp('section_179_deduction_amount', '$' + Math.round(eligibleDeduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('immediate_cash_tax_savings', '$' + Math.round(taxSaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Cash Saved');
          setDisp('net_effective_equipment_cost', '$' + Math.round(netCost).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + discountPct.toFixed(0) + '% Effective Discount)');
          setDisp('phaseout_status_indicator', cost <= phaseout2024 ? 'Full Deduction (Below Phase-Out Ceiling)' : 'Reduced by Phase-Out');
        """
    },
    {
        "slug": "bonus-depreciation",
        "category": "finance",
        "name": "Section 168(k) Bonus Depreciation Phase-Down Calculator",
        "description": "Calculate Section 168(k) bonus depreciation under the TCJA phase-down schedule (60% in 2024, 40% in 2025, 20% in 2026, 0% in 2027).",
        "hero_badge": "Tax Accounting • Bonus Depreciation Schedule",
        "formula_display": "Year 1 Deduction = (Asset Cost × Bonus %) + [(Asset Cost - Bonus Deduction) / MACRS Life]",
        "fields": [
            {"id": "asset_purchase_cost", "label": "Qualifying Asset Purchase Cost", "default": 180000, "prefix": "$", "min": 2500, "max": 20000000, "step": 5000, "hint": "Qualifying property with MACRS life ≤ 20 years"},
            {"id": "tax_year_placed_in_service", "label": "Tax Year Placed in Service (2024=60%, 2025=40%, 2026=20%)", "default": 2024, "min": 2023, "max": 2027, "step": 1, "hint": "Year equipment was actually operational"},
            {"id": "macrs_recovery_years", "label": "MACRS Recovery Period (Years)", "default": 5, "suffix": "years", "min": 3, "max": 20, "step": 2, "hint": "5-year (computers/vehicles) or 7-year (office furniture/machinery)"},
            {"id": "owner_tax_bracket_pct", "label": "Marginal Tax Bracket (%)", "default": 35, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Marginal income tax bracket"}
        ],
        "metrics": [
            {"id": "total_year1_writeoff", "label": "Total Year 1 Tax Deduction", "default_display": "$122,400.00", "highlight": True},
            {"id": "immediate_bonus_portion", "label": "Bonus Depreciation Share", "default_display": "$108,000.00 (60% Bonus)", "highlight": True},
            {"id": "year1_cash_tax_savings", "label": "First Year Cash Tax Savings", "default_display": "$42,840.00 Cash Saved", "highlight": True},
            {"id": "remaining_depreciable_basis", "label": "Remaining Depreciable Basis", "default_display": "$57,600.00"}
        ],
        "proof_steps": [
            {"step_title": "TCJA Phase-Down Statutory Schedule", "step_text": "Bonus rates: 100% (2018-2022) ➔ 80% (2023) ➔ 60% (2024) ➔ 40% (2025) ➔ 20% (2026) ➔ 0% (2027)."},
            {"step_title": "Year 1 Combined Formula", "step_text": "Bonus Deduction = Cost × Bonus%. Remaining Basis = Cost - Bonus. First-Year MACRS = Remaining Basis × MACRS Year 1 Rate (20% for 5-yr half-year convention)."},
            {"step_title": "Total Deduction Consolidation", "step_text": "Year 1 Write-off = $108,000 (Bonus) + $14,400 (MACRS) = $122,400. Total Cash Tax Saved at 35% = $42,840."}
        ],
        "faqs": [
            {"q": "What assets qualify for Section 168(k) bonus depreciation?", "a": "Qualifying assets must have a recovery period of 20 years or less, including machinery, computers, appliances, office furniture, qualified improvement property (QIP), and heavy commercial vehicles over 6,000 lbs GVWR."},
            {"q": "Can bonus depreciation create a tax loss?", "a": "YES! Unlike Section 179 which cannot exceed net business income, bonus depreciation can create a Net Operating Loss (NOL) that can offset up to 80% of taxable income in future years."}
        ],
        "js_logic": """
          const cost = getNum('asset_purchase_cost');
          const year = getNum('tax_year_placed_in_service');
          const life = getNum('macrs_recovery_years') || 5;
          const taxRate = (getNum('owner_tax_bracket_pct') || 35) / 100;

          let bonusRate = 0.60;
          if (year === 2023) bonusRate = 0.80;
          else if (year === 2024) bonusRate = 0.60;
          else if (year === 2025) bonusRate = 0.40;
          else if (year === 2026) bonusRate = 0.20;
          else if (year >= 2027) bonusRate = 0.00;

          const bonusDeduction = cost * bonusRate;
          const remainingBasis = cost - bonusDeduction;
          const macrsYr1Rate = 1 / life; // simplified half-year
          const macrsDeduction = remainingBasis * macrsYr1Rate;
          const totalYr1 = bonusDeduction + macrsDeduction;
          const taxSaved = totalYr1 * taxRate;

          setDisp('total_year1_writeoff', '$' + Math.round(totalYr1).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('immediate_bonus_portion', '$' + Math.round(bonusDeduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + (bonusRate * 100).toFixed(0) + '% Bonus)');
          setDisp('year1_cash_tax_savings', '$' + Math.round(taxSaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Cash Saved');
          setDisp('remaining_depreciable_basis', '$' + Math.round(cost - totalYr1).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "rsu-vesting-tax",
        "category": "finance",
        "name": "Restricted Stock Unit (RSU) Vesting Tax Calculator",
        "description": "Calculate RSU vesting income, mandatory supplemental tax withholding (22% vs 37%), shares sold-to-cover taxes, and net shares delivered.",
        "hero_badge": "Equity Compensation • RSU Vesting Matrix",
        "formula_display": "Vesting Tax = Shares Vested × Share Price × Marginal Tax Rate | Net Shares = Total Shares - Shares Sold to Cover",
        "fields": [
            {"id": "rsu_shares_vesting", "label": "Number of RSU Shares Vesting", "default": 500, "suffix": "shares", "min": 10, "max": 100000, "step": 25, "hint": "Vesting grant share count"},
            {"id": "stock_market_price_vest", "label": "Stock Fair Market Value at Vesting", "default": 175.00, "prefix": "$", "min": 1.00, "max": 5000.00, "step": 5.00, "hint": "Closing share price on vesting date"},
            {"id": "statutory_withholding_rate", "label": "Employer Statutory Tax Withholding (%)", "default": 22.0, "suffix": "%", "min": 22.0, "max": 37.0, "step": 1.0, "hint": "IRS standard: 22% under $1M, 37% over $1M"},
            {"id": "actual_marginal_tax_rate", "label": "Your Actual Marginal Income Tax Bracket (%)", "default": 35.0, "suffix": "%", "min": 12.0, "max": 50.0, "step": 1.0, "hint": "True federal + state marginal rate"}
        ],
        "metrics": [
            {"id": "gross_rsu_vesting_income", "label": "Gross RSU Compensation Income", "default_display": "$87,500.00", "highlight": True},
            {"id": "net_shares_deposited", "label": "Net Shares Deposited in Brokerage", "default_display": "390 Shares", "highlight": True},
            {"id": "shares_sold_to_cover", "label": "Shares Sold-to-Cover Mandatory Taxes", "default_display": "110 Shares (22.0%)", "highlight": True},
            {"id": "tax_underwithholding_bill", "label": "Estimated Tax Underwithholding Owed at Tax Time", "default_display": "$11,375.00 (Due April 15)"}
        ],
        "proof_steps": [
            {"step_title": "Ordinary W-2 Income Recognition", "step_text": "RSUs are taxed as ordinary W-2 income on the exact day they vest: Gross Income = Shares Vested × Fair Market Value = 500 × $175 = $87,500."},
            {"step_title": "Sell-to-Cover Mechanics", "step_text": "Most companies automatically sell shares to pay required withholding taxes: Shares Sold = ceil(Gross Income × Statutory Withholding% / Share Price) = 110 shares."},
            {"step_title": "The 22% Underwithholding Trap", "step_text": "The IRS mandates 22% supplemental withholding. If your actual marginal tax bracket is 35%, your employer under-withheld by 13% ($11,375), resulting in a surprise tax bill in April."}
        ],
        "faqs": [
            {"q": "Should I sell or hold my RSUs after they vest?", "a": "Holding vested company stock is mathematically identical to receiving a cash bonus and buying company stock on the open market. Unless you would proactively buy your company stock with cash, selling immediately to diversify into broad market index funds eliminates concentrated single-stock risk."},
            {"q": "What is the tax basis of vested RSUs?", "a": "Your cost basis is the fair market value on the date of vesting. If you sell immediately upon vesting, your capital gain is approximately $0."}
        ],
        "js_logic": """
          const shares = getNum('rsu_shares_vesting');
          const price = getNum('stock_market_price_vest');
          const statutory = (getNum('statutory_withholding_rate') || 22.0) / 100;
          const actualTax = (getNum('actual_marginal_tax_rate') || 35.0) / 100;

          const grossIncome = shares * price;
          const statutoryTaxOwed = grossIncome * statutory;
          const sharesSold = Math.ceil(statutoryTaxOwed / price);
          const netShares = Math.max(0, shares - sharesSold);

          const trueTaxOwed = grossIncome * actualTax;
          const underwithheld = Math.max(0, trueTaxOwed - statutoryTaxOwed);

          setDisp('gross_rsu_vesting_income', '$' + Math.round(grossIncome).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_shares_deposited', netShares + ' Shares');
          setDisp('shares_sold_to_cover', sharesSold + ' Shares (' + (statutory * 100).toFixed(1) + '%)');
          setDisp('tax_underwithholding_bill', underwithheld > 0 ? ('$' + Math.round(underwithheld).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (Due April 15)') : '$0.00 (Fully Withheld)');
        """
    },
    {
        "slug": "espp-discount",
        "category": "finance",
        "name": "Employee Stock Purchase Plan (ESPP) Calculator",
        "description": "Calculate Employee Stock Purchase Plan (ESPP) returns with 15% discount and lookback provision, annualized IRR, and qualifying vs disqualifying dispositions.",
        "hero_badge": "Equity Compensation • ESPP Alpha Matrix",
        "formula_display": "Purchase Price = min(Start Price, End Price) × 85% | Instant Gain = (End Price - Purchase Price) / Purchase Price",
        "fields": [
            {"id": "espp_offering_start_price", "label": "Stock Price at Offering Start", "default": 100.00, "prefix": "$", "min": 1.00, "max": 2500.00, "step": 5.00, "hint": "Share price on day 1 of 6-month offering period"},
            {"id": "espp_purchase_date_price", "label": "Stock Price on Purchase Date", "default": 120.00, "prefix": "$", "min": 1.00, "max": 2500.00, "step": 5.00, "hint": "Share price at end of offering period"},
            {"id": "annual_salary_payroll", "label": "Annual Salary", "default": 120000, "prefix": "$", "min": 25000, "max": 1000000, "step": 5000, "hint": "Base salary"},
            {"id": "espp_contribution_pct", "label": "Salary Contribution Percentage (%)", "default": 10.0, "suffix": "%", "min": 1.0, "max": 15.0, "step": 1.0, "hint": "IRS statutory limit: $25,000/yr"}
        ],
        "metrics": [
            {"id": "espp_instant_profit", "label": "Net Profit on Purchase Date", "default_display": "+$2,470.59", "highlight": True},
            {"id": "purchase_price_per_share", "label": "Discounted Purchase Price per Share", "default_display": "$85.00 (15% Lookback Discount)", "highlight": True},
            {"id": "instant_roi_percentage", "label": "Immediate Risk-Free ROI", "default_display": "41.18% Instant Gain", "highlight": True},
            {"id": "annualized_espp_irr", "label": "Annualized Return (IRR)", "default_display": "~85.0% - 95.0% Annualized"}
        ],
        "proof_steps": [
            {"step_title": "The Lookback Provision Super-Power", "step_text": "With a lookback provision, your 15% discount applies to the LOWER of the start price ($100) or end price ($120): Purchase Price = min($100, $120) × 85% = $85.00."},
            {"step_title": "Instant Market Arbitrage", "step_text": "You purchase shares for $85.00 and can immediately sell them on the open market for $120.00: Instant Gain = ($120 - $85) / $85 = +41.18%."},
            {"step_title": "Capital Utilization Reality", "step_text": "Because payroll deductions accumulate gradually over 6 months (average dollar held for only 3 months), a 41% gain translates into an annualized IRR exceeding 85% to 95%."}
        ],
        "faqs": [
            {"q": "What is the difference between a qualifying and disqualifying disposition?", "a": "A qualifying disposition requires holding shares for 2 years from the offering date and 1 year from the purchase date, granting favorable capital gains rates. In a disqualifying disposition (selling immediately), the 15% discount is taxed as ordinary income, but eliminates all market downside risk."},
            {"q": "Should I sell my ESPP shares immediately upon purchase?", "a": "Yes! Selling immediately locks in an immediate, risk-free 17.6% to 40%+ return without taking on single-stock volatility."}
        ],
        "js_logic": """
          const pStart = getNum('espp_offering_start_price');
          const pEnd = getNum('espp_purchase_date_price');
          const salary = getNum('annual_salary_payroll');
          const contribPct = (getNum('espp_contribution_pct') || 10.0) / 100;

          // 6-month contribution capped at $12,500 ($25k / yr)
          const sixMoContrib = Math.min(12500, (salary / 2) * contribPct);
          const lowerPrice = Math.min(pStart, pEnd);
          const buyPrice = lowerPrice * 0.85;
          const sharesBought = buyPrice > 0 ? (sixMoContrib / buyPrice) : 0;
          const marketValue = sharesBought * pEnd;
          const profit = marketValue - sixMoContrib;
          const instantGain = sixMoContrib > 0 ? ((profit / sixMoContrib) * 100) : 0;

          setDisp('espp_instant_profit', '+$' + profit.toFixed(2));
          setDisp('purchase_price_per_share', '$' + buyPrice.toFixed(2) + ' (15% Lookback Discount)');
          setDisp('instant_roi_percentage', instantGain.toFixed(2) + '% Instant Gain');
          setDisp('annualized_espp_irr', '~' + (instantGain * 2.2).toFixed(0) + '% - ' + (instantGain * 2.5).toFixed(0) + '% Annualized');
        """
    },
    {
        "slug": "nua-company-stock",
        "category": "finance",
        "name": "Net Unrealized Appreciation (NUA) 401(k) Stock Calculator",
        "description": "Calculate Net Unrealized Appreciation (NUA) tax savings on employer stock inside a 401(k), converting 37% ordinary income tax into 20% capital gains tax.",
        "hero_badge": "Retirement Distribution • NUA Strategy Matrix",
        "formula_display": "NUA = Current Market Value of Employer Stock - Original Cost Basis",
        "fields": [
            {"id": "company_stock_market_val", "label": "Current Market Value of 401(k) Company Stock", "default": 450000, "prefix": "$", "min": 25000, "max": 10000000, "step": 25000, "hint": "Total value of employer shares held in 401(k)"},
            {"id": "company_stock_cost_basis", "label": "Original Cost Basis of Company Stock", "default": 85000, "prefix": "$", "min": 5000, "max": 5000000, "step": 5000, "hint": "Cost basis when shares were purchased in plan"},
            {"id": "ordinary_income_tax_rate_nua", "label": "Your Marginal Income Tax Rate (%)", "default": 35.0, "suffix": "%", "min": 12.0, "max": 45.0, "step": 1.0, "hint": "Ordinary tax rate on IRA distributions"},
            {"id": "long_term_capital_gains_rate", "label": "Long-Term Capital Gains Tax Rate (%)", "default": 20.0, "suffix": "%", "min": 0.0, "max": 23.8, "step": 1.0, "hint": "Federal capital gains rate"}
        ],
        "metrics": [
            {"id": "net_nua_tax_savings", "label": "Total Cash Tax Saved via NUA", "default_display": "$54,750.00 Saved", "highlight": True},
            {"id": "nua_unrealized_gain_amount", "label": "Net Unrealized Appreciation (NUA)", "default_display": "$365,000.00", "highlight": True},
            {"id": "tax_due_at_distribution", "label": "Immediate Tax Due on Cost Basis", "default_display": "$29,750.00 (on $85k basis)"},
            {"id": "nua_vs_ira_recommendation", "label": "Strategy Recommendation", "default_display": "Elect NUA (Saves 15% on $365k Gain)"}
        ],
        "proof_steps": [
            {"step_title": "The Standard Rollover Pitfall", "step_text": "If you roll company stock into a Traditional IRA, 100% of future withdrawals are taxed at ordinary income tax rates (up to 37%)."},
            {"step_title": "The NUA Strategy Execution", "step_text": "Under IRC Section 402(e)(4), you roll non-company assets to an IRA, but transfer company stock in-kind to a taxable brokerage account. You pay ordinary income tax ONLY on the original cost basis ($85,000 × 35% = $29,750)."},
            {"step_title": "Permanent Capital Gains Arbitrage", "step_text": "The $365,000 NUA gain is permanently locked in at the lower 20% long-term capital gains rate: ($365,000 × 35%) - ($365,000 × 20%) = $54,750 in cash tax savings."}
        ],
        "faqs": [
            {"q": "What trigger events are required to execute an NUA strategy?", "a": "NUA requires a lump-sum distribution within a single calendar year following one of four qualifying triggering events: 1) Separation from service (retirement/quitting), 2) Reaching age 59½, 3) Total disability, or 4) Death."},
            {"q": "When is NUA NOT recommended?", "a": "If your company stock has little appreciation (e.g. cost basis is 80% of current value) or if you plan to hold assets for decades in low tax brackets, rolling everything to an IRA may be superior."}
        ],
        "js_logic": """
          const marketVal = getNum('company_stock_market_val');
          const costBasis = getNum('company_stock_cost_basis');
          const ordRate = (getNum('ordinary_income_tax_rate_nua') || 35.0) / 100;
          const capRate = (getNum('long_term_capital_gains_rate') || 20.0) / 100;

          const nua = Math.max(0, marketVal - costBasis);
          const taxIfIra = marketVal * ordRate;
          const taxWithNua = (costBasis * ordRate) + (nua * capRate);
          const savings = Math.max(0, taxIfIra - taxWithNua);
          const taxAtDist = costBasis * ordRate;

          setDisp('net_nua_tax_savings', '$' + Math.round(savings).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Saved');
          setDisp('nua_unrealized_gain_amount', '$' + Math.round(nua).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('tax_due_at_distribution', '$' + Math.round(taxAtDist).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (on $' + Math.round(costBasis/1000) + 'k basis)');
          setDisp('nua_vs_ira_recommendation', savings > 5000 ? 'Elect NUA (Saves ' + ((ordRate - capRate)*100).toFixed(0) + '% on $' + Math.round(nua/1000) + 'k Gain)' : 'Roll to Traditional IRA (NUA basis too high)');
        """
    },
    {
        "slug": "sepp-72t-distribution",
        "category": "finance",
        "name": "Rule 72(t) SEPP Early IRA Withdrawal Calculator",
        "description": "Calculate penalty-free early retirement withdrawals from traditional or Roth IRAs prior to age 59½ using IRS Rule 72(t) Substantially Equal Periodic Payments.",
        "hero_badge": "Early Retirement • Rule 72(t) SEPP Matrix",
        "formula_display": "SEPP Payment = Account Balance / Annuity Factor (or Amortization Formula)",
        "fields": [
            {"id": "ira_account_balance", "label": "Designated IRA Account Balance", "default": 650000, "prefix": "$", "min": 50000, "max": 10000000, "step": 25000, "hint": "Balance in specific IRA used for SEPP"},
            {"id": "retiree_current_age", "label": "Retiree Current Age (Under 59½)", "default": 52, "suffix": "years", "min": 30, "max": 58, "step": 1, "hint": "Age when payments begin"},
            {"id": "irs_midterm_rate_pct", "label": "IRS 72(t) Interest Rate (Up to 5% Cap)", "default": 4.85, "suffix": "%", "min": 1.0, "max": 5.0, "step": 0.05, "hint": "120% of federal mid-term rate (capped at 5.0%)"}
        ],
        "metrics": [
            {"id": "annual_fixed_sepp_payout", "label": "Annual Penalty-Free Withdrawal (Amortization)", "default_display": "$41,470.00 / yr", "highlight": True},
            {"id": "monthly_sepp_cashflow", "label": "Monthly Penalty-Free Cash Flow", "default_display": "$3,455.83 / mo", "highlight": True},
            {"id": "ten_percent_penalty_avoided", "label": "10% Early Withdrawal Penalty Avoided", "default_display": "$4,147.00 / yr Saved", "highlight": True},
            {"id": "mandatory_sepp_duration", "label": "Mandatory SEPP Commitment Duration", "default_display": "7.5 Years (Until Age 59½)"}
        ],
        "proof_steps": [
            {"step_title": "The 10% Early Penalty Waiver", "step_text": "Withdrawals from IRAs before age 59½ normally trigger a 10% early withdrawal excise tax penalty. Section 72(t) waives the penalty if payments are substantially equal."},
            {"step_title": "IRS Approved Calculation Methods", "step_text": "Three calculation methods exist: 1) Required Minimum Distribution (RMD - variable), 2) Fixed Amortization (highest payout), and 3) Fixed Annuitization."},
            {"step_title": "Strict Commitment Lock-In", "step_text": "Once started, payments must continue without modification for the LONGER of 5 full years or until you reach age 59½. Any modification retroactively triggers all waived 10% penalties plus interest."}
        ],
        "faqs": [
            {"q": "Can you change the withdrawal amount once a 72(t) SEPP starts?", "a": "No! If you alter the withdrawal amount by even $1 before age 59½ (or 5 years), the IRS busts the plan, demanding retroactive 10% penalties plus interest on every single distribution taken since inception."},
            {"q": "Can I split my IRA before starting a 72(t) plan?", "a": "YES! This is a premier wealth planning strategy: roll the exact amount needed for your desired annual income into a separate IRA and establish the 72(t) on only that specific account, leaving other IRAs untouched."}
        ],
        "js_logic": """
          const bal = getNum('ira_account_balance');
          const age = getNum('retiree_current_age');
          const r = (getNum('irs_midterm_rate_pct') || 4.85) / 100;

          // Single life expectancy approximation (IRS Table)
          const lifeExp = 84 - age;
          // Amortization method factor
          const annualPayment = bal * (r / (1 - Math.pow(1 + r, -lifeExp)));
          const monthly = annualPayment / 12;
          const penaltySaved = annualPayment * 0.10;
          const yearsRequired = Math.max(5, 59.5 - age);

          setDisp('annual_fixed_sepp_payout', '$' + Math.round(annualPayment).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('monthly_sepp_cashflow', '$' + monthly.toFixed(2) + ' / mo');
          setDisp('ten_percent_penalty_avoided', '$' + Math.round(penaltySaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr Saved');
          setDisp('mandatory_sepp_duration', yearsRequired.toFixed(1) + ' Years (Until Age 59½)');
        """
    },
    {
        "slug": "charitable-remainder-trust",
        "category": "finance",
        "name": "Charitable Remainder Unitrust (CRUT) Tax Calculator",
        "description": "Calculate immediate upfront income tax deductions, tax-free appreciated asset sales, and annual annuity income streams using a Charitable Remainder Trust (CRUT).",
        "hero_badge": "High Net Worth • Philanthropic Tax Shield",
        "formula_display": "Upfront Tax Deduction = Present Value of Remainder Interest (≥ 10% of Contributed Value)",
        "fields": [
            {"id": "appreciated_asset_market_val", "label": "Highly Appreciated Asset Value (Stock / Real Estate)", "default": 1000000, "prefix": "$", "min": 100000, "max": 50000000, "step": 50000, "hint": "Zero-basis stock, crypto, or real estate"},
            {"id": "annual_unitrust_payout_pct", "label": "Annual Unitrust Payout Rate (%)", "default": 6.0, "suffix": "%", "min": 5.0, "max": 12.0, "step": 0.5, "hint": "Mandatory minimum 5% / max ~10%"},
            {"id": "donor_current_age", "label": "Donor Primary Beneficiary Age", "default": 62, "suffix": "years", "min": 35, "max": 90, "step": 1, "hint": "Age of lifetime income recipient"},
            {"id": "irs_section_7520_rate", "label": "IRS Section 7520 Hurdle Discount Rate (%)", "default": 5.2, "suffix": "%", "min": 2.0, "max": 10.0, "step": 0.2, "hint": "Current monthly statutory discount rate"}
        ],
        "metrics": [
            {"id": "upfront_income_tax_deduction", "label": "Immediate Upfront Tax Deduction", "default_display": "$284,500.00", "highlight": True},
            {"id": "capital_gains_tax_eliminated", "label": "Capital Gains Tax Eliminated at Sale", "default_display": "$238,000.00 Saved", "highlight": True},
            {"id": "year1_annual_income_stream", "label": "Year 1 Annual Income Distribution", "default_display": "$60,000.00 / yr", "highlight": True},
            {"id": "charity_remainder_payout", "label": "Estimated Future Remainder to Charity", "default_display": "$1,450,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Tax-Exempt Trust Sale", "step_text": "Because a CRUT is a tax-exempt entity under IRC Section 664, it sells the $1,000,000 asset for full value with ZERO capital gains tax, reinvesting 100% of gross proceeds."},
            {"step_title": "The 10% Remainder Test", "step_text": "To qualify under IRS rules, the actuarial present value of the ultimate charitable remainder must equal at least 10% of the initial contribution."},
            {"step_title": "Immediate Cash Tax Shield", "step_text": "Donating $1M generates an immediate ~$284,500 charitable tax deduction, saving ~$105,000 in personal income taxes in Year 1 while providing a $60,000/year lifetime income stream."}
        ],
        "faqs": [
            {"q": "What is the difference between a CRUT and a CRAT?", "a": "A Charitable Remainder Unitrust (CRUT) pays a fixed percentage of trust assets revalued annually (income grows with market performance). A Charitable Remainder Annuity Trust (CRAT) pays a fixed dollar amount annually regardless of market performance."},
            {"q": "Can I replace the wealth given to charity for my children?", "a": "Yes! Many families pair a CRUT with a Wealth Replacement Trust (Irrevocable Life Insurance Trust - ILIT), using a portion of the annual income stream to fund life insurance that passes completely tax-free to children."}
        ],
        "js_logic": """
          const assetVal = getNum('appreciated_asset_market_val');
          const payoutRate = (getNum('annual_unitrust_payout_pct') || 6.0) / 100;
          const age = getNum('donor_current_age');
          const sec7520 = (getNum('irs_section_7520_rate') || 5.2) / 100;

          const lifeExpectancy = Math.max(5, 86 - age);
          const capGainsAvoided = assetVal * 0.238; // 20% + 3.8% NIIT
          const deductionFraction = Math.max(0.10, Math.pow(1 - payoutRate, lifeExpectancy));
          const deduction = assetVal * deductionFraction;
          const yr1Income = assetVal * payoutRate;
          const futureCharity = assetVal * 1.45;

          setDisp('upfront_income_tax_deduction', '$' + Math.round(deduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('capital_gains_tax_eliminated', '$' + Math.round(capGainsAvoided).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Saved');
          setDisp('year1_annual_income_stream', '$' + Math.round(yr1Income).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('charity_remainder_payout', '$' + Math.round(futureCharity).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "estate-gift-tax",
        "category": "finance",
        "name": "Federal Estate & Lifetime Gift Tax Exemption Calculator",
        "description": "Calculate federal estate and gift tax exposure (40% rate), lifetime unified credit ($13.61M individual / $27.22M married), and 2026 TCJA sunset impact.",
        "hero_badge": "Wealth Preservation • Estate Tax Matrix",
        "formula_display": "Estate Tax = (Gross Estate - Applicable Lifetime Exemption) × 40%",
        "fields": [
            {"id": "net_estate_worth", "label": "Estimated Total Net Estate Value", "default": 18000000, "prefix": "$", "min": 1000000, "max": 200000000, "step": 500000, "hint": "Real estate, business equity, stocks, life insurance"},
            {"id": "marital_status_estate", "label": "Marital Status (1 = Single, 2 = Married / Portability)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "Married couples share portability ($27.22M total)"},
            {"id": "tcja_sunset_2026_flag", "label": "2026 TCJA Sunset Scenario (0 = Current $13.61M, 1 = Post-Sunset ~$7M)", "default": 0, "min": 0, "max": 1, "step": 1, "hint": "TCJA exemption cuts by 50% on Jan 1, 2026"}
        ],
        "metrics": [
            {"id": "federal_estate_tax_owed", "label": "Estimated Federal Estate Tax Owed", "default_display": "$0.00 (Exempt under current law)", "highlight": True},
            {"id": "applicable_lifetime_exemption", "label": "Applicable Lifetime Exemption Ceiling", "default_display": "$27,220,000.00", "highlight": True},
            {"id": "post_sunset_tax_exposure", "label": "Projected Tax if 2026 Sunset Occurs", "default_display": "$1,600,000.00 (at $14M exemption)", "highlight": True},
            {"id": "annual_gift_exclusion_limit", "label": "Annual Exclusion Gift Limit per Child", "default_display": "$18,000 / recipient ($36,000 MFJ)"}
        ],
        "proof_steps": [
            {"step_title": "The Unified Lifetime Exemption", "step_text": "For 2024, the federal estate and gift tax exemption is $13,610,000 per individual ($27,220,000 for married couples with portability)."},
            {"step_title": "Flat 40% Estate Tax Rate", "step_text": "Any net estate value exceeding the applicable lifetime exemption is taxed at a flat federal rate of 40% within 9 months of death."},
            {"step_title": "The 2026 Sunset Cliff", "step_text": "Unless Congress passes legislation, the TCJA exemption expires on December 31, 2025, cutting the lifetime exemption roughly in half to ~$7 million per individual."}
        ],
        "faqs": [
            {"q": "What is estate tax portability?", "a": "Portability allows a surviving spouse to elect to transfer any unused estate tax exemption from their deceased spouse by filing IRS Form 706 within 5 years of death, effectively doubling the household exemption."},
            {"q": "How does the annual gift exclusion work?", "a": "In 2024, you can gift up to $18,000 per recipient ($36,000 for married couples) to an unlimited number of people without reporting it to the IRS or reducing your lifetime estate tax exemption."}
        ],
        "js_logic": """
          const estate = getNum('net_estate_worth');
          const isMarried = getNum('marital_status_estate') === 2;
          const isSunset = getNum('tcja_sunset_2026_flag') === 1;

          let singleExemption = isSunset ? 7000000 : 13610000;
          let totalExemption = isMarried ? (singleExemption * 2) : singleExemption;

          const taxableEstate = Math.max(0, estate - totalExemption);
          const tax = taxableEstate * 0.40;

          const sunsetExemptionMfj = 14000000;
          const sunsetTax = Math.max(0, estate - (isMarried ? sunsetExemptionMfj : 7000000)) * 0.40;

          setDisp('federal_estate_tax_owed', tax > 0 ? ('$' + Math.round(tax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})) : '$0.00 (Exempt under current law)');
          setDisp('applicable_lifetime_exemption', '$' + totalExemption.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('post_sunset_tax_exposure', sunsetTax > 0 ? ('$' + Math.round(sunsetTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (at $' + (isMarried ? '14M' : '7M') + ' exemption)') : '$0.00 (Still Exempt)');
          setDisp('annual_gift_exclusion_limit', '$18,000 / recipient ($36,000 MFJ)');
        """
    },
    {
        "slug": "inherited-ira-10-year",
        "category": "finance",
        "name": "Inherited IRA 10-Year Rule & RMD Calculator",
        "description": "Calculate SECURE Act 10-year mandatory withdrawal schedules for inherited traditional and Roth IRAs, minimizing bracket creep and tax drag.",
        "hero_badge": "Estate Distribution • SECURE Act 10-Year Matrix",
        "formula_display": "10-Year Distribution = Equal Annual Withdrawals over 10 Years to Prevent Bracket Spikes",
        "fields": [
            {"id": "inherited_ira_balance", "label": "Inherited Traditional IRA Balance", "default": 450000, "prefix": "$", "min": 25000, "max": 10000000, "step": 25000, "hint": "Pre-tax IRA balance inherited from non-spouse"},
            {"id": "beneficiary_annual_income", "label": "Beneficiary Current W-2 / Ordinary Income", "default": 110000, "prefix": "$", "min": 0, "max": 1000000, "step": 5000, "hint": "Existing baseline taxable income"},
            {"id": "withdrawal_strategy_choice", "label": "Distribution Strategy (1 = Equal 10-Year Installments, 2 = Year 10 Lump-Sum)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1 = Smooth spread across 10 years; 2 = Defer until Year 10"}
        ],
        "metrics": [
            {"id": "annual_recommended_withdrawal", "label": "Optimal Annual Distribution Amount", "default_display": "$45,000.00 / yr", "highlight": True},
            {"id": "bracket_creep_penalty", "label": "Estimated Tax Saved by Spreading vs Lump-Sum", "default_display": "$48,500.00 Tax Saved", "highlight": True},
            {"id": "year10_lump_sum_tax_hit", "label": "Year 10 Lump-Sum Tax Disaster", "default_display": "~$185,000.00 in Taxes (37% Bracket)", "highlight": True},
            {"id": "inherited_roth_alternative", "label": "If Inherited Account was a Roth IRA", "default_display": "100% Tax-Free (Hold to Year 10)"}
        ],
        "proof_steps": [
            {"step_title": "The SECURE Act 10-Year Mandate", "step_text": "Under the SECURE Act, non-eligible designated beneficiaries (adult children) must completely liquidate inherited IRAs by December 31 of the 10th year following death."},
            {"step_title": "Lump-Sum Bracket Explosion", "step_text": "Waiting until Year 10 to withdraw $450,000 on top of existing salary pushes the beneficiary directly into the maximum 37% federal tax bracket, forfeiting nearly half the inheritance."},
            {"step_title": "Tax-Smoothing Spreading Optimization", "step_text": "Withdrawing $45,000 annually over 10 years keeps taxable income inside the 24% tax bracket, saving over $48,000 in pure cash taxes."}
        ],
        "faqs": [
            {"q": "Who is exempt from the 10-year inherited IRA rule?", "a": "Eligible Designated Beneficiaries (EDBs) are exempt: 1) Surviving spouses, 2) Minor children of the deceased (until age 21), 3) Disabled individuals, 4) Chronically ill individuals, and 5) Beneficiaries not more than 10 years younger than the deceased."},
            {"q": "What is the rule for inherited Roth IRAs?", "a": "Inherited Roth IRAs are also subject to the 10-year rule, BUT withdrawals are 100% tax-free! For Roths, you should leave 100% of the money in the account to compound tax-free for the full 10 years before taking a single lump sum."}
        ],
        "js_logic": """
          const bal = getNum('inherited_ira_balance');
          const income = getNum('beneficiary_annual_income');
          const isSmooth = getNum('withdrawal_strategy_choice') === 1;

          const annualSpread = bal / 10;
          // Tax bracket comparison
          const taxSpreadAnnual = annualSpread * 0.24;
          const totalTaxSpread = taxSpreadAnnual * 10;
          const lumpSumTax = bal * 0.35; // pushed into 35-37% bracket
          const savings = Math.max(0, lumpSumTax - totalTaxSpread);

          setDisp('annual_recommended_withdrawal', '$' + Math.round(annualSpread).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('bracket_creep_penalty', '$' + Math.round(savings).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Tax Saved');
          setDisp('year10_lump_sum_tax_hit', '~$' + Math.round(lumpSumTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' in Taxes (35-37% Bracket)');
          setDisp('inherited_roth_alternative', '100% Tax-Free (Hold to Year 10)');
        """
    },
    {
        "slug": "social-security-taxation",
        "category": "finance",
        "name": "Social Security Benefits Taxation Calculator",
        "description": "Calculate how much of your Social Security retirement benefit is subject to federal income tax (0%, 50%, or 85%) based on provisional combined income.",
        "hero_badge": "Retirement Taxation • Social Security Matrix",
        "formula_display": "Provisional Income = AGI (Excluding SS) + Non-Taxable Interest + (50% of Social Security)",
        "fields": [
            {"id": "annual_social_security_benefit", "label": "Annual Social Security Benefits Received", "default": 32000, "prefix": "$", "min": 5000, "max": 100000, "step": 1000, "hint": "Gross benefit on Form SSA-1099 box 5"},
            {"id": "other_taxable_income", "label": "Other Income (Pensions, 401k, Dividends, W-2)", "default": 45000, "prefix": "$", "min": 0, "max": 500000, "step": 1000, "hint": "All ordinary income, pensions, and RMDs"},
            {"id": "tax_exempt_municipal_interest", "label": "Tax-Exempt Municipal Bond Interest", "default": 0, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Muni interest is counted in combined income"},
            {"id": "filing_status_ss", "label": "Tax Filing Status (1 = Single, 2 = Married Filing Jointly)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "Single: $25k-$34k (50%), >$34k (85%); MFJ: $32k-$44k (50%), >$44k (85%)"}
        ],
        "metrics": [
            {"id": "taxable_social_security_amount", "label": "Taxable Social Security Income", "default_display": "$23,700.00 (74.1%)", "highlight": True},
            {"id": "provisional_combined_income", "label": "Provisional Combined Income", "default_display": "$61,000.00", "highlight": True},
            {"id": "tax_free_benefit_share", "label": "100% Tax-Free Benefit Share", "default_display": "$8,300.00 (25.9% Tax-Free)", "highlight": True},
            {"id": "tax_tier_category", "label": "Social Security Tax Bracket Tier", "default_display": "Tier 2 (Up to 85% Taxable)"}
        ],
        "proof_steps": [
            {"step_title": "Provisional Combined Income Formula", "step_text": "Provisional Income = Adjusted Gross Income + Tax-Exempt Interest + (50% of Social Security Benefit). For example: $45,000 + $0 + $16,000 = $61,000."},
            {"step_title": "Statutory Threshold Tiers", "step_text": "For married couples: Under $32,000 = 0% taxable. Between $32,000 and $44,000 = up to 50% taxable. Above $44,000 = up to 85% taxable."},
            {"step_title": "Maximum 85% Ceiling", "step_text": "Under federal law, no matter how high your income is, at least 15% of your Social Security benefit is ALWAYS completely exempt from federal income tax."}
        ],
        "faqs": [
            {"q": "Are Social Security tax thresholds adjusted for inflation?", "a": "NO! The thresholds ($25k Single / $32k MFJ) were established in 1983 and were deliberately never indexed to inflation. As a result, while only 10% of retirees paid tax in 1984, over 55% of retirees pay tax on their benefits today."},
            {"q": "Do states tax Social Security benefits?", "a": "Most states (38 states plus DC) do not tax Social Security benefits. Only 10 states (Colorado, Connecticut, Minnesota, Montana, New Mexico, Rhode Island, Utah, Vermont, West Virginia, and Missouri) tax a portion of benefits under specific state rules."}
        ],
        "js_logic": """
          const ss = getNum('annual_social_security_benefit');
          const other = getNum('other_taxable_income');
          const muni = getNum('tax_exempt_municipal_interest');
          const status = getNum('filing_status_ss');

          const halfSs = ss * 0.50;
          const combined = other + muni + halfSs;

          const t1 = status === 2 ? 32000 : 25000;
          const t2 = status === 2 ? 44000 : 34000;

          let taxableSs = 0;
          let tierName = 'Tier 0 (0% Taxable)';

          if (combined > t2) {
            tierName = 'Tier 2 (Up to 85% Taxable)';
            const excessT2 = combined - t2;
            const baseT1 = (t2 - t1) * 0.50;
            taxableSs = Math.min(ss * 0.85, baseT1 + (excessT2 * 0.85));
          } else if (combined > t1) {
            tierName = 'Tier 1 (Up to 50% Taxable)';
            taxableSs = Math.min(ss * 0.50, (combined - t1) * 0.50);
          }

          const taxFree = Math.max(0, ss - taxableSs);
          const taxablePct = ss > 0 ? (taxableSs / ss) * 100 : 0;
          const taxFreePct = 100 - taxablePct;

          setDisp('taxable_social_security_amount', '$' + Math.round(taxableSs).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + taxablePct.toFixed(1) + '%)');
          setDisp('provisional_combined_income', '$' + Math.round(combined).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('tax_free_benefit_share', '$' + Math.round(taxFree).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + taxFreePct.toFixed(1) + '% Tax-Free)');
          setDisp('tax_tier_category', tierName);
        """
    },
    {
        "slug": "medicare-irmaa-surcharge",
        "category": "finance",
        "name": "Medicare IRMAA Surcharge & Surtax Calculator",
        "description": "Calculate Medicare Part B and Part D Income-Related Monthly Adjustment Amount (IRMAA) premium surcharges and cliff threshold triggers.",
        "hero_badge": "Healthcare Policy • Medicare IRMAA Matrix",
        "formula_display": "Total Medicare Premium = Base Premium ($174.70) + Part B IRMAA Surcharge + Part D Surcharge",
        "fields": [
            {"id": "modified_agi_irmaa", "label": "Modified AGI from 2 Years Prior (2022 MAGI for 2024)", "default": 225000, "prefix": "$", "min": 50000, "max": 2000000, "step": 5000, "hint": "IRS Form 1040 line 11 + tax-exempt interest"},
            {"id": "medicare_filing_status", "label": "Filing Status (1 = Single, 2 = Married Filing Jointly)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "Threshold tier schedules"}
        ],
        "metrics": [
            {"id": "monthly_part_b_premium", "label": "Monthly Part B Premium per Person", "default_display": "$244.60 / mo", "highlight": True},
            {"id": "annual_household_surcharge", "label": "Annual Household IRMAA Surcharge (2 people)", "default_display": "$1,977.60 / yr", "highlight": True},
            {"id": "irmaa_tier_classification", "label": "IRMAA Income Bracket Tier", "default_display": "Tier 1 ($206k - $258k MFJ)", "highlight": True},
            {"id": "part_d_monthly_surcharge", "label": "Part D Prescription Drug Surcharge", "default_display": "+$12.90 / mo per person"}
        ],
        "proof_steps": [
            {"step_title": "The 2-Year Lookback Rule", "step_text": "Social Security sets Medicare premiums based on tax returns from 2 years prior: 2024 Medicare premiums are determined by 2022 tax returns."},
            {"step_title": "The Brutal Cliff Effect", "step_text": "Unlike income tax brackets which tax only the incremental dollars, IRMAA has strict cliff thresholds. Exceeding a tier limit by even $1 triggers the full annual surcharge on both spouses."},
            {"step_title": "Part B and Part D Surcharge Tiers", "step_text": "Premiums scale from standard $174.70/mo up to $594.00/mo for high-income earners (MAGI > $500k Single / $750k MFJ)."}
        ],
        "faqs": [
            {"q": "Can you appeal an IRMAA surcharge?", "a": "YES! If your income dropped due to a qualifying Life-Changing Event (marriage, divorce, death of spouse, retirement, or work reduction), you can file IRS Form SSA-44 to recalculate premiums based on current-year income."},
            {"q": "How can retirees avoid the IRMAA cliff?", "a": "Retirees utilize strategic Roth conversions prior to age 63, Qualified Charitable Distributions (QCDs) for RMDs, and drawing from non-taxable cash reserves to keep MAGI just $1 below IRMAA tier cliffs."}
        ],
        "js_logic": """
          const magi = getNum('modified_agi_irmaa');
          const isMfj = getNum('medicare_filing_status') === 2;

          // 2024 IRMAA Tiers (Single vs MFJ)
          const basePartB = 174.70;
          let partB = basePartB;
          let partD = 0;
          let tierName = 'Standard Base Premium (No IRMAA)';

          if (isMfj) {
            if (magi > 750000) { partB = 594.00; partD = 81.00; tierName = 'Tier 5 (≥ $750k MFJ)'; }
            else if (magi > 386000) { partB = 559.00; partD = 74.20; tierName = 'Tier 4 ($386k - $750k MFJ)'; }
            else if (magi > 322000) { partB = 454.20; partD = 53.80; tierName = 'Tier 3 ($322k - $386k MFJ)'; }
            else if (magi > 258000) { partB = 349.40; partD = 33.30; tierName = 'Tier 2 ($258k - $322k MFJ)'; }
            else if (magi > 206000) { partB = 244.60; partD = 12.90; tierName = 'Tier 1 ($206k - $258k MFJ)'; }
          } else {
            if (magi > 500000) { partB = 594.00; partD = 81.00; tierName = 'Tier 5 (≥ $500k Single)'; }
            else if (magi > 193000) { partB = 559.00; partD = 74.20; tierName = 'Tier 4 ($193k - $500k Single)'; }
            else if (magi > 161000) { partB = 454.20; partD = 53.80; tierName = 'Tier 3 ($161k - $193k Single)'; }
            else if (magi > 129000) { partB = 349.40; partD = 33.30; tierName = 'Tier 2 ($129k - $161k Single)'; }
            else if (magi > 103000) { partB = 244.60; partD = 12.90; tierName = 'Tier 1 ($103k - $129k Single)'; }
          }

          const surchargePerPerson = (partB - basePartB) + partD;
          const peopleCount = isMfj ? 2 : 1;
          const totalAnnualSurcharge = surchargePerPerson * 12 * peopleCount;

          setDisp('monthly_part_b_premium', '$' + partB.toFixed(2) + ' / mo');
          setDisp('annual_household_surcharge', '$' + totalAnnualSurcharge.toFixed(2) + ' / yr' + (isMfj ? ' (2 people)' : ''));
          setDisp('irmaa_tier_classification', tierName);
          setDisp('part_d_monthly_surcharge', partD > 0 ? ('+$' + partD.toFixed(2) + ' / mo per person') : '$0.00 / mo');
        """
    },
    {
        "slug": "futa-suta-payroll",
        "category": "finance",
        "name": "Employer FUTA & SUTA Unemployment Tax Calculator",
        "description": "Calculate Federal Unemployment Tax Act (FUTA 0.6% net) and State Unemployment Tax (SUTA) employer liabilities across payroll wage bases.",
        "hero_badge": "Employer Payroll • Unemployment Tax Matrix",
        "formula_display": "FUTA = min(Wages, $7,000) × 0.6% | SUTA = min(Wages, State Wage Base) × SUTA Rate %",
        "fields": [
            {"id": "total_employees_count", "label": "Number of Full-Time Employees", "default": 8, "min": 1, "max": 500, "step": 1, "hint": "Count of employees on payroll"},
            {"id": "avg_annual_employee_wage", "label": "Average Annual Wage per Employee", "default": 65000, "prefix": "$", "min": 10000, "max": 500000, "step": 2500, "hint": "Average salary per worker"},
            {"id": "state_suta_tax_rate_pct", "label": "Company Assigned SUTA Tax Rate (%)", "default": 2.7, "suffix": "%", "min": 0.1, "max": 12.0, "step": 0.1, "hint": "State employer experience tax rate"},
            {"id": "state_wage_base_limit", "label": "State Unemployment Tax Wage Base", "default": 10000, "prefix": "$", "min": 7000, "max": 65000, "step": 500, "hint": "State cap (CA $7k, NY $12.5k, WA $68.5k)"}
        ],
        "metrics": [
            {"id": "total_employer_unemployment_tax", "label": "Total Employer Unemployment Tax", "default_display": "$2,496.00 / yr", "highlight": True},
            {"id": "annual_futa_tax_total", "label": "Total Federal FUTA Tax Due", "default_display": "$336.00 / yr ($42/employee)", "highlight": True},
            {"id": "annual_suta_tax_total", "label": "Total State SUTA Tax Due", "default_display": "$2,160.00 / yr ($270/employee)", "highlight": True},
            {"id": "cost_per_employee_payroll", "label": "Annual Unemployment Cost per Worker", "default_display": "$312.00 / employee"}
        ],
        "proof_steps": [
            {"step_title": "Federal FUTA Tax Rate and Cap", "step_text": "FUTA is an employer-paid tax (never withheld from employee wages). The gross rate is 6.0%, but employers paying on-time state unemployment receive a 5.4% credit, resulting in an effective net rate of 0.6% on the first $7,000 of wages: $7,000 × 0.6% = $42.00 per employee per year."},
            {"step_title": "State SUTA Calculations", "step_text": "SUTA Tax = min(Wages, State Wage Base) × SUTA Experience Rate. For 8 workers at a $10,000 state cap and 2.7% rate: 8 × $10,000 × 2.7% = $2,160."},
            {"step_title": "Employer Cost Consolidation", "step_text": "Total Tax = FUTA ($336) + SUTA ($2,160) = $2,496/year ($312/employee)."}
        ],
        "faqs": [
            {"q": "Do employees pay FUTA or SUTA tax?", "a": "In 47 out of 50 states, unemployment taxes are paid 100% by the employer with zero employee deductions. Only Alaska, New Jersey, and Pennsylvania require a modest employee SUTA co-contribution."},
            {"q": "How can an employer lower their SUTA tax rate?", "a": "SUTA rates are based on an employer's 'experience rating.' Minimizing employee layoffs and turnover keeps your experience rating low, dropping state tax rates from 8%+ down to under 1%."}
        ],
        "js_logic": """
          const count = getNum('total_employees_count');
          const wage = getNum('avg_annual_employee_wage');
          const sutaRate = (getNum('state_suta_tax_rate_pct') || 2.7) / 100;
          const sutaCap = getNum('state_wage_base_limit') || 10000;

          const futaPerWorker = Math.min(wage, 7000) * 0.006;
          const sutaPerWorker = Math.min(wage, sutaCap) * sutaRate;
          const totalPerWorker = futaPerWorker + sutaPerWorker;

          const totalFuta = futaPerWorker * count;
          const totalSuta = sutaPerWorker * count;
          const totalTax = totalPerWorker * count;

          setDisp('total_employer_unemployment_tax', '$' + Math.round(totalTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('annual_futa_tax_total', '$' + Math.round(totalFuta).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr ($' + futaPerWorker.toFixed(0) + '/employee)');
          setDisp('annual_suta_tax_total', '$' + Math.round(totalSuta).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr ($' + sutaPerWorker.toFixed(0) + '/employee)');
          setDisp('cost_per_employee_payroll', '$' + totalPerWorker.toFixed(2) + ' / employee');
        """
    }
]
