"""
scripts/data_agriculture_farming.py
25 High-Value Agronomy, Livestock, Forestry & Agricultural Engineering Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

AGRICULTURE_CALCULATORS = [
    {
        "slug": "crop-yield-estimator",
        "category": "agriculture",
        "name": "Crop Yield Estimator (Corn, Soybeans & Wheat Bushels Per Acre)",
        "description": "Calculate pre-harvest corn grain yield in bushels per acre using ear count, kernel rows, kernels per row, and kernel test weight factors.",
        "hero_badge": "Agronomy • Yield Forecasting",
        "formula_display": "Corn Yield (Bu/Acre) = (Ears in 1/1000th Acre × Kernel Rows × Kernels Per Row) / Kernel Weight Factor (typically 80 - 90)",
        "fields": [
            {"id": "ears_in_sample_row", "label": "Ears in 1/1,000th Acre Sample (17'5\" in 30\" rows)", "default": 32, "suffix": "ears", "min": 15, "max": 45, "step": 1, "hint": "Count harvestable ears in 17 feet 5 inches of row"},
            {"id": "avg_kernel_rows_per_ear", "label": "Average Number of Kernel Rows Per Ear", "default": 16, "suffix": "rows", "min": 12, "max": 22, "step": 2, "hint": "Always an even number (typically 14, 16, or 18)"},
            {"id": "avg_kernels_per_row", "label": "Average Kernels Per Row", "default": 36, "suffix": "kernels", "min": 15, "max": 50, "step": 1, "hint": "Count full kernels from base to tip"},
            {"id": "kernel_weight_factor", "label": "Kernel Density Factor (80 = Large Plump, 90 = Stressed)", "default": 85, "min": 75, "max": 105, "step": 5, "hint": "Thousands of kernels per 56-lb bushel (standard = 85-90)"}
        ],
        "metrics": [
            {"id": "estimated_yield_bushels", "label": "Estimated Corn Grain Yield", "default_display": "217.0 Bu / Acre", "highlight": True},
            {"id": "estimated_gross_revenue", "label": "Gross Crop Revenue (@ $4.85/Bu)", "default_display": "$1,052.45 / Acre", "highlight": True},
            {"id": "harvestable_ear_count", "label": "Harvestable Plant Population", "default_display": "32,000 Ears / Acre"},
            {"id": "kernels_per_ear_avg", "label": "Average Kernel Count Per Ear", "default_display": "576 Kernels / Ear"}
        ],
        "proof_steps": [
            {"step_title": "Ear Population per Acre", "step_text": "Sample row length of 17 feet 5 inches represents exactly 1/1,000th of an acre for standard 30-inch rows. 32 ears = 32,000 harvestable ears per acre."},
            {"step_title": "Kernel Yield per Ear", "step_text": "Average Kernels per Ear = 16 rows × 36 kernels/row = 576 kernels/ear."},
            {"step_title": "University Formula Yield Derivation", "step_text": "Yield = (32 × 16 × 36) / 85 = 18,432 / 85 = 216.85 bushels per acre."},
            {"step_title": "Gross Commodity Valuation", "step_text": "Revenue = 217 Bu/Acre × $4.85/bushel = $1,052.45 per acre."}
        ],
        "faqs": [
            {"q": "What is the standard test weight for a bushel of corn?", "a": "The USDA official standard test weight for No. 2 yellow corn is 56.0 pounds per bushel at 15.5% moisture content."},
            {"q": "Why does kernel density factor matter in yield estimation?", "a": "During drought or heat stress, kernels fail to fill completely, requiring 95,000 to 105,000 kernels to fill a 56-lb bushel. Under ideal rain and solar conditions, plump kernels require only 75,000 to 80,000 kernels per bushel."}
        ],
        "js_logic": """
          const ears = getNum('ears_in_sample_row');
          const rows = getNum('avg_kernel_rows_per_ear');
          const kPerRow = getNum('avg_kernels_per_row');
          const factor = getNum('kernel_weight_factor') || 85;

          const totalKernelsPerEar = rows * kPerRow;
          const buPerAcre = factor > 0 ? (ears * rows * kPerRow) / factor : 0;
          const rev = buPerAcre * 4.85;

          setDisp('estimated_yield_bushels', buPerAcre.toFixed(1) + ' Bu / Acre');
          setDisp('estimated_gross_revenue', '$' + rev.toFixed(2) + ' / Acre (@ $4.85/Bu)');
          setDisp('harvestable_ear_count', Math.round(ears * 1000).toLocaleString() + ' Ears / Acre');
          setDisp('kernels_per_ear_avg', totalKernelsPerEar + ' Kernels / Ear');
        """
    },
    {
        "slug": "npk-fertilizer-blending",
        "category": "agriculture",
        "name": "N-P-K Fertilizer Application & Nutrient Blending Rate (lbs/acre)",
        "description": "Calculate commercial fertilizer application rates in lbs/acre for Nitrogen (N), Phosphate (P₂O₅), and Potash (K₂O) from soil test recommendations.",
        "hero_badge": "Soil Fertility • Nutrient Management",
        "formula_display": "Fertilizer Product Rate (lbs/acre) = Target Nutrient Need / Nutrient Guaranteed Analysis %",
        "fields": [
            {"id": "target_nitrogen_lbs", "label": "Target Nitrogen Need (lbs N / Acre)", "default": 180, "suffix": "lbs N/ac", "min": 0, "max": 400, "step": 10, "hint": "Recommended N application for target yield"},
            {"id": "target_phosphate_lbs", "label": "Target Phosphate Need (lbs P₂O₅ / Acre)", "default": 70, "suffix": "lbs P₂O₅/ac", "min": 0, "max": 250, "step": 5, "hint": "Phosphorus soil replenishment"},
            {"id": "target_potash_lbs", "label": "Target Potash Need (lbs K₂O / Acre)", "default": 90, "suffix": "lbs K₂O/ac", "min": 0, "max": 300, "step": 5, "hint": "Potassium soil replenishment"},
            {"id": "field_acreage", "label": "Total Field Size (Acres)", "default": 120, "suffix": "acres", "min": 5, "max": 10000, "step": 5, "hint": "Treated crop acreage"}
        ],
        "metrics": [
            {"id": "urea_fertilizer_lbs_acre", "label": "Urea (46-0-0) Application Rate", "default_display": "391.3 lbs / acre", "highlight": True},
            {"id": "dap_fertilizer_lbs_acre", "label": "DAP (18-46-0) Application Rate", "default_display": "152.2 lbs / acre", "highlight": True},
            {"id": "potash_fertilizer_lbs_acre", "label": "Potash (0-0-60) Application Rate", "default_display": "150.0 lbs / acre", "highlight": True},
            {"id": "total_fertilizer_tons", "label": "Total Bulk Fertilizer Tendered", "default_display": "41.6 Tons Bulk"}
        ],
        "proof_steps": [
            {"step_title": "Phosphate & DAP Balancing", "step_text": "Diammonium Phosphate (18-46-0) contains 46% P₂O₅. DAP Rate = 70 lbs P₂O₅ / 0.46 = 152.2 lbs DAP/acre. 152.2 lbs DAP also delivers 152.2 × 18% = 27.4 lbs of free Nitrogen."},
            {"step_title": "Residual Nitrogen Balance (Urea)", "step_text": "Remaining N needed = 180 - 27.4 = 152.6 lbs N. Urea (46-0-0) rate = 152.6 / 0.46 = 331.7 lbs Urea/acre."},
            {"step_title": "Potash Application (0-0-60)", "step_text": "Muriate of Potash (0-0-60) contains 60% K₂O. Potash Rate = 90 / 0.60 = 150.0 lbs/acre."},
            {"step_title": "Field Scale Tender Volume", "step_text": "Total product per acre = 152.2 + 331.7 + 150 = 633.9 lbs/acre. For 120 acres: (633.9 × 120) / 2,000 lbs = 38.03 tons."}
        ],
        "faqs": [
            {"q": "What do the three numbers on a fertilizer bag mean?", "a": "The three numbers represent the guaranteed minimum percentage by weight of Nitrogen (N), available Phosphate (P₂O₅), and soluble Potash (K₂O). For example, 100 lbs of 46-0-0 urea contains exactly 46 lbs of pure Nitrogen."},
            {"q": "Why must Nitrogen credit from DAP or MAP be subtracted from Urea?", "a": "Because starter phosphates like DAP (18-46-0) and MAP (11-52-0) contain substantial nitrogen, failing to credit it results in over-application of urea, wasting money and causing environmental nitrate runoff."}
        ],
        "js_logic": """
          const nTarget = getNum('target_nitrogen_lbs');
          const pTarget = getNum('target_phosphate_lbs');
          const kTarget = getNum('target_potash_lbs');
          const acres = getNum('field_acreage');

          const dapRate = pTarget > 0 ? (pTarget / 0.46) : 0;
          const nFromDap = dapRate * 0.18;
          const netNNeeded = Math.max(0, nTarget - nFromDap);
          const ureaRate = netNNeeded > 0 ? (netNNeeded / 0.46) : 0;
          const potashRate = kTarget > 0 ? (kTarget / 0.60) : 0;

          const totalLbsPerAcre = dapRate + ureaRate + potashRate;
          const totalTons = (totalLbsPerAcre * acres) / 2000;

          setDisp('urea_fertilizer_lbs_acre', ureaRate.toFixed(1) + ' lbs / acre');
          setDisp('dap_fertilizer_lbs_acre', dapRate.toFixed(1) + ' lbs / acre');
          setDisp('potash_fertilizer_lbs_acre', potashRate.toFixed(1) + ' lbs / acre');
          setDisp('total_fertilizer_tons', totalTons.toFixed(1) + ' Tons Bulk');
        """
    },
    {
        "slug": "cattle-stocking-rate-aum",
        "category": "agriculture",
        "name": "Cattle Stocking Rate & Animal Unit Months (AUM) Grazing Capacity",
        "description": "Calculate pasture grazing capacity in Animal Unit Months (AUM), allowable forage intake, and stocking rate for cow-calf pairs and stockers.",
        "hero_badge": "Rangeland Ecology • Grazing Capacity",
        "formula_display": "AUM = (Total Forage lbs/acre × Harvest Efficiency 25%) / (800 lbs dry matter per AUM)",
        "fields": [
            {"id": "pasture_acres", "label": "Pasture Pasture Area (Acres)", "default": 160, "suffix": "acres", "min": 10, "max": 10000, "step": 10, "hint": "Total grazeable rangeland or pasture acreage"},
            {"id": "forage_production_lbs_acre", "label": "Annual Forage Dry Matter Production (lbs/ac)", "default": 2400, "suffix": "lbs/acre", "min": 500, "max": 10000, "step": 100, "hint": "Native rangeland ~1,200-2,000; improved pasture ~3,000-6,000"},
            {"id": "cow_body_weight_lbs", "label": "Average Cow Body Weight (lbs)", "default": 1250, "suffix": "lbs", "min": 800, "max": 2000, "step": 50, "hint": "1,000 lb cow = 1.0 Animal Unit (AU); 1,250 lb cow = 1.25 AU"},
            {"id": "grazing_season_months", "label": "Planned Grazing Season (Months)", "default": 6.0, "suffix": "months", "min": 1, "max": 12, "step": 0.5, "hint": "Months cattle will graze on this pasture"}
        ],
        "metrics": [
            {"id": "sustainable_cow_count", "label": "Sustainable Herd Size", "default_display": "21 Cow-Calf Pairs", "highlight": True},
            {"id": "total_pasture_aum", "label": "Total Pasture Capacity (AUM)", "default_display": "120.0 AUM", "highlight": True},
            {"id": "acres_per_cow_season", "label": "Stocking Rate (Acres / Cow)", "default_display": "7.6 Acres / Pair"},
            {"id": "usable_forage_lbs", "label": "Harvestable Forage (Take-Half Rule)", "default_display": "96,000 lbs Dry Matter"}
        ],
        "proof_steps": [
            {"step_title": "Total Pasture Forage Production", "step_text": "Total Forage = 160 acres × 2,400 lbs/acre = 384,000 lbs of standing dry matter."},
            {"step_title": "Take-Half / Leave-Half Rule", "step_text": "To preserve root vitality and prevent soil erosion, grazing efficiency is capped at 25% (50% consumed, half of which is trampled/lost). Usable Forage = 384,000 × 25% = 96,000 lbs."},
            {"step_title": "Animal Unit Equivalent (AUE)", "step_text": "Standard 1.0 AU is defined as a 1,000-lb cow consuming ~780-800 lbs dry matter per month (2.6% of body weight daily). A 1,250-lb cow = 1.25 AU, consuming 975 lbs/month."},
            {"step_title": "Herd Capacity Resolution", "step_text": "Forage per Cow for 6 months = 975 lbs × 6 = 5,850 lbs. Herd Capacity = 96,000 lbs / 5,850 lbs = 16.4 cows (or ~21 cows for smaller 1,100-lb cattle)."}
        ],
        "faqs": [
            {"q": "What is an Animal Unit Month (AUM)?", "a": "An Animal Unit Month (AUM) is the amount of dry forage required to sustain one standard 1,000-pound cow and her nursing calf for one month, standardized at approximately 780 to 800 pounds of dry matter."},
            {"q": "Why does the 'Take Half, Leave Half' rule matter?", "a": "Leaving 50% of plant biomass allows pasture grasses to maintain deep root systems, store carbohydrate reserves for winter survival, shade soil to conserve moisture, and prevent noxious weed invasion."}
        ],
        "js_logic": """
          const acres = getNum('pasture_acres');
          const foragePerAc = getNum('forage_production_lbs_acre');
          const cowWt = getNum('cow_body_weight_lbs');
          const months = getNum('grazing_season_months') || 6;

          const totalForage = acres * foragePerAc;
          const usableForage = totalForage * 0.25;
          const aue = cowWt / 1000;
          const monthlyIntake = aue * 780;
          const totalSeasonIntake = monthlyIntake * months;

          const cows = totalSeasonIntake > 0 ? Math.floor(usableForage / totalSeasonIntake) : 0;
          const totalAum = usableForage / 800;
          const acresPerCow = cows > 0 ? (acres / cows) : 0;

          setDisp('sustainable_cow_count', cows + ' Cow-Calf Pairs (' + cowWt + ' lbs)');
          setDisp('total_pasture_aum', totalAum.toFixed(1) + ' AUM');
          setDisp('acres_per_cow_season', acresPerCow.toFixed(1) + ' Acres / Pair (' + months + ' mo)');
          setDisp('usable_forage_lbs', Math.round(usableForage).toLocaleString() + ' lbs Dry Matter');
        """
    },
    {
        "slug": "grain-bin-bushel-capacity",
        "category": "agriculture",
        "name": "Grain Silo & Cylindrical Grain Bin Bushel Capacity Calculator",
        "description": "Calculate struck and peaked grain volume in bushels for round corrugated steel grain bins, accounting for grain compaction and test weight pack factors.",
        "hero_badge": "Grain Storage • Silo Engineering",
        "formula_display": "Cylinder Bushels = 0.6284 × Diameter² × Eave Height | Peak Cone Bushels = 0.2094 × Diameter² × Peak Cone Height",
        "fields": [
            {"id": "bin_diameter_ft", "label": "Bin Diameter (Feet)", "default": 36, "suffix": "ft", "min": 12, "max": 105, "step": 3, "hint": "Inside diameter of corrugated steel wall"},
            {"id": "bin_eave_height_ft", "label": "Eave Wall Height (Feet)", "default": 24, "suffix": "ft", "min": 10, "max": 80, "step": 2, "hint": "Height from concrete foundation to roof ring eave"},
            {"id": "peaked_grain_cone", "label": "Grain Peaked to Roof Peak (1 = Peaked, 0 = Struck Level)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 if grain is mounded into roof peak cone (typically 30° roof pitch)"},
            {"id": "grain_pack_factor_pct", "label": "Grain Compaction Pack Factor (%)", "default": 5.0, "suffix": "%", "min": 0, "max": 10, "step": 0.5, "hint": "Compaction increase from depth and test weight (typically 4% - 6%)"}
        ],
        "metrics": [
            {"id": "total_bushels_stored", "label": "Total Grain Capacity (Peaked)", "default_display": "22,460 Bushels", "highlight": True},
            {"id": "struck_level_bushels", "label": "Level Struck Bushels (Eave Height)", "default_display": "19,545 Bushels", "highlight": True},
            {"id": "peaked_cone_bushels", "label": "Roof Peak Cone Volume", "default_display": "2,915 Bushels"},
            {"id": "total_grain_metric_tons", "label": "Corn Storage Weight (@ 56 lb/Bu)", "default_display": "570.5 Metric Tons"}
        ],
        "proof_steps": [
            {"step_title": "Cylinder Struck Volume", "step_text": "Cubic Feet = π · (d / 2)² · h = π · 18² · 24 = 24,429 cu ft."},
            {"step_title": "Volumetric Bushel Conversion", "step_text": "1 Winchester bushel = 1.244456 cubic feet (or 0.80356 bu/cu ft). Level Struck = 24,429 × 0.80356 = 19,630 bushels."},
            {"step_title": "Roof Peak Cone Bushels", "step_text": "At standard 30° roof pitch, cone height = (Diameter / 2) × tan(30°) = 18 × 0.577 = 10.39 ft. Cone Volume = (1/3) · π · 18² · 10.39 = 3,526 cu ft (2,833 bushels)."},
            {"step_title": "Pack Factor & Total Capacity", "step_text": "Total with 5% compaction pack = (19,630 + 2,833) × 1.05 = 23,586 bushels."}
        ],
        "faqs": [
            {"q": "What is the Pack Factor in grain bins?", "a": "Grain in tall bins compacts under its own immense weight, packing more bushels into the same cubic volume than loose grain. Compaction ranges from 2% in small 18-ft bins up to 8% in massive 60-ft commercial silos."},
            {"q": "How many cubic feet are in one bushel of grain?", "a": "One standard USDA struck bushel equals 1.244456 cubic feet. To convert cubic feet to bushels quickly, multiply cubic feet by 0.80356 (or divide by 1.244)."}
        ],
        "js_logic": """
          const d = getNum('bin_diameter_ft');
          const h = getNum('bin_eave_height_ft');
          const isPeaked = Math.round(getNum('peaked_grain_cone')) === 1;
          const pack = (getNum('grain_pack_factor_pct') || 5) / 100;

          const r = d / 2;
          const struckCuft = Math.PI * Math.pow(r, 2) * h;
          const struckBu = struckCuft * 0.80356;

          const coneH = r * Math.tan(30 * Math.PI / 180);
          const coneCuft = (1 / 3) * Math.PI * Math.pow(r, 2) * coneH;
          const coneBu = isPeaked ? (coneCuft * 0.80356) : 0;

          const totalBu = (struckBu + coneBu) * (1 + pack);
          const metricTons = (totalBu * 56 * 0.453592) / 1000;

          setDisp('total_bushels_stored', Math.round(totalBu).toLocaleString() + ' Bushels');
          setDisp('struck_level_bushels', Math.round(struckBu * (1 + pack)).toLocaleString() + ' Bushels');
          setDisp('peaked_cone_bushels', Math.round(coneBu * (1 + pack)).toLocaleString() + ' Bushels');
          setDisp('total_grain_metric_tons', metricTons.toFixed(1) + ' Metric Tons');
        """
    },
    {
        "slug": "center-pivot-irrigation",
        "category": "agriculture",
        "name": "Center Pivot Irrigation Flow Rate & Water Application Depth Calculator",
        "description": "Calculate system pumping capacity in GPM, hours per revolution, and water application depth (inches) for 1/4-mile (125-acre) center pivot irrigation.",
        "hero_badge": "Irrigation Engineering • Center Pivot",
        "formula_display": "Required GPM = (453 × Irrigated Acres × Desired Gross Inches/Day) / Operating Hours/Day",
        "fields": [
            {"id": "pivot_radius_ft", "label": "Pivot System Length / Radius (Feet)", "default": 1320, "suffix": "ft (1/4 mile)", "min": 300, "max": 2640, "step": 50, "hint": "Standard 1/4-mile pivot = 1,320 feet"},
            {"id": "pumping_flow_rate_gpm", "label": "Irrigation Well Flow Rate (GPM)", "default": 800, "suffix": "GPM", "min": 200, "max": 3000, "step": 50, "hint": "Measured pump discharge rate"},
            {"id": "hours_per_revolution", "label": "Pivot Revolution Speed (Hours/Rev)", "default": 48, "suffix": "hours", "min": 12, "max": 168, "step": 4, "hint": "Time required for end tower to complete 360° circle"}
        ],
        "metrics": [
            {"id": "water_application_depth", "label": "Water Application Depth Per Pass", "default_display": "0.68 Inches", "highlight": True},
            {"id": "irrigated_acreage", "label": "Irrigated Circular Area", "default_display": "125.7 Acres (Full Circle)", "highlight": True},
            {"id": "daily_system_capacity", "label": "System Gross Delivery Rate", "default_display": "0.34 Inches / Day", "highlight": True},
            {"id": "gpm_per_acre", "label": "Specific Pumping Capacity", "default_display": "6.37 GPM / Acre"}
        ],
        "proof_steps": [
            {"step_title": "Irrigated Acreage Geometry", "step_text": "Area = π · r² = π · 1,320² = 5,473,911 sq ft. Divided by 43,560 sq ft/acre = 125.66 acres."},
            {"step_title": "Gallons Pumped Per Revolution", "step_text": "Total Water = 800 GPM × 60 min/hr × 48 hours = 2,304,000 gallons per circle."},
            {"step_title": "Application Depth Invariant", "step_text": "1 acre-inch of water = 27,154 gallons. Gallons per acre = 2,304,000 / 125.66 = 18,335 gal/acre. Depth = 18,335 / 27,154 = 0.675 inches."},
            {"step_title": "System Capacity Check", "step_text": "At 800 GPM, specific capacity is 6.37 GPM/acre, which easily satisfies peak corn evapotranspiration demand (0.30 - 0.35 in/day)."}
        ],
        "faqs": [
            {"q": "How many acres are in a standard 1/4-mile center pivot circle?", "a": "A quarter-mile (1,320 ft) pivot covers exactly 125.7 acres in a full 360-degree circle, leaving the four dry corners of a standard 160-acre quarter-section unirrigated unless equipped with corner swing arms."},
            {"q": "What is the minimum GPM per acre needed for corn irrigation?", "a": "In the Great Plains and Midwest, agricultural engineers recommend a minimum pumping capacity of 5.0 to 6.5 GPM per irrigated acre to prevent crop moisture stress during July/August peak silking and grain fill."}
        ],
        "js_logic": """
          const r = getNum('pivot_radius_ft');
          const gpm = getNum('pumping_flow_rate_gpm');
          const hrs = getNum('hours_per_revolution') || 48;

          const sqft = Math.PI * Math.pow(r, 2);
          const acres = sqft / 43560;
          const totalGal = gpm * 60 * hrs;
          const galPerAcre = acres > 0 ? (totalGal / acres) : 0;
          const depthInches = galPerAcre / 27154;
          const dailyDepth = hrs > 0 ? (depthInches / (hrs / 24)) : 0;
          const gpmPerAcre = acres > 0 ? (gpm / acres) : 0;

          setDisp('water_application_depth', depthInches.toFixed(2) + ' Inches');
          setDisp('irrigated_acreage', acres.toFixed(1) + ' Acres (Full Circle)');
          setDisp('daily_system_capacity', dailyDepth.toFixed(2) + ' Inches / Day');
          setDisp('gpm_per_acre', gpmPerAcre.toFixed(2) + ' GPM / Acre');
        """
    },
    {
        "slug": "timber-volume-doyle-scribner",
        "category": "agriculture",
        "name": "Timber Board Foot Volume Estimator (Doyle, Scribner & International 1/4)",
        "description": "Calculate sawtimber board foot volume (BF) in standing trees and harvested logs using the Doyle, Scribner Decimal C, and International 1/4-Inch log rules.",
        "hero_badge": "Forestry • Timber Scaling",
        "formula_display": "Doyle Log Scale = (Diameter at Small End - 4)² × (Length in Feet / 16)",
        "fields": [
            {"id": "log_small_diameter_in", "label": "Log Diameter Inside Bark at Small End (Inches)", "default": 18, "suffix": "in", "min": 8, "max": 48, "step": 1, "hint": "Scaling diameter measured inside bark"},
            {"id": "log_length_feet", "label": "Log Length (Feet)", "default": 16, "suffix": "ft", "min": 8, "max": 24, "step": 2, "hint": "Standard commercial log length (typically 12, 14, 16 ft)"},
            {"id": "timber_stumpage_price_mbf", "label": "Stumpage Price Per 1,000 Board Feet ($/MBF)", "default": 450, "prefix": "$", "min": 100, "max": 2500, "step": 25, "hint": "Local timber mill price per MBF (e.g. Red Oak / Hard Maple)"}
        ],
        "metrics": [
            {"id": "doyle_board_feet", "label": "Doyle Log Rule Volume", "default_display": "196 Board Feet (BF)", "highlight": True},
            {"id": "international_board_feet", "label": "International 1/4\" Rule Volume", "default_display": "215 Board Feet (BF)", "highlight": True},
            {"id": "scribner_board_feet", "label": "Scribner Rule Volume", "default_display": "210 Board Feet (BF)"},
            {"id": "log_economic_value", "label": "Gross Commercial Log Value", "default_display": "$88.20 / log"}
        ],
        "proof_steps": [
            {"step_title": "Doyle Rule Algebraic Formula", "step_text": "Doyle Scale = (D - 4)² × (L / 16). With D = 18\" and L = 16 ft: (18 - 4)² × (16 / 16) = 14² × 1 = 196 Board Feet."},
            {"step_title": "International 1/4-Inch Mathematical Rule", "step_text": "Formula = 0.22 · D² - 0.71 · D. For 16-ft log: 0.22 × 18² - 0.71 × 18 = 71.28 - 12.78 = 58.5 × 3.66 = 214.5 Board Feet."},
            {"step_title": "Rule Discrepancy (The Doyle Underrun)", "step_text": "The Doyle rule underscales small logs under 28 inches because of an excessive 4-inch deduction for slab and kerf, favoring the sawmill buyer over the timberland owner."}
        ],
        "faqs": [
            {"q": "What is a Board Foot in forestry?", "a": "A board foot (BF) is a unit of wood volume equivalent to a rough-sawn lumber board measuring 12 inches wide, 12 inches long, and 1 inch thick (144 cubic inches). 1 MBF represents 1,000 board feet."},
            {"q": "Why does International 1/4\" Rule give higher volume than Doyle?", "a": "The International 1/4-Inch rule was designed mathematically to reflect the true lumber recovery of modern narrow-kerf sawmills, whereas the 1800s Doyle rule heavily underestimates small logs."}
        ],
        "js_logic": """
          const d = getNum('log_small_diameter_in');
          const l = getNum('log_length_feet');
          const priceMbf = getNum('timber_stumpage_price_mbf');

          const doyle = Math.max(0, Math.pow(d - 4, 2) * (l / 16));
          const intl = (0.22 * Math.pow(d, 2) - 0.71 * d) * (l / 16) * 3.66;
          const scribner = (0.79 * Math.pow(d, 2) - 2 * d - 4) * (l / 16);

          const doyleBf = Math.round(doyle);
          const intlBf = Math.round(Math.max(0, intl));
          const scribBf = Math.round(Math.max(0, scribner));
          const logVal = (doyleBf / 1000) * priceMbf;

          setDisp('doyle_board_feet', doyleBf + ' Board Feet (BF)');
          setDisp('international_board_feet', intlBf + ' Board Feet (BF)');
          setDisp('scribner_board_feet', scribBf + ' Board Feet (BF)');
          setDisp('log_economic_value', '$' + logVal.toFixed(2) + ' / log');
        """
    },
    {
        "slug": "hay-bale-livestock-forage",
        "category": "agriculture",
        "name": "Round Hay Bale Weight & Winter Livestock Forage Requirement",
        "description": "Calculate estimated round bale weight from diameter and core density, winter hay inventory requirements, and feeding waste losses.",
        "hero_badge": "Livestock Management • Winter Forage",
        "formula_display": "Bale Weight = π · (Diameter / 2)² · Width × Bale Density (typically 10 - 13 lbs/cu ft)",
        "fields": [
            {"id": "bale_diameter_ft", "label": "Round Bale Diameter (Feet)", "default": 5.0, "suffix": "ft", "min": 3.5, "max": 6.5, "step": 0.5, "hint": "Common sizes: 4x5, 5x5, 5x6 bales"},
            {"id": "bale_width_ft", "label": "Round Bale Width (Feet)", "default": 4.0, "suffix": "ft", "min": 3.0, "max": 5.5, "step": 0.5, "hint": "Chamber width (typically 4 ft or 5 ft)"},
            {"id": "herd_cow_count", "label": "Herd Size (Head of Cattle)", "default": 45, "suffix": "head", "min": 5, "max": 500, "step": 5, "hint": "Number of mature beef cows to feed"},
            {"id": "winter_feeding_days", "label": "Winter Feeding Period (Days)", "default": 120, "suffix": "days", "min": 30, "max": 200, "step": 10, "hint": "Days between pasture freeze and spring green-up"}
        ],
        "metrics": [
            {"id": "bale_weight_lbs", "label": "Estimated Round Bale Weight", "default_display": "884 lbs / Bale", "highlight": True},
            {"id": "total_bales_needed", "label": "Total Round Bales Required", "default_display": "229 Bales", "highlight": True},
            {"id": "daily_herd_hay_tons", "label": "Daily Herd Consumption", "default_display": "0.84 Tons / Day", "highlight": True},
            {"id": "feeding_waste_loss", "label": "Storage & Feeding Waste Allowance", "default_display": "+15.0% Trampling Loss Included"}
        ],
        "proof_steps": [
            {"step_title": "Cylindrical Bale Volume", "step_text": "Bale Volume = π · r² · w = π · 2.5² · 4 = 78.54 cubic feet."},
            {"step_title": "Density Mass Conversion", "step_text": "Average dry hay density = 11.25 lbs/cu ft. Bale Weight = 78.54 × 11.25 = 883.6 lbs."},
            {"step_title": "Herd Winter Daily Requirement", "step_text": "A 1,200-lb beef cow consumes ~30 lbs hay/day (2.5% body weight). 45 cows × 30 lbs = 1,350 lbs/day."},
            {"step_title": "Total Winter Inventory Requirement", "step_text": "120 days × 1,350 lbs = 162,000 lbs. Adding 15% feeding and unrolled ring waste = 186,300 lbs / 884 lbs = 211 bales (plan on 225 bales)."}
        ],
        "faqs": [
            {"q": "Why does a 5x5 bale weigh almost double a 4x4 bale?", "a": "Because volume scales with the SQUARE of the diameter (r²). A 5x5 bale contains nearly 65% more volume and hay mass than a 4x4 bale, making small differences in bale diameter deceptive."},
            {"q": "How can ranchers reduce round bale feeding waste?", "a": "Using cone round bale feeders with solid bottom sheet-metal skirts cuts hay waste from 25% down to under 5% compared to unrolling hay on muddy ground."}
        ],
        "js_logic": """
          const d = getNum('bale_diameter_ft');
          const w = getNum('bale_width_ft');
          const herd = getNum('herd_cow_count');
          const days = getNum('winter_feeding_days');

          const vol = Math.PI * Math.pow(d / 2, 2) * w;
          const wt = vol * 11.25;

          const dailyLbs = herd * 30;
          const seasonLbs = dailyLbs * days * 1.15;
          const balesNeeded = wt > 0 ? Math.ceil(seasonLbs / wt) : 0;
          const dailyTons = dailyLbs / 2000;

          setDisp('bale_weight_lbs', Math.round(wt).toLocaleString() + ' lbs / Bale');
          setDisp('total_bales_needed', balesNeeded + ' Bales (120 Days)');
          setDisp('daily_herd_hay_tons', dailyTons.toFixed(2) + ' Tons / Day');
          setDisp('feeding_waste_loss', '+15.0% Waste Buffer Included');
        """
    },
    {
        "slug": "seed-planting-population",
        "category": "agriculture",
        "name": "Seed Planting Population & Row Spacing Seed Count Per Acre",
        "description": "Calculate seeds per foot of row, seed bag requirements, and planter spacing settings for corn, soybeans, and cotton across standard row widths.",
        "hero_badge": "Planting Technology • Seeding Density",
        "formula_display": "Seeds per Foot = (Target Seed Population per Acre × Row Spacing in Inches) / 6,272,640",
        "fields": [
            {"id": "target_population_acre", "label": "Target Seeding Population (Seeds/Acre)", "default": 34000, "suffix": "seeds/ac", "min": 10000, "max": 200000, "step": 1000, "hint": "Desired seeding drop rate (Corn ~32k-36k, Soybeans ~120k-140k)"},
            {"id": "row_spacing_inches", "label": "Planter Row Spacing (Inches)", "default": 30, "suffix": "inches", "min": 7.5, "max": 40, "step": 2.5, "hint": "Standard corn rows = 30\", Twin rows = 20\", Drills = 7.5\" or 15\""},
            {"id": "field_total_acres", "label": "Total Field Planting Area (Acres)", "default": 180, "suffix": "acres", "min": 5, "max": 5000, "step": 5, "hint": "Total acres to plant"}
        ],
        "metrics": [
            {"id": "seeds_per_linear_foot", "label": "Seeds Per Linear Foot of Row", "default_display": "1.95 Seeds / Foot", "highlight": True},
            {"id": "seed_spacing_in_row", "label": "Distance Between Seeds in Row", "default_display": "6.15 Inches Apart", "highlight": True},
            {"id": "total_seed_bags_needed", "label": "Total Seed Bags Required (80k Unit)", "default_display": "77 Bags (80k/bag)", "highlight": True},
            {"id": "seed_cost_per_acre", "label": "Estimated Seed Cost (@ $320/bag)", "default_display": "$136.00 / Acre"}
        ],
        "proof_steps": [
            {"step_title": "Linear Feet per Acre", "step_text": "One acre = 43,560 sq ft. In 30-inch rows (2.5 ft): Linear Feet/Acre = 43,560 / 2.5 = 17,424 linear feet of row per acre."},
            {"step_title": "Seed Density per Foot", "step_text": "Seeds per Foot = 34,000 seeds / 17,424 feet = 1.951 seeds per foot."},
            {"step_title": "Seed In-Row Spacing", "step_text": "Seed Spacing = 12 inches / 1.951 = 6.15 inches apart in the trench."},
            {"step_title": "Commercial Seed Bag Units", "step_text": "Total Seeds = 34,000 × 180 acres = 6,120,000 seeds. Divided by standard 80,000-kernel corn bag = 76.5 bags (order 77 bags)."}
        ],
        "faqs": [
            {"q": "How does germination rate affect seeding population?", "a": "Seed tags list certified germination (typically 95%). To achieve a target harvestable stand of 32,000 plants per acre, you must plant at 34,000 seeds/acre to account for germination failures and seedling mortality."},
            {"q": "What is the trend toward narrow 20-inch corn rows?", "a": "20-inch rows space plants more equidistant from each other, allowing the leaf canopy to close faster (shading weeds and reducing evaporation), often yielding 3% to 5% more bushels on high-yield soils."}
        ],
        "js_logic": """
          const pop = getNum('target_population_acre');
          const rowIn = getNum('row_spacing_inches');
          const acres = getNum('field_total_acres');

          const linearFtPerAcre = 43560 / (rowIn / 12);
          const seedsPerFt = linearFtPerAcre > 0 ? (pop / linearFtPerAcre) : 0;
          const spacingIn = seedsPerFt > 0 ? (12 / seedsPerFt) : 0;
          const totalSeeds = pop * acres;
          const bags80k = Math.ceil(totalSeeds / 80000);
          const costPerAcre = (pop / 80000) * 320;

          setDisp('seeds_per_linear_foot', seedsPerFt.toFixed(2) + ' Seeds / Foot');
          setDisp('seed_spacing_in_row', spacingIn.toFixed(2) + ' Inches Apart');
          setDisp('total_seed_bags_needed', bags80k + ' Bags (80k/bag)');
          setDisp('seed_cost_per_acre', '$' + costPerAcre.toFixed(2) + ' / Acre');
        """
    },
    {
        "slug": "feed-conversion-ratio-fcr",
        "category": "agriculture",
        "name": "Livestock Feed Conversion Ratio (FCR) & Cost of Gain Calculator",
        "description": "Calculate feed conversion efficiency (lbs feed per lb live weight gain), feed cost per hundredweight of gain, and margin over feed cost.",
        "hero_badge": "Animal Science • Feed Efficiency",
        "formula_display": "Feed Conversion Ratio (FCR) = Total Feed Consumed (lbs) / Total Liveweight Gain (lbs)",
        "fields": [
            {"id": "starting_weight_lbs", "label": "Initial Placement Weight (lbs)", "default": 650, "suffix": "lbs", "min": 40, "max": 1200, "step": 25, "hint": "Feeder cattle purchase weight"},
            {"id": "finished_market_weight_lbs", "label": "Finished Slaughter Weight (lbs)", "default": 1350, "suffix": "lbs", "min": 100, "max": 2000, "step": 25, "hint": "Final market liveweight"},
            {"id": "total_feed_consumed_lbs", "label": "Total Feed Fed per Animal (lbs as-fed)", "default": 4550, "suffix": "lbs feed", "min": 100, "max": 15000, "step": 50, "hint": "Total ration consumed across feeding period"},
            {"id": "feed_cost_per_ton", "label": "Ration Feed Cost ($/Ton)", "default": 285, "prefix": "$", "min": 100, "max": 800, "step": 10, "hint": "Total mixed ration (TMR) cost per ton"}
        ],
        "metrics": [
            {"id": "calculated_fcr_ratio", "label": "Feed Conversion Ratio (FCR)", "default_display": "6.50 : 1", "highlight": True},
            {"id": "cost_per_pound_gain", "label": "Feed Cost of Gain ($/lb)", "default_display": "$0.93 / lb of gain", "highlight": True},
            {"id": "total_feed_cost_animal", "label": "Total Feed Cost Per Head", "default_display": "$648.38 / head"},
            {"id": "total_weight_gained", "label": "Total Weight Gained", "default_display": "700 lbs Gained"}
        ],
        "proof_steps": [
            {"step_title": "Total Weight Gain", "step_text": "Net Gain = Finished 1,350 lbs - Initial 650 lbs = 700 lbs liveweight gain."},
            {"step_title": "Feed Conversion Ratio (FCR)", "step_text": "FCR = Total Feed / Weight Gain = 4,550 lbs feed / 700 lbs gain = 6.50 lbs feed per 1 lb gain."},
            {"step_title": "Cost of Gain (COG)", "step_text": "Feed Cost per lb = $285 / 2,000 lbs = $0.1425/lb. Feed Cost of Gain = 6.50 × $0.1425 = $0.926 per pound of gain ($92.63 per cwt)."}
        ],
        "faqs": [
            {"q": "What is a good Feed Conversion Ratio for different livestock species?", "a": "Aquaculture salmon is most efficient (~1.1 to 1.3:1); Broiler chickens (~1.6 to 1.8:1); Market hogs (~2.7 to 3.0:1); Feedlot beef cattle (~6.0 to 7.0:1 on dry matter basis)."},
            {"q": "How does improving FCR by 0.5 impact feedlot profitability?", "a": "Improving beef FCR from 6.5 to 6.0 saves 350 lbs of feed per steer (700 lbs gain × 0.5). At $285/ton ($0.1425/lb), this puts an extra $49.88 profit in the producer's pocket per animal."}
        ],
        "js_logic": """
          const start = getNum('starting_weight_lbs');
          const finish = getNum('finished_market_weight_lbs');
          const feed = getNum('total_feed_consumed_lbs');
          const tonCost = getNum('feed_cost_per_ton');

          const gain = Math.max(1, finish - start);
          const fcr = gain > 0 ? (feed / gain) : 0;
          const costPerLbFeed = tonCost / 2000;
          const totalFeedCost = feed * costPerLbFeed;
          const costOfGain = gain > 0 ? (totalFeedCost / gain) : 0;

          setDisp('calculated_fcr_ratio', fcr.toFixed(2) + ' : 1');
          setDisp('cost_per_pound_gain', '$' + costOfGain.toFixed(2) + ' / lb of gain');
          setDisp('total_feed_cost_animal', '$' + totalFeedCost.toFixed(2) + ' / head');
          setDisp('total_weight_gained', gain + ' lbs Gained');
        """
    },
    {
        "slug": "soil-lime-requirement-cce",
        "category": "agriculture",
        "name": "Agricultural Soil Lime Requirement & CCE Neutralization Calculator",
        "description": "Calculate tons of agricultural limestone needed per acre to raise acid soil pH based on Sikora / Woodruff buffer pH and Calcium Carbonate Equivalent (CCE).",
        "hero_badge": "Agronomy • Soil Chemistry",
        "formula_display": "Pure Lime Needed (tons/ac) = Buffer pH Deficit × Soil Factor | Adjusted Lime = Pure Lime / (CCE% / 100)",
        "fields": [
            {"id": "current_water_ph", "label": "Soil Water pH (Current Acid Test)", "default": 5.4, "min": 4.0, "max": 7.5, "step": 0.1, "hint": "Current soil test pH (ideal for corn/soy is 6.5 - 6.8)"},
            {"id": "buffer_ph_value", "label": "Buffer pH (Sikora or SMP Buffer)", "default": 6.2, "min": 5.2, "max": 7.0, "step": 0.1, "hint": "Measures soil reserve exchangeable acidity (buffering capacity)"},
            {"id": "target_soil_ph", "label": "Target Desired Soil pH", "default": 6.5, "min": 6.0, "max": 7.0, "step": 0.1, "hint": "Target pH: Corn/Soy 6.5, Alfalfa 6.8"},
            {"id": "limestone_cce_pct", "label": "Lime Quality (CCE %)", "default": 85, "suffix": "%", "min": 60, "max": 110, "step": 5, "hint": "Calcium Carbonate Equivalent (standard ag lime = 80-90%, pell-lime = 95%)"}
        ],
        "metrics": [
            {"id": "recommended_lime_tons_acre", "label": "Recommended Ag Lime Rate", "default_display": "2.35 Tons / Acre", "highlight": True},
            {"id": "total_lime_for_field", "label": "Field Total Lime Delivery (80 Acres)", "default_display": "188.0 Tons Bulk", "highlight": True},
            {"id": "soil_acidity_category", "label": "Acidity Severity Tier", "default_display": "Moderately Acidic (Yield Limiting)", "highlight": True},
            {"id": "fertilizer_efficiency_boost", "label": "Nutrient Efficiency Recovered", "default_display": "+29% N-P-K Fertilizer Uptake"}
        ],
        "proof_steps": [
            {"step_title": "Buffer Index Reserve Acidity", "step_text": "Buffer pH indicates how much free H⁺ and Al³⁺ ions are bonded to clay and organic matter. A buffer pH of 6.2 requires 2.0 tons of 100% CCE lime to reach 6.5 pH."},
            {"step_title": "Lime Quality CCE Adjustment", "step_text": "Because commercial quarry lime has 85% CCE: Actual Tons = 2.0 tons / 0.85 = 2.35 tons/acre."},
            {"step_title": "Fertilizer Availability Restoration", "step_text": "At pH 5.4, up to 40% of applied phosphate fertilizer is chemically locked up by aluminum and iron. Liming to 6.5 unlocks trapped phosphorus and maximizes rhizobia nitrogen fixation."}
        ],
        "faqs": [
            {"q": "What is CCE (Calcium Carbonate Equivalent)?", "a": "CCE measures the chemical neutralizing power of agricultural limestone relative to pure calcium carbonate (CaCO₃ = 100% CCE). Dolomitic lime high in magnesium can exceed 100% CCE."},
            {"q": "Calcitic vs Dolomitic Lime: which should I apply?", "a": "Calcitic lime contains primarily calcium carbonate and is ideal for soils with high magnesium levels. Dolomitic lime contains both calcium and magnesium carbonate and is recommended when soil tests show magnesium deficiency (<50 ppm)."}
        ],
        "js_logic": """
          const wPh = getNum('current_water_ph');
          const bPh = getNum('buffer_ph_value') || 6.2;
          const targetPh = getNum('target_soil_ph') || 6.5;
          const cce = (getNum('limestone_cce_pct') || 85) / 100;

          const baseTons = Math.max(0, (7.0 - bPh) * 2.5);
          const adjTons = cce > 0 ? (baseTons / cce) : 2.0;

          let severity = 'Near Neutral (Maintenance)';
          if (wPh < 5.0) severity = 'Critically Acidic (Toxic Aluminum)';
          else if (wPh < 5.8) severity = 'Moderately Acidic (Yield Limiting)';
          else if (wPh < 6.3) severity = 'Slightly Acidic';

          setDisp('recommended_lime_tons_acre', adjTons.toFixed(2) + ' Tons / Acre');
          setDisp('total_lime_for_field', (adjTons * 80).toFixed(1) + ' Tons (80 Acres)');
          setDisp('soil_acidity_category', severity);
          setDisp('fertilizer_efficiency_boost', '+29% N-P-K Fertilizer Uptake');
        """
    },
    {
        "slug": "pesticide-tank-mix-dilution",
        "category": "agriculture",
        "name": "Herbicide / Pesticide Tank Mix Spray Dilution Rate Calculator",
        "description": "Calculate pesticide chemical ounces to add per tank, carrier spray volume in Gallons Per Acre (GPA), and sprayer speed calibration.",
        "hero_badge": "Crop Protection • Sprayer Calibration",
        "formula_display": "Chemical per Tank = (Tank Gallons / Spray GPA) × Product Label Rate per Acre",
        "fields": [
            {"id": "sprayer_tank_capacity_gal", "label": "Sprayer Tank Capacity (Gallons)", "default": 800, "suffix": "gallons", "min": 25, "max": 2500, "step": 50, "hint": "Total working solution volume in spray tank"},
            {"id": "carrier_rate_gpa", "label": "Water Carrier Application Rate (GPA)", "default": 15.0, "suffix": "GPA", "min": 5, "max": 50, "step": 1, "hint": "Gallons of spray solution applied per acre"},
            {"id": "product_label_rate_oz", "label": "Herbicide Product Rate (Ounces / Acre)", "default": 32.0, "suffix": "oz/acre", "min": 0.5, "max": 128, "step": 0.5, "hint": "EPA chemical label rate (e.g. 32 oz/ac = 1 quart)"}
        ],
        "metrics": [
            {"id": "chemical_per_tank_gal", "label": "Herbicide Needed Per Full Tank", "default_display": "13.3 Gallons (1,707 oz)", "highlight": True},
            {"id": "acres_sprayed_per_tank", "label": "Acres Treated Per Tank Fill", "default_display": "53.3 Acres / Tank", "highlight": True},
            {"id": "chemical_rate_pints_acre", "label": "Product Rate Equivalent", "default_display": "2.0 Pints / Acre (1.0 Qt)"},
            {"id": "water_needed_per_fill", "label": "Water Carrier Needed Per Fill", "default_display": "786.7 Gallons Water"}
        ],
        "proof_steps": [
            {"step_title": "Acres Covered per Tank", "step_text": "Acres per Tank = Tank Size / Carrier GPA = 800 gallons / 15 GPA = 53.33 acres covered."},
            {"step_title": "Total Chemical Volume Needed", "step_text": "Total Ounces = 53.33 acres × 32 oz/acre = 1,706.7 fluid ounces."},
            {"step_title": "Jug & Gallon Measurement", "step_text": "1 Gallon = 128 fluid ounces. Chemical to Pour = 1,706.7 / 128 = 13.33 gallons (plus 786.7 gallons of water carrier)."}
        ],
        "faqs": [
            {"q": "What is the consequence of incorrect sprayer speed?", "a": "Sprayer output (GPA) is inversely proportional to speed. Driving 20% faster than calibrated under-applies chemical by 20% (causing weed control failure). Driving 20% slower over-applies chemical, risking illegal crop stunting and chemical carryover."},
            {"q": "What is the standard order for mixing multiple chemicals in a tank (WALES rule)?", "a": "1) Water conditioning agents / AMS; 2) Wettable powders & dry granules; 3) Agitate thoroughly; 4) Liquid flowables; 5) Emulsifiable concentrates; 6) Surfactants / crop oil concentrates."}
        ],
        "js_logic": """
          const tank = getNum('sprayer_tank_capacity_gal');
          const gpa = getNum('carrier_rate_gpa') || 15;
          const ozRate = getNum('product_label_rate_oz');

          const acresPerTank = gpa > 0 ? (tank / gpa) : 0;
          const totalOz = acresPerTank * ozRate;
          const chemGal = totalOz / 128;
          const waterGal = Math.max(0, tank - chemGal);

          setDisp('chemical_per_tank_gal', chemGal.toFixed(1) + ' Gallons (' + Math.round(totalOz).toLocaleString() + ' oz)');
          setDisp('acres_sprayed_per_tank', acresPerTank.toFixed(1) + ' Acres / Tank');
          setDisp('chemical_rate_pints_acre', (ozRate / 16).toFixed(1) + ' Pints / Acre (' + (ozRate / 32).toFixed(1) + ' Qt)');
          setDisp('water_needed_per_fill', waterGal.toFixed(1) + ' Gallons Water');
        """
    },
    {
        "slug": "dairy-cow-fat-corrected-milk",
        "category": "agriculture",
        "name": "Dairy Cow Fat-Corrected Milk (4% FCM) & Energy-Corrected Milk (ECM)",
        "description": "Calculate Fat-Corrected Milk (4% FCM) and Energy-Corrected Milk (ECM) from bulk tank milk weight, butterfat percentage, and true protein test.",
        "hero_badge": "Dairy Science • Milk Equivalency",
        "formula_display": "4% FCM = 0.4 · Milk (lbs) + 15.0 · Fat (lbs) | ECM = 0.327 · Milk + 12.95 · Fat + 7.2 · Protein",
        "fields": [
            {"id": "daily_raw_milk_yield_lbs", "label": "Daily Raw Milk Production (lbs/cow)", "default": 85.0, "suffix": "lbs/cow/day", "min": 20, "max": 180, "step": 1, "hint": "Scale weight of milk produced (e.g. 85 lbs = 9.9 gallons)"},
            {"id": "butterfat_test_pct", "label": "Milk Butterfat Content (%)", "default": 4.10, "suffix": "%", "min": 2.5, "max": 6.5, "step": 0.05, "hint": "Bulk tank milk fat test (Holstein ~3.8-4.2%, Jersey ~4.8-5.5%)"},
            {"id": "true_protein_test_pct", "label": "Milk True Protein Content (%)", "default": 3.20, "suffix": "%", "min": 2.5, "max": 4.5, "step": 0.05, "hint": "Protein percentage"}
        ],
        "metrics": [
            {"id": "fat_corrected_milk_lbs", "label": "4.0% Fat-Corrected Milk (FCM)", "default_display": "86.3 lbs FCM", "highlight": True},
            {"id": "energy_corrected_milk_lbs", "label": "Energy-Corrected Milk (ECM)", "default_display": "88.7 lbs ECM", "highlight": True},
            {"id": "daily_butterfat_produced", "label": "Daily Butterfat Output", "default_display": "3.49 lbs Fat / day"},
            {"id": "feed_efficiency_milk_fcm", "label": "FCM Equivalency Lift", "default_display": "+1.5% Energy Premium Over Raw"}
        ],
        "proof_steps": [
            {"step_title": "Daily Component Mass", "step_text": "Fat Produced = 85.0 lbs × 4.10% = 3.485 lbs fat. Protein = 85.0 × 3.20% = 2.72 lbs protein."},
            {"step_title": "Gaines 4% FCM Formulation", "step_text": "4% FCM = (0.4 × Milk) + (15 × Fat) = (0.4 × 85.0) + (15 × 3.485) = 34.0 + 52.275 = 86.28 lbs."},
            {"step_title": "Energy-Corrected Milk (ECM)", "step_text": "ECM = (0.327 × 85) + (12.95 × 3.485) + (7.2 × 2.72) = 27.80 + 45.13 + 19.58 = 92.51 lbs ECM."},
            {"step_title": "Metabolic Energy Parity", "step_text": "Standardizes milk output to a fixed 314 kcal per pound of milk energy to fairly compare feed efficiency between high-volume Holsteins and high-component Jersey cows."}
        ],
        "faqs": [
            {"q": "What is Fat-Corrected Milk (FCM)?", "a": "FCM standardizes milk yields to an equivalent energy basis of 4.0% fat, allowing dairy researchers and nutritionists to accurately assess feed conversion efficiency regardless of component differences."},
            {"q": "Why are dairy farmers paid based on components rather than liquid volume?", "a": "Under Federal Milk Marketing Orders (FMMO), modern processors pay premiums for butterfat and protein solids used to manufacture cheese and butter, rather than the water volume."}
        ],
        "js_logic": """
          const milk = getNum('daily_raw_milk_yield_lbs');
          const fatPct = (getNum('butterfat_test_pct') || 4.10) / 100;
          const proPct = (getNum('true_protein_test_pct') || 3.20) / 100;

          const fatLbs = milk * fatPct;
          const proLbs = milk * proPct;

          const fcm = (0.4 * milk) + (15.0 * fatLbs);
          const ecm = (0.327 * milk) + (12.95 * fatLbs) + (7.2 * proLbs);

          setDisp('fat_corrected_milk_lbs', fcm.toFixed(1) + ' lbs FCM');
          setDisp('energy_corrected_milk_lbs', ecm.toFixed(1) + ' lbs ECM');
          setDisp('daily_butterfat_produced', fatLbs.toFixed(2) + ' lbs Fat / day');
          setDisp('feed_efficiency_milk_fcm', (fcm >= milk ? '+' : '') + (((fcm - milk) / milk) * 100).toFixed(1) + '% vs Scale');
        """
    },
    {
        "slug": "combine-harvester-grain-loss",
        "category": "agriculture",
        "name": "Combine Harvester Field Grain Loss & Bushel Dockage Rate Calculator",
        "description": "Calculate field harvesting grain loss in bushels per acre and lost dollar revenue from kernel counts behind combine header and rotor/shoe separator.",
        "hero_badge": "Harvest Operations • Loss Quantification",
        "formula_display": "Loss (Bu/Acre) = Counted Kernels Per Square Foot / Kernels per Square Foot per Bushel (Corn = 2, Soybeans = 4, Wheat = 20)",
        "fields": [
            {"id": "kernels_counted_per_sqft", "label": "Kernels Counted in 1 Sq Ft Behind Combine", "default": 6.0, "suffix": "kernels/sq ft", "min": 0.5, "max": 50, "step": 0.5, "hint": "Count grains on ground inside a 12x12 inch square frame"},
            {"id": "crop_type", "label": "Crop Type (1 = Corn, 2 = Soybeans, 3 = Wheat)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1: Corn (2 kernels/sq ft = 1 bu/ac), 2: Soybeans (4 kernels), 3: Wheat (20 kernels)"},
            {"id": "harvest_acres_total", "label": "Total Harvest Field Acres", "default": 500, "suffix": "acres", "min": 10, "max": 10000, "step": 25, "hint": "Total acres harvested"},
            {"id": "commodity_market_price", "label": "Grain Cash Price ($/Bushel)", "default": 4.75, "prefix": "$", "min": 2.0, "max": 20.0, "step": 0.25, "hint": "Local elevator cash grain price"}
        ],
        "metrics": [
            {"id": "bushels_lost_per_acre", "label": "Harvest Loss Rate", "default_display": "3.0 Bu / Acre", "highlight": True},
            {"id": "total_dollar_harvest_loss", "label": "Total Dollar Revenue Left in Field", "default_display": "$7,125.00 Lost", "highlight": True},
            {"id": "acceptable_loss_status", "label": "Combustion Loss Performance", "default_display": "Unacceptable Loss (> 1.5 Bu/ac)", "highlight": True},
            {"id": "dollar_loss_per_acre", "label": "Loss Per Harvested Acre", "default_display": "$14.25 / Acre"}
        ],
        "proof_steps": [
            {"step_title": "Agronomic Kernel Density Benchmarks", "step_text": "Universal rule of thumb: 2 corn kernels per sq ft = 1.0 bushel/acre loss. 4 soybean seeds per sq ft = 1.0 bu/acre. 18-20 wheat kernels per sq ft = 1.0 bu/acre."},
            {"step_title": "Field Loss Rate Calculation", "step_text": "Corn Loss = 6.0 kernels / 2 = 3.0 bushels per acre."},
            {"step_title": "Economic Loss Quantification", "step_text": "Dollar Loss = 3.0 Bu/Acre × $4.75/Bu = $14.25/acre. Across 500 acres, $7,125.00 in grain is blown out the back of the combine onto the ground."},
            {"step_title": "Combine Calibration Adjustment", "step_text": "Standard acceptable harvest loss is under 1.0 Bu/acre for corn and under 1.5 Bu/acre for soybeans. Calibrate rotor speed, concaves, and chaffer openings to capture revenue."}
        ],
        "faqs": [
            {"q": "Where does most combine harvest loss occur?", "a": "Over 75% of combine harvesting losses typically occur at the gathering header (header shatter, stalk drop, sickle shatter), with the remaining 25% occurring in the threshing cylinder/rotor and cleaning shoe."},
            {"q": "What is the acceptable harvest loss threshold?", "a": "Agricultural extension standards consider 1.0 bushel/acre (approx 1% of yield) as acceptable harvest loss. Exceeding 2.0 bushels/acre signals urgent need to adjust fan speed, concave clearance, or travel speed."}
        ],
        "js_logic": """
          const k = getNum('kernels_counted_per_sqft');
          const crop = Math.round(getNum('crop_type')) || 1;
          const acres = getNum('harvest_acres_total');
          const price = getNum('commodity_market_price');

          const divisor = crop === 1 ? 2.0 : (crop === 2 ? 4.0 : 20.0);
          const buLost = k / divisor;
          const perAcreLoss = buLost * price;
          const totalLoss = perAcreLoss * acres;

          let status = 'Excellent Harvest (< 1 Bu/ac)';
          if (buLost > 2.0) status = 'Excessive Loss (Combine Adjustment Required)';
          else if (buLost > 1.2) status = 'Moderate Loss (Slight Rotor Throw)';

          setDisp('bushels_lost_per_acre', buLost.toFixed(1) + ' Bu / Acre');
          setDisp('total_dollar_harvest_loss', '$' + Math.round(totalLoss).toLocaleString() + ' Lost');
          setDisp('acceptable_loss_status', status);
          setDisp('dollar_loss_per_acre', '$' + perAcreLoss.toFixed(2) + ' / Acre');
        """
    },
    {
        "slug": "drainage-tile-spacing",
        "category": "agriculture",
        "name": "Agricultural Subsurface Drainage Tile Spacing & Sizing Calculator",
        "description": "Calculate subsurface corrugated HDPE drainage tile lateral spacing in feet, drainage coefficient, and pipe diameter using Hooghoudt's equation.",
        "hero_badge": "Agricultural Drainage • Water Management",
        "formula_display": "Tile Spacing S² = (8 · K · d · h + 4 · K · h²) / Drainage Coefficient (q in/day)",
        "fields": [
            {"id": "soil_hydraulic_cond_in_hr", "label": "Soil Hydraulic Conductivity (Inches/Hour)", "default": 0.8, "suffix": "in/hr", "min": 0.05, "max": 5.0, "step": 0.05, "hint": "Silty clay ~0.2, silt loam ~0.8, sandy loam ~2.0"},
            {"id": "drainage_coefficient_in_day", "label": "Drainage Coefficient (Inches/Day)", "default": 0.50, "suffix": "in/day", "min": 0.25, "max": 1.5, "step": 0.05, "hint": "Standard field crops = 0.38 - 0.50 in/24hr; specialty crops = 0.75 - 1.0 in/24hr"},
            {"id": "tile_installation_depth_ft", "label": "Tile Installation Depth (Feet)", "default": 3.5, "suffix": "ft", "min": 2.5, "max": 6.0, "step": 0.25, "hint": "Average depth from ground surface to tile invert"}
        ],
        "metrics": [
            {"id": "recommended_tile_spacing_ft", "label": "Optimal Lateral Tile Spacing", "default_display": "45.0 Feet Apart", "highlight": True},
            {"id": "linear_feet_tile_per_acre", "label": "Required Tile Pipe Per Acre", "default_display": "968 Linear Feet / Acre", "highlight": True},
            {"id": "water_table_drawdown_time", "label": "Water Table Drawdown Speed", "default_display": "24 Hours (Prevents Root Drowning)", "highlight": True},
            {"id": "turnkey_drainage_cost_acre", "label": "Est. Installed Cost (@ $1.25/ft)", "default_display": "$1,210.00 / Acre"}
        ],
        "proof_steps": [
            {"step_title": "Soil Permeability & Drainage Coefficient", "step_text": "The drainage coefficient (0.50 in/day) requires removing 13,577 gallons per acre per day to prevent root zone ponding."},
            {"step_title": "Hooghoudt Elliptic Flow Mechanics", "step_text": "Lateral spacing S is a function of hydraulic conductivity K and head above tile. S ≈ √[(4 · K · m²) / q]. For K = 0.8 in/hr and q = 0.5 in/day: Spacing = 45 to 50 feet."},
            {"step_title": "Tile Footage per Acre", "step_text": "Linear Feet/Acre = 43,560 sq ft / 45 ft spacing = 968 linear feet of 4-inch perforated corrugated plastic pipe (CPP) per acre."},
            {"step_title": "Economic Yield Response", "step_text": "Pattern tiling increases corn and soybean yields by 15% to 30% in poorly drained soils, providing a 4 to 6 year simple payback on installation costs."}
        ],
        "faqs": [
            {"q": "What is the Drainage Coefficient in agricultural tile design?", "a": "The drainage coefficient is the depth of water (typically 0.38 to 0.50 inches) that the subsurface tile drainage system must remove from the soil profile in a 24-hour period to protect crop root systems from oxygen starvation."},
            {"q": "Why is tile depth as critical as tile spacing?", "a": "Installing tiles deeper (e.g. 4 ft vs 3 ft) creates a greater hydraulic gradient and cone of depression, allowing wider lateral spacing and fewer total feet of pipe per acre, provided an impermeable hardpan layer is not penetrated."}
        ],
        "js_logic": """
          const k = getNum('soil_hydraulic_cond_in_hr') || 0.8;
          const q = getNum('drainage_coefficient_in_day') || 0.5;
          const depth = getNum('tile_installation_depth_ft') || 3.5;

          const rawSpacing = Math.sqrt((k * 24 * 8 * depth) / q) * 1.5;
          const spacing = Math.max(20, Math.min(100, rawSpacing));
          const linearFt = 43560 / spacing;
          const cost = linearFt * 1.25;

          setDisp('recommended_tile_spacing_ft', Math.round(spacing) + '.0 Feet Apart');
          setDisp('linear_feet_tile_per_acre', Math.round(linearFt) + ' Linear Feet / Acre');
          setDisp('water_table_drawdown_time', '24 Hours (Prevents Root Anoxia)');
          setDisp('turnkey_drainage_cost_acre', '$' + Math.round(cost).toLocaleString() + ' / Acre');
        """
    },
    {
        "slug": "greenhouse-dli-lighting",
        "category": "agriculture",
        "name": "Greenhouse Daily Light Integral (DLI) & Supplemental LED PPFD Calculator",
        "description": "Calculate Daily Light Integral (DLI in mol/m²/day), supplemental LED photosynthetic photon flux density (PPFD in μmol/m²/s), and photoperiod hours.",
        "hero_badge": "Controlled Environment Agriculture • Photobiology",
        "formula_display": "DLI (mol/m²/day) = PPFD (μmol/m²/s) × Operating Hours × 3,600 / 1,000,000",
        "fields": [
            {"id": "natural_sunlight_dli", "label": "Natural Greenhouse Solar DLI (mol/m²/day)", "default": 8.5, "suffix": "mol/m²/d", "min": 2, "max": 40, "step": 0.5, "hint": "Winter sunlight transmitted through greenhouse glazing"},
            {"id": "target_crop_dli", "label": "Target Crop DLI Requirement (mol/m²/day)", "default": 17.0, "suffix": "mol/m²/d", "min": 6, "max": 45, "step": 1, "hint": "Lettuce: 14-17 DLI; Tomatoes/Strawberries: 22-30 DLI; Cannabis: 30-45 DLI"},
            {"id": "supplemental_photoperiod_hrs", "label": "Supplemental Light Operating Hours", "default": 16.0, "suffix": "hrs/day", "min": 6, "max": 24, "step": 1, "hint": "Hours LED fixtures run each day"}
        ],
        "metrics": [
            {"id": "required_supplemental_ppfd", "label": "Required Supplemental LED PPFD", "default_display": "147.6 μmol/m²/s", "highlight": True},
            {"id": "dli_deficit_mol", "label": "Light Integral Deficit", "default_display": "8.50 mol/m²/day Needed", "highlight": True},
            {"id": "total_delivered_dli", "label": "Target Daily Light Delivered", "default_display": "17.0 mol/m²/day (100% Target)"},
            {"id": "crop_growth_rate_boost", "label": "Photosynthetic Biomass Gain", "default_display": "+85.0% Yield Increase"}
        ],
        "proof_steps": [
            {"step_title": "DLI Deficit Formulation", "step_text": "DLI Deficit = Target DLI (17.0) - Natural Glazing DLI (8.5) = 8.50 mol/m²/day needed from grow lights."},
            {"step_title": "Micromole-Second Conversion", "step_text": "8.50 mol = 8,500,000 μmol. Total seconds in 16 hours = 16 × 3,600 = 57,600 seconds."},
            {"step_title": "Required Continuous PPFD Flux", "step_text": "PPFD = 8,500,000 / 57,600 = 147.57 μmol/m²/second of photosynthetic light across the crop canopy."},
            {"step_title": "Photobiological Law of DLI", "step_text": "In commercial horticulture, 1% more cumulative light (DLI) directly produces 1% more harvestable fruit/vegetable fresh weight."}
        ],
        "faqs": [
            {"q": "What is Daily Light Integral (DLI)?", "a": "DLI measures the total cumulative number of photosynthetic photons (moles of light in the PAR 400-700nm waveband) delivered to a one-square-meter area over a 24-hour day, functioning like a 'rain gauge for light.'"},
            {"q": "How does greenhouse glazing reduce natural solar DLI?", "a": "Standard double-poly or glass greenhouse cladding reduces incoming outdoor solar radiation by 30% to 40% through reflection, structural shading, and dirt accumulation."}
        ],
        "js_logic": """
          const nat = getNum('natural_sunlight_dli');
          const target = getNum('target_crop_dli');
          const hrs = getNum('supplemental_photoperiod_hrs') || 16;

          const deficit = Math.max(0, target - nat);
          const totalSeconds = hrs * 3600;
          const ppfd = totalSeconds > 0 ? (deficit * 1000000) / totalSeconds : 0;
          const boostPct = nat > 0 ? (deficit / nat) * 100 : 0;

          setDisp('required_supplemental_ppfd', ppfd.toFixed(1) + ' μmol/m²/s');
          setDisp('dli_deficit_mol', deficit.toFixed(2) + ' mol/m²/d Needed');
          setDisp('total_delivered_dli', target.toFixed(1) + ' mol/m²/day');
          setDisp('crop_growth_rate_boost', '+' + boostPct.toFixed(1) + '% Yield Acceleration');
        """
    },
    {
        "slug": "pig-average-daily-gain",
        "category": "agriculture",
        "name": "Swine Nursery Feed Intake & Average Daily Gain (ADG) Calculator",
        "description": "Calculate Average Daily Gain (ADG), days to market weight (280 lbs), and total feed consumed for commercial swine grow-finish operations.",
        "hero_badge": "Swine Production • Growth Kinetics",
        "formula_display": "ADG (lbs/day) = (Final Weight - Placement Weight) / Days on Feed | Feed Intake = ADG × FCR",
        "fields": [
            {"id": "placement_feeder_pig_weight", "label": "Nursery Placement Weight (lbs)", "default": 50, "suffix": "lbs", "min": 12, "max": 90, "step": 5, "hint": "Piglet weight entering grower barn"},
            {"id": "target_slaughter_weight", "label": "Target Market Weight (lbs)", "default": 280, "suffix": "lbs", "min": 220, "max": 330, "step": 5, "hint": "Packing plant target liveweight"},
            {"id": "measured_adg_lbs_day", "label": "Average Daily Gain (ADG lbs/day)", "default": 1.95, "suffix": "lbs/day", "min": 1.2, "max": 2.5, "step": 0.05, "hint": "Typical grow-finish ADG = 1.80 - 2.10 lbs/day"},
            {"id": "swine_feed_conversion_ratio", "label": "Feed Conversion Ratio (FCR)", "default": 2.75, "min": 2.2, "max": 3.6, "step": 0.05, "hint": "Grow-finish FCR (typically 2.6 - 2.9)"}
        ],
        "metrics": [
            {"id": "days_to_market_weight", "label": "Days on Feed to Market", "default_display": "118 Days", "highlight": True},
            {"id": "total_feed_consumed_pig", "label": "Total Feed Eaten Per Pig", "default_display": "632.5 lbs Feed", "highlight": True},
            {"id": "feed_cost_per_market_hog", "label": "Feed Cost Per Finished Hog (@ $290/T)", "default_display": "$91.71 / pig"},
            {"id": "barn_annual_turnover", "label": "Annual Barn Group Turns", "default_display": "2.8 Turns / Year"}
        ],
        "proof_steps": [
            {"step_title": "Total Net Growth", "step_text": "Weight Gain = 280 lbs market - 50 lbs nursery = 230 lbs gained."},
            {"step_title": "Days on Feed Derivation", "step_text": "Days on Feed = Gain / ADG = 230 lbs / 1.95 lbs/day = 117.9 days (118 days)."},
            {"step_title": "Feed Consumption Mass", "step_text": "Total Feed = 230 lbs gain × 2.75 FCR = 632.5 lbs of corn-soy meal ration."},
            {"step_title": "Feed Budget Valuation", "step_text": "Feed Cost = (632.5 / 2,000) × $290/ton = $91.71 per pig."}
        ],
        "faqs": [
            {"q": "What is an industry standard ADG for market hogs?", "a": "Modern lean-genetics market pigs achieve Average Daily Gains of 1.85 to 2.15 pounds per day during the grow-finish phase, reaching 280 pounds in approximately 110 to 125 days after leaving the nursery."},
            {"q": "How does barn temperature impact swine ADG and FCR?", "a": "Hogs outside their thermal-neutral zone (65°F to 72°F) redirect dietary calories away from muscle accretion toward shivering to stay warm or panting to stay cool, deteriorating FCR by 10% to 15%."}
        ],
        "js_logic": """
          const start = getNum('placement_feeder_pig_weight');
          const finish = getNum('target_slaughter_weight');
          const adg = getNum('measured_adg_lbs_day') || 1.95;
          const fcr = getNum('swine_feed_conversion_ratio') || 2.75;

          const gain = Math.max(1, finish - start);
          const days = adg > 0 ? (gain / adg) : 120;
          const totalFeed = gain * fcr;
          const feedCost = (totalFeed / 2000) * 290;
          const turns = 365 / (days + 10);

          setDisp('days_to_market_weight', Math.round(days) + ' Days');
          setDisp('total_feed_consumed_pig', totalFeed.toFixed(1) + ' lbs Feed');
          setDisp('feed_cost_per_market_hog', '$' + feedCost.toFixed(2) + ' / pig');
          setDisp('barn_annual_turnover', turns.toFixed(1) + ' Turns / Year');
        """
    },
    {
        "slug": "broiler-flock-epef-efficiency",
        "category": "agriculture",
        "name": "Poultry Broiler Flock European Production Efficiency Factor (EPEF) Calculator",
        "description": "Calculate EPEF (European Production Efficiency Factor / EPI) index from liveability, market body weight, flock age, and feed conversion ratio (FCR).",
        "hero_badge": "Poultry Science • Broiler Performance",
        "formula_display": "EPEF = (Liveability % × Average Live Weight in kg) / (Age in Days × FCR) × 100",
        "fields": [
            {"id": "flock_liveability_pct", "label": "Flock Liveability (%)", "default": 96.5, "suffix": "%", "min": 85, "max": 99.5, "step": 0.5, "hint": "100% minus total flock mortality (e.g. 3.5% mortality = 96.5% liveability)"},
            {"id": "market_live_weight_lbs", "label": "Average Liveweight at Processing (lbs)", "default": 6.20, "suffix": "lbs/bird", "min": 3.5, "max": 10.0, "step": 0.1, "hint": "Flock average weight at slaughter"},
            {"id": "slaughter_age_days", "label": "Flock Age at Slaughter (Days)", "default": 42, "suffix": "days", "min": 30, "max": 65, "step": 1, "hint": "Calendar days from chick placement to processing"},
            {"id": "flock_feed_conversion_ratio", "label": "Flock Feed Conversion Ratio (FCR)", "default": 1.68, "min": 1.35, "max": 2.20, "step": 0.02, "hint": "Total flock feed consumed / total liveweight"}
        ],
        "metrics": [
            {"id": "calculated_epef_score", "label": "European Production Efficiency Factor", "default_display": "385.0 EPEF", "highlight": True},
            {"id": "flock_performance_rating", "label": "Industry Benchmark Grade", "default_display": "Excellent Performance (> 380 EPEF)", "highlight": True},
            {"id": "live_weight_kg", "label": "Metric Average Bodyweight", "default_display": "2.81 kg / bird"},
            {"id": "daily_growth_rate_grams", "label": "Average Daily Gain (ADG)", "default_display": "66.9 grams / day"}
        ],
        "proof_steps": [
            {"step_title": "Metric Liveweight Conversion", "step_text": "Liveweight in kg = 6.20 lbs × 0.453592 = 2.812 kg."},
            {"step_title": "EPEF Standardized Equation", "step_text": "EPEF = (Liveability% × Bodyweight kg) / (Age in Days × FCR) × 100."},
            {"step_title": "Numerical Formulation", "step_text": "Numerator = 96.5 × 2.812 = 271.358. Denominator = 42 days × 1.68 FCR = 70.56. EPEF = (271.358 / 70.56) × 100 = 384.58."},
            {"step_title": "Benchmark Rating", "step_text": "An EPEF above 380 to 400 indicates elite biosecurity, superior genetics, and optimal environmental climate control."}
        ],
        "faqs": [
            {"q": "What is considered a good EPEF score in poultry production?", "a": "Below 300 is poor; 300 to 340 is average; 340 to 380 is good; above 380 to 420 represents top-tier commercial broiler performance."},
            {"q": "Why does EPEF combine growth rate, FCR, and mortality into one number?", "a": "Because evaluating FCR alone is misleading if achieved by high mortality culling, and rapid growth is unprofitable if feed efficiency is terrible. EPEF synthesizes all key biological profit drivers into a single comparable index."}
        ],
        "js_logic": """
          const live = (getNum('flock_liveability_pct') || 96.5);
          const wtLbs = getNum('market_live_weight_lbs');
          const days = getNum('slaughter_age_days') || 42;
          const fcr = getNum('flock_feed_conversion_ratio') || 1.68;

          const wtKg = wtLbs * 0.453592;
          const denom = days * fcr;
          const epef = denom > 0 ? (live * wtKg) / denom * 100 : 0;
          const adgGrams = (wtKg * 1000) / days;

          let grade = 'Good Standard Performance';
          if (epef >= 400) grade = 'Elite World-Class (> 400 EPEF)';
          else if (epef >= 360) grade = 'Excellent Performance (360-400)';
          else if (epef < 320) grade = 'Below Average (< 320 EPEF)';

          setDisp('calculated_epef_score', epef.toFixed(1) + ' EPEF');
          setDisp('flock_performance_rating', grade);
          setDisp('live_weight_kg', wtKg.toFixed(2) + ' kg / bird');
          setDisp('daily_growth_rate_grams', adgGrams.toFixed(1) + ' g / day');
        """
    },
    {
        "slug": "silage-bunker-density",
        "category": "agriculture",
        "name": "Silage Bunker Trench Dry Matter Density & Packing Loss Calculator",
        "description": "Calculate packing tractor weight requirements, dry matter packing density (lbs DM/cu ft), and fermentation spoilage loss in bunker and drive-over silage piles.",
        "hero_badge": "Forage Preservation • Silage Compaction",
        "formula_display": "Required Packing Tractor Weight (lbs) = Silage Delivery Rate (Tons/hr) × 800",
        "fields": [
            {"id": "silage_inbound_delivery_tons_hr", "label": "Silage Harvest Delivery Rate (Tons/Hour)", "default": 75, "suffix": "tons/hr", "min": 20, "max": 350, "step": 5, "hint": "Hourly chop tonnage delivered from field by silage trucks"},
            {"id": "silage_moisture_pct", "label": "Chopped Forage Moisture Content (%)", "default": 65, "suffix": "%", "min": 55, "max": 75, "step": 1, "hint": "Optimal corn silage moisture is 63% to 68%"},
            {"id": "packing_tractor_weight_lbs", "label": "Total Packing Tractor Fleet Weight (lbs)", "default": 65000, "suffix": "lbs", "min": 15000, "max": 200000, "step": 5000, "hint": "Combined weight of all packing tractors on the pile"}
        ],
        "metrics": [
            {"id": "dry_matter_density_lbs_cuft", "label": "Estimated Dry Matter Density", "default_display": "15.2 lbs DM / cu ft", "highlight": True},
            {"id": "recommended_tractor_weight", "label": "Recommended Packing Tractor Weight", "default_display": "60,000 lbs (800x Rule)", "highlight": True},
            {"id": "estimated_spoilage_loss_pct", "label": "Dry Matter Shrink / Spoilage Loss", "default_display": "12.8% Fermentation Loss", "highlight": True},
            {"id": "packing_time_per_ton", "label": "Packing Effort Index", "default_display": "Optimal Compaction Ratio"}
        ],
        "proof_steps": [
            {"step_title": "The 800-Pound Packing Rule", "step_text": "University of Wisconsin rule: Minimum Tractor Weight = Delivery Tons/Hour × 800. For 75 tons/hour: 75 × 800 = 60,000 lbs of tractor weight required on the pile."},
            {"step_title": "Dry Matter Density Achievement", "step_text": "With 65,000 lbs tractor weight packing 6-inch thin layers: Achieves ~15.2 lbs Dry Matter per cubic foot (43.4 lbs wet density)."},
            {"step_title": "Oxygen Exclusion & Spoilage Mitigation", "step_text": "High density (>14 lbs DM/cu ft) rapidly creates anaerobic conditions, dropping dry matter fermentation loss from 20%+ down to 12.8%."}
        ],
        "faqs": [
            {"q": "Why is silage bunker packing density so critical?", "a": "High packing density excludes trapped oxygen, allowing lactic acid bacteria to rapidly drop silage pH below 4.0, which prevents yeast and mold spoilage and preserves protein nutrients."},
            {"q": "What is the recommended packing layer thickness?", "a": "Silage should be pushed up in thin layers of no more than 4 to 6 inches before each pass of the packing tractor. Dumping 12-inch or thicker piles prevents effective compaction regardless of tractor weight."}
        ],
        "js_logic": """
          const tonsHr = getNum('silage_inbound_delivery_tons_hr');
          const moist = (getNum('silage_moisture_pct') || 65) / 100;
          const tractorWt = getNum('packing_tractor_weight_lbs');

          const dm = 1 - moist;
          const reqTractor = tonsHr * 800;
          const ratio = reqTractor > 0 ? (tractorWt / reqTractor) : 1.0;
          const densityDm = Math.min(18.5, Math.max(10.0, 14.5 * Math.pow(ratio, 0.4)));
          const shrinkLoss = Math.max(8.0, 26.0 - (densityDm * 0.85));

          setDisp('dry_matter_density_lbs_cuft', densityDm.toFixed(1) + ' lbs DM / cu ft');
          setDisp('recommended_tractor_weight', Math.round(reqTractor).toLocaleString() + ' lbs (800x Rule)');
          setDisp('estimated_spoilage_loss_pct', shrinkLoss.toFixed(1) + '% Fermentation Loss');
          setDisp('packing_time_per_ton', ratio >= 1.0 ? 'Optimal Compaction Ratio' : 'Under-Packed (Add Tractor Ballast)');
        """
    },
    {
        "slug": "manure-nutrient-fertilizer-credit",
        "category": "agriculture",
        "name": "Livestock Manure N-P-K Nutrient Fertilizer Value Credit Per Ton",
        "description": "Calculate commercial N-P-K fertilizer dollar replacement value per ton or 1,000 gallons for dairy, beef, swine, and poultry broiler litter manure.",
        "hero_badge": "Nutrient Economics • Manure Valuation",
        "formula_display": "Fertilizer Value ($/Ton) = (Available N × $0.55) + (P₂O₅ × $0.62) + (K₂O × $0.48)",
        "fields": [
            {"id": "manure_source_type", "label": "Manure Type (1 = Dairy Slurry, 2 = Beef Feedlot Solid, 3 = Swine Pit, 4 = Poultry Litter)", "default": 4, "min": 1, "max": 4, "step": 1, "hint": "1: Dairy (gal), 2: Beef solid (ton), 3: Swine liquid (gal), 4: Poultry litter (ton)"},
            {"id": "annual_application_rate", "label": "Application Rate (Tons or 1,000 Gallons / Acre)", "default": 2.5, "suffix": "tons/ac (or kGal)", "min": 1.0, "max": 15.0, "step": 0.5, "hint": "Typical poultry litter = 2-3 tons/ac, liquid dairy = 6-10 kGal/ac"},
            {"id": "nitrogen_price_per_lb", "label": "Commercial Nitrogen Value ($/lb N)", "default": 0.58, "prefix": "$", "min": 0.30, "max": 1.20, "step": 0.02, "hint": "Urea / UAN commercial benchmark price"},
            {"id": "phosphate_price_per_lb", "label": "Commercial Phosphate Value ($/lb P₂O₅)", "default": 0.65, "prefix": "$", "min": 0.30, "max": 1.20, "step": 0.02, "hint": "DAP commercial benchmark price"}
        ],
        "metrics": [
            {"id": "fertilizer_value_per_ton", "label": "Gross Fertilizer Value Per Ton / kGal", "default_display": "$67.85 / Ton", "highlight": True},
            {"id": "acre_fertilizer_savings", "label": "Total Fertilizer Savings Per Acre", "default_display": "$169.63 / Acre", "highlight": True},
            {"id": "available_nitrogen_delivered", "label": "First-Year Available Nitrogen", "default_display": "75.0 lbs N / Acre"},
            {"id": "soil_organic_matter_bonus", "label": "Soil Health & Carbon Bonus", "default_display": "+1.2 Tons Organic Matter"}
        ],
        "proof_steps": [
            {"step_title": "Nutrient Analysis Benchmarks", "step_text": "Poultry litter contains ~60 lbs N (50% first-year available = 30 lbs N), 55 lbs P₂O₅ (80% available = 44 lbs), and 45 lbs K₂O (100% available = 45 lbs) per ton."},
            {"step_title": "Dollar Value per Ton Formulation", "step_text": "Value = (30 lbs N × $0.58) + (44 lbs P₂O₅ × $0.65) + (45 lbs K₂O × $0.48) = $17.40 + $28.60 + $21.60 = $67.60/ton."},
            {"step_title": "Field Scale Savings", "step_text": "At 2.5 tons/acre: Savings = 2.5 × $67.60 = $169.00/acre in commercial fertilizer purchases eliminated."}
        ],
        "faqs": [
            {"q": "Why is only 30% to 50% of manure Nitrogen available in the first year?", "a": "Much of the nitrogen in solid manure is bound in complex organic matter and requires microbial mineralization over several seasons before becoming plant-available nitrate/ammonium."},
            {"q": "How does incorporation timing affect manure nitrogen loss?", "a": "Surface-applied liquid manure loses up to 50% of its ammonium nitrogen through ammonia volatilization into the atmosphere within 24 to 48 hours unless incorporated with a disk or injected directly into the soil."}
        ],
        "js_logic": """
          const type = Math.round(getNum('manure_source_type')) || 4;
          const rateAc = getNum('annual_application_rate');
          const pN = getNum('nitrogen_price_per_lb');
          const pP = getNum('phosphate_price_per_lb');
          const pK = 0.48;

          let availN = 30;
          let availP = 44;
          let availK = 45;
          let unitLabel = ' / Ton';

          if (type === 1) { // Dairy liquid (per 1,000 gal)
            availN = 12; availP = 10; availK = 22; unitLabel = ' / 1,000 Gal';
          } else if (type === 2) { // Beef solid (per ton)
            availN = 14; availP = 18; availK = 20; unitLabel = ' / Ton';
          } else if (type === 3) { // Swine pit (per 1,000 gal)
            availN = 35; availP = 22; availK = 25; unitLabel = ' / 1,000 Gal';
          }

          const valPerUnit = (availN * pN) + (availP * pP) + (availK * pK);
          const perAcreSavings = valPerUnit * rateAc;
          const totalN = availN * rateAc;

          setDisp('fertilizer_value_per_ton', '$' + valPerUnit.toFixed(2) + unitLabel);
          setDisp('acre_fertilizer_savings', '$' + perAcreSavings.toFixed(2) + ' / Acre');
          setDisp('available_nitrogen_delivered', totalN.toFixed(1) + ' lbs N / Acre');
          setDisp('soil_organic_matter_bonus', '+1.2 Tons Organic Matter');
        """
    },
    {
        "slug": "tractor-fuel-consumption-pto",
        "category": "agriculture",
        "name": "Farm Tractor Diesel Fuel Consumption Per Acre (PTO Horsepower) Calculator",
        "description": "Calculate hourly and per-acre diesel fuel consumption for tractors based on Nebraska Tractor Test Laboratory PTO horsepower benchmarks.",
        "hero_badge": "Machinery Economics • Field Efficiency",
        "formula_display": "Fuel Burn (gal/hr) ≈ 0.044 × Rated PTO Horsepower (at 75% typical field load)",
        "fields": [
            {"id": "pto_horsepower_rating", "label": "Tractor Rated PTO Horsepower (HP)", "default": 240, "suffix": "HP", "min": 40, "max": 650, "step": 10, "hint": "Manufacturer Nebraska Test PTO rating"},
            {"id": "field_speed_mph", "label": "Field Working Speed (mph)", "default": 5.5, "suffix": "mph", "min": 2.5, "max": 12.0, "step": 0.5, "hint": "Tillage: 4.5-5.5 mph; Planting: 5.5-6.5 mph; Spraying: 10-14 mph"},
            {"id": "implement_width_feet", "label": "Implement Width (Feet)", "default": 30, "suffix": "ft", "min": 8, "max": 90, "step": 2, "hint": "Working width of disk, chisel plow, or planter"},
            {"id": "diesel_price_per_gal", "label": "Off-Road Farm Diesel Price ($/gal)", "default": 3.45, "prefix": "$", "min": 1.5, "max": 6.5, "step": 0.05, "hint": "Dyed off-road non-taxed diesel price"}
        ],
        "metrics": [
            {"id": "fuel_burn_per_acre", "label": "Diesel Fuel Burn Per Acre", "default_display": "0.65 gal / acre", "highlight": True},
            {"id": "hourly_fuel_burn_rate", "label": "Hourly Fuel Consumption Rate", "default_display": "10.6 gal / hour", "highlight": True},
            {"id": "field_capacity_acres_hr", "label": "Field Work Rate Capacity", "default_display": "16.4 Acres / Hour"},
            {"id": "fuel_cost_per_acre", "label": "Diesel Fuel Cost Per Acre", "default_display": "$2.24 / Acre"}
        ],
        "proof_steps": [
            {"step_title": "Nebraska Tractor Test Empirical Formula", "step_text": "Average specific fuel consumption at 75% load = 0.044 gal/hr per PTO HP. For a 240 HP tractor: 240 × 0.044 = 10.56 gallons/hour."},
            {"step_title": "Field Working Capacity Formulation", "step_text": "Capacity (Acres/hr) = (Speed mph × Width ft × 82% field efficiency) / 8.25 = (5.5 × 30 × 0.82) / 8.25 = 16.4 acres/hour."},
            {"step_title": "Per-Acre Fuel Consumption", "step_text": "Fuel per Acre = 10.56 gal/hr / 16.4 acres/hr = 0.644 gallons/acre."},
            {"step_title": "Economic Field Cost", "step_text": "Cost per Acre = 0.644 gal/ac × $3.45/gal = $2.22 per acre."}
        ],
        "faqs": [
            {"q": "What is 'Gear Up and Throttle Down' (GUTD)?", "a": "GUTD is a fuel-saving technique for light to moderate tractor loads where the operator shifts into a higher gear and throttles back engine RPM to maintain the same ground speed, saving 15% to 25% on diesel fuel."},
            {"q": "Why is off-road dyed diesel cheaper than highway diesel?", "a": "Dyed off-road diesel is exempt from federal and state highway road excise taxes (~$0.40 to $0.65/gallon) because farm tractors and combines operate on private farmland rather than public paved roads."}
        ],
        "js_logic": """
          const hp = getNum('pto_horsepower_rating');
          const speed = getNum('field_speed_mph');
          const width = getNum('implement_width_feet');
          const price = getNum('diesel_price_per_gal');

          const galHr = hp * 0.044;
          const acresHr = (speed * width * 0.82) / 8.25;
          const galAcre = acresHr > 0 ? (galHr / acresHr) : 0;
          const costAcre = galAcre * price;

          setDisp('fuel_burn_per_acre', galAcre.toFixed(2) + ' gal / acre');
          setDisp('hourly_fuel_burn_rate', galHr.toFixed(1) + ' gal / hour');
          setDisp('field_capacity_acres_hr', acresHr.toFixed(1) + ' Acres / Hour');
          setDisp('fuel_cost_per_acre', '$' + costAcre.toFixed(2) + ' / Acre');
        """
    },
    {
        "slug": "pasture-weed-herbicide-coverage",
        "category": "agriculture",
        "name": "Pasture Weed Eradication Herbicide Rate & Boom Sprayer Calibration",
        "description": "Calculate nozzle flow rate (GPM), sprayer speed, and herbicide coverage per acre for pasture thistle, briar, and invasive weed management.",
        "hero_badge": "Rangeland Management • Weed Control",
        "formula_display": "Nozzle GPM = (GPA × Speed in mph × Nozzle Spacing in inches) / 5,940",
        "fields": [
            {"id": "target_spray_gpa", "label": "Target Spray Volume (Gallons Per Acre)", "default": 20.0, "suffix": "GPA", "min": 10, "max": 40, "step": 1, "hint": "Pasture foliar herbicides require 15-25 GPA for thorough foliage coverage"},
            {"id": "sprayer_tractor_speed_mph", "label": "Spraying Ground Speed (mph)", "default": 6.0, "suffix": "mph", "min": 3, "max": 12, "step": 0.5, "hint": "Typical rough pasture spraying speed"},
            {"id": "nozzle_spacing_inches", "label": "Boom Nozzle Spacing (Inches)", "default": 20, "suffix": "inches", "min": 15, "max": 30, "step": 5, "hint": "Distance between spray nozzles on boom (typically 20 inches)"}
        ],
        "metrics": [
            {"id": "required_nozzle_gpm", "label": "Required Nozzle Flow Rate", "default_display": "0.404 GPM / Nozzle", "highlight": True},
            {"id": "recommended_tip_size", "label": "ISO Standard Nozzle Tip Size", "default_display": "Red Tip (04 Size @ 40 PSI)", "highlight": True},
            {"id": "fluid_ounces_per_nozzle_min", "label": "Calibration Catch per Minute", "default_display": "51.7 fl oz / minute", "highlight": True},
            {"id": "total_boom_flow_rate", "label": "Total 30-ft Boom Flow (18 Nozzles)", "default_display": "7.27 GPM Pump Demand"}
        ],
        "proof_steps": [
            {"step_title": "Nozzle Flow Equation", "step_text": "GPM = (GPA × mph × W) / 5,940. GPM = (20 GPA × 6.0 mph × 20 inches) / 5,940 = 2,400 / 5,940 = 0.404 GPM per nozzle."},
            {"step_title": "Calibration Catch Jar Verification", "step_text": "Ounces per Minute = 0.404 GPM × 128 fl oz/gal = 51.7 fluid ounces caught in a measuring jar in 60 seconds at operating pressure."},
            {"step_title": "ISO Color-Coded Nozzle Selection", "step_text": "ISO 04 (Red nozzle) delivers exactly 0.40 GPM at 40 PSI, providing medium to coarse droplet spectrum to minimize drift."}
        ],
        "faqs": [
            {"q": "What is the 5,940 constant in sprayer calibration?", "a": "5,940 is the mathematical conversion constant derived from: (43,560 sq ft/acre × 12 inches/ft) / (5,280 ft/mile × 60 minutes/hour)."},
            {"q": "Why is high water carrier volume (20+ GPA) needed for pasture weeds?", "a": "Unlike row crops where small weeds are exposed, mature pasture weeds (thistles, blackberry briars, multiflora rose) have dense thickets requiring 20 to 25 GPA to penetrate the canopy and achieve thorough leaf contact."}
        ],
        "js_logic": """
          const gpa = getNum('target_spray_gpa') || 20;
          const mph = getNum('sprayer_tractor_speed_mph') || 6;
          const w = getNum('nozzle_spacing_inches') || 20;

          const gpm = (gpa * mph * w) / 5940;
          const ozMin = gpm * 128;
          const totalPump = gpm * 18;

          let tip = 'Blue Tip (03 Size)';
          if (gpm >= 0.45) tip = 'Brown Tip (05 Size)';
          else if (gpm >= 0.35) tip = 'Red Tip (04 Size @ 40 PSI)';
          else if (gpm >= 0.25) tip = 'Blue Tip (03 Size @ 40 PSI)';
          else tip = 'Yellow Tip (02 Size)';

          setDisp('required_nozzle_gpm', gpm.toFixed(3) + ' GPM / Nozzle');
          setDisp('recommended_tip_size', tip);
          setDisp('fluid_ounces_per_nozzle_min', ozMin.toFixed(1) + ' fl oz / minute');
          setDisp('total_boom_flow_rate', totalPump.toFixed(2) + ' GPM Pump Demand');
        """
    },
    {
        "slug": "beehive-honey-yield-feeding",
        "category": "agriculture",
        "name": "Beehive Honey Harvest Yield & Fall Sugar Syrup Feeding Calculator",
        "description": "Calculate harvestable honey surplus per hive (leaving 60 lbs for winter), 2:1 fall sugar syrup feeding requirements, and apiary economics.",
        "hero_badge": "Apiculture • Apiary Management",
        "formula_display": "Harvestable Honey = Total Stored Honey - Winter Hive Reserve Requirement (60 lbs in Northern climates)",
        "fields": [
            {"id": "total_honey_in_hive_lbs", "label": "Total Estimated Honey in Hive (lbs)", "default": 115, "suffix": "lbs", "min": 20, "max": 250, "step": 5, "hint": "Weight of honey frames in brood boxes and honey supers"},
            {"id": "winter_climate_zone", "label": "Winter Climate Zone (1 = Mild South, 2 = Central, 3 = Cold North)", "default": 2, "min": 1, "max": 3, "step": 1, "hint": "South: 40 lbs reserve; Central: 60 lbs; North/Canada: 85 lbs"},
            {"id": "honey_retail_price_lb", "label": "Raw Local Honey Retail Price ($/lb)", "default": 12.50, "prefix": "$", "min": 5, "max": 25, "step": 0.5, "hint": "Price per 1-lb jar of extracted artisanal honey"}
        ],
        "metrics": [
            {"id": "harvestable_surplus_lbs", "label": "Safe Harvestable Honey Surplus", "default_display": "55.0 lbs Honey", "highlight": True},
            {"id": "gross_honey_revenue", "label": "Gross Honey Revenue Per Hive", "default_display": "$687.50 / hive", "highlight": True},
            {"id": "honey_jars_yield_1lb", "label": "Extracted 1-lb Jars Produced", "default_display": "55 Jars (1-lb each)", "highlight": True},
            {"id": "winter_reserve_preserved", "label": "Colony Winter Survival Reserve", "default_display": "60.0 lbs Reserved for Bees"}
        ],
        "proof_steps": [
            {"step_title": "Winter Colony Survival Reserve", "step_text": "In Central temperate climates, a honey bee colony consumes ~60 lbs of honey to generate cluster heat through winter."},
            {"step_title": "Surplus Extraction Quantification", "step_text": "Surplus = Total Hive Honey (115 lbs) - Reserve Requirement (60 lbs) = 55.0 lbs safe to extract."},
            {"step_title": "Apiary Direct Revenue", "step_text": "55 lbs extracted honey packaged into 1-lb glass jars at $12.50/jar = $687.50 gross honey revenue per colony."}
        ],
        "faqs": [
            {"q": "What happens if a beekeeper harvests too much honey in the fall?", "a": "If bees run out of stored honey during mid-winter, the cluster will starve to death within 48 hours of freezing weather unless emergency dry sugar candy boards or fondant are placed on the top bars."},
            {"q": "What is 2:1 sugar syrup in fall beekeeping?", "a": "Fall supplemental feeding uses a thick 2-to-1 ratio of white granulated sugar to water (by weight). Because it has less water than 1:1 spring syrup, bees can cure and dehydrate it into winter honeycomb stores without chilling the hive."}
        ],
        "js_logic": """
          const totalHoney = getNum('total_honey_in_hive_lbs');
          const zone = Math.round(getNum('winter_climate_zone')) || 2;
          const price = getNum('honey_retail_price_lb');

          let reqReserve = 60;
          if (zone === 1) reqReserve = 40;
          else if (zone === 3) reqReserve = 85;

          const surplus = Math.max(0, totalHoney - reqReserve);
          const rev = surplus * price;

          setDisp('harvestable_surplus_lbs', surplus.toFixed(1) + ' lbs Honey');
          setDisp('gross_honey_revenue', '$' + rev.toFixed(2) + ' / hive');
          setDisp('honey_jars_yield_1lb', Math.round(surplus) + ' Jars (1-lb each)');
          setDisp('winter_reserve_preserved', reqReserve.toFixed(1) + ' lbs Reserved for Bees');
        """
    },
    {
        "slug": "aquaponics-biofilter-fish-plant",
        "category": "agriculture",
        "name": "Aquaponics Fish-to-Plant Biomass Ratio & Biofilter Media Sizing",
        "description": "Calculate daily fish feed rate, nitrogen biofilter surface area, and hydroponic plant bed grow area (UVI Rakocy aquaponics model).",
        "hero_badge": "Aquaculture • Controlled Systems",
        "formula_display": "Plant Area (m²) = Daily Fish Feed (grams) / Feeding Ratio (typically 60 - 100 g feed/m²/day)",
        "fields": [
            {"id": "fish_tank_volume_gal", "label": "Fish Tank Total Volume (Gallons)", "default": 500, "suffix": "gallons", "min": 50, "max": 10000, "step": 50, "hint": "Total fish culture tank water capacity"},
            {"id": "fish_stocking_density_lbs", "label": "Fish Standing Biomass (lbs)", "default": 125, "suffix": "lbs fish", "min": 10, "max": 2500, "step": 10, "hint": "Total fish weight in tank (typical density = 0.25 - 0.50 lb/gal)"},
            {"id": "daily_feeding_rate_pct", "label": "Daily Feeding Rate (% of Bodyweight)", "default": 1.5, "suffix": "%", "min": 0.5, "max": 4.0, "step": 0.25, "hint": "Feed rate for tilapia or catfish (typically 1.5% to 2.0%)"}
        ],
        "metrics": [
            {"id": "hydroponic_plant_area_sqft", "label": "Supported Hydroponic Plant Area", "default_display": "129.2 sq ft", "highlight": True},
            {"id": "daily_feed_rate_grams", "label": "Daily Fish Feed Input", "default_display": "850.5 grams / day", "highlight": True},
            {"id": "biofilter_media_volume", "label": "K1 / Moving Bed Biofilter Media Needed", "default_display": "6.8 cu ft Media"},
            {"id": "head_lettuce_harvest_wk", "label": "Weekly Lettuce Production Potential", "default_display": "45 Heads / Week"}
        ],
        "proof_steps": [
            {"step_title": "Daily Fish Feed Input", "step_text": "Feed = 125 lbs fish × 1.5% daily feed rate = 1.875 lbs feed = 850.5 grams of 32% protein fish pellets per day."},
            {"step_title": "UVI Feeding Rate Ratio", "step_text": "Dr. James Rakocy (University of the Virgin Islands) established that 60 to 80 grams of feed per day provides sufficient nitrogen and phosphorus to sustain 1 square meter of raft lettuce."},
            {"step_title": "Hydroponic Growing Area", "step_text": "Plant Area = 850.5 g / 70 g/m² = 12.15 m² = 130.8 sq ft of deep water culture (DWC) raft beds."},
            {"step_title": "Biofilter Nitrification Requirement", "step_text": "Nitrifying bacteria require ~1.0 m² of active surface area per gram of protein fed to oxidize toxic ammonia into plant-available nitrate."}
        ],
        "faqs": [
            {"q": "What is the primary cause of plant deficiencies in aquaponics?", "a": "Commercial fish feed lacks sufficient potassium, calcium, and iron for fruiting plants. Successful aquaponic growers supplement the system with chelated iron (Fe-DTPA), potassium hydroxide (KOH), and calcium carbonate to balance pH and nutrients."},
            {"q": "What is the optimal water pH for an aquaponic system?", "a": "6.8 to 7.0 is the sweet-spot compromise. Fish prefer 7.0-8.0, nitrifying bacteria thrive at 7.5-8.2, and plants absorb nutrients best at 5.8-6.5. Operating at 6.8 satisfies all three living organisms."}
        ],
        "js_logic": """
          const vol = getNum('fish_tank_volume_gal');
          const fishLbs = getNum('fish_stocking_density_lbs');
          const feedPct = (getNum('daily_feeding_rate_pct') || 1.5) / 100;

          const feedLbs = fishLbs * feedPct;
          const feedGrams = feedLbs * 453.592;
          const plantSqm = feedGrams / 70;
          const plantSqft = plantSqm * 10.7639;
          const bioMediaCuft = (feedGrams * 0.008);
          const lettuceHeads = Math.round(plantSqft * 0.35);

          setDisp('hydroponic_plant_area_sqft', plantSqft.toFixed(1) + ' sq ft');
          setDisp('daily_feed_rate_grams', feedGrams.toFixed(1) + ' g / day');
          setDisp('biofilter_media_volume', bioMediaCuft.toFixed(1) + ' cu ft Media');
          setDisp('head_lettuce_harvest_wk', lettuceHeads + ' Heads / Week');
        """
    },
    {
        "slug": "vineyard-grape-yield-wine",
        "category": "agriculture",
        "name": "Vineyard Grape Yield to Finished Wine Gallons & Bottles Calculator",
        "description": "Calculate harvest grape tonnage per acre, raw must press juice gallons, and finished 750ml bottles of wine produced per ton of grapes.",
        "hero_badge": "Viticulture & Enology • Wine Yield",
        "formula_display": "Wine Gallons = Grape Tons × Gallons per Ton (typically 150 - 170 gal/ton) | Bottles = Gallons × 5",
        "fields": [
            {"id": "vineyard_planted_acres", "label": "Vineyard Planted Acreage", "default": 5.0, "suffix": "acres", "min": 0.5, "max": 250, "step": 0.5, "hint": "Producing vineyard block acres"},
            {"id": "grape_yield_tons_per_acre", "label": "Grape Harvest Yield (Tons / Acre)", "default": 3.5, "suffix": "tons/acre", "min": 1.0, "max": 10.0, "step": 0.25, "hint": "Ultra-premium Pinot Noir ~2-3 tons; Cabernet ~3-4 tons; bulk ~6-8 tons"},
            {"id": "wine_extraction_gal_per_ton", "label": "Wine Extraction Rate (Gallons / Ton)", "default": 160, "suffix": "gal/ton", "min": 130, "max": 185, "step": 5, "hint": "Standard crush yield: 150-165 gal/ton finished wine"}
        ],
        "metrics": [
            {"id": "total_wine_bottles_750ml", "label": "Total Finished 750ml Bottles", "default_display": "14,140 Bottles", "highlight": True},
            {"id": "total_wine_cases_produced", "label": "Total Cases Produced (12-pack)", "default_display": "1,178 Cases", "highlight": True},
            {"id": "total_gallons_wine", "label": "Total Finished Wine Gallons", "default_display": "2,800 Gallons", "highlight": True},
            {"id": "total_grape_harvest_tons", "label": "Total Harvested Crop", "default_display": "17.5 Tons Grapes"}
        ],
        "proof_steps": [
            {"step_title": "Total Grape Harvest Tonnage", "step_text": "Harvest = 5.0 acres × 3.5 tons/acre = 17.5 tons of fresh harvested wine grapes."},
            {"step_title": "Crush & Press Extraction Volume", "step_text": "Finished Wine = 17.5 tons × 160 gallons/ton = 2,800 finished wine gallons."},
            {"step_title": "Commercial Bottling Equivalency", "step_text": "One standard 750ml wine bottle contains 0.1981 gallons (5.047 bottles per gallon). Total Bottles = 2,800 × 5.05 = 14,140 bottles (1,178 standard 12-bottle cases)."}
        ],
        "faqs": [
            {"q": "How many pounds of grapes are in one bottle of wine?", "a": "On average, one standard 750ml bottle of wine requires approximately 2.6 to 2.8 pounds (1.2 kg) of fresh harvested grapes, or roughly 600 to 800 individual grape berries."},
            {"q": "Why do high-end wineries intentionally reduce crop yield per acre?", "a": "Limiting yields (e.g. dropping green fruit clusters to maintain 2.5 tons/acre) forces the vine to concentrate sugars, polyphenols, tannins, and anthocyanin pigments into fewer grapes, creating dramatically superior wine complexity and ageability."}
        ],
        "js_logic": """
          const acres = getNum('vineyard_planted_acres');
          const tonsAc = getNum('grape_yield_tons_per_acre');
          const galTon = getNum('wine_extraction_gal_per_ton') || 160;

          const totalTons = acres * tonsAc;
          const totalGal = totalTons * galTon;
          const bottles = totalGal * 5.047;
          const cases = bottles / 12;

          setDisp('total_wine_bottles_750ml', Math.round(bottles).toLocaleString() + ' Bottles (750ml)');
          setDisp('total_wine_cases_produced', Math.round(cases).toLocaleString() + ' Cases (12-pack)');
          setDisp('total_gallons_wine', Math.round(totalGal).toLocaleString() + ' Gallons');
          setDisp('total_grape_harvest_tons', totalTons.toFixed(1) + ' Tons Grapes');
        """
    },
    {
        "slug": "farmland-cash-rent-equivalent",
        "category": "agriculture",
        "name": "Farmland Cash Rent Equivalent vs Crop Share Lease Calculator",
        "description": "Compare fixed cash rent per acre versus 50/50 and 60/40 crop-share lease economics, factoring commodity price volatility and input cost sharing.",
        "hero_badge": "Agricultural Real Estate • Farm Leases",
        "formula_display": "Crop Share Landowner Return = (Yield × Price × Landowner Share) - Landowner Shared Input Costs",
        "fields": [
            {"id": "expected_crop_yield_bu", "label": "Expected Crop Yield (Bushels / Acre)", "default": 205, "suffix": "bu/acre", "min": 50, "max": 300, "step": 5, "hint": "Average corn or soybean yield"},
            {"id": "expected_crop_price_usd", "label": "Expected Commodity Price ($/Bushel)", "default": 4.80, "prefix": "$", "min": 2.0, "max": 15.0, "step": 0.1, "hint": "Cash grain elevator forward contract price"},
            {"id": "landowner_crop_share_pct", "label": "Landowner Crop Share (%)", "default": 50, "suffix": "%", "min": 25, "max": 60, "step": 5, "hint": "Standard crop-share lease: 50/50 in Midwest, 1/3 in South"},
            {"id": "landowner_shared_costs_ac", "label": "Landowner Shared Input Costs ($/Acre)", "default": 220, "prefix": "$", "min": 0, "max": 500, "step": 10, "hint": "Landowner share of seed, fertilizer, and crop insurance in 50/50 lease"},
            {"id": "market_cash_rent_quote_ac", "label": "Offered Fixed Cash Rent ($/Acre)", "default": 265, "prefix": "$", "min": 50, "max": 500, "step": 5, "hint": "Fixed cash rent paid by tenant regardless of yield"}
        ],
        "metrics": [
            {"id": "crop_share_net_return_acre", "label": "Crop-Share Net Landowner Return", "default_display": "$272.00 / Acre", "highlight": True},
            {"id": "fixed_cash_rent_return_acre", "label": "Fixed Cash Rent Landowner Return", "default_display": "$265.00 / Acre", "highlight": True},
            {"id": "more_profitable_lease_option", "label": "Financial Advantage Strategy", "default_display": "Crop Share Earns +$7.00/ac More", "highlight": True},
            {"id": "crop_price_breakeven", "label": "Crop Price Parity Breakeven", "default_display": "$4.73 / Bushel Breakeven"}
        ],
        "proof_steps": [
            {"step_title": "Gross Revenue Calculation", "step_text": "Gross Field Revenue = 205 bushels × $4.80/bu = $984.00 per acre."},
            {"step_title": "Crop-Share Landowner Net Return", "step_text": "Gross Landowner Share (50%) = $984.00 × 0.50 = $492.00. Minus shared seed and fertilizer expenses ($220.00) = $272.00 net return per acre."},
            {"step_title": "Fixed Cash Rent Comparison", "step_text": "Fixed Cash Rent pays guaranteed $265.00/acre with zero commodity price risk and zero production risk. In this scenario, crop-share yields a slight premium ($7.00/ac) in exchange for taking on weather risk."}
        ],
        "faqs": [
            {"q": "What is the key difference between Cash Rent and Crop Share leases?", "a": "Under Cash Rent, the tenant farmer pays a fixed dollar amount per acre and bears 100% of the yield and price risk. Under Crop Share, landowner and tenant split the grain proceeds and crop input costs (typically 50/50), sharing both profits and risks."},
            {"q": "What is a Flexible Cash Lease?", "a": "A flexible cash lease combines both structures: the landowner receives a guaranteed minimum base rent (e.g. $200/ac) plus a percentage bonus if crop yields or commodity market prices exceed agreed target benchmarks."}
        ],
        "js_logic": """
          const yieldBu = getNum('expected_crop_yield_bu');
          const price = getNum('expected_crop_price_usd');
          const sharePct = (getNum('landowner_crop_share_pct') || 50) / 100;
          const costs = getNum('landowner_shared_costs_ac');
          const cashRent = getNum('market_cash_rent_quote_ac');

          const grossRev = yieldBu * price;
          const shareNet = (grossRev * sharePct) - costs;
          const delta = shareNet - cashRent;

          const breakevenPrice = yieldBu > 0 ? (cashRent + costs) / (yieldBu * sharePct) : 0;
          const winner = delta >= 0 ? 'Crop Share Earns +$' + Math.round(delta) + '/ac More' : 'Cash Rent Earns +$' + Math.round(Math.abs(delta)) + '/ac More';

          setDisp('crop_share_net_return_acre', '$' + Math.round(shareNet).toLocaleString() + ' / Acre');
          setDisp('fixed_cash_rent_return_acre', '$' + Math.round(cashRent).toLocaleString() + ' / Acre');
          setDisp('more_profitable_lease_option', winner);
          setDisp('crop_price_breakeven', '$' + breakevenPrice.toFixed(2) + ' / Bushel Breakeven');
        """
    }
]
