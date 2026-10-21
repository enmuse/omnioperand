"""
scripts/data_engineering_civil.py
25 High-Value Civil, Structural, Geotechnical & Hydraulic Engineering Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

ENGINEERING_CALCULATORS = [
    {
        "slug": "beam-deflection-bending-moment",
        "category": "engineering",
        "name": "Beam Deflection & Maximum Bending Moment Calculator",
        "description": "Calculate maximum bending moment, shear force, and mid-span elastic deflection for simply supported and cantilever steel or wood structural beams.",
        "hero_badge": "Structural Mechanics • Beam Analysis",
        "formula_display": "Max Deflection δ_max = (5 · w · L⁴) / (384 · E · I) | Max Moment M_max = (w · L²) / 8",
        "fields": [
            {"id": "beam_span_length_ft", "label": "Beam Clear Span Length (Feet)", "default": 20.0, "suffix": "ft", "min": 4, "max": 80, "step": 1, "hint": "Distance between support bearings"},
            {"id": "uniform_load_plf", "label": "Uniform Distributed Load (lbs/linear ft)", "default": 650, "suffix": "PLF", "min": 50, "max": 10000, "step": 25, "hint": "Combined Dead Load + Live Load (w)"},
            {"id": "elastic_modulus_ksi", "label": "Modulus of Elasticity (E in ksi)", "default": 29000, "suffix": "ksi", "min": 1000, "max": 35000, "step": 500, "hint": "Structural Steel = 29,000 ksi; Douglas Fir = 1,600 ksi"},
            {"id": "moment_of_inertia_in4", "label": "Moment of Inertia (I in inches⁴)", "default": 199, "suffix": "in⁴", "min": 5, "max": 5000, "step": 5, "hint": "Strong-axis section property (e.g. W12x26 = 204 in⁴)"}
        ],
        "metrics": [
            {"id": "max_bending_moment_ft_lbs", "label": "Maximum Bending Moment", "default_display": "32,500 ft-lbs", "highlight": True},
            {"id": "max_deflection_inches", "label": "Mid-Span Elastic Deflection", "default_display": "0.52 Inches", "highlight": True},
            {"id": "deflection_span_ratio", "label": "Deflection-to-Span Ratio", "default_display": "L / 462 (Passes L/360 Limit)", "highlight": True},
            {"id": "end_shear_reaction_lbs", "label": "End Support Shear Reaction", "default_display": "6,500 lbs Reaction"}
        ],
        "proof_steps": [
            {"step_title": "Maximum Bending Moment", "step_text": "M_max = (w · L²) / 8 = (650 PLF × 20²) / 8 = (650 × 400) / 8 = 32,500 ft-lbs (390,000 in-lbs)."},
            {"step_title": "Unit Harmonization for Deflection", "step_text": "Span L = 20 ft × 12 = 240 inches. Load w = 650 / 12 = 54.167 lbs/inch. E = 29,000,000 psi. I = 199 in⁴."},
            {"step_title": "Navier 4th-Order Elastic Deflection", "step_text": "δ_max = (5 · w · L⁴) / (384 · E · I) = (5 × 54.167 × 240⁴) / (384 × 29,000,000 × 199) = 899,105,280,000 / 2,216,064,000,000 = 0.405 inches."},
            {"step_title": "Building Code Deflection Limit Check", "step_text": "Span ratio = 240\" / 0.405\" = L / 592. This exceeds the IBC building code floor limit of L/360, proving adequate stiffness without perceptible floor bounce."}
        ],
        "faqs": [
            {"q": "What is the standard building code deflection limit for floors?", "a": "The International Building Code (IBC Table 1604.3) mandates that floor live load deflection must not exceed L/360 to prevent drywall ceiling cracking and uncomfortable occupant footstep bounce."},
            {"q": "What is the difference between strength and serviceability in beam design?", "a": "Strength checks ensure the beam will not physically break or yield under maximum loads (bending stress σ = M/S ≤ allowable yield). Serviceability checks ensure the beam does not sag noticeably (deflection) or vibrate during normal daily use."}
        ],
        "js_logic": """
          const lFt = getNum('beam_span_length_ft');
          const wPlf = getNum('uniform_load_plf');
          const eKsi = getNum('elastic_modulus_ksi');
          const iIn4 = getNum('moment_of_inertia_in4');

          const momentFtLbs = (wPlf * Math.pow(lFt, 2)) / 8;
          const endShear = (wPlf * lFt) / 2;

          const lIn = lFt * 12;
          const wIn = wPlf / 12;
          const ePsi = eKsi * 1000;
          const defl = (384 * ePsi * iIn4 > 0) ? (5 * wIn * Math.pow(lIn, 4)) / (384 * ePsi * iIn4) : 0;
          const spanRatio = defl > 0 ? Math.round(lIn / defl) : 999;

          setDisp('max_bending_moment_ft_lbs', Math.round(momentFtLbs).toLocaleString() + ' ft-lbs');
          setDisp('max_deflection_inches', defl.toFixed(2) + ' Inches');
          setDisp('deflection_span_ratio', 'L / ' + spanRatio + (spanRatio >= 360 ? ' (Passes L/360)' : ' (EXCEEDS LIMIT)'));
          setDisp('end_shear_reaction_lbs', Math.round(endShear).toLocaleString() + ' lbs Reaction');
        """
    },
    {
        "slug": "proctor-soil-compaction",
        "category": "engineering",
        "name": "Soil Compaction Dry Density & Optimum Moisture (Proctor Test)",
        "description": "Calculate soil dry density from wet bulk density and moisture content, and determine relative compaction percentage against ASTM D698 / D1557 Proctor maximums.",
        "hero_badge": "Geotechnical Engineering • Soil Compaction",
        "formula_display": "Dry Density γ_d = Wet Density γ_wet / (1 + Moisture Content w% / 100) | Relative Compaction = (γ_d / Max γ_d) × 100",
        "fields": [
            {"id": "measured_wet_density_pcf", "label": "Measured Field Wet Density (PCF)", "default": 132.5, "suffix": "PCF (lbs/cu ft)", "min": 85, "max": 160, "step": 0.5, "hint": "Nuclear density gauge field wet density measurement"},
            {"id": "soil_moisture_content_pct", "label": "Field Moisture Content (w %)", "default": 11.2, "suffix": "%", "min": 2, "max": 35, "step": 0.2, "hint": "Oven-dry or gauge moisture percentage"},
            {"id": "proctor_max_dry_density", "label": "Laboratory Maximum Dry Density (PCF)", "default": 122.0, "suffix": "PCF", "min": 90, "max": 150, "step": 0.5, "hint": "ASTM D698 Standard or D1557 Modified Proctor peak density"},
            {"id": "specified_compaction_pct", "label": "Specified Engineering Requirement (%)", "default": 95.0, "suffix": "%", "min": 85, "max": 100, "step": 0.5, "hint": "Standard specification: 95% under foundations and roadways"}
        ],
        "metrics": [
            {"id": "calculated_dry_density_pcf", "label": "Calculated Field Dry Density", "default_display": "119.15 PCF", "highlight": True},
            {"id": "relative_compaction_pct", "label": "Achieved Relative Compaction", "default_display": "97.7% Compaction", "highlight": True},
            {"id": "pass_fail_status", "label": "Engineering Specification Status", "default_display": "PASSES Specification (≥ 95.0%)", "highlight": True},
            {"id": "water_mass_pcf", "label": "Water Mass in Soil Matrix", "default_display": "13.35 lbs Water / cu ft"}
        ],
        "proof_steps": [
            {"step_title": "Phase Relationship for Dry Density", "step_text": "Dry Density γ_d = γ_wet / (1 + w/100) = 132.5 PCF / (1 + 0.112) = 132.5 / 1.112 = 119.15 lbs/cu ft."},
            {"step_title": "Relative Compaction Formulation", "step_text": "Relative Compaction RC% = (Field Dry Density / Lab Max Dry Density) × 100 = (119.15 / 122.0) × 100 = 97.66%."},
            {"step_title": "Quality Assurance Verdict", "step_text": "Because 97.7% exceeds the 95.0% specification, the soil lift meets structural subgrade bearing requirements without requiring re-rolling."}
        ],
        "faqs": [
            {"q": "What is the difference between Standard and Modified Proctor tests?", "a": "Standard Proctor (ASTM D698) uses a 5.5-lb hammer dropped from 12 inches (12,375 ft-lb/cu ft compactive energy). Modified Proctor (ASTM D1557) uses a 10-lb hammer dropped from 18 inches (56,250 ft-lb/cu ft), simulating heavy airfield and highway axle loads."},
            {"q": "Why does adding water increase soil compaction up to an optimum point?", "a": "Water acts as a lubricant between soil grains, allowing particles to slide into a tight, dense interlocking packing structure until the Optimum Moisture Content (OMC) is reached. Beyond OMC, water fills pore spaces and displaces solid soil grains, reducing density."}
        ],
        "js_logic": """
          const wetPcf = getNum('measured_wet_density_pcf');
          const moistPct = (getNum('soil_moisture_content_pct') || 11.2) / 100;
          const maxPcf = getNum('proctor_max_dry_density') || 122.0;
          const spec = getNum('specified_compaction_pct') || 95.0;

          const dryPcf = wetPcf / (1 + moistPct);
          const achievedComp = (dryPcf / maxPcf) * 100;
          const passes = achievedComp >= spec;
          const waterLbs = wetPcf - dryPcf;

          setDisp('calculated_dry_density_pcf', dryPcf.toFixed(2) + ' PCF');
          setDisp('relative_compaction_pct', achievedComp.toFixed(1) + '% Compaction');
          setDisp('pass_fail_status', passes ? 'PASSES Specification (>= ' + spec.toFixed(1) + '%)' : 'FAILS SPECIFICATION (Re-compact Lift)');
          setDisp('water_mass_pcf', waterLbs.toFixed(2) + ' lbs Water / cu ft');
        """
    },
    {
        "slug": "darcy-weisbach-head-loss",
        "category": "engineering",
        "name": "Darcy-Weisbach Pipe Friction Head Loss & Pressure Drop Calculator",
        "description": "Calculate friction head loss (h_f in feet), pressure drop (psi), and Reynolds number (laminar vs turbulent) for pressurized fluid flow in commercial pipe networks.",
        "hero_badge": "Hydraulic Engineering • Pipe Networks",
        "formula_display": "Head Loss h_f = f · (L / D) · (v² / [2 · g]) | Pressure Drop ΔP = h_f · ρ · g / 144",
        "fields": [
            {"id": "pipe_inside_diameter_in", "label": "Pipe Inside Diameter (Inches)", "default": 6.065, "suffix": "in", "min": 0.5, "max": 72, "step": 0.25, "hint": "Nominal 6-inch Schedule 40 Steel = 6.065 inches ID"},
            {"id": "pipe_length_feet", "label": "Total Pipe Run Length (Feet)", "default": 500, "suffix": "ft", "min": 10, "max": 50000, "step": 50, "hint": "Length of straight pipe run"},
            {"id": "flow_rate_gpm", "label": "Volumetric Flow Rate (GPM)", "default": 650, "suffix": "GPM", "min": 5, "max": 15000, "step": 25, "hint": "Water flow rate through pipe"},
            {"id": "darcy_friction_factor", "label": "Darcy Friction Factor (f)", "default": 0.019, "min": 0.008, "max": 0.08, "step": 0.001, "hint": "Moody chart value (commercial steel water pipe typically 0.018 - 0.022)"}
        ],
        "metrics": [
            {"id": "friction_head_loss_feet", "label": "Total Friction Head Loss", "default_display": "14.28 ft H₂O", "highlight": True},
            {"id": "pressure_drop_psi", "label": "Total Pressure Drop across Run", "default_display": "6.18 PSI Drop", "highlight": True},
            {"id": "fluid_flow_velocity_fps", "label": "Mean Flow Velocity", "default_display": "7.23 ft / second", "highlight": True},
            {"id": "reynolds_flow_regime", "label": "Reynolds Number Flow Regime", "default_display": "Turbulent (Re ≈ 3.7 × 10⁵)"}
        ],
        "proof_steps": [
            {"step_title": "Pipe Cross-Sectional Velocity", "step_text": "Inside Diameter D = 6.065\" / 12 = 0.5054 ft. Area A = π · (0.5054/2)² = 0.2006 sq ft. Flow Q = 650 GPM / 448.83 = 1.448 CFS. Velocity v = Q / A = 1.448 / 0.2006 = 7.22 ft/second."},
            {"step_title": "Velocity Head Component", "step_text": "v² / (2g) = 7.22² / (2 × 32.174) = 52.13 / 64.35 = 0.810 ft."},
            {"step_title": "Darcy-Weisbach Formulation", "step_text": "h_f = f · (L / D) · (v² / 2g) = 0.019 × (500 / 0.5054) × 0.810 = 0.019 × 989.3 × 0.810 = 15.23 feet of water column."},
            {"step_title": "Hydraulic Pressure Conversion", "step_text": "ΔP = h_f × 0.4335 psi/ft = 15.23 × 0.4335 = 6.60 PSI pressure drop."}
        ],
        "faqs": [
            {"q": "What is the recommended maximum water velocity in pipes?", "a": "For commercial water distribution, civil engineers design for 4 to 8 feet per second (fps). Velocities above 8-10 fps cause accelerated pipe wall erosion, excessive noise, and severe destructive water hammer surges."},
            {"q": "Why is Darcy-Weisbach preferred over Hazen-Williams?", "a": "Darcy-Weisbach is a fundamental physical law valid for all fluids (oil, gas, water, chemicals) across all temperatures and flow regimes. Hazen-Williams is an empirical approximation valid only for clean ambient water."}
        ],
        "js_logic": """
          const dIn = getNum('pipe_inside_diameter_in');
          const lFt = getNum('pipe_length_feet');
          const gpm = getNum('flow_rate_gpm');
          const f = getNum('darcy_friction_factor') || 0.019;

          const dFt = dIn / 12;
          const area = Math.PI * Math.pow(dFt / 2, 2);
          const cfs = gpm / 448.831;
          const v = area > 0 ? (cfs / area) : 0;
          const g = 32.174;

          const hf = dFt > 0 ? (f * (lFt / dFt) * (Math.pow(v, 2) / (2 * g))) : 0;
          const psi = hf * 0.4335;
          const re = (v * dFt) / 1.08e-5;

          setDisp('friction_head_loss_feet', hf.toFixed(2) + ' ft H₂O');
          setDisp('pressure_drop_psi', psi.toFixed(2) + ' PSI Drop');
          setDisp('fluid_flow_velocity_fps', v.toFixed(2) + ' ft / second');
          setDisp('reynolds_flow_regime', re > 4000 ? 'Turbulent (Re ≈ ' + (re / 1000).toFixed(0) + 'k)' : 'Laminar Flow');
        """
    },
    {
        "slug": "mannings-open-channel-flow",
        "category": "engineering",
        "name": "Manning's Open Channel Flow Velocity & Discharge Capacity Calculator",
        "description": "Calculate discharge capacity in CFS, flow velocity in fps, and hydraulic radius for trapezoidal, rectangular, and circular open channels.",
        "hero_badge": "Hydraulics • Open Channel Flow",
        "formula_display": "Flow Q = (1.486 / n) · Area · (Hydraulic Radius)^(2/3) · (Slope)^(1/2)",
        "fields": [
            {"id": "channel_bottom_width_ft", "label": "Channel Bottom Width (Feet)", "default": 6.0, "suffix": "ft", "min": 1, "max": 50, "step": 0.5, "hint": "Base width b of ditch or canal"},
            {"id": "water_flow_depth_ft", "label": "Water Flow Depth (Feet)", "default": 2.5, "suffix": "ft", "min": 0.2, "max": 20, "step": 0.1, "hint": "Vertical flow depth y"},
            {"id": "channel_bed_slope", "label": "Channel Bed Slope (ft/ft)", "default": 0.005, "min": 0.0001, "max": 0.05, "step": 0.0005, "hint": "Longitudinal slope S (e.g. 0.005 = 0.5% grade = 5 ft drop per 1,000 ft)"},
            {"id": "mannings_roughness_n", "label": "Manning's Roughness Coefficient (n)", "default": 0.035, "min": 0.010, "max": 0.100, "step": 0.002, "hint": "Smooth concrete = 0.013; Grass swale = 0.035; Natural stony stream = 0.050"}
        ],
        "metrics": [
            {"id": "total_discharge_cfs", "label": "Channel Discharge Capacity (Q)", "default_display": "148.5 CFS", "highlight": True},
            {"id": "flow_velocity_fps", "label": "Average Flow Velocity (v)", "default_display": "7.07 ft / second", "highlight": True},
            {"id": "flow_cross_section_sqft", "label": "Wetted Flow Area", "default_display": "21.0 sq ft"},
            {"id": "froude_number_regime", "label": "Froude Number Flow State", "default_display": "Supercritical Flow (Fr = 1.15)"}
        ],
        "proof_steps": [
            {"step_title": "Geometric Wetted Area and Perimeter", "step_text": "For a trapezoidal channel with 2:1 side slopes (z = 2): Area A = (b + zy) · y = (6 + 2×2.5) × 2.5 = 11.0 × 2.5 = 27.5 sq ft. Wetted Perimeter P = b + 2y√(1 + z²) = 6 + 2(2.5)√5 = 6 + 11.18 = 17.18 ft."},
            {"step_title": "Hydraulic Radius R", "step_text": "R = Area / Wetted Perimeter = 27.5 / 17.18 = 1.601 ft."},
            {"step_title": "Manning's Empirical Velocity Equation", "step_text": "v = (1.486 / n) · R^(2/3) · S^(1/2) = (1.486 / 0.035) × 1.601^(0.667) × 0.005^(0.5) = 42.457 × 1.368 × 0.07071 = 4.11 ft/sec."},
            {"step_title": "Total Discharge Capacity", "step_text": "Q = v · A = 4.11 ft/s × 27.5 sq ft = 113.0 CFS (cubic feet per second)."}
        ],
        "faqs": [
            {"q": "What is the Froude Number in open channel hydraulics?", "a": "The Froude number (Fr = v / √(g · D)) represents the ratio of inertial forces to gravity forces. Fr < 1 is tranquil subcritical flow; Fr = 1 is critical flow; Fr > 1 is rapid supercritical flow prone to hydraulic jumps."},
            {"q": "What is an acceptable velocity in grass-lined drainage swales?", "a": "To prevent soil scour and sod tearing, grassed waterways are typically limited to velocities between 3.0 and 5.0 fps depending on grass species and soil cohesiveness."}
        ],
        "js_logic": """
          const b = getNum('channel_bottom_width_ft');
          const y = getNum('water_flow_depth_ft');
          const s = getNum('channel_bed_slope') || 0.005;
          const n = getNum('mannings_roughness_n') || 0.035;

          const z = 2.0; // standard 2:1 side slopes
          const a = (b + z * y) * y;
          const p = b + 2 * y * Math.sqrt(1 + Math.pow(z, 2));
          const r = p > 0 ? (a / p) : 0;

          const v = r > 0 && n > 0 ? (1.486 / n) * Math.pow(r, 2 / 3) * Math.sqrt(s) : 0;
          const q = v * a;

          const dHyd = a / (b + 2 * z * y);
          const fr = dHyd > 0 ? v / Math.sqrt(32.174 * dHyd) : 0;

          setDisp('total_discharge_cfs', q.toFixed(1) + ' CFS');
          setDisp('flow_velocity_fps', v.toFixed(2) + ' ft / second');
          setDisp('flow_cross_section_sqft', a.toFixed(1) + ' sq ft');
          setDisp('froude_number_regime', fr > 1.0 ? 'Supercritical (Fr = ' + fr.toFixed(2) + ')' : 'Subcritical (Fr = ' + fr.toFixed(2) + ')');
        """
    },
    {
        "slug": "asce7-wind-load-pressure",
        "category": "engineering",
        "name": "ASCE 7 Wind Load Velocity Pressure on Building Envelopes Calculator",
        "description": "Calculate design wind velocity pressure (q_z in PSF) based on basic wind speed, surface roughness exposure category (B, C, D), and mean roof height (ASCE 7-16 / 7-22).",
        "hero_badge": "Structural Engineering • ASCE 7 Standards",
        "formula_display": "Velocity Pressure q_z = 0.00256 · K_z · K_zt · K_d · K_e · V²",
        "fields": [
            {"id": "basic_wind_speed_mph", "label": "Basic Design Wind Speed (mph)", "default": 115, "suffix": "mph (3-sec gust)", "min": 85, "max": 200, "step": 5, "hint": "ASCE 7-16 hazard wind speed map for project location"},
            {"id": "mean_roof_height_ft", "label": "Mean Roof Height (Feet)", "default": 30.0, "suffix": "ft", "min": 10, "max": 250, "step": 5, "hint": "Average height between eave and ridge"},
            {"id": "exposure_category", "label": "Surface Exposure Category (1 = B Suburban, 2 = C Open Grass, 3 = D Coastal)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "B: Urban/suburban wooded, C: Open terrain, D: Flat water/coastal"},
            {"id": "wind_directionality_kd", "label": "Wind Directionality Factor (K_d)", "default": 0.85, "min": 0.85, "max": 1.00, "step": 0.05, "hint": "0.85 for Main Wind-Force Resisting System (MWFRS) and Components"}
        ],
        "metrics": [
            {"id": "velocity_pressure_qz", "label": "Design Velocity Pressure (q_z)", "default_display": "20.3 PSF", "highlight": True},
            {"id": "height_exposure_factor_kz", "label": "Velocity Pressure Coefficient (K_z)", "default_display": "0.70 (Exposure B @ 30 ft)", "highlight": True},
            {"id": "cladding_peak_suction_psf", "label": "Corner Roof Cladding Suction", "default_display": "-38.6 PSF (Zone 3 Uplift)"},
            {"id": "dynamic_impact_head_psi", "label": "Dynamic Wind Pressure", "default_display": "0.14 PSI"}
        ],
        "proof_steps": [
            {"step_title": "Height Exposure Coefficient (K_z)", "step_text": "For Exposure Category B at 30 feet: K_z = 2.01 · (30 / 1200)^(2 / 7.0) = 0.70."},
            {"step_title": "Velocity Pressure Equation", "step_text": "q_z = 0.00256 · K_z · K_zt · K_d · K_e · V². Assuming flat terrain (K_zt = 1.0) and sea level (K_e = 1.0):"},
            {"step_title": "Numerical Evaluation", "step_text": "q_z = 0.00256 × 0.70 × 1.0 × 0.85 × 1.0 × (115)² = 0.0015232 × 13,225 = 20.14 lbs/sq ft (PSF)."},
            {"step_title": "Component & Cladding Zone 3 Suction", "step_text": "Applying roof corner external pressure coefficient GC_p = -1.8: Design Suction = 20.14 × (-1.8 - 0.18 internal) = -39.88 PSF net uplift."}
        ],
        "faqs": [
            {"q": "What is the difference between ASCE 7 Exposure B, C, and D?", "a": "Exposure B applies to urban, suburban, and wooded areas with closely spaced obstructions. Exposure C applies to open flat grasslands and agricultural plains. Exposure D applies to unobstructed flat coastal water surfaces extending at least 1 mile inland."},
            {"q": "Why are wind suction pressures on roof corners so much higher than wall pressures?", "a": "When wind hits a sharp building edge, intense localized flow separation vortices peel over the roof perimeter, creating localized negative suction uplift forces 2 to 3 times higher than wall stagnation pressures."}
        ],
        "js_logic": """
          const v = getNum('basic_wind_speed_mph');
          const h = getNum('mean_roof_height_ft');
          const exp = Math.round(getNum('exposure_category')) || 1;
          const kd = getNum('wind_directionality_kd') || 0.85;

          let kz = 0.70;
          let expName = 'Exposure B (Suburban)';
          if (exp === 1) {
            kz = 2.01 * Math.pow(Math.max(15, h) / 1200, 2 / 7.0);
            expName = 'Exposure B';
          } else if (exp === 2) {
            kz = 2.01 * Math.pow(Math.max(15, h) / 900, 2 / 9.5);
            expName = 'Exposure C (Open Terrain)';
          } else {
            kz = 2.01 * Math.pow(Math.max(15, h) / 700, 2 / 11.5);
            expName = 'Exposure D (Coastal)';
          }

          const qz = 0.00256 * kz * 1.0 * kd * 1.0 * Math.pow(v, 2);
          const cornerSuction = qz * (-1.8 - 0.18);

          setDisp('velocity_pressure_qz', qz.toFixed(1) + ' PSF');
          setDisp('height_exposure_factor_kz', kz.toFixed(2) + ' (' + expName + ' @ ' + h + ' ft)');
          setDisp('cladding_peak_suction_psf', cornerSuction.toFixed(1) + ' PSF (Zone 3 Suction)');
          setDisp('dynamic_impact_head_psi', (qz / 144).toFixed(3) + ' PSI');
        """
    },
    {
        "slug": "concrete-slab-shear-capacity",
        "category": "engineering",
        "name": "Reinforced Concrete Slab One-Way & Two-Way Punching Shear Capacity (ACI 318)",
        "description": "Calculate nominal concrete shear strength (V_c), critical shear perimeter (b_0), and punching shear failure capacity around interior column supports.",
        "hero_badge": "Structural Concrete • ACI 318 Standard",
        "formula_display": "Two-Way Punching Shear V_c = 4 · λ · √(f'c) · b₀ · d | One-Way Beam Shear V_c = 2 · λ · √(f'c) · b · d",
        "fields": [
            {"id": "concrete_strength_f_c", "label": "Concrete Compressive Strength (f'c in PSI)", "default": 4000, "suffix": "PSI", "min": 2500, "max": 10000, "step": 500, "hint": "28-day cylinder compressive strength"},
            {"id": "slab_effective_depth_d", "label": "Slab Effective Structural Depth (d in Inches)", "default": 7.0, "suffix": "in", "min": 3.5, "max": 36, "step": 0.5, "hint": "Distance from extreme compression fiber to center of rebar (slab thickness minus cover)"},
            {"id": "column_dimension_c1", "label": "Square Column Width (Inches)", "default": 18, "suffix": "in", "min": 8, "max": 48, "step": 2, "hint": "Supporting column face dimension"}
        ],
        "metrics": [
            {"id": "two_way_punching_shear_kips", "label": "Design Two-Way Punching Capacity (φV_c)", "default_display": "133.4 Kips", "highlight": True},
            {"id": "critical_shear_perimeter_b0", "label": "Critical Shear Perimeter (b₀)", "default_display": "100.0 Inches (at d/2)", "highlight": True},
            {"id": "nominal_shear_strength_psi", "label": "Nominal Concrete Shear Stress", "default_display": "253.0 PSI (4√f'c)", "highlight": True},
            {"id": "one_way_shear_per_foot", "label": "One-Way Beam Shear Capacity", "default_display": "7.97 Kips / Linear Foot"}
        ],
        "proof_steps": [
            {"step_title": "Critical Perimeter at d/2 Face", "step_text": "ACI 318-19 Section 22.6 specifies punching shear failure occurs on a truncated pyramid perimeter at distance d/2 from the column face. b₀ = 4 × (Column Width + d) = 4 × (18\" + 7\") = 4 × 25\" = 100 inches."},
            {"step_title": "Nominal Concrete Shear Stress", "step_text": "v_c = 4 · λ · √(f'c) = 4 · 1.0 · √4000 = 4 × 63.245 = 252.98 PSI."},
            {"step_title": "Nominal Punching Shear Strength (V_c)", "step_text": "V_c = v_c · b₀ · d = 252.98 PSI × 100\" × 7.0\" = 177,086 lbs = 177.09 kips."},
            {"step_title": "Design Shear Strength (φV_c)", "step_text": "Strength reduction factor φ = 0.75 for shear. φV_c = 0.75 × 177.09 = 132.82 kips allowable column reaction."}
        ],
        "faqs": [
            {"q": "Why is punching shear the most dangerous failure mode in flat-slab buildings?", "a": "Punching shear is a sudden, brittle failure with zero warning signs. The floor slab punches downward around the column head, which can trigger a progressive 'pancake' collapse of entire multi-story concrete structures."},
            {"q": "How do structural engineers increase punching shear capacity?", "a": "Increase slab thickness, enlarge column capitals, add drop panels, or cast vertical shear reinforcement studs (stud rails) within the slab around column perimeters."}
        ],
        "js_logic": """
          const fc = getNum('concrete_strength_f_c');
          const d = getNum('slab_effective_depth_d');
          const col = getNum('column_dimension_c1');

          const b0 = 4 * (col + d);
          const sqrtFc = Math.sqrt(fc);
          const vcStress = 4 * sqrtFc;
          const vcKips = (vcStress * b0 * d) / 1000;
          const phiVc = vcKips * 0.75;
          const oneWayPerFt = (2 * sqrtFc * 12 * d * 0.75) / 1000;

          setDisp('two_way_punching_shear_kips', phiVc.toFixed(1) + ' Kips (Design phi*Vc)');
          setDisp('critical_shear_perimeter_b0', b0.toFixed(1) + ' Inches (at d/2)');
          setDisp('nominal_shear_strength_psi', vcStress.toFixed(1) + ' PSI (4*sqrt[f\'c])');
          setDisp('one_way_shear_per_foot', oneWayPerFt.toFixed(2) + ' Kips / Linear Foot');
        """
    },
    {
        "slug": "earthwork-cut-and-fill",
        "category": "engineering",
        "name": "Earthwork Cut and Fill Volume Calculator (Average End Area Method)",
        "description": "Calculate earthwork excavation cut and fill volumes in cubic yards between station cross-sections using the standard civil Average End Area Method.",
        "hero_badge": "Civil Site Design • Earthwork Volumes",
        "formula_display": "Volume (Cu Yds) = [(Area₁ + Area₂) / 2] × (Station Distance L in Feet) / 27",
        "fields": [
            {"id": "station_1_cut_area_sqft", "label": "Station 1 Cut Cross-Section Area (sq ft)", "default": 245.0, "suffix": "sq ft", "min": 0, "max": 10000, "step": 5, "hint": "End area of cut at first station"},
            {"id": "station_2_cut_area_sqft", "label": "Station 2 Cut Cross-Section Area (sq ft)", "default": 310.0, "suffix": "sq ft", "min": 0, "max": 10000, "step": 5, "hint": "End area of cut at second station"},
            {"id": "station_interval_length_ft", "label": "Distance Between Stations (Feet)", "default": 100.0, "suffix": "ft", "min": 10, "max": 500, "step": 10, "hint": "Standard survey station distance = 100 ft (1+00 to 2+00)"},
            {"id": "soil_shrink_swell_pct", "label": "Soil Compaction Shrinkage Factor (%)", "default": 12.0, "suffix": "%", "min": 0, "max": 30, "step": 1, "hint": "Volume loss when loose excavated cut is compacted into fill"}
        ],
        "metrics": [
            {"id": "cut_volume_cubic_yards", "label": "Total Cut Volume (In-Situ Bank)", "default_display": "1,027.8 Cu Yds", "highlight": True},
            {"id": "compacted_fill_equivalent", "label": "Compacted Fill Yield", "default_display": "904.4 Cu Yds (After 12% Shrink)", "highlight": True},
            {"id": "truckloads_triaxle_15cy", "label": "Estimated Dump Truck Hauls", "default_display": "69 Truckloads (15 CY Tri-Axle)"},
            {"id": "average_cut_area_sqft", "label": "Mean Cross-Sectional Area", "default_display": "277.5 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Average End Area Rule", "step_text": "Mean End Area A_avg = (A₁ + A₂) / 2 = (245 + 310) / 2 = 277.5 sq ft."},
            {"step_title": "Prismatic Volume Conversion", "step_text": "Cubic Feet = A_avg × Distance = 277.5 sq ft × 100 ft = 27,750 cubic feet."},
            {"step_title": "Cubic Yardage Quantification", "step_text": "Volume in Bank Cubic Yards (BCY) = 27,750 / 27 = 1,027.78 Cu Yds."},
            {"step_title": "Compaction Shrinkage Correction", "step_text": "When placed into engineered embankment fill, soil loses volume to compaction: Fill Volume = 1,027.78 × (1 - 0.12) = 904.45 Compacted Cubic Yards (CCY)."}
        ],
        "faqs": [
            {"q": "What is the difference between Bank, Loose, and Compacted cubic yards?", "a": "Bank (In-situ): Soil in its natural undisturbed ground state. Loose: Soil after excavation that has expanded (swelled by 15-25%). Compacted: Soil rolled with heavy machinery into a dense fill embankment (shrinks by 10-15% below bank volume)."},
            {"q": "When is the Prismoidal formula preferred over Average End Area?", "a": "Average End Area tends to slightly overestimate volumes (typically by 1% to 3%) when adjacent cross-section areas differ significantly. The Prismoidal formula incorporates a middle cross-section for higher precision in steep, irregular terrain."}
        ],
        "js_logic": """
          const a1 = getNum('station_1_cut_area_sqft');
          const a2 = getNum('station_2_cut_area_sqft');
          const l = getNum('station_interval_length_ft') || 100;
          const shrink = (getNum('soil_shrink_swell_pct') || 12) / 100;

          const avgArea = (a1 + a2) / 2;
          const cuft = avgArea * l;
          const bcy = cuft / 27;
          const ccy = bcy * (1 - shrink);
          const trucks = Math.ceil(bcy / 15);

          setDisp('cut_volume_cubic_yards', Math.round(bcy * 10) / 10 + ' Cu Yds');
          setDisp('compacted_fill_equivalent', Math.round(ccy * 10) / 10 + ' Cu Yds (After Shrink)');
          setDisp('truckloads_triaxle_15cy', trucks + ' Truckloads (15 CY Tri-Axle)');
          setDisp('average_cut_area_sqft', avgArea.toFixed(1) + ' sq ft');
        """
    },
    {
        "slug": "retaining-wall-rankine-earth",
        "category": "engineering",
        "name": "Retaining Wall Rankine Lateral Earth Pressure (Active & Passive) Calculator",
        "description": "Calculate active and passive earth pressure coefficients (Ka, Kp), total lateral thrust force, and overturning moment for retaining wall design.",
        "hero_badge": "Geotechnical • Retaining Wall Mechanics",
        "formula_display": "Active Coefficient Ka = tan²(45° - ϕ / 2) | Total Thrust P_a = ½ · Ka · γ · H²",
        "fields": [
            {"id": "wall_stem_height_ft", "label": "Retaining Wall Height (H in Feet)", "default": 12.0, "suffix": "ft", "min": 3, "max": 35, "step": 0.5, "hint": "Height from footing base to top of retained soil"},
            {"id": "soil_internal_friction_angle_deg", "label": "Soil Internal Friction Angle (ϕ in Degrees)", "default": 32.0, "suffix": "degrees", "min": 20, "max": 45, "step": 1, "hint": "Granular backfill typically ϕ = 30° to 34°"},
            {"id": "soil_unit_weight_pcf", "label": "Backfill Moist Soil Unit Weight (γ in PCF)", "default": 120.0, "suffix": "PCF", "min": 95, "max": 140, "step": 5, "hint": "Compacted sand/gravel backfill density"}
        ],
        "metrics": [
            {"id": "total_active_thrust_force", "label": "Total Active Lateral Force (P_a)", "default_display": "2,642.0 lbs / linear ft", "highlight": True},
            {"id": "active_pressure_coeff_ka", "label": "Rankine Active Coefficient (Ka)", "default_display": "0.307", "highlight": True},
            {"id": "overturning_moment_ft_lbs", "label": "Overturning Moment About Toe", "default_display": "10,568 ft-lbs / ft", "highlight": True},
            {"id": "passive_pressure_coeff_kp", "label": "Rankine Passive Coefficient (Kp)", "default_display": "3.255"}
        ],
        "proof_steps": [
            {"step_title": "Rankine Active Earth Coefficient (Ka)", "step_text": "Ka = tan²(45° - ϕ / 2). For ϕ = 32°: Ka = tan²(45° - 16°) = tan²(29°) = 0.5543² = 0.3073."},
            {"step_title": "Triangular Pressure Distribution", "step_text": "Lateral pressure increases linearly with depth: Pressure at base σ_h = Ka · γ · H = 0.3073 × 120 PCF × 12 ft = 442.5 lbs/sq ft."},
            {"step_title": "Total Resultant Force (P_a)", "step_text": "P_a = ½ · σ_h · H = ½ × 442.5 × 12 = 2,655.0 lbs per linear foot of wall, acting at H/3 (4.0 ft above the base)."},
            {"step_title": "Overturning Moment About Toe", "step_text": "Moment M_ot = P_a × (H / 3) = 2,655.0 × 4.0 ft = 10,620.0 ft-lbs per linear foot."}
        ],
        "faqs": [
            {"q": "What is the difference between Active (Ka), At-Rest (K0), and Passive (Kp) earth pressure?", "a": "Active pressure (Ka ~0.3) develops when the wall tilts slightly away from the soil, mobilizing internal friction. At-Rest (K0 ~0.5) applies to rigid basement walls that cannot deflect. Passive pressure (Kp ~3.0+) develops when the wall is pushed violently INTO the soil, generating massive resisting force."},
            {"q": "Why is free-draining gravel backfill required behind retaining walls?", "a": "If water pools behind a retaining wall without drainage weep holes, hydrostatic water pressure adds 62.4 lbs/sq ft per foot of depth, tripling total overturning forces and causing sudden catastrophic wall blowouts."}
        ],
        "js_logic": """
          const h = getNum('wall_stem_height_ft');
          const phiDeg = getNum('soil_internal_friction_angle_deg') || 32;
          const gamma = getNum('soil_unit_weight_pcf') || 120;

          const phiRad = (phiDeg * Math.PI) / 180;
          const ka = Math.pow(Math.tan((45 * Math.PI / 180) - (phiRad / 2)), 2);
          const kp = Math.pow(Math.tan((45 * Math.PI / 180) + (phiRad / 2)), 2);

          const pa = 0.5 * ka * gamma * Math.pow(h, 2);
          const moment = pa * (h / 3);

          setDisp('total_active_thrust_force', Math.round(pa).toLocaleString() + '.0 lbs / linear ft');
          setDisp('active_pressure_coeff_ka', ka.toFixed(3));
          setDisp('overturning_moment_ft_lbs', Math.round(moment).toLocaleString() + ' ft-lbs / ft');
          setDisp('passive_pressure_coeff_kp', kp.toFixed(3));
        """
    },
    {
        "slug": "rational-method-stormwater",
        "category": "engineering",
        "name": "Stormwater Runoff Peak Discharge Calculator (Rational Method Q = C·I·A)",
        "description": "Calculate watershed peak stormwater runoff discharge in cubic feet per second (CFS) for drainage culverts and retention detention basin sizing.",
        "hero_badge": "Civil Hydrology • Stormwater Runoff",
        "formula_display": "Peak Runoff Q = C · I · A | 1 Acre-Inch/Hour ≈ 1.008 CFS",
        "fields": [
            {"id": "runoff_coefficient_c", "label": "Runoff Coefficient (C)", "default": 0.85, "min": 0.10, "max": 0.95, "step": 0.05, "hint": "Asphalt/Roofs = 0.85 - 0.95; Lawns/Grass = 0.15 - 0.25; Commercial = 0.70 - 0.85"},
            {"id": "rainfall_intensity_in_hr", "label": "Design Rainfall Intensity (I in Inches/Hour)", "default": 4.2, "suffix": "in/hr", "min": 0.5, "max": 12.0, "step": 0.1, "hint": "NOAA Atlas 14 precipitation rate for design storm (e.g. 10-year or 25-year event)"},
            {"id": "drainage_basin_acres", "label": "Contributing Drainage Basin Area (Acres)", "default": 14.5, "suffix": "acres", "min": 0.2, "max": 200, "step": 0.5, "hint": "Catchment watershed area draining to point"}
        ],
        "metrics": [
            {"id": "peak_discharge_cfs", "label": "Peak Stormwater Discharge (Q)", "default_display": "51.8 CFS", "highlight": True},
            {"id": "required_culvert_diameter_in", "label": "Recommended Culvert Diameter", "default_display": "36-Inch RCP Pipe", "highlight": True},
            {"id": "rainfall_volume_gallons_min", "label": "Peak Inflow Rate (GPM)", "default_display": "23,248 Gallons / Minute"},
            {"id": "impervious_coverage_rating", "label": "Surface Imperviousness", "default_display": "High Impervious Commercial Site"}
        ],
        "proof_steps": [
            {"step_title": "Rational Equation Derivation", "step_text": "Q = C · I · A = 0.85 × 4.2 in/hr × 14.5 acres = 51.765 CFS."},
            {"step_title": "Unit Dimensional Parity", "step_text": "1 acre = 43,560 sq ft. 1 inch/hour = 1/12 ft / 3,600s = 1/43,200 ft/s. 43,560 / 43,200 = 1.0083 CFS per acre-inch/hr. Therefore, Q ≈ C · I · A directly in CFS."},
            {"step_title": "Conveyance Infrastructure Sizing", "step_text": "To convey 51.8 CFS at allowable 6 fps velocity requires a 36-inch reinforced concrete pipe (RCP culvert cross-sectional area = 7.07 sq ft × 7.3 fps = 51.6 CFS)."}
        ],
        "faqs": [
            {"q": "What is the maximum watershed size for the Rational Method?", "a": "The Rational Method is strictly valid only for small catchments under 200 acres (or under 1 square mile). For larger watersheds, hydrologists must use unit hydrograph methods (NRCS TR-55 or HEC-HMS) to account for spatial rainfall variation and routing delay."},
            {"q": "What is the Time of Concentration (Tc)?", "a": "Time of concentration is the time required for water to travel from the most hydraulically remote point in the watershed to the outlet. In the Rational Method, the rainfall intensity (I) used MUST equal the storm duration corresponding to Tc."}
        ],
        "js_logic": """
          const c = getNum('runoff_coefficient_c') || 0.85;
          const i = getNum('rainfall_intensity_in_hr') || 4.2;
          const a = getNum('drainage_basin_acres');

          const q = c * i * a;
          const gpm = q * 448.831;

          let pipeDia = '18-Inch RCP';
          if (q > 75) pipeDia = '48-Inch RCP / Double 36\"';
          else if (q > 45) pipeDia = '36-Inch RCP Pipe';
          else if (q > 25) pipeDia = '30-Inch RCP Pipe';
          else if (q > 12) pipeDia = '24-Inch RCP Pipe';

          setDisp('peak_discharge_cfs', q.toFixed(1) + ' CFS');
          setDisp('required_culvert_diameter_in', pipeDia);
          setDisp('rainfall_volume_gallons_min', Math.round(gpm).toLocaleString() + ' GPM');
          setDisp('impervious_coverage_rating', c >= 0.8 ? 'High Impervious Commercial (C >= 0.8)' : (c >= 0.5 ? 'Moderate Residential (C ≈ 0.5)' : 'Pervious Parkland / Grass'));
        """
    },
    {
        "slug": "pavement-structural-number-esal",
        "category": "engineering",
        "name": "Asphalt Pavement Structural Number & AASHTO ESAL Design Life Calculator",
        "description": "Calculate flexible asphalt pavement Structural Number (SN), layer thicknesses (surface, base, subbase), and allowable 18-kip Equivalent Single Axle Loads (ESAL).",
        "hero_badge": "Highway Engineering • AASHTO Pavement",
        "formula_display": "Structural Number SN = (a₁ · D₁) + (a₂ · D₂ · m₂) + (a₃ · D₃ · m₃)",
        "fields": [
            {"id": "surface_course_thickness_in", "label": "Asphalt Surface Layer Thickness (D₁ in Inches)", "default": 4.0, "suffix": "in", "min": 2.0, "max": 10.0, "step": 0.5, "hint": "Hot Mix Asphalt (HMA) wearing course thickness (a₁ = 0.44)"},
            {"id": "crushed_stone_base_thickness_in", "label": "Crushed Stone Base Thickness (D₂ in Inches)", "default": 8.0, "suffix": "in", "min": 4.0, "max": 18.0, "step": 1.0, "hint": "Dense graded aggregate base course (a₂ = 0.14)"},
            {"id": "subbase_layer_thickness_in", "label": "Granular Subbase Thickness (D₃ in Inches)", "default": 6.0, "suffix": "in", "min": 0.0, "max": 24.0, "step": 1.0, "hint": "Subbase layer thickness (a₃ = 0.11)"}
        ],
        "metrics": [
            {"id": "calculated_structural_number", "label": "Total Structural Number (SN)", "default_display": "3.54 SN", "highlight": True},
            {"id": "allowable_design_esals", "label": "Allowable 18-kip Heavy Axle ESALs", "default_display": "2,450,000 ESALs", "highlight": True},
            {"id": "traffic_corridor_class", "label": "Roadway Classification Capacity", "default_display": "Heavy Commercial Highway (Class 3)", "highlight": True},
            {"id": "total_pavement_section_depth", "label": "Total Cross-Section Depth", "default_display": "18.0 Inches Combined"}
        ],
        "proof_steps": [
            {"step_title": "AASHTO Flexible Pavement Structural Layer Coefficients", "step_text": "Dense HMA surface a₁ = 0.44/inch. Crushed stone base a₂ = 0.14/inch. Granular subbase a₃ = 0.11/inch. Drainage coefficients m₂ = m₃ = 1.0."},
            {"step_title": "Structural Number (SN) Integration", "step_text": "SN = (0.44 × 4.0\") + (0.14 × 8.0\") + (0.11 × 6.0\") = 1.76 + 1.12 + 0.66 = 3.54."},
            {"step_title": "AASHTO Empirical Traffic Capacity", "step_text": "An SN of 3.54 over a standard subgrade CBR of 5 supports approximately 2.45 million 18,000-lb equivalent single axle load (ESAL) truck passes over a 20-year design life."}
        ],
        "faqs": [
            {"q": "What is an ESAL in highway design?", "a": "An ESAL (Equivalent Single Axle Load) standardizes all truck axle weights to the damaging effect of a single 18,000-lb axle. Under the AASHTO Fourth Power Law, one 80,000-lb semi-truck causes the pavement damage equivalent of nearly 4,000 passenger cars!"},
            {"q": "Why is aggregate base thickness critical in cold climates?", "a": "Aggregate base and subbase layers must provide adequate total pavement depth to exceed the regional winter frost depth line (frost penetration), preventing destructive frost heaves and springtime thaw-weakening."}
        ],
        "js_logic": """
          const d1 = getNum('surface_course_thickness_in');
          const d2 = getNum('crushed_stone_base_thickness_in');
          const d3 = getNum('subbase_layer_thickness_in');

          const sn = (0.44 * d1) + (0.14 * d2) + (0.11 * d3);
          const totalDepth = d1 + d2 + d3;
          const esal = Math.pow(10, (sn - 0.5) * 1.6) * 5000;

          let roadClass = 'Light Residential Street';
          if (sn >= 4.0) roadClass = 'Heavy Interstate Highway (High Truck Volume)';
          else if (sn >= 3.2) roadClass = 'Heavy Commercial Arterial Highway';
          else if (sn >= 2.5) roadClass = 'Collector Roadway / Bus Route';

          setDisp('calculated_structural_number', sn.toFixed(2) + ' SN');
          setDisp('allowable_design_esals', Math.round(esal).toLocaleString() + ' ESALs');
          setDisp('traffic_corridor_class', roadClass);
          setDisp('total_pavement_section_depth', totalDepth.toFixed(1) + ' Inches Combined');
        """
    },
    {
        "slug": "euler-column-buckling-load",
        "category": "engineering",
        "name": "Steel Column Euler Critical Buckling Load & Slenderness Ratio Calculator",
        "description": "Calculate Euler critical elastic buckling load (P_cr in kips), slenderness ratio (KL/r), and critical buckling stress for structural columns.",
        "hero_badge": "Mechanics of Materials • Buckling",
        "formula_display": "Critical Buckling Load P_cr = (π² · E · I) / (K · L)² | Critical Stress σ_cr = (π² · E) / (KL / r)²",
        "fields": [
            {"id": "column_unbraced_length_ft", "label": "Column Unbraced Length (Feet)", "default": 14.0, "suffix": "ft", "min": 4, "max": 50, "step": 1, "hint": "Clear vertical height between lateral braces"},
            {"id": "end_boundary_condition", "label": "End Support Boundary (1 = Pinned-Pinned, 2 = Fixed-Free, 3 = Fixed-Pinned, 4 = Fixed-Fixed)", "default": 1, "min": 1, "max": 4, "step": 1, "hint": "1: K=1.0, 2: K=2.0 (flagpole), 3: K=0.7, 4: K=0.5"},
            {"id": "column_moment_of_inertia_in4", "label": "Weak-Axis Moment of Inertia (I_y in in⁴)", "default": 53.4, "suffix": "in⁴", "min": 2, "max": 2000, "step": 2, "hint": "Weak-axis section property (e.g. W8x31 I_y = 37.1 in⁴, W10x49 I_y = 93.4 in⁴)"},
            {"id": "steel_modulus_elasticity_ksi", "label": "Steel Elastic Modulus (E in ksi)", "default": 29000, "suffix": "ksi", "min": 10000, "max": 35000, "step": 500, "hint": "Standard structural steel E = 29,000 ksi"}
        ],
        "metrics": [
            {"id": "euler_critical_buckling_load", "label": "Euler Critical Buckling Load (P_cr)", "default_display": "537.4 Kips", "highlight": True},
            {"id": "effective_length_factor_k", "label": "Effective Length Factor (K)", "default_display": "1.00 (Pinned-Pinned)", "highlight": True},
            {"id": "effective_column_length_in", "label": "Effective Length (KL)", "default_display": "168.0 Inches"},
            {"id": "buckling_failure_mode", "label": "Dominant Failure Mode", "default_display": "Elastic Global Flexural Buckling"}
        ],
        "proof_steps": [
            {"step_title": "Effective Length (KL) Formulation", "step_text": "Pinned-Pinned boundary condition yields K = 1.0. Effective Length KL = 1.0 × 14 ft × 12 = 168.0 inches."},
            {"step_title": "Euler Fundamental Formula", "step_text": "P_cr = (π² · E · I) / (KL)². E = 29,000,000 psi. I = 53.4 in⁴. KL = 168.0 in."},
            {"step_title": "Numerical Evaluation", "step_text": "Numerator = π² × 29,000,000 × 53.4 = 9.8696 × 1.5486×10⁹ = 15,284,000,000. Denominator = 168² = 28,224. P_cr = 15,284,000,000 / 28,224 = 541,525 lbs = 541.5 kips."}
        ],
        "faqs": [
            {"q": "What is the Effective Length Factor K in column buckling?", "a": "Factor K modifies the physical length of a column based on how its ends are restrained against rotation and translation. K=1.0 for pinned-pinned, K=0.5 for fixed-fixed, and K=2.0 for a cantilever flagpole fixed at base and free at top."},
            {"q": "Why does a column always buckle about its weak axis?", "a": "Buckling resistance is directly proportional to moment of inertia I. Because I_y (weak axis) is much smaller than I_x (strong axis) in standard I-beams and wide flanges, a column without intermediate lateral bracing will always buckle sideways around its weak axis."}
        ],
        "js_logic": """
          const lFt = getNum('column_unbraced_length_ft');
          const cond = Math.round(getNum('end_boundary_condition')) || 1;
          const iVal = getNum('column_moment_of_inertia_in4');
          const eKsi = getNum('steel_modulus_elasticity_ksi') || 29000;

          let k = 1.0;
          let condLabel = '1.00 (Pinned-Pinned)';
          if (cond === 2) { k = 2.0; condLabel = '2.00 (Fixed-Free Cantilever)'; }
          else if (cond === 3) { k = 0.7; condLabel = '0.70 (Fixed-Pinned)'; }
          else if (cond === 4) { k = 0.5; condLabel = '0.50 (Fixed-Fixed)'; }

          const kl = k * lFt * 12;
          const ePsi = eKsi * 1000;
          const pcrLbs = kl > 0 ? (Math.pow(Math.PI, 2) * ePsi * iVal) / Math.pow(kl, 2) : 0;
          const pcrKips = pcrLbs / 1000;

          setDisp('euler_critical_buckling_load', pcrKips.toFixed(1) + ' Kips');
          setDisp('effective_length_factor_k', condLabel);
          setDisp('effective_column_length_in', kl.toFixed(1) + ' Inches');
          setDisp('buckling_failure_mode', 'Elastic Flexural Column Buckling');
        """
    },
    {
        "slug": "terzaghi-bearing-capacity",
        "category": "engineering",
        "name": "Shallow Foundation Bearing Capacity Calculator (Terzaghi Equation)",
        "description": "Calculate ultimate and allowable soil bearing capacity (q_ult, q_all in PSF) for strip and square shallow footings using Terzaghi's bearing capacity factors.",
        "hero_badge": "Geotechnical • Foundation Bearing",
        "formula_display": "q_ult = (c · Nc · sc) + (q · Nq) + (0.5 · γ · B · Nγ · sγ) | q_all = q_ult / Safety Factor (typically 3.0)",
        "fields": [
            {"id": "footing_width_b_ft", "label": "Footing Width (B in Feet)", "default": 6.0, "suffix": "ft", "min": 1.5, "max": 30, "step": 0.5, "hint": "Width of shallow spread footing"},
            {"id": "footing_embedment_depth_df_ft", "label": "Footing Embedment Depth (Df in Feet)", "default": 4.0, "suffix": "ft", "min": 1.5, "max": 15, "step": 0.5, "hint": "Depth below finished grade to bottom of footing"},
            {"id": "soil_cohesion_psf", "label": "Soil Cohesion (c in PSF)", "default": 250, "suffix": "PSF", "min": 0, "max": 4000, "step": 50, "hint": "Clay cohesion (c=0 for pure clean sand)"},
            {"id": "soil_internal_friction_deg", "label": "Soil Friction Angle (ϕ in Degrees)", "default": 28.0, "suffix": "degrees", "min": 0, "max": 45, "step": 1, "hint": "Internal angle of shearing resistance"},
            {"id": "soil_unit_weight_pcf", "label": "Soil Unit Weight (γ in PCF)", "default": 115.0, "suffix": "PCF", "min": 90, "max": 140, "step": 5, "hint": "Moist soil density"}
        ],
        "metrics": [
            {"id": "allowable_bearing_capacity_psf", "label": "Allowable Bearing Capacity (q_all)", "default_display": "4,120 PSF", "highlight": True},
            {"id": "ultimate_bearing_capacity_psf", "label": "Ultimate Bearing Capacity (q_ult)", "default_display": "12,360 PSF (FS = 3.0)", "highlight": True},
            {"id": "total_column_load_allowable", "label": "Max Safe Column Load on 6x6 Footing", "default_display": "148.3 Kips (148,320 lbs)", "highlight": True},
            {"id": "overburden_pressure_q", "label": "Surcharge Overburden Pressure (q)", "default_display": "460.0 PSF"}
        ],
        "proof_steps": [
            {"step_title": "Terzaghi Bearing Capacity Factors (ϕ = 28°)", "step_text": "Nc = 31.61, Nq = 17.81, Nγ = 15.70. Shape factors for square footing: sc = 1.3, sγ = 0.8."},
            {"step_title": "Overburden Surcharge at Base", "step_text": "q = γ · Df = 115 PCF × 4.0 ft = 460.0 PSF."},
            {"step_title": "Terzaghi General Bearing Equation", "step_text": "q_ult = (1.3 · c · Nc) + (q · Nq) + (0.4 · γ · B · Nγ) = (1.3 × 250 × 31.61) + (460 × 17.81) + (0.4 × 115 × 6 × 15.70) = 10,273 + 8,193 + 4,333 = 22,799 PSF."},
            {"step_title": "Engineering Safety Factor Application", "step_text": "q_all = q_ult / FS = 22,799 / 3.0 = 7,600 PSF. Maximum column load on 6x6 footing = 7,600 × 36 sq ft = 273,600 lbs."}
        ],
        "faqs": [
            {"q": "Why is a Factor of Safety of 3.0 standard for foundation bearing capacity?", "a": "A high safety factor of 3.0 is required in geotechnical engineering due to inherent soil variability across a building site, sampling disturbances, and to strictly limit total settlement to under 1.0 inch."},
            {"q": "What happens if the groundwater table rises above footing depth?", "a": "When groundwater submerges the footing, the soil's effective unit weight drops by nearly 50% (buoyant unit weight γ' = γ_sat - 62.4 PCF), cutting the soil self-weight bearing component in half."}
        ],
        "js_logic": """
          const b = getNum('footing_width_b_ft');
          const df = getNum('footing_embedment_depth_df_ft');
          const c = getNum('soil_cohesion_psf');
          const phi = getNum('soil_internal_friction_deg') || 28;
          const gamma = getNum('soil_unit_weight_pcf') || 115;

          const phiRad = (phi * Math.PI) / 180;
          const nq = Math.pow(Math.tan((45 * Math.PI / 180) + (phiRad / 2)), 2) * Math.exp(Math.PI * Math.tan(phiRad));
          const nc = phi > 0 ? (nq - 1) / Math.tan(phiRad) : 5.7;
          const nGamma = 2 * (nq + 1) * Math.tan(phiRad);

          const qOverburden = gamma * df;
          const qUlt = (1.3 * c * nc) + (qOverburden * nq) + (0.4 * gamma * b * nGamma);
          const qAll = qUlt / 3.0;
          const totalColKips = (qAll * Math.pow(b, 2)) / 1000;

          setDisp('allowable_bearing_capacity_psf', Math.round(qAll).toLocaleString() + ' PSF');
          setDisp('ultimate_bearing_capacity_psf', Math.round(qUlt).toLocaleString() + ' PSF (FS = 3.0)');
          setDisp('total_column_load_allowable', totalColKips.toFixed(1) + ' Kips (' + Math.round(totalColKips * 1000).toLocaleString() + ' lbs)');
          setDisp('overburden_pressure_q', qOverburden.toFixed(1) + ' PSF');
        """
    },
    {
        "slug": "culvert-headwater-inlet-outlet",
        "category": "engineering",
        "name": "Highway Culvert Hydraulics (Inlet vs Outlet Control Headwater Depth)",
        "description": "Calculate culvert headwater depth (HW/D ratio), flow control regime (inlet control vs outlet control), and discharge capacity (FHWA HDS-5 standards).",
        "hero_badge": "Highway Drainage • Culvert Hydraulics",
        "formula_display": "Inlet Control HW/D = c · (Q / [A · √D])^Y - 0.5 · S | Allowable HW/D ≤ 1.2 to 1.5",
        "fields": [
            {"id": "culvert_flow_q_cfs", "label": "Design Peak Flow Rate (Q in CFS)", "default": 45.0, "suffix": "CFS", "min": 2, "max": 500, "step": 1, "hint": "10-year or 25-year design storm runoff"},
            {"id": "culvert_diameter_in", "label": "Culvert Inside Diameter (Inches)", "default": 36, "suffix": "in", "min": 12, "max": 96, "step": 6, "hint": "Circular pipe culvert diameter D"},
            {"id": "culvert_barrel_length_ft", "label": "Culvert Barrel Length (Feet)", "default": 65, "suffix": "ft", "min": 20, "max": 250, "step": 5, "hint": "Length under road embankment"}
        ],
        "metrics": [
            {"id": "headwater_depth_ft", "label": "Upstream Headwater Depth (HW)", "default_display": "3.85 Feet", "highlight": True},
            {"id": "headwater_to_diameter_ratio", "label": "Headwater Ratio (HW/D)", "default_display": "1.28 (Acceptable ≤ 1.5)", "highlight": True},
            {"id": "hydraulic_control_regime", "label": "Governing Hydraulic Regime", "default_display": "Inlet Control (Submerged Entrance)", "highlight": True},
            {"id": "culvert_barrel_velocity_fps", "label": "Barrel Flow Velocity", "default_display": "6.37 ft / second"}
        ],
        "proof_steps": [
            {"step_title": "FHWA HDS-5 Inlet Control Equations", "step_text": "Diameter D = 36\" = 3.0 ft. Pipe Area A = π · 1.5² = 7.07 sq ft."},
            {"step_title": "Specific Discharge Parameter", "step_text": "Q / (A · √D) = 45 / (7.07 × √3.0) = 45 / (7.07 × 1.732) = 45 / 12.245 = 3.675."},
            {"step_title": "Submerged Inlet Control Formulation", "step_text": "HW/D = c · [Q / (A·√D)]² + Y - 0.5S. For grooved concrete pipe: HW/D = 1.28."},
            {"step_title": "Headwater Elevation", "step_text": "HW = 1.28 × 3.0 ft = 3.84 ft. Because HW/D ≤ 1.5, the water level remains safely below the roadway shoulder without overtopping the pavement."}
        ],
        "faqs": [
            {"q": "What is the difference between Inlet Control and Outlet Control?", "a": "Inlet Control occurs when the culvert barrel can carry more water than the inlet opening can admit, so flow capacity is governed strictly by inlet geometry. Outlet Control occurs when tailwater, pipe friction, and barrel slope choke the flow, causing water to back up along the entire pipe length."},
            {"q": "What is the allowable HW/D ratio for highway culvert design?", "a": "State DOT standards generally limit Headwater-to-Diameter (HW/D) to 1.2 for secondary roads and 1.5 for primary highways to maintain minimum 2 feet of freeboard below the edge of the travel lane."}
        ],
        "js_logic": """
          const q = getNum('culvert_flow_q_cfs');
          const dIn = getNum('culvert_diameter_in');
          const l = getNum('culvert_barrel_length_ft');

          const dFt = dIn / 12;
          const a = Math.PI * Math.pow(dFt / 2, 2);
          const param = a > 0 && dFt > 0 ? (q / (a * Math.sqrt(dFt))) : 0;
          const hwd = 0.038 * Math.pow(param, 1.8) + 0.75;
          const hwFt = hwd * dFt;
          const v = a > 0 ? (q / a) : 0;

          setDisp('headwater_depth_ft', hwFt.toFixed(2) + ' Feet');
          setDisp('headwater_to_diameter_ratio', hwd.toFixed(2) + ' (HW/D)');
          setDisp('hydraulic_control_regime', hwd >= 1.2 ? 'Inlet Control (Submerged Entrance)' : 'Inlet Control (Unsubmerged Weir)');
          setDisp('culvert_barrel_velocity_fps', v.toFixed(2) + ' ft / second');
        """
    },
    {
        "slug": "detention-pond-settling-volume",
        "category": "engineering",
        "name": "Stormwater Detention Basin Storage Volume & Settling Inflow Calculator",
        "description": "Calculate required active flood retention storage volume (acre-feet and cubic feet) and orifice release diameter for post-development stormwater mitigation.",
        "hero_badge": "Water Resources • Stormwater Detention",
        "formula_display": "Storage Volume V_s = (Runoff Volume Post - Runoff Volume Pre) | Inflow Hydrograph Routing",
        "fields": [
            {"id": "post_development_peak_cfs", "label": "Post-Development Peak Runoff (Q_post in CFS)", "default": 42.0, "suffix": "CFS", "min": 5, "max": 500, "step": 1, "hint": "Unmitigated 25-year post-construction peak flow"},
            {"id": "pre_development_target_cfs", "label": "Pre-Development Allowable Discharge (Q_pre in CFS)", "default": 18.0, "suffix": "CFS", "min": 2, "max": 250, "step": 1, "hint": "Pre-existing natural pasture/forest peak discharge limit"},
            {"id": "storm_duration_hours", "label": "Design Storm Duration (Hours)", "default": 2.5, "suffix": "hours", "min": 1, "max": 24, "step": 0.5, "hint": "Critical duration for peak storage requirement"}
        ],
        "metrics": [
            {"id": "required_retention_storage_cuft", "label": "Required Active Storage Volume", "default_display": "108,000 cu ft", "highlight": True},
            {"id": "required_storage_acre_feet", "label": "Storage in Acre-Feet", "default_display": "2.48 Acre-Feet", "highlight": True},
            {"id": "pond_footprint_half_depth", "label": "Pond Water Surface Area (@ 4 ft depth)", "default_display": "27,000 sq ft (0.62 Acres)", "highlight": True},
            {"id": "discharge_reduction_pct", "label": "Peak Flow Attenuation", "default_display": "57.1% Flow Reduction"}
        ],
        "proof_steps": [
            {"step_title": "Peak Discharge Differential", "step_text": "ΔQ = Q_post - Q_pre = 42.0 CFS - 18.0 CFS = 24.0 CFS excess stormwater flow."},
            {"step_title": "Hydrograph Triangle Integration", "step_text": "Storage Volume V_s ≈ ½ · (Q_post - Q_pre) · Duration = ½ × 24 CFS × (2.5 hrs × 3,600s) = 12 × 9,000 = 108,000 cubic feet."},
            {"step_title": "Acre-Foot Conversion", "step_text": "1 Acre-Foot = 43,560 cubic feet. Required Volume = 108,000 / 43,560 = 2.479 Acre-Feet."},
            {"step_title": "Basin Footprint Geometry", "step_text": "At a standard 4-foot average design pond depth, required surface footprint = 108,000 / 4 = 27,000 sq ft (0.62 acres)."}
        ],
        "faqs": [
            {"q": "What is the difference between a Detention Basin and a Retention Basin?", "a": "A Detention Basin (dry pond) temporarily holds peak stormwater and drains completely dry between storms within 24 to 48 hours. A Retention Basin (wet pond) maintains a permanent pool of water year-round for biological pollutant removal."},
            {"q": "Why do municipalities require pre-development runoff matching?", "a": "Urbanization replaces permeable soil with impervious asphalt and rooftops, dramatically increasing runoff volume. Mandating that post-construction discharge match pre-development rates prevents downstream river flooding and streambank erosion."}
        ],
        "js_logic": """
          const qPost = getNum('post_development_peak_cfs');
          const qPre = getNum('pre_development_target_cfs');
          const hrs = getNum('storm_duration_hours') || 2.5;

          const deltaQ = Math.max(0, qPost - qPre);
          const cuft = 0.5 * deltaQ * (hrs * 3600);
          const acFt = cuft / 43560;
          const footprintSqft = cuft / 4;
          const reductionPct = qPost > 0 ? (deltaQ / qPost) * 100 : 0;

          setDisp('required_retention_storage_cuft', Math.round(cuft).toLocaleString() + ' cu ft');
          setDisp('required_storage_acre_feet', acFt.toFixed(2) + ' Acre-Feet');
          setDisp('pond_footprint_half_depth', Math.round(footprintSqft).toLocaleString() + ' sq ft (' + (footprintSqft / 43560).toFixed(2) + ' Ac)');
          setDisp('discharge_reduction_pct', reductionPct.toFixed(1) + '% Attenuation');
        """
    },
    {
        "slug": "truss-method-of-joints",
        "category": "engineering",
        "name": "Truss Member Axial Tension & Compression (Method of Joints) Calculator",
        "description": "Calculate internal axial forces (tension or compression in kips) in pin-jointed Pratt and Warren truss members using static equilibrium.",
        "hero_badge": "Structural Mechanics • Truss Statics",
        "formula_display": "Σ F_x = 0 | Σ F_y = 0 | T_member = P / (2 · sin(θ))",
        "fields": [
            {"id": "vertical_node_load_kips", "label": "Point Load at Center Joint (P in Kips)", "default": 24.0, "suffix": "kips", "min": 2, "max": 250, "step": 1, "hint": "Concentrated load applied at middle bottom chord node"},
            {"id": "truss_panel_span_ft", "label": "Truss Panel Length (Feet)", "default": 10.0, "suffix": "ft", "min": 3, "max": 40, "step": 1, "hint": "Horizontal distance between joints"},
            {"id": "truss_depth_height_ft", "label": "Truss Overall Height (Feet)", "default": 7.5, "suffix": "ft", "min": 2, "max": 30, "step": 0.5, "hint": "Vertical height between top and bottom chords"}
        ],
        "metrics": [
            {"id": "diagonal_member_force_kips", "label": "Diagonal Web Member Force", "default_display": "20.0 Kips (Tension)", "highlight": True},
            {"id": "top_chord_compression_kips", "label": "Top Chord Axial Compression", "default_display": "16.0 Kips (Compression)", "highlight": True},
            {"id": "end_reaction_force_kips", "label": "End Support Vertical Reaction", "default_display": "12.0 Kips Upward", "highlight": True},
            {"id": "web_angle_degrees", "label": "Diagonal Web Member Angle", "default_display": "36.9° Slope Angle"}
        ],
        "proof_steps": [
            {"step_title": "Global Support Equilibrium", "step_text": "By symmetry, left and right vertical support reactions R_y = P / 2 = 24.0 / 2 = 12.0 kips upward."},
            {"step_title": "Geometric Web Angle", "step_text": "θ = arctan(Height / Length) = arctan(7.5 / 10.0) = arctan(0.75) = 36.87°."},
            {"step_title": "Joint Equilibrium (Σ Fy = 0)", "step_text": "At end support joint: R_y - F_diag · sin(36.87°) = 0. F_diag = 12.0 / sin(36.87°) = 12.0 / 0.60 = 20.0 kips in Tension."},
            {"step_title": "Joint Equilibrium (Σ Fx = 0)", "step_text": "Top Chord Compression = F_diag · cos(36.87°) = 20.0 × 0.80 = 16.0 kips in Compression."}
        ],
        "faqs": [
            {"q": "What is the difference between Pratt and Howe trusses?", "a": "In a Pratt truss, the diagonal web members slope downward toward the center and are in tension under gravity loads. In a Howe truss, the diagonals slope upward toward the center and are in compression. Because steel excels in tension and bucking threatens compression, Pratt trusses are more efficient for steel designs."},
            {"q": "What is a zero-force member in a truss?", "a": "A zero-force member is a truss element that carries no theoretical axial force under a specific static loading condition, but provides essential lateral bracing to prevent buckling or carries load during shifting wind/seismic events."}
        ],
        "js_logic": """
          const p = getNum('vertical_node_load_kips');
          const l = getNum('truss_panel_span_ft');
          const h = getNum('truss_depth_height_ft');

          const ry = p / 2;
          const thetaRad = Math.atan(h / l);
          const thetaDeg = (thetaRad * 180) / Math.PI;

          const diagForce = ry / Math.sin(thetaRad);
          const chordForce = diagForce * Math.cos(thetaRad);

          setDisp('diagonal_member_force_kips', diagForce.toFixed(1) + ' Kips (Tension)');
          setDisp('top_chord_compression_kips', chordForce.toFixed(1) + ' Kips (Compression)');
          setDisp('end_reaction_force_kips', ry.toFixed(1) + ' Kips Upward');
          setDisp('web_angle_degrees', thetaDeg.toFixed(1) + '° Slope Angle');
        """
    },
    {
        "slug": "concrete-maturity-index",
        "category": "engineering",
        "name": "Concrete Curing Compressive Strength Maturity Index (Nurse-Saul Method)",
        "description": "Calculate Nurse-Saul Temperature-Time Maturity Index (TTF in °C-hours) to predict in-place concrete early compressive strength for formwork stripping (ASTM C1074).",
        "hero_badge": "Materials Engineering • Concrete Maturity",
        "formula_display": "Maturity M(t) = Σ (T_concrete - T_datum) · Δt | Datum Temp T₀ typically -10°C (14°F)",
        "fields": [
            {"id": "curing_duration_hours", "label": "Concrete Elapsed Curing Time (Hours)", "default": 72, "suffix": "hours (3 days)", "min": 6, "max": 672, "step": 6, "hint": "Time since concrete placement"},
            {"id": "avg_internal_concrete_temp_c", "label": "Internal Core Concrete Temp (°C)", "default": 28.0, "suffix": "°C", "min": 0, "max": 70, "step": 1, "hint": "Core temperature from embedded thermocouple sensor (e.g. 28°C = 82.4°F)"},
            {"id": "target_stripping_strength_psi", "label": "Required Formwork Stripping Strength (PSI)", "default": 3000, "suffix": "PSI", "min": 1500, "max": 6000, "step": 250, "hint": "Typically 70% to 75% of 28-day design strength (4,000 PSI)"}
        ],
        "metrics": [
            {"id": "maturity_index_c_hours", "label": "Nurse-Saul Maturity Index", "default_display": "2,736 °C-Hours", "highlight": True},
            {"id": "predicted_strength_psi", "label": "Predicted In-Place Strength", "default_display": "3,480 PSI", "highlight": True},
            {"id": "formwork_strip_ready", "label": "Formwork Stripping Status", "default_display": "SAFE TO STRIP FORMS (≥ 3,000 PSI)", "highlight": True},
            {"id": "pct_28day_design_strength", "label": "Percentage of 28-Day Strength", "default_display": "87.0% of 4,000 PSI"}
        ],
        "proof_steps": [
            {"step_title": "Nurse-Saul Temperature-Time Formulation", "step_text": "ASTM C1074 sets standard datum temperature T₀ = -10°C (temperature below which hydration stops). Effective Thermal Increment = T - T₀ = 28°C - (-10°C) = 38°C."},
            {"step_title": "Cumulative Maturity Calculation", "step_text": "Maturity Index = 38°C × 72 hours = 2,736 °C-hours."},
            {"step_title": "Logarithmic Strength Correlation", "step_text": "Using calibrated hyperbolic curve S = S_inf · [M / (k + M)]: At 2,736 °C-hours, in-place compressive strength reaches 3,480 PSI, satisfying the 3,000 PSI requirement to strip formwork 2 days ahead of schedule."}
        ],
        "faqs": [
            {"q": "What is the ASTM C1074 Maturity Method in concrete construction?", "a": "ASTM C1074 is a non-destructive testing method that uses embedded temperature sensors to continuously log concrete hydration heat, correlating real-time maturity index to laboratory calibration curves to determine exact in-place compressive strength."},
            {"q": "How does concrete maturity save money for commercial contractors?", "a": "Instead of waiting 7 to 14 days for traditional lab cylinder breaks, contractors verify in-place strength in 48 to 72 hours, allowing them to strip forms and post-tension slabs days earlier, accelerating high-rise construction cycles."}
        ],
        "js_logic": """
          const hrs = getNum('curing_duration_hours');
          const tC = getNum('avg_internal_concrete_temp_c');
          const reqPsi = getNum('target_stripping_strength_psi') || 3000;

          const datum = -10;
          const deltaT = Math.max(0, tC - datum);
          const maturity = deltaT * hrs;

          const strength = Math.min(4800, (4800 * maturity) / (1000 + maturity));
          const ready = strength >= reqPsi;

          setDisp('maturity_index_c_hours', Math.round(maturity).toLocaleString() + ' °C-Hours');
          setDisp('predicted_strength_psi', Math.round(strength).toLocaleString() + ' PSI');
          setDisp('formwork_strip_ready', ready ? 'SAFE TO STRIP FORMS (>= ' + reqPsi + ' PSI)' : 'HOLD FORMS (Insufficient Strength)');
          setDisp('pct_28day_design_strength', ((strength / 4000) * 100).toFixed(1) + '% of 4,000 PSI');
        """
    },
    {
        "slug": "water-hammer-joukowsky-surge",
        "category": "engineering",
        "name": "Water Hammer Joukowsky Shockwave Pressure Surge & Wave Speed Calculator",
        "description": "Calculate rapid valve closure acoustic pressure spike (Joukowsky equation ΔP = ρ·c·Δv) and acoustic wave speed in elastic pipe walls.",
        "hero_badge": "Fluid Transient Dynamics • Water Hammer",
        "formula_display": "Pressure Surge ΔP = ρ · c · Δv | Acoustic Wave Speed c = √[(K / ρ) / (1 + (K / E) · (D / t))]",
        "fields": [
            {"id": "steady_flow_velocity_fps", "label": "Initial Steady Water Velocity (v in ft/s)", "default": 8.0, "suffix": "ft/sec", "min": 1.0, "max": 25.0, "step": 0.5, "hint": "Normal operating velocity prior to valve shutoff"},
            {"id": "pipe_material_modulus", "label": "Pipe Material (1 = Carbon Steel, 2 = Ductile Iron, 3 = PVC Plastic)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1: Steel (c ≈ 3,800 fps), 2: Ductile Iron (c ≈ 3,500 fps), 3: PVC (c ≈ 1,200 fps)"},
            {"id": "valve_closure_time_sec", "label": "Valve Closure Duration (Seconds)", "default": 0.25, "suffix": "seconds", "min": 0.05, "max": 10.0, "step": 0.05, "hint": "Solenoid valve ~0.1-0.3s; quarter-turn ball valve ~0.5-1.0s"}
        ],
        "metrics": [
            {"id": "joukowsky_pressure_spike_psi", "label": "Peak Water Hammer Pressure Surge", "default_display": "411.0 PSI Spike", "highlight": True},
            {"id": "acoustic_wave_speed_fps", "label": "Acoustic Pressure Wave Speed (c)", "default_display": "3,820 ft / second", "highlight": True},
            {"id": "critical_closure_time_sec", "label": "Critical Sudden Closure Time (2L/c)", "default_display": "0.26 Seconds (1000 ft pipe)", "highlight": True},
            {"id": "surge_severity_grade", "label": "Pipe Burst Threat Assessment", "default_display": "Severe Transient (Water Hammer Arrestor Required)"}
        ],
        "proof_steps": [
            {"step_title": "Acoustic Wave Speed in Elastic Steel", "step_text": "Water bulk modulus K = 319,000 psi. In standard steel pipe, elasticity reduces wave speed from 4,860 fps (pure water) down to c = 3,820 ft/second."},
            {"step_title": "Joukowsky Momentum Equation", "step_text": "ΔP = (ρ · c · Δv) / 144g. Density of water ρ = 62.4 lb/cu ft. g = 32.174 ft/s²."},
            {"step_title": "Pressure Spike Evaluation", "step_text": "ΔP = (62.4 × 3,820 × 8.0) / (144 × 32.174) = 1,906,944 / 4,633 = 411.6 PSI pressure spike above baseline line pressure."},
            {"step_title": "Failure Prevention", "step_text": "A 411 PSI sudden surge instantly ruptures standard 150-PSI fittings, requiring mechanical water hammer arrestors or controlled motorized slow-closing actuators."}
        ],
        "faqs": [
            {"q": "What is the critical valve closure time (2L/c)?", "a": "If a valve closes faster than the time it takes the pressure wave to travel to the reservoir and reflect back (T_crit = 2L/c), maximum Joukowsky water hammer pressure develops. If closure time is significantly longer than 2L/c, the surge is substantially attenuated."},
            {"q": "Why do PVC pipes experience lower water hammer spikes than steel?", "a": "PVC is much more flexible (lower elastic modulus E) than steel. The flexible plastic pipe wall expands elastically to absorb the kinetic shockwave, reducing wave speed to ~1,200 fps and cutting the pressure spike to one-third of steel."}
        ],
        "js_logic": """
          const v = getNum('steady_flow_velocity_fps');
          const mat = Math.round(getNum('pipe_material_modulus')) || 1;
          const tClose = getNum('valve_closure_time_sec');

          let c = 3820; // steel
          if (mat === 2) c = 3500; // ductile iron
          else if (mat === 3) c = 1250; // PVC

          const rho = 62.4;
          const g = 32.174;
          const maxPsi = (rho * c * v) / (144 * g);

          const l = 500;
          const tCrit = (2 * l) / c;
          const actualPsi = tClose < tCrit ? maxPsi : maxPsi * (tCrit / tClose);

          setDisp('joukowsky_pressure_spike_psi', Math.round(actualPsi) + '.0 PSI Spike');
          setDisp('acoustic_wave_speed_fps', c.toLocaleString() + ' ft / second');
          setDisp('critical_closure_time_sec', (2 * 500 / c).toFixed(2) + ' Seconds (500 ft pipe)');
          setDisp('surge_severity_grade', actualPsi > 200 ? 'Severe (Water Hammer Arrestor Required)' : 'Moderate Controlled Surge');
        """
    },
    {
        "slug": "slope-stability-safety-factor",
        "category": "engineering",
        "name": "Soil Slope Stability Safety Factor (Ordinary / Bishop Method)",
        "description": "Calculate factor of safety against deep rotational circular slip failure in earthen embankments, highway cuts, and hillside slopes.",
        "hero_badge": "Geotechnical • Slope Stability",
        "formula_display": "Factor of Safety FS = Total Resisting Shear Strength / Total Driving Shear Stress | Target FS ≥ 1.50",
        "fields": [
            {"id": "slope_angle_degrees", "label": "Slope Inclination Angle (Degrees)", "default": 26.5, "suffix": "degrees (2:1 slope)", "min": 10, "max": 45, "step": 1, "hint": "2:1 slope = 26.6°; 3:1 slope = 18.4°; 1.5:1 slope = 33.7°"},
            {"id": "soil_internal_friction_phi", "label": "Internal Angle of Friction (ϕ Degrees)", "default": 30.0, "suffix": "degrees", "min": 15, "max": 42, "step": 1, "hint": "Drained soil friction angle"},
            {"id": "soil_cohesion_c_psf", "label": "Soil Effective Cohesion (c' in PSF)", "default": 200, "suffix": "PSF", "min": 0, "max": 1000, "step": 25, "hint": "Clay cohesion along slip arc"},
            {"id": "pore_water_pressure_ru", "label": "Pore Water Pressure Ratio (r_u)", "default": 0.15, "min": 0.0, "max": 0.50, "step": 0.05, "hint": "0.0 = Dry slope; 0.25 = Moderate seepage; 0.50 = Fully saturated slope"}
        ],
        "metrics": [
            {"id": "slope_safety_factor_fs", "label": "Calculated Factor of Safety (FS)", "default_display": "1.52 (Stable)", "highlight": True},
            {"id": "stability_classification", "label": "Slope Stability Condition", "default_display": "Stable Slope (Exceeds FS 1.50 Requirement)", "highlight": True},
            {"id": "friction_contribution_pct", "label": "Frictional Resistance Share", "default_display": "68.5% of Total Shear Resistance"},
            {"id": "pore_pressure_destabilization", "label": "Pore Water Strength Penalty", "default_display": "-22.5% Loss in Stability"}
        ],
        "proof_steps": [
            {"step_title": "Infinite Slope Simplified Formulation", "step_text": "FS = [c' / (γ · z · sin β · cos β)] + [tan ϕ' / tan β] · (1 - r_u · sec² β)."},
            {"step_title": "Resisting vs Driving Equilibrium", "step_text": "Driving shear stress = gravity component parallel to failure plane (sin β). Resisting shear strength = cohesion c' + effective normal stress (σ - u) · tan ϕ'."},
            {"step_title": "Pore Water Pressure Effect", "step_text": "Rising groundwater buoyancy reduces intergranular contact stress between soil particles, drastically reducing frictional shear resistance by 22.5%."},
            {"step_title": "Geotechnical Acceptance", "step_text": "With FS = 1.52, the engineered slope satisfies US Army Corps of Engineers and DOT requirements for permanent highway embankments (minimum FS ≥ 1.50)."}
        ],
        "faqs": [
            {"q": "What is the minimum required Factor of Safety for engineered slopes?", "a": "Standard civil engineering practice requires a minimum Factor of Safety of 1.50 for permanent slopes supporting structures, 1.30 for temporary construction cuts, and 1.10 under extreme seismic earthquake loading."},
            {"q": "Why do landslides usually occur during heavy rainfall?", "a": "Rainwater saturates pore spaces between soil grains, generating high positive pore water pressure (u) that acts like a hydraulic jack, lifting soil particles apart and eliminating frictional shear strength."}
        ],
        "js_logic": """
          const betaDeg = getNum('slope_angle_degrees') || 26.5;
          const phiDeg = getNum('soil_internal_friction_phi') || 30;
          const c = getNum('soil_cohesion_c_psf');
          const ru = getNum('pore_water_pressure_ru') || 0.15;

          const beta = (betaDeg * Math.PI) / 180;
          const phi = (phiDeg * Math.PI) / 180;

          const frictionTerm = (Math.tan(phi) / Math.tan(beta)) * (1 - ru / Math.pow(Math.cos(beta), 2));
          const cohesionTerm = c / (120 * 15 * Math.sin(beta) * Math.cos(beta));
          const fs = Math.max(0.5, frictionTerm + cohesionTerm);

          let status = 'Stable Slope (FS >= 1.50)';
          if (fs < 1.0) status = 'ACTIVE IMMINENT FAILURE (FS < 1.0)';
          else if (fs < 1.3) status = 'Marginally Stable (Warning: Prone to Failure)';
          else if (fs < 1.5) status = 'Adequate for Temporary Cut Only';

          setDisp('slope_safety_factor_fs', fs.toFixed(2));
          setDisp('stability_classification', status);
          setDisp('friction_contribution_pct', ((frictionTerm / fs) * 100).toFixed(1) + '% Frictional Resistance');
          setDisp('pore_pressure_destabilization', '-' + (ru * 100 * 1.5).toFixed(1) + '% Water Penalty');
        """
    },
    {
        "slug": "geotextile-roadbed-stabilization",
        "category": "engineering",
        "name": "Geotextile Fabric Tensile Modulus for Subgrade Stabilization Calculator",
        "description": "Calculate aggregate base reduction, subgrade California Bearing Ratio (CBR) reinforcement, and tensile modulus for roadbed geotextiles (FHWA design).",
        "hero_badge": "Geosynthetics • Highway Subgrades",
        "formula_display": "Aggregate Savings = H_unreinforced - H_reinforced (typically 20% to 35% gravel reduction)",
        "fields": [
            {"id": "subgrade_soil_cbr", "label": "Subgrade Soil Strength (CBR %)", "default": 2.0, "suffix": "% CBR", "min": 0.5, "max": 10.0, "step": 0.5, "hint": "Soft clay / saturated silt CBR ≤ 3.0 requires stabilization"},
            {"id": "design_axle_load_kips", "label": "Single Axle Wheel Load (P in Kips)", "default": 18.0, "suffix": "kips", "min": 8.0, "max": 40.0, "step": 2.0, "hint": "Standard 18-kip highway wheel load"},
            {"id": "gravel_cost_per_ton", "label": "Crushed Aggregate Base Cost ($/Ton)", "default": 28.0, "prefix": "$", "min": 10, "max": 65, "step": 2, "hint": "Delivered and compacted aggregate base"}
        ],
        "metrics": [
            {"id": "aggregate_thickness_saved_in", "label": "Gravel Base Thickness Saved", "default_display": "4.5 Inches Saved", "highlight": True},
            {"id": "dollar_savings_per_mile", "label": "Net Dollar Savings Per Lane-Mile", "default_display": "$38,400.00 / mile", "highlight": True},
            {"id": "geotextile_tensile_strength_req", "label": "Recommended Fabric Class", "default_display": "Class 1 Woven Geotextile (AASHTO M288)", "highlight": True},
            {"id": "rutting_prevention_status", "label": "Subgrade Pumping Mitigation", "default_display": "100% Intermixing Prevention"}
        ],
        "proof_steps": [
            {"step_title": "Unreinforced Gravel Thickness Requirement", "step_text": "Over weak CBR 2.0 subgrade, standard Giroud-Noiray design requires 15.0 inches of crushed stone to prevent deep wheel rutting."},
            {"step_title": "Geotextile Membrane Effect", "step_text": "Placing a high-modulus woven geotextile at the subgrade interface mobilizes tensile membrane support and spreads tire loads over a wider angle."},
            {"step_title": "Reinforced Thickness Reduction", "step_text": "Reinforced Aggregate Thickness = 10.5 inches (saving 4.5 inches of imported quarry aggregate)."},
            {"step_title": "Lane-Mile Economics", "step_text": "4.5 inches over a 12-ft wide lane = 1,466 tons of stone saved per mile ($41,048) minus $2,640 fabric cost = $38,408 net savings per lane-mile."}
        ],
        "faqs": [
            {"q": "How does a geotextile prevent subgrade pumping?", "a": "Under repeated heavy truck wheel loads, soft subgrade clay pumps upward into loose aggregate base voids, contaminating the gravel and causing structural collapse. A separation geotextile acts as an impermeable barrier to soil fines while allowing clean water drainage."},
            {"q": "What is the difference between woven and non-woven geotextiles?", "a": "Woven geotextiles offer high tensile strength and puncture resistance with low elongation, making them ideal for subgrade stabilization and base reinforcement. Non-woven (felt-like) geotextiles excel at filtration and subsurface drainage."}
        ],
        "js_logic": """
          const cbr = getNum('subgrade_soil_cbr');
          const p = getNum('design_axle_load_kips');
          const costTon = getNum('gravel_cost_per_ton');

          const unreinforcedIn = Math.max(6, (25 / Math.sqrt(Math.max(0.5, cbr))));
          const reinforcedIn = unreinforcedIn * 0.70;
          const savedIn = unreinforcedIn - reinforcedIn;

          const tonsSavedMile = (savedIn / 12) * 12 * 5280 * (135 / 2000);
          const grossGravelSaved = tonsSavedMile * costTon;
          const fabricCost = (12 * 5280 / 9) * 1.50; // $1.50/sq yd
          const netSavings = grossGravelSaved - fabricCost;

          setDisp('aggregate_thickness_saved_in', savedIn.toFixed(1) + ' Inches Saved');
          setDisp('dollar_savings_per_mile', '$' + Math.round(netSavings).toLocaleString() + ' / mile');
          setDisp('geotextile_tensile_strength_req', cbr < 2.0 ? 'Class 1 High-Modulus Woven' : 'Class 2 Woven Stabilization');
          setDisp('rutting_prevention_status', '100% Intermixing Separation');
        """
    },
    {
        "slug": "seismic-base-shear-asce7",
        "category": "engineering",
        "name": "Seismic Equivalent Lateral Force Base Shear Calculator (ASCE 7 / IBC)",
        "description": "Calculate total seismic design base shear (V = Cs · W) and seismic response coefficient (Cs) compliant with ASCE 7-16 and International Building Code.",
        "hero_badge": "Earthquake Engineering • Seismic Base Shear",
        "formula_display": "Base Shear V = Cs · W | Seismic Coefficient Cs = S_DS / (R / I_e)",
        "fields": [
            {"id": "effective_seismic_weight_kips", "label": "Total Effective Building Weight (W in Kips)", "default": 4500, "suffix": "kips", "min": 100, "max": 100000, "step": 250, "hint": "Total building dead load plus permanent partitions and 25% snow"},
            {"id": "spectral_acceleration_sds", "label": "Design Spectral Acceleration (S_DS)", "default": 0.85, "suffix": "g (gravity)", "min": 0.1, "max": 2.5, "step": 0.05, "hint": "Short-period design acceleration from USGS seismic maps"},
            {"id": "response_modification_r", "label": "Response Modification Factor (R)", "default": 6.5, "min": 1.5, "max": 8.0, "step": 0.5, "hint": "Ductile moment frame = 8.0; Braced frame = 6.0; Concrete shear wall = 5.0"},
            {"id": "importance_factor_ie", "label": "Seismic Importance Factor (I_e)", "default": 1.25, "min": 1.0, "max": 1.5, "step": 0.25, "hint": "Standard = 1.0; Schools/Assembly = 1.25; Hospitals/Emergency = 1.5"}
        ],
        "metrics": [
            {"id": "total_seismic_base_shear_kips", "label": "Total Seismic Design Base Shear (V)", "default_display": "735.6 Kips", "highlight": True},
            {"id": "seismic_response_coeff_cs", "label": "Seismic Coefficient (Cs)", "default_display": "0.1635 g", "highlight": True},
            {"id": "base_shear_weight_pct", "label": "Lateral Force as % of Building Weight", "default_display": "16.4% of Total Weight", "highlight": True},
            {"id": "seismic_design_category", "label": "Seismic Design Category (SDC)", "default_display": "Category D (High Seismic Risk)"}
        ],
        "proof_steps": [
            {"step_title": "Seismic Response Coefficient (Cs)", "step_text": "Cs = S_DS / (R / I_e) = 0.85 / (6.5 / 1.25) = 0.85 / 5.20 = 0.16346."},
            {"step_title": "Total Seismic Base Shear Formulation", "step_text": "V = Cs · W = 0.16346 × 4,500 kips = 735.58 kips."},
            {"step_title": "Lateral Load Resisting System Demand", "step_text": "Foundation and lateral shear walls must resist 735.6 kips of total horizontal ground acceleration shear force during the Maximum Considered Earthquake (MCE)."}
        ],
        "faqs": [
            {"q": "What is the Response Modification Factor R in seismic design?", "a": "Factor R represents a structural system's inherent ability to dissipate earthquake energy through ductile inelastic yielding (bending without snapping). A ductile steel moment frame has R=8.0, reducing required design forces by a factor of 8 compared to an elastic brittle structure."},
            {"q": "What is included in the effective seismic weight (W)?", "a": "Total building structural dead weight, plus permanent equipment, 25% of storage floor live load, total partition allowance (minimum 10 PSF), and 20% of design snow load if roof snow exceeds 30 PSF."}
        ],
        "js_logic": """
          const w = getNum('effective_seismic_weight_kips');
          const sds = getNum('spectral_acceleration_sds');
          const r = getNum('response_modification_r') || 6.5;
          const ie = getNum('importance_factor_ie') || 1.25;

          const cs = sds / (r / ie);
          const v = cs * w;
          const pct = cs * 100;

          let sdc = 'Category C (Moderate)';
          if (sds >= 0.50) sdc = 'Category D (High Seismic Zone)';
          else if (sds < 0.167) sdc = 'Category A (Low Seismic)';

          setDisp('total_seismic_base_shear_kips', v.toFixed(1) + ' Kips');
          setDisp('seismic_response_coeff_cs', cs.toFixed(4) + ' g');
          setDisp('base_shear_weight_pct', pct.toFixed(1) + '% of Building Weight');
          setDisp('seismic_design_category', sdc);
        """
    },
    {
        "slug": "wastewater-bod-aeration-tank",
        "category": "engineering",
        "name": "Wastewater BOD Removal Efficiency & Aeration Tank Sizing Calculator",
        "description": "Calculate municipal and industrial wastewater Biochemical Oxygen Demand (BOD₅) removal efficiency, hydraulic retention time (HRT), and aeration basin volume.",
        "hero_badge": "Environmental Engineering • Wastewater Treatment",
        "formula_display": "BOD Removal (%) = ([BOD_in - BOD_out] / BOD_in) × 100 | Volume = (Q × HRT) / 24",
        "fields": [
            {"id": "wastewater_inflow_mgd", "label": "Daily Wastewater Inflow (MGD)", "default": 2.5, "suffix": "MGD (Million Gal/Day)", "min": 0.1, "max": 100, "step": 0.5, "hint": "Municipal plant average daily design flow"},
            {"id": "influent_bod_mg_l", "label": "Influent Raw BOD₅ Concentration (mg/L)", "default": 240, "suffix": "mg/L", "min": 50, "max": 2000, "step": 10, "hint": "Typical municipal raw sewage = 200 - 300 mg/L"},
            {"id": "effluent_target_bod_mg_l", "label": "Target Effluent BOD₅ Limit (mg/L)", "default": 10, "suffix": "mg/L", "min": 2, "max": 50, "step": 1, "hint": "NPDES environmental discharge permit limit"},
            {"id": "hydraulic_retention_time_hrs", "label": "Hydraulic Retention Time (HRT in Hours)", "default": 6.5, "suffix": "hours", "min": 2, "max": 24, "step": 0.5, "hint": "Aeration basin contact time (standard = 4 - 8 hrs)"}
        ],
        "metrics": [
            {"id": "bod_removal_efficiency_pct", "label": "BOD₅ Removal Efficiency", "default_display": "95.8% Removal", "highlight": True},
            {"id": "aeration_tank_volume_gal", "label": "Required Aeration Basin Volume", "default_display": "677,083 Gallons", "highlight": True},
            {"id": "daily_bod_mass_removed_lbs", "label": "Daily Organic Mass Removed", "default_display": "4,795.5 lbs BOD / day", "highlight": True},
            {"id": "oxygen_demand_lbs_day", "label": "Biological Oxygen Delivery Demand", "default_display": "5,750 lbs O₂ / day"}
        ],
        "proof_steps": [
            {"step_title": "BOD Removal Efficiency", "step_text": "Efficiency = (Influent - Effluent) / Influent = (240 - 10) / 240 = 230 / 240 = 95.83% removal."},
            {"step_title": "Daily Organic Loading Mass", "step_text": "Daily BOD Mass = MGD × 8.34 × Concentration mg/L. Daily Influent = 2.5 MGD × 8.34 × 240 = 5,004 lbs BOD/day. Removed = 2.5 × 8.34 × 230 = 4,795.5 lbs/day."},
            {"step_title": "Aeration Basin Volumetric Sizing", "step_text": "Volume = Inflow MGD × (HRT / 24) = 2,500,000 gallons × (6.5 / 24) = 677,083 gallons (90,520 cubic feet)."}
        ],
        "faqs": [
            {"q": "What is Biochemical Oxygen Demand (BOD)?", "a": "BOD₅ measures the amount of dissolved oxygen consumed by aerobic microorganisms as they decompose organic matter in a water sample over a standardized 5-day incubation period at 20°C."},
            {"q": "What is MLSS in activated sludge aeration?", "a": "Mixed Liquor Suspended Solids (MLSS) represents the concentration of active microbial biomass (bacteria and protozoa) suspended in the aeration tank, maintained between 2,000 and 4,000 mg/L in conventional plants."}
        ],
        "js_logic": """
          const mgd = getNum('wastewater_inflow_mgd');
          const bodIn = getNum('influent_bod_mg_l');
          const bodOut = getNum('effluent_target_bod_mg_l');
          const hrt = getNum('hydraulic_retention_time_hrs') || 6.5;

          const eff = bodIn > 0 ? ((bodIn - bodOut) / bodIn) * 100 : 0;
          const tankGal = (mgd * 1000000) * (hrt / 24);
          const dailyLbsRemoved = mgd * 8.34 * (bodIn - bodOut);
          const o2Demand = dailyLbsRemoved * 1.2;

          setDisp('bod_removal_efficiency_pct', eff.toFixed(1) + '% Removal');
          setDisp('aeration_tank_volume_gal', Math.round(tankGal).toLocaleString() + ' Gallons');
          setDisp('daily_bod_mass_removed_lbs', Math.round(dailyLbsRemoved).toLocaleString() + ' lbs BOD / day');
          setDisp('oxygen_demand_lbs_day', Math.round(o2Demand).toLocaleString() + ' lbs O₂ / day');
        """
    },
    {
        "slug": "pile-axial-capacity-bearing",
        "category": "engineering",
        "name": "Deep Foundation Driven Pile Static Axial Skin Friction & End Bearing Capacity",
        "description": "Calculate ultimate and allowable axial compressive load capacity for driven steel H-piles and concrete friction piles (Q_ult = Q_skin + Q_tip).",
        "hero_badge": "Deep Foundations • Pile Dynamics",
        "formula_display": "Total Ultimate Capacity Q_ult = Skin Friction (Σ f_s · A_s) + End Bearing (q_p · A_p)",
        "fields": [
            {"id": "pile_embedded_depth_ft", "label": "Pile Penetration Depth (Feet)", "default": 45, "suffix": "ft", "min": 10, "max": 150, "step": 5, "hint": "Depth driven below ground surface"},
            {"id": "pile_perimeter_inches", "label": "Pile Cross-Section Perimeter (Inches)", "default": 48.0, "suffix": "in", "min": 12, "max": 120, "step": 2, "hint": "Outer perimeter for skin friction (e.g. 14\" square pile = 56 inches)"},
            {"id": "average_skin_friction_psf", "label": "Average Unit Skin Friction (f_s in PSF)", "default": 650, "suffix": "PSF", "min": 100, "max": 2500, "step": 50, "hint": "Unit adhesion/friction along pile shaft"},
            {"id": "unit_tip_bearing_psf", "label": "Unit End Bearing Capacity (q_p in PSF)", "default": 45000, "suffix": "PSF", "min": 5000, "max": 150000, "step": 2500, "hint": "End bearing on dense gravel or bedrock"}
        ],
        "metrics": [
            {"id": "allowable_pile_capacity_kips", "label": "Allowable Axial Pile Capacity (Q_all)", "default_display": "78.2 Kips (FS = 2.5)", "highlight": True},
            {"id": "ultimate_pile_capacity_kips", "label": "Total Ultimate Capacity (Q_ult)", "default_display": "195.5 Kips", "highlight": True},
            {"id": "shaft_skin_friction_kips", "label": "Shaft Skin Friction Contribution", "default_display": "117.0 Kips (60%)", "highlight": True},
            {"id": "tip_end_bearing_kips", "label": "Toe End Bearing Contribution", "default_display": "78.5 Kips (40%)"}
        ],
        "proof_steps": [
            {"step_title": "Shaft Surface Area", "step_text": "Shaft Area A_s = Perimeter (48\" / 12 = 4.0 ft) × Depth (45 ft) = 180.0 sq ft."},
            {"step_title": "Skin Friction Resistance", "step_text": "Q_skin = 180.0 sq ft × 650 PSF = 117,000 lbs = 117.0 kips."},
            {"step_title": "Tip End Bearing Resistance", "step_text": "Toe Area A_p = (12\" × 12\" / 144) = 1.74 sq ft. Q_tip = 1.74 sq ft × 45,000 PSF = 78,500 lbs = 78.5 kips."},
            {"step_title": "Allowable Working Load", "step_text": "Q_ult = 117.0 + 78.5 = 195.5 kips. Applying standard geotechnical safety factor FS = 2.5: Q_all = 195.5 / 2.5 = 78.2 kips (39.1 tons)."}
        ],
        "faqs": [
            {"q": "What is the difference between Friction Piles and End-Bearing Piles?", "a": "Friction piles derive the vast majority of their load capacity from shearing resistance along the embedded sides of the pile shaft in clay/sand. End-bearing piles pass through soft upper soils to rest their tip directly on unyielding dense bedrock or cemented hardpan."},
            {"q": "What is pile setup (freeze)?", "a": "During driving, soil pore water pressure spikes, temporarily reducing resistance. Over the next 24 to 72 hours, pore pressures dissipate and soil reconsolidates against the pile, significantly increasing load capacity (known as 'set-up' or freeze)."}
        ],
        "js_logic": """
          const depth = getNum('pile_embedded_depth_ft');
          const perimIn = getNum('pile_perimeter_inches');
          const fsPsf = getNum('average_skin_friction_psf');
          const qpPsf = getNum('unit_tip_bearing_psf');

          const perimFt = perimIn / 12;
          const shaftArea = perimFt * depth;
          const qSkinLbs = shaftArea * fsPsf;
          const qSkinKips = qSkinLbs / 1000;

          const sideFt = perimFt / 4;
          const tipArea = Math.pow(sideFt, 2);
          const qTipLbs = tipArea * qpPsf;
          const qTipKips = qTipLbs / 1000;

          const qUltKips = qSkinKips + qTipKips;
          const qAllKips = qUltKips / 2.5;

          setDisp('allowable_pile_capacity_kips', qAllKips.toFixed(1) + ' Kips (FS = 2.5)');
          setDisp('ultimate_pile_capacity_kips', qUltKips.toFixed(1) + ' Kips');
          setDisp('shaft_skin_friction_kips', qSkinKips.toFixed(1) + ' Kips (' + Math.round((qSkinKips / qUltKips) * 100) + '%)');
          setDisp('tip_end_bearing_kips', qTipKips.toFixed(1) + ' Kips (' + Math.round((qTipKips / qUltKips) * 100) + '%)');
        """
    },
    {
        "slug": "prestressed-concrete-elongation",
        "category": "engineering",
        "name": "Pre-Stressed Concrete Post-Tension Tendon Elongation & Friction Loss Calculator",
        "description": "Calculate theoretical tendon elongation (ΔL in inches), jack jacking force, and curvature wobble friction losses (PTI / ACI 318 standards).",
        "hero_badge": "Structural Concrete • Post-Tensioning",
        "formula_display": "Tendon Elongation ΔL = (P_avg · L) / (A_ps · E_ps) | Friction Loss P_x = P_0 · e^-(μα + Kx)",
        "fields": [
            {"id": "tendon_length_feet", "label": "Total Tendon Length (Feet)", "default": 120.0, "suffix": "ft", "min": 20, "max": 400, "step": 5, "hint": "Length between jacking anchorages"},
            {"id": "number_of_strands", "label": "Number of 0.5-inch 7-Wire Strands", "default": 4, "suffix": "strands", "min": 1, "max": 27, "step": 1, "hint": "Standard unbonded monostrand or bonded multi-strand tendon"},
            {"id": "initial_jacking_force_kips", "label": "Total Initial Jacking Force (kips)", "default": 133.2, "suffix": "kips (33.3 kips/strand)", "min": 20, "max": 1000, "step": 5, "hint": "80% of ultimate 270 ksi tensile strength"}
        ],
        "metrics": [
            {"id": "theoretical_elongation_inches", "label": "Theoretical Tendon Elongation", "default_display": "9.18 Inches", "highlight": True},
            {"id": "allowable_tolerance_range", "label": "Job-Site Acceptance Tolerance (±7%)", "default_display": "8.54\" to 9.82\" Range", "highlight": True},
            {"id": "friction_wobble_loss_kips", "label": "Friction & Wobble Force Loss", "default_display": "14.2 Kips Lost to Friction"},
            {"id": "average_prestress_force_kips", "label": "Effective Average Tendon Force", "default_display": "126.1 Kips"}
        ],
        "proof_steps": [
            {"step_title": "Strand Cross-Sectional Area", "step_text": "One 0.5-inch 270k strand = 0.153 sq inches. For 4 strands: A_ps = 4 × 0.153 = 0.612 sq inches."},
            {"step_title": "Average Effective Force Accounting for Friction", "step_text": "Due to angular curvature and wobble friction, jacking force decays along the tendon: P_avg ≈ Jacking Force × 0.947 = 133.2 × 0.947 = 126.14 kips."},
            {"step_title": "Hooke's Law Elastic Elongation", "step_text": "ΔL = (P_avg · L) / (A_ps · E_ps). L = 120 ft × 12 = 1,440 inches. E_ps = 28,500 ksi. ΔL = (126.14 × 1,440) / (0.612 × 28,500) = 181,641 / 17,442 = 10.41 inches."},
            {"step_title": "ACI Field Verification Mandate", "step_text": "ACI 318 Section 26.10 mandates measured field jack elongation must match theoretical calculations within ±7% (9.68\" to 11.14\") to verify lack of tendon binding."}
        ],
        "faqs": [
            {"q": "Why must post-tension tendon elongation be measured on site?", "a": "Measuring how many inches the hydraulic jack stretches the steel tendon provides direct physical proof that the engineered prestress force has traveled all the way through the concrete slab without pinching, kinking, or binding."},
            {"q": "What happens if measured elongation is outside ±7% tolerance?", "a": "If elongation is too short, the tendon bound up in the duct, leaving the concrete under-stressed (cracking hazard). If too long, the tendon may have slipped in the dead-end anchor or steel strands broke."}
        ],
        "js_logic": """
          const lFt = getNum('tendon_length_feet');
          const strands = getNum('number_of_strands');
          const pJack = getNum('initial_jacking_force_kips');

          const aps = strands * 0.153;
          const eps = 28500;
          const pAvg = pJack * 0.947;
          const lIn = lFt * 12;

          const deltaL = aps > 0 ? (pAvg * lIn) / (aps * eps) : 0;
          const lowTol = deltaL * 0.93;
          const highTol = deltaL * 1.07;
          const loss = pJack - pAvg;

          setDisp('theoretical_elongation_inches', deltaL.toFixed(2) + ' Inches');
          setDisp('allowable_tolerance_range', lowTol.toFixed(2) + '" to ' + highTol.toFixed(2) + '" (+-7%)');
          setDisp('friction_wobble_loss_kips', loss.toFixed(1) + ' Kips Friction Loss');
          setDisp('average_prestress_force_kips', pAvg.toFixed(1) + ' Kips');
        """
    },
    {
        "slug": "thermal-expansion-bridge-joints",
        "category": "engineering",
        "name": "Bridge Superstructure Thermal Expansion & Expansion Joint Sizing Calculator",
        "description": "Calculate total thermal movement (expansion and contraction ΔL in inches) and select bridge expansion joint seals (strip seal, modular joint) under AASHTO LRFD.",
        "hero_badge": "Bridge Engineering • Expansion Joints",
        "formula_display": "Thermal Movement ΔL = α · L · ΔT | Steel α = 6.5 × 10⁻⁶ /°F, Concrete α = 6.0 × 10⁻⁶ /°F",
        "fields": [
            {"id": "bridge_expansion_length_ft", "label": "Bridge Continuous Expansion Length (Feet)", "default": 350, "suffix": "ft", "min": 25, "max": 2500, "step": 25, "hint": "Distance from fixed bearing to expansion joint"},
            {"id": "superstructure_material", "label": "Superstructure Material (1 = Structural Steel, 2 = Prestressed Concrete)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1: Steel (α = 0.0000065/°F), 2: Concrete (α = 0.0000060/°F)"},
            {"id": "max_design_temp_f", "label": "Maximum Design Summer Temperature (°F)", "default": 110, "suffix": "°F", "min": 85, "max": 130, "step": 5, "hint": "AASHTO maximum bridge deck temperature"},
            {"id": "min_design_temp_f", "label": "Minimum Design Winter Temperature (°F)", "default": -10, "suffix": "°F", "min": -40, "max": 30, "step": 5, "hint": "AASHTO minimum bridge deck temperature"}
        ],
        "metrics": [
            {"id": "total_thermal_movement_in", "label": "Total Thermal Movement Range (ΔL)", "default_display": "3.28 Inches", "highlight": True},
            {"id": "recommended_joint_type", "label": "Recommended Expansion Joint", "default_display": "Strip Seal Joint (Up to 4.0\" movement)", "highlight": True},
            {"id": "effective_temperature_range", "label": "Design Temperature Range (ΔT)", "default_display": "120.0°F Range"},
            {"id": "installation_gap_at_60f", "label": "Target Setting Gap @ 60°F", "default_display": "1.91 Inches Setting Gap"}
        ],
        "proof_steps": [
            {"step_title": "Thermal Differential Range", "step_text": "ΔT = 110°F - (-10°F) = 120.0°F design thermal range."},
            {"step_title": "Thermal Elongation Equation", "step_text": "ΔL = α · L · ΔT. Length L = 350 ft × 12 = 4,200 inches. α_steel = 6.5 × 10⁻⁶ /°F."},
            {"step_title": "Total Movement Range", "step_text": "ΔL = 0.0000065 × 4,200\" × 120°F = 3.276 inches."},
            {"step_title": "Joint Hardware Selection", "step_text": "Because 3.28\" is under 4.0\", a single-cell elastomeric Strip Seal joint is specified. If movement exceeded 4.0\", a multi-cell modular expansion joint would be required."}
        ],
        "faqs": [
            {"q": "What happens if bridge expansion joints jam or freeze with debris?", "a": "When summer heat causes bridge girders to expand against a jammed joint, immense thermal stresses develop (over 10,000 PSI), crushing abutment backwalls, blowing out bridge bearings, and spalling concrete decks."},
            {"q": "Why is the setting gap adjusted based on installation temperature?", "a": "The joint cannot simply be installed at half-width. If installed on a cold 30°F winter day, the gap must be left wide open because the bridge will expand significantly come summer. If installed on a 90°F day, the gap must be set very narrow."}
        ],
        "js_logic": """
          const lFt = getNum('bridge_expansion_length_ft');
          const mat = Math.round(getNum('superstructure_material')) || 1;
          const tMax = getNum('max_design_temp_f');
          const tMin = getNum('min_design_temp_f');

          const deltaT = tMax - tMin;
          const alpha = mat === 1 ? 0.0000065 : 0.0000060;
          const lIn = lFt * 12;

          const deltaL = alpha * lIn * deltaT;
          const settingGap60 = deltaL * ((tMax - 60) / deltaT) + 0.5;

          let jointType = 'Strip Seal Joint (Up to 4.0")';
          if (deltaL > 4.0) jointType = 'Modular Expansion Joint (Multi-Cell)';
          else if (deltaL <= 1.75) jointType = 'Asphaltic Plug / Compression Seal';

          setDisp('total_thermal_movement_in', deltaL.toFixed(2) + ' Inches');
          setDisp('recommended_joint_type', jointType);
          setDisp('effective_temperature_range', deltaT.toFixed(1) + '°F Range');
          setDisp('installation_gap_at_60f', settingGap60.toFixed(2) + ' Inches Gap @ 60°F');
        """
    },
    {
        "slug": "highway-horizontal-curve-radius",
        "category": "engineering",
        "name": "Roadway Horizontal Alignment Minimum Curve Radius & Superelevation Calculator",
        "description": "Calculate minimum curve radius (R_min in feet), maximum design superelevation banking (e_max %), and side friction factors compliant with AASHTO Green Book.",
        "hero_badge": "Transportation • Highway Geometric Design",
        "formula_display": "R_min = V² / [15 · (0.01 · e_max + f_max)] | AASHTO Geometric Design Standard",
        "fields": [
            {"id": "highway_design_speed_mph", "label": "Design Travel Speed (V in mph)", "default": 65, "suffix": "mph", "min": 25, "max": 85, "step": 5, "hint": "Highway design speed (e.g. 65 mph freeway)"},
            {"id": "maximum_superelevation_rate", "label": "Maximum Superelevation Rate (e_max %)", "default": 6.0, "suffix": "%", "min": 4.0, "max": 10.0, "step": 1.0, "hint": "Standard rural highway: 6% or 8%; Ice/snow regions: 6%"},
            {"id": "side_friction_factor", "label": "Side Friction Factor (f_max)", "default": 0.11, "min": 0.08, "max": 0.18, "step": 0.01, "hint": "AASHTO Green Book comfort factor (0.11 at 65 mph, 0.15 at 40 mph)"}
        ],
        "metrics": [
            {"id": "minimum_radius_feet", "label": "Minimum Safe Horizontal Radius (R_min)", "default_display": "1,480 Feet", "highlight": True},
            {"id": "degree_of_curvature", "label": "Maximum Degree of Curve (D_max)", "default_display": "3.87° Curvature", "highlight": True},
            {"id": "curve_length_feet", "label": "Standard Curve Length (for 30° turn)", "default_display": "775 Feet Length"},
            {"id": "cross_slope_elevation_diff", "label": "Roadway Banking Lift (12-ft Lane)", "default_display": "8.6 Inches Banking Rise"}
        ],
        "proof_steps": [
            {"step_title": "Centrifugal Force Equilibrium", "step_text": "Centrifugal force pushing a car outward must be counterbalanced by pavement superelevation slope (e) and tire side friction (f): e + f = V² / (15 · R)."},
            {"step_title": "AASHTO Minimum Radius Derivation", "step_text": "R_min = V² / [15 · (0.01 · e + f)]. For V = 65 mph, e = 6.0%, and f = 0.11: R_min = 65² / [15 · (0.06 + 0.11)] = 4,225 / [15 · 0.17] = 4,225 / 2.55 = 1,657 feet."},
            {"step_title": "Degree of Curvature Formulation", "step_text": "Degree of Curve D = 5,729.58 / R = 5,729.58 / 1,657 = 3.46°."},
            {"step_title": "Superelevation Banking Elevation", "step_text": "Over a standard 12-foot travel lane at 6.0% slope: Outer edge of pavement is elevated by 12 ft × 0.06 = 0.72 ft = 8.64 inches above the centerline."}
        ],
        "faqs": [
            {"q": "What is Superelevation in highway engineering?", "a": "Superelevation is the lateral banking of a roadway curve, raising the outer edge of the pavement to use gravity to help vehicles turn safely without skidding off the road."},
            {"q": "Why is maximum superelevation capped at 6% or 8% in freezing climates?", "a": "If superelevation is too steep (e.g. 10% or 12%), slow-moving or stopped trucks on an icy highway will slide sideways down the banked slope into the inside ditch."}
        ],
        "js_logic": """
          const v = getNum('highway_design_speed_mph');
          const e = (getNum('maximum_superelevation_rate') || 6.0) / 100;
          const f = getNum('side_friction_factor') || 0.11;

          const denom = 15 * (e + f);
          const rMin = denom > 0 ? (Math.pow(v, 2) / denom) : 1000;
          const degCurve = rMin > 0 ? (5729.58 / rMin) : 0;
          const bankInches = 12 * e * 12;

          setDisp('minimum_radius_feet', Math.round(rMin).toLocaleString() + ' Feet');
          setDisp('degree_of_curvature', degCurve.toFixed(2) + '° Curvature');
          setDisp('curve_length_feet', Math.round(rMin * (30 * Math.PI / 180)) + ' Feet (for 30° Turn)');
          setDisp('cross_slope_elevation_diff', bankInches.toFixed(1) + ' Inches Banking Rise');
        """
    }
]
