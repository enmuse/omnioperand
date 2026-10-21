"""
scripts/data_logistics_freight.py
25 High-Value Freight, Logistics, Supply Chain & Warehousing Engineering Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

LOGISTICS_CALCULATORS = [
    {
        "slug": "dim-weight-calculator",
        "category": "logistics",
        "name": "Dimensional Weight (DIM Factor 139 / 166) Calculator",
        "description": "Calculate volumetric dimensional weight, billable weight, and carrier rate adjustments for FedEx, UPS, DHL, and USPS domestic and international parcels.",
        "hero_badge": "Parcel Logistics • Volumetric Rating",
        "formula_display": "DIM Weight (lbs) = (Length × Width × Height in inches) / DIM Divisor (139 or 166)",
        "fields": [
            {"id": "box_length_in", "label": "Box Length (Inches)", "default": 24.0, "suffix": "in", "min": 1, "max": 108, "step": 0.5, "hint": "Longest package dimension"},
            {"id": "box_width_in", "label": "Box Width (Inches)", "default": 18.0, "suffix": "in", "min": 1, "max": 72, "step": 0.5, "hint": "Second package dimension"},
            {"id": "box_height_in", "label": "Box Height (Inches)", "default": 16.0, "suffix": "in", "min": 1, "max": 72, "step": 0.5, "hint": "Third package dimension"},
            {"id": "actual_weight_lbs", "label": "Actual Scale Weight (lbs)", "default": 22.0, "suffix": "lbs", "min": 0.5, "max": 150, "step": 0.5, "hint": "Physical weight measured on postal scale"},
            {"id": "dim_divisor", "label": "Carrier DIM Factor (139 = FedEx/UPS Daily, 166 = USPS/Retail)", "default": 139, "min": 115, "max": 250, "step": 1, "hint": "Standard commercial divisor is 139, retail is 166"}
        ],
        "metrics": [
            {"id": "billable_weight_lbs", "label": "Carrier Billable Weight", "default_display": "50.0 lbs", "highlight": True},
            {"id": "dimensional_weight_lbs", "label": "Calculated DIM Weight", "default_display": "49.8 lbs (Billed as 50 lbs)", "highlight": True},
            {"id": "package_volume_cuft", "label": "Total Package Volume", "default_display": "4.00 cu ft"},
            {"id": "dim_premium_pct", "label": "Volumetric Weight Penalty", "default_display": "+127% Above Scale Weight"}
        ],
        "proof_steps": [
            {"step_title": "Cubic Volume Calculation", "step_text": "Cubic Inches = 24 × 18 × 16 = 6,912 cu in. In cubic feet: 6,912 / 1,728 = 4.00 cu ft."},
            {"step_title": "Volumetric DIM Weight Derivation", "step_text": "DIM Weight = Cubic Inches / Divisor. 6,912 / 139 = 49.73 lbs."},
            {"step_title": "Commercial Carrier Rounding Rule", "step_text": "Carriers always round fractions of a pound UP to the next whole integer. 49.73 lbs rounds to 50 lbs."},
            {"step_title": "Billable Weight Selection", "step_text": "Billable Weight = Max(Actual Weight, DIM Weight) = Max(22.0, 50.0) = 50.0 lbs. The shipper pays for 28 lbs of empty air."}
        ],
        "faqs": [
            {"q": "What is the standard DIM divisor for FedEx and UPS?", "a": "FedEx and UPS apply a DIM divisor of 139 for all domestic and international shipments under standard daily commercial account tariffs. Retail counter rates often use 166."},
            {"q": "How can e-commerce shippers avoid DIM weight penalties?", "a": "Use custom-sized boxes, poly-mailers for soft goods, or carton-resizing automated pack stations. Trimming just 2 inches off each dimension can cut billable weight by 35%!"}
        ],
        "js_logic": """
          const l = getNum('box_length_in');
          const w = getNum('box_width_in');
          const h = getNum('box_height_in');
          const act = getNum('actual_weight_lbs');
          const div = getNum('dim_divisor') || 139;

          const cuIn = l * w * h;
          const cuFt = cuIn / 1728;
          const rawDim = cuIn / div;
          const billedDim = Math.ceil(rawDim);
          const billable = Math.max(act, billedDim);
          const penalty = act > 0 ? ((billable - act) / act) * 100 : 0;

          setDisp('billable_weight_lbs', billable.toFixed(1) + ' lbs');
          setDisp('dimensional_weight_lbs', rawDim.toFixed(1) + ' lbs (Billed as ' + billedDim + ' lbs)');
          setDisp('package_volume_cuft', cuFt.toFixed(2) + ' cu ft');
          setDisp('dim_premium_pct', (penalty > 0 ? '+' : '') + Math.round(penalty) + '% vs Scale');
        """
    },
    {
        "slug": "pallet-ti-hi-optimizer",
        "category": "logistics",
        "name": "Pallet Ti-Hi & Carton Stacking Pattern Calculator",
        "description": "Calculate optimal Tie (cases per layer) and High (layers per pallet) for standard GMA 48x40 pallets, maximizing cube utilization without overhang.",
        "hero_badge": "Warehousing • Palletization Matrix",
        "formula_display": "Total Cartons = Tie (cartons/layer) × High (layers) | Max Height ≤ 52\" (or 96\" for double stack)",
        "fields": [
            {"id": "carton_length_in", "label": "Carton Length (Inches)", "default": 16.0, "suffix": "in", "min": 4, "max": 48, "step": 0.5, "hint": "External case length"},
            {"id": "carton_width_in", "label": "Carton Width (Inches)", "default": 10.0, "suffix": "in", "min": 3, "max": 40, "step": 0.5, "hint": "External case width"},
            {"id": "carton_height_in", "label": "Carton Height (Inches)", "default": 8.0, "suffix": "in", "min": 2, "max": 36, "step": 0.5, "hint": "External case height"},
            {"id": "carton_weight_lbs", "label": "Gross Carton Weight (lbs)", "default": 24.0, "suffix": "lbs", "min": 1, "max": 100, "step": 0.5, "hint": "Weight per individual carton"},
            {"id": "max_pallet_height_in", "label": "Max Allowed Pallet Height (Inches)", "default": 54.0, "suffix": "in", "min": 30, "max": 96, "step": 2, "hint": "Standard GMA rack clearance (includes 5.5\" wooden pallet)"}
        ],
        "metrics": [
            {"id": "ti_hi_configuration", "label": "Optimal Ti × Hi Pattern", "default_display": "12 Tie × 6 High", "highlight": True},
            {"id": "total_cartons_pallet", "label": "Total Cases Per Pallet", "default_display": "72 Cartons", "highlight": True},
            {"id": "total_pallet_weight", "label": "Gross Pallet Weight", "default_display": "1,778 lbs (Incl. Pallet)", "highlight": True},
            {"id": "area_utilization_pct", "label": "Pallet Deck Surface Efficiency", "default_display": "92.0% Coverage"}
        ],
        "proof_steps": [
            {"step_title": "Standard GMA Pallet Footprint", "step_text": "GMA standard pallet deck = 48\" L × 40\" W = 1,920 sq inches surface area with 5.5\" pallet base height."},
            {"step_title": "Maximum Stacking Layers (High)", "step_text": "Usable height = Max Height - 5.5\" wooden pallet. 54\" - 5.5\" = 48.5\". High = Floor(48.5\" / 8\" case) = 6 layers."},
            {"step_title": "Surface Packing (Tie)", "step_text": "Packing 16\" × 10\" cartons into 48\" × 40\": 3 lengthwise (3 × 16 = 48\") by 4 widthwise (4 × 10 = 40\") = exactly 12 cartons per layer with zero overhang."},
            {"step_title": "Payload Mass Quantification", "step_text": "Cartons = 12 × 6 = 72 cases. Cargo Weight = 72 × 24 lbs = 1,728 lbs. Gross Weight = 1,728 + 50 lb GMA wood pallet = 1,778 lbs."}
        ],
        "faqs": [
            {"q": "What is the maximum weight a standard wood pallet can hold?", "a": "A standard 48x40 grade-A hardwood GMA pallet has a dynamic load capacity of 2,800 lbs in transit and a static load rating of up to 4,500 lbs on flat concrete warehouse floors."},
            {"q": "Why is pallet overhang prohibited by major retailers?", "a": "Overhanging cartons by even 1 inch reduces box compression strength by up to 30%, leads to crushed corners during forklift transit, and causes snagging on warehouse racking beams."}
        ],
        "js_logic": """
          const l = getNum('carton_length_in');
          const w = getNum('carton_width_in');
          const h = getNum('carton_height_in');
          const wt = getNum('carton_weight_lbs');
          const maxH = getNum('max_pallet_height_in') || 54;

          const usableH = Math.max(10, maxH - 5.5);
          const hi = Math.max(1, Math.floor(usableH / (h || 8)));

          const ti1 = Math.floor(48 / l) * Math.floor(40 / w);
          const ti2 = Math.floor(48 / w) * Math.floor(40 / l);
          const ti = Math.max(ti1, ti2, 4);

          const total = ti * hi;
          const grossWt = (total * wt) + 48;
          const areaCovered = (ti * l * w) / 1920 * 100;

          setDisp('ti_hi_configuration', ti + ' Tie × ' + hi + ' High');
          setDisp('total_cartons_pallet', total + ' Cartons');
          setDisp('total_pallet_weight', Math.round(grossWt).toLocaleString() + ' lbs');
          setDisp('area_utilization_pct', Math.min(100, areaCovered).toFixed(1) + '% Coverage');
        """
    },
    {
        "slug": "freight-density-nmfc",
        "category": "logistics",
        "name": "Freight Density & NMFC Freight Class Calculator",
        "description": "Calculate shipment density in pounds per cubic foot (PCF) and determine the National Motor Freight Classification (NMFC) freight class for LTL shipping.",
        "hero_badge": "LTL Freight • NMFC Classification",
        "formula_display": "Density (PCF) = Total Weight (lbs) / (Length × Width × Height / 1,728)",
        "fields": [
            {"id": "shipment_length_in", "label": "Pallet Length (Inches)", "default": 48.0, "suffix": "in", "min": 10, "max": 120, "step": 1, "hint": "Length of packaged skid"},
            {"id": "shipment_width_in", "label": "Pallet Width (Inches)", "default": 40.0, "suffix": "in", "min": 10, "max": 96, "step": 1, "hint": "Width of packaged skid"},
            {"id": "shipment_height_in", "label": "Pallet Height (Inches)", "default": 48.0, "suffix": "in", "min": 10, "max": 108, "step": 1, "hint": "Height from floor to top of load"},
            {"id": "shipment_weight_lbs", "label": "Total Gross Weight (lbs)", "default": 650.0, "suffix": "lbs", "min": 25, "max": 10000, "step": 10, "hint": "Total scale weight including pallet"}
        ],
        "metrics": [
            {"id": "calculated_density_pcf", "label": "Shipment Density (PCF)", "default_display": "12.2 PCF", "highlight": True},
            {"id": "recommended_nmfc_class", "label": "Standard NMFC Freight Class", "default_display": "Class 85", "highlight": True},
            {"id": "total_cubic_feet", "label": "Total Shipment Volume", "default_display": "53.3 cu ft"},
            {"id": "ltl_rate_impact", "label": "Freight Rate Pricing Tier", "default_display": "Medium Density (Standard)"}
        ],
        "proof_steps": [
            {"step_title": "Shipment Cubic Footage", "step_text": "Cubic Inches = 48 × 40 × 48 = 92,160 cu in. Volume = 92,160 / 1,728 = 53.33 cubic feet."},
            {"step_title": "Density Formulation", "step_text": "Density = Total Weight / Volume = 650 lbs / 53.33 cu ft = 12.19 pounds per cubic foot (PCF)."},
            {"step_title": "NMFC Density Matrix Lookup", "step_text": "Standard NMFC density tiers: >50 PCF = Class 50; 35-50 PCF = Class 55; 12-15 PCF = Class 85; 8-10 PCF = Class 110; 4-6 PCF = Class 175; <1 PCF = Class 500."},
            {"step_title": "Classification Assignment", "step_text": "At 12.2 PCF, the cargo qualifies as Class 85. Lower numbers yield lower freight rates per hundredweight."}
        ],
        "faqs": [
            {"q": "What does NMFC freight class mean in trucking?", "a": "The National Motor Freight Traffic Association (NMFTA) classifies all freight into 18 classes (from 50 to 500) based on four transportability characteristics: density, stowability, handling, and liability."},
            {"q": "Why does low density freight cost more to ship per pound?", "a": "Low density freight (e.g. ping pong balls, lampshades) fills up a semi-trailer's volume ('cubes out') long before reaching the truck's 45,000-lb legal weight limit, forcing the carrier to charge higher rates per pound."}
        ],
        "js_logic": """
          const l = getNum('shipment_length_in');
          const w = getNum('shipment_width_in');
          const h = getNum('shipment_height_in');
          const wt = getNum('shipment_weight_lbs');

          const cuFt = (l * w * h) / 1728;
          const pcf = cuFt > 0 ? (wt / cuFt) : 0;

          let nmfc = 'Class 100';
          let tier = 'Standard General Freight';
          if (pcf >= 50) { nmfc = 'Class 50'; tier = 'Ultra Dense (Cheapest)'; }
          else if (pcf >= 35) { nmfc = 'Class 55'; tier = 'Heavy Machinery / Steel'; }
          else if (pcf >= 30) { nmfc = 'Class 60'; tier = 'Dense Packaged Goods'; }
          else if (pcf >= 22.5) { nmfc = 'Class 65'; tier = 'Canned Goods / Hardware'; }
          else if (pcf >= 15) { nmfc = 'Class 70'; tier = 'Medium-High Density'; }
          else if (pcf >= 13.5) { nmfc = 'Class 77.5'; tier = 'Standard Palletized Freight'; }
          else if (pcf >= 12) { nmfc = 'Class 85'; tier = 'Medium Density'; }
          else if (pcf >= 10.5) { nmfc = 'Class 92.5'; tier = 'Medium-Low Density'; }
          else if (pcf >= 9) { nmfc = 'Class 100'; tier = 'General Freight'; }
          else if (pcf >= 8) { nmfc = 'Class 110'; tier = 'Light Industrial Goods'; }
          else if (pcf >= 7) { nmfc = 'Class 125'; tier = 'Medium-Light Freight'; }
          else if (pcf >= 6) { nmfc = 'Class 150'; tier = 'Bulky Boxed Goods'; }
          else if (pcf >= 4) { nmfc = 'Class 200'; tier = 'Very Bulky / Furniture'; }
          else if (pcf >= 2) { nmfc = 'Class 300'; tier = 'Low Density Bulky'; }
          else { nmfc = 'Class 500'; tier = 'Ultra-Light / Ping Pong Balls'; }

          setDisp('calculated_density_pcf', pcf.toFixed(1) + ' PCF');
          setDisp('recommended_nmfc_class', nmfc);
          setDisp('total_cubic_feet', cuFt.toFixed(1) + ' cu ft');
          setDisp('ltl_rate_impact', tier);
        """
    },
    {
        "slug": "ftl-vs-ltl-freight",
        "category": "logistics",
        "name": "Full Truckload (FTL) vs Less-Than-Truckload (LTL) Cost Breakeven",
        "description": "Calculate whether shipping high-volume palletized freight is cheaper via Less-Than-Truckload (LTL) or dedicated Full Truckload (FTL) dry van.",
        "hero_badge": "Freight Procurement • Breakeven Analysis",
        "formula_display": "Breakeven Pallets = Dedicated FTL Flat Rate / LTL Rate Per Pallet",
        "fields": [
            {"id": "pallet_count", "label": "Number of Pallets to Ship", "default": 8, "suffix": "pallets", "min": 1, "max": 26, "step": 1, "hint": "Standard 48x40 pallets (max 26 in a 53ft trailer)"},
            {"id": "ltl_rate_per_pallet", "label": "Average LTL Cost per Pallet ($)", "default": 245, "prefix": "$", "min": 75, "max": 800, "step": 10, "hint": "Quoted LTL tariff per skid including accessorials"},
            {"id": "dedicated_ftl_rate", "label": "Dedicated FTL Flat Lane Rate ($)", "default": 2150, "prefix": "$", "min": 500, "max": 7500, "step": 50, "hint": "Point-to-point flatbed or 53ft dry van spot rate"}
        ],
        "metrics": [
            {"id": "cheapest_shipping_mode", "label": "Most Cost-Effective Mode", "default_display": "LTL Saves ~$190.00", "highlight": True},
            {"id": "breakeven_pallet_count", "label": "FTL Breakeven Threshold", "default_display": "8.8 Pallets", "highlight": True},
            {"id": "total_ltl_cost", "label": "Total LTL Shipping Cost", "default_display": "$1,960.00"},
            {"id": "ftl_capacity_used_pct", "label": "Trailer Space Utilization", "default_display": "30.8% of 53ft Van"}
        ],
        "proof_steps": [
            {"step_title": "LTL Aggregate Cost Formulation", "step_text": "Total LTL Cost = Pallet Count × Rate per Pallet. 8 pallets × $245 = $1,960.00."},
            {"step_title": "FTL Breakeven Derivation", "step_text": "N_breakeven = FTL Flat Rate / LTL Cost per Pallet. $2,150 / $245 = 8.78 pallets."},
            {"step_title": "Cost Decision Threshold", "step_text": "If shipping ≤ 8 pallets, LTL is cheaper. At 9 pallets or more ($2,205 LTL vs $2,150 FTL), booking a dedicated FTL trailer saves money."},
            {"step_title": "Speed & Damage Secondary Tradeoff", "step_text": "FTL moves directly dock-to-dock with zero transshipment terminals, eliminating transit delays and cross-dock forklift damage risk."}
        ],
        "faqs": [
            {"q": "How many pallets fit in a standard 53-foot dry van trailer?", "a": "A 53ft dry van holds 26 single-stacked 48x40 pallets (straight loading) or up to 30 pallets with turned/pinwheeled loading. Double-stacking increases capacity to 52 pallets if weight allows."},
            {"q": "What is Volume LTL / Partial Truckload?", "a": "Volume LTL (or partial truckload) bridges the gap for shipments of 6 to 14 pallets that are too large for standard LTL hub-and-spoke networks but don't justify a full dedicated truckload."}
        ],
        "js_logic": """
          const pallets = getNum('pallet_count');
          const ltlRate = getNum('ltl_rate_per_pallet');
          const ftlRate = getNum('dedicated_ftl_rate');

          const ltlTotal = pallets * ltlRate;
          const breakeven = ltlRate > 0 ? (ftlRate / ltlRate) : 9;
          const delta = Math.abs(ltlTotal - ftlRate);
          const winner = ltlTotal < ftlRate ? 'LTL Saves ~$' + Math.round(delta) : 'FTL Saves ~$' + Math.round(delta);
          const space = (pallets / 26) * 100;

          setDisp('cheapest_shipping_mode', winner);
          setDisp('breakeven_pallet_count', breakeven.toFixed(1) + ' Pallets');
          setDisp('total_ltl_cost', '$' + Math.round(ltlTotal).toLocaleString());
          setDisp('ftl_capacity_used_pct', space.toFixed(1) + '% of 53ft Van');
        """
    },
    {
        "slug": "container-cbm-utilization",
        "category": "logistics",
        "name": "Ocean Shipping Container CBM Volume & Payload Calculator",
        "description": "Calculate cubic meter (CBM) volume, metric ton payload capacity, and container utilization percentage for 20ft, 40ft, and 40ft High Cube (HC) ocean containers.",
        "hero_badge": "Ocean Freight • Container Utilization",
        "formula_display": "Total CBM = Total Cartons × (Length × Width × Height in meters) | 1 CBM = 35.315 cu ft",
        "fields": [
            {"id": "carton_count", "label": "Total Number of Cartons", "default": 850, "suffix": "cartons", "min": 10, "max": 10000, "step": 10, "hint": "Total packaged shipping cartons"},
            {"id": "carton_l_cm", "label": "Carton Length (cm)", "default": 45, "suffix": "cm", "min": 10, "max": 200, "step": 1, "hint": "External case length"},
            {"id": "carton_w_cm", "label": "Carton Width (cm)", "default": 35, "suffix": "cm", "min": 10, "max": 150, "step": 1, "hint": "External case width"},
            {"id": "carton_h_cm", "label": "Carton Height (cm)", "default": 30, "suffix": "cm", "min": 10, "max": 150, "step": 1, "hint": "External case height"},
            {"id": "carton_weight_kg", "label": "Weight per Carton (kg)", "default": 14.5, "suffix": "kg", "min": 0.5, "max": 100, "step": 0.5, "hint": "Weight per case in kilograms"}
        ],
        "metrics": [
            {"id": "total_cargo_cbm", "label": "Total Cargo Volume (CBM)", "default_display": "40.2 CBM", "highlight": True},
            {"id": "best_container_type", "label": "Recommended Container", "default_display": "1x 40ft Standard (59% full)", "highlight": True},
            {"id": "total_cargo_mass_kg", "label": "Total Cargo Weight", "default_display": "12,325 kg (12.33 MT)", "highlight": True},
            {"id": "weight_utilization_pct", "label": "Payload Weight Allowance", "default_display": "46.5% of 26,500 kg limit"}
        ],
        "proof_steps": [
            {"step_title": "Individual Carton CBM", "step_text": "CBM per case = (45 / 100) × (35 / 100) × (30 / 100) = 0.45 × 0.35 × 0.30 = 0.04725 m³."},
            {"step_title": "Total Cargo Volume", "step_text": "Total CBM = 850 cartons × 0.04725 m³ = 40.16 CBM."},
            {"step_title": "Ocean Container Standard Capacities", "step_text": "20ft Container = 33.2 CBM (usable ~28 CBM, max payload 21,700 kg). 40ft Standard = 67.7 CBM (usable ~58 CBM, max payload 26,500 kg). 40ft High Cube = 76.3 CBM (usable ~68 CBM)."},
            {"step_title": "Container Equipment Assignment", "step_text": "Because 40.2 CBM exceeds a 20ft box (28 CBM max usable), a 40ft GP container is required, utilizing 59% of cubic volume and 46.5% of maximum allowable weight."}
        ],
        "faqs": [
            {"q": "What is the practical usable volume of a shipping container?", "a": "Due to carton nesting limitations, ceiling clearance, and door latch gaps, experienced freight forwarders plan on 85% of theoretical volume: ~28 CBM for a 20ft box, ~58 CBM for a 40ft box, and ~68 CBM for a 40ft High Cube."},
            {"q": "What is the difference between a 40ft Standard and 40ft High Cube?", "a": "A 40ft High Cube container is exactly 1 foot taller (9'6\" external vs 8'6\" standard), providing ~13% more cubic volume for roughly the same ocean freight shipping rate."}
        ],
        "js_logic": """
          const count = getNum('carton_count');
          const l = getNum('carton_l_cm') / 100;
          const w = getNum('carton_w_cm') / 100;
          const h = getNum('carton_h_cm') / 100;
          const wt = getNum('carton_weight_kg');

          const singleCbm = l * w * h;
          const totalCbm = count * singleCbm;
          const totalKg = count * wt;

          let reco = '';
          if (totalCbm <= 28 && totalKg <= 21700) {
            reco = '1x 20ft Standard (' + Math.round((totalCbm / 28) * 100) + '% full)';
          } else if (totalCbm <= 58 && totalKg <= 26500) {
            reco = '1x 40ft Standard (' + Math.round((totalCbm / 58) * 100) + '% full)';
          } else if (totalCbm <= 68 && totalKg <= 26500) {
            reco = '1x 40ft High Cube (' + Math.round((totalCbm / 68) * 100) + '% full)';
          } else {
            const boxes = Math.ceil(totalCbm / 65);
            reco = boxes + 'x 40ft Containers Required';
          }

          setDisp('total_cargo_cbm', totalCbm.toFixed(1) + ' CBM');
          setDisp('best_container_type', reco);
          setDisp('total_cargo_mass_kg', Math.round(totalKg).toLocaleString() + ' kg (' + (totalKg / 1000).toFixed(2) + ' MT)');
          setDisp('weight_utilization_pct', ((totalKg / 26500) * 100).toFixed(1) + '% of Max Payload');
        """
    },
    {
        "slug": "reorder-point-safety-stock",
        "category": "logistics",
        "name": "Reorder Point (ROP) & Safety Stock Volatility Calculator",
        "description": "Calculate statistical reorder point (ROP) and safety stock inventory buffers using Z-score service levels, daily demand variation, and supplier lead time.",
        "hero_badge": "Inventory Science • Demand Volatility",
        "formula_display": "ROP = (Daily Demand × Lead Time) + (Z × √[Lead Time × σ_demand² + Demand² × σ_leadtime²])",
        "fields": [
            {"id": "avg_daily_demand", "label": "Average Daily Sales Demand (Units)", "default": 85, "suffix": "units/day", "min": 1, "max": 10000, "step": 5, "hint": "Mean daily unit sales volume"},
            {"id": "std_dev_demand", "label": "Daily Demand Standard Deviation (σ_d)", "default": 18, "suffix": "units", "min": 0, "max": 500, "step": 1, "hint": "Volatility in day-to-day sales"},
            {"id": "lead_time_days", "label": "Supplier Lead Time (Days)", "default": 21, "suffix": "days", "min": 1, "max": 180, "step": 1, "hint": "Average elapsed days from PO issuance to dock receipt"},
            {"id": "service_level_pct", "label": "Target In-Stock Service Level (%)", "default": 95, "suffix": "%", "min": 80, "max": 99.9, "step": 1, "hint": "95% (Z=1.65), 98% (Z=2.05), 99% (Z=2.33)"}
        ],
        "metrics": [
            {"id": "reorder_point_units", "label": "Optimal Reorder Point (ROP)", "default_display": "1,921 Units", "highlight": True},
            {"id": "safety_stock_units", "label": "Calculated Safety Stock Buffer", "default_display": "136 Units", "highlight": True},
            {"id": "lead_time_demand", "label": "Expected Lead Time Demand", "default_display": "1,785 Units"},
            {"id": "stockout_risk_pct", "label": "Theoretical Stockout Probability", "default_display": "5.0% Risk"}
        ],
        "proof_steps": [
            {"step_title": "Base Lead Time Demand", "step_text": "Expected Lead Time Demand D_L = Daily Demand × Lead Time = 85 × 21 = 1,785 units."},
            {"step_title": "Standard Deviation over Lead Time", "step_text": "σ_LT = √(Lead Time) × σ_demand = √21 × 18 = 4.5826 × 18 = 82.49 units."},
            {"step_title": "Z-Factor Service Level Multiplier", "step_text": "A 95% cycle service level corresponds to a standard normal Z-score of 1.645."},
            {"step_title": "Safety Stock & Reorder Point", "step_text": "Safety Stock SS = Z × σ_LT = 1.645 × 82.49 = 135.7 ≈ 136 units. Reorder Point ROP = 1,785 + 136 = 1,921 units. Place PO the moment stock touches 1,921."}
        ],
        "faqs": [
            {"q": "What happens if I set service level to 99% vs 95%?", "a": "Moving from 95% (Z=1.65) to 99% (Z=2.33) requires increasing your safety stock buffer by over 41%, tying up substantially more working capital in warehouse inventory to protect against rare demand surges."},
            {"q": "What is the most effective way to lower the Reorder Point?", "a": "Shortening supplier lead times (e.g. nearshoring from 60 days to 14 days) drastically shrinks both lead time demand and the lead time standard deviation √L, slashing required safety stock."}
        ],
        "js_logic": """
          const d = getNum('avg_daily_demand');
          const sd = getNum('std_dev_demand');
          const lt = getNum('lead_time_days');
          const sl = getNum('service_level_pct') || 95;

          let z = 1.645;
          if (sl >= 99) z = 2.326;
          else if (sl >= 98) z = 2.054;
          else if (sl >= 95) z = 1.645;
          else if (sl >= 90) z = 1.282;
          else z = 1.0;

          const leadDemand = d * lt;
          const sigmaLt = Math.sqrt(lt) * sd;
          const ss = Math.ceil(z * sigmaLt);
          const rop = leadDemand + ss;

          setDisp('reorder_point_units', Math.round(rop).toLocaleString() + ' Units');
          setDisp('safety_stock_units', Math.round(ss).toLocaleString() + ' Units');
          setDisp('lead_time_demand', Math.round(leadDemand).toLocaleString() + ' Units');
          setDisp('stockout_risk_pct', (100 - sl).toFixed(1) + '% Risk');
        """
    },
    {
        "slug": "economic-order-quantity-eoq",
        "category": "logistics",
        "name": "Economic Order Quantity (EOQ) & Annual Holding Cost Calculator",
        "description": "Calculate optimal purchasing batch size (EOQ), annual ordering frequency, and minimized total inventory holding costs (Ford W. Harris formula).",
        "hero_badge": "Inventory Optimization • EOQ Formulation",
        "formula_display": "EOQ = √[(2 · Annual Demand · Order Cost) / Annual Holding Cost per Unit]",
        "fields": [
            {"id": "annual_unit_demand", "label": "Annual Demand (Units/Year)", "default": 12000, "suffix": "units/yr", "min": 100, "max": 1000000, "step": 250, "hint": "Total annual sales demand in units"},
            {"id": "order_setup_cost", "label": "Fixed Cost per Purchase Order ($)", "default": 75, "prefix": "$", "min": 5, "max": 1000, "step": 5, "hint": "Labor, PO processing, customs documentation, receiving fee"},
            {"id": "unit_purchase_cost", "label": "Unit Item Cost ($)", "default": 45, "prefix": "$", "min": 1, "max": 5000, "step": 1, "hint": "Cost of goods purchased from manufacturer"},
            {"id": "holding_cost_rate_pct", "label": "Annual Carrying Cost Rate (%)", "default": 20, "suffix": "%", "min": 5, "max": 40, "step": 1, "hint": "Warehousing, insurance, capital cost, obsolescence (typically 18-25%)"}
        ],
        "metrics": [
            {"id": "optimal_eoq_units", "label": "Economic Order Quantity (EOQ)", "default_display": "447 Units", "highlight": True},
            {"id": "annual_orders_count", "label": "Optimal Orders Per Year", "default_display": "26.8 Orders / Year", "highlight": True},
            {"id": "min_total_inventory_cost", "label": "Total Annual Inventory Cost", "default_display": "$4,025.00 / yr"},
            {"id": "cycle_inventory_days", "label": "Days of Supply Per Order", "default_display": "13.6 Days"}
        ],
        "proof_steps": [
            {"step_title": "Unit Holding Cost H Derivation", "step_text": "H = Unit Cost × Carrying Cost% = $45 × 0.20 = $9.00 per unit per year."},
            {"step_title": "EOQ Radical Derivation", "step_text": "EOQ = √[(2 × D × S) / H] = √[(2 × 12,000 × $75) / $9.00] = √[1,800,000 / 9] = √200,000 = 447.2 units."},
            {"step_title": "Order Frequency Optimization", "step_text": "Orders per year = 12,000 / 447.2 = 26.83 orders (placing a PO roughly every 13.6 days)."},
            {"step_title": "Annual Cost Parity Invariant", "step_text": "At exact EOQ, Annual Ordering Cost ($75 × 26.83 = $2,012.50) exactly equals Annual Holding Cost (447.2 / 2 × $9.00 = $2,012.50). Total minimized cost = $4,025.00."}
        ],
        "faqs": [
            {"q": "What components make up inventory holding cost rate (%)?", "a": "Holding cost rate typically comprises: cost of capital (8-12%), warehouse storage and utility rent (3-5%), insurance and taxes (2-3%), and shrinkage/obsolescence risk (3-6%), totaling 18% to 26% annually."},
            {"q": "How do supplier MOQ (Minimum Order Quantity) rules affect EOQ?", "a": "If a factory's MOQ is 1,000 units but your EOQ is 447 units, ordering the MOQ increases your average inventory and holding cost, but may unlock volume tiered price discounts that offset the penalty."}
        ],
        "js_logic": """
          const d = getNum('annual_unit_demand');
          const s = getNum('order_setup_cost');
          const c = getNum('unit_purchase_cost');
          const i = (getNum('holding_cost_rate_pct') || 20) / 100;

          const h = c * i;
          const eoq = h > 0 ? Math.sqrt((2 * d * s) / h) : 100;
          const orders = eoq > 0 ? (d / eoq) : 0;
          const orderCost = orders * s;
          const holdCost = (eoq / 2) * h;
          const totalCost = orderCost + holdCost;
          const daysSupply = orders > 0 ? (365 / orders) : 0;

          setDisp('optimal_eoq_units', Math.round(eoq) + ' Units');
          setDisp('annual_orders_count', orders.toFixed(1) + ' Orders / Year');
          setDisp('min_total_inventory_cost', '$' + Math.round(totalCost).toLocaleString() + ' / yr');
          setDisp('cycle_inventory_days', daysSupply.toFixed(1) + ' Days');
        """
    },
    {
        "slug": "forklift-aisle-turning-radius",
        "category": "logistics",
        "name": "Warehouse Aisle Width & Forklift Turning Radius Calculator",
        "description": "Calculate minimum clear rack-to-rack aisle width for counterbalance, reach trucks, and turret VNA forklifts compliant with OSHA safety clearances.",
        "hero_badge": "Facility Engineering • Aisle Clearances",
        "formula_display": "Aisle Width = Turning Radius (TR) + Load Distance (L) + Load Length (b) + Safety Clearance (typically 6\" - 12\")",
        "fields": [
            {"id": "truck_turning_radius_in", "label": "Forklift Turning Radius (Inches)", "default": 85.0, "suffix": "in", "min": 40, "max": 160, "step": 1, "hint": "Manufacturer specification outer turning radius (Wa)"},
            {"id": "load_length_in", "label": "Pallet Load Depth (Inches)", "default": 48.0, "suffix": "in", "min": 24, "max": 72, "step": 1, "hint": "Standard GMA pallet depth = 48 inches"},
            {"id": "load_distance_in", "label": "Front Axle to Fork Face Distance (Inches)", "default": 16.0, "suffix": "in", "min": 5, "max": 30, "step": 0.5, "hint": "Horizontal distance from drive tire center to fork heel (x)"},
            {"id": "forklift_type", "label": "Forklift Class (1 = Standard Counterbalance, 2 = Narrow Reach Truck, 3 = Turret VNA)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "Counterbalance ~12-13ft, Reach ~8.5-9.5ft, VNA ~5.5-6ft"}
        ],
        "metrics": [
            {"id": "min_aisle_width_ft", "label": "Minimum Clear Aisle Width", "default_display": "13.2 ft (158 inches)", "highlight": True},
            {"id": "safety_clearance_in", "label": "OSHA Operating Safety Clearance", "default_display": "12.0 inches", "highlight": True},
            {"id": "storage_density_category", "label": "Aisle Density Category", "default_display": "Standard Wide Aisle (WA)"},
            {"id": "aisle_width_meters", "label": "Metric Dimension", "default_display": "4.01 meters"}
        ],
        "proof_steps": [
            {"step_title": "Geometric 90-Degree Stacking Aisle Formula", "step_text": "Basic Aisle Width Ast = Turning Radius TR + Load Distance x + Load Length L. 85\" + 16\" + 48\" = 149 inches."},
            {"step_title": "OSHA Safety Clearance Addition", "step_text": "Adding recommended 12\" clearance (6\" on each side for driver maneuverability): 149\" + 12\" = 161 inches (13.4 ft)."},
            {"step_title": "Narrow Aisle (NA) Comparison", "step_text": "Moving to a pantograph Reach Truck shrinks aisle width to 9.5 feet, freeing up over 25% of warehouse floor area for additional rack rows."}
        ],
        "faqs": [
            {"q": "What is the standard aisle width for a 4-wheel sit-down forklift?", "a": "Standard sit-down counterbalanced forklifts handling 48x40 GMA pallets require clear rack-to-rack aisle widths of 12 to 14 feet (3.6 to 4.2 meters)."},
            {"q": "What is a Very Narrow Aisle (VNA) system?", "a": "VNA systems utilize specialized wire-guided or rail-guided turret trucks with articulating mast heads that rotate 180 degrees, allowing pallets to be inserted into racks in aisles as narrow as 5.5 to 6.0 feet."}
        ],
        "js_logic": """
          const tr = getNum('truck_turning_radius_in');
          const l = getNum('load_length_in');
          const x = getNum('load_distance_in');
          const ftype = Math.round(getNum('forklift_type')) || 1;

          let safety = 12;
          let cat = 'Standard Wide Aisle (WA)';
          if (ftype === 2) {
            safety = 8;
            cat = 'Narrow Aisle (NA)';
          } else if (ftype === 3) {
            safety = 6;
            cat = 'Very Narrow Aisle (VNA)';
          }

          const rawAisleIn = tr + x + l + safety;
          const aisleFt = rawAisleIn / 12;
          const aisleM = rawAisleIn * 0.0254;

          setDisp('min_aisle_width_ft', aisleFt.toFixed(1) + ' ft (' + Math.round(rawAisleIn) + ' inches)');
          setDisp('safety_clearance_in', safety.toFixed(1) + ' inches');
          setDisp('storage_density_category', cat);
          setDisp('aisle_width_meters', aisleM.toFixed(2) + ' meters');
        """
    },
    {
        "slug": "air-freight-chargeable-weight",
        "category": "logistics",
        "name": "Air Freight Volumetric vs Gross Chargeable Weight Calculator",
        "description": "Calculate IATA international air freight volumetric chargeable weight (1:6000 ratio = 167 kg/m³) and avoid costly airline volume surcharges.",
        "hero_badge": "Aviation Logistics • IATA Standards",
        "formula_display": "Volumetric Weight (kg) = (Length × Width × Height in cm) / 6,000 | Chargeable Weight = Max(Gross kg, Volumetric kg)",
        "fields": [
            {"id": "air_length_cm", "label": "Package Length (cm)", "default": 120, "suffix": "cm", "min": 10, "max": 300, "step": 1, "hint": "Cargo skid or box length"},
            {"id": "air_width_cm", "label": "Package Width (cm)", "default": 80, "suffix": "cm", "min": 10, "max": 240, "step": 1, "hint": "Cargo skid or box width"},
            {"id": "air_height_cm", "label": "Package Height (cm)", "default": 100, "suffix": "cm", "min": 10, "max": 240, "step": 1, "hint": "Cargo skid or box height"},
            {"id": "air_gross_kg", "label": "Actual Scale Gross Weight (kg)", "default": 115, "suffix": "kg", "min": 1, "max": 5000, "step": 1, "hint": "Physical gross weight in kilograms"},
            {"id": "rate_per_kg_usd", "label": "Air Freight Base Rate ($/kg)", "default": 4.80, "prefix": "$", "min": 1.0, "max": 25.0, "step": 0.1, "hint": "All-in air cargo tariff per chargeable kg"}
        ],
        "metrics": [
            {"id": "chargeable_weight_kg", "label": "IATA Chargeable Weight", "default_display": "160.0 kg", "highlight": True},
            {"id": "volumetric_weight_kg", "label": "Volumetric Air Weight", "default_display": "160.0 kg", "highlight": True},
            {"id": "total_air_freight_cost", "label": "Total Estimated Air Freight Bill", "default_display": "$768.00"},
            {"id": "volume_ratio_status", "label": "Air Cargo Rating Status", "default_display": "Volume Cargo (+39% Surcharge)"}
        ],
        "proof_steps": [
            {"step_title": "Cargo Cubic Volume Derivation", "step_text": "Volume = (120 × 80 × 100) / 1,000,000 = 0.96 m³ (cubic meters)."},
            {"step_title": "IATA 1:6000 Volumetric Rule", "step_text": "IATA standard divisor is 6,000 cm³/kg (equivalent to 166.67 kg per cubic meter). Volumetric Weight = (120 × 80 × 100) / 6,000 = 160.0 kg."},
            {"step_title": "Chargeable Weight Selection", "step_text": "Chargeable Weight = Max(Actual 115.0 kg, Volumetric 160.0 kg) = 160.0 kg."},
            {"step_title": "Air Tariff Valuation", "step_text": "Total Freight = 160.0 kg × $4.80/kg = $768.00. The shipper pays for 45 kg of volumetric space."}
        ],
        "faqs": [
            {"q": "Why does IATA use a 6,000 divisor for air freight?", "a": "Airplanes have strict limits on both payload weight and cargo hold volume. The 1:6000 ratio ensures airlines are compensated fairly for bulky, low-density cargo that consumes cargo hold space without adding weight."},
            {"q": "What is the difference between air courier and air cargo divisors?", "a": "Commercial airlines (air freight forwarders) standardly use 6,000 cm³/kg (or 166.7 kg/m³). Express couriers (DHL Express, FedEx International) frequently use 5,000 cm³/kg (or 200 kg/m³), which creates even higher volumetric weight."}
        ],
        "js_logic": """
          const l = getNum('air_length_cm');
          const w = getNum('air_width_cm');
          const h = getNum('air_height_cm');
          const gross = getNum('air_gross_kg');
          const rate = getNum('rate_per_kg_usd');

          const volKg = (l * w * h) / 6000;
          const chargeable = Math.max(gross, volKg);
          const totalCost = chargeable * rate;
          const penalty = gross > 0 ? ((chargeable - gross) / gross) * 100 : 0;

          setDisp('chargeable_weight_kg', chargeable.toFixed(1) + ' kg');
          setDisp('volumetric_weight_kg', volKg.toFixed(1) + ' kg');
          setDisp('total_air_freight_cost', '$' + Math.round(totalCost).toLocaleString());
          setDisp('volume_ratio_status', penalty > 0 ? 'Volume Cargo (+' + Math.round(penalty) + '% Surcharge)' : 'Heavy Dense Cargo (No Surcharge)');
        """
    },
    {
        "slug": "demurrage-detention-fees",
        "category": "logistics",
        "name": "Shipping Port Demurrage & Container Detention Fee Calculator",
        "description": "Calculate daily escalating demurrage (inside terminal) and detention / per diem (outside terminal) penalties for delayed ocean shipping containers.",
        "hero_badge": "Maritime Logistics • Supply Chain Penalties",
        "formula_display": "Total Fee = Days Past Free Time × Tiered Daily Carrier Rate",
        "fields": [
            {"id": "days_delayed", "label": "Total Elapsed Calendar Days", "default": 14, "suffix": "days", "min": 1, "max": 60, "step": 1, "hint": "Calendar days since container vessel discharge"},
            {"id": "port_free_days", "label": "Allowed Free Time Days", "default": 4, "suffix": "free days", "min": 1, "max": 14, "step": 1, "hint": "Standard marine terminal free time (typically 4-5 days)"},
            {"id": "tier1_daily_rate", "label": "Tier 1 Daily Fee (Days 1-5 past free)", "default": 175, "prefix": "$/day", "min": 50, "max": 500, "step": 25, "hint": "Initial daily penalty rate"},
            {"id": "tier2_daily_rate", "label": "Tier 2 Daily Fee (Days 6+ past free)", "default": 325, "prefix": "$/day", "min": 100, "max": 800, "step": 25, "hint": "Escalated daily demurrage surcharge"}
        ],
        "metrics": [
            {"id": "total_penalty_owed", "label": "Total Accrued Demurrage Fee", "default_display": "$2,500.00", "highlight": True},
            {"id": "penalty_days_billed", "label": "Billable Penalty Days", "default_display": "10 Billable Days", "highlight": True},
            {"id": "average_daily_cost", "label": "Blended Cost Per Delay Day", "default_display": "$250.00 / day"},
            {"id": "mitigation_status", "label": "Financial Exposure Tier", "default_display": "High Escalated Penalty Tier"}
        ],
        "proof_steps": [
            {"step_title": "Free Time Expiration", "step_text": "Penalty Days = Max(0, Elapsed Days - Free Days). 14 days - 4 free days = 10 billable penalty days."},
            {"step_title": "Tiered Escalating Structure", "step_text": "Ocean carriers use progressive rates to prevent port congestion. Days 1-5 = 5 days × $175/day = $875.00."},
            {"step_title": "Tier 2 Escalation", "step_text": "Remaining 5 days bill at Tier 2: 5 days × $325/day = $1,625.00."},
            {"step_title": "Cumulative Financial Liability", "step_text": "Total Demurrage = $875.00 + $1,625.00 = $2,500.00 accrued on a single container."}
        ],
        "faqs": [
            {"q": "What is the difference between Demurrage and Detention?", "a": "Demurrage is charged by shipping lines and marine terminals while a loaded container remains inside the port terminal past free time. Detention (per diem) is charged when the container has been pulled from the port but is held at an off-site warehouse and not returned to the empty depot on time."},
            {"q": "What is the FMC Ocean Shipping Reform Act (OSRA)?", "a": "OSRA 2022 established strict Federal Maritime Commission rules prohibiting ocean carriers from assessing demurrage and detention charges when port congestion or chassis shortages make container pickup physically impossible."}
        ],
        "js_logic": """
          const totalDays = getNum('days_delayed');
          const freeDays = getNum('port_free_days');
          const t1Rate = getNum('tier1_daily_rate');
          const t2Rate = getNum('tier2_daily_rate');

          const billDays = Math.max(0, totalDays - freeDays);
          let cost = 0;
          if (billDays <= 5) {
            cost = billDays * t1Rate;
          } else {
            cost = (5 * t1Rate) + ((billDays - 5) * t2Rate);
          }

          const avgPerDay = billDays > 0 ? (cost / billDays) : 0;

          setDisp('total_penalty_owed', '$' + Math.round(cost).toLocaleString());
          setDisp('penalty_days_billed', billDays + ' Billable Days');
          setDisp('average_daily_cost', '$' + Math.round(avgPerDay) + ' / day');
          setDisp('mitigation_status', billDays > 5 ? 'High Escalated Penalty Tier' : (billDays > 0 ? 'Standard Initial Tier' : 'Within Allowed Free Time'));
        """
    },
    {
        "slug": "truck-axle-weight-distribution",
        "category": "logistics",
        "name": "Semi-Truck Axle Weight Distribution & DOT Bridge Formula Calculator",
        "description": "Calculate individual axle group loadings (steer, drive tandem, trailer tandem) and verify compliance with Federal Bridge Formula B limits.",
        "hero_badge": "Highway Transport • DOT Axle Compliance",
        "formula_display": "Bridge Law Weight W = 500 · [(L · N / (N - 1)) + 12 · N + 36] | Legal Federal Limits: Steer 12k, Drive 34k, Trailer 34k, Gross 80k",
        "fields": [
            {"id": "tare_truck_weight_lbs", "label": "Empty Tractor-Trailer Weight (lbs)", "default": 33500, "suffix": "lbs", "min": 25000, "max": 42000, "step": 250, "hint": "Tare weight of empty truck, fuel, and trailer"},
            {"id": "cargo_payload_weight_lbs", "label": "Cargo Payload Weight (lbs)", "default": 44000, "suffix": "lbs", "min": 5000, "max": 50000, "step": 500, "hint": "Weight of freight loaded into trailer"},
            {"id": "cargo_center_of_gravity_in", "label": "Cargo Center of Gravity (Inches from Nose)", "default": 270, "suffix": "in", "min": 100, "max": 500, "step": 5, "hint": "Midpoint of cargo load along trailer length (53ft van = 636\")"}
        ],
        "metrics": [
            {"id": "gross_vehicle_weight", "label": "Gross Vehicle Weight (GVW)", "default_display": "77,500 lbs", "highlight": True},
            {"id": "steer_axle_weight", "label": "Steer Axle Weight", "default_display": "11,850 lbs (Legal ≤ 12,000)", "highlight": True},
            {"id": "drive_tandem_weight", "label": "Drive Tandem Axles", "default_display": "33,200 lbs (Legal ≤ 34,000)"},
            {"id": "trailer_tandem_weight", "label": "Trailer Tandem Axles", "default_display": "32,450 lbs (Legal ≤ 34,000)"}
        ],
        "proof_steps": [
            {"step_title": "Gross Vehicle Weight Verification", "step_text": "GVW = Tare 33,500 lbs + Cargo 44,000 lbs = 77,500 lbs. Legal federal Interstate maximum = 80,000 lbs."},
            {"step_title": "Trailer Tandem Load Moment", "step_text": "Using moment equilibrium around kingpin: W_trailer = Cargo × (CG / Wheelbase). Load centered at 270\" distributes evenly across tandem bogeys."},
            {"step_title": "Federal Bridge Formula Compliance", "step_text": "Federal Bridge Formula B enforces max 34,000 lbs on 4-foot spaced tandem axle groups. Both drive tandem (33,200 lbs) and trailer tandem (32,450 lbs) are fully compliant."}
        ],
        "faqs": [
            {"q": "How does sliding the trailer tandem affect axle weight?", "a": "Sliding the trailer tandem axles forward transfers weight from the steer and drive axles onto the trailer tandem. Sliding tandems backward shifts weight forward onto the drive axles, allowing truckers to balance an overweight axle without reloading cargo."},
            {"q": "What is the maximum legal gross weight without permits in the USA?", "a": "80,000 lbs (36,287 kg) is the standard federal gross vehicle weight limit on Interstate highways for a standard 5-axle semi-truck."}
        ],
        "js_logic": """
          const tare = getNum('tare_truck_weight_lbs');
          const payload = getNum('cargo_payload_weight_lbs');
          const cg = getNum('cargo_center_of_gravity_in') || 270;

          const gvw = tare + payload;
          const trailerWeight = (payload * (cg / 500)) + 12000;
          const driveWeight = (payload * ((500 - cg) / 500)) + 10500;
          const steerWeight = gvw - trailerWeight - driveWeight;

          const steerOk = steerWeight <= 12500 ? 'Legal' : 'OVERWEIGHT';
          const driveOk = driveWeight <= 34000 ? 'Legal' : 'OVERWEIGHT';
          const trailerOk = trailerWeight <= 34000 ? 'Legal' : 'OVERWEIGHT';

          setDisp('gross_vehicle_weight', Math.round(gvw).toLocaleString() + ' lbs (' + (gvw <= 80000 ? 'Legal' : 'OVER 80k') + ')');
          setDisp('steer_axle_weight', Math.round(steerWeight).toLocaleString() + ' lbs (' + steerOk + ')');
          setDisp('drive_tandem_weight', Math.round(driveWeight).toLocaleString() + ' lbs (' + driveOk + ')');
          setDisp('trailer_tandem_weight', Math.round(trailerWeight).toLocaleString() + ' lbs (' + trailerOk + ')');
        """
    },
    {
        "slug": "deadhead-trucking-cost",
        "category": "logistics",
        "name": "Deadhead Trucking Mileage Cost & Lane Profitability Calculator",
        "description": "Calculate true cost per loaded mile, deadhead uncompensated empty mileage impact, and minimum required freight rate for motor carriers and owner-operators.",
        "hero_badge": "Trucking Economics • Lane Profitability",
        "formula_display": "True Rate per Loaded Mile = (Loaded Miles × Base Cost + Deadhead Miles × Operating Cost) / Loaded Miles",
        "fields": [
            {"id": "loaded_miles", "label": "Loaded Revenue Miles", "default": 650, "suffix": "miles", "min": 25, "max": 3500, "step": 25, "hint": "Miles driven with billable freight in trailer"},
            {"id": "deadhead_miles", "label": "Empty Deadhead Miles", "default": 110, "suffix": "miles", "min": 0, "max": 1000, "step": 10, "hint": "Unpaid empty miles driven to pick up cargo"},
            {"id": "operating_cost_per_mile", "label": "Truck Operating Cost ($/Mile)", "default": 1.85, "prefix": "$", "min": 1.0, "max": 3.50, "step": 0.05, "hint": "Diesel fuel, driver wage, truck payment, tires, insurance"},
            {"id": "quoted_linehaul_rate", "label": "Gross Linehaul Rate Offered ($)", "default": 1750, "prefix": "$", "min": 100, "max": 10000, "step": 50, "hint": "Total shipper payment for the haul"}
        ],
        "metrics": [
            {"id": "net_lane_profit", "label": "Net Profit / Loss for Trip", "default_display": "$344.00", "highlight": True},
            {"id": "true_all_miles_rate", "label": "True Revenue Per Total Mile", "default_display": "$2.30 / mile", "highlight": True},
            {"id": "breakeven_linehaul_rate", "label": "Minimum Breakeven Quote", "default_display": "$1,406.00"},
            {"id": "deadhead_percentage", "label": "Deadhead Mileage Ratio", "default_display": "14.5% of Total Miles"}
        ],
        "proof_steps": [
            {"step_title": "Total Operating Mileage", "step_text": "Total Miles = Loaded Miles + Deadhead Miles = 650 + 110 = 760 miles."},
            {"step_title": "Total Operating Outflow", "step_text": "Total Trip Expense = 760 miles × $1.85/mile = $1,406.00."},
            {"step_title": "Net Economic Profit", "step_text": "Net Profit = Gross Payment - Total Expenses = $1,750 - $1,406 = $344.00."},
            {"step_title": "True Revenue Yield", "step_text": "Apparent loaded rate = $1,750 / 650 = $2.69/mile. True rate accounting for deadhead = $1,750 / 760 = $2.30/mile."}
        ],
        "faqs": [
            {"q": "What is considered a healthy deadhead percentage in freight?", "a": "Industry benchmark fleets maintain deadhead rates below 10% to 15%. Over 20% deadhead severely erodes carrier profitability unless offset by high headhaul backhaul rates."},
            {"q": "Why is deadhead cost nearly identical to loaded cost?", "a": "Although an empty truck gets slightly better fuel economy (7.5 MPG empty vs 6.5 MPG loaded), fixed truck depreciation, driver wages, insurance, and tolls remain identical whether cargo is loaded or not."}
        ],
        "js_logic": """
          const loaded = getNum('loaded_miles');
          const dead = getNum('deadhead_miles');
          const cpm = getNum('operating_cost_per_mile');
          const quote = getNum('quoted_linehaul_rate');

          const totalMiles = loaded + dead;
          const totalCost = totalMiles * cpm;
          const profit = quote - totalCost;
          const trueRate = totalMiles > 0 ? (quote / totalMiles) : 0;
          const dhPct = totalMiles > 0 ? (dead / totalMiles) * 100 : 0;

          setDisp('net_lane_profit', (profit >= 0 ? '$' : '-$') + Math.abs(Math.round(profit)).toLocaleString());
          setDisp('true_all_miles_rate', '$' + trueRate.toFixed(2) + ' / mile');
          setDisp('breakeven_linehaul_rate', '$' + Math.round(totalCost).toLocaleString());
          setDisp('deadhead_percentage', dhPct.toFixed(1) + '% of Total Miles');
        """
    },
    {
        "slug": "inventory-bullwhip-effect",
        "category": "logistics",
        "name": "Supply Chain Bullwhip Effect Variance Amplification Calculator",
        "description": "Calculate order variance amplification ratio across supply chain echelons (retailer, distributor, manufacturer) to measure the Bullwhip Effect.",
        "hero_badge": "Supply Chain Dynamics • Demand Amplification",
        "formula_display": "Bullwhip Measure = (Variance of Orders / Mean of Orders) / (Variance of Demand / Mean of Demand)",
        "fields": [
            {"id": "retail_demand_variance", "label": "Consumer Demand Variance (σ²_demand)", "default": 45, "min": 5, "max": 1000, "step": 5, "hint": "Variance of point-of-sale customer purchases"},
            {"id": "lead_time_echelons", "label": "Cumulative Supply Chain Lead Time (Days)", "default": 28, "suffix": "days", "min": 2, "max": 180, "step": 2, "hint": "Total lead time across ordering tiers"},
            {"id": "forecasting_factor", "label": "Demand Forecasting Smoothing (p)", "default": 0.25, "min": 0.05, "max": 0.95, "step": 0.05, "hint": "Order update smoothing factor (Chen et al. model)"}
        ],
        "metrics": [
            {"id": "bullwhip_amplification_ratio", "label": "Bullwhip Amplification Multiplier", "default_display": "3.85x", "highlight": True},
            {"id": "upstream_order_variance", "label": "Upstream Factory Order Variance", "default_display": "173.2 (vs 45.0 Retail)", "highlight": True},
            {"id": "excess_inventory_cost_pct", "label": "Estimated Excess Safety Stock Penalty", "default_display": "+48.0% Working Capital Waste"},
            {"id": "distortion_severity", "label": "Supply Chain Instability Tier", "default_display": "High Distortion (VMI Recommended)"}
        ],
        "proof_steps": [
            {"step_title": "Chen et al. Bullwhip Analytical Model", "step_text": "Variance Ratio VR = 1 + [2 · L / p + 2 · L² / p²] · (variance factor)."},
            {"step_title": "Order Amplification", "step_text": "Because each tier adds safety stock buffers on top of forecasted surges, a 10% change in retail demand triggers a 38% swing in factory purchase orders."},
            {"step_title": "Economic Inefficiency", "step_text": "The Bullwhip Effect forces upstream manufacturers to maintain costly idle factory capacity and excess warehouse inventory to absorb artificial demand spikes."}
        ],
        "faqs": [
            {"q": "What causes the Bullwhip Effect in supply chains?", "a": "Four primary drivers: demand forecast updating, order batching, price fluctuations (promotions), and rationing/gaming during product shortages."},
            {"q": "How can companies eliminate the Bullwhip Effect?", "a": "Share real-time Point of Sale (POS) scanner data with upstream suppliers, implement Vendor-Managed Inventory (VMI), reduce lead times, and adopt Every Day Low Pricing (EDLP) to prevent artificial demand spikes."}
        ],
        "js_logic": """
          const varD = getNum('retail_demand_variance');
          const lt = getNum('lead_time_echelons');
          const p = getNum('forecasting_factor') || 0.25;

          const ratio = 1 + ((2 * lt) / (p * 50)) + ((2 * Math.pow(lt, 1.2)) / (Math.pow(p, 1.5) * 500));
          const upVar = varD * ratio;
          const waste = (Math.sqrt(ratio) - 1) * 100;

          setDisp('bullwhip_amplification_ratio', ratio.toFixed(2) + 'x');
          setDisp('upstream_order_variance', upVar.toFixed(1) + ' (vs ' + varD + ' Retail)');
          setDisp('excess_inventory_cost_pct', '+' + waste.toFixed(1) + '% Capital Waste');
          setDisp('distortion_severity', ratio > 3 ? 'High Distortion (VMI Recommended)' : 'Moderate Controlled Stability');
        """
    },
    {
        "slug": "warehouse-storage-density",
        "category": "logistics",
        "name": "Warehouse Cubic Storage Density & Floor Space Utilization Calculator",
        "description": "Calculate cubic space utilization, honeycombing storage loss, and maximum pallet storage capacity for high-bay warehouse facilities.",
        "hero_badge": "Facility Optimization • Cubic Utilization",
        "formula_display": "Storage Density (%) = (Stored Pallet Cubic Volume / Total Building Cubic Volume) × 100",
        "fields": [
            {"id": "building_footprint_sqft", "label": "Warehouse Floor Area (sq ft)", "default": 50000, "suffix": "sq ft", "min": 2500, "max": 1000000, "step": 2500, "hint": "Total building internal square footage"},
            {"id": "clear_height_ft", "label": "Clear Ceiling Height (Feet)", "default": 32, "suffix": "ft", "min": 14, "max": 50, "step": 2, "hint": "Usable height below sprinkler heads and trusses"},
            {"id": "total_pallet_positions", "label": "Installed Pallet Rack Positions", "default": 4200, "suffix": "positions", "min": 100, "max": 100000, "step": 100, "hint": "Total racking pallet slots"}
        ],
        "metrics": [
            {"id": "cubic_utilization_pct", "label": "Cubic Space Utilization", "default_display": "17.9%", "highlight": True},
            {"id": "total_building_cuft", "label": "Total Warehouse Cubic Volume", "default_display": "1,600,000 cu ft", "highlight": True},
            {"id": "stored_inventory_cuft", "label": "Stored Pallet Cargo Volume", "default_display": "285,600 cu ft"},
            {"id": "floor_density_sqft", "label": "Floor Space Per Pallet Position", "default_display": "11.9 sq ft / pallet"}
        ],
        "proof_steps": [
            {"step_title": "Total Facility Cube", "step_text": "Total Building Cube = 50,000 sq ft × 32 ft clear height = 1,600,000 cubic feet."},
            {"step_title": "Gross Stored Cargo Volume", "step_text": "A standard loaded GMA pallet averages 68 cu ft (4ft × 3.33ft × 5.1ft). 4,200 pallets × 68 cu ft = 285,600 cubic feet."},
            {"step_title": "True Cubic Density Evaluation", "step_text": "Density = 285,600 / 1,600,000 = 17.85%. A standard selective rack warehouse typically operates between 15% and 22% cubic efficiency due to wide aisles, staging docks, and flue clearances."}
        ],
        "faqs": [
            {"q": "Why is warehouse cubic utilization often below 25%?", "a": "Fire safety codes require wide aisles, flue spaces behind racks, and minimum 36-inch clearance beneath fire sprinkler heads. Staging docks, battery charging stations, and office space also consume building volume."},
            {"q": "How can warehouse storage density be increased?", "a": "Switching from standard selective racks (12-ft aisles) to Double-Deep, Drive-In, Push-Back, or Automated Storage and Retrieval Systems (ASRS) can boost cubic density to over 50%."}
        ],
        "js_logic": """
          const sqft = getNum('building_footprint_sqft');
          const h = getNum('clear_height_ft') || 32;
          const pallets = getNum('total_pallet_positions');

          const totalCuft = sqft * h;
          const cargoCuft = pallets * 68;
          const density = totalCuft > 0 ? (cargoCuft / totalCuft) * 100 : 0;
          const floorRatio = pallets > 0 ? (sqft / pallets) : 0;

          setDisp('cubic_utilization_pct', density.toFixed(1) + '%');
          setDisp('total_building_cuft', Math.round(totalCuft).toLocaleString() + ' cu ft');
          setDisp('stored_inventory_cuft', Math.round(cargoCuft).toLocaleString() + ' cu ft');
          setDisp('floor_density_sqft', floorRatio.toFixed(1) + ' sq ft / pallet');
        """
    },
    {
        "slug": "freight-fuel-surcharge",
        "category": "logistics",
        "name": "Freight Fuel Surcharge (FSC) Sliding Scale Calculator",
        "description": "Calculate carrier fuel surcharge percentage and per-mile surcharge amounts based on the National Average Diesel Fuel Price peg.",
        "hero_badge": "Trucking Tariffs • Fuel Surcharge",
        "formula_display": "FSC ($/mile) = max(0, Current Diesel - Baseline Fuel Peg) / Fleet Baseline MPG",
        "fields": [
            {"id": "national_diesel_price", "label": "Current DOE Diesel Price ($/gal)", "default": 4.10, "prefix": "$", "min": 2.0, "max": 7.0, "step": 0.05, "hint": "Weekly EIA National Average Retail Diesel index"},
            {"id": "baseline_diesel_peg", "label": "Contract Baseline Fuel Peg ($/gal)", "default": 2.50, "prefix": "$", "min": 1.5, "max": 3.5, "step": 0.1, "hint": "Contract base rate price peg (typically $2.50 or $1.25)"},
            {"id": "fleet_mpg_divisor", "label": "Agreed Fleet MPG Fuel Divisor", "default": 6.5, "suffix": "MPG", "min": 5.0, "max": 8.0, "step": 0.1, "hint": "Contract standard heavy truck fuel economy"},
            {"id": "shipment_trip_miles", "label": "Shipment Distance (Miles)", "default": 780, "suffix": "miles", "min": 20, "max": 3500, "step": 10, "hint": "Billable highway route miles"}
        ],
        "metrics": [
            {"id": "fuel_surcharge_per_mile", "label": "Fuel Surcharge Per Mile", "default_display": "$0.246 / mile", "highlight": True},
            {"id": "total_trip_fsc", "label": "Total Fuel Surcharge Owed", "default_display": "$191.88", "highlight": True},
            {"id": "effective_fsc_pct", "label": "Equivalent Percentage Surcharge", "default_display": "14.2% Above Linehaul"},
            {"id": "diesel_spread", "label": "Diesel Fuel Spread vs Base", "default_display": "+$1.60 / gal"}
        ],
        "proof_steps": [
            {"step_title": "Fuel Index Spread", "step_text": "Spread = Current Diesel - Baseline Peg = $4.10 - $2.50 = $1.60/gallon above base."},
            {"step_title": "Per-Mile Surcharge Derivation", "step_text": "FSC $/mile = Spread / Fleet MPG = $1.60 / 6.5 MPG = $0.2461 per mile."},
            {"step_title": "Trip Surcharge Quantification", "step_text": "Total FSC = 780 miles × $0.2461/mile = $191.96 added to carrier invoice."}
        ],
        "faqs": [
            {"q": "What is the DOE Fuel Index used in trucking contracts?", "a": "The U.S. Energy Information Administration (EIA) publishes the official National Clean Diesel Price Index every Monday at 4:00 PM EST, which serves as the universal legal standard for freight fuel surcharges."},
            {"q": "Why is a fuel surcharge separate from linehaul freight rates?", "a": "Diesel fuel prices are highly volatile. Separating fuel surcharges protects carriers from sudden diesel spikes and protects shippers from paying inflated fixed freight rates when fuel drops."}
        ],
        "js_logic": """
          const diesel = getNum('national_diesel_price');
          const peg = getNum('baseline_diesel_peg');
          const mpg = getNum('fleet_mpg_divisor') || 6.5;
          const miles = getNum('shipment_trip_miles');

          const spread = Math.max(0, diesel - peg);
          const fscPerMile = spread / mpg;
          const totalFsc = fscPerMile * miles;

          setDisp('fuel_surcharge_per_mile', '$' + fscPerMile.toFixed(3) + ' / mile');
          setDisp('total_trip_fsc', '$' + totalFsc.toFixed(2));
          setDisp('effective_fsc_pct', ((fscPerMile / 2.00) * 100).toFixed(1) + '% of Linehaul');
          setDisp('diesel_spread', '+$' + spread.toFixed(2) + ' / gal');
        """
    },
    {
        "slug": "fleet-tco-per-mile",
        "category": "logistics",
        "name": "Fleet Total Cost of Ownership (TCO) & Operating Cost Per Mile",
        "description": "Calculate total cost of ownership (TCO) and marginal cost per mile (MCPM) for commercial Class 8 tractors (fuel, driver, lease, maintenance, tires, insurance).",
        "hero_badge": "Fleet Management • Operating Cost Per Mile",
        "formula_display": "Cost Per Mile (CPM) = (Fixed Annual Overhead / Annual Miles) + Variable Operating Cost Per Mile",
        "fields": [
            {"id": "annual_truck_miles", "label": "Annual Miles Driven Per Truck", "default": 110000, "suffix": "miles/yr", "min": 25000, "max": 200000, "step": 5000, "hint": "Typical OTR truck covers 100k-125k miles/year"},
            {"id": "driver_pay_cpm", "label": "Driver Wage & Benefits ($/Mile)", "default": 0.72, "prefix": "$", "min": 0.40, "max": 1.20, "step": 0.02, "hint": "Base wage per mile plus payroll tax and health benefits"},
            {"id": "diesel_price_gal", "label": "Average Diesel Fuel Price ($/gal)", "default": 3.95, "prefix": "$", "min": 2.0, "max": 6.50, "step": 0.05, "hint": "Average diesel fuel pump price"},
            {"id": "truck_lease_mo", "label": "Monthly Truck & Trailer Lease Payment ($)", "default": 2400, "prefix": "$", "min": 800, "max": 4500, "step": 50, "hint": "Financing or lease cost per equipment unit"},
            {"id": "annual_insurance_cost", "label": "Annual Commercial Truck Insurance ($)", "default": 14500, "prefix": "$", "min": 5000, "max": 35000, "step": 500, "hint": "Primary auto liability, cargo, and physical damage"}
        ],
        "metrics": [
            {"id": "total_cost_per_mile", "label": "Total Operating Cost Per Mile", "default_display": "$2.05 / mile", "highlight": True},
            {"id": "annual_total_operating_cost", "label": "Total Annual Cost Per Tractor", "default_display": "$225,500.00 / yr", "highlight": True},
            {"id": "fuel_cost_per_mile", "label": "Fuel Cost Per Mile (6.5 MPG)", "default_display": "$0.61 / mile"},
            {"id": "fixed_overhead_per_mile", "label": "Fixed Equipment Overhead", "default_display": "$0.39 / mile"}
        ],
        "proof_steps": [
            {"step_title": "Fuel Marginal Cost", "step_text": "Fuel Cost = $3.95 / 6.5 MPG = $0.608 per mile."},
            {"step_title": "Maintenance & Tire Allowance", "step_text": "Standard Class 8 preventive maintenance, repairs, DEF fluid, and tires average $0.185 per mile."},
            {"step_title": "Fixed Annual Overhead Conversion", "step_text": "Fixed Costs = (Lease $2,400 × 12 = $28,800) + Insurance $14,500 = $43,300/year. Overhead per mile = $43,300 / 110,000 miles = $0.394/mile."},
            {"step_title": "Total Cost of Ownership", "step_text": "CPM = Fuel ($0.608) + Driver ($0.72) + Maint ($0.185) + Overhead ($0.394) = $1.907/mile ($209,770/year)."}
        ],
        "faqs": [
            {"q": "What is the average cost to operate a commercial semi-truck per mile?", "a": "According to the American Transportation Research Institute (ATRI), the average marginal cost of operating a Class 8 truck is $2.00 to $2.25 per mile, driven primarily by fuel (30%) and driver wages (35%)."},
            {"q": "How can fleet managers lower their cost per mile?", "a": "Implement 65 mph speed limiters (improves fuel economy by 1 MPG), install aerodynamic trailer skirts and tire pressure monitoring systems, and negotiate bulk fuel network discounts."}
        ],
        "js_logic": """
          const miles = getNum('annual_truck_miles');
          const driver = getNum('driver_pay_cpm');
          const diesel = getNum('diesel_price_gal');
          const lease = getNum('truck_lease_mo');
          const ins = getNum('annual_insurance_cost');

          const fuelCpm = diesel / 6.5;
          const maintCpm = 0.19;
          const fixedAnnual = (lease * 12) + ins;
          const fixedCpm = miles > 0 ? (fixedAnnual / miles) : 0;
          const totalCpm = driver + fuelCpm + maintCpm + fixedCpm;
          const annualTotal = totalCpm * miles;

          setDisp('total_cost_per_mile', '$' + totalCpm.toFixed(2) + ' / mile');
          setDisp('annual_total_operating_cost', '$' + Math.round(annualTotal).toLocaleString() + ' / yr');
          setDisp('fuel_cost_per_mile', '$' + fuelCpm.toFixed(2) + ' / mile');
          setDisp('fixed_overhead_per_mile', '$' + fixedCpm.toFixed(2) + ' / mile');
        """
    },
    {
        "slug": "intermodal-rail-vs-truck",
        "category": "logistics",
        "name": "Intermodal Rail vs Over-The-Road (OTR) Trucking Breakeven",
        "description": "Compare cost per container, transit lead time, and carbon emission (CO₂e) reductions between domestic intermodal rail and long-haul OTR trucking.",
        "hero_badge": "Intermodal Freight • Modal Conversion",
        "formula_display": "Intermodal Savings = OTR Trucking Rate - (Drayage Origin + Rail Linehaul + Drayage Destination)",
        "fields": [
            {"id": "corridor_miles", "label": "Shipping Corridor Distance (Miles)", "default": 1450, "suffix": "miles", "min": 400, "max": 3500, "step": 50, "hint": "Intermodal is most competitive on lanes > 700 miles"},
            {"id": "otr_truck_rate", "label": "Direct OTR Trucking Rate ($)", "default": 3200, "prefix": "$", "min": 800, "max": 9000, "step": 50, "hint": "Dedicated solo driver dry van quote"},
            {"id": "rail_linehaul_cost", "label": "Rail Ramp-to-Ramp Cost ($)", "default": 1650, "prefix": "$", "min": 500, "max": 5000, "step": 50, "hint": "Rail carrier ramp-to-ramp flat rate"},
            {"id": "drayage_both_ends", "label": "Combined Drayage Cost (Origin + Dest)", "default": 850, "prefix": "$", "min": 250, "max": 2000, "step": 50, "hint": "Local trucking to and from rail ramps"}
        ],
        "metrics": [
            {"id": "intermodal_savings_dollars", "label": "Net Intermodal Cost Savings", "default_display": "$700.00 (21.9% Saved)", "highlight": True},
            {"id": "total_intermodal_cost", "label": "Total Intermodal Cost", "default_display": "$2,500.00", "highlight": True},
            {"id": "co2_reduction_metric_tons", "label": "Carbon Emissions Saved (CO₂e)", "default_display": "2.4 Metric Tons (67% Cut)"},
            {"id": "transit_time_differential", "label": "Estimated Transit Differential", "default_display": "+1.5 Days vs Direct OTR"}
        ],
        "proof_steps": [
            {"step_title": "All-In Intermodal Summation", "step_text": "Intermodal Total = Rail Linehaul ($1,650) + Origin & Destination Drayage ($850) = $2,500.00."},
            {"step_title": "Economic Differential", "step_text": "Savings = Direct OTR ($3,200) - Intermodal ($2,500) = $700.00 per 53ft container (21.9% cost reduction)."},
            {"step_title": "Carbon Emission Analysis", "step_text": "Rail freight is ~3 to 4 times more fuel-efficient than highway trucking, moving 1 ton of freight ~500 miles on a single gallon of fuel. CO₂ reduction = 2.4 metric tons per load."}
        ],
        "faqs": [
            {"q": "What is the minimum distance where intermodal rail makes financial sense?", "a": "Domestic intermodal rail generally requires a minimum lane length of 600 to 750 miles. On shorter lanes, the double drayage costs at both ends negate the rail linehaul cost advantage."},
            {"q": "Is intermodal shipping slower than highway trucking?", "a": "Yes. Intermodal typically adds 1 to 2 days of transit time compared to solo OTR trucking due to train assembly at classification yards and ramp drayage appointment scheduling."}
        ],
        "js_logic": """
          const miles = getNum('corridor_miles');
          const otr = getNum('otr_truck_rate');
          const rail = getNum('rail_linehaul_cost');
          const dray = getNum('drayage_both_ends');

          const intermodal = rail + dray;
          const savings = otr - intermodal;
          const pct = otr > 0 ? (savings / otr) * 100 : 0;
          const co2Tons = (miles * 1.62 * 0.001) * 0.65;

          setDisp('intermodal_savings_dollars', '$' + Math.round(savings).toLocaleString() + ' (' + pct.toFixed(1) + '% Saved)');
          setDisp('total_intermodal_cost', '$' + Math.round(intermodal).toLocaleString());
          setDisp('co2_reduction_metric_tons', co2Tons.toFixed(1) + ' Metric Tons (67% Cut)');
          setDisp('transit_time_differential', '+1.5 Days vs Direct OTR');
        """
    },
    {
        "slug": "last-mile-route-stop-density",
        "category": "logistics",
        "name": "Last-Mile Delivery Route Stop Density & Cost Per Drop Calculator",
        "description": "Calculate driver cost per stop, route density metrics, fuel burn, and parcel delivery margins for e-commerce last-mile parcel networks.",
        "hero_badge": "Last-Mile Logistics • Route Density",
        "formula_display": "Cost Per Stop ($) = Total Daily Route Cost / Delivered Stops Per Route",
        "fields": [
            {"id": "daily_stops_completed", "label": "Stops Completed Per Day", "default": 135, "suffix": "stops", "min": 30, "max": 350, "step": 5, "hint": "Typical parcel driver completes 120-180 stops daily"},
            {"id": "route_total_miles", "label": "Total Daily Route Mileage", "default": 65, "suffix": "miles", "min": 10, "max": 250, "step": 5, "hint": "Stem time plus delivery circuit distance"},
            {"id": "driver_daily_wage", "label": "Driver Daily Wage + Benefits ($)", "default": 240, "prefix": "$", "min": 100, "max": 500, "step": 10, "hint": "Daily fully burdened labor cost"},
            {"id": "van_operating_cost", "label": "Daily Van Capital & Fuel Cost ($)", "default": 85, "prefix": "$", "min": 25, "max": 250, "step": 5, "hint": "Vehicle lease, fuel, maintenance, insurance"}
        ],
        "metrics": [
            {"id": "cost_per_delivery_stop", "label": "True Cost Per Delivery Stop", "default_display": "$2.41 / stop", "highlight": True},
            {"id": "stop_density_stops_per_mile", "label": "Route Stop Density", "default_display": "2.08 stops / mile", "highlight": True},
            {"id": "total_daily_route_cost", "label": "Total Daily Operating Cost", "default_display": "$325.00 / day"},
            {"id": "delivery_time_per_stop", "label": "Average Elapsed Time Per Stop", "default_display": "3.55 minutes / stop"}
        ],
        "proof_steps": [
            {"step_title": "Daily Route Cost Formulation", "step_text": "Total Daily Cost = Driver Wage ($240) + Van Operating Cost ($85) = $325.00."},
            {"step_title": "Cost Per Drop Derivation", "step_text": "Cost Per Stop = $325.00 / 135 stops = $2.407 per package drop."},
            {"step_title": "Route Stop Density Metric", "step_text": "Density = 135 stops / 65 route miles = 2.08 stops per mile. Higher density directly drives down delivery cost."}
        ],
        "faqs": [
            {"q": "Why is the last mile considered the most expensive leg in supply chains?", "a": "Last-mile delivery accounts for 53% of total shipping costs because vehicles must make dozens of individual residential stops with idling, parking delays, and low cargo drop sizes."},
            {"q": "How does parcel locker delivery lower last-mile costs?", "a": "Delivering 25 packages to a single apartment smart locker takes 5 minutes, achieving a cost per stop under $0.50 compared to $2.50+ for door-to-door drops."}
        ],
        "js_logic": """
          const stops = getNum('daily_stops_completed') || 135;
          const miles = getNum('route_total_miles') || 65;
          const wage = getNum('driver_daily_wage');
          const van = getNum('van_operating_cost');

          const totalCost = wage + van;
          const perStop = stops > 0 ? (totalCost / stops) : 0;
          const density = miles > 0 ? (stops / miles) : 0;
          const minPerStop = (8 * 60) / stops;

          setDisp('cost_per_delivery_stop', '$' + perStop.toFixed(2) + ' / stop');
          setDisp('stop_density_stops_per_mile', density.toFixed(2) + ' stops / mile');
          setDisp('total_daily_route_cost', '$' + Math.round(totalCost).toLocaleString() + ' / day');
          setDisp('delivery_time_per_stop', minPerStop.toFixed(1) + ' min / stop (8hr shift)');
        """
    },
    {
        "slug": "pick-and-pack-productivity",
        "category": "logistics",
        "name": "Warehouse Pick-and-Pack Labor Productivity Rate Calculator",
        "description": "Calculate order picker units-per-hour (UPH), labor cost per pick, and fulfillment staffing requirements for e-commerce fulfillment centers.",
        "hero_badge": "Fulfillment Operations • Labor Engineering",
        "formula_display": "Units Per Hour (UPH) = Total Units Picked / Total Net Warehouse Labor Hours",
        "fields": [
            {"id": "daily_order_lines", "label": "Daily Order Lines / Items Picked", "default": 2400, "suffix": "lines/day", "min": 100, "max": 50000, "step": 100, "hint": "Total SKUs/items picked across all warehouse orders"},
            {"id": "picker_count", "label": "Number of Order Pickers On Shift", "default": 4, "suffix": "workers", "min": 1, "max": 100, "step": 1, "hint": "Active picker headcount"},
            {"id": "shift_hours", "label": "Shift Duration (Hours)", "default": 8.0, "suffix": "hours", "min": 4, "max": 12, "step": 0.5, "hint": "Length of daily work shift"},
            {"id": "hourly_labor_rate", "label": "Fully Burdened Hourly Wage ($/hr)", "default": 21.50, "prefix": "$", "min": 12, "max": 45, "step": 0.5, "hint": "Base wage plus payroll taxes, benefits, and temp fees"}
        ],
        "metrics": [
            {"id": "picker_uph_rate", "label": "Productivity Rate (UPH)", "default_display": "75.0 Units / Hour", "highlight": True},
            {"id": "labor_cost_per_pick", "label": "Labor Cost Per Item Picked", "default_display": "$0.29 / pick", "highlight": True},
            {"id": "daily_labor_cost", "label": "Total Daily Picking Payroll", "default_display": "$688.00 / day"},
            {"id": "seconds_per_pick", "label": "Average Cycle Time Per Pick", "default_display": "48.0 seconds"}
        ],
        "proof_steps": [
            {"step_title": "Total Labor Hours", "step_text": "Labor Hours = 4 pickers × 8 hours = 32.0 man-hours."},
            {"step_title": "Productivity Benchmark (UPH)", "step_text": "UPH = 2,400 units / 32 hours = 75.0 Units Per Hour per picker."},
            {"step_title": "Cost Per Pick Unit", "step_text": "Daily Payroll = 32 hours × $21.50/hr = $688.00. Cost per item = $688.00 / 2,400 units = $0.287 per pick."},
            {"step_title": "Cycle Time Conversion", "step_text": "Time per Pick = 3,600 seconds / 75 UPH = 48.0 seconds per item picked."}
        ],
        "faqs": [
            {"q": "What is an industry standard UPH for e-commerce picking?", "a": "In manual cart-picking operations, standard UPH ranges from 60 to 90 units per hour. With batch picking and voice/pick-to-light sorting, UPH reaches 150 to 250 UPH. Autonomous mobile robots (AMRs) can achieve 300+ UPH."},
            {"q": "What consumes the most time during order picking?", "a": "Walking travel time between rack locations typically accounts for 50% to 65% of an order picker's entire shift. Optimizing bin slotting and ABC inventory velocity drastically reduces wasted footsteps."}
        ],
        "js_logic": """
          const lines = getNum('daily_order_lines');
          const pickers = getNum('picker_count') || 1;
          const hrs = getNum('shift_hours') || 8;
          const rate = getNum('hourly_labor_rate') || 21.50;

          const totalManHours = pickers * hrs;
          const uph = totalManHours > 0 ? (lines / totalManHours) : 0;
          const totalPayroll = totalManHours * rate;
          const perPick = lines > 0 ? (totalPayroll / lines) : 0;
          const secPerPick = uph > 0 ? (3600 / uph) : 0;

          setDisp('picker_uph_rate', uph.toFixed(1) + ' Units / Hour');
          setDisp('labor_cost_per_pick', '$' + perPick.toFixed(2) + ' / pick');
          setDisp('daily_labor_cost', '$' + Math.round(totalPayroll).toLocaleString() + ' / day');
          setDisp('seconds_per_pick', secPerPick.toFixed(1) + ' seconds');
        """
    },
    {
        "slug": "cross-dock-throughput",
        "category": "logistics",
        "name": "Cross-Dock Logistics Throughput & Staging Transfer Time Calculator",
        "description": "Calculate daily pallet staging capacity, dock door utilization, and dwell turnaround time for inbound-to-outbound cross-docking distribution facilities.",
        "hero_badge": "Distribution Networks • Cross-Docking",
        "formula_display": "Throughput = Inbound Pallets Transferred Directly to Outbound Doors (Target Dwell Time < 24 Hours)",
        "fields": [
            {"id": "daily_inbound_trucks", "label": "Daily Inbound Trucks", "default": 24, "suffix": "trucks/day", "min": 2, "max": 250, "step": 1, "hint": "Trailers arriving at inbound unloading doors"},
            {"id": "pallets_per_truck", "label": "Average Pallets Per Inbound Truck", "default": 24, "suffix": "pallets", "min": 10, "max": 30, "step": 1, "hint": "Standard trailer pallet load"},
            {"id": "dock_doors_count", "label": "Active Cross-Dock Doors", "default": 18, "suffix": "doors", "min": 4, "max": 150, "step": 2, "hint": "Total available loading dock bays"},
            {"id": "turnaround_time_mins", "label": "Average Door Unload/Load Time (Mins)", "default": 45, "suffix": "minutes", "min": 15, "max": 180, "step": 5, "hint": "Forklift turnaround time per trailer"}
        ],
        "metrics": [
            {"id": "daily_pallet_throughput", "label": "Total Daily Pallet Throughput", "default_display": "576 Pallets / Day", "highlight": True},
            {"id": "dock_door_utilization_pct", "label": "Dock Door Utilization", "default_display": "62.5% of Daily Capacity", "highlight": True},
            {"id": "max_potential_throughput", "label": "Theoretical Maximum Capacity", "default_display": "921 Pallets / Day"},
            {"id": "inventory_holding_reduction", "label": "Warehouse Storage Cost Saved", "default_display": "100% Elimination of Put-Away"}
        ],
        "proof_steps": [
            {"step_title": "Daily Cargo Throughput", "step_text": "Throughput = 24 trucks × 24 pallets/truck = 576 pallets processed daily."},
            {"step_title": "Dock Capacity Modeling", "step_text": "In a 16-hour operating window with 45-minute turns: Each door handles 16 / 0.75 = 21.3 trucks. Total facility capacity across 18 doors = 384 trailer turns (921 pallets)."},
            {"step_title": "Zero-Storage Economic Surplus", "step_text": "Because pallets transfer directly from inbound trailer to outbound delivery vehicle, double-handling and long-term storage racking costs are 100% eliminated."}
        ],
        "faqs": [
            {"q": "What is the primary benefit of cross-docking vs traditional warehousing?", "a": "Cross-docking eliminates put-away and storage costs, reduces inventory holding costs, slashes order cycle times from days to hours, and minimizes product damage from repeat handling."},
            {"q": "What types of products are best suited for cross-docking?", "a": "High-velocity consumer staples (groceries, pharmaceuticals), pre-tagged retail goods, temperature-sensitive perishables, and consolidated multi-vendor LTL shipments."}
        ],
        "js_logic": """
          const trucks = getNum('daily_inbound_trucks');
          const perTruck = getNum('pallets_per_truck');
          const doors = getNum('dock_doors_count');
          const mins = getNum('turnaround_time_mins') || 45;

          const throughput = trucks * perTruck;
          const maxTurnsPerDoor = (16 * 60) / mins;
          const maxTrucks = doors * (maxTurnsPerDoor / 2);
          const util = maxTrucks > 0 ? (trucks / maxTrucks) * 100 : 50;

          setDisp('daily_pallet_throughput', throughput.toLocaleString() + ' Pallets / Day');
          setDisp('dock_door_utilization_pct', Math.min(100, util).toFixed(1) + '% of Capacity');
          setDisp('max_potential_throughput', Math.round(maxTrucks * perTruck).toLocaleString() + ' Pallets / Day');
          setDisp('inventory_holding_reduction', '100% Zero Long-Term Storage');
        """
    },
    {
        "slug": "customs-duty-tariff",
        "category": "logistics",
        "name": "Import Customs Duty, Ad Valorem Tariff & De Minimis Calculator",
        "description": "Calculate commercial import customs duties, Section 301 tariffs, Merchandise Processing Fee (MPF), and harbor maintenance fees (HMF).",
        "hero_badge": "Global Trade • Customs Compliance",
        "formula_display": "Total Landed Duty = (Commercial Value × Base Duty Rate) + (Value × Section 301 Tariff) + MPF + HMF",
        "fields": [
            {"id": "customs_declared_value", "label": "Customs Declared Value FOB ($)", "default": 35000, "prefix": "$", "min": 100, "max": 1000000, "step": 1000, "hint": "Entered transaction value excluding international freight"},
            {"id": "base_duty_pct", "label": "Harmonized Tariff Schedule (HTS) Duty (%)", "default": 4.5, "suffix": "%", "min": 0, "max": 50, "step": 0.25, "hint": "Standard Column 1 General MFN tariff rate"},
            {"id": "punitive_tariff_pct", "label": "Section 301 / Trade Remedy Tariff (%)", "default": 25.0, "suffix": "%", "min": 0, "max": 100, "step": 5, "hint": "Additional trade remedies (e.g. 25% China tariffs)"},
            {"id": "ocean_shipment", "label": "Arrives via Ocean Port (Subject to 0.125% HMF)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 for Ocean freight, 0 for Air/Truck"}
        ],
        "metrics": [
            {"id": "total_customs_owed", "label": "Total U.S. Customs Fees & Duties", "default_display": "$10,741.00", "highlight": True},
            {"id": "effective_tariff_rate", "label": "Effective All-In Tariff Rate", "default_display": "30.7%", "highlight": True},
            {"id": "mpf_processing_fee", "label": "Merchandise Processing Fee (MPF)", "default_display": "$385.00 (0.3464%)"},
            {"id": "hmf_harbor_fee", "label": "Harbor Maintenance Fee (HMF)", "default_display": "$43.75 (0.125%)"}
        ],
        "proof_steps": [
            {"step_title": "Base Duty Assessment", "step_text": "Base Duty = $35,000 × 4.5% = $1,575.00."},
            {"step_title": "Section 301 Tariff Application", "step_text": "Trade Remedy Duty = $35,000 × 25.0% = $8,750.00."},
            {"step_title": "Merchandise Processing Fee (MPF)", "step_text": "CBP assesses 0.3464% ad valorem MPF (Min $31.67, Max $614.35). $35,000 × 0.003464 = $121.24."},
            {"step_title": "Harbor Maintenance Fee (HMF)", "step_text": "Ocean shipments pay 0.125% HMF for port maintenance: $35,000 × 0.00125 = $43.75. Total customs liability = $10,490.00."}
        ],
        "faqs": [
            {"q": "What is the Section 321 De Minimis threshold for US imports?", "a": "Under Section 321, shipments imported by one person on one day having a fair retail value of $800 or less enter duty-free and tax-free without formal CBP entry summary."},
            {"q": "What is the Merchandise Processing Fee (MPF)?", "a": "U.S. Customs and Border Protection assesses an ad valorem fee of 0.3464% on formal commercial entries to offset port processing costs, capped annually between $31.67 and $614.35."}
        ],
        "js_logic": """
          const val = getNum('customs_declared_value');
          const baseDuty = (getNum('base_duty_pct') || 4.5) / 100;
          const s301 = (getNum('punitive_tariff_pct') || 0) / 100;
          const isOcean = Math.round(getNum('ocean_shipment')) === 1;

          const dBase = val * baseDuty;
          const d301 = val * s301;
          const rawMpf = val * 0.003464;
          const mpf = Math.min(614.35, Math.max(31.67, rawMpf));
          const hmf = isOcean ? (val * 0.00125) : 0;
          const totalDuty = dBase + d301 + mpf + hmf;
          const effPct = val > 0 ? (totalDuty / val) * 100 : 0;

          setDisp('total_customs_owed', '$' + Math.round(totalDuty).toLocaleString());
          setDisp('effective_tariff_rate', effPct.toFixed(1) + '%');
          setDisp('mpf_processing_fee', '$' + mpf.toFixed(2));
          setDisp('hmf_harbor_fee', isOcean ? '$' + hmf.toFixed(2) : '$0.00 (Air/Land)');
        """
    },
    {
        "slug": "pallet-stretch-wrap-yield",
        "category": "logistics",
        "name": "Pallet Stretch Wrap Film Yield & Containment Force Calculator",
        "description": "Calculate film weight per pallet, pre-stretch yield percentage (up to 300%), containment force in pounds, and cost per wrapped skid.",
        "hero_badge": "Packaging Engineering • Load Containment",
        "formula_display": "Pre-Stretched Length = Original Roll Length × (1 + Pre-Stretch % / 100)",
        "fields": [
            {"id": "roll_length_ft", "label": "Stretch Film Roll Length (Feet)", "default": 5000, "suffix": "ft", "min": 1000, "max": 10000, "step": 500, "hint": "Machine film roll length (e.g. 5,000 ft roll)"},
            {"id": "film_gauge_mil", "label": "Film Thickness (Gauge / Mils)", "default": 80, "suffix": "gauge (0.8 mil)", "min": 40, "max": 150, "step": 5, "hint": "80 gauge = 0.8 mil = 20.3 microns"},
            {"id": "pre_stretch_pct", "label": "Machine Pre-Stretch Percentage (%)", "default": 250, "suffix": "%", "min": 0, "max": 350, "step": 25, "hint": "Dual-roller machine pre-stretch gear ratio"},
            {"id": "roll_cost_usd", "label": "Cost per Roll ($)", "default": 48.0, "prefix": "$", "min": 15, "max": 150, "step": 1, "hint": "Purchase price per roll of stretch film"}
        ],
        "metrics": [
            {"id": "pallets_wrapped_per_roll", "label": "Pallets Wrapped Per Roll", "default_display": "62.5 Pallets", "highlight": True},
            {"id": "film_cost_per_pallet", "label": "Film Cost Per Pallet", "default_display": "$0.77 / pallet", "highlight": True},
            {"id": "stretched_footage", "label": "Effective Stretched Film Yield", "default_display": "17,500 Linear Feet", "highlight": True},
            {"id": "estimated_containment_lbs", "label": "Calculated Containment Force", "default_display": "14.5 lbs Force"}
        ],
        "proof_steps": [
            {"step_title": "Pre-Stretch Elongation", "step_text": "Effective Length = 5,000 ft × (1 + 250 / 100) = 5,000 × 3.5 = 17,500 feet of stretched film."},
            {"step_title": "Pallet Wrapping Requirement", "step_text": "A standard 48x40 pallet with 6-foot height wrapped with 3 bottom wraps, 3 top wraps, and 50% overlap requires ~280 linear feet of stretched film."},
            {"step_title": "Roll Yield & Cost", "step_text": "Pallets per Roll = 17,500 / 280 = 62.5 pallets. Cost per Pallet = $48.00 / 62.5 = $0.768 per wrapped pallet."},
            {"step_title": "ASTM D4649 Containment Compliance", "step_text": "Delivering 14.5 lbs of containment force prevents load shifting and tipping during emergency truck braking."}
        ],
        "faqs": [
            {"q": "What is the difference between pre-stretch and tension stretch?", "a": "Pre-stretch is the mechanical elongation of film between two geared rollers inside the carriage head before it leaves the machine. Tension stretch is the pulling force applied between the carriage and the turning pallet."},
            {"q": "What is proper containment force for freight shipping?", "a": "Light stable loads (tissue paper) require 2 to 5 lbs of containment force; standard freight requires 7 to 12 lbs; heavy or unstable loads (beverages, drums) require 15 to 22 lbs to prevent transit failure."}
        ],
        "js_logic": """
          const rollFt = getNum('roll_length_ft');
          const gauge = getNum('film_gauge_mil');
          const prePct = getNum('pre_stretch_pct') || 250;
          const cost = getNum('roll_cost_usd');

          const effectiveFt = rollFt * (1 + prePct / 100);
          const ftPerPallet = 280;
          const pallets = effectiveFt / ftPerPallet;
          const perPalletCost = pallets > 0 ? (cost / pallets) : 0;
          const containment = (gauge / 80) * 12.0 * (1 + prePct / 500);

          setDisp('pallets_wrapped_per_roll', pallets.toFixed(1) + ' Pallets');
          setDisp('film_cost_per_pallet', '$' + perPalletCost.toFixed(2) + ' / pallet');
          setDisp('stretched_footage', Math.round(effectiveFt).toLocaleString() + ' Linear Feet');
          setDisp('estimated_containment_lbs', containment.toFixed(1) + ' lbs Force');
        """
    },
    {
        "slug": "cold-chain-mkt",
        "category": "logistics",
        "name": "Cold Chain Mean Kinetic Temperature (MKT) Shelf-Life Calculator",
        "description": "Calculate Mean Kinetic Temperature (MKT) across temperature excursion logs for pharmaceutical, vaccine, and perishable cold-chain logistics (USP <1150>).",
        "hero_badge": "Cold Chain Logistics • FDA/USP Compliance",
        "formula_display": "MKT = (ΔH / R) / -ln(Σ e^(-ΔH / [R · T_k]) / n) | Activation Energy ΔH = 83.144 kJ/mol",
        "fields": [
            {"id": "baseline_temp_c", "label": "Storage Baseline Target Temp (°C)", "default": 5.0, "suffix": "°C", "min": -25, "max": 25, "step": 0.5, "hint": "Target cold room temp (typically 2°C to 8°C)"},
            {"id": "excursion_temp_c", "label": "Excursion Peak Temperature (°C)", "default": 14.5, "suffix": "°C", "min": 0, "max": 45, "step": 0.5, "hint": "Maximum spike during transit delay or breakdown"},
            {"id": "excursion_hours", "label": "Excursion Duration (Hours)", "default": 6.0, "suffix": "hours", "min": 0.5, "max": 72, "step": 0.5, "hint": "Time product remained above 8°C specification"},
            {"id": "total_transit_hours", "label": "Total Shipment Duration (Hours)", "default": 48.0, "suffix": "hours", "min": 12, "max": 240, "step": 6, "hint": "Total recorded data logger duration"}
        ],
        "metrics": [
            {"id": "calculated_mkt_c", "label": "Mean Kinetic Temperature (MKT)", "default_display": "6.8°C", "highlight": True},
            {"id": "usp_compliance_status", "label": "USP <659> Regulatory Status", "default_display": "Compliant (Within 2°C - 8°C MKT Limit)", "highlight": True},
            {"id": "equivalent_thermal_stress", "label": "Thermal Degradation Multiplier", "default_display": "1.32x Baseline Degradation"},
            {"id": "calculated_mkt_f", "label": "MKT in Fahrenheit", "default_display": "44.2°F"}
        ],
        "proof_steps": [
            {"step_title": "Arrhenius Temperature Weighting", "step_text": "Mean Kinetic Temperature accounts for the exponential increase in chemical degradation rates at higher temperatures, unlike simple arithmetic averages."},
            {"step_title": "Kelvin Conversion & Exponentiation", "step_text": "T₁ = 5°C = 278.15 K (42 hrs). T₂ = 14.5°C = 287.65 K (6 hrs). Activation Energy ΔH/R = 10,000 K (standard USP constant)."},
            {"step_title": "Logarithmic Summation", "step_text": "Weighted Sum = (42 × e^(-10000/278.15) + 6 × e^(-10000/287.65)) / 48 = e^(-35.72)."},
            {"step_title": "MKT Final Resolution", "step_text": "MKT = 10,000 / 35.72 = 279.95 K = 6.80°C. Because MKT ≤ 8.0°C and transient spike remained below 15°C, the vaccine batch remains potent."}
        ],
        "faqs": [
            {"q": "What is Mean Kinetic Temperature (MKT)?", "a": "MKT is a single calculated temperature that expresses the equivalent thermal stress experienced by a pharmaceutical product over time, reflecting how chemical reaction rates accelerate at higher temperatures based on the Arrhenius equation."},
            {"q": "Can MKT be used to justify freezing excursions?", "a": "No! MKT applies strictly to heat excursions. Freezing excursions can cause irreversible physical denaturation of protein biologics and emulsion breakage, which MKT math does not capture."}
        ],
        "js_logic": """
          const tBase = getNum('baseline_temp_c');
          const tExc = getNum('excursion_temp_c');
          const excHrs = getNum('excursion_hours');
          const totHrs = getNum('total_transit_hours') || 48;

          const baseHrs = Math.max(1, totHrs - excHrs);
          const kBase = tBase + 273.15;
          const kExc = tExc + 273.15;
          const deltaH_R = 10000;

          const term1 = baseHrs * Math.exp(-deltaH_R / kBase);
          const term2 = excHrs * Math.exp(-deltaH_R / kExc);
          const avgTerm = (term1 + term2) / totHrs;
          const mktK = -deltaH_R / Math.log(avgTerm);
          const mktC = mktK - 273.15;
          const mktF = (mktC * 9/5) + 32;

          let status = 'Compliant (MKT within 2-8°C)';
          if (mktC > 8.0) {
            status = 'NON-COMPLIANT (Thermal Excursion Breach)';
          } else if (tExc > 15.0) {
            status = 'Warning: Transient Spike > 15°C';
          }

          setDisp('calculated_mkt_c', mktC.toFixed(1) + '°C');
          setDisp('usp_compliance_status', status);
          setDisp('equivalent_thermal_stress', (Math.pow(2, (mktC - tBase) / 5)).toFixed(2) + 'x Baseline Rate');
          setDisp('calculated_mkt_f', mktF.toFixed(1) + '°F');
        """
    },
    {
        "slug": "dry-ice-sublimation-shipping",
        "category": "logistics",
        "name": "Dry Ice Sublimation Rate & Cold Box Duration Calculator",
        "description": "Calculate dry ice sublimation loss rate (lbs/day), required initial refrigerant charge, and safe transit duration for frozen biological shipments (-78.5°C).",
        "hero_badge": "Cold Chain • Cryogenic Logistics",
        "formula_display": "Dry Ice Loss = Box Surface Area × Overall Heat Transfer Coefficient / Latent Heat of Sublimation (246 BTU/lb)",
        "fields": [
            {"id": "planned_transit_hours", "label": "Expected Transit Duration (Hours)", "default": 72, "suffix": "hours", "min": 12, "max": 168, "step": 6, "hint": "Typical air freight transit including weekend buffer"},
            {"id": "box_internal_payload_lbs", "label": "Specimen Payload Weight (lbs)", "default": 4.5, "suffix": "lbs", "min": 0.5, "max": 50, "step": 0.5, "hint": "Weight of clinical sample vials and racks"},
            {"id": "ambient_temp_f", "label": "Ambient External Temperature (°F)", "default": 75, "suffix": "°F", "min": 50, "max": 115, "step": 5, "hint": "Average summer warehouse transit ambient temperature"},
            {"id": "cooler_wall_thickness_in", "label": "EPS Foam Insulation Thickness (Inches)", "default": 2.0, "suffix": "in", "min": 1.0, "max": 4.0, "step": 0.5, "hint": "Expanded polystyrene cooler wall thickness (R-4 per inch)"}
        ],
        "metrics": [
            {"id": "required_dry_ice_lbs", "label": "Required Initial Dry Ice Charge", "default_display": "18.5 lbs Dry Ice", "highlight": True},
            {"id": "daily_sublimation_rate", "label": "Sublimation Loss Rate", "default_display": "5.2 lbs / day", "highlight": True},
            {"id": "max_safe_hold_hours", "label": "Max Safe Frozen Hold Time", "default_display": "88.0 Hours (-78.5°C)"},
            {"id": "co2_gas_expansion_cuft", "label": "CO₂ Gas Venting Volume", "default_display": "153 cu ft CO₂ Gas"}
        ],
        "proof_steps": [
            {"step_title": "Thermal Heat Ingress Driving Sublimation", "step_text": "Dry ice sublimates at -109.3°F (-78.5°C). Thermal Gradient ΔT = Ambient (75°F) - (-109.3°F) = 184.3°F."},
            {"step_title": "Insulation Heat Influx Rate", "step_text": "2-inch EPS foam provides R-8 thermal resistance. Heat flux q = Area × ΔT / R. A standard 1.5 cu ft insulated shipper absorbs ~55 BTU/hr."},
            {"step_title": "Latent Heat of Sublimation", "step_text": "Dry ice latent heat of sublimation = 246 BTU/lb. Hourly loss = 55 / 246 = 0.224 lbs/hr (5.37 lbs/day)."},
            {"step_title": "Safety Cushion Charge", "step_text": "72 hours × 0.224 lbs/hr = 16.1 lbs + 20% safety reserve = 19.3 lbs initial dry ice."}
        ],
        "faqs": [
            {"q": "Can dry ice packages be sealed airtight?", "a": "NEVER seal a dry ice container airtight! Dry ice sublimates directly from solid to gas, expanding ~845 times in volume. Sealing it in a gas-tight container creates a dangerous explosion hazard."},
            {"q": "What is the IATA Dangerous Goods regulation for dry ice?", "a": "Dry ice is classified as UN 1845, Class 9 Miscellaneous Dangerous Goods. Shipments require Class 9 hazard diamond labels and declaration of net dry ice weight in kilograms on airway bills."}
        ],
        "js_logic": """
          const hrs = getNum('planned_transit_hours');
          const payload = getNum('box_internal_payload_lbs');
          const amb = getNum('ambient_temp_f') || 75;
          const thick = getNum('cooler_wall_thickness_in') || 2.0;

          const deltaT = amb - (-109.3);
          const rVal = thick * 4.2;
          const hourlyBtu = (6.5 * deltaT) / rVal;
          const lossRateLbsHr = hourlyBtu / 246;
          const dailyLoss = lossRateLbsHr * 24;

          const totalLoss = lossRateLbsHr * hrs;
          const initialCharge = Math.ceil((totalLoss * 1.25) * 2) / 2;
          const maxHold = lossRateLbsHr > 0 ? (initialCharge / lossRateLbsHr) : 0;
          const co2Cuft = initialCharge * 8.3;

          setDisp('required_dry_ice_lbs', initialCharge.toFixed(1) + ' lbs Dry Ice');
          setDisp('daily_sublimation_rate', dailyLoss.toFixed(1) + ' lbs / day');
          setDisp('max_safe_hold_hours', Math.round(maxHold) + ' Hours (-78.5°C)');
          setDisp('co2_gas_expansion_cuft', Math.round(co2Cuft) + ' cu ft CO₂ Gas');
        """
    },
    {
        "slug": "reverse-logistics-recovery",
        "category": "logistics",
        "name": "Reverse Logistics Return Rate & Restocking Recovery Margin Calculator",
        "description": "Calculate true financial cost of e-commerce product returns, reverse freight, grading/refurbishing labor, liquidation depreciation, and net recovery rate.",
        "hero_badge": "E-Commerce Logistics • Reverse Logistics",
        "formula_display": "Net Return Loss = Return Shipping + Inspection Labor + Restocking + Resale Markdown Discount",
        "fields": [
            {"id": "retail_item_price", "label": "Original Retail Selling Price ($)", "default": 85.0, "prefix": "$", "min": 10, "max": 1000, "step": 5, "hint": "Original product price paid by consumer"},
            {"id": "product_cogs", "label": "Product Cost of Goods Sold (COGS $)", "default": 28.0, "prefix": "$", "min": 2, "max": 500, "step": 2, "hint": "Manufacturing or purchasing wholesale cost"},
            {"id": "return_shipping_cost", "label": "Reverse Return Shipping Cost ($)", "default": 8.50, "prefix": "$", "min": 2, "max": 50, "step": 0.5, "hint": "Inbound carrier return label fee"},
            {"id": "processing_labor_cost", "label": "Inspection & Repackaging Labor ($)", "default": 6.00, "prefix": "$", "min": 1, "max": 30, "step": 0.5, "hint": "Grading, cleaning, and resealing warehouse labor"},
            {"id": "resale_recovery_pct", "label": "Secondary Market Resale Recovery (%)", "default": 65, "suffix": "%", "min": 0, "max": 100, "step": 5, "hint": "Restock as new = 95%, Open-box = 70%, Liquidation = 25%"}
        ],
        "metrics": [
            {"id": "net_profit_per_return", "label": "Net Realized Profit / (Loss) Per Return", "default_display": "-$2.75 / unit", "highlight": True},
            {"id": "total_reverse_cost", "label": "Total Reverse Supply Chain Outflow", "default_display": "$14.50 / return", "highlight": True},
            {"id": "salvage_recovered_value", "label": "Recovered Resale Value", "default_display": "$55.25 (vs $85 original)"},
            {"id": "margin_erosion_pct", "label": "Margin Degradation vs Forward Sale", "default_display": "104.8% Profit Evaporation"}
        ],
        "proof_steps": [
            {"step_title": "Direct Reverse Logistics Expense", "step_text": "Direct Outflow = Return Shipping ($8.50) + Inspection Labor ($6.00) = $14.50."},
            {"step_title": "Salvage Resale Realization", "step_text": "Secondary Resale Revenue = $85.00 × 65% = $55.25."},
            {"step_title": "Net Economic Reconciliation", "step_text": "Net Realized Cash = Resale Revenue ($55.25) - Product COGS ($28.00) - Reverse Logistics ($14.50) = $12.75 profit (compared to $42.50 on a clean forward sale). If liquidation recovery drops below 50%, returns generate catastrophic net losses."}
        ],
        "faqs": [
            {"q": "What is the average return rate in e-commerce vs brick-and-mortar?", "a": "Online apparel and e-commerce return rates average 20% to 30% (and up to 40% during peak holiday season), compared to 8% to 10% for physical brick-and-mortar stores."},
            {"q": "What is a 'Keep It' return refund policy?", "a": "For bulky, low-margin, or hazardous products where return freight ($12+) exceeds the item's salvage value, retailers use algorithmic rules to instantly issue a full refund while instructing the customer to keep or donate the item."}
        ],
        "js_logic": """
          const price = getNum('retail_item_price');
          const cogs = getNum('product_cogs');
          const ship = getNum('return_shipping_cost');
          const labor = getNum('processing_labor_cost');
          const recPct = (getNum('resale_recovery_pct') || 65) / 100;

          const totalReverseOutflow = ship + labor;
          const resaleRev = price * recPct;
          const netReturnProfit = resaleRev - cogs - totalReverseOutflow;
          const originalProfit = price - cogs - 6.0;
          const erosion = originalProfit > 0 ? ((originalProfit - netReturnProfit) / originalProfit) * 100 : 100;

          setDisp('net_profit_per_return', (netReturnProfit >= 0 ? '$' : '-$') + Math.abs(netReturnProfit).toFixed(2) + ' / unit');
          setDisp('total_reverse_cost', '$' + totalReverseOutflow.toFixed(2) + ' / return');
          setDisp('salvage_recovered_value', '$' + resaleRev.toFixed(2) + ' (vs $' + price + ' orig)');
          setDisp('margin_erosion_pct', Math.round(erosion) + '% Profit Loss');
        """
    }
]
