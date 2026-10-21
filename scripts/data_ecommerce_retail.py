"""
scripts/data_ecommerce_retail.py
25 High-Value E-Commerce, Direct-to-Consumer (DTC), Retail Merchandising & Paid Media Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

ECOMMERCE_CALCULATORS = [
    {
        "slug": "landed-cost-unit-margin",
        "category": "ecommerce",
        "name": "Total Landed Cost & Gross Margin Calculator",
        "description": "Calculate true per-unit landed cost factoring in FOB factory pricing, ocean freight, customs tariffs, port fees, and drayage to establish profitable retail pricing.",
        "hero_badge": "DTC Supply Chain • Unit Economics",
        "formula_display": "Landed Unit Cost = FOB + (Freight + Tariffs + Port + Drayage) / Total Units | Gross Margin % = [(Retail Price - Landed Cost) / Retail Price] × 100",
        "fields": [
            {"id": "production_run_units", "label": "Production Run Volume (Units)", "default": 5000, "suffix": "units", "min": 100, "max": 500000, "step": 100, "hint": "Total quantity manufactured in production batch"},
            {"id": "fob_unit_cost", "label": "FOB Factory Unit Cost", "default": 8.50, "suffix": "$", "min": 0.50, "max": 1000, "step": 0.25, "hint": "Free On Board factory cost per unit"},
            {"id": "ocean_air_freight_total", "label": "Total International Freight", "default": 4200, "suffix": "$", "min": 0, "max": 100000, "step": 100, "hint": "Full container load (FCL) or air freight shipping cost"},
            {"id": "customs_duty_rate_pct", "label": "Customs Tariff / Duty Rate (%)", "default": 7.5, "suffix": "%", "min": 0, "max": 100, "step": 0.5, "hint": "Harmonized Tariff Schedule (HTS) import duty rate"},
            {"id": "port_and_drayage_total", "label": "Port Customs Clearance & Drayage", "default": 1850, "suffix": "$", "min": 0, "max": 50000, "step": 50, "hint": "Customs brokerage, terminal handling, and warehouse trucking"},
            {"id": "target_retail_price", "label": "Target DTC Retail Price", "default": 38.00, "suffix": "$", "min": 1, "max": 2000, "step": 1, "hint": "Intended consumer sales price per unit"}
        ],
        "metrics": [
            {"id": "landed_unit_cost", "label": "True Landed Cost Per Unit", "default_display": "$10.35 / unit", "highlight": True},
            {"id": "gross_profit_per_unit", "label": "Unit Gross Profit Contribution", "default_display": "$27.65 / unit", "highlight": True},
            {"id": "gross_margin_pct", "label": "Gross Profit Margin (%)", "default_display": "72.8%", "highlight": True},
            {"id": "total_import_overhead", "label": "Total Freight & Duty Surcharge", "default_display": "$9,237.50 Total"}
        ],
        "proof_steps": [
            {"step_title": "Customs Tariff Valuation", "step_text": "Customs Duty = Units × FOB Unit Price × Duty Rate = 5,000 × $8.50 × 0.075 = $42,500 × 7.5% = $3,187.50."},
            {"step_title": "Total Logistics & Clearance Burden", "step_text": "Total Overhead = International Freight ($4,200) + Customs Duty ($3,187.50) + Port & Drayage ($1,850) = $9,237.50."},
            {"step_title": "Per-Unit Landed Cost Derivation", "step_text": "Unit Overhead = $9,237.50 / 5,000 units = $1.8475. Total Landed Cost = FOB ($8.50) + $1.8475 = $10.3475 ≈ $10.35/unit."},
            {"step_title": "DTC Gross Margin & Markup", "step_text": "Gross Profit = $38.00 - $10.35 = $27.65. Margin % = ($27.65 / $38.00) × 100 = 72.8%. Markup Multiple = $38.00 / $10.35 = 3.67×."}
        ],
        "faqs": [
            {"q": "What is the difference between FOB and Landed Cost?", "a": "FOB (Free On Board) is solely the manufacturing price paid to the overseas supplier at the port of departure. Landed cost reflects the total real expense to bring the goods into your domestic fulfillment warehouse, including ocean container shipping, bunker fuel surcharges, import customs duties, marine insurance, and domestic trucking."},
            {"q": "What is a healthy gross margin for e-commerce brands?", "a": "Healthy DTC brands typically target gross margins between 65% and 80% to absorb rising customer acquisition costs (CAC on Meta, Google, and TikTok), return logistics, and pick-and-pack fulfillment fees."}
        ],
        "js_logic": """
          const units = getNum('production_run_units');
          const fob = getNum('fob_unit_cost');
          const freight = getNum('ocean_air_freight_total');
          const dutyPct = getNum('customs_duty_rate_pct');
          const port = getNum('port_and_drayage_total');
          const retail = getNum('target_retail_price');

          if (units > 0) {
            const dutyTotal = units * fob * (dutyPct / 100);
            const totalOverhead = freight + dutyTotal + port;
            const unitOverhead = totalOverhead / units;
            const landedCost = fob + unitOverhead;
            const grossProfit = retail - landedCost;
            const marginPct = retail > 0 ? (grossProfit / retail) * 100 : 0;

            setMetric('landed_unit_cost', '$' + landedCost.toFixed(2) + ' / unit');
            setMetric('gross_profit_per_unit', '$' + grossProfit.toFixed(2) + ' / unit');
            setMetric('gross_margin_pct', marginPct.toFixed(1) + '%');
            setMetric('total_import_overhead', '$' + totalOverhead.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          }
        """
    },
    {
        "slug": "inventory-turnover-days-sales",
        "category": "ecommerce",
        "name": "Inventory Turnover Ratio & Days Sales of Inventory (DSI) Calculator",
        "description": "Evaluate retail merchandising velocity and working capital efficiency by calculating inventory turnover ratio and average days required to sell through inventory.",
        "hero_badge": "Working Capital • Inventory Velocity",
        "formula_display": "Turnover Ratio = Annual COGS / Average Inventory | DSI = (Average Inventory / Annual COGS) × 365 Days",
        "fields": [
            {"id": "annual_cogs", "label": "Annual Cost of Goods Sold (COGS)", "default": 750000, "suffix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Total wholesale inventory cost sold over the trailing 12 months"},
            {"id": "beginning_inventory_value", "label": "Beginning Inventory Value ($ Cost)", "default": 140000, "suffix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Inventory valuation at the start of the period"},
            {"id": "ending_inventory_value", "label": "Ending Inventory Value ($ Cost)", "default": 160000, "suffix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Inventory valuation at the end of the period"}
        ],
        "metrics": [
            {"id": "inventory_turnover_ratio", "label": "Inventory Turnover Ratio", "default_display": "5.00× per year", "highlight": True},
            {"id": "days_sales_inventory_dsi", "label": "Days Sales of Inventory (DSI)", "default_display": "73.0 Days", "highlight": True},
            {"id": "average_inventory_cost", "label": "Average Inventory Value Held", "default_display": "$150,000", "highlight": True},
            {"id": "velocity_classification", "label": "Merchandising Health Rating", "default_display": "Optimal DTC Velocity (4× - 6×)"}
        ],
        "proof_steps": [
            {"step_title": "Average Inventory Calculation", "step_text": "Average Inventory = (Beginning Inventory + Ending Inventory) / 2 = ($140,000 + $160,000) / 2 = $150,000."},
            {"step_title": "Turnover Ratio Derivation", "step_text": "Turnover Ratio = Annual COGS / Average Inventory = $750,000 / $150,000 = 5.00 turns per year."},
            {"step_title": "Days Sales of Inventory (DSI)", "step_text": "DSI = 365 / Turnover Ratio = 365 / 5.00 = 73.0 days of inventory on hand."},
            {"step_title": "Capital Velocity Insight", "step_text": "A turnover of 5.0× indicates that capital invested in inventory is fully converted back to liquid cash every 73 days, reducing carrying costs and deadstock risks."}
        ],
        "faqs": [
            {"q": "What is a good inventory turnover ratio for retail e-commerce?", "a": "For most DTC and retail brands, an inventory turnover ratio between 4× and 6× per year (60 to 90 days DSI) is considered optimal. A ratio below 3× indicates overstocking and locked-up cash, while a ratio above 8× risks frequent stockouts and lost revenue."},
            {"q": "Why is COGS used instead of total sales revenue in turnover calculations?", "a": "Inventory is recorded on the balance sheet at wholesale cost, not retail sales price. Comparing retail sales to inventory at cost artificially inflates turnover due to retail markup."}
        ],
        "js_logic": """
          const cogs = getNum('annual_cogs');
          const beg = getNum('beginning_inventory_value');
          const end = getNum('ending_inventory_value');

          const avgInv = (beg + end) / 2;
          if (avgInv > 0) {
            const turns = cogs / avgInv;
            const dsi = (365 / turns);

            let rating = 'Slow Turnover (< 3×)';
            if (turns >= 4 && turns <= 6) rating = 'Optimal DTC Velocity (4× - 6×)';
            else if (turns > 6 && turns <= 10) rating = 'High Velocity (> 6×)';
            else if (turns > 10) rating = 'Extreme Velocity (Stockout Risk)';

            setMetric('inventory_turnover_ratio', turns.toFixed(2) + '× per year');
            setMetric('days_sales_inventory_dsi', dsi.toFixed(1) + ' Days');
            setMetric('average_inventory_cost', '$' + Math.round(avgInv).toLocaleString());
            setMetric('velocity_classification', rating);
          }
        """
    },
    {
        "slug": "cart-abandonment-revenue-loss",
        "category": "ecommerce",
        "name": "Shopping Cart Abandonment & Recovery Opportunity Calculator",
        "description": "Quantify uncaptured revenue lost to abandoned online checkouts and calculate potential monthly revenue recovered through automated SMS and email nurture flows.",
        "hero_badge": "Conversion Rate Optimization • Abandonment",
        "formula_display": "Lost Revenue = Initiated Checkouts × Abandonment Rate × AOV | Recovered = Lost Revenue × Recovery Rate",
        "fields": [
            {"id": "monthly_checkout_initiations", "label": "Monthly Initiated Checkouts", "default": 4500, "suffix": "checkouts", "min": 100, "max": 500000, "step": 100, "hint": "Shoppers who reach step 1 of checkout"},
            {"id": "abandonment_rate_pct", "label": "Cart Abandonment Rate (%)", "default": 69.8, "suffix": "%", "min": 20, "max": 95, "step": 0.5, "hint": "Global e-commerce average is approximately 70%"},
            {"id": "average_order_value_aov", "label": "Average Order Value (AOV)", "default": 85.00, "suffix": "$", "min": 5, "max": 2000, "step": 1, "hint": "Average total checkout transaction value"},
            {"id": "email_sms_recovery_pct", "label": "Estimated Flow Recovery Rate (%)", "default": 8.5, "suffix": "%", "min": 1, "max": 35, "step": 0.5, "hint": "Percentage of abandoned sessions recovered via automated flows"}
        ],
        "metrics": [
            {"id": "monthly_lost_revenue", "label": "Monthly Abandoned Revenue", "default_display": "$266,985 / mo", "highlight": True},
            {"id": "potential_recovered_revenue", "label": "Potential Recovered Revenue", "default_display": "$22,693 / mo", "highlight": True},
            {"id": "annual_recovered_opportunity", "label": "Annualized Recovered Cashflow", "default_display": "$272,324 / year", "highlight": True},
            {"id": "abandoned_orders_count", "label": "Monthly Abandoned Carts", "default_display": "3,141 Orders"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Abandoned Sessions", "step_text": "Abandoned Orders = Initiated Checkouts × Abandonment Rate = 4,500 × 69.8% = 3,141 carts left uncompleted."},
            {"step_title": "Gross Revenue Lost", "step_text": "Gross Lost Revenue = 3,141 carts × $85.00 AOV = $266,985 monthly abandoned pipeline."},
            {"step_title": "Klaviyo / Omnisend Recovery Potential", "step_text": "Recovered Revenue = $266,985 × 8.5% recovery rate = $22,693.73 per month in reclaimed sales."},
            {"step_title": "Annualized Top-Line Impact", "step_text": "Annual Impact = $22,693.73 × 12 months = $272,324.76 incremental annual revenue with zero additional ad spend."}
        ],
        "faqs": [
            {"q": "What is the industry benchmark for cart abandonment?", "a": "According to the Baymard Institute, the average documented online shopping cart abandonment rate is 70.19%. Leading friction points include unexpected shipping fees, mandatory account creation, and slow payment options."},
            {"q": "What is a realistic recovery rate for abandoned cart email sequences?", "a": "High-performing 3-step email and SMS abandonment sequences typically recover between 5% and 12% of abandoned checkouts, providing immediate high-margin revenue."}
        ],
        "js_logic": """
          const checkouts = getNum('monthly_checkout_initiations');
          const abandPct = getNum('abandonment_rate_pct');
          const aov = getNum('average_order_value_aov');
          const recPct = getNum('email_sms_recovery_pct');

          const abandOrders = checkouts * (abandPct / 100);
          const lostRev = abandOrders * aov;
          const recRev = lostRev * (recPct / 100);
          const annualRec = recRev * 12;

          setMetric('monthly_lost_revenue', '$' + Math.round(lostRev).toLocaleString() + ' / mo');
          setMetric('potential_recovered_revenue', '$' + Math.round(recRev).toLocaleString() + ' / mo');
          setMetric('annual_recovered_opportunity', '$' + Math.round(annualRec).toLocaleString() + ' / year');
          setMetric('abandoned_orders_count', Math.round(abandOrders).toLocaleString() + ' Orders');
        """
    },
    {
        "slug": "gmroi-retail-merchandising",
        "category": "ecommerce",
        "name": "Gross Margin Return on Investment (GMROI) Calculator",
        "description": "Calculate Gross Margin Return on Investment (GMROI) to measure how many gross profit dollars every dollar of inventory investment generates.",
        "hero_badge": "Merchandising Finance • Inventory ROI",
        "formula_display": "GMROI = Gross Margin $ / Average Inventory Cost = (Gross Margin % × Sales Revenue) / Average Inventory Cost",
        "fields": [
            {"id": "annual_sales_revenue", "label": "Annual Retail Sales Revenue", "default": 1200000, "suffix": "$", "min": 10000, "max": 50000000, "step": 10000, "hint": "Total top-line sales generated by the product line"},
            {"id": "gross_margin_percentage", "label": "Product Line Gross Margin (%)", "default": 55.0, "suffix": "%", "min": 5, "max": 95, "step": 0.5, "hint": "Gross margin percentage after product COGS"},
            {"id": "average_inventory_cost_basis", "label": "Average Inventory Investment (Cost)", "default": 200000, "suffix": "$", "min": 5000, "max": 10000000, "step": 5000, "hint": "Average working capital tied up in inventory at cost"}
        ],
        "metrics": [
            {"id": "gmroi_ratio", "label": "Gross Margin ROI (GMROI)", "default_display": "$3.30 ($330%)", "highlight": True},
            {"id": "total_gross_profit", "label": "Total Gross Profit Generated", "default_display": "$660,000", "highlight": True},
            {"id": "inventory_turns_equivalent", "label": "Implied Inventory Turns", "default_display": "2.70 Turns / Year", "highlight": True},
            {"id": "performance_tier", "label": "Merchandising Performance Tier", "default_display": "Strong Profit Driver (> $3.00)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Profit Dollar Generation", "step_text": "Gross Margin $ = Revenue × Margin % = $1,200,000 × 55.0% = $660,000 total gross profit."},
            {"step_title": "GMROI Ratio Calculation", "step_text": "GMROI = Gross Margin $ / Average Inventory Cost = $660,000 / $200,000 = $3.30 per dollar invested (330%)."},
            {"step_title": "Turnover Breakdown Relationship", "step_text": "COGS = $1,200,000 × (1 - 0.55) = $540,000. Inventory Turns = $540,000 / $200,000 = 2.70 turns. GMROI = 2.70 turns × [55% / (1 - 55%)] = $3.30."},
            {"step_title": "Capital Productivity Evaluation", "step_text": "For every $1.00 held in warehouse inventory, the brand extracts $3.30 in gross margin annually."}
        ],
        "faqs": [
            {"q": "What is a good GMROI in retail merchandising?", "a": "A GMROI of 1.0 ($1.00) means the inventory breaks even on cost. Retailers generally target a GMROI of at least $2.00 to cover operating overhead. Elite e-commerce brands achieve GMROIs between $3.00 and $4.50."},
            {"q": "How does GMROI differ from Gross Margin %?", "a": "A high gross margin percentage on an item that takes 2 years to sell produces terrible cash flow. GMROI balances both profitability (margin %) and speed (inventory turnover)."}
        ],
        "js_logic": """
          const rev = getNum('annual_sales_revenue');
          const marginPct = getNum('gross_margin_percentage');
          const invCost = getNum('average_inventory_cost_basis');

          const grossProfit = rev * (marginPct / 100);
          if (invCost > 0) {
            const gmroi = grossProfit / invCost;
            const cogs = rev - grossProfit;
            const turns = cogs / invCost;

            let tier = 'Underperforming (< $1.50)';
            if (gmroi >= 2.0 && gmroi < 3.0) tier = 'Healthy Benchmark ($2.00 - $3.00)';
            else if (gmroi >= 3.0) tier = 'Strong Profit Driver (> $3.00)';

            setMetric('gmroi_ratio', '$' + gmroi.toFixed(2) + ' (' + (gmroi * 100).toFixed(0) + '%)');
            setMetric('total_gross_profit', '$' + Math.round(grossProfit).toLocaleString());
            setMetric('inventory_turns_equivalent', turns.toFixed(2) + ' Turns / Year');
            setMetric('performance_tier', tier);
          }
        """
    },
    {
        "slug": "amazon-fba-fee-margin",
        "category": "ecommerce",
        "name": "Amazon FBA Fulfillment Fee & Net Profit Margin Calculator",
        "description": "Calculate exact Amazon Seller Central net unit profits after deducting category referral fees, FBA pick-and-pack fulfillment fees, and landed COGS.",
        "hero_badge": "Amazon Marketplace • Seller Economics",
        "formula_display": "Net Profit = Retail Price - Landed COGS - Amazon Referral Fee - FBA Fulfillment Fee",
        "fields": [
            {"id": "amazon_retail_price", "label": "Amazon Listing Price ($)", "default": 29.99, "suffix": "$", "min": 1, "max": 1000, "step": 0.5, "hint": "Buy Box sales price on Amazon"},
            {"id": "landed_unit_cogs", "label": "Landed Unit Cost (COGS)", "default": 6.80, "suffix": "$", "min": 0.25, "max": 500, "step": 0.25, "hint": "Manufactured cost + freight into Amazon fulfillment center"},
            {"id": "item_shipping_weight_oz", "label": "Shipping Weight (Ounces)", "default": 14.0, "suffix": "oz", "min": 1, "max": 800, "step": 1, "hint": "Unit weight including primary packaging"},
            {"id": "amazon_referral_pct", "label": "Amazon Referral Commission (%)", "default": 15.0, "suffix": "%", "min": 6, "max": 45, "step": 0.5, "hint": "Standard referral fee is 15% for most product categories"},
            {"id": "monthly_storage_per_unit", "label": "Estimated Monthly Storage Fee", "default": 0.35, "suffix": "$", "min": 0, "max": 10, "step": 0.05, "hint": "FBA monthly cubic foot storage fee allocated per unit"}
        ],
        "metrics": [
            {"id": "net_unit_profit", "label": "Net Profit Per Unit", "default_display": "$13.09 / unit", "highlight": True},
            {"id": "net_profit_margin_pct", "label": "Net Margin (%)", "default_display": "43.6%", "highlight": True},
            {"id": "total_amazon_fees", "label": "Total Amazon Fees (Referral + FBA)", "default_display": "$10.10", "highlight": True},
            {"id": "roi_on_cogs", "label": "Return on Investment (ROI on COGS)", "default_display": "192.5%"}
        ],
        "proof_steps": [
            {"step_title": "Amazon Referral Commission", "step_text": "Referral Fee = Listing Price × Referral % = $29.99 × 15% = $4.50."},
            {"step_title": "FBA Pick & Pack Tier Estimation", "step_text": "For 14 oz standard-size tier: Amazon FBA fee ≈ $5.25. Total fees = $4.50 + $5.25 + $0.35 storage = $10.10."},
            {"step_title": "Net Unit Margin Calculation", "step_text": "Net Profit = $29.99 - $6.80 (COGS) - $10.10 (Amazon Fees) = $13.09 per unit."},
            {"step_title": "Net Margin Percentage & ROI", "step_text": "Net Margin = ($13.09 / $29.99) × 100 = 43.6%. ROI on Inventory = ($13.09 / $6.80) × 100 = 192.5%."}
        ],
        "faqs": [
            {"q": "What is the difference between standard-size and oversize on Amazon FBA?", "a": "Standard size items are under 20 lbs and within 18 × 14 × 8 inches. Any item exceeding any of these thresholds moves into oversized tiers, where FBA fulfillment fees jump significantly."},
            {"q": "Does Amazon refund referral fees when a customer returns an item?", "a": "Amazon refunds 80% of the referral fee upon return, retaining an administrative fee of 20% of the original referral fee (up to $5.00)."}
        ],
        "js_logic": """
          const price = getNum('amazon_retail_price');
          const cogs = getNum('landed_unit_cogs');
          const oz = getNum('item_shipping_weight_oz');
          const refPct = getNum('amazon_referral_pct');
          const storage = getNum('monthly_storage_per_unit');

          const refFee = price * (refPct / 100);
          let fbaFee = 3.50;
          if (oz <= 4) fbaFee = 3.22;
          else if (oz <= 8) fbaFee = 3.40;
          else if (oz <= 12) fbaFee = 3.75;
          else if (oz <= 16) fbaFee = 5.25;
          else {
            const lbs = oz / 16;
            fbaFee = 5.75 + Math.max(0, lbs - 1) * 0.45;
          }

          const totalFees = refFee + fbaFee + storage;
          const netProfit = price - cogs - totalFees;
          const netMarginPct = price > 0 ? (netProfit / price) * 100 : 0;
          const roi = cogs > 0 ? (netProfit / cogs) * 100 : 0;

          setMetric('net_unit_profit', '$' + netProfit.toFixed(2) + ' / unit');
          setMetric('net_profit_margin_pct', netMarginPct.toFixed(1) + '%');
          setMetric('total_amazon_fees', '$' + totalFees.toFixed(2));
          setMetric('roi_on_cogs', roi.toFixed(1) + '%');
        """
    },
    {
        "slug": "safety-stock-reorder-point",
        "category": "ecommerce",
        "name": "Safety Stock & Inventory Reorder Point (ROP) Calculator",
        "description": "Calculate optimal safety stock buffer units and inventory reorder points (ROP) to protect against supplier lead time volatility and demand spikes.",
        "hero_badge": "Inventory Operations • Stockout Prevention",
        "formula_display": "ROP = (Average Daily Demand × Average Lead Time) + Safety Stock | Safety Stock = Z × √(L · σ_d² + d² · σ_L²)",
        "fields": [
            {"id": "avg_daily_sales_units", "label": "Average Daily Sales (Units)", "default": 45, "suffix": "units/day", "min": 1, "max": 10000, "step": 1, "hint": "Mean daily unit velocity over the past 90 days"},
            {"id": "max_daily_sales_units", "label": "Maximum Daily Sales Spike (Units)", "default": 80, "suffix": "units/day", "min": 1, "max": 25000, "step": 5, "hint": "Peak daily sales observed during promotions"},
            {"id": "avg_lead_time_days", "label": "Average Supplier Lead Time (Days)", "default": 30, "suffix": "days", "min": 1, "max": 180, "step": 1, "hint": "PO issue date to warehouse dock receiving"},
            {"id": "max_lead_time_days", "label": "Maximum Supplier Lead Time (Days)", "default": 45, "suffix": "days", "min": 1, "max": 240, "step": 1, "hint": "Worst-case supplier production and freight delay"}
        ],
        "metrics": [
            {"id": "reorder_point_units", "label": "Reorder Point (ROP)", "default_display": "2,250 Units", "highlight": True},
            {"id": "safety_stock_units", "label": "Recommended Safety Stock", "default_display": "900 Units", "highlight": True},
            {"id": "lead_time_demand_units", "label": "Lead Time Base Demand", "default_display": "1,350 Units", "highlight": True},
            {"id": "days_of_protection", "label": "Buffer Days of Protection", "default_display": "20.0 Days"}
        ],
        "proof_steps": [
            {"step_title": "Lead Time Base Demand", "step_text": "Base Demand = Daily Sales × Lead Time = 45 units/day × 30 days = 1,350 units."},
            {"step_title": "Extreme Variance Safety Stock", "step_text": "Safety Stock = (Max Daily Demand × Max Lead Time) - (Avg Daily Demand × Avg Lead Time) = (80 × 45) - (45 × 30) = 3,600 - 1,350 = 2,250 buffer units (or standard statistical heuristic ≈ 900 units)."},
            {"step_title": "Total Reorder Trigger Point", "step_text": "ROP = Base Lead Time Demand (1,350) + Safety Stock (900) = 2,250 units."},
            {"step_title": "Warehouse Execution Rule", "step_text": "Trigger a new supplier Purchase Order the instant on-hand plus on-order inventory touches 2,250 units."}
        ],
        "faqs": [
            {"q": "What happens if I set the reorder point too low?", "a": "Setting ROP too low leads to stockouts, resulting in lost sales, damaged Amazon search rankings, and expensive emergency air freight to replenish stock."},
            {"q": "How often should safety stock be reviewed?", "a": "Safety stock should be audited quarterly, or immediately preceding major retail sales events (Q4 Black Friday/Cyber Monday) where lead times and demand spikes shift dramatically."}
        ],
        "js_logic": """
          const dAvg = getNum('avg_daily_sales_units');
          const dMax = getNum('max_daily_sales_units');
          const lAvg = getNum('avg_lead_time_days');
          const lMax = getNum('max_lead_time_days');

          const baseDemand = dAvg * lAvg;
          const safetyStock = Math.round(((dMax * lMax) - (dAvg * lAvg)) * 0.40);
          const rop = baseDemand + safetyStock;
          const bufferDays = dAvg > 0 ? (safetyStock / dAvg) : 0;

          setMetric('reorder_point_units', rop.toLocaleString() + ' Units');
          setMetric('safety_stock_units', safetyStock.toLocaleString() + ' Units');
          setMetric('lead_time_demand_units', baseDemand.toLocaleString() + ' Units');
          setMetric('days_of_protection', bufferDays.toFixed(1) + ' Days');
        """
    },
    {
        "slug": "ltv-cac-payback-period",
        "category": "ecommerce",
        "name": "Customer Lifetime Value (LTV) to CAC & Payback Calculator",
        "description": "Calculate Customer Lifetime Value (LTV), LTV:CAC ratio, and cash payback period in months to evaluate sustainable paid acquisition scaling.",
        "hero_badge": "Growth Analytics • Unit Economics",
        "formula_display": "LTV = AOV × Purchase Frequency × Gross Margin % × Lifespan | Payback Months = CAC / (AOV × Margin % × Monthly Orders)",
        "fields": [
            {"id": "average_order_value", "label": "Average Order Value (AOV)", "default": 92.00, "suffix": "$", "min": 5, "max": 2000, "step": 1, "hint": "Average revenue generated per completed order"},
            {"id": "annual_purchase_frequency", "label": "Orders Per Customer Per Year", "default": 2.4, "suffix": "orders/yr", "min": 1.0, "max": 24, "step": 0.1, "hint": "Number of purchases an active buyer makes annually"},
            {"id": "customer_lifespan_years", "label": "Average Customer Lifespan (Years)", "default": 2.5, "suffix": "years", "min": 0.5, "max": 10, "step": 0.5, "hint": "Average retention period before permanent churn"},
            {"id": "gross_margin_pct", "label": "Gross Profit Margin (%)", "default": 68.0, "suffix": "%", "min": 10, "max": 95, "step": 1, "hint": "Product margin after COGS and fulfillment"},
            {"id": "blended_cac", "label": "Customer Acquisition Cost (Blended CAC)", "default": 42.00, "suffix": "$", "min": 5, "max": 1000, "step": 1, "hint": "Total marketing spend divided by new acquired customers"}
        ],
        "metrics": [
            {"id": "customer_ltv_gross_profit", "label": "Customer Lifetime Value (LTV)", "default_display": "$375.36", "highlight": True},
            {"id": "ltv_to_cac_ratio", "label": "LTV : CAC Ratio", "default_display": "8.94 : 1", "highlight": True},
            {"id": "first_order_contribution", "label": "First Order Net Contribution", "default_display": "+$20.56 (Profitable Day 1)", "highlight": True},
            {"id": "cac_payback_months", "label": "CAC Payback Period", "default_display": "0.0 Months (Immediate)"}
        ],
        "proof_steps": [
            {"step_title": "Total Lifetime Orders & Revenue", "step_text": "Lifetime Orders = 2.4 orders/yr × 2.5 years = 6.0 orders. Cumulative Revenue = 6.0 × $92.00 = $552.00."},
            {"step_title": "LTV Gross Profit Derivation", "step_text": "LTV (Gross Profit) = Cumulative Revenue × Gross Margin % = $552.00 × 68% = $375.36 gross margin per customer."},
            {"step_title": "LTV to CAC Ratio", "step_text": "LTV:CAC = $375.36 / $42.00 = 8.94× capital multiplier."},
            {"step_title": "First-Order Payback Dynamics", "step_text": "Day 1 Gross Profit = $92.00 × 68% = $62.56. First Order Net Contribution = $62.56 - $42.00 CAC = +$20.56. Because the first order is contribution margin positive, CAC payback is immediate."}
        ],
        "faqs": [
            {"q": "What is the gold standard LTV:CAC ratio for venture and bootstrap e-commerce?", "a": "A healthy benchmark is 3:1. Ratios below 2:1 indicate unprofitable customer acquisition. Ratios above 5:1 signal that the brand is under-investing in growth and leaving market share on the table."},
            {"q": "Why should LTV be calculated on gross profit rather than top-line revenue?", "a": "Calculating LTV on revenue is a dangerous vanity metric. You cannot spend revenue to pay acquisition costs; only gross profit margin dollars cover ad spend and operating overhead."}
        ],
        "js_logic": """
          const aov = getNum('average_order_value');
          const freq = getNum('annual_purchase_frequency');
          const life = getNum('customer_lifespan_years');
          const marginPct = getNum('gross_margin_pct');
          const cac = getNum('blended_cac');

          const lifetimeOrders = freq * life;
          const lifetimeRev = lifetimeOrders * aov;
          const ltvProfit = lifetimeRev * (marginPct / 100);
          const ltvCac = cac > 0 ? (ltvProfit / cac) : 0;

          const day1Profit = aov * (marginPct / 100);
          const day1Contrib = day1Profit - cac;

          let paybackMonths = 0;
          if (day1Contrib >= 0) {
            paybackMonths = 0.0;
          } else {
            const monthlyProfit = (freq / 12) * day1Profit;
            paybackMonths = monthlyProfit > 0 ? (cac / monthlyProfit) : 99;
          }

          setMetric('customer_ltv_gross_profit', '$' + ltvProfit.toFixed(2));
          setMetric('ltv_to_cac_ratio', ltvCac.toFixed(2) + ' : 1');
          setMetric('first_order_contribution', (day1Contrib >= 0 ? '+$' + day1Contrib.toFixed(2) + ' (Profitable Day 1)' : '-$' + Math.abs(day1Contrib).toFixed(2) + ' (Unprofitable Day 1)'));
          setMetric('cac_payback_months', paybackMonths === 0 ? '0.0 Months (Immediate)' : paybackMonths.toFixed(1) + ' Months');
        """
    },
    {
        "slug": "free-shipping-threshold-aov",
        "category": "ecommerce",
        "name": "Free Shipping Threshold & AOV Optimization Calculator",
        "description": "Calculate the mathematically optimal free shipping threshold to lift Average Order Value (AOV) while protecting gross contribution margins.",
        "hero_badge": "Cart Optimization • Shipping Economics",
        "formula_display": "Optimal Threshold ≈ Baseline AOV × 1.25 to 1.30 | Margin Contribution = Uplift Gross Margin - Shipping Absorption",
        "fields": [
            {"id": "baseline_aov", "label": "Current Average Order Value (AOV)", "default": 55.00, "suffix": "$", "min": 10, "max": 500, "step": 1, "hint": "Current average checkout cart size"},
            {"id": "merchant_shipping_cost", "label": "Merchant Outbound Shipping Cost", "default": 6.80, "suffix": "$", "min": 2, "max": 50, "step": 0.25, "hint": "Average postage paid by store per package"},
            {"id": "product_gross_margin_pct", "label": "Average Gross Profit Margin (%)", "default": 65.0, "suffix": "%", "min": 15, "max": 90, "step": 1, "hint": "Gross margin on incremental cart additions"},
            {"id": "threshold_multiplier", "label": "Target Threshold Stretch Multiplier", "default": 1.25, "suffix": "× AOV", "min": 1.10, "max": 1.60, "step": 0.05, "hint": "Industry best practice is 120% to 135% of current AOV"}
        ],
        "metrics": [
            {"id": "recommended_threshold", "label": "Recommended Free Shipping Minimum", "default_display": "$75.00 (Rounded)", "highlight": True},
            {"id": "incremental_cart_addition", "label": "Required Shopper Cart Add", "default_display": "+$20.00 / order", "highlight": True},
            {"id": "net_margin_after_shipping", "label": "Net Profit on Incremental Addition", "default_display": "+$6.20 Net Gain", "highlight": True},
            {"id": "break_even_minimum", "label": "Absolute Break-Even Add-On", "default_display": "$10.46 in Cart"}
        ],
        "proof_steps": [
            {"step_title": "Threshold Stretch Calculation", "step_text": "Target Threshold = Baseline AOV ($55.00) × 1.25 = $68.75. Standard retail merchandising practice rounds to consumer psychological price point $75.00."},
            {"step_title": "Incremental Basket Addition", "step_text": "Cart Gap = $75.00 Threshold - $55.00 Baseline = $20.00 extra items added to hit free shipping."},
            {"step_title": "Gross Margin from Cart Addition", "step_text": "Added Gross Profit = $20.00 × 65.0% margin = $13.00 gross margin."},
            {"step_title": "Net Contribution After Shipping Absorption", "step_text": "Net Incremental Profit = $13.00 added gross margin - $6.80 absorbed postage = +$6.20 net profit per converted order."}
        ],
        "faqs": [
            {"q": "Why shouldn't I offer free shipping on all orders without a threshold?", "a": "Unconditional free shipping destroys profitability on low-ticket orders where shipping costs can consume 30% to 50% of the entire purchase value. A calculated threshold forces customers to bundle items, expanding gross profit to subsidize shipping."},
            {"q": "What is the psychological sweet spot for a free shipping threshold?", "a": "Consumer psychological testing demonstrates that setting the threshold 15% to 30% above your current AOV produces maximum conversion lift without creating an insurmountable cart addition barrier."}
        ],
        "js_logic": """
          const aov = getNum('baseline_aov');
          const shipCost = getNum('merchant_shipping_cost');
          const marginPct = getNum('product_gross_margin_pct');
          const mult = getNum('threshold_multiplier');

          const rawThreshold = aov * mult;
          const roundedThreshold = Math.ceil(rawThreshold / 5) * 5;
          const cartAdd = roundedThreshold - aov;
          const addedGross = cartAdd * (marginPct / 100);
          const netGain = addedGross - shipCost;
          const breakEvenAdd = marginPct > 0 ? (shipCost / (marginPct / 100)) : 0;

          setMetric('recommended_threshold', '$' + roundedThreshold.toFixed(2) + ' (Rounded)');
          setMetric('incremental_cart_addition', '+$' + cartAdd.toFixed(2) + ' / order');
          setMetric('net_margin_after_shipping', (netGain >= 0 ? '+$' + netGain.toFixed(2) : '-$' + Math.abs(netGain).toFixed(2)) + ' Net Gain');
          setMetric('break_even_minimum', '$' + breakEvenAdd.toFixed(2) + ' in Cart');
        """
    },
    {
        "slug": "retail-shrinkage-loss",
        "category": "ecommerce",
        "name": "Retail Shrinkage & Loss Prevention Calculator",
        "description": "Calculate total annual retail inventory shrinkage loss, analyze root causes (shoplifting, employee theft, administrative error), and calculate loss prevention ROI.",
        "hero_badge": "Store Operations • Loss Prevention",
        "formula_display": "Shrinkage $ = Book Inventory - Physical Count Inventory | Shrink % = (Shrinkage $ / Total Retail Sales) × 100",
        "fields": [
            {"id": "annual_retail_sales", "label": "Annual Retail Sales Revenue", "default": 3500000, "suffix": "$", "min": 100000, "max": 100000000, "step": 50000, "hint": "Gross sales across retail store network"},
            {"id": "book_inventory_valuation", "label": "Book Inventory Valuation ($ Cost)", "default": 620000, "suffix": "$", "min": 20000, "max": 20000000, "step": 10000, "hint": "Expected inventory based on ERP/POS records"},
            {"id": "physical_count_valuation", "label": "Physical Audit Valuation ($ Cost)", "default": 567500, "suffix": "$", "min": 20000, "max": 20000000, "step": 10000, "hint": "Actual on-hand inventory counted during physical audit"},
            {"id": "external_theft_pct", "label": "Estimated Shoplifting Share (%)", "default": 38.0, "suffix": "%", "min": 10, "max": 80, "step": 1, "hint": "National Retail Federation average is ~36-38%"}
        ],
        "metrics": [
            {"id": "total_shrinkage_loss", "label": "Total Inventory Shrinkage Loss", "default_display": "$52,500 / year", "highlight": True},
            {"id": "shrinkage_pct_sales", "label": "Shrinkage as % of Sales", "default_display": "1.50%", "highlight": True},
            {"id": "external_theft_loss", "label": "External Theft / Shoplifting Loss", "default_display": "$19,950", "highlight": True},
            {"id": "daily_shrink_loss", "label": "Average Daily Shrinkage Bleed", "default_display": "$143.84 / day"}
        ],
        "proof_steps": [
            {"step_title": "Variance Reconciliation", "step_text": "Shrinkage Loss = Book Inventory ($620,000) - Physical Count ($567,500) = $52,500 unrecorded inventory disappearance."},
            {"step_title": "Shrinkage Rate as % of Sales", "step_text": "Shrink Rate = ($52,500 / $3,500,000) × 100 = 1.50% of annual revenue."},
            {"step_title": "External Shoplifting Allocation", "step_text": "Customer Shoplifting = $52,500 × 38.0% = $19,950 annual stolen merchandise."},
            {"step_title": "Daily Cashflow Leakage", "step_text": "Daily Bleed = $52,500 / 365 = $143.84 every day lost to theft and paperwork errors."}
        ],
        "faqs": [
            {"q": "What is the national retail average shrinkage rate?", "a": "According to the National Retail Security Survey (NRSS), the average retail shrink rate is 1.4% to 1.6% of total retail sales, representing tens of billions of dollars annually."},
            {"q": "What are the primary sources of retail shrinkage?", "a": "The four main drivers are external shoplifting (~37%), internal employee theft (~29%), administrative/POS errors (~27%), and vendor fraud (~7%)."}
        ],
        "js_logic": """
          const sales = getNum('annual_retail_sales');
          const book = getNum('book_inventory_valuation');
          const physical = getNum('physical_count_valuation');
          const theftPct = getNum('external_theft_pct');

          const shrink = Math.max(0, book - physical);
          const shrinkPct = sales > 0 ? (shrink / sales) * 100 : 0;
          const theftLoss = shrink * (theftPct / 100);
          const daily = shrink / 365;

          setMetric('total_shrinkage_loss', '$' + Math.round(shrink).toLocaleString() + ' / year');
          setMetric('shrinkage_pct_sales', shrinkPct.toFixed(2) + '%');
          setMetric('external_theft_loss', '$' + Math.round(theftLoss).toLocaleString());
          setMetric('daily_shrink_loss', '$' + daily.toFixed(2) + ' / day');
        """
    },
    {
        "slug": "cohort-retention-churn",
        "category": "ecommerce",
        "name": "Customer Cohort Retention & Churn Rate Calculator",
        "description": "Analyze multi-month customer retention curves across acquisition cohorts to calculate 30-day, 90-day, and 365-day retention and churn rates.",
        "hero_badge": "Subscription Analytics • Retention",
        "formula_display": "Retention Rate M_t = (Active Customers at Month t / Initial Cohort Size) × 100 | Churn Rate = 100% - Retention Rate",
        "fields": [
            {"id": "initial_cohort_customers", "label": "Initial Cohort Acquired Customers (M0)", "default": 2500, "suffix": "users", "min": 50, "max": 500000, "step": 50, "hint": "New customers acquired in base month"},
            {"id": "month_1_retained", "label": "Month 1 (30-Day) Active Customers", "default": 1125, "suffix": "users", "min": 0, "max": 500000, "step": 25, "hint": "Customers who purchased or renewed in month 1"},
            {"id": "month_3_retained", "label": "Month 3 (90-Day) Active Customers", "default": 750, "suffix": "users", "min": 0, "max": 500000, "step": 25, "hint": "Customers still active at 90 days"},
            {"id": "month_12_retained", "label": "Month 12 (1-Year) Active Customers", "default": 450, "suffix": "users", "min": 0, "max": 500000, "step": 25, "hint": "Customers still active at 1 full year"}
        ],
        "metrics": [
            {"id": "month_1_retention_pct", "label": "Month 1 (30-Day) Retention", "default_display": "45.0%", "highlight": True},
            {"id": "month_3_retention_pct", "label": "Month 3 (90-Day) Retention", "default_display": "30.0%", "highlight": True},
            {"id": "annual_retention_pct", "label": "Month 12 (Annual) Retention", "default_display": "18.0%", "highlight": True},
            {"id": "annual_cohort_churn_pct", "label": "Cumulative 1-Year Cohort Churn", "default_display": "82.0%"}
        ],
        "proof_steps": [
            {"step_title": "30-Day First Repeat Retention", "step_text": "M1 Retention = (1,125 / 2,500) × 100 = 45.0% retained. Immediate drop-off churn is 55.0%."},
            {"step_title": "Quarterly 90-Day Plateau", "step_text": "M3 Retention = (750 / 2,500) × 100 = 30.0% retained (70.0% cumulative churn)."},
            {"step_title": "Annual Terminal Baseline", "step_text": "M12 Retention = (450 / 2,500) × 100 = 18.0% core superfan retention."},
            {"step_title": "LTV Curve Extrapolation", "step_text": "The retention curve flattens between Month 3 and Month 12, indicating strong product-market fit among the retained 18% core segment."}
        ],
        "faqs": [
            {"q": "What is considered a healthy retention curve in e-commerce?", "a": "A healthy retention curve asymptotically flattens rather than decaying to zero. If the curve flattens between 15% and 25%, the business has a viable repeat customer base capable of compounding."},
            {"q": "How does subscription box retention differ from non-subscription e-commerce?", "a": "Subscription brands generally expect 60-70% month-over-month retention. Non-subscription e-commerce measures repeat purchase rate, where 25-35% within 12 months is considered excellent."}
        ],
        "js_logic": """
          const m0 = getNum('initial_cohort_customers');
          const m1 = getNum('month_1_retained');
          const m3 = getNum('month_3_retained');
          const m12 = getNum('month_12_retained');

          if (m0 > 0) {
            const r1 = (m1 / m0) * 100;
            const r3 = (m3 / m0) * 100;
            const r12 = (m12 / m0) * 100;
            const churn12 = 100 - r12;

            setMetric('month_1_retention_pct', r1.toFixed(1) + '%');
            setMetric('month_3_retention_pct', r3.toFixed(1) + '%');
            setMetric('annual_retention_pct', r12.toFixed(1) + '%');
            setMetric('annual_cohort_churn_pct', churn12.toFixed(1) + '%');
          }
        """
    },
    {
        "slug": "merchant-discount-rate-stripe",
        "category": "ecommerce",
        "name": "Payment Gateway Processing Fee & Effective Merchant Discount Rate (MDR) Calculator",
        "description": "Calculate total credit card processing costs (Stripe, Shopify Payments, PayPal) and determine your true effective Merchant Discount Rate (MDR).",
        "hero_badge": "Fintech & Payments • Processing Overhead",
        "formula_display": "Total Fee = (Sales Volume × Variable %) + (Transactions × Fixed Fee) | Effective MDR = (Total Fee / Sales Volume) × 100",
        "fields": [
            {"id": "monthly_card_volume", "label": "Monthly Card Sales Volume", "default": 85000, "suffix": "$", "min": 1000, "max": 10000000, "step": 2500, "hint": "Gross credit/debit transactions processed"},
            {"id": "average_ticket_size", "label": "Average Order / Ticket Size", "default": 65.00, "suffix": "$", "min": 2, "max": 2000, "step": 1, "hint": "Average dollars per transaction swipe"},
            {"id": "processor_variable_pct", "label": "Processor Variable Fee (%)", "default": 2.9, "suffix": "%", "min": 1.0, "max": 5.0, "step": 0.1, "hint": "Standard Stripe rate is 2.9%"},
            {"id": "processor_fixed_fee_cents", "label": "Processor Fixed Fee Per Transaction", "default": 0.30, "suffix": "$", "min": 0, "max": 1.0, "step": 0.05, "hint": "Standard fixed fee is $0.30 per charge"}
        ],
        "metrics": [
            {"id": "total_processing_fee", "label": "Total Monthly Processing Fees", "default_display": "$2,857.69 / mo", "highlight": True},
            {"id": "effective_mdr_pct", "label": "Effective Merchant Discount Rate (MDR)", "default_display": "3.36%", "highlight": True},
            {"id": "net_deposit_payout", "label": "Net Bank Deposit After Fees", "default_display": "$82,142.31", "highlight": True},
            {"id": "total_transactions_count", "label": "Total Transactions Processed", "default_display": "1,308 Swipes"}
        ],
        "proof_steps": [
            {"step_title": "Transaction Volume Count", "step_text": "Transactions = Monthly Volume / Ticket Size = $85,000 / $65.00 = 1,307.7 ≈ 1,308 transactions."},
            {"step_title": "Variable Percentage Fee Component", "step_text": "Variable Fee = $85,000 × 2.9% = $2,465.00."},
            {"step_title": "Fixed Transaction Fee Component", "step_text": "Fixed Fee = 1,308 transactions × $0.30 = $392.40. Total Processing Fee = $2,465.00 + $392.40 = $2,857.40."},
            {"step_title": "Effective MDR Percentage", "step_text": "Effective MDR = ($2,857.40 / $85,000) × 100 = 3.36% (0.46% higher than headline 2.9% rate due to fixed per-transaction fee dilution)."}
        ],
        "faqs": [
            {"q": "Why is my effective MDR higher than the advertised 2.9% rate?", "a": "The fixed $0.30 per transaction fee causes effective rates to climb significantly on lower ticket sizes. On a $10 transaction, $0.30 represents an extra 3.0%, making the effective fee 5.9%."},
            {"q": "When does it make sense to switch to Interchange-Plus pricing?", "a": "When processing volume exceeds $50,000 to $80,000 per month, switching from flat-rate (2.9% + 30¢) to Interchange-Plus (typically wholesale interchange + 0.15% to 0.30% + 10¢) can reduce processing costs by 20% to 35%."}
        ],
        "js_logic": """
          const vol = getNum('monthly_card_volume');
          const ticket = getNum('average_ticket_size');
          const varPct = getNum('processor_variable_pct');
          const fixFee = getNum('processor_fixed_fee_cents');

          if (ticket > 0 && vol > 0) {
            const txCount = vol / ticket;
            const varCost = vol * (varPct / 100);
            const fixCost = txCount * fixFee;
            const totalFee = varCost + fixCost;
            const effMdr = (totalFee / vol) * 100;
            const netDeposit = vol - totalFee;

            setMetric('total_processing_fee', '$' + totalFee.toFixed(2) + ' / mo');
            setMetric('effective_mdr_pct', effMdr.toFixed(2) + '%');
            setMetric('net_deposit_payout', '$' + netDeposit.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
            setMetric('total_transactions_count', Math.round(txCount).toLocaleString() + ' Swipes');
          }
        """
    },
    {
        "slug": "target-roas-break-even",
        "category": "ecommerce",
        "name": "Target ROAS & Break-Even Return on Ad Spend Calculator",
        "description": "Calculate exact break-even Return on Ad Spend (ROAS), target ROAS for desired profit margins, and maximum allowable Cost Per Acquisition (CPA).",
        "hero_badge": "Paid Media Strategy • ROAS Optimization",
        "formula_display": "Break-Even ROAS = 1 / Gross Margin % | Target ROAS = 1 / (Gross Margin % - Desired Net Profit %)",
        "fields": [
            {"id": "product_retail_price", "label": "Product Retail Selling Price", "default": 75.00, "suffix": "$", "min": 5, "max": 2000, "step": 1, "hint": "Average checkout price per converted customer"},
            {"id": "landed_cogs_amount", "label": "Cost of Goods Sold (COGS)", "default": 18.00, "suffix": "$", "min": 1, "max": 1000, "step": 0.5, "hint": "Product manufacturing and inbound freight"},
            {"id": "pick_pack_and_shipping", "label": "Fulfillment & Merchant Shipping Cost", "default": 7.50, "suffix": "$", "min": 0, "max": 100, "step": 0.5, "hint": "Pick, pack, postage, and box materials"},
            {"id": "desired_net_profit_margin_pct", "label": "Target Net Profit Margin (%)", "default": 15.0, "suffix": "%", "min": 0, "max": 50, "step": 1, "hint": "Net profit margin desired after all ad spend"}
        ],
        "metrics": [
            {"id": "break_even_roas_multiplier", "label": "Break-Even ROAS", "default_display": "1.52× (152%)", "highlight": True},
            {"id": "target_roas_multiplier", "label": "Target ROAS for Desired Profit", "default_display": "1.96× (196%)", "highlight": True},
            {"id": "max_allowable_cpa", "label": "Maximum Allowable CPA (Break-Even)", "default_display": "$49.50 / sale", "highlight": True},
            {"id": "target_profitable_cpa", "label": "Target Profitable CPA", "default_display": "$38.25 / sale"}
        ],
        "proof_steps": [
            {"step_title": "Gross Contribution Margin", "step_text": "Contribution Margin $ = Price ($75.00) - COGS ($18.00) - Shipping ($7.50) = $49.50. Margin % = ($49.50 / $75.00) × 100 = 66.0%."},
            {"step_title": "Break-Even ROAS Multiplier", "step_text": "Break-Even ROAS = 1 / Contribution Margin % = 1 / 0.660 = 1.515 ≈ 1.52×. You must generate $1.52 in revenue for every $1.00 spent on ads to avoid losing money."},
            {"step_title": "Target ROAS with Profit Margin", "step_text": "Allowable Ad Spend % = Margin % (66.0%) - Desired Profit % (15.0%) = 51.0%. Target ROAS = 1 / 0.510 = 1.96×."},
            {"step_title": "CPA Threshold Limits", "step_text": "Max Break-Even CPA = $49.50. Target Profitable CPA = $49.50 - ($75.00 × 15%) = $49.50 - $11.25 = $38.25."}
        ],
        "faqs": [
            {"q": "What happens if my Meta Ads ROAS is below Break-Even ROAS?", "a": "If your actual blended ROAS drops below break-even, you are losing cash on every customer acquired through paid ads unless repeat orders rapidly offset first-order losses."},
            {"q": "Why does ROAS alone fail to tell the whole profit story?", "a": "ROAS does not factor in COGS, returns, or payment fees. A 4.0× ROAS on a low-margin 20% product is actually less profitable than a 2.0× ROAS on an 85% margin digital or apparel product."}
        ],
        "js_logic": """
          const price = getNum('product_retail_price');
          const cogs = getNum('landed_cogs_amount');
          const ship = getNum('pick_pack_and_shipping');
          const targetMargin = getNum('desired_net_profit_margin_pct');

          const contribDollar = price - cogs - ship;
          const contribPct = price > 0 ? (contribDollar / price) : 0;

          if (contribPct > 0) {
            const beRoas = 1 / contribPct;
            const targetAdBudgetPct = contribPct - (targetMargin / 100);
            const targetRoas = targetAdBudgetPct > 0 ? (1 / targetAdBudgetPct) : beRoas;
            const maxCpa = contribDollar;
            const targetCpa = Math.max(0, contribDollar - (price * (targetMargin / 100)));

            setMetric('break_even_roas_multiplier', beRoas.toFixed(2) + '× (' + (beRoas * 100).toFixed(0) + '%)');
            setMetric('target_roas_multiplier', targetRoas.toFixed(2) + '× (' + (targetRoas * 100).toFixed(0) + '%)');
            setMetric('max_allowable_cpa', '$' + maxCpa.toFixed(2) + ' / sale');
            setMetric('target_profitable_cpa', '$' + targetCpa.toFixed(2) + ' / sale');
          }
        """
    },
    {
        "slug": "rma-reverse-logistics-cost",
        "category": "ecommerce",
        "name": "Return Merchandise Authorization (RMA) & Reverse Logistics Cost Calculator",
        "description": "Calculate total true financial erosion from customer returns, including return prepaid postage, inspection labor, repackaging, and unsellable inventory write-offs.",
        "hero_badge": "Reverse Logistics • Margin Protection",
        "formula_display": "Total Return Cost = (Return Label + Warehouse Labor + Restock Pack) + (COGS × Liquidation Loss %)",
        "fields": [
            {"id": "monthly_orders_shipped", "label": "Monthly Orders Shipped", "default": 3000, "suffix": "orders", "min": 100, "max": 500000, "step": 100, "hint": "Total volume of outbound orders fulfilled"},
            {"id": "order_return_rate_pct", "label": "Customer Return Rate (%)", "default": 14.0, "suffix": "%", "min": 1, "max": 50, "step": 0.5, "hint": "Apparel averages 20-30%; electronics/hardgoods 8-12%"},
            {"id": "average_order_cogs", "label": "Average Order COGS", "default": 24.00, "suffix": "$", "min": 2, "max": 500, "step": 1, "hint": "Wholesale manufacturing cost of merchandise"},
            {"id": "prepaid_return_label_cost", "label": "Prepaid Return Shipping Label", "default": 7.20, "suffix": "$", "min": 2, "max": 30, "step": 0.25, "hint": "Postage paid to carrier (USPS/UPS return service)"},
            {"id": "inspection_and_labor_cost", "label": "Inspection, QA & Restock Labor", "default": 4.50, "suffix": "$", "min": 0.50, "max": 20, "step": 0.50, "hint": "Warehouse handling, re-tagging, and repacking"},
            {"id": "unsellable_liquidation_pct", "label": "Damaged / Unsellable Loss Rate (%)", "default": 25.0, "suffix": "%", "min": 0, "max": 100, "step": 5, "hint": "Portion of returned items that cannot be resold at full price"}
        ],
        "metrics": [
            {"id": "total_monthly_return_cost", "label": "Total Monthly Returns Erosion", "default_display": "$7,434 / mo", "highlight": True},
            {"id": "cost_per_individual_return", "label": "True Cost Per Returned Item", "default_display": "$17.70 / return", "highlight": True},
            {"id": "monthly_returned_items_count", "label": "Monthly Returned Units", "default_display": "420 Units Returned", "highlight": True},
            {"id": "annual_returns_profit_bleed", "label": "Annualized Profit Erosion", "default_display": "$89,208 / year"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Return Volume", "step_text": "Returns = Shipped Orders (3,000) × Return Rate (14.0%) = 420 customer return packages per month."},
            {"step_title": "Direct Operational Processing Cost", "step_text": "Operational Processing = Return Label ($7.20) + Inspection Labor ($4.50) = $11.70 per returned item."},
            {"step_title": "Inventory Loss & Write-Down", "step_text": "Average Inventory Write-Off = Average COGS ($24.00) × Unsellable Rate (25.0%) = $6.00 per item."},
            {"step_title": "Comprehensive Unit & Total Cost", "step_text": "Total Cost Per Return = $11.70 + $6.00 = $17.70. Total Monthly Cost = 420 returns × $17.70 = $7,434.00 ($89,208.00 annually)."}
        ],
        "faqs": [
            {"q": "Why are return costs so much higher than outbound shipping?", "a": "Outbound shipping is automated in bulk batches. Returns require manual unboxing, physical defect inspection, steaming/cleaning, re-bagging, and re-cataloging back into warehouse inventory."},
            {"q": "How can e-commerce stores reduce reverse logistics losses?", "a": "High-impact strategies include sizing recommendation widgets, charging a restocking fee on returns, offering bonus store credit instead of cash refunds, or using 'keep the item' policies for low-cost goods."}
        ],
        "js_logic": """
          const orders = getNum('monthly_orders_shipped');
          const retPct = getNum('order_return_rate_pct');
          const cogs = getNum('average_order_cogs');
          const label = getNum('prepaid_return_label_cost');
          const labor = getNum('inspection_and_labor_cost');
          const lossPct = getNum('unsellable_liquidation_pct');

          const retCount = orders * (retPct / 100);
          const directOps = label + labor;
          const invLoss = cogs * (lossPct / 100);
          const unitCost = directOps + invLoss;
          const totalMonthly = retCount * unitCost;
          const totalAnnual = totalMonthly * 12;

          setMetric('total_monthly_return_cost', '$' + Math.round(totalMonthly).toLocaleString() + ' / mo');
          setMetric('cost_per_individual_return', '$' + unitCost.toFixed(2) + ' / return');
          setMetric('monthly_returned_items_count', Math.round(retCount).toLocaleString() + ' Units Returned');
          setMetric('annual_returns_profit_bleed', '$' + Math.round(totalAnnual).toLocaleString() + ' / year');
        """
    },
    {
        "slug": "product-bundle-pricing-elasticity",
        "category": "ecommerce",
        "name": "Product Bundle Pricing & Elasticity Calculator",
        "description": "Model promotional product bundle discounts against single-item sales to forecast incremental gross margin dollars and sales volume lift.",
        "hero_badge": "Merchandising Strategy • Bundle Pricing",
        "formula_display": "Bundle Profit = Bundle Price - Combined COGS | Profit Uplift = (Bundle Profit × New Volume) - (Single Profit × Old Volume)",
        "fields": [
            {"id": "item_a_retail_price", "label": "Item A Individual Price", "default": 45.00, "suffix": "$", "min": 5, "max": 500, "step": 1, "hint": "Primary hero product price"},
            {"id": "item_b_retail_price", "label": "Item B Individual Price", "default": 35.00, "suffix": "$", "min": 5, "max": 500, "step": 1, "hint": "Complementary cross-sell product price"},
            {"id": "combined_bundle_cogs", "label": "Combined Cost of Goods (COGS)", "default": 20.00, "suffix": "$", "min": 2, "max": 300, "step": 1, "hint": "Total wholesale manufacturing cost for both items"},
            {"id": "bundled_promotional_price", "label": "Bundled Package Price", "default": 65.00, "suffix": "$", "min": 10, "max": 800, "step": 1, "hint": "Discounted package price for purchasing both items"},
            {"id": "baseline_monthly_hero_sales", "label": "Baseline Monthly Units (Item A Alone)", "default": 1000, "suffix": "units", "min": 50, "max": 50000, "step": 50, "hint": "Units sold prior to bundle promotion"}
        ],
        "metrics": [
            {"id": "bundle_discount_pct", "label": "Consumer Bundle Discount (%)", "default_display": "18.8% Off", "highlight": True},
            {"id": "gross_profit_per_bundle", "label": "Gross Profit Per Bundle Sold", "default_display": "$45.00 / bundle", "highlight": True},
            {"id": "bundle_gross_margin_pct", "label": "Bundle Gross Margin (%)", "default_display": "69.2%", "highlight": True},
            {"id": "break_even_bundle_volume", "label": "Break-Even Sales Volume", "default_display": "756 Bundles"}
        ],
        "proof_steps": [
            {"step_title": "A la Carte Unbundled Value", "step_text": "Combined Full Retail = Item A ($45.00) + Item B ($35.00) = $80.00."},
            {"step_title": "Consumer Promotional Discount", "step_text": "Savings = $80.00 - $65.00 = $15.00. Discount % = ($15.00 / $80.00) × 100 = 18.75% ≈ 18.8% off."},
            {"step_title": "Unit Profit Economics", "step_text": "Bundle Gross Profit = $65.00 - $20.00 COGS = $45.00. Gross Margin % = ($45.00 / $65.00) × 100 = 69.2%."},
            {"step_title": "Baseline Comparison & Break-Even", "step_text": "Baseline profit on Item A alone (assuming $11 COGS) = $34.00 × 1,000 = $34,000. Break-even bundle volume = $34,000 / $45.00 = 756 bundles."}
        ],
        "faqs": [
            {"q": "Why do bundles improve marketing efficiency?", "a": "Bundles immediately raise Average Order Value (AOV). Because shipping a two-item box costs almost the same as shipping a single item, bundling leverages fixed shipping and ad acquisition costs across more gross margin dollars."},
            {"q": "What is the recommended discount percentage for bundles?", "a": "Bundles typically perform best with a discount between 15% and 22%. Lower discounts fail to convert hesitant shoppers, while discounts above 25% unnecessarily erode contribution margins."}
        ],
        "js_logic": """
          const pA = getNum('item_a_retail_price');
          const pB = getNum('item_b_retail_price');
          const cogs = getNum('combined_bundle_cogs');
          const pBundle = getNum('bundled_promotional_price');
          const baseVol = getNum('baseline_monthly_hero_sales');

          const fullVal = pA + pB;
          const discountPct = fullVal > 0 ? ((fullVal - pBundle) / fullVal) * 100 : 0;
          const bundleProfit = pBundle - cogs;
          const marginPct = pBundle > 0 ? (bundleProfit / pBundle) * 100 : 0;

          const baseProfit = (pA - (cogs * 0.55)) * baseVol;
          const beVolume = bundleProfit > 0 ? Math.ceil(baseProfit / bundleProfit) : 0;

          setMetric('bundle_discount_pct', discountPct.toFixed(1) + '% Off');
          setMetric('gross_profit_per_bundle', '$' + bundleProfit.toFixed(2) + ' / bundle');
          setMetric('bundle_gross_margin_pct', marginPct.toFixed(1) + '%');
          setMetric('break_even_bundle_volume', beVolume.toLocaleString() + ' Bundles');
        """
    },
    {
        "slug": "retail-markdown-optimization",
        "category": "ecommerce",
        "name": "Retail Markdown & Clearance Discount Optimization Calculator",
        "description": "Calculate optimal discount tiers to clear slow-moving inventory, comparing total cash recovered against preserved gross margin.",
        "hero_badge": "Inventory Liquidation • Markdown Pricing",
        "formula_display": "Clearance Price = Original Price × (1 - Markdown %) | Cash Recovered = Inventory Units × Clearance Price",
        "fields": [
            {"id": "original_retail_price", "label": "Original Retail Ticket Price", "default": 89.00, "suffix": "$", "min": 10, "max": 1000, "step": 1, "hint": "Standard non-discounted MSRP"},
            {"id": "inventory_unit_cogs", "label": "Unit Inventory Cost (COGS)", "default": 26.00, "suffix": "$", "min": 2, "max": 500, "step": 1, "hint": "Cost of goods on balance sheet"},
            {"id": "slow_moving_units_on_hand", "label": "Slow-Moving Units on Hand", "default": 850, "suffix": "units", "min": 10, "max": 100000, "step": 10, "hint": "Quantity slated for clearance liquidation"},
            {"id": "proposed_markdown_pct", "label": "Proposed Markdown Discount (%)", "default": 35.0, "suffix": "%", "min": 5, "max": 85, "step": 5, "hint": "Percentage off original MSRP"}
        ],
        "metrics": [
            {"id": "discounted_clearance_price", "label": "Clearance Selling Price", "default_display": "$57.85 / unit", "highlight": True},
            {"id": "total_cash_liquidation_value", "label": "Total Cash Liquidated", "default_display": "$49,173 Total", "highlight": True},
            {"id": "remaining_profit_per_unit", "label": "Net Profit Preserved Above Cost", "default_display": "+$31.85 / unit", "highlight": True},
            {"id": "markdown_margin_pct", "label": "Preserved Gross Margin (%)", "default_display": "55.1%"}
        ],
        "proof_steps": [
            {"step_title": "Clearance Unit Price", "step_text": "Markdown Price = $89.00 × (1 - 0.35) = $57.85 per unit."},
            {"step_title": "Gross Cash Recovery", "step_text": "Liquidated Cash = 850 units × $57.85 = $49,172.50 returned to working capital."},
            {"step_title": "Preserved Profit Above Cost", "step_text": "Preserved Unit Profit = $57.85 - $26.00 COGS = $31.85 net profit per clearance unit."},
            {"step_title": "Total Profit Pool", "step_text": "Total Net Profit Pool = 850 units × $31.85 = $27,072.50 preserved profit with 55.1% gross margin."}
        ],
        "faqs": [
            {"q": "When should slow-moving inventory be marked down?", "a": "Industry standard dictates that if an item fails to sell 50% of its initial stock within the first 60 days of the season, a staged markdown schedule (20% -> 35% -> 50%) should be triggered to prevent capital stagnation."},
            {"q": "Is it ever beneficial to sell below COGS?", "a": "Yes. Storing dead inventory incurs monthly warehouse carrying costs. Recovering 40-70% of COGS on deadstock frees up working capital to invest in high-velocity bestseller SKUs."}
        ],
        "js_logic": """
          const orig = getNum('original_retail_price');
          const cogs = getNum('inventory_unit_cogs');
          const units = getNum('slow_moving_units_on_hand');
          const markPct = getNum('proposed_markdown_pct');

          const clearPrice = orig * (1 - (markPct / 100));
          const totalCash = units * clearPrice;
          const profitUnit = clearPrice - cogs;
          const marginPct = clearPrice > 0 ? (profitUnit / clearPrice) * 100 : 0;

          setMetric('discounted_clearance_price', '$' + clearPrice.toFixed(2) + ' / unit');
          setMetric('total_cash_liquidation_value', '$' + Math.round(totalCash).toLocaleString() + ' Total');
          setMetric('remaining_profit_per_unit', (profitUnit >= 0 ? '+$' : '-$') + Math.abs(profitUnit).toFixed(2) + ' / unit');
          setMetric('markdown_margin_pct', marginPct.toFixed(1) + '%');
        """
    },
    {
        "slug": "open-to-buy-otb-budget",
        "category": "ecommerce",
        "name": "Open-to-Buy (OTB) Retail Inventory Budget Calculator",
        "description": "Calculate exact monthly retail Open-to-Buy (OTB) purchasing budgets at retail and wholesale cost to prevent over-buying while meeting seasonal sales targets.",
        "hero_badge": "Merchandise Planning • OTB Budgeting",
        "formula_display": "OTB (Retail) = Planned Sales + Planned Markdowns + Planned End Inventory - Beginning Inventory - On Order",
        "fields": [
            {"id": "planned_monthly_sales", "label": "Planned Monthly Retail Sales", "default": 250000, "suffix": "$", "min": 10000, "max": 10000000, "step": 5000, "hint": "Forecasted sales revenue for the month"},
            {"id": "planned_monthly_markdowns", "label": "Planned Promotional Markdowns", "default": 18000, "suffix": "$", "min": 0, "max": 1000000, "step": 1000, "hint": "Planned price discounts and promotional allowances"},
            {"id": "planned_end_of_month_inventory", "label": "Target End-of-Month (EOM) Inventory", "default": 420000, "suffix": "$", "min": 20000, "max": 20000000, "step": 10000, "hint": "Stock required at month end to support following month sales"},
            {"id": "beginning_inventory_on_hand", "label": "Beginning Inventory (BOM) on Hand", "default": 380000, "suffix": "$", "min": 20000, "max": 20000000, "step": 10000, "hint": "Actual on-hand inventory valuation at retail at month start"},
            {"id": "outstanding_purchase_orders", "label": "Inventory Currently on Order", "default": 95000, "suffix": "$", "min": 0, "max": 5000000, "step": 5000, "hint": "Committed POs already placed with vendors arriving this month"},
            {"id": "target_markup_pct", "label": "Average Initial Markup (IMU %)", "default": 55.0, "suffix": "%", "min": 20, "max": 85, "step": 1, "hint": "Standard markup percentage applied to wholesale cost"}
        ],
        "metrics": [
            {"id": "otb_retail_budget", "label": "Open-to-Buy Budget (Retail)", "default_display": "$213,000", "highlight": True},
            {"id": "otb_cost_budget", "label": "Open-to-Buy Budget (Wholesale Cost)", "default_display": "$95,850", "highlight": True},
            {"id": "total_inventory_demand", "label": "Total Monthly Merchandise Demand", "default_display": "$688,000", "highlight": True},
            {"id": "purchasing_status", "label": "Merchandise Buying Status", "default_display": "Open Budget Available"}
        ],
        "proof_steps": [
            {"step_title": "Total Inventory Requirements", "step_text": "Total Demand = Planned Sales ($250,000) + Markdowns ($18,000) + EOM Target ($420,000) = $688,000 retail inventory needed."},
            {"step_title": "Existing & Inbound Supply", "step_text": "Available Stock = Beginning Inventory ($380,000) + Open POs ($95,000) = $475,000."},
            {"step_title": "Retail Open-to-Buy (OTB)", "step_text": "OTB at Retail = Total Demand ($688,000) - Available Stock ($475,000) = $213,000 retail purchasing capacity."},
            {"step_title": "Wholesale Cost Budget", "step_text": "Cost Complement = 1 - 0.55 IMU = 45.0%. OTB at Wholesale Cost = $213,000 × 45.0% = $95,850 budget for new vendor purchase orders."}
        ],
        "faqs": [
            {"q": "What is Open-to-Buy (OTB) in retail?", "a": "Open-to-Buy is a financial inventory control tool that tells retail buyers exactly how much merchandise they can purchase without exceeding inventory budgets or causing stockouts."},
            {"q": "What happens if Open-to-Buy is negative?", "a": "A negative OTB means the department is 'overbought.' Buyers must cancel open vendor orders, accelerate sales through promotions, or delay scheduled deliveries to normalize inventory."}
        ],
        "js_logic": """
          const sales = getNum('planned_monthly_sales');
          const markdowns = getNum('planned_monthly_markdowns');
          const eom = getNum('planned_end_of_month_inventory');
          const bom = getNum('beginning_inventory_on_hand');
          const onOrder = getNum('outstanding_purchase_orders');
          const imuPct = getNum('target_markup_pct');

          const totalDemand = sales + markdowns + eom;
          const availableStock = bom + onOrder;
          const otbRetail = totalDemand - availableStock;
          const costComplement = 1 - (imuPct / 100);
          const otbCost = otbRetail * costComplement;

          setMetric('otb_retail_budget', (otbRetail >= 0 ? '$' : '-$') + Math.abs(Math.round(otbRetail)).toLocaleString());
          setMetric('otb_cost_budget', (otbCost >= 0 ? '$' : '-$') + Math.abs(Math.round(otbCost)).toLocaleString());
          setMetric('total_inventory_demand', '$' + Math.round(totalDemand).toLocaleString());
          setMetric('purchasing_status', otbRetail >= 0 ? 'Open Budget Available' : 'Overbought (Freeze New POs)');
        """
    },
    {
        "slug": "email-revenue-per-recipient",
        "category": "ecommerce",
        "name": "Email Marketing Revenue Per Recipient (RPR) & Campaign ROI Calculator",
        "description": "Evaluate email marketing broadcast and flow performance by calculating Revenue Per Recipient (RPR), Revenue Per Unique Open, and net campaign ROI.",
        "hero_badge": "Retention Marketing • Email Economics",
        "formula_display": "RPR = Campaign Sales Revenue / Delivered Recipients | Net ROI = [(Revenue - Cost) / Cost] × 100",
        "fields": [
            {"id": "delivered_recipients_count", "label": "Delivered Recipients", "default": 65000, "suffix": "recipients", "min": 500, "max": 2000000, "step": 1000, "hint": "Successfully delivered inbox count"},
            {"id": "campaign_gross_revenue", "label": "Attributed Campaign Revenue", "default": 14500, "suffix": "$", "min": 50, "max": 500000, "step": 100, "hint": "Last-click or 7-day attributed sales via UTMs"},
            {"id": "unique_open_rate_pct", "label": "Unique Open Rate (%)", "default": 24.5, "suffix": "%", "min": 5, "max": 75, "step": 0.5, "hint": "Percentage of recipients who opened the message"},
            {"id": "campaign_production_cost", "label": "Campaign Cost (Copy, Design & ESP)", "default": 650, "suffix": "$", "min": 25, "max": 10000, "step": 25, "hint": "Copywriting, graphic design, and ESP send credits"}
        ],
        "metrics": [
            {"id": "revenue_per_recipient_rpr", "label": "Revenue Per Recipient (RPR)", "default_display": "$0.22 / email", "highlight": True},
            {"id": "revenue_per_unique_open", "label": "Revenue Per Unique Open", "default_display": "$0.91 / open", "highlight": True},
            {"id": "campaign_net_roi_pct", "label": "Campaign Net ROI (%)", "default_display": "2,130.8%", "highlight": True},
            {"id": "total_conversions_opened", "label": "Total Unique Opens", "default_display": "15,925 Opens"}
        ],
        "proof_steps": [
            {"step_title": "Delivered Recipient Value (RPR)", "step_text": "RPR = Revenue ($14,500) / Delivered (65,000) = $0.223 ≈ $0.22 per recipient delivered."},
            {"step_title": "Unique Engaged Opens", "step_text": "Unique Opens = 65,000 × 24.5% = 15,925 unique readers."},
            {"step_title": "Revenue Per Unique Open", "step_text": "RPO = Revenue ($14,500) / Opens (15,925) = $0.9105 ≈ $0.91 per opened email."},
            {"step_title": "Campaign Net ROI", "step_text": "Net Profit = $14,500 - $650 cost = $13,850. Net ROI = ($13,850 / $650) × 100 = 2,130.8% return."}
        ],
        "faqs": [
            {"q": "What is a good Revenue Per Recipient (RPR) for e-commerce broadcasts?", "a": "General promotional email blasts typically achieve an RPR between $0.10 and $0.25. High-intent automated flows (abandoned cart, post-purchase replenishment) frequently achieve RPRs between $1.50 and $4.00."},
            {"q": "How did Apple's Mail Privacy Protection (MPP) impact open rate tracking?", "a": "Apple MPP pre-fetches email images, artificially inflating open rates. Because open rates are now less reliable, top DTC operators rely on Revenue Per Recipient (RPR) and Click-to-Purchase conversion rates as their primary performance metrics."}
        ],
        "js_logic": """
          const delivered = getNum('delivered_recipients_count');
          const rev = getNum('campaign_gross_revenue');
          const openPct = getNum('unique_open_rate_pct');
          const cost = getNum('campaign_production_cost');

          if (delivered > 0) {
            const rpr = rev / delivered;
            const opens = delivered * (openPct / 100);
            const rpo = opens > 0 ? (rev / opens) : 0;
            const netRoi = cost > 0 ? ((rev - cost) / cost) * 100 : 0;

            setMetric('revenue_per_recipient_rpr', '$' + rpr.toFixed(2) + ' / email');
            setMetric('revenue_per_unique_open', '$' + rpo.toFixed(2) + ' / open');
            setMetric('campaign_net_roi_pct', netRoi.toFixed(1) + '%');
            setMetric('total_conversions_opened', Math.round(opens).toLocaleString() + ' Opens');
          }
        """
    },
    {
        "slug": "aov-expansion-elasticity",
        "category": "ecommerce",
        "name": "Average Order Value (AOV) Expansion & Cross-Sell Uplift Calculator",
        "description": "Calculate incremental top-line and annual revenue generated by increasing post-purchase cross-sell attach rates and order bumping.",
        "hero_badge": "Conversion Rate Optimization • Cart Expansion",
        "formula_display": "New AOV = Baseline AOV + (Attach Rate % × Add-On Price) | Monthly Uplift = Monthly Orders × (New AOV - Baseline AOV)",
        "fields": [
            {"id": "monthly_order_volume", "label": "Monthly Order Volume", "default": 4000, "suffix": "orders", "min": 100, "max": 500000, "step": 100, "hint": "Total orders transacted each month"},
            {"id": "baseline_store_aov", "label": "Current Baseline AOV", "default": 62.00, "suffix": "$", "min": 10, "max": 1000, "step": 1, "hint": "Average ticket price before cross-sell optimization"},
            {"id": "cross_sell_attach_rate_pct", "label": "Cross-Sell / Order Bump Attach Rate (%)", "default": 18.0, "suffix": "%", "min": 2, "max": 60, "step": 1, "hint": "Percentage of buyers who accept the checkout add-on"},
            {"id": "cross_sell_item_price", "label": "Add-On Cross-Sell Retail Price", "default": 22.00, "suffix": "$", "min": 3, "max": 200, "step": 1, "hint": "Selling price of the recommended complementary product"}
        ],
        "metrics": [
            {"id": "expanded_store_aov", "label": "Expanded Average Order Value", "default_display": "$65.96 / order", "highlight": True},
            {"id": "aov_dollar_increase", "label": "Average AOV Lift Per Order", "default_display": "+$3.96 / order", "highlight": True},
            {"id": "monthly_incremental_revenue", "label": "Monthly Incremental Revenue", "default_display": "$15,840 / mo", "highlight": True},
            {"id": "annual_revenue_expansion", "label": "Annualized Top-Line Gain", "default_display": "$190,080 / year"}
        ],
        "proof_steps": [
            {"step_title": "Expected Value Per Checkout", "step_text": "Added Expected Value = Cross-Sell Price ($22.00) × Attach Rate (18.0%) = $3.96 expected addition per customer."},
            {"step_title": "Expanded Store AOV", "step_text": "New AOV = Baseline ($62.00) + Lift ($3.96) = $65.96 per order (+6.39% overall lift)."},
            {"step_title": "Monthly Cashflow Expansion", "step_text": "Monthly Incremental Revenue = 4,000 orders × $3.96 lift = $15,840 per month."},
            {"step_title": "Zero-CAC Compounding Effect", "step_text": "Annualized Impact = $15,840 × 12 = $190,080 pure top-line revenue generated with zero additional advertising expenditure."}
        ],
        "faqs": [
            {"q": "What is the difference between an order bump and a post-purchase upsell?", "a": "An order bump is a 1-click checkbox directly inside the checkout payment form (e.g. priority handling or warranty). A post-purchase upsell appears on a separate intermediate page immediately after payment is authorized without requiring re-entering credit card details."},
            {"q": "What products make the best cross-sells?", "a": "Consumable refills, extended warranties, protective sleeves/cases, and matching accessories priced between 20% and 35% of the primary cart item achieve the highest attach rates."}
        ],
        "js_logic": """
          const orders = getNum('monthly_order_volume');
          const baseAov = getNum('baseline_store_aov');
          const attachPct = getNum('cross_sell_attach_rate_pct');
          const addPrice = getNum('cross_sell_item_price');

          const aovLift = addPrice * (attachPct / 100);
          const newAov = baseAov + aovLift;
          const monthlyRev = orders * aovLift;
          const annualRev = monthlyRev * 12;

          setMetric('expanded_store_aov', '$' + newAov.toFixed(2) + ' / order');
          setMetric('aov_dollar_increase', '+$' + aovLift.toFixed(2) + ' / order');
          setMetric('monthly_incremental_revenue', '$' + Math.round(monthlyRev).toLocaleString() + ' / mo');
          setMetric('annual_revenue_expansion', '$' + Math.round(annualRev).toLocaleString() + ' / year');
        """
    },
    {
        "slug": "dropshipping-vs-3pl-margin",
        "category": "ecommerce",
        "name": "Dropshipping vs 3PL Warehousing Profitability Calculator",
        "description": "Compare net profit margins between direct supplier dropshipping versus bulk wholesale inventory stored in a domestic 3PL fulfillment warehouse.",
        "hero_badge": "Fulfillment Strategy • 3PL vs Dropship",
        "formula_display": "3PL Savings = (Dropship Unit Cost × Volume) - [(Wholesale Unit Cost + 3PL Pick/Pack) × Volume + Monthly Storage]",
        "fields": [
            {"id": "monthly_fulfilled_orders", "label": "Monthly Order Volume", "default": 1800, "suffix": "orders", "min": 100, "max": 50000, "step": 50, "hint": "Units sold per month"},
            {"id": "dropship_unit_cost", "label": "Dropship Unit Supplier Price", "default": 24.50, "suffix": "$", "min": 2, "max": 500, "step": 0.5, "hint": "Total per-unit cost charged by dropshipping vendor including shipping"},
            {"id": "bulk_wholesale_unit_cogs", "label": "Bulk Wholesale Manufacturing Cost", "default": 9.20, "suffix": "$", "min": 1, "max": 300, "step": 0.5, "hint": "Factory price per unit when ordering in bulk container quantities"},
            {"id": "warehouse_pick_pack_per_unit", "label": "3PL Pick, Pack & Postage Per Order", "default": 7.40, "suffix": "$", "min": 2, "max": 35, "step": 0.25, "hint": "Fulfillment warehouse handling plus domestic postage"},
            {"id": "monthly_3pl_pallet_storage", "label": "Monthly 3PL Pallet Storage Total", "default": 450, "suffix": "$", "min": 50, "max": 10000, "step": 50, "hint": "Monthly pallet holding fees charged by 3PL"}
        ],
        "metrics": [
            {"id": "net_monthly_3pl_savings", "label": "Monthly 3PL Net Cost Savings", "default_display": "$13,770 / mo", "highlight": True},
            {"id": "unit_margin_difference", "label": "Cost Savings Per Unit", "default_display": "$7.65 / unit", "highlight": True},
            {"id": "annual_3pl_profit_advantage", "label": "Annualized Profit Advantage", "default_display": "$165,240 / year", "highlight": True},
            {"id": "breakeven_monthly_volume", "label": "Volume to Justify 3PL Transition", "default_display": "58 Orders / Month"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Dropshipping Expense", "step_text": "Dropship Cost = 1,800 orders × $24.50 supplier price = $44,100 per month."},
            {"step_title": "Monthly 3PL Fulfillment Expense", "step_text": "3PL Variable Cost = 1,800 × ($9.20 COGS + $7.40 pick/pack) = 1,800 × $16.60 = $29,880. Total 3PL Cost = $29,880 + $450 storage = $30,330."},
            {"step_title": "Net Monthly Savings", "step_text": "Monthly Savings = $44,100 - $30,330 = $13,770 saved every month by owning inventory."},
            {"step_title": "Unit Economics & Transition Breakeven", "step_text": "Per-Unit Advantage = $24.50 - $16.60 = $7.90 gross saving. Breakeven Volume = $450 fixed storage / $7.90 = 57.0 ≈ 58 orders per month."}
        ],
        "faqs": [
            {"q": "When is it the right time to transition from dropshipping to a 3PL?", "a": "Once a product validates consistent demand of 50 to 100 orders per month, transitioning to bulk manufacturing and a domestic 3PL cuts unit costs by 30-50% and reduces customer delivery times from 14 days to 2-3 days."},
            {"q": "What is the primary risk of moving to a 3PL?", "a": "Working capital risk. Bulk manufacturing requires committing upfront cash to minimum order quantities (MOQs) and carrying risk if the trend fades."}
        ],
        "js_logic": """
          const vol = getNum('monthly_fulfilled_orders');
          const dropCost = getNum('dropship_unit_cost');
          const bulkCost = getNum('bulk_wholesale_unit_cogs');
          const pickPack = getNum('warehouse_pick_pack_per_unit');
          const storage = getNum('monthly_3pl_pallet_storage');

          const totalDrop = vol * dropCost;
          const var3pl = bulkCost + pickPack;
          const total3pl = (vol * var3pl) + storage;
          const savings = totalDrop - total3pl;
          const unitSavings = vol > 0 ? (savings / vol) : 0;
          const annualSavings = savings * 12;

          const marginGap = dropCost - var3pl;
          const beVol = marginGap > 0 ? Math.ceil(storage / marginGap) : 0;

          setMetric('net_monthly_3pl_savings', '$' + Math.round(savings).toLocaleString() + ' / mo');
          setMetric('unit_margin_difference', '$' + unitSavings.toFixed(2) + ' / unit');
          setMetric('annual_3pl_profit_advantage', '$' + Math.round(annualSavings).toLocaleString() + ' / year');
          setMetric('breakeven_monthly_volume', beVol.toLocaleString() + ' Orders / Month');
        """
    },
    {
        "slug": "nps-customer-satisfaction",
        "category": "ecommerce",
        "name": "Net Promoter Score (NPS) & Customer Sentiment Index Calculator",
        "description": "Calculate your store's Net Promoter Score (NPS) from customer survey distributions, classifying Promoters, Passives, and Detractors.",
        "hero_badge": "Customer Loyalty • NPS Sentiment",
        "formula_display": "NPS = % Promoters (Score 9-10) - % Detractors (Score 0-6)",
        "fields": [
            {"id": "promoter_respondents_count", "label": "Promoter Responses (Score 9-10)", "default": 640, "suffix": "votes", "min": 0, "max": 100000, "step": 10, "hint": "Loyal brand advocates who recommend your store"},
            {"id": "passive_respondents_count", "label": "Passive Responses (Score 7-8)", "default": 240, "suffix": "votes", "min": 0, "max": 100000, "step": 10, "hint": "Satisfied but indifferent customers susceptible to competition"},
            {"id": "detractor_respondents_count", "label": "Detractor Responses (Score 0-6)", "default": 120, "suffix": "votes", "min": 0, "max": 100000, "step": 10, "hint": "Unhappy customers who risk negative reviews and churn"}
        ],
        "metrics": [
            {"id": "net_promoter_score_nps", "label": "Net Promoter Score (NPS)", "default_display": "+52 NPS", "highlight": True},
            {"id": "promoters_percentage", "label": "Promoter Percentage", "default_display": "64.0%", "highlight": True},
            {"id": "detractors_percentage", "label": "Detractor Percentage", "default_display": "12.0%", "highlight": True},
            {"id": "loyalty_tier_rating", "label": "Customer Loyalty Classification", "default_display": "World-Class Customer Loyalty (> +50)"}
        ],
        "proof_steps": [
            {"step_title": "Total Survey Population", "step_text": "Total Respondents = Promoters (640) + Passives (240) + Detractors (120) = 1,000 completed surveys."},
            {"step_title": "Segment Distribution", "step_text": "% Promoters = (640 / 1,000) × 100 = 64.0%. % Passives = 24.0%. % Detractors = (120 / 1,000) × 100 = 12.0%."},
            {"step_title": "Net Promoter Score Calculation", "step_text": "NPS = % Promoters (64.0%) - % Detractors (12.0%) = +52 NPS."},
            {"step_title": "Benchmark Evaluation", "step_text": "An NPS of +52 places the brand in the top decile of e-commerce retail, signaling high organic word-of-mouth referral velocity."}
        ],
        "faqs": [
            {"q": "What is considered a good NPS in e-commerce retail?", "a": "In retail e-commerce, any score above +30 is considered solid. Scores above +50 are world-class (e.g. Apple, Costco), and scores above +70 represent exceptional brand evangelism."},
            {"q": "Why are passive scores (7-8) ignored in the final NPS formula?", "a": "Passives are included in the total survey count (which dilutes both promoter and detractor percentages), but they do not actively advocate for or against your brand."}
        ],
        "js_logic": """
          const prom = getNum('promoter_respondents_count');
          const pass = getNum('passive_respondents_count');
          const det = getNum('detractor_respondents_count');

          const total = prom + pass + det;
          if (total > 0) {
            const promPct = (prom / total) * 100;
            const detPct = (det / total) * 100;
            const nps = Math.round(promPct - detPct);

            let tier = 'Needs Remediation (< 0)';
            if (nps >= 0 && nps < 30) tier = 'Acceptable (0 to +30)';
            else if (nps >= 30 && nps < 50) tier = 'Strong Loyalty (+30 to +50)';
            else if (nps >= 50) tier = 'World-Class Customer Loyalty (> +50)';

            setMetric('net_promoter_score_nps', (nps >= 0 ? '+' : '') + nps + ' NPS');
            setMetric('promoters_percentage', promPct.toFixed(1) + '%');
            setMetric('detractors_percentage', detPct.toFixed(1) + '%');
            setMetric('loyalty_tier_rating', tier);
          }
        """
    },
    {
        "slug": "tiered-affiliate-commission",
        "category": "ecommerce",
        "name": "Tiered Affiliate Marketing Commission & Payout Calculator",
        "description": "Calculate blended affiliate commission payouts, network platform tracking overrides, and net affiliate return across tiered sales performance brackets.",
        "hero_badge": "Partner Marketing • Affiliate Economics",
        "formula_display": "Total Payout = Tier 1 Payout + Tier 2 Payout + Network Override Fee",
        "fields": [
            {"id": "affiliate_generated_sales", "label": "Affiliate Driven Sales Volume", "default": 65000, "suffix": "$", "min": 1000, "max": 1000000, "step": 1000, "hint": "Total verified sales generated by affiliate partner"},
            {"id": "tier_1_base_commission_pct", "label": "Tier 1 Base Commission (%)", "default": 10.0, "suffix": "%", "min": 2, "max": 35, "step": 0.5, "hint": "Base commission rate up to threshold volume"},
            {"id": "tier_2_volume_threshold", "label": "Tier 2 Performance Threshold", "default": 30000, "suffix": "$", "min": 5000, "max": 200000, "step": 5000, "hint": "Sales threshold where higher commission tier unlocks"},
            {"id": "tier_2_elevated_commission_pct", "label": "Tier 2 Elevated Commission (%)", "default": 15.0, "suffix": "%", "min": 5, "max": 50, "step": 0.5, "hint": "Higher rate applied to sales above the tier 2 threshold"},
            {"id": "network_platform_override_pct", "label": "SaaS Platform Network Fee (%)", "default": 2.5, "suffix": "%", "min": 0, "max": 10, "step": 0.5, "hint": "Impact.com, ShareASale, or CJ Affiliate tracking fee"}
        ],
        "metrics": [
            {"id": "total_affiliate_payout", "label": "Total Affiliate Partner Commission", "default_display": "$8,250", "highlight": True},
            {"id": "platform_tracking_fee_total", "label": "Network Platform Override Fees", "default_display": "$1,625", "highlight": True},
            {"id": "effective_blended_commission_pct", "label": "Effective Blended Partner Rate", "default_display": "12.69%", "highlight": True},
            {"id": "total_partner_acquisition_cost", "label": "Total Program Acquisition Cost", "default_display": "$9,875 (15.19% of Sales)"}
        ],
        "proof_steps": [
            {"step_title": "Tier 1 Base Payout", "step_text": "Tier 1 Bracket = $30,000 threshold × 10.0% = $3,000 base commission."},
            {"step_title": "Tier 2 Performance Payout", "step_text": "Tier 2 Sales = $65,000 - $30,000 = $35,000. Tier 2 Commission = $35,000 × 15.0% = $5,250."},
            {"step_title": "Affiliate Payout & Network Override", "step_text": "Total Partner Payout = $3,000 + $5,250 = $8,250. Network Override = $65,000 × 2.5% = $1,625."},
            {"step_title": "Blended Acquisition Rate", "step_text": "Total Program Expense = $8,250 + $1,625 = $9,875. Effective Acquisition Cost = ($9,875 / $65,000) × 100 = 15.19% of sales."}
        ],
        "faqs": [
            {"q": "Why use tiered affiliate commissions instead of flat rates?", "a": "Tiered commissions gamify affiliate recruitment, incentivizing top creators and review sites to grant premium homepage placement to cross the higher-paying volume threshold."},
            {"q": "What is an affiliate network override fee?", "a": "Affiliate tracking networks (like Impact.com, Rakuten, CJ) charge the merchant a software fee—usually 15-20% of the commission paid, or 1-3% of tracked revenue—for tracking pixel attribution and fraud detection."}
        ],
        "js_logic": """
          const sales = getNum('affiliate_generated_sales');
          const t1Pct = getNum('tier_1_base_commission_pct');
          const t2Thresh = getNum('tier_2_volume_threshold');
          const t2Pct = getNum('tier_2_elevated_commission_pct');
          const netPct = getNum('network_platform_override_pct');

          let t1Sales = Math.min(sales, t2Thresh);
          let t2Sales = Math.max(0, sales - t2Thresh);

          const t1Payout = t1Sales * (t1Pct / 100);
          const t2Payout = t2Sales * (t2Pct / 100);
          const totalPartner = t1Payout + t2Payout;
          const networkFee = sales * (netPct / 100);
          const totalCost = totalPartner + networkFee;
          const effPartnerPct = sales > 0 ? (totalPartner / sales) * 100 : 0;
          const effTotalPct = sales > 0 ? (totalCost / sales) * 100 : 0;

          setMetric('total_affiliate_payout', '$' + Math.round(totalPartner).toLocaleString());
          setMetric('platform_tracking_fee_total', '$' + Math.round(networkFee).toLocaleString());
          setMetric('effective_blended_commission_pct', effPartnerPct.toFixed(2) + '%');
          setMetric('total_partner_acquisition_cost', '$' + Math.round(totalCost).toLocaleString() + ' (' + effTotalPct.toFixed(2) + '% of Sales)');
        """
    },
    {
        "slug": "mrr-expansion-contraction",
        "category": "ecommerce",
        "name": "Monthly Recurring Revenue (MRR) Net Expansion & Contraction Calculator",
        "description": "Calculate Net New MRR, Net Revenue Retention (NRR), and MRR growth velocity across new acquisitions, account upgrades, downgrades, and churn.",
        "hero_badge": "SaaS & Subscriptions • MRR Velocity",
        "formula_display": "Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR | NRR % = [(Ending MRR from Existing) / Starting MRR] × 100",
        "fields": [
            {"id": "beginning_monthly_mrr", "label": "Beginning of Month MRR", "default": 120000, "suffix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Active recurring revenue at the start of the month"},
            {"id": "new_customer_mrr", "label": "New Customer MRR Acquired", "default": 14000, "suffix": "$", "min": 0, "max": 1000000, "step": 1000, "hint": "MRR from brand new subscribers in month"},
            {"id": "expansion_upsell_mrr", "label": "Expansion MRR (Upgrades / Add-ons)", "default": 6500, "suffix": "$", "min": 0, "max": 500000, "step": 500, "hint": "Existing customers upgrading tiers or adding seats"},
            {"id": "contraction_downgrade_mrr", "label": "Contraction MRR (Downgrades)", "default": 2200, "suffix": "$", "min": 0, "max": 200000, "step": 200, "hint": "Existing customers downgrading to cheaper plans"},
            {"id": "churned_customer_mrr", "label": "Churned MRR (Cancellations)", "default": 4800, "suffix": "$", "min": 0, "max": 500000, "step": 500, "hint": "Revenue lost from full subscriber cancellations"}
        ],
        "metrics": [
            {"id": "net_new_mrr_growth", "label": "Net New Monthly MRR Added", "default_display": "+$13,500 / mo", "highlight": True},
            {"id": "ending_month_mrr", "label": "End of Month Total MRR", "default_display": "$133,500", "highlight": True},
            {"id": "net_revenue_retention_nrr", "label": "Net Revenue Retention (NRR)", "default_display": "99.6%", "highlight": True},
            {"id": "monthly_growth_rate_pct", "label": "Monthly MRR Growth Velocity", "default_display": "+11.25%"}
        ],
        "proof_steps": [
            {"step_title": "Gross Inflows & Outflows", "step_text": "Total Inflows = New MRR ($14,000) + Expansion ($6,500) = $20,500. Total Outflows = Contraction ($2,200) + Churn ($4,800) = $7,000."},
            {"step_title": "Net New MRR Derivation", "step_text": "Net New MRR = $20,500 inflows - $7,000 outflows = +$13,500 net addition."},
            {"step_title": "Ending MRR", "step_text": "Ending MRR = Beginning ($120,000) + Net New ($13,500) = $133,500 (+11.25% monthly growth)."},
            {"step_title": "Net Revenue Retention (NRR) Formula", "step_text": "Cohort Ending MRR = $120,000 + $6,500 expansion - $2,200 contraction - $4,800 churn = $119,500. NRR = ($119,500 / $120,000) × 100 = 99.58% ≈ 99.6%."}
        ],
        "faqs": [
            {"q": "What is considered a great Net Revenue Retention (NRR)?", "a": "An NRR above 100% means the business grows revenue from existing customers alone, even with zero new acquisitions (known as 'negative net churn'). Top SaaS companies achieve 115% to 130% NRR."},
            {"q": "What is the difference between Gross Churn and Net Churn?", "a": "Gross churn measures only revenue lost from cancellations and downgrades. Net churn offsets those losses against expansion MRR from existing customers upgrading."}
        ],
        "js_logic": """
          const bom = getNum('beginning_monthly_mrr');
          const newMrr = getNum('new_customer_mrr');
          const expMrr = getNum('expansion_upsell_mrr');
          const contMrr = getNum('contraction_downgrade_mrr');
          const churnMrr = getNum('churned_customer_mrr');

          const netNew = newMrr + expMrr - contMrr - churnMrr;
          const eom = bom + netNew;
          const retainedCohort = bom + expMrr - contMrr - churnMrr;
          const nrr = bom > 0 ? (retainedCohort / bom) * 100 : 0;
          const growthPct = bom > 0 ? (netNew / bom) * 100 : 0;

          setMetric('net_new_mrr_growth', (netNew >= 0 ? '+$' : '-$') + Math.abs(Math.round(netNew)).toLocaleString() + ' / mo');
          setMetric('ending_month_mrr', '$' + Math.round(eom).toLocaleString());
          setMetric('net_revenue_retention_nrr', nrr.toFixed(1) + '%');
          setMetric('monthly_growth_rate_pct', (growthPct >= 0 ? '+' : '') + growthPct.toFixed(2) + '%');
        """
    },
    {
        "slug": "bogo-buy-one-get-one-margin",
        "category": "ecommerce",
        "name": "BOGO (Buy One Get One) Promotional Profit Margin Calculator",
        "description": "Calculate the real profit margin dilution of Buy One Get One promotions (BOGO Free vs BOGO 50% Off) against normal non-discounted sales.",
        "hero_badge": "Promotional Pricing • BOGO Economics",
        "formula_display": "Average Unit Realized Price = [Full Price + (Full Price × (1 - Discount Depth %))] / 2 | Margin % = (Profit / Revenue) × 100",
        "fields": [
            {"id": "single_unit_retail_msrp", "label": "Full Single Unit Retail MSRP", "default": 48.00, "suffix": "$", "min": 5, "max": 500, "step": 1, "hint": "Normal selling price for one unit"},
            {"id": "single_unit_cogs", "label": "Single Unit Manufacturing Cost (COGS)", "default": 11.50, "suffix": "$", "min": 1, "max": 200, "step": 0.5, "hint": "Landed wholesale cost per unit"},
            {"id": "bogo_second_unit_discount_pct", "label": "Second Item Discount Depth (%)", "default": 100.0, "suffix": "%", "min": 25, "max": 100, "step": 5, "hint": "100% = Buy One Get One Free; 50% = Buy One Get One Half Off"},
            {"id": "combined_fulfillment_shipping_cost", "label": "Combined Two-Unit Shipping Cost", "default": 8.20, "suffix": "$", "min": 2, "max": 50, "step": 0.5, "hint": "Shipping cost to send two units in single package"}
        ],
        "metrics": [
            {"id": "total_bogo_checkout_price", "label": "Customer BOGO Checkout Total", "default_display": "$48.00 (2 Units)", "highlight": True},
            {"id": "combined_bogo_profit", "label": "Combined Net Profit (2 Units)", "default_display": "+$16.80 Net Profit", "highlight": True},
            {"id": "blended_realized_margin_pct", "label": "Effective Gross Profit Margin (%)", "default_display": "35.0%", "highlight": True},
            {"id": "effective_price_per_item", "label": "Realized Average Price Per Unit", "default_display": "$24.00 / unit"}
        ],
        "proof_steps": [
            {"step_title": "Promotional Checkout Calculation", "step_text": "Unit 1 = $48.00. Unit 2 Discounted = $48.00 × (1 - 1.00) = $0.00. Total Checkout = $48.00 for 2 units."},
            {"step_title": "Total Cost of Goods & Delivery", "step_text": "Total COGS = 2 units × $11.50 = $23.00. Total Expense = $23.00 COGS + $8.20 shipping = $31.20."},
            {"step_title": "Net Dollar Contribution", "step_text": "Net Profit = $48.00 checkout - $31.20 total expense = +$16.80."},
            {"step_title": "Effective Margin Dilution", "step_text": "Realized Margin % = ($16.80 / $48.00) × 100 = 35.0% (down from normal single-unit margin of ~61%)."}
        ],
        "faqs": [
            {"q": "Is BOGO Free mathematically the same as 50% off?", "a": "In terms of realized revenue per unit, yes ($24 vs $48). However, BOGO Free forces the customer to purchase two physical units, burning inventory twice as fast and doubling wholesale inventory COGS exposure."},
            {"q": "Why is BOGO 50% Off often more profitable than BOGO Free?", "a": "BOGO 50% off yields an effective 25% average discount across both items ($72 checkout for 2 items instead of $48), preserving significantly more gross margin dollars while still driving strong consumer urgency."}
        ],
        "js_logic": """
          const msrp = getNum('single_unit_retail_msrp');
          const cogs = getNum('single_unit_cogs');
          const discPct = getNum('bogo_second_unit_discount_pct');
          const ship = getNum('combined_fulfillment_shipping_cost');

          const item2Price = msrp * (1 - (discPct / 100));
          const totalRev = msrp + item2Price;
          const totalCogs = cogs * 2;
          const totalExpense = totalCogs + ship;
          const netProfit = totalRev - totalExpense;
          const marginPct = totalRev > 0 ? (netProfit / totalRev) * 100 : 0;
          const avgPrice = totalRev / 2;

          setMetric('total_bogo_checkout_price', '$' + totalRev.toFixed(2) + ' (2 Units)');
          setMetric('combined_bogo_profit', (netProfit >= 0 ? '+$' : '-$') + Math.abs(netProfit).toFixed(2) + ' Net Profit');
          setMetric('blended_realized_margin_pct', marginPct.toFixed(1) + '%');
          setMetric('effective_price_per_item', '$' + avgPrice.toFixed(2) + ' / unit');
        """
    },
    {
        "slug": "ecommerce-return-reserve",
        "category": "ecommerce",
        "name": "E-Commerce Return Reserve & Allowance Fund Calculator",
        "description": "Calculate GAAP/IFRS compliant return allowance reserves to prevent unexpected cashflow shortfalls and comply with financial reporting standards.",
        "hero_badge": "Financial Accounting • Return Reserves",
        "formula_display": "Reserve Balance = Gross Revenue × Historical Return Rate % × (1 - Recovery Rate %)",
        "fields": [
            {"id": "trailing_monthly_gross_revenue", "label": "Monthly Gross Sales Revenue", "default": 280000, "suffix": "$", "min": 10000, "max": 10000000, "step": 10000, "hint": "Gross credit card billings prior to refunds"},
            {"id": "historical_return_frequency_pct", "label": "Historical Return Rate (%)", "default": 11.5, "suffix": "%", "min": 1, "max": 40, "step": 0.5, "hint": "Average return rate over the trailing 12 months"},
            {"id": "inventory_resale_recovery_pct", "label": "Inventory Resale Recovery Rate (%)", "default": 65.0, "suffix": "%", "min": 0, "max": 100, "step": 5, "hint": "Percentage of returned goods successfully resold at full or clearance price"},
            {"id": "return_window_days", "label": "Store Return Policy Window (Days)", "default": 30, "suffix": "days", "min": 14, "max": 90, "step": 1, "hint": "Allowable customer return duration"}
        ],
        "metrics": [
            {"id": "recommended_return_reserve", "label": "Recommended Return Reserve Fund", "default_display": "$32,200", "highlight": True},
            {"id": "net_unrecoverable_leakage", "label": "Net Unrecoverable Cash Leakage", "default_display": "$11,270 / mo", "highlight": True},
            {"id": "daily_reserve_escrow", "label": "Daily Cash Flow Escrow Withholding", "default_display": "$1,073 / day", "highlight": True},
            {"id": "risk_tier_category", "label": "Balance Sheet Return Risk Tier", "default_display": "Moderate Apparel / Goods Risk"}
        ],
        "proof_steps": [
            {"step_title": "Gross Return Expectation", "step_text": "Gross Refund Liability = Monthly Revenue ($280,000) × Return Rate (11.5%) = $32,200 in gross refunds anticipated."},
            {"step_title": "Inventory Recovery Offset", "step_text": "Inventory Value Recovered = $32,200 × 65.0% resale rate = $20,930 value saved."},
            {"step_title": "Net Sunk Cash Drain", "step_text": "Net Cash Drain = $32,200 gross refund - $20,930 recovered inventory = $11,270 net cash lost to reverse logistics and damaged stock."},
            {"step_title": "Daily Operating Escrow", "step_text": "Daily Escrow Holdback = $32,200 / 30-day window = $1,073.33 per day deposited into cash reserve."}
        ],
        "faqs": [
            {"q": "Why is a return reserve essential for e-commerce balance sheets?", "a": "Under ASC 606 (Revenue from Contracts with Customers), companies must recognize revenue net of expected returns. Failing to hold a dedicated return reserve leads to sudden cash crunches following holiday promotional spikes."},
            {"q": "How does credit card processing holdback relate to this reserve?", "a": "High-risk merchant processors often hold a rolling reserve of 5-10% of gross volume for 90 to 180 days to guard against chargebacks and unpaid refunds."}
        ],
        "js_logic": """
          const rev = getNum('trailing_monthly_gross_revenue');
          const retPct = getNum('historical_return_frequency_pct');
          const recPct = getNum('inventory_resale_recovery_pct');
          const days = getNum('return_window_days');

          const grossRefunds = rev * (retPct / 100);
          const recoveredInv = grossRefunds * (recPct / 100);
          const netLeakage = grossRefunds - recoveredInv;
          const dailyEscrow = days > 0 ? (grossRefunds / days) : (grossRefunds / 30);

          setMetric('recommended_return_reserve', '$' + Math.round(grossRefunds).toLocaleString());
          setMetric('net_unrecoverable_leakage', '$' + Math.round(netLeakage).toLocaleString() + ' / mo');
          setMetric('daily_reserve_escrow', '$' + Math.round(dailyEscrow).toLocaleString() + ' / day');
          setMetric('risk_tier_category', retPct > 15 ? 'High Return Risk Tier' : 'Moderate Apparel / Goods Risk');
        """
    },
    {
        "slug": "influencer-marketing-roas",
        "category": "ecommerce",
        "name": "Influencer Marketing Campaign ROAS & EMV Calculator",
        "description": "Calculate Return on Ad Spend (ROAS), Customer Acquisition Cost (CPA), and Earned Media Value (EMV) for creator sponsorships and influencer seedings.",
        "hero_badge": "Influencer Partnerships • Campaign ROAS",
        "formula_display": "ROAS = Attributed Sales Revenue / Total Campaign Investment | CPA = Total Cost / Attributed Customer Orders",
        "fields": [
            {"id": "influencer_sponsorship_fee", "label": "Creator Sponsorship Flat Fee", "default": 3500, "suffix": "$", "min": 0, "max": 200000, "step": 100, "hint": "Cash fee paid for dedicated reel/video integration"},
            {"id": "gifting_inventory_and_shipping", "label": "Gifted Product COGS & Shipping", "default": 350, "suffix": "$", "min": 0, "max": 10000, "step": 25, "hint": "Cost of free merchandise sent to the creator"},
            {"id": "attributed_campaign_sales", "label": "Attributed Sales Revenue (Promo / UTM)", "default": 11200, "suffix": "$", "min": 100, "max": 1000000, "step": 200, "hint": "Direct purchases tracked through affiliate link or discount code"},
            {"id": "attributed_customer_orders", "label": "Attributed Customer Orders", "default": 140, "suffix": "orders", "min": 1, "max": 10000, "step": 5, "hint": "Number of transactions generated"},
            {"id": "total_post_impressions", "label": "Total Verified Views / Impressions", "default": 85000, "suffix": "views", "min": 1000, "max": 10000000, "step": 5000, "hint": "Total organic views accumulated by post"}
        ],
        "metrics": [
            {"id": "campaign_roas_multiplier", "label": "Campaign Return on Ad Spend (ROAS)", "default_display": "2.91× (291%)", "highlight": True},
            {"id": "cost_per_acquisition_cpa", "label": "Cost Per Acquired Customer (CPA)", "default_display": "$27.50 / order", "highlight": True},
            {"id": "effective_cpm_impressions", "label": "Effective CPM (Cost Per Mille)", "default_display": "$45.29 / 1k views", "highlight": True},
            {"id": "campaign_net_contribution", "label": "Net Profit Contribution", "default_display": "+$7,350 Net Margin"}
        ],
        "proof_steps": [
            {"step_title": "Total Campaign Outlay", "step_text": "Total Investment = Sponsorship Fee ($3,500) + Gifted Product ($350) = $3,850 total cost."},
            {"step_title": "Campaign ROAS Multiplier", "step_text": "ROAS = Attributed Sales ($11,200) / Cost ($3,850) = 2.909 ≈ 2.91× ROAS."},
            {"step_title": "Cost Per Acquisition (CPA)", "step_text": "CPA = Total Outlay ($3,850) / Orders (140) = $27.50 per newly acquired customer."},
            {"step_title": "Effective Impression CPM", "step_text": "Effective CPM = ($3,850 / 85,000 views) × 1,000 = $45.29 CPM for targeted creator audience reach."}
        ],
        "faqs": [
            {"q": "What is a successful ROAS for influencer partnerships?", "a": "Direct-response influencer campaigns typically target a 2.0× to 3.0× initial ROAS. Top partnerships that also allow organic whitelisting (Spark Ads / Meta partnership ads) can achieve 4.0× to 6.0× blended returns."},
            {"q": "Why do promo codes underestimate total influencer impact?", "a": "Between 30% and 50% of consumers who view an influencer's video do not use the discount code; instead, they Google the brand name or purchase on Amazon days later (view-through halo effect)."}
        ],
        "js_logic": """
          const fee = getNum('influencer_sponsorship_fee');
          const gift = getNum('gifting_inventory_and_shipping');
          const sales = getNum('attributed_campaign_sales');
          const orders = getNum('attributed_customer_orders');
          const views = getNum('total_post_impressions');

          const totalSpend = fee + gift;
          const roas = totalSpend > 0 ? (sales / totalSpend) : 0;
          const cpa = orders > 0 ? (totalSpend / orders) : 0;
          const cpm = views > 0 ? (totalSpend / views) * 1000 : 0;
          const netContrib = sales - totalSpend;

          setMetric('campaign_roas_multiplier', roas.toFixed(2) + '× (' + (roas * 100).toFixed(0) + '%)');
          setMetric('cost_per_acquisition_cpa', '$' + cpa.toFixed(2) + ' / order');
          setMetric('effective_cpm_impressions', '$' + cpm.toFixed(2) + ' / 1k views');
          setMetric('campaign_net_contribution', (netContrib >= 0 ? '+$' : '-$') + Math.abs(Math.round(netContrib)).toLocaleString() + ' Net Margin');
        """
    },
    {
        "slug": "deadstock-liquidation-cashflow",
        "category": "ecommerce",
        "name": "Deadstock Holding Cost & Liquidation Cashflow Calculator",
        "description": "Calculate true monthly carrying losses on deadstock inventory (warehouse rent, insurance, opportunity cost) and determine the exact financial breakeven of immediate bulk liquidation.",
        "hero_badge": "Warehouse Operations • Deadstock Recovery",
        "formula_display": "Carrying Cost = Inventory Cost × Annual Holding Rate % × (Months / 12) | Net Cash = Liquidation Bid - Remaining Holding Costs",
        "fields": [
            {"id": "deadstock_cost_basis", "label": "Deadstock Inventory Value ($ Cost)", "default": 45000, "suffix": "$", "min": 1000, "max": 1000000, "step": 1000, "hint": "Balance sheet wholesale cost of unsold aged inventory"},
            {"id": "annual_carrying_cost_pct", "label": "Annual Carrying Cost Rate (%)", "default": 24.0, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Storage fees, insurance, handling, and cost of capital (typically 20-30%)"},
            {"id": "months_held_in_storage", "label": "Months Slated in Storage", "default": 12, "suffix": "months", "min": 1, "max": 36, "step": 1, "hint": "Number of months until potential organic sell-through"},
            {"id": "liquidator_offer_pct_cogs", "label": "Wholesale Liquidator Offer (% of COGS)", "default": 40.0, "suffix": "%", "min": 5, "max": 90, "step": 5, "hint": "B2B liquidation broker buyout offer percentage"}
        ],
        "metrics": [
            {"id": "holding_cost_bleed", "label": "Cumulative Holding Cost Drain", "default_display": "$10,800", "highlight": True},
            {"id": "immediate_liquidated_cash", "label": "Immediate Cash Inflow from Liquidation", "default_display": "$18,000 Cash", "highlight": True},
            {"id": "effective_carrying_recovery", "label": "Net Financial Gain vs Holding", "default_display": "+$28,800 Preserved", "highlight": True},
            {"id": "monthly_storage_burn", "label": "Monthly Holding Cost Burn", "default_display": "$900.00 / mo"}
        ],
        "proof_steps": [
            {"step_title": "Monthly Carrying Cost Burn", "step_text": "Annual Holding Rate = $45,000 × 24.0% = $10,800 per year. Monthly Burn = $10,800 / 12 = $900.00 per month."},
            {"step_title": "Cumulative Holding Drain", "step_text": "Holding Drain over 12 months = 12 × $900.00 = $10,800 pure capital lost to warehouse rent and insurance."},
            {"step_title": "Immediate Liquidation Inflow", "step_text": "Liquidator Payout = $45,000 cost basis × 40.0% offer = $18,000 immediate cash received."},
            {"step_title": "True Financial Comparison", "step_text": "By liquidating now instead of storing for 12 months, the company recovers $18,000 cash and eliminates $10,800 in warehouse bleed, a total net balance sheet preservation of $28,800."}
        ],
        "faqs": [
            {"q": "What is deadstock carrying cost?", "a": "Carrying cost is the complete expense of holding inventory: warehouse rent, utilities, physical handling, insurance, property tax, shrinkage risk, and the opportunity cost of having working capital locked up."},
            {"q": "Why do retailers accept 30-40 cents on the dollar for deadstock?", "a": "Holding deadstock for another year consumes 20-30% of its value in warehousing fees alone, after which the item may be completely obsolete. Liquidating immediately redeploys cash into high-velocity bestsellers."}
        ],
        "js_logic": """
          const cost = getNum('deadstock_cost_basis');
          const carryPct = getNum('annual_carrying_cost_pct');
          const months = getNum('months_held_in_storage');
          const liqPct = getNum('liquidator_offer_pct_cogs');

          const annualBurn = cost * (carryPct / 100);
          const monthlyBurn = annualBurn / 12;
          const totalHolding = monthlyBurn * months;
          const liqCash = cost * (liqPct / 100);
          const totalPreserved = liqCash + totalHolding;

          setMetric('holding_cost_bleed', '$' + Math.round(totalHolding).toLocaleString());
          setMetric('immediate_liquidated_cash', '$' + Math.round(liqCash).toLocaleString() + ' Cash');
          setMetric('effective_carrying_recovery', '+$' + Math.round(totalPreserved).toLocaleString() + ' Preserved');
          setMetric('monthly_storage_burn', '$' + monthlyBurn.toFixed(2) + ' / mo');
        """
    },
    {
        "slug": "retail-sales-per-square-foot",
        "category": "ecommerce",
        "name": "Retail Store Sales Per Square Foot & Space Productivity Calculator",
        "description": "Calculate retail store sales per square foot, analyze sales per selling foot versus backroom storage, and benchmark space productivity.",
        "hero_badge": "Brick & Mortar • Space Productivity",
        "formula_display": "Sales Per Sq Ft = Total Retail Sales / Total Store Selling Square Footage",
        "fields": [
            {"id": "annual_gross_store_sales", "label": "Annual Store Sales Revenue", "default": 1450000, "suffix": "$", "min": 50000, "max": 50000000, "step": 25000, "hint": "Gross in-store sales over past 12 months"},
            {"id": "total_retail_gross_sqft", "label": "Total Store Lease Footprint (Sq Ft)", "default": 3200, "suffix": "sq ft", "min": 200, "max": 100000, "step": 100, "hint": "Total leased physical premises square footage"},
            {"id": "selling_space_percentage", "label": "Selling Floor Area Share (%)", "default": 75.0, "suffix": "%", "min": 30, "max": 95, "step": 5, "hint": "Portion of store accessible to shoppers (excluding backroom/breakroom)"},
            {"id": "annual_lease_rent_total", "label": "Annual Lease Base Rent", "default": 115000, "suffix": "$", "min": 5000, "max": 2000000, "step": 2500, "hint": "Annual rent paid to commercial landlord"}
        ],
        "metrics": [
            {"id": "sales_per_selling_sqft", "label": "Sales Per Selling Sq Ft", "default_display": "$604.17 / sq ft", "highlight": True},
            {"id": "sales_per_gross_sqft", "label": "Sales Per Gross Leased Sq Ft", "default_display": "$453.13 / sq ft", "highlight": True},
            {"id": "rent_to_sales_occupancy_pct", "label": "Occupancy Cost Ratio (Rent to Sales)", "default_display": "7.93%", "highlight": True},
            {"id": "industry_productivity_tier", "label": "Store Productivity Classification", "default_display": "Strong Specialty Retail ($500 - $800)"}
        ],
        "proof_steps": [
            {"step_title": "Selling Floor Area", "step_text": "Selling Space = 3,200 total sq ft × 75.0% = 2,400 sq ft customer showroom area."},
            {"step_title": "Sales Per Selling Square Foot", "step_text": "Sales Per Selling Sq Ft = $1,450,000 / 2,400 sq ft = $604.17 per sq ft."},
            {"step_title": "Sales Per Gross Footprint", "step_text": "Sales Per Gross Sq Ft = $1,450,000 / 3,200 sq ft = $453.13 per sq ft."},
            {"step_title": "Occupancy Cost Burden", "step_text": "Rent to Sales Ratio = ($115,000 / $1,450,000) × 100 = 7.93% (well within healthy retail threshold of < 10%)."}
        ],
        "faqs": [
            {"q": "What is a good sales per square foot benchmark for retail?", "a": "Average specialty apparel retailers generate $300 to $450 per square foot. Elite retailers (like Apple, Lululemon, Tiffany) generate $1,000 to $5,000+ per square foot."},
            {"q": "What is the recommended occupancy cost percentage for retail leases?", "a": "Commercial retail occupancy cost (rent + CAM + taxes) should ideally remain between 6% and 10% of gross store revenue to maintain healthy store-level profitability."}
        ],
        "js_logic": """
          const sales = getNum('annual_gross_store_sales');
          const grossSqft = getNum('total_retail_gross_sqft');
          const sellingPct = getNum('selling_space_percentage');
          const rent = getNum('annual_lease_rent_total');

          const sellingSqft = grossSqft * (sellingPct / 100);
          if (sellingSqft > 0 && grossSqft > 0) {
            const salesPerSelling = sales / sellingSqft;
            const salesPerGross = sales / grossSqft;
            const occRatio = sales > 0 ? (rent / sales) * 100 : 0;

            let tier = 'Average Retail ($250 - $400)';
            if (salesPerSelling >= 500 && salesPerSelling < 800) tier = 'Strong Specialty Retail ($500 - $800)';
            else if (salesPerSelling >= 800) tier = 'Elite Tier Retail (> $800)';

            setMetric('sales_per_selling_sqft', '$' + salesPerSelling.toFixed(2) + ' / sq ft');
            setMetric('sales_per_gross_sqft', '$' + salesPerGross.toFixed(2) + ' / sq ft');
            setMetric('rent_to_sales_occupancy_pct', occRatio.toFixed(2) + '%');
            setMetric('industry_productivity_tier', tier);
          }
        """
    },
    {
        "slug": "direct-mail-catalog-roi",
        "category": "ecommerce",
        "name": "Direct Mail Postcard & Catalog Campaign ROI Calculator",
        "description": "Calculate Customer Acquisition Cost (CPA), breakeven response rate, and net ROI for direct mail postcard, flyer, and retail catalog campaigns.",
        "hero_badge": "Offline Marketing • Direct Mail ROI",
        "formula_display": "Breakeven Response Rate % = [Cost Per Piece / (AOV × Gross Margin %)] × 100 | ROI = [(Revenue - Cost) / Cost] × 100",
        "fields": [
            {"id": "total_pieces_mailed", "label": "Total Mailers Sent", "default": 25000, "suffix": "pieces", "min": 500, "max": 1000000, "step": 500, "hint": "Total postcards or catalogs mailed via USPS EDDM or targeted list"},
            {"id": "cost_per_piece_all_in", "label": "Cost Per Piece (Print + Postage + List)", "default": 0.85, "suffix": "$", "min": 0.25, "max": 5.0, "step": 0.05, "hint": "Printing, addressing, list rental, and USPS postage per mailer"},
            {"id": "average_order_value_aov", "label": "Average Order Value (AOV)", "default": 115.00, "suffix": "$", "min": 10, "max": 1000, "step": 5, "hint": "Average checkout value generated from mail response"},
            {"id": "campaign_response_rate_pct", "label": "Mail Response Rate (%)", "default": 1.80, "suffix": "%", "min": 0.1, "max": 10.0, "step": 0.1, "hint": "Percentage of recipients who make a purchase using promo code/QR"},
            {"id": "product_gross_margin_pct", "label": "Product Gross Margin (%)", "default": 65.0, "suffix": "%", "min": 15, "max": 95, "step": 1, "hint": "Gross margin after merchandise COGS"}
        ],
        "metrics": [
            {"id": "total_campaign_cost", "label": "Total Campaign Investment", "default_display": "$21,250", "highlight": True},
            {"id": "total_attributed_revenue", "label": "Total Generated Revenue", "default_display": "$51,750", "highlight": True},
            {"id": "net_campaign_roi_pct", "label": "Net Campaign ROI (%)", "default_display": "143.5%", "highlight": True},
            {"id": "cost_per_acquired_customer", "label": "Cost Per Acquired Customer (CPA)", "default_display": "$47.22 / customer"}
        ],
        "proof_steps": [
            {"step_title": "Total Campaign Expense", "step_text": "Campaign Cost = 25,000 mailers × $0.85 per piece = $21,250 total print and postage investment."},
            {"step_title": "Order Response Count", "step_text": "Orders = 25,000 pieces × 1.80% response rate = 450 customer orders."},
            {"step_title": "Top-Line Revenue & Profit Pool", "step_text": "Revenue = 450 orders × $115.00 AOV = $51,750. Gross Margin Dollars = $51,750 × 65.0% = $33,637.50."},
            {"step_title": "Net ROI & Customer Acquisition Cost", "step_text": "Net Profit = $33,637.50 gross profit - $21,250 cost = +$12,387.50. Net ROI = ($12,387.50 / $21,250) × 100 = 58.3% (or 143.5% top-line ROI). CPA = $21,250 / 450 = $47.22."}
        ],
        "faqs": [
            {"q": "What is an average response rate for direct mail in e-commerce?", "a": "According to the Association of National Advertisers (ANA), direct mail to a house list achieves a 3-5% response rate, while cold prospecting lists achieve a 1.0-2.0% response rate."},
            {"q": "Why is direct mail experiencing a resurgence for DTC brands?", "a": "As digital CPMs on Meta and Google continue to rise due to iOS privacy changes, tactile physical mail stands out with higher open rates and zero ad-blocker competition."}
        ],
        "js_logic": """
          const pieces = getNum('total_pieces_mailed');
          const unitCost = getNum('cost_per_piece_all_in');
          const aov = getNum('average_order_value_aov');
          const respPct = getNum('campaign_response_rate_pct');
          const marginPct = getNum('product_gross_margin_pct');

          const cost = pieces * unitCost;
          const orders = pieces * (respPct / 100);
          const rev = orders * aov;
          const grossProfit = rev * (marginPct / 100);
          const netProfit = grossProfit - cost;
          const roi = cost > 0 ? (netProfit / cost) * 100 : 0;
          const cpa = orders > 0 ? (cost / orders) : 0;

          setMetric('total_campaign_cost', '$' + Math.round(cost).toLocaleString());
          setMetric('total_attributed_revenue', '$' + Math.round(rev).toLocaleString());
          setMetric('net_campaign_roi_pct', roi.toFixed(1) + '%');
          setMetric('cost_per_acquired_customer', '$' + cpa.toFixed(2) + ' / customer');
        """
    },
    {
        "slug": "customs-import-duty-hts",
        "category": "ecommerce",
        "name": "Customs Import Duty & Section 301 Tariff Calculator",
        "description": "Calculate US customs import duties, Section 301 China trade tariffs, Merchandise Processing Fees (MPF), and Harbor Maintenance Fees (HMF).",
        "hero_badge": "International Trade • Customs Tariffs",
        "formula_display": "Total Customs Duty = Base Duty + Section 301 Tariff + MPF Fee (0.3464%) + HMF Fee (0.125%)",
        "fields": [
            {"id": "commercial_invoice_value", "label": "Commercial Invoice Customs Value (FOB $)", "default": 65000, "suffix": "$", "min": 1000, "max": 5000000, "step": 1000, "hint": "Transaction value declared to US Customs & Border Protection"},
            {"id": "base_hts_duty_rate_pct", "label": "Base HTS Tariff Duty Rate (%)", "default": 4.5, "suffix": "%", "min": 0, "max": 40, "step": 0.5, "hint": "Harmonized Tariff Schedule base duty rate for product code"},
            {"id": "section_301_tariff_rate_pct", "label": "Section 301 China Tariff Rate (%)", "default": 25.0, "suffix": "%", "min": 0, "max": 50, "step": 7.5, "hint": "Section 301 punitive tariff (e.g. 7.5% or 25% for China origin)"},
            {"id": "is_ocean_freight_shipment", "label": "Ocean Freight Entry (Subject to HMF)", "default": 1, "suffix": "1=Yes, 0=Air", "min": 0, "max": 1, "step": 1, "hint": "Ocean entries incur 0.125% Harbor Maintenance Fee"}
        ],
        "metrics": [
            {"id": "total_customs_duties_due", "label": "Total Customs Duties & Fees", "default_display": "$19,481.41", "highlight": True},
            {"id": "section_301_tariff_subtotal", "label": "Section 301 Tariff Portion", "default_display": "$16,250.00", "highlight": True},
            {"id": "effective_customs_rate_pct", "label": "Effective Customs Tariff Rate", "default_display": "29.97%", "highlight": True},
            {"id": "mpf_and_hmf_fees", "label": "Customs User Fees (MPF + HMF)", "default_display": "$306.41 Fees"}
        ],
        "proof_steps": [
            {"step_title": "Base HTS Duty", "step_text": "Base Duty = Commercial Value ($65,000) × 4.5% = $2,925.00."},
            {"step_title": "Section 301 China Trade Tariff", "step_text": "Section 301 Tariff = $65,000 × 25.0% = $16,250.00."},
            {"step_title": "Customs User Fees (MPF & HMF)", "step_text": "Merchandise Processing Fee (MPF) = $65,000 × 0.3464% = $225.16 (subject to CBP caps). Harbor Maintenance Fee (HMF) = $65,000 × 0.125% = $81.25. Total User Fees = $306.41."},
            {"step_title": "Total US Customs Obligation", "step_text": "Total Due = $2,925.00 + $16,250.00 + $306.41 = $19,481.41 (Effective Tariff Rate = 29.97%)."}
        ],
        "faqs": [
            {"q": "What is the US Merchandise Processing Fee (MPF)?", "a": "MPF is an ad valorem fee of 0.3464% assessed by US Customs on formal commercial entries, with a statutory minimum of $31.67 and a maximum cap of $614.35 (subject to annual inflation adjustments)."},
            {"q": "What is Section 301 tariff?", "a": "Section 301 of the Trade Act of 1974 imposes punitive additional tariffs (typically 7.5% or 25%) on thousands of goods manufactured in China, assessed in addition to standard HTS column 1 duty rates."}
        ],
        "js_logic": """
          const val = getNum('commercial_invoice_value');
          const basePct = getNum('base_hts_duty_rate_pct');
          const sec301Pct = getNum('section_301_tariff_rate_pct');
          const isOcean = getNum('is_ocean_freight_shipment');

          const baseDuty = val * (basePct / 100);
          const sec301Duty = val * (sec301Pct / 100);

          let mpf = val * 0.003464;
          if (mpf < 31.67) mpf = 31.67;
          if (mpf > 614.35) mpf = 614.35;

          const hmf = isOcean > 0 ? (val * 0.00125) : 0;
          const userFees = mpf + hmf;
          const totalDuties = baseDuty + sec301Duty + userFees;
          const effRate = val > 0 ? (totalDuties / val) * 100 : 0;

          setMetric('total_customs_duties_due', '$' + totalDuties.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setMetric('section_301_tariff_subtotal', '$' + sec301Duty.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
          setMetric('effective_customs_rate_pct', effRate.toFixed(2) + '%');
          setMetric('mpf_and_hmf_fees', '$' + userFees.toFixed(2) + ' Fees');
        """
    },
    {
        "slug": "retail-replenishment-lead-time-eoq",
        "category": "ecommerce",
        "name": "Economic Order Quantity (EOQ) & Total Cost of Inventory Calculator",
        "description": "Calculate the mathematically optimal Economic Order Quantity (EOQ) that minimizes the sum of inventory ordering costs and holding carrying costs.",
        "hero_badge": "Supply Chain Operations • EOQ Model",
        "formula_display": "EOQ = √[(2 · D · S) / H] | Total Cost = (D / Q) · S + (Q / 2) · H",
        "fields": [
            {"id": "annual_unit_demand_d", "label": "Annual Unit Demand (Units / Year)", "default": 12000, "suffix": "units", "min": 100, "max": 1000000, "step": 500, "hint": "Total quantity of units sold over a 12-month period (D)"},
            {"id": "fixed_order_cost_s", "label": "Fixed Cost Per Purchase Order (S)", "default": 150.00, "suffix": "$", "min": 10, "max": 5000, "step": 10, "hint": "Administrative PO processing, wire transfer fees, and receiving labor"},
            {"id": "annual_unit_holding_cost_h", "label": "Annual Holding Cost Per Unit (H)", "default": 3.60, "suffix": "$/unit/yr", "min": 0.20, "max": 100, "step": 0.20, "hint": "Annual cost to hold one unit in warehouse (storage + interest + insurance)"}
        ],
        "metrics": [
            {"id": "economic_order_quantity_eoq", "label": "Economic Order Quantity (EOQ)", "default_display": "1,000 Units / Order", "highlight": True},
            {"id": "total_annual_inventory_cost", "label": "Minimized Total Annual Inventory Cost", "default_display": "$3,600 / year", "highlight": True},
            {"id": "optimal_orders_per_year", "label": "Optimal Orders Per Year", "default_display": "12 Orders / Year", "highlight": True},
            {"id": "order_cycle_days", "label": "Optimal Order Interval", "default_display": "Every 30.4 Days"}
        ],
        "proof_steps": [
            {"step_title": "EOQ Square Root Derivation", "step_text": "EOQ = √[(2 × D × S) / H] = √[(2 × 12,000 × $150) / $3.60] = √[3,600,000 / 3.60] = √1,000,000 = 1,000 units."},
            {"step_title": "Annual Purchase Order Frequency", "step_text": "Orders Per Year = D / EOQ = 12,000 / 1,000 = 12 orders per year."},
            {"step_title": "Annual Ordering Cost", "step_text": "Annual Ordering Cost = 12 orders × $150.00 = $1,800.00."},
            {"step_title": "Annual Carrying Holding Cost", "step_text": "Average Inventory = EOQ / 2 = 500 units. Holding Cost = 500 × $3.60 = $1,800.00. Total Cost = $1,800 + $1,800 = $3,600.00 (Ordering costs exactly equal holding costs at the EOQ minimum)."}
        ],
        "faqs": [
            {"q": "What is the Ford W. Harris Economic Order Quantity (EOQ) formula?", "a": "Published in 1913, EOQ balances ordering costs (which decrease per unit as batch size rises) against holding costs (which increase linearly as batch size rises). The optimal order size occurs where ordering costs equal holding costs."},
            {"q": "What happens if a supplier has a Minimum Order Quantity (MOQ) higher than EOQ?", "a": "If supplier MOQ exceeds your EOQ, you are forced to order at the MOQ, accepting higher inventory holding costs to meet factory production requirements."}
        ],
        "js_logic": """
          const d = getNum('annual_unit_demand_d');
          const s = getNum('fixed_order_cost_s');
          const h = getNum('annual_unit_holding_cost_h');

          if (d > 0 && s > 0 && h > 0) {
            const eoq = Math.round(Math.sqrt((2 * d * s) / h));
            const numOrders = d / eoq;
            const orderCost = numOrders * s;
            const holdCost = (eoq / 2) * h;
            const totalCost = orderCost + holdCost;
            const cycleDays = 365 / numOrders;

            setMetric('economic_order_quantity_eoq', eoq.toLocaleString() + ' Units / Order');
            setMetric('total_annual_inventory_cost', '$' + Math.round(totalCost).toLocaleString() + ' / year');
            setMetric('optimal_orders_per_year', numOrders.toFixed(1) + ' Orders / Year');
            setMetric('order_cycle_days', 'Every ' + cycleDays.toFixed(1) + ' Days');
          }
        """
    }
]
