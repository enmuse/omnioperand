"""
scripts/data_finance_2.py
Second batch of Finance & Wealth Calculators:
RMD, DRIP, FIRE, Social Security, Pension, CD, HYSA, Inflation, Rule of 72,
Stock Options/RSU, Crypto Tax, Capital Gains, Self-Employment Tax, Salary/Hourly, Commission, Break-Even, Margin/Markup.
"""

FINANCE_CALCULATORS_2 = [
    {
        "slug": "rmd",
        "category": "finance",
        "name": "Required Minimum Distribution (RMD) Calculator",
        "description": "Calculate IRS mandatory annual withdrawals from Traditional IRA and 401(k) accounts using the IRS Uniform Lifetime Table.",
        "hero_badge": "IRS Mandates • Uniform Lifetime Table",
        "formula_display": "RMD = Account Balance as of Dec 31 / IRS Distribution Period",
        "fields": [
            {"id": "account_balance", "label": "Traditional IRA / 401(k) Balance", "default": 650000, "prefix": "$", "min": 10000, "max": 10000000, "step": 10000, "hint": "Account balance on December 31 of prior year"},
            {"id": "owner_age", "label": "Account Owner Age", "default": 75, "suffix": "yrs", "min": 73, "max": 105, "step": 1, "hint": "Current age (RMD begins at age 73)"}
        ],
        "metrics": [
            {"id": "rmd_amount", "label": "Mandatory Annual RMD", "default_display": "$26,422.76", "highlight": True},
            {"id": "distribution_period", "label": "IRS Life Expectancy Factor", "default_display": "24.6 years"},
            {"id": "monthly_equivalent", "label": "Monthly Withdrawal Equivalent", "default_display": "$2,201.90"}
        ],
        "proof_steps": [
            {"step_title": "SECURE Act 2.0 Starting Age", "step_text": "RMDs commence at age 73 (rising to age 75 in 2033)."},
            {"step_title": "IRS Table Division", "step_text": "Annual RMD = Prior Dec 31 Balance / Distribution Factor (from IRS Pub 590-B Table III)."}
        ],
        "faqs": [
            {"q": "What is the penalty for failing to take an RMD?", "a": "Under SECURE 2.0, the excise penalty for missing an RMD is 25% of the undistributed amount (reduced to 10% if corrected in a timely manner)."}
        ],
        "js_logic": """
          const B = getNum('account_balance');
          const age = getNum('owner_age');
          // Uniform Lifetime table lookup
          const factors = {
            73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7, 77: 22.9, 78: 22.0, 79: 21.1,
            80: 20.2, 81: 19.4, 82: 18.5, 83: 17.7, 84: 16.8, 85: 16.0, 86: 15.2,
            87: 14.4, 88: 13.7, 89: 12.9, 90: 12.2, 95: 8.9, 100: 6.4
          };
          const factor = factors[age] || (26.5 - (age - 73) * 0.85);
          const rmd = factor > 0 ? B / factor : 0;

          setDisp('rmd_amount', '$' + rmd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
          setDisp('distribution_period', factor.toFixed(1) + ' years');
          setDisp('monthly_equivalent', '$' + (rmd / 12).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
        """
    },
    {
        "slug": "drip",
        "category": "finance",
        "name": "Dividend Reinvestment (DRIP) Calculator",
        "description": "Simulate exponential compounding through automatic dividend reinvestment (DRIP), dividend growth rates, and recurring cash contributions.",
        "hero_badge": "Equity Compounding • DRIP Engine",
        "formula_display": "Total Shares(t+1) = Shares(t) + [Dividends Paid / Share Price]",
        "fields": [
            {"id": "starting_principal", "label": "Initial Investment ($)", "default": 25000, "prefix": "$", "min": 1000, "max": 1000000, "step": 1000, "hint": "Starting portfolio balance"},
            {"id": "dividend_yield", "label": "Annual Dividend Yield (%)", "default": 4.2, "suffix": "%", "min": 0.5, "max": 15, "step": 0.1, "hint": "Starting annual dividend yield"},
            {"id": "dividend_growth", "label": "Annual Dividend Growth Rate (%)", "default": 6.5, "suffix": "%", "min": 0, "max": 20, "step": 0.5, "hint": "Annual rate at which dividends increase"},
            {"id": "share_price_appreciation", "label": "Annual Capital Appreciation (%)", "default": 5.0, "suffix": "%", "min": 0, "max": 20, "step": 0.5, "hint": "Stock price annual appreciation"},
            {"id": "holding_years", "label": "Investment Horizon (Years)", "default": 20, "suffix": "yrs", "min": 1, "max": 40, "step": 1, "hint": "Years of compounding"}
        ],
        "metrics": [
            {"id": "final_portfolio_value", "label": "Final Portfolio Balance", "default_display": "$182,450.00", "highlight": True},
            {"id": "annual_dividend_income", "label": "Final Annual Passive Income", "default_display": "$9,840.00"},
            {"id": "yield_on_cost", "label": "Yield on Cost (YoC)", "default_display": "39.4%"}
        ],
        "proof_steps": [
            {"step_title": "Share Accumulation Mechanism", "step_text": "Reinvesting dividends purchases incremental shares without capital transaction fees, increasing the share base that earns next quarter's dividend."},
            {"step_title": "Yield on Cost Multiplication", "step_text": "Yield on Cost = (Annual Dividend at Year t / Initial Investment) × 100%."}
        ],
        "faqs": [
            {"q": "What is Yield on Cost?", "a": "Yield on Cost (YoC) measures your current annual dividend income divided by your original dollar purchase basis, demonstrating how dividend growth dramatically multiplies income over time."}
        ],
        "js_logic": """
          let balance = getNum('starting_principal');
          const initP = balance;
          let yieldPct = getNum('dividend_yield') / 100;
          const divGrowth = getNum('dividend_growth') / 100;
          const capGrowth = getNum('share_price_appreciation') / 100;
          const yrs = getNum('holding_years');

          let annualDiv = 0;
          for (let y = 1; y <= yrs; y++) {
            annualDiv = balance * yieldPct;
            balance = (balance + annualDiv) * (1 + capGrowth);
            yieldPct = yieldPct * (1 + divGrowth);
          }
          const yoc = initP > 0 ? (annualDiv / initP) * 100 : 0;

          setDisp('final_portfolio_value', '$' + Math.round(balance).toLocaleString());
          setDisp('annual_dividend_income', '$' + Math.round(annualDiv).toLocaleString());
          setDisp('yield_on_cost', yoc.toFixed(1) + '%');
        """
    },
    {
        "slug": "fire",
        "category": "finance",
        "name": "FIRE Calculator (Financial Independence, Retire Early)",
        "description": "Calculate your exact FIRE Number, Lean/Fat FIRE targets, and time to complete financial freedom using Trinity Study safe withdrawal rates.",
        "hero_badge": "Financial Independence • 4% Rule",
        "formula_display": "FIRE Number = Annual Living Expenses / Safe Withdrawal Rate (e.g. Expenses × 25)",
        "fields": [
            {"id": "annual_expenses", "label": "Annual Living Expenses", "default": 60000, "prefix": "$", "min": 10000, "max": 500000, "step": 2500, "hint": "Target retirement spending per year"},
            {"id": "current_net_worth", "label": "Current Invested Net Worth", "default": 180000, "prefix": "$", "min": 0, "max": 5000000, "step": 10000, "hint": "Current liquid investable assets"},
            {"id": "annual_savings", "label": "Annual Savings Contribution", "default": 35000, "prefix": "$", "min": 0, "max": 300000, "step": 2500, "hint": "Total saved and invested per year"},
            {"id": "swr_pct", "label": "Safe Withdrawal Rate (%)", "default": 4.0, "suffix": "%", "min": 3.0, "max": 5.0, "step": 0.25, "hint": "4% standard (Trinity study); 3.25%-3.5% for early retirees"},
            {"id": "real_return", "label": "Inflation-Adjusted Real Return (%)", "default": 6.5, "suffix": "%", "min": 3, "max": 10, "step": 0.5, "hint": "Real return after subtracting inflation"}
        ],
        "metrics": [
            {"id": "fire_number", "label": "Target FIRE Nest Egg", "default_display": "$1,500,000.00", "highlight": True},
            {"id": "years_to_fire", "label": "Timeline to Financial Freedom", "default_display": "14.2 years"},
            {"id": "lean_fire", "label": "Lean FIRE (75% Expenses)", "default_display": "$1,125,000.00"}
        ],
        "proof_steps": [
            {"step_title": "The Trinity Study 4% Invariant", "step_text": "FIRE Target = Expenses / SWR. Under a 4.0% SWR, Target = Expenses × 25. Under a conservative 3.33% SWR, Target = Expenses × 30."},
            {"step_title": "Logarithmic Annuity Inversion", "step_text": "Solving FV = PV(1 + r)ⁿ + PMT · [((1 + r)ⁿ - 1) / r] for n yields the exact years to reach financial independence."}
        ],
        "faqs": [
            {"q": "What is the 4% rule?", "a": "The 4% rule comes from the 1998 Trinity Study, proving that a portfolio invested in 50/50 to 75/25 stocks and bonds has a 95%+ probability of surviving a 30-year retirement without depletion when withdrawing 4% initially and adjusting for inflation annually."}
        ],
        "js_logic": """
          const exp = getNum('annual_expenses');
          const swr = getNum('swr_pct') / 100;
          const fireNum = swr > 0 ? exp / swr : 0;
          const pv = getNum('current_net_worth');
          const pmt = getNum('annual_savings');
          const r = getNum('real_return') / 100;

          let bal = pv;
          let yrs = 0;
          while (bal < fireNum && yrs < 80) {
            bal = bal * (1 + r) + pmt;
            yrs++;
          }

          setDisp('fire_number', '$' + Math.round(fireNum).toLocaleString());
          setDisp('lean_fire', '$' + Math.round(fireNum * 0.75).toLocaleString());
          setDisp('years_to_fire', yrs < 80 ? yrs + ' years' : '80+ years');
        """
    },
    {
        "slug": "social-security",
        "category": "finance",
        "name": "Social Security Benefit & Age Optimizer",
        "description": "Determine your optimal Social Security claiming age (62 vs 67 vs 70), breakeven life expectancy, and lifetime benefit maximization.",
        "hero_badge": "Actuarial Retirement • Social Security",
        "formula_display": "Monthly Benefit = PIA × (1 ± Actuarial Adjustment Factor)",
        "fields": [
            {"id": "pia_amount", "label": "Full Retirement Primary Insurance (PIA)", "default": 2400, "prefix": "$", "min": 500, "max": 4500, "step": 50, "hint": "Estimated benefit at Full Retirement Age (67)"},
            {"id": "claiming_age", "label": "Selected Claiming Age", "default": 67, "suffix": "yrs", "min": 62, "max": 70, "step": 1, "hint": "Age you plan to start benefits"}
        ],
        "metrics": [
            {"id": "monthly_benefit", "label": "Monthly Benefit Received", "default_display": "$2,400.00", "highlight": True},
            {"id": "age_62_benefit", "label": "Early Benefit at Age 62 (-30%)", "default_display": "$1,680.00"},
            {"id": "age_70_benefit", "label": "Delayed Benefit at Age 70 (+24%)", "default_display": "$2,976.00"},
            {"id": "breakeven_age", "label": "Breakeven Life Expectancy", "default_display": "80.4 years"}
        ],
        "proof_steps": [
            {"step_title": "Early Claiming Reduction (Age 62-66)", "step_text": "Claiming early at age 62 reduces your PIA by 30% permanently (5/9 of 1% per month for first 36 months + 5/12 of 1% for remaining)."},
            {"step_title": "Delayed Retirement Credits (Age 67-70)", "step_text": "Delaying past FRA yields an 8.0% guaranteed real increase per year up to age 70 (max +24%)."}
        ],
        "faqs": [
            {"q": "At what age should I take Social Security?", "a": "If you expect to live past age 80 or have other retirement assets, delaying until age 70 maximizes both your monthly cash flow and cumulative lifetime benefits."}
        ],
        "js_logic": """
          const pia = getNum('pia_amount');
          const age = getNum('claiming_age');
          let factor = 1.0;
          if (age < 67) {
            factor = 1.0 - (67 - age) * 0.06;
          } else if (age > 67) {
            factor = 1.0 + (age - 67) * 0.08;
          }

          setDisp('monthly_benefit', '$' + Math.round(pia * factor).toLocaleString());
          setDisp('age_62_benefit', '$' + Math.round(pia * 0.70).toLocaleString());
          setDisp('age_70_benefit', '$' + Math.round(pia * 1.24).toLocaleString());
        """
    },
    {
        "slug": "pension-vs-lump-sum",
        "category": "finance",
        "name": "Pension Annuity vs Lump Sum Calculator",
        "description": "Evaluate defined benefit pension options. Determine the internal rate of return (IRR) required to beat a lifetime pension annuity with a lump sum rollover.",
        "hero_badge": "Actuarial Science • Pension Decisions",
        "formula_display": "Required Hurdle Rate = Internal Rate of Return (IRR) Equating Lump Sum to Annuity",
        "fields": [
            {"id": "monthly_pension", "label": "Monthly Lifetime Pension Annuity", "default": 2800, "prefix": "$", "min": 200, "max": 25000, "step": 100, "hint": "Single life or joint-and-survivor monthly payout"},
            {"id": "lump_sum", "label": "Offered Lump Sum Buyout", "default": 420000, "prefix": "$", "min": 20000, "max": 3000000, "step": 10000, "hint": "One-time cash buyout offered by employer"},
            {"id": "life_expectancy_years", "label": "Expected Years in Retirement", "default": 25, "suffix": "yrs", "min": 10, "max": 40, "step": 1, "hint": "Actuarial life horizon"}
        ],
        "metrics": [
            {"id": "hurdle_rate", "label": "Required Hurdle Return Rate", "default_display": "6.35%", "highlight": True},
            {"id": "total_pension_collected", "label": "Cumulative Pension Payout", "default_display": "$840,000.00"},
            {"id": "recommendation", "label": "Actuarial Verdict", "default_display": "Annuity Favored (High Hurdle Rate)"}
        ],
        "proof_steps": [
            {"step_title": "Present Value Equivalence", "step_text": "PV_annuity = PMT · [1 - (1 + r)⁻ⁿ] / r. Solving for r establishes the hurdle return your portfolio must achieve net of fees to outperform the pension."}
        ],
        "faqs": [
            {"q": "What happens to a pension if the employer goes bankrupt?", "a": "In the United States, private defined benefit pensions are insured up to statutory maximum limits by the Pension Benefit Guaranty Corporation (PBGC)."}
        ],
        "js_logic": """
          const pmt = getNum('monthly_pension');
          const L = getNum('lump_sum');
          const yrs = getNum('life_expectancy_years');
          const totalPaid = pmt * 12 * yrs;

          // Binary search for hurdle rate
          let low = 0.001, high = 0.20, r = 0.05;
          for (let iter = 0; iter < 25; iter++) {
            r = (low + high) / 2;
            const rMo = r / 12;
            const nMo = yrs * 12;
            const pv = pmt * (1 - Math.pow(1 + rMo, -nMo)) / rMo;
            if (pv > L) low = r;
            else high = r;
          }

          setDisp('hurdle_rate', (r * 100).toFixed(2) + '%');
          setDisp('total_pension_collected', '$' + Math.round(totalPaid).toLocaleString());
          setDisp('recommendation', r > 0.065 ? 'Annuity Preferred (Hurdle > 6.5%)' : 'Lump Sum Feasible (Hurdle <= 6.5%)');
        """
    },
    {
        "slug": "cd-calculator",
        "category": "finance",
        "name": "Certificate of Deposit (CD) Calculator",
        "description": "Calculate Certificate of Deposit (CD) compounding yields, early withdrawal penalties, and fixed returns across terms from 3 months to 5 years.",
        "hero_badge": "Fixed Income • Compound Yield",
        "formula_display": "CD Balance = Principal · [1 + (APY / 100)]^(Months / 12)",
        "fields": [
            {"id": "cd_deposit", "label": "Initial CD Deposit", "default": 20000, "prefix": "$", "min": 500, "max": 1000000, "step": 1000, "hint": "Fixed principal deposit"},
            {"id": "cd_apy", "label": "Annual Percentage Yield (APY %)", "default": 4.85, "suffix": "%", "min": 0.5, "max": 12, "step": 0.05, "hint": "Locked APY"},
            {"id": "cd_term_months", "label": "CD Term (Months)", "default": 12, "suffix": "mo", "min": 3, "max": 60, "step": 3, "hint": "CD maturity duration"}
        ],
        "metrics": [
            {"id": "total_cd_interest", "label": "Total Interest Earned", "default_display": "$970.00", "highlight": True},
            {"id": "ending_cd_balance", "label": "Maturity Balance", "default_display": "$20,970.00"},
            {"id": "early_penalty", "label": "Est. Early Withdrawal Penalty (90 days)", "default_display": "$239.18"}
        ],
        "proof_steps": [
            {"step_title": "Compound Interest Formulation", "step_text": "FV = P · [1 + r/m]ᵐᵗ. APY expresses the effective annualized compounding return."}
        ],
        "faqs": [
            {"q": "Are CDs FDIC insured?", "a": "Yes! Deposits at FDIC-insured banks are protected up to $250,000 per depositor, per insured bank, for each account ownership category."}
        ],
        "js_logic": """
          const P = getNum('cd_deposit');
          const apy = getNum('cd_apy') / 100;
          const mos = getNum('cd_term_months');
          const fv = P * Math.pow(1 + apy, mos / 12);
          const intEarned = fv - P;
          const penalty90Days = (P * apy) * (90 / 365);

          setDisp('total_cd_interest', '$' + intEarned.toFixed(2));
          setDisp('ending_cd_balance', '$' + fv.toFixed(2));
          setDisp('early_penalty', '$' + penalty90Days.toFixed(2));
        """
    },
    {
        "slug": "hysa",
        "category": "finance",
        "name": "High-Yield Savings Account (HYSA) Calculator",
        "description": "Calculate compound growth in a High-Yield Savings Account with monthly deposits, daily interest accrual, and inflation comparisons.",
        "hero_badge": "Cash Management • Liquid Compounding",
        "formula_display": "Future Value = P(1 + r/365)³⁶⁵ᵗ + PMT · [((1 + r/12)¹²ᵗ - 1) / (r/12)]",
        "fields": [
            {"id": "hysa_principal", "label": "Initial Cash Deposit", "default": 15000, "prefix": "$", "min": 100, "max": 500000, "step": 500, "hint": "Starting savings balance"},
            {"id": "hysa_monthly", "label": "Monthly Contribution", "default": 400, "prefix": "$", "min": 0, "max": 10000, "step": 50, "hint": "Recurring monthly transfer"},
            {"id": "hysa_apy", "label": "HYSA APY (%)", "default": 4.50, "suffix": "%", "min": 0.5, "max": 10, "step": 0.1, "hint": "Annual Percentage Yield"},
            {"id": "hysa_years", "label": "Timeline (Years)", "default": 5, "suffix": "yrs", "min": 1, "max": 20, "step": 1, "hint": "Years of saving"}
        ],
        "metrics": [
            {"id": "hysa_final_balance", "label": "Total Savings Balance", "default_display": "$43,724.80", "highlight": True},
            {"id": "hysa_interest_earned", "label": "Total Compound Interest", "default_display": "$4,724.80"},
            {"id": "traditional_diff", "label": "Extra Interest vs Standard Bank (0.01%)", "default_display": "+$4,714.20"}
        ],
        "proof_steps": [
            {"step_title": "Daily Compounding Mechanics", "step_text": "HYSA accounts credit interest monthly but compound daily using: Effective Rate = (1 + APY)^(1/365) - 1."}
        ],
        "faqs": [
            {"q": "Can HYSA interest rates change?", "a": "Yes. HYSAs have variable interest rates tied to the Federal Reserve's Federal Funds Target Rate and can fluctuate up or down over time."}
        ],
        "js_logic": """
          const P = getNum('hysa_principal');
          const pmt = getNum('hysa_monthly');
          const apy = getNum('hysa_apy') / 100;
          const yrs = getNum('hysa_years');
          const mos = yrs * 12;
          const rMo = apy / 12;

          let bal = P;
          let totalContrib = P;
          for (let m = 1; m <= mos; m++) {
            bal = bal * (1 + rMo) + pmt;
            totalContrib += pmt;
          }
          const intEarned = bal - totalContrib;

          setDisp('hysa_final_balance', '$' + Math.round(bal).toLocaleString());
          setDisp('hysa_interest_earned', '$' + Math.round(intEarned).toLocaleString());
          setDisp('traditional_diff', '+$' + Math.round(intEarned * 0.99).toLocaleString());
        """
    },
    {
        "slug": "inflation",
        "category": "finance",
        "name": "Inflation & Purchasing Power Calculator",
        "description": "Calculate the erosion of purchasing power over time, future cost of living, and required future income based on CPI inflation rates.",
        "hero_badge": "Monetary Economics • Purchasing Power",
        "formula_display": "Future Cost = Present Cost · (1 + Inflation Rate)ⁿ",
        "fields": [
            {"id": "present_amount", "label": "Current Dollar Amount", "default": 100000, "prefix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Today's money"},
            {"id": "inflation_rate", "label": "Average Annual Inflation Rate (%)", "default": 3.2, "suffix": "%", "min": 1, "max": 15, "step": 0.1, "hint": "CPI inflation rate"},
            {"id": "horizon_years", "label": "Time Horizon (Years)", "default": 20, "suffix": "yrs", "min": 1, "max": 50, "step": 1, "hint": "Years into the future"}
        ],
        "metrics": [
            {"id": "future_cost_equivalent", "label": "Future Cost for Same Goods", "default_display": "$187,908.00", "highlight": True},
            {"id": "purchasing_power_loss", "label": "Purchasing Power Remaining", "default_display": "53.2% of original value"},
            {"id": "loss_in_value", "label": "Real Purchasing Power Loss", "default_display": "-$46,782.00"}
        ],
        "proof_steps": [
            {"step_title": "Exponential Purchasing Power Degradation", "step_text": "Purchasing Power Factor = 1 / (1 + i)ⁿ. At a 3.2% annual rate over 20 years, $1.00 degrades to $0.53."}
        ],
        "faqs": [
            {"q": "How can I protect my savings from inflation?", "a": "Holding assets with real pricing power—such as broad-market equity index funds, Treasury Inflation-Protected Securities (TIPS), and income-producing real estate—historically outpaces inflation."}
        ],
        "js_logic": """
          const P = getNum('present_amount');
          const i = getNum('inflation_rate') / 100;
          const n = getNum('horizon_years');
          const futureCost = P * Math.pow(1 + i, n);
          const powerPct = (1 / Math.pow(1 + i, n)) * 100;
          const powerDollar = P * (powerPct / 100);

          setDisp('future_cost_equivalent', '$' + Math.round(futureCost).toLocaleString());
          setDisp('purchasing_power_loss', powerPct.toFixed(1) + '% of original');
          setDisp('loss_in_value', '-$' + Math.round(P - powerDollar).toLocaleString());
        """
    },
    {
        "slug": "rule-of-72",
        "category": "finance",
        "name": "Rule of 72 Investment Doubling Calculator",
        "description": "Calculate exact and heuristic investment doubling periods using the logarithmic Rule of 72, Rule of 70, and Rule of 69.3.",
        "hero_badge": "Mental Math • Logarithmic Approximation",
        "formula_display": "Years to Double ≈ 72 / Interest Rate % (Exact: ln(2) / ln(1 + r))",
        "fields": [
            {"id": "interest_rate", "label": "Annual Interest Rate (%)", "default": 8.0, "suffix": "%", "min": 0.5, "max": 50, "step": 0.25, "hint": "Compound return rate"}
        ],
        "metrics": [
            {"id": "rule_72_years", "label": "Rule of 72 Doubling Time", "default_display": "9.00 years", "highlight": True},
            {"id": "exact_doubling_years", "label": "Exact Analytical Doubling Time", "default_display": "9.01 years"},
            {"id": "rule_70_years", "label": "Rule of 70 (Continuous)", "default_display": "8.75 years"}
        ],
        "proof_steps": [
            {"step_title": "Mathematical Derivation from Natural Logarithms", "step_text": "2P = P(1 + r)ⁿ ⟹ ln(2) = n · ln(1 + r) ⟹ n = ln(2) / ln(1 + r). For small r, ln(1 + r) ≈ r, and ln(2) ≈ 0.6931. Using 72 provides maximum integer divisibility."}
        ],
        "faqs": [
            {"q": "Why is 72 used instead of 69.3?", "a": "72 has many convenient divisors (1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36), making mental arithmetic effortless while matching annual discrete compounding closely."}
        ],
        "js_logic": """
          const r = getNum('interest_rate');
          const rule72 = r > 0 ? 72 / r : 0;
          const exact = r > 0 ? Math.log(2) / Math.log(1 + (r / 100)) : 0;
          const rule70 = r > 0 ? 70 / r : 0;

          setDisp('rule_72_years', rule72.toFixed(2) + ' years');
          setDisp('exact_doubling_years', exact.toFixed(2) + ' years');
          setDisp('rule_70_years', rule70.toFixed(2) + ' years');
        """
    },
    {
        "slug": "stock-option-rsu",
        "category": "finance",
        "name": "Stock Option & RSU Vesting Calculator",
        "description": "Calculate equity compensation value, vested shares, tax withholding, and net after-tax proceeds for RSUs, ISOs, and NSOs.",
        "hero_badge": "Equity Compensation • Tax Withholding",
        "formula_display": "Pre-Tax Value = Vested Shares × Market Price per Share",
        "fields": [
            {"id": "shares_granted", "label": "Total Shares Granted", "default": 4000, "suffix": "shares", "min": 100, "max": 1000000, "step": 100, "hint": "Total equity grant size"},
            {"id": "vested_pct", "label": "Vested Percentage (%)", "default": 50, "suffix": "%", "min": 0, "max": 100, "step": 5, "hint": "Vested portion based on schedule"},
            {"id": "stock_price", "label": "Current Stock Price ($)", "default": 85.00, "prefix": "$", "min": 1, "max": 5000, "step": 1, "hint": "Fair market value per share"},
            {"id": "tax_rate", "label": "Supplemental Tax Withholding (%)", "default": 37, "suffix": "%", "min": 20, "max": 55, "step": 1, "hint": "Federal + state tax rate on vested RSUs"}
        ],
        "metrics": [
            {"id": "net_payout", "label": "Net Take-Home Value", "default_display": "$107,100.00", "highlight": True},
            {"id": "pretax_value", "label": "Gross Pre-Tax Value", "default_display": "$170,000.00"},
            {"id": "tax_withheld", "label": "Estimated Tax Withheld", "default_display": "$62,900.00"}
        ],
        "proof_steps": [
            {"step_title": "RSU Ordinary Income Event", "step_text": "Upon vesting, RSUs are treated as supplemental W-2 earned income: Gross = Vested Shares × Stock Price. Taxes are automatically withheld by selling shares to cover."}
        ],
        "faqs": [
            {"q": "What happens if the stock price drops after my RSUs vest?", "a": "You owe taxes based on the fair market value on the exact day of vesting. If the stock drops subsequently, you realize a capital loss when selling, but your W-2 taxable compensation for the vesting year remains unchanged."}
        ],
        "js_logic": """
          const shares = getNum('shares_granted') * (getNum('vested_pct') / 100);
          const price = getNum('stock_price');
          const tax = getNum('tax_rate') / 100;
          const gross = shares * price;
          const taxAmt = gross * tax;
          const net = gross - taxAmt;

          setDisp('pretax_value', '$' + Math.round(gross).toLocaleString());
          setDisp('tax_withheld', '$' + Math.round(taxAmt).toLocaleString());
          setDisp('net_payout', '$' + Math.round(net).toLocaleString());
        """
    },
    {
        "slug": "crypto-profit-tax",
        "category": "finance",
        "name": "Crypto Profit & Capital Gains Tax Calculator",
        "description": "Calculate cryptocurrency trading profits, short-term vs long-term capital gains, and IRS tax liability using FIFO cost basis.",
        "hero_badge": "Digital Assets • Tax Accounting",
        "formula_display": "Capital Gain = Selling Price - Cost Basis - Transaction Fees",
        "fields": [
            {"id": "buy_price", "label": "Purchase Cost Basis per Coin", "default": 28000, "prefix": "$", "min": 0.01, "max": 200000, "step": 500, "hint": "Original buy price per token"},
            {"id": "sell_price", "label": "Selling Price per Coin", "default": 64000, "prefix": "$", "min": 0.01, "max": 200000, "step": 500, "hint": "Exit price per token"},
            {"id": "coin_quantity", "label": "Number of Coins", "default": 1.5, "suffix": "coins", "min": 0.001, "max": 1000000, "step": 0.1, "hint": "Tokens traded"},
            {"id": "holding_period", "label": "Tax Rate (%)", "default": 15, "suffix": "%", "min": 0, "max": 45, "step": 1, "hint": "15% Long-Term (held > 1 yr) or Ordinary Income Short-Term"}
        ],
        "metrics": [
            {"id": "net_profit", "label": "Net Profit After Tax", "default_display": "$45,900.00", "highlight": True},
            {"id": "gross_capital_gain", "label": "Gross Capital Gain", "default_display": "$54,000.00"},
            {"id": "tax_liability", "label": "Estimated Tax Liability", "default_display": "$8,100.00"}
        ],
        "proof_steps": [
            {"step_title": "IRS Property Classification", "step_text": "Under IRS Notice 2014-21, cryptocurrency is classified as property. Every trade, swap, or sale triggers a taxable realization event."}
        ],
        "faqs": [
            {"q": "Is swapping one crypto for another taxable?", "a": "Yes! Swapping Bitcoin for Ethereum or a stablecoin is treated by the IRS as selling Bitcoin at fair market value and immediately purchasing the second asset, triggering a capital gain or loss."}
        ],
        "js_logic": """
          const buy = getNum('buy_price');
          const sell = getNum('sell_price');
          const qty = getNum('coin_quantity');
          const taxPct = getNum('holding_period') / 100;
          const gain = (sell - buy) * qty;
          const tax = Math.max(0, gain * taxPct);
          const net = gain - tax;

          setDisp('gross_capital_gain', (gain >= 0 ? '$' : '-$') + Math.round(Math.abs(gain)).toLocaleString());
          setDisp('tax_liability', '$' + Math.round(tax).toLocaleString());
          setDisp('net_profit', (net >= 0 ? '$' : '-$') + Math.round(Math.abs(net)).toLocaleString());
        """
    },
    {
        "slug": "capital-gains-tax",
        "category": "finance",
        "name": "Capital Gains Tax Calculator",
        "description": "Calculate federal and state capital gains taxes on stocks, real estate, and collectibles with standard 0%, 15%, and 20% brackets.",
        "hero_badge": "Tax Optimization • Statutory Brackets",
        "formula_display": "Capital Gain = Sale Proceeds - Cost Basis",
        "fields": [
            {"id": "purchase_basis", "label": "Original Purchase Basis", "default": 40000, "prefix": "$", "min": 100, "max": 5000000, "step": 1000, "hint": "Initial cost + reinvested dividends"},
            {"id": "sale_proceeds", "label": "Total Sale Proceeds", "default": 95000, "prefix": "$", "min": 100, "max": 5000000, "step": 1000, "hint": "Gross sales proceeds"},
            {"id": "capital_tax_rate", "label": "Effective Capital Gains Rate (%)", "default": 15, "suffix": "%", "min": 0, "max": 35, "step": 1, "hint": "0%, 15%, or 20% + state taxes"}
        ],
        "metrics": [
            {"id": "after_tax_profit", "label": "After-Tax Net Profit", "default_display": "$46,750.00", "highlight": True},
            {"id": "total_capital_gain", "label": "Total Realized Capital Gain", "default_display": "$55,000.00"},
            {"id": "tax_amount", "label": "Taxes Owed", "default_display": "$8,250.00"}
        ],
        "proof_steps": [
            {"step_title": "Realization Event", "step_text": "Taxable Gain = Proceeds - Adjusted Basis. Unsold unrealized gains incur zero tax liability."}
        ],
        "faqs": [
            {"q": "What qualifies for the 0% long-term capital gains tax rate?", "a": "Single filers with taxable income under $47,025 (or married filing jointly under $94,050 for 2024) qualify for a federal long-term capital gains tax rate of 0%."}
        ],
        "js_logic": """
          const basis = getNum('purchase_basis');
          const proceeds = getNum('sale_proceeds');
          const rate = getNum('capital_tax_rate') / 100;
          const gain = proceeds - basis;
          const tax = Math.max(0, gain * rate);
          const net = gain - tax;

          setDisp('total_capital_gain', '$' + Math.round(gain).toLocaleString());
          setDisp('tax_amount', '$' + Math.round(tax).toLocaleString());
          setDisp('after_tax_profit', '$' + Math.round(net).toLocaleString());
        """
    },
    {
        "slug": "self-employment-tax",
        "category": "finance",
        "name": "1099 Self-Employment Tax (SECA) Calculator",
        "description": "Calculate 15.3% self-employment tax (Social Security & Medicare), above-the-line 50% SE deduction, and quarterly estimated payments.",
        "hero_badge": "1099 Contracting • SECA Matrix",
        "formula_display": "SE Tax = Net Earnings × 92.35% × 15.3% (Social Security + Medicare)",
        "fields": [
            {"id": "gross_1099_income", "label": "Gross 1099 Contracting Income", "default": 95000, "prefix": "$", "min": 1000, "max": 1000000, "step": 2500, "hint": "Total freelance / business revenue"},
            {"id": "business_expenses", "label": "Annual Business Expenses", "default": 18000, "prefix": "$", "min": 0, "max": 500000, "step": 1000, "hint": "Valid Schedule C deductions"}
        ],
        "metrics": [
            {"id": "se_tax_total", "label": "Total Self-Employment Tax (15.3%)", "default_display": "$10,879.62", "highlight": True},
            {"id": "net_schedule_c", "label": "Net Schedule C Profit", "default_display": "$77,000.00"},
            {"id": "quarterly_estimate", "label": "Quarterly Estimated SE Payment", "default_display": "$2,719.91"},
            {"id": "tax_deduction_50", "label": "50% Above-the-Line Tax Deduction", "default_display": "$5,439.81"}
        ],
        "proof_steps": [
            {"step_title": "Net Self-Employment Earnings", "step_text": "Net Earnings = Gross Revenue - Allowable Business Expenses."},
            {"step_title": "The 92.35% Multiplier", "step_text": "IRS rules assess SECA tax on 92.35% of net profit (reflecting the employer portion deduction): Taxable SE Base = Net × 0.9235."},
            {"step_title": "15.3% SECA Tax Rate", "step_text": "Social Security (12.4% up to wage base) + Medicare (2.9% uncapped) = 15.3%."}
        ],
        "faqs": [
            {"q": "Can I deduct half of my self-employment tax?", "a": "Yes! You can deduct 50% of your total self-employment tax directly on Form 1040 Schedule 1 as an above-the-line deduction, reducing your adjusted gross income (AGI)."}
        ],
        "js_logic": """
          const gross = getNum('gross_1099_income');
          const exp = getNum('business_expenses');
          const net = Math.max(0, gross - exp);
          const seBase = net * 0.9235;
          const seTax = seBase * 0.153;
          const deduction = seTax * 0.50;
          const quarterly = seTax / 4;

          setDisp('net_schedule_c', '$' + Math.round(net).toLocaleString());
          setDisp('se_tax_total', '$' + seTax.toFixed(2));
          setDisp('quarterly_estimate', '$' + quarterly.toFixed(2));
          setDisp('tax_deduction_50', '$' + deduction.toFixed(2));
        """
    },
    {
        "slug": "salary-to-hourly",
        "category": "finance",
        "name": "Salary to Hourly Wage Calculator",
        "description": "Convert annual salary into equivalent hourly, daily, weekly, and bi-weekly wage rates based on standard 2,080 annual work hours.",
        "hero_badge": "Compensation • Wage Conversion",
        "formula_display": "Hourly Wage = Annual Salary / 2,080 Hours (40 hrs/wk × 52 weeks)",
        "fields": [
            {"id": "annual_salary", "label": "Annual Salary ($)", "default": 85000, "prefix": "$", "min": 10000, "max": 1000000, "step": 1000, "hint": "Base annual compensation"},
            {"id": "hours_per_week", "label": "Work Hours per Week", "default": 40, "suffix": "hrs", "min": 10, "max": 80, "step": 1, "hint": "Standard is 40 hours per week"},
            {"id": "paid_weeks", "label": "Paid Weeks per Year", "default": 52, "suffix": "wks", "min": 40, "max": 52, "step": 1, "hint": "52 weeks including paid time off"}
        ],
        "metrics": [
            {"id": "hourly_rate", "label": "Equivalent Hourly Wage", "default_display": "$40.87 / hr", "highlight": True},
            {"id": "weekly_rate", "label": "Weekly Pay", "default_display": "$1,634.62"},
            {"id": "biweekly_rate", "label": "Bi-Weekly Paycheck", "default_display": "$3,269.23"}
        ],
        "proof_steps": [
            {"step_title": "Standard Work Year Constant", "step_text": "Annual Hours = Hours_per_Week × Paid_Weeks. Standard: 40 × 52 = 2,080 hours."},
            {"step_title": "Direct Wage Resolution", "step_text": "Hourly Rate = Salary / Annual Hours."}
        ],
        "faqs": [
            {"q": "How many working hours are in a typical year?", "a": "A standard full-time employee working 40 hours per week works 2,080 total hours across 52 weeks in a calendar year."}
        ],
        "js_logic": """
          const salary = getNum('annual_salary');
          const hrsWk = getNum('hours_per_week');
          const wks = getNum('paid_weeks');
          const totalHrs = hrsWk * wks;
          const hourly = totalHrs > 0 ? salary / totalHrs : 0;

          setDisp('hourly_rate', '$' + hourly.toFixed(2) + ' / hr');
          setDisp('weekly_rate', '$' + (hourly * hrsWk).toFixed(2));
          setDisp('biweekly_rate', '$' + (hourly * hrsWk * 2).toFixed(2));
        """
    },
    {
        "slug": "hourly-to-salary",
        "category": "finance",
        "name": "Hourly to Salary Wage Calculator",
        "description": "Convert hourly pay into gross annual salary, accounting for overtime hours at 1.5x time-and-a-half rates.",
        "hero_badge": "Payroll Math • Overtime Invariant",
        "formula_display": "Annual Salary = (Base Hourly × 2,080) + (Overtime Hours × 1.5 × Hourly × 52)",
        "fields": [
            {"id": "hourly_pay", "label": "Base Hourly Wage", "default": 32.50, "prefix": "$", "min": 7.25, "max": 300, "step": 0.50, "hint": "Hourly pay rate"},
            {"id": "base_hours", "label": "Regular Hours / Week", "default": 40, "suffix": "hrs", "min": 1, "max": 40, "step": 1, "hint": "Regular hours up to 40"},
            {"id": "overtime_hours", "label": "Overtime Hours / Week", "default": 5, "suffix": "hrs", "min": 0, "max": 40, "step": 1, "hint": "Overtime hours at 1.5x pay"}
        ],
        "metrics": [
            {"id": "gross_annual_salary", "label": "Total Gross Annual Salary", "default_display": "$80,275.00", "highlight": True},
            {"id": "regular_annual_pay", "label": "Base Regular Pay", "default_display": "$67,600.00"},
            {"id": "overtime_annual_pay", "label": "Annual Overtime Premium", "default_display": "$12,675.00"}
        ],
        "proof_steps": [
            {"step_title": "FLSA Overtime Multiplier", "step_text": "The Fair Labor Standards Act requires 1.5x pay for hours worked over 40 in a workweek: OT_Rate = Base × 1.5."},
            {"step_title": "Total Annual Compensation", "step_text": "Annual = (Regular_Hrs × Base × 52) + (OT_Hrs × Base × 1.5 × 52)."}
        ],
        "faqs": [
            {"q": "Does paid time off count toward overtime hours?", "a": "Under federal law, only actual hours physically worked count toward the 40-hour overtime threshold; vacation, sick, and holiday hours are excluded."}
        ],
        "js_logic": """
          const base = getNum('hourly_pay');
          const regHrs = getNum('base_hours');
          const otHrs = getNum('overtime_hours');
          const regAnnual = regHrs * base * 52;
          const otAnnual = otHrs * (base * 1.5) * 52;
          const total = regAnnual + otAnnual;

          setDisp('gross_annual_salary', '$' + Math.round(total).toLocaleString());
          setDisp('regular_annual_pay', '$' + Math.round(regAnnual).toLocaleString());
          setDisp('overtime_annual_pay', '$' + Math.round(otAnnual).toLocaleString());
        """
    },
    {
        "slug": "commission",
        "category": "finance",
        "name": "Sales Commission & Quota Calculator",
        "description": "Calculate tiered sales commission payouts, accelerated accelerator tiers, and On-Target Earnings (OTE) achievement.",
        "hero_badge": "Sales Compensation • Tier Accelerators",
        "formula_display": "Total Payout = Base Salary + (Base Commission) + (Accelerated Over-Quota Commission)",
        "fields": [
            {"id": "sales_volume", "label": "Total Closed Sales Revenue", "default": 180000, "prefix": "$", "min": 0, "max": 5000000, "step": 5000, "hint": "Total gross revenue closed"},
            {"id": "quota_target", "label": "Quarterly Sales Quota", "default": 150000, "prefix": "$", "min": 10000, "max": 5000000, "step": 5000, "hint": "Target sales quota"},
            {"id": "base_commission_rate", "label": "Base Commission Rate (%)", "default": 10, "suffix": "%", "min": 1, "max": 40, "step": 0.5, "hint": "Commission up to 100% of quota"},
            {"id": "accelerator_rate", "label": "Accelerator Rate (Over 100%)", "default": 15, "suffix": "%", "min": 1, "max": 50, "step": 0.5, "hint": "Commission rate for sales exceeding quota"}
        ],
        "metrics": [
            {"id": "total_commission", "label": "Total Commission Payout", "default_display": "$19,500.00", "highlight": True},
            {"id": "quota_attainment", "label": "Quota Attainment", "default_display": "120.0%"},
            {"id": "accelerated_bonus", "label": "Accelerator Earnings", "default_display": "$4,500.00"}
        ],
        "proof_steps": [
            {"step_title": "Attainment Percentage", "step_text": "Attainment = (Sales Volume / Quota Target) × 100%."},
            {"step_title": "Tiered Accelerators", "step_text": "Sales up to quota are paid at the base rate. Sales above quota are multiplied by the enhanced accelerator rate."}
        ],
        "faqs": [
            {"q": "What is an accelerator in sales compensation?", "a": "An accelerator is a higher commission percentage awarded to sales representatives for revenue generated beyond 100% of their assigned quota, rewarding top performers."}
        ],
        "js_logic": """
          const sales = getNum('sales_volume');
          const quota = getNum('quota_target');
          const rBase = getNum('base_commission_rate') / 100;
          const rAccel = getNum('accelerator_rate') / 100;

          let commBase = 0;
          let commAccel = 0;
          if (sales <= quota) {
            commBase = sales * rBase;
          } else {
            commBase = quota * rBase;
            commAccel = (sales - quota) * rAccel;
          }
          const totalComm = commBase + commAccel;
          const attain = quota > 0 ? (sales / quota) * 100 : 0;

          setDisp('total_commission', '$' + Math.round(totalComm).toLocaleString());
          setDisp('quota_attainment', attain.toFixed(1) + '%');
          setDisp('accelerated_bonus', '$' + Math.round(commAccel).toLocaleString());
        """
    },
    {
        "slug": "break-even",
        "category": "finance",
        "name": "Break-Even Point Analysis Calculator",
        "description": "Calculate exact unit and revenue break-even points, contribution margins, and safety margins for commercial operations.",
        "hero_badge": "Corporate Finance • Breakeven Invariant",
        "formula_display": "Break-Even Units = Fixed Costs / (Price per Unit - Variable Cost per Unit)",
        "fields": [
            {"id": "fixed_costs", "label": "Total Fixed Costs", "default": 45000, "prefix": "$", "min": 1000, "max": 5000000, "step": 1000, "hint": "Rent, executive salaries, insurance, depreciation"},
            {"id": "price_per_unit", "label": "Sale Price per Unit", "default": 120, "prefix": "$", "min": 1, "max": 10000, "step": 5, "hint": "Selling price to customer"},
            {"id": "variable_cost_per_unit", "label": "Variable Cost per Unit", "default": 45, "prefix": "$", "min": 0.1, "max": 10000, "step": 1, "hint": "Materials, direct labor, packaging per unit"}
        ],
        "metrics": [
            {"id": "breakeven_units", "label": "Break-Even Units Required", "default_display": "600 units", "highlight": True},
            {"id": "breakeven_revenue", "label": "Break-Even Sales Revenue", "default_display": "$72,000.00"},
            {"id": "contribution_margin", "label": "Contribution Margin per Unit", "default_display": "$75.00 (62.5%)"}
        ],
        "proof_steps": [
            {"step_title": "Contribution Margin Derivation", "step_text": "Unit Contribution Margin CM = Price - Variable_Cost. CM Ratio = CM / Price."},
            {"step_title": "Break-Even Volume Invariant", "step_text": "At break-even, Total Revenue = Total Cost ⟹ Q × P = Fixed + Q × V ⟹ Q_be = Fixed / (P - V)."}
        ],
        "faqs": [
            {"q": "Why is the contribution margin important?", "a": "The contribution margin represents the incremental cash earned on each unit sale available to cover fixed operational overhead. Once fixed costs are covered, 100% of subsequent contribution margin drops straight to operating profit."}
        ],
        "js_logic": """
          const FC = getNum('fixed_costs');
          const P = getNum('price_per_unit');
          const VC = getNum('variable_cost_per_unit');
          const cm = P - VC;
          const beUnits = cm > 0 ? Math.ceil(FC / cm) : 0;
          const beRev = beUnits * P;
          const cmRatio = P > 0 ? (cm / P) * 100 : 0;

          setDisp('breakeven_units', beUnits.toLocaleString() + ' units');
          setDisp('breakeven_revenue', '$' + beRev.toLocaleString());
          setDisp('contribution_margin', '$' + cm.toFixed(2) + ' (' + cmRatio.toFixed(1) + '%)');
        """
    },
    {
        "slug": "margin-markup",
        "category": "finance",
        "name": "Margin vs Markup Multiplier Calculator",
        "description": "Convert between Gross Profit Margin and Markup percentage, calculate target selling prices, and eliminate pricing confusion.",
        "hero_badge": "Pricing Strategy • Margin-Markup Dual",
        "formula_display": "Margin % = Markup / (1 + Markup) vs Markup % = Margin / (1 - Margin)",
        "fields": [
            {"id": "item_cost", "label": "Cost of Goods Sold (COGS)", "default": 80, "prefix": "$", "min": 1, "max": 50000, "step": 5, "hint": "Wholesale or manufacturing cost"},
            {"id": "selling_price", "label": "Selling Price to Customer", "default": 125, "prefix": "$", "min": 1, "max": 100000, "step": 5, "hint": "Retail sales price"}
        ],
        "metrics": [
            {"id": "gross_margin_pct", "label": "Gross Profit Margin", "default_display": "36.00%", "highlight": True},
            {"id": "markup_pct", "label": "Markup on Cost", "default_display": "56.25%"},
            {"id": "gross_profit_dollars", "label": "Gross Profit ($)", "default_display": "$45.00"}
        ],
        "proof_steps": [
            {"step_title": "Mathematical Divergence", "step_text": "Margin = (Price - Cost) / Price. Markup = (Price - Cost) / Cost. Margin can never exceed 100%, whereas Markup can exceed 1,000%."}
        ],
        "faqs": [
            {"q": "What is the difference between margin and markup?", "a": "Margin measures profit as a percentage of the final selling price. Markup measures profit as a percentage of your original cost. A 50% markup equals a 33.3% margin."}
        ],
        "js_logic": """
          const cost = getNum('item_cost');
          const price = getNum('selling_price');
          const profit = price - cost;
          const margin = price > 0 ? (profit / price) * 100 : 0;
          const markup = cost > 0 ? (profit / cost) * 100 : 0;

          setDisp('gross_margin_pct', margin.toFixed(2) + '%');
          setDisp('markup_pct', markup.toFixed(2) + '%');
          setDisp('gross_profit_dollars', '$' + profit.toFixed(2));
        """
    }
]
