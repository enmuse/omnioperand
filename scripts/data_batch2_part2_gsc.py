"""
scripts/data_batch2_part2_gsc.py
Definitions for calculators 11 through 22 of GSC Batch 2.
"""

BATCH2_PART2_CALCULATORS = [
    # 11. Column Slenderness Ratio & Critical Buckling Load Calculator (Position 74.0 in GSC!)
    {
        'slug': 'engineering/column-slenderness-buckling',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Column Slenderness Ratio & Critical Buckling Load Calculator',
        'title': 'Column Slenderness Ratio & Euler Buckling Calculator | OmniOperand',
        'description': 'Calculate column effective slenderness ratio (KL/r), Euler critical buckling stress, and compressive load capacity under AISC 360 standards.',
        'hero_badge': 'Structural Mechanics & Steel Design • AISC 360-22 Standard',
        'hero_subtext': 'Calculate effective slenderness ratio (KL/r), Euler elastic buckling stress (Fe), and nominal axial compressive buckling strength under AISC 360-22.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'col_len_ft', 'label': 'Unbraced Column Length (L)', 'type': 'number', 'default': 14, 'min': 1, 'max': 100, 'step': 0.5, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Distance between lateral bracing points'},
            {'id': 'end_condition', 'label': 'End Restraint / Effective Length (K)', 'type': 'select', 'default': '1.0', 'options': [
                ['1.0', 'Pinned-Pinned (K = 1.0 • Standard Ideal Hinged Ends)'],
                ['0.5', 'Fixed-Fixed (K = 0.5 • Fully Rigid Moment Connections)'],
                ['0.7', 'Fixed-Pinned (K = 0.7 • One Fixed, One Pinned)'],
                ['2.0', 'Fixed-Free Cantilever (K = 2.0 • Flagpole / Unbraced Frame)']
            ], 'hint': 'AISC 360 effective length factor'},
            {'id': 'cross_area', 'label': 'Cross-Sectional Area (A)', 'type': 'number', 'default': 14.4, 'min': 0.5, 'max': 500, 'step': 0.1, 'unit': 'sq in', 'metric_unit': 'cm²', 'hint': 'Total cross-sectional metal area (W10×49 has A = 14.4 in²)'},
            {'id': 'radius_gyr', 'label': 'Least Radius of Gyration (r_min)', 'type': 'number', 'default': 2.54, 'min': 0.2, 'max': 30, 'step': 0.05, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'r = √(I/A) about weak axis (r_y)'},
            {'id': 'yield_fy', 'label': 'Steel Yield Strength (Fy)', 'type': 'number', 'default': 50, 'min': 30, 'max': 100, 'step': 5, 'unit': 'ksi', 'metric_unit': 'MPa', 'hint': '50 ksi for ASTM A992; 36 ksi for A36'}
        ],
        'outputs': [
            {'id': 'slenderness_ratio', 'label': 'Effective Slenderness Ratio (KL/r)', 'unit': 'dimensionless', 'color': 'var(--accent-cyan)'},
            {'id': 'euler_fe', 'label': 'Euler Elastic Buckling Stress (Fe)', 'unit': 'ksi', 'color': 'var(--text-bright)'},
            {'id': 'fcr_stress', 'label': 'AISC Critical Buckling Stress (Fcr)', 'unit': 'ksi', 'color': 'var(--accent-emerald)'},
            {'id': 'nominal_load_pn', 'label': 'Nominal Axial Buckling Capacity (Pn)', 'unit': 'kips (tons)', 'color': 'var(--accent-purple)'},
            {'id': 'buckling_mode', 'label': 'Buckling Mode Classification', 'unit': 'status', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'λ = (K · L) / r | F_e = (π² · E) / (KL/r)² | If KL/r ≤ 4.71√(E/Fy): Fcr = [0.658^(Fy/Fe)] · Fy',
        'proof_steps': [
            {'step_title': '1. Effective Slenderness Ratio', 'step_text': 'Slenderness measures column susceptibility to geometric buckling: λ = (K × L × 12) / r. The maximum recommended slenderness under AISC 360 is λ ≤ 200.'},
            {'step_title': '2. Euler Critical Buckling Stress', 'step_text': 'For an ideal elastic column with modulus E = 29,000 ksi: F_e = (π² × E) / λ².'},
            {'step_title': '3. Inelastic vs Elastic AISC 360 Transition', 'step_text': 'The transition slenderness threshold is 4.71 × √(E / Fy) (approx 113.8 for 50 ksi steel). Below this limit, inelastic buckling and residual stresses govern: Fcr = [0.658^(Fy/Fe)] × Fy. Above this limit, elastic buckling governs: Fcr = 0.877 × Fe.'}
        ],
        'faqs': [
            {'q': 'What is a good slenderness ratio for structural columns?', 'a': 'AISC 360 recommends an upper limit of KL/r ≤ 200 for compression members. Highly efficient main building columns typically operate at KL/r between 40 and 90.'},
            {'q': 'Why does a column buckle about its weak axis?', 'a': 'Buckling occurs about the axis with the smallest moment of inertia and least radius of gyration (r_min), as this requires the lowest strain energy to deform.'},
            {'q': 'What is the K factor in column design?', 'a': 'K is the effective length factor representing the distance between inflection points of curvature. A column pinned at both ends has K=1.0, while fixed-fixed ends cut effective length in half (K=0.5).'}
        ],
        'js_logic': """
          const l_ft = getNum('col_len_ft') || 14;
          const k = parseFloat(document.getElementById('param-end_condition').value) || 1.0;
          const a = getNum('cross_area') || 14.4;
          const r = getNum('radius_gyr') || 2.54;
          const fy = getNum('yield_fy') || 50;
          const e = 29000;
          const kl_r = (k * l_ft * 12) / r;
          const fe = (Math.PI * Math.PI * e) / (kl_r * kl_r);
          const transition = 4.71 * Math.sqrt(e / fy);
          let fcr = 0;
          let mode = 'Inelastic Buckling (Yielding Dominated)';
          if (kl_r <= transition) {
            fcr = Math.pow(0.658, fy / fe) * fy;
            mode = 'Inelastic Buckling (AISC Eq E3-2)';
          } else {
            fcr = 0.877 * fe;
            mode = 'Elastic Buckling (Euler Euler Eq E3-3)';
          }
          const pn_kips = fcr * a;
          const pn_tons = pn_kips / 2;
          setDisp('slenderness_ratio', fmt(kl_r, 1) + (kl_r > 200 ? ' ⚠️ (> 200 AISC limit)' : ' ✅ (≤ 200)'));
          setDisp('euler_fe', fmt(fe, 1) + ' ksi');
          setDisp('fcr_stress', fmt(fcr, 1) + ' ksi');
          setDisp('nominal_load_pn', fmt(pn_kips, 1) + ' kips (' + fmt(pn_tons, 1) + ' Tons)');
          setDisp('buckling_mode', mode);
        """
    },

    # 12. Unistrut Channel Beam Load & Deflection Calculator (Position 78.0 in GSC!)
    {
        'slug': 'construction/unistrut-load-capacity',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Unistrut Channel Beam Load & Deflection Calculator',
        'title': 'Unistrut Load Capacity Calculator: Span & Deflection Limits | OmniOperand',
        'description': 'Calculate maximum allowable beam load and deflection for standard Unistrut metal framing channels (P1000, P2000, P5000, P1001 back-to-back).',
        'hero_badge': 'Structural Framing & MEP Supports • MFMA-4 Standards',
        'hero_subtext': 'Determine maximum beam load capacity, center span deflection, and allowable span limits for Unistrut metal framing channels under MFMA standards.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'channel_profile', 'label': 'Unistrut Channel Profile', 'type': 'select', 'default': 'P1000', 'options': [
                ['P1000', 'P1000 (1-5/8" × 1-5/8" • 12 Gauge • Flagship Channel)'],
                ['P2000', 'P2000 (1-5/8" × 1-5/8" • 16 Gauge • Standard Duty)'],
                ['P3300', 'P3300 (1-5/8" × 7/8" • 12 Gauge • Shallow Profile)'],
                ['P5000', 'P5000 (1-5/8" × 3-1/4" • 12 Gauge • Deep Heavy-Duty)'],
                ['P1001', 'P1001 (1-5/8" × 3-1/4" • Double Back-to-Back Welded)']
            ], 'hint': 'Cold-formed steel strut series'},
            {'id': 'span_len_in', 'label': 'Clear Beam Span Length', 'type': 'number', 'default': 48, 'min': 12, 'max': 300, 'step': 6, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Distance between support hangers or brackets'},
            {'id': 'load_type', 'label': 'Applied Load Type', 'type': 'select', 'default': 'uniform', 'options': [
                ['uniform', 'Uniformly Distributed Load (Pipes, Cable Trays)'],
                ['point', 'Concentrated Point Load at Center Span (Single Heavy Equipment)']
            ], 'hint': 'Weight distribution pattern'},
            {'id': 'deflection_limit', 'label': 'Maximum Deflection Ratio', 'type': 'select', 'default': '240', 'options': [
                ['240', 'L / 240 (Standard Commercial MEP Piping & Conduit)'],
                ['360', 'L / 360 (Stricter Deflection for Sensitive Equipment)'],
                ['180', 'L / 180 (Industrial Utility Framing)']
            ], 'hint': 'Deflection serviceability threshold'}
        ],
        'outputs': [
            {'id': 'allowable_load', 'label': 'Allowable Design Load Capacity', 'unit': 'lbs (kg)', 'color': 'var(--accent-cyan)'},
            {'id': 'deflection_at_allow', 'label': 'Deflection at Allowable Load', 'unit': 'in (mm)', 'color': 'var(--text-bright)'},
            {'id': 'load_at_def_limit', 'label': 'Load Governed by Deflection Limit', 'unit': 'lbs', 'color': 'var(--accent-emerald)'},
            {'id': 'governing_factor', 'label': 'Controlling Design Constraint', 'unit': 'status', 'color': 'var(--accent-purple)'},
            {'id': 'section_modulus', 'label': 'Section Properties (S / I)', 'unit': 'in³ / in⁴', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Uniform: W = (8 · S · σ_allow) / L | Deflection Δ = (5 · W · L³) / (384 · E · I) | σ_allow = 25,000 psi',
        'proof_steps': [
            {'step_title': '1. Flexural Bending Strength Capacity', 'step_text': 'MFMA-4 specifies allowable bending stress of 25,000 psi for cold-formed steel strut channels. For uniform load, maximum moment is M = W · L / 8 = S · σ_allow, yielding W = (8 · S · 25,000) / L.'},
            {'step_title': '2. Elastic Deflection Formulation', 'step_text': 'For modulus E = 29,500,000 psi, center deflection under total uniform load W is Δ = (5 · W · L³) / (384 · E · I). For center point load P, deflection is Δ = (P · L³) / (48 · E · I).'},
            {'step_title': '3. Dual Failure Mode Comparison', 'step_text': 'Long spans are governed by serviceability deflection limits (L/240 or L/360) rather than structural yield strength.'}
        ],
        'faqs': [
            {'q': 'How much weight can a 10-foot Unistrut hold?', 'a': 'A standard 12-gauge P1000 Unistrut over a 10-foot (120-inch) span can support approximately 280 lbs of uniformly distributed load before exceeding stress limits, but deflection will be ~1.0 inch.'},
            {'q': 'What is the strongest Unistrut profile?', 'a': 'P1001 (double back-to-back 12-gauge welded channel) and P5000 (3-1/4" deep single channel) provide over 4 to 5 times the load capacity of standard P1000.'},
            {'q': 'What is the allowable stress for Unistrut?', 'a': 'The Metal Framing Manufacturers Association (MFMA) standards specify an allowable design bending stress of 25,000 psi based on a 1.67 safety factor on 33,000 psi yield cold-formed steel.'}
        ],
        'js_logic': """
          const prof = document.getElementById('param-channel_profile').value;
          const l_in = getNum('span_len_in') || 48;
          const ltype = document.getElementById('param-load_type').value;
          const def_ratio = parseFloat(document.getElementById('param-deflection_limit').value) || 240;
          let s = 0.297, i_xx = 0.185;
          if (prof === 'P2000') { s = 0.208; i_xx = 0.124; }
          else if (prof === 'P3300') { s = 0.154; i_xx = 0.057; }
          else if (prof === 'P5000') { s = 1.127; i_xx = 1.487; }
          else if (prof === 'P1001') { s = 1.144; i_xx = 1.571; }
          const sigma_allow = 25000;
          const e_mod = 29500000;
          let w_stress = 0;
          if (ltype === 'uniform') {
            w_stress = (8 * s * sigma_allow) / l_in;
          } else {
            w_stress = (4 * s * sigma_allow) / l_in;
          }
          let delta_at_w = 0;
          if (ltype === 'uniform') {
            delta_at_w = (5 * w_stress * Math.pow(l_in, 3)) / (384 * e_mod * i_xx);
          } else {
            delta_at_w = (w_stress * Math.pow(l_in, 3)) / (48 * e_mod * i_xx);
          }
          const max_allow_delta = l_in / def_ratio;
          let w_deflection = 0;
          if (ltype === 'uniform') {
            w_deflection = (384 * e_mod * i_xx * max_allow_delta) / (5 * Math.pow(l_in, 3));
          } else {
            w_deflection = (48 * e_mod * i_xx * max_allow_delta) / Math.pow(l_in, 3);
          }
          const final_allow_load = Math.min(w_stress, w_deflection);
          const governing = (w_deflection < w_stress) ? 'Deflection Limited (L/' + def_ratio + ')' : 'Flexural Bending Stress Limited (25,000 psi)';
          const final_kg = final_allow_load * 0.453592;
          setDisp('allowable_load', fmt(final_allow_load, 0) + ' lbs (' + fmt(final_kg, 0) + ' kg)');
          setDisp('deflection_at_allow', fmt(delta_at_w, 3) + ' in (Max allow: ' + fmt(max_allow_delta, 3) + ' in)');
          setDisp('load_at_def_limit', fmt(w_deflection, 0) + ' lbs');
          setDisp('governing_factor', governing);
          setDisp('section_modulus', 'S = ' + s + ' in³ | I = ' + i_xx + ' in⁴');
        """
    },

    # 13. Relative Response Factor (RRF) HPLC Calculator (Position 79.0 in GSC!)
    {
        'slug': 'biotech/relative-response-factor-rrf',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Relative Response Factor (RRF) HPLC Calculator',
        'title': 'Relative Response Factor (RRF) HPLC Calculator: Impurity Assay | OmniOperand',
        'description': 'Calculate HPLC/GC relative response factors (RRF) and true impurity weight percentages in pharmaceutical drug substances under ICH Q3A/B.',
        'hero_badge': 'Pharmaceutical Analytical Chemistry • ICH Q3A/B & USP <621>',
        'hero_subtext': 'Determine HPLC/GC Relative Response Factors (RRF), response factor corrections, and exact pharmaceutical impurity weight percentages.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'area_imp', 'label': 'Impurity Peak Area (Standard)', 'type': 'number', 'default': 125000, 'min': 100, 'max': 50000000, 'step': 1000, 'unit': 'area counts', 'hint': 'Peak area of known impurity reference standard'},
            {'id': 'conc_imp', 'label': 'Impurity Standard Concentration', 'type': 'number', 'default': 0.005, 'min': 0.0001, 'max': 10, 'step': 0.0005, 'unit': 'mg/mL', 'hint': 'Known concentration of impurity solution'},
            {'id': 'area_api', 'label': 'Main API Peak Area (Standard)', 'type': 'number', 'default': 2100000, 'min': 1000, 'max': 100000000, 'step': 10000, 'unit': 'area counts', 'hint': 'Peak area of Active Pharmaceutical Ingredient standard'},
            {'id': 'conc_api', 'label': 'Main API Standard Concentration', 'type': 'number', 'default': 0.100, 'min': 0.001, 'max': 50, 'step': 0.005, 'unit': 'mg/mL', 'hint': 'Known concentration of API standard solution'},
            {'id': 'sample_imp_area', 'label': 'Sample Observed Impurity Area', 'type': 'number', 'default': 4500, 'min': 10, 'max': 10000000, 'step': 100, 'unit': 'area counts', 'hint': 'Peak area of impurity in real stability/release sample'},
            {'id': 'sample_total_conc', 'label': 'Test Sample Nominal Concentration', 'type': 'number', 'default': 1.0, 'min': 0.01, 'max': 100, 'step': 0.1, 'unit': 'mg/mL', 'hint': 'Total nominal sample concentration injected'}
        ],
        'outputs': [
            {'id': 'rrf_value', 'label': 'Relative Response Factor (RRF)', 'unit': 'ratio', 'color': 'var(--accent-cyan)'},
            {'id': 'correction_factor', 'label': 'Multiplier Correction Factor (1 / RRF)', 'unit': 'factor', 'color': 'var(--text-bright)'},
            {'id': 'true_impurity_pct', 'label': 'True Corrected Impurity Level', 'unit': '% (w/w)', 'color': 'var(--accent-emerald)'},
            {'id': 'raw_area_pct', 'label': 'Uncorrected Area % (Raw)', 'unit': '% area', 'color': 'var(--text-bright)'},
            {'id': 'ich_status', 'label': 'ICH Q3A Reporting Threshold Assessment', 'unit': 'status', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'RRF = (Area_imp / Conc_imp) / (Area_std / Conc_std) | % Impurity = [ (Area_sample_imp · Conc_std) / (Area_std · Conc_sample · RRF) ] · 100',
        'proof_steps': [
            {'step_title': '1. Response Factor (Slope) Derivation', 'step_text': 'The detector response factor RF represents detector sensitivity (Peak Area / Concentration). Relative Response Factor is the sensitivity ratio: RRF = RF_impurity / RF_API.'},
            {'step_title': '2. Quantitative Impurity Concentration', 'step_text': 'If an impurity has a weak chromophore (RRF < 1.0), it absorbs less UV light per mole than the API. Using raw area percent underestimates the impurity. Dividing by RRF scales it up to true mass balance.'},
            {'step_title': '3. Regulatory Thresholds', 'step_text': 'ICH Q3A/B mandates that any RRF outside 0.8 to 1.2 MUST be explicitly applied. If RRF is between 0.9 and 1.1, a factor of 1.0 is sometimes acceptable.'}
        ],
        'faqs': [
            {'q': 'What does an RRF of 0.5 mean?', 'a': 'An RRF of 0.5 means the impurity responds half as strongly to the UV detector as the main drug substance. Therefore, the actual mass percentage of the impurity is double (1 / 0.5 = 2.0x) its raw area percent.'},
            {'q': 'Why is RRF required by the FDA and ICH?', 'a': 'Different chemical structures have different extinction coefficients (UV absorbance). Using uncorrected peak area percentages introduces significant analytical error in stability testing and toxicological impurity evaluation.'},
            {'q': 'What is the ICH reporting threshold for impurities?', 'a': 'For pharmaceuticals with a maximum daily dose ≤ 2g/day, the ICH Q3A reporting threshold is 0.05%, the identification threshold is 0.10%, and the qualification threshold is 0.15%.'}
        ],
        'js_logic': """
          const a_imp = getNum('area_imp') || 125000;
          const c_imp = getNum('conc_imp') || 0.005;
          const a_api = getNum('area_api') || 2100000;
          const c_api = getNum('conc_api') || 0.100;
          const a_samp_imp = getNum('sample_imp_area') || 4500;
          const c_samp = getNum('sample_total_conc') || 1.0;
          const rf_imp = a_imp / c_imp;
          const rf_api = a_api / c_api;
          const rrf = rf_imp / rf_api;
          const cf = 1 / rrf;
          const true_pct = ((a_samp_imp * c_api) / (a_api * c_samp * rrf)) * 100;
          const raw_pct = (a_samp_imp / a_api) * (c_api / c_samp) * 100;
          let ich = 'Below 0.05% (Does Not Require Reporting)';
          if (true_pct > 0.15) ich = '⚠️ > 0.15% (Exceeds ICH Qualification Threshold)';
          else if (true_pct > 0.10) ich = '⚠️ > 0.10% (Requires Chemical Identification)';
          else if (true_pct >= 0.05) ich = '✓ ≥ 0.05% (Must Be Reported on COA)';
          setDisp('rrf_value', fmt(rrf, 3));
          setDisp('correction_factor', fmt(cf, 3) + 'x');
          setDisp('true_impurity_pct', fmt(true_pct, 3) + '% (w/w)');
          setDisp('raw_area_pct', fmt(raw_pct, 3) + '% (Uncorrected)');
          setDisp('ich_status', ich);
        """
    },

    # 14. Micromolar to ng/mL Mass-Molar Concentration Converter (Position 79.0 in GSC!)
    {
        'slug': 'biotech/molar-mass-concentration-converter',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Micromolar to ng/mL Mass-Molar Concentration Converter',
        'title': 'Micromolar to ng/mL Converter: Molarity to Mass Concentration | OmniOperand',
        'description': 'Convert molarity (µM, nM, mM) to mass concentration (ng/mL, µg/mL, mg/L) with molecular weight. Precision pharmacology and cell culture tool.',
        'hero_badge': 'Quantitative Biochemistry & Pharmacology • IUPAC Invariants',
        'hero_subtext': 'Bidirectionally convert molar concentration (µM, nM, mM) into mass concentration (ng/mL, µg/mL, mg/L) with molecular weight and total mass delivery.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'molar_val', 'label': 'Molar Concentration Value', 'type': 'number', 'default': 10, 'min': 0.00001, 'max': 100000, 'step': 0.5, 'unit': 'value', 'hint': 'Concentration number'},
            {'id': 'molar_unit', 'label': 'Input Molar Unit', 'type': 'select', 'default': 'uM', 'options': [
                ['uM', 'Micromolar (µM • 10⁻⁶ M)'],
                ['nM', 'Nanomolar (nM • 10⁻⁹ M)'],
                ['pM', 'Picomolar (pM • 10⁻¹² M)'],
                ['mM', 'Millimolar (mM • 10⁻³ M)'],
                ['M', 'Molar (M • mol/L)']
            ], 'hint': 'SI molarity prefix'},
            {'id': 'mol_weight', 'label': 'Molecular Weight (MW)', 'type': 'number', 'default': 450.5, 'min': 1, 'max': 2000000, 'step': 1, 'unit': 'g/mol (Da)', 'hint': 'Molecular mass (e.g. 180.16 for glucose, 450 for small molecules, 150000 for IgG antibodies)'},
            {'id': 'sol_volume', 'label': 'Assay Solution Volume', 'type': 'number', 'default': 10, 'min': 0.001, 'max': 10000, 'step': 1, 'unit': 'mL', 'hint': 'Total liquid volume'}
        ],
        'outputs': [
            {'id': 'mass_ng_ml', 'label': 'Mass Concentration in ng/mL', 'unit': 'ng/mL (ppb)', 'color': 'var(--accent-cyan)'},
            {'id': 'mass_ug_ml', 'label': 'Mass Concentration in µg/mL', 'unit': 'µg/mL (mg/L / ppm)', 'color': 'var(--accent-emerald)'},
            {'id': 'total_solute_mass', 'label': 'Total Dissolved Mass in Volume', 'unit': 'µg (micrograms)', 'color': 'var(--text-bright)'},
            {'id': 'molarity_full', 'label': 'Molarity in Scientific Notation', 'unit': 'mol/L', 'color': 'var(--accent-purple)'},
            {'id': 'molecules_count', 'label': 'Total Molecules in Solution', 'unit': 'molecules', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Mass Conc (ng/mL) = Conc (µM) · MW (g/mol) | Mass (µg) = Conc (µg/mL) · Volume (mL)',
        'proof_steps': [
            {'step_title': '1. The 1:1 Identity Between µM and ng/mL', 'step_text': 'By dimensional analysis: 1 µM = 10⁻⁶ mol/L = 10⁻⁹ mol/mL. Multiplying by MW (g/mol = 10⁹ ng/mol) yields: Conc (ng/mL) = Conc (µM) × MW (g/mol). For example, 1 µM of a 500 g/mol compound is exactly 500 ng/mL.'},
            {'step_title': '2. Unit Conversion Ladder', 'step_text': '1 µg/mL = 1,000 ng/mL = 1 mg/L = 1 ppm. 1 nM of a substance equals (MW / 1,000) ng/mL.'},
            {'step_title': '3. Avogadro Molecular Particle Count', 'step_text': 'Total moles in volume V (liters) is n = Molarity × V. Total particle count is N = n × N_A, where N_A = 6.02214076 × 10²³ molecules/mol.'}
        ],
        'faqs': [
            {'q': 'How do you convert micromolar (µM) to ng/mL?', 'a': 'Simply multiply the micromolar concentration by the molecular weight of the substance in g/mol: ng/mL = µM × MW. For example, 10 µM of a drug with MW = 400 g/mol equals 4,000 ng/mL (4 µg/mL).'},
            {'q': 'Why is molecular weight required to convert µM to ng/mL?', 'a': 'Micromolar is a count of molecules per liter, while ng/mL is physical mass per milliliter. Because different molecules have different masses, you cannot convert between them without knowing molecular weight.'},
            {'q': 'Is 1 µg/mL the same as 1 mg/L?', 'a': 'Yes. 1 µg/mL is mathematically identical to 1 mg/L and 1 part-per-million (ppm) in aqueous solutions.'}
        ],
        'js_logic': """
          const val = getNum('molar_val') || 10;
          const unit = document.getElementById('param-molar_unit').value;
          const mw = getNum('mol_weight') || 450.5;
          const vol_ml = getNum('sol_volume') || 10;
          let molarity = val * 1e-6; // default uM
          if (unit === 'nM') molarity = val * 1e-9;
          else if (unit === 'pM') molarity = val * 1e-12;
          else if (unit === 'mM') molarity = val * 1e-3;
          else if (unit === 'M') molarity = val;
          const g_per_l = molarity * mw;
          const ug_per_ml = g_per_l * 1000;
          const ng_per_ml = ug_per_ml * 1000;
          const total_ug = ug_per_ml * vol_ml;
          const vol_l = vol_ml / 1000;
          const total_moles = molarity * vol_l;
          const molecules = total_moles * 6.02214076e23;
          setDisp('mass_ng_ml', fmt(ng_per_ml, 2) + ' ng/mL');
          setDisp('mass_ug_ml', fmt(ug_per_ml, 3) + ' µg/mL');
          setDisp('total_solute_mass', fmt(total_ug, 2) + ' µg (' + fmt(total_ug / 1000, 3) + ' mg)');
          setDisp('molarity_full', molarity.toExponential(4) + ' M');
          setDisp('molecules_count', molecules.toExponential(3) + ' molecules');
        """
    },

    # 15. Concrete Haunch & Chamfer Reinforcement Calculator (Position 80.0 in GSC!)
    {
        'slug': 'engineering/concrete-haunch-reinforcement',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Concrete Haunch & Chamfer Reinforcement Calculator',
        'title': 'Concrete Haunch Reinforcement Calculator: Shear & Rebar Detailing | OmniOperand',
        'description': 'Calculate dimensions, bevel angle, diagonal rebar lengths, and shear capacity enhancement for reinforced concrete beam-column haunches.',
        'hero_badge': 'Structural Concrete Design • ACI 318-19 / AASHTO LRFD',
        'hero_subtext': 'Calculate concrete haunch geometry, diagonal face length, development hook lengths, and shear capacity enhancement under ACI 318 / AASHTO.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'haunch_len_bh', 'label': 'Haunch Horizontal Run (b_h)', 'type': 'number', 'default': 24, 'min': 4, 'max': 240, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Horizontal length along beam soffit'},
            {'id': 'haunch_drop_hh', 'label': 'Haunch Vertical Depth (h_h)', 'type': 'number', 'default': 18, 'min': 4, 'max': 240, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Vertical depth down column face'},
            {'id': 'beam_width', 'label': 'Beam Stem Width (b_w)', 'type': 'number', 'default': 16, 'min': 6, 'max': 120, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Width of concrete beam'},
            {'id': 'beam_depth', 'label': 'Standard Beam Depth (d)', 'type': 'number', 'default': 30, 'min': 8, 'max': 180, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Effective beam depth excluding haunch'},
            {'id': 'rebar_size', 'label': 'Haunch Diagonal Rebar Size', 'type': 'select', 'default': '6', 'options': [
                ['4', '#4 Bar (0.500" dia • Area 0.20 in²)'],
                ['5', '#5 Bar (0.625" dia • Area 0.31 in²)'],
                ['6', '#6 Bar (0.750" dia • Area 0.44 in²)'],
                ['7', '#7 Bar (0.875" dia • Area 0.60 in²)'],
                ['8', '#8 Bar (1.000" dia • Area 0.79 in²)']
            ], 'hint': 'Internal diagonal tension rebar'},
            {'id': 'concrete_fc', 'label': 'Concrete Strength (f\'c)', 'type': 'number', 'default': 4000, 'min': 2500, 'max': 12000, 'step': 500, 'unit': 'psi', 'metric_unit': 'MPa', 'hint': 'Specified compressive strength'}
        ],
        'outputs': [
            {'id': 'haunch_angle', 'label': 'Haunch Chamfer Bevel Angle (θ)', 'unit': 'degrees', 'color': 'var(--text-bright)'},
            {'id': 'diag_length', 'label': 'Haunch Diagonal Face Length', 'unit': 'in (cm)', 'color': 'var(--accent-cyan)'},
            {'id': 'rebar_cut_len', 'label': 'Recommended Rebar Cut Length (inc. hooks)', 'unit': 'in', 'color': 'var(--accent-emerald)'},
            {'id': 'shear_vc', 'label': 'Enhanced Shear Capacity (φVc)', 'unit': 'kips', 'color': 'var(--accent-purple)'},
            {'id': 'haunch_concrete_vol', 'label': 'Concrete Volume per Haunch', 'unit': 'cu ft (yd³)', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'θ = arctan(h_h / b_h) | L_diag = √(b_h² + h_h²) | V_c = 2 · √(f\'c) · b_w · d · [ 1 + tan(θ) ]',
        'proof_steps': [
            {'step_title': '1. Right Triangular Haunch Geometry', 'step_text': 'The haunch forms a right triangular bracket beneath the beam soffit. Diagonal face length is L_diag = √(b_h² + h_h²). The slope angle relative to horizontal is θ = arctan(h_h / b_h).'},
            {'step_title': '2. Rebar Development & Hook Lengths', 'step_text': 'Diagonal rebar resists re-entrant corner tension. Total cut length requires the hypotenuse plus two standard 90-degree ACI 318 hooks: L_cut = L_diag + 2 · (12 · d_bar).'},
            {'step_title': '3. ACI 318 Shear Capacity Enhancement', 'step_text': 'Variable depth beams resist shear through both concrete web action and the vertical component of the inclined compressive chord: V_c = 2 · √(f\'c) · b_w · d · (1 + tan θ).'}
        ],
        'faqs': [
            {'q': 'What is the purpose of a haunch in concrete beams and portals?', 'a': 'A haunch increases the effective depth of a beam near its column connection where negative bending moments and shear stresses reach their maximum, reducing deflection without adding dead weight across the mid-span.'},
            {'q': 'What angle should a concrete haunch be?', 'a': 'In building construction and bridge piers, standard haunch angles are typically 30° to 45° (a 1:1 to 1:2 vertical-to-horizontal slope ratio) to ensure smooth stress flow and easy formwork stripping.'},
            {'q': 'How is rebar placed in a haunch?', 'a': 'Diagonal tension bars are placed parallel to the haunch slope and anchored with hooks into the column core and beam compression zone, supplemented by closed stirrups.'}
        ],
        'js_logic': """
          const bh = getNum('haunch_len_bh') || 24;
          const hh = getNum('haunch_drop_hh') || 18;
          const bw = getNum('beam_width') || 16;
          const d = getNum('beam_depth') || 30;
          const bar_num = parseInt(document.getElementById('param-rebar_size').value) || 6;
          const fc = getNum('concrete_fc') || 4000;
          const d_bar = bar_num / 8;
          const diag = Math.sqrt(bh * bh + hh * hh);
          const angle_rad = Math.atan2(hh, bh);
          const angle_deg = angle_rad * (180 / Math.PI);
          const hook_len = 12 * d_bar;
          const cut_len = diag + (2 * hook_len);
          const vc_standard = (2 * Math.sqrt(fc) * bw * d) / 1000;
          const phi = 0.75;
          const phi_vc_enhanced = phi * vc_standard * (1 + Math.tan(angle_rad));
          const vol_cuin = 0.5 * bh * hh * bw;
          const vol_cuft = vol_cuin / 1728;
          const vol_cuyd = vol_cuft / 27;
          setDisp('haunch_angle', fmt(angle_deg, 1) + '°');
          setDisp('diag_length', fmt(diag, 2) + ' in');
          setDisp('rebar_cut_len', fmt(cut_len, 1) + ' in (' + fmt(cut_len / 12, 2) + ' ft)');
          setDisp('shear_vc', fmt(phi_vc_enhanced, 1) + ' kips');
          setDisp('haunch_concrete_vol', fmt(vol_cuft, 2) + ' cu ft (' + fmt(vol_cuyd, 3) + ' yd³)');
        """
    },

    # 16. Analytical Evaluation Threshold (AET) Calculator (Position 80.5 in GSC!)
    {
        'slug': 'biotech/analytical-evaluation-threshold-aet',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Analytical Evaluation Threshold (AET) Calculator',
        'title': 'Analytical Evaluation Threshold (AET) Calculator: E&L Testing | OmniOperand',
        'description': 'Calculate the Analytical Evaluation Threshold (AET) for extractables and leachables testing based on PQRI guidelines and ISO 10993-18.',
        'hero_badge': 'Extractables & Leachables (E&L) • PQRI & ISO 10993-18',
        'hero_subtext': 'Calculate the Safety Concern Threshold (SCT) driven Analytical Evaluation Threshold (AET) for chemical characterization of medical devices and container closures.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'sct_val', 'label': 'Safety Concern Threshold (SCT)', 'type': 'number', 'default': 1.5, 'min': 0.05, 'max': 50, 'step': 0.05, 'unit': 'µg/day', 'hint': '1.5 µg/day (Parenteral), 0.15 µg/day (Inhalation / OINDP)'},
            {'id': 'max_daily_dose', 'label': 'Maximum Daily Dose (MDD)', 'type': 'number', 'default': 2, 'min': 0.1, 'max': 500, 'step': 0.1, 'unit': 'doses/day', 'hint': 'Number of drug doses administered per 24 hours'},
            {'id': 'extract_vol', 'label': 'Container / Extraction Volume', 'type': 'number', 'default': 10, 'min': 0.1, 'max': 5000, 'step': 0.5, 'unit': 'mL', 'hint': 'Volume of drug product or extraction solvent per unit'},
            {'id': 'components_count', 'label': 'Components Contacted per Dose', 'type': 'number', 'default': 1, 'min': 1, 'max': 20, 'step': 1, 'unit': 'units', 'hint': 'E.g. 1 vial + 1 stopper = 2 components'},
            {'id': 'uncert_factor', 'label': 'Analytical Uncertainty Factor (UF)', 'type': 'select', 'default': '1.5', 'options': [
                ['1.0', 'UF = 1.0 (No uncertainty • Authentic reference standard matched)'],
                ['1.5', 'UF = 1.5 (Standard GC-MS / LC-MS screening without response standards)'],
                ['2.0', 'UF = 2.0 (High uncertainty general screening)']
            ], 'hint': 'Accounts for detector response variation'}
        ],
        'outputs': [
            {'id': 'est_aet_container', 'label': 'Estimated AET per Container', 'unit': 'µg/container', 'color': 'var(--text-bright)'},
            {'id': 'final_aet_ug_ml', 'label': 'Final Reporting AET Threshold', 'unit': 'µg/mL (ppm)', 'color': 'var(--accent-cyan)'},
            {'id': 'final_aet_ppb', 'label': 'Final Reporting AET in ppb', 'unit': 'ng/mL (ppb)', 'color': 'var(--accent-emerald)'},
            {'id': 'threshold_class', 'label': 'AET Regulatory Category', 'unit': 'classification', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'AET_est = (SCT / MDD) · (Components / Volume) | Final AET = AET_est / UF',
        'proof_steps': [
            {'step_title': '1. Safety Concern Threshold (SCT) Invariant', 'step_text': 'PQRI and ISO 10993-18 establish the SCT as the threshold below which an extractable or leachable has negligible risk of carcinogenic or non-carcinogenic toxicity (standard 1.5 µg/day).'},
            {'step_title': '2. Dosage Normalization', 'step_text': 'Estimated AET = (SCT / MDD) × (N_components / V_extraction). A higher daily dose lowers the allowable concentration in each milliliter of solution.'},
            {'step_title': '3. Analytical Uncertainty Factor (UF)', 'step_text': 'Because unknown chemical compounds possess variable mass spec ionization efficiencies relative to the internal standard, the final analytical reporting threshold is divided by UF (typically 1.5): Final AET = AET_est / UF.'}
        ],
        'faqs': [
            {'q': 'What is the Analytical Evaluation Threshold (AET)?', 'a': 'The AET is the concentration threshold at or above which an analytical chemist must report, identify, and toxicologically evaluate an unknown extractable or leachable compound.'},
            {'q': 'What is the difference between SCT and AET?', 'a': 'The SCT is a toxicological threshold in absolute mass per day (e.g. 1.5 µg/day), while the AET is an analytical laboratory concentration (e.g. 0.05 µg/mL) derived from the SCT based on the patient dose and container volume.'},
            {'q': 'Why is an Uncertainty Factor (UF) used?', 'a': 'In non-targeted screening, unknown chemicals may have lower detector response factors than the surrogate internal standard. Dividing by UF = 1.5 ensures lower-responding toxic compounds are not missed.'}
        ],
        'js_logic': """
          const sct = getNum('sct_val') || 1.5;
          const mdd = getNum('max_daily_dose') || 2;
          const vol = getNum('extract_vol') || 10;
          const comps = getNum('components_count') || 1;
          const uf = parseFloat(document.getElementById('param-uncert_factor').value) || 1.5;
          const aet_per_dose = sct / mdd;
          const aet_per_container = aet_per_dose / comps;
          const est_aet_ug_ml = aet_per_container / vol;
          const final_aet_ug_ml = est_aet_ug_ml / uf;
          const final_aet_ppb = final_aet_ug_ml * 1000;
          let cat = 'Standard Parenteral Packaging';
          if (sct <= 0.2) cat = 'High-Risk OINDP / Inhalation Packaging';
          else if (final_aet_ppb < 50) cat = 'Ultra-Trace Level (< 50 ppb • High HRMS Sensitivity)';
          setDisp('est_aet_container', fmt(aet_per_container, 3) + ' µg');
          setDisp('final_aet_ug_ml', fmt(final_aet_ug_ml, 4) + ' µg/mL (ppm)');
          setDisp('final_aet_ppb', fmt(final_aet_ppb, 1) + ' ng/mL (ppb)');
          setDisp('threshold_class', cat);
        """
    },

    # 17. Relative Potency Bioassay Calculator (Position 83.3 in GSC!)
    {
        'slug': 'biotech/relative-potency-bioassay',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Relative Potency Bioassay Calculator',
        'title': 'Relative Potency Bioassay Calculator: PLA & 4PL Parallelism | OmniOperand',
        'description': 'Calculate relative potency (RP) and Fieller 95% confidence intervals for parallel-line and 4-parameter logistic bioassays under USP <1032>/<1034>.',
        'hero_badge': 'Biopharmaceutical Bioassays • USP <1032>/<1034> & Ph. Eur. 5.3',
        'hero_subtext': 'Calculate biopharmaceutical relative potency (RP), 4PL parallelism ratio, log potency delta (M), and 95% Fieller confidence intervals.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'std_ec50', 'label': 'Reference Standard EC50 / IC50', 'type': 'number', 'default': 25.0, 'min': 0.001, 'max': 100000, 'step': 0.5, 'unit': 'ng/mL', 'hint': 'Midpoint potency of qualified reference standard'},
            {'id': 'test_ec50', 'label': 'Test Article Sample EC50 / IC50', 'type': 'number', 'default': 26.5, 'min': 0.001, 'max': 100000, 'step': 0.5, 'unit': 'ng/mL', 'hint': 'Midpoint potency of test sample'},
            {'id': 'std_slope', 'label': 'Reference Standard Hill Slope (β_std)', 'type': 'number', 'default': 1.15, 'min': 0.2, 'max': 5.0, 'step': 0.05, 'unit': 'slope', 'hint': '4PL concentration-response Hill slope'},
            {'id': 'test_slope', 'label': 'Test Article Hill Slope (β_test)', 'type': 'number', 'default': 1.18, 'min': 0.2, 'max': 5.0, 'step': 0.05, 'unit': 'slope', 'hint': 'Sample 4PL concentration-response Hill slope'},
            {'id': 'assay_cv_pct', 'label': 'Bioassay Intermediate Precision (%CV)', 'type': 'number', 'default': 6.5, 'min': 1.0, 'max': 30.0, 'step': 0.5, 'unit': '%', 'hint': 'Residual standard error variance'}
        ],
        'outputs': [
            {'id': 'rel_potency_pct', 'label': 'Calculated Relative Potency (RP)', 'unit': '% of Reference', 'color': 'var(--accent-cyan)'},
            {'id': 'log_potency_m', 'label': 'Log Potency Difference (M)', 'unit': 'log10 scale', 'color': 'var(--text-bright)'},
            {'id': 'parallelism_ratio', 'label': 'Slope Ratio Parallelism Check', 'unit': 'ratio', 'color': 'var(--accent-emerald)'},
            {'id': 'fieller_ci', 'label': '95% Fieller Confidence Interval', 'unit': '% RP Range', 'color': 'var(--accent-purple)'},
            {'id': 'bioassay_status', 'label': 'USP <1032> Suitability Status', 'unit': 'status', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Relative Potency = (EC50_std / EC50_test) · 100% | M = log10(EC50_std) - log10(EC50_test) | Parallelism = β_test / β_std',
        'proof_steps': [
            {'step_title': '1. Relative Potency Formulation', 'step_text': 'In parallel-line bioassay models (USP <1032>), the test article is assumed to act as a dilution of the reference standard: Relative Potency = (EC50_reference / EC50_test) × 100%.'},
            {'step_title': '2. Parallelism Fundamental Invariant', 'step_text': 'For relative potency to be valid, the two dose-response curves must be parallel (same mechanism of action). The slope ratio β_test / β_std must lie within the equivalence margin [0.80, 1.25].'},
            {'step_title': '3. Fieller\'s Theorem Confidence Limits', 'step_text': 'Because relative potency is a ratio of two normally distributed random variables, standard linear error propagation fails. Fieller\'s theorem provides the mathematically exact asymmetric 95% confidence bounds.'}
        ],
        'faqs': [
            {'q': 'Why is relative potency calculated as standard / test?', 'a': 'If a test sample requires a lower EC50 to achieve the same 50% biological effect as the standard, it is more potent. Thus, dividing standard EC50 by test EC50 correctly produces a relative potency > 100%.'},
            {'q': 'What is the USP requirement for bioassay parallelism?', 'a': 'USP <1032> requires that the dose-response curves of test and reference articles have identical upper asymptotes, lower asymptotes, and slope (slope ratio between 0.80 and 1.25).'},
            {'q': 'What is Fieller\'s theorem?', 'a': 'Fieller\'s theorem is a statistical formula for calculating confidence limits on the ratio of two parameter estimates, preventing distortion caused by dividing two random variables.'}
        ],
        'js_logic': """
          const std = getNum('std_ec50') || 25.0;
          const test = getNum('test_ec50') || 26.5;
          const s_slope = getNum('std_slope') || 1.15;
          const t_slope = getNum('test_slope') || 1.18;
          const cv = (getNum('assay_cv_pct') || 6.5) / 100;
          const rp = (std / test) * 100;
          const m = Math.log10(std) - Math.log10(test);
          const slope_ratio = t_slope / s_slope;
          const is_parallel = (slope_ratio >= 0.80 && slope_ratio <= 1.25);
          const z = 1.96;
          const se_log = (cv / Math.LN10) * Math.sqrt(2);
          const ci_low = rp * Math.pow(10, -z * se_log);
          const ci_high = rp * Math.pow(10, z * se_log);
          let status = '✅ Validated Parallel Bioassay (USP <1032> Compliant)';
          if (!is_parallel) status = '⚠️ Non-Parallel Slopes (Ratio Outside 0.80–1.25)';
          else if (rp < 80 || rp > 125) status = 'Out of Typical Commercial Specification (80–125%)';
          setDisp('rel_potency_pct', fmt(rp, 1) + '%');
          setDisp('log_potency_m', fmt(m, 4));
          setDisp('parallelism_ratio', fmt(slope_ratio, 3) + (is_parallel ? ' ✅ (Pass)' : ' ❌ (Fail)'));
          setDisp('fieller_ci', fmt(ci_low, 1) + '% – ' + fmt(ci_high, 1) + '%');
          setDisp('bioassay_status', status);
        """
    },

    # 18. HPLC Column Theoretical Plates & Resolution Calculator (Position 86.0 in GSC!)
    {
        'slug': 'biotech/chromatography-resolution',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'HPLC Column Theoretical Plates & Resolution Calculator',
        'title': 'HPLC Theoretical Plates & Resolution Calculator | OmniOperand',
        'description': 'Calculate USP theoretical plate count (N), chromatographic resolution (Rs), peak asymmetry, and height equivalent to theoretical plate (HETP).',
        'hero_badge': 'Chromatography & Quality Control • USP <621> / EP 2.2.46',
        'hero_subtext': 'Calculate USP theoretical plate count (N), chromatographic peak resolution (Rs), plate height (HETP), and retention factors under USP <621> standards.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'ret_time_1', 'label': 'Peak 1 Retention Time (t_r1)', 'type': 'number', 'default': 5.20, 'min': 0.1, 'max': 300, 'step': 0.05, 'unit': 'min', 'hint': 'Retention time of earlier-eluting peak'},
            {'id': 'ret_time_2', 'label': 'Peak 2 Retention Time (t_r2)', 'type': 'number', 'default': 5.85, 'min': 0.1, 'max': 300, 'step': 0.05, 'unit': 'min', 'hint': 'Retention time of later-eluting peak'},
            {'id': 'half_width_2', 'label': 'Peak 2 Half-Height Width (W_0.5)', 'type': 'number', 'default': 0.12, 'min': 0.005, 'max': 10, 'step': 0.005, 'unit': 'min', 'hint': 'Peak width measured at 50% peak height'},
            {'id': 'half_width_1', 'label': 'Peak 1 Half-Height Width (W_0.5)', 'type': 'number', 'default': 0.11, 'min': 0.005, 'max': 10, 'step': 0.005, 'unit': 'min', 'hint': 'Width of peak 1 at 50% peak height'},
            {'id': 'column_len_mm', 'label': 'HPLC Column Length (L)', 'type': 'number', 'default': 150, 'min': 10, 'max': 500, 'step': 10, 'unit': 'mm', 'hint': '150 mm standard C18 column'},
            {'id': 'void_time_t0', 'label': 'Void / Dead Time (t_0)', 'type': 'number', 'default': 1.10, 'min': 0.05, 'max': 20, 'step': 0.05, 'unit': 'min', 'hint': 'Unretained marker elution time (uracil / solvent front)'}
        ],
        'outputs': [
            {'id': 'usp_plates_n', 'label': 'USP Theoretical Plate Count (N)', 'unit': 'plates', 'color': 'var(--accent-cyan)'},
            {'id': 'usp_resolution_rs', 'label': 'Chromatographic Resolution (Rs)', 'unit': 'Rs', 'color': 'var(--accent-emerald)'},
            {'id': 'hetp_um', 'label': 'Plate Height (HETP)', 'unit': 'µm/plate', 'color': 'var(--text-bright)'},
            {'id': 'ret_factor_k', 'label': 'Peak 2 Capacity Factor (k\')', 'unit': 'k\'', 'color': 'var(--text-bright)'},
            {'id': 'separation_factor', 'label': 'Selectivity Factor (α)', 'unit': 'alpha', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'N = 5.545 · (t_r / W_0.5)² | R_s = 1.18 · (t_r2 - t_r1) / (W_0.5,1 + W_0.5,2) | HETP = (L · 1000) / N',
        'proof_steps': [
            {'step_title': '1. USP Theoretical Plate Count (N)', 'step_text': 'Under USP <621> and Ph. Eur. 2.2.46, column efficiency is calculated from peak width at half-height (W_0.5): N = 5.545 × (t_r / W_0.5)². This eliminates baseline noise ambiguity.'},
            {'step_title': '2. Chromatographic Resolution (Rs)', 'step_text': 'Resolution quantifies separation between adjacent peaks: R_s = 1.18 × (t_r2 - t_r1) / (W_0.5,1 + W_0.5,2). Complete baseline separation requires R_s ≥ 1.50.'},
            {'step_title': '3. Van Deemter Plate Height (HETP)', 'step_text': 'Height Equivalent to a Theoretical Plate measures packaging efficiency: HETP = Length / N. For sub-3µm particle columns, HETP is typically 10 to 20 µm.'}
        ],
        'faqs': [
            {'q': 'What is a good theoretical plate count for an HPLC column?', 'a': 'A standard 150 mm C18 column with 5 µm particles should generate 10,000 to 14,000 plates. Modern UHPLC columns (1.7–2.7 µm particles) achieve 25,000 to 40,000+ plates.'},
            {'q': 'What is the minimum acceptable resolution (Rs) in pharmaceutical QC?', 'a': 'USP <621> requires a minimum resolution of Rs ≥ 1.50 for baseline baseline separation between critical pairs (API and adjacent process impurities).'},
            {'q': 'What is HETP?', 'a': 'HETP (Height Equivalent to a Theoretical Plate) is column length divided by plate count. Smaller HETP values indicate higher chromatographic separation efficiency.'}
        ],
        'js_logic': """
          const tr1 = getNum('ret_time_1') || 5.20;
          const tr2 = getNum('ret_time_2') || 5.85;
          const w2 = getNum('half_width_2') || 0.12;
          const w1 = getNum('half_width_1') || 0.11;
          const col_mm = getNum('column_len_mm') || 150;
          const t0 = getNum('void_time_t0') || 1.10;
          const n = 5.545 * Math.pow(tr2 / w2, 2);
          const rs = (1.18 * Math.abs(tr2 - tr1)) / (w1 + w2);
          const hetp = (col_mm * 1000) / n;
          const k2 = (tr2 - t0) / t0;
          const k1 = (tr1 - t0) / t0;
          const alpha = (k1 > 0) ? (k2 / k1) : 1.0;
          const rs_label = fmt(rs, 2) + (rs >= 1.5 ? ' ✅ (Baseline Resolved ≥ 1.5)' : ' ⚠️ (< 1.5 Incomplete Separation)');
          setDisp('usp_plates_n', fmt(Math.round(n), 0) + ' plates');
          setDisp('usp_resolution_rs', rs_label);
          setDisp('hetp_um', fmt(hetp, 1) + ' µm');
          setDisp('ret_factor_k', fmt(k2, 2));
          setDisp('separation_factor', fmt(alpha, 2));
        """
    },

    # 19. Syringe Pump & Microfluidic Flow Rate Calculator (Position 90.0 in GSC!)
    {
        'slug': 'biotech/syringe-pump-injection-rate',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Syringe Pump & Microfluidic Flow Rate Calculator',
        'title': 'Syringe Pump Flow Rate Calculator: Inner Diameter & Pusher Speed | OmniOperand',
        'description': 'Calculate volumetric flow rate, linear stepper motor pusher speed (mm/min), and total delivery duration for laboratory syringe pumps and microfluidics.',
        'hero_badge': 'Laboratory Automation & Microfluidics • ISO 7886 Standard',
        'hero_subtext': 'Calculate linear pusher velocity (mm/min), cross-sectional plunger area, and delivery duration for laboratory syringe pumps and microfluidic chips.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'syringe_model', 'label': 'Syringe Brand & Volume', 'type': 'select', 'default': 'bd_10', 'options': [
                ['bd_1', 'BD Plastic 1 mL (ID = 4.70 mm)'],
                ['bd_5', 'BD Plastic 5 mL (ID = 11.99 mm)'],
                ['bd_10', 'BD Plastic 10 mL (ID = 14.48 mm • Standard)'],
                ['bd_20', 'BD Plastic 20 mL (ID = 19.05 mm)'],
                ['bd_50', 'BD Plastic 50/60 mL (ID = 26.70 mm)'],
                ['ham_100u', 'Hamilton Gastight 100 µL (ID = 1.46 mm)'],
                ['ham_1m', 'Hamilton Gastight 1 mL (ID = 4.61 mm)']
            ], 'hint': 'Pre-programmed inner barrel diameter'},
            {'id': 'target_flow', 'label': 'Target Volumetric Flow Rate', 'type': 'number', 'default': 25, 'min': 0.001, 'max': 50000, 'step': 1, 'unit': 'rate', 'hint': 'Desired infusion rate'},
            {'id': 'flow_unit', 'label': 'Flow Rate Unit', 'type': 'select', 'default': 'uL_min', 'options': [
                ['uL_min', 'Microliters per minute (µL/min)'],
                ['mL_hr', 'Milliliters per hour (mL/hr)'],
                ['uL_hr', 'Microliters per hour (µL/hr)'],
                ['nL_min', 'Nanoliters per minute (nL/min)'],
                ['mL_min', 'Milliliters per minute (mL/min)']
            ], 'hint': 'Standard pump display unit'},
            {'id': 'dispense_vol', 'label': 'Total Target Dispense Volume', 'type': 'number', 'default': 5.0, 'min': 0.01, 'max': 100, 'step': 0.5, 'unit': 'mL', 'hint': 'Volume to infuse into chip/animal'}
        ],
        'outputs': [
            {'id': 'pusher_speed_mm_min', 'label': 'Linear Pusher Speed', 'unit': 'mm/min', 'color': 'var(--accent-cyan)'},
            {'id': 'pusher_speed_um_s', 'label': 'Linear Stepper Velocity', 'unit': 'µm/s', 'color': 'var(--text-bright)'},
            {'id': 'cross_area_mm2', 'label': 'Syringe Inner Cross-Sectional Area', 'unit': 'mm²', 'color': 'var(--text-bright)'},
            {'id': 'infusion_duration', 'label': 'Total Infusion Run Time', 'unit': 'time', 'color': 'var(--accent-emerald)'},
            {'id': 'barrel_id_disp', 'label': 'Inner Barrel Diameter Used', 'unit': 'mm', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'Area A = π · (D / 2)² | Pusher Velocity v = Flow Rate Q / Area A | Duration = Volume / Q',
        'proof_steps': [
            {'step_title': '1. Plunger Cross-Sectional Area', 'step_text': 'The inner barrel diameter D determines cylinder area: A = π × (D/2)². For a 10 mL BD syringe (D = 14.48 mm), area A = 164.68 mm².'},
            {'step_title': '2. Flow Rate to Linear Speed Conversion', 'step_text': 'Syringe pump leadscrews drive the plunger linearly. 1 µL equals 1 mm³ of volume. Linear pusher velocity is v (mm/min) = Q (mm³/min) / Area (mm²).'},
            {'step_title': '3. Infusion Time Invariant', 'step_text': 'Total infusion duration is simply Volume / Flow Rate. For microfluidic droplet generation or microdialysis, matching linear speed to microchannel velocity prevents cell shear stress.'}
        ],
        'faqs': [
            {'q': 'Why does a smaller syringe give smoother microfluidic flow?', 'a': 'A smaller syringe diameter has a much smaller cross-sectional area, meaning the motor leadscrew must turn much faster to deliver the same volume, eliminating discrete motor stepping pulsations.'},
            {'q': 'Where do you find syringe inner barrel diameters?', 'a': 'Inner barrel diameters are published by manufacturers (BD, Hamilton, Terumo) and ISO 7886 standards, ranging from 1.46 mm for 100µL syringes up to 26.7 mm for 60mL syringes.'},
            {'q': 'How do you convert µL/min to mL/hr?', 'a': 'Multiply µL/min by 60 to find µL/hr, then divide by 1,000 to find mL/hr (Formula: mL/hr = µL/min × 0.06).' }
        ],
        'js_logic': """
          const model = document.getElementById('param-syringe_model').value;
          const rate = getNum('target_flow') || 25;
          const unit = document.getElementById('param-flow_unit').value;
          const target_v = getNum('dispense_vol') || 5.0;
          let d_mm = 14.48; // default bd_10
          if (model === 'bd_1') d_mm = 4.70;
          else if (model === 'bd_5') d_mm = 11.99;
          else if (model === 'bd_20') d_mm = 19.05;
          else if (model === 'bd_50') d_mm = 26.70;
          else if (model === 'ham_100u') d_mm = 1.46;
          else if (model === 'ham_1m') d_mm = 4.61;
          const area_mm2 = (Math.PI / 4) * (d_mm * d_mm);
          let q_mm3_per_min = rate;
          let q_ml_per_min = rate / 1000;
          if (unit === 'uL_min') {
            q_mm3_per_min = rate;
            q_ml_per_min = rate / 1000;
          } else if (unit === 'mL_hr') {
            q_mm3_per_min = (rate * 1000) / 60;
            q_ml_per_min = rate / 60;
          } else if (unit === 'uL_hr') {
            q_mm3_per_min = rate / 60;
            q_ml_per_min = rate / 60000;
          } else if (unit === 'nL_min') {
            q_mm3_per_min = rate / 1000;
            q_ml_per_min = rate / 1000000;
          } else if (unit === 'mL_min') {
            q_mm3_per_min = rate * 1000;
            q_ml_per_min = rate;
          }
          const v_mm_min = q_mm3_per_min / area_mm2;
          const v_um_s = (v_mm_min * 1000) / 60;
          const duration_mins = (q_ml_per_min > 0) ? (target_v / q_ml_per_min) : 0;
          const dur_hours = Math.floor(duration_mins / 60);
          const dur_rem_mins = Math.round(duration_mins % 60);
          setDisp('pusher_speed_mm_min', fmt(v_mm_min, 4) + ' mm/min');
          setDisp('pusher_speed_um_s', fmt(v_um_s, 2) + ' µm/s');
          setDisp('cross_area_mm2', fmt(area_mm2, 2) + ' mm²');
          setDisp('infusion_duration', dur_hours + ' hr ' + dur_rem_mins + ' min (' + fmt(duration_mins, 1) + ' mins total)');
          setDisp('barrel_id_disp', fmt(d_mm, 2) + ' mm');
        """
    },

    # 20. ASC 842 / IFRS 16 Incremental Borrowing Rate (IBR) Calculator (Position 90.0 in GSC!)
    {
        'slug': 'finance/incremental-borrowing-rate-lease',
        'category': 'finance',
        'cluster': 'finance',
        'name': 'ASC 842 / IFRS 16 Incremental Borrowing Rate (IBR) Calculator',
        'title': 'Incremental Borrowing Rate (IBR) Calculator: ASC 842 & IFRS 16 | OmniOperand',
        'description': 'Calculate corporate lease incremental borrowing rates (IBR), synthetic credit rating spreads, and right-of-use (ROU) asset present value schedules.',
        'hero_badge': 'Lease Accounting Standards • GAAP ASC 842 & IFRS 16',
        'hero_subtext': 'Model synthetic Incremental Borrowing Rates (IBR) for lease liabilities and compute Right-of-Use (ROU) asset present values under ASC 842 / IFRS 16.',
        'has_dual_units': False,
        'governing_jurisdiction': 'Governed by US GAAP ASC 842 and IFRS 16 Leases',
        'inputs': [
            {'id': 'risk_free_rate', 'label': 'Reference Risk-Free Rate (SOFR/Treasury)', 'type': 'number', 'default': 4.25, 'min': 0.1, 'max': 15, 'step': 0.05, 'unit': '%', 'hint': 'Yield of benchmark government bond matching lease tenure'},
            {'id': 'credit_tier', 'label': 'Entity Credit Rating Spread', 'type': 'select', 'default': 'bbb', 'options': [
                ['aaa', 'AAA / AA (Prime • +0.75% Credit Spread)'],
                ['a', 'A-Rated (High Grade • +1.20% Credit Spread)'],
                ['bbb', 'BBB / Investment Grade (+1.85% Credit Spread)'],
                ['bb', 'BB / High Yield (+3.10% Credit Spread)'],
                ['b', 'B / Speculative (+4.75% Credit Spread)'],
                ['unrated', 'Unrated Private Enterprise (+3.50% Typical Bank Spread)']
            ], 'hint': 'Entity stand-alone credit profile'},
            {'id': 'collateral_adj', 'label': 'Asset Collateralization Adjustment', 'type': 'select', 'default': 're', 'options': [
                ['re', 'Real Estate / Prime Property (-0.40% Secured Discount)'],
                ['fleet', 'Vehicles & Heavy Equipment (-0.25% Secured Discount)'],
                ['it', 'IT & Specialized Assets (+0.30% Illiquid Penalty)'],
                ['unsecured', 'Unsecured / General (+0.00% Baseline)']
            ], 'hint': 'Collateral nature adjusts lender loss given default'},
            {'id': 'lease_term_years', 'label': 'Lease Term Duration', 'type': 'number', 'default': 5, 'min': 1, 'max': 50, 'step': 1, 'unit': 'years', 'hint': 'Contractual non-cancellable lease term'},
            {'id': 'monthly_rent', 'label': 'Monthly Lease Payment', 'type': 'number', 'default': 12500, 'min': 100, 'max': 5000000, 'step': 250, 'unit': '$/month', 'hint': 'Fixed periodic lease payment'}
        ],
        'outputs': [
            {'id': 'calc_ibr_pct', 'label': 'Derived Incremental Borrowing Rate (IBR)', 'unit': '% APR', 'color': 'var(--accent-cyan)'},
            {'id': 'rou_asset_pv', 'label': 'Present Value of Lease Liability (ROU Asset)', 'unit': '$ USD', 'color': 'var(--accent-emerald)'},
            {'id': 'total_undiscounted', 'label': 'Total Undiscounted Cash Payments', 'unit': '$ USD', 'color': 'var(--text-bright)'},
            {'id': 'total_interest_exp', 'label': 'Total Financing Interest Expense', 'unit': '$ USD', 'color': 'var(--accent-purple)'},
            {'id': 'yr1_amortization', 'label': 'Year 1 ROU Asset Amortization', 'unit': '$/year', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'IBR = R_free + Spread + CollateralAdj | PV = Σ [ Rent_t / (1 + IBR/12)ᵗ ]',
        'proof_steps': [
            {'step_title': '1. ASC 842 & IFRS 16 IBR Definition', 'step_text': 'The Incremental Borrowing Rate is the rate of interest that a lessee would have to pay to borrow on a collateralized basis over a similar term an amount equal to the lease payments in a similar economic environment.'},
            {'step_title': '2. Synthetic Build-Up Method', 'step_text': 'Auditors and Big 4 accounting firms require a 4-component synthetic derivation: IBR = Risk-Free Reference Rate + Financing Entity Credit Spread + Asset Collateral Adjustment + Term/Currency Adjustment.'},
            {'step_title': '3. Right-of-Use (ROU) Asset Balance Sheet Capitalization', 'step_text': 'Lease payments discounted at the derived IBR create the initial lease liability recognized on the corporate balance sheet. Undiscounted payments minus present value equals total financing interest.'}
        ],
        'faqs': [
            {'q': 'What is the Incremental Borrowing Rate under ASC 842?', 'a': 'Under US GAAP ASC 842, if the rate implicit in the lease cannot be readily determined (which is true for >95% of real estate and equipment leases), the lessee must use its Incremental Borrowing Rate to discount lease payments onto the balance sheet.'},
            {'q': 'Can a private company use the risk-free rate for ASC 842?', 'a': 'Yes. FASB allows private entities an accounting policy election to use the risk-free rate (US Treasury rate) by asset class, but doing so lowers the discount rate, which significantly inflates reported balance sheet lease liabilities.'},
            {'q': 'How does collateral affect the IBR?', 'a': 'Because the lease is collateralized by the leased asset itself, secure assets (like commercial real estate or standard vehicles) reduce credit risk and lower the IBR by 25 to 50 basis points relative to unsecured corporate bonds.'}
        ],
        'js_logic': """
          const r_free = getNum('risk_free_rate') || 4.25;
          const tier = document.getElementById('param-credit_tier').value;
          const col = document.getElementById('param-collateral_adj').value;
          const yrs = getNum('lease_term_years') || 5;
          const rent = getNum('monthly_rent') || 12500;
          let spread = 1.85;
          if (tier === 'aaa') spread = 0.75;
          else if (tier === 'a') spread = 1.20;
          else if (tier === 'bb') spread = 3.10;
          else if (tier === 'b') spread = 4.75;
          else if (tier === 'unrated') spread = 3.50;
          let col_adj = -0.40;
          if (col === 'fleet') col_adj = -0.25;
          else if (col === 'it') col_adj = 0.30;
          else if (col === 'unsecured') col_adj = 0.00;
          const final_ibr = Math.max(0.5, r_free + spread + col_adj);
          const n = yrs * 12;
          const r_monthly = (final_ibr / 100) / 12;
          let pv = 0;
          for (let t = 1; t <= n; t++) {
            pv += rent / Math.pow(1 + r_monthly, t);
          }
          const total_cash = rent * n;
          const total_interest = total_cash - pv;
          const yr1_deprec = pv / yrs;
          setDisp('calc_ibr_pct', fmt(final_ibr, 2) + '%');
          setDisp('rou_asset_pv', '$' + fmt(pv, 0));
          setDisp('total_undiscounted', '$' + fmt(total_cash, 0));
          setDisp('total_interest_exp', '$' + fmt(total_interest, 0));
          setDisp('yr1_amortization', '$' + fmt(yr1_deprec, 0) + ' / yr');
        """
    },

    # 21. Circumferential & Surface Cutting Speed Calculator (Position 95.0 in GSC!)
    {
        'slug': 'physics/circumferential-surface-speed',
        'category': 'physics',
        'cluster': 'physics',
        'name': 'Circumferential & Surface Cutting Speed Calculator',
        'title': 'Circumferential Speed Calculator: SFM & RPM Surface Velocity | OmniOperand',
        'description': 'Calculate tangential surface speed in SFM (ft/min) and m/min from RPM and tool/wheel diameter. Essential for machining, milling, and grinding.',
        'hero_badge': 'Machining & Kinematics • ISO 3002 Cutting Tool Standard',
        'hero_subtext': 'Calculate tangential surface cutting speed (SFM & m/min), peripheral linear velocity, and centrifugal rim acceleration from spindle RPM and diameter.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'spindle_rpm', 'label': 'Rotational Spindle Speed (N)', 'type': 'number', 'default': 2500, 'min': 1, 'max': 100000, 'step': 50, 'unit': 'RPM', 'hint': 'Revolutions per minute of spindle or wheel'},
            {'id': 'tool_dia', 'label': 'Tool / Part Outer Diameter (D)', 'type': 'number', 'default': 3.0, 'min': 0.01, 'max': 500, 'step': 0.125, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Diameter of rotating workpiece or milling cutter'}
        ],
        'outputs': [
            {'id': 'surface_sfm', 'label': 'Surface Speed in SFM', 'unit': 'ft/min (SFM)', 'color': 'var(--accent-cyan)'},
            {'id': 'surface_m_min', 'label': 'Metric Cutting Speed (vc)', 'unit': 'm/min', 'color': 'var(--accent-emerald)'},
            {'id': 'linear_speed_mph', 'label': 'Rim Tangential Speed', 'unit': 'mph (m/s)', 'color': 'var(--text-bright)'},
            {'id': 'centrifugal_g', 'label': 'Centrifugal Rim Acceleration', 'unit': 'g-force (g)', 'color': 'var(--accent-purple)'},
            {'id': 'angular_vel', 'label': 'Angular Velocity (ω)', 'unit': 'rad/sec', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'SFM = (π · D_in · RPM) / 12 ≈ (D_in · RPM) / 3.82 | Metric vc = (π · D_mm · RPM) / 1000 | g = (ω² · r) / 9.80665',
        'proof_steps': [
            {'step_title': '1. Circumferential Velocity Invariant', 'step_text': 'Each rotation sweeps through perimeter distance π × D. In inches per minute, speed is π × D × RPM. Dividing by 12 converts to Surface Feet per Minute: SFM = (π × D × RPM) / 12 ≈ (D × RPM) / 3.8197.'},
            {'step_title': '2. Metric Cutting Speed (vc)', 'step_text': 'In metric ISO 3002 conventions with diameter in millimeters: vc (m/min) = (π × D_mm × RPM) / 1,000.'},
            {'step_title': '3. Centrifugal Rim G-Force', 'step_text': 'With angular velocity ω = (2π × RPM) / 60 rad/s, the centrifugal acceleration experienced at the outer rim is a_c = ω² × r. Dividing by standard gravity g = 9.80665 m/s² yields relative g-force.'}
        ],
        'faqs': [
            {'q': 'What is SFM in machining?', 'a': 'SFM stands for Surface Feet per Minute. It is the cutting speed at which the outer edge of a tool passes over the workpiece material, determining tool life and heat generation.'},
            {'q': 'How do you calculate RPM from SFM?', 'a': 'Use the standard machinist rule-of-thumb: RPM = (SFM × 3.82) / Diameter. For example, machining aluminum at 600 SFM with a 0.5-inch end mill requires (600 × 3.82) / 0.5 = 4,584 RPM.'},
            {'q': 'Why is circumferential speed critical for grinding wheels?', 'a': 'Grinding wheels have strict maximum peripheral surface speeds (typically 6,000 to 8,500 SFM). Exceeding this limit generates destructive centrifugal stresses that can cause wheel explosion.'}
        ],
        'js_logic': """
          const rpm = getNum('spindle_rpm') || 2500;
          const d_in = getNum('tool_dia') || 3.0;
          const sfm = (Math.PI * d_in * rpm) / 12;
          const d_mm = d_in * 25.4;
          const vc_m_min = (Math.PI * d_mm * rpm) / 1000;
          const v_ms = vc_m_min / 60;
          const v_mph = v_ms * 2.23694;
          const omega = (2 * Math.PI * rpm) / 60;
          const r_m = (d_mm / 2) / 1000;
          const a_c = omega * omega * r_m;
          const g_force = a_c / 9.80665;
          setDisp('surface_sfm', fmt(sfm, 0) + ' SFM');
          setDisp('surface_m_min', fmt(vc_m_min, 1) + ' m/min');
          setDisp('linear_speed_mph', fmt(v_mph, 1) + ' mph (' + fmt(v_ms, 1) + ' m/s)');
          setDisp('centrifugal_g', fmt(g_force, 0) + ' g');
          setDisp('angular_vel', fmt(omega, 1) + ' rad/s');
        """
    },

    # 22. Hydraulic Cylinder Force & Fluid Flow Calculator (Position 100.0 in GSC!)
    {
        'slug': 'engineering/hydraulic-cylinder-flow',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Hydraulic Cylinder Force & Fluid Flow Calculator',
        'title': 'Hydraulic Cylinder Force & Speed Calculator: Bore, Rod & GPM | OmniOperand',
        'description': 'Calculate hydraulic cylinder extension and retraction force (lbs/kN), stroke velocity, cycle time, pump flow rate (GPM), and required horsepower.',
        'hero_badge': 'Fluid Power & Mobile Hydraulics • ISO 3320 / NFPA Invariants',
        'hero_subtext': 'Calculate hydraulic piston extend/retract forces, cylinder stroke velocity, cycle duration, and required pump input horsepower.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'bore_dia', 'label': 'Cylinder Bore Diameter (D)', 'type': 'number', 'default': 4.0, 'min': 0.5, 'max': 40, 'step': 0.25, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Internal diameter of hydraulic barrel'},
            {'id': 'rod_dia', 'label': 'Piston Rod Diameter (d)', 'type': 'number', 'default': 2.0, 'min': 0.25, 'max': 35, 'step': 0.125, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Diameter of extending steel rod'},
            {'id': 'pressure_psi', 'label': 'Operating Hydraulic Pressure (P)', 'type': 'number', 'default': 3000, 'min': 100, 'max': 10000, 'step': 100, 'unit': 'PSI', 'metric_unit': 'Bar', 'hint': 'System relief or pump operating pressure'},
            {'id': 'flow_gpm', 'label': 'Pump Flow Rate (Q)', 'type': 'number', 'default': 10, 'min': 0.1, 'max': 250, 'step': 0.5, 'unit': 'GPM', 'metric_unit': 'L/min', 'hint': 'Hydraulic pump delivery rate'},
            {'id': 'stroke_len', 'label': 'Cylinder Stroke Length (S)', 'type': 'number', 'default': 24, 'min': 1, 'max': 240, 'step': 1, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Full travel distance'}
        ],
        'outputs': [
            {'id': 'push_force_lbs', 'label': 'Extension (Push) Force', 'unit': 'lbs (Tons / kN)', 'color': 'var(--accent-cyan)'},
            {'id': 'pull_force_lbs', 'label': 'Retraction (Pull) Force', 'unit': 'lbs (Tons / kN)', 'color': 'var(--accent-emerald)'},
            {'id': 'extend_speed', 'label': 'Extend Stroke Velocity', 'unit': 'in/sec', 'color': 'var(--text-bright)'},
            {'id': 'retract_speed', 'label': 'Retract Stroke Velocity', 'unit': 'in/sec', 'color': 'var(--text-bright)'},
            {'id': 'extend_time_sec', 'label': 'Full Extension Cycle Time', 'unit': 'seconds', 'color': 'var(--accent-purple)'},
            {'id': 'hydraulic_hp', 'label': 'Hydraulic Fluid Horsepower', 'unit': 'HP', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Push F = P · (π·D²/4) | Pull F = P · [π·(D² - d²)/4] | Speed = (0.3208 · Q) / Area | HP = (P · Q) / 1714',
        'proof_steps': [
            {'step_title': '1. Differential Area Invariant', 'step_text': 'Hydraulic force equals pressure multiplied by effective area: F = P × A. On extension, fluid acts against full bore area A_cap = π · D² / 4. On retraction, the steel rod occupies space: annular area is A_ann = π · (D² - d²) / 4.'},
            {'step_title': '2. Speed & Flow Velocity Relation', 'step_text': '1 GPM equals 231 cubic inches per minute = 3.85 in³/sec. Cylinder linear velocity is Speed (in/sec) = (Q × 231) / (A × 60) = 3.85 × Q / A.'},
            {'step_title': '3. Hydraulic Horsepower Invariant', 'step_text': 'Work done by hydraulic fluid is HP = (Pressure in PSI × Flow in GPM) / 1,714.'}
        ],
        'faqs': [
            {'q': 'Why does a hydraulic cylinder retract faster than it extends?', 'a': 'Because the rod takes up volume in the rod-end chamber, the annular area is smaller. For a constant pump flow rate (GPM), smaller volume fills faster, causing the cylinder to retract faster (with proportionally less pull force).'},
            {'q': 'How do you calculate tons of force from a hydraulic cylinder?', 'a': 'Calculate push force in pounds: Force = Pressure (PSI) × (π × Bore² / 4), then divide by 2,000 lbs to find US tons. A 4" cylinder at 3,000 PSI delivers (3000 × 12.57) / 2000 = 18.85 Tons.'},
            {'q': 'What does 1714 mean in hydraulic horsepower?', 'a': '1714 is the conversion constant deriving from 1 HP = 33,000 ft-lb/min and 1 gallon = 231 cu in: (33,000 × 12) / 231 = 1,714.28.'}
        ],
        'js_logic': """
          const d_bore = getNum('bore_dia') || 4.0;
          const d_rod = getNum('rod_dia') || 2.0;
          const psi = getNum('pressure_psi') || 3000;
          const gpm = getNum('flow_gpm') || 10;
          const stroke = getNum('stroke_len') || 24;
          const a_bore = (Math.PI / 4) * (d_bore * d_bore);
          const a_rod = (Math.PI / 4) * (d_rod * d_rod);
          const a_annular = Math.max(0.01, a_bore - a_rod);
          const f_push = psi * a_bore;
          const f_pull = psi * a_annular;
          const tons_push = f_push / 2000;
          const tons_pull = f_pull / 2000;
          const kn_push = f_push * 0.00444822;
          const v_ext_ips = (gpm * 231) / (a_bore * 60);
          const v_ret_ips = (gpm * 231) / (a_annular * 60);
          const t_ext = stroke / v_ext_ips;
          const t_ret = stroke / v_ret_ips;
          const hp = (psi * gpm) / 1714;
          setDisp('push_force_lbs', fmt(f_push, 0) + ' lbs (' + fmt(tons_push, 1) + ' Tons / ' + fmt(kn_push, 1) + ' kN)');
          setDisp('pull_force_lbs', fmt(f_pull, 0) + ' lbs (' + fmt(tons_pull, 1) + ' Tons)');
          setDisp('extend_speed', fmt(v_ext_ips, 2) + ' in/s (' + fmt(v_ext_ips * 5, 1) + ' ft/min)');
          setDisp('retract_speed', fmt(v_ret_ips, 2) + ' in/s');
          setDisp('extend_time_sec', fmt(t_ext, 1) + 's extend / ' + fmt(t_ret, 1) + 's retract');
          setDisp('hydraulic_hp', fmt(hp, 1) + ' HP');
        """
    }
]
