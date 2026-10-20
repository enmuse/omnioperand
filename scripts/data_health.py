"""
scripts/data_health.py
25 High-Value Health, Fitness, Bio-Quant & Physiological Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

HEALTH_CALCULATORS = [
    {
        "slug": "bmr",
        "category": "health",
        "name": "Basal Metabolic Rate (BMR) Calculator",
        "description": "Calculate daily basal calories burned at rest using the clinically validated Mifflin-St Jeor and Harris-Benedict equations.",
        "hero_badge": "Bio-Quant • Metabolic Invariants",
        "formula_display": "BMR (men) = 10W + 6.25H - 5A + 5 | BMR (women) = 10W + 6.25H - 5A - 161",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 175, "suffix": "lbs", "min": 70, "max": 500, "step": 1, "hint": "Current body weight in pounds"},
            {"id": "height_in", "label": "Height", "default": 70, "suffix": "in", "min": 48, "max": 90, "step": 1, "hint": "Height in inches (e.g. 5'10\" = 70 in)"},
            {"id": "age_years", "label": "Age", "default": 32, "suffix": "yrs", "min": 15, "max": 100, "step": 1, "hint": "Age in years"},
            {"id": "gender_factor", "label": "Biological Sex (1 for Male, 0 for Female)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 for Male (+5), 0 for Female (-161)"}
        ],
        "metrics": [
            {"id": "bmr_calories", "label": "Basal Metabolic Rate", "default_display": "1,774 kcal/day", "highlight": True},
            {"id": "sedentary_burn", "label": "Sedentary TDEE (1.2×)", "default_display": "2,129 kcal/day"},
            {"id": "hourly_burn", "label": "Resting Hourly Burn", "default_display": "73.9 kcal/hr"},
            {"id": "harris_benedict", "label": "Harris-Benedict Equivalent", "default_display": "1,812 kcal/day"}
        ],
        "proof_steps": [
            {"step_title": "Metric Mass and Stature Normalization", "step_text": "Convert imperial measurements to SI units: Mass W_kg = Weight (lbs) / 2.20462. Stature H_cm = Height (in) × 2.54."},
            {"step_title": "Mifflin-St Jeor Metabolic Derivation", "step_text": "The Mifflin-St Jeor equation: BMR = (10 × W_kg) + (6.25 × H_cm) - (5 × Age) + s, where sex constant s = +5 for biological males and -161 for biological females."},
            {"step_title": "Clinical Validity", "step_text": "Extensive meta-analyses show the Mifflin-St Jeor formulation predicts resting metabolic expenditure within 10% of indirect calorimetry for over 82% of healthy non-obese adults."}
        ],
        "faqs": [
            {"q": "What is the difference between BMR and TDEE?", "a": "BMR (Basal Metabolic Rate) is the minimum energy required to sustain vital autonomic organ functions (brain, heart, kidneys, lungs) in a complete resting state. TDEE includes BMR plus physical movement and food digestion."},
            {"q": "Does muscle mass increase BMR?", "a": "Yes. Skeletal muscle tissue is metabolically active, burning approximately 6 kcal per pound per day at rest, compared to adipose fat tissue which burns approximately 2 kcal per pound per day."}
        ],
        "js_logic": """
          const wLbs = getNum('weight_lbs');
          const hIn = getNum('height_in');
          const age = getNum('age_years');
          const isMale = getNum('gender_factor') === 1;

          const wKg = wLbs / 2.20462;
          const hCm = hIn * 2.54;
          const s = isMale ? 5 : -161;
          const bmr = (10 * wKg) + (6.25 * hCm) - (5 * age) + s;
          const sed = bmr * 1.2;
          const hr = bmr / 24;

          const hb = isMale ? 
            (66.5 + (13.75 * wKg) + (5.003 * hCm) - (6.75 * age)) :
            (655.1 + (9.563 * wKg) + (1.850 * hCm) - (4.676 * age));

          setDisp('bmr_calories', Math.round(bmr).toLocaleString() + ' kcal/day');
          setDisp('sedentary_burn', Math.round(sed).toLocaleString() + ' kcal/day');
          setDisp('hourly_burn', hr.toFixed(1) + ' kcal/hr');
          setDisp('harris_benedict', Math.round(hb).toLocaleString() + ' kcal/day');
        """
    },
    {
        "slug": "tdee",
        "category": "health",
        "name": "Total Daily Energy Expenditure (TDEE) Calculator",
        "description": "Calculate total daily calorie expenditure based on BMR and physical activity level for bulking, cutting, or weight maintenance.",
        "hero_badge": "Thermodynamics • Energy Expenditure Solver",
        "formula_display": "TDEE = BMR × Physical Activity Level (PAL) Multiplier",
        "fields": [
            {"id": "bmr_input", "label": "Basal Metabolic Rate (BMR)", "default": 1775, "suffix": "kcal", "min": 800, "max": 4000, "step": 25, "hint": "Your resting daily calorie burn"},
            {"id": "activity_level", "label": "Activity Tier (1.2 Sedentary to 1.9 Athlete)", "default": 1.55, "min": 1.2, "max": 1.9, "step": 0.05, "hint": "1.2: Desk job, 1.375: Light (1-3 d/wk), 1.55: Moderate (3-5 d/wk), 1.725: Heavy"}
        ],
        "metrics": [
            {"id": "maintenance_calories", "label": "Maintenance Calories (TDEE)", "default_display": "2,751 kcal/day", "highlight": True},
            {"id": "mild_cut", "label": "Fat Loss Deficit (-500 kcal)", "default_display": "2,251 kcal/day"},
            {"id": "lean_bulk", "label": "Lean Hypertrophy (+300 kcal)", "default_display": "3,051 kcal/day"},
            {"id": "weekly_burn", "label": "Weekly Energy Expenditure", "default_display": "19,257 kcal/wk"}
        ],
        "proof_steps": [
            {"step_title": "Thermodynamic Energy Balance", "step_text": "TDEE encompasses three major components: BMR (~60-70%), Thermic Effect of Food TEF (~10%), and Physical Activity Expenditure (~20-30%)."},
            {"step_title": "PAL Standardized Multipliers", "step_text": "Sedentary = BMR × 1.20; Lightly Active = BMR × 1.375; Moderately Active = BMR × 1.55; Very Active = BMR × 1.725; Extremely Active = BMR × 1.90."},
            {"step_title": "Adipose Caloric Equivalence", "step_text": "One pound of human adipose tissue stores approximately 3,500 kcal of chemical energy. A sustained daily deficit of 500 kcal produces exactly 1 lb of fat loss per week."}
        ],
        "faqs": [
            {"q": "Which activity level should I select?", "a": "Most desk workers who exercise 3 to 4 days per week fall into the 'Moderately Active' (1.55) bracket. When in doubt, select one tier lower to prevent overestimating energy burn."},
            {"q": "What happens if I eat below my BMR?", "a": "Occasional dips are harmless, but chronically consuming fewer calories than your BMR can cause hormonal downregulation (leptin, thyroid T3), muscle wasting, and lethargy."}
        ],
        "js_logic": """
          const bmr = getNum('bmr_input');
          const pal = getNum('activity_level') || 1.55;

          const tdee = bmr * pal;
          const cut = Math.max(1200, tdee - 500);
          const bulk = tdee + 300;
          const weekly = tdee * 7;

          setDisp('maintenance_calories', Math.round(tdee).toLocaleString() + ' kcal/day');
          setDisp('mild_cut', Math.round(cut).toLocaleString() + ' kcal/day');
          setDisp('lean_bulk', Math.round(bulk).toLocaleString() + ' kcal/day');
          setDisp('weekly_burn', Math.round(weekly).toLocaleString() + ' kcal/wk');
        """
    },
    {
        "slug": "bmi",
        "category": "health",
        "name": "Body Mass Index (BMI) & Weight Category Calculator",
        "description": "Calculate BMI, prime BMI, and healthy weight range classifications based on World Health Organization (WHO) and CDC criteria.",
        "hero_badge": "Anthropometry • WHO BMI Invariants",
        "formula_display": "BMI = [Weight (lbs) / Height (in)²] × 703",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 170, "suffix": "lbs", "min": 60, "max": 500, "step": 1, "hint": "Current body weight"},
            {"id": "height_in", "label": "Height", "default": 69, "suffix": "in", "min": 48, "max": 90, "step": 1, "hint": "Height in inches (5'9\" = 69 in)"}
        ],
        "metrics": [
            {"id": "bmi_score", "label": "Body Mass Index (BMI)", "default_display": "25.1 kg/m²", "highlight": True},
            {"id": "cdc_category", "label": "CDC Classification", "default_display": "Overweight (25.0 - 29.9)"},
            {"id": "healthy_range", "label": "Normal Weight Range (18.5 - 24.9)", "default_display": "125.3 - 168.7 lbs"},
            {"id": "bmi_prime", "label": "BMI Prime Ratio (BMI / 25.0)", "default_display": "1.00"}
        ],
        "proof_steps": [
            {"step_title": "Quetelet Index Derivation", "step_text": "BMI was formulated in 1832 by Adolphe Quetelet: BMI = Mass (kg) / Height (m)². In imperial units: BMI = [Weight (lbs) / Height (in)²] × 703.0695."},
            {"step_title": "WHO Diagnostic Cutoffs", "step_text": "Underweight: < 18.5; Normal: 18.5–24.9; Overweight: 25.0–29.9; Class I Obesity: 30.0–34.9; Class II: 35.0–39.9; Class III: ≥ 40.0."},
            {"step_title": "BMI Prime Normalization", "step_text": "BMI Prime = BMI / 25.0. An individual with BMI Prime < 1.0 is within the non-overweight spectrum."}
        ],
        "faqs": [
            {"q": "Why is BMI inaccurate for muscular athletes and bodybuilders?", "a": "BMI does not distinguish between skeletal muscle mass and adipose fat tissue. Muscular athletes often have high BMI scores that falsely categorize them as overweight or obese despite low body fat percentages."},
            {"q": "What is a healthy BMI for adults?", "a": "For adults 20 and older, a BMI between 18.5 and 24.9 is categorized as normal or healthy by the CDC and World Health Organization."}
        ],
        "js_logic": """
          const W = getNum('weight_lbs');
          const H = getNum('height_in');

          const bmi = (W / Math.pow(H, 2)) * 703.0695;
          const prime = bmi / 25.0;
          const minW = (18.5 * Math.pow(H, 2)) / 703.0695;
          const maxW = (24.9 * Math.pow(H, 2)) / 703.0695;

          let cat = 'Normal Weight';
          if (bmi < 18.5) cat = 'Underweight (< 18.5)';
          else if (bmi < 25.0) cat = 'Normal Weight (18.5 - 24.9)';
          else if (bmi < 30.0) cat = 'Overweight (25.0 - 29.9)';
          else if (bmi < 35.0) cat = 'Class I Obesity (30.0 - 34.9)';
          else cat = 'Class II+ Obesity (≥ 35.0)';

          setDisp('bmi_score', bmi.toFixed(1) + ' kg/m²');
          setDisp('cdc_category', cat);
          setDisp('healthy_range', minW.toFixed(1) + ' - ' + maxW.toFixed(1) + ' lbs');
          setDisp('bmi_prime', prime.toFixed(2));
        """
    },
    {
        "slug": "body-fat",
        "category": "health",
        "name": "US Navy Body Fat Percentage Calculator",
        "description": "Calculate body fat percentage and fat-free lean mass using the official Department of Defense US Navy circumference equations.",
        "hero_badge": "Body Composition • US Navy Circumference Method",
        "formula_display": "BF% (men) = 86.010 · log10(Waist - Neck) - 70.041 · log10(Height) + 36.76",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 180, "suffix": "lbs", "min": 80, "max": 500, "step": 1, "hint": "Current scale weight"},
            {"id": "height_in", "label": "Height", "default": 70, "suffix": "in", "min": 48, "max": 90, "step": 0.5, "hint": "Height without shoes"},
            {"id": "neck_in", "label": "Neck Circumference", "default": 15.5, "suffix": "in", "min": 10, "max": 25, "step": 0.25, "hint": "Circumference below Adam's apple"},
            {"id": "waist_in", "label": "Abdominal Waist Circumference", "default": 34, "suffix": "in", "min": 20, "max": 60, "step": 0.25, "hint": "Horizontal circumference at navel"}
        ],
        "metrics": [
            {"id": "body_fat_pct", "label": "Body Fat Percentage", "default_display": "17.4%", "highlight": True},
            {"id": "fat_mass", "label": "Adipose Fat Mass", "default_display": "31.3 lbs"},
            {"id": "lean_mass", "label": "Fat-Free Lean Mass", "default_display": "148.7 lbs"},
            {"id": "fitness_category", "label": "Fitness Classification", "default_display": "Fitness Tier (14 - 17%)"}
        ],
        "proof_steps": [
            {"step_title": "Logarithmic Circumference Model", "step_text": "The US Navy equation correlates abdominal adiposity against upper neck circumference: BF% = 86.010 · log10(Waist - Neck) - 70.041 · log10(Height) + 36.76."},
            {"step_title": "Two-Compartment Mass Partitioning", "step_text": "Fat Mass (lbs) = Weight × (BF% / 100). Fat-Free Mass (FFM) = Weight - Fat Mass."},
            {"step_title": "Military Standards Invariant", "step_text": "US Department of Defense standard DoD 1308.3 validates this circumference approach within 3% to 4% of dual-energy X-ray absorptiometry (DEXA) scans."}
        ],
        "faqs": [
            {"q": "How accurate is the US Navy body fat formula?", "a": "When tape measurements are taken precisely with a non-stretchable tension tape at horizontal planes, the US Navy formula has a strong correlation coefficient (r > 0.90) with DEXA hydrostatic weighing."},
            {"q": "What is considered an athletic body fat percentage for men and women?", "a": "For men, athletic body fat is typically 8% to 13%, with general fitness at 14% to 17%. For women, athletic body fat is 14% to 20%, with general fitness at 21% to 24%."}
        ],
        "js_logic": """
          const W = getNum('weight_lbs');
          const H = getNum('height_in');
          const N = getNum('neck_in');
          const waist = getNum('waist_in');

          const diff = Math.max(1, waist - N);
          const bf = (86.010 * Math.log10(diff)) - (70.041 * Math.log10(H)) + 36.76;
          const cleanBf = Math.max(3, Math.min(50, bf));
          const fatMass = W * (cleanBf / 100);
          const leanMass = W - fatMass;

          let cat = 'Fitness';
          if (cleanBf < 6) cat = 'Essential Fat (< 6%)';
          else if (cleanBf < 14) cat = 'Athletes (6 - 13%)';
          else if (cleanBf < 18) cat = 'Fitness (14 - 17%)';
          else if (cleanBf < 25) cat = 'Acceptable (18 - 24%)';
          else cat = 'Obese (≥ 25%)';

          setDisp('body_fat_pct', cleanBf.toFixed(1) + '%');
          setDisp('fat_mass', fatMass.toFixed(1) + ' lbs');
          setDisp('lean_mass', leanMass.toFixed(1) + ' lbs');
          setDisp('fitness_category', cat);
        """
    },
    {
        "slug": "macro",
        "category": "health",
        "name": "Macronutrient Split (Carbs, Protein, Fats) Calculator",
        "description": "Calculate daily macronutrient targets in grams and calories based on fitness goals (cutting, lean bulk, or maintenance).",
        "hero_badge": "Nutritional Biochemistry • Macronutrient Gram Matrix",
        "formula_display": "Total Calories = (Protein × 4) + (Carbohydrates × 4) + (Fats × 9)",
        "fields": [
            {"id": "daily_calories", "label": "Daily Calorie Target", "default": 2400, "suffix": "kcal", "min": 1000, "max": 6000, "step": 50, "hint": "Target daily caloric intake"},
            {"id": "protein_pct", "label": "Protein Percentage (%)", "default": 30, "suffix": "%", "min": 15, "max": 50, "step": 5, "hint": "4 kcal/gram (30% recommended for lifting)"},
            {"id": "fats_pct", "label": "Fats Percentage (%)", "default": 25, "suffix": "%", "min": 15, "max": 45, "step": 5, "hint": "9 kcal/gram (25% for hormone balance)"}
        ],
        "metrics": [
            {"id": "protein_grams", "label": "Daily Protein Target", "default_display": "180 g (720 kcal)", "highlight": True},
            {"id": "carbs_grams", "label": "Daily Carbohydrate Target", "default_display": "270 g (1,080 kcal)", "highlight": True},
            {"id": "fats_grams", "label": "Daily Fats Target", "default_display": "67 g (600 kcal)"},
            {"id": "macro_ratio", "label": "Macronutrient Split", "default_display": "45C / 30P / 25F"}
        ],
        "proof_steps": [
            {"step_title": "Caloric Density Invariants (Atwater Factors)", "step_text": "Proteins and carbohydrates yield exactly 4.0 kcal per gram of combustible energy. Dietary lipids (fats) yield 9.0 kcal per gram."},
            {"step_title": "Gram Equivalence Transformation", "step_text": "Protein Grams = (Total kcal × Protein%) / 4. Fat Grams = (Total kcal × Fat%) / 9. Carbs Grams = (Total kcal × [100 - Protein% - Fat%]) / 4."},
            {"step_title": "Thermic Effect of Food (TEF)", "step_text": "Protein has the highest thermic cost, with 20% to 30% of ingested protein calories burned during enzymatic peptide hydrolysis."}
        ],
        "faqs": [
            {"q": "How many grams of protein do I need to build muscle?", "a": "Peer-reviewed sports nutrition literature (ISSN) establishes that 0.7 to 1.0 grams of protein per pound of body weight (1.6 to 2.2 g/kg) maximizes muscle protein synthesis (MPS)."},
            {"q": "Can dietary fats drop below 15%?", "a": "Dropping dietary fats below 15% to 20% of total calories can impair steroid hormone synthesis (testosterone, estrogen), fat-soluble vitamin absorption (A, D, E, K), and cell membrane integrity."}
        ],
        "js_logic": """
          const kcal = getNum('daily_calories');
          const pPct = getNum('protein_pct') || 30;
          const fPct = getNum('fats_pct') || 25;
          const cPct = Math.max(0, 100 - pPct - fPct);

          const pGrams = (kcal * (pPct / 100)) / 4;
          const fGrams = (kcal * (fPct / 100)) / 9;
          const cGrams = (kcal * (cPct / 100)) / 4;

          setDisp('protein_grams', Math.round(pGrams) + ' g (' + Math.round(pGrams * 4) + ' kcal)');
          setDisp('carbs_grams', Math.round(cGrams) + ' g (' + Math.round(cGrams * 4) + ' kcal)');
          setDisp('fats_grams', Math.round(fGrams) + ' g (' + Math.round(fGrams * 9) + ' kcal)');
          setDisp('macro_ratio', cPct + 'C / ' + pPct + 'P / ' + fPct + 'F');
        """
    },
    {
        "slug": "calorie-deficit",
        "category": "health",
        "name": "Calorie Deficit & Fat Loss Timeline Calculator",
        "description": "Calculate daily caloric deficit, weekly fat loss rate, and exact calendar target date to reach your goal body weight.",
        "hero_badge": "Thermodynamics • Fat Loss Vector",
        "formula_display": "Target Date = Today + [(Weight to Lose × 3,500) / Daily Deficit] Days",
        "fields": [
            {"id": "current_weight", "label": "Current Weight", "default": 200, "suffix": "lbs", "min": 80, "max": 500, "step": 1, "hint": "Current scale weight"},
            {"id": "goal_weight", "label": "Goal Weight", "default": 175, "suffix": "lbs", "min": 80, "max": 500, "step": 1, "hint": "Target dream weight"},
            {"id": "tdee", "label": "Maintenance Calories (TDEE)", "default": 2600, "suffix": "kcal", "min": 1200, "max": 5000, "step": 50, "hint": "Your maintenance burn"},
            {"id": "daily_deficit", "label": "Target Daily Deficit", "default": 500, "suffix": "kcal/day", "min": 250, "max": 1200, "step": 50, "hint": "500 kcal/day = 1.0 lb fat loss per week"}
        ],
        "metrics": [
            {"id": "target_calories", "label": "Daily Intake Calorie Target", "default_display": "2,100 kcal/day", "highlight": True},
            {"id": "weekly_loss", "label": "Weekly Fat Loss Rate", "default_display": "1.00 lbs / week", "highlight": True},
            {"id": "days_to_goal", "label": "Days to Goal Weight", "default_display": "175 days (25.0 weeks)"},
            {"id": "total_energy_deficit", "label": "Total Cumulative Deficit", "default_display": "87,500 kcal"}
        ],
        "proof_steps": [
            {"step_title": "Wishnofsky Adipose Rule", "step_text": "One pound of human fat tissue contains ~3,500 kilocalories of stored chemical energy: Total Energy Deficit = (Weight_current - Weight_goal) × 3,500 kcal."},
            {"step_title": "Daily Prescribed Intake", "step_text": "Daily Food Intake Target = TDEE - Daily Deficit."},
            {"step_title": "Temporal Projection", "step_text": "Days to Goal = Total Energy Deficit / Daily Deficit. Weekly Loss Rate = (Daily Deficit × 7) / 3,500."}
        ],
        "faqs": [
            {"q": "What is a safe weekly rate of fat loss?", "a": "A sustainable rate of fat loss is 0.5% to 1.0% of your total body weight per week (typically 1 to 2 lbs per week). Faster deficits risk losing lean muscle mass and triggering metabolic slowdown."},
            {"q": "What causes weight loss plateaus?", "a": "As you lose weight, your BMR decreases (smaller body requires less energy), non-exercise physical activity (NEAT) unconsciously declines, and water retention may temporarily mask fat loss."}
        ],
        "js_logic": """
          const curr = getNum('current_weight');
          const goal = getNum('goal_weight');
          const tdee = getNum('tdee');
          const def = getNum('daily_deficit');

          const deltaLbs = Math.max(0, curr - goal);
          const totalKcal = deltaLbs * 3500;
          const targetKcal = Math.max(1200, tdee - def);
          const weeklyLbs = (def * 7) / 3500;
          const days = def > 0 ? (totalKcal / def) : 0;
          const weeks = days / 7;

          setDisp('target_calories', Math.round(targetKcal).toLocaleString() + ' kcal/day');
          setDisp('weekly_loss', weeklyLbs.toFixed(2) + ' lbs / week');
          setDisp('days_to_goal', Math.round(days) + ' days (' + weeks.toFixed(1) + ' weeks)');
          setDisp('total_energy_deficit', Math.round(totalKcal).toLocaleString() + ' kcal');
        """
    },
    {
        "slug": "ideal-weight",
        "category": "health",
        "name": "Ideal Body Weight (IBW) Calculator",
        "description": "Calculate clinical ideal body weight using Devine, Robinson, Miller, and Hamwi pharmacological dosing equations.",
        "hero_badge": "Clinical Pharmacokinetics • IBW Formula Suite",
        "formula_display": "Devine IBW (men) = 50.0 kg + 2.3 kg × (Height in inches - 60)",
        "fields": [
            {"id": "height_in", "label": "Height", "default": 70, "suffix": "in", "min": 60, "max": 84, "step": 1, "hint": "Height in inches (5'10\" = 70 in)"},
            {"id": "gender", "label": "Biological Sex (1 for Male, 0 for Female)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 for Male, 0 for Female"}
        ],
        "metrics": [
            {"id": "devine_ibw", "label": "Devine Formula (Clinical Gold Standard)", "default_display": "160.9 lbs (73.0 kg)", "highlight": True},
            {"id": "robinson_ibw", "label": "Robinson Formula", "default_display": "160.7 lbs (72.9 kg)"},
            {"id": "miller_ibw", "label": "Miller Formula", "default_display": "156.7 lbs (71.1 kg)"},
            {"id": "hamwi_ibw", "label": "Hamwi Rule of Thumb", "default_display": "166.0 lbs (75.3 kg)"}
        ],
        "proof_steps": [
            {"step_title": "Dr. Devine Pharmacological Baseline", "step_text": "Originally developed in 1974 for renal clearance drug dosing: Men: 50.0 kg + 2.3 kg per inch over 5 feet. Women: 45.5 kg + 2.3 kg per inch over 5 feet."},
            {"step_title": "Robinson and Miller Empirical Adjustments", "step_text": "Robinson (1983) and Miller (1983) modified coefficients based on updated Metropolitan Life actuarial mortality tables."},
            {"step_title": "Conversion to Imperial Mass", "step_text": "Mass in pounds = Mass (kg) × 2.20462."}
        ],
        "faqs": [
            {"q": "Why do hospitals use Ideal Body Weight instead of actual weight?", "a": "Many critical medications (aminoglycosides, anesthetics, and chemotherapy) distribute poorly into adipose tissue. Dosing based on actual weight in an obese patient could cause fatal toxicity."},
            {"q": "What if my weight is higher than the IBW score?", "a": "IBW formulas represent a lean baseline. Athletes with substantial skeletal muscle mass naturally exceed IBW recommendations without adverse health risks."}
        ],
        "js_logic": """
          const H = getNum('height_in');
          const isMale = getNum('gender') === 1;
          const over60 = Math.max(0, H - 60);

          let devKg = isMale ? (50.0 + 2.3 * over60) : (45.5 + 2.3 * over60);
          let robKg = isMale ? (52.0 + 1.9 * over60) : (49.0 + 1.7 * over60);
          let milKg = isMale ? (56.2 + 1.41 * over60) : (53.1 + 1.36 * over60);
          let hamKg = isMale ? (48.0 + 2.7 * over60) : (45.5 + 2.2 * over60);

          setDisp('devine_ibw', (devKg * 2.20462).toFixed(1) + ' lbs (' + devKg.toFixed(1) + ' kg)');
          setDisp('robinson_ibw', (robKg * 2.20462).toFixed(1) + ' lbs (' + robKg.toFixed(1) + ' kg)');
          setDisp('miller_ibw', (milKg * 2.20462).toFixed(1) + ' lbs (' + milKg.toFixed(1) + ' kg)');
          setDisp('hamwi_ibw', (hamKg * 2.20462).toFixed(1) + ' lbs (' + hamKg.toFixed(1) + ' kg)');
        """
    },
    {
        "slug": "water-intake",
        "category": "health",
        "name": "Daily Water Intake & Hydration Calculator",
        "description": "Calculate daily water hydration requirements in ounces, liters, and standard glasses based on weight, exercise, and climate.",
        "hero_badge": "Fluid Dynamics • Hydration Solver",
        "formula_display": "Daily Water (oz) = [Weight (lbs) × 0.5] + (Exercise Minutes × 0.4)",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 175, "suffix": "lbs", "min": 60, "max": 450, "step": 1, "hint": "Current body weight"},
            {"id": "exercise_minutes", "label": "Daily Exercise Duration", "default": 45, "suffix": "min", "min": 0, "max": 240, "step": 5, "hint": "Minutes of strenuous or aerobic physical activity"},
            {"id": "hot_climate", "label": "Hot Climate or Heavy Sweating (1 Yes, 0 No)", "default": 0, "min": 0, "max": 1, "step": 1, "hint": "Adds 16 oz for humid heat"}
        ],
        "metrics": [
            {"id": "total_ounces", "label": "Daily Target Fluid Intake", "default_display": "105.5 oz / day", "highlight": True},
            {"id": "total_liters", "label": "Volume in Liters", "default_display": "3.12 Liters"},
            {"id": "glasses_count", "label": "Standard 8-oz Glasses", "default_display": "13 glasses"},
            {"id": "hourly_intake", "label": "Wakeful Pacing (16 hrs)", "default_display": "6.6 oz / hour"}
        ],
        "proof_steps": [
            {"step_title": "Baseline Physiological Water Turnover", "step_text": "Base requirement is 0.5 fluid ounces per pound of body weight to cover respiratory, renal, and dermal insensate fluid losses."},
            {"step_title": "Exercise Induced Sweating Supplement", "step_text": "Sweat rates during exercise average 0.5 to 1.0 liters per hour. Add 12 oz of water for every 30 minutes of vigorous training (0.4 oz/min)."},
            {"step_title": "Dimensional Metric Conversion", "step_text": "Liters = Ounces / 33.814. Standard 8-oz glass count = ceil(Ounces / 8)."}
        ],
        "faqs": [
            {"q": "Does coffee or tea count toward my water intake?", "a": "Yes! While caffeine has a mild diuretic effect, scientific studies demonstrate that caffeinated beverages still contribute net positive hydration toward your daily fluid balance."},
            {"q": "Can you drink too much water?", "a": "Yes. Drinking excessive water (e.g. several liters within an hour) without replenishing electrolytes can cause hyponatremia (water intoxication), diluting blood sodium to dangerously low levels."}
        ],
        "js_logic": """
          const W = getNum('weight_lbs');
          const ex = getNum('exercise_minutes');
          const hot = getNum('hot_climate') === 1;

          const baseOz = W * 0.5;
          const exOz = ex * 0.4;
          const climateOz = hot ? 16 : 0;
          const totalOz = baseOz + exOz + climateOz;
          const liters = totalOz / 33.814;
          const glasses = Math.ceil(totalOz / 8);
          const perHr = totalOz / 16;

          setDisp('total_ounces', totalOz.toFixed(1) + ' oz / day');
          setDisp('total_liters', liters.toFixed(2) + ' Liters');
          setDisp('glasses_count', glasses + ' glasses (8 oz)');
          setDisp('hourly_intake', perHr.toFixed(1) + ' oz / hour');
        """
    },
    {
        "slug": "target-heart-rate",
        "category": "health",
        "name": "Target Heart Rate & Training Zones Calculator",
        "description": "Calculate cardiovascular training heart rate zones (Zone 1 Recovery to Zone 5 VO2 Max) using the Karvonen Heart Rate Reserve formula.",
        "hero_badge": "Cardiovascular Physiology • Karvonen Matrix",
        "formula_display": "Target HR = [(Max HR - Resting HR) × Intensity%] + Resting HR",
        "fields": [
            {"id": "age_years", "label": "Age", "default": 35, "suffix": "yrs", "min": 15, "max": 95, "step": 1, "hint": "Your age in years"},
            {"id": "resting_hr", "label": "Resting Heart Rate (RHR)", "default": 62, "suffix": "BPM", "min": 35, "max": 110, "step": 1, "hint": "Morning resting pulse before getting out of bed"}
        ],
        "metrics": [
            {"id": "zone2_hr", "label": "Zone 2 (Aerobic Base / Fat Burn 60-70%)", "default_display": "136 - 148 BPM", "highlight": True},
            {"id": "zone4_hr", "label": "Zone 4 (Lactate Threshold 80-90%)", "default_display": "160 - 173 BPM", "highlight": True},
            {"id": "max_hr", "label": "Estimated Max Heart Rate", "default_display": "185 BPM"},
            {"id": "hr_reserve", "label": "Heart Rate Reserve (HRR)", "default_display": "123 BPM"}
        ],
        "proof_steps": [
            {"step_title": "Maximal Heart Rate Derivation", "step_text": "Estimated HR_max using Tanaka formula: HR_max = 208 - (0.7 × Age)."},
            {"step_title": "Heart Rate Reserve (HRR) Calculation", "step_text": "HRR = HR_max - Resting HR. HRR reflects true physiological cardiovascular working capacity."},
            {"step_title": "Karvonen Multi-Zone Stratification", "step_text": "Zone 1 (50-60%): Recovery; Zone 2 (60-70%): Mitochondrial endurance; Zone 3 (70-80%): Aerobic tempo; Zone 4 (80-90%): Anaerobic threshold; Zone 5 (90-100%): Maximal neuromuscular sprint."}
        ],
        "faqs": [
            {"q": "Why is Zone 2 training so popular for endurance and longevity?", "a": "Zone 2 training stimulates mitochondrial biogenesis, enhances cellular fat oxidation (lactate clearance), and builds capillary density in slow-twitch muscle fibers without excessive cortisol or central nervous system fatigue."},
            {"q": "How do I accurately measure my resting heart rate?", "a": "Measure your pulse for 60 seconds immediately upon waking in the morning while still lying quietly in bed, before drinking coffee or looking at your phone."}
        ],
        "js_logic": """
          const age = getNum('age_years');
          const rhr = getNum('resting_hr');

          const maxHr = Math.round(208 - (0.7 * age));
          const hrr = maxHr - rhr;

          const z2Low = Math.round((hrr * 0.60) + rhr);
          const z2High = Math.round((hrr * 0.70) + rhr);
          const z4Low = Math.round((hrr * 0.80) + rhr);
          const z4High = Math.round((hrr * 0.90) + rhr);

          setDisp('zone2_hr', z2Low + ' - ' + z2High + ' BPM');
          setDisp('zone4_hr', z4Low + ' - ' + z4High + ' BPM');
          setDisp('max_hr', maxHr + ' BPM');
          setDisp('hr_reserve', hrr + ' BPM');
        """
    },
    {
        "slug": "one-rep-max",
        "category": "health",
        "name": "One Rep Max (1RM) Calculator",
        "description": "Calculate estimated 1RM and percentage load working sets (95%, 85%, 70%) using Epley, Brzycki, and Lander lifting equations.",
        "hero_badge": "Biomechanics • Strength 1RM Matrix",
        "formula_display": "1RM (Epley) = Weight × (1 + Reps / 30) | 1RM (Brzycki) = Weight / (1.0278 - 0.0278 × Reps)",
        "fields": [
            {"id": "weight_lifted", "label": "Lifted Weight", "default": 225, "suffix": "lbs", "min": 20, "max": 1000, "step": 5, "hint": "Weight lifted during set"},
            {"id": "reps_completed", "label": "Repetitions Completed", "default": 5, "suffix": "reps", "min": 1, "max": 20, "step": 1, "hint": "Reps performed before failure (1-10 most accurate)"}
        ],
        "metrics": [
            {"id": "one_rep_max", "label": "Estimated 1RM (Epley)", "default_display": "262.5 lbs", "highlight": True},
            {"id": "brzycki_max", "label": "Brzycki Formula Estimate", "default_display": "253.1 lbs"},
            {"id": "load_85pct", "label": "85% 1RM Working Load (5-Rep)", "default_display": "223.1 lbs"},
            {"id": "load_70pct", "label": "70% 1RM Hypertrophy Load (12-Rep)", "default_display": "183.8 lbs"}
        ],
        "proof_steps": [
            {"step_title": "Epley Strength Dynamic", "step_text": "Formulated by Boyd Epley in 1985: 1RM = Weight × [1 + (Reps / 30)]."},
            {"step_title": "Brzycki Non-Linear Hyperbolic Form", "step_text": "Matt Brzycki formulation: 1RM = Weight / [1.0278 - (0.0278 × Reps)]."},
            {"step_title": "Predictive Accuracy Threshold", "step_text": "Both formulas maintain high correlation (r > 0.98) when repetitions are under 10. Accuracy diminishes significantly above 12 to 15 reps due to muscle endurance bias."}
        ],
        "faqs": [
            {"q": "Why estimate 1RM instead of actually testing it?", "a": "Testing a true maximal 1RM imposes extreme neural and tendon strain with significant risk of injury. Submaximal 3-rep to 5-rep testing yields safe, highly accurate projections for program periodization."},
            {"q": "What percentage of 1RM builds muscle best?", "a": "Hypertrophy occurs effectively across 60% to 85% of 1RM, provided working sets are taken within 1 to 3 repetitions of muscular failure."}
        ],
        "js_logic": """
          const W = getNum('weight_lifted');
          const R = getNum('reps_completed');

          const epley = R === 1 ? W : W * (1 + (R / 30));
          const brzycki = R === 1 ? W : W / (1.0278 - (0.0278 * R));
          const p85 = epley * 0.85;
          const p70 = epley * 0.70;

          setDisp('one_rep_max', epley.toFixed(1) + ' lbs');
          setDisp('brzycki_max', brzycki.toFixed(1) + ' lbs');
          setDisp('load_85pct', p85.toFixed(1) + ' lbs');
          setDisp('load_70pct', p70.toFixed(1) + ' lbs');
        """
    },
    {
        "slug": "running-pace",
        "category": "health",
        "name": "Running Pace & Race Finish Time Calculator",
        "description": "Calculate running speed (mph, km/h), splits per mile/km, and projected finish times for 5K, 10K, Half Marathon, and Full Marathon.",
        "hero_badge": "Athletic Kinetics • Running Pace Matrix",
        "formula_display": "Pace = Time / Distance | Projected Time = Distance × Pace",
        "fields": [
            {"id": "distance_miles", "label": "Run Distance", "default": 6.214, "suffix": "miles", "min": 0.5, "max": 100, "step": 0.1, "hint": "6.214 miles = 10K; 13.1 = Half; 26.2 = Marathon"},
            {"id": "hours", "label": "Time: Hours", "default": 0, "suffix": "hrs", "min": 0, "max": 24, "step": 1, "hint": "Elapsed hours"},
            {"id": "minutes", "label": "Time: Minutes", "default": 52, "suffix": "min", "min": 0, "max": 59, "step": 1, "hint": "Elapsed minutes"},
            {"id": "seconds", "label": "Time: Seconds", "default": 30, "suffix": "sec", "min": 0, "max": 59, "step": 1, "hint": "Elapsed seconds"}
        ],
        "metrics": [
            {"id": "pace_per_mile", "label": "Pace per Mile", "default_display": "8:27 min/mile", "highlight": True},
            {"id": "pace_per_km", "label": "Pace per Kilometer", "default_display": "5:15 min/km"},
            {"id": "speed_mph", "label": "Running Speed (MPH)", "default_display": "7.10 mph (11.43 km/h)"},
            {"id": "marathon_proj", "label": "Full Marathon Projection (26.2 mi)", "default_display": "3h 41m 27s"}
        ],
        "proof_steps": [
            {"step_title": "Temporal Decimal Conversion", "step_text": "Total minutes T_min = (Hours × 60) + Minutes + (Seconds / 60)."},
            {"step_title": "Mile and Kilometer Split Calculus", "step_text": "Pace_mile = T_min / Distance (mi). Pace_km = Pace_mile / 1.60934."},
            {"step_title": "Riegel Race Projection Power Model", "step_text": "Peter Riegel's endurance formula predicts finish times: T2 = T1 × (D2 / D1)^1.06, modeling cardiovascular fatigue over extended distances."}
        ],
        "faqs": [
            {"q": "What pace is needed to run a sub-4-hour marathon?", "a": "To complete a marathon in under 4 hours, you must maintain an average pace of 9 minutes and 9 seconds per mile (5:41 per kilometer) across all 26.2 miles."},
            {"q": "What pace is required for a sub-20-minute 5K?", "a": "A sub-20-minute 5K (3.107 miles) requires an average pace of 6 minutes and 26 seconds per mile (3:59 per kilometer)."}
        ],
        "js_logic": """
          const D = getNum('distance_miles') || 1;
          const h = getNum('hours');
          const m = getNum('minutes');
          const s = getNum('seconds');

          const totalSec = (h * 3600) + (m * 60) + s;
          const totalMin = totalSec / 60;
          const totalHours = totalSec / 3600;

          const paceMinPerMile = totalMin / D;
          const paceSecMile = paceMinPerMile * 60;
          const pMin = Math.floor(paceSecMile / 60);
          const pSec = Math.round(paceSecMile % 60);

          const paceMinPerKm = paceMinPerMile / 1.60934;
          const paceSecKm = paceMinPerKm * 60;
          const kMin = Math.floor(paceSecKm / 60);
          const kSec = Math.round(paceSecKm % 60);

          const mph = totalHours > 0 ? (D / totalHours) : 0;
          const kmh = mph * 1.60934;

          // Riegel Marathon formula: T2 = T1 * (26.219 / D)^1.06
          const marSec = totalSec * Math.pow(26.21875 / D, 1.06);
          const marH = Math.floor(marSec / 3600);
          const marM = Math.floor((marSec % 3600) / 60);
          const marS = Math.round(marSec % 60);

          setDisp('pace_per_mile', pMin + ':' + (pSec < 10 ? '0' : '') + pSec + ' min/mile');
          setDisp('pace_per_km', kMin + ':' + (kSec < 10 ? '0' : '') + kSec + ' min/km');
          setDisp('speed_mph', mph.toFixed(2) + ' mph (' + kmh.toFixed(2) + ' km/h)');
          setDisp('marathon_proj', marH + 'h ' + marM + 'm ' + marS + 's');
        """
    },
    {
        "slug": "vo2-max",
        "category": "health",
        "name": "VO2 Max & Aerobic Fitness Calculator",
        "description": "Calculate maximal oxygen uptake (VO2 Max in mL/kg/min) and cardio fitness percentile using the Uth-Sørensen-Overgaard-Pedersen resting formula.",
        "hero_badge": "Cardiopulmonary • VO2 Max Matrix",
        "formula_display": "VO2 Max = 15.3 × (HR_max / HR_resting)",
        "fields": [
            {"id": "age_years", "label": "Age", "default": 30, "suffix": "yrs", "min": 18, "max": 85, "step": 1, "hint": "Your age in years"},
            {"id": "resting_hr", "label": "Resting Heart Rate", "default": 58, "suffix": "BPM", "min": 35, "max": 100, "step": 1, "hint": "True morning resting heart rate"}
        ],
        "metrics": [
            {"id": "vo2_score", "label": "Estimated VO2 Max", "default_display": "49.3 mL/kg/min", "highlight": True},
            {"id": "cardio_tier", "label": "Cardiorespiratory Fitness Tier", "default_display": "Excellent (Top 15%)"},
            {"id": "oxygen_uptake", "label": "Max Oxygen Flow (70kg body)", "default_display": "3.45 Liters O2 / min"},
            {"id": "longevity_hazard", "label": "Mortality Risk Hazard Ratio", "default_display": "0.55 (Low all-cause mortality)"}
        ],
        "proof_steps": [
            {"step_title": "Maximal Heart Rate Approximation", "step_text": "HR_max = 208 - (0.7 × Age)."},
            {"step_title": "Uth-Sørensen-Overgaard-Pedersen Ratio Derivation", "step_text": "Extensively validated equation based on cardiac stroke volume: VO2 Max = 15.3 × (HR_max / HR_resting)."},
            {"step_title": "Cardiovascular Longevity Metric", "step_text": "Landmark clinical studies (Mandsager et al., JAMA) show that individuals in the elite and superior VO2 max categories exhibit up to a 5-fold reduction in all-cause mortality compared to sedentary cohorts."}
        ],
        "faqs": [
            {"q": "What is a good VO2 max for a 30-year-old?", "a": "For a 30-year-old male, a VO2 max above 45 mL/kg/min is considered good, and above 52 is excellent. For a 30-year-old female, above 38 is good, and above 45 is excellent."},
            {"q": "How can I increase my VO2 max?", "a": "High-Intensity Interval Training (HIIT) such as Norwegian 4×4 protocols (4 minutes at 90-95% max HR followed by 3 minutes active recovery) combined with consistent Zone 2 aerobic volume produces rapid VO2 max improvements."}
        ],
        "js_logic": """
          const age = getNum('age_years');
          const rhr = getNum('resting_hr') || 60;

          const maxHr = 208 - (0.7 * age);
          const vo2 = 15.3 * (maxHr / rhr);
          const liters = (vo2 * 70) / 1000;

          let tier = 'Good';
          if (vo2 < 32) tier = 'Poor (Bottom 20%)';
          else if (vo2 < 40) tier = 'Fair (20 - 40th percentile)';
          else if (vo2 < 48) tier = 'Good (40 - 70th percentile)';
          else if (vo2 < 55) tier = 'Excellent (Top 15%)';
          else tier = 'Superior / Elite (Top 5%)';

          setDisp('vo2_score', vo2.toFixed(1) + ' mL/kg/min');
          setDisp('cardio_tier', tier);
          setDisp('oxygen_uptake', liters.toFixed(2) + ' Liters O2 / min');
          setDisp('longevity_hazard', '0.55 (Low all-cause mortality)');
        """
    },
    {
        "slug": "intermittent-fasting",
        "category": "health",
        "name": "Intermittent Fasting & Autophagy Schedule Calculator",
        "description": "Calculate fasting and feeding windows for 16:8, 18:6, 20:4, and OMAD fasting schedules with biological milestones (ketosis, autophagy).",
        "hero_badge": "Circadian Biology • Fasting Protocol Matrix",
        "formula_display": "Fasting Window = 24 Hours - Eating Window Hours",
        "fields": [
            {"id": "fasting_hours", "label": "Fasting Protocol (16, 18, 20, or 23)", "default": 16, "suffix": "hours", "min": 12, "max": 24, "step": 2, "hint": "16 for 16:8 Leangains, 18 for 18:6, 20 for Warrior Diet"},
            {"id": "first_meal_hour", "label": "First Meal Time (24-Hour Format)", "default": 12, "suffix": ":00", "min": 6, "max": 20, "step": 1, "hint": "12 = 12:00 PM noon"}
        ],
        "metrics": [
            {"id": "feeding_window", "label": "Daily Eating Window", "default_display": "12:00 PM – 8:00 PM (8 hrs)", "highlight": True},
            {"id": "fasting_window", "label": "Fasting Period", "default_display": "8:00 PM – 12:00 PM (16 hrs)", "highlight": True},
            {"id": "ketosis_onset", "label": "Mild Ketosis Transition", "default_display": "Hour 12 to 14 of fast"},
            {"id": "autophagy_peak", "label": "Cellular Autophagy Onset", "default_display": "Hour 16 to 18 of fast"}
        ],
        "proof_steps": [
            {"step_title": "Circadian Digestive Partitioning", "step_text": "Feeding Window Hours = 24 - Fasting Hours. End of feeding window = First Meal Hour + Feeding Window Hours."},
            {"step_title": "Hepatic Glycogen Depletion Timeline", "step_text": "Liver glycogen reserves deplete after 12 to 14 hours of caloric fasting, triggering AMPK activation and adipose lipolysis for ketone generation (acetoacetate and beta-hydroxybutyrate)."},
            {"step_title": "Autophagy Cellular Cleanup", "step_text": "Inhibition of mammalian target of rapamycin (mTOR) through amino acid deprivation initiates cellular macroautophagy, clearing damaged mitochondria and misfolded proteins."}
        ],
        "faqs": [
            {"q": "What can I drink during the fasting window?", "a": "Water, black coffee, unflavored unsweetened green/black tea, and plain mineral water with electrolytes will not break your fast or spike insulin."},
            {"q": "Does 16:8 intermittent fasting cause muscle loss?", "a": "No. As long as you consume adequate daily protein (0.7 to 1.0 g/lb) and maintain progressive resistance training, intermittent fasting preserves lean muscle while targeting body fat."}
        ],
        "js_logic": """
          const fastH = getNum('fasting_hours') || 16;
          const startH = getNum('first_meal_hour') || 12;

          const feedH = 24 - fastH;
          const endH = (startH + feedH) % 24;

          function fmt(h) {
            const period = h >= 12 ? 'PM' : 'AM';
            const h12 = h % 12 === 0 ? 12 : (h % 12);
            return h12 + ':00 ' + period;
          }

          setDisp('feeding_window', fmt(startH) + ' – ' + fmt(endH) + ' (' + feedH + ' hrs)');
          setDisp('fasting_window', fmt(endH) + ' – ' + fmt(startH) + ' (' + fastH + ' hrs)');
          setDisp('ketosis_onset', 'Hour 12 to 14 of fast');
          setDisp('autophagy_peak', fastH >= 16 ? 'Hour 16+ active autophagy' : 'Requires 16+ hours');
        """
    },
    {
        "slug": "sleep-cycles",
        "category": "health",
        "name": "Sleep Cycle & Optimal Bedtime Calculator",
        "description": "Calculate exact bedtimes and wake times aligned with 90-minute ultradian sleep cycles (REM and Slow-Wave Deep Sleep) to eliminate grogginess.",
        "hero_badge": "Neuro-Physiology • 90-Min Sleep Architecture",
        "formula_display": "Optimal Wake Time = Bedtime + (N × 90 Minutes) + 15 Minutes Fall-Asleep Latency",
        "fields": [
            {"id": "wake_hour", "label": "Target Wake Hour (24-Hour Format)", "default": 7, "suffix": ":00", "min": 4, "max": 12, "step": 1, "hint": "7 = 7:00 AM"},
            {"id": "wake_min", "label": "Target Wake Minute", "default": 0, "suffix": "min", "min": 0, "max": 45, "step": 15, "hint": "0, 15, 30, or 45"},
            {"id": "sleep_latency", "label": "Time to Fall Asleep", "default": 15, "suffix": "min", "min": 5, "max": 45, "step": 5, "hint": "Standard healthy latency is 10 to 20 minutes"}
        ],
        "metrics": [
            {"id": "bedtime_5cycles", "label": "Recommended Bedtime (5 Cycles / 7.5 hrs)", "default_display": "11:15 PM", "highlight": True},
            {"id": "bedtime_6cycles", "label": "Extended Bedtime (6 Cycles / 9.0 hrs)", "default_display": "9:45 PM"},
            {"id": "bedtime_4cycles", "label": "Minimum Bedtime (4 Cycles / 6.0 hrs)", "default_display": "12:45 AM"},
            {"id": "sleep_inertia", "label": "Sleep Inertia Risk", "default_display": "Zero (Waking at end of light sleep)"}
        ],
        "proof_steps": [
            {"step_title": "Ultradian Sleep Architecture", "step_text": "Human sleep is structured into discrete 90-minute ultradian cycles transitioning through NREM Stage 1 (light), Stage 2, Stage 3 (Slow-Wave Deep Sleep), and REM (Rapid Eye Movement)."},
            {"step_title": "Sleep Inertia Prevention", "step_text": "Waking up in the middle of Stage 3 deep delta-wave sleep causes intense sleep inertia (grogginess and impaired cognitive function lasting up to 4 hours). Waking at the completion of a 90-minute cycle ensures effortless alertness."},
            {"step_title": "Sleep Latency Buffer", "step_text": "Bedtime = Wake Time - (Cycles × 90 min) - Latency Buffer."}
        ],
        "faqs": [
            {"q": "Why do I feel more tired after 8 hours than 7.5 hours?", "a": "8 hours (480 minutes) equals 5.33 sleep cycles, meaning an alarm wakes you directly in the middle of Stage 3 slow-wave deep sleep. 7.5 hours (450 minutes) is exactly 5 complete 90-minute cycles, allowing you to wake up naturally during light Stage 1 sleep."},
            {"q": "How many sleep cycles do adults need per night?", "a": "Most healthy adults require 5 complete cycles (7.5 hours of actual sleep) to facilitate physical tissue repair, hormone secretion (HGH), and memory consolidation."}
        ],
        "js_logic": """
          const wH = getNum('wake_hour') || 7;
          const wM = getNum('wake_min') || 0;
          const lat = getNum('sleep_latency') || 15;

          const totalWakeMin = (wH * 60) + wM;

          function getBedtime(cycles) {
            const sleepMin = (cycles * 90) + lat;
            let bedMin = (totalWakeMin - sleepMin) % 1440;
            if (bedMin < 0) bedMin += 1440;

            const bH = Math.floor(bedMin / 60);
            const bM = Math.round(bedMin % 60);
            const period = bH >= 12 ? 'PM' : 'AM';
            const h12 = bH % 12 === 0 ? 12 : (bH % 12);
            return h12 + ':' + (bM < 10 ? '0' : '') + bM + ' ' + period;
          }

          setDisp('bedtime_5cycles', getBedtime(5));
          setDisp('bedtime_6cycles', getBedtime(6));
          setDisp('bedtime_4cycles', getBedtime(4));
          setDisp('sleep_inertia', 'Zero (Waking at end of light cycle)');
        """
    },
    {
        "slug": "pregnancy-due-date",
        "category": "health",
        "name": "Pregnancy Due Date & Gestational Age Calculator",
        "description": "Calculate Estimated Delivery Date (EDD), current gestational age in weeks and days, and trimester milestones using Naegele's rule.",
        "hero_badge": "Obstetrics • Naegele's Rule EDD Matrix",
        "formula_display": "Estimated Due Date = First Day of Last Menstrual Period + 280 Days (40 Weeks)",
        "fields": [
            {"id": "cycle_length", "label": "Menstrual Cycle Length", "default": 28, "suffix": "days", "min": 21, "max": 35, "step": 1, "hint": "Standard cycle is 28 days"},
            {"id": "weeks_since_lmp", "label": "Weeks Elapsed Since LMP", "default": 14, "suffix": "weeks", "min": 1, "max": 42, "step": 1, "hint": "Weeks since first day of last menstrual period"}
        ],
        "metrics": [
            {"id": "gestational_age", "label": "Current Gestational Age", "default_display": "14 Weeks 0 Days", "highlight": True},
            {"id": "current_trimester", "label": "Current Trimester", "default_display": "Second Trimester (Weeks 13–27)", "highlight": True},
            {"id": "days_remaining", "label": "Days Until Estimated Due Date", "default_display": "182 Days Left"},
            {"id": "viability_horizon", "label": "Fetal Viability Benchmark (Week 24)", "default_display": "In 10 Weeks"}
        ],
        "proof_steps": [
            {"step_title": "Naegele's Obstetric Rule", "step_text": "Devised by Franz Naegele: EDD = LMP + 1 year - 3 months + 7 days, corresponding to exactly 280 days (40 full weeks) from LMP."},
            {"step_title": "Cycle Length Adjustment", "step_text": "If cycle length deviates from 28 days: Adjusted Due Date = EDD + (Cycle Length - 28 days)."},
            {"step_title": "Trimester Benchmarks", "step_text": "First Trimester: Conception to Week 12. Second Trimester: Week 13 to Week 27. Third Trimester: Week 28 to Delivery."}
        ],
        "faqs": [
            {"q": "How many babies are born exactly on their estimated due date?", "a": "Only approximately 4% to 5% of babies are born on their exact calculated due date. However, over 80% of babies are born within 10 days before or after the EDD."},
            {"q": "Why is gestational age calculated from the last period instead of conception?", "a": "The exact date of ovulation and conception is rarely known with certainty, whereas the first day of the last menstrual period is a clear, identifiable biological marker."}
        ],
        "js_logic": """
          const cycle = getNum('cycle_length') || 28;
          const weeks = getNum('weeks_since_lmp');

          const cycleAdj = cycle - 28;
          const totalDays = (weeks * 7);
          const daysLeft = Math.max(0, 280 + cycleAdj - totalDays);

          let tri = 'First Trimester (Weeks 1–12)';
          if (weeks >= 28) tri = 'Third Trimester (Weeks 28–40)';
          else if (weeks >= 13) tri = 'Second Trimester (Weeks 13–27)';

          setDisp('gestational_age', weeks + ' Weeks 0 Days');
          setDisp('current_trimester', tri);
          setDisp('days_remaining', daysLeft + ' Days Left (~' + (daysLeft / 7).toFixed(1) + ' weeks)');
          setDisp('viability_horizon', weeks >= 24 ? 'Viability Reached' : 'In ' + (24 - weeks) + ' Weeks');
        """
    },
    {
        "slug": "ovulation",
        "category": "health",
        "name": "Ovulation & Fertile Window Calculator",
        "description": "Calculate ovulation peak day, fertile window (5 days prior + ovulation day), and luteal phase timeline based on cycle length.",
        "hero_badge": "Reproductive Endocrinology • Ovulation Matrix",
        "formula_display": "Ovulation Day = Cycle Length - Luteal Phase Length (Typically 14 Days)",
        "fields": [
            {"id": "cycle_length", "label": "Average Cycle Length", "default": 28, "suffix": "days", "min": 21, "max": 40, "step": 1, "hint": "Typical range is 26 to 32 days"},
            {"id": "luteal_phase", "label": "Luteal Phase Duration", "default": 14, "suffix": "days", "min": 10, "max": 16, "step": 1, "hint": "Standard luteal phase is consistently 14 days"}
        ],
        "metrics": [
            {"id": "ovulation_day", "label": "Estimated Ovulation Day", "default_display": "Day 14 of Cycle", "highlight": True},
            {"id": "fertile_window", "label": "High-Fertility Conception Window", "default_display": "Days 9 through 14 of Cycle", "highlight": True},
            {"id": "peak_fertility", "label": "Peak LH Surge Window", "default_display": "Days 12 and 13"},
            {"id": "next_period_day", "label": "Expected Next Menstruation", "default_display": "Day 29 of Cycle"}
        ],
        "proof_steps": [
            {"step_title": "Luteal Phase Constancy", "step_text": "While follicular phases vary widely between individuals, the post-ovulatory luteal phase remains biologically constant at ~14 days (range 12-15 days)."},
            {"step_title": "Ovulation Derivation", "step_text": "Day of Ovulation = Cycle Length - Luteal Duration. For a 28-day cycle: 28 - 14 = Day 14. For a 32-day cycle: 32 - 14 = Day 18."},
            {"step_title": "Sperm Viability Window", "step_text": "Human spermatozoa survive up to 5 days in cervical mucus, while an unfertilized ovum survives only 12 to 24 hours. Thus, the 6-day fertile window spans days (Ovulation - 5) through Ovulation."}
        ],
        "faqs": [
            {"q": "What biological signs indicate ovulation?", "a": "Key indicators include clear, stretchy 'egg-white' cervical mucus (spinnbarkeit), a slight pelvic cramp (mittelschmerz), and a positive urine luteinizing hormone (LH) strip test."},
            {"q": "Does basal body temperature (BBT) predict ovulation in advance?", "a": "No. Basal body temperature rises 0.5°F to 1.0°F only after ovulation has occurred due to progesterone secretion from the corpus luteum, confirming that ovulation took place."}
        ],
        "js_logic": """
          const cycle = getNum('cycle_length') || 28;
          const luteal = getNum('luteal_phase') || 14;

          const ovDay = cycle - luteal;
          const fertStart = Math.max(1, ovDay - 5);
          const peakStart = Math.max(1, ovDay - 2);

          setDisp('ovulation_day', 'Day ' + ovDay + ' of Cycle');
          setDisp('fertile_window', 'Days ' + fertStart + ' through ' + ovDay + ' of Cycle');
          setDisp('peak_fertility', 'Days ' + peakStart + ' and ' + (ovDay - 1));
          setDisp('next_period_day', 'Day ' + (cycle + 1) + ' of Cycle');
        """
    },
    {
        "slug": "bac",
        "category": "health",
        "name": "Blood Alcohol Concentration (BAC) Calculator",
        "description": "Calculate Blood Alcohol Concentration (BAC) and hours until sober using the clinically validated Widmark chemical distribution formula.",
        "hero_badge": "Toxicology • Widmark Pharmacokinetic Matrix",
        "formula_display": "BAC = [Alcohol Consumed (g) / (Body Weight (g) × r)] × 100 - (β × Hours)",
        "fields": [
            {"id": "drinks_count", "label": "Standard Drinks Consumed", "default": 3, "min": 1, "max": 20, "step": 1, "hint": "1 drink = 12oz beer (5%), 5oz wine (12%), or 1.5oz shot (40%)"},
            {"id": "body_weight_lbs", "label": "Body Weight", "default": 175, "suffix": "lbs", "min": 80, "max": 400, "step": 1, "hint": "Weight in pounds"},
            {"id": "drinking_hours", "label": "Hours Since First Drink", "default": 2, "suffix": "hrs", "min": 0.5, "max": 12, "step": 0.5, "hint": "Total elapsed drinking duration"},
            {"id": "gender_factor", "label": "Biological Sex (1 for Male, 0 for Female)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "r = 0.68 for males, r = 0.55 for females"}
        ],
        "metrics": [
            {"id": "bac_percentage", "label": "Estimated BAC", "default_display": "0.046%", "highlight": True},
            {"id": "legal_status", "label": "Legal Driving Status (0.08% Limit)", "default_display": "Under Legal Limit", "highlight": True},
            {"id": "hours_to_sober", "label": "Hours Until 0.00% Zero BAC", "default_display": "3.1 Hours Remaining"},
            {"id": "alcohol_grams", "label": "Pure Alcohol Ingested", "default_display": "42.0 grams"}
        ],
        "proof_steps": [
            {"step_title": "Standard Drink Pure Ethanol Mass", "step_text": "One US standard drink contains exactly 14.0 grams (0.6 fl oz) of pure ethyl alcohol."},
            {"step_title": "Widmark Distribution Equation", "step_text": "BAC = [Alcohol_grams / (Weight_grams × r)] × 100 - (0.015 × Hours). Distribution ratio r = 0.68 for biological men, 0.55 for biological women (reflecting higher average body fat and lower water content)."},
            {"step_title": "Hepatic Metabolic Clearance Rate", "step_text": "Human liver alcohol dehydrogenase (ADH) metabolizes ethanol at a steady zero-order kinetic rate of approximately β = 0.015% BAC reduction per hour."}
        ],
        "faqs": [
            {"q": "Can drinking coffee or taking a cold shower lower my BAC?", "a": "No. Neither coffee, exercise, cold showers, nor vomiting accelerates alcohol elimination. The liver metabolizes alcohol at a fixed zero-order rate of ~0.015% per hour. Only time will sober you up."},
            {"q": "What is the legal BAC limit in the United States?", "a": "In all US states (except Utah, which is 0.05%), the legal per se limit for operating a motor vehicle is 0.08% BAC for non-commercial drivers aged 21 and older."}
        ],
        "js_logic": """
          const drinks = getNum('drinks_count');
          const W_lbs = getNum('body_weight_lbs');
          const H = getNum('drinking_hours');
          const isMale = getNum('gender_factor') === 1;

          const alcGrams = drinks * 14.0;
          const wGrams = W_lbs * 453.592;
          const r = isMale ? 0.68 : 0.55;
          const beta = 0.015; // hourly metabolic burn

          const rawBac = (alcGrams / (wGrams * r)) * 100;
          const netBac = Math.max(0, rawBac - (beta * H));
          const timeSober = netBac > 0 ? (netBac / beta) : 0;

          setDisp('bac_percentage', netBac.toFixed(3) + '%');
          setDisp('legal_status', netBac >= 0.08 ? 'ILLEGAL (Over 0.08% Limit)' : 'Under Legal Limit');
          setDisp('hours_to_sober', timeSober.toFixed(1) + ' Hours Remaining');
          setDisp('alcohol_grams', alcGrams.toFixed(1) + ' grams');
        """
    },
    {
        "slug": "caffeine-half-life",
        "category": "health",
        "name": "Caffeine Half-Life & Sleep Clearance Calculator",
        "description": "Calculate remaining active bloodstream caffeine (mg) and clearance timeline based on CYP1A2 liver enzyme pharmacokinetics.",
        "hero_badge": "Pharmacokinetics • CYP1A2 Degradation Matrix",
        "formula_display": "Remaining Caffeine = Initial Dose × (0.5)^(Hours Elapsed / 5.0)",
        "fields": [
            {"id": "coffee_cups", "label": "Initial Caffeine Dose", "default": 200, "suffix": "mg", "min": 20, "max": 1000, "step": 10, "hint": "Mug of drip coffee ~150-200mg; Espresso shot ~65mg; Energy drink ~200mg"},
            {"id": "hours_elapsed", "label": "Hours Since Consumption", "default": 6, "suffix": "hrs", "min": 1, "max": 24, "step": 0.5, "hint": "Hours since your last sip of coffee/energy drink"}
        ],
        "metrics": [
            {"id": "remaining_caffeine", "label": "Active Circulating Caffeine", "default_display": "87.1 mg", "highlight": True},
            {"id": "sleep_disruption", "label": "Adenosine Receptor Blockade", "default_display": "Moderate disruption (Over 50mg active)"},
            {"id": "hours_to_trace", "label": "Time to Trace Level (<20mg)", "default_display": "16.6 Hours from Intake"},
            {"id": "quarter_life", "label": "Quarter-Life (25% Remaining)", "default_display": "10.0 Hours"}
        ],
        "proof_steps": [
            {"step_title": "First-Order Elimination Kinetics", "step_text": "Caffeine is metabolized by hepatic cytochrome P450 CYP1A2 enzymes following exponential decay: C(t) = C_0 · (0.5)^(t / t_half)."},
            {"step_title": "Elimination Half-Life Variation", "step_text": "In healthy adults, caffeine's elimination half-life averages 5.0 hours (range 3 to 7 hours). Oral contraceptives and pregnancy can double half-life to 10+ hours, while smoking accelerates clearance."},
            {"step_title": "Adenosine Receptor Antagonism", "step_text": "Caffeine competitively binds to adenosine A1 and A2A receptors in the brain, blocking the natural accumulation of sleep pressure. Having more than 25-50mg circulating at bedtime reduces Stage 3 slow-wave sleep by up to 30%."}
        ],
        "faqs": [
            {"q": "What is the caffeine curfew for good sleep?", "a": "Because caffeine has a 5-hour half-life and 10-hour quarter-life, neuroscientists recommend a caffeine cutoff 8 to 10 hours before your target bedtime (e.g., no caffeine after 1:00 PM for an 11:00 PM bedtime)."},
            {"q": "Why do some people fall asleep easily after coffee?", "a": "Genetic polymorphisms in the CYP1A2 gene categorize individuals as fast or slow metabolizers. However, even if 'fast metabolizers' fall asleep, EEG sleep studies show that caffeine fragments deep restorative slow-wave sleep."}
        ],
        "js_logic": """
          const dose = getNum('coffee_cups');
          const t = getNum('hours_elapsed');
          const halfLife = 5.0;

          const remaining = dose * Math.pow(0.5, t / halfLife);
          const timeTrace = dose > 20 ? (halfLife * (Math.log(dose / 20) / Math.log(2))) : 0;

          let status = 'Minimal Impact';
          if (remaining > 100) status = 'Severe Disruption (>100mg active)';
          else if (remaining > 50) status = 'Moderate Disruption (50-100mg active)';
          else if (remaining > 20) status = 'Mild Disruption (20-50mg active)';

          setDisp('remaining_caffeine', remaining.toFixed(1) + ' mg');
          setDisp('sleep_disruption', status);
          setDisp('hours_to_trace', timeTrace.toFixed(1) + ' Hours from Intake');
          setDisp('quarter_life', (halfLife * 2).toFixed(1) + ' Hours');
        """
    },
    {
        "slug": "keto-carb-limit",
        "category": "health",
        "name": "Keto Net Carbs & Ketogenic Ratio Calculator",
        "description": "Calculate daily net carbohydrate limits, total fiber deductions, and ketogenic macronutrient ratios (fat-to-protein+carb) for nutritional ketosis.",
        "hero_badge": "Biochemistry • Ketogenic Ratio Matrix",
        "formula_display": "Net Carbs = Total Carbohydrates - Dietary Fiber - Sugar Alcohols",
        "fields": [
            {"id": "daily_calories", "label": "Target Daily Calories", "default": 2000, "suffix": "kcal", "min": 1000, "max": 5000, "step": 50, "hint": "Daily caloric intake"},
            {"id": "net_carb_target", "label": "Net Carb Limit", "default": 25, "suffix": "g/day", "min": 15, "max": 50, "step": 5, "hint": "20-25g standard for guaranteed ketosis"},
            {"id": "protein_intake", "label": "Protein Target", "default": 110, "suffix": "g/day", "min": 50, "max": 250, "step": 5, "hint": "Moderate protein to prevent gluconeogenesis"}
        ],
        "metrics": [
            {"id": "fat_grams", "label": "Required Healthy Fats", "default_display": "162 g (1,460 kcal)", "highlight": True},
            {"id": "keto_ratio", "label": "Ketogenic Ratio (Fat : [Protein+Carb])", "default_display": "1.20 : 1.0 (Nutritional Ketosis)", "highlight": True},
            {"id": "carb_calorie_pct", "label": "Carbohydrate Calorie Share", "default_display": "5.0% of Total Calories"},
            {"id": "blood_ketone_range", "label": "Target Blood BHB Ketones", "default_display": "0.5 – 3.0 mmol/L"}
        ],
        "proof_steps": [
            {"step_title": "Net Carbohydrate Glycemic Impact", "step_text": "Insoluble and soluble dietary fibers pass unabsorbed through the small intestine without triggering insulin secretion: Net Carbs = Total Carbs - Dietary Fiber."},
            {"step_title": "Lipid Energy Balancing", "step_text": "Fats provide the remaining balance of caloric energy: Fat kcal = Total kcal - (Net Carbs × 4) - (Protein × 4). Fat grams = Fat kcal / 9."},
            {"step_title": "Withrow-Woodyatt Ketogenic Index", "step_text": "Ketogenic Ratio = Fat grams / (Protein grams + Net Carb grams). A ratio above 1.0 indicates steady nutritional ketosis; medical epilepsy diets target 3.0 to 4.0."}
        ],
        "faqs": [
            {"q": "What is the difference between total carbs and net carbs?", "a": "Total carbs include starches, sugars, and dietary fiber. Net carbs count only digestible carbohydrates that break down into glucose and trigger insulin."},
            {"q": "How long does it take to enter ketosis?", "a": "Restricting net carbs below 20-30 grams per day typically induces nutritional ketosis (blood beta-hydroxybutyrate ≥ 0.5 mmol/L) within 48 to 72 hours as hepatic glycogen stores deplete."}
        ],
        "js_logic": """
          const kcal = getNum('daily_calories');
          const carbs = getNum('net_carb_target') || 25;
          const prot = getNum('protein_intake') || 110;

          const carbKcal = carbs * 4;
          const protKcal = prot * 4;
          const fatKcal = Math.max(0, kcal - carbKcal - protKcal);
          const fatGrams = fatKcal / 9;

          const ratio = (prot + carbs) > 0 ? (fatGrams / (prot + carbs)) : 0;
          const carbPct = (carbKcal / kcal) * 100;

          setDisp('fat_grams', Math.round(fatGrams) + ' g (' + Math.round(fatKcal) + ' kcal)');
          setDisp('keto_ratio', ratio.toFixed(2) + ' : 1.0 (Nutritional Ketosis)');
          setDisp('carb_calorie_pct', carbPct.toFixed(1) + '% of Total Calories');
          setDisp('blood_ketone_range', '0.5 – 3.0 mmol/L');
        """
    },
    {
        "slug": "daily-protein",
        "category": "health",
        "name": "Daily Protein Requirement & Muscle Synthesis Calculator",
        "description": "Calculate optimal daily protein intake in grams and meals based on lean body mass, resistance training goals, and age-related anabolic resistance.",
        "hero_badge": "Sports Nutrition • Protein Synthesis Matrix",
        "formula_display": "Target Protein (g) = Body Weight (lbs) × Protein Density Factor (g/lb)",
        "fields": [
            {"id": "body_weight", "label": "Body Weight", "default": 175, "suffix": "lbs", "min": 80, "max": 400, "step": 1, "hint": "Current scale weight"},
            {"id": "activity_tier", "label": "Training Goal (0.8 Sedentary, 1.0 Hypertrophy, 1.2 Cut)", "default": 1.0, "min": 0.36, "max": 1.4, "step": 0.1, "hint": "1.0 g/lb standard for lifters; 1.2 g/lb during caloric cuts"}
        ],
        "metrics": [
            {"id": "daily_protein_g", "label": "Daily Protein Target", "default_display": "175 g / day", "highlight": True},
            {"id": "protein_per_meal", "label": "Per-Meal Bolus (4 Meals)", "default_display": "43.8 g / meal (3g Leucine)", "highlight": True},
            {"id": "protein_calories", "label": "Total Protein Calories", "default_display": "700 kcal (4 kcal/g)"},
            {"id": "rda_comparison", "label": "Comparison to FDA RDA (0.36 g/lb)", "default_display": "278% of basic survival RDA"}
        ],
        "proof_steps": [
            {"step_title": "Morton et al. Meta-Analysis Consensus", "step_text": "Extensive meta-analysis of 49 randomized controlled trials (British Journal of Sports Medicine) demonstrated that protein intakes beyond 1.62 g/kg (0.73 g/lb) to 2.2 g/kg (1.0 g/lb) maximize fat-free mass gains in resistance-trained individuals."},
            {"step_title": "Leucine Trigger and Anabolic Threshold", "step_text": "Muscle protein synthesis (MPS) is initiated via the mTORC1 pathway, requiring a per-meal threshold of approximately 2.7 to 3.5 grams of the essential amino acid leucine (found in ~30-40g high-quality whey/meat protein)."},
            {"step_title": "Hypocaloric Nitrogen Retention", "step_text": "During calorie deficits, protein demands elevate to 1.0 to 1.2 g/lb to prevent skeletal muscle catabolism."}
        ],
        "faqs": [
            {"q": "Can the body only absorb 30 grams of protein in one meal?", "a": "No, this is a persistent myth. Your gut absorbs virtually 100% of the amino acids you eat, even from a 100g steak; it simply digests and absorbs them over a longer timeframe of 5 to 8 hours."},
            {"q": "Does high protein intake damage healthy kidneys?", "a": "No. Decades of clinical trials in individuals with normal renal function show that high-protein diets (up to 1.5 g/lb) do not impair glomerular filtration rate or kidney health."}
        ],
        "js_logic": """
          const W = getNum('body_weight');
          const factor = getNum('activity_tier') || 1.0;

          const totalG = W * factor;
          const perMeal = totalG / 4;
          const kcal = totalG * 4;
          const rda = W * 0.36;
          const rdaPct = Math.round((totalG / rda) * 100);

          setDisp('daily_protein_g', Math.round(totalG) + ' g / day');
          setDisp('protein_per_meal', perMeal.toFixed(1) + ' g / meal (~3g Leucine)');
          setDisp('protein_calories', Math.round(kcal) + ' kcal (' + (factor * 2.20462).toFixed(2) + ' g/kg)');
          setDisp('rda_comparison', rdaPct + '% of basic survival RDA');
        """
    },
    {
        "slug": "smoking-cost",
        "category": "health",
        "name": "Smoking Cost & Pack-Years Health Calculator",
        "description": "Calculate lifetime financial cost, lost investment compound interest, and clinical pack-years lung cancer risk index from cigarette smoking.",
        "hero_badge": "Public Health & Finance • Pack-Year Matrix",
        "formula_display": "Pack-Years = (Cigarettes per Day / 20) × Years Smoked",
        "fields": [
            {"id": "packs_per_day", "label": "Packs Smoked per Day", "default": 1.0, "suffix": "packs/day", "min": 0.25, "max": 4, "step": 0.25, "hint": "1 pack = 20 cigarettes"},
            {"id": "cost_per_pack", "label": "Cost per Pack", "default": 9.50, "prefix": "$", "min": 5, "max": 20, "step": 0.5, "hint": "Average US pack price: $8 to $14"},
            {"id": "years_smoked", "label": "Years Smoked", "default": 15, "suffix": "yrs", "min": 1, "max": 60, "step": 1, "hint": "Total duration of smoking"}
        ],
        "metrics": [
            {"id": "annual_cash_cost", "label": "Annual Cash Out-of-Pocket", "default_display": "$3,467.50 / yr", "highlight": True},
            {"id": "lifetime_spent", "label": "Lifetime Cash Spent", "default_display": "$52,012.50"},
            {"id": "investment_lost", "label": "Opportunity Cost (8% S&P 500)", "default_display": "$94,150.00", "highlight": True},
            {"id": "pack_years_index", "label": "Clinical Pack-Years Index", "default_display": "15.0 Pack-Years (High Risk)"}
        ],
        "proof_steps": [
            {"step_title": "Direct Out-of-Pocket Cash Flow", "step_text": "Annual Cost = Packs per day × Cost per pack × 365. Lifetime Cash = Annual Cost × Years Smoked."},
            {"step_title": "Compound Opportunity Cost of Capital", "step_text": "Investing the annual expenditure into an S&P 500 index fund compounding at an annualized 8%: FV = PMT · [((1 + r)ⁿ - 1) / r]."},
            {"step_title": "Clinical Pack-Year Diagnostic Standard", "step_text": "Pack-Years = Packs/day × Years. The US Preventive Services Task Force (USPSTF) recommends annual low-dose CT lung screening for individuals with a 20+ pack-year history."}
        ],
        "faqs": [
            {"q": "What is a clinical 'pack-year'?", "a": "A pack-year is a standardized epidemiological measurement: smoking 1 pack per day for 1 year equals 1 pack-year. Smoking 2 packs per day for 10 years equals 20 pack-years."},
            {"q": "How quickly do lungs begin to heal after quitting smoking?", "a": "Within 2 weeks to 3 months, circulation and lung function increase up to 30%. Within 1 year, coronary heart disease risk drops to half that of a smoker. Within 10 years, lung cancer mortality risk drops by 50%."}
        ],
        "js_logic": """
          const packs = getNum('packs_per_day');
          const cost = getNum('cost_per_pack');
          const yrs = getNum('years_smoked');

          const annual = packs * cost * 365;
          const lifetime = annual * yrs;
          const r = 0.08;
          const fv = annual * ((Math.pow(1 + r, yrs) - 1) / r);
          const packYears = packs * yrs;

          setDisp('annual_cash_cost', '$' + annual.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' / yr');
          setDisp('lifetime_spent', '$' + Math.round(lifetime).toLocaleString());
          setDisp('investment_lost', '$' + Math.round(fv).toLocaleString());
          setDisp('pack_years_index', packYears.toFixed(1) + ' Pack-Years (' + (packYears >= 20 ? 'Screening Candidate' : 'Moderate Exposure') + ')');
        """
    },
    {
        "slug": "bench-press-pyramid",
        "category": "health",
        "name": "Bench Press Pyramid & Warm-Up Set Calculator",
        "description": "Calculate ascending and descending strength pyramid sets, progressive overload percentages, and plate loading per side for bench press.",
        "hero_badge": "Barbell Biomechanics • Pyramid Set Matrix",
        "formula_display": "Working Set = 1RM × Target Intensity% | Plate Weight = (Barbell Weight - 45 lbs) / 2",
        "fields": [
            {"id": "working_weight", "label": "Target Top Working Weight", "default": 225, "suffix": "lbs", "min": 65, "max": 600, "step": 5, "hint": "Weight for your heavy set of 5 reps"}
        ],
        "metrics": [
            {"id": "set1_warmup", "label": "Set 1: Barbell Only (10 reps)", "default_display": "45 lbs (Empty Bar)", "highlight": True},
            {"id": "set2_warmup", "label": "Set 2: 50% Load (6 reps)", "default_display": "115 lbs (35 lb plate / side)"},
            {"id": "set3_warmup", "label": "Set 3: 75% Load (3 reps)", "default_display": "170 lbs (1×45, 1×17.5 / side)"},
            {"id": "set4_working", "label": "Top Working Set (5 reps)", "default_display": "225 lbs (2×45 lb plates / side)", "highlight": True}
        ],
        "proof_steps": [
            {"step_title": "Neural Potentiation Without Fatigue", "step_text": "Warm-up pyramids potentiate motor unit recruitment via post-activation potentiation (PAP) while conserving intracellular adenosine triphosphate (ATP) and phosphocreatine."},
            {"step_title": "Pyramid Percentage Scaling", "step_text": "Set 1: 45 lbs (empty bar) × 10 reps. Set 2: 50% working load × 6 reps. Set 3: 75% working load × 3 reps. Set 4: 90% working load × 1 rep. Set 5: 100% working set × 5 reps."},
            {"step_title": "Barbell Plate Math Invariant", "step_text": "Olympic barbell = 45 lbs. Weight per side = (Total Weight - 45) / 2."}
        ],
        "faqs": [
            {"q": "Why should warm-up repetitions decrease as weight increases?", "a": "High repetitions with heavy weights deplete glycogen and generate lactic acid, reducing performance on your top working sets. Low-rep heavy warm-ups prime your central nervous system without causing metabolic fatigue."},
            {"q": "What rest interval is best between heavy working sets?", "a": "For maximum strength and complete ATP-CP restoration, rest 3 to 5 minutes between heavy multi-joint compound sets (squats, bench press, deadlifts)."}
        ],
        "js_logic": """
          const W = getNum('working_weight');

          const s2 = Math.round((W * 0.50) / 5) * 5;
          const s3 = Math.round((W * 0.75) / 5) * 5;
          const s4 = Math.round((W * 0.90) / 5) * 5;

          function plates(tot) {
            const side = Math.max(0, tot - 45) / 2;
            return tot + ' lbs (' + side.toFixed(1) + ' lbs/side)';
          }

          setDisp('set1_warmup', '45 lbs (Empty Olympic Bar)');
          setDisp('set2_warmup', plates(s2) + ' × 6 reps');
          setDisp('set3_warmup', plates(s3) + ' × 3 reps');
          setDisp('set4_working', plates(W) + ' × 5 reps');
        """
    },
    {
        "slug": "creatine-dosing",
        "category": "health",
        "name": "Creatine Monohydrate Dosing & Saturation Calculator",
        "description": "Calculate creatine monohydrate loading protocol (20g/day) vs maintenance dosing (5g/day) and intramuscular phosphocreatine saturation timeline.",
        "hero_badge": "Ergogenic Bio-Quant • Creatine Saturation Matrix",
        "formula_display": "Loading Dose = 0.3g / kg Body Weight / Day (or 20g/day) for 5-7 Days",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 180, "suffix": "lbs", "min": 90, "max": 400, "step": 1, "hint": "Current body weight"},
            {"id": "protocol_type", "label": "Protocol (1 Fast Loading 20g, 0 Daily Maintenance 5g)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 for 5-day fast load, 0 for steady daily intake"}
        ],
        "metrics": [
            {"id": "daily_dose", "label": "Prescribed Daily Dose", "default_display": "20.0 g / day (4 × 5g doses)", "highlight": True},
            {"id": "maintenance_dose", "label": "Long-Term Maintenance Dose", "default_display": "5.0 g / day (1 scoop)", "highlight": True},
            {"id": "saturation_days", "label": "Days to Full Intramuscular Saturation", "default_display": "5 to 7 Days", "highlight": True},
            {"id": "water_weight_gain", "label": "Est. Intracellular Water Retention", "default_display": "2.0 – 4.5 lbs (Hydration)"}
        ],
        "proof_steps": [
            {"step_title": "Intramuscular Phosphocreatine (PCr) Pool", "step_text": "Skeletal muscle stores approximately 120 mmol of creatine per kilogram of dry muscle. Supplementation elevates this pool by 20% to the biological ceiling of ~160 mmol/kg."},
            {"step_title": "Loading vs Continuous Dosing Kinetics", "step_text": "Loading protocol: 20g/day split into 4 equal 5g doses for 5 to 7 days achieves maximal PCr saturation within 1 week. Continuous protocol: 3 to 5g/day reaches identical saturation levels at day 28."},
            {"step_title": "Intracellular Osmotic Hydration", "step_text": "Creatine is an active cellular osmolyte, drawing water into muscle cells and expanding intracellular volume by 1 to 2 kg without extracellular edema."}
        ],
        "faqs": [
            {"q": "Do you need to cycle on and off creatine?", "a": "No. Peer-reviewed clinical safety trials spanning up to 5 continuous years show that uninterrupted creatine monohydrate supplementation does not downregulate natural creatine synthesis or harm health."},
            {"q": "What is the best time of day to take creatine?", "a": "Timing is secondary to consistent daily saturation. However, research suggests taking creatine post-workout alongside protein and carbohydrates slightly enhances cellular uptake via insulin-mediated transport."}
        ],
        "js_logic": """
          const W = getNum('weight_lbs');
          const isLoad = getNum('protocol_type') === 1;

          const wKg = W / 2.20462;
          const maint = Math.max(3, Math.min(10, Math.round(wKg * 0.05)));

          if (isLoad) {
            setDisp('daily_dose', '20.0 g / day (4 × 5g doses)');
            setDisp('saturation_days', '5 to 7 Days');
          } else {
            setDisp('daily_dose', maint.toFixed(1) + ' g / day (Single Dose)');
            setDisp('saturation_days', '28 Days (Continuous)');
          }

          setDisp('maintenance_dose', maint.toFixed(1) + ' g / day (' + (maint / 5).toFixed(1) + ' scoops)');
          setDisp('water_weight_gain', (W * 0.015).toFixed(1) + ' – ' + (W * 0.025).toFixed(1) + ' lbs (Intracellular)');
        """
    },
    {
        "slug": "blood-volume",
        "category": "health",
        "name": "Total Blood Volume (Nadler) Calculator",
        "description": "Calculate circulating total blood volume (TBV), plasma volume, and red cell mass using the clinical Nadler and Gilcher equations.",
        "hero_badge": "Hematology • Nadler Hemodynamic Matrix",
        "formula_display": "TBV (men) = 0.3669 × H³ + 0.03219 × W + 0.6041 (Liters)",
        "fields": [
            {"id": "weight_lbs", "label": "Body Weight", "default": 175, "suffix": "lbs", "min": 70, "max": 450, "step": 1, "hint": "Weight in pounds"},
            {"id": "height_in", "label": "Height", "default": 70, "suffix": "in", "min": 48, "max": 88, "step": 1, "hint": "Height in inches"},
            {"id": "gender_factor", "label": "Biological Sex (1 for Male, 0 for Female)", "default": 1, "min": 0, "max": 1, "step": 1, "hint": "1 for Male, 0 for Female"}
        ],
        "metrics": [
            {"id": "total_blood_liters", "label": "Total Circulating Blood Volume", "default_display": "5.32 Liters", "highlight": True},
            {"id": "plasma_volume", "label": "Plasma Volume (55%)", "default_display": "2.93 Liters"},
            {"id": "red_cell_mass", "label": "Red Blood Cell Mass (45%)", "default_display": "2.39 Liters"},
            {"id": "blood_pints", "label": "Volume in Pints (Donation units)", "default_display": "11.2 Pints"}
        ],
        "proof_steps": [
            {"step_title": "Nadler's Dimensional Hemodynamic Model", "step_text": "Formulated by Dr. S.B. Nadler in 1962: Men: TBV = 0.3669 × H(m)³ + 0.03219 × W(kg) + 0.6041. Women: TBV = 0.3561 × H(m)³ + 0.03308 × W(kg) + 0.1833."},
            {"step_title": "Height-Cubed Volumetric Scaling", "step_text": "Because vascular tree capacity scales with three-dimensional body stature, height is cubed rather than squared, providing superior accuracy over simple body surface area (BSA) models."},
            {"step_title": "Hematocrit Partitioning", "step_text": "Normal venous hematocrit partitions blood volume into ~55% liquid plasma and ~45% cellular formed elements (erythrocytes)."}
        ],
        "faqs": [
            {"q": "How much blood can a person safely donate?", "a": "A standard whole blood donation collects exactly 1 pint (~500 mL), representing roughly 8% to 10% of total circulating blood volume. The body replaces plasma fluid within 24 to 48 hours and red blood cells within 4 to 6 weeks."},
            {"q": "What percentage of body weight is blood?", "a": "Blood accounts for approximately 7% to 8% of an adult's total body weight (roughly 70 mL of blood per kilogram in males and 65 mL/kg in females)."}
        ],
        "js_logic": """
          const W_lbs = getNum('weight_lbs');
          const H_in = getNum('height_in');
          const isMale = getNum('gender_factor') === 1;

          const wKg = W_lbs / 2.20462;
          const hM = (H_in * 2.54) / 100;

          const tbv = isMale ?
            (0.3669 * Math.pow(hM, 3)) + (0.03219 * wKg) + 0.6041 :
            (0.3561 * Math.pow(hM, 3)) + (0.03308 * wKg) + 0.1833;

          const plasma = tbv * 0.55;
          const rbc = tbv * 0.45;
          const pints = tbv * 2.11338;

          setDisp('total_blood_liters', tbv.toFixed(2) + ' Liters');
          setDisp('plasma_volume', plasma.toFixed(2) + ' Liters (55%)');
          setDisp('red_cell_mass', rbc.toFixed(2) + ' Liters (45%)');
          setDisp('blood_pints', pints.toFixed(1) + ' Pints');
        """
    },
    {
        "slug": "mean-arterial-pressure",
        "category": "health",
        "name": "Mean Arterial Pressure (MAP) Calculator",
        "description": "Calculate Mean Arterial Pressure (MAP) and organ perfusion adequacy from systolic and diastolic blood pressure readings.",
        "hero_badge": "Hemodynamics • Perfusion Pressure Matrix",
        "formula_display": "MAP = Diastolic BP + [1/3 × (Systolic BP - Diastolic BP)]",
        "fields": [
            {"id": "systolic_bp", "label": "Systolic Blood Pressure (SBP)", "default": 120, "suffix": "mmHg", "min": 60, "max": 240, "step": 1, "hint": "Top number (peak ventricular contraction)"},
            {"id": "diastolic_bp", "label": "Diastolic Blood Pressure (DBP)", "default": 80, "suffix": "mmHg", "min": 40, "max": 140, "step": 1, "hint": "Bottom number (ventricular relaxation)"}
        ],
        "metrics": [
            {"id": "map_value", "label": "Mean Arterial Pressure", "default_display": "93.3 mmHg", "highlight": True},
            {"id": "pulse_pressure", "label": "Pulse Pressure (SBP - DBP)", "default_display": "40.0 mmHg", "highlight": True},
            {"id": "perfusion_status", "label": "Organ Perfusion Adequacy", "default_display": "Optimal Perfusion (70 - 105 mmHg)"},
            {"id": "cardiac_cycle_split", "label": "Cardiac Cycle Weighting", "default_display": "67% Diastole / 33% Systole"}
        ],
        "proof_steps": [
            {"step_title": "Time-Weighted Cardiac Pressure Integral", "step_text": "Because the human heart spends approximately two-thirds of the cardiac cycle in diastole and one-third in systole at resting heart rates, the arithmetic mean is weighted: MAP = [SBP + (2 × DBP)] / 3 = DBP + ⅓(SBP - DBP)."},
            {"step_title": "Pulse Pressure Invariant", "step_text": "Pulse Pressure PP = SBP - DBP. Pulse pressures consistently above 60 mmHg reflect increased arterial stiffness and cardiovascular disease risk."},
            {"step_title": "Critical Organ Perfusion Threshold", "step_text": "In critical care medicine, a MAP of at least 65 mmHg is mandatory to maintain adequate capillary perfusion to vital organs (kidneys, brain, coronary arteries)."}
        ],
        "faqs": [
            {"q": "What is considered a normal MAP range?", "a": "A normal resting MAP is between 70 and 100 mmHg. A MAP consistently below 65 mmHg indicates hypoperfusion/shock, while a MAP above 105 mmHg indicates hypertension."},
            {"q": "Why is MAP more clinically useful than systolic blood pressure alone?", "a": "Systolic pressure fluctuates dramatically with stress, caffeine, and arterial wave reflections. MAP represents the true steady-state driving pressure delivering oxygenated blood across microvascular capillary beds."}
        ],
        "js_logic": """
          const sbp = getNum('systolic_bp');
          const dbp = getNum('diastolic_bp');

          const pp = sbp - dbp;
          const map = dbp + (pp / 3);

          let status = 'Optimal Perfusion';
          if (map < 65) status = 'Hypoperfusion Risk (< 65 mmHg)';
          else if (map > 105) status = 'Hypertensive State (> 105 mmHg)';

          setDisp('map_value', map.toFixed(1) + ' mmHg');
          setDisp('pulse_pressure', pp.toFixed(1) + ' mmHg');
          setDisp('perfusion_status', status);
          setDisp('cardiac_cycle_split', '67% Diastole / 33% Systole');
        """
    }
]
