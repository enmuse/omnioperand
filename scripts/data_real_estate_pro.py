"""
scripts/data_real_estate_pro.py
25 High-Value Commercial Real Estate, Syndication, Private Equity & Property Investment Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

REAL_ESTATE_PRO_CALCULATORS = [
    {
        "slug": "internal-rate-of-return",
        "category": "finance",
        "name": "Commercial Real Estate IRR & Equity Multiple Calculator",
        "description": "Calculate commercial property Internal Rate of Return (IRR), Equity Multiple (EM), and multi-year cash flow yield including disposition sale proceeds.",
        "hero_badge": "Private Equity • Real Estate IRR Matrix",
        "formula_display": "NPV = ∑ [CF_t / (1 + IRR)^t] = 0 | Equity Multiple = Total Cash Distributions / Total Equity Invested",
        "fields": [
            {"id": "initial_equity_invested", "label": "Initial Equity Invested (Year 0)", "default": 500000, "prefix": "$", "min": 10000, "max": 100000000, "step": 25000, "hint": "Total out-of-pocket LP/GP equity down payment"},
            {"id": "annual_cash_flow_avg", "label": "Average Annual Operating Cash Flow", "default": 42000, "prefix": "$", "min": 0, "max": 20000000, "step": 5000, "hint": "Net operating cash distribution to equity"},
            {"id": "hold_period_years", "label": "Investment Hold Period (Years)", "default": 5, "suffix": "years", "min": 2, "max": 15, "step": 1, "hint": "Projected asset hold duration"},
            {"id": "net_sale_proceeds", "label": "Net Disposition Proceeds at Sale", "default": 820000, "prefix": "$", "min": 10000, "max": 200000000, "step": 50000, "hint": "Sale price minus loan payoff, closing fees"}
        ],
        "metrics": [
            {"id": "property_irr_result", "label": "Project Internal Rate of Return (IRR)", "default_display": "17.42% IRR", "highlight": True},
            {"id": "equity_multiple_em", "label": "Equity Multiple (EM)", "default_display": "2.06×", "highlight": True},
            {"id": "net_profit_dollar", "label": "Total Net Cash Profit", "default_display": "$530,000.00", "highlight": True},
            {"id": "annualized_cash_yield", "label": "Average Cash-on-Cash Yield", "default_display": "8.40% / yr"}
        ],
        "proof_steps": [
            {"step_title": "The Net Present Value Equilibrium", "step_text": "Internal Rate of Return (IRR) is the discount rate r that equates the present value of all future cash flows to the initial equity: 0 = -CF_0 + ∑ [CF_t / (1 + r)^t]."},
            {"step_title": "Equity Multiple Formulation", "step_text": "Equity Multiple = (Total Cash Distributions + Terminal Sale Proceeds) / Initial Equity Invested. For example: ($210,000 + $820,000) / $500,000 = 2.06×."},
            {"step_title": "Time-Value Sensitivity", "step_text": "A 2.0× Equity Multiple in 3 years generates ~26% IRR; that same 2.0× in 10 years yields only ~7.2% IRR. IRR penalizes capital that takes longer to return."}
        ],
        "faqs": [
            {"q": "What is considered a good IRR for commercial real estate syndications?", "a": "Private equity real estate sponsors typically target a 14% to 18% net LP IRR for value-add multifamily, and 18% to 22%+ for ground-up opportunistic developments over a 3 to 7-year hold period."},
            {"q": "Why is Equity Multiple needed alongside IRR?", "a": "IRR can be gamed through early refinances or short flips (e.g. 50% IRR on a 6-month flip might only generate a 1.25× multiple with small net dollar profit). Equity multiple measures how much total cash wealth was actually created."}
        ],
        "js_logic": """
          const c0 = getNum('initial_equity_invested');
          const cfAnnual = getNum('annual_cash_flow_avg');
          const years = getNum('hold_period_years') || 5;
          const exitProceeds = getNum('net_sale_proceeds');

          const totalDistributions = (cfAnnual * years) + exitProceeds;
          const em = c0 > 0 ? (totalDistributions / c0) : 0;
          const netProfit = totalDistributions - c0;
          const avgYield = c0 > 0 ? ((cfAnnual / c0) * 100) : 0;

          // Newton-Raphson approximation for IRR
          let r = 0.15;
          for (let iter = 0; iter < 40; iter++) {
            let npv = -c0;
            let dNpv = 0;
            for (let t = 1; t <= years; t++) {
              const flow = (t === years) ? (cfAnnual + exitProceeds) : cfAnnual;
              npv += flow / Math.pow(1 + r, t);
              dNpv -= (t * flow) / Math.pow(1 + r, t + 1);
            }
            if (Math.abs(dNpv) < 1e-9) break;
            const nextR = r - (npv / dNpv);
            if (Math.abs(nextR - r) < 1e-6) {
              r = nextR;
              break;
            }
            r = nextR;
          }

          setDisp('property_irr_result', (r * 100).toFixed(2) + '% IRR');
          setDisp('equity_multiple_em', em.toFixed(2) + '×');
          setDisp('net_profit_dollar', '$' + Math.round(netProfit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('annualized_cash_yield', avgYield.toFixed(2) + '% / yr');
        """
    },
    {
        "slug": "net-present-value",
        "category": "finance",
        "name": "Commercial Real Estate NPV & DCF Calculator",
        "description": "Calculate Net Present Value (NPV) and Discounted Cash Flow (DCF) valuation for commercial real estate properties at your required hurdle discount rate.",
        "hero_badge": "Institutional Underwriting • Real Estate DCF Matrix",
        "formula_display": "NPV = ∑ [CF_t / (1 + Discount Rate)^t] - Initial Investment",
        "fields": [
            {"id": "initial_purchase_equity", "label": "Initial Investment Outflow", "default": 750000, "prefix": "$", "min": 25000, "max": 100000000, "step": 25000, "hint": "Total equity capital deployed at acquisition"},
            {"id": "discount_rate_pct", "label": "Required Discount Rate / Hurdle Rate", "default": 9.5, "suffix": "%", "min": 2.0, "max": 25.0, "step": 0.25, "hint": "Weighted Average Cost of Capital (WACC) / hurdle rate"},
            {"id": "annual_noi_cashflow", "label": "Annual Net Cash Flow to Equity", "default": 68000, "prefix": "$", "min": 0, "max": 20000000, "step": 5000, "hint": "Net distributable cash flow per year"},
            {"id": "dcf_terminal_value", "label": "Terminal Net Exit Value (Year 5)", "default": 1150000, "prefix": "$", "min": 50000, "max": 200000000, "step": 50000, "hint": "Projected net exit value at Year 5"}
        ],
        "metrics": [
            {"id": "net_present_value_result", "label": "Net Present Value (NPV)", "default_display": "+$245,860.00", "highlight": True},
            {"id": "pv_future_cashflows", "label": "Present Value of Future Cash Flows", "default_display": "$995,860.00", "highlight": True},
            {"id": "profitability_index_pi", "label": "Profitability Index (PI)", "default_display": "1.33", "highlight": True},
            {"id": "investment_decision", "label": "Underwriting Directive", "default_display": "Accept (Generates +$245,860 above hurdle)"}
        ],
        "proof_steps": [
            {"step_title": "Discounted Cash Flow Summation", "step_text": "PV = ∑ [CF_t / (1 + r)^t], where r is your target discount rate (hurdle rate)."},
            {"step_title": "Net Economic Surplus (NPV)", "step_text": "NPV = PV of all future cash flows - Initial Capital Investment. NPV > 0 indicates the property yields returns above your required cost of capital."},
            {"step_title": "Profitability Index (Benefit-Cost Ratio)", "step_text": "Profitability Index PI = PV of Cash Inflows / Initial Outflow. PI > 1.0 confirms positive economic value creation."}
        ],
        "faqs": [
            {"q": "What discount rate should be used for real estate DCF?", "a": "Most commercial real estate investors use a discount rate between 8.0% and 12.0%, composed of the risk-free rate (10-year Treasury) plus a risk premium for asset illiquidity, tenant rollover risk, and debt leverage."},
            {"q": "What does a negative NPV mean?", "a": "A negative NPV does NOT mean the investment loses money! It simply means the investment earns less than your required discount rate. If your hurdle is 10% and the property earns 8%, NPV is negative."}
        ],
        "js_logic": """
          const c0 = getNum('initial_purchase_equity');
          const r = (getNum('discount_rate_pct') || 9.5) / 100;
          const cf = getNum('annual_noi_cashflow');
          const exitVal = getNum('dcf_terminal_value');

          let pv = 0;
          for (let t = 1; t <= 5; t++) {
            const flow = (t === 5) ? (cf + exitVal) : cf;
            pv += flow / Math.pow(1 + r, t);
          }

          const npv = pv - c0;
          const pi = c0 > 0 ? (pv / c0) : 0;

          setDisp('net_present_value_result', (npv >= 0 ? '+$' : '-$') + Math.abs(npv).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('pv_future_cashflows', '$' + Math.round(pv).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('profitability_index_pi', pi.toFixed(2));
          setDisp('investment_decision', npv >= 0 ? 'Accept (Generates +$' + Math.round(npv).toLocaleString() + ' above hurdle)' : 'Reject (Falls short of required ' + (r*100).toFixed(1) + '% return)');
        """
    },
    {
        "slug": "cash-on-cash-return",
        "category": "finance",
        "name": "Cash-on-Cash Return & Pre-Tax Yield Calculator",
        "description": "Calculate Cash-on-Cash (CoC) return percentage measuring annual pre-tax cash flow divided by total out-of-pocket cash capital invested.",
        "hero_badge": "Real Estate Investing • Cash-on-Cash Matrix",
        "formula_display": "Cash-on-Cash Return % = (Annual Pre-Tax Cash Flow / Total Cash Invested) × 100",
        "fields": [
            {"id": "annual_pretax_cf", "label": "Annual Pre-Tax Cash Flow (After Debt)", "default": 21600, "prefix": "$", "min": 0, "max": 5000000, "step": 500, "hint": "NOI minus annual mortgage principal and interest"},
            {"id": "purchase_down_payment", "label": "Cash Down Payment", "default": 175000, "prefix": "$", "min": 5000, "max": 50000000, "step": 5000, "hint": "Equity cash paid at closing"},
            {"id": "closing_costs_acquisition", "label": "Acquisition Closing Costs & Fees", "default": 12500, "prefix": "$", "min": 500, "max": 1000000, "step": 500, "hint": "Lender fees, title, legal, appraisal"},
            {"id": "upfront_rehab_capex", "label": "Initial Renovation & Repair Budget", "default": 25000, "prefix": "$", "min": 0, "max": 10000000, "step": 1000, "hint": "Upfront capital expenditures"}
        ],
        "metrics": [
            {"id": "coc_return_pct", "label": "Cash-on-Cash (CoC) Return", "default_display": "10.16% / yr", "highlight": True},
            {"id": "total_out_of_pocket_cash", "label": "Total Cash Invested (Denominator)", "default_display": "$212,500.00", "highlight": True},
            {"id": "monthly_cashflow_dividend", "label": "Monthly Net Cash Distribution", "default_display": "$1,800.00 / mo"},
            {"id": "payback_horizon_coc", "label": "Pure Cash Payback Horizon", "default_display": "9.8 years"}
        ],
        "proof_steps": [
            {"step_title": "Total Initial Capital Allocation", "step_text": "Total Cash Invested C_total = Down Payment + Closing Costs + Upfront Renovation/Rehab."},
            {"step_title": "Cash-on-Cash Return Formulation", "step_text": "CoC = (Annual Pre-Tax Cash Flow / C_total) × 100%. Measures instant liquid dividend yield on cash deployed."},
            {"step_title": "Leverage Multiplier Effect", "step_text": "If cap rate exceeds the cost of debt (positive leverage), financing a property with 75% LTV increases Cash-on-Cash return significantly above the unlevered cap rate."}
        ],
        "faqs": [
            {"q": "What is considered a good Cash-on-Cash return for rental property?", "a": "Most residential and small commercial real estate investors target an 8% to 12% Cash-on-Cash return. In ultra-prime appreciation markets (Los Angeles, New York), investors often accept 4% to 6%."},
            {"q": "How does Cash-on-Cash differ from Cap Rate?", "a": "Cap rate measures the property's unlevered operating return independent of financing (NOI / Purchase Price). Cash-on-Cash accounts for mortgage debt service and your actual out-of-pocket down payment."}
        ],
        "js_logic": """
          const cf = getNum('annual_pretax_cf');
          const down = getNum('purchase_down_payment');
          const close = getNum('closing_costs_acquisition');
          const rehab = getNum('upfront_rehab_capex');

          const totalInvested = down + close + rehab;
          const coc = totalInvested > 0 ? ((cf / totalInvested) * 100) : 0;
          const payback = cf > 0 ? (totalInvested / cf) : 0;

          setDisp('coc_return_pct', coc.toFixed(2) + '% / yr');
          setDisp('total_out_of_pocket_cash', '$' + totalInvested.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('monthly_cashflow_dividend', '$' + (cf / 12).toFixed(2) + ' / mo');
          setDisp('payback_horizon_coc', payback > 0 ? payback.toFixed(1) + ' years' : 'No cash flow');
        """
    },
    {
        "slug": "gross-rent-multiplier",
        "category": "finance",
        "name": "Gross Rent Multiplier (GRM) & Valuation Calculator",
        "description": "Calculate Gross Rent Multiplier (GRM) and estimate fair market multifamily property values from annual gross scheduled rents.",
        "hero_badge": "Multifamily Screening • GRM Metric Matrix",
        "formula_display": "GRM = Property Purchase Price / Gross Annual Scheduled Rent | Property Value = Gross Rent × GRM",
        "fields": [
            {"id": "property_price_grm", "label": "Property Purchase Price / Valuation", "default": 850000, "prefix": "$", "min": 50000, "max": 100000000, "step": 25000, "hint": "Asking or market price"},
            {"id": "gross_annual_rent", "label": "Gross Annual Scheduled Rent", "default": 96000, "prefix": "$", "min": 5000, "max": 20000000, "step": 2500, "hint": "Total gross rental income before expenses"},
            {"id": "market_target_grm", "label": "Comparable Market GRM Benchmark", "default": 8.5, "min": 3.0, "max": 25.0, "step": 0.1, "hint": "Average GRM of recent comparable neighborhood sales"}
        ],
        "metrics": [
            {"id": "actual_grm_result", "label": "Property Gross Rent Multiplier", "default_display": "8.85 GRM", "highlight": True},
            {"id": "market_fair_value", "label": "Indicated Value at Market GRM (8.5)", "default_display": "$816,000.00", "highlight": True},
            {"id": "monthly_gross_rent", "label": "Monthly Gross Scheduled Rent", "default_display": "$8,000.00 / mo"},
            {"id": "valuation_verdict", "label": "Pricing Relative to Market", "default_display": "Priced Above Market (Overpriced by $34,000)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Rent Multiplier Definition", "step_text": "GRM = Purchase Price / Gross Annual Rent. A GRM of 8.85 means the purchase price is 8.85 times annual gross income."},
            {"step_title": "Comparable Valuation Inversion", "step_text": "Fair Market Property Value = Gross Annual Rent × Neighborhood Target GRM."},
            {"step_title": "Rapid Screening Utility", "step_text": "GRM provides a 10-second preliminary filter to identify potentially undervalued multifamily properties before undertaking detailed expense due diligence."}
        ],
        "faqs": [
            {"q": "What is considered a good Gross Rent Multiplier?", "a": "A lower GRM indicates a potentially better value. In most mid-sized US markets, a GRM between 6.0 and 8.5 is considered attractive. High-growth coastal markets often trade at GRMs of 12.0 to 18.0+."},
            {"q": "What is the primary limitation of GRM?", "a": "GRM ignores operating expenses, property taxes, insurance, and utilities. Two buildings with identical gross rents and GRMs may have vastly different net profits if one has separate electric meters while the other has an owner-paid central boiler."}
        ],
        "js_logic": """
          const price = getNum('property_price_grm');
          const rent = getNum('gross_annual_rent') || 1;
          const targetGrm = getNum('market_target_grm');

          const grm = price / rent;
          const fairVal = rent * targetGrm;
          const diff = price - fairVal;

          let verdict = 'Priced at Fair Market Value';
          if (diff > 5000) verdict = 'Priced Above Market (Overpriced by $' + Math.round(diff).toLocaleString() + ')';
          else if (diff < -5000) verdict = 'Attractively Discounted (Underpriced by $' + Math.round(Math.abs(diff)).toLocaleString() + ')';

          setDisp('actual_grm_result', grm.toFixed(2) + ' GRM');
          setDisp('market_fair_value', '$' + Math.round(fairVal).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('monthly_gross_rent', '$' + (rent / 12).toFixed(2) + ' / mo');
          setDisp('valuation_verdict', verdict);
        """
    },
    {
        "slug": "exchange-1031",
        "category": "finance",
        "name": "Section 1031 Like-Kind Exchange & Tax Deferral Calculator",
        "description": "Calculate deferred federal capital gains tax, net boot, depreciation recapture tax, and replacement property equity requirements under IRS Section 1031.",
        "hero_badge": "Tax Deferral • Section 1031 Matrix",
        "formula_display": "Realized Gain = Net Sales Price - Adjusted Basis | Tax Deferred = (Cap Gain × Rate) + (Recapture × 25%)",
        "fields": [
            {"id": "relinquished_sales_price", "label": "Relinquished Property Sale Price", "default": 1200000, "prefix": "$", "min": 50000, "max": 100000000, "step": 25000, "hint": "Gross sales price of sold property"},
            {"id": "original_purchase_basis", "label": "Original Purchase Basis (Cost + Improvements)", "default": 650000, "prefix": "$", "min": 25000, "max": 100000000, "step": 25000, "hint": "Original cost basis plus capitalized capital improvements"},
            {"id": "accumulated_depreciation", "label": "Total Accumulated Depreciation Deducted", "default": 180000, "prefix": "$", "min": 0, "max": 20000000, "step": 10000, "hint": "Depreciation taken over ownership"},
            {"id": "relinquished_loan_payoff", "label": "Mortgage Debt Paid Off at Closing", "default": 450000, "prefix": "$", "min": 0, "max": 50000000, "step": 25000, "hint": "Lender payoff balance"}
        ],
        "metrics": [
            {"id": "total_tax_deferred", "label": "Total Estimated Tax Deferred", "default_display": "$191,000.00", "highlight": True},
            {"id": "net_capital_gain", "label": "Total Realized Taxable Gain", "default_display": "$730,000.00", "highlight": True},
            {"id": "replacement_min_purchase", "label": "Min Replacement Purchase to Avoid Boot", "default_display": "$1,200,000.00", "highlight": True},
            {"id": "net_exchange_equity", "label": "Cash Equity Transferred to QI Escrow", "default_display": "$750,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Adjusted Basis Calculation", "step_text": "Adjusted Basis = Original Basis - Accumulated Depreciation. For example: $650,000 - $180,000 = $470,000."},
            {"step_title": "Realized Gain Decomposition", "step_text": "Total Gain = Sales Price - Adjusted Basis = $1,200,000 - $470,000 = $730,000. Composed of $180,000 depreciation recapture (taxed at 25%) + $550,000 capital gain (taxed at 20% federal + 3.8% NIIT + ~3% state)."},
            {"step_title": "Full Deferral Rules", "step_text": "To achieve 100% tax deferral with zero taxable boot, the replacement property must have equal or greater purchase price AND equal or greater debt/equity."}
        ],
        "faqs": [
            {"q": "What are the strict Section 1031 exchange deadlines?", "a": "You must formally identify replacement properties within 45 calendar days of closing on the relinquished property, and close on the replacement property within 180 calendar days."},
            {"q": "What is 'Boot' in a 1031 exchange?", "a": "Boot is any non-like-kind property received during the exchange (such as cash left over from the closing or debt reduction). Boot is fully taxable up to the amount of realized gain."}
        ],
        "js_logic": """
          const sale = getNum('relinquished_sales_price');
          const orig = getNum('original_purchase_basis');
          const dep = getNum('accumulated_depreciation');
          const debt = getNum('relinquished_loan_payoff');

          const adjustedBasis = Math.max(0, orig - dep);
          const totalGain = Math.max(0, sale - adjustedBasis);
          const capGainPortion = Math.max(0, totalGain - dep);

          const depRecaptureTax = dep * 0.25;
          const capGainTax = capGainPortion * 0.265; // 20% fed + 3.8% NIIT + state avg
          const totalTaxDeferred = depRecaptureTax + capGainTax;
          const netEquity = Math.max(0, sale - debt);

          setDisp('total_tax_deferred', '$' + Math.round(totalTaxDeferred).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_capital_gain', '$' + Math.round(totalGain).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('replacement_min_purchase', '$' + sale.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_exchange_equity', '$' + netEquity.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "cap-rate-sensitivity",
        "category": "finance",
        "name": "Cap Rate Sensitivity & Valuation Matrix Calculator",
        "description": "Calculate commercial property asset valuation sensitivity across varying Net Operating Income (NOI) levels and exit capitalization rates.",
        "hero_badge": "Valuation Engineering • Cap Rate Sensitivity Matrix",
        "formula_display": "Property Value = Net Operating Income (NOI) / Capitalization Rate (Cap Rate)",
        "fields": [
            {"id": "base_noi_annual", "label": "Current Net Operating Income (NOI)", "default": 180000, "prefix": "$", "min": 10000, "max": 25000000, "step": 5000, "hint": "Base annual NOI before debt service"},
            {"id": "base_cap_rate_pct", "label": "Current Capitalization Rate (%)", "default": 6.0, "suffix": "%", "min": 2.5, "max": 14.0, "step": 0.25, "hint": "Current market baseline cap rate"},
            {"id": "noi_growth_scenario_pct", "label": "Projected NOI Growth / Optimization (%)", "default": 15, "suffix": "%", "min": -30, "max": 100, "step": 1, "hint": "Value-add upside from raising rents/cutting expenses"},
            {"id": "exit_cap_rate_shift_bps", "label": "Exit Cap Rate Expansion (+/- bps)", "default": 50, "suffix": "bps", "min": -200, "max": 300, "step": 25, "hint": "Cap rate expansion/compression (+50 bps = +0.50%)"}
        ],
        "metrics": [
            {"id": "optimized_exit_value", "label": "Projected Future Exit Valuation", "default_display": "$3,184,615.00", "highlight": True},
            {"id": "current_base_valuation", "label": "Current Baseline Asset Valuation", "default_display": "$3,000,000.00", "highlight": True},
            {"id": "net_value_created", "label": "Net Equity Value Created", "default_display": "+$184,615.00", "highlight": True},
            {"id": "exit_cap_rate_used", "label": "Exit Cap Rate Applied", "default_display": "6.50% (50 bps expansion)"}
        ],
        "proof_steps": [
            {"step_title": "Direct Capitalization Valuation Formula", "step_text": "Value = NOI / Cap Rate. Baseline Value = $180,000 / 0.06 = $3,000,000."},
            {"step_title": "Optimized Value-Add NOI", "step_text": "Future NOI = Base NOI × (1 + Growth% / 100). For example: $180,000 × 1.15 = $207,000."},
            {"step_title": "Cap Rate Decompression Drag", "step_text": "Exit Cap Rate = Base Cap Rate + (Basis Points / 100). Exit Value = $207,000 / 0.065 = $3,184,615. Increasing NOI by 15% preserved value creation even as interest rates pushed cap rates up by 50 bps."}
        ],
        "faqs": [
            {"q": "What happens to commercial property value when cap rates rise?", "a": "Rising cap rates decrease property values unless NOI increases fast enough to offset the expansion. For a property with $100k NOI, a cap rate increase from 5% to 6% cuts property value from $2,000,000 down to $1,666,667 (a $333,333 loss)."},
            {"q": "What causes cap rates to compress or expand?", "a": "Cap rates compress (lowering yields, raising valuations) during periods of low interest rates, high institutional capital inflows, and strong rent growth. Cap rates expand when borrowing interest rates rise."}
        ],
        "js_logic": """
          const baseNoi = getNum('base_noi_annual');
          const baseCap = (getNum('base_cap_rate_pct') || 6.0) / 100;
          const growth = (getNum('noi_growth_scenario_pct') || 15) / 100;
          const bps = getNum('exit_cap_rate_shift_bps');

          const currentVal = baseCap > 0 ? (baseNoi / baseCap) : 0;
          const optNoi = baseNoi * (1 + growth);
          const exitCap = baseCap + (bps / 10000);
          const exitVal = exitCap > 0 ? (optNoi / exitCap) : 0;
          const valueCreated = exitVal - currentVal;

          setDisp('optimized_exit_value', '$' + Math.round(exitVal).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('current_base_valuation', '$' + Math.round(currentVal).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_value_created', (valueCreated >= 0 ? '+$' : '-$') + Math.abs(Math.round(valueCreated)).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('exit_cap_rate_used', (exitCap * 100).toFixed(2) + '% (' + (bps >= 0 ? '+' : '') + bps + ' bps shift)');
        """
    },
    {
        "slug": "rent-roll-analysis",
        "category": "finance",
        "name": "Commercial Rent Roll & Economic Vacancy Calculator",
        "description": "Analyze commercial rent rolls, Gross Potential Rent (GPR), physical vacancy, economic concessions, and Effective Gross Income (EGI).",
        "hero_badge": "Property Management • Rent Roll Underwriting",
        "formula_display": "Effective Gross Income (EGI) = Gross Potential Rent - Physical Vacancy - Concessions + Ancillary Income",
        "fields": [
            {"id": "gross_potential_rent_gpr", "label": "Gross Potential Rent (100% Occupied)", "default": 360000, "prefix": "$", "min": 10000, "max": 50000000, "step": 5000, "hint": "Market rent if 100% of units occupied at market rates"},
            {"id": "physical_vacancy_pct", "label": "Physical Vacancy Rate (%)", "default": 6.5, "suffix": "%", "min": 0.0, "max": 50.0, "step": 0.5, "hint": "Percentage of units physically unleased"},
            {"id": "tenant_concessions_discounts", "label": "Annual Concessions & Free Rent", "default": 7500, "prefix": "$", "min": 0, "max": 1000000, "step": 500, "hint": "Move-in discounts, rent abatements, bad debt"},
            {"id": "ancillary_income_annual", "label": "Ancillary Other Income (Parking, Laundry, Storage)", "default": 18000, "prefix": "$", "min": 0, "max": 5000000, "step": 500, "hint": "Pet fees, RUBS utility reimbursement, storage"}
        ],
        "metrics": [
            {"id": "effective_gross_income_egi", "label": "Effective Gross Income (EGI)", "default_display": "$347,100.00 / yr", "highlight": True},
            {"id": "economic_occupancy_pct", "label": "Economic Occupancy Rate", "default_display": "91.42%", "highlight": True},
            {"id": "total_revenue_loss", "label": "Total Revenue Leakage (Vacancy + Concessions)", "default_display": "$30,900.00 / yr"},
            {"id": "monthly_egi", "label": "Average Monthly Operating Collections", "default_display": "$28,925.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Gross Potential vs Collected Realization", "step_text": "Gross Potential Rent (GPR) represents the mathematical upper bound ceiling assuming 100% occupancy at full market rent."},
            {"step_title": "Physical vs Economic Vacancy Disparity", "step_text": "A building can be 95% physically occupied, but if tenants receive 1 month free rent or default on payments, economic occupancy may only be 87%: Economic Occupancy = (Actual Collected Rent / GPR) × 100%."},
            {"step_title": "EGI Underwriting Metric", "step_text": "EGI = GPR - Vacancy Loss - Concessions + Ancillary Income. EGI is the foundational top-line revenue number used by banks for commercial loan underwriting."}
        ],
        "faqs": [
            {"q": "What is the difference between physical occupancy and economic occupancy?", "a": "Physical occupancy measures whether a warm body has keys to the apartment. Economic occupancy measures actual dollars collected relative to market potential. Economic occupancy accounts for uncollected rent, concessions, and employee model units."},
            {"q": "What is a standard vacancy factor used by commercial lenders?", "a": "Lenders typically underwrite a minimum 5.0% to 10.0% vacancy and credit loss factor, even if a property is currently 100% leased."}
        ],
        "js_logic": """
          const gpr = getNum('gross_potential_rent_gpr') || 1;
          const vacRate = (getNum('physical_vacancy_pct') || 6.5) / 100;
          const concessions = getNum('tenant_concessions_discounts');
          const ancillary = getNum('ancillary_income_annual');

          const vacLoss = gpr * vacRate;
          const totalLeakage = vacLoss + concessions;
          const egi = (gpr - totalLeakage) + ancillary;
          const collectedRentalOnly = gpr - totalLeakage;
          const economicOcc = (collectedRentalOnly / gpr) * 100;

          setDisp('effective_gross_income_egi', '$' + Math.round(egi).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('economic_occupancy_pct', economicOcc.toFixed(2) + '%');
          setDisp('total_revenue_loss', '$' + Math.round(totalLeakage).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('monthly_egi', '$' + (egi / 12).toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "cost-segregation",
        "category": "finance",
        "name": "Cost Segregation & Accelerated Depreciation Calculator",
        "description": "Estimate year 1 bonus depreciation tax deductions segregating commercial or residential real estate into 5-year, 15-year, and 27.5/39-year property.",
        "hero_badge": "Tax Engineering • Cost Segregation Shield",
        "formula_display": "Year 1 Deduction = (5-Year Asset × Bonus %) + (15-Year Asset × Bonus %) + Straight-Line Real Property",
        "fields": [
            {"id": "depreciable_building_basis", "label": "Depreciable Basis (Excluding Land)", "default": 1500000, "prefix": "$", "min": 100000, "max": 100000000, "step": 50000, "hint": "Purchase price minus non-depreciable land allocation (~15-20%)"},
            {"id": "bonus_depreciation_pct", "label": "IRS Bonus Depreciation Percentage", "default": 60, "suffix": "%", "min": 0, "max": 100, "step": 20, "hint": "Tax cuts phase-down: 80% in 2023, 60% in 2024, 40% in 2025, 20% in 2026"},
            {"id": "investor_marginal_tax_rate", "label": "Investor Marginal Tax Bracket", "default": 37, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Top federal + state income tax bracket"}
        ],
        "metrics": [
            {"id": "year1_total_tax_deduction", "label": "Estimated Year 1 Accelerated Deduction", "default_display": "$288,000.00", "highlight": True},
            {"id": "year1_cash_tax_savings", "label": "Immediate Cash Tax Shield Savings", "default_display": "$106,560.00 Cash Saved", "highlight": True},
            {"id": "personal_property_reallocated", "label": "5-Year Personal Property (18%)", "default_display": "$270,000.00"},
            {"id": "land_improvement_reallocated", "label": "15-Year Land Improvements (12%)", "default_display": "$180,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Asset Class Decomposition Engineering", "step_text": "Standard commercial real estate depreciates over 39 years (27.5 for residential). Cost segregation reclassifies 20% to 35% of building components into 5-year personal property (carpeting, millwork, specialty lighting) and 15-year land improvements (paving, sidewalks, fences)."},
            {"step_title": "Bonus Depreciation Acceleration", "step_text": "Under IRC Section 168(k), qualifying 5-year and 15-year assets qualify for immediate bonus depreciation write-offs."},
            {"step_title": "Instant Cash Tax Shield", "step_text": "Cash Tax Savings = Total Year 1 Deductions × Investor Marginal Tax Rate. Accelerating $288,000 in deductions at a 37% bracket yields $106,560 in immediate cash tax reduction in Year 1."}
        ],
        "faqs": [
            {"q": "What is the cost of a formal engineering cost segregation study?", "a": "A certified engineering-based cost segregation study typically costs $4,000 to $8,000 for mid-sized commercial properties, but routinely generates $50,000 to $150,000+ in immediate first-year tax savings."},
            {"q": "Can passive investors use cost segregation losses against active W2 income?", "a": "Generally no, unless the taxpayer or their spouse qualifies as a Real Estate Professional (REPS) under IRS rules, or utilizes the Short-Term Rental (STR) average 7-day stay loophole."}
        ],
        "js_logic": """
          const basis = getNum('depreciable_building_basis');
          const bonusRate = (getNum('bonus_depreciation_pct') || 60) / 100;
          const taxRate = (getNum('investor_marginal_tax_rate') || 37) / 100;

          const prop5Yr = basis * 0.18;
          const prop15Yr = basis * 0.12;
          const propReal = basis * 0.70;

          const bonusDeduction = (prop5Yr + prop15Yr) * bonusRate;
          const straightLineYr1 = (propReal / 27.5) + ((prop5Yr + prop15Yr) * (1 - bonusRate) / 10);
          const totalYr1Deduction = bonusDeduction + straightLineYr1;
          const taxSaved = totalYr1Deduction * taxRate;

          setDisp('year1_total_tax_deduction', '$' + Math.round(totalYr1Deduction).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('year1_cash_tax_savings', '$' + Math.round(taxSaved).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Cash Saved');
          setDisp('personal_property_reallocated', '$' + Math.round(prop5Yr).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('land_improvement_reallocated', '$' + Math.round(prop15Yr).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "preferred-return-waterfall",
        "category": "finance",
        "name": "Syndication Preferred Return & Waterfall Equity Calculator",
        "description": "Calculate private equity syndication waterfall distributions between General Partners (GP) and Limited Partners (LP) with preferred returns and promote hurdles.",
        "hero_badge": "Syndication Structuring • Equity Waterfall Matrix",
        "formula_display": "Hurdle 1: 100% to LP until 8% Pref | Hurdle 2: 80% LP / 20% GP Promote Split",
        "fields": [
            {"id": "lp_capital_invested", "label": "Limited Partner (LP) Capital Invested", "default": 2000000, "prefix": "$", "min": 50000, "max": 100000000, "step": 50000, "hint": "Total equity contributed by outside passive investors"},
            {"id": "lp_preferred_return_pct", "label": "LP Preferred Return (Pref Rate %)", "default": 8.0, "suffix": "%", "min": 4.0, "max": 15.0, "step": 0.5, "hint": "Annual hurdle return before GP receives promote"},
            {"id": "gp_promote_split_pct", "label": "GP Promote Share Above Hurdle", "default": 20, "suffix": "%", "min": 5, "max": 50, "step": 5, "hint": "Carried interest share to sponsor (e.g. 80/20 split = 20% GP)"},
            {"id": "total_distributable_cash", "label": "Total Cash Available for Distribution", "default": 450000, "prefix": "$", "min": 10000, "max": 20000000, "step": 10000, "hint": "Operating cash or refinancing/sale proceeds"}
        ],
        "metrics": [
            {"id": "lp_total_payout", "label": "Limited Partner (LP) Total Distribution", "default_display": "$392,000.00 (87.1%)", "highlight": True},
            {"id": "gp_promote_payout", "label": "General Partner (GP) Promote Distribution", "default_display": "$58,000.00 (12.9%)", "highlight": True},
            {"id": "lp_pref_hurdle_dollar", "label": "LP 8.0% Preferred Return Amount", "default_display": "$160,000.00"},
            {"id": "excess_split_cash", "label": "Distributable Cash Above Hurdle", "default_display": "$290,000.00"}
        ],
        "proof_steps": [
            {"step_title": "First Priority Preferred Hurdle", "step_text": "LP Preferred Dollar Hurdle = LP Capital × (Pref Rate% / 100). The first $160,000 goes 100% to passive LP investors."},
            {"step_title": "Secondary Tier Promote Split", "step_text": "Excess Distributable Cash = Total Cash - LP Pref. Any surplus is split according to the promote agreement (e.g. 80% to LP, 20% to GP sponsor)."},
            {"step_title": "Alignment of Interests", "step_text": "Waterfalls ensure sponsors earn performance fees (promote) only after delivering passive investors their promised hurdle return."}
        ],
        "faqs": [
            {"q": "What is cumulative vs non-cumulative preferred return?", "a": "A cumulative pref means if property cash flow is insufficient to pay the full 8% in Year 1, the unpaid balance accrues into Year 2 and must be paid in full before the GP can ever receive promote distributions."},
            {"q": "What is a GP catch-up clause?", "a": "A catch-up clause allows the GP to receive 50% to 100% of distributions immediately following the preferred return until the GP's share matches their promote percentage on total profits."}
        ],
        "js_logic": """
          const lpCap = getNum('lp_capital_invested');
          const prefRate = (getNum('lp_preferred_return_pct') || 8.0) / 100;
          const gpPromoteRate = (getNum('gp_promote_split_pct') || 20) / 100;
          const totalCash = getNum('total_distributable_cash');

          const prefDollar = lpCap * prefRate;
          let lpPayout = Math.min(totalCash, prefDollar);
          let gpPayout = 0;

          const excess = Math.max(0, totalCash - prefDollar);
          if (excess > 0) {
            const gpShare = excess * gpPromoteRate;
            const lpShare = excess * (1 - gpPromoteRate);
            gpPayout += gpShare;
            lpPayout += lpShare;
          }

          const lpPct = totalCash > 0 ? (lpPayout / totalCash) * 100 : 0;
          const gpPct = totalCash > 0 ? (gpPayout / totalCash) * 100 : 0;

          setDisp('lp_total_payout', '$' + Math.round(lpPayout).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + lpPct.toFixed(1) + '%)');
          setDisp('gp_promote_payout', '$' + Math.round(gpPayout).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + gpPct.toFixed(1) + '%)');
          setDisp('lp_pref_hurdle_dollar', '$' + Math.round(prefDollar).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('excess_split_cash', '$' + Math.round(excess).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "commercial-lease-nnn",
        "category": "finance",
        "name": "Triple Net (NNN) vs Full Service Gross Lease Calculator",
        "description": "Compare commercial lease structures: Triple Net (NNN) versus Full Service Gross (FSG), converting CAM, property tax, and insurance into effective rates.",
        "hero_badge": "Commercial Leasing • NNN vs Gross Matrix",
        "formula_display": "Total NNN Rent = Base Rent + CAM Pass-Through + Property Taxes + Insurance",
        "fields": [
            {"id": "rentable_sqft", "label": "Leased Space Area (Rentable SF)", "default": 4500, "suffix": "RSF", "min": 250, "max": 500000, "step": 250, "hint": "Square feet leased"},
            {"id": "nnn_base_rent_psf", "label": "NNN Quoted Base Rent ($/SF/Yr)", "default": 24.00, "prefix": "$", "min": 5.00, "max": 200.00, "step": 0.50, "hint": "Base annual rent per square foot"},
            {"id": "cam_expenses_psf", "label": "Estimated CAM Operating Expenses ($/SF/Yr)", "default": 5.50, "prefix": "$", "min": 0.50, "max": 50.00, "step": 0.25, "hint": "Common area maintenance pass-through"},
            {"id": "property_tax_insurance_psf", "label": "Taxes & Insurance Pass-Through ($/SF/Yr)", "default": 3.75, "prefix": "$", "min": 0.50, "max": 50.00, "step": 0.25, "hint": "Building property taxes and hazard insurance"},
            {"id": "comp_gross_rent_psf", "label": "Alternative Full Service Gross Quote ($/SF/Yr)", "default": 35.00, "prefix": "$", "min": 10.00, "max": 250.00, "step": 0.50, "hint": "All-inclusive gross lease quote"}
        ],
        "metrics": [
            {"id": "all_in_nnn_rent_psf", "label": "Effective All-In NNN Cost ($/SF/Yr)", "default_display": "$33.25 / SF / yr", "highlight": True},
            {"id": "annual_nnn_total_cost", "label": "Total Annual NNN Outflow", "default_display": "$149,625.00 / yr", "highlight": True},
            {"id": "fsg_annual_cost", "label": "Total Annual Full Service Gross Cost", "default_display": "$157,500.00 / yr", "highlight": True},
            {"id": "lease_recommendation", "label": "Financial Advantage", "default_display": "NNN Lease Saves $7,875.00 / year"}
        ],
        "proof_steps": [
            {"step_title": "NNN Expense Pass-Through Summation", "step_text": "Effective NNN Rent PSF = Base Rent + CAM + Property Taxes + Insurance = $24.00 + $5.50 + $3.75 = $33.25/SF."},
            {"step_title": "Total Annual Commitment", "step_text": "Annual Cost = RSF × Effective Rate PSF. 4,500 RSF × $33.25 = $149,625/yr ($12,468.75/mo)."},
            {"step_title": "Risk Transfer Trade-off", "step_text": "Full service gross leases charge a premium ($35.00/SF) in exchange for the landlord absorbing all future spikes in property taxes and utility rates."}
        ],
        "faqs": [
            {"q": "What is included in commercial CAM expenses?", "a": "Common Area Maintenance (CAM) includes parking lot sweeping, snow removal, exterior landscaping, security, roof maintenance, HVAC service contracts, and property management administrative fees."},
            {"q": "What is an expense stop in a modified gross lease?", "a": "An expense stop sets a baseline year of operating expenses paid by the landlord. If expenses rise in subsequent years above that stop, the tenant pays the pro-rata increase."}
        ],
        "js_logic": """
          const sf = getNum('rentable_sqft');
          const base = getNum('nnn_base_rent_psf');
          const cam = getNum('cam_expenses_psf');
          const ti = getNum('property_tax_insurance_psf');
          const grossPsf = getNum('comp_gross_rent_psf');

          const allInNnn = base + cam + ti;
          const totalNnnAnnual = sf * allInNnn;
          const totalGrossAnnual = sf * grossPsf;
          const diff = totalGrossAnnual - totalNnnAnnual;

          let adv = totalNnnAnnual < totalGrossAnnual ? ('NNN Lease Saves $' + Math.round(diff).toLocaleString() + ' / year') : ('Gross Lease Saves $' + Math.round(Math.abs(diff)).toLocaleString() + ' / year');

          setDisp('all_in_nnn_rent_psf', '$' + allInNnn.toFixed(2) + ' / SF / yr');
          setDisp('annual_nnn_total_cost', '$' + Math.round(totalNnnAnnual).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('fsg_annual_cost', '$' + Math.round(totalGrossAnnual).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('lease_recommendation', adv);
        """
    },
    {
        "slug": "tenant-improvement",
        "category": "finance",
        "name": "Tenant Improvement (TI) Allowance & Amortization Calculator",
        "description": "Calculate Tenant Improvement (TI) build-out costs, landlord allowances per square foot, leasing commissions, and effective net rent.",
        "hero_badge": "Commercial Underwriting • TI Amortization Matrix",
        "formula_display": "TI Amortization = Total TI Allowance × [r(1+r)ⁿ] / [(1+r)ⁿ - 1] | Effective Net Rent = Base Rent - Amortized TI",
        "fields": [
            {"id": "leased_square_footage", "label": "Leased Premises Area (SF)", "default": 5000, "suffix": "SF", "min": 500, "max": 250000, "step": 500, "hint": "Rentable square footage"},
            {"id": "ti_allowance_psf", "label": "Landlord TI Allowance ($/SF)", "default": 45.00, "prefix": "$", "min": 0, "max": 250.00, "step": 5.00, "hint": "Cash contributed by landlord toward buildout"},
            {"id": "lease_term_years", "label": "Lease Term Duration (Years)", "default": 5, "suffix": "years", "min": 1, "max": 20, "step": 1, "hint": "Primary lease commitment term"},
            {"id": "landlord_cost_of_capital", "label": "Landlord Cost of Capital / Interest Rate", "default": 8.0, "suffix": "%", "min": 4.0, "max": 15.0, "step": 0.5, "hint": "Cost of financing TI capital"},
            {"id": "contract_base_rent_psf", "label": "Contract Base Rent ($/SF/Yr)", "default": 32.00, "prefix": "$", "min": 10.00, "max": 150.00, "step": 1.00, "hint": "Stated annual rent per SF"}
        ],
        "metrics": [
            {"id": "total_ti_cash_outflow", "label": "Total Landlord TI Cash Outlay", "default_display": "$225,000.00", "highlight": True},
            {"id": "annualized_ti_amortization", "label": "Annualized TI Amortization Drag", "default_display": "$56,350.00 / yr", "highlight": True},
            {"id": "ti_cost_psf_annual", "label": "Amortized TI Cost per SF", "default_display": "$11.27 / SF / yr", "highlight": True},
            {"id": "effective_net_rent_psf", "label": "Effective Net Rent Realized by Landlord", "default_display": "$20.73 / SF / yr"}
        ],
        "proof_steps": [
            {"step_title": "Gross TI Capital Deployment", "step_text": "Total TI Outlay = Leased Area (SF) × Allowance per SF = 5,000 × $45 = $225,000."},
            {"step_title": "Capital Recovery Amortization", "step_text": "Amortizing $225,000 over 5 years at 8% cost of capital requires $56,350 annually ($11.27/SF/yr)."},
            {"step_title": "Effective Net Rent Reality", "step_text": "Effective Net Rent = Contract Rent - Amortized TI. While the lease reads $32.00/SF, the landlord actually nets only $20.73/SF after recovering upfront buildout capital."}
        ],
        "faqs": [
            {"q": "What is the difference between turnkey buildout and a TI allowance?", "a": "A TI allowance provides a fixed dollar budget (e.g. $45/SF); any cost overruns must be paid by the tenant. In a turnkey buildout, the landlord agrees to deliver the space completed to agreed architectural specifications regardless of cost overruns."},
            {"q": "Can unused TI allowance be taken as rent credit?", "a": "Only if explicitly negotiated in the commercial lease agreement. Most standard commercial leases stipulate that unused TI allowances are forfeited by the tenant at rent commencement."}
        ],
        "js_logic": """
          const sf = getNum('leased_square_footage');
          const tiPsf = getNum('ti_allowance_psf');
          const term = getNum('lease_term_years') || 5;
          const r = ((getNum('landlord_cost_of_capital') || 8.0) / 100);
          const baseRent = getNum('contract_base_rent_psf');

          const totalTi = sf * tiPsf;
          const annualPmt = r > 0 ? (totalTi * (r * Math.pow(1 + r, term)) / (Math.pow(1 + r, term) - 1)) : (totalTi / term);
          const tiPsfAnnual = sf > 0 ? (annualPmt / sf) : 0;
          const effectiveNetRent = baseRent - tiPsfAnnual;

          setDisp('total_ti_cash_outflow', '$' + Math.round(totalTi).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('annualized_ti_amortization', '$' + Math.round(annualPmt).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('ti_cost_psf_annual', '$' + tiPsfAnnual.toFixed(2) + ' / SF / yr');
          setDisp('effective_net_rent_psf', '$' + effectiveNetRent.toFixed(2) + ' / SF / yr');
        """
    },
    {
        "slug": "str-airbnb-cashflow",
        "category": "finance",
        "name": "Short-Term Rental (Airbnb) Cash Flow & ADR Calculator",
        "description": "Calculate Short-Term Rental (STR / VRBO) net monthly cash flow, Average Daily Rate (ADR), occupancy yields, cleaning fees, and platform commissions.",
        "hero_badge": "Hospitality Economics • STR Cash Flow Matrix",
        "formula_display": "Gross Revenue = ADR × Occupied Nights + Cleaning Fees | Net Cash Flow = Gross Revenue - OpEx - Mortgage",
        "fields": [
            {"id": "avg_daily_rate_adr", "label": "Average Daily Rate (ADR)", "default": 245, "prefix": "$", "min": 50, "max": 3500, "step": 5, "hint": "Average nightly booking price"},
            {"id": "occupancy_rate_pct", "label": "Projected Occupancy Rate (%)", "default": 68, "suffix": "%", "min": 15, "max": 95, "step": 1, "hint": "Percentage of days booked per year"},
            {"id": "monthly_mortgage_pi", "label": "Monthly Mortgage Debt (P&I + Taxes + Insurance)", "default": 2400, "prefix": "$", "min": 500, "max": 25000, "step": 50, "hint": "Total monthly housing payment"},
            {"id": "cleaning_mgmt_fee_pct", "label": "Management & Platform Fee Share (%)", "default": 20, "suffix": "%", "min": 3, "max": 40, "step": 1, "hint": "Airbnb fee (3%) + Co-host/PMS management (15-20%)"}
        ],
        "metrics": [
            {"id": "net_monthly_str_cashflow", "label": "Net Monthly Cash Flow", "default_display": "+$1,650.00 / mo", "highlight": True},
            {"id": "gross_annual_str_revenue", "label": "Gross Annual Rental Revenue", "default_display": "$60,809.00 / yr", "highlight": True},
            {"id": "annual_occupied_nights", "label": "Total Booked Nights per Year", "default_display": "248 nights"},
            {"id": "monthly_operating_expenses", "label": "Operating Expenses (OpEx + Fees)", "default_display": "$1,413.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Nightly Booking Realization", "step_text": "Booked Nights = 365 × (Occupancy% / 100) = 365 × 0.68 = 248 nights."},
            {"step_title": "Top-Line Revenue Realization", "step_text": "Gross Annual Revenue = Booked Nights × ADR. 248 × $245 = $60,809/yr ($5,067/mo)."},
            {"step_title": "Hospitality Operating Cost Burden", "step_text": "STRs incur higher operating expenses than long-term rentals: utilities, consumable amenities, PMS software, co-host fees, and high-frequency maintenance consume 25% to 35% of gross revenue."}
        ],
        "faqs": [
            {"q": "What is the STR Tax Loophole?", "a": "Under Treasury Regulation Section 1.469-1T(e)(3)(ii)(A), short-term rentals with an average guest stay of 7 days or less are classified as non-rental businesses. If you materially participate (100+ hours), cost segregation depreciation losses can shelter W-2 and active business income without needing Real Estate Professional Status."},
            {"q": "What is a healthy STR occupancy rate?", "a": "National average STR occupancy is 55% to 65%. Well-located, highly reviewed properties with dynamic pricing software (PriceLabs, Wheelhouse) achieve 70% to 80%."}
        ],
        "js_logic": """
          const adr = getNum('avg_daily_rate_adr');
          const occ = (getNum('occupancy_rate_pct') || 68) / 100;
          const mortgage = getNum('monthly_mortgage_pi');
          const feePct = (getNum('cleaning_mgmt_fee_pct') || 20) / 100;

          const nights = Math.round(365 * occ);
          const grossAnnual = nights * adr;
          const grossMo = grossAnnual / 12;

          const utilitiesAndSuppliesMo = 400;
          const mgmtMo = grossMo * feePct;
          const totalOpexMo = mgmtMo + utilitiesAndSuppliesMo;
          const netCashFlowMo = grossMo - totalOpexMo - mortgage;

          setDisp('net_monthly_str_cashflow', (netCashFlowMo >= 0 ? '+$' : '-$') + Math.abs(Math.round(netCashFlowMo)).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
          setDisp('gross_annual_str_revenue', '$' + Math.round(grossAnnual).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('annual_occupied_nights', nights + ' nights');
          setDisp('monthly_operating_expenses', '$' + Math.round(totalOpexMo).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / mo');
        """
    },
    {
        "slug": "property-tax-proration",
        "category": "finance",
        "name": "Closing Day Property Tax Proration Calculator",
        "description": "Calculate exact real estate closing day property tax prorations, daily per diem tax rates, and buyer/seller credits using 365-day calendar year rules.",
        "hero_badge": "Closing Escrow • Tax Proration Matrix",
        "formula_display": "Daily Tax Rate = Annual Property Tax / 365 | Seller Credit = Daily Tax × Seller Days Owned",
        "fields": [
            {"id": "annual_tax_bill_total", "label": "Total Annual Property Tax Bill", "default": 6200, "prefix": "$", "min": 250, "max": 150000, "step": 100, "hint": "Annual county/city tax assessment"},
            {"id": "closing_day_of_year", "label": "Closing Day of Year (Day 1 to 365)", "default": 182, "min": 1, "max": 365, "step": 1, "hint": "Day of year (e.g. July 1 = Day 182)"},
            {"id": "tax_status_prior_paid", "label": "Taxes Paid in Arrears (0 = Arrears, 1 = Paid in Advance)", "default": 0, "min": 0, "max": 1, "step": 1, "hint": "0 = Paid in arrears (standard); 1 = Paid in advance"}
        ],
        "metrics": [
            {"id": "proration_credit_result", "label": "Settlement Statement Proration", "default_display": "$3,092.60 Seller Credit to Buyer", "highlight": True},
            {"id": "daily_tax_per_diem", "label": "Daily Property Tax Per Diem", "default_display": "$16.99 / day", "highlight": True},
            {"id": "seller_days_owned", "label": "Seller Days of Ownership", "default_display": "182 days"},
            {"id": "buyer_days_owned", "label": "Buyer Remaining Days", "default_display": "183 days"}
        ],
        "proof_steps": [
            {"step_title": "Daily Per Diem Formulation", "step_text": "Daily Tax Rate = Annual Property Tax / 365 days = $6,200 / 365 = $16.9863/day."},
            {"step_title": "Ownership Allocation", "step_text": "The seller is legally responsible for taxes up to the day of closing (or day prior). 182 days × $16.9863 = $3,091.51."},
            {"step_title": "Arrears vs Advance Direction", "step_text": "When taxes are paid in arrears, the seller credits the buyer at closing because the buyer will pay the full tax bill at year-end."}
        ],
        "faqs": [
            {"q": "What does paying taxes 'in arrears' mean?", "a": "Taxes paid in arrears are billed at the end of the tax period for time already passed (common in most US states). At closing, the seller gives the buyer a cash credit for the portion of the year the seller occupied the home."},
            {"q": "What is the difference between a 360-day and 365-day proration?", "a": "A statutory 360-day proration treats every month as exactly 30 days (common in commercial lending). A 365-day calendar proration counts exact days."}
        ],
        "js_logic": """
          const tax = getNum('annual_tax_bill_total');
          const day = getNum('closing_day_of_year');
          const inAdvance = getNum('tax_status_prior_paid') === 1;

          const daily = tax / 365;
          const sellerDays = day;
          const buyerDays = 365 - day;
          const sellerShare = daily * sellerDays;
          const buyerShare = daily * buyerDays;

          let displayStr = '';
          if (inAdvance) {
            displayStr = '$' + buyerShare.toFixed(2) + ' Buyer Credit to Seller (Paid Ahead)';
          } else {
            displayStr = '$' + sellerShare.toFixed(2) + ' Seller Credit to Buyer (Paid in Arrears)';
          }

          setDisp('proration_credit_result', displayStr);
          setDisp('daily_tax_per_diem', '$' + daily.toFixed(2) + ' / day');
          setDisp('seller_days_owned', sellerDays + ' days');
          setDisp('buyer_days_owned', buyerDays + ' days');
        """
    },
    {
        "slug": "house-flip-profit",
        "category": "finance",
        "name": "House Flipping 70% Rule & MAO Calculator",
        "description": "Calculate Maximum Allowable Offer (MAO) for fix-and-flip real estate deals using the investor 70% rule, repair budgets, and holding costs.",
        "hero_badge": "Real Estate Wholesaling • 70% Rule Matrix",
        "formula_display": "MAO = (After Repair Value × 70%) - Estimated Repair Costs - Wholesale Fee",
        "fields": [
            {"id": "after_repair_value_arv", "label": "After Repair Value (ARV)", "default": 375000, "prefix": "$", "min": 25000, "max": 10000000, "step": 5000, "hint": "Appraised market value after full renovation"},
            {"id": "estimated_rehab_costs", "label": "Estimated Renovation & Rehab Budget", "default": 55000, "prefix": "$", "min": 2000, "max": 2000000, "step": 2500, "hint": "Labor, materials, permits, contingency"},
            {"id": "wholesale_assignment_fee", "label": "Wholesaler Assignment Fee (or Buffer)", "default": 10000, "prefix": "$", "min": 0, "max": 100000, "step": 1000, "hint": "Profit margin for wholesaler"},
            {"id": "target_profit_pct", "label": "Target Investor Margin Percentage", "default": 70, "suffix": "%", "min": 60, "max": 85, "step": 5, "hint": "70% Rule standard (allows 30% for profit & holding)"}
        ],
        "metrics": [
            {"id": "max_allowable_offer_mao", "label": "Maximum Allowable Offer (MAO)", "default_display": "$197,500.00", "highlight": True},
            {"id": "target_flipper_net_profit", "label": "Projected Flipper Net Profit (15%)", "default_display": "$56,250.00", "highlight": True},
            {"id": "carrying_closing_costs", "label": "Financing & Transaction Overhead (15%)", "default_display": "$56,250.00"},
            {"id": "purchase_to_arv_ratio", "label": "Purchase to ARV Discount", "default_display": "52.7% of ARV"}
        ],
        "proof_steps": [
            {"step_title": "The 70% Rule Core Mechanism", "step_text": "The 70% rule reserves 30% of ARV to cover two things: 1) Investor Net Profit (~15%) and 2) Transaction & Holding Costs (~15% for realtor commissions, closing fees, hard money interest)."},
            {"step_title": "Maximum Allowable Offer Formulation", "step_text": "MAO = (ARV × Rule%) - Rehab Costs - Wholesale Fee = ($375,000 × 0.70) - $55,000 - $10,000 = $197,500."},
            {"step_title": "Margin of Safety Protection", "step_text": "Sticking strictly to the 70% rule protects house flippers against unforeseen construction cost overruns or market price drops."}
        ],
        "faqs": [
            {"q": "What is the 70% rule in real estate?", "a": "The 70% rule states that an investor should pay no more than 70% of the property's After Repair Value (ARV) minus repair costs. It guarantees adequate profit margin after accounting for financing and resale commissions."},
            {"q": "Can you use the 70% rule in competitive high-price markets?", "a": "In expensive coastal markets (San Diego, Seattle), flippers often compress margins to a 75% or 80% rule because fixed percentage fees translate into higher absolute dollar profits on $1M+ homes."}
        ],
        "js_logic": """
          const arv = getNum('after_repair_value_arv');
          const rehab = getNum('estimated_rehab_costs');
          const fee = getNum('wholesale_assignment_fee');
          const rulePct = (getNum('target_profit_pct') || 70) / 100;

          const mao = Math.max(0, (arv * rulePct) - rehab - fee);
          const flipperProfit = arv * 0.15;
          const overhead = arv * (1 - rulePct);
          const ratio = arv > 0 ? (mao / arv) * 100 : 0;

          setDisp('max_allowable_offer_mao', '$' + Math.round(mao).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('target_flipper_net_profit', '$' + Math.round(flipperProfit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('carrying_closing_costs', '$' + Math.round(overhead).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('purchase_to_arv_ratio', ratio.toFixed(1) + '% of ARV');
        """
    },
    {
        "slug": "land-development-yield",
        "category": "finance",
        "name": "Land Subdivision & Development Lot Yield Calculator",
        "description": "Calculate residential subdivision lot yields, infrastructure loss deductions (roads, storm detention, wetlands), and residual land raw value.",
        "hero_badge": "Civil Engineering • Land Subdivision Matrix",
        "formula_display": "Net Buildable Area = Gross Acres × (1 - Infrastructure Loss %) | Lot Yield = Net Area / Minimum Lot Size",
        "fields": [
            {"id": "gross_parcel_acres", "label": "Gross Parcel Land Area (Acres)", "default": 25.0, "suffix": "acres", "min": 1.0, "max": 5000.0, "step": 0.5, "hint": "Total boundary deeded acreage"},
            {"id": "infrastructure_loss_pct", "label": "Infrastructure & Right-of-Way Loss (%)", "default": 22.0, "suffix": "%", "min": 5.0, "max": 45.0, "step": 1.0, "hint": "Roads, sidewalks, stormwater ponds, green space"},
            {"id": "min_lot_size_sqft", "label": "Zoning Minimum Lot Size (Sq Ft)", "default": 8500, "suffix": "sq ft", "min": 1000, "max": 200000, "step": 250, "hint": "Municipal minimum zoning requirement"},
            {"id": "finished_lot_sale_price", "label": "Finished Finished Lot Market Price", "default": 95000, "prefix": "$", "min": 10000, "max": 1500000, "step": 5000, "hint": "Price homebuilder pays per paper/finished lot"}
        ],
        "metrics": [
            {"id": "total_buildable_lots", "label": "Estimated Buildable Lot Yield", "default_display": "99 Residential Lots", "highlight": True},
            {"id": "gross_subdivision_revenue", "label": "Gross Finished Lot Revenue", "default_display": "$9,405,000.00", "highlight": True},
            {"id": "net_buildable_acres", "label": "Net Usable Buildable Land", "default_display": "19.50 acres (849,420 sq ft)"},
            {"id": "density_yield_per_acre", "label": "Gross Density Yield", "default_display": "3.96 Lots / Gross Acre"}
        ],
        "proof_steps": [
            {"step_title": "Acre to Square Foot Conversion", "step_text": "One acre equals 43,560 square feet. Gross Square Footage = Gross Acres × 43,560."},
            {"step_title": "Infrastructure Efficiency Deduction", "step_text": "Subdivisions lose 18% to 28% of gross land to public road rights-of-way, stormwater detention basins, wetlands buffers, and open space mandates: Net Usable Area = Gross Sq Ft × (1 - Infrastructure Loss%)."},
            {"step_title": "Lot Yield Formulation", "step_text": "Estimated Lot Yield = floor(Net Usable Area / Minimum Lot Size). For 19.5 net acres: 849,420 sq ft / 8,500 sq ft = 99 finished single-family lots."}
        ],
        "faqs": [
            {"q": "What is the typical infrastructure loss percentage for land subdivisions?", "a": "Standard single-family subdivisions typically lose 20% to 25% of gross acreage to street rights-of-way, curbs, utility easements, and stormwater detention basins. Mountainous or wetland terrain can exceed 35%."},
            {"q": "What is the difference between paper lots and finished lots?", "a": "Paper lots are legally approved and platted on paper by the municipality, but have no physical roads or utilities. Finished lots are fully graded with asphalt roads, curbs, water, sewer, and electric stubs ready for home framing."}
        ],
        "js_logic": """
          const acres = getNum('gross_parcel_acres');
          const lossRate = (getNum('infrastructure_loss_pct') || 22.0) / 100;
          const lotSize = getNum('min_lot_size_sqft') || 8500;
          const lotPrice = getNum('finished_lot_sale_price');

          const grossSqFt = acres * 43560;
          const netSqFt = grossSqFt * (1 - lossRate);
          const netAcres = netSqFt / 43560;
          const lots = Math.floor(netSqFt / lotSize);
          const grossRev = lots * lotPrice;
          const density = acres > 0 ? (lots / acres) : 0;

          setDisp('total_buildable_lots', lots + ' Residential Lots');
          setDisp('gross_subdivision_revenue', '$' + Math.round(grossRev).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('net_buildable_acres', netAcres.toFixed(2) + ' acres (' + Math.round(netSqFt).toLocaleString() + ' sq ft)');
          setDisp('density_yield_per_acre', density.toFixed(2) + ' Lots / Gross Acre');
        """
    },
    {
        "slug": "self-storage-roi",
        "category": "finance",
        "name": "Self-Storage Facility Feasibility & Revenue Calculator",
        "description": "Calculate self-storage facility rental revenue, Net Rentable Square Footage (NRSF), unit mix rent optimization, and commercial valuation.",
        "hero_badge": "Commercial Feasibility • Self-Storage Matrix",
        "formula_display": "Annual Revenue = NRSF × Average Rent PSF × Economic Occupancy %",
        "fields": [
            {"id": "net_rentable_nrsf", "label": "Total Net Rentable Area (NRSF)", "default": 65000, "suffix": "NRSF", "min": 5000, "max": 350000, "step": 2500, "hint": "Square feet of rentable storage units"},
            {"id": "avg_rent_psf_month", "label": "Average Blended Rental Rate ($/SF/Mo)", "default": 1.45, "prefix": "$", "min": 0.50, "max": 5.00, "step": 0.05, "hint": "Blended rate across climate & non-climate units"},
            {"id": "economic_occupancy_pct", "label": "Projected Economic Occupancy", "default": 88, "suffix": "%", "min": 50, "max": 98, "step": 1, "hint": "Standard stabilized occupancy: 85-92%"},
            {"id": "operating_expense_ratio_pct", "label": "Operating Expense Ratio (OER %)", "default": 35, "suffix": "%", "min": 20, "max": 55, "step": 1, "hint": "Staff, software, taxes, insurance, utilities % of revenue"}
        ],
        "metrics": [
            {"id": "net_operating_income_noi", "label": "Projected Annual NOI", "default_display": "$648,154.00 / yr", "highlight": True},
            {"id": "facility_valuation_6cap", "label": "Asset Valuation at 6.25% Cap Rate", "default_display": "$10,370,464.00", "highlight": True},
            {"id": "gross_collected_revenue", "label": "Gross Collected Annual Revenue", "default_display": "$997,160.00 / yr"},
            {"id": "monthly_gross_collections", "label": "Average Monthly Operating Collections", "default_display": "$83,096.67 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Gross Rent Potential Realization", "step_text": "Gross Potential Revenue = NRSF × Rate PSF × 12 months. 65,000 × $1.45 × 12 = $1,131,000/yr."},
            {"step_title": "Economic Occupancy Collection", "step_text": "Collected Revenue = Gross Potential × Economic Occupancy% = $1,131,000 × 0.88 = $997,160/yr."},
            {"step_title": "Operating Expense Ratio (OER) Invariant", "step_text": "Self-storage boasts the lowest OER in commercial real estate (30-38% vs 45-55% for apartments). NOI = Revenue × (1 - OER%) = $997,160 × 0.65 = $648,154/yr."}
        ],
        "faqs": [
            {"q": "Why is self-storage considered a recession-resilient asset class?", "a": "Self-storage demand is driven by the '4 Ds': Death, Divorce, Downsizing, and Dislocation. In economic booms, people buy more items; in recessions, people downsize homes and store their possessions."},
            {"q": "What is the premium for climate-controlled storage units?", "a": "Climate-controlled units rent for a 20% to 35% premium over drive-up non-climate units while costing only 10% to 15% more to construct."}
        ],
        "js_logic": """
          const nrsf = getNum('net_rentable_nrsf');
          const rentPsf = getNum('avg_rent_psf_month');
          const occ = (getNum('economic_occupancy_pct') || 88) / 100;
          const oer = (getNum('operating_expense_ratio_pct') || 35) / 100;

          const grossPotential = nrsf * rentPsf * 12;
          const collected = grossPotential * occ;
          const opex = collected * oer;
          const noi = collected - opex;
          const capRate = 0.0625;
          const valuation = capRate > 0 ? (noi / capRate) : 0;

          setDisp('net_operating_income_noi', '$' + Math.round(noi).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('facility_valuation_6cap', '$' + Math.round(valuation).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('gross_collected_revenue', '$' + Math.round(collected).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('monthly_gross_collections', '$' + (collected / 12).toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "mobile-home-park",
        "category": "finance",
        "name": "Mobile Home Park (MHP) Lot Rent & Cap Rate Calculator",
        "description": "Calculate Mobile Home Park (MHP / Manufactured Housing) Net Operating Income (NOI), tenant-owned home (TOH) lot rents, and commercial valuation.",
        "hero_badge": "Affordable Housing • MHP Valuation Matrix",
        "formula_display": "NOI = (Occupied Lots × Lot Rent × 12) × (1 - Operating Expense Ratio %)",
        "fields": [
            {"id": "total_park_lots", "label": "Total Permitted Mobile Home Lots", "default": 85, "suffix": "lots", "min": 10, "max": 1000, "step": 5, "hint": "Total pad spaces in community"},
            {"id": "lot_occupancy_pct", "label": "Park Lot Occupancy Rate (%)", "default": 92, "suffix": "%", "min": 40, "max": 100, "step": 1, "hint": "Percentage of occupied pads"},
            {"id": "monthly_lot_rent_pad", "label": "Average Monthly Lot Rent per Pad", "default": 475, "prefix": "$", "min": 150, "max": 1500, "step": 25, "hint": "Pad rent only (excluding home rent)"},
            {"id": "utility_submetered_status", "label": "Utilities Submetered (0 = Master Metered 40% OER, 1 = Submetered 28% OER)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "Submetered parks shift water/sewer costs to tenants"}
        ],
        "metrics": [
            {"id": "annual_park_noi", "label": "Net Operating Income (NOI)", "default_display": "$320,860.00 / yr", "highlight": True},
            {"id": "park_valuation_result", "label": "Park Valuation at 7.0% Cap Rate", "default_display": "$4,583,714.00", "highlight": True},
            {"id": "price_per_pad_metric", "label": "Implied Price per Permitted Pad", "default_display": "$53,926.00 / pad"},
            {"id": "gross_annual_lot_collections", "label": "Gross Annual Lot Collections", "default_display": "$445,740.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Tenant-Owned Home (TOH) Business Model", "step_text": "In pure MHP investing, the park owner owns ONLY the dirt and utility infrastructure. Tenants own the mobile homes, eliminating all appliance, roofing, and interior maintenance liabilities."},
            {"step_title": "Gross Lot Rent Aggregation", "step_text": "Gross Annual Revenue = Total Pads × Occupancy% × Monthly Pad Rent × 12."},
            {"step_title": "Submetering Margin Expansion", "step_text": "Submetering city water and sewer to tenants reduces the Operating Expense Ratio from 40% down to 28-30%, adding hundreds of thousands of dollars directly to asset value."}
        ],
        "faqs": [
            {"q": "Why do mobile home parks have the lowest tenant turnover in real estate?", "a": "Moving a mobile home costs $5,000 to $10,000 in transport permits, teardown, and setup fees. Because homes are expensive to relocate, average tenant tenure in a well-managed MHP exceeds 10 to 15 years."},
            {"q": "Why are new mobile home parks almost never built?", "a": "Zoning restrictions. Municipalities almost universally refuse to grant new zoning permits for mobile home parks due to NIMBY opposition, making existing licensed parks grandfathered, non-replicable monopolies."}
        ],
        "js_logic": """
          const pads = getNum('total_park_lots');
          const occ = (getNum('lot_occupancy_pct') || 92) / 100;
          const rent = getNum('monthly_lot_rent_pad');
          const submetered = getNum('utility_submetered_status') === 1;

          const occupiedPads = Math.round(pads * occ);
          const grossAnnual = occupiedPads * rent * 12;
          const oer = submetered ? 0.28 : 0.40;
          const noi = grossAnnual * (1 - oer);
          const capRate = 0.07;
          const valuation = capRate > 0 ? (noi / capRate) : 0;
          const perPad = pads > 0 ? (valuation / pads) : 0;

          setDisp('annual_park_noi', '$' + Math.round(noi).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('park_valuation_result', '$' + Math.round(valuation).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('price_per_pad_metric', '$' + Math.round(perPad).toLocaleString() + ' / pad');
          setDisp('gross_annual_lot_collections', '$' + Math.round(grossAnnual).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
        """
    },
    {
        "slug": "mezzanine-debt",
        "category": "finance",
        "name": "Mezzanine Debt & Subordinated Financing Blended Cost Calculator",
        "description": "Calculate blended Weighted Average Cost of Capital (WACC) across senior mortgage debt, mezzanine subordinated debt, and sponsor equity.",
        "hero_badge": "Capital Stack Structuring • Mezzanine Debt Matrix",
        "formula_display": "Blended Rate = (Senior % × Senior APR) + (Mezz % × Mezz APR) + (Equity % × Equity Hurdle)",
        "fields": [
            {"id": "total_capital_stack", "label": "Total Project Capital Stack", "default": 20000000, "prefix": "$", "min": 1000000, "max": 500000000, "step": 500000, "hint": "Total acquisition or development cost"},
            {"id": "senior_debt_pct", "label": "Senior Debt LTV (%)", "default": 65, "suffix": "%", "min": 30, "max": 80, "step": 5, "hint": "First mortgage lender share"},
            {"id": "senior_debt_rate", "label": "Senior Debt Interest Rate (%)", "default": 6.5, "suffix": "%", "min": 3.0, "max": 12.0, "step": 0.25, "hint": "First mortgage APR"},
            {"id": "mezz_debt_pct", "label": "Mezzanine Subordinated Debt Share (%)", "default": 15, "suffix": "%", "min": 0, "max": 30, "step": 5, "hint": "Mezzanine debt bridging the gap"},
            {"id": "mezz_debt_rate", "label": "Mezzanine Debt Interest Coupon (%)", "default": 12.5, "suffix": "%", "min": 8.0, "max": 20.0, "step": 0.5, "hint": "Mezzanine coupon rate"}
        ],
        "metrics": [
            {"id": "blended_debt_rate", "label": "Blended Total Debt Cost (80% Leverage)", "default_display": "7.63% APR", "highlight": True},
            {"id": "total_annual_debt_service", "label": "Annual Combined Debt Service Outflow", "default_display": "$1,220,000.00 / yr", "highlight": True},
            {"id": "equity_required_dollar", "label": "Remaining Sponsor Equity Required", "default_display": "$4,000,000.00 (20.0%)", "highlight": True},
            {"id": "mezz_dollar_amount", "label": "Mezzanine Capital Funded", "default_display": "$3,000,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Capital Stack Tier Decomposition", "step_text": "Senior Debt (65% = $13M) + Mezzanine Debt (15% = $3M) + Equity (20% = $4M) = $20,000,000."},
            {"step_title": "Weighted Average Cost of Debt", "step_text": "Total Debt = 80%. Blended Rate = [(Senior Debt / Total Debt) × Senior Rate] + [(Mezz Debt / Total Debt) × Mezz Rate]. For example: (65/80 × 6.5%) + (15/80 × 12.5%) = 5.28% + 2.34% = 7.625%."},
            {"step_title": "Leverage Arbitrage", "step_text": "Mezzanine debt allows sponsors to minimize equity dilution while maintaining lower borrowing costs than raising expensive preferred equity."}
        ],
        "faqs": [
            {"q": "What is the difference between mezzanine debt and second mortgage debt?", "a": "A second mortgage holds a junior recorded lien against the physical real estate. Mezzanine debt does NOT hold a mortgage on the property; it holds a pledge of equity shares in the entity that owns the property, enabling faster foreclosure under the Uniform Commercial Code (UCC)."},
            {"q": "When do real estate developers use mezzanine financing?", "a": "When senior lenders limit loans to 60-65% LTV, but the developer does not want to raise dilutive outside equity. Mezzanine debt bridges the gap up to 80-85% LTV."}
        ],
        "js_logic": """
          const total = getNum('total_capital_stack');
          const sPct = (getNum('senior_debt_pct') || 65) / 100;
          const sRate = (getNum('senior_debt_rate') || 6.5) / 100;
          const mPct = (getNum('mezz_debt_pct') || 15) / 100;
          const mRate = (getNum('mezz_debt_rate') || 12.5) / 100;

          const eqPct = Math.max(0, 1 - (sPct + mPct));
          const seniorDol = total * sPct;
          const mezzDol = total * mPct;
          const eqDol = total * eqPct;

          const seniorInt = seniorDol * sRate;
          const mezzInt = mezzDol * mRate;
          const totalDebtService = seniorInt + mezzInt;
          const totalDebtDol = seniorDol + mezzDol;
          const blendedRate = totalDebtDol > 0 ? (totalDebtService / totalDebtDol) * 100 : 0;

          setDisp('blended_debt_rate', blendedRate.toFixed(2) + '% APR');
          setDisp('total_annual_debt_service', '$' + Math.round(totalDebtService).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('equity_required_dollar', '$' + Math.round(eqDol).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + (eqPct * 100).toFixed(1) + '%)');
          setDisp('mezz_dollar_amount', '$' + Math.round(mezzDol).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "hard-money-points",
        "category": "finance",
        "name": "Hard Money Loan Cost & Points Calculator",
        "description": "Calculate total financing fees, upfront origination points, monthly interest-only payments, and effective annualized APR on hard money bridge loans.",
        "hero_badge": "Private Lending • Hard Money APR Matrix",
        "formula_display": "Total Loan Cost = (Loan Amount × Points %) + (Monthly Interest × Term) + Underwriting/Doc Fees",
        "fields": [
            {"id": "hard_money_loan_amount", "label": "Hard Money Loan Principal Amount", "default": 280000, "prefix": "$", "min": 25000, "max": 10000000, "step": 10000, "hint": "Principal borrowed for acquisition + rehab"},
            {"id": "origination_points_charged", "label": "Origination Points Charged", "default": 2.5, "suffix": "points", "min": 0.5, "max": 6.0, "step": 0.5, "hint": "Upfront lender fee (1 point = 1% of loan)"},
            {"id": "interest_only_rate_pct", "label": "Annual Interest-Only Rate (APR %)", "default": 11.5, "suffix": "%", "min": 7.0, "max": 20.0, "step": 0.5, "hint": "Monthly interest payment rate"},
            {"id": "loan_duration_months", "label": "Loan Term Duration (Months)", "default": 6, "suffix": "months", "min": 1, "max": 36, "step": 1, "hint": "Months until loan payoff"}
        ],
        "metrics": [
            {"id": "total_cost_of_capital", "label": "Total Hard Money Financing Cost", "default_display": "$23,100.00", "highlight": True},
            {"id": "monthly_interest_only_pmt", "label": "Monthly Interest-Only Payment", "default_display": "$2,683.33 / mo", "highlight": True},
            {"id": "upfront_points_dollar", "label": "Upfront Points Fee Paid at Closing", "default_display": "$7,000.00 (2.5 points)", "highlight": True},
            {"id": "effective_annual_apr", "label": "Effective Annualized APR Yield", "default_display": "16.50% APR"}
        ],
        "proof_steps": [
            {"step_title": "Upfront Points Cash Deduction", "step_text": "Points Cost = Loan Amount × (Points / 100). For example: $280,000 × 2.5% = $7,000 deducted at closing table."},
            {"step_title": "Monthly Interest-Only Cash Outflow", "step_text": "Monthly Interest = (Loan Amount × Interest Rate%) / 12 = ($280,000 × 11.5%) / 12 = $2,683.33/mo."},
            {"step_title": "Effective Annualized APR Formulation", "step_text": "Because points are paid upfront over a short 6-month term, the effective annualized APR is significantly higher than the nominal coupon rate: Effective APR = 11.5% + (2.5% × 12 / 6) = 16.5%."}
        ],
        "faqs": [
            {"q": "What do hard money lenders look for during approval?", "a": "Unlike traditional mortgage banks that scrutinize personal tax returns and W-2 paystubs, hard money lenders focus on the asset's After Repair Value (ARV), the borrower's track record of successful flips, and sufficient equity cushion (typically 65-75% ARV limit)."},
            {"q": "Can hard money points be rolled into the loan balance?", "a": "Many hard money lenders allow points, processing fees, and even an interest reserve to be financed directly into the total loan balance, minimizing out-of-pocket cash required at closing."}
        ],
        "js_logic": """
          const loan = getNum('hard_money_loan_amount');
          const pts = (getNum('origination_points_charged') || 2.5) / 100;
          const apr = (getNum('interest_only_rate_pct') || 11.5) / 100;
          const term = getNum('loan_duration_months') || 6;

          const pointsDollar = loan * pts;
          const monthlyInt = (loan * apr) / 12;
          const totalInt = monthlyInt * term;
          const docFees = 0; // nominal
          const totalCost = pointsDollar + totalInt + docFees;
          const effApr = ((totalCost / loan) / (term / 12)) * 100;

          setDisp('total_cost_of_capital', '$' + Math.round(totalCost).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('monthly_interest_only_pmt', '$' + monthlyInt.toFixed(2) + ' / mo');
          setDisp('upfront_points_dollar', '$' + Math.round(pointsDollar).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' (' + (pts*100).toFixed(1) + ' pts)');
          setDisp('effective_annual_apr', effApr.toFixed(2) + '% APR');
        """
    },
    {
        "slug": "bridge-loan-interest",
        "category": "finance",
        "name": "Commercial Bridge Loan Interest Reserve Calculator",
        "description": "Calculate interest reserve escrows, floating SOFR spreads, and monthly carrying costs for commercial bridge loans during property repositioning.",
        "hero_badge": "Bridge Financing • Interest Reserve Matrix",
        "formula_display": "Interest Reserve = Monthly Interest Payment × Stabilization Months",
        "fields": [
            {"id": "bridge_facility_amount", "label": "Commercial Bridge Loan Commitment", "default": 5500000, "prefix": "$", "min": 250000, "max": 100000000, "step": 100000, "hint": "Total loan facility commitment"},
            {"id": "sofr_base_rate_pct", "label": "Underlying SOFR Benchmark Index (%)", "default": 5.25, "suffix": "%", "min": 1.0, "max": 10.0, "step": 0.25, "hint": "Current 30-day SOFR benchmark rate"},
            {"id": "lender_spread_bps", "label": "Lender Credit Spread (Basis Points)", "default": 375, "suffix": "bps", "min": 150, "max": 800, "step": 25, "hint": "Lender margin over SOFR (375 bps = 3.75%)"},
            {"id": "reserve_term_months", "label": "Interest Reserve Duration (Months)", "default": 18, "suffix": "months", "min": 6, "max": 36, "step": 3, "hint": "Months of interest held in lender escrow"}
        ],
        "metrics": [
            {"id": "total_interest_reserve_escrow", "label": "Required Interest Reserve Escrow", "default_display": "$742,500.00", "highlight": True},
            {"id": "floating_all_in_rate", "label": "Floating All-In Interest Rate", "default_display": "9.00% APR (SOFR + 375 bps)", "highlight": True},
            {"id": "monthly_debt_carrying_cost", "label": "Monthly Interest Carrying Cost", "default_display": "$41,250.00 / mo"},
            {"id": "reserve_share_of_loan", "label": "Interest Reserve Share of Facility", "default_display": "13.5% of Loan Amount"}
        ],
        "proof_steps": [
            {"step_title": "All-In Floating Rate Formula", "step_text": "All-In Rate = SOFR Index + (Spread Basis Points / 100). For example: 5.25% + (375 / 100)% = 9.00%."},
            {"step_title": "Monthly Interest Payment", "step_text": "Monthly Interest = (Facility Amount × All-In Rate) / 12 = ($5,500,000 × 9.0%) / 12 = $41,250/mo."},
            {"step_title": "Lender Reserve Holdback Escrow", "step_text": "Interest Reserve = Monthly Payment × Stabilization Term = $41,250 × 18 months = $742,500. The lender holds this cash in escrow to make interest payments while the property is renovated and re-tenanted."}
        ],
        "faqs": [
            {"q": "What happens if a property stabilizes before the interest reserve is exhausted?", "a": "Unused interest reserve funds are not kept by the lender. When the bridge loan is paid off through a permanent refinance or sale, any remaining balance in the interest reserve escrow reduces the final loan payoff balance dollar-for-dollar."},
            {"q": "What is an interest rate cap in commercial bridge lending?", "a": "Because bridge loans have floating interest rates, lenders mandate that borrowers purchase an Interest Rate Cap (derivative hedge) that sets a maximum ceiling on SOFR to protect against default during rate spikes."}
        ],
        "js_logic": """
          const loan = getNum('bridge_facility_amount');
          const sofr = (getNum('sofr_base_rate_pct') || 5.25) / 100;
          const spreadBps = getNum('lender_spread_bps');
          const term = getNum('reserve_term_months') || 18;

          const spread = spreadBps / 10000;
          const allInRate = sofr + spread;
          const monthlyInt = (loan * allInRate) / 12;
          const totalReserve = monthlyInt * term;
          const sharePct = loan > 0 ? (totalReserve / loan) * 100 : 0;

          setDisp('total_interest_reserve_escrow', '$' + Math.round(totalReserve).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('floating_all_in_rate', (allInRate * 100).toFixed(2) + '% APR (SOFR + ' + spreadBps + ' bps)');
          setDisp('monthly_debt_carrying_cost', '$' + monthlyInt.toFixed(2) + ' / mo');
          setDisp('reserve_share_of_loan', sharePct.toFixed(1) + '% of Loan Amount');
        """
    },
    {
        "slug": "opportunity-zone",
        "category": "finance",
        "name": "Qualified Opportunity Zone (QOZ) Tax Incentive Calculator",
        "description": "Calculate capital gains tax deferral and complete 10-year tax-free gain elimination on Qualified Opportunity Zone Fund (QOF) investments.",
        "hero_badge": "Tax Policy • Opportunity Zone Matrix",
        "formula_display": "10-Year QOZ Benefit = Permanent Zero Capital Gains Tax on All Fund Appreciation",
        "fields": [
            {"id": "reinvested_capital_gain", "label": "Rolled-Over Capital Gain Amount", "default": 500000, "prefix": "$", "min": 25000, "max": 50000000, "step": 25000, "hint": "Original capital gain invested into QOZ fund within 180 days"},
            {"id": "projected_fund_annual_return", "label": "Expected Fund Annual Return (%)", "default": 10.0, "suffix": "%", "min": 4.0, "max": 25.0, "step": 0.5, "hint": "Compound annual growth rate of QOZ fund"},
            {"id": "capital_gains_tax_rate_pct", "label": "Combined Capital Gains Tax Rate (%)", "default": 23.8, "suffix": "%", "min": 15.0, "max": 37.0, "step": 0.1, "hint": "20% federal + 3.8% NIIT (plus state if applicable)"}
        ],
        "metrics": [
            {"id": "tax_free_wealth_gain", "label": "10-Year Tax-Free Appreciation Created", "default_display": "$796,871.00", "highlight": True},
            {"id": "eliminated_exit_tax", "label": "Taxes Completely Eliminated at Exit", "default_display": "$189,655.00 Saved", "highlight": True},
            {"id": "future_fund_value_10yr", "label": "Total Portfolio Value after 10 Years", "default_display": "$1,296,871.00", "highlight": True},
            {"id": "initial_tax_deferred", "label": "Deferred Initial Gain Tax (Due 2026)", "default_display": "$119,000.00"}
        ],
        "proof_steps": [
            {"step_title": "180-Day Rollover Deferral", "step_text": "Eligible taxpayers can defer capital gains from stocks, crypto, or businesses by rolling the gain into a Qualified Opportunity Fund within 180 days."},
            {"step_title": "The 10-Year Permanent Step-Up to Fair Market Value", "step_text": "If the QOF investment is held for at least 10 years, the investor's tax basis steps up to 100% of Fair Market Value: ZERO federal or state capital gains tax is owed on all post-acquisition appreciation."},
            {"step_title": "Compound Wealth Creation", "step_text": "A $500,000 investment compounding at 10% for 10 years grows to $1,296,871. The $796,871 profit is 100% tax-free, saving $189,655 in cash taxes."}
        ],
        "faqs": [
            {"q": "What is the substantial improvement requirement for Opportunity Zone real estate?", "a": "A QOF purchasing an existing building must substantially improve it by investing an amount equal to or greater than the building's original purchase basis (excluding land) within 30 months of acquisition."},
            {"q": "Can you invest ordinary income into an Opportunity Zone fund?", "a": "You can invest ordinary income, but only capital gains qualify for the special tax deferral and tax-free 10-year appreciation benefits under IRC Section 1400Z-2."}
        ],
        "js_logic": """
          const gain = getNum('reinvested_capital_gain');
          const r = (getNum('projected_fund_annual_return') || 10.0) / 100;
          const taxRate = (getNum('capital_gains_tax_rate_pct') || 23.8) / 100;

          const futureVal = gain * Math.pow(1 + r, 10);
          const appreciation = futureVal - gain;
          const taxEliminated = appreciation * taxRate;
          const deferredInitTax = gain * taxRate;

          setDisp('tax_free_wealth_gain', '$' + Math.round(appreciation).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('eliminated_exit_tax', '$' + Math.round(taxEliminated).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Saved');
          setDisp('future_fund_value_10yr', '$' + Math.round(futureVal).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('initial_tax_deferred', '$' + Math.round(deferredInitTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "hoa-reserve-fund",
        "category": "finance",
        "name": "HOA Reserve Fund Adequacy & Percent Funded Calculator",
        "description": "Calculate Homeowners Association (HOA) or Condominium Reserve Fund Percent Funded metric, Fully Funded Balance (FFB), and special assessment insolvency risk.",
        "hero_badge": "Condo Governance • Reserve Fund Matrix",
        "formula_display": "Percent Funded % = (Current Reserve Bank Balance / Fully Funded Balance) × 100",
        "fields": [
            {"id": "current_reserve_balance", "label": "Current Reserve Bank Account Balance", "default": 285000, "prefix": "$", "min": 5000, "max": 25000000, "step": 10000, "hint": "Liquid cash in HOA reserve savings"},
            {"id": "fully_funded_balance_ffb", "label": "Actuarial Fully Funded Balance (FFB)", "default": 450000, "prefix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Target balance calculated in reserve study"},
            {"id": "total_condo_units", "label": "Total Units in Community", "default": 64, "min": 4, "max": 2000, "step": 1, "hint": "Total doors sharing reserve obligations"}
        ],
        "metrics": [
            {"id": "percent_funded_score", "label": "HOA Percent Funded", "default_display": "63.33%", "highlight": True},
            {"id": "reserve_health_category", "label": "Reserve Fund Health Classification", "default_display": "Fair (30% to 69% Funded)", "highlight": True},
            {"id": "total_reserve_deficit", "label": "Reserve Fund Capital Deficit", "default_display": "$165,000.00 Deficit"},
            {"id": "deficit_per_homeowner", "label": "Potential Special Assessment per Owner", "default_display": "$2,578.13 / owner"}
        ],
        "proof_steps": [
            {"step_title": "Fully Funded Balance (FFB) Actuarial Law", "step_text": "For each common asset (roof, elevator, pool), Fractional Depreciation = Current Age / Useful Life. Component FFB = Replacement Cost × Fractional Depreciation."},
            {"step_title": "National Reserve Study Benchmark", "step_text": "Percent Funded = (Actual Balance / FFB) × 100%. < 30% = Poor / Critical Special Assessment Risk; 30%–69% = Fair; 70%–100% = Strong / Low Risk."},
            {"step_title": "Homebuyer Mortgage Fannie Mae Guardrail", "step_text": "Following the Surfside condo collapse, Fannie Mae and Freddie Mac require HOAs to allocate at least 10% of annual budget to reserves, red-flagging underfunded communities."}
        ],
        "faqs": [
            {"q": "What happens if an HOA is less than 30% funded?", "a": "Communities with under 30% reserves face massive risk of sudden special assessments ($10,000 to $50,000+ per homeowner) when roofs, elevators, or balconies fail, often causing mortgage lenders to blacklist the building."},
            {"q": "What is an HOA special assessment?", "a": "A special assessment is an emergency mandatory lump-sum bill charged to all homeowners in addition to monthly dues when the reserve fund has insufficient cash to cover major capital repairs."}
        ],
        "js_logic": """
          const balance = getNum('current_reserve_balance');
          const ffb = getNum('fully_funded_balance_ffb') || 1;
          const units = getNum('total_condo_units') || 1;

          const pct = (balance / ffb) * 100;
          const deficit = Math.max(0, ffb - balance);
          const perOwner = deficit / units;

          let category = 'Fair (30% to 69% Funded)';
          if (pct < 30) category = 'Critical / Poor (< 30% Funded) - High Special Assessment Risk';
          else if (pct >= 70) category = 'Strong / Optimal (≥ 70% Funded) - Minimal Risk';

          setDisp('percent_funded_score', pct.toFixed(2) + '%');
          setDisp('reserve_health_category', category);
          setDisp('total_reserve_deficit', '$' + Math.round(deficit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' Deficit');
          setDisp('deficit_per_homeowner', '$' + perOwner.toFixed(2) + ' / owner');
        """
    },
    {
        "slug": "depreciation-recapture",
        "category": "finance",
        "name": "Section 1250 Depreciation Recapture Tax Calculator",
        "description": "Calculate IRS Section 1250 unrecaptured depreciation tax (25% rate) versus long-term capital gains tax upon commercial or rental property sale.",
        "hero_badge": "Tax Accounting • Section 1250 Matrix",
        "formula_display": "Total Tax = (Depreciation Deducted × 25%) + (Net Capital Gain × Capital Gains Rate)",
        "fields": [
            {"id": "property_net_sale_price", "label": "Property Net Sales Price (After Closing Costs)", "default": 950000, "prefix": "$", "min": 25000, "max": 100000000, "step": 25000, "hint": "Sale price minus brokerage and title fees"},
            {"id": "original_cost_basis_acq", "label": "Original Purchase Basis (Cost + Improvements)", "default": 600000, "prefix": "$", "min": 10000, "max": 100000000, "step": 25000, "hint": "Original purchase price plus capitalized capital improvements"},
            {"id": "total_depreciation_taken", "label": "Total Depreciation Claimed Over Ownership", "default": 145000, "prefix": "$", "min": 0, "max": 20000000, "step": 5000, "hint": "All straight-line and bonus depreciation deducted"},
            {"id": "federal_cap_gain_rate", "label": "Federal Long-Term Capital Gains Rate (%)", "default": 20.0, "suffix": "%", "min": 0.0, "max": 20.0, "step": 5.0, "hint": "0%, 15%, or 20% based on taxable income"}
        ],
        "metrics": [
            {"id": "total_tax_liability_sale", "label": "Total Federal Tax Liability on Sale", "default_display": "$106,250.00", "highlight": True},
            {"id": "depreciation_recapture_tax", "label": "Section 1250 Recapture Tax (25%)", "default_display": "$36,250.00", "highlight": True},
            {"id": "pure_capital_gains_tax", "label": "Long-Term Capital Gains Tax (20%)", "default_display": "$70,000.00", "highlight": True},
            {"id": "effective_tax_rate_on_gain", "label": "Blended Tax Rate on Total Profit", "default_display": "21.46%"}
        ],
        "proof_steps": [
            {"step_title": "Adjusted Basis Calculation", "step_text": "Adjusted Basis = Original Basis - Depreciation Claimed = $600,000 - $145,000 = $455,000."},
            {"step_title": "Two-Tier Profit Bifurcation", "step_text": "Total Taxable Gain = Net Sale Price - Adjusted Basis = $950,000 - $455,000 = $495,000. The first $145,000 represents prior depreciation deductions; the remaining $350,000 is pure asset appreciation."},
            {"step_title": "The Section 1250 Special 25% Rate", "step_text": "Unrecaptured Section 1250 depreciation is taxed at a maximum federal rate of 25%: $145,000 × 25% = $36,250. The remaining $350,000 capital gain is taxed at 20%: $350,000 × 20% = $70,000. Total Tax = $106,250."}
        ],
        "faqs": [
            {"q": "What happens if I never claimed depreciation on my tax returns?", "a": "You still owe depreciation recapture tax! The IRS code specifies that recapture tax applies to depreciation 'allowed or allowable.' If you failed to claim it, the IRS still taxes you on it upon sale unless you file Form 3115 to amend prior returns."},
            {"q": "How can I avoid paying depreciation recapture tax?", "a": "Execute a Section 1031 like-kind exchange into a replacement property, or hold the property until death, passing it to heirs with a stepped-up basis that erases all accumulated depreciation."}
        ],
        "js_logic": """
          const sale = getNum('property_net_sale_price');
          const orig = getNum('original_cost_basis_acq');
          const dep = getNum('total_depreciation_taken');
          const capRate = (getNum('federal_cap_gain_rate') || 20.0) / 100;

          const adjustedBasis = Math.max(0, orig - dep);
          const totalProfit = Math.max(0, sale - adjustedBasis);
          const recapturePortion = Math.min(totalProfit, dep);
          const pureGainPortion = Math.max(0, totalProfit - recapturePortion);

          const recaptureTax = recapturePortion * 0.25;
          const gainTax = pureGainPortion * capRate;
          const totalTax = recaptureTax + gainTax;
          const effectiveRate = totalProfit > 0 ? (totalTax / totalProfit) * 100 : 0;

          setDisp('total_tax_liability_sale', '$' + Math.round(totalTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('depreciation_recapture_tax', '$' + Math.round(recaptureTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('pure_capital_gains_tax', '$' + Math.round(gainTax).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('effective_tax_rate_on_gain', effectiveRate.toFixed(2) + '%');
        """
    },
    {
        "slug": "promoted-interest-carry",
        "category": "finance",
        "name": "Real Estate GP Promoted Interest (Carried Interest) Calculator",
        "description": "Calculate General Partner (GP) carried interest promote compensation across multi-tier IRR hurdles and equity waterfall agreements.",
        "hero_badge": "Private Equity Structuring • GP Promote Matrix",
        "formula_display": "GP Promote = Excess Distributable Profits Above Hurdle × Carried Interest %",
        "fields": [
            {"id": "deal_total_net_profit", "label": "Total Deal Net Cash Profit", "default": 3500000, "prefix": "$", "min": 100000, "max": 100000000, "step": 100000, "hint": "Total net cash profit generated across hold period"},
            {"id": "preferred_return_absorbed", "label": "Profits Paid to LP Preferred Return Hurdle", "default": 1400000, "prefix": "$", "min": 0, "max": 50000000, "step": 50000, "hint": "Profit absorbed by LP 8% preferred return"},
            {"id": "tier1_promote_pct", "label": "Tier 1 Promote Split (% to GP)", "default": 20, "suffix": "%", "min": 10, "max": 40, "step": 5, "hint": "GP promote share above pref (standard 20%)"},
            {"id": "gp_co_invest_equity_share", "label": "GP Co-Invest Equity Share (%)", "default": 5, "suffix": "%", "min": 1, "max": 25, "step": 1, "hint": "Sponsor's pro-rata equity investment"}
        ],
        "metrics": [
            {"id": "total_gp_earnings", "label": "Total GP Earnings (Promote + Equity)", "default_display": "$595,000.00", "highlight": True},
            {"id": "pure_promote_bonus", "label": "Pure Carried Interest Promote", "default_display": "$420,000.00", "highlight": True},
            {"id": "gp_pro_rata_equity_profit", "label": "GP Pro-Rata Equity Profit Share", "default_display": "$175,000.00"},
            {"id": "lp_net_profit_share", "label": "Limited Partner (LP) Net Profit", "default_display": "$2,905,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Preferred Return Priority Satisfaction", "step_text": "Before the GP earns a single dollar of promote, passive LPs receive their full preferred return hurdle ($1,400,000)."},
            {"step_title": "Excess Profit Carried Interest Promote", "step_text": "Excess Profit = Total Profit - Pref = $3,500,000 - $1,400,000 = $2,100,000. Pure GP Promote = $2,100,000 × 20% = $420,000."},
            {"step_title": "Total GP Value Realization", "step_text": "GP Total Income = Pro-Rata Equity Share (5% of $3.5M = $175,000) + Pure Promote ($420,000) = $595,000."}
        ],
        "faqs": [
            {"q": "What is Carried Interest (Promote) in private equity real estate?", "a": "Promote is a performance fee paid to the General Partner sponsor. It is a share of project profits (typically 20%) distributed above an agreed preferred return hurdle, incentivizing sponsors to outperform return targets."},
            {"q": "What is a clawback provision in a real estate waterfall?", "a": "A clawback clause mandates that if a sponsor takes promote payments in early years, but the deal ultimately underperforms over the full hold period, the sponsor must return excess promote to ensure LPs achieve their preferred return."}
        ],
        "js_logic": """
          const totalProfit = getNum('deal_total_net_profit');
          const pref = getNum('preferred_return_absorbed');
          const promoteRate = (getNum('tier1_promote_pct') || 20) / 100;
          const gpEqRate = (getNum('gp_co_invest_equity_share') || 5) / 100;

          const excess = Math.max(0, totalProfit - pref);
          const purePromote = excess * promoteRate;
          const gpEquityShare = totalProfit * gpEqRate;
          const totalGp = purePromote + gpEquityShare;
          const lpProfit = totalProfit - totalGp;

          setDisp('total_gp_earnings', '$' + Math.round(totalGp).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('pure_promote_bonus', '$' + Math.round(purePromote).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('gp_pro_rata_equity_profit', '$' + Math.round(gpEquityShare).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('lp_net_profit_share', '$' + Math.round(lpProfit).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "blended-mortgage-rate",
        "category": "finance",
        "name": "Blended Mortgage Interest Rate & Second Loan Calculator",
        "description": "Calculate effective blended interest rate combining a low-rate first mortgage with a Home Equity Loan, HELOC, or mezzanine second mortgage.",
        "hero_badge": "Debt Architecture • Blended APR Matrix",
        "formula_display": "Blended APR = [(First Balance × First Rate) + (Second Balance × Second Rate)] / Total Debt",
        "fields": [
            {"id": "first_mortgage_balance", "label": "Existing 1st Mortgage Balance", "default": 320000, "prefix": "$", "min": 10000, "max": 10000000, "step": 5000, "hint": "Low fixed-rate existing mortgage"},
            {"id": "first_mortgage_rate", "label": "1st Mortgage Interest Rate (%)", "default": 3.25, "suffix": "%", "min": 1.5, "max": 10.0, "step": 0.125, "hint": "Locked historical low interest rate"},
            {"id": "second_loan_balance", "label": "New 2nd Mortgage / HELOC / Cash-Out", "default": 80000, "prefix": "$", "min": 5000, "max": 5000000, "step": 5000, "hint": "Subordinate loan or home equity line"},
            {"id": "second_loan_rate", "label": "2nd Loan Interest Rate (%)", "default": 9.5, "suffix": "%", "min": 3.0, "max": 20.0, "step": 0.25, "hint": "Current higher market interest rate"}
        ],
        "metrics": [
            {"id": "blended_effective_apr", "label": "Effective Blended Interest Rate", "default_display": "4.50% APR", "highlight": True},
            {"id": "total_combined_debt", "label": "Total Combined Debt Balance", "default_display": "$400,000.00", "highlight": True},
            {"id": "annual_total_interest", "label": "Annual Combined Interest Expense", "default_display": "$18,000.00 / yr"},
            {"id": "refinance_decision_verdict", "label": "Cash-Out Refinance Comparison", "default_display": "Keep 1st + HELOC (Beats 6.8% Cash-Out Refinance)"}
        ],
        "proof_steps": [
            {"step_title": "Debt Balance Weighting", "step_text": "Total Debt = 1st Mortgage ($320,000) + 2nd Mortgage ($80,000) = $400,000. 1st Mortgage represents 80% of total debt; 2nd represents 20%."},
            {"step_title": "Blended Rate Equation", "step_text": "Blended APR = (0.80 × 3.25%) + (0.20 × 9.50%) = 2.60% + 1.90% = 4.50%."},
            {"step_title": "Preserving Low-Rate Primary Debt", "step_text": "Borrowing $80,000 at a steep 9.5% HELOC rate creates a blended rate of only 4.50%, far superior to refinancing the entire $400,000 at a current 6.8% cash-out mortgage rate."}
        ],
        "faqs": [
            {"q": "Why is keeping a low-rate first mortgage and taking a HELOC better than a cash-out refinance?", "a": "If you have a 3% mortgage, a cash-out refinance wipes out that 3% rate across your ENTIRE balance. Taking a 9% HELOC for only the incremental cash you need keeps your blended borrowing cost significantly lower."},
            {"q": "What is a wraparound mortgage?", "a": "A wraparound mortgage is a form of creative seller financing where the seller keeps their existing low-interest mortgage in place while extending a larger loan to the buyer at a higher rate, profiting from the spread between the two rates."}
        ],
        "js_logic": """
          const b1 = getNum('first_mortgage_balance');
          const r1 = (getNum('first_mortgage_rate') || 3.25) / 100;
          const b2 = getNum('second_loan_balance');
          const r2 = (getNum('second_loan_rate') || 9.5) / 100;

          const totalDebt = b1 + b2;
          const int1 = b1 * r1;
          const int2 = b2 * r2;
          const totalInt = int1 + int2;
          const blended = totalDebt > 0 ? (totalInt / totalDebt) * 100 : 0;

          let verdict = 'Keep 1st + HELOC (Beats current cash-out refi)';
          if (blended > 6.8) verdict = 'Consider Full Cash-Out Refinance if market rate is lower';

          setDisp('blended_effective_apr', blended.toFixed(2) + '% APR');
          setDisp('total_combined_debt', '$' + totalDebt.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setDisp('annual_total_interest', '$' + Math.round(totalInt).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('refinance_decision_verdict', verdict);
        """
    }
]
