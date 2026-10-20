"""
scripts/data_b2b_saas.py
25 High-Value B2B, SaaS, Startup & Venture Capital Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

B2B_SAAS_CALCULATORS = [
    {
        "slug": "cac",
        "category": "finance",
        "name": "Customer Acquisition Cost (CAC) Calculator",
        "description": "Calculate blended and paid Customer Acquisition Cost (CAC) from total sales and marketing expenditure divided by new acquired customers.",
        "hero_badge": "B2B SaaS Metrics • CAC Unit Economics",
        "formula_display": "CAC = Total Sales & Marketing Spend / Number of New Customers Acquired",
        "fields": [
            {"id": "marketing_spend", "label": "Total Marketing & Ad Spend", "default": 25000, "prefix": "$", "min": 500, "max": 2000000, "step": 500, "hint": "Paid advertising, software, agency, and creative fees"},
            {"id": "sales_spend", "label": "Sales Salaries & Commissions", "default": 35000, "prefix": "$", "min": 500, "max": 2000000, "step": 500, "hint": "SDR/AE salaries, bonuses, and commission payouts"},
            {"id": "new_customers", "label": "New Customers Acquired", "default": 120, "min": 1, "max": 50000, "step": 1, "hint": "Total new paying customers in the measurement window"}
        ],
        "metrics": [
            {"id": "blended_cac", "label": "Blended Customer Acquisition Cost", "default_display": "$500.00", "highlight": True},
            {"id": "total_acquisition_spend", "label": "Total S&M Expenditure", "default_display": "$60,000.00"},
            {"id": "marketing_cac_share", "label": "Marketing Share per Customer", "default_display": "$208.33"},
            {"id": "sales_cac_share", "label": "Sales Share per Customer", "default_display": "$291.67"}
        ],
        "proof_steps": [
            {"step_title": "Direct S&M Capital Consolidation", "step_text": "Total acquisition expenditure C_total = Marketing Spend + Sales Team Costs (salaries, commissions, CRM overhead, and paid ad media)."},
            {"step_title": "Cohort Unit Economics Ratio", "step_text": "CAC = C_total / N_acquired. Dividing total capital deployed by the cohort of acquired paying accounts yields average unit acquisition cost."},
            {"step_title": "Blended vs Paid Segmentation", "step_text": "Blended CAC incorporates organic word-of-mouth users; Paid CAC isolates strictly direct paid channel acquisition efficiency."}
        ],
        "faqs": [
            {"q": "What is a good Customer Acquisition Cost (CAC) for B2B SaaS?", "a": "A healthy CAC depends entirely on Customer Lifetime Value (LTV). Generally, a viable SaaS business model requires an LTV:CAC ratio of at least 3:1, with CAC recovered within 12 months."},
            {"q": "Should overhead and software tools be included in CAC?", "a": "Yes! Fully loaded CAC must include sales salaries, marketing tools (HubSpot, Salesforce), creative agencies, and travel costs in addition to direct paid ad spend."}
        ],
        "js_logic": """
          const mkt = getNum('marketing_spend');
          const sales = getNum('sales_spend');
          const cust = getNum('new_customers') || 1;

          const totalSpend = mkt + sales;
          const cac = totalSpend / cust;
          const mktShare = mkt / cust;
          const salesShare = sales / cust;

          setDisp('blended_cac', '$' + cac.toFixed(2));
          setDisp('total_acquisition_spend', '$' + totalSpend.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('marketing_cac_share', '$' + mktShare.toFixed(2));
          setDisp('sales_cac_share', '$' + salesShare.toFixed(2));
        """
    },
    {
        "slug": "clv-ltv",
        "category": "finance",
        "name": "Customer Lifetime Value (LTV / CLV) Calculator",
        "description": "Calculate Customer Lifetime Value (LTV) from Average Revenue Per Account (ARPA), gross margin percentage, and customer churn rate.",
        "hero_badge": "SaaS Unit Economics • LTV Vector Matrix",
        "formula_display": "LTV = (ARPU × Gross Margin %) / Churn Rate",
        "fields": [
            {"id": "arpa_monthly", "label": "Average Monthly Revenue / Customer (ARPA)", "default": 250, "prefix": "$", "min": 5, "max": 50000, "step": 10, "hint": "Average monthly subscription bill per account"},
            {"id": "gross_margin_pct", "label": "Gross Margin Percentage", "default": 80, "suffix": "%", "min": 20, "max": 95, "step": 1, "hint": "SaaS typically 75% to 85% gross margin"},
            {"id": "churn_monthly_pct", "label": "Monthly Customer Churn Rate", "default": 2.5, "suffix": "%", "min": 0.1, "max": 20, "step": 0.1, "hint": "Percentage of customers canceling each month"}
        ],
        "metrics": [
            {"id": "customer_ltv", "label": "Customer Lifetime Value (LTV)", "default_display": "$8,000.00", "highlight": True},
            {"id": "average_lifespan", "label": "Average Customer Lifespan", "default_display": "40.0 months (3.3 yrs)", "highlight": True},
            {"id": "annual_arpa", "label": "Annual Revenue per Account (ACV)", "default_display": "$3,000.00 / yr"},
            {"id": "margin_contribution", "label": "Monthly Gross Margin Contribution", "default_display": "$200.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Customer Lifespan Geometric Series", "step_text": "Assuming a constant monthly churn rate c, average customer lifespan in months is T = 1 / c (e.g. 1 / 0.025 = 40 months)."},
            {"step_title": "Gross Margin Adjusted Revenue Contribution", "step_text": "Net revenue contribution per month M = ARPA · (Gross Margin% / 100)."},
            {"step_title": "Lifetime Economic Value", "step_text": "LTV = M · T = [ARPA · Gross Margin%] / Churn. Gross margin adjustment is mandatory to prevent inflating lifetime value with delivery cost."}
        ],
        "faqs": [
            {"q": "Why is gross margin required when calculating LTV?", "a": "Calculating LTV on top-line revenue without gross margin ignores hosting, customer support, and payment processing costs, falsely inflating how much you can afford to spend on acquisition."},
            {"q": "What is a healthy monthly churn rate for B2B SaaS?", "a": "For enterprise SaaS ($25k+ ACV), monthly churn should be under 0.5% to 1.0% (net negative churn). For mid-market SaaS, 1.0% to 2.0% is typical. For SMB SaaS, 2.5% to 4.0% is common."}
        ],
        "js_logic": """
          const arpa = getNum('arpa_monthly');
          const margin = (getNum('gross_margin_pct') || 80) / 100;
          const churn = (getNum('churn_monthly_pct') || 2.5) / 100;

          const lifespanMo = churn > 0 ? (1 / churn) : 0;
          const ltv = churn > 0 ? ((arpa * margin) / churn) : 0;
          const acv = arpa * 12;
          const marginContrib = arpa * margin;

          setDisp('customer_ltv', '$' + ltv.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('average_lifespan', lifespanMo.toFixed(1) + ' months (' + (lifespanMo / 12).toFixed(1) + ' yrs)');
          setDisp('annual_arpa', '$' + acv.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('margin_contribution', '$' + marginContrib.toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "ltv-cac-ratio",
        "category": "finance",
        "name": "LTV:CAC Ratio & Payback Period Calculator",
        "description": "Calculate the gold-standard SaaS unit economics ratio (LTV:CAC) and months required to recover acquisition cash outflows.",
        "hero_badge": "Venture Capital • Capital Efficiency Matrix",
        "formula_display": "LTV:CAC = Customer Lifetime Value / CAC | Payback Months = CAC / (ARPA × Gross Margin %)",
        "fields": [
            {"id": "cac_input", "label": "Customer Acquisition Cost (CAC)", "default": 1800, "prefix": "$", "min": 50, "max": 100000, "step": 50, "hint": "Fully loaded cost to acquire one customer"},
            {"id": "ltv_input", "label": "Customer Lifetime Value (LTV)", "default": 7200, "prefix": "$", "min": 100, "max": 500000, "step": 100, "hint": "Gross-margin adjusted lifetime value"},
            {"id": "monthly_arpa", "label": "Average Monthly Revenue (ARPA)", "default": 250, "prefix": "$", "min": 10, "max": 50000, "step": 10, "hint": "Monthly recurring bill per customer"},
            {"id": "margin_pct", "label": "Gross Margin Percentage", "default": 80, "suffix": "%", "min": 20, "max": 95, "step": 1, "hint": "Cost of goods sold margin"}
        ],
        "metrics": [
            {"id": "ltv_cac_score", "label": "LTV to CAC Ratio", "default_display": "4.00 : 1.0", "highlight": True},
            {"id": "cac_payback_months", "label": "CAC Payback Horizon", "default_display": "9.0 months", "highlight": True},
            {"id": "capital_health", "label": "VC Benchmark Assessment", "default_display": "Optimal Growth Efficiency (3:1 to 5:1)"},
            {"id": "net_profit_per_customer", "label": "Net Profit Contribution / Customer", "default_display": "$5,400.00"}
        ],
        "proof_steps": [
            {"step_title": "Unit Economic Multiplier", "step_text": "LTV:CAC Ratio = LTV / CAC. Benchmarks: < 1.0 = Value destructive; 1.0–2.9 = Sub-optimal margin; 3.0–5.0 = Gold standard scalable growth; > 5.0 = Under-investing in acquisition."},
            {"step_title": "Cash Flow Payback Period", "step_text": "Payback Period in Months = CAC / (ARPA × Gross Margin%). Measures how many months of customer subscription cash flow are required to recover upfront marketing and sales cash outflows."},
            {"step_title": "Net Economic Profit Contribution", "step_text": "Net Capital Surplus = LTV - CAC. Represents net scalable profit returned per customer account."}
        ],
        "faqs": [
            {"q": "What is an ideal CAC payback period for SaaS?", "a": "Top-quartile venture-backed B2B SaaS companies target a CAC payback period between 8 and 12 months. Payback longer than 18 months creates severe working capital constraints and cash drag."},
            {"q": "Can an LTV:CAC ratio be too high?", "a": "Yes! An LTV:CAC ratio above 5:1 or 6:1 usually indicates that you are under-spending on sales and marketing, leaving significant market share on the table for competitors."}
        ],
        "js_logic": """
          const cac = getNum('cac_input') || 1;
          const ltv = getNum('ltv_input');
          const arpa = getNum('monthly_arpa');
          const margin = (getNum('margin_pct') || 80) / 100;

          const ratio = ltv / cac;
          const monthlyGrossProfit = arpa * margin;
          const payback = monthlyGrossProfit > 0 ? (cac / monthlyGrossProfit) : 0;
          const netProfit = ltv - cac;

          let status = 'Optimal Efficiency (3:1 to 5:1)';
          if (ratio < 1.0) status = 'Value Destructive (< 1:1)';
          else if (ratio < 3.0) status = 'Low Return (< 3:1)';
          else if (ratio > 5.0) status = 'Under-Investing (> 5:1)';

          setDisp('ltv_cac_score', ratio.toFixed(2) + ' : 1.0');
          setDisp('cac_payback_months', payback.toFixed(1) + ' months');
          setDisp('capital_health', status);
          setDisp('net_profit_per_customer', '$' + netProfit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "churn-rate",
        "category": "finance",
        "name": "Customer & Revenue Churn Rate Calculator",
        "description": "Calculate logo churn, gross revenue churn, net revenue retention (NRR), and annualized churn compound curves.",
        "hero_badge": "Retention Engineering • Churn Matrix",
        "formula_display": "Customer Churn % = (Customers Lost / Starting Customers) × 100",
        "fields": [
            {"id": "starting_customers", "label": "Starting Customers (Beginning of Month)", "default": 1000, "min": 10, "max": 500000, "step": 10, "hint": "Active paying customer count on day 1"},
            {"id": "lost_customers", "label": "Customers Canceled / Lost", "default": 25, "min": 0, "max": 100000, "step": 1, "hint": "Accounts downgraded or terminated during month"},
            {"id": "starting_mrr", "label": "Starting Monthly Revenue (MRR)", "default": 100000, "prefix": "$", "min": 1000, "max": 10000000, "step": 1000, "hint": "Beginning of period recurring revenue"},
            {"id": "expansion_mrr", "label": "Expansion / Upsell MRR", "default": 6000, "prefix": "$", "min": 0, "max": 500000, "step": 500, "hint": "Revenue expansion from existing customer upgrades"}
        ],
        "metrics": [
            {"id": "monthly_churn_pct", "label": "Monthly Customer Churn", "default_display": "2.50% / mo", "highlight": True},
            {"id": "annualized_churn", "label": "Annualized Compound Churn", "default_display": "26.24% / yr", "highlight": True},
            {"id": "net_revenue_retention", "label": "Net Revenue Retention (NRR)", "default_display": "103.50% (Net Expansion)"},
            {"id": "customer_half_life", "label": "Customer Cohort Half-Life", "default_display": "27.4 months"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Logo Churn Formulation", "step_text": "Customer Churn Rate c_mo = Lost Customers / Starting Customers. Measures account attrition rate."},
            {"step_title": "Compound Annualized Churn Curve", "step_text": "Because churn compounds each period, annualized churn is non-linear: c_annual = 1 - (1 - c_mo)¹². For example, 2.5% monthly churn produces 1 - (0.975)¹² = 26.24% annual account loss."},
            {"step_title": "Net Revenue Retention (NRR)", "step_text": "NRR = [(Starting MRR - Churned MRR + Expansion MRR) / Starting MRR] × 100%. NRR above 100% indicates that expansion revenue outpaces churn."}
        ],
        "faqs": [
            {"q": "What is the difference between Gross Churn and Net Churn?", "a": "Gross churn only measures lost dollars from cancellations and downgrades. Net churn subtracts expansion revenue from retained accounts, allowing net churn to be negative (which is ideal)."},
            {"q": "What is Net Negative Churn?", "a": "Net negative churn occurs when upsells and expansion from retained customers exceed the revenue lost from churned customers (NRR > 100%). Your business grows even with zero new customer acquisition."}
        ],
        "js_logic": """
          const startCust = getNum('starting_customers') || 1;
          const lostCust = getNum('lost_customers');
          const startMrr = getNum('starting_mrr') || 1;
          const expMrr = getNum('expansion_mrr');

          const moChurn = (lostCust / startCust);
          const annualChurn = 1 - Math.pow(1 - moChurn, 12);
          const lostMrr = startMrr * moChurn;
          const nrr = ((startMrr - lostMrr + expMrr) / startMrr) * 100;
          const halfLife = moChurn > 0 ? (Math.log(0.5) / Math.log(1 - moChurn)) : 0;

          setDisp('monthly_churn_pct', (moChurn * 100).toFixed(2) + '% / mo');
          setDisp('annualized_churn', (annualChurn * 100).toFixed(2) + '% / yr');
          setDisp('net_revenue_retention', nrr.toFixed(2) + '% ' + (nrr >= 100 ? '(Net Expansion)' : '(Net Contraction)'));
          setDisp('customer_half_life', halfLife > 0 ? halfLife.toFixed(1) + ' months' : 'No churn');
        """
    },
    {
        "slug": "mrr-arr",
        "category": "finance",
        "name": "MRR to ARR & Net New MRR Calculator",
        "description": "Calculate Annual Recurring Revenue (ARR) run rate, Net New MRR, expansion rate, and contraction churn components.",
        "hero_badge": "Subscription Economics • Recurring Revenue Matrix",
        "formula_display": "ARR = MRR × 12 | Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR",
        "fields": [
            {"id": "new_mrr", "label": "New Customer MRR", "default": 8500, "prefix": "$", "min": 0, "max": 1000000, "step": 500, "hint": "MRR from newly signed accounts"},
            {"id": "expansion_mrr", "label": "Expansion / Upgrade MRR", "default": 3200, "prefix": "$", "min": 0, "max": 500000, "step": 100, "hint": "Existing customers upgrading tiers or adding seats"},
            {"id": "contraction_mrr", "label": "Contraction / Downgrade MRR", "default": 800, "prefix": "$", "min": 0, "max": 100000, "step": 50, "hint": "Existing customers downgrading plans"},
            {"id": "churned_mrr", "label": "Churned / Canceled MRR", "default": 1900, "prefix": "$", "min": 0, "max": 200000, "step": 100, "hint": "MRR completely terminated from cancellations"}
        ],
        "metrics": [
            {"id": "net_new_mrr", "label": "Net New MRR Added", "default_display": "+$9,000.00 / mo", "highlight": True},
            {"id": "annual_arr_added", "label": "Net ARR Added (Annualized)", "default_display": "+$108,000.00 / yr", "highlight": True},
            {"id": "gross_new_mrr", "label": "Gross New Inflow", "default_display": "$11,700.00 / mo"},
            {"id": "total_mrr_churn", "label": "Total Revenue Leakage", "default_display": "-$2,700.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Annual Run Rate Equivalence", "step_text": "ARR = MRR × 12. Annualizes recurring monthly cash subscriptions."},
            {"step_title": "Net New MRR Decomposition", "step_text": "Net New MRR = (New MRR + Expansion MRR) - (Contraction MRR + Churned MRR)."},
            {"step_title": "Revenue Growth Quality Assessment", "step_text": "High-efficiency SaaS organizations maintain Quick Ratios: Quick Ratio = (New MRR + Expansion MRR) / (Contraction MRR + Churned MRR) > 4.0."}
        ],
        "faqs": [
            {"q": "What is the difference between MRR and GAAP Revenue?", "a": "MRR is a non-GAAP normalized operational metric measuring monthly predictable recurring subscription commitments. GAAP revenue recognizes earned revenue according to ASC 606 standards over the service delivery period."},
            {"q": "Should one-time setup fees be included in MRR?", "a": "No! One-time implementation, onboarding, and professional services fees must be excluded from MRR because they do not recur."}
        ],
        "js_logic": """
          const newM = getNum('new_mrr');
          const expM = getNum('expansion_mrr');
          const conM = getNum('contraction_mrr');
          const chuM = getNum('churned_mrr');

          const netNew = (newM + expM) - (conM + chuM);
          const arrAdded = netNew * 12;
          const inflow = newM + expM;
          const outflow = conM + chuM;

          setDisp('net_new_mrr', (netNew >= 0 ? '+$' : '-$') + Math.abs(netNew).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('annual_arr_added', (arrAdded >= 0 ? '+$' : '-$') + Math.abs(arrAdded).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('gross_new_mrr', '$' + inflow.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('total_mrr_churn', '-$' + outflow.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
        """
    },
    {
        "slug": "runway-burn",
        "category": "finance",
        "name": "Startup Cash Runway & Burn Rate Calculator",
        "description": "Calculate net monthly burn rate, gross cash outflows, and exact operational runway in months until zero cash date (ZCD).",
        "hero_badge": "Startup Treasury • Cash Runway Vector",
        "formula_display": "Runway (Months) = Current Cash Balance / Net Monthly Burn Rate",
        "fields": [
            {"id": "cash_balance", "label": "Current Bank Cash Balance", "default": 750000, "prefix": "$", "min": 5000, "max": 100000000, "step": 10000, "hint": "Total available liquid cash in operating accounts"},
            {"id": "monthly_revenue", "label": "Monthly Cash Collections (Revenue)", "default": 35000, "prefix": "$", "min": 0, "max": 5000000, "step": 1000, "hint": "Actual monthly cash incoming"},
            {"id": "monthly_expenses", "label": "Monthly Operating Expenses (OpEx)", "default": 85000, "prefix": "$", "min": 1000, "max": 10000000, "step": 2500, "hint": "Payroll, hosting, rent, and overhead"}
        ],
        "metrics": [
            {"id": "cash_runway_months", "label": "Available Cash Runway", "default_display": "15.0 months", "highlight": True},
            {"id": "net_burn_rate", "label": "Net Monthly Burn Rate", "default_display": "$50,000.00 / mo", "highlight": True},
            {"id": "gross_burn_rate", "label": "Gross Monthly Burn Rate", "default_display": "$85,000.00 / mo"},
            {"id": "fundraising_deadline", "label": "Fundraising Kickoff Window", "default_display": "In 9.0 Months (6mo buffer)"}
        ],
        "proof_steps": [
            {"step_title": "Gross vs Net Burn Differential", "step_text": "Gross Burn = Total Monthly Cash Operating Expenses. Net Burn = Gross Expenses - Monthly Cash Collections."},
            {"step_title": "Runway Derivation", "step_text": "Runway (Months) = Cash Balance / Net Burn Rate. Represents exact timeline until Zero Cash Date (ZCD)."},
            {"step_title": "Fundraising Buffer Heuristic", "step_text": "Because institutional Series A/B venture capital rounds average 4 to 6 months to close, founders must kick off fundraising when runway reaches 6 months."}
        ],
        "faqs": [
            {"q": "What is considered a safe cash runway for startups?", "a": "Early-stage startups should maintain 18 to 24 months of cash runway. Having under 6 months of runway significantly weakens your negotiating leverage with investors."},
            {"q": "How can a startup extend runway without raising capital?", "a": "Founders can extend runway by cutting non-essential SaaS tooling, freezing non-revenue headcount, renegotiating cloud hosting commitments, and converting customers to upfront annual billing."}
        ],
        "js_logic": """
          const cash = getNum('cash_balance');
          const rev = getNum('monthly_revenue');
          const exp = getNum('monthly_expenses');

          const netBurn = Math.max(0, exp - rev);
          const runway = netBurn > 0 ? (cash / netBurn) : 999;
          const fundDeadline = Math.max(0, runway - 6);

          setDisp('cash_runway_months', netBurn > 0 ? runway.toFixed(1) + ' months' : 'Profitable (Infinite)');
          setDisp('net_burn_rate', '$' + netBurn.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('gross_burn_rate', '$' + exp.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('fundraising_deadline', netBurn > 0 ? 'In ' + fundDeadline.toFixed(1) + ' Months (6mo buffer)' : 'Default Alive');
        """
    },
    {
        "slug": "saas-magic-number",
        "category": "finance",
        "name": "SaaS Magic Number & Sales Efficiency Calculator",
        "description": "Calculate the SaaS Magic Number measuring Net New ARR generated per dollar spent on sales and marketing.",
        "hero_badge": "Growth Engineering • Magic Number Matrix",
        "formula_display": "Magic Number = [(Q_curr Revenue - Q_prev Revenue) × 4] / Q_prev Sales & Marketing",
        "fields": [
            {"id": "curr_q_revenue", "label": "Current Quarter Revenue", "default": 650000, "prefix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Total revenue in quarter Q"},
            {"id": "prev_q_revenue", "label": "Prior Quarter Revenue", "default": 500000, "prefix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Total revenue in quarter Q-1"},
            {"id": "prev_q_sm_spend", "label": "Prior Quarter S&M Spend", "default": 450000, "prefix": "$", "min": 5000, "max": 50000000, "step": 5000, "hint": "Sales & marketing expenditure in quarter Q-1"}
        ],
        "metrics": [
            {"id": "magic_number_score", "label": "SaaS Magic Number", "default_display": "1.33", "highlight": True},
            {"id": "growth_efficiency", "label": "Capital Efficiency Rating", "default_display": "Exceptional Efficiency (> 1.0)", "highlight": True},
            {"id": "net_new_arr", "label": "Annualized Net New ARR", "default_display": "$600,000.00 / yr"},
            {"id": "action_directive", "label": "Capital Allocation Recommendation", "default_display": "Pour gas on the fire (Accelerate S&M hiring)"}
        ],
        "proof_steps": [
            {"step_title": "Quarterly Sequential Net ARR Growth", "step_text": "Annualized New ARR Generated = (Revenue_Q - Revenue_Q-1) × 4."},
            {"step_title": "Magic Number Ratio", "step_text": "Magic Number = [Annualized Net New ARR] / Sales & Marketing Expense_Q-1."},
            {"step_title": "Benchmark Allocation Heuristic", "step_text": "< 0.5 = Broken model (evaluate churn and pricing); 0.5–0.75 = Acceptable efficiency; 0.75–1.0 = Strong unit economics; > 1.0 = Pour gas on the fire (sales capacity pays back in under 12 months)."}
        ],
        "faqs": [
            {"q": "Who created the SaaS Magic Number?", "a": "The SaaS Magic Number was popularized by venture capital firm Scale Venture Partners as a standard metric to evaluate when a software company is ready to scale go-to-market spending."},
            {"q": "Why does the formula use the previous quarter's sales & marketing spend?", "a": "Sales cycles in B2B require time; marketing spend in quarter Q-1 typically generates closed deals that show up as recognized revenue in quarter Q."}
        ],
        "js_logic": """
          const qCurr = getNum('curr_q_revenue');
          const qPrev = getNum('prev_q_revenue');
          const smPrev = getNum('prev_q_sm_spend') || 1;

          const deltaRev = qCurr - qPrev;
          const annualizedNewArr = deltaRev * 4;
          const magic = annualizedNewArr / smPrev;

          let rating = 'Strong (> 0.75)';
          let rec = 'Invest aggressively';
          if (magic < 0.5) {
            rating = 'Poor (< 0.50)';
            rec = 'Pause hiring; fix onboarding & churn';
          } else if (magic < 0.75) {
            rating = 'Moderate (0.50 - 0.75)';
            rec = 'Optimize conversion before scaling';
          } else if (magic > 1.0) {
            rating = 'Exceptional (> 1.0)';
            rec = 'Pour gas on the fire (Accelerate S&M hiring)';
          }

          setDisp('magic_number_score', magic.toFixed(2));
          setDisp('growth_efficiency', rating);
          setDisp('net_new_arr', '$' + annualizedNewArr.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('action_directive', rec);
        """
    },
    {
        "slug": "saas-rule-of-40",
        "category": "finance",
        "name": "SaaS Rule of 40 Calculator",
        "description": "Calculate the Rule of 40 score balancing YoY ARR revenue growth rate percentage and Free Cash Flow (FCF) margin percentage.",
        "hero_badge": "Public SaaS Valuation • Rule of 40 Matrix",
        "formula_display": "Rule of 40 Score = YoY Revenue Growth Rate (%) + Profit Margin (%)",
        "fields": [
            {"id": "growth_rate_pct", "label": "Year-over-Year (YoY) Growth Rate", "default": 45, "suffix": "%", "min": -50, "max": 300, "step": 1, "hint": "YoY ARR or GAAP revenue growth percentage"},
            {"id": "profit_margin_pct", "label": "Profitability (FCF or EBITDA Margin)", "default": 5, "suffix": "%", "min": -100, "max": 80, "step": 1, "hint": "Free Cash Flow or EBITDA margin percentage"}
        ],
        "metrics": [
            {"id": "rule_of_40_score", "label": "Rule of 40 Score", "default_display": "50.0%", "highlight": True},
            {"id": "benchmark_status", "label": "Venture Benchmark Status", "default_display": "Passes Rule of 40 (Top Quartile)", "highlight": True},
            {"id": "valuation_premium", "label": "Expected Public Multiple Premium", "default_display": "Premium EV/ARR Multiple (> 12×)"},
            {"id": "growth_profile", "label": "Operating Strategy Profile", "default_display": "Hypergrowth Scaling (Growth > 40%)"}
        ],
        "proof_steps": [
            {"step_title": "The Rule of 40 Equation", "step_text": "Rule of 40 = Growth Rate% + Free Cash Flow Margin%. For example: 45% growth + 5% FCF margin = 50% score."},
            {"step_title": "Growth vs Profit Trade-off", "step_text": "A SaaS business can operate at negative margins (e.g. -20% FCF) if its growth rate is high enough (e.g. 65% growth = 45% score) and remain an elite financial asset."},
            {"step_title": "Enterprise Multiple Valuation Elasticity", "step_text": "Public market data shows companies beating the Rule of 40 trade at median enterprise value to revenue multiples 2× to 3× higher than sub-40 peers."}
        ],
        "faqs": [
            {"q": "When does the Rule of 40 become relevant for startups?", "a": "The Rule of 40 is most applicable once a SaaS business scales past $5 million to $10 million in ARR. Earlier startups should focus almost exclusively on rapid growth and product-market fit."},
            {"q": "Should EBITDA or Free Cash Flow margin be used?", "a": "Free Cash Flow (FCF) margin is preferred by Wall Street and top private equity investors because it accounts for working capital fluctuations and capitalized software development expenses."}
        ],
        "js_logic": """
          const growth = getNum('growth_rate_pct');
          const margin = getNum('profit_margin_pct');

          const score = growth + margin;

          let status = 'Meets Rule of 40 (Top Tier)';
          let prem = 'Above Average EV/ARR Multiple (8x - 12x)';
          if (score < 25) {
            status = 'Struggling (< 25%)';
            prem = 'Discounted Multiple (< 4x EV/ARR)';
          } else if (score < 40) {
            status = 'Below 40% Threshold';
            prem = 'Market Median Multiple (4x - 7x)';
          } else if (score >= 50) {
            status = 'Passes Rule of 40 (Top Quartile)';
            prem = 'Premium EV/ARR Multiple (> 12x)';
          }

          setDisp('rule_of_40_score', score.toFixed(1) + '%');
          setDisp('benchmark_status', status);
          setDisp('valuation_premium', prem);
          setDisp('growth_profile', growth >= 40 ? 'Hypergrowth Scaling (Growth > 40%)' : 'Balanced / Mature Profile');
        """
    },
    {
        "slug": "net-promoter-score",
        "category": "finance",
        "name": "Net Promoter Score (NPS) Calculator",
        "description": "Calculate Net Promoter Score (NPS), Promoters (9-10), Passives (7-8), Detractors (0-6), and statistical standard error margin.",
        "hero_badge": "Customer Experience • NPS Matrix",
        "formula_display": "NPS = % Promoters (9-10) - % Detractors (0-6)",
        "fields": [
            {"id": "promoters_count", "label": "Promoters (Rated 9 or 10)", "default": 650, "min": 0, "max": 1000000, "step": 10, "hint": "Loyal enthusiasts who refer others"},
            {"id": "passives_count", "label": "Passives (Rated 7 or 8)", "default": 250, "min": 0, "max": 1000000, "step": 10, "hint": "Satisfied but unenthusiastic accounts"},
            {"id": "detractors_count", "label": "Detractors (Rated 0 through 6)", "default": 100, "min": 0, "max": 1000000, "step": 10, "hint": "Unhappy customers prone to churn"}
        ],
        "metrics": [
            {"id": "nps_score", "label": "Net Promoter Score (NPS)", "default_display": "+55.0", "highlight": True},
            {"id": "total_respondents", "label": "Total Survey Respondents", "default_display": "1,000 responses"},
            {"id": "promoter_share", "label": "Promoter Share (%)", "default_display": "65.0%"},
            {"id": "detractor_share", "label": "Detractor Share (%)", "default_display": "10.0%"}
        ],
        "proof_steps": [
            {"step_title": "Response Partitioning", "step_text": "Total Respondents N = Promoters + Passives + Detractors."},
            {"step_title": "Bain & Company NPS Formulation", "step_text": "NPS = [(Promoters / N) × 100] - [(Detractors / N) × 100]. Passives count toward total population N, thereby diluting the percentage."},
            {"step_title": "Score Range Interpretation", "step_text": "NPS ranges from -100 to +100. > 0 is good, > +50 is excellent, and > +70 is world-class customer loyalty (Apple, Costco tier)."}
        ],
        "faqs": [
            {"q": "What is considered a good Net Promoter Score for B2B SaaS?", "a": "For B2B software companies, an NPS above +30 is considered good, above +50 is excellent, and above +70 represents best-in-class product-led growth."},
            {"q": "Why are ratings 7 and 8 excluded from the subtraction?", "a": "Passives (7-8) are satisfied but not enthusiastic enough to proactively recommend your product. They count in the total denominator, naturally moderating the score."}
        ],
        "js_logic": """
          const prom = getNum('promoters_count');
          const pass = getNum('passives_count');
          const det = getNum('detractors_count');

          const total = prom + pass + det;
          const pPct = total > 0 ? (prom / total) * 100 : 0;
          const dPct = total > 0 ? (det / total) * 100 : 0;
          const nps = pPct - dPct;

          setDisp('nps_score', (nps >= 0 ? '+' : '') + nps.toFixed(1));
          setDisp('total_respondents', total.toLocaleString() + ' responses');
          setDisp('promoter_share', pPct.toFixed(1) + '%');
          setDisp('detractor_share', dPct.toFixed(1) + '%');
        """
    },
    {
        "slug": "arpu",
        "category": "finance",
        "name": "Average Revenue Per User (ARPU / ARPA) Calculator",
        "description": "Calculate Average Revenue Per User (ARPU) and Average Revenue Per Account (ARPA) across monthly, quarterly, and annual intervals.",
        "hero_badge": "Monetization Analytics • ARPU Solver",
        "formula_display": "ARPU = Total Period Revenue / Total Active Users",
        "fields": [
            {"id": "total_revenue", "label": "Total Recurring Revenue", "default": 85000, "prefix": "$", "min": 500, "max": 10000000, "step": 1000, "hint": "Revenue generated in measurement month"},
            {"id": "active_users", "label": "Active Users / Subscribers", "default": 340, "min": 1, "max": 1000000, "step": 10, "hint": "Count of active paying user accounts"}
        ],
        "metrics": [
            {"id": "monthly_arpu", "label": "Monthly ARPU / ARPA", "default_display": "$250.00 / mo", "highlight": True},
            {"id": "annual_arpu", "label": "Annualized ARPU (ACV)", "default_display": "$3,000.00 / yr", "highlight": True},
            {"id": "daily_arpu", "label": "Daily Revenue per User", "default_display": "$8.33 / day"},
            {"id": "segment_tier", "label": "Market Segment Tier", "default_display": "Mid-Market ($1k - $5k ACV)"}
        ],
        "proof_steps": [
            {"step_title": "Arithmetic Mean Unit Realization", "step_text": "ARPU = Period Revenue / Active User Count."},
            {"step_title": "Annualized Account Contract Value (ACV)", "step_text": "Annual ARPU = Monthly ARPU × 12. Reflected in Annual Contract Value (ACV)."},
            {"step_title": "Pricing Power Indicator", "step_text": "A rising ARPU over time indicates successful pricing expansion, seat tier expansion, and premium add-on adoption."}
        ],
        "faqs": [
            {"q": "What is the difference between ARPU and ARPA?", "a": "ARPU measures revenue per individual user (seat), while ARPA measures revenue per account/company. In B2B SaaS with multi-seat teams, ARPA = ARPU × Average Seats per Company."},
            {"q": "How can a company increase ARPU without losing customers?", "a": "Usage-based pricing meters (API calls, storage, contacts), value-added feature gating, and packaging premium support tiers effectively drive organic ARPU expansion."}
        ],
        "js_logic": """
          const rev = getNum('total_revenue');
          const users = getNum('active_users') || 1;

          const arpuMo = rev / users;
          const arpuYr = arpuMo * 12;
          const arpuDay = arpuMo / 30;

          let tier = 'SMB (< $1k ACV)';
          if (arpuYr >= 25000) tier = 'Enterprise (≥ $25k ACV)';
          else if (arpuYr >= 5000) tier = 'Mid-Market ($5k - $25k ACV)';
          else if (arpuYr >= 1000) tier = 'Mid-Market ($1k - $5k ACV)';

          setDisp('monthly_arpu', '$' + arpuMo.toFixed(2) + ' / mo');
          setDisp('annual_arpu', '$' + arpuYr.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('daily_arpu', '$' + arpuDay.toFixed(2) + ' / day');
          setDisp('segment_tier', tier);
        """
    },
    {
        "slug": "viral-coefficient",
        "category": "finance",
        "name": "Viral Coefficient (K-Factor) & Growth Calculator",
        "description": "Calculate K-factor viral expansion, viral cycle time, customer compounding multiplier, and organic user generation.",
        "hero_badge": "Growth Loops • K-Factor Matrix",
        "formula_display": "K = Number of Invites per User × Referral Conversion Rate %",
        "fields": [
            {"id": "invites_sent", "label": "Invites Sent per Customer", "default": 4.5, "suffix": "invites", "min": 0.1, "max": 50, "step": 0.1, "hint": "Average referral invitations sent by each user"},
            {"id": "conversion_rate_pct", "label": "Invite Acceptance / Conversion Rate", "default": 25, "suffix": "%", "min": 1, "max": 100, "step": 1, "hint": "Percentage of invited users who register"},
            {"id": "initial_cohort", "label": "Initial Cohort Size", "default": 1000, "min": 10, "max": 1000000, "step": 50, "hint": "Starting seed user population"}
        ],
        "metrics": [
            {"id": "k_factor_score", "label": "Viral Coefficient (K-Factor)", "default_display": "1.13", "highlight": True},
            {"id": "virality_status", "label": "Virality Classification", "default_display": "True Exponential Virality (K > 1.0)", "highlight": True},
            {"id": "viral_multiplier", "label": "Total Growth Multiplier", "default_display": "Infinite (Self-Sustaining Exponential)"},
            {"id": "cycle1_growth", "label": "Cycle 1 New Viral Users", "default_display": "1,125 users"}
        ],
        "proof_steps": [
            {"step_title": "K-Factor Formulation", "step_text": "Viral Coefficient K = i · c, where i is number of invites sent per user, and c is the conversion rate percentage."},
            {"step_title": "Geometric Series Infinite Horizon", "step_text": "Total users over infinite viral cycles: N_total = N_0 · [1 + K + K² + K³ + ...]. If K < 1, the series converges to N_total = N_0 / (1 - K)."},
            {"step_title": "Viral Threshold (K > 1.0)", "step_text": "When K > 1.0, the geometric series diverges to infinity, achieving self-sustaining viral growth without paid marketing spend."}
        ],
        "faqs": [
            {"q": "What happens if K-factor is less than 1.0?", "a": "Even if K is 0.5 or 0.7, your product still benefits from strong viral amplification! A K-factor of 0.5 acts as a 2× multiplier on all paid advertising, cutting your effective CAC in half."},
            {"q": "What products have achieved K > 1.0?", "a": "Historic examples of products achieving true K > 1.0 include Hotmail (with its signature line invite), PayPal (referral bonus cash), Zoom, and TikTok."}
        ],
        "js_logic": """
          const invites = getNum('invites_sent');
          const conv = (getNum('conversion_rate_pct') || 25) / 100;
          const n0 = getNum('initial_cohort');

          const k = invites * conv;
          const cycle1 = Math.round(n0 * k);

          let status = 'Viral Sub-Critical (K < 1.0)';
          let mult = (1 / (1 - k)).toFixed(2) + 'x Paid Multiplier';
          if (k >= 1.0) {
            status = 'True Exponential Virality (K > 1.0)';
            mult = 'Infinite (Self-Sustaining Exponential)';
          }

          setDisp('k_factor_score', k.toFixed(2));
          setDisp('virality_status', status);
          setDisp('viral_multiplier', mult);
          setDisp('cycle1_growth', cycle1.toLocaleString() + ' users');
        """
    },
    {
        "slug": "employee-turnover-cost",
        "category": "finance",
        "name": "Employee Turnover & Replacement Cost Calculator",
        "description": "Calculate true financial and organizational cost of employee turnover, recruiting fees, onboarding lag, and lost institutional productivity.",
        "hero_badge": "HR Economics • Turnover Cost Matrix",
        "formula_display": "Turnover Cost = (Recruiting + Onboarding + Lost Productivity) × Departing Headcount",
        "fields": [
            {"id": "annual_salary", "label": "Average Annual Employee Salary", "default": 85000, "prefix": "$", "min": 20000, "max": 500000, "step": 5000, "hint": "Base salary of the departing role"},
            {"id": "turnover_count", "label": "Employees Leaving per Year", "default": 6, "min": 1, "max": 1000, "step": 1, "hint": "Annual voluntary and involuntary departures"},
            {"id": "role_complexity", "label": "Role Seniority Tier (0.5 Entry, 1.0 Mid, 1.5 Senior/Exec)", "default": 1.0, "min": 0.3, "max": 2.5, "step": 0.1, "hint": "Senior roles cost 1.5x to 2x salary to replace"}
        ],
        "metrics": [
            {"id": "total_annual_cost", "label": "Total Annual Turnover Cost", "default_display": "$510,000.00 / yr", "highlight": True},
            {"id": "cost_per_departure", "label": "Cost per Single Departure", "default_display": "$85,000.00", "highlight": True},
            {"id": "recruiting_cost", "label": "Direct Recruiting & Agency Fees", "default_display": "$17,000.00 / hire"},
            {"id": "ramp_lost_output", "label": "Productivity & Ramp Loss", "default_display": "$51,000.00 / hire"}
        ],
        "proof_steps": [
            {"step_title": "Direct Hard Recruiting Costs", "step_text": "Recruiting agency fees (15-25% of salary), job board advertising, and interview panel time: C_recruit ≈ 20% of salary."},
            {"step_title": "Onboarding and Productivity Ramp Lag", "step_text": "A new hire takes 3 to 6 months to reach full 100% productivity, operating at an average of 50% efficiency during onboarding: C_ramp ≈ 40-60% of salary."},
            {"step_title": "Seniority Multiplier Invariant", "step_text": "SHRM (Society for Human Resource Management) benchmarks indicate replacing mid-level employees costs 75% to 125% of annual salary; technical and executive roles cost 150% to 200%."}
        ],
        "faqs": [
            {"q": "Why is employee turnover so expensive?", "a": "Direct recruiting fees are only the tip of the iceberg. The hidden costs—departing employee knowledge loss, team overtime, interview disruption, and the 6-month ramp-up time of the replacement—account for over 70% of total turnover expense."},
            {"q": "What is considered a healthy corporate turnover rate?", "a": "Across all industries, a healthy annual employee turnover rate is approximately 10% (composed mostly of natural attrition and managing out low performers)."}
        ],
        "js_logic": """
          const sal = getNum('annual_salary');
          const count = getNum('turnover_count');
          const tier = getNum('role_complexity') || 1.0;

          const perDeparture = sal * tier;
          const totalCost = perDeparture * count;
          const recruitFee = sal * 0.20;
          const rampLoss = sal * 0.60 * tier;

          setDisp('total_annual_cost', '$' + Math.round(totalCost).toLocaleString() + ' / yr');
          setDisp('cost_per_departure', '$' + Math.round(perDeparture).toLocaleString());
          setDisp('recruiting_cost', '$' + Math.round(recruitFee).toLocaleString() + ' / hire');
          setDisp('ramp_lost_output', '$' + Math.round(rampLoss).toLocaleString() + ' / hire');
        """
    },
    {
        "slug": "roas",
        "category": "finance",
        "name": "Return on Ad Spend (ROAS) & Breakeven Calculator",
        "description": "Calculate ROAS, Breakeven ROAS from product profit margin, net advertising profit, and target ad budget scale.",
        "hero_badge": "Performance Marketing • ROAS Matrix",
        "formula_display": "ROAS = Ad Revenue Generated / Total Ad Spend | Breakeven ROAS = 1 / Profit Margin %",
        "fields": [
            {"id": "ad_spend", "label": "Total Advertising Spend", "default": 10000, "prefix": "$", "min": 100, "max": 10000000, "step": 250, "hint": "Paid Google, Meta, TikTok ad spend"},
            {"id": "revenue_generated", "label": "Attributed Revenue Generated", "default": 35000, "prefix": "$", "min": 100, "max": 50000000, "step": 500, "hint": "Total gross sales driven by ads"},
            {"id": "profit_margin_pct", "label": "Gross Product Profit Margin", "default": 40, "suffix": "%", "min": 5, "max": 95, "step": 1, "hint": "Margin before advertising expenses"}
        ],
        "metrics": [
            {"id": "current_roas", "label": "Achieved ROAS", "default_display": "3.50× (350%)", "highlight": True},
            {"id": "breakeven_roas", "label": "Mandatory Breakeven ROAS", "default_display": "2.50× (250%)", "highlight": True},
            {"id": "net_ad_profit", "label": "Net Profit After Ad Spend", "default_display": "$4,000.00", "highlight": True},
            {"id": "campaign_status", "label": "Campaign Profitability", "default_display": "Profitable (Surpassing Breakeven)"}
        ],
        "proof_steps": [
            {"step_title": "ROAS Yield Calculation", "step_text": "ROAS = Attributed Revenue / Ad Spend. For example, $35,000 / $10,000 = 3.50×."},
            {"step_title": "Breakeven ROAS Derivation", "step_text": "To not lose money, Gross Profit = Ad Spend. (Revenue × Margin%) = Ad Spend, implying Breakeven ROAS = Revenue / Ad Spend = 1 / Margin%."},
            {"step_title": "Net Economic Ad Profit", "step_text": "Net Profit = (Attributed Revenue × Margin%) - Ad Spend."}
        ],
        "faqs": [
            {"q": "What is the difference between ROAS and ROI?", "a": "ROAS measures gross revenue generated per ad dollar without deducting product manufacturing or operating costs. ROI measures net profit generated relative to total business costs."},
            {"q": "What is a good ROAS for eCommerce?", "a": "For a brand with 50% gross margins, Breakeven ROAS is 2.0×. A healthy target is 3.5× to 4.5× to cover overhead, shipping, and return rates."}
        ],
        "js_logic": """
          const spend = getNum('ad_spend') || 1;
          const rev = getNum('revenue_generated');
          const margin = (getNum('profit_margin_pct') || 40) / 100;

          const roas = rev / spend;
          const beRoas = margin > 0 ? (1 / margin) : 0;
          const grossProfit = rev * margin;
          const netProfit = grossProfit - spend;

          setDisp('current_roas', roas.toFixed(2) + '× (' + (roas * 100).toFixed(0) + '%)');
          setDisp('breakeven_roas', beRoas.toFixed(2) + '× (' + (beRoas * 100).toFixed(0) + '%)');
          setDisp('net_ad_profit', (netProfit >= 0 ? '$' : '-$') + Math.abs(netProfit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('campaign_status', roas >= beRoas ? 'Profitable (Surpassing Breakeven)' : 'Unprofitable (Below Breakeven)');
        """
    },
    {
        "slug": "cpa-cpc",
        "category": "finance",
        "name": "Cost Per Acquisition (CPA) from CPC Calculator",
        "description": "Calculate Cost Per Acquisition (CPA) from Cost Per Click (CPC) and Landing Page Conversion Rate (CVR).",
        "hero_badge": "Digital Advertising • CPA Unit Economics",
        "formula_display": "CPA = Cost Per Click (CPC) / Conversion Rate %",
        "fields": [
            {"id": "cpc_input", "label": "Average Cost Per Click (CPC)", "default": 2.75, "prefix": "$", "min": 0.05, "max": 100, "step": 0.05, "hint": "Average Google/Meta cost per click"},
            {"id": "conversion_rate_pct", "label": "Landing Page Conversion Rate", "default": 3.5, "suffix": "%", "min": 0.1, "max": 50, "step": 0.1, "hint": "Percentage of visitors who convert into leads/buyers"},
            {"id": "clicks_count", "label": "Traffic Volume (Clicks)", "default": 5000, "min": 50, "max": 1000000, "step": 250, "hint": "Total paid click volume"}
        ],
        "metrics": [
            {"id": "cpa_result", "label": "Cost Per Acquisition (CPA)", "default_display": "$78.57", "highlight": True},
            {"id": "total_conversions", "label": "Total Conversions Driven", "default_display": "175 conversions", "highlight": True},
            {"id": "total_campaign_cost", "label": "Total Campaign Ad Spend", "default_display": "$13,750.00"},
            {"id": "clicks_per_conversion", "label": "Clicks Needed per Conversion", "default_display": "29 clicks"}
        ],
        "proof_steps": [
            {"step_title": "Traffic Funnel Mathematical Coupling", "step_text": "Conversions = Clicks × Conversion Rate%. Total Ad Spend = Clicks × CPC."},
            {"step_title": "CPA Algebraic Derivation", "step_text": "CPA = Total Spend / Conversions = (Clicks × CPC) / (Clicks × CVR) = CPC / CVR."},
            {"step_title": "Optimization Leverage", "step_text": "Doubling conversion rate from 2% to 4% cuts your CPA in half without changing ad auction bids."}
        ],
        "faqs": [
            {"q": "How can I lower my CPA without lowering ad bids?", "a": "Improve landing page load speed, simplify form fields, add social proof and reviews, and ensure your ad copy perfectly aligns with your headline offer."},
            {"q": "What is an average landing page conversion rate?", "a": "Across all industries, average landing page conversion rates range between 2.5% and 5.0%. Top-quartile landing pages achieve 10% to 15%."}
        ],
        "js_logic": """
          const cpc = getNum('cpc_input');
          const cvr = (getNum('conversion_rate_pct') || 3.5) / 100;
          const clicks = getNum('clicks_count');

          const cpa = cvr > 0 ? (cpc / cvr) : 0;
          const convs = Math.round(clicks * cvr);
          const totalCost = clicks * cpc;
          const clicksPerConv = cvr > 0 ? (1 / cvr) : 0;

          setDisp('cpa_result', '$' + cpa.toFixed(2));
          setDisp('total_conversions', convs.toLocaleString() + ' conversions');
          setDisp('total_campaign_cost', '$' + totalCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('clicks_per_conversion', Math.round(clicksPerConv) + ' clicks');
        """
    },
    {
        "slug": "email-marketing-roi",
        "category": "finance",
        "name": "Email Marketing Campaign ROI Calculator",
        "description": "Calculate open rates, click-through rates (CTR), conversion yields, total campaign revenue, and net ROI percentage.",
        "hero_badge": "Direct Response • Email ROI Matrix",
        "formula_display": "ROI % = [(Campaign Revenue - Campaign Cost) / Campaign Cost] × 100",
        "fields": [
            {"id": "list_size", "label": "Email List Size (Recipients)", "default": 25000, "min": 100, "max": 5000000, "step": 500, "hint": "Total emails sent in blast"},
            {"id": "open_rate_pct", "label": "Open Rate (%)", "default": 24, "suffix": "%", "min": 1, "max": 90, "step": 0.5, "hint": "Average B2B/eCommerce open rate: 20-30%"},
            {"id": "ctr_pct", "label": "Click-Through Rate (CTR %)", "default": 3.2, "suffix": "%", "min": 0.1, "max": 30, "step": 0.1, "hint": "Percentage of total delivered emails clicked"},
            {"id": "conversion_pct", "label": "Purchase Conversion Rate", "default": 4.5, "suffix": "%", "min": 0.5, "max": 50, "step": 0.1, "hint": "Clicks converting into paid orders"},
            {"id": "aov_input", "label": "Average Order Value (AOV)", "default": 125, "prefix": "$", "min": 5, "max": 10000, "step": 5, "hint": "Average dollars spent per checkout"},
            {"id": "campaign_cost", "label": "Total Campaign Cost", "default": 750, "prefix": "$", "min": 10, "max": 50000, "step": 25, "hint": "Copywriter, ESP fees, design"}
        ],
        "metrics": [
            {"id": "total_campaign_revenue", "label": "Total Campaign Revenue", "default_display": "$4,500.00", "highlight": True},
            {"id": "campaign_roi_pct", "label": "Net Campaign ROI", "default_display": "500.00%", "highlight": True},
            {"id": "total_clicks", "label": "Total Click-Throughs", "default_display": "800 clicks"},
            {"id": "total_orders", "label": "Total Orders Generated", "default_display": "36 orders"}
        ],
        "proof_steps": [
            {"step_title": "Engagement Funnel Stages", "step_text": "Opens = List × Open%. Clicks = List × CTR%. Orders = Clicks × Conversion%."},
            {"step_title": "Total Attributed Revenue", "step_text": "Revenue = Orders × Average Order Value (AOV)."},
            {"step_title": "Return on Investment Formula", "step_text": "Net ROI% = [(Revenue - Cost) / Cost] × 100. Direct marketing studies consistently show email marketing delivers an average $36 to $42 return for every $1 invested."}
        ],
        "faqs": [
            {"q": "What is considered an average email marketing ROI?", "a": "According to the Data & Marketing Association (DMA), email marketing averages a 3,600% to 4,200% ROI ($36 to $42 return per $1 spent), outperforming social media and paid search."},
            {"q": "What is Click-to-Open Rate (CTOR)?", "a": "CTOR measures clicks divided by opens (rather than total delivered emails), isolating how compelling your email body copy and call-to-action were to people who actually opened the email."}
        ],
        "js_logic": """
          const list = getNum('list_size');
          const ctr = (getNum('ctr_pct') || 3.2) / 100;
          const cvr = (getNum('conversion_pct') || 4.5) / 100;
          const aov = getNum('aov_input');
          const cost = getNum('campaign_cost') || 1;

          const clicks = Math.round(list * ctr);
          const orders = Math.round(clicks * cvr);
          const rev = orders * aov;
          const roi = ((rev - cost) / cost) * 100;

          setDisp('total_campaign_revenue', '$' + rev.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('campaign_roi_pct', roi.toFixed(2) + '%');
          setDisp('total_clicks', clicks.toLocaleString() + ' clicks');
          setDisp('total_orders', orders.toLocaleString() + ' orders');
        """
    },
    {
        "slug": "sales-pipeline-velocity",
        "category": "finance",
        "name": "Sales Pipeline Velocity Calculator",
        "description": "Calculate sales pipeline velocity (revenue generated per day) and forecast monthly deal flow from win rate, deal size, and sales cycle length.",
        "hero_badge": "Enterprise Sales • Pipeline Velocity Matrix",
        "formula_display": "Pipeline Velocity = (Number of Deals × Win Rate % × Average Deal Size) / Sales Cycle (Days)",
        "fields": [
            {"id": "deal_count", "label": "Qualified Opportunities in Pipeline", "default": 60, "min": 1, "max": 5000, "step": 5, "hint": "Active sales opportunities currently in pipeline"},
            {"id": "win_rate_pct", "label": "Average Win Rate Percentage", "default": 25, "suffix": "%", "min": 1, "max": 90, "step": 1, "hint": "Percentage of qualified deals closed won"},
            {"id": "avg_deal_size", "label": "Average Deal Size (ACV)", "default": 18000, "prefix": "$", "min": 500, "max": 1000000, "step": 1000, "hint": "Average contract revenue per deal"},
            {"id": "sales_cycle_days", "label": "Sales Cycle Length (Days)", "default": 45, "suffix": "days", "min": 5, "max": 365, "step": 5, "hint": "Days from initial qualification to closed won"}
        ],
        "metrics": [
            {"id": "daily_velocity", "label": "Daily Pipeline Velocity", "default_display": "$6,000.00 / day", "highlight": True},
            {"id": "monthly_forecast", "label": "Monthly Revenue Generation", "default_display": "$180,000.00 / mo", "highlight": True},
            {"id": "total_pipeline_value", "label": "Total Active Pipeline Value", "default_display": "$1,080,000.00"},
            {"id": "expected_closed_deals", "label": "Expected Closed Won Deals", "default_display": "15 deals"}
        ],
        "proof_steps": [
            {"step_title": "Pipeline Velocity Equation", "step_text": "Velocity V = (Deals × Win Rate% × Average Deal Size) / Cycle Length (Days). Measures daily revenue momentum passing through the sales pipeline."},
            {"step_title": "Monthly Cash Flow Scaling", "step_text": "Monthly Run Rate = Velocity × 30 days."},
            {"step_title": "Four Levers of Sales Growth", "step_text": "Revenue velocity increases by improving any of the four variables: increasing deal volume, increasing average contract value, boosting close rates, or shortening sales cycle duration."}
        ],
        "faqs": [
            {"q": "How can an enterprise sales team accelerate pipeline velocity?", "a": "Shortening the sales cycle by 15% has the exact same revenue impact as increasing win rates by 15%. Clear buyer enablement materials, transparent pricing, and streamlined legal/security reviews accelerate deal velocity."},
            {"q": "What is considered a good B2B win rate?", "a": "For sales-qualified opportunities (SQOs), an average win rate is 20% to 25%. Top enterprise sales organizations achieve 30% to 40%."}
        ],
        "js_logic": """
          const deals = getNum('deal_count');
          const winRate = (getNum('win_rate_pct') || 25) / 100;
          const acv = getNum('avg_deal_size');
          const days = getNum('sales_cycle_days') || 1;

          const totalValue = deals * acv;
          const expectedDeals = Math.round(deals * winRate);
          const dailyVelocity = (deals * winRate * acv) / days;
          const monthlyForecast = dailyVelocity * 30;

          setDisp('daily_velocity', '$' + dailyVelocity.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / day');
          setDisp('monthly_forecast', '$' + monthlyForecast.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('total_pipeline_value', '$' + totalValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('expected_closed_deals', expectedDeals + ' deals');
        """
    },
    {
        "slug": "working-capital-ratio",
        "category": "finance",
        "name": "Working Capital & Current Ratio Calculator",
        "description": "Calculate Net Working Capital (NWC), Current Ratio, and short-term corporate liquidity solvency from current assets and liabilities.",
        "hero_badge": "Corporate Treasury • Liquidity Solvency Matrix",
        "formula_display": "Net Working Capital = Current Assets - Current Liabilities | Current Ratio = Current Assets / Current Liabilities",
        "fields": [
            {"id": "current_assets", "label": "Total Current Assets", "default": 450000, "prefix": "$", "min": 1000, "max": 100000000, "step": 5000, "hint": "Cash, marketable securities, accounts receivable, and inventory"},
            {"id": "current_liabilities", "label": "Total Current Liabilities", "default": 225000, "prefix": "$", "min": 1000, "max": 100000000, "step": 5000, "hint": "Accounts payable, short-term debt, and accrued payroll due within 1 yr"}
        ],
        "metrics": [
            {"id": "current_ratio_score", "label": "Current Ratio", "default_display": "2.00 : 1.0", "highlight": True},
            {"id": "net_working_capital", "label": "Net Working Capital (NWC)", "default_display": "$225,000.00", "highlight": True},
            {"id": "liquidity_health", "label": "Liquidity Solvency Status", "default_display": "Healthy Liquidity (1.5 - 3.0)"},
            {"id": "cushion_percentage", "label": "Asset Cushion Factor", "default_display": "200.0% of obligations"}
        ],
        "proof_steps": [
            {"step_title": "Net Working Capital Metric", "step_text": "NWC = Current Assets - Current Liabilities. Positive NWC indicates that a firm can satisfy all short-term obligations due within 12 months with liquid assets."},
            {"step_title": "Current Ratio Relative Liquidity", "step_text": "Current Ratio = Current Assets / Current Liabilities. A ratio of 2.0:1.0 indicates $2.00 of liquid resources for every $1.00 of current debt."},
            {"step_title": "Credit Rating Heuristic", "step_text": "< 1.0 = Danger of technical insolvency; 1.5–2.5 = Optimal liquidity balance; > 3.0 = Excess idle cash not deployed for productive yield."}
        ],
        "faqs": [
            {"q": "What is a healthy current ratio?", "a": "A healthy current ratio is typically between 1.5 and 2.5. A ratio below 1.0 indicates that a business may face difficulties meeting immediate vendor and debt obligations."},
            {"q": "What is the difference between Current Ratio and Quick Ratio?", "a": "The current ratio includes all current assets (including physical inventory and prepaid expenses). The quick ratio (acid-test) excludes inventory because goods cannot always be liquidated immediately without heavy discounts."}
        ],
        "js_logic": """
          const assets = getNum('current_assets');
          const liab = getNum('current_liabilities') || 1;

          const nwc = assets - liab;
          const cr = assets / liab;

          let status = 'Healthy Liquidity (1.5 - 2.5)';
          if (cr < 1.0) status = 'Insolvency Risk (< 1.0)';
          else if (cr < 1.5) status = 'Tight Working Capital (1.0 - 1.5)';
          else if (cr > 3.0) status = 'Excess Cash Cushion (> 3.0)';

          setDisp('current_ratio_score', cr.toFixed(2) + ' : 1.0');
          setDisp('net_working_capital', (nwc >= 0 ? '$' : '-$') + Math.abs(nwc).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('liquidity_health', status);
          setDisp('cushion_percentage', (cr * 100).toFixed(1) + '% of obligations');
        """
    },
    {
        "slug": "quick-ratio",
        "category": "finance",
        "name": "Quick Ratio (Acid-Test) Calculator",
        "description": "Calculate the Acid-Test Quick Ratio isolating liquid cash, marketable securities, and accounts receivable against current liabilities.",
        "hero_badge": "Balance Sheet Analysis • Acid-Test Matrix",
        "formula_display": "Quick Ratio = (Cash + Marketable Securities + Accounts Receivable) / Current Liabilities",
        "fields": [
            {"id": "cash_equivalents", "label": "Cash & Cash Equivalents", "default": 180000, "prefix": "$", "min": 0, "max": 100000000, "step": 5000, "hint": "Liquid bank balances and money market funds"},
            {"id": "marketable_securities", "label": "Marketable Securities", "default": 45000, "prefix": "$", "min": 0, "max": 100000000, "step": 5000, "hint": "Treasuries and liquid stock holdings"},
            {"id": "accounts_receivable", "label": "Accounts Receivable (A/R)", "default": 95000, "prefix": "$", "min": 0, "max": 100000000, "step": 5000, "hint": "Money owed by customers on invoices"},
            {"id": "current_liabilities", "label": "Total Current Liabilities", "default": 220000, "prefix": "$", "min": 1000, "max": 100000000, "step": 5000, "hint": "Short-term debt, payables, and accrued obligations"}
        ],
        "metrics": [
            {"id": "quick_ratio_score", "label": "Acid-Test Quick Ratio", "default_display": "1.45 : 1.0", "highlight": True},
            {"id": "quick_assets_total", "label": "Total Quick Assets", "default_display": "$320,000.00"},
            {"id": "solvency_tier", "label": "Short-Term Solvency Tier", "default_display": "Strong Liquidity (Quick Ratio ≥ 1.0)", "highlight": True},
            {"id": "cash_ratio_score", "label": "Pure Cash Ratio (Cash / Liabilities)", "default_display": "0.82"}
        ],
        "proof_steps": [
            {"step_title": "Acid-Test Asset Isolation", "step_text": "Quick Assets = Cash + Marketable Securities + Net Receivables. Excludes physical inventory and prepaid insurance."},
            {"step_title": "Quick Ratio Derivation", "step_text": "Quick Ratio = Quick Assets / Current Liabilities."},
            {"step_title": "Solvency Invariant", "step_text": "A Quick Ratio ≥ 1.0 proves that the firm possesses sufficient instant liquidity to pay off 100% of current debt immediately without needing to sell a single unit of inventory."}
        ],
        "faqs": [
            {"q": "Why is the Quick Ratio called the 'Acid-Test'?", "a": "The name originates from early gold prospectors who applied nitric acid to metal samples: real gold was impervious, while base metals dissolved. In finance, the quick ratio tests whether a business survives an immediate financial crisis."},
            {"q": "What is an acceptable Quick Ratio?", "a": "A Quick Ratio of 1.0 or higher is considered healthy for most commercial enterprises. In software and services with minimal inventory, quick ratios often match current ratios."}
        ],
        "js_logic": """
          const cash = getNum('cash_equivalents');
          const sec = getNum('marketable_securities');
          const ar = getNum('accounts_receivable');
          const liab = getNum('current_liabilities') || 1;

          const quickAssets = cash + sec + ar;
          const qr = quickAssets / liab;
          const cr = cash / liab;

          setDisp('quick_ratio_score', qr.toFixed(2) + ' : 1.0');
          setDisp('quick_assets_total', '$' + quickAssets.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('solvency_tier', qr >= 1.0 ? 'Strong Liquidity (Quick Ratio ≥ 1.0)' : 'Liquidity Pressure (Quick Ratio < 1.0)');
          setDisp('cash_ratio_score', cr.toFixed(2));
        """
    },
    {
        "slug": "debt-service-coverage",
        "category": "finance",
        "name": "Corporate DSCR & Interest Coverage Calculator",
        "description": "Calculate Debt Service Coverage Ratio (DSCR) and Times Interest Earned (TIE) from Net Operating Income (NOI) / EBITDA and debt service obligations.",
        "hero_badge": "Credit Underwriting • Commercial Debt Coverage",
        "formula_display": "DSCR = Net Operating Income (NOI) / Total Debt Service (Principal + Interest)",
        "fields": [
            {"id": "ebitda_noi", "label": "Net Operating Income (NOI) / EBITDA", "default": 240000, "prefix": "$", "min": 10000, "max": 50000000, "step": 5000, "hint": "Annual cash flow available for debt service"},
            {"id": "annual_principal", "label": "Annual Principal Repayments", "default": 85000, "prefix": "$", "min": 0, "max": 20000000, "step": 2500, "hint": "Mandatory loan principal amortization"},
            {"id": "annual_interest", "label": "Annual Interest Expense", "default": 65000, "prefix": "$", "min": 1000, "max": 20000000, "step": 2500, "hint": "Interest payments on all outstanding loans"}
        ],
        "metrics": [
            {"id": "dscr_score", "label": "Debt Service Coverage Ratio (DSCR)", "default_display": "1.60× Coverage", "highlight": True},
            {"id": "interest_coverage_tie", "label": "Interest Coverage (TIE)", "default_display": "3.69× Interest", "highlight": True},
            {"id": "total_debt_service", "label": "Total Annual Debt Service", "default_display": "$150,000.00 / yr"},
            {"id": "underwriting_status", "label": "Commercial Bank Underwriting", "default_display": "Approved (Exceeds 1.25x minimum covenant)"}
        ],
        "proof_steps": [
            {"step_title": "Total Debt Service Obligations", "step_text": "Total Debt Service = Principal Payments + Interest Expense."},
            {"step_title": "DSCR Underwriting Formulation", "step_text": "DSCR = NOI / Total Debt Service. Measures operational cash buffer over mandatory lender debt service."},
            {"step_title": "Times Interest Earned (TIE)", "step_text": "TIE = EBITDA / Interest Expense. Assesses ability to service interest burdens independent of principal amortization schedules."}
        ],
        "faqs": [
            {"q": "What is the minimum DSCR required by commercial banks?", "a": "Most commercial banks and SBA lenders require a minimum DSCR of 1.20× to 1.25×. A 1.25× DSCR means the company generates $1.25 in operating cash flow for every $1.00 of required debt payment."},
            {"q": "What happens if a loan breaches a DSCR covenant?", "a": "Breaching a loan agreement's DSCR covenant is a technical default. Lenders may increase interest rates, freeze revolving credit lines, require additional collateral, or accelerate debt repayment."}
        ],
        "js_logic": """
          const noi = getNum('ebitda_noi');
          const prin = getNum('annual_principal');
          const intExp = getNum('annual_interest');

          const debtService = prin + intExp;
          const dscr = debtService > 0 ? (noi / debtService) : 0;
          const tie = intExp > 0 ? (noi / intExp) : 0;

          let status = 'Approved (Exceeds 1.25x minimum covenant)';
          if (dscr < 1.0) status = 'Default Territory (Cash flow insufficient to cover debt)';
          else if (dscr < 1.25) status = 'High Risk (Below standard 1.25x lender threshold)';

          setDisp('dscr_score', dscr.toFixed(2) + '× Coverage');
          setDisp('interest_coverage_tie', tie.toFixed(2) + '× Interest');
          setDisp('total_debt_service', '$' + debtService.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('underwriting_status', status);
        """
    },
    {
        "slug": "economic-order-quantity",
        "category": "finance",
        "name": "Economic Order Quantity (EOQ) & Reorder Point Calculator",
        "description": "Calculate optimal inventory order batch size (EOQ), annual carrying costs, ordering costs, and safety stock reorder point.",
        "hero_badge": "Supply Chain & Operations • Ford-Harris EOQ Model",
        "formula_display": "EOQ = √[(2 · Demand · Order Cost) / Holding Cost per Unit]",
        "fields": [
            {"id": "annual_demand", "label": "Annual Unit Demand (D)", "default": 12000, "suffix": "units/yr", "min": 100, "max": 10000000, "step": 500, "hint": "Total units sold or consumed per year"},
            {"id": "ordering_cost", "label": "Fixed Cost per Order (S)", "default": 75, "prefix": "$", "min": 5, "max": 5000, "step": 5, "hint": "Setup, freight, and purchase order administration"},
            {"id": "holding_cost", "label": "Annual Holding Cost per Unit (H)", "default": 2.50, "prefix": "$", "min": 0.10, "max": 500, "step": 0.25, "hint": "Warehousing, insurance, and inventory capital cost"},
            {"id": "lead_time_days", "label": "Supplier Lead Time (Days)", "default": 14, "suffix": "days", "min": 1, "max": 180, "step": 1, "hint": "Days from purchase order to delivery"}
        ],
        "metrics": [
            {"id": "eoq_units", "label": "Optimal Order Quantity (EOQ)", "default_display": "849 units", "highlight": True},
            {"id": "reorder_point", "label": "Reorder Trigger Point (ROP)", "default_display": "460 units", "highlight": True},
            {"id": "orders_per_year", "label": "Optimal Orders per Year", "default_display": "14.1 orders / yr"},
            {"id": "total_inventory_cost", "label": "Total Minimum Annual Inventory Cost", "default_display": "$2,121.32 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Ford-Harris Cost Trade-Off Balance", "step_text": "Annual Ordering Cost = (D / Q) · S. Annual Carrying/Holding Cost = (Q / 2) · H. Total Cost C(Q) = (D/Q)S + (Q/2)H."},
            {"step_title": "Calculus First-Derivative Optimization", "step_text": "Setting dC/dQ = -DS/Q² + H/2 = 0 yields the iconic Wilson-Harris formula: EOQ = √[(2 · D · S) / H]."},
            {"step_title": "Reorder Point Formulation", "step_text": "Reorder Point ROP = (Daily Demand × Lead Time Days) = [(Annual Demand / 365) × Lead Time Days]."}
        ],
        "faqs": [
            {"q": "What happens if you order more units than the EOQ?", "a": "Ordering above the EOQ reduces ordering frequency and administrative costs, but increases warehouse carrying costs, insurance, and the risk of obsolescence."},
            {"q": "Does EOQ account for supplier bulk quantity discounts?", "a": "Classic EOQ assumes constant purchase price. When suppliers offer tier discounts (e.g. 5% off at 2,000 units), you compare total costs at each price break tier against the EOQ."}
        ],
        "js_logic": """
          const D = getNum('annual_demand');
          const S = getNum('ordering_cost');
          const H = getNum('holding_cost') || 1;
          const lead = getNum('lead_time_days');

          const eoq = Math.sqrt((2 * D * S) / H);
          const ordersYr = D / eoq;
          const totalCost = (D / eoq) * S + (eoq / 2) * H;
          const rop = Math.ceil((D / 365) * lead);

          setDisp('eoq_units', Math.round(eoq) + ' units');
          setDisp('reorder_point', rop.toLocaleString() + ' units');
          setDisp('orders_per_year', ordersYr.toFixed(1) + ' orders / yr');
          setDisp('total_inventory_cost', '$' + totalCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    },
    {
        "slug": "burn-multiple",
        "category": "finance",
        "name": "Bessemer Burn Multiple Calculator",
        "description": "Calculate the Bessemer Venture Partners Burn Multiple measuring net cash burned for each dollar of Net New ARR generated.",
        "hero_badge": "Venture Efficiency • Bessemer Burn Multiple",
        "formula_display": "Burn Multiple = Net Burn / Net New ARR",
        "fields": [
            {"id": "net_burn_amount", "label": "Annual / Period Net Cash Burn", "default": 2400000, "prefix": "$", "min": 10000, "max": 100000000, "step": 50000, "hint": "Total cash burned in measurement period"},
            {"id": "net_new_arr_added", "label": "Net New ARR Generated", "default": 2000000, "prefix": "$", "min": 10000, "max": 100000000, "step": 50000, "hint": "Net ARR added in same measurement period"}
        ],
        "metrics": [
            {"id": "burn_multiple_score", "label": "Burn Multiple", "default_display": "1.20×", "highlight": True},
            {"id": "capital_efficiency_tier", "label": "Bessemer Capital Efficiency Tier", "default_display": "Good (1.0x - 1.5x)", "highlight": True},
            {"id": "cost_per_arr_dollar", "label": "Cash Burned per $1.00 ARR Added", "default_display": "$1.20"},
            {"id": "growth_verdict", "label": "Investor Perspective", "default_display": "Fundable Series A/B Growth Profile"}
        ],
        "proof_steps": [
            {"step_title": "Bessemer Unit Capital Burn Metric", "step_text": "Burn Multiple = Net Burn / Net New ARR. Unlike CAC, which only measures sales and marketing, the Burn Multiple includes all corporate expenses (R&D, G&A, management, cloud infrastructure)."},
            {"step_title": "Venture Capital Benchmark Thresholds", "step_text": "< 1.0× = Amazing (Best-in-class); 1.0×–1.5× = Good; 1.5×–2.0× = Suspect (Needs optimization); > 2.0× = Bad (Burning too much cash for slow growth)."},
            {"step_title": "Macro Cycle Significance", "step_text": "In zero-interest-rate environments, investors tolerated 2.5×+ multiples. In modern disciplined capital markets, sub-1.5× multiples are required for premium venture valuations."}
        ],
        "faqs": [
            {"q": "What is the Burn Multiple formula?", "a": "Burn Multiple = Net Burn / Net New ARR. For example, if a startup burns $3 million to generate $2 million in new ARR, its Burn Multiple is 1.5×."},
            {"q": "How does the Burn Multiple differ from CAC Payback?", "a": "CAC payback only tracks sales and marketing spend. The Burn Multiple is comprehensive—capturing engineering salaries, rent, legal fees, server costs, and churn drag."}
        ],
        "js_logic": """
          const burn = getNum('net_burn_amount');
          const arr = getNum('net_new_arr_added') || 1;

          const bm = burn / arr;

          let tier = 'Good (1.0x - 1.5x)';
          let verdict = 'Fundable Series A/B Growth Profile';
          if (bm < 1.0) {
            tier = 'Amazing (< 1.0x)';
            verdict = 'Top-tier Venture Quality (Highly capital efficient)';
          } else if (bm <= 1.5) {
            tier = 'Good (1.0x - 1.5x)';
            verdict = 'Fundable Series A/B Growth Profile';
          } else if (bm <= 2.0) {
            tier = 'Suspect (1.5x - 2.0x)';
            verdict = 'Scrutiny on burn efficiency and CAC payback';
          } else {
            tier = 'Alarming (> 2.0x)';
            verdict = 'Excessive cash burn; pause hiring and trim OpEx';
          }

          setDisp('burn_multiple_score', bm.toFixed(2) + '×');
          setDisp('capital_efficiency_tier', tier);
          setDisp('cost_per_arr_dollar', '$' + bm.toFixed(2));
          setDisp('growth_verdict', verdict);
        """
    },
    {
        "slug": "freemium-conversion",
        "category": "finance",
        "name": "Freemium to Paid Conversion Calculator",
        "description": "Calculate freemium user conversion rates, free-to-paid funnel velocity, monthly recurring revenue from free tier, and cohort monetization.",
        "hero_badge": "Product-Led Growth • PLG Funnel Matrix",
        "formula_display": "Conversion Rate % = (New Paid Upgrades / Active Free Users) × 100",
        "fields": [
            {"id": "free_tier_users", "label": "Active Free Tier Users", "default": 50000, "min": 100, "max": 10000000, "step": 1000, "hint": "Monthly active free tier accounts"},
            {"id": "free_to_paid_pct", "label": "Free-to-Paid Conversion Rate", "default": 3.5, "suffix": "%", "min": 0.1, "max": 25, "step": 0.1, "hint": "Industry benchmark: 2% to 5%"},
            {"id": "paid_plan_price", "label": "Average Paid Subscription Price", "default": 29, "prefix": "$", "min": 1, "max": 1000, "step": 1, "hint": "Monthly price per upgraded account"}
        ],
        "metrics": [
            {"id": "paying_conversions", "label": "New Paying Customers", "default_display": "1,750 subscribers", "highlight": True},
            {"id": "mrr_generated", "label": "Monthly Recurring Revenue Added", "default_display": "$50,750.00 / mo", "highlight": True},
            {"id": "arr_potential", "label": "Annualized Recurring Run Rate", "default_display": "$609,000.00 / yr"},
            {"id": "monetization_yield", "label": "Revenue per Free Tier User", "default_display": "$1.02 / free user"}
        ],
        "proof_steps": [
            {"step_title": "Product-Led Funnel Transition", "step_text": "Upgraded Accounts N_paid = N_free × (Conversion Rate% / 100)."},
            {"step_title": "Recurring Revenue Creation", "step_text": "MRR = N_paid × Monthly Price. ARR = MRR × 12."},
            {"step_title": "Blended Free User Monetization Yield", "step_text": "Yield per Free User = MRR / N_free = Conversion Rate% × Price. Useful for setting maximum allowable free tier server hosting costs."}
        ],
        "faqs": [
            {"q": "What is an average freemium conversion rate for SaaS?", "a": "Standard freemium conversion rates range between 2% and 5%. Companies with strict usage gating (e.g. Dropbox, Slack) achieve 4% to 8%, while lightweight freemium apps often see 1% to 2%."},
            {"q": "How can a SaaS improve free-to-paid conversions?", "a": "Introduce clear usage paywalls (seat limits, feature locks, export watermarks), time-limited pro trials, and in-app onboarding triggers when users hit high-intent milestones."}
        ],
        "js_logic": """
          const freeUsers = getNum('free_tier_users');
          const convRate = (getNum('free_to_paid_pct') || 3.5) / 100;
          const price = getNum('paid_plan_price');

          const paidCust = Math.round(freeUsers * convRate);
          const mrr = paidCust * price;
          const arr = mrr * 12;
          const yieldPerUser = freeUsers > 0 ? (mrr / freeUsers) : 0;

          setDisp('paying_conversions', paidCust.toLocaleString() + ' subscribers');
          setDisp('mrr_generated', '$' + mrr.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('arr_potential', '$' + arr.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('monetization_yield', '$' + yieldPerUser.toFixed(2) + ' / free user');
        """
    },
    {
        "slug": "gross-revenue-retention",
        "category": "finance",
        "name": "Gross Revenue Retention (GRR) vs NRR Calculator",
        "description": "Calculate Gross Revenue Retention (GRR), isolating core churn and contraction without obscuring losses behind expansion revenue.",
        "hero_badge": "Retention Analytics • GRR Foundation Matrix",
        "formula_display": "GRR % = [(Beginning MRR - Churn - Contraction) / Beginning MRR] × 100",
        "fields": [
            {"id": "beg_mrr", "label": "Beginning of Period MRR", "default": 200000, "prefix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Base recurring revenue at start of year/month"},
            {"id": "churn_lost", "label": "Canceled / Churned MRR", "default": 12000, "prefix": "$", "min": 0, "max": 5000000, "step": 500, "hint": "Revenue lost from total cancellations"},
            {"id": "contract_lost", "label": "Contraction / Downgrade MRR", "default": 6000, "prefix": "$", "min": 0, "max": 2000000, "step": 500, "hint": "Revenue lost from plan downgrades"}
        ],
        "metrics": [
            {"id": "grr_percentage", "label": "Gross Revenue Retention (GRR)", "default_display": "91.00%", "highlight": True},
            {"id": "gross_churn_pct", "label": "Total Gross Revenue Churn", "default_display": "9.00%", "highlight": True},
            {"id": "retained_base_mrr", "label": "Retained Cohort Base Revenue", "default_display": "$182,000.00 / mo"},
            {"id": "pe_benchmark_status", "label": "Private Equity Benchmark", "default_display": "Top Quartile (> 90% GRR)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Revenue Preservation Principle", "step_text": "GRR = [(Starting MRR - Churn - Contraction) / Starting MRR] × 100%. Expansion MRR is strictly omitted from the numerator."},
            {"step_title": "GRR Upper Bound Ceiling", "step_text": "By mathematical definition, GRR can never exceed 100.0%. A GRR of 90%+ indicates that customers stick with the platform even without factoring in upgrades."},
            {"step_title": "The Leaky Bucket Test", "step_text": "A business with 120% NRR but 75% GRR has a severe underlying product defect that is masked only by aggressive upselling to a small fraction of customers."}
        ],
        "faqs": [
            {"q": "What is the difference between GRR and NRR?", "a": "GRR measures the percentage of recurring revenue retained from existing customers excluding all expansion and upsells. NRR includes expansion. GRR can never exceed 100%, whereas NRR can."},
            {"q": "What is a good GRR benchmark for enterprise software?", "a": "For enterprise B2B SaaS, top-quartile GRR is 90% to 95%. For mid-market SaaS, 85% to 90% is solid. For SMB SaaS, 75% to 85% is typical."}
        ],
        "js_logic": """
          const start = getNum('beg_mrr') || 1;
          const churn = getNum('churn_lost');
          const contract = getNum('contract_lost');

          const loss = churn + contract;
          const retained = Math.max(0, start - loss);
          const grr = (retained / start) * 100;
          const grossChurn = 100 - grr;

          let status = 'Top Quartile (> 90% GRR)';
          if (grr < 75) status = 'Severe Churn Risk (< 75% GRR)';
          else if (grr < 85) status = 'Average SMB Retention (75% - 85%)';
          else if (grr < 90) status = 'Good Mid-Market Retention (85% - 90%)';

          setDisp('grr_percentage', grr.toFixed(2) + '%');
          setDisp('gross_churn_pct', grossChurn.toFixed(2) + '%');
          setDisp('retained_base_mrr', '$' + retained.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('pe_benchmark_status', status);
        """
    },
    {
        "slug": "cac-payback",
        "category": "finance",
        "name": "SaaS CAC Payback Period Calculator",
        "description": "Calculate exact customer acquisition cost payback period in months accounting for gross margin and customer revenue churn drag.",
        "hero_badge": "Unit Economics • Payback Horizon Matrix",
        "formula_display": "Payback Period (Months) = CAC / (Monthly ARPA × Gross Margin %)",
        "fields": [
            {"id": "cac_dollar", "label": "Fully Loaded CAC per Account", "default": 2400, "prefix": "$", "min": 50, "max": 200000, "step": 100, "hint": "All sales, SDR, and marketing expenses per acquired account"},
            {"id": "arpa_dollar", "label": "Average Monthly Revenue (ARPA)", "default": 250, "prefix": "$", "min": 10, "max": 50000, "step": 10, "hint": "Monthly recurring billing amount"},
            {"id": "margin_pct_val", "label": "Gross Margin Percentage", "default": 80, "suffix": "%", "min": 20, "max": 95, "step": 1, "hint": "Cost of goods sold (hosting, support, payment fees)"}
        ],
        "metrics": [
            {"id": "exact_payback_months", "label": "CAC Payback Horizon", "default_display": "12.0 months", "highlight": True},
            {"id": "monthly_gp_contribution", "label": "Monthly Gross Profit per Account", "default_display": "$200.00 / mo", "highlight": True},
            {"id": "capital_recycle_speed", "label": "Capital Recycling Velocity", "default_display": "1.00 Cycles / Year"},
            {"id": "underwriting_rating", "label": "Venture Benchmark Score", "default_display": "Target Benchmark (12 Months)"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Margin Contribution", "step_text": "Net Margin Contribution per Account = ARPA × (Gross Margin% / 100). For example: $250 × 80% = $200 gross margin per month."},
            {"step_title": "Direct Payback Horizon Equation", "step_text": "Payback Months = CAC / Net Monthly Margin. With $2,400 CAC and $200 monthly margin: 2,400 / 200 = 12.0 months."},
            {"step_title": "Capital Velocity Implication", "step_text": "A 12-month payback allows a company to recycle the same dollar of acquisition capital annually to fund compounding growth."}
        ],
        "faqs": [
            {"q": "Why is CAC payback preferred over LTV:CAC by CFOs?", "a": "LTV relies on future churn predictions that may take 3 to 5 years to validate. CAC payback is immediate and cash-flow concrete: it tells you exactly when acquisition cash is back in your bank account."},
            {"q": "What is an ideal payback period for SMB vs Enterprise?", "a": "For SMB SaaS ($50-$500/mo), payback should be 6 to 12 months due to higher churn risk. For Enterprise ($25k-$100k+ ACV), 12 to 18 months is acceptable because enterprise churn is historically low."}
        ],
        "js_logic": """
          const cac = getNum('cac_dollar');
          const arpa = getNum('arpa_dollar');
          const margin = (getNum('margin_pct_val') || 80) / 100;

          const gp = arpa * margin;
          const payback = gp > 0 ? (cac / gp) : 0;
          const cycleSpeed = payback > 0 ? (12 / payback) : 0;

          let rating = 'Target Benchmark (12 Months)';
          if (payback < 8) rating = 'Elite Velocity (< 8 Months)';
          else if (payback <= 12) rating = 'Target Benchmark (8 - 12 Months)';
          else if (payback <= 18) rating = 'Acceptable for Mid-Market (12 - 18 Months)';
          else rating = 'Capital Drag (> 18 Months)';

          setDisp('exact_payback_months', payback.toFixed(1) + ' months');
          setDisp('monthly_gp_contribution', '$' + gp.toFixed(2) + ' / mo');
          setDisp('capital_recycle_speed', cycleSpeed.toFixed(2) + ' Cycles / Year');
          setDisp('underwriting_rating', rating);
        """
    },
    {
        "slug": "inventory-turnover",
        "category": "finance",
        "name": "Inventory Turnover & Days Sales of Inventory (DSI) Calculator",
        "description": "Calculate inventory turnover ratio, Days Sales of Inventory (DSI / DIO), and capital tied up in warehouse stock.",
        "hero_badge": "Working Capital • Inventory Velocity",
        "formula_display": "Inventory Turnover = Cost of Goods Sold (COGS) / Average Inventory | DSI = (Average Inventory / COGS) × 365",
        "fields": [
            {"id": "annual_cogs", "label": "Annual Cost of Goods Sold (COGS)", "default": 1800000, "prefix": "$", "min": 10000, "max": 100000000, "step": 25000, "hint": "Total annual cost of manufactured or purchased inventory sold"},
            {"id": "avg_inventory_val", "label": "Average Inventory Value", "default": 300000, "prefix": "$", "min": 1000, "max": 50000000, "step": 5000, "hint": "Average value of inventory held in warehouse"}
        ],
        "metrics": [
            {"id": "inventory_turns", "label": "Inventory Turnover Ratio", "default_display": "6.00 Turns / Year", "highlight": True},
            {"id": "dsi_days", "label": "Days Sales of Inventory (DSI)", "default_display": "60.8 days", "highlight": True},
            {"id": "capital_velocity", "label": "Inventory Liquidity Health", "default_display": "Efficient Turnover (5 - 8 Turns)"},
            {"id": "holding_capital_drag", "label": "Estimated Annual Holding Drag (20%)", "default_display": "$60,000.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Inventory Turnover Ratio", "step_text": "Inventory Turnover = COGS / Average Inventory. Measures how many times inventory is sold and replaced over the year."},
            {"step_title": "Days Sales of Inventory (DSI)", "step_text": "DSI (Days Inventory Outstanding - DIO) = (Average Inventory / COGS) × 365 = 365 / Inventory Turnover. Represents average days required to turn inventory into sales."},
            {"step_title": "Working Capital Free Cash Flow Drag", "step_text": "Each excess day of inventory ties up corporate cash. Inventory holding costs (storage, insurance, spoilage, financing) typically equal 20% to 25% of inventory value annually."}
        ],
        "faqs": [
            {"q": "What is a good inventory turnover ratio?", "a": "For retail and eCommerce, 4 to 8 turns per year is standard. Fast-moving consumer goods (groceries) target 12 to 20 turns, while luxury jewelry or heavy machinery may turn only 1 to 2 times per year."},
            {"q": "Why is COGS used instead of sales revenue in the formula?", "a": "Inventory is recorded on the balance sheet at cost. Comparing inventory cost to sales revenue (which includes markup) would falsely inflate the turnover ratio."}
        ],
        "js_logic": """
          const cogs = getNum('annual_cogs');
          const inv = getNum('avg_inventory_val') || 1;

          const turns = cogs / inv;
          const dsi = (inv / cogs) * 365;
          const holdingDrag = inv * 0.20;

          let health = 'Efficient Turnover (5 - 8 Turns)';
          if (turns < 3) health = 'Sluggish Inventory (High obsolescence risk)';
          else if (turns < 5) health = 'Moderate Velocity (3 - 5 Turns)';
          else if (turns > 10) health = 'Hyper-Velocity (Risk of stockouts)';

          setDisp('inventory_turns', turns.toFixed(2) + ' Turns / Year');
          setDisp('dsi_days', dsi.toFixed(1) + ' days');
          setDisp('capital_velocity', health);
          setDisp('holding_capital_drag', '$' + holdingDrag.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    }
]
