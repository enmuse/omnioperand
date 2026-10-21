"""
scripts/data_crypto_fintech.py
25 High-Value Digital Assets, DeFi, Cryptoeconomics & Web3 Quantitative Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

CRYPTO_CALCULATORS = [
    {
        "slug": "crypto-mining-profitability",
        "category": "crypto",
        "name": "Proof-of-Work Bitcoin Mining Profitability & Hash Rate Calculator",
        "description": "Calculate daily net profit, break-even electricity rate, and hardware payback for ASIC Bitcoin miners accounting for network difficulty and halving epochs.",
        "hero_badge": "Proof of Work • Mining Economics",
        "formula_display": "Daily BTC = (Hashrate in TH/s / Network Hashrate) × (Block Reward × 144 blocks/day) | Profit = Revenue - (kW × 24 × $/kWh)",
        "fields": [
            {"id": "asic_hashrate_ths", "label": "ASIC Miner Hashrate (TH/s)", "default": 140.0, "suffix": "TH/s", "min": 10, "max": 1000, "step": 5, "hint": "Nominal hash rate (e.g. Antminer S19 XP = 140 TH/s)"},
            {"id": "power_consumption_w", "label": "Miner Power Consumption (Watts)", "default": 3010, "suffix": "Watts", "min": 500, "max": 10000, "step": 50, "hint": "Wall plug electricity consumption"},
            {"id": "electricity_cost_kwh", "label": "Electricity Rate ($/kWh)", "default": 0.065, "prefix": "$", "min": 0.01, "max": 0.30, "step": 0.005, "hint": "All-in hosting or utility power rate"},
            {"id": "bitcoin_price_usd", "label": "Bitcoin Market Price ($)", "default": 65000, "prefix": "$", "min": 10000, "max": 500000, "step": 1000, "hint": "Current BTC spot price"},
            {"id": "network_hashrate_ehs", "label": "Total Network Hashrate (EH/s)", "default": 650, "suffix": "EH/s", "min": 100, "max": 2000, "step": 10, "hint": "Global Bitcoin network hash rate"}
        ],
        "metrics": [
            {"id": "daily_net_profit", "label": "Daily Net Profit (After Power)", "default_display": "$4.55 / day", "highlight": True},
            {"id": "monthly_net_profit", "label": "Estimated Monthly Profit", "default_display": "$136.50 / mo", "highlight": True},
            {"id": "daily_power_cost", "label": "Daily Electricity Expense", "default_display": "$4.70 / day"},
            {"id": "breakeven_power_cost", "label": "Shutdown Breakeven Power Cost", "default_display": "$0.128 / kWh"}
        ],
        "proof_steps": [
            {"step_title": "Daily BTC Block Share Formulation", "step_text": "Global Blocks = 144 blocks/day (10-min block time). Block Reward = 3.125 BTC post-halving. Total daily coins = 144 × 3.125 = 450 BTC."},
            {"step_title": "Miner Network Share", "step_text": "Share = 140 TH/s / (650 EH/s × 1,000,000 TH/EH) = 2.1538 × 10⁻⁷ of global network."},
            {"step_title": "Gross Daily Revenue", "step_text": "Daily BTC = 450 × 2.1538 × 10⁻⁷ = 0.00009692 BTC. At $65,000/BTC: Gross Revenue = $6.30/day."},
            {"step_title": "Electricity Outflow & Net Margin", "step_text": "Daily kWh = (3,010W × 24h) / 1000 = 72.24 kWh. Power Cost = 72.24 × $0.065 = $4.70/day. Net Daily Profit = $6.30 - $4.70 = $1.60/day."}
        ],
        "faqs": [
            {"q": "How does the Bitcoin Halving affect mining profitability?", "a": "Every 210,000 blocks (roughly every 4 years), the block subsidy cuts in half (from 6.25 BTC to 3.125 BTC in April 2024), cutting gross block reward revenue in half unless Bitcoin spot price doubles or transaction fees spike."},
            {"q": "What is the maximum electricity rate for profitable Bitcoin mining?", "a": "With modern high-efficiency hardware (20 J/TH), mining remains profitable only with power tariffs below $0.06 to $0.08/kWh. Retail rates ($0.14+) almost always generate negative operational cash flow."}
        ],
        "js_logic": """
          const th = getNum('asic_hashrate_ths');
          const watts = getNum('power_consumption_w');
          const pCost = getNum('electricity_cost_kwh');
          const btcPrice = getNum('bitcoin_price_usd');
          const netEh = getNum('network_hashrate_ehs') || 650;

          const totalNetTh = netEh * 1000000;
          const share = totalNetTh > 0 ? (th / totalNetTh) : 0;
          const dailyBtc = share * (144 * 3.125);
          const grossRev = dailyBtc * btcPrice;
          const dailyKwh = (watts * 24) / 1000;
          const powerExpense = dailyKwh * pCost;
          const netDaily = grossRev - powerExpense;
          const breakevenKwh = dailyKwh > 0 ? (grossRev / dailyKwh) : 0;

          setDisp('daily_net_profit', (netDaily >= 0 ? '$' : '-$') + Math.abs(netDaily).toFixed(2) + ' / day');
          setDisp('monthly_net_profit', (netDaily >= 0 ? '$' : '-$') + Math.abs(netDaily * 30).toFixed(2) + ' / mo');
          setDisp('daily_power_cost', '$' + powerExpense.toFixed(2) + ' / day');
          setDisp('breakeven_power_cost', '$' + breakevenKwh.toFixed(3) + ' / kWh');
        """
    },
    {
        "slug": "staking-rewards-apr-apy",
        "category": "crypto",
        "name": "Proof-of-Stake Validator Staking Yield (APR vs APY) Calculator",
        "description": "Calculate annual staking returns, validator commission deduction, and compound APY for Ethereum, Solana, Cosmos, and Avalanche proof-of-stake networks.",
        "hero_badge": "Proof of Stake • Validator Economics",
        "formula_display": "APY = (1 + [APR · (1 - Commission)] / n)ⁿ - 1 | Terminal Value = Principal × (1 + APY)ᵗ",
        "fields": [
            {"id": "staked_token_amount", "label": "Staked Token Quantity", "default": 32.0, "suffix": "Tokens (e.g. ETH)", "min": 0.1, "max": 100000, "step": 1, "hint": "Number of native tokens staked"},
            {"id": "token_price_usd", "label": "Token Market Price ($)", "default": 3200, "prefix": "$", "min": 0.1, "max": 100000, "step": 10, "hint": "Current spot exchange price"},
            {"id": "network_base_apr_pct", "label": "Network Gross Staking APR (%)", "default": 4.2, "suffix": "%", "min": 1.0, "max": 50.0, "step": 0.1, "hint": "Protocol emission rate plus MEV tips"},
            {"id": "validator_commission_pct", "label": "Validator / Pool Fee (%)", "default": 5.0, "suffix": "%", "min": 0, "max": 25, "step": 0.5, "hint": "Staking pool fee (e.g. Lido = 10%, Rocket Pool = 8%)"},
            {"id": "compounding_frequency", "label": "Reward Compounding (1=Annual, 12=Monthly, 365=Daily)", "default": 365, "min": 1, "max": 365, "step": 1, "hint": "Compounding frequency of restaked rewards"}
        ],
        "metrics": [
            {"id": "net_annual_apy_pct", "label": "Net Effective APY", "default_display": "4.07%", "highlight": True},
            {"id": "annual_dollar_earnings", "label": "Annual Staking Yield ($ USD)", "default_display": "$4,168.00 / yr", "highlight": True},
            {"id": "annual_token_rewards", "label": "Tokens Earned Per Year", "default_display": "1.30 Tokens"},
            {"id": "commission_paid_usd", "label": "Validator Fee Paid", "default_display": "$219.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Net APR Commission Haircut", "step_text": "Net APR = Gross APR × (1 - Commission% / 100) = 4.2% × (1 - 0.05) = 3.99%."},
            {"step_title": "Continuous Daily Compounding APY", "step_text": "APY = (1 + 0.0399 / 365)³⁶⁵ - 1 = (1.0001093)³⁶⁵ - 1 = 4.070%."},
            {"step_title": "Nominal Token Yield", "step_text": "Annual Token Growth = 32.0 ETH × 4.07% = 1.302 ETH earned per year."},
            {"step_title": "USD Value Realization", "step_text": "At $3,200/ETH: Capital Value = $102,400. Annual Staking Cash Flow = 1.302 × $3,200 = $4,168.00."}
        ],
        "faqs": [
            {"q": "What is the difference between APR and APY in crypto staking?", "a": "APR (Annual Percentage Rate) reflects the simple interest rate without reinvesting rewards. APY (Annual Percentage Yield) accounts for the compounding effect of restaking your earned rewards daily or weekly."},
            {"q": "What is the risk of slashing in Proof of Stake?", "a": "Slashing is a protocol penalty where a validator loses a portion of their staked capital (e.g. 1 ETH or more) for malicious actions such as double-signing blocks or prolonged unexcused downtime."}
        ],
        "js_logic": """
          const tokens = getNum('staked_token_amount');
          const price = getNum('token_price_usd');
          const grossApr = (getNum('network_base_apr_pct') || 4.2) / 100;
          const comm = (getNum('validator_commission_pct') || 5.0) / 100;
          const n = Math.round(getNum('compounding_frequency')) || 365;

          const netApr = grossApr * (1 - comm);
          const apy = Math.pow(1 + (netApr / n), n) - 1;
          const annualTokens = tokens * apy;
          const annualUsd = annualTokens * price;
          const grossAnnualUsd = (tokens * grossApr) * price;
          const commPaid = grossAnnualUsd - annualUsd;

          setDisp('net_annual_apy_pct', (apy * 100).toFixed(2) + '%');
          setDisp('annual_dollar_earnings', '$' + Math.round(annualUsd).toLocaleString() + ' / yr');
          setDisp('annual_token_rewards', annualTokens.toFixed(3) + ' Tokens');
          setDisp('commission_paid_usd', '$' + Math.round(Math.max(0, commPaid)).toLocaleString() + ' / yr');
        """
    },
    {
        "slug": "impermanent-loss-amm",
        "category": "crypto",
        "name": "Automated Market Maker (AMM) Impermanent Loss Calculator",
        "description": "Calculate exact impermanent loss (IL) for liquidity providers on Uniswap, SushiSwap, and PancakeSwap constant-product (x·y=k) pools.",
        "hero_badge": "DeFi • AMM Mathematics",
        "formula_display": "IL = 2 · √k / (1 + k) - 1 | where k = Price Ratio (P_new / P_initial)",
        "fields": [
            {"id": "initial_deposit_usd", "label": "Initial Liquidity Deposit ($ USD)", "default": 10000, "prefix": "$", "min": 100, "max": 1000000, "step": 500, "hint": "Total 50/50 token pair value deposited into pool"},
            {"id": "price_change_ratio", "label": "Price Multiplier of Token A relative to B (k)", "default": 2.0, "suffix": "x (e.g. 2x = 100% gain)", "min": 0.05, "max": 20.0, "step": 0.1, "hint": "Relative price shift between pool assets"}
        ],
        "metrics": [
            {"id": "impermanent_loss_pct", "label": "Impermanent Loss Percentage", "default_display": "-5.72%", "highlight": True},
            {"id": "current_pool_value", "label": "Current Value in AMM Pool", "default_display": "$13,333.33", "highlight": True},
            {"id": "hodl_value_usd", "label": "Value If Held (HODL Strategy)", "default_display": "$14,142.14"},
            {"id": "net_dollar_divergence", "label": "Opportunity Cost Lost to Arbitrage", "default_display": "-$808.81"}
        ],
        "proof_steps": [
            {"step_title": "Constant Product Invariant", "step_text": "AMM invariant x · y = k requires rebalancing as relative price changes. Price ratio k = P_new / P_initial = 2.0."},
            {"step_title": "Analytical Impermanent Loss Derivation", "step_text": "IL = [2 · √k / (1 + k)] - 1. For k = 2.0: 2 · √2 / (1 + 2) - 1 = (2 · 1.41421 / 3) - 1 = 0.9428 - 1 = -0.05719 (-5.72%)."},
            {"step_title": "HODL Benchmark Valuation", "step_text": "If held in a private wallet: Value = $5,000 in Token B + $5,000 × 2.0 in Token A = $15,000 total."},
            {"step_title": "Arbitrage Drain Reconciliation", "step_text": "AMM Pool Value = HODL Value × (1 + IL) = $15,000 × (1 - 0.0572) = $14,142.14. Arbitrageurs drained $857.86 from the pool."}
        ],
        "faqs": [
            {"q": "When does impermanent loss become permanent?", "a": "Impermanent loss is only theoretical while you stay in the pool. It becomes permanently realized the moment you withdraw your liquidity tokens and swap back to cash."},
            {"q": "Can fee yields overcome impermanent loss?", "a": "Yes! If the trading volume in the pool generates swap fee earnings (e.g. +12% APR) that exceed the impermanent loss (-5.7%), the liquidity provider achieves positive net alpha over holding."}
        ],
        "js_logic": """
          const deposit = getNum('initial_deposit_usd');
          const k = Math.max(0.01, getNum('price_change_ratio') || 2.0);

          const sqrtK = Math.sqrt(k);
          const ilFraction = (2 * sqrtK) / (1 + k) - 1;
          const ilPct = ilFraction * 100;

          const half = deposit / 2;
          const hodlVal = half + (half * k);
          const poolVal = hodlVal * (1 + ilFraction);
          const dollarLoss = poolVal - hodlVal;

          setDisp('impermanent_loss_pct', ilPct.toFixed(2) + '%');
          setDisp('current_pool_value', '$' + Math.round(poolVal).toLocaleString());
          setDisp('hodl_value_usd', '$' + Math.round(hodlVal).toLocaleString());
          setDisp('net_dollar_divergence', '-$' + Math.abs(Math.round(dollarLoss)).toLocaleString());
        """
    },
    {
        "slug": "liquidity-pool-fee-yield",
        "category": "crypto",
        "name": "Liquidity Pool Swap Fee APR & LP Capital Efficiency Calculator",
        "description": "Calculate annual fee income, daily fee yield, and capital efficiency for liquidity providers on Uniswap v2, v3 (concentrated liquidity), and Curve pools.",
        "hero_badge": "DeFi • Fee Monetization",
        "formula_display": "Fee APR (%) = (Daily Pool Volume × Swap Fee Tier × 365) / Total Value Locked (TVL)",
        "fields": [
            {"id": "lp_deposit_usd", "label": "Your LP Position Value ($)", "default": 5000, "prefix": "$", "min": 50, "max": 500000, "step": 250, "hint": "Your capital deposited into the pool"},
            {"id": "pool_tvl_usd", "label": "Total Pool TVL ($)", "default": 2500000, "prefix": "$", "min": 10000, "max": 100000000, "step": 50000, "hint": "Total Value Locked across all providers in this pool"},
            {"id": "daily_trading_vol_usd", "label": "24h Trading Volume ($)", "default": 1200000, "prefix": "$", "min": 1000, "max": 50000000, "step": 25000, "hint": "24-hour pool swap volume"},
            {"id": "pool_fee_tier_pct", "label": "Pool Fee Tier (%)", "default": 0.30, "suffix": "%", "min": 0.01, "max": 1.0, "step": 0.01, "hint": "Uniswap fee tiers: 0.01%, 0.05%, 0.30%, 1.00%"}
        ],
        "metrics": [
            {"id": "lp_fee_apr_pct", "label": "Annual Swap Fee APR", "default_display": "52.56%", "highlight": True},
            {"id": "daily_fee_income_usd", "label": "Your Estimated Daily Fee Income", "default_display": "$7.20 / day", "highlight": True},
            {"id": "monthly_fee_income_usd", "label": "Your Estimated Monthly Income", "default_display": "$216.00 / mo"},
            {"id": "pool_turnover_ratio", "label": "Daily Capital Turnover Velocity", "default_display": "0.48x Daily Volume / TVL"}
        ],
        "proof_steps": [
            {"step_title": "Daily Pool Fee Generation", "step_text": "Total Daily Fees = Daily Volume × Fee Tier% = $1,200,000 × 0.30% = $3,600.00 daily fees collected."},
            {"step_title": "LP Ownership Share", "step_text": "Share = Your Deposit / Total TVL = $5,000 / $2,500,000 = 0.0020 (0.20% pool share)."},
            {"step_title": "Daily LP Earnings", "step_text": "Daily Earnings = $3,600 × 0.0020 = $7.20 per day."},
            {"step_title": "Annualized APR Yield", "step_text": "Annual Income = $7.20 × 365 = $2,628.00. Fee APR = $2,628 / $5,000 = 52.56%."}
        ],
        "faqs": [
            {"q": "How does Uniswap v3 concentrated liquidity increase fee APR?", "a": "Uniswap v3 allows LPs to concentrate capital within custom price bounds (e.g. ±5%), achieving 10x to 50x higher capital efficiency and earning the same fees with a fraction of the capital."},
            {"q": "What is the optimal fee tier for stablecoin pairs?", "a": "Stablecoin pairs (USDC/USDT, DAI/USDC) trade at ultra-low price volatility, making the 0.01% or 0.05% tier standard to attract massive multi-million dollar institutional volume."}
        ],
        "js_logic": """
          const myDeposit = getNum('lp_deposit_usd');
          const tvl = getNum('pool_tvl_usd');
          const vol = getNum('daily_trading_vol_usd');
          const feeTier = (getNum('pool_fee_tier_pct') || 0.30) / 100;

          const totalDailyFees = vol * feeTier;
          const share = tvl > 0 ? (myDeposit / tvl) : 0;
          const myDailyFees = totalDailyFees * share;
          const myAnnualFees = myDailyFees * 365;
          const apr = myDeposit > 0 ? (myAnnualFees / myDeposit) * 100 : 0;
          const velocity = tvl > 0 ? (vol / tvl) : 0;

          setDisp('lp_fee_apr_pct', apr.toFixed(2) + '%');
          setDisp('daily_fee_income_usd', '$' + myDailyFees.toFixed(2) + ' / day');
          setDisp('monthly_fee_income_usd', '$' + (myDailyFees * 30).toFixed(2) + ' / mo');
          setDisp('pool_turnover_ratio', velocity.toFixed(2) + 'x Vol / TVL');
        """
    },
    {
        "slug": "futures-liquidation-price",
        "category": "crypto",
        "name": "Crypto Futures Liquidation Price & Maintenance Margin Calculator",
        "description": "Calculate exact liquidation price, margin call threshold, and distance to liquidation for isolated and cross-margin crypto perpetual contracts.",
        "hero_badge": "Derivatives • Liquidation Risk",
        "formula_display": "Long Liq Price = Entry Price · (1 - [1 / Leverage] + Maintenance Margin Rate)",
        "fields": [
            {"id": "entry_price_usd", "label": "Entry Price ($ USD)", "default": 65000, "prefix": "$", "min": 10, "max": 500000, "step": 500, "hint": "Order execution price"},
            {"id": "position_leverage", "label": "Leverage Multiplier (x)", "default": 10, "suffix": "x", "min": 1, "max": 125, "step": 1, "hint": "5x, 10x, 20x, 50x, 100x leverage"},
            {"id": "position_direction", "label": "Position Direction (1 = Long, 2 = Short)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1 for Long (Buy), 2 for Short (Sell)"},
            {"id": "maintenance_margin_pct", "label": "Exchange Maintenance Margin Rate (%)", "default": 0.5, "suffix": "%", "min": 0.2, "max": 5.0, "step": 0.1, "hint": "Binance/Bybit tier maintenance margin (typically 0.4% - 1.0%)"}
        ],
        "metrics": [
            {"id": "liquidation_price_usd", "label": "Bankruptcy Liquidation Price", "default_display": "$58,825.00", "highlight": True},
            {"id": "price_drop_to_liquidation", "label": "Adverse Distance to Liquidation", "default_display": "-9.50% Drop", "highlight": True},
            {"id": "initial_margin_req_pct", "label": "Initial Margin Required", "default_display": "10.0% of Notional Value"},
            {"id": "risk_assessment", "label": "Position Volatility Safety Tier", "default_display": "High Leverage Risk"}
        ],
        "proof_steps": [
            {"step_title": "Initial Margin Fraction", "step_text": "Initial Margin IMR = 1 / Leverage = 1 / 10 = 10.0%."},
            {"step_title": "Long Liquidation Formula", "step_text": "P_liq = Entry × (1 - IMR + MMR). For $65,000 at 10x with 0.5% MMR: $65,000 × (1 - 0.10 + 0.005) = $65,000 × 0.905 = $58,825.00."},
            {"step_title": "Short Liquidation Inversion", "step_text": "For a Short position: P_liq = Entry × (1 + IMR - MMR) = $65,000 × (1 + 0.10 - 0.005) = $65,000 × 1.095 = $71,175.00."},
            {"step_title": "Distance to Wipeout", "step_text": "Distance = ($58,825 - $65,000) / $65,000 = -9.50%. A normal 10% market pullback liquidates 100% of collateral."}
        ],
        "faqs": [
            {"q": "What happens during a crypto futures liquidation?", "a": "When the mark price touches your liquidation price, the exchange's risk engine takes over the position, cancels open orders, closes the trade at the prevailing market price, and transfers your initial margin to the insurance fund."},
            {"q": "How does Maintenance Margin affect liquidation price?", "a": "Maintenance margin is the minimum collateral required to keep the position open. The higher the maintenance margin, the sooner liquidation triggers before your account balance hits true zero."}
        ],
        "js_logic": """
          const entry = getNum('entry_price_usd');
          const lev = Math.max(1, getNum('position_leverage') || 10);
          const isLong = Math.round(getNum('position_direction')) !== 2;
          const mmr = (getNum('maintenance_margin_pct') || 0.5) / 100;

          const imr = 1 / lev;
          let liq = 0;
          let dropPct = 0;

          if (isLong) {
            liq = entry * (1 - imr + mmr);
            dropPct = ((liq - entry) / entry) * 100;
          } else {
            liq = entry * (1 + imr - mmr);
            dropPct = ((liq - entry) / entry) * 100;
          }

          let risk = 'Conservative Leverage';
          if (lev >= 50) risk = 'Extreme Danger (Flash Crash Wipeout)';
          else if (lev >= 20) risk = 'High Leverage Volatility';
          else if (lev >= 10) risk = 'Moderate Margin Risk';

          setDisp('liquidation_price_usd', '$' + Math.round(liq).toLocaleString());
          setDisp('price_drop_to_liquidation', (dropPct > 0 ? '+' : '') + dropPct.toFixed(2) + '% Adverse Move');
          setDisp('initial_margin_req_pct', (imr * 100).toFixed(1) + '% Margin');
          setDisp('risk_assessment', risk);
        """
    },
    {
        "slug": "dollar-cost-averaging-dca",
        "category": "crypto",
        "name": "Crypto Dollar-Cost Averaging (DCA) Accumulation Calculator",
        "description": "Simulate historical and projected recurring cryptocurrency investments (weekly/monthly DCA) versus lump-sum investing to reduce timing risk.",
        "hero_badge": "Wealth Building • Systematic DCA",
        "formula_display": "Average Acquisition Cost = Total Capital Invested / Total Accumulated Tokens",
        "fields": [
            {"id": "recurring_investment_usd", "label": "Recurring Contribution Amount ($)", "default": 250, "prefix": "$", "min": 10, "max": 10000, "step": 25, "hint": "Periodic purchase amount"},
            {"id": "purchase_frequency", "label": "Purchase Frequency (1 = Weekly, 2 = Bi-Weekly, 3 = Monthly)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1: Weekly (52x/yr), 2: Bi-Weekly (26x/yr), 3: Monthly (12x/yr)"},
            {"id": "dca_duration_months", "label": "Investment Horizon (Months)", "default": 24, "suffix": "months", "min": 6, "max": 120, "step": 6, "hint": "Total duration of systematic DCA program"},
            {"id": "projected_annual_growth_pct", "label": "Projected Annual Asset CAGR (%)", "default": 35.0, "suffix": "%", "min": -20, "max": 200, "step": 5, "hint": "Expected compound annual capital appreciation"}
        ],
        "metrics": [
            {"id": "total_portfolio_value_usd", "label": "Projected Terminal Value", "default_display": "$38,420.00", "highlight": True},
            {"id": "total_capital_invested", "label": "Total Principal Invested", "default_display": "$26,000.00", "highlight": True},
            {"id": "net_profit_earned", "label": "Net Unrealized Profit", "default_display": "+$12,420.00 (+47.8%)"},
            {"id": "total_purchases_count", "label": "Number of Recurring Orders", "default_display": "104 Automatic Buys"}
        ],
        "proof_steps": [
            {"step_title": "Periodic Inflow Frequency", "step_text": "Weekly buys over 24 months = 104 contributions. Total Principal = 104 × $250 = $26,000.00."},
            {"step_title": "Future Value of Annuity Compounding", "step_text": "FV = PMT · [((1 + r)ⁿ - 1) / r]. With weekly rate r = (35% / 52) = 0.673%: Terminal Value = $38,420.00."},
            {"step_title": "Volatility Neutralization Benefit", "step_text": "DCA mechanically buys more tokens during market crashes and fewer tokens during market bubbles, eliminating emotional timing errors."}
        ],
        "faqs": [
            {"q": "Is Dollar-Cost Averaging better than Lump-Sum investing?", "a": "In pure upward-trending markets, lump-sum investing mathematically outperforms ~68% of the time. However, in hyper-volatile crypto markets, DCA drastically lowers emotional stress and protects against buying market cycle tops."},
            {"q": "What is the best frequency for crypto DCA?", "a": "Empirical backtests show minimal difference in long-term returns between daily, weekly, and monthly DCA. Weekly DCA is widely favored because it balances smooth dollar-cost averaging with manageable exchange transaction fees."}
        ],
        "js_logic": """
          const pmt = getNum('recurring_investment_usd');
          const freq = Math.round(getNum('purchase_frequency')) || 1;
          const months = getNum('dca_duration_months') || 24;
          const cagr = (getNum('projected_annual_growth_pct') || 35) / 100;

          let periodsPerYear = 52;
          if (freq === 2) periodsPerYear = 26;
          else if (freq === 3) periodsPerYear = 12;

          const totalPeriods = Math.round((months / 12) * periodsPerYear);
          const r = cagr / periodsPerYear;
          const totalInvested = pmt * totalPeriods;

          let fv = 0;
          if (r === 0) {
            fv = totalInvested;
          } else {
            fv = pmt * ((Math.pow(1 + r, totalPeriods) - 1) / r);
          }

          const profit = fv - totalInvested;
          const pct = totalInvested > 0 ? (profit / totalInvested) * 100 : 0;

          setDisp('total_portfolio_value_usd', '$' + Math.round(fv).toLocaleString());
          setDisp('total_capital_invested', '$' + Math.round(totalInvested).toLocaleString());
          setDisp('net_profit_earned', (profit >= 0 ? '+$' : '-$') + Math.abs(Math.round(profit)).toLocaleString() + ' (' + (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%)');
          setDisp('total_purchases_count', totalPeriods + ' Automatic Buys');
        """
    },
    {
        "slug": "gas-fee-gwei-usd",
        "category": "crypto",
        "name": "Ethereum Gas Fee Estimator (Gwei, EIP-1559 & USD Cost)",
        "description": "Calculate exact dollar transaction costs on Ethereum mainnet and L2 networks across simple transfers, ERC-20 transfers, and Uniswap smart contract swaps.",
        "hero_badge": "Ethereum • EIP-1559 Gas Economics",
        "formula_display": "Total Fee = Gas Units × (Base Fee + Priority Fee) in Gwei × (1 ETH / 10⁹ Gwei) × ETH Price",
        "fields": [
            {"id": "base_fee_gwei", "label": "Network Base Fee (Gwei)", "default": 24.0, "suffix": "Gwei", "min": 1, "max": 500, "step": 1, "hint": "Protocol algorithmic burn fee (EIP-1559)"},
            {"id": "priority_fee_gwei", "label": "Priority Tip to Validator (Gwei)", "default": 2.0, "suffix": "Gwei", "min": 0.5, "max": 50, "step": 0.5, "hint": "Miner / builder incentive tip"},
            {"id": "transaction_type", "label": "Transaction Complexity (1=ETH, 2=ERC20, 3=DEX Swap, 4=NFT Mint)", "default": 3, "min": 1, "max": 4, "step": 1, "hint": "1: 21k gas, 2: 65k gas, 3: 150k gas, 4: 180k gas"},
            {"id": "eth_market_price", "label": "ETH Market Price ($)", "default": 3200, "prefix": "$", "min": 500, "max": 25000, "step": 50, "hint": "Current ETH exchange price"}
        ],
        "metrics": [
            {"id": "total_tx_fee_usd", "label": "Estimated Transaction Cost", "default_display": "$12.48 USD", "highlight": True},
            {"id": "total_gas_units", "label": "Gas Units Consumed", "default_display": "150,000 Gas", "highlight": True},
            {"id": "eth_burned_amount", "label": "ETH Burned by Protocol", "default_display": "0.00360 ETH", "highlight": True},
            {"id": "effective_gwei_rate", "label": "Total Gas Price", "default_display": "26.0 Gwei"}
        ],
        "proof_steps": [
            {"step_title": "Effective Gas Price", "step_text": "Total Gwei = Base Fee (24.0) + Priority Tip (2.0) = 26.0 Gwei."},
            {"step_title": "EVM Gas Unit Allocation", "step_text": "DEX smart contract swaps (Uniswap v3) require ~150,000 gas units to execute routing, slippage checks, and token balance transfers."},
            {"step_title": "Ether Conversion", "step_text": "Fee in ETH = 150,000 units × 26.0 × 10⁻⁹ = 0.00390 ETH."},
            {"step_title": "Dollar Valuation", "step_text": "Dollar Fee = 0.00390 ETH × $3,200/ETH = $12.48. Under EIP-1559, 92.3% of this fee (0.00360 ETH = $11.52) is permanently burned from circulation."}
        ],
        "faqs": [
            {"q": "What is 1 Gwei in Ethereum?", "a": "1 Gwei (giga-wei) is 10⁻⁹ ETH (0.000000001 ETH). It is the standard denomination used to quote gas prices on the Ethereum network."},
            {"q": "Why do DEX swaps cost more gas than simple ETH transfers?", "a": "A simple native ETH transfer between two wallets requires exactly 21,000 gas units. A DEX swap executes multiple storage read/write operations, arithmetic validations, and token allowance updates across smart contracts, consuming 130,000 to 180,000 gas units."}
        ],
        "js_logic": """
          const base = getNum('base_fee_gwei');
          const tip = getNum('priority_fee_gwei');
          const tType = Math.round(getNum('transaction_type')) || 3;
          const ethPrice = getNum('eth_market_price');

          let gasUnits = 150000;
          if (tType === 1) gasUnits = 21000;
          else if (tType === 2) gasUnits = 65000;
          else if (tType === 3) gasUnits = 150000;
          else if (tType === 4) gasUnits = 180000;

          const totalGwei = base + tip;
          const feeEth = (gasUnits * totalGwei) / 1000000000;
          const feeUsd = feeEth * ethPrice;
          const burnEth = (gasUnits * base) / 1000000000;

          setDisp('total_tx_fee_usd', '$' + feeUsd.toFixed(2) + ' USD');
          setDisp('total_gas_units', gasUnits.toLocaleString() + ' Gas');
          setDisp('eth_burned_amount', burnEth.toFixed(5) + ' ETH');
          setDisp('effective_gwei_rate', totalGwei.toFixed(1) + ' Gwei');
        """
    },
    {
        "slug": "cdp-health-factor-ltv",
        "category": "crypto",
        "name": "Collateralized Debt Position (CDP) LTV & Liquidation Health Factor",
        "description": "Calculate Health Factor, Loan-to-Value (LTV), and collateral drop buffer before liquidation on MakerDAO (DAI), Aave, and Compound lending vaults.",
        "hero_badge": "DeFi Lending • Liquidation Health",
        "formula_display": "Health Factor = (Collateral Value × Liquidation Threshold) / Total Borrowed Debt",
        "fields": [
            {"id": "deposited_collateral_usd", "label": "Total Collateral Deposited ($ USD)", "default": 25000, "prefix": "$", "min": 500, "max": 5000000, "step": 500, "hint": "Market value of pledged collateral (e.g. ETH, WBTC)"},
            {"id": "borrowed_debt_usd", "label": "Total Borrowed Debt ($ USD)", "default": 12500, "prefix": "$", "min": 100, "max": 2500000, "step": 500, "hint": "Outstanding borrowed loan balance (e.g. USDC, DAI)"},
            {"id": "liquidation_threshold_pct", "label": "Protocol Liquidation Threshold (%)", "default": 82.5, "suffix": "%", "min": 50, "max": 95, "step": 0.5, "hint": "Maximum LTV before vault liquidation triggers (Aave ETH = 82.5%)"}
        ],
        "metrics": [
            {"id": "current_health_factor", "label": "Vault Health Factor (HF)", "default_display": "1.65", "highlight": True},
            {"id": "current_ltv_pct", "label": "Current Loan-to-Value (LTV)", "default_display": "50.0%", "highlight": True},
            {"id": "collateral_drop_tolerance", "label": "Collateral Price Drop to Liquidation", "default_display": "-39.4% Cushion", "highlight": True},
            {"id": "max_additional_borrow", "label": "Safe Additional Borrowing Capacity", "default_display": "$4,125.00"}
        ],
        "proof_steps": [
            {"step_title": "Loan-to-Value Ratio", "step_text": "LTV = Borrowed Debt / Collateral Value = $12,500 / $25,000 = 50.0%."},
            {"step_title": "Health Factor Derivation", "step_text": "HF = (Collateral × Liquidation Threshold%) / Debt = ($25,000 × 0.825) / $12,500 = $20,625 / $12,500 = 1.65."},
            {"step_title": "Liquidation Price Threshold", "step_text": "Liquidation triggers when HF < 1.0. Critical Collateral Value = Debt / Threshold = $12,500 / 0.825 = $15,151.52."},
            {"step_title": "Market Crash Safety Buffer", "step_text": "Allowable Drop = ($15,151.52 - $25,000) / $25,000 = -39.39%. Collateral can plummet by ~39% before liquidation bot liquidates the vault."}
        ],
        "faqs": [
            {"q": "What happens when a DeFi Health Factor drops below 1.0?", "a": "The instant Health Factor drops below 1.0, third-party liquidation bots repay up to 50% of your debt and seize your collateral at a discounted penalty (typically 5% to 10% liquidation bonus)."},
            {"q": "What is considered a safe Health Factor in DeFi lending?", "a": "Conservative DeFi practitioners maintain a Health Factor of 2.0 or higher (LTV ≤ 40%), providing enough cushion to withstand historic 50%+ single-day crypto market flash crashes."}
        ],
        "js_logic": """
          const col = getNum('deposited_collateral_usd');
          const debt = getNum('borrowed_debt_usd');
          const thresh = (getNum('liquidation_threshold_pct') || 82.5) / 100;

          const ltv = col > 0 ? (debt / col) * 100 : 0;
          const hf = debt > 0 ? (col * thresh) / debt : 99;
          const minCol = thresh > 0 ? (debt / thresh) : 0;
          const dropPct = col > 0 ? ((minCol - col) / col) * 100 : 0;
          const maxBorrowSafe = Math.max(0, (col * thresh * 0.8) - debt);

          setDisp('current_health_factor', hf.toFixed(2));
          setDisp('current_ltv_pct', ltv.toFixed(1) + '%');
          setDisp('collateral_drop_tolerance', (dropPct <= 0 ? '' : '+') + dropPct.toFixed(1) + '% Cushion');
          setDisp('max_additional_borrow', '$' + Math.round(maxBorrowSafe).toLocaleString());
        """
    },
    {
        "slug": "funding-rate-arbitrage",
        "category": "crypto",
        "name": "Perpetual Swap Funding Rate Arbitrage Annualized Yield (Cash & Carry)",
        "description": "Calculate market-neutral annualized return (APR) for funding rate arbitrage (Cash & Carry: Long Spot + Short Perpetual Swap).",
        "hero_badge": "Quantitative Trading • Market-Neutral Alpha",
        "formula_display": "Annualized APR (%) = (8-Hour Funding Rate % × 3 funding periods/day) × 365 days",
        "fields": [
            {"id": "arbitrage_capital_usd", "label": "Total Strategy Capital ($ USD)", "default": 50000, "prefix": "$", "min": 1000, "max": 10000000, "step": 2500, "hint": "Split 50/50 between Long Spot and Short Perp"},
            {"id": "average_8h_funding_rate_pct", "label": "8-Hour Funding Rate (%)", "default": 0.035, "suffix": "%", "min": -0.1, "max": 0.5, "step": 0.005, "hint": "Average 8-hour rate (0.01% = 10.9% APR, 0.03% = 32.8% APR)"},
            {"id": "taker_trading_fee_pct", "label": "Round-Trip Trading Fee (%)", "default": 0.08, "suffix": "%", "min": 0.02, "max": 0.3, "step": 0.01, "hint": "Entry and exit taker/maker fees on spot and perp"}
        ],
        "metrics": [
            {"id": "annualized_funding_apr", "label": "Market-Neutral Annualized APR", "default_display": "38.33%", "highlight": True},
            {"id": "annual_net_yield_usd", "label": "Projected Annual Net Cash Flow", "default_display": "$9,581.00 / yr", "highlight": True},
            {"id": "daily_funding_income_usd", "label": "Daily Funding Payment Received", "default_display": "$26.25 / day"},
            {"id": "breakeven_holding_days", "label": "Trading Fee Breakeven Horizon", "default_display": "1.5 Days"}
        ],
        "proof_steps": [
            {"step_title": "Daily Funding Multiplier", "step_text": "Perpetuals settle funding every 8 hours (3 times daily). Daily Rate = 0.035% × 3 = 0.105% per day."},
            {"step_title": "Annualized Yield Invariant", "step_text": "Annual APR = 0.105% × 365 = 38.325% gross APR."},
            {"step_title": "Capital Position Allocation", "step_text": "$50,000 capital is deployed: $25,000 buys physical spot BTC, and $25,000 collaterals a 1x Short BTC Perpetual swap. Price delta is 100% neutralized (0.00 delta)."},
            {"step_title": "Net Dollar Cash Flow", "step_text": "Short Perp Position ($25,000) collects 38.325% = $9,581.25/year in pure passive funding fees regardless of whether Bitcoin surges to $150k or crashes to $20k."}
        ],
        "faqs": [
            {"q": "What is Funding Rate Cash and Carry Arbitrage?", "a": "When perpetual swap markets trade at a premium to spot, longs pay shorts funding every 8 hours. By holding spot long and shorting the perp 1x, you eliminate all price risk while collecting continuous funding yields."},
            {"q": "What are the primary risks of funding rate arbitrage?", "a": "Execution/slippage risk on entry, exchange counterparty risk (insolvency), funding rates turning negative (requiring position unwinding), and liquidation risk on the short leg during violent upward short-squeezes."}
        ],
        "js_logic": """
          const cap = getNum('arbitrage_capital_usd');
          const rate8h = (getNum('average_8h_funding_rate_pct') || 0.035) / 100;
          const feePct = (getNum('taker_trading_fee_pct') || 0.08) / 100;

          const shortCapital = cap / 2;
          const dailyRate = rate8h * 3;
          const apr = dailyRate * 365 * 100;
          const dailyIncome = shortCapital * dailyRate;
          const annualIncome = dailyIncome * 365;

          const totalFees = cap * feePct;
          const breakevenDays = dailyIncome > 0 ? (totalFees / dailyIncome) : 0;

          setDisp('annualized_funding_apr', apr.toFixed(2) + '%');
          setDisp('annual_net_yield_usd', '$' + Math.round(annualIncome).toLocaleString() + ' / yr');
          setDisp('daily_funding_income_usd', '$' + dailyIncome.toFixed(2) + ' / day');
          setDisp('breakeven_holding_days', breakevenDays.toFixed(1) + ' Days');
        """
    },
    {
        "slug": "token-vesting-inflation",
        "category": "crypto",
        "name": "Token Vesting Cliff, Unlock Schedule & Circulating Inflation Model",
        "description": "Calculate monthly unlock volume, circulating supply inflation rate, and impending token unlock price pressure for venture-backed Web3 tokens.",
        "hero_badge": "Tokenomics • Supply Dilution",
        "formula_display": "Monthly Unlock = Total Allocation × (1 - TGE Unlock %) / Vesting Linear Months",
        "fields": [
            {"id": "total_token_supply", "label": "Total Token Max Supply", "default": 1000000000, "suffix": "Tokens", "min": 1000000, "max": 100000000000, "step": 10000000, "hint": "Total supply cap (e.g. 1 Billion tokens)"},
            {"id": "current_circulating_supply", "label": "Current Circulating Supply", "default": 180000000, "suffix": "Tokens (18%)", "min": 100000, "max": 50000000000, "step": 5000000, "hint": "Tokens currently liquid and trading"},
            {"id": "monthly_unlock_tokens", "label": "Upcoming Monthly Unlock Volume", "default": 22500000, "suffix": "Tokens/mo", "min": 10000, "max": 500000000, "step": 500000, "hint": "Team, investor, and ecosystem unlocks per month"},
            {"id": "token_price_usd", "label": "Current Token Market Price ($)", "default": 1.25, "prefix": "$", "min": 0.01, "max": 500, "step": 0.05, "hint": "Token exchange price"}
        ],
        "metrics": [
            {"id": "monthly_supply_inflation_pct", "label": "Monthly Supply Inflation Rate", "default_display": "+12.5% / month", "highlight": True},
            {"id": "monthly_sell_pressure_usd", "label": "Monthly New Dilution Inflow ($)", "default_display": "$28,125,000 / mo", "highlight": True},
            {"id": "annualized_inflation_pct", "label": "Annualized Supply Dilution", "default_display": "150.0% / year"},
            {"id": "market_cap_to_fdv_ratio", "label": "Circulating Mcap / FDV Ratio", "default_display": "18.0% (Low Float / High FDV)"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Supply Inflation Rate", "step_text": "Inflation = Monthly Unlock / Current Circulating = 22,500,000 / 180,000,000 = 12.5% per month."},
            {"step_title": "Dollar Sell Pressure Magnitude", "step_text": "New Monthly Sell Pressure = 22,500,000 tokens × $1.25 = $28,125,000 per month entering the market."},
            {"step_title": "FDV Overhang Ratio", "step_text": "Current Mcap = 180M × $1.25 = $225M. Fully Diluted Valuation (FDV) = 1B × $1.25 = $1.25B. Mcap/FDV = 18.0%."},
            {"step_title": "Price Depreciation Equilibrium", "step_text": "To keep the token price flat at $1.25, the project must attract $28.1M in fresh net buyer liquidity every single month just to absorb investor sell-offs."}
        ],
        "faqs": [
            {"q": "What is 'Low Float / High FDV' in crypto?", "a": "Low float tokens launch with only 5% to 15% of supply circulating, creating an artificially high price and massive Fully Diluted Valuation (FDV). As team and VC unlocks dump over years, supply inflation relentlessly crushes the token price."},
            {"q": "How can investors track major token unlock events?", "a": "Use on-chain vesting dashboards (TokenUnlocks, DefiLlama) to monitor cliff dates where massive blocks of venture capital tokens unlock simultaneously."}
        ],
        "js_logic": """
          const maxSupply = getNum('total_token_supply');
          const circ = getNum('current_circulating_supply');
          const unlock = getNum('monthly_unlock_tokens');
          const price = getNum('token_price_usd');

          const moInf = circ > 0 ? (unlock / circ) * 100 : 0;
          const annualInf = moInf * 12;
          const sellPressure = unlock * price;
          const mcapFdvRatio = maxSupply > 0 ? (circ / maxSupply) * 100 : 100;

          setDisp('monthly_supply_inflation_pct', '+' + moInf.toFixed(1) + '% / mo');
          setDisp('monthly_sell_pressure_usd', '$' + Math.round(sellPressure).toLocaleString() + ' / mo');
          setDisp('annualized_inflation_pct', annualInf.toFixed(1) + '% / yr');
          setDisp('market_cap_to_fdv_ratio', mcapFdvRatio.toFixed(1) + '% (' + (mcapFdvRatio < 25 ? 'Low Float / High FDV' : 'Healthy Float') + ')');
        """
    },
    {
        "slug": "crypto-fifo-lifo-tax",
        "category": "crypto",
        "name": "Crypto Capital Gains Tax Lot (FIFO vs LIFO vs HIFO) Calculator",
        "description": "Calculate realized short-term and long-term capital gains across First-In First-Out (FIFO), Last-In First-Out (LIFO), and Highest-In First-Out (HIFO) accounting.",
        "hero_badge": "Tax Optimization • Crypto Accounting",
        "formula_display": "Realized Capital Gain = Proceeds - Adjusted Cost Basis | Tax Owed = Capital Gain × Tax Rate",
        "fields": [
            {"id": "sale_proceeds_usd", "label": "Disposal Sale Proceeds ($ USD)", "default": 45000, "prefix": "$", "min": 100, "max": 1000000, "step": 1000, "hint": "Gross sale price received on disposal/swap"},
            {"id": "fifo_cost_basis", "label": "FIFO Cost Basis (Oldest Lots)", "default": 18000, "prefix": "$", "min": 500, "max": 1000000, "step": 500, "hint": "Cost of earliest purchased tokens"},
            {"id": "hifo_cost_basis", "label": "HIFO Cost Basis (Highest Price Lots)", "default": 38000, "prefix": "$", "min": 500, "max": 1000000, "step": 500, "hint": "Cost of highest price purchased tokens"},
            {"id": "capital_gains_tax_rate_pct", "label": "Estimated Tax Rate (%)", "default": 24.0, "suffix": "%", "min": 0, "max": 50, "step": 1, "hint": "Federal plus state capital gains tax bracket"}
        ],
        "metrics": [
            {"id": "hifo_tax_savings", "label": "Tax Savings Using HIFO vs FIFO", "default_display": "$4,800.00 Saved", "highlight": True},
            {"id": "hifo_capital_gain", "label": "HIFO Realized Capital Gain", "default_display": "$7,000.00", "highlight": True},
            {"id": "fifo_capital_gain", "label": "FIFO Realized Capital Gain", "default_display": "$27,000.00"},
            {"id": "hifo_tax_owed", "label": "Actual Tax Liability (HIFO)", "default_display": "$1,680.00"}
        ],
        "proof_steps": [
            {"step_title": "FIFO Accounting Realization", "step_text": "FIFO Gain = Proceeds ($45,000) - Oldest Basis ($18,000) = $27,000.00 gain. Tax Owed = $27,000 × 24% = $6,480.00."},
            {"step_title": "HIFO Optimization Method", "step_text": "HIFO Gain = Proceeds ($45,000) - Highest Basis ($38,000) = $7,000.00 gain. Tax Owed = $7,000 × 24% = $1,680.00."},
            {"step_title": "Direct Tax Alpha Surplus", "step_text": "Immediate Tax Savings = $6,480.00 - $1,680.00 = $4,800.00 in cash preserved. Specific ID / HIFO minimizes current taxable income."}
        ],
        "faqs": [
            {"q": "Does the IRS allow HIFO accounting for cryptocurrency?", "a": "Yes! IRS Notice 2014-21 and Revenue Ruling 2019-24 allow specific identification of cryptocurrency tax lots, provided the taxpayer can document the date acquired, cost basis, and fair market value of each specific unit sold."},
            {"q": "Are crypto-to-crypto swaps taxable events in the United States?", "a": "Yes! Swapping Bitcoin for Ethereum or swapping ETH for USDC is legally treated as a property disposal at fair market value, triggering a taxable capital gain or loss event."}
        ],
        "js_logic": """
          const proceeds = getNum('sale_proceeds_usd');
          const fifoBasis = getNum('fifo_cost_basis');
          const hifoBasis = getNum('hifo_cost_basis');
          const rate = (getNum('capital_gains_tax_rate_pct') || 24) / 100;

          const fifoGain = Math.max(0, proceeds - fifoBasis);
          const hifoGain = Math.max(0, proceeds - hifoBasis);
          const fifoTax = fifoGain * rate;
          const hifoTax = hifoGain * rate;
          const savings = fifoTax - hifoTax;

          setDisp('hifo_tax_savings', '$' + Math.round(savings).toLocaleString() + ' Saved');
          setDisp('hifo_capital_gain', '$' + Math.round(hifoGain).toLocaleString());
          setDisp('fifo_capital_gain', '$' + Math.round(fifoGain).toLocaleString());
          setDisp('hifo_tax_owed', '$' + Math.round(hifoTax).toLocaleString());
        """
    },
    {
        "slug": "zk-rollup-gas-compression",
        "category": "crypto",
        "name": "Zero-Knowledge (ZK) Rollup Calldata Compression & L2 Gas Savings",
        "description": "Calculate batch compression ratios, state diff rollup costs, and gas savings per transaction on Ethereum Layer 2 rollups (Arbitrum, Optimism, zkSync, Starknet).",
        "hero_badge": "Layer 2 Scaling • ZK Compression",
        "formula_display": "L2 Cost = (L2 Execution Gas × L2 Gas Price) + (L1 Calldata Bytes × 16 gas/byte × L1 Price / Batch Size)",
        "fields": [
            {"id": "l1_gas_price_gwei", "label": "Ethereum L1 Gas Price (Gwei)", "default": 30.0, "suffix": "Gwei", "min": 5, "max": 300, "step": 1, "hint": "L1 base fee for settling batch proofs"},
            {"id": "batch_size_transactions", "label": "Batch Proof Aggregation Size", "default": 1200, "suffix": "txs/batch", "min": 100, "max": 10000, "step": 100, "hint": "Number of transactions rolled into a single ZK SNARK/STARK proof"},
            {"id": "compressed_bytes_per_tx", "label": "Compressed Calldata Per Tx (Bytes)", "default": 24, "suffix": "bytes", "min": 10, "max": 200, "step": 2, "hint": "State diff compression size (standard L1 tx = ~110 bytes)"},
            {"id": "eth_spot_price", "label": "ETH Market Price ($)", "default": 3200, "prefix": "$", "min": 500, "max": 25000, "step": 50, "hint": "Current ETH spot price"}
        ],
        "metrics": [
            {"id": "l2_transaction_cost_usd", "label": "Effective L2 Transaction Cost", "default_display": "$0.04 USD", "highlight": True},
            {"id": "gas_reduction_pct", "label": "Gas Savings vs Ethereum Mainnet", "default_display": "99.4% Cheaper", "highlight": True},
            {"id": "mainnet_equivalent_usd", "label": "Ethereum L1 Mainnet Cost", "default_display": "$6.72 USD"},
            {"id": "data_compression_ratio", "label": "Calldata Compression Factor", "default_display": "4.6x Calldata Reduction"}
        ],
        "proof_steps": [
            {"step_title": "Mainnet Baseline Benchmark", "step_text": "A standard ERC-20 transfer on L1 consumes 65,000 gas units. At 30 Gwei and $3,200/ETH: 65,000 × 30 × 10⁻⁹ × $3,200 = $6.24."},
            {"step_title": "ZK State-Diff Compression", "step_text": "ZK-rollups only publish the final net state differences rather than full transaction signatures, compressing 110-byte inputs down to 24 bytes."},
            {"step_title": "Amortized L1 Batch Verification", "step_text": "Verifying a ZK-SNARK on L1 costs ~300,000 gas. Amortized across 1,200 transactions in the batch: 300,000 / 1,200 = 250 gas per user."},
            {"step_title": "All-In L2 Cost", "step_text": "User Gas = (24 bytes × 16 gas/byte) + 250 proof gas = 634 gas. Total Cost = 634 × 30 Gwei × $3,200 = $0.06 (99.0% savings)."}
        ],
        "faqs": [
            {"q": "How does EIP-4844 (Blobs) reduce Layer 2 rollup fees?", "a": "EIP-4844 introduced 'data blobs' on Ethereum that store rollup calldata off the execution layer and purge it after 18 days, reducing Layer 2 settlement costs by 80% to 95%."},
            {"q": "What is the difference between Optimistic rollups and ZK-rollups?", "a": "Optimistic rollups assume transactions are valid and rely on a 7-day fraud-proof challenge window for withdrawals. ZK-rollups use cryptographic validity proofs (SNARKs/STARKs) allowing mathematically instant withdrawals once the proof settles on L1."}
        ],
        "js_logic": """
          const l1Gwei = getNum('l1_gas_price_gwei');
          const batch = getNum('batch_size_transactions') || 1200;
          const bytes = getNum('compressed_bytes_per_tx') || 24;
          const ethPrice = getNum('eth_spot_price');

          const l1TxGas = 70000;
          const l1Cost = (l1TxGas * l1Gwei * 1e-9) * ethPrice;

          const calldataGas = bytes * 16;
          const proofAmortized = 350000 / batch;
          const l2TotalGas = calldataGas + proofAmortized;
          const l2Cost = (l2TotalGas * l1Gwei * 1e-9) * ethPrice + 0.01;
          const savings = l1Cost > 0 ? ((l1Cost - l2Cost) / l1Cost) * 100 : 99;

          setDisp('l2_transaction_cost_usd', '$' + l2Cost.toFixed(3) + ' USD');
          setDisp('gas_reduction_pct', savings.toFixed(1) + '% Cheaper');
          setDisp('mainnet_equivalent_usd', '$' + l1Cost.toFixed(2) + ' USD');
          setDisp('data_compression_ratio', (110 / bytes).toFixed(1) + 'x Calldata Reduction');
        """
    },
    {
        "slug": "slippage-tolerance-price-impact",
        "category": "crypto",
        "name": "DEX Slippage Tolerance & Price Impact Calculator",
        "description": "Calculate price impact percentage, minimum received tokens, and sandwich MEV vulnerability on Uniswap constant product liquidity pools.",
        "hero_badge": "DEX Mechanics • Price Impact",
        "formula_display": "Price Impact (%) ≈ Trade Size / (2 · Pool Reserves) | Min Received = Quoted Amount · (1 - Slippage % / 100)",
        "fields": [
            {"id": "trade_swap_amount_usd", "label": "Swap Trade Size ($ USD)", "default": 25000, "prefix": "$", "min": 50, "max": 10000000, "step": 1000, "hint": "Size of market swap"},
            {"id": "pool_liquidity_reserve_usd", "label": "Pool Total Liquidity ($ USD)", "default": 500000, "prefix": "$", "min": 5000, "max": 50000000, "step": 25000, "hint": "Total reserve depth in the trading pool"},
            {"id": "slippage_tolerance_pct", "label": "Configured Slippage Tolerance (%)", "default": 0.5, "suffix": "%", "min": 0.1, "max": 5.0, "step": 0.1, "hint": "Max allowable price deviation before transaction reverts"}
        ],
        "metrics": [
            {"id": "calculated_price_impact", "label": "Algorithmic Price Impact", "default_display": "4.88%", "highlight": True},
            {"id": "minimum_received_usd", "label": "Minimum Guaranteed Proceeds", "default_display": "$23,780.00", "highlight": True},
            {"id": "mev_sandwich_risk", "label": "MEV Bot Sandwich Vulnerability", "default_display": "Elevated Risk (Use Private RPC)", "highlight": True},
            {"id": "slippage_buffer_dollars", "label": "Slippage Loss Buffer", "default_display": "$125.00 Maximum"}
        ],
        "proof_steps": [
            {"step_title": "Constant Product Price Shift", "step_text": "In x · y = k pools, trading Δx shifts the spot price. Price Impact = Δx / (x + Δx) = $25,000 / ($500,000 + $25,000) = 4.76%."},
            {"step_title": "Slippage Tolerance Protection", "step_text": "With 0.5% slippage tolerance, the transaction reverts if executed price drops more than 0.5% below the simulated quote."},
            {"step_title": "MEV Sandwich Exploitation Risk", "step_text": "Setting a high slippage tolerance (e.g. 2%+) on a large order allows MEV searchers to front-run and back-run your swap, extracting the entire slippage tolerance as risk-free profit."}
        ],
        "faqs": [
            {"q": "What is the difference between Price Impact and Slippage?", "a": "Price impact is the mathematically unavoidable price movement caused by your own trade size relative to pool liquidity reserves. Slippage is the external price movement caused by other traders or MEV bots between the time you submit the transaction and when it is mined into a block."},
            {"q": "How can large traders eliminate MEV sandwich attacks?", "a": "Route orders through DEX aggregators (1inch, CoW Swap) that split trades across multiple pools, use MEV-Blocker private RPC endpoints, or execute intent-based batch auctions."}
        ],
        "js_logic": """
          const trade = getNum('trade_swap_amount_usd');
          const pool = getNum('pool_liquidity_reserve_usd');
          const slip = (getNum('slippage_tolerance_pct') || 0.5) / 100;

          const impact = pool > 0 ? (trade / (pool + trade)) * 100 : 10;
          const quoted = trade * (1 - impact / 100);
          const minRec = quoted * (1 - slip);
          const slipBuffer = quoted * slip;

          let mev = 'Low (Safe Trade Size)';
          if (impact > 5.0 || slip > 0.02) {
            mev = 'High Vulnerability (MEV Sandwich Attack Risk)';
          } else if (impact > 2.0) {
            mev = 'Elevated Risk (Use Private RPC)';
          }

          setDisp('calculated_price_impact', impact.toFixed(2) + '%');
          setDisp('minimum_received_usd', '$' + Math.round(minRec).toLocaleString());
          setDisp('mev_sandwich_risk', mev);
          setDisp('slippage_buffer_dollars', '$' + slipBuffer.toFixed(2) + ' Max');
        """
    },
    {
        "slug": "bonding-curve-token-mint",
        "category": "crypto",
        "name": "Continuous Token Bonding Curve Price & Minting Cost Model",
        "description": "Calculate instantaneous token price, buy/sell minting costs, and reserve pool backing for linear and polynomial bonding curves (Pump.fun, Bancor).",
        "hero_badge": "Tokenomics • Automated Market Curves",
        "formula_display": "Price P(S) = m · Sᵇ | Total Cost to Mint = ∫ P(S) dS = (m / [b + 1]) · S^(b + 1)",
        "fields": [
            {"id": "current_token_supply", "label": "Current Circulating Supply (S)", "default": 25000000, "suffix": "Tokens", "min": 10000, "max": 1000000000, "step": 100000, "hint": "Tokens minted so far along the curve"},
            {"id": "tokens_to_buy", "label": "Tokens to Purchase / Mint (ΔS)", "default": 5000000, "suffix": "Tokens", "min": 1000, "max": 50000000, "step": 100000, "hint": "Number of new tokens to mint"},
            {"id": "curve_slope_m", "label": "Curve Price Slope Coefficient (m)", "default": 0.00000002, "min": 0.0000000001, "max": 0.001, "step": 0.000000005, "hint": "Linear price scaling factor"},
            {"id": "curve_exponent_b", "label": "Curve Exponent Power (1 = Linear, 2 = Quadratic)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1 for linear curve, 2 for exponential steepness"}
        ],
        "metrics": [
            {"id": "total_purchase_cost_eth", "label": "Total Cost to Mint Tokens", "default_display": "13.75 SOL / ETH", "highlight": True},
            {"id": "final_token_price", "label": "New Token Price After Buy", "default_display": "$0.60 / token", "highlight": True},
            {"id": "average_cost_per_token", "label": "Average Purchase Price", "default_display": "$0.55 / token"},
            {"id": "reserve_pool_balance", "label": "Total Collateral Locked in Curve", "default_display": "$90.00 Total Reserve"}
        ],
        "proof_steps": [
            {"step_title": "Instantaneous Starting Price", "step_text": "P(25M) = 0.00000002 × 25,000,000 = $0.50 per token."},
            {"step_title": "Integral Cost Formulation", "step_text": "Cost = ∫₂₅ᴹ³⁰ᴹ (m · S) dS = (m / 2) · [S₂² - S₁²]."},
            {"step_title": "Definite Integral Evaluation", "step_text": "Cost = (0.00000002 / 2) · [30,000,000² - 25,000,000²] = 10⁻⁸ · [900×10¹² - 625×10¹²] = 10⁻⁸ · 275×10¹² = $2,750,000."},
            {"step_title": "Average Execution Price", "step_text": "Average Price = $2,750,000 / 5,000,000 = $0.55 per token. Final price escalates to $0.60."}
        ],
        "faqs": [
            {"q": "How do memecoin launchpads (Pump.fun) use bonding curves?", "a": "Launchpads use a deterministic linear bonding curve where early buyers purchase tokens cheaply from the contract. Once $69k of liquidity is deposited and the market cap reaches $69k, the curve automatically migrates and seeds a Raydium DEX pool with burned liquidity."},
            {"q": "Does a bonding curve guarantee 100% exit liquidity?", "a": "Yes! Because tokens are bought and sold directly against a smart contract reserve pool according to mathematical integration, there are no order books and buyers can always sell tokens back to the curve at the current marginal price."}
        ],
        "js_logic": """
          const s1 = getNum('current_token_supply');
          const deltaS = getNum('tokens_to_buy');
          const m = getNum('curve_slope_m') || 0.00000002;
          const b = Math.round(getNum('curve_exponent_b')) || 1;

          const s2 = s1 + deltaS;
          const p1 = m * Math.pow(s1, b);
          const p2 = m * Math.pow(s2, b);

          const cost = (m / (b + 1)) * (Math.pow(s2, b + 1) - Math.pow(s1, b + 1));
          const avgPrice = deltaS > 0 ? (cost / deltaS) : p1;
          const totalReserve = (m / (b + 1)) * Math.pow(s2, b + 1);

          setDisp('total_purchase_cost_eth', '$' + Math.round(cost).toLocaleString());
          setDisp('final_token_price', '$' + p2.toFixed(4) + ' / token');
          setDisp('average_cost_per_token', '$' + avgPrice.toFixed(4) + ' / token');
          setDisp('reserve_pool_balance', '$' + Math.round(totalReserve).toLocaleString() + ' Locked');
        """
    },
    {
        "slug": "stablecoin-depeg-arbitrage",
        "category": "crypto",
        "name": "Stablecoin Peg Deviation & Mint/Redeem Arbitrage Spread Calculator",
        "description": "Calculate net profit margin, execution slippage, and capital turnover ROI when arbitraging stablecoins (USDT, USDC, DAI) during depeg events.",
        "hero_badge": "DeFi Arbitrage • Stablecoin Pegs",
        "formula_display": "Net Arbitrage Margin = (1.00 - Discounted Market Price) - Mint/Redeem Fee - Gas Slippage",
        "fields": [
            {"id": "discounted_market_price", "label": "Discounted Market Price ($)", "default": 0.965, "prefix": "$", "min": 0.50, "max": 1.05, "step": 0.005, "hint": "Depegged market trading price (e.g. $0.965)"},
            {"id": "arbitrage_capital_usd", "label": "Arbitrage Capital Deployed ($)", "default": 100000, "prefix": "$", "min": 5000, "max": 10000000, "step": 10000, "hint": "Capital used to purchase discounted stablecoin"},
            {"id": "redemption_fee_pct", "label": "Issuer Redemption Fee (%)", "default": 0.10, "suffix": "%", "min": 0, "max": 1.0, "step": 0.05, "hint": "Tether / Circle official 1:1 fiat redemption fee"},
            {"id": "redemption_holding_days", "label": "Redemption Wire Processing Time (Days)", "default": 3, "suffix": "days", "min": 1, "max": 14, "step": 1, "hint": "Banking wire settlement turnaround time"}
        ],
        "metrics": [
            {"id": "net_arbitrage_profit", "label": "Net Realized Profit", "default_display": "$3,525.00", "highlight": True},
            {"id": "net_roi_percentage", "label": "Return on Investment (ROI)", "default_display": "3.53% Net ROI", "highlight": True},
            {"id": "annualized_arbitrage_apr", "label": "Annualized Capital Yield (APR)", "default_display": "429.5% APR (3-Day Turn)", "highlight": True},
            {"id": "gross_discount_spread", "label": "Gross Market Peg Discount", "default_display": "3.50% Discount ($0.965 vs $1.00)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Discount Spread", "step_text": "Tokens Purchased = $100,000 / $0.965 = 103,626.94 depegged stablecoin tokens."},
            {"step_title": "Official 1:1 Parity Redemption", "step_text": "Redeemed at Issuer for USD: 103,626.94 × $1.00 = $103,626.94 gross wire value."},
            {"step_title": "Redemption & Wire Fees", "step_text": "Issuer Fee = $103,626.94 × 0.10% = $103.63. Net proceeds received = $103,523.31."},
            {"step_title": "Net ROI & Capital Velocity", "step_text": "Net Profit = $103,523.31 - $100,000 = $3,523.31 (3.52% ROI). Turning over capital every 3 days yields an annualized APR over 420%."}
        ],
        "faqs": [
            {"q": "What is the primary risk of stablecoin depeg arbitrage?", "a": "Issuer insolvency risk. If the stablecoin depegs because its underlying reserves are frozen, seized, or compromised (e.g. Terra Luna algorithmic collapse or Silicon Valley Bank USDC freeze), redemptions may be halted, causing catastrophic capital loss."},
            {"q": "Why don't retail traders capture depeg arbitrage?", "a": "Direct 1:1 fiat redemptions at Tether or Circle require institutional verification, minimum $100,000 batch sizes, and multi-day wire settlement through traditional banking partner rails."}
        ],
        "js_logic": """
          const price = getNum('discounted_market_price');
          const cap = getNum('arbitrage_capital_usd');
          const feePct = (getNum('redemption_fee_pct') || 0.10) / 100;
          const days = getNum('redemption_holding_days') || 3;

          const tokensBought = price > 0 ? (cap / price) : 0;
          const grossRedemption = tokensBought * 1.0;
          const fee = grossRedemption * feePct;
          const netProceeds = grossRedemption - fee;
          const netProfit = netProceeds - cap;
          const roi = cap > 0 ? (netProfit / cap) * 100 : 0;
          const apr = days > 0 ? (roi / days) * 365 : 0;

          setDisp('net_arbitrage_profit', '$' + Math.round(netProfit).toLocaleString());
          setDisp('net_roi_percentage', roi.toFixed(2) + '% Net ROI');
          setDisp('annualized_arbitrage_apr', apr.toFixed(1) + '% APR (' + days + '-Day Turn)');
          setDisp('gross_discount_spread', ((1.0 - price) * 100).toFixed(2) + '% Discount');
        """
    },
    {
        "slug": "cross-chain-bridge-fee",
        "category": "crypto",
        "name": "Cross-Chain Token Bridge Fee & Gas Slippage Optimizer",
        "description": "Calculate total cost, bridge operator fee, destination gas subsidy, and slippage when bridging tokens across Ethereum, Arbitrum, Polygon, and Solana.",
        "hero_badge": "Interoperability • Bridge Analytics",
        "formula_display": "Total Bridge Fee = Origin Gas + Operator Fixed Fee + Protocol % + Destination Mint Gas",
        "fields": [
            {"id": "bridged_amount_usd", "label": "Amount to Bridge ($ USD)", "default": 5000, "prefix": "$", "min": 50, "max": 500000, "step": 250, "hint": "Transfer amount in USDC or ETH"},
            {"id": "origin_gas_fee_usd", "label": "Origin Chain Gas Fee ($)", "default": 8.50, "prefix": "$", "min": 0.05, "max": 100, "step": 0.5, "hint": "L1 gas to approve and deposit tokens"},
            {"id": "bridge_protocol_fee_pct", "label": "Bridge Protocol Fee (%)", "default": 0.06, "suffix": "%", "min": 0, "max": 0.5, "step": 0.01, "hint": "Across, Stargate, or Hop protocol fee"},
            {"id": "dest_gas_drop_usd", "label": "Destination Gas Refuel ($)", "default": 5.00, "prefix": "$", "min": 0, "max": 50, "step": 1, "hint": "Optional native gas subsidy credited on destination chain"}
        ],
        "metrics": [
            {"id": "net_amount_received", "label": "Net Amount Received on Destination", "default_display": "$4,983.50", "highlight": True},
            {"id": "total_bridge_toll_usd", "label": "Total Bridge Toll & Gas Paid", "default_display": "$16.50", "highlight": True},
            {"id": "effective_toll_percentage", "label": "Effective Bridge Cost Percentage", "default_display": "0.33%", "highlight": True},
            {"id": "protocol_fee_dollars", "label": "Protocol Liquidity Fee", "default_display": "$3.00"}
        ],
        "proof_steps": [
            {"step_title": "Protocol Liquidity Fee", "step_text": "Protocol Fee = $5,000 × 0.06% = $3.00."},
            {"step_title": "Destination Gas Refuel Deductions", "step_text": "Destination Gas = $5.00. Net Token Credit = $5,000 - $3.00 - $5.00 = $4,992.00."},
            {"step_title": "All-In Cross-Chain Cost", "step_text": "Total Expense = Origin Gas ($8.50) + Protocol Fee ($3.00) + Dest Gas ($5.00) = $16.50 (0.33% total toll)."}
        ],
        "faqs": [
            {"q": "What is the difference between Burn-and-Mint and Lock-and-Mint bridges?", "a": "Lock-and-Mint bridges lock collateral in a source chain multisig and mint wrapped tokens on the destination (high smart contract hack risk). Burn-and-Mint (like Circle CCTP) burns native USDC natively on source and mints real native USDC on destination with zero wrapper risk."},
            {"q": "Why do cross-chain bridges get hacked so frequently?", "a": "Bridges custody massive multi-hundred-million-dollar honey pots of locked assets secured by complex multi-chain relayer nodes, making verification oracle bugs catastrophic targets for state-sponsored exploits."}
        ],
        "js_logic": """
          const amount = getNum('bridged_amount_usd');
          const originGas = getNum('origin_gas_fee_usd');
          const feePct = (getNum('bridge_protocol_fee_pct') || 0.06) / 100;
          const destGas = getNum('dest_gas_drop_usd');

          const protoFee = amount * feePct;
          const netReceived = Math.max(0, amount - protoFee - destGas);
          const totalToll = originGas + protoFee + destGas;
          const tollPct = amount > 0 ? (totalToll / amount) * 100 : 0;

          setDisp('net_amount_received', '$' + netReceived.toFixed(2));
          setDisp('total_bridge_toll_usd', '$' + totalToll.toFixed(2));
          setDisp('effective_toll_percentage', tollPct.toFixed(2) + '%');
          setDisp('protocol_fee_dollars', '$' + protoFee.toFixed(2));
        """
    },
    {
        "slug": "nft-royalty-split",
        "category": "crypto",
        "name": "NFT Marketplace Creator Royalty Split & Net Secondary Proceeds",
        "description": "Calculate creator royalty splits, marketplace fees (OpenSea, Blur, Magic Eden), and net seller payout on secondary NFT market sales.",
        "hero_badge": "Digital Collectibles • Creator Royalties",
        "formula_display": "Net Seller Payout = Sale Price - Marketplace Fee - Creator Royalty Fee",
        "fields": [
            {"id": "nft_sale_price_eth", "label": "NFT Gross Sale Price (ETH or SOL)", "default": 2.5, "suffix": "ETH", "min": 0.05, "max": 250, "step": 0.1, "hint": "Agreed secondary market transaction price"},
            {"id": "marketplace_fee_pct", "label": "Marketplace Platform Fee (%)", "default": 0.5, "suffix": "%", "min": 0, "max": 5.0, "step": 0.1, "hint": "Blur = 0.5%, OpenSea = 2.5%, Magic Eden = 2.0%"},
            {"id": "creator_royalty_pct", "label": "Enforced Creator Royalty (%)", "default": 5.0, "suffix": "%", "min": 0, "max": 15.0, "step": 0.5, "hint": "Original artist / collection royalty share"},
            {"id": "eth_market_price_usd", "label": "Native Token Price ($ USD)", "default": 3200, "prefix": "$", "min": 10, "max": 10000, "step": 50, "hint": "Current ETH or SOL spot price"}
        ],
        "metrics": [
            {"id": "net_seller_payout_eth", "label": "Net Seller Payout", "default_display": "2.36 ETH ($7,560.00)", "highlight": True},
            {"id": "creator_royalty_earned", "label": "Creator Royalty Received", "default_display": "0.125 ETH ($400.00)", "highlight": True},
            {"id": "marketplace_cut_usd", "label": "Marketplace Fee Deducted", "default_display": "0.0125 ETH ($40.00)"},
            {"id": "total_deduction_pct", "label": "Total Overhead Cut", "default_display": "5.5% Total Deductions"}
        ],
        "proof_steps": [
            {"step_title": "Creator Royalty Allocation", "step_text": "Royalty = 2.5 ETH × 5.0% = 0.125 ETH ($400.00) transferred directly to creator royalty split contract."},
            {"step_title": "Marketplace Fee Deductions", "step_text": "Platform Fee = 2.5 ETH × 0.5% = 0.0125 ETH ($40.00)."},
            {"step_title": "Net Seller Proceeds", "step_text": "Net Seller = 2.5 - 0.125 - 0.0125 = 2.3625 ETH ($7,560.00)."}
        ],
        "faqs": [
            {"q": "Are creator royalties guaranteed on Ethereum smart contracts?", "a": "Standard ERC-721 contracts do not enforce royalties on-chain because transfers can happen peer-to-peer. Modern collections use ERC-2981 royalty standards and programmable marketplace filter registries to block zero-royalty trading platforms."},
            {"q": "Why did major NFT marketplaces slash creator royalties?", "a": "In 2022-2023, zero-fee aggregators (Blur) captured 80%+ of trading volume by making royalties optional, forcing OpenSea and Magic Eden to lower default royalty enforcement to compete for pro traders."}
        ],
        "js_logic": """
          const sale = getNum('nft_sale_price_eth');
          const mktPct = (getNum('marketplace_fee_pct') || 0.5) / 100;
          const royPct = (getNum('creator_royalty_pct') || 5.0) / 100;
          const price = getNum('eth_market_price_usd');

          const royEth = sale * royPct;
          const mktEth = sale * mktPct;
          const netEth = Math.max(0, sale - royEth - mktEth);
          const totalDedPct = (mktPct + royPct) * 100;

          setDisp('net_seller_payout_eth', netEth.toFixed(3) + ' ETH ($' + Math.round(netEth * price).toLocaleString() + ')');
          setDisp('creator_royalty_earned', royEth.toFixed(3) + ' ETH ($' + Math.round(royEth * price).toLocaleString() + ')');
          setDisp('marketplace_cut_usd', mktEth.toFixed(4) + ' ETH ($' + Math.round(mktEth * price).toLocaleString() + ')');
          setDisp('total_deduction_pct', totalDedPct.toFixed(1) + '% Total Deductions');
        """
    },
    {
        "slug": "algorithmic-lending-apy",
        "category": "crypto",
        "name": "Algorithmic Lending Supply & Borrow APY (Aave / Compound Model)",
        "description": "Calculate interest rate curves, utilization rate 'kink' point, and supply/borrow APYs for algorithmic money markets (Aave v3 / Compound v3).",
        "hero_badge": "DeFi • Interest Rate Curves",
        "formula_display": "Borrow APY = Base Rate + (Utilization / Optimal) · Slope₁ | If U > U_opt: + Slope₂ · ([U - U_opt] / [1 - U_opt])",
        "fields": [
            {"id": "total_deposited_pool_usd", "label": "Total Pool Supplied Deposits ($)", "default": 10000000, "prefix": "$", "min": 100000, "max": 500000000, "step": 500000, "hint": "Total collateral liquidity supplied by depositors"},
            {"id": "total_borrowed_pool_usd", "label": "Total Active Borrows ($)", "default": 7500000, "prefix": "$", "min": 10000, "max": 450000000, "step": 500000, "hint": "Total loans currently drawn from the pool"},
            {"id": "optimal_utilization_kink_pct", "label": "Optimal Utilization Kink Point (%)", "default": 80, "suffix": "%", "min": 50, "max": 95, "step": 5, "hint": "Kink inflection threshold (typically 80% or 90%)"},
            {"id": "reserve_factor_pct", "label": "Protocol Reserve Factor (%)", "default": 15, "suffix": "%", "min": 5, "max": 30, "step": 1, "hint": "Portion of borrow interest retained by protocol treasury"}
        ],
        "metrics": [
            {"id": "borrow_apy_rate", "label": "Current Variable Borrow APY", "default_display": "5.63%", "highlight": True},
            {"id": "supply_apy_rate", "label": "Current Passive Supply APY", "default_display": "3.59%", "highlight": True},
            {"id": "pool_utilization_ratio", "label": "Pool Utilization Rate (U)", "default_display": "75.0%", "highlight": True},
            {"id": "kink_status", "label": "Interest Rate Regime", "default_display": "Below Kink (Stable Interest Curve)"}
        ],
        "proof_steps": [
            {"step_title": "Pool Utilization Rate U", "step_text": "U = Total Borrows / Total Deposits = $7,500,000 / $10,000,000 = 75.0%."},
            {"step_title": "Below-Kink Borrow Rate", "step_text": "Because U (75%) ≤ Optimal Kink (80%): Borrow Rate = Base (0.5%) + (75% / 80%) × Slope₁ (5.5%) = 0.5% + 5.156% = 5.66%."},
            {"step_title": "Supply APY Derivation", "step_text": "Supply APY = Borrow Rate × Utilization Rate × (1 - Reserve Factor) = 5.66% × 0.75 × (1 - 0.15) = 3.61% passive yield."}
        ],
        "faqs": [
            {"q": "What happens when DeFi utilization passes the 'kink' point?", "a": "When borrowing exceeds the kink point (e.g. >80%), the interest rate curve slope accelerates steeply (Slope₂ up to 100%+ APY) to strongly incentivize borrowers to repay loans and depositors to supply liquidity before the pool runs dry."},
            {"q": "Why can't utilization be allowed to reach 100%?", "a": "If utilization touches 100%, depositors cannot withdraw their funds because every dollar is loaned out. The steep interest rate curve preserves liquidity buffers for withdrawals."}
        ],
        "js_logic": """
          const dep = getNum('total_deposited_pool_usd');
          const borrow = Math.min(dep, getNum('total_borrowed_pool_usd'));
          const uOpt = (getNum('optimal_utilization_kink_pct') || 80) / 100;
          const rf = (getNum('reserve_factor_pct') || 15) / 100;

          const u = dep > 0 ? (borrow / dep) : 0;
          const baseRate = 0.005;
          const slope1 = 0.055;
          const slope2 = 0.75;

          let borrowApy = 0;
          let status = 'Below Kink (Stable)';
          if (u <= uOpt) {
            borrowApy = baseRate + (u / uOpt) * slope1;
          } else {
            status = 'ABOVE KINK (Steep Surge Regime)';
            borrowApy = baseRate + slope1 + ((u - uOpt) / (1 - uOpt)) * slope2;
          }

          const supplyApy = borrowApy * u * (1 - rf);

          setDisp('borrow_apy_rate', (borrowApy * 100).toFixed(2) + '%');
          setDisp('supply_apy_rate', (supplyApy * 100).toFixed(2) + '%');
          setDisp('pool_utilization_ratio', (u * 100).toFixed(1) + '%');
          setDisp('kink_status', status);
        """
    },
    {
        "slug": "mining-difficulty-adjustment",
        "category": "crypto",
        "name": "Bitcoin Mining Difficulty Adjustment & Block Time Estimator",
        "description": "Calculate upcoming Bitcoin epoch difficulty adjustment percentage, estimated hash rate change, and average block discovery interval.",
        "hero_badge": "Consensus Dynamics • Difficulty Adjustment",
        "formula_display": "New Difficulty = Old Difficulty × (Actual 2,016 Block Duration in seconds / 1,209,600 target seconds)",
        "fields": [
            {"id": "current_difficulty_trillion", "label": "Current Network Difficulty (Trillion)", "default": 84.5, "suffix": "T", "min": 10, "max": 500, "step": 1, "hint": "Current epoch target difficulty (T = 10¹²)"},
            {"id": "blocks_elapsed_in_epoch", "label": "Blocks Mined in Current Epoch", "default": 1450, "suffix": "blocks (of 2,016)", "min": 100, "max": 2015, "step": 50, "hint": "Progress through 2,016-block difficulty period"},
            {"id": "average_block_time_sec", "label": "Measured Average Block Time (Seconds)", "default": 565, "suffix": "seconds", "min": 300, "max": 900, "step": 5, "hint": "Target is exactly 600 seconds (10 minutes)"}
        ],
        "metrics": [
            {"id": "projected_difficulty_adj_pct", "label": "Projected Difficulty Adjustment", "default_display": "+6.19% Increase", "highlight": True},
            {"id": "next_difficulty_target", "label": "Projected Next Difficulty", "default_display": "89.7 T", "highlight": True},
            {"id": "remaining_epoch_days", "label": "Time Remaining Until Retarget", "default_display": "3.7 Days", "highlight": True},
            {"id": "network_hashrate_growth", "label": "Implied Hashrate Momentum", "default_display": "Hashrate Expanding Faster than Target"}
        ],
        "proof_steps": [
            {"step_title": "Epoch Block Target Invariant", "step_text": "Bitcoin difficulty recalibrates every 2,016 blocks. At 10 minutes (600s) per block, target duration = 2,016 × 600s = 1,209,600 seconds (exactly 2 weeks)."},
            {"step_title": "Observed Block Time Deviation", "step_text": "Blocks are currently being solved in 565 seconds (faster than 600s target), indicating miners have added substantial new hash power."},
            {"step_title": "Adjustment Ratio Derivation", "step_text": "Ratio = 600 / 565 = 1.0619 (+6.19% adjustment)."},
            {"step_title": "Difficulty Recalibration", "step_text": "Next Difficulty = 84.5 T × 1.0619 = 89.73 T. Difficulty adjusts upward to slow block times back to 10 minutes."}
        ],
        "faqs": [
            {"q": "What is the maximum allowed difficulty adjustment in Bitcoin?", "a": "Satoshi Nakamoto built a 4x cap into the protocol: difficulty can never adjust up by more than 300% (4x) or drop by more than 75% (0.25x) in any single 2,016-block epoch to prevent catastrophic swings."},
            {"q": "Why does difficulty adjust every 2,016 blocks?", "a": "The 2-week adjustment mechanism ensures Bitcoin's monetary emission schedule remains mathematically deterministic regardless of how many millions of ASIC computers join or leave the network."}
        ],
        "js_logic": """
          const diff = getNum('current_difficulty_trillion') || 84.5;
          const blocks = getNum('blocks_elapsed_in_epoch') || 1450;
          const timeSec = getNum('average_block_time_sec') || 565;

          const ratio = 600 / timeSec;
          const clampedRatio = Math.min(4.0, Math.max(0.25, ratio));
          const adjPct = (clampedRatio - 1) * 100;
          const nextDiff = diff * clampedRatio;

          const remainingBlocks = Math.max(1, 2016 - blocks);
          const remainingSec = remainingBlocks * timeSec;
          const remainingDays = remainingSec / 86400;

          setDisp('projected_difficulty_adj_pct', (adjPct >= 0 ? '+' : '') + adjPct.toFixed(2) + '% Adjustment');
          setDisp('next_difficulty_target', nextDiff.toFixed(1) + ' T');
          setDisp('remaining_epoch_days', remainingDays.toFixed(1) + ' Days');
          setDisp('network_hashrate_growth', adjPct > 0 ? 'Hashrate Expanding (+Mining Competition)' : 'Hashrate Retracting (-Miners Shutting Down)');
        """
    },
    {
        "slug": "crypto-payment-processor-fees",
        "category": "crypto",
        "name": "Crypto Payment Gateway vs Credit Card Interchange Processing Fees",
        "description": "Calculate annual payment processing dollar savings, chargeback elimination, and settlement fees when accepting crypto (1% flat) vs credit cards (2.9% + $0.30).",
        "hero_badge": "Fintech • Merchant Processing",
        "formula_display": "Annual Savings = (Credit Card Fees + Chargebacks) - Crypto Gateway Fees",
        "fields": [
            {"id": "annual_merchant_sales", "label": "Annual Merchant Sales ($ USD)", "default": 750000, "prefix": "$", "min": 25000, "max": 50000000, "step": 25000, "hint": "Total annual e-commerce or B2B sales volume"},
            {"id": "average_order_value_usd", "label": "Average Order Value ($ AOV)", "default": 85.0, "prefix": "$", "min": 5, "max": 5000, "step": 5, "hint": "Mean checkout dollar amount"},
            {"id": "cc_interchange_rate_pct", "label": "Credit Card Processing Fee (%)", "default": 2.9, "suffix": "%", "min": 1.5, "max": 4.5, "step": 0.1, "hint": "Stripe/PayPal standard = 2.9% + $0.30"},
            {"id": "crypto_gateway_fee_pct", "label": "Crypto Processor Fee (%)", "default": 1.0, "suffix": "%", "min": 0.1, "max": 2.5, "step": 0.1, "hint": "BitPay, Coinbase Commerce, or NOWPayments (typically 0.5% - 1.0%)"},
            {"id": "chargeback_loss_pct", "label": "Credit Card Chargeback Fraud Rate (%)", "default": 0.75, "suffix": "%", "min": 0, "max": 3.0, "step": 0.05, "hint": "Lost revenue from credit card friendly fraud and chargebacks"}
        ],
        "metrics": [
            {"id": "annual_merchant_savings", "label": "Annual Processing Savings", "default_display": "$19,650.00 / yr", "highlight": True},
            {"id": "net_fee_reduction_pct", "label": "Payment Processing Cost Reduction", "default_display": "71.5% Fee Cut", "highlight": True},
            {"id": "credit_card_total_fees", "label": "Total Credit Card Fees + Fraud", "default_display": "$27,150.00 / yr"},
            {"id": "crypto_processing_cost", "label": "Total Crypto Processing Cost", "default_display": "$7,500.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Credit Card Total Cost Breakdown", "step_text": "Number of Orders = $750,000 / $85 = 8,824 orders. Fixed fee ($0.30 × 8,824) = $2,647. Variable fee (2.9% × $750k) = $21,750. Fraud chargebacks (0.75% × $750k) = $5,625. Total CC outflow = $30,022.00."},
            {"step_title": "Crypto Gateway Economics", "step_text": "Crypto Gateway (1.0% flat) = $7,500.00 with ZERO chargeback fraud risk due to cryptographic finality."},
            {"step_title": "Net Merchant Margin Expansion", "step_text": "Annual Savings = $30,022 - $7,500 = $22,522.00 in bottom-line net profit."}
        ],
        "faqs": [
            {"q": "Can customers initiate chargebacks on cryptocurrency payments?", "a": "No! Blockchain transactions are cryptographically final and irreversible. Once confirmed, a customer cannot call their bank to claim 'friendly fraud' or dispute the charge, saving merchants thousands in dispute fees."},
            {"q": "How do merchants protect against crypto price volatility?", "a": "Crypto gateways (BitPay, Coinbase Commerce) automatically convert incoming Bitcoin or Ethereum into USD stablecoins (USDC) or wire fiat dollars directly to the merchant's business bank account instantly at the moment of checkout."}
        ],
        "js_logic": """
          const sales = getNum('annual_merchant_sales');
          const aov = Math.max(5, getNum('average_order_value_usd'));
          const ccRate = (getNum('cc_interchange_rate_pct') || 2.9) / 100;
          const cryptoRate = (getNum('crypto_gateway_fee_pct') || 1.0) / 100;
          const cbRate = (getNum('chargeback_loss_pct') || 0.75) / 100;

          const orders = sales / aov;
          const ccFixed = orders * 0.30;
          const ccVar = sales * ccRate;
          const ccFraud = sales * cbRate;
          const totalCc = ccFixed + ccVar + ccFraud;

          const totalCrypto = sales * cryptoRate;
          const savings = totalCc - totalCrypto;
          const cutPct = totalCc > 0 ? (savings / totalCc) * 100 : 0;

          setDisp('annual_merchant_savings', '$' + Math.round(savings).toLocaleString() + ' / yr');
          setDisp('net_fee_reduction_pct', cutPct.toFixed(1) + '% Fee Cut');
          setDisp('credit_card_total_fees', '$' + Math.round(totalCc).toLocaleString() + ' / yr');
          setDisp('crypto_processing_cost', '$' + Math.round(totalCrypto).toLocaleString() + ' / yr');
        """
    },
    {
        "slug": "smart-contract-gas-limit",
        "category": "crypto",
        "name": "Smart Contract EVM Opcode Gas Execution Cost Analyzer",
        "description": "Calculate granular EVM opcode execution gas (SSTORE, SLOAD, KECCAK256, LOG, Memory expansion) for Solidity smart contracts.",
        "hero_badge": "Solidity Engineering • EVM Gas Optimization",
        "formula_display": "Total Gas = 21,000 Base + Σ (Opcode Cost) + Memory Expansion Gas",
        "fields": [
            {"id": "storage_writes_sstore_new", "label": "New Storage Slots Written (Zero to Non-Zero)", "default": 2, "min": 0, "max": 50, "step": 1, "hint": "SSTORE (20,000 gas each for new storage slot)"},
            {"id": "storage_updates_sstore_mod", "label": "Existing Storage Slots Modified", "default": 1, "min": 0, "max": 50, "step": 1, "hint": "SSTORE (2,900 gas each for non-zero to non-zero)"},
            {"id": "storage_reads_sload", "label": "Storage Read Operations (SLOAD)", "default": 4, "min": 0, "max": 100, "step": 1, "hint": "Cold SLOAD = 2,100 gas, Warm SLOAD = 100 gas"},
            {"id": "emitted_events_count", "label": "Emitted Events / Logs (LOG3)", "default": 1, "min": 0, "max": 10, "step": 1, "hint": "Event emission with 2-3 indexed topics (~1,500 gas)"}
        ],
        "metrics": [
            {"id": "total_execution_gas", "label": "Total EVM Execution Gas", "default_display": "73,800 Gas", "highlight": True},
            {"id": "storage_cost_percentage", "label": "Storage Dominance Ratio", "default_display": "67.8% of Total Gas (State Storage)", "highlight": True},
            {"id": "cost_at_30_gwei_usd", "label": "Execution Cost @ 30 Gwei ($3,200 ETH)", "default_display": "$7.08 USD"},
            {"id": "optimization_potential", "label": "Gas Packing Optimization Potential", "default_display": "Save ~20,000 Gas by Packing Structs"}
        ],
        "proof_steps": [
            {"step_title": "EVM Base Transaction Overhead", "step_text": "Every Ethereum transaction carries a mandatory base gas cost of 21,000 gas units."},
            {"step_title": "Storage Opcode Dominance", "step_text": "Writing 2 brand new 32-byte storage slots (SSTORE) costs 2 × 20,000 = 40,000 gas. Modifying 1 slot costs 2,900 gas. Storage reads (SLOAD) = 4 × 2,100 = 8,400 gas."},
            {"step_title": "Event Logging & Arithmetic", "step_text": "Emitting 1 LOG3 event costs ~1,500 gas. Internal opcode execution and memory expansion adds ~2,000 gas."},
            {"step_title": "Total Gas Budget", "step_text": "Total = 21,000 + 40,000 + 2,900 + 8,400 + 1,500 = 73,800 gas units ($7.08 at 30 Gwei and $3,200/ETH)."}
        ],
        "faqs": [
            {"q": "Why is EVM storage (SSTORE) so expensive compared to memory (MSTORE)?", "a": "SSTORE permanently writes 32 bytes of data to the global Ethereum state trie across tens of thousands of validator nodes worldwide, whereas memory (MSTORE) is temporary and wiped clean the instant the transaction finishes execution."},
            {"q": "What is variable packing in Solidity?", "a": "Solidity stores data in 32-byte slots. Packing multiple smaller types (e.g. uint128 + uint128, or uint64 + address) into a single 32-byte slot allows you to write multiple variables in a single 20,000-gas SSTORE instead of two separate writes."}
        ],
        "js_logic": """
          const sstoreNew = getNum('storage_writes_sstore_new');
          const sstoreMod = getNum('storage_updates_sstore_mod');
          const sload = getNum('storage_reads_sload');
          const events = getNum('emitted_events_count');

          const base = 21000;
          const newCost = sstoreNew * 20000;
          const modCost = sstoreMod * 2900;
          const readCost = sload * 2100;
          const eventCost = events * 1500;
          const totalGas = base + newCost + modCost + readCost + eventCost;

          const storageGas = newCost + modCost;
          const storagePct = totalGas > 0 ? (storageGas / totalGas) * 100 : 0;
          const usd = (totalGas * 30 * 1e-9) * 3200;

          setDisp('total_execution_gas', totalGas.toLocaleString() + ' Gas');
          setDisp('storage_cost_percentage', storagePct.toFixed(1) + '% of Total Gas');
          setDisp('cost_at_30_gwei_usd', '$' + usd.toFixed(2) + ' USD');
          setDisp('optimization_potential', sstoreNew > 1 ? 'Save ~20,000 Gas by Variable Packing' : 'Optimal Storage Allocation');
        """
    },
    {
        "slug": "yield-farming-reinvest-frequency",
        "category": "crypto",
        "name": "Optimal Compounding Frequency for DeFi Yield Farming Calculator",
        "description": "Calculate the mathematically optimal reinvestment frequency that maximizes compound APY while minimizing transaction gas harvesting fees.",
        "hero_badge": "DeFi Yield Optimization • Game Theory",
        "formula_display": "Optimal Days Between Harvests = √[(2 · Gas Cost in USD) / (Principal · Daily APR · Daily Yield)]",
        "fields": [
            {"id": "farming_principal_usd", "label": "Farmed Capital Value ($ USD)", "default": 15000, "prefix": "$", "min": 250, "max": 1000000, "step": 500, "hint": "Principal deposited in liquidity farm"},
            {"id": "nominal_farm_apr_pct", "label": "Nominal Stated Farm APR (%)", "default": 45.0, "suffix": "%", "min": 5, "max": 500, "step": 5, "hint": "Uncompounded reward token emission APR"},
            {"id": "harvest_gas_cost_usd", "label": "Harvest & Re-stake Gas Fee ($)", "default": 6.50, "prefix": "$", "min": 0.01, "max": 100, "step": 0.5, "hint": "All-in transaction cost to claim, swap, and restake"}
        ],
        "metrics": [
            {"id": "optimal_reinvest_interval", "label": "Optimal Compounding Interval", "default_display": "Every 4.8 Days", "highlight": True},
            {"id": "net_apy_after_gas", "label": "Net Effective APY (After Gas)", "default_display": "53.8% APY", "highlight": True},
            {"id": "annual_harvest_gas_cost", "label": "Total Annual Gas Spend", "default_display": "$494.00 / yr", "highlight": True},
            {"id": "compounding_boost_usd", "label": "Net Dollar Value Added by Compounding", "default_display": "+$1,320.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Tradeoff Invariant", "step_text": "Compounding too frequently wastes excessive capital on gas fees. Compounding too infrequently loses compound interest."},
            {"step_title": "Economic Order Model for Yield", "step_text": "Optimal Interval T (days) = √[(2 × Gas) / (Principal × (APR/365)²)]."},
            {"step_title": "Parameter Evaluation", "step_text": "For $15,000 at 45% APR ($18.49 daily yield) and $6.50 gas: Optimal Interval = 4.8 days (roughly once every 5 days)."},
            {"step_title": "Net Economic Alpha", "step_text": "Harvesting every 5 days yields a 53.8% net APY (accounting for $494/year in gas), beating simple 45% APR by over $1,320/year."}
        ],
        "faqs": [
            {"q": "Why is auto-compounding via yield aggregators (Beefy) superior?", "a": "Yield aggregators pool thousands of users' deposits and execute a single shared harvest transaction, dividing the gas cost across the entire pool and compounding rewards multiple times per day at virtually zero cost per user."},
            {"q": "Should I compound daily if farming on Polygon or Arbitrum?", "a": "On low-fee Layer 2 networks where gas is pennies ($0.03), you can profitably compound daily or every other day even with smaller balances ($1,000+)."}
        ],
        "js_logic": """
          const p = getNum('farming_principal_usd');
          const apr = (getNum('nominal_farm_apr_pct') || 45) / 100;
          const gas = getNum('harvest_gas_cost_usd');

          const dailyR = apr / 365;
          const optimalDays = dailyR > 0 && p > 0 ? Math.sqrt((2 * gas) / (p * Math.pow(dailyR, 1.8))) : 7;
          const clampedDays = Math.max(0.5, Math.min(180, optimalDays));

          const compoundsPerYear = 365 / clampedDays;
          const grossApy = Math.pow(1 + (apr / compoundsPerYear), compoundsPerYear) - 1;
          const totalGas = compoundsPerYear * gas;
          const netYield = (p * grossApy) - totalGas;
          const netApy = p > 0 ? (netYield / p) * 100 : 0;
          const boost = netYield - (p * apr);

          setDisp('optimal_reinvest_interval', 'Every ' + clampedDays.toFixed(1) + ' Days');
          setDisp('net_apy_after_gas', netApy.toFixed(1) + '% APY');
          setDisp('annual_harvest_gas_cost', '$' + Math.round(totalGas).toLocaleString() + ' / yr');
          setDisp('compounding_boost_usd', (boost >= 0 ? '+$' : '-$') + Math.abs(Math.round(boost)).toLocaleString() + ' / yr');
        """
    },
    {
        "slug": "flash-loan-arbitrage-net",
        "category": "crypto",
        "name": "DeFi Flash Loan Arbitrage Spread vs Net Profitability Calculator",
        "description": "Calculate uncollateralized flash loan protocol fees (Aave 0.05%, Balancer 0%), DEX swap gas, routing slippage, and net transaction profit.",
        "hero_badge": "DeFi Engineering • Flash Loans",
        "formula_display": "Net Profit = Arbitrage Spread ($) - Flash Loan Fee ($) - Total Gas Fees ($)",
        "fields": [
            {"id": "flash_borrow_amount_usd", "label": "Flash Loan Borrowed Capital ($)", "default": 250000, "prefix": "$", "min": 10000, "max": 10000000, "step": 25000, "hint": "Principal borrowed in single transaction block"},
            {"id": "gross_arbitrage_spread_pct", "label": "Gross Price Spread Across DEXs (%)", "default": 0.45, "suffix": "%", "min": 0.05, "max": 5.0, "step": 0.05, "hint": "Price difference between Pool A (buy) and Pool B (sell)"},
            {"id": "flash_protocol_fee_pct", "label": "Flash Loan Protocol Fee (%)", "default": 0.05, "suffix": "%", "min": 0, "max": 0.1, "step": 0.01, "hint": "Aave = 0.05% (5 bps), Balancer = 0%, Uniswap v3 = 0.05%"},
            {"id": "total_execution_gas_usd", "label": "Estimated Atomic Gas Cost ($ USD)", "default": 85.0, "prefix": "$", "min": 5, "max": 1000, "step": 5, "hint": "Complex multi-DEX swap execution gas"}
        ],
        "metrics": [
            {"id": "net_atomic_profit_usd", "label": "Net Realized Profit", "default_display": "$915.00", "highlight": True},
            {"id": "gross_arbitrage_revenue", "label": "Gross Arbitrage Revenue", "default_display": "$1,125.00", "highlight": True},
            {"id": "flash_loan_fee_cost", "label": "Flash Loan Fee Paid to Protocol", "default_display": "$125.00 (0.05%)"},
            {"id": "execution_status", "label": "Transaction Viability", "default_display": "Highly Profitable Arbitrage"}
        ],
        "proof_steps": [
            {"step_title": "Gross Arbitrage Gain", "step_text": "Gross Profit = Borrowed $250,000 × 0.45% spread = $1,125.00."},
            {"step_title": "Flash Loan Fee Deduction", "step_text": "Aave 0.05% fee = $250,000 × 0.0005 = $125.00."},
            {"step_title": "Atomic Net Profit Reconciliation", "step_text": "Net Profit = $1,125.00 - $125.00 (loan fee) - $85.00 (EVM gas) = $915.00 in instant risk-free profit."},
            {"step_title": "Zero Collateral Risk Invariant", "step_text": "If the price moves before execution and profit drops below $0, the smart contract automatically reverts the entire transaction, losing only the gas fee."}
        ],
        "faqs": [
            {"q": "What is a DeFi Flash Loan?", "a": "A flash loan is an uncollateralized loan where borrowing, arbitrage swapping across multiple decentralized exchanges, and full principal repayment happen within a single atomic Ethereum transaction block."},
            {"q": "Can you lose money on a flash loan?", "a": "You cannot lose borrowed capital because the smart contract reverts the transaction if debt is not repaid. However, you can lose transaction gas fees ($20-$100+) if your transaction reverts or gets front-run by an MEV searcher bot."}
        ],
        "js_logic": """
          const borrow = getNum('flash_borrow_amount_usd');
          const spread = (getNum('gross_arbitrage_spread_pct') || 0.45) / 100;
          const feePct = (getNum('flash_protocol_fee_pct') || 0.05) / 100;
          const gas = getNum('total_execution_gas_usd');

          const gross = borrow * spread;
          const loanFee = borrow * feePct;
          const net = gross - loanFee - gas;

          setDisp('net_atomic_profit_usd', (net >= 0 ? '$' : '-$') + Math.abs(Math.round(net)).toLocaleString());
          setDisp('gross_arbitrage_revenue', '$' + Math.round(gross).toLocaleString());
          setDisp('flash_loan_fee_cost', '$' + loanFee.toFixed(2) + ' (' + (feePct * 100).toFixed(2) + '%)');
          setDisp('execution_status', net > 100 ? 'Highly Profitable Arbitrage' : (net > 0 ? 'Marginal Profit (Tight)' : 'UNPROFITABLE (Reverts)'));
        """
    },
    {
        "slug": "dex-aggregator-split-routing",
        "category": "crypto",
        "name": "Multi-Route DEX Aggregator Optimal Trade Split Calculator",
        "description": "Calculate optimal trade splitting across multiple liquidity pools (Uniswap, Curve, Balancer) to minimize price impact on large token swaps.",
        "hero_badge": "DEX Aggregation • Split Routing",
        "formula_display": "Optimal Split: Allocate trade proportional to pool liquidity depths (x_i / Σ x)",
        "fields": [
            {"id": "total_swap_size_usd", "label": "Total Swap Size ($ USD)", "default": 100000, "prefix": "$", "min": 5000, "max": 10000000, "step": 10000, "hint": "Large token trade amount"},
            {"id": "pool1_liquidity_usd", "label": "Pool A Reserve Liquidity ($)", "default": 400000, "prefix": "$", "min": 25000, "max": 20000000, "step": 25000, "hint": "Uniswap v3 primary pool"},
            {"id": "pool2_liquidity_usd", "label": "Pool B Reserve Liquidity ($)", "default": 250000, "prefix": "$", "min": 25000, "max": 20000000, "step": 25000, "hint": "SushiSwap / Curve secondary pool"}
        ],
        "metrics": [
            {"id": "split_allocation_ratio", "label": "Optimal Order Split", "default_display": "61.5% Pool A / 38.5% Pool B", "highlight": True},
            {"id": "aggregate_price_impact", "label": "Aggregated Blended Price Impact", "default_display": "13.3%", "highlight": True},
            {"id": "single_route_impact", "label": "Worst Single-Route Impact (No Split)", "default_display": "20.0% Impact (Pool A only)", "highlight": True},
            {"id": "dollar_slippage_saved", "label": "Value Preserved via Split Routing", "default_display": "$6,700.00 Saved"}
        ],
        "proof_steps": [
            {"step_title": "Total Liquidity Depth", "step_text": "Combined Liquidity = $400,000 + $250,000 = $650,000."},
            {"step_title": "Optimal Convex Split Allocation", "step_text": "To equalize marginal price impact: Route A = $100k × (400k / 650k) = $61,538. Route B = $100k × (250k / 650k) = $38,462."},
            {"step_title": "Aggregated Price Impact Reduction", "step_text": "Single Pool A impact = $100k / ($400k + $100k) = 20.0%. Split Route Impact = 13.3%. Split routing saves $6,700 in execution slippage."}
        ],
        "faqs": [
            {"q": "How do DEX aggregators (1inch, ParaSwap) work?", "a": "Aggregators query dozens of liquidity pools in parallel and use dynamic programming algorithms to find the mathematical path of least price resistance, splitting orders across multiple routes and hops in a single transaction."},
            {"q": "Does split routing cost more gas?", "a": "Yes. Splitting an order across three DEX pools requires three separate smart contract calls, increasing EVM gas by roughly 40% to 60%, but on large trades ($50k+) the slippage savings far outweigh the $5 gas difference."}
        ],
        "js_logic": """
          const swap = getNum('total_swap_size_usd');
          const p1 = getNum('pool1_liquidity_usd');
          const p2 = getNum('pool2_liquidity_usd');

          const totalPool = p1 + p2;
          const share1 = totalPool > 0 ? (p1 / totalPool) : 0.6;
          const share2 = 1 - share1;

          const trade1 = swap * share1;
          const trade2 = swap * share2;

          const impact1 = p1 > 0 ? (trade1 / (p1 + trade1)) * 100 : 0;
          const impact2 = p2 > 0 ? (trade2 / (p2 + trade2)) * 100 : 0;
          const blendedImpact = (impact1 * share1) + (impact2 * share2);

          const singleImpact = p1 > 0 ? (swap / (p1 + swap)) * 100 : 20;
          const savedDollars = swap * ((singleImpact - blendedImpact) / 100);

          setDisp('split_allocation_ratio', (share1 * 100).toFixed(1) + '% Pool A / ' + (share2 * 100).toFixed(1) + '% Pool B');
          setDisp('aggregate_price_impact', blendedImpact.toFixed(1) + '%');
          setDisp('single_route_impact', singleImpact.toFixed(1) + '% (No Split)');
          setDisp('dollar_slippage_saved', '$' + Math.round(savedDollars).toLocaleString() + ' Saved');
        """
    },
    {
        "slug": "crypto-portfolio-sharpe-ratio",
        "category": "crypto",
        "name": "Crypto Portfolio Sharpe Ratio & Value at Risk (VaR 95%) Calculator",
        "description": "Calculate risk-adjusted Sharpe Ratio, downside Sortino Ratio, and 95% Parametric Value at Risk (VaR) for multi-asset cryptocurrency portfolios.",
        "hero_badge": "Quantitative Risk • Portfolio Analytics",
        "formula_display": "Sharpe Ratio = (Expected Return - Risk-Free Rate) / Portfolio Volatility (σ)",
        "fields": [
            {"id": "portfolio_value_usd", "label": "Total Portfolio Capital ($ USD)", "default": 100000, "prefix": "$", "min": 1000, "max": 100000000, "step": 5000, "hint": "Current total net asset value"},
            {"id": "annual_expected_return_pct", "label": "Annual Expected Portfolio Return (%)", "default": 42.0, "suffix": "%", "min": -50, "max": 300, "step": 5, "hint": "Historical or projected 12-month return"},
            {"id": "annual_volatility_sigma_pct", "label": "Annualized Volatility (σ %)", "default": 55.0, "suffix": "%", "min": 10, "max": 150, "step": 5, "hint": "Standard deviation of returns (BTC ~50%, ETH ~65%)"},
            {"id": "risk_free_rate_pct", "label": "Risk-Free Treasury Benchmark (%)", "default": 4.5, "suffix": "%", "min": 0, "max": 10, "step": 0.25, "hint": "Current 3-month U.S. Treasury Bill yield"}
        ],
        "metrics": [
            {"id": "calculated_sharpe_ratio", "label": "Portfolio Sharpe Ratio", "default_display": "0.68", "highlight": True},
            {"id": "daily_var_95_usd", "label": "1-Day 95% Value at Risk (VaR)", "default_display": "$5,660.00 (5.66%)", "highlight": True},
            {"id": "monthly_var_95_usd", "label": "1-Month 95% Value at Risk", "default_display": "$17,800.00 (17.8%)"},
            {"id": "risk_adjusted_grade", "label": "Risk-Adjusted Performance Grade", "default_display": "Moderate Alpha (High Volatility)"}
        ],
        "proof_steps": [
            {"step_title": "Excess Return Over Cash", "step_text": "Excess Return = 42.0% - 4.5% Risk-Free = 37.5%."},
            {"step_title": "Sharpe Ratio Formulation", "step_text": "Sharpe Ratio = 37.5% / 55.0% = 0.6818. A Sharpe ratio below 1.0 indicates returns are heavily driven by sheer market volatility rather than genuine alpha."},
            {"step_title": "Daily Parametric Value at Risk (VaR 95%)", "step_text": "Daily Volatility = 55% / √365 = 2.879%. At 95% confidence (Z = 1.645): Daily VaR = 1.645 × 2.879% × $100,000 = $4,736.00."},
            {"step_title": "Downside Tail Risk", "step_text": "On 95 out of 100 days, daily portfolio loss will not exceed $4,736. On the remaining 5 days, losses may be substantially higher."}
        ],
        "faqs": [
            {"q": "What is considered a good Sharpe Ratio in crypto?", "a": "A Sharpe ratio above 1.0 is considered good; above 2.0 is very good; above 3.0 is elite. Many buy-and-hold crypto portfolios exhibit Sharpe ratios between 0.6 and 1.1 due to severe 70%+ drawdowns."},
            {"q": "Why is the Sortino Ratio often preferred over the Sharpe Ratio for crypto?", "a": "The Sharpe Ratio penalizes upside volatility equally alongside downside crashes. The Sortino Ratio penalizes only downside volatility, giving a fairer score to asymmetric assets like Bitcoin."}
        ],
        "js_logic": """
          const val = getNum('portfolio_value_usd');
          const ret = getNum('annual_expected_return_pct');
          const sigma = getNum('annual_volatility_sigma_pct');
          const rf = getNum('risk_free_rate_pct');

          const excess = ret - rf;
          const sharpe = sigma > 0 ? (excess / sigma) : 0;

          const dailySigma = (sigma / 100) / Math.sqrt(365);
          const dailyVarPct = 1.645 * dailySigma;
          const dailyVarUsd = val * dailyVarPct;
          const monthlyVarUsd = dailyVarUsd * Math.sqrt(21);

          let grade = 'Poor Risk-Adjusted Alpha';
          if (sharpe >= 2.0) grade = 'Elite Risk-Adjusted Alpha';
          else if (sharpe >= 1.0) grade = 'Strong Risk-Adjusted Alpha';
          else if (sharpe >= 0.5) grade = 'Moderate Alpha (High Volatility)';

          setDisp('calculated_sharpe_ratio', sharpe.toFixed(2));
          setDisp('daily_var_95_usd', '$' + Math.round(dailyVarUsd).toLocaleString() + ' (' + (dailyVarPct * 100).toFixed(2) + '%)');
          setDisp('monthly_var_95_usd', '$' + Math.round(monthlyVarUsd).toLocaleString() + ' (' + ((monthlyVarUsd / val) * 100).toFixed(1) + '%)');
          setDisp('risk_adjusted_grade', grade);
        """
    }
]
