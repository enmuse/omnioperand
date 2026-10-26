"""
scripts/data_batch3_gap_calculators.py
Data definitions for the 5 GSC high-intent gap calculators:
1. construction/polymeric-sand
2. construction/rafter-birdsmouth-cut
3. construction/gutter-downspout-sizing
4. engineering/three-phase-transformer-kva
5. finance/crypto-tax-hifo
"""

BATCH3_CALCULATORS = [
    # 1. Polymeric & Paver Joint Sand Estimator
    {
        'slug': 'construction/polymeric-sand',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Polymeric Sand & Paver Joint Calculator',
        'title': 'Polymeric Sand Calculator | Paver Joint & Bedding Sand Estimator | OmniOperand',
        'description': 'Calculate exact 50lb bags of polymeric sand and cubic yards of bedding sand for pavers, patio stones, and flagstone joints. Compliant with ICPI standards.',
        'hero_badge': 'Hardscape Engineering & Masonry • ICPI Tech Spec 9 Standard',
        'hero_subtext': 'Estimate polymeric joint sand bags (50-lb), joint volume, and 1-inch bedding sand base for concrete pavers, brick, and flagstone patios.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'patio_area_sqft', 'label': 'Total Patio / Walkway Area', 'type': 'number', 'default': 300, 'min': 10, 'max': 50000, 'step': 10, 'unit': 'sq ft', 'metric_unit': 'm²', 'hint': 'Total surface area to be paved'},
            {'id': 'paver_length_in', 'label': 'Paver Length (L)', 'type': 'number', 'default': 8, 'min': 2, 'max': 48, 'step': 0.25, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Length of individual paver unit'},
            {'id': 'paver_width_in', 'label': 'Paver Width (W)', 'type': 'number', 'default': 4, 'min': 2, 'max': 48, 'step': 0.25, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Width of individual paver unit'},
            {'id': 'paver_thick_in', 'label': 'Paver Thickness / Height', 'type': 'number', 'default': 2.375, 'min': 1, 'max': 6, 'step': 0.125, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Standard 60mm paver is 2-3/8" (2.375 in)'},
            {'id': 'joint_width_in', 'label': 'Average Joint Width', 'type': 'number', 'default': 0.25, 'min': 0.0625, 'max': 2, 'step': 0.0625, 'unit': 'in', 'metric_unit': 'mm', 'hint': '1/8" (0.125) for tight pavers; 1/4" to 1/2" for standard/flagstone'},
            {'id': 'joint_depth_in', 'label': 'Joint Depth Filled', 'type': 'number', 'default': 2.0, 'min': 0.5, 'max': 6, 'step': 0.125, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Leave 1/8" below paver chamfer edge'},
            {'id': 'waste_buffer_pct', 'label': 'Waste & Compaction Allowance', 'type': 'number', 'default': 10, 'min': 0, 'max': 25, 'step': 1, 'unit': '%', 'metric_unit': '%', 'hint': 'Industry standard is 10% for vibration settling and waste'}
        ],
        'outputs': [
            {'id': 'poly_sand_bags', 'label': '50-lb Polymeric Sand Bags Needed', 'unit': 'Bags', 'color': 'var(--accent-cyan)'},
            {'id': 'joint_volume_cuft', 'label': 'Total Joint Void Volume', 'unit': 'cu ft', 'color': 'var(--text-bright)'},
            {'id': 'total_sand_lbs', 'label': 'Total Sand Weight', 'unit': 'lbs (kg)', 'color': 'var(--accent-emerald)'},
            {'id': 'bedding_sand_cuyd', 'label': '1" Bedding Sand Base Needed', 'unit': 'cu yd (Tons)', 'color': 'var(--accent-purple)'},
            {'id': 'paver_unit_count', 'label': 'Estimated Paver Units Required', 'unit': 'Pavers', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'V_j = Area · [ 1 - (L · W) / ((L + W_j) · (W + W_j)) ] · (D_j / 12) | Bags = ⌈ (V_j · 100 lbs/cuft) / 50 ⌉',
        'proof_steps': [
            {'step_title': '1. Paver Unit Area & Joint Ratio', 'step_text': 'The effective footprint of a paver including its surrounding joint width is (L + W_j) × (W + W_j). The ratio of solid paver face area to total footprint establishes the joint surface percentage: Joint% = 1 - (L × W) / [(L + W_j) × (W + W_j)].'},
            {'step_title': '2. Joint Volume & Compaction Allowance', 'step_text': 'Multiplying the patio area by Joint% and effective joint depth gives raw joint volume: V_raw = Area × Joint% × (D_j / 12). Applying the ICPI 10% compaction buffer yields design volume: V_design = V_raw × (1 + Waste%).'},
            {'step_title': '3. Commercial Bag Weight & Bedding Base', 'step_text': 'Commercial polymeric sand has an installed bulk density of approx 100 lbs/cu ft (1,600 kg/m³). Dividing total weight by 50 lbs gives required bags. The underlying 1-inch (25 mm) ASTM C33 concrete sand bedding layer is computed independently: V_bed = (Area × 1/12) / 27 × 1.10 cubic yards.'}
        ],
        'faqs': [
            {'q': 'How many square feet does a 50 lb bag of polymeric sand cover?', 'a': 'For standard 4x8 inch pavers with tight 1/8" joints, a 50-lb bag covers approximately 60 to 85 sq ft. For wider 1/4" joints, coverage drops to 25 to 40 sq ft per bag.'},
            {'q': 'How deep should polymeric sand be in paver joints?', 'a': 'Polymeric sand must fill at least 1 inch or the full depth of the paver minus 1/8 inch below the chamfer (beveled edge). Filling above the chamfer causes surface hazing and joint degradation.'},
            {'q': 'Can you put polymeric sand over regular sand?', 'a': 'Yes, but the joints themselves must be cleared of regular sand to a depth of at least 1 to 1.5 inches to allow the polymeric polymers to bind into an impermeable composite matrix.'}
        ],
        'js_logic': """
          const area = getNum('patio_area_sqft') || 300;
          const l = getNum('paver_length_in') || 8;
          const w = getNum('paver_width_in') || 4;
          const th = getNum('paver_thick_in') || 2.375;
          const wj = getNum('joint_width_in') || 0.25;
          const dj = getNum('joint_depth_in') || 2.0;
          const waste = (getNum('waste_buffer_pct') || 10) / 100;
          
          const paverFaceSqFt = (l * w) / 144;
          const unitFootprintSqFt = ((l + wj) * (w + wj)) / 144;
          const jointFraction = 1 - (paverFaceSqFt / unitFootprintSqFt);
          const rawJointCuFt = area * jointFraction * (dj / 12);
          const designJointCuFt = rawJointCuFt * (1 + waste);
          const totalSandLbs = designJointCuFt * 100;
          const bags50lb = Math.ceil(totalSandLbs / 50);
          
          const paverCount = Math.ceil((area / paverFaceSqFt) * (1 + waste));
          const beddingCuYd = ((area * (1 / 12)) / 27) * (1 + waste);
          const beddingTons = beddingCuYd * 1.35;
          
          setDisp('poly_sand_bags', bags50lb + ' Bags (50-lb)');
          setDisp('joint_volume_cuft', fmt(designJointCuFt, 2) + ' cu ft');
          setDisp('total_sand_lbs', fmt(totalSandLbs, 0) + ' lbs (' + fmt(totalSandLbs * 0.453592, 0) + ' kg)');
          setDisp('bedding_sand_cuyd', fmt(beddingCuYd, 2) + ' cu yd (' + fmt(beddingTons, 1) + ' Tons)');
          setDisp('paver_unit_count', paverCount.toLocaleString() + ' Pavers');
        """
    },

    # 2. Rafter Length, Overhang & Birdsmouth Cut Calculator
    {
        'slug': 'construction/rafter-birdsmouth-cut',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Rafter Length & Birdsmouth Cut Calculator',
        'title': 'Rafter Length & Birdsmouth Cut Calculator | Roof Framing & Seat Cuts | OmniOperand',
        'description': 'Calculate common rafter length, plumb cuts, seat cut width, heel cut depth, and eave overhang with birdsmouth notch limits compliant with IRC R802.4.1.',
        'hero_badge': 'Carpentry & Timber Framing • IRC R802.4.1 Structural Code',
        'hero_subtext': 'Calculate true rafter line length, birdsmouth seat cut width, heel cut vertical plumb depth, overhang tail length, and bevel angles for roof framing.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'building_span_ft', 'label': 'Building Span (Wall-to-Wall)', 'type': 'number', 'default': 24, 'min': 4, 'max': 100, 'step': 0.5, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Total building out-to-out framing width'},
            {'id': 'roof_pitch_in', 'label': 'Roof Pitch (Rise per 12" Run)', 'type': 'number', 'default': 6, 'min': 1, 'max': 24, 'step': 0.5, 'unit': 'in/12', 'metric_unit': 'in/12', 'hint': 'e.g. 6/12 pitch = 26.57°'},
            {'id': 'rafter_depth_in', 'label': 'Rafter Timber Depth (Nominal Width)', 'type': 'number', 'default': 7.25, 'min': 3.5, 'max': 16, 'step': 0.25, 'unit': 'in', 'metric_unit': 'cm', 'hint': '2x6 is 5.5", 2x8 is 7.25", 2x10 is 9.25"'},
            {'id': 'wall_thickness_in', 'label': 'Wall Top Plate Width', 'type': 'number', 'default': 3.5, 'min': 3.5, 'max': 12, 'step': 0.5, 'unit': 'in', 'metric_unit': 'cm', 'hint': '2x4 wall top plate is 3.5"; 2x6 wall is 5.5"'},
            {'id': 'overhang_run_in', 'label': 'Eave Overhang Horizontal Run', 'type': 'number', 'default': 12, 'min': 0, 'max': 60, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Horizontal projection past outside of wall plate'},
            {'id': 'ridge_thick_in', 'label': 'Ridge Board Thickness', 'type': 'number', 'default': 1.5, 'min': 0, 'max': 6, 'step': 0.25, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Standard 2x dimensional ridge board is 1.5"'}
        ],
        'outputs': [
            {'id': 'line_length_ft_in', 'label': 'Rafter Line Length (Work Point to Work Point)', 'unit': 'ft & in', 'color': 'var(--accent-cyan)'},
            {'id': 'pitch_angle_deg', 'label': 'Plumb Cut & Miter Angle', 'unit': 'degrees', 'color': 'var(--text-bright)'},
            {'id': 'seat_cut_width', 'label': 'Birdsmouth Seat Cut (Bearing Width)', 'unit': 'inches', 'color': 'var(--accent-emerald)'},
            {'id': 'heel_cut_depth', 'label': 'Birdsmouth Heel Cut (Plumb Depth)', 'unit': 'inches (status)', 'color': 'var(--accent-purple)'},
            {'id': 'overhang_tail_len', 'label': 'Overhang Tail Rafter Length', 'unit': 'inches', 'color': 'var(--text-bright)'},
            {'id': 'min_stock_timber', 'label': 'Minimum Stock Lumber Board to Order', 'unit': 'standard ft', 'color': 'var(--accent-cyan)'}
        ],
        'formula_display': 'Run = (Span - Ridge) / 2 | L_line = Run · √[ 1 + (Pitch/12)² ] | HeelCut = Seat · (Pitch/12) ≤ Depth / 3',
        'proof_steps': [
            {'step_title': '1. Theoretical Horizontal Run', 'step_text': 'For a symmetrical gable roof, horizontal run is half the building span minus half the ridge board thickness: Run = (Span - Ridge / 12) / 2.'},
            {'step_title': '2. Pitch Hypotenuse Factor & True Line Length', 'step_text': 'Roof pitch angle is θ = arctan(Pitch / 12). The line length factor is sec(θ) = √[1 + (Pitch / 12)²]. The true rafter line length from ridge work point to wall plate work point is L_line = Run × sec(θ).'},
            {'step_title': '3. Birdsmouth Seat & Heel Cut IRC Limits', 'step_text': 'The horizontal seat cut rests on the wall plate (minimum 1.5 inches per IRC R802.4.1). For full plate bearing, Seat = WallThickness. The vertical plumb heel cut depth is H = Seat × (Pitch / 12). IRC R802.4.1 strictly prohibits notching rafters deeper than one-third of the lumber depth (H ≤ Depth / 3) to prevent shear split.'}
        ],
        'faqs': [
            {'q': 'What is the maximum depth for a birdsmouth cut?', 'a': 'According to International Residential Code (IRC R802.4.1), the maximum vertical depth of a birdsmouth heel cut cannot exceed one-third (1/3) of the rafter depth. For a 2x8 (7.25" actual), the maximum heel cut is 2.41 inches.'},
            {'q': 'What angle do I set my miter saw for roof rafters?', 'a': 'Set your saw angle to the plumb angle θ = arctan(Pitch/12). For example, a 4/12 pitch is 18.4°, a 6/12 pitch is 26.6°, an 8/12 pitch is 33.7°, and a 12/12 pitch is 45.0°.'},
            {'q': 'How do you measure rafter length with an overhang?', 'a': 'Total rafter board length equals the line length (from ridge cut to birdsmouth plumb line) PLUS the overhang tail length (from birdsmouth to fascia tail plumb cut) plus an allowance for square cuts.'}
        ],
        'js_logic': """
          const span = getNum('building_span_ft') || 24;
          const pitch = getNum('roof_pitch_in') || 6;
          const depth = getNum('rafter_depth_in') || 7.25;
          const wallThick = getNum('wall_thickness_in') || 3.5;
          const overhangIn = getNum('overhang_run_in') || 12;
          const ridgeThick = getNum('ridge_thick_in') || 1.5;
          
          const runFt = (span - (ridgeThick / 12)) / 2;
          const rad = Math.atan(pitch / 12);
          const deg = rad * (180 / Math.PI);
          const factor = Math.sqrt(1 + Math.pow(pitch / 12, 2));
          
          const lineLengthFt = runFt * factor;
          const lineFtWhole = Math.floor(lineLengthFt);
          const lineInchesRem = (lineLengthFt - lineFtWhole) * 12;
          
          const seatCut = wallThick;
          const heelCut = seatCut * (pitch / 12);
          const maxAllowedHeel = depth / 3;
          const heelCheck = heelCut <= maxAllowedHeel ? ' ✅ (IRC ≤ ' + fmt(maxAllowedHeel, 2) + ' in)' : ' ⚠️ Exceeds 1/3 depth limit (' + fmt(maxAllowedHeel, 2) + ' in)';
          
          const tailLenIn = overhangIn * factor;
          const totalLengthIn = (lineLengthFt * 12) + tailLenIn;
          const totalLengthFt = totalLengthIn / 12;
          
          const stdLumberSizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30];
          let recommendedStock = 32;
          for (const s of stdLumberSizes) {
            if (s >= totalLengthFt + 0.5) {
              recommendedStock = s;
              break;
            }
          }
          
          setDisp('line_rafter_length', lineFtWhole + ' ft ' + fmt(lineInchesRem, 2) + ' in (' + fmt(lineLengthFt, 3) + ' ft)');
          setDisp('pitch_angle_deg', fmt(deg, 2) + '° (Bevel: ' + fmt(90 - deg, 2) + '°)');
          setDisp('seat_cut_width', fmt(seatCut, 2) + ' in (Full Bearing)');
          setDisp('heel_cut_depth', fmt(heelCut, 2) + ' in' + heelCheck);
          setDisp('overhang_tail_len', fmt(tailLenIn, 2) + ' in (' + fmt(tailLenIn / 12, 2) + ' ft)');
          setDisp('min_stock_timber', recommendedStock + ' ft Board (Actual: ' + fmt(totalLengthFt, 2) + ' ft)');
        """
    },

    # 3. Roof Drainage, Gutter & Downspout Sizing Calculator
    {
        'slug': 'construction/gutter-downspout-sizing',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Gutter & Downspout Sizing Calculator',
        'title': 'Gutter & Downspout Sizing Calculator | Roof Drainage & Rainfall Flow | OmniOperand',
        'description': 'Size K-style and half-round gutters and rectangular/round downspouts from roof area, pitch factor, and rainfall intensity under SMACNA & IPC standards.',
        'hero_badge': 'Architectural Sheet Metal & Stormwater • SMACNA & IPC 1106 Standard',
        'hero_subtext': 'Calculate peak storm runoff flow rate (GPM), effective roof drainage area, recommended gutter width (5" or 6"), and downspout capacity under IPC Chapter 11.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'roof_length_ft', 'label': 'Gutter Run Length (L)', 'type': 'number', 'default': 50, 'min': 10, 'max': 300, 'step': 1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Horizontal length of eave with gutter'},
            {'id': 'roof_width_ft', 'label': 'Rafter Rake Width (W)', 'type': 'number', 'default': 20, 'min': 5, 'max': 150, 'step': 1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Distance from ridge to eave draining into this gutter'},
            {'id': 'roof_pitch', 'label': 'Roof Pitch (Slope)', 'type': 'select', 'default': '1.10', 'options': [
                ['1.00', 'Flat to 4/12 Pitch (Factor B = 1.00)'],
                ['1.10', '5/12 to 8/12 Pitch (Factor B = 1.10)'],
                ['1.20', '9/12 to 11/12 Pitch (Factor B = 1.20)'],
                ['1.30', '12/12 Pitch or Steeper (Factor B = 1.30)']
            ], 'hint': 'SMACNA wind-driven rain pitch multiplier'},
            {'id': 'rainfall_intensity_in_hr', 'label': 'Design Rainfall Intensity (I)', 'type': 'number', 'default': 4.0, 'min': 1.0, 'max': 10.0, 'step': 0.25, 'unit': 'in/hr', 'metric_unit': 'mm/hr', 'hint': '100-year 60-minute rainfall rate (typically 2.5 to 5.0 in/hr in US)'},
            {'id': 'downspout_count', 'label': 'Number of Downspouts Along Run', 'type': 'number', 'default': 2, 'min': 1, 'max': 10, 'step': 1, 'unit': 'outlets', 'metric_unit': 'outlets', 'hint': 'Spacing recommended at max 40 ft intervals'},
            {'id': 'gutter_profile', 'label': 'Gutter Profile Style', 'type': 'select', 'default': 'k_style', 'options': [
                ['k_style', 'K-Style Gutter (Ogee Profile • Higher Flow Capacity)'],
                ['half_round', 'Half-Round Gutter (Traditional Round Profile)']
            ], 'hint': 'Architectural gutter cross-section'}
        ],
        'outputs': [
            {'id': 'design_flow_gpm', 'label': 'Peak Design Runoff Rate', 'unit': 'GPM', 'color': 'var(--accent-cyan)'},
            {'id': 'effective_area_sqft', 'label': 'Adjusted Effective Drainage Area', 'unit': 'sq ft', 'color': 'var(--text-bright)'},
            {'id': 'recommended_gutter_size', 'label': 'Recommended Gutter Size', 'unit': 'profile inches', 'color': 'var(--accent-emerald)'},
            {'id': 'min_downspout_area_sqin', 'label': 'Required Area per Downspout', 'unit': 'sq in', 'color': 'var(--accent-purple)'},
            {'id': 'recommended_downspout_type', 'label': 'Standard Downspout Recommendation', 'unit': 'dimensions', 'color': 'var(--text-bright)'},
            {'id': 'total_gutter_capacity_gpm', 'label': 'Installed Gutter Flow Capacity', 'unit': 'GPM at 1/16" slope', 'color': 'var(--accent-cyan)'}
        ],
        'formula_display': 'A_eff = (L · W) · Factor_B | Q = A_eff · I · 0.01039 GPM | A_ds = (A_eff / N) · (I / 100)',
        'proof_steps': [
            {'step_title': '1. Effective Drainage Area Adjustment', 'step_text': 'Wind-driven rain strikes pitched roofs with greater effective cross-section. SMACNA applies pitch factor B to plan area: A_eff = (Length × Width) × Factor_B.'},
            {'step_title': '2. Peak Storm Runoff Flow Rate (GPM)', 'step_text': 'Converting rainfall intensity I (inches/hr) over A_eff gives volumetric flow: Q = A_eff × (I / 12 ft/hr) × (7.4805 gal/cu ft) / (60 min/hr) = A_eff × I × 0.010389 GPM.'},
            {'step_title': '3. Downspout & Gutter Sizing Thresholds', 'step_text': 'Under IPC Chapter 11 and SMACNA, each 2x3" rectangular downspout drains up to 600 sq ft at 4 in/hr (approx 25-30 GPM), while a 3x4" downspout drains up to 1,200 sq ft (approx 50-60 GPM). A 5-inch K-style gutter sloped at 1/16 inch per foot carries 45 GPM, whereas a 6-inch K-style carries 85 GPM.'}
        ],
        'faqs': [
            {'q': 'When should you use 6-inch gutters instead of 5-inch?', 'a': 'Upgrade to 6-inch gutters if your roof pitch is 8/12 or steeper, if the roof drainage area per gutter exceeds 600 to 800 sq ft, or if you live in a high-intensity rainfall zone exceeding 3.5 inches per hour.'},
            {'q': 'How many downspouts do I need for a 50 foot gutter?', 'a': 'SMACNA recommends at least one downspout for every 30 to 40 feet of gutter run. For a 50-foot gutter, 2 downspouts (one at each end or centered) are recommended to prevent mid-span overflow.'},
            {'q': 'What is the slope required for gutters?', 'a': 'Standard residential gutters must slope at least 1/16 inch to 1/8 inch per linear foot (approx 1 inch per 16 to 20 feet of gutter) toward the downspout outlet.'}
        ],
        'js_logic': """
          const l = getNum('roof_length_ft') || 50;
          const w = getNum('roof_width_ft') || 20;
          const pitchFactor = parseFloat(document.getElementById('param-roof_pitch').value) || 1.10;
          const intensity = getNum('rainfall_intensity_in_hr') || 4.0;
          const dsCount = getNum('downspout_count') || 2;
          const profile = document.getElementById('param-gutter_profile').value;
          
          const planArea = l * w;
          const effArea = planArea * pitchFactor;
          const q_gpm = effArea * intensity * 0.010389;
          
          const reqDsAreaPerOutlet = (effArea / dsCount) * (intensity / 100);
          
          let gutterSize = '5-Inch K-Style';
          let gutterCapacityGpm = 45;
          if (profile === 'k_style') {
            if (q_gpm > 85) {
              gutterSize = '7-Inch Commercial K-Style';
              gutterCapacityGpm = 135;
            } else if (q_gpm > 45) {
              gutterSize = '6-Inch K-Style (Recommended)';
              gutterCapacityGpm = 85;
            } else {
              gutterSize = '5-Inch K-Style (Standard)';
              gutterCapacityGpm = 45;
            }
          } else {
            if (q_gpm > 60) {
              gutterSize = '6-Inch Half-Round (High Flow)';
              gutterCapacityGpm = 65;
            } else {
              gutterSize = '5-Inch Half-Round';
              gutterCapacityGpm = 35;
            }
          }
          
          let dsRec = '2×3" Rectangular (or 3" Round)';
          if (reqDsAreaPerOutlet > 11.5) {
            dsRec = '4×5" Commercial Rectangular (or 5" Round)';
          } else if (reqDsAreaPerOutlet > 5.7) {
            dsRec = '3×4" Rectangular (or 4" Round)';
          }
          
          setDisp('design_flow_gpm', fmt(q_gpm, 1) + ' GPM (' + fmt(q_gpm * 3.78541, 1) + ' L/min)');
          setDisp('effective_area_sqft', fmt(effArea, 0) + ' sq ft (Plan: ' + fmt(planArea, 0) + ' sq ft)');
          setDisp('recommended_gutter_size', gutterSize);
          setDisp('min_downspout_area_sqin', fmt(reqDsAreaPerOutlet, 2) + ' sq in / outlet');
          setDisp('recommended_downspout_type', dsRec);
          setDisp('total_gutter_capacity_gpm', gutterCapacityGpm + ' GPM (' + (gutterCapacityGpm >= q_gpm ? '✅ Adequate Capacity' : '⚠️ Potential Overflow') + ')');
        """
    },

    # 4. 3-Phase Electrical Transformer kVA & Amperage Calculator
    {
        'slug': 'engineering/three-phase-transformer-kva',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': '3-Phase Transformer kVA & Amps Calculator',
        'title': '3-Phase Transformer kVA Calculator | Full-Load Current & Sizing | OmniOperand',
        'description': 'Calculate 3-phase transformer apparent power (kVA), primary and secondary full-load amperes (FLA), and standard kVA ratings compliant with NEC 450.',
        'hero_badge': 'Electrical Power Systems • NEC 450 & IEEE C57.12 Standard',
        'hero_subtext': 'Calculate 3-phase apparent power (kVA), primary/secondary full-load amperes (FLA), NEC 450 standard rating selection, and core/winding losses.',
        'has_dual_units': False,
        'governing_jurisdiction': 'NEC (NFPA 70)',
        'inputs': [
            {'id': 'primary_voltage_v', 'label': 'Primary Line-to-Line Voltage (V1)', 'type': 'select', 'default': '480', 'options': [
                ['208', '208 V (3-Phase Delta / Wye)'],
                ['240', '240 V (3-Phase Delta)'],
                ['480', '480 V (Standard Industrial High Voltage)'],
                ['600', '600 V (Canadian Industrial Standard)'],
                ['2400', '2,400 V (Medium Voltage Distribution)'],
                ['4160', '4,160 V (Medium Voltage Industrial)'],
                ['13800', '13,800 V (13.8 kV Substation Feed)']
            ], 'hint': 'Primary utility or supply voltage'},
            {'id': 'secondary_voltage_v', 'label': 'Secondary Line-to-Line Voltage (V2)', 'type': 'select', 'default': '208', 'options': [
                ['208', '120/208 V (Commercial Lighting & Receptacle Wye)'],
                ['240', '240 V (Commercial / Industrial Delta)'],
                ['480', '277/480 V (Industrial Motor & High-Bay Wye)'],
                ['600', '600 V (Heavy Manufacturing Wye)']
            ], 'hint': 'Secondary utilization voltage feeding the load panel'},
            {'id': 'load_kw', 'label': 'Connected Active Load (kW)', 'type': 'number', 'default': 60, 'min': 1, 'max': 5000, 'step': 5, 'unit': 'kW', 'hint': 'Total real power demand of connected equipment'},
            {'id': 'power_factor', 'label': 'Load Power Factor (cos θ)', 'type': 'number', 'default': 0.85, 'min': 0.5, 'max': 1.0, 'step': 0.05, 'unit': 'PF', 'hint': 'Inductive motor load typically 0.80 - 0.85; resistive is 1.0'},
            {'id': 'safety_margin_pct', 'label': 'Continuous Duty & Growth Margin', 'type': 'number', 'default': 25, 'min': 0, 'max': 50, 'step': 5, 'unit': '%', 'hint': 'NEC Article 215/450 requires 125% factor for continuous duty'}
        ],
        'outputs': [
            {'id': 'calculated_demand_kva', 'label': 'Operating Load Demand (kVA)', 'unit': 'kVA', 'color': 'var(--accent-cyan)'},
            {'id': 'standard_nec_kva', 'label': 'Standard NEC Transformer Size', 'unit': 'kVA (Rating)', 'color': 'var(--accent-emerald)'},
            {'id': 'primary_fla', 'label': 'Primary Full-Load Amperes (FLA)', 'unit': 'Amperes', 'color': 'var(--text-bright)'},
            {'id': 'secondary_fla', 'label': 'Secondary Full-Load Amperes (FLA)', 'unit': 'Amperes', 'color': 'var(--accent-purple)'},
            {'id': 'loss_heat_kw', 'label': 'Full-Load Heat Loss Dissipation', 'unit': 'kW (BTU/hr)', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'kVA = kW / PF | FLA = (kVA · 1,000) / (√3 · V_LL) | P_heat ≈ kVA · 0.015',
        'proof_steps': [
            {'step_title': '1. Apparent Power from Active Load', 'step_text': 'In AC systems, apparent power S (in kVA) accounts for reactive currents: S_load = P_kW / PowerFactor. Applying the continuous duty safety margin gives design capacity: S_design = S_load × (1 + Margin%).'},
            {'step_title': '2. Three-Phase Voltage & Current Relation', 'step_text': 'For a balanced 3-phase system, apparent power is S = √3 × V_LL × I_line. Inverting for full-load amperes yields: FLA = (kVA × 1,000) / (√3 × V_LL), where √3 ≈ 1.7320508.'},
            {'step_title': '3. NEC Standard Rating Selection & Heat Dissipation', 'step_text': 'Commercial dry-type transformers follow standard NEMA/NEC step ratings: 15, 30, 45, 75, 112.5, 150, 225, 300, 500 kVA. Core hysteresis and I²R winding resistance dissipate approx 1.5% to 2.5% of rated capacity as heat under full load.'}
        ],
        'faqs': [
            {'q': 'What is the formula to calculate 3-phase kVA to Amps?', 'a': 'To find Amps from 3-phase kVA: Amps = (kVA × 1,000) / (1.732 × Voltage). For example, a 75 kVA transformer at 208V delivers: (75 × 1,000) / (1.732 × 208) = 208.2 Amperes.'},
            {'q': 'Why is square root of 3 (1.732) used in three-phase calculations?', 'a': 'In a 3-phase system, the line-to-line voltage is vectorially 120° out of phase with line-to-neutral voltage. The geometric vector difference between any two phases is 2 × sin(60°) = √3 ≈ 1.732.'},
            {'q': 'What size transformer do I need for a 100 kW load?', 'a': 'Assuming an 0.85 power factor, 100 kW equals 117.6 kVA. Adding a 25% continuous duty factor requires 147 kVA. The nearest standard commercial transformer rating is 150 kVA.'}
        ],
        'js_logic': """
          const v1 = parseFloat(document.getElementById('param-primary_voltage_v').value) || 480;
          const v2 = parseFloat(document.getElementById('param-secondary_voltage_v').value) || 208;
          const kw = getNum('load_kw') || 60;
          const pf = getNum('power_factor') || 0.85;
          const margin = (getNum('safety_margin_pct') || 25) / 100;
          
          const rawKva = kw / pf;
          const designKva = rawKva * (1 + margin);
          
          const stdKvaList = [15, 30, 45, 75, 112.5, 150, 225, 300, 500, 750, 1000, 1500, 2000, 2500];
          let selectedKva = 3000;
          for (const s of stdKvaList) {
            if (s >= designKva) {
              selectedKva = s;
              break;
            }
          }
          
          const sqrt3 = Math.sqrt(3);
          const priFla = (selectedKva * 1000) / (sqrt3 * v1);
          const secFla = (selectedKva * 1000) / (sqrt3 * v2);
          const heatLossKw = selectedKva * 0.016;
          const heatBtuHr = heatLossKw * 3412.14;
          
          setDisp('calculated_demand_kva', fmt(rawKva, 1) + ' kVA (Design: ' + fmt(designKva, 1) + ' kVA)');
          setDisp('standard_nec_kva', selectedKva + ' kVA Standard Unit');
          setDisp('primary_fla', fmt(priFla, 1) + ' A (at ' + v1 + 'V)');
          setDisp('secondary_fla', fmt(secFla, 1) + ' A (at ' + v2 + 'V)');
          setDisp('loss_heat_kw', fmt(heatLossKw, 2) + ' kW (' + fmt(heatBtuHr, 0) + ' BTU/hr)');
        """
    },

    # 5. Cryptocurrency Capital Gains & HIFO Tax Calculator
    {
        'slug': 'finance/crypto-tax-hifo',
        'category': 'finance',
        'cluster': 'finance',
        'name': 'Crypto Capital Gains & HIFO Tax Calculator',
        'title': 'Crypto Tax & HIFO Calculator | Highest-In First-Out vs FIFO Gains | OmniOperand',
        'description': 'Compare HIFO, FIFO, and LIFO cost basis accounting methods for cryptocurrency sales to minimize IRS capital gains tax and optimize tax-loss harvesting.',
        'hero_badge': 'Tax Accounting & Digital Assets • IRS Notice 2014-21 & Rev. Rul. 2019-24',
        'hero_subtext': 'Compare HIFO (Highest-In, First-Out), FIFO (First-In, First-Out), and LIFO accounting methods to minimize cryptocurrency capital gains taxes.',
        'has_dual_units': False,
        'governing_jurisdiction': 'IRS (United States)',
        'inputs': [
            {'id': 'disposal_amount', 'label': 'Crypto Amount Sold / Disposed', 'type': 'number', 'default': 1.5, 'min': 0.001, 'max': 10000, 'step': 0.1, 'unit': 'Units', 'hint': 'Total Bitcoin, ETH, or token units sold'},
            {'id': 'sale_price_usd', 'label': 'Current Sale Price per Unit', 'type': 'number', 'default': 65000, 'min': 1, 'max': 1000000, 'step': 500, 'unit': '$ / unit', 'hint': 'Gross price realized at execution'},
            {'id': 'lot1_units', 'label': 'Lot 1: Units Owned', 'type': 'number', 'default': 0.5, 'min': 0, 'max': 1000, 'step': 0.1, 'unit': 'Units', 'hint': 'Earliest acquisition lot'},
            {'id': 'lot1_price', 'label': 'Lot 1: Cost Basis per Unit', 'type': 'number', 'default': 30000, 'min': 1, 'max': 1000000, 'step': 500, 'unit': '$ / unit', 'hint': 'Purchase price of Lot 1'},
            {'id': 'lot1_days', 'label': 'Lot 1: Holding Period (Days)', 'type': 'number', 'default': 420, 'min': 1, 'max': 3000, 'step': 10, 'unit': 'Days', 'hint': '>365 days qualifies for Long-Term Capital Gains'},
            {'id': 'lot2_units', 'label': 'Lot 2: Units Owned', 'type': 'number', 'default': 0.5, 'min': 0, 'max': 1000, 'step': 0.1, 'unit': 'Units', 'hint': 'Second purchase lot'},
            {'id': 'lot2_price', 'label': 'Lot 2: Cost Basis per Unit', 'type': 'number', 'default': 68000, 'min': 1, 'max': 1000000, 'step': 500, 'unit': '$ / unit', 'hint': 'Purchased near recent peak'},
            {'id': 'lot2_days', 'label': 'Lot 2: Holding Period (Days)', 'type': 'number', 'default': 180, 'min': 1, 'max': 3000, 'step': 10, 'unit': 'Days', 'hint': '<365 days = Short-Term Ordinary Income Tax'},
            {'id': 'lot3_units', 'label': 'Lot 3: Units Owned', 'type': 'number', 'default': 0.5, 'min': 0, 'max': 1000, 'step': 0.1, 'unit': 'Units', 'hint': 'Third purchase lot'},
            {'id': 'lot3_price', 'label': 'Lot 3: Cost Basis per Unit', 'type': 'number', 'default': 45000, 'min': 1, 'max': 1000000, 'step': 500, 'unit': '$ / unit', 'hint': 'Purchase price of Lot 3'},
            {'id': 'lot3_days', 'label': 'Lot 3: Holding Period (Days)', 'type': 'number', 'default': 390, 'min': 1, 'max': 3000, 'step': 10, 'unit': 'Days', 'hint': '>365 days = Long-Term Capital Gains'},
            {'id': 'ordinary_tax_rate', 'label': 'Federal Ordinary Income Tax Rate', 'type': 'number', 'default': 32, 'min': 10, 'max': 45, 'step': 1, 'unit': '%', 'hint': 'Marginal tax bracket applied to short-term gains'},
            {'id': 'lt_cap_gains_rate', 'label': 'Long-Term Capital Gains Tax Rate', 'type': 'number', 'default': 15, 'min': 0, 'max': 25, 'step': 1, 'unit': '%', 'hint': '0%, 15%, or 20% (+3.8% NIIT if applicable)'}
        ],
        'outputs': [
            {'id': 'hifo_taxable_gain', 'label': 'Taxable Capital Gain (HIFO Method)', 'unit': 'USD ($)', 'color': 'var(--accent-cyan)'},
            {'id': 'fifo_taxable_gain', 'label': 'Taxable Capital Gain (FIFO Method)', 'unit': 'USD ($)', 'color': 'var(--text-bright)'},
            {'id': 'tax_savings_hifo', 'label': 'Immediate Tax Savings with HIFO', 'unit': 'USD ($)', 'color': 'var(--accent-emerald)'},
            {'id': 'hifo_tax_owed', 'label': 'Estimated Tax Liability (HIFO)', 'unit': 'USD ($)', 'color': 'var(--text-bright)'},
            {'id': 'fifo_tax_owed', 'label': 'Estimated Tax Liability (FIFO)', 'unit': 'USD ($)', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'Proceeds = Units · P_sale | Gain = Proceeds - CostBasis | HIFO sorts by max(CostBasis) | Tax = (ST_Gain · Rate_ord) + (LT_Gain · Rate_lt)',
        'proof_steps': [
            {'step_title': '1. IRS Specific Identification Guidance', 'step_text': 'Under IRS Revenue Ruling 2019-24, cryptocurrency investors who maintain detailed records (transaction IDs, timestamps, cost basis) are legally permitted to use Specific Identification, including HIFO (Highest-In, First-Out).'},
            {'step_title': '2. HIFO vs FIFO Tax Mechanics', 'step_text': 'FIFO (First-In, First-Out) assumes the earliest coins acquired are sold first, which typically results in the lowest cost basis and largest taxable capital gain. HIFO matches sales against the highest acquisition prices first, immediately maximizing cost basis deductions and generating tax-loss harvesting benefits.'},
            {'step_title': '3. Holding Period Bifurcation', 'step_text': 'Assets held 365 days or less are classified as short-term capital gains and taxed as ordinary income (up to 37% federal). Assets held greater than 365 days receive preferential long-term capital gains tax rates (0%, 15%, or 20%).'}
        ],
        'faqs': [
            {'q': 'Is HIFO legal according to the IRS for cryptocurrency?', 'a': 'Yes. Under IRS Notice 2014-21 and FAQ 39-41, taxpayers can use specific identification (including HIFO) if they can document the date/time acquired, cost basis, fair market value, and wallet address of each lot.'},
            {'q': 'Why is HIFO better than FIFO for crypto taxes?', 'a': 'HIFO sells your highest-priced purchases first. This minimizes your net taxable gain in the current year, and can even trigger legal capital losses (up to $3,000 per year against ordinary income) to lower your tax bill.'},
            {'q': 'Can you switch between FIFO and HIFO?', 'a': 'You can select specific identification on each individual sale transaction as long as you maintain consistent cryptographic accounting records and avoid double-counting previously sold lots.'}
        ],
        'js_logic': """
          const sellUnits = getNum('disposal_amount') || 1.5;
          const salePrice = getNum('sale_price_usd') || 65000;
          const ordRate = (getNum('ordinary_tax_rate') || 32) / 100;
          const ltRate = (getNum('lt_cap_gains_rate') || 15) / 100;
          
          const lots = [
            { id: 1, units: getNum('lot1_units') || 0.5, price: getNum('lot1_price') || 30000, days: getNum('lot1_days') || 420 },
            { id: 2, units: getNum('lot2_units') || 0.5, price: getNum('lot2_price') || 68000, days: getNum('lot2_days') || 180 },
            { id: 3, units: getNum('lot3_units') || 0.5, price: getNum('lot3_price') || 45000, days: getNum('lot3_days') || 390 }
          ];
          
          function calculateGains(sortedLots) {
            let remSell = sellUnits;
            let stGain = 0;
            let ltGain = 0;
            let totalGain = 0;
            
            for (const lot of sortedLots) {
              if (remSell <= 0) break;
              const used = Math.min(remSell, lot.units);
              const gain = used * (salePrice - lot.price);
              totalGain += gain;
              if (lot.days > 365) {
                ltGain += gain;
              } else {
                stGain += gain;
              }
              remSell -= used;
            }
            
            const tax = (Math.max(0, stGain) * ordRate) + (Math.max(0, ltGain) * ltRate);
            return { totalGain, stGain, ltGain, tax };
          }
          
          const fifoLots = [...lots];
          const hifoLots = [...lots].sort((a, b) => b.price - a.price);
          
          const fifo = calculateGains(fifoLots);
          const hifo = calculateGains(hifoLots);
          const savings = Math.max(0, fifo.tax - hifo.tax);
          
          setDisp('hifo_taxable_gain', '$' + fmt(hifo.totalGain, 2) + (hifo.totalGain < 0 ? ' (Capital Loss Harvested)' : ''));
          setDisp('fifo_taxable_gain', '$' + fmt(fifo.totalGain, 2));
          setDisp('tax_savings_hifo', '$' + fmt(savings, 2) + ' Saved');
          setDisp('hifo_tax_owed', '$' + fmt(hifo.tax, 2));
          setDisp('fifo_tax_owed', '$' + fmt(fifo.tax, 2));
        """
    }
]
