"""
scripts/data_biotech_pharma.py
25 High-Value Biotechnology, Pharmacology, Clinical Trials & Laboratory Medicine Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

BIOTECH_CALCULATORS = [
    {
        "slug": "drug-elimination-half-life",
        "category": "biotech",
        "name": "Pharmacokinetics Drug Elimination Half-Life (t½) & Clearance Calculator",
        "description": "Calculate elimination rate constant (ke), elimination half-life (t½), systemic drug clearance (CL), and time to steady state accumulation or 99% elimination.",
        "hero_badge": "Pharmacokinetics • Drug Metabolism",
        "formula_display": "t½ = ln(2) / ke ≈ 0.693 / ke | ke = CL / Vd | t_99% = 6.64 · t½",
        "fields": [
            {"id": "volume_of_distribution_vd", "label": "Volume of Distribution (Vd in Liters)", "default": 42.0, "suffix": "L", "min": 1.0, "max": 1000, "step": 1.0, "hint": "Apparent physiological volume into which drug distributes"},
            {"id": "systemic_clearance_cl", "label": "Systemic Clearance (CL in L/hour)", "default": 3.5, "suffix": "L/hr", "min": 0.1, "max": 100, "step": 0.1, "hint": "Volume of plasma cleared of drug per unit time (hepatic + renal)"},
            {"id": "initial_peak_concentration_c0", "label": "Peak Plasma Concentration (C₀ in mg/L)", "default": 25.0, "suffix": "mg/L", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Maximum post-infusion or absorption plasma level"},
            {"id": "elapsed_time_hours", "label": "Elapsed Post-Dose Time (Hours)", "default": 12.0, "suffix": "hours", "min": 0.5, "max": 168, "step": 0.5, "hint": "Hours following dose administration"}
        ],
        "metrics": [
            {"id": "elimination_half_life_hours", "label": "Elimination Half-Life (t½)", "default_display": "8.32 Hours", "highlight": True},
            {"id": "elimination_rate_constant_ke", "label": "Elimination Rate Constant (ke)", "default_display": "0.0833 hr⁻¹", "highlight": True},
            {"id": "plasma_concentration_at_time_t", "label": "Remaining Plasma Level C(t)", "default_display": "9.20 mg/L", "highlight": True},
            {"id": "time_to_complete_washout", "label": "Time to 97% Elimination (5 t½)", "default_display": "41.6 Hours (5 Half-Lives)"}
        ],
        "proof_steps": [
            {"step_title": "First-Order Elimination Rate Constant", "step_text": "ke = Systemic Clearance (CL) / Volume of Distribution (Vd) = 3.5 L/hr / 42.0 L = 0.08333 hr⁻¹."},
            {"step_title": "Half-Life (t½) Derivation", "step_text": "t½ = ln(2) / ke = 0.69315 / 0.08333 hr⁻¹ = 8.318 ≈ 8.32 hours."},
            {"step_title": "Exponential Plasma Decay Equation", "step_text": "C(t) = C₀ · e^(-ke · t) = 25.0 mg/L · e^(-0.08333 × 12) = 25.0 · e^(-1.000) = 25.0 · 0.3679 = 9.20 mg/L."},
            {"step_title": "Clinical Washout & Steady-State Rule", "step_text": "In clinical pharmacology, 5 half-lives (5 × 8.32 = 41.6 hours) eliminates 96.88% of the drug, representing complete therapeutic washout or time to steady-state plateau during continuous dosing."}
        ],
        "faqs": [
            {"q": "What is the difference between clearance and half-life?", "a": "Clearance (CL) is the true physiological organ capacity (liver and kidneys) to remove drug from the blood per unit time. Half-life (t½) is a dependent hybrid parameter determined by both clearance and how widely the drug distributes throughout tissue (Vd)."},
            {"q": "How many half-lives until a drug is completely gone from the body?", "a": "After 1 half-life, 50% remains; after 3.3 half-lives, 90% is cleared; after 5 half-lives, 97% is cleared; and after 7 half-lives, 99.2% is eliminated."}
        ],
        "js_logic": """
          const vd = getNum('volume_of_distribution_vd');
          const cl = getNum('systemic_clearance_cl');
          const c0 = getNum('initial_peak_concentration_c0');
          const t = getNum('elapsed_time_hours');

          if (vd > 0 && cl > 0) {
            const ke = cl / vd;
            const thalf = Math.log(2) / ke;
            const ct = c0 * Math.exp(-ke * t);
            const washout = 5 * thalf;

            setMetric('elimination_half_life_hours', thalf.toFixed(2) + ' Hours');
            setMetric('elimination_rate_constant_ke', ke.toFixed(4) + ' hr⁻¹');
            setMetric('plasma_concentration_at_time_t', ct.toFixed(2) + ' mg/L');
            setMetric('time_to_complete_washout', washout.toFixed(1) + ' Hours (5 Half-Lives)');
          }
        """
    },
    {
        "slug": "cockcroft-gault-crcl",
        "category": "biotech",
        "name": "Cockcroft-Gault Creatinine Clearance (CrCl) & Renal Dosing Calculator",
        "description": "Calculate estimated Creatinine Clearance (CrCl) via the standard Cockcroft-Gault equation for clinical pharmacokinetic drug dosing and renal impairment staging.",
        "hero_badge": "Clinical Pharmacology • Renal Function",
        "formula_display": "CrCl (Male) = [(140 - Age) · Weight (kg)] / (72 · SCr) | CrCl (Female) = CrCl (Male) · 0.85",
        "fields": [
            {"id": "patient_age_years", "label": "Patient Age (Years)", "default": 65, "suffix": "years", "min": 18, "max": 110, "step": 1, "hint": "Adult patient age"},
            {"id": "patient_weight_kg", "label": "Actual Body Weight (kg)", "default": 72.0, "suffix": "kg", "min": 30, "max": 250, "step": 1, "hint": "Patient weight in kilograms (1 lb = 0.4536 kg)"},
            {"id": "serum_creatinine_mg_dl", "label": "Serum Creatinine (SCr in mg/dL)", "default": 1.40, "suffix": "mg/dL", "min": 0.2, "max": 15.0, "step": 0.05, "hint": "Laboratory serum creatinine concentration"},
            {"id": "patient_sex_biological", "label": "Biological Sex (1=Male, 0=Female)", "default": 1, "suffix": "1=M, 0=F", "min": 0, "max": 1, "step": 1, "hint": "Female factor multiplies result by 0.85 due to lower average muscle mass"}
        ],
        "metrics": [
            {"id": "estimated_crcl_ml_min", "label": "Estimated Creatinine Clearance (CrCl)", "default_display": "53.6 mL/min", "highlight": True},
            {"id": "ckd_renal_impairment_stage", "label": "Renal Function Impairment Classification", "default_display": "Moderate Renal Impairment (30-59 mL/min)", "highlight": True},
            {"id": "cleared_volume_24hr", "label": "Daily Filtered Blood Plasma", "default_display": "77.1 Liters / Day", "highlight": True},
            {"id": "dosing_adjustment_alert", "label": "FDA Renal Dosing Advisory", "default_display": "Dose Reduction Required for Renally Cleared Drugs"}
        ],
        "proof_steps": [
            {"step_title": "Numerator Product", "step_text": "Numerator = (140 - Age) × Weight (kg) = (140 - 65) × 72.0 = 75 × 72.0 = 5,400."},
            {"step_title": "Denominator Serum Creatinine Product", "step_text": "Denominator = 72 × Serum Creatinine (1.40 mg/dL) = 100.8."},
            {"step_title": "Base Male Creatinine Clearance", "step_text": "CrCl = 5,400 / 100.8 = 53.57 mL/min (if female, multiply by 0.85 = 45.54 mL/min)."},
            {"step_title": "Clinical Dosing Classification", "step_text": "A CrCl of 53.6 mL/min indicates moderate renal impairment (Stage 3). Common renally cleared antibiotics (e.g. Vancomycin, Levofloxacin, Cefepime) require extended dosing intervals or 25-50% dose reductions."}
        ],
        "faqs": [
            {"q": "Why does the FDA mandate Cockcroft-Gault over eGFR (CKD-EPI) for drug dosing?", "a": "Most pharmaceutical clinical trials and drug package inserts historically established renal dosage adjustments using Cockcroft-Gault CrCl (mL/min) rather than body-surface-adjusted eGFR (mL/min/1.73m²)."},
            {"q": "When should Ideal Body Weight (IBW) be used instead of actual weight?", "a": "In significantly obese patients (BMI ≥ 30 kg/m²), using actual weight overestimates renal clearance because adipose tissue does not produce creatinine. Clinicians typically substitute Ideal Body Weight (IBW) or Adjusted Body Weight (AdjBW)."}
        ],
        "js_logic": """
          const age = getNum('patient_age_years');
          const wt = getNum('patient_weight_kg');
          const scr = getNum('serum_creatinine_mg_dl');
          const isMale = getNum('patient_sex_biological');

          if (scr > 0 && wt > 0) {
            let crcl = ((140 - age) * wt) / (72 * scr);
            if (isMale === 0) crcl *= 0.85;

            const dailyLiters = (crcl * 60 * 24) / 1000;

            let stage = 'Severe Renal Impairment (< 30 mL/min)';
            let advisory = 'Major Dose Reduction Required (50-75% cut)';
            if (crcl >= 90) {
              stage = 'Normal Renal Function (≥ 90 mL/min)';
              advisory = 'Standard Full Dose Permitted';
            } else if (crcl >= 60 && crcl < 90) {
              stage = 'Mild Renal Impairment (60-89 mL/min)';
              advisory = 'Standard Dose; Monitor Trough Levels';
            } else if (crcl >= 30 && crcl < 60) {
              stage = 'Moderate Renal Impairment (30-59 mL/min)';
              advisory = 'Dose Reduction Required for Renally Cleared Drugs';
            }

            setMetric('estimated_crcl_ml_min', crcl.toFixed(1) + ' mL/min');
            setMetric('ckd_renal_impairment_stage', stage);
            setMetric('cleared_volume_24hr', dailyLiters.toFixed(1) + ' Liters / Day');
            setMetric('dosing_adjustment_alert', advisory);
          }
        """
    },
    {
        "slug": "iv-drip-infusion-rate",
        "category": "biotech",
        "name": "IV Drip Rate & Infusion Velocity Calculator",
        "description": "Calculate electronic IV infusion pump rates in mL/hr and gravity drip rates in drops per minute (gtt/min) across macrodrip and microdrip tubing sets.",
        "hero_badge": "Clinical Nursing • IV Pharmacology",
        "formula_display": "Infusion Rate = Total Volume (mL) / Infusion Time (Hours) | Drip Rate (gtt/min) = [Volume (mL) · Drip Factor] / Time (Minutes)",
        "fields": [
            {"id": "prescribed_iv_volume_ml", "label": "Prescribed IV Fluid Volume (mL)", "default": 1000, "suffix": "mL", "min": 10, "max": 5000, "step": 50, "hint": "Total infusion volume (e.g. 0.9% Normal Saline or D5W)"},
            {"id": "infusion_duration_hours", "label": "Infusion Duration (Hours)", "default": 8.0, "suffix": "hours", "min": 0.25, "max": 72, "step": 0.5, "hint": "Target run time ordered by physician"},
            {"id": "iv_tubing_drip_factor", "label": "Tubing Drip Factor (gtt/mL)", "default": 15, "suffix": "gtt/mL", "min": 10, "max": 60, "step": 5, "hint": "Standard macrodrip is 10, 15, or 20 gtt/mL; pediatric microdrip is 60 gtt/mL"}
        ],
        "metrics": [
            {"id": "pump_rate_ml_hr", "label": "Electronic Pump Flow Rate", "default_display": "125.0 mL/hr", "highlight": True},
            {"id": "gravity_drip_rate_gtt_min", "label": "Gravity Drip Rate (Drops/Min)", "default_display": "31 gtt/min", "highlight": True},
            {"id": "seconds_per_drop", "label": "Timing Cadence Per Drop", "default_display": "1 Drop Every 1.9 Seconds", "highlight": True},
            {"id": "total_infused_drops", "label": "Total Cumulative Drops", "default_display": "15,000 Drops"}
        ],
        "proof_steps": [
            {"step_title": "Electronic Volumetric Pump Rate", "step_text": "Hourly Flow Rate = Volume (1,000 mL) / Time (8.0 hours) = 125.0 mL/hour."},
            {"step_title": "Time Conversion to Minutes", "step_text": "Total Minutes = 8.0 hours × 60 minutes/hr = 480 minutes."},
            {"step_title": "Gravity Drip Rate (gtt/min)", "step_text": "Drip Rate = (1,000 mL × 15 gtt/mL) / 480 minutes = 15,000 drops / 480 minutes = 31.25 ≈ 31 drops/minute."},
            {"step_title": "Bedside Counting Interval", "step_text": "Interval = 60 seconds / 31.25 drops = 1.92 seconds per drop (count ~8 drops every 15 seconds at the bedside chamber)."}
        ],
        "faqs": [
            {"q": "What is the difference between macrodrip and microdrip tubing sets?", "a": "Macrodrip sets deliver 10, 15, or 20 drops per mL and are used for adult fluid resuscitation. Microdrip sets deliver exactly 60 drops per mL and are used for pediatric, ICU, and precise medication infusions."},
            {"q": "What does 'gtt' stand for?", "a": "'gtt' is the standard pharmaceutical abbreviation for the Latin word 'guttae', meaning drops."}
        ],
        "js_logic": """
          const vol = getNum('prescribed_iv_volume_ml');
          const hrs = getNum('infusion_duration_hours');
          const factor = getNum('iv_tubing_drip_factor');

          if (hrs > 0) {
            const mlHr = vol / hrs;
            const totalMins = hrs * 60;
            const gttMin = (vol * factor) / totalMins;
            const secPerDrop = gttMin > 0 ? (60 / gttMin) : 0;
            const totalDrops = vol * factor;

            setMetric('pump_rate_ml_hr', mlHr.toFixed(1) + ' mL/hr');
            setMetric('gravity_drip_rate_gtt_min', Math.round(gttMin) + ' gtt/min');
            setMetric('seconds_per_drop', '1 Drop Every ' + secPerDrop.toFixed(1) + ' Seconds');
            setMetric('total_infused_drops', Math.round(totalDrops).toLocaleString() + ' Drops');
          }
        """
    },
    {
        "slug": "pcr-primer-tm",
        "category": "biotech",
        "name": "PCR Primer Melting Temperature (Tm) & Annealing Calculator",
        "description": "Calculate DNA oligonucleotide PCR primer melting temperature (Tm) via the Wallace 2+4 rule and nearest-neighbor thermodynamics, and determine optimal annealing temperature (Ta).",
        "hero_badge": "Molecular Biology • PCR Design",
        "formula_display": "Tm (Wallace) = 2 · (A + T) + 4 · (G + C) | Optimal Annealing Ta ≈ Tm_primer - 5°C",
        "fields": [
            {"id": "primer_length_bp", "label": "Primer Length (Base Pairs)", "default": 22, "suffix": "bp", "min": 10, "max": 50, "step": 1, "hint": "Typical PCR primers are 18-25 nucleotides long"},
            {"id": "gc_nucleotide_count", "label": "Number of G and C Bases", "default": 11, "suffix": "bases", "min": 0, "max": 50, "step": 1, "hint": "Number of Guanine (G) and Cytosine (C) residues"},
            {"id": "monovalent_salt_concentration_mm", "label": "Monovalent Cation [Na⁺/K⁺] (mM)", "default": 50, "suffix": "mM", "min": 10, "max": 500, "step": 5, "hint": "Standard PCR buffer contains 50 mM KCl"}
        ],
        "metrics": [
            {"id": "basic_wallace_tm", "label": "Basic Wallace Rule Tm", "default_display": "66.0°C", "highlight": True},
            {"id": "salt_adjusted_tm", "label": "Salt-Adjusted Primer Tm", "default_display": "60.4°C", "highlight": True},
            {"id": "optimal_pcr_annealing_ta", "label": "Recommended Annealing Temp (Ta)", "default_display": "55.4°C (Tm - 5°C)", "highlight": True},
            {"id": "gc_content_percentage", "label": "Primer GC Content (%)", "default_display": "50.0% GC"}
        ],
        "proof_steps": [
            {"step_title": "AT Base Pair Deduction", "step_text": "Total Length = 22 bp. GC Count = 11. AT Count = 22 - 11 = 11 bases. GC Content = (11 / 22) × 100 = 50.0%."},
            {"step_title": "Wallace Rule (Simple Heuristic)", "step_text": "Tm = 2 × (A + T) + 4 × (G + C) = 2 × (11) + 4 × (11) = 22 + 44 = 66.0°C."},
            {"step_title": "Salt-Corrected Melting Temperature", "step_text": "Tm(adjusted) = 64.9 + 41 × (GC - 16.4) / Length + 16.6 × log₁₀([Na⁺]/1000) = 64.9 + 41 × (11 - 16.4)/22 + 16.6 × log₁₀(0.05) = 60.4°C."},
            {"step_title": "Recommended Thermal Cycler Annealing Temperature", "step_text": "Ta = Tm(adjusted) - 5.0°C = 60.4°C - 5.0°C = 55.4°C. Setting Ta 5°C below primer Tm ensures high specificity while promoting robust primer-template duplex hybridization."}
        ],
        "faqs": [
            {"q": "What is the optimal GC content for PCR primers?", "a": "The ideal GC content is 40% to 60%, with a 'GC clamp' (1-2 G or C bases at the 3' end) to ensure strong thermal binding where DNA polymerase initiates synthesis."},
            {"q": "What happens if the PCR annealing temperature is set too low or too high?", "a": "If Ta is set too low, primers bind non-specifically to off-target sequences, producing messy artifact bands. If Ta is set too high, primers fail to hybridize to the template, resulting in zero PCR product."}
        ],
        "js_logic": """
          const len = getNum('primer_length_bp');
          const gc = getNum('gc_nucleotide_count');
          const salt = getNum('monovalent_salt_concentration_mm');

          const at = Math.max(0, len - gc);
          const gcPct = len > 0 ? (gc / len) * 100 : 0;
          const wallace = (2 * at) + (4 * gc);

          let saltTm = wallace;
          if (len > 0) {
            const naM = salt / 1000;
            saltTm = 64.9 + (41 * (gc - 16.4) / len) + (16.6 * Math.log10(naM));
          }
          const ta = saltTm - 5.0;

          setMetric('basic_wallace_tm', wallace.toFixed(1) + '°C');
          setMetric('salt_adjusted_tm', saltTm.toFixed(1) + '°C');
          setMetric('optimal_pcr_annealing_ta', ta.toFixed(1) + '°C (Tm - 5°C)');
          setMetric('gc_content_percentage', gcPct.toFixed(1) + '% GC');
        """
    },
    {
        "slug": "michaelis-menten-kinetics",
        "category": "biotech",
        "name": "Michaelis-Menten Enzyme Kinetics & Lineweaver-Burk Calculator",
        "description": "Calculate steady-state enzyme reaction velocity (v), maximum velocity (Vmax), Michaelis constant (Km), and double-reciprocal Lineweaver-Burk coordinates.",
        "hero_badge": "Enzymology • Enzyme Kinetics",
        "formula_display": "v = (Vmax · [S]) / (Km + [S]) | 1/v = (Km / Vmax) · (1/[S]) + (1 / Vmax)",
        "fields": [
            {"id": "substrate_concentration_s", "label": "Substrate Concentration [S] (μM)", "default": 25.0, "suffix": "μM", "min": 0.1, "max": 10000, "step": 1.0, "hint": "Concentration of reaction substrate in assay"},
            {"id": "max_reaction_velocity_vmax", "label": "Maximum Velocity Vmax (μmol/min)", "default": 120.0, "suffix": "μmol/min", "min": 1.0, "max": 10000, "step": 5.0, "hint": "Asymptotic maximum rate at enzyme substrate saturation"},
            {"id": "michaelis_constant_km", "label": "Michaelis Constant Km (μM)", "default": 15.0, "suffix": "μM", "min": 0.1, "max": 5000, "step": 0.5, "hint": "Substrate concentration at which velocity is exactly half of Vmax"}
        ],
        "metrics": [
            {"id": "reaction_velocity_v", "label": "Enzymatic Reaction Rate (v)", "default_display": "75.0 μmol/min", "highlight": True},
            {"id": "saturation_fraction_pct", "label": "Enzyme Active Site Saturation", "default_display": "62.5% of Vmax", "highlight": True},
            {"id": "lineweaver_burk_reciprocal_v", "label": "Lineweaver-Burk 1/v Coordinate", "default_display": "0.0133 min/μmol", "highlight": True},
            {"id": "lineweaver_burk_reciprocal_s", "label": "Lineweaver-Burk 1/[S] Coordinate", "default_display": "0.0400 μM⁻¹"}
        ],
        "proof_steps": [
            {"step_title": "Michaelis-Menten Hyperbolic Rate Law", "step_text": "v = (Vmax × [S]) / (Km + [S]) = (120.0 × 25.0) / (15.0 + 25.0) = 3,000 / 40.0 = 75.0 μmol/min."},
            {"step_title": "Active Site Fractional Occupancy", "step_text": "Fractional Saturation = v / Vmax = [S] / (Km + [S]) = 25.0 / 40.0 = 0.625 (62.5% of active sites occupied)."},
            {"step_title": "Lineweaver-Burk Double Reciprocal Coordinates", "step_text": "1/[S] = 1 / 25.0 μM = 0.0400 μM⁻¹. 1/v = 1 / 75.0 = 0.0133 min/μmol."},
            {"step_title": "Biochemical Interpretation", "step_text": "Because [S] (25 μM) > Km (15 μM), the enzyme operates in the mixed zero-order transition regime where velocity increases non-linearly toward Vmax."}
        ],
        "faqs": [
            {"q": "What does a low Km signify in enzyme kinetics?", "a": "A low Km indicates high enzyme affinity for its substrate, meaning very little substrate is required to achieve half-maximal catalytic velocity."},
            {"q": "How does a competitive inhibitor alter Km and Vmax?", "a": "A competitive inhibitor increases apparent Km (requiring more substrate to reach half-speed) but does not change Vmax, because high substrate concentrations displace the inhibitor."}
        ],
        "js_logic": """
          const s = getNum('substrate_concentration_s');
          const vmax = getNum('max_reaction_velocity_vmax');
          const km = getNum('michaelis_constant_km');

          if ((km + s) > 0 && s > 0 && vmax > 0) {
            const v = (vmax * s) / (km + s);
            const satPct = (v / vmax) * 100;
            const invV = 1 / v;
            const invS = 1 / s;

            setMetric('reaction_velocity_v', v.toFixed(1) + ' μmol/min');
            setMetric('saturation_fraction_pct', satPct.toFixed(1) + '% of Vmax');
            setMetric('lineweaver_burk_reciprocal_v', invV.toFixed(4) + ' min/μmol');
            setMetric('lineweaver_burk_reciprocal_s', invS.toFixed(4) + ' μM⁻¹');
          }
        """
    },
    {
        "slug": "body-surface-area-mosteller",
        "category": "biotech",
        "name": "Body Surface Area (BSA) Calculator (Mosteller & Du Bois Formulas)",
        "description": "Calculate adult and pediatric Body Surface Area (BSA in m²) via the Mosteller and Du Bois formulas for oncology chemotherapy dosing and hemodynamic index calculations.",
        "hero_badge": "Clinical Oncology • BSA Dosing",
        "formula_display": "BSA (Mosteller) = √[(Height (cm) · Weight (kg)) / 3600] | BSA (Du Bois) = 0.007184 · H^0.725 · W^0.425",
        "fields": [
            {"id": "patient_height_cm", "label": "Patient Height (Centimeters)", "default": 175.0, "suffix": "cm", "min": 40, "max": 240, "step": 1, "hint": "1 inch = 2.54 cm (e.g. 5'9\" = 175 cm)"},
            {"id": "patient_weight_kg", "label": "Patient Weight (Kilograms)", "default": 75.0, "suffix": "kg", "min": 2, "max": 300, "step": 1, "hint": "1 lb = 0.4536 kg (e.g. 165 lbs = 75 kg)"},
            {"id": "chemo_protocol_dose_per_m2", "label": "Chemotherapy Protocol Dose (mg/m²)", "default": 75.0, "suffix": "mg/m²", "min": 1, "max": 2000, "step": 5, "hint": "Standard protocol dose (e.g. Cisplatin or Doxorubicin)"}
        ],
        "metrics": [
            {"id": "bsa_mosteller_m2", "label": "Body Surface Area (Mosteller)", "default_display": "1.91 m²", "highlight": True},
            {"id": "bsa_dubois_m2", "label": "Body Surface Area (Du Bois)", "default_display": "1.90 m²", "highlight": True},
            {"id": "individualized_chemo_dose", "label": "Calculated Patient Chemotherapy Dose", "default_display": "143.3 mg Total", "highlight": True},
            {"id": "bsa_demographic_norm", "label": "Standard Reference Comparison", "default_display": "Average Adult Reference (1.7 - 2.0 m²)"}
        ],
        "proof_steps": [
            {"step_title": "Mosteller Square Root Formula", "step_text": "BSA = √[(Height × Weight) / 3,600] = √[(175 × 75) / 3,600] = √[13,125 / 3,600] = √3.6458 = 1.909 ≈ 1.91 m²."},
            {"step_title": "Du Bois & Du Bois Power Law Check", "step_text": "BSA = 0.007184 × Height^0.725 × Weight^0.425 = 0.007184 × (175^0.725) × (75^0.425) = 0.007184 × 42.50 × 6.22 = 1.898 ≈ 1.90 m²."},
            {"step_title": "Chemotherapy Dose Individualization", "step_text": "Total Prescribed Dose = BSA (1.91 m²) × Protocol Dose (75.0 mg/m²) = 143.25 ≈ 143.3 mg total dose."},
            {"step_title": "Clinical Safety Margin", "step_text": "Dosing by BSA rather than body weight accounts for metabolic rate scaling, minimizing toxicity in cytotoxic therapies."}
        ],
        "faqs": [
            {"q": "Why is the Mosteller formula preferred over Du Bois in modern clinical practice?", "a": "The Mosteller formula produces virtually identical results to the complex Du Bois exponential equation while requiring only simple multiplication and square root, making it less prone to bedside calculation errors."},
            {"q": "What is the average human adult BSA?", "a": "The widely accepted average adult BSA is 1.73 m² (typically 1.6 m² for women and 1.9 m² for men)."}
        ],
        "js_logic": """
          const h = getNum('patient_height_cm');
          const w = getNum('patient_weight_kg');
          const dosePerM2 = getNum('chemo_protocol_dose_per_m2');

          if (h > 0 && w > 0) {
            const mosteller = Math.sqrt((h * w) / 3600);
            const dubois = 0.007184 * Math.pow(h, 0.725) * Math.pow(w, 0.425);
            const totalDose = mosteller * dosePerM2;

            setMetric('bsa_mosteller_m2', mosteller.toFixed(2) + ' m²');
            setMetric('bsa_dubois_m2', dubois.toFixed(2) + ' m²');
            setMetric('individualized_chemo_dose', totalDose.toFixed(1) + ' mg Total');
            setMetric('bsa_demographic_norm', mosteller >= 1.7 && mosteller <= 2.0 ? 'Average Adult Reference (1.7 - 2.0 m²)' : (mosteller < 1.7 ? 'Small Adult / Pediatric (< 1.7 m²)' : 'Large Adult (> 2.0 m²)'));
          }
        """
    },
    {
        "slug": "serial-dilution-c1v1",
        "category": "biotech",
        "name": "Laboratory Serial Dilution & Stock Solution Concentration (C₁V₁ = C₂V₂) Calculator",
        "description": "Calculate stock solution volume, buffer diluent required, and multi-step serial dilution ratios for molecular biology, chemistry, and pharmacology bench work.",
        "hero_badge": "Wet Lab Chemistry • Dilution Math",
        "formula_display": "C₁ · V₁ = C₂ · V₂ | V_diluent = V₂ - V₁ | Dilution Factor = C₁ / C₂ = V₂ / V₁",
        "fields": [
            {"id": "stock_concentration_c1", "label": "Initial Stock Concentration (C₁)", "default": 10.0, "suffix": "M or mg/mL", "min": 0.001, "max": 10000, "step": 0.5, "hint": "Concentration of concentrated stock chemical"},
            {"id": "desired_final_concentration_c2", "label": "Desired Target Concentration (C₂)", "default": 0.25, "suffix": "M or mg/mL", "min": 0.0001, "max": 5000, "step": 0.05, "hint": "Concentration needed in experimental working solution"},
            {"id": "final_working_volume_v2", "label": "Desired Final Volume (V₂ in mL)", "default": 100.0, "suffix": "mL", "min": 0.1, "max": 10000, "step": 5, "hint": "Total final volume needed for experiment"}
        ],
        "metrics": [
            {"id": "required_stock_volume_v1", "label": "Stock Volume to Pipette (V₁)", "default_display": "2.50 mL", "highlight": True},
            {"id": "required_buffer_volume", "label": "Buffer Diluent Volume to Add", "default_display": "97.50 mL", "highlight": True},
            {"id": "dilution_factor_ratio", "label": "Dilution Factor", "default_display": "1 : 40 (40× Dilution)", "highlight": True},
            {"id": "stock_consumption_pct", "label": "Stock Solution Share", "default_display": "2.5% of Final Volume"}
        ],
        "proof_steps": [
            {"step_title": "Conservation of Solute Mass", "step_text": "C₁ · V₁ = C₂ · V₂ => V₁ = (C₂ · V₂) / C₁."},
            {"step_title": "Required Stock Pipette Volume", "step_text": "V₁ = (0.25 × 100.0 mL) / 10.0 = 25.0 / 10.0 = 2.50 mL of stock solution."},
            {"step_title": "Diluent Buffer Addition", "step_text": "V_diluent = V₂ - V₁ = 100.0 mL - 2.50 mL = 97.50 mL of deionized water or assay buffer."},
            {"step_title": "Dilution Ratio Factor", "step_text": "Dilution Factor = C₁ / C₂ = 10.0 / 0.25 = 40× (a 1:40 dilution)."}
        ],
        "faqs": [
            {"q": "Does C₁V₁ = C₂V₂ work with any units?", "a": "Yes, as long as C₁ and C₂ share the exact same concentration units (e.g. mM to mM, mg/mL to mg/mL) and V₁ and V₂ share the same volume units (e.g. mL to mL, μL to μL)."},
            {"q": "What is the difference between a 1:10 dilution and a 1 to 10 dilution?", "a": "In laboratory convention, a 1:10 dilution means 1 part stock plus 9 parts diluent for a total of 10 parts (a 10-fold dilution). Always confirm whether the ratio specifies stock:diluent or stock:total."}
        ],
        "js_logic": """
          const c1 = getNum('stock_concentration_c1');
          const c2 = getNum('desired_final_concentration_c2');
          const v2 = getNum('final_working_volume_v2');

          if (c1 > 0 && c2 > 0 && v2 > 0 && c1 >= c2) {
            const v1 = (c2 * v2) / c1;
            const vDiluent = v2 - v1;
            const factor = c1 / c2;
            const stockShare = (v1 / v2) * 100;

            setMetric('required_stock_volume_v1', v1.toFixed(2) + ' mL');
            setMetric('required_buffer_volume', vDiluent.toFixed(2) + ' mL');
            setMetric('dilution_factor_ratio', '1 : ' + Math.round(factor) + ' (' + factor.toFixed(1) + '× Dilution)');
            setMetric('stock_consumption_pct', stockShare.toFixed(1) + '% of Final Volume');
          }
        """
    },
    {
        "slug": "cell-culture-doubling-time",
        "category": "biotech",
        "name": "In Vitro Cell Culture Doubling Time & Specific Growth Rate Calculator",
        "description": "Calculate mammalian and bacterial cell culture doubling time (Td), specific growth rate constant (μ), and cumulative fold expansion across passage intervals.",
        "hero_badge": "Cell Biology • Cell Proliferation",
        "formula_display": "Doubling Time Td = [t · ln(2)] / ln(Nt / N₀) | Growth Rate μ = ln(Nt / N₀) / t",
        "fields": [
            {"id": "initial_seeded_cell_count", "label": "Initial Seeded Cell Count (N₀)", "default": 500000, "suffix": "cells", "min": 1000, "max": 100000000, "step": 25000, "hint": "Cells seeded into flask at start of passage"},
            {"id": "final_harvested_cell_count", "label": "Harvested Final Cell Count (Nt)", "default": 4200000, "suffix": "cells", "min": 1000, "max": 500000000, "step": 50000, "hint": "Total cells counted at harvesting/trypsinization"},
            {"id": "culture_growth_time_hours", "label": "Culture Duration (Hours)", "default": 48.0, "suffix": "hours", "min": 1, "max": 336, "step": 1, "hint": "Elapsed incubation time"}
        ],
        "metrics": [
            {"id": "cell_doubling_time_hours", "label": "Cell Doubling Time (Td)", "default_display": "15.65 Hours", "highlight": True},
            {"id": "specific_growth_rate_mu", "label": "Specific Growth Rate (μ)", "default_display": "0.0443 hr⁻¹", "highlight": True},
            {"id": "total_cell_fold_expansion", "label": "Cumulative Fold Expansion", "default_display": "8.40× Expansion", "highlight": True},
            {"id": "total_population_doublings", "label": "Number of Population Doublings", "default_display": "3.07 Doublings"}
        ],
        "proof_steps": [
            {"step_title": "Fold Proliferation Multiplier", "step_text": "Fold Expansion = Nt / N₀ = 4,200,000 / 500,000 = 8.40×."},
            {"step_title": "Population Doublings (PD)", "step_text": "Doublings = log₂(Nt / N₀) = ln(8.40) / ln(2) = 2.1282 / 0.69315 = 3.07 doublings."},
            {"step_title": "Doubling Time (Td)", "step_text": "Td = Culture Duration (48.0 hours) / Doublings (3.07) = 15.65 hours per cell division cycle."},
            {"step_title": "Specific Growth Rate Constant (μ)", "step_text": "μ = ln(Nt / N₀) / t = 2.1282 / 48.0 = 0.04434 hr⁻¹ (confirming Td = ln(2) / μ = 0.69315 / 0.04434 = 15.65 hours)."}
        ],
        "faqs": [
            {"q": "What is the typical doubling time for human cell lines?", "a": "Standard cancer and immortalized cell lines (e.g. HEK293, HeLa) double every 18 to 24 hours. Primary human fibroblasts double every 24 to 36 hours, while bacterial cultures (E. coli) can double every 20 minutes under optimal nutrient conditions."},
            {"q": "Why does doubling time increase as cultures reach confluence?", "a": "As cells fill the flask surface, contact inhibition and nutrient depletion force cells out of active M-phase division into G0 quiescence, slowing the apparent doubling rate."}
        ],
        "js_logic": """
          const n0 = getNum('initial_seeded_cell_count');
          const nt = getNum('final_harvested_cell_count');
          const t = getNum('culture_growth_time_hours');

          if (n0 > 0 && nt > n0 && t > 0) {
            const ratio = nt / n0;
            const doublings = Math.log(ratio) / Math.log(2);
            const td = t / doublings;
            const mu = Math.log(ratio) / t;

            setMetric('cell_doubling_time_hours', td.toFixed(2) + ' Hours');
            setMetric('specific_growth_rate_mu', mu.toFixed(4) + ' hr⁻¹');
            setMetric('total_cell_fold_expansion', ratio.toFixed(2) + '× Expansion');
            setMetric('total_population_doublings', doublings.toFixed(2) + ' Doublings');
          }
        """
    },
    {
        "slug": "beer-lambert-spectrophotometry",
        "category": "biotech",
        "name": "Beer-Lambert Law Spectrophotometry & Protein Concentration Calculator",
        "description": "Calculate solute molar concentration, absorbance (A), and percent transmittance (%T) using the Beer-Lambert spectrophotometric absorption law.",
        "hero_badge": "Biochemistry • UV-Vis Spectroscopy",
        "formula_display": "A = ε · l · c | c = A / (ε · l) | %T = 10^(2 - A)",
        "fields": [
            {"id": "measured_absorbance_a", "label": "Measured Absorbance (OD Units)", "default": 0.650, "suffix": "OD", "min": 0.001, "max": 3.0, "step": 0.005, "hint": "Spectrophotometer reading (linear range: 0.1 to 1.5)"},
            {"id": "molar_extinction_coefficient_e", "label": "Molar Extinction Coefficient ε (M⁻¹ cm⁻¹)", "default": 43824, "suffix": "M⁻¹ cm⁻¹", "min": 100, "max": 500000, "step": 500, "hint": "Protein/nucleic acid molar absorptivity (e.g. BSA at 280 nm = 43,824)"},
            {"id": "cuvette_path_length_l", "label": "Cuvette Path Length (cm)", "default": 1.0, "suffix": "cm", "min": 0.1, "max": 5.0, "step": 0.1, "hint": "Standard UV cuvette optical path length is 1.0 cm (NanoDrop is 0.1 cm)"}
        ],
        "metrics": [
            {"id": "molar_solute_concentration", "label": "Molar Concentration (c)", "default_display": "14.83 μM (0.0148 mM)", "highlight": True},
            {"id": "protein_mass_concentration", "label": "Protein Mass Concentration (BSA)", "default_display": "0.985 mg/mL", "highlight": True},
            {"id": "percent_transmittance_pct", "label": "Transmittance (%T)", "default_display": "22.39% Transmitted", "highlight": True},
            {"id": "spectrophotometer_linearity_check", "label": "Photometric Linearity Status", "default_display": "Optimal Linear Range (0.1 - 1.0 OD)"}
        ],
        "proof_steps": [
            {"step_title": "Beer-Lambert Law Inversion", "step_text": "c = A / (ε · l) = 0.650 / (43,824 M⁻¹ cm⁻¹ × 1.0 cm) = 0.650 / 43,824 = 1.483 × 10⁻⁵ M = 14.83 μM."},
            {"step_title": "Protein Mass Concentration Conversion", "step_text": "For Bovine Serum Albumin (MW ≈ 66,430 g/mol): Mass Conc = 1.483 × 10⁻⁵ mol/L × 66,430 g/mol = 0.985 g/L = 0.985 mg/mL."},
            {"step_title": "Percent Transmittance Derivation", "step_text": "%T = 10^(2 - A) = 10^(2 - 0.650) = 10^1.350 = 22.39% light transmitted through sample."},
            {"step_title": "Photometric Accuracy Verification", "step_text": "An absorbance of 0.650 falls within the sweet spot of photomultiplier detector linearity (0.1 to 1.0 OD), avoiding stray-light saturation artifacts."}
        ],
        "faqs": [
            {"q": "Why does the Beer-Lambert law fail at high absorbance (> 2.0)?", "a": "At high solute concentrations (> 2.0 OD), less than 1% of light reaches the detector. Stray light and electrostatic interactions between closely packed chromophores cause deviations from linearity."},
            {"q": "What is the standard wavelength for measuring nucleic acids and proteins?", "a": "Nucleic acids (DNA/RNA) have peak aromatic ring absorption at 260 nm (A260). Proteins absorb at 280 nm (A280) due to tryptophan, tyrosine, and phenylalanine residues."}
        ],
        "js_logic": """
          const a = getNum('measured_absorbance_a');
          const e = getNum('molar_extinction_coefficient_e');
          const l = getNum('cuvette_path_length_l');

          if (e > 0 && l > 0) {
            const molar = a / (e * l);
            const uM = molar * 1000000;
            const bsaMgMl = molar * 66430;
            const pctT = Math.pow(10, 2 - a);

            let lin = 'Optimal Linear Range (0.1 - 1.0 OD)';
            if (a < 0.1) lin = 'Low Signal (Consider Concentrating)';
            else if (a > 1.2 && a <= 2.0) lin = 'High OD (Dilution Recommended)';
            else if (a > 2.0) lin = 'Non-Linear Saturation (Must Dilute Sample)';

            setMetric('molar_solute_concentration', uM.toFixed(2) + ' μM (' + (molar * 1000).toFixed(4) + ' mM)');
            setMetric('protein_mass_concentration', bsaMgMl.toFixed(3) + ' mg/mL');
            setMetric('percent_transmittance_pct', pctT.toFixed(2) + '% Transmitted');
            setMetric('spectrophotometer_linearity_check', lin);
          }
        """
    },
    {
        "slug": "hemocytometer-cell-viability",
        "category": "biotech",
        "name": "Hemocytometer Cell Count & Trypan Blue Viability Calculator",
        "description": "Calculate total cell concentration (cells/mL), percentage viability from Trypan blue dye exclusion, and total yield for bioreactors and culture flasks.",
        "hero_badge": "Laboratory Protocols • Cell Counting",
        "formula_display": "Concentration = (Live Cells / Squares) · Dilution · 10⁴ cells/mL | % Viability = [Live / (Live + Dead)] · 100",
        "fields": [
            {"id": "live_viable_cells_counted", "label": "Viable Live Cells Counted (Clear)", "default": 180, "suffix": "cells", "min": 1, "max": 2000, "step": 5, "hint": "Cells excluding Trypan blue dye across counted grid squares"},
            {"id": "dead_nonviable_cells_counted", "label": "Non-Viable Dead Cells Counted (Blue)", "default": 20, "suffix": "cells", "min": 0, "max": 1000, "step": 1, "hint": "Cells stained blue due to compromised membrane"},
            {"id": "large_grid_squares_counted", "label": "Number of Large Squares Counted (1 mm²)", "default": 4, "suffix": "squares", "min": 1, "max": 9, "step": 1, "hint": "Typically 4 corner squares of Neubauer hemocytometer"},
            {"id": "trypan_dilution_factor", "label": "Dilution Factor (e.g. 1:1 Trypan Blue = 2×)", "default": 2.0, "suffix": "×", "min": 1.0, "max": 100, "step": 0.5, "hint": "1:1 cell suspension to dye ratio equals a 2× dilution"},
            {"id": "original_cell_suspension_volume_ml", "label": "Total Harvest Suspension Volume (mL)", "default": 15.0, "suffix": "mL", "min": 0.1, "max": 5000, "step": 0.5, "hint": "Total volume of cell pellet suspension"}
        ],
        "metrics": [
            {"id": "viable_cell_concentration_per_ml", "label": "Viable Cell Concentration", "default_display": "9.00 × 10⁵ cells/mL", "highlight": True},
            {"id": "cell_viability_percentage", "label": "Culture Viability (%)", "default_display": "90.0% Viable", "highlight": True},
            {"id": "total_viable_cell_yield", "label": "Total Harvest Cell Yield", "default_display": "1.35 × 10⁷ Total Cells", "highlight": True},
            {"id": "average_cells_per_square", "label": "Average Density Per Square", "default_display": "45.0 Cells / Square (Optimal)"}
        ],
        "proof_steps": [
            {"step_title": "Trypan Blue Dye Exclusion Viability", "step_text": "Total Counted = Live (180) + Dead (20) = 200 cells. Viability % = (180 / 200) × 100 = 90.0%."},
            {"step_title": "Neubauer Chamber Volume Constant", "step_text": "Each 1 mm × 1 mm square with a 0.1 mm depth represents exactly 0.1 mm³ = 10⁻⁴ mL. Therefore, the multiplication factor is 10⁴."},
            {"step_title": "Concentration Derivation", "step_text": "Concentration = (180 live cells / 4 squares) × 2.0 dilution × 10⁴ = 45.0 × 2 × 10,000 = 900,000 cells/mL (9.00 × 10⁵ cells/mL)."},
            {"step_title": "Total Harvest Yield", "step_text": "Total Viable Cells = 9.00 × 10⁵ cells/mL × 15.0 mL suspension = 13,500,000 cells (1.35 × 10⁷ cells)."}
        ],
        "faqs": [
            {"q": "What is the optimal cell count per large square on a hemocytometer?", "a": "For maximum statistical precision without counting fatigue, aim for 20 to 50 cells per 1 mm² large square. If squares contain > 100 cells, dilute the sample; if < 15 cells, concentrate the cell pellet."},
            {"q": "Why must Trypan blue counting be completed within 3 to 5 minutes?", "a": "Trypan blue is cytotoxic over extended exposure. After 10-15 minutes, viable cells begin absorbing the dye, creating false non-viable readings."}
        ],
        "js_logic": """
          const live = getNum('live_viable_cells_counted');
          const dead = getNum('dead_nonviable_cells_counted');
          const squares = getNum('large_grid_squares_counted');
          const dil = getNum('trypan_dilution_factor');
          const vol = getNum('original_cell_suspension_volume_ml');

          const totalCounted = live + dead;
          if (squares > 0 && totalCounted > 0) {
            const viability = (live / totalCounted) * 100;
            const avgPerSq = live / squares;
            const conc = avgPerSq * dil * 10000;
            const totalCells = conc * vol;

            let avgStatus = 'Optimal Density (20-50/sq)';
            if (avgPerSq < 20) avgStatus = 'Low Density (< 20/sq, consider concentrating)';
            else if (avgPerSq > 70) avgStatus = 'High Density (> 70/sq, consider diluting)';

            setMetric('viable_cell_concentration_per_ml', conc.toExponential(2) + ' cells/mL');
            setMetric('cell_viability_percentage', viability.toFixed(1) + '% Viable');
            setMetric('total_viable_cell_yield', totalCells.toExponential(2) + ' Total Cells');
            setMetric('average_cells_per_square', avgPerSq.toFixed(1) + ' Cells / Sq (' + avgStatus + ')');
          }
        """
    },
    {
        "slug": "henderson-hasselbalch-ph",
        "category": "biotech",
        "name": "Henderson-Hasselbalch Buffer pH & Acid-Base Equilibrium Calculator",
        "description": "Calculate aqueous buffer solution pH, conjugate acid-base equilibrium ratios, and buffer capacity using the Henderson-Hasselbalch equation.",
        "hero_badge": "Physical Biochemistry • Buffer Systems",
        "formula_display": "pH = pKa + log₁₀([A⁻] / [HA]) | [A⁻] / [HA] = 10^(pH - pKa)",
        "fields": [
            {"id": "acid_dissociation_constant_pka", "label": "Acid Dissociation Constant (pKa)", "default": 4.76, "suffix": "pKa", "min": 1.0, "max": 14.0, "step": 0.05, "hint": "pKa of weak acid (e.g. Acetic Acid = 4.76; Phosphate pKa2 = 7.20)"},
            {"id": "conjugate_base_concentration", "label": "Conjugate Base [A⁻] (Molar M)", "default": 0.150, "suffix": "M", "min": 0.001, "max": 5.0, "step": 0.01, "hint": "Concentration of deprotonated salt (e.g. Sodium Acetate)"},
            {"id": "weak_acid_concentration", "label": "Weak Acid [HA] (Molar M)", "default": 0.100, "suffix": "M", "min": 0.001, "max": 5.0, "step": 0.01, "hint": "Concentration of protonated acid (e.g. Acetic Acid)"}
        ],
        "metrics": [
            {"id": "calculated_buffer_ph", "label": "Equilibrium Solution pH", "default_display": "4.94 pH", "highlight": True},
            {"id": "base_to_acid_ratio", "label": "Conjugate Base to Acid Ratio [A⁻]/[HA]", "default_display": "1.50 : 1", "highlight": True},
            {"id": "effective_buffer_capacity_range", "label": "Effective Buffering Range (pKa ± 1)", "default_display": "pH 3.76 to 5.76", "highlight": True},
            {"id": "buffer_efficacy_rating", "label": "Buffering Capacity Status", "default_display": "High Buffering Capacity (Near pKa)"}
        ],
        "proof_steps": [
            {"step_title": "Conjugate Base to Acid Ratio", "step_text": "Ratio = [A⁻] / [HA] = 0.150 M / 0.100 M = 1.50."},
            {"step_title": "Logarithmic Ratio Component", "step_text": "log₁₀(1.50) = +0.176."},
            {"step_title": "Henderson-Hasselbalch Solution pH", "step_text": "pH = pKa + log₁₀([A⁻]/[HA]) = 4.76 + 0.176 = 4.936 ≈ 4.94 pH."},
            {"step_title": "Buffer Capacity Rule", "step_text": "A buffer is chemically effective within ±1.0 pH unit of its pKa (pH 3.76 to 5.76). Operating at pH 4.94 is within 0.18 units of the pKa, ensuring excellent resistance to both acid and base titration shocks."}
        ],
        "faqs": [
            {"q": "What happens when [A⁻] equals [HA]?", "a": "When conjugate base and weak acid concentrations are exactly equal, [A⁻]/[HA] = 1, and log₁₀(1) = 0. Therefore, pH = pKa. This represents the point of maximum buffer capacity."},
            {"q": "What is the primary buffer system that maintains human physiological blood pH at 7.40?", "a": "The carbonic acid-bicarbonate buffer system (H₂CO₃ / HCO₃⁻), which has a pKa of 6.1 and maintains a 20:1 ratio of bicarbonate to carbonic acid via respiratory CO₂ venting and renal bicarbonate retention."}
        ],
        "js_logic": """
          const pka = getNum('acid_dissociation_constant_pka');
          const base = getNum('conjugate_base_concentration');
          const acid = getNum('weak_acid_concentration');

          if (base > 0 && acid > 0) {
            const ratio = base / acid;
            const logRatio = Math.log10(ratio);
            const ph = pka + logRatio;
            const minRange = pka - 1.0;
            const maxRange = pka + 1.0;

            let rating = 'High Buffering Capacity (Near pKa)';
            if (Math.abs(ph - pka) > 1.0) rating = 'Poor Buffering (Outside pKa ± 1 Range)';

            setMetric('calculated_buffer_ph', ph.toFixed(2) + ' pH');
            setMetric('base_to_acid_ratio', ratio.toFixed(2) + ' : 1');
            setMetric('effective_buffer_capacity_range', 'pH ' + minRange.toFixed(2) + ' to ' + maxRange.toFixed(2));
            setMetric('buffer_efficacy_rating', rating);
          }
        """
    },
    {
        "slug": "centrifuge-rcf-g-force",
        "category": "biotech",
        "name": "Centrifuge Relative Centrifugal Force (RCF / g-Force) & RPM Calculator",
        "description": "Convert between rotational speed (RPM) and Relative Centrifugal Force (RCF in ×g) using exact rotor radius geometry to reproduce centrifugation protocols.",
        "hero_badge": "Laboratory Centrifugation • RCF Math",
        "formula_display": "RCF (×g) = 1.118 × 10⁻⁵ · r_cm · (RPM)² | RPM = √[RCF / (1.118 × 10⁻⁵ · r_cm)]",
        "fields": [
            {"id": "centrifuge_rotor_speed_rpm", "label": "Rotational Speed (RPM)", "default": 14000, "suffix": "RPM", "min": 100, "max": 100000, "step": 250, "hint": "Rotor revolutions per minute"},
            {"id": "rotor_radius_centimeters", "label": "Rotor Radius (r in cm)", "default": 8.5, "suffix": "cm", "min": 1.0, "max": 50.0, "step": 0.5, "hint": "Distance from center of centrifuge spindle to bottom of tube bucket"}
        ],
        "metrics": [
            {"id": "relative_centrifugal_force_rcf", "label": "Relative Centrifugal Force (RCF)", "default_display": "18,624 ×g", "highlight": True},
            {"id": "tangential_linear_velocity", "label": "Tube Tangential Velocity", "default_display": "124.6 m/s (448.6 km/h)", "highlight": True},
            {"id": "protocol_centrifugation_tier", "label": "Centrifugation Application Tier", "default_display": "Microcentrifuge (DNA / RNA / Protein Pelleting)"},
            {"id": "radius_variance_factor", "label": "Rotor Radius Metric", "default_display": "85 mm Radius"}
        ],
        "proof_steps": [
            {"step_title": "Centrifugal Acceleration Formula", "step_text": "Centrifugal acceleration a = ω² · r, where angular velocity ω = 2π · RPM / 60. Normalizing to Earth gravity (g = 9.80665 m/s²) yields the constant 1.118 × 10⁻⁵."},
            {"step_title": "RCF Calculation", "step_text": "RCF = 1.118 × 10⁻⁵ × Radius (8.5 cm) × (14,000 RPM)² = 1.118 × 10⁻⁵ × 8.5 × 196,000,000 = 18,624.76 ≈ 18,625 ×g."},
            {"step_title": "Peripheral Speed", "step_text": "Linear Velocity v = (2π · 8.5 cm / 100) × (14,000 / 60) = 0.534 m × 233.33 rev/s = 124.6 m/s (448.6 km/h)."},
            {"step_title": "Protocol Reproducibility Rule", "step_text": "Scientific protocols must always specify g-force (RCF), never RPM alone. Running 14,000 RPM on a larger 12 cm rotor produces 26,295 ×g (+41% higher force), potentially lysing delicate organelles."}
        ],
        "faqs": [
            {"q": "Why is it dangerous to report centrifugation speeds in RPM?", "a": "RPM describes only how fast the rotor spins, ignoring the physical size of the rotor. Two centrifuges running at the same 5,000 RPM will exert drastically different forces if one has an 8 cm rotor (2,236 ×g) and the other has a 16 cm rotor (4,472 ×g)."},
            {"q": "What is the difference between r_min, r_av, and r_max in centrifuge rotors?", "a": "r_min is the distance from the spindle to the liquid surface, r_max is the distance to the tube tip, and r_av is the midpoint. RCF is typically reported at r_max (pellet force)."}
        ],
        "js_logic": """
          const rpm = getNum('centrifuge_rotor_speed_rpm');
          const r = getNum('rotor_radius_centimeters');

          if (rpm > 0 && r > 0) {
            const rcf = 0.00001118 * r * Math.pow(rpm, 2);
            const vMs = (2 * Math.PI * (r / 100) * (rpm / 60));
            const vKmh = vMs * 3.6;

            let tier = 'Low-Speed Clinical (Blood / Cell Separation)';
            if (rcf >= 10000 && rcf < 30000) tier = 'Microcentrifuge (DNA / RNA / Protein Pelleting)';
            else if (rcf >= 30000 && rcf < 100000) tier = 'High-Speed Subcellular Fractionation';
            else if (rcf >= 100000) tier = 'Ultracentrifugation (Ribosomes / Viruses)';

            setMetric('relative_centrifugal_force_rcf', Math.round(rcf).toLocaleString() + ' ×g');
            setMetric('tangential_linear_velocity', vMs.toFixed(1) + ' m/s (' + vKmh.toFixed(1) + ' km/h)');
            setMetric('protocol_centrifugation_tier', tier);
            setMetric('radius_variance_factor', (r * 10).toFixed(0) + ' mm Radius');
          }
        """
    },
    {
        "slug": "clinical-trial-sample-size",
        "category": "biotech",
        "name": "Clinical Trial Sample Size & Statistical Power Calculator",
        "description": "Calculate required patient sample size per treatment arm for superiority randomized controlled trials (RCTs) based on statistical power, alpha, and effect size.",
        "hero_badge": "Biostatistics • Clinical Trial Design",
        "formula_display": "N_arm = 2 · (Z_α/2 + Z_β)² · p̄(1 - p̄) / (p₁ - p₂)²",
        "fields": [
            {"id": "control_group_event_rate_p1", "label": "Control Group Response Rate (p₁ in %)", "default": 20.0, "suffix": "%", "min": 1.0, "max": 90.0, "step": 1.0, "hint": "Expected baseline response rate or historical control"},
            {"id": "experimental_event_rate_p2", "label": "Experimental Group Target Rate (p₂ in %)", "default": 35.0, "suffix": "%", "min": 2.0, "max": 99.0, "step": 1.0, "hint": "Clinically meaningful target response rate for new drug"},
            {"id": "type_1_error_alpha_pct", "label": "Significance Level α (Two-Tailed %)", "default": 5.0, "suffix": "% (α=0.05)", "min": 1.0, "max": 10.0, "step": 1.0, "hint": "Standard medical threshold is α = 0.05 (Z = 1.96)"},
            {"id": "statistical_power_pct", "label": "Statistical Power (1 - β %)", "default": 80.0, "suffix": "% (Power)", "min": 70.0, "max": 99.0, "step": 5.0, "hint": "Probability of detecting a true difference (typically 80% or 90%)"},
            {"id": "anticipated_dropout_rate_pct", "label": "Anticipated Patient Dropout Rate (%)", "default": 15.0, "suffix": "%", "min": 0, "max": 40, "step": 1, "hint": "Patients lost to follow-up over trial duration"}
        ],
        "metrics": [
            {"id": "required_sample_size_per_arm", "label": "Sample Size Per Treatment Arm", "default_display": "138 Patients / Arm", "highlight": True},
            {"id": "total_evaluable_trial_n", "label": "Total Evaluable Patients (2 Arms)", "default_display": "276 Patients", "highlight": True},
            {"id": "total_recruitment_enrollment", "label": "Target Enrollment (With Dropout Buffer)", "default_display": "326 Total Recruits", "highlight": True},
            {"id": "absolute_treatment_effect_delta", "label": "Target Effect Size (Absolute Delta)", "default_display": "+15.0% Difference"}
        ],
        "proof_steps": [
            {"step_title": "Standard Normal Critical Values", "step_text": "For two-tailed α = 0.05: Z_α/2 = 1.960. For 80% statistical power (β = 0.20): Z_β = 0.842. (Z_α/2 + Z_β)² = (1.960 + 0.842)² = (2.802)² = 7.851."},
            {"step_title": "Pooled Variance Proportions", "step_text": "p₁ = 0.20, p₂ = 0.35. Pooled mean p̄ = (0.20 + 0.35) / 2 = 0.275. Variance factor = 2 · p̄(1 - p̄) = 2 × 0.275 × 0.725 = 0.39875."},
            {"step_title": "Per-Arm Sample Size Equation", "step_text": "N_arm = [7.851 × 0.39875] / (0.35 - 0.20)² = 3.1306 / (0.15)² = 3.1306 / 0.0225 = 139.1 ≈ 138 patients per arm."},
            {"step_title": "Attrition & Dropout Buffer", "step_text": "Total needed = 138 × 2 arms = 276 evaluable patients. With 15% dropout: Total Enrolled = 276 / (1 - 0.15) = 324.7 ≈ 326 total patients to recruit."}
        ],
        "faqs": [
            {"q": "What is the consequence of an underpowered clinical trial?", "a": "An underpowered study (e.g. 50% power) has a high probability of committing a Type II error (false negative), causing a genuinely effective, lifesaving drug to fail statistical significance and be abandoned."},
            {"q": "Why is statistical power typically set to 80% instead of 99%?", "a": "Increasing power from 80% to 99% quadruples the required patient sample size, dramatically increasing clinical trial cost and multi-year patient enrollment timelines."}
        ],
        "js_logic": """
          const p1 = getNum('control_group_event_rate_p1') / 100;
          const p2 = getNum('experimental_event_rate_p2') / 100;
          const alpha = getNum('type_1_error_alpha_pct');
          const power = getNum('statistical_power_pct');
          const dropPct = getNum('anticipated_dropout_rate_pct') / 100;

          const delta = Math.abs(p2 - p1);
          if (delta > 0) {
            let zAlpha = 1.96;
            if (alpha <= 1) zAlpha = 2.576;
            else if (alpha <= 2) zAlpha = 2.326;
            else if (alpha <= 5) zAlpha = 1.960;
            else zAlpha = 1.645;

            let zBeta = 0.842;
            if (power >= 95) zBeta = 1.645;
            else if (power >= 90) zBeta = 1.282;
            else if (power >= 85) zBeta = 1.036;
            else if (power >= 80) zBeta = 0.842;
            else zBeta = 0.524;

            const pBar = (p1 + p2) / 2;
            const numerator = Math.pow(zAlpha + zBeta, 2) * (2 * pBar * (1 - pBar));
            const nArm = Math.ceil(numerator / Math.pow(delta, 2));
            const totalEvaluable = nArm * 2;
            const totalRecruit = Math.ceil(totalEvaluable / (1 - dropPct));

            setMetric('required_sample_size_per_arm', nArm + ' Patients / Arm');
            setMetric('total_evaluable_trial_n', totalEvaluable + ' Patients');
            setMetric('total_recruitment_enrollment', totalRecruit + ' Total Recruits');
            setMetric('absolute_treatment_effect_delta', '+' + (delta * 100).toFixed(1) + '% Difference');
          }
        """
    },
    {
        "slug": "hazard-ratio-relative-risk",
        "category": "biotech",
        "name": "Hazard Ratio (HR), Relative Risk (RR) & Odds Ratio (OR) Calculator",
        "description": "Calculate clinical evidence metrics including Relative Risk (RR), Relative Risk Reduction (RRR), Absolute Risk Reduction (ARR), and Number Needed to Treat (NNT).",
        "hero_badge": "Evidence-Based Medicine • Clinical Epidemiology",
        "formula_display": "RR = (a / n₁) / (c / n₂) | ARR = CER - EER | NNT = 1 / ARR",
        "fields": [
            {"id": "experimental_event_count_a", "label": "Experimental Group Events (a)", "default": 35, "suffix": "events", "min": 0, "max": 10000, "step": 1, "hint": "Patients experiencing primary outcome in treatment arm"},
            {"id": "experimental_total_count_n1", "label": "Experimental Group Total Sample (n₁)", "default": 500, "suffix": "patients", "min": 10, "max": 100000, "step": 10, "hint": "Total patients in experimental treatment arm"},
            {"id": "control_event_count_c", "label": "Control / Placebo Events (c)", "default": 70, "suffix": "events", "min": 0, "max": 10000, "step": 1, "hint": "Patients experiencing primary outcome in placebo arm"},
            {"id": "control_total_count_n2", "label": "Control Group Total Sample (n₂)", "default": 500, "suffix": "patients", "min": 10, "max": 100000, "step": 10, "hint": "Total patients in control placebo arm"}
        ],
        "metrics": [
            {"id": "relative_risk_ratio_rr", "label": "Relative Risk (RR)", "default_display": "0.50 (50% Risk Reduction)", "highlight": True},
            {"id": "absolute_risk_reduction_arr", "label": "Absolute Risk Reduction (ARR)", "default_display": "7.00% Absolute Gain", "highlight": True},
            {"id": "number_needed_to_treat_nnt", "label": "Number Needed to Treat (NNT)", "default_display": "15 Patients to Prevent 1 Event", "highlight": True},
            {"id": "odds_ratio_or", "label": "Odds Ratio (OR)", "default_display": "0.46 (Protective Effect)"}
        ],
        "proof_steps": [
            {"step_title": "Experimental & Control Event Rates", "step_text": "Experimental Event Rate (EER) = 35 / 500 = 0.070 (7.0%). Control Event Rate (CER) = 70 / 500 = 0.140 (14.0%)."},
            {"step_title": "Relative Risk & Risk Reduction", "step_text": "Relative Risk (RR) = EER / CER = 0.070 / 0.140 = 0.50. Relative Risk Reduction (RRR) = 1 - 0.50 = 50.0% relative drop in adverse events."},
            {"step_title": "Absolute Risk Reduction (ARR)", "step_text": "ARR = CER - EER = 14.0% - 7.0% = 7.0% absolute reduction in event frequency."},
            {"step_title": "Number Needed to Treat (NNT)", "step_text": "NNT = 1 / ARR = 1 / 0.070 = 14.28 ≈ 15 patients. Treating 15 patients with the experimental drug prevents exactly 1 adverse clinical event compared to placebo."}
        ],
        "faqs": [
            {"q": "Why is Absolute Risk Reduction (ARR) more honest than Relative Risk Reduction (RRR)?", "a": "Pharmaceutical marketing often highlights a '50% reduction' (RRR). However, if baseline risk drops from 2 in 10,000 to 1 in 10,000, the absolute benefit is only 0.01%, requiring 10,000 patients to be treated to prevent one event."},
            {"q": "What is an ideal Number Needed to Treat (NNT)?", "a": "An NNT of 1 means every single treated patient benefits. In clinical medicine, an NNT between 5 and 20 for life-threatening conditions (e.g. statins for secondary prevention of myocardial infarction) represents a major therapeutic success."}
        ],
        "js_logic": """
          const a = getNum('experimental_event_count_a');
          const n1 = getNum('experimental_total_count_n1');
          const c = getNum('control_event_count_c');
          const n2 = getNum('control_total_count_n2');

          if (n1 > 0 && n2 > 0) {
            const eer = a / n1;
            const cer = c / n2;
            const rr = cer > 0 ? (eer / cer) : 1;
            const arr = cer - eer;
            const nnt = arr > 0 ? Math.ceil(1 / arr) : 999;

            const b = n1 - a;
            const d = n2 - c;
            const orVal = (b * c > 0) ? (a * d) / (b * c) : 1;

            setMetric('relative_risk_ratio_rr', rr.toFixed(2) + ' (' + ((1 - rr) * 100).toFixed(0) + '% Risk Reduction)');
            setMetric('absolute_risk_reduction_arr', (arr * 100).toFixed(2) + '% Absolute Gain');
            setMetric('number_needed_to_treat_nnt', nnt + ' Patients to Prevent 1 Event');
            setMetric('odds_ratio_or', orVal.toFixed(2) + (orVal < 1 ? ' (Protective Effect)' : ' (Increased Risk)'));
          }
        """
    },
    {
        "slug": "diagnostic-sensitivity-specificity",
        "category": "biotech",
        "name": "Clinical Diagnostic Test Sensitivity, Specificity & Predictive Value (PPV/NPV) Calculator",
        "description": "Calculate diagnostic Sensitivity, Specificity, Positive Predictive Value (PPV), Negative Predictive Value (NPV), and Likelihood Ratios from a 2×2 contingency table.",
        "hero_badge": "Diagnostic Medicine • Test Performance",
        "formula_display": "Sensitivity = TP / (TP + FN) | Specificity = TN / (TN + FP) | PPV = TP / (TP + FP)",
        "fields": [
            {"id": "true_positives_tp", "label": "True Positives (TP)", "default": 95, "suffix": "cases", "min": 0, "max": 10000, "step": 1, "hint": "Sick patients correctly identified by test as positive"},
            {"id": "false_positives_fp", "label": "False Positives (FP)", "default": 10, "suffix": "cases", "min": 0, "max": 10000, "step": 1, "hint": "Healthy individuals incorrectly flagged as positive"},
            {"id": "false_negatives_fn", "label": "False Negatives (FN)", "default": 5, "suffix": "cases", "min": 0, "max": 10000, "step": 1, "hint": "Sick patients incorrectly flagged as negative"},
            {"id": "true_negatives_tn", "label": "True Negatives (TN)", "default": 890, "suffix": "cases", "min": 0, "max": 100000, "step": 5, "hint": "Healthy individuals correctly identified as negative"}
        ],
        "metrics": [
            {"id": "diagnostic_sensitivity_pct", "label": "Diagnostic Sensitivity", "default_display": "95.0% True Positive Rate", "highlight": True},
            {"id": "diagnostic_specificity_pct", "label": "Diagnostic Specificity", "default_display": "98.9% True Negative Rate", "highlight": True},
            {"id": "positive_predictive_value_ppv", "label": "Positive Predictive Value (PPV)", "default_display": "90.5% (Post-Test Probability)", "highlight": True},
            {"id": "negative_predictive_value_npv", "label": "Negative Predictive Value (NPV)", "default_display": "99.4% Ruled Out"}
        ],
        "proof_steps": [
            {"step_title": "Total Gold-Standard Disease Population", "step_text": "Total Diseased = TP (95) + FN (5) = 100 patients. Total Non-Diseased = FP (10) + TN (890) = 900 healthy individuals."},
            {"step_title": "Intrinsic Test Accuracy (Sensitivity & Specificity)", "step_text": "Sensitivity = TP / (TP + FN) = 95 / 100 = 95.0%. Specificity = TN / (TN + FP) = 890 / 900 = 98.89% ≈ 98.9%."},
            {"step_title": "Positive Predictive Value (PPV)", "step_text": "Total Positive Tests = TP (95) + FP (10) = 105. PPV = 95 / 105 = 90.48% ≈ 90.5% probability a positive patient truly has the disease."},
            {"step_title": "Negative Predictive Value (NPV)", "step_text": "Total Negative Tests = TN (890) + FN (5) = 895. NPV = 890 / 895 = 99.44% probability a negative test is genuinely healthy."}
        ],
        "faqs": [
            {"q": "How does disease prevalence affect PPV and NPV?", "a": "Sensitivity and specificity are intrinsic properties of the assay that do not change with prevalence. However, in low-prevalence screening populations (e.g. 0.1%), even a 99% specific test will produce more false positives than true positives, dramatically lowering PPV."},
            {"q": "What is the clinical heuristic 'SnNout' and 'SpPin'?", "a": "A highly Sensitive test, when Negative, rules OUT disease (SnNout). A highly Specific test, when Positive, rules IN disease (SpPin)."}
        ],
        "js_logic": """
          const tp = getNum('true_positives_tp');
          const fp = getNum('false_positives_fp');
          const fn = getNum('false_negatives_fn');
          const tn = getNum('true_negatives_tn');

          const diseased = tp + fn;
          const healthy = fp + tn;
          const totalPos = tp + fp;
          const totalNeg = tn + fn;

          if (diseased > 0 && healthy > 0 && totalPos > 0 && totalNeg > 0) {
            const sens = (tp / diseased) * 100;
            const spec = (tn / healthy) * 100;
            const ppv = (tp / totalPos) * 100;
            const npv = (tn / totalNeg) * 100;

            setMetric('diagnostic_sensitivity_pct', sens.toFixed(1) + '% True Positive Rate');
            setMetric('diagnostic_specificity_pct', spec.toFixed(1) + '% True Negative Rate');
            setMetric('positive_predictive_value_ppv', ppv.toFixed(1) + '% (Post-Test Probability)');
            setMetric('negative_predictive_value_npv', npv.toFixed(1) + '% Ruled Out');
          }
        """
    },
    {
        "slug": "molarity-normality-solution",
        "category": "biotech",
        "name": "Solution Molarity, Molality & Normality Preparation Calculator",
        "description": "Calculate chemical solute mass required in grams to prepare precise laboratory solutions of defined Molarity (M), Normality (N), and target volume.",
        "hero_badge": "Analytical Chemistry • Solution Prep",
        "formula_display": "Solute Mass (g) = Molarity (mol/L) · Volume (L) · Molecular Weight (g/mol) | Normality = Molarity · Valence (eq/mol)",
        "fields": [
            {"id": "target_molarity_mol_l", "label": "Desired Target Molarity (M in mol/L)", "default": 0.50, "suffix": "M", "min": 0.001, "max": 20.0, "step": 0.05, "hint": "Molar concentration of final solution"},
            {"id": "solution_volume_liters", "label": "Target Solution Volume (Liters)", "default": 1.0, "suffix": "L", "min": 0.01, "max": 1000, "step": 0.1, "hint": "Total final volume of prepared liquid (1,000 mL = 1.0 L)"},
            {"id": "molecular_weight_g_mol", "label": "Solute Formula Weight / MW (g/mol)", "default": 58.44, "suffix": "g/mol", "min": 1.0, "max": 2000, "step": 0.5, "hint": "Molecular weight from reagent label (e.g. NaCl = 58.44, NaOH = 40.00)"},
            {"id": "solute_valence_factor", "label": "Valence Factor (Equivalents per Mole)", "default": 1, "suffix": "eq/mol", "min": 1, "max": 6, "step": 1, "hint": "H⁺ or OH⁻ equivalents (e.g. HCl = 1; H₂SO₄ = 2; H₃PO₄ = 3)"}
        ],
        "metrics": [
            {"id": "required_solute_mass_grams", "label": "Solute Mass to Weigh on Balance", "default_display": "29.22 Grams", "highlight": True},
            {"id": "solution_normality_n", "label": "Solution Normality (N)", "default_display": "0.50 N (eq/L)", "highlight": True},
            {"id": "total_moles_dissolved", "label": "Total Dissolved Moles", "default_display": "0.500 Moles", "highlight": True},
            {"id": "solution_mass_percentage", "label": "Approximate Weight/Volume (w/v %)", "default_display": "2.92% (w/v)"}
        ],
        "proof_steps": [
            {"step_title": "Total Moles Required", "step_text": "Moles = Molarity (0.50 mol/L) × Volume (1.0 L) = 0.500 moles."},
            {"step_title": "Mass Formulation Weight", "step_text": "Mass = Moles × Formula Weight = 0.500 moles × 58.44 g/mol = 29.22 grams."},
            {"step_title": "Normality Equivalent Calculation", "step_text": "Normality N = Molarity (0.50 M) × Valence (1 eq/mol) = 0.50 N."},
            {"step_title": "Benchtop Preparation Procedure", "step_text": "Weigh exactly 29.22 g of reagent on an analytical balance. Dissolve in ~800 mL of deionized water in a volumetric flask, then adjust to the 1.0 L calibration meniscus line."}
        ],
        "faqs": [
            {"q": "What is the difference between Molarity (M) and Normality (N)?", "a": "Molarity is moles of solute per liter of solution. Normality is gram equivalent weights per liter, accounting for reactive capacity (e.g. a 1 M H₂SO₄ sulfuric acid solution is 2 N because each molecule yields 2 hydronium ions)."},
            {"q": "Why must you never add water directly to concentrated acid?", "a": "Always add acid to water ('AAA'). Dissolving concentrated acid is violently exothermic; adding water to acid causes boiling and dangerous corrosive splashing."}
        ],
        "js_logic": """
          const m = getNum('target_molarity_mol_l');
          const v = getNum('solution_volume_liters');
          const mw = getNum('molecular_weight_g_mol');
          const val = getNum('solute_valence_factor');

          if (m > 0 && v > 0 && mw > 0) {
            const moles = m * v;
            const grams = moles * mw;
            const normality = m * val;
            const wvPct = (grams / (v * 1000)) * 100;

            setMetric('required_solute_mass_grams', grams.toFixed(2) + ' Grams');
            setMetric('solution_normality_n', normality.toFixed(2) + ' N (eq/L)');
            setMetric('total_moles_dissolved', moles.toFixed(3) + ' Moles');
            setMetric('solution_mass_percentage', wvPct.toFixed(2) + '% (w/v)');
          }
        """
    },
    {
        "slug": "radioisotope-decay-law",
        "category": "biotech",
        "name": "Radioactive Isotope Exponential Decay & Specific Activity Calculator",
        "description": "Calculate residual radioactivity, decay constants (λ), remaining activity fractions, and radiological cooling durations via Rutherford's radioactive decay law.",
        "hero_badge": "Nuclear Medicine • Radiobiology",
        "formula_display": "A(t) = A₀ · e^(-λ · t) | λ = ln(2) / t½ ≈ 0.69315 / t½",
        "fields": [
            {"id": "initial_radioactivity_a0", "label": "Initial Radioactivity (A₀)", "default": 100.0, "suffix": "mCi or MBq", "min": 0.1, "max": 100000, "step": 1.0, "hint": "Calibrated radioactive dose at reference time t=0"},
            {"id": "isotope_half_life_hours", "label": "Isotope Physical Half-Life (t½ in Hours)", "default": 6.006, "suffix": "hours", "min": 0.01, "max": 876000, "step": 0.1, "hint": "Technetium-99m = 6.01 hr; Fluorine-18 = 1.83 hr (110 min); Iodine-131 = 192.5 hr (8.02 days)"},
            {"id": "elapsed_decay_time_hours", "label": "Elapsed Decay Time (Hours)", "default": 12.0, "suffix": "hours", "min": 0.1, "max": 100000, "step": 0.5, "hint": "Time interval between dose calibration and patient injection"}
        ],
        "metrics": [
            {"id": "remaining_radioactivity_at", "label": "Remaining Radioactivity A(t)", "default_display": "25.04 mCi (MBq)", "highlight": True},
            {"id": "percentage_retained_activity", "label": "Fraction of Initial Activity Retained", "default_display": "25.04% Retained", "highlight": True},
            {"id": "radioactive_decay_constant_lambda", "label": "Decay Constant (λ)", "default_display": "0.1154 hr⁻¹", "highlight": True},
            {"id": "elapsed_half_lives_count", "label": "Elapsed Physical Half-Lives", "default_display": "2.00 Half-Lives"}
        ],
        "proof_steps": [
            {"step_title": "Nuclear Decay Constant (λ)", "step_text": "λ = ln(2) / t½ = 0.693147 / 6.006 hours = 0.115409 hr⁻¹."},
            {"step_title": "Elapsed Half-Lives Interval", "step_text": "Elapsed Half-Lives n = 12.0 hours / 6.006 hours = 1.998 ≈ 2.00 half-lives."},
            {"step_title": "Residual Activity Exponential Law", "step_text": "A(t) = A₀ · e^(-λ · t) = 100.0 · e^(-0.115409 × 12.0) = 100.0 · e^(-1.3849) = 100.0 · 0.25035 = 25.04 mCi."},
            {"step_title": "Radiopharmacy Clinical Implication", "step_text": "After exactly 2 half-lives, 74.96% of the radionuclide has decayed. Nuclear medicine technologists must administer 4× the original volume to deliver the equivalent diagnostic dose."}
        ],
        "faqs": [
            {"q": "What is the difference between physical half-life and biological half-life?", "a": "Physical half-life (Tp) is the immutable nuclear decay rate of the isotope. Biological half-life (Tb) is the physiological clearance rate by human organs. The effective half-life (Te) is given by 1/Te = 1/Tp + 1/Tb."},
            {"q": "What unit conversion exists between Curies (Ci) and Becquerels (Bq)?", "a": "1 Curie (Ci) equals exactly 3.7 × 10¹⁰ disintegrations per second = 37 GigaBecquerels (GBq). 1 milliCurie (mCi) = 37 MegaBecquerels (MBq)."}
        ],
        "js_logic": """
          const a0 = getNum('initial_radioactivity_a0');
          const thalf = getNum('isotope_half_life_hours');
          const t = getNum('elapsed_decay_time_hours');

          if (a0 > 0 && thalf > 0) {
            const lambda = Math.log(2) / thalf;
            const at = a0 * Math.exp(-lambda * t);
            const pct = (at / a0) * 100;
            const numHalves = t / thalf;

            setMetric('remaining_radioactivity_at', at.toFixed(2) + ' mCi (MBq)');
            setMetric('percentage_retained_activity', pct.toFixed(2) + '% Retained');
            setMetric('radioactive_decay_constant_lambda', lambda.toFixed(4) + ' hr⁻¹');
            setMetric('elapsed_half_lives_count', numHalves.toFixed(2) + ' Half-Lives');
          }
        """
    },
    {
        "slug": "insulin-carb-ratio-isf",
        "category": "biotech",
        "name": "Diabetes Insulin-to-Carb Ratio (ICR) & Insulin Sensitivity Factor (ISF) Calculator",
        "description": "Calculate individualized rapid-acting insulin bolus doses for diabetes management using the Rule of 500 (ICR) and Rule of 1800 (ISF / Correction Factor).",
        "hero_badge": "Endocrinology • Diabetes Pharmacotherapy",
        "formula_display": "ICR = 500 / TDD | ISF = 1800 / TDD | Total Bolus = (Carbs / ICR) + [(BG - Target) / ISF]",
        "fields": [
            {"id": "total_daily_dose_tdd", "label": "Total Daily Insulin Dose (TDD in Units)", "default": 50, "suffix": "units/day", "min": 5, "max": 250, "step": 1, "hint": "Combined basal (long-acting) and bolus (rapid-acting) daily insulin"},
            {"id": "meal_carbohydrates_grams", "label": "Meal Carbohydrates (Grams)", "default": 60, "suffix": "g carbs", "min": 0, "max": 300, "step": 5, "hint": "Total digestible carbohydrate grams in meal"},
            {"id": "current_blood_glucose_mg_dl", "label": "Current Blood Glucose (mg/dL)", "default": 220, "suffix": "mg/dL", "min": 50, "max": 500, "step": 5, "hint": "Pre-meal fingerstick or continuous glucose monitor reading"},
            {"id": "target_blood_glucose_mg_dl", "label": "Target Blood Glucose (mg/dL)", "default": 110, "suffix": "mg/dL", "min": 70, "max": 180, "step": 5, "hint": "Physician-ordered target pre-prandial glucose"}
        ],
        "metrics": [
            {"id": "total_recommended_bolus_units", "label": "Total Meal Bolus Injection", "default_display": "9.1 Units (Rapid-Acting)", "highlight": True},
            {"id": "carb_coverage_bolus_units", "label": "Carbohydrate Coverage Dose", "default_display": "6.0 Units", "highlight": True},
            {"id": "high_blood_sugar_correction", "label": "Correction Bolus Dose", "default_display": "3.1 Units", "highlight": True},
            {"id": "calculated_icr_and_isf", "label": "Patient ICR & ISF Factors", "default_display": "ICR 1:10g | ISF 1:36 mg/dL"}
        ],
        "proof_steps": [
            {"step_title": "Rule of 500 (Insulin-to-Carb Ratio ICR)", "step_text": "ICR = 500 / Total Daily Dose (50 units) = 10. Exactly 1 unit of rapid-acting insulin covers 10 grams of dietary carbohydrates (1:10g)."},
            {"step_title": "Rule of 1800 (Insulin Sensitivity Factor ISF)", "step_text": "ISF = 1800 / TDD (50 units) = 36. Exactly 1 unit of rapid-acting insulin drops blood glucose by 36 mg/dL (1:36 mg/dL)."},
            {"step_title": "Meal Carbohydrate Bolus Component", "step_text": "Carb Bolus = Meal Carbs (60g) / ICR (10g) = 6.0 units."},
            {"step_title": "High Blood Sugar Correction Component", "step_text": "Correction Bolus = (Current BG 220 - Target BG 110) / ISF (36) = 110 / 36 = 3.06 ≈ 3.1 units. Total Bolus = 6.0 + 3.1 = 9.1 units."}
        ],
        "faqs": [
            {"q": "What is the difference between the Rule of 500 and the Rule of 450?", "a": "The Rule of 500 is calibrated for modern rapid-acting insulin analogs (Humalog, Novolog, Apidra). The older Rule of 450 was formulated for slower regular human insulin (Regular R)."},
            {"q": "What is 'insulin on board' (IOB)?", "a": "IOB refers to remaining active bolus insulin injected within the prior 3 to 4 hours. Failing to subtract IOB before administering an additional correction bolus leads to insulin stacking and dangerous hypoglycemia."}
        ],
        "js_logic": """
          const tdd = getNum('total_daily_dose_tdd');
          const carbs = getNum('meal_carbohydrates_grams');
          const bg = getNum('current_blood_glucose_mg_dl');
          const target = getNum('target_blood_glucose_mg_dl');

          if (tdd > 0) {
            const icr = Math.round(500 / tdd);
            const isf = Math.round(1800 / tdd);

            const carbBolus = icr > 0 ? (carbs / icr) : 0;
            const corrBolus = (bg > target && isf > 0) ? ((bg - target) / isf) : 0;
            const totalBolus = carbBolus + corrBolus;

            setMetric('total_recommended_bolus_units', totalBolus.toFixed(1) + ' Units (Rapid-Acting)');
            setMetric('carb_coverage_bolus_units', carbBolus.toFixed(1) + ' Units');
            setMetric('high_blood_sugar_correction', corrBolus.toFixed(1) + ' Units');
            setMetric('calculated_icr_and_isf', 'ICR 1:' + icr + 'g | ISF 1:' + isf + ' mg/dL');
          }
        """
    },
    {
        "slug": "arterial-blood-gas-anion-gap",
        "category": "biotech",
        "name": "Arterial Blood Gas (ABG) & Serum Anion Gap Calculator",
        "description": "Interpret Arterial Blood Gas (ABG) acid-base disorders, calculate serum anion gap, and evaluate metabolic acidosis versus respiratory compensation.",
        "hero_badge": "Critical Care Medicine • ABG Diagnostics",
        "formula_display": "Serum Anion Gap = [Na⁺] - ([Cl⁻] + [HCO₃⁻]) | Normal Reference = 8 to 12 mEq/L",
        "fields": [
            {"id": "arterial_blood_ph", "label": "Arterial Blood pH", "default": 7.30, "suffix": "pH", "min": 6.80, "max": 7.80, "step": 0.01, "hint": "Normal reference: 7.35 to 7.45"},
            {"id": "arterial_paco2_mmhg", "label": "Partial Pressure of CO₂ (PaCO₂ in mmHg)", "default": 30, "suffix": "mmHg", "min": 10, "max": 100, "step": 1, "hint": "Normal reference: 35 to 45 mmHg"},
            {"id": "serum_bicarbonate_hco3", "label": "Serum Bicarbonate (HCO₃⁻ in mEq/L)", "default": 14, "suffix": "mEq/L", "min": 2, "max": 50, "step": 1, "hint": "Normal reference: 22 to 26 mEq/L"},
            {"id": "serum_sodium_na", "label": "Serum Sodium (Na⁺ in mEq/L)", "default": 140, "suffix": "mEq/L", "min": 110, "max": 180, "step": 1, "hint": "Normal reference: 135 to 145 mEq/L"},
            {"id": "serum_chloride_cl", "label": "Serum Chloride (Cl⁻ in mEq/L)", "default": 102, "suffix": "mEq/L", "min": 70, "max": 140, "step": 1, "hint": "Normal reference: 96 to 106 mEq/L"}
        ],
        "metrics": [
            {"id": "serum_anion_gap_val", "label": "Serum Anion Gap (AG)", "default_display": "24.0 mEq/L (Elevated Gap)", "highlight": True},
            {"id": "primary_acid_base_disorder", "label": "Primary Acid-Base Disorder", "default_display": "High Anion Gap Metabolic Acidosis (HAGMA)", "highlight": True},
            {"id": "winters_formula_compensation", "label": "Winter's Expected PaCO₂", "default_display": "27 - 31 mmHg (Adequate Compensation)", "highlight": True},
            {"id": "differential_diagnosis_mnemonic", "label": "Clinical Etiology Category", "default_display": "Ketoacidosis, Lactic Acidosis, Toxic Ingestion"}
        ],
        "proof_steps": [
            {"step_title": "Primary Acidemia Identification", "step_text": "Blood pH = 7.30 (< 7.35 indicates acidemia). Bicarbonate HCO₃⁻ = 14 mEq/L (< 22 indicates metabolic driver)."},
            {"step_title": "Serum Anion Gap Derivation", "step_text": "Anion Gap = [Na⁺] - ([Cl⁻] + [HCO₃⁻]) = 140 - (102 + 14) = 140 - 116 = 24.0 mEq/L (Normal reference is 8 to 12 mEq/L)."},
            {"step_title": "Winter's Formula for Respiratory Compensation", "step_text": "Expected PaCO₂ = (1.5 × HCO₃⁻) + 8 ± 2 = (1.5 × 14) + 8 ± 2 = 21 + 8 ± 2 = 29 mmHg (range: 27 to 31 mmHg)."},
            {"step_title": "Clinical Integration", "step_text": "Because measured PaCO₂ (30 mmHg) matches Winter's formula (27-31 mmHg), the respiratory system is properly hyperventilating to blow off acidic CO₂ (compensating for primary High Anion Gap Metabolic Acidosis)."}
        ],
        "faqs": [
            {"q": "What causes High Anion Gap Metabolic Acidosis (HAGMA)?", "a": "Common etiologies are memorized via the mnemonic GOLD MARK: Glycols, Oxoproline, L-lactate, D-lactate, Methanol, Aspirin (salicylates), Renal failure (uremia), and Ketoacidosis (diabetic, alcoholic, starvation)."},
            {"q": "Why must the Anion Gap be corrected for hypoalbuminemia?", "a": "Albumin constitutes the majority of unmeasured plasma anions. For every 1.0 g/dL decrease in serum albumin below normal (4.0 g/dL), add 2.5 mEq/L to the calculated anion gap."}
        ],
        "js_logic": """
          const ph = getNum('arterial_blood_ph');
          const paco2 = getNum('arterial_paco2_mmhg');
          const hco3 = getNum('serum_bicarbonate_hco3');
          const na = getNum('serum_sodium_na');
          const cl = getNum('serum_chloride_cl');

          const ag = na - (cl + hco3);
          const expPaco2 = (1.5 * hco3) + 8;
          const minPaco2 = expPaco2 - 2;
          const maxPaco2 = expPaco2 + 2;

          let disorder = 'Normal Acid-Base Homeostasis';
          let diff = 'No significant metabolic derangement';

          if (ph < 7.35) {
            if (hco3 < 22) {
              if (ag > 12) {
                disorder = 'High Anion Gap Metabolic Acidosis (HAGMA)';
                diff = 'Ketoacidosis, Lactic Acidosis, Toxic Ingestion';
              } else {
                disorder = 'Normal Anion Gap Acidosis (NAGMA)';
                diff = 'Diarrhea, Renal Tubular Acidosis (RTA)';
              }
            } else if (paco2 > 45) {
              disorder = 'Respiratory Acidosis (Hypoventilation)';
              diff = 'COPD Exacerbation, Opioid Hypoventilation';
            }
          } else if (ph > 7.45) {
            if (hco3 > 26) {
              disorder = 'Metabolic Alkalosis';
              diff = 'Vomiting, Diuretic Use, Nasogastric Suction';
            } else if (paco2 < 35) {
              disorder = 'Respiratory Alkalosis (Hyperventilation)';
              diff = 'Panic Attack, Pulmonary Embolism, Early Sepsis';
            }
          }

          let comp = paco2.toFixed(0) + ' mmHg (No Compensation)';
          if (ph < 7.35 && hco3 < 22) {
            comp = minPaco2.toFixed(0) + ' - ' + maxPaco2.toFixed(0) + ' mmHg ' + (paco2 >= minPaco2 && paco2 <= maxPaco2 ? '(Adequate Compensation)' : '(Mixed Disorder)');
          }

          setMetric('serum_anion_gap_val', ag.toFixed(1) + ' mEq/L ' + (ag > 12 ? '(Elevated Gap)' : '(Normal Gap)'));
          setMetric('primary_acid_base_disorder', disorder);
          setMetric('winters_formula_compensation', comp);
          setMetric('differential_diagnosis_mnemonic', diff);
        """
    },
    {
        "slug": "qpcr-delta-delta-ct",
        "category": "biotech",
        "name": "Quantitative Real-Time PCR (qPCR) 2^(-ΔΔCt) Relative Gene Expression Calculator",
        "description": "Calculate relative gene expression fold change in RT-qPCR experiments using the Livak and Schmittgen comparative 2^(-ΔΔCt) quantification method.",
        "hero_badge": "Genomics • qPCR Quantification",
        "formula_display": "ΔΔCt = (Ct_target - Ct_ref)_treated - (Ct_target - Ct_ref)_control | Fold Change = 2^(-ΔΔCt)",
        "fields": [
            {"id": "target_gene_ct_treated", "label": "Target Gene Ct (Treated Sample)", "default": 21.4, "suffix": "Ct", "min": 5, "max": 40, "step": 0.1, "hint": "Threshold cycle of gene of interest in experimental condition"},
            {"id": "reference_gene_ct_treated", "label": "Housekeeping Reference Ct (Treated)", "default": 18.2, "suffix": "Ct", "min": 5, "max": 40, "step": 0.1, "hint": "Threshold cycle of internal control (e.g. GAPDH, ACTB) in treated sample"},
            {"id": "target_gene_ct_control", "label": "Target Gene Ct (Untreated Control)", "default": 24.8, "suffix": "Ct", "min": 5, "max": 40, "step": 0.1, "hint": "Threshold cycle of gene of interest in vehicle control"},
            {"id": "reference_gene_ct_control", "label": "Housekeeping Reference Ct (Control)", "default": 18.3, "suffix": "Ct", "min": 5, "max": 40, "step": 0.1, "hint": "Threshold cycle of internal control in untreated control"}
        ],
        "metrics": [
            {"id": "relative_fold_change_2_ddct", "label": "Relative Gene Expression Fold Change", "default_display": "9.85-Fold Upregulation", "highlight": True},
            {"id": "delta_delta_ct_value", "label": "Comparative ΔΔCt Value", "default_display": "-3.30 ΔΔCt", "highlight": True},
            {"id": "delta_ct_treated_sample", "label": "ΔCt (Treated Sample)", "default_display": "+3.20 Ct", "highlight": True},
            {"id": "delta_ct_control_sample", "label": "ΔCt (Control Calibrator)", "default_display": "+6.50 Ct"}
        ],
        "proof_steps": [
            {"step_title": "Internal Normalization to Reference Gene (ΔCt)", "step_text": "ΔCt(Treated) = Target Ct (21.4) - Ref Ct (18.2) = 3.20. ΔCt(Control) = Target Ct (24.8) - Ref Ct (18.3) = 6.50."},
            {"step_title": "Comparative Calibrator Normalization (ΔΔCt)", "step_text": "ΔΔCt = ΔCt(Treated) - ΔCt(Control) = 3.20 - 6.50 = -3.30."},
            {"step_title": "Exponential Fold Change Equation", "step_text": "Fold Change = 2^(-ΔΔCt) = 2^(-(-3.30)) = 2^(3.30) = 9.849 ≈ 9.85-fold relative increase."},
            {"step_title": "Livak Method Assumptions", "step_text": "The 2^(-ΔΔCt) method assumes PCR amplification efficiency is near 100% (doubling every cycle) for both target and housekeeping amplicons."}
        ],
        "faqs": [
            {"q": "What does a negative ΔΔCt signify?", "a": "A negative ΔΔCt means the target gene in the treated sample crossed the fluorescence threshold earlier (lower Ct), representing gene upregulation. Conversely, a positive ΔΔCt indicates downregulation."},
            {"q": "What if primer amplification efficiencies differ from 100%?", "a": "If primer efficiency is below 90% or differs significantly between target and reference, the Pfaffl mathematical model should be used instead of 2^(-ΔΔCt) to adjust for specific primer slope efficiencies."}
        ],
        "js_logic": """
          const tgT = getNum('target_gene_ct_treated');
          const rgT = getNum('reference_gene_ct_treated');
          const tgC = getNum('target_gene_ct_control');
          const rgC = getNum('reference_gene_ct_control');

          const dCtTreated = tgT - rgT;
          const dCtControl = tgC - rgC;
          const ddCt = dCtTreated - dCtControl;
          const fold = Math.pow(2, -ddCt);

          let foldDisplay = fold.toFixed(2) + '-Fold Upregulation';
          if (fold < 1) {
            foldDisplay = (1 / fold).toFixed(2) + '-Fold Downregulation (' + fold.toFixed(3) + '×)';
          }

          setMetric('relative_fold_change_2_ddct', foldDisplay);
          setMetric('delta_delta_ct_value', (ddCt >= 0 ? '+' : '') + ddCt.toFixed(2) + ' ΔΔCt');
          setMetric('delta_ct_treated_sample', (dCtTreated >= 0 ? '+' : '') + dCtTreated.toFixed(2) + ' Ct');
          setMetric('delta_ct_control_sample', (dCtControl >= 0 ? '+' : '') + dCtControl.toFixed(2) + ' Ct');
        """
    },
    {
        "slug": "recombinant-protein-yield",
        "category": "biotech",
        "name": "Recombinant Protein Fermentation Yield & Specific Productivity Calculator",
        "description": "Calculate total recombinant protein yield, specific cellular productivity (qP), volumetric productivity, and post-purification recovery efficiency for bioprocessing runs.",
        "hero_badge": "Bioprocessing • Fermentation Scale-Up",
        "formula_display": "Total Yield = Bioreactor Volume (L) · Protein Titer (g/L) | Specific Productivity qP = Titer / (Biomass · Induction Hours)",
        "fields": [
            {"id": "bioreactor_working_volume_liters", "label": "Bioreactor Working Volume (Liters)", "default": 250.0, "suffix": "L", "min": 1, "max": 25000, "step": 10, "hint": "Liquid culture volume in fermenter"},
            {"id": "crude_protein_titer_g_l", "label": "Crude Fermentation Titer (g/L)", "default": 3.80, "suffix": "g/L", "min": 0.05, "max": 50.0, "step": 0.1, "hint": "Expressed protein concentration in broth at harvest"},
            {"id": "downstream_purification_recovery_pct", "label": "Downstream Purification Recovery (%)", "default": 65.0, "suffix": "%", "min": 10, "max": 95, "step": 1, "hint": "Overall yield across chromatography and filtration unit operations"},
            {"id": "bulk_api_commercial_value_per_gram", "label": "Bulk Drug Substance Value ($/gram)", "default": 450, "suffix": "$/g", "min": 10, "max": 10000, "step": 25, "hint": "Commercial value of pure active pharmaceutical ingredient (API)"}
        ],
        "metrics": [
            {"id": "purified_bulk_protein_yield", "label": "Net Purified Protein Yield", "default_display": "617.5 Grams", "highlight": True},
            {"id": "total_crude_protein_harvest", "label": "Crude Bioreactor Harvest Mass", "default_display": "950.0 Grams Total", "highlight": True},
            {"id": "bioprocess_run_commercial_value", "label": "Batch Commercial API Value", "default_display": "$277,875 Value", "highlight": True},
            {"id": "purification_losses_mass", "label": "Downstream Purification Losses", "default_display": "332.5 g Lost"}
        ],
        "proof_steps": [
            {"step_title": "Crude Bioreactor Mass Output", "step_text": "Crude Mass = Working Volume (250.0 L) × Titer (3.80 g/L) = 950.0 grams expressed protein."},
            {"step_title": "Downstream Purification Recovery", "step_text": "Net Purified Yield = 950.0 g × 65.0% chromatography recovery = 617.5 grams pure therapeutic protein."},
            {"step_title": "Downstream Scrap & Losses", "step_text": "Purification Losses = 950.0 g - 617.5 g = 332.5 grams lost to column fouling, hold-up volume, and filter binding."},
            {"step_title": "Commercial Batch Valuation", "step_text": "Gross API Value = 617.5 grams × $450/gram = $277,875 commercial drug substance produced in single run."}
        ],
        "faqs": [
            {"q": "What is a competitive protein expression titer for CHO cell fed-batch cultures?", "a": "Modern industrial Chinese Hamster Ovary (CHO) cell platforms for monoclonal antibodies (mAbs) achieve titers between 3.0 and 8.0 g/L over 14-day fed-batch production cycles."},
            {"q": "Why is downstream purification often the primary bottleneck in biomanufacturing?", "a": "High-titer expression often overwhelms downstream Protein A affinity chromatography columns, requiring multiple cycles and high volumes of expensive buffers."}
        ],
        "js_logic": """
          const vol = getNum('bioreactor_working_volume_liters');
          const titer = getNum('crude_protein_titer_g_l');
          const recPct = getNum('downstream_purification_recovery_pct');
          const valPerG = getNum('bulk_api_commercial_value_per_gram');

          const crudeMass = vol * titer;
          const purifiedMass = crudeMass * (recPct / 100);
          const losses = crudeMass - purifiedMass;
          const batchVal = purifiedMass * valPerG;

          setMetric('purified_bulk_protein_yield', purifiedMass.toFixed(1) + ' Grams');
          setMetric('total_crude_protein_harvest', crudeMass.toFixed(1) + ' Grams Total');
          setMetric('bioprocess_run_commercial_value', '$' + Math.round(batchVal).toLocaleString() + ' Value');
          setMetric('purification_losses_mass', losses.toFixed(1) + ' g Lost');
        """
    },
    {
        "slug": "maintenance-fluid-pediatric",
        "category": "biotech",
        "name": "Maintenance IV Fluid Requirements (Holliday-Segar 4-2-1 Rule) Calculator",
        "description": "Calculate daily and hourly maintenance IV fluid requirements for pediatric and adult patients using the standard clinical Holliday-Segar 4-2-1 methodology.",
        "hero_badge": "Pediatric Critical Care • Fluid Maintenance",
        "formula_display": "First 10 kg: 4 mL/kg/hr | Next 10 kg: 2 mL/kg/hr | Each kg > 20 kg: 1 mL/kg/hr",
        "fields": [
            {"id": "patient_body_weight_kg", "label": "Patient Body Weight (kg)", "default": 24.0, "suffix": "kg", "min": 1.0, "max": 180, "step": 0.5, "hint": "Patient weight in kilograms"}
        ],
        "metrics": [
            {"id": "hourly_maintenance_infusion_rate", "label": "Hourly Maintenance IV Rate", "default_display": "64.0 mL/hr", "highlight": True},
            {"id": "daily_maintenance_fluid_volume", "label": "24-Hour Total Maintenance Fluid", "default_display": "1,536 mL / Day", "highlight": True},
            {"id": "recommended_electrolyte_solution", "label": "Recommended Maintenance Solution", "default_display": "D5 0.9% NS + 20 mEq/L KCl", "highlight": True},
            {"id": "weight_tier_bracket", "label": "Weight Tier Classification", "default_display": "Tier 3 (> 20 kg Bracket)"}
        ],
        "proof_steps": [
            {"step_title": "First 10 kg Tier (0 to 10 kg)", "step_text": "Rate = 10 kg × 4.0 mL/kg/hr = 40.0 mL/hr."},
            {"step_title": "Second 10 kg Tier (11 to 20 kg)", "step_text": "Rate = 10 kg × 2.0 mL/kg/hr = 20.0 mL/hr (cumulative: 60.0 mL/hr)."},
            {"step_title": "Remaining Weight Tier (> 20 kg)", "step_text": "Weight over 20 kg = 24.0 kg - 20.0 kg = 4.0 kg. Additional Rate = 4.0 kg × 1.0 mL/kg/hr = 4.0 mL/hr."},
            {"step_title": "Hourly & 24-Hour Totals", "step_text": "Hourly Rate = 40.0 + 20.0 + 4.0 = 64.0 mL/hour. 24-Hour Volume = 64.0 mL/hr × 24 hrs = 1,536 mL/day."}
        ],
        "faqs": [
            {"q": "What is the Holliday-Segar rule based on?", "a": "Published in 1957, Malcolm Holliday and William Segar established that human caloric expenditure scales in tiers (100 kcal/kg for 1st 10 kg, 50 kcal/kg for next 10 kg, 20 kcal/kg above 20 kg). Because 1 mL of water is needed per 1 kcal expended, fluid requirements follow the exact same 4-2-1 hourly pattern."},
            {"q": "Why is hypotonic saline (D5 0.2% NS) no longer recommended for pediatric maintenance?", "a": "Modern pediatric clinical guidelines recommend isotonic fluids (D5 0.9% Normal Saline or Plasmalyte) to prevent hospital-acquired hyponatremia and cerebral edema."}
        ],
        "js_logic": """
          const wt = getNum('patient_body_weight_kg');

          if (wt > 0) {
            let hourly = 0;
            let tier = 'Tier 1 (≤ 10 kg Bracket)';

            if (wt <= 10) {
              hourly = wt * 4;
            } else if (wt <= 20) {
              hourly = 40 + (wt - 10) * 2;
              tier = 'Tier 2 (10 - 20 kg Bracket)';
            } else {
              hourly = 60 + (wt - 20) * 1;
              tier = 'Tier 3 (> 20 kg Bracket)';
            }

            const daily = hourly * 24;

            setMetric('hourly_maintenance_infusion_rate', hourly.toFixed(1) + ' mL/hr');
            setMetric('daily_maintenance_fluid_volume', Math.round(daily).toLocaleString() + ' mL / Day');
            setMetric('recommended_electrolyte_solution', 'D5 0.9% NS + 20 mEq/L KCl');
            setMetric('weight_tier_bracket', tier);
          }
        """
    },
    {
        "slug": "drug-volume-of-distribution",
        "category": "biotech",
        "name": "Apparent Volume of Distribution (Vd) & Loading Dose Calculator",
        "description": "Calculate apparent Volume of Distribution (Vd in L and L/kg) and determine exact intravenous or oral loading doses required to reach target plasma concentrations immediately.",
        "hero_badge": "Clinical Pharmacokinetics • Loading Dose",
        "formula_display": "Vd = Dose_IV / C₀ | Loading Dose = (Target Plasma Conc · Vd) / Bioavailability (F)",
        "fields": [
            {"id": "administered_iv_dose_mg", "label": "Administered IV Bolus Dose (mg)", "default": 500, "suffix": "mg", "min": 1, "max": 10000, "step": 25, "hint": "Intravenous dose administered at start of trial"},
            {"id": "extrapolated_peak_c0_mg_l", "label": "Extrapolated Peak Plasma Conc C₀ (mg/L)", "default": 12.5, "suffix": "mg/L", "min": 0.01, "max": 500, "step": 0.5, "hint": "Plasma level extrapolated back to time t=0"},
            {"id": "patient_body_weight_kg", "label": "Patient Weight (kg)", "default": 70.0, "suffix": "kg", "min": 10, "max": 250, "step": 1, "hint": "Patient weight to calculate normalized Vd (L/kg)"},
            {"id": "desired_target_plasma_conc", "label": "Desired Target Plasma Level (mg/L)", "default": 15.0, "suffix": "mg/L", "min": 0.1, "max": 500, "step": 0.5, "hint": "Therapeutic trough or peak target"}
        ],
        "metrics": [
            {"id": "apparent_volume_of_distribution_vd", "label": "Apparent Volume of Distribution (Vd)", "default_display": "40.0 Liters", "highlight": True},
            {"id": "normalized_vd_liters_per_kg", "label": "Normalized Vd (L/kg)", "default_display": "0.57 L/kg", "highlight": True},
            {"id": "calculated_target_loading_dose", "label": "Required Loading Dose (IV)", "default_display": "600.0 mg Loading Dose", "highlight": True},
            {"id": "tissue_binding_classification", "label": "Physiological Distribution Pattern", "default_display": "Total Body Water Distribution (~0.6 L/kg)"}
        ],
        "proof_steps": [
            {"step_title": "Apparent Volume of Distribution (Vd)", "step_text": "Vd = Dose / C₀ = 500 mg / 12.5 mg/L = 40.0 Liters."},
            {"step_title": "Normalized Weight Scaling", "step_text": "Normalized Vd = 40.0 L / 70.0 kg = 0.571 ≈ 0.57 L/kg."},
            {"step_title": "Target Loading Dose Calculation", "step_text": "Loading Dose = Target Conc (15.0 mg/L) × Vd (40.0 L) = 600.0 mg IV bolus."},
            {"step_title": "Physiological Interpretation", "step_text": "A Vd of ~0.6 L/kg corresponds roughly to total body water, indicating the drug penetrates both extracellular fluid and intracellular space without extreme tissue sequestration."}
        ],
        "faqs": [
            {"q": "Can Volume of Distribution exceed total human body volume?", "a": "Yes! Highly lipophilic drugs (like Chloroquine with a Vd of ~15,000 L, or Amiodarone with ~5,000 L) bind extensively to adipose tissue and organs, leaving almost zero drug in the bloodstream. Because Vd = Dose / Blood Conc, an extremely tiny blood concentration produces an apparent Vd thousands of liters larger than the human body."},
            {"q": "Why does clearance NOT affect the loading dose?", "a": "Loading dose depends entirely on Volume of Distribution (filling the tank), not clearance. Clearance only dictates the maintenance infusion rate (replenishing what leaks out)."}
        ],
        "js_logic": """
          const dose = getNum('administered_iv_dose_mg');
          const c0 = getNum('extrapolated_peak_c0_mg_l');
          const wt = getNum('patient_body_weight_kg');
          const target = getNum('desired_target_plasma_conc');

          if (c0 > 0 && wt > 0) {
            const vd = dose / c0;
            const vdLkg = vd / wt;
            const loading = target * vd;

            let pattern = 'Extracellular Fluid Restricted (~0.2 L/kg)';
            if (vdLkg < 0.1) pattern = 'Plasma Confined (< 0.1 L/kg)';
            else if (vdLkg >= 0.5 && vdLkg <= 0.8) pattern = 'Total Body Water Distribution (~0.6 L/kg)';
            else if (vdLkg > 1.0) pattern = 'Extensive Tissue Sequestration (> 1.0 L/kg)';

            setMetric('apparent_volume_of_distribution_vd', vd.toFixed(1) + ' Liters');
            setMetric('normalized_vd_liters_per_kg', vdLkg.toFixed(2) + ' L/kg');
            setMetric('calculated_target_loading_dose', loading.toFixed(1) + ' mg Loading Dose');
            setMetric('tissue_binding_classification', pattern);
          }
        """
    },
    {
        "slug": "cohen-d-effect-size",
        "category": "biotech",
        "name": "Biostatistical Cohen's d Effect Size & Standardized Mean Difference Calculator",
        "description": "Calculate Cohen's d, Hedges' g (unbiased small-sample adjustment), and pooled standard deviation to quantify standardized effect sizes across clinical trials.",
        "hero_badge": "Meta-Analysis • Statistical Effect Size",
        "formula_display": "Cohen's d = (μ₁ - μ₂) / s_pooled | s_pooled = √[((n₁ - 1)·s₁² + (n₂ - 1)·s₂²) / (n₁ + n₂ - 2)]",
        "fields": [
            {"id": "treatment_group_mean_m1", "label": "Treatment Group Mean (μ₁)", "default": 48.5, "suffix": "units", "min": -1000, "max": 1000, "step": 0.5, "hint": "Mean outcome score in experimental cohort"},
            {"id": "control_group_mean_m2", "label": "Control Group Mean (μ₂)", "default": 41.2, "suffix": "units", "min": -1000, "max": 1000, "step": 0.5, "hint": "Mean outcome score in control placebo cohort"},
            {"id": "treatment_std_dev_s1", "label": "Treatment Standard Deviation (s₁)", "default": 9.2, "suffix": "SD", "min": 0.1, "max": 500, "step": 0.1, "hint": "Standard deviation of treatment cohort"},
            {"id": "control_std_dev_s2", "label": "Control Standard Deviation (s₂)", "default": 8.8, "suffix": "SD", "min": 0.1, "max": 500, "step": 0.1, "hint": "Standard deviation of control cohort"},
            {"id": "sample_size_per_group_n", "label": "Sample Size Per Group (n)", "default": 45, "suffix": "n/group", "min": 3, "max": 10000, "step": 5, "hint": "Patients in each arm (assuming equal cohorts)"}
        ],
        "metrics": [
            {"id": "cohens_d_effect_size", "label": "Cohen's d Effect Size", "default_display": "0.81 (Large Effect Size)", "highlight": True},
            {"id": "hedges_g_unbiased", "label": "Hedges' g (Small-Sample Corrected)", "default_display": "0.80 Unbiased", "highlight": True},
            {"id": "pooled_standard_deviation", "label": "Pooled Standard Deviation (s_pooled)", "default_display": "9.00 SD Units", "highlight": True},
            {"id": "non_overlap_u3_percentage", "label": "Cohen's U₃ Distribution Non-Overlap", "default_display": "79.1% Superior to Control Mean"}
        ],
        "proof_steps": [
            {"step_title": "Pooled Variance Derivation", "step_text": "s_pooled = √[(s₁² + s₂²) / 2] = √[(9.2² + 8.8²) / 2] = √[(84.64 + 77.44) / 2] = √[162.08 / 2] = √81.04 = 9.002 ≈ 9.00."},
            {"step_title": "Cohen's d Standardized Difference", "step_text": "d = (48.5 - 41.2) / 9.002 = 7.3 / 9.002 = 0.811 ≈ 0.81."},
            {"step_title": "Hedges' g Correction Factor", "step_text": "Correction J ≈ 1 - [3 / (4 · df - 1)] = 1 - [3 / (4 · 88 - 1)] = 1 - [3 / 351] = 0.9915. Hedges' g = 0.811 × 0.9915 = 0.804 ≈ 0.80."},
            {"step_title": "Cohen's Benchmark Interpretation", "step_text": "d = 0.2 represents a small effect, d = 0.5 a medium effect, and d ≥ 0.8 represents a large clinical effect size, meaning the average treated patient scores higher than 79.1% of control subjects."}
        ],
        "faqs": [
            {"q": "Why is effect size superior to p-values in clinical trials?", "a": "A p-value merely tells you whether an effect is statistically distinguishable from zero; with a huge sample size, even a clinically trivial difference becomes statistically significant. Cohen's d measures the actual magnitude of the clinical improvement in standard deviation units."},
            {"q": "When must Hedges' g be used instead of Cohen's d?", "a": "When group sample size is small (n < 20 per group), Cohen's d systematically overestimates the true population effect size. Hedges' g applies an exact correction factor to eliminate this positive bias."}
        ],
        "js_logic": """
          const m1 = getNum('treatment_group_mean_m1');
          const m2 = getNum('control_group_mean_m2');
          const s1 = getNum('treatment_std_dev_s1');
          const s2 = getNum('control_std_dev_s2');
          const n = getNum('sample_size_per_group_n');

          const sPooled = Math.sqrt((Math.pow(s1, 2) + Math.pow(s2, 2)) / 2);
          if (sPooled > 0 && n > 1) {
            const d = (m1 - m2) / sPooled;
            const df = (2 * n) - 2;
            const j = 1 - (3 / (4 * df - 1));
            const g = d * j;

            let label = 'Trivial Effect (< 0.2)';
            if (Math.abs(d) >= 0.2 && Math.abs(d) < 0.5) label = 'Small Effect (0.2 - 0.5)';
            else if (Math.abs(d) >= 0.5 && Math.abs(d) < 0.8) label = 'Medium Effect (0.5 - 0.8)';
            else if (Math.abs(d) >= 0.8) label = 'Large Effect Size (≥ 0.8)';

            setMetric('cohens_d_effect_size', d.toFixed(2) + ' (' + label + ')');
            setMetric('hedges_g_unbiased', g.toFixed(2) + ' Unbiased');
            setMetric('pooled_standard_deviation', sPooled.toFixed(2) + ' SD Units');
            setMetric('non_overlap_u3_percentage', d > 0 ? (50 + Math.min(49, d * 35)).toFixed(1) + '% Superior to Control Mean' : 'Inferior to Control');
          }
        """
    },
    {
        "slug": "ld50-therapeutic-index",
        "category": "biotech",
        "name": "Toxicology Therapeutic Index (TI) & Margin of Safety (MOS) Calculator",
        "description": "Calculate Therapeutic Index (TI), Margin of Safety (MOS / Certain Safety Factor), and drug therapeutic window safety ratios from preclinical dose-response curves.",
        "hero_badge": "Preclinical Toxicology • Drug Safety",
        "formula_display": "Therapeutic Index (TI) = LD₅₀ / ED₅₀ | Margin of Safety (MOS) = LD₁ / ED₉₉",
        "fields": [
            {"id": "median_lethal_dose_ld50", "label": "Median Lethal Dose LD₅₀ (mg/kg)", "default": 450.0, "suffix": "mg/kg", "min": 0.1, "max": 10000, "step": 5, "hint": "Dose lethal to 50% of preclinical animal population"},
            {"id": "median_effective_dose_ed50", "label": "Median Effective Dose ED₅₀ (mg/kg)", "default": 25.0, "suffix": "mg/kg", "min": 0.01, "max": 1000, "step": 1, "hint": "Dose producing desired therapeutic effect in 50% of population"},
            {"id": "minimal_lethal_dose_ld1", "label": "Minimal Lethal Dose LD₁ (mg/kg)", "default": 180.0, "suffix": "mg/kg", "min": 0.1, "max": 5000, "step": 5, "hint": "Dose lethal to 1% of population (start of toxicity curve)"},
            {"id": "maximal_effective_dose_ed99", "label": "Maximal Effective Dose ED₉₉ (mg/kg)", "default": 60.0, "suffix": "mg/kg", "min": 0.1, "max": 2000, "step": 2, "hint": "Dose effective in 99% of population"}
        ],
        "metrics": [
            {"id": "therapeutic_index_ratio", "label": "Therapeutic Index (TI)", "default_display": "18.00 (Wide Therapeutic Window)", "highlight": True},
            {"id": "margin_of_safety_mos", "label": "Margin of Safety (MOS)", "default_display": "3.00 Certain Safety Factor", "highlight": True},
            {"id": "safety_tier_classification", "label": "Clinical Safety Profile", "default_display": "Safe Pharmaceutical Agent (TI > 10)"},
            {"id": "dose_overlap_check", "label": "Lethal / Efficacious Overlap", "default_display": "Zero Toxic Overlap (LD₁ > ED₉₉)"}
        ],
        "proof_steps": [
            {"step_title": "Therapeutic Index (TI) Derivation", "step_text": "Therapeutic Index = LD₅₀ / ED₅₀ = 450.0 mg/kg / 25.0 mg/kg = 18.00. The median lethal dose is 18 times higher than the median effective dose."},
            {"step_title": "Margin of Safety (Certain Safety Factor MOS)", "step_text": "MOS = LD₁ / ED₉₉ = 180.0 mg/kg / 60.0 mg/kg = 3.00. Because MOS > 1.0, the dose required to cure 99% of patients is 3 times lower than the dose that causes toxicity in even 1%."},
            {"step_title": "Preclinical Safety Significance", "step_text": "A drug with TI > 10 and MOS > 1.0 represents an exceptionally favorable safety profile, qualifying for progression into Phase I First-in-Human clinical trials."}
        ],
        "faqs": [
            {"q": "Why is Margin of Safety (MOS) safer than Therapeutic Index (TI)?", "a": "TI compares median 50% points, which ignores the slope of dose-response curves. If the toxicity curve has a very steep slope, a drug with an apparently safe TI of 10 might have an LD₁ lower than the ED₉₉ (meaning patients could die before reaching 99% efficacy). MOS tests the extreme tails (LD₁ vs ED₉₉)."},
            {"q": "What is an example of a drug with a Narrow Therapeutic Index (NTI)?", "a": "Digoxin, Warfarin, Lithium, and Theophylline have narrow therapeutic indices (TI < 2.0). Small dosage variations or drug-drug interactions can quickly cause severe clinical toxicity."}
        ],
        "js_logic": """
          const ld50 = getNum('median_lethal_dose_ld50');
          const ed50 = getNum('median_effective_dose_ed50');
          const ld1 = getNum('minimal_lethal_dose_ld1');
          const ed99 = getNum('maximal_effective_dose_ed99');

          if (ed50 > 0 && ed99 > 0) {
            const ti = ld50 / ed50;
            const mos = ld1 / ed99;

            let tier = 'Narrow Therapeutic Index (NTI - High Toxicity Risk)';
            if (ti >= 10) tier = 'Safe Pharmaceutical Agent (TI > 10)';
            else if (ti >= 3 && ti < 10) tier = 'Moderate Therapeutic Window (TI 3-10)';

            const overlap = mos >= 1.0 ? 'Zero Toxic Overlap (LD₁ > ED₉₉)' : 'Dangerous Curve Overlap (LD₁ < ED₉₉)';

            setMetric('therapeutic_index_ratio', ti.toFixed(2) + (ti >= 10 ? ' (Wide Therapeutic Window)' : ' (Narrow Window)'));
            setMetric('margin_of_safety_mos', mos.toFixed(2) + ' Certain Safety Factor');
            setMetric('safety_tier_classification', tier);
            setMetric('dose_overlap_check', overlap);
          }
        """
    }
]
