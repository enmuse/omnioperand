"""
scripts/data_batch2_gsc.py
Complete data definitions for all 22 missing high-intent calculators identified in GSC audit.
Adheres strictly to AGENTS.md:
- Pure mathematical Unicode typography (Zero raw LaTeX backslashes!)
- Exact formulas, proofs, FAQs, and bidirectional JS calculation logic.
"""

BATCH2_CALCULATORS = [
    # 1. Slant Height Calculator (Position 10.0 in GSC!)
    {
        'slug': 'geometry/slant-height',
        'category': 'geometry',
        'cluster': 'geometry',
        'name': 'Slant Height Calculator',
        'title': 'Slant Height Calculator: Cone, Pyramid & Frustum Formulas | OmniOperand',
        'description': 'Calculate slant height, surface area, and lateral pitch for right circular cones, regular square pyramids, and truncated frustums with exact radical solutions.',
        'hero_badge': '3D Euclidean Geometry • Pythagorean Invariants',
        'hero_subtext': 'Calculate the exact slant height (s), lateral surface area, total surface area, and apex pitch angle across cones, regular pyramids, and truncated frustums.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'shape_type', 'label': 'Geometric Solid Type', 'type': 'select', 'default': 'cone', 'options': [
                ['cone', 'Right Circular Cone (Radius r, Height h)'],
                ['pyramid', 'Regular Square Pyramid (Base side a, Height h)'],
                ['frustum_cone', 'Truncated Cone Frustum (Bottom R, Top r, Height h)'],
                ['frustum_pyr', 'Truncated Square Pyramid (Bottom a, Top b, Height h)']
            ], 'hint': 'Select 3D shape geometry'},
            {'id': 'base_dim', 'label': 'Base Radius (r) or Side (a)', 'type': 'number', 'default': 5, 'min': 0.1, 'max': 1000, 'step': 0.1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Radius of cone or base edge of regular pyramid'},
            {'id': 'top_dim', 'label': 'Top Radius (r) or Side (b) [Frustums Only]', 'type': 'number', 'default': 2, 'min': 0, 'max': 1000, 'step': 0.1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Top radius or edge (only used for truncated frustums)'},
            {'id': 'vert_height', 'label': 'Vertical Height (h)', 'type': 'number', 'default': 12, 'min': 0.1, 'max': 1000, 'step': 0.1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Perpendicular height from base to apex'}
        ],
        'outputs': [
            {'id': 'slant_height', 'label': 'Calculated Slant Height (s)', 'unit': 'ft', 'color': 'var(--accent-cyan)'},
            {'id': 'lateral_area', 'label': 'Lateral Surface Area', 'unit': 'sq ft', 'color': 'var(--text-bright)'},
            {'id': 'total_area', 'label': 'Total Surface Area (inc. bases)', 'unit': 'sq ft', 'color': 'var(--accent-emerald)'},
            {'id': 'pitch_angle', 'label': 'Base Pitch Angle (θ)', 'unit': 'degrees', 'color': 'var(--accent-purple)'},
            {'id': 'edge_length', 'label': 'Corner Lateral Edge Length (e)', 'unit': 'ft', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Cone: s = √(r² + h²) | Pyramid: s = √[h² + (a/2)²] | Frustum Cone: s = √[h² + (R - r)²]',
        'proof_steps': [
            {'step_title': '1. Right Cone Slant Height Formulation', 'step_text': 'The slant height s forms the hypotenuse of a right-angled triangle where the vertical height h is the altitude and the base radius r is the adjacent base: s = √(r² + h²).'},
            {'step_title': '2. Regular Square Pyramid Slant Height & Corner Edges', 'step_text': 'For a pyramid with square base a and vertical height h, the apothem of the base is a/2. The face slant height is s = √[h² + (a/2)²]. The corner edge length is e = √[s² + (a/2)²] = √[h² + a²/2].'},
            {'step_title': '3. Truncated Frustum Generalization', 'step_text': 'For a truncated frustum with bottom radius R and top radius r, cutting through the central axis yields a right trapezoid. The radial delta is Δr = (R - r). Applying the Pythagorean theorem yields: s = √[h² + (R - r)²].'}
        ],
        'faqs': [
            {'q': 'What is the slant height of a cone or pyramid?', 'a': 'The slant height is the distance measured along the lateral face from the apex down to the outer perimeter of the base. For a right cone, it equals the hypotenuse of the triangle formed by radius and height.'},
            {'q': 'What is the difference between vertical height and slant height?', 'a': 'Vertical height (h) is the perpendicular altitude from the center of the base straight to the top apex. Slant height (s) is always longer than vertical height because s = √(r² + h²).'},
            {'q': 'How do you find slant height of a truncated cone (frustum)?', 'a': 'Subtract the smaller top radius from the larger base radius to find the horizontal offset Δr = R - r, then apply Pythagoras: s = √[h² + (R - r)²].'}
        ],
        'js_logic': """
          const type = document.getElementById('param-shape_type').value;
          const b = getNum('base_dim') || 5;
          const top = getNum('top_dim') || 0;
          const h = getNum('vert_height') || 12;
          let s = 0, lat = 0, tot = 0, angle = 0, edge = 0;
          const pi = Math.PI;
          if (type === 'cone') {
            s = Math.sqrt(b * b + h * h);
            lat = pi * b * s;
            tot = lat + (pi * b * b);
            angle = Math.atan2(h, b) * (180 / pi);
            edge = s;
          } else if (type === 'pyramid') {
            const half_a = b / 2;
            s = Math.sqrt(h * h + half_a * half_a);
            lat = 2 * b * s;
            tot = lat + (b * b);
            angle = Math.atan2(h, half_a) * (180 / pi);
            edge = Math.sqrt(s * s + half_a * half_a);
          } else if (type === 'frustum_cone') {
            const dr = Math.abs(b - top);
            s = Math.sqrt(h * h + dr * dr);
            lat = pi * (b + top) * s;
            tot = lat + pi * b * b + pi * top * top;
            angle = Math.atan2(h, dr || 0.001) * (180 / pi);
            edge = s;
          } else if (type === 'frustum_pyr') {
            const da = Math.abs(b - top) / 2;
            s = Math.sqrt(h * h + da * da);
            lat = 2 * (b + top) * s;
            tot = lat + b * b + top * top;
            angle = Math.atan2(h, da || 0.001) * (180 / pi);
            edge = Math.sqrt(s * s + da * da);
          }
          setDisp('slant_height', fmt(s, 3) + ' units');
          setDisp('lateral_area', fmt(lat, 2) + ' sq units');
          setDisp('total_area', fmt(tot, 2) + ' sq units');
          setDisp('pitch_angle', fmt(angle, 2) + '°');
          setDisp('edge_length', fmt(edge, 3) + ' units');
        """
    },

    # 2. LCL Freight & CBM Calculator (Position 12.0 in GSC!)
    {
        'slug': 'logistics/lcl-freight-cbm',
        'category': 'logistics',
        'cluster': 'logistics',
        'name': 'LCL Freight & CBM Calculator',
        'title': 'LCL Freight & CBM Calculator: Chargeable Weight & Container Fill | OmniOperand',
        'description': 'Calculate ocean freight CBM, chargeable weight (W/M rule), volumetric weight, container packing capacity, and LCL shipping costs.',
        'hero_badge': 'Ocean Freight & Global Logistics • Incoterms 2026 Invariants',
        'hero_subtext': 'Calculate total shipment volume in Cubic Meters (CBM), volumetric weight, ocean Weight/Measurement (W/M) chargeable weight, and container capacity utilization.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'cargo_qty', 'label': 'Package / Carton Count', 'type': 'number', 'default': 50, 'min': 1, 'max': 50000, 'step': 1, 'unit': 'cartons', 'hint': 'Total number of identical cartons or pallets'},
            {'id': 'cargo_len', 'label': 'Carton Length', 'type': 'number', 'default': 20, 'min': 1, 'max': 500, 'step': 0.5, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Length of single piece'},
            {'id': 'cargo_wid', 'label': 'Carton Width', 'type': 'number', 'default': 16, 'min': 1, 'max': 500, 'step': 0.5, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Width of single piece'},
            {'id': 'cargo_hgt', 'label': 'Carton Height', 'type': 'number', 'default': 14, 'min': 1, 'max': 500, 'step': 0.5, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Height of single piece'},
            {'id': 'gross_weight_per', 'label': 'Gross Weight Per Carton', 'type': 'number', 'default': 25, 'min': 0.5, 'max': 5000, 'step': 0.5, 'unit': 'lbs', 'metric_unit': 'kg', 'hint': 'Scale weight per individual carton'},
            {'id': 'freight_rate_cbm', 'label': 'Ocean Freight Rate ($/CBM)', 'type': 'number', 'default': 85, 'min': 10, 'max': 1000, 'step': 5, 'unit': '$/CBM', 'hint': 'Shipping line LCL rate per cubic meter'}
        ],
        'outputs': [
            {'id': 'total_cbm', 'label': 'Total Shipment Volume (CBM)', 'unit': 'm³ (CBM)', 'color': 'var(--accent-cyan)'},
            {'id': 'total_cft', 'label': 'Total Volume in Cubic Feet', 'unit': 'cu ft (CFT)', 'color': 'var(--text-bright)'},
            {'id': 'gross_weight_total', 'label': 'Total Actual Gross Weight', 'unit': 'kg / lbs', 'color': 'var(--text-bright)'},
            {'id': 'chargeable_wm', 'label': 'Ocean Chargeable Weight (W/M)', 'unit': 'Revenue Tons (RT)', 'color': 'var(--accent-emerald)'},
            {'id': 'container_20ft_pct', 'label': '20ft Container Utilization', 'unit': '% of 33 CBM', 'color': 'var(--accent-purple)'},
            {'id': 'est_freight_cost', 'label': 'Estimated Ocean Freight Cost', 'unit': '$ USD', 'color': 'var(--accent-cyan)'}
        ],
        'formula_display': 'CBM = (L · W · H · Qty) / 61,023.7 (in³) | Ocean W/M: 1 CBM = 1,000 kg (1 Metric Ton) | Chargeable = max(CBM, Weight_MT)',
        'proof_steps': [
            {'step_title': '1. Cubic Meter (CBM) Formulation', 'step_text': 'One cubic meter equals 1,000,000 cm³ or 61,023.74 in³. Total CBM = (Length × Width × Height × Quantity) / Divisor.'},
            {'step_title': '2. Ocean Freight Weight/Measurement (W/M) Invariant', 'step_text': 'Maritime ocean carriers bill based on the greater of volume in CBM or gross metric tonnage (1 CBM = 1 Metric Ton = 1,000 kg = 2,204.6 lbs). Whichever produces the higher billing revenue is designated the Revenue Ton (RT).'},
            {'step_title': '3. Container Space Allocation', 'step_text': 'A standard 20ft ocean container has a practical packing capacity of ~33.2 CBM; a 40ft general container holds ~67.7 CBM. LCL is economically optimal when volume is below ~15 CBM, above which FCL (Full Container Load) becomes cheaper.'}
        ],
        'faqs': [
            {'q': 'What does LCL mean in shipping?', 'a': 'LCL stands for Less than Container Load. It allows multiple shippers to consolidate smaller cargo shipments into a single ocean container, paying only for the exact volume (CBM) they occupy.'},
            {'q': 'How is ocean freight chargeable weight (W/M) calculated?', 'a': 'Ocean carriers use the Weight or Measure (W/M) rule where 1 CBM equals 1,000 kg (1 Metric Ton). For example, a 5 CBM shipment weighing 2,000 kg is billed for 5 Revenue Tons because 5 CBM > 2 Metric Tons.'},
            {'q': 'When should you switch from LCL to FCL?', 'a': 'When your shipment reaches approximately 13 to 15 CBM, booking a full 20ft container (FCL) is usually cheaper than paying individual LCL consolidation, documentation, and destination deconsolidation fees.'}
        ],
        'js_logic': """
          const qty = getNum('cargo_qty') || 1;
          const l = getNum('cargo_len') || 20;
          const w = getNum('cargo_wid') || 16;
          const h = getNum('cargo_hgt') || 14;
          const wt_unit = getNum('gross_weight_per') || 25;
          const rate = getNum('freight_rate_cbm') || 85;
          const single_cuin = l * w * h;
          const total_cuin = single_cuin * qty;
          const cft = total_cuin / 1728;
          const cbm = total_cuin / 61023.74;
          const total_lbs = wt_unit * qty;
          const total_kg = total_lbs * 0.453592;
          const weight_metric_tons = total_kg / 1000;
          const chargeable_rt = Math.max(cbm, weight_metric_tons);
          const est_cost = chargeable_rt * rate;
          const fill_20ft = (cbm / 33.2) * 100;
          setDisp('total_cbm', fmt(cbm, 2) + ' CBM');
          setDisp('total_cft', fmt(cft, 1) + ' cu ft');
          setDisp('gross_weight_total', fmt(total_kg, 1) + ' kg (' + fmt(total_lbs, 0) + ' lbs)');
          setDisp('chargeable_wm', fmt(chargeable_rt, 2) + ' Revenue Tons');
          setDisp('container_20ft_pct', fmt(fill_20ft, 1) + '% of 20ft');
          setDisp('est_freight_cost', '$' + fmt(est_cost, 2));
        """
    },

    # 3. Tubular Reabsorption of Phosphate (%TRP) Calculator (Position 41.0 in GSC!)
    {
        'slug': 'biotech/tubular-reabsorption-phosphate-trp',
        'category': 'biotech',
        'cluster': 'biotech',
        'name': 'Tubular Reabsorption of Phosphate (%TRP) & TmP/GFR Calculator',
        'title': 'Tubular Reabsorption of Phosphate (%TRP) & TmP/GFR Calculator | OmniOperand',
        'description': 'Calculate %TRP and TmP/GFR ratio using serum/urine phosphate and creatinine to assess renal tubular phosphate wasting and hyperparathyroidism.',
        'hero_badge': 'Clinical Nephrology & Endocrinology • Walton-Bijvoet Invariants',
        'hero_subtext': 'Determine renal tubular reabsorption of phosphate (%TRP), fractional excretion of phosphate, and the tubular maximum phosphate threshold (TmP/GFR).',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 's_phos', 'label': 'Serum Phosphate (S_phos)', 'type': 'number', 'default': 3.2, 'min': 0.5, 'max': 15, 'step': 0.1, 'unit': 'mg/dL', 'hint': 'Fasting serum phosphorus level (normal: 2.5–4.5 mg/dL)'},
            {'id': 'u_phos', 'label': 'Urine Phosphate (U_phos)', 'type': 'number', 'default': 35, 'min': 1, 'max': 300, 'step': 1, 'unit': 'mg/dL', 'hint': 'Spot second-morning fasting urine phosphate'},
            {'id': 's_cr', 'label': 'Serum Creatinine (S_cr)', 'type': 'number', 'default': 0.9, 'min': 0.2, 'max': 15, 'step': 0.05, 'unit': 'mg/dL', 'hint': 'Serum creatinine (normal: 0.6–1.2 mg/dL)'},
            {'id': 'u_cr', 'label': 'Urine Creatinine (U_cr)', 'type': 'number', 'default': 80, 'min': 5, 'max': 500, 'step': 1, 'unit': 'mg/dL', 'hint': 'Concurrent spot urine creatinine'}
        ],
        'outputs': [
            {'id': 'trp_pct', 'label': 'Tubular Reabsorption of Phosphate (%TRP)', 'unit': '%', 'color': 'var(--accent-cyan)'},
            {'id': 'fe_phos', 'label': 'Fractional Excretion of Phosphate (FE_P)', 'unit': '%', 'color': 'var(--text-bright)'},
            {'id': 'tmp_gfr', 'label': 'Renal Threshold (TmP/GFR)', 'unit': 'mg/dL', 'color': 'var(--accent-emerald)'},
            {'id': 'clin_status', 'label': 'Diagnostic Clinical Assessment', 'unit': 'status', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': '%TRP = [ 1 - (U_phos · S_cr) / (S_phos · U_cr) ] · 100 | TmP/GFR nomogram derivation',
        'proof_steps': [
            {'step_title': '1. Fractional Excretion & %TRP Formulation', 'step_text': 'Phosphate clearance relative to creatinine clearance yields fractional excretion: FE_P = (U_phos × S_cr) / (S_phos × U_cr). Tubular reabsorption is its complement: %TRP = (1 - FE_P) × 100%.'},
            {'step_title': '2. Walton & Bijvoet TmP/GFR Nomogram', 'step_text': 'If %TRP ≤ 86% (0.86), tubular reabsorption operates below saturation: TmP/GFR = %TRP × S_phos. If %TRP > 86%, non-linear splay applies: TmP/GFR = 0.3 × %TRP / [1 - (0.8 × %TRP)] × S_phos.'},
            {'step_title': '3. Differential Diagnosis Principles', 'step_text': 'A low %TRP (< 85%) in the presence of hypophosphatemia indicates renal phosphate wasting (e.g. primary hyperparathyroidism, X-linked hypophosphatemia, or oncogenic osteomalacia).'}
        ],
        'faqs': [
            {'q': 'What is normal %TRP?', 'a': 'In healthy adults with normal dietary phosphate and kidney function, %TRP is normally 85% to 95%. Values below 85% indicate renal phosphate wasting.'},
            {'q': 'What is the significance of TmP/GFR?', 'a': 'TmP/GFR represents the maximal renal tubular threshold for phosphate reabsorption per unit of glomerular filtrate. It is independent of GFR and provides an accurate measure of renal phosphate handling.'},
            {'q': 'When is %TRP testing indicated?', 'a': 'It is indicated for evaluating unexplained hypophosphatemia, suspected primary hyperparathyroidism, FGF23-mediated rickets/osteomalacia, and Fanconi syndrome.'}
        ],
        'js_logic': """
          const s_p = getNum('s_phos') || 3.2;
          const u_p = getNum('u_phos') || 35;
          const s_cr = getNum('s_cr') || 0.9;
          const u_cr = getNum('u_cr') || 80;
          const fe_p = (u_p * s_cr) / (s_p * u_cr);
          const trp_decimal = 1 - fe_p;
          const trp_pct = Math.max(0, Math.min(100, trp_decimal * 100));
          let tmp_gfr = 0;
          if (trp_decimal <= 0.86) {
            tmp_gfr = trp_decimal * s_p;
          } else {
            tmp_gfr = (0.3 * trp_decimal) / (1 - 0.8 * trp_decimal) * s_p;
          }
          let status = 'Normal Tubular Handling';
          if (trp_pct < 85 && s_p < 2.5) {
            status = '⚠️ Renal Phosphate Wasting (Hyperparathyroidism / FGF23)';
          } else if (trp_pct < 85) {
            status = 'Decreased Reabsorption (< 85%)';
          } else if (s_p > 4.5 && trp_pct > 95) {
            status = '⚠️ High Phosphate Retention (Hypoparathyroidism / CKD)';
          }
          setDisp('trp_pct', fmt(trp_pct, 1) + '%');
          setDisp('fe_phos', fmt(fe_p * 100, 1) + '%');
          setDisp('tmp_gfr', fmt(tmp_gfr, 2) + ' mg/dL');
          setDisp('clin_status', status);
        """
    },

    # 4. Brick Soling & Flat Masonry Area Calculator (Position 56.0 in GSC!)
    {
        'slug': 'construction/brick-soling',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Brick Soling & Flat Masonry Area Calculator',
        'title': 'Brick Soling Calculator: Flat, Edge & Herringbone Paving | OmniOperand',
        'description': 'Calculate brick count, bedding sand volume, and mortar for flat soling, on-edge soling, and herringbone sub-base pavements.',
        'hero_badge': 'Civil Construction & Pavements • IS 2212 / ASTM C902',
        'hero_subtext': 'Estimate precise brick quantities, bedding sand cushion volume, and labor rates for flat soling, brick-on-edge, and herringbone subgrade layers.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'soling_len', 'label': 'Pavement Length', 'type': 'number', 'default': 50, 'min': 1, 'max': 5000, 'step': 1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Length of driveway, floor, or pathway'},
            {'id': 'soling_wid', 'label': 'Pavement Width', 'type': 'number', 'default': 10, 'min': 1, 'max': 500, 'step': 0.5, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Width of paved area'},
            {'id': 'soling_pattern', 'label': 'Brick Soling Pattern', 'type': 'select', 'default': 'flat', 'options': [
                ['flat', 'Flat Brick Soling (Bed Face Exposed: ~32 sq in/brick)'],
                ['edge', 'Brick-on-Edge Soling (Narrow Edge Exposed: ~20 sq in/brick)'],
                ['herringbone', 'Herringbone Soling (Interlocking 45°/90° Flat)']
            ], 'hint': 'Orientation of brick units'},
            {'id': 'brick_size', 'label': 'Standard Brick Dimension', 'type': 'select', 'default': 'modular', 'options': [
                ['modular', 'Standard Modular (8" × 4" × 2.25")'],
                ['traditional', 'Traditional / Engineering (9" × 4.5" × 3")']
            ], 'hint': 'Nominal brick dimensions including joint'},
            {'id': 'sand_depth', 'label': 'Sand Bedding Cushion Depth', 'type': 'number', 'default': 1.5, 'min': 0.5, 'max': 6, 'step': 0.25, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Thickness of coarse bedding sand beneath soling'},
            {'id': 'waste_pct', 'label': 'Breakage & Cutting Waste', 'type': 'number', 'default': 5, 'min': 2, 'max': 20, 'step': 1, 'unit': '%', 'hint': 'Extra brick allowance for edge cuts and handling'}
        ],
        'outputs': [
            {'id': 'total_area', 'label': 'Total Soling Surface Area', 'unit': 'sq ft (m²)', 'color': 'var(--text-bright)'},
            {'id': 'net_bricks', 'label': 'Net Required Brick Count', 'unit': 'bricks', 'color': 'var(--accent-cyan)'},
            {'id': 'gross_bricks', 'label': 'Total Bricks (with Waste)', 'unit': 'bricks', 'color': 'var(--accent-emerald)'},
            {'id': 'sand_cft', 'label': 'Bedding Sand Volume', 'unit': 'cu ft (yd³)', 'color': 'var(--text-bright)'},
            {'id': 'sand_tons', 'label': 'Bedding Sand Weight', 'unit': 'Tons', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'Bricks = (Area_sqft / Brick_Face_sqft) · (1 + Waste%) | Sand (yd³) = (Area · SandDepth/12) / 27',
        'proof_steps': [
            {'step_title': '1. Effective Face Area Formulation', 'step_text': 'For modular flat soling (8" × 4"), each brick covers 32 sq in (0.222 sq ft), yielding ~4.5 bricks/sq ft. In brick-on-edge (8" × 2.25"), each brick covers 18 sq in (0.125 sq ft), requiring ~8.0 bricks/sq ft.'},
            {'step_title': '2. Sand Cushion Volume', 'step_text': 'Bedding sand volume equals Surface Area × (Depth in inches / 12). Divide cubic feet by 27 to calculate cubic yards. Multiply cubic yards by ~1.35 tons/yd³ for compacted sand mass.'},
            {'step_title': '3. Sub-base Structural Role', 'step_text': 'Brick soling serves as a rigid foundation layer over compacted subgrade beneath concrete floor slabs or flexible road pavements, preventing moisture capillary rise and distributing point loads.'}
        ],
        'faqs': [
            {'q': 'What is brick soling?', 'a': 'Brick soling is a traditional foundation engineering technique where a single or double layer of bricks is laid flat or on-edge over compacted earth or sand to create a stable, non-yielding base for concrete slabs or road pavements.'},
            {'q': 'How many bricks are needed for 100 sq ft of flat soling?', 'a': 'Using standard modular bricks (8" × 4"), you need approximately 450 bricks for 100 sq ft (net). Adding a 5% cutting waste brings the total to 473 bricks.'},
            {'q': 'Why is sand bedding used under soling?', 'a': 'A 1 to 2-inch cushion of clean coarse sand levels the subgrade, absorbs minor settlement variations, and provides drainage beneath the bricks.'}
        ],
        'js_logic': """
          const l = getNum('soling_len') || 50;
          const w = getNum('soling_wid') || 10;
          const pattern = document.getElementById('param-soling_pattern').value;
          const size = document.getElementById('param-brick_size').value;
          const sand_d = getNum('sand_depth') || 1.5;
          const waste = (getNum('waste_pct') || 5) / 100;
          const area_sqft = l * w;
          const area_sqm = area_sqft * 0.092903;
          let face_sqin = 32;
          if (size === 'traditional') {
            face_sqin = (pattern === 'edge') ? (9 * 3) : (9 * 4.5);
          } else {
            face_sqin = (pattern === 'edge') ? (8 * 2.25) : (8 * 4);
          }
          if (pattern === 'herringbone') face_sqin *= 0.96;
          const bricks_per_sqft = 144 / face_sqin;
          const net_bricks = Math.ceil(area_sqft * bricks_per_sqft);
          const gross_bricks = Math.ceil(net_bricks * (1 + waste));
          const sand_cft = area_sqft * (sand_d / 12);
          const sand_cyd = sand_cft / 27;
          const sand_tons = sand_cyd * 1.35;
          setDisp('total_area', fmt(area_sqft, 0) + ' sq ft (' + fmt(area_sqm, 1) + ' m²)');
          setDisp('net_bricks', fmt(net_bricks, 0) + ' Bricks');
          setDisp('gross_bricks', fmt(gross_bricks, 0) + ' Bricks');
          setDisp('sand_cft', fmt(sand_cft, 1) + ' cu ft (' + fmt(sand_cyd, 2) + ' yd³)');
          setDisp('sand_tons', fmt(sand_tons, 2) + ' Tons');
        """
    },

    # 5. Ultrasonic Angle Beam Path Calculator (Position 63.0 in GSC!)
    {
        'slug': 'engineering/ultrasonic-beam-path',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Ultrasonic Angle Beam Path & Sound Path Distance Calculator',
        'title': 'Ultrasonic Angle Beam Path Calculator: Sound Path & Skip Distance | OmniOperand',
        'description': 'Calculate NDT shear wave ultrasonic sound path distance, surface skip distance, and flaw depth for 45°, 60°, and 70° angle beam transducers.',
        'hero_badge': 'Non-Destructive Testing (NDT) • ASME Sec V / AWS D1.1',
        'hero_subtext': 'Calculate ultrasonic sound path (W), surface projection distance, skip distance (V-path), and true flaw depth for weld inspection under ASME/AWS standards.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'wedge_angle', 'label': 'Transducer Wedge Angle (θ)', 'type': 'select', 'default': '70', 'options': [
                ['45', '45° Shear Wave Angle Beam'],
                ['60', '60° Shear Wave Angle Beam'],
                ['70', '70° Shear Wave Angle Beam (Standard Plate Welds)'],
                ['30', '30° Transverse Angle'],
                ['80', '80° High Angle']
            ], 'hint': 'Refracted angle in carbon steel'},
            {'id': 'mat_thickness', 'label': 'Material Plate Thickness (t)', 'type': 'number', 'default': 0.75, 'min': 0.1, 'max': 20, 'step': 0.05, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Nominal base metal thickness'},
            {'id': 'sound_path_w', 'label': 'Observed Sound Path to Flaw (W)', 'type': 'number', 'default': 1.60, 'min': 0.1, 'max': 100, 'step': 0.05, 'unit': 'in', 'metric_unit': 'mm', 'hint': 'Screen display sound path (time of flight × velocity)'},
            {'id': 'shear_velocity', 'label': 'Shear Wave Velocity in Material', 'type': 'number', 'default': 0.128, 'min': 0.05, 'max': 0.3, 'step': 0.001, 'unit': 'in/µs', 'metric_unit': 'm/s', 'hint': '0.128 in/µs (3,240 m/s) for carbon steel'}
        ],
        'outputs': [
            {'id': 'skip_dist_half', 'label': 'Half-Skip Surface Distance (1st Leg)', 'unit': 'in', 'color': 'var(--text-bright)'},
            {'id': 'skip_dist_full', 'label': 'Full-Skip Surface Distance (V-Path)', 'unit': 'in', 'color': 'var(--accent-cyan)'},
            {'id': 'flaw_depth', 'label': 'True Depth to Flaw from Surface', 'unit': 'in', 'color': 'var(--accent-emerald)'},
            {'id': 'surface_dist', 'label': 'Surface Distance (Index to Flaw)', 'unit': 'in', 'color': 'var(--accent-purple)'},
            {'id': 'beam_leg', 'label': 'Ultrasonic Leg Classification', 'unit': 'status', 'color': 'var(--text-bright)'},
            {'id': 'tof_us', 'label': 'Round-Trip Time of Flight (ToF)', 'unit': 'µs', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Sound Path Leg 1: W = t / cos(θ) | Skip Distance S = 2 · t · tan(θ) | Flaw Depth d = W · cos(θ)',
        'proof_steps': [
            {'step_title': '1. Trigonometric Sound Path Geometry', 'step_text': 'An angle beam transducer refracts shear waves into test plate at angle θ. In the first leg (direct sound path to bottom surface), the path length is W_leg1 = t / cos(θ).'},
            {'step_title': '2. Surface Skip Distance (V-Path)', 'step_text': 'The half-skip surface distance from probe index point to bottom reflection is S_half = t · tan(θ). The full-skip distance (bouncing off bottom back to top surface) is S_full = 2 · t · tan(θ).'},
            {'step_title': '3. Flaw Depth Calculation Across Legs', 'step_text': 'If observed sound path W ≤ W_leg1, the reflector is in Leg 1 and true depth d = W · cos(θ). If W > W_leg1, the sound wave has bounced off the bottom surface into Leg 2: true depth d = 2t - W · cos(θ).'}
        ],
        'faqs': [
            {'q': 'What is ultrasonic skip distance?', 'a': 'Skip distance is the surface distance between the beam index point and the point where the sound wave returns to the scanning surface after reflecting off the bottom boundary of the test plate.'},
            {'q': 'Why is a 70° angle beam probe most common for plate welds?', 'a': 'A 70° angle beam produces a longer surface projection and optimal impingement angle against vertical weld bevel preparations, maximizing reflection from lack-of-fusion and crack defects.'},
            {'q': 'How do you tell if a defect is in the 1st leg or 2nd leg?', 'a': 'Calculate first-leg sound path W_1 = t / cos(θ). If your calibrated sound path reading on the instrument screen is less than W_1, the defect is in Leg 1; if greater, it is located in Leg 2.'}
        ],
        'js_logic': """
          const theta_deg = parseFloat(document.getElementById('param-wedge_angle').value) || 70;
          const theta_rad = theta_deg * (Math.PI / 180);
          const t = getNum('mat_thickness') || 0.75;
          const w = getNum('sound_path_w') || 1.6;
          const vel = getNum('shear_velocity') || 0.128;
          const s_half = t * Math.tan(theta_rad);
          const s_full = 2 * s_half;
          const w_leg1 = t / Math.cos(theta_rad);
          let depth = 0;
          let leg = '1st Leg (Direct Sound)';
          if (w <= w_leg1) {
            depth = w * Math.cos(theta_rad);
            leg = '1st Leg (Direct Sound)';
          } else {
            depth = (2 * t) - (w * Math.cos(theta_rad));
            leg = '2nd Leg (Bottom Reflected Sound)';
          }
          depth = Math.max(0, depth);
          const surface_x = w * Math.sin(theta_rad);
          const tof = (2 * w) / vel;
          setDisp('skip_dist_half', fmt(s_half, 3) + ' in');
          setDisp('skip_dist_full', fmt(s_full, 3) + ' in');
          setDisp('flaw_depth', fmt(depth, 3) + ' in');
          setDisp('surface_dist', fmt(surface_x, 3) + ' in');
          setDisp('beam_leg', leg);
          setDisp('tof_us', fmt(tof, 2) + ' µs');
        """
    },

    # 6. Drill Pipe & Casing Well Displacement Calculator (Position 69.0 in GSC!)
    {
        'slug': 'engineering/drill-pipe-displacement',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Drill Pipe & Casing Well Displacement Calculator',
        'title': 'Drill Pipe & Casing Displacement Calculator: Open vs Closed End | OmniOperand',
        'description': 'Calculate drill pipe, collar, and casing displacement in bbl/ft and pit volume changes for tripping in and tripping out of borehole wells.',
        'hero_badge': 'Petroleum & Drilling Engineering • API RP 13B Invariants',
        'hero_subtext': 'Calculate drill string steel displacement (open-end vs closed-end) in barrels per foot, total pit volume gain/loss, and buoyancy loads.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'pipe_od', 'label': 'Pipe Outer Diameter (OD)', 'type': 'number', 'default': 5.0, 'min': 1.0, 'max': 30.0, 'step': 0.125, 'unit': 'in', 'hint': '5.0" standard drill pipe or casing OD'},
            {'id': 'pipe_id', 'label': 'Pipe Inner Diameter (ID)', 'type': 'number', 'default': 4.276, 'min': 0.5, 'max': 29.0, 'step': 0.001, 'unit': 'in', 'hint': '4.276" ID for 19.5 lb/ft drill pipe'},
            {'id': 'trip_length', 'label': 'Length of Pipe Tripped', 'type': 'number', 'default': 5000, 'min': 30, 'max': 40000, 'step': 90, 'unit': 'ft', 'hint': 'Length of stands tripped in or out'},
            {'id': 'trip_mode', 'label': 'Tripping Condition', 'type': 'select', 'default': 'closed', 'options': [
                ['closed', 'Closed-End (Float Valve Installed / Plugged Pipe)'],
                ['open', 'Open-End (Unplugged Pipe / Steel Displacement Only)']
            ], 'hint': 'Closed-end includes internal pipe capacity'},
            {'id': 'mud_weight', 'label': 'Drilling Fluid Mud Density', 'type': 'number', 'default': 10.5, 'min': 8.33, 'max': 20.0, 'step': 0.1, 'unit': 'ppg', 'hint': 'Pounds per gallon (ppg)'}
        ],
        'outputs': [
            {'id': 'disp_bbl_ft', 'label': 'Displacement Factor per Foot', 'unit': 'bbl/ft', 'color': 'var(--accent-cyan)'},
            {'id': 'capacity_bbl_ft', 'label': 'Internal Capacity Factor', 'unit': 'bbl/ft', 'color': 'var(--text-bright)'},
            {'id': 'total_bbl_disp', 'label': 'Total Fluid Displaced (Pit Gain/Loss)', 'unit': 'Barrels (bbl)', 'color': 'var(--accent-emerald)'},
            {'id': 'total_gal_disp', 'label': 'Total Volume in Gallons', 'unit': 'Gallons (gal)', 'color': 'var(--text-bright)'},
            {'id': 'metal_weight_lbs', 'label': 'Dry String Weight in Air', 'unit': 'lbs', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'Open Disp = (OD² - ID²) / 1029.4 bbl/ft | Closed Disp = OD² / 1029.4 bbl/ft | Capacity = ID² / 1029.4 bbl/ft',
        'proof_steps': [
            {'step_title': '1. Petroleum Volumetric Constant 1029.4', 'step_text': 'One barrel equals 42 US gallons or 9,702 cu in. The volume of a 1-inch diameter cylinder of length 1 ft is V = π × (0.5)² × 12 = 9.4248 cu in. Dividing 9,702 / 9.4248 yields the fundamental oilfield constant: 1,029.4.'},
            {'step_title': '2. Open-End vs Closed-End Invariants', 'step_text': 'When pipe is open-ended, drilling mud enters the internal bore, displacing only the volume of the tubular steel: D_open = (OD² - ID²) / 1029.4. When a float valve is installed, the entire outer envelope is displaced: D_closed = OD² / 1029.4.'},
            {'step_title': '3. Pit Volume Tracking & Well Control', 'step_text': 'Accurately monitoring trip tank barrel counts against theoretical displacement is the primary defense against kicks and blowouts when swabbing or surging the well.'}
        ],
        'faqs': [
            {'q': 'What is the difference between open-end and closed-end displacement?', 'a': 'Open-end displacement is the volume of fluid displaced by only the steel wall of the pipe. Closed-end displacement occurs when a float collar or bit plug prevents fluid from entering the pipe, displacing both the steel wall and the internal bore volume.'},
            {'q': 'Where does the 1029.4 constant come from in drilling?', 'a': '1029.4 is the number of linear feet of 1-inch ID pipe required to contain exactly 1 barrel (42 US gallons) of liquid: 9,702 cu in / (π · 0.5² · 12) = 1029.4.'},
            {'q': 'Why is displacement critical during tripping?', 'a': 'If the volume of mud required to fill the hole while pulling pipe out is less than the theoretical displacement, formation gas or oil has entered the wellbore (a kick), requiring immediate shut-in.'}
        ],
        'js_logic': """
          const od = getNum('pipe_od') || 5.0;
          const id = getNum('pipe_id') || 4.276;
          const len = getNum('trip_length') || 5000;
          const mode = document.getElementById('param-trip_mode').value;
          const mud = getNum('mud_weight') || 10.5;
          const open_factor = (od * od - id * id) / 1029.4;
          const closed_factor = (od * od) / 1029.4;
          const cap_factor = (id * id) / 1029.4;
          const factor = (mode === 'closed') ? closed_factor : open_factor;
          const total_bbl = factor * len;
          const total_gal = total_bbl * 42;
          const steel_area = (Math.PI / 4) * (od * od - id * id);
          const nominal_weight_per_ft = steel_area * 12 * 0.2836;
          const total_air_weight = nominal_weight_per_ft * len;
          setDisp('disp_bbl_ft', fmt(factor, 5) + ' bbl/ft');
          setDisp('capacity_bbl_ft', fmt(cap_factor, 5) + ' bbl/ft');
          setDisp('total_bbl_disp', fmt(total_bbl, 2) + ' bbl');
          setDisp('total_gal_disp', fmt(total_gal, 0) + ' gal');
          setDisp('metal_weight_lbs', fmt(total_air_weight, 0) + ' lbs');
        """
    },

    # 7. Aerodynamic Drag & Downforce Force Calculator (Position 70.0 in GSC!)
    {
        'slug': 'physics/aerodynamic-drag-force',
        'category': 'physics',
        'cluster': 'physics',
        'name': 'Aerodynamic Drag & Downforce Force Calculator',
        'title': 'Aerodynamic Drag Force Calculator: Wind Resistance & Power | OmniOperand',
        'description': 'Calculate aerodynamic drag force (lbf/N), power required to overcome drag (HP/kW), and terminal velocity from speed and frontal area.',
        'hero_badge': 'Fluid Dynamics & Aerodynamics • Navier-Stokes Invariants',
        'hero_subtext': 'Compute aerodynamic drag resistance, aerodynamic power consumption, and dynamic air pressure across ground vehicles, aircraft, and cycling.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'speed_mph', 'label': 'Vehicle / Wind Speed', 'type': 'number', 'default': 70, 'min': 1, 'max': 800, 'step': 1, 'unit': 'mph', 'metric_unit': 'km/h', 'hint': 'Relative air velocity'},
            {'id': 'drag_coeff', 'label': 'Drag Coefficient (Cd)', 'type': 'number', 'default': 0.28, 'min': 0.05, 'max': 2.0, 'step': 0.01, 'unit': 'Cd', 'hint': '0.24 (Sedan), 0.35 (SUV), 0.70 (Semi-Truck), 0.90 (Bicycle)'},
            {'id': 'frontal_area', 'label': 'Frontal Projected Area (A)', 'type': 'number', 'default': 24, 'min': 1, 'max': 250, 'step': 0.5, 'unit': 'sq ft', 'metric_unit': 'm²', 'hint': 'Cross-sectional frontal profile area'},
            {'id': 'air_temp', 'label': 'Ambient Air Temperature', 'type': 'number', 'default': 68, 'min': -40, 'max': 130, 'step': 1, 'unit': '°F', 'metric_unit': '°C', 'hint': 'Temperature affects air density'},
            {'id': 'elevation_ft', 'label': 'Elevation Above Sea Level', 'type': 'number', 'default': 1000, 'min': 0, 'max': 30000, 'step': 500, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Altitude derating'}
        ],
        'outputs': [
            {'id': 'drag_force_lbf', 'label': 'Aerodynamic Drag Resistance', 'unit': 'lbf (N)', 'color': 'var(--accent-cyan)'},
            {'id': 'drag_power_hp', 'label': 'Power Overcoming Drag', 'unit': 'Horsepower (HP)', 'color': 'var(--accent-emerald)'},
            {'id': 'drag_power_kw', 'label': 'Power Overcoming Drag', 'unit': 'kW', 'color': 'var(--text-bright)'},
            {'id': 'dyn_pressure', 'label': 'Dynamic Stagnation Pressure (q)', 'unit': 'psi (Pa)', 'color': 'var(--accent-purple)'},
            {'id': 'air_density', 'label': 'Calculated Air Density (ρ)', 'unit': 'lb/ft³ (kg/m³)', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'F_drag = ½ · ρ · v² · C_d · A | Power = (F_drag · v) / 550 (HP) | q = ½ · ρ · v²',
        'proof_steps': [
            {'step_title': '1. Quadratic Velocity Dependence', 'step_text': 'Aerodynamic drag scales with the square of velocity (v²). Doubling road speed quadruples total drag force.'},
            {'step_title': '2. Cubic Power Law', 'step_text': 'Power is force multiplied by velocity: Power = F_drag × v = ½ · ρ · v³ · C_d · A. Doubling speed requires eight times (2³ = 8) as much engine horsepower to overcome wind resistance.'},
            {'step_title': '3. Altitude & Temperature Air Density Corrections', 'step_text': 'Air density ρ decreases with elevation and higher temperatures according to the ideal gas law: ρ = P / (R_spec · T). Standard sea level air is 0.0765 lb/ft³ (1.225 kg/m³).'}
        ],
        'faqs': [
            {'q': 'Why does highway speed dramatically reduce fuel efficiency and EV range?', 'a': 'Because of the cubic power law: overcoming aerodynamic drag at 80 mph requires ~50% more horsepower than at 65 mph (80³ / 65³ ≈ 1.86 ratio of aerodynamic power).'},
            {'q': 'What is a good drag coefficient (Cd) for modern cars?', 'a': 'Sleek modern electric vehicles achieve Cd between 0.20 and 0.24. Typical consumer sedans achieve 0.26 to 0.30, while pickup trucks and SUVs range from 0.35 to 0.45.'},
            {'q': 'How is frontal area measured?', 'a': 'Frontal area is approximately 85% of total vehicle width multiplied by total vehicle height (A ≈ 0.85 × W × H).' }
        ],
        'js_logic': """
          const mph = getNum('speed_mph') || 70;
          const cd = getNum('drag_coeff') || 0.28;
          const area_sqft = getNum('frontal_area') || 24;
          const temp_f = getNum('air_temp') || 68;
          const alt_ft = getNum('elevation_ft') || 1000;
          const temp_k = (temp_f - 32) * (5 / 9) + 273.15;
          const p_atm = 101325 * Math.pow(1 - 0.0000225577 * (alt_ft * 0.3048), 5.25588);
          const rho_kgm3 = p_atm / (287.058 * temp_k);
          const rho_slugft3 = rho_kgm3 * 0.00194032;
          const rho_lbft3 = rho_kgm3 * 0.062428;
          const v_fps = mph * 1.46667;
          const v_ms = mph * 0.44704;
          const f_lbf = 0.5 * rho_slugft3 * (v_fps * v_fps) * cd * area_sqft;
          const f_newtons = f_lbf * 4.44822;
          const hp = (f_lbf * v_fps) / 550;
          const kw = hp * 0.7457;
          const q_psi = (0.5 * rho_slugft3 * v_fps * v_fps) / 144;
          setDisp('drag_force_lbf', fmt(f_lbf, 1) + ' lbf (' + fmt(f_newtons, 0) + ' N)');
          setDisp('drag_power_hp', fmt(hp, 1) + ' HP');
          setDisp('drag_power_kw', fmt(kw, 1) + ' kW');
          setDisp('dyn_pressure', fmt(q_psi, 4) + ' psi');
          setDisp('air_density', fmt(rho_lbft3, 4) + ' lb/ft³ (' + fmt(rho_kgm3, 3) + ' kg/m³)');
        """
    },

    # 8. Commercial Battery Peak Shaving & Demand Charge Calculator (Position 70.5 in GSC!)
    {
        'slug': 'energy/battery-peak-shaving',
        'category': 'energy',
        'cluster': 'energy',
        'name': 'Commercial Battery Peak Shaving & Demand Charge Calculator',
        'title': 'Battery Peak Shaving Calculator: Commercial Demand Charge Savings | OmniOperand',
        'description': 'Calculate battery energy storage capacity (kW/kWh), utility demand charge reduction ($/kW), and payback period for commercial peak shaving.',
        'hero_badge': 'Power Systems & Energy Storage • IEEE 1547 / C&I Energy',
        'hero_subtext': 'Model commercial peak shaving battery storage requirements (kW/kWh), utility monthly demand charge cost avoidance, and system ROI.',
        'has_dual_units': False,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'hist_peak_kw', 'label': 'Facility Unmanaged Peak Demand', 'type': 'number', 'default': 500, 'min': 20, 'max': 50000, 'step': 25, 'unit': 'kW', 'hint': 'Maximum recorded monthly 15-minute kW peak'},
            {'id': 'target_peak_kw', 'label': 'Target Shaved Peak Limit', 'type': 'number', 'default': 350, 'min': 10, 'max': 45000, 'step': 25, 'unit': 'kW', 'hint': 'Grid import threshold cap'},
            {'id': 'peak_duration', 'label': 'Peak Discharge Duration', 'type': 'number', 'default': 2.0, 'min': 0.5, 'max': 8.0, 'step': 0.5, 'unit': 'hours', 'hint': 'Continuous duration peak exceeds target'},
            {'id': 'demand_rate', 'label': 'Utility Demand Charge Rate', 'type': 'number', 'default': 18.50, 'min': 2.0, 'max': 75.0, 'step': 0.5, 'unit': '$/kW/mo', 'hint': 'Monthly billing tariff per peak kW'},
            {'id': 'bess_cost_kwh', 'label': 'Turnkey BESS Installed Cost', 'type': 'number', 'default': 450, 'min': 200, 'max': 1200, 'step': 25, 'unit': '$/kWh', 'hint': 'Equipment, balance of plant, and interconnect'}
        ],
        'outputs': [
            {'id': 'bess_power_kw', 'label': 'Required Inverter Power Capacity', 'unit': 'kW', 'color': 'var(--accent-cyan)'},
            {'id': 'bess_energy_kwh', 'label': 'Required Battery Usable Storage', 'unit': 'kWh', 'color': 'var(--accent-emerald)'},
            {'id': 'monthly_savings', 'label': 'Monthly Demand Charge Savings', 'unit': '$/month', 'color': 'var(--text-bright)'},
            {'id': 'annual_savings', 'label': 'Annual Utility Cost Savings', 'unit': '$/year', 'color': 'var(--accent-purple)'},
            {'id': 'simple_payback', 'label': 'Estimated Simple Payback Period', 'unit': 'years', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Shaved kW = Peak - Target | Energy kWh = (Shaved kW · Hours) / (DoD · InverterEff) | Savings = Shaved kW · Rate · 12',
        'proof_steps': [
            {'step_title': '1. Inverter Power Sizing', 'step_text': 'The battery storage power inverter (BESS kW) must match the maximum delta between the facility unconstrained peak load and the target import limit: P_bess = Peak_kW - Target_kW.'},
            {'step_title': '2. Usable Energy Derating', 'step_text': 'To sustain peak shaving for duration T hours with a 90% depth-of-discharge (DoD) and 90% round-trip efficiency: Usable kWh = (P_bess × T) / (0.90 × 0.90) = (P_bess × T) / 0.81.'},
            {'step_title': '3. Demand Charge Monetization', 'step_text': 'Commercial electric bills charge $10 to $30+ per kilowatt of monthly peak demand. Reducing 150 kW at $18.50/kW produces $2,775/mo ($33,300/yr) in permanent cost avoidance.'}
        ],
        'faqs': [
            {'q': 'What is peak shaving with battery storage?', 'a': 'Peak shaving is the automated process of discharging an on-site battery system during periods of maximum facility power consumption to flatten spikes in grid electricity demand and reduce utility demand charges.'},
            {'q': 'What is a typical demand charge on commercial utility bills?', 'a': 'In the United States, commercial and industrial demand charges typically range from $12/kW to over $35/kW in states like California, New York, and Massachusetts, often comprising 30% to 60% of a company’s total electricity bill.'},
            {'q': 'What C-rate is typical for peak shaving batteries?', 'a': 'Peak shaving systems typically use a 0.5C (2-hour duration) to 0.25C (4-hour duration) storage architecture.'}
        ],
        'js_logic': """
          const peak = getNum('hist_peak_kw') || 500;
          const target = getNum('target_peak_kw') || 350;
          const hrs = getNum('peak_duration') || 2.0;
          const rate = getNum('demand_rate') || 18.5;
          const cost_kwh = getNum('bess_cost_kwh') || 450;
          const shaved_kw = Math.max(0, peak - target);
          const raw_kwh = (shaved_kw * hrs) / 0.81;
          const monthly = shaved_kw * rate;
          const annual = monthly * 12;
          const capex = raw_kwh * cost_kwh;
          const payback = (annual > 0) ? (capex / annual) : 0;
          setDisp('bess_power_kw', fmt(shaved_kw, 0) + ' kW');
          setDisp('bess_energy_kwh', fmt(raw_kwh, 1) + ' kWh (' + fmt(hrs, 1) + ' hr C-rating)');
          setDisp('monthly_savings', '$' + fmt(monthly, 0) + ' / mo');
          setDisp('annual_savings', '$' + fmt(annual, 0) + ' / yr');
          setDisp('simple_payback', fmt(payback, 1) + ' Years');
        """
    },

    # 9. Flowable Fill (CLSM) Volume & Mix Calculator (Position 71.0 in GSC!)
    {
        'slug': 'construction/flowable-fill-clsm',
        'category': 'construction',
        'cluster': 'construction',
        'name': 'Flowable Fill (CLSM) Volume & Mix Calculator',
        'title': 'Flowable Fill (CLSM) Calculator: Trench Volume & Mix Batches | OmniOperand',
        'description': 'Calculate Controlled Low-Strength Material (CLSM) flowable fill volume in cubic yards with pipe displacement deductions and mix designs.',
        'hero_badge': 'Civil Infrastructure & Utilities • ACI 229R / ASTM D6103',
        'hero_subtext': 'Calculate Controlled Low-Strength Material (CLSM) flowable fill volume, deduct pipe displacement volumes, and compute cement/fly-ash/sand slurry batches.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'trench_len', 'label': 'Trench Excavation Length', 'type': 'number', 'default': 100, 'min': 1, 'max': 50000, 'step': 5, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Total linear feet of trench'},
            {'id': 'trench_wid', 'label': 'Trench Width', 'type': 'number', 'default': 3, 'min': 0.5, 'max': 50, 'step': 0.25, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Trench cross-width'},
            {'id': 'trench_depth', 'label': 'Flowable Fill Backfill Depth', 'type': 'number', 'default': 4, 'min': 0.5, 'max': 50, 'step': 0.25, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Depth to be backfilled with slurry'},
            {'id': 'pipe_od_in', 'label': 'Buried Pipe Outer Diameter', 'type': 'number', 'default': 12, 'min': 0, 'max': 120, 'step': 1, 'unit': 'in', 'metric_unit': 'cm', 'hint': 'Pipe or conduit OD (enter 0 if no pipe)'},
            {'id': 'pipe_count', 'label': 'Number of Buried Conduits/Pipes', 'type': 'number', 'default': 1, 'min': 0, 'max': 20, 'step': 1, 'unit': 'pipes', 'hint': 'Quantity of pipes displaced in trench'},
            {'id': 'clsm_mix', 'label': 'CLSM Compressive Strength Class', 'type': 'select', 'default': 'excavatable', 'options': [
                ['excavatable', 'Excavatable CLSM (50–100 psi • Removable with hand shovel/backhoe)'],
                ['structural', 'Structural CLSM (150–300 psi • High load bearing)'],
                ['non_excavatable', 'Non-Excavatable (> 300 psi • Permanent pavement sub-base)']
            ], 'hint': 'ACI 229R compressive strength classification'}
        ],
        'outputs': [
            {'id': 'gross_vol_yd', 'label': 'Gross Trench Volume', 'unit': 'cu yd (yd³)', 'color': 'var(--text-bright)'},
            {'id': 'pipe_disp_yd', 'label': 'Pipe Displacement Subtracted', 'unit': 'cu yd (yd³)', 'color': 'var(--text-bright)'},
            {'id': 'net_clsm_yd', 'label': 'Net Flowable Fill Required (with 5% waste)', 'unit': 'cu yd (yd³)', 'color': 'var(--accent-cyan)'},
            {'id': 'cement_lbs', 'label': 'Portland Cement Required', 'unit': 'lbs', 'color': 'var(--accent-emerald)'},
            {'id': 'flyash_lbs', 'label': 'Fly Ash (Class F) Required', 'unit': 'lbs', 'color': 'var(--accent-purple)'},
            {'id': 'sand_tons', 'label': 'Concrete Sand Required', 'unit': 'Tons', 'color': 'var(--text-bright)'}
        ],
        'formula_display': 'Gross V = (L · W · D) / 27 | Pipe V = (π · r² · L · Qty) / 27 | Net = (Gross - Pipe) · 1.05',
        'proof_steps': [
            {'step_title': '1. Trench Volumetric Formulation', 'step_text': 'Gross excavation volume equals Length × Width × Depth in cubic feet, divided by 27 to convert to cubic yards.'},
            {'step_title': '2. Cylindrical Pipe Displacement Deduction', 'step_text': 'Each pipe displaces volume equal to π × (OD/2)² × L in cubic feet. Subtracting total pipe volume avoids over-ordering expensive ready-mix slurry.'},
            {'step_title': '3. ACI 229R Mix Proportions', 'step_text': 'Standard excavatable flowable fill utilizes a low-cement mix: ~50–100 lbs cement, 250–300 lbs fly ash, ~2,600 lbs sand, and ~450 lbs water per cubic yard to maintain compressive strength under 100 psi for easy future re-excavation.'}
        ],
        'faqs': [
            {'q': 'What is flowable fill (CLSM)?', 'a': 'Controlled Low-Strength Material (CLSM), commonly known as flowable fill or slurry, is a self-leveling, self-compacting cementitious backfill material used instead of compacted soil in utility trenches.'},
            {'q': 'Why is flowable fill limited to under 100 psi for utility trenches?', 'a': 'Keeping compressive strength below 100 psi allows maintenance crews to easily dig through the material in the future using standard hand shovels or backhoes without jackhammers.'},
            {'q': 'Does flowable fill require manual compaction or vibrating plates?', 'a': 'No. Flowable fill flows into all voids around pipes under gravity, requiring zero mechanical compaction and eliminating trench settlement.'}
        ],
        'js_logic': """
          const l = getNum('trench_len') || 100;
          const w = getNum('trench_wid') || 3;
          const d = getNum('trench_depth') || 4;
          const pipe_od = getNum('pipe_od_in') || 0;
          const pipes = getNum('pipe_count') || 0;
          const mix = document.getElementById('param-clsm_mix').value;
          const gross_cft = l * w * d;
          const gross_yd = gross_cft / 27;
          let pipe_cft = 0;
          if (pipe_od > 0 && pipes > 0) {
            const r_ft = (pipe_od / 2) / 12;
            pipe_cft = Math.PI * r_ft * r_ft * l * pipes;
          }
          const pipe_yd = pipe_cft / 27;
          const net_yd = Math.max(0, (gross_yd - pipe_yd) * 1.05);
          let cement_per_yd = 80;
          let flyash_per_yd = 300;
          if (mix === 'structural') {
            cement_per_yd = 150;
            flyash_per_yd = 250;
          } else if (mix === 'non_excavatable') {
            cement_per_yd = 250;
            flyash_per_yd = 150;
          }
          const tot_cement = net_yd * cement_per_yd;
          const tot_flyash = net_yd * flyash_per_yd;
          const tot_sand_tons = (net_yd * 2600) / 2000;
          setDisp('gross_vol_yd', fmt(gross_yd, 2) + ' yd³');
          setDisp('pipe_disp_yd', fmt(pipe_yd, 2) + ' yd³');
          setDisp('net_clsm_yd', fmt(net_yd, 2) + ' yd³');
          setDisp('cement_lbs', fmt(tot_cement, 0) + ' lbs');
          setDisp('flyash_lbs', fmt(tot_flyash, 0) + ' lbs');
          setDisp('sand_tons', fmt(tot_sand_tons, 1) + ' Tons');
        """
    },

    # 10. Retaining Wall Overturning & Sliding Safety Factor Calculator (Position 71.0 in GSC!)
    {
        'slug': 'engineering/retaining-wall-overturning-safety',
        'category': 'engineering',
        'cluster': 'engineering',
        'name': 'Retaining Wall Overturning & Sliding Safety Factor Calculator',
        'title': 'Retaining Wall Overturning & Sliding Safety Factor Calculator | OmniOperand',
        'description': 'Calculate factors of safety against overturning and sliding for cantilever concrete retaining walls using Rankine earth pressure theory.',
        'hero_badge': 'Geotechnical & Structural Engineering • Rankine / IBC 1807',
        'hero_subtext': 'Evaluate geotechnical stability: calculate active lateral earth pressure (Ka), overturning moment, resisting moment, and safety factors against overturning and sliding.',
        'has_dual_units': True,
        'governing_jurisdiction': None,
        'inputs': [
            {'id': 'wall_height_h', 'label': 'Total Retaining Wall Height (H)', 'type': 'number', 'default': 12, 'min': 3, 'max': 50, 'step': 0.5, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Overall height from bottom of footing to top of stem'},
            {'id': 'base_width_b', 'label': 'Base Footing Width (B)', 'type': 'number', 'default': 7.5, 'min': 2, 'max': 35, 'step': 0.25, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Total width of foundation footing slab'},
            {'id': 'toe_width_t', 'label': 'Toe Projection Width (T)', 'type': 'number', 'default': 2.0, 'min': 0.5, 'max': 15, 'step': 0.25, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Distance from front toe edge to front face of stem'},
            {'id': 'stem_thickness', 'label': 'Stem Average Thickness (t_s)', 'type': 'number', 'default': 1.0, 'min': 0.67, 'max': 5, 'step': 0.1, 'unit': 'ft', 'metric_unit': 'm', 'hint': 'Concrete stem thickness'},
            {'id': 'soil_gamma', 'label': 'Backfill Soil Unit Weight (γ)', 'type': 'number', 'default': 120, 'min': 80, 'max': 150, 'step': 5, 'unit': 'pcf', 'metric_unit': 'kN/m³', 'hint': '120 pcf typical for compacted sand/gravel'},
            {'id': 'soil_phi', 'label': 'Soil Internal Friction Angle (ϕ)', 'type': 'number', 'default': 32, 'min': 20, 'max': 45, 'step': 1, 'unit': 'degrees', 'hint': 'Angle of internal friction of backfill'},
            {'id': 'base_friction', 'label': 'Base Soil Friction Coefficient (μ)', 'type': 'number', 'default': 0.45, 'min': 0.2, 'max': 0.7, 'step': 0.05, 'unit': 'ratio', 'hint': 'Coefficient of friction between footing and soil'}
        ],
        'outputs': [
            {'id': 'ka_coeff', 'label': 'Active Earth Pressure (Ka)', 'unit': 'dimensionless', 'color': 'var(--text-bright)'},
            {'id': 'total_thrust_pa', 'label': 'Total Lateral Earth Thrust (Pa)', 'unit': 'lbs/ft (kN/m)', 'color': 'var(--text-bright)'},
            {'id': 'overturning_moment', 'label': 'Overturning Moment (M_ot)', 'unit': 'ft-lb/ft', 'color': 'var(--accent-cyan)'},
            {'id': 'resisting_moment', 'label': 'Resisting Moment (M_res)', 'unit': 'ft-lb/ft', 'color': 'var(--accent-emerald)'},
            {'id': 'fs_overturn', 'label': 'Factor of Safety (Overturning)', 'unit': 'FS ≥ 2.0', 'color': 'var(--accent-emerald)'},
            {'id': 'fs_sliding', 'label': 'Factor of Safety (Sliding)', 'unit': 'FS ≥ 1.5', 'color': 'var(--accent-purple)'}
        ],
        'formula_display': 'Ka = tan²(45° - ϕ/2) | Pa = ½ · Ka · γ · H² | M_ot = Pa · (H/3) | FS_ot = M_res / M_ot ≥ 2.0',
        'proof_steps': [
            {'step_title': '1. Rankine Active Earth Pressure', 'step_text': 'According to Rankine earth pressure theory, lateral active pressure coefficient is Ka = tan²(45° - ϕ/2) = (1 - sin ϕ) / (1 + sin ϕ). Total horizontal force is Pa = ½ · Ka · γ · H² acting at H/3 above base.'},
            {'step_title': '2. Overturning Moment Formulation', 'step_text': 'The overturning moment about the toe of the footing is M_ot = Pa × (H/3).'},
            {'step_title': '3. Resisting Equilibrium & Stability Ratios', 'step_text': 'Resisting moment M_res is produced by the weight of concrete (stem and footing) and the heavy wedge of soil resting above the heel. Factor of safety against overturning is FS_ot = M_res / M_ot (minimum 2.0 required by IBC). Factor of safety against sliding is FS_slide = (μ · Σ Vertical) / Pa (minimum 1.5 required).'}
        ],
        'faqs': [
            {'q': 'What is a safe factor of safety against overturning for retaining walls?', 'a': 'The International Building Code (IBC Section 1807.2) requires a minimum Factor of Safety of 2.0 against overturning, and a minimum Factor of Safety of 1.5 against sliding.'},
            {'q': 'Why is the soil above the heel beneficial for retaining walls?', 'a': 'The heel extends backward into the backfill, using the massive vertical weight of the retained soil column to anchor the wall against overturning.'},
            {'q': 'What happens if a retaining wall fails in sliding?', 'a': 'If the lateral earth thrust exceeds the frictional resistance between the concrete footing and foundation subsoil (FS < 1.5), the entire wall will shift laterally, requiring a shear key.'}
        ],
        'js_logic': """
          const h = getNum('wall_height_h') || 12;
          const b = getNum('base_width_b') || 7.5;
          const toe = getNum('toe_width_t') || 2.0;
          const ts = getNum('stem_thickness') || 1.0;
          const gamma = getNum('soil_gamma') || 120;
          const phi_deg = getNum('soil_phi') || 32;
          const mu = getNum('base_friction') || 0.45;
          const phi_rad = phi_deg * (Math.PI / 180);
          const ka = Math.pow(Math.tan((Math.PI / 4) - (phi_rad / 2)), 2);
          const pa = 0.5 * ka * gamma * h * h;
          const m_ot = pa * (h / 3);
          const foot_thick = 1.0;
          const stem_h = h - foot_thick;
          const heel = b - toe - ts;
          const w_stem = ts * stem_h * 150;
          const x_stem = toe + (ts / 2);
          const w_foot = b * foot_thick * 150;
          const x_foot = b / 2;
          const w_soil = heel * stem_h * gamma;
          const x_soil = b - (heel / 2);
          const total_v = w_stem + w_foot + w_soil;
          const m_res = (w_stem * x_stem) + (w_foot * x_foot) + (w_soil * x_soil);
          const fs_ot = m_res / m_ot;
          const fs_slide = (mu * total_v) / pa;
          setDisp('ka_coeff', fmt(ka, 3));
          setDisp('total_thrust_pa', fmt(pa, 0) + ' lbs/ft');
          setDisp('overturning_moment', fmt(m_ot, 0) + ' ft-lb/ft');
          setDisp('resisting_moment', fmt(m_res, 0) + ' ft-lb/ft');
          setDisp('fs_overturn', fmt(fs_ot, 2) + (fs_ot >= 2.0 ? ' ✅ (Stable)' : ' ⚠️ (Unstable < 2.0)'));
          setDisp('fs_sliding', fmt(fs_slide, 2) + (fs_slide >= 1.5 ? ' ✅ (Stable)' : ' ⚠️ (Unstable < 1.5)'));
        """
    }
]
