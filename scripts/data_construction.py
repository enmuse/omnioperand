"""
scripts/data_construction.py
26 High-Value Construction, Trade, Landscaping & Engineering Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

CONSTRUCTION_CALCULATORS = [
    {
        "slug": "square-footage",
        "category": "construction",
        "name": "Square Footage & Area Calculator",
        "description": "Calculate square footage for single rooms, multi-room floorplans, and landscaping with perimeter and area conversion.",
        "hero_badge": "Construction Math • Precision Area Solver",
        "formula_display": "Square Footage = Length (ft) × Width (ft)",
        "fields": [
            {"id": "length", "label": "Length", "default": 20, "suffix": "ft", "min": 1, "max": 1000, "step": 0.5, "hint": "Length of the area in feet"},
            {"id": "width", "label": "Width", "default": 15, "suffix": "ft", "min": 1, "max": 1000, "step": 0.5, "hint": "Width of the area in feet"},
            {"id": "cost_per_sqft", "label": "Material Cost per Sq Ft", "default": 4.50, "prefix": "$", "min": 0, "max": 500, "step": 0.25, "hint": "Optional material or flooring cost"}
        ],
        "metrics": [
            {"id": "total_sqft", "label": "Total Square Footage", "default_display": "300.0 sq ft", "highlight": True},
            {"id": "square_yards", "label": "Square Yards", "default_display": "33.3 sq yd"},
            {"id": "perimeter", "label": "Total Perimeter", "default_display": "70.0 linear ft"},
            {"id": "total_cost", "label": "Estimated Material Cost", "default_display": "$1,350.00"}
        ],
        "proof_steps": [
            {"step_title": "Quadrilateral Area Formula", "step_text": "Area of a rectangular surface is given by A = L × W. For non-rectangular zones, divide into composite rectangles and sum the partial areas."},
            {"step_title": "Square Yards Dimensional Conversion", "step_text": "Since 1 yard = 3 feet, 1 square yard = 9 square feet. Therefore: Area (sq yd) = Area (sq ft) / 9."},
            {"step_title": "Linear Perimeter Derivation", "step_text": "Perimeter around the boundary is P = 2(L + W), providing baseboard, framing, or fencing material requirements."}
        ],
        "faqs": [
            {"q": "How do I calculate square footage for an L-shaped room?", "a": "Split the L-shape into two separate rectangles, calculate L × W for each section individually, and add the two square footages together."},
            {"q": "How much extra material should I order for waste?", "a": "Standard practice is to order 10% extra for standard square rooms, and 15% for diagonal installations, herringbone layouts, or rooms with multiple closets."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const cost = getNum('cost_per_sqft');
          const sqft = L * W;
          const sqyd = sqft / 9;
          const perim = 2 * (L + W);
          const totalCost = sqft * cost;

          setDisp('total_sqft', sqft.toFixed(1) + ' sq ft');
          setDisp('square_yards', sqyd.toFixed(1) + ' sq yd');
          setDisp('perimeter', perim.toFixed(1) + ' linear ft');
          setDisp('total_cost', '$' + totalCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));
        """
    },
    {
        "slug": "concrete-slab",
        "category": "construction",
        "name": "Concrete Slab & Footing Volume Calculator",
        "description": "Calculate cubic yards of ready-mix concrete, 60lb/80lb bag counts, and estimated cost for slabs, footings, and driveways.",
        "hero_badge": "Ready-Mix Concrete • Volume & Bag Matrix",
        "formula_display": "Cubic Yards = [Length (ft) × Width (ft) × (Thickness (in) / 12)] / 27",
        "fields": [
            {"id": "length", "label": "Slab Length", "default": 24, "suffix": "ft", "min": 1, "max": 200, "step": 1, "hint": "Length of concrete slab in feet"},
            {"id": "width", "label": "Slab Width", "default": 12, "suffix": "ft", "min": 1, "max": 200, "step": 1, "hint": "Width of concrete slab in feet"},
            {"id": "thickness", "label": "Thickness", "default": 4, "suffix": "in", "min": 2, "max": 24, "step": 0.5, "hint": "Slab thickness in inches (4in typical for patios/driveways)"},
            {"id": "waste", "label": "Waste & Spillage Factor", "default": 10, "suffix": "%", "min": 0, "max": 25, "step": 1, "hint": "Standard margin for uneven excavation and spillage"}
        ],
        "metrics": [
            {"id": "cubic_yards", "label": "Required Ready-Mix Concrete", "default_display": "3.91 cu yd", "highlight": True},
            {"id": "cubic_feet", "label": "Total Volume", "default_display": "105.6 cu ft"},
            {"id": "bags_80lb", "label": "80 lb Pre-Mix Bags", "default_display": "176 bags"},
            {"id": "bags_60lb", "label": "60 lb Pre-Mix Bags", "default_display": "235 bags"}
        ],
        "proof_steps": [
            {"step_title": "Dimensional Volumetric Conversion", "step_text": "Convert slab thickness from inches to feet: h_ft = thickness / 12. Volume in cubic feet is V_cf = L × W × h_ft."},
            {"step_title": "Cubic Yards Derivation", "step_text": "One cubic yard contains 3 × 3 × 3 = 27 cubic feet: V_cy = V_cf / 27."},
            {"step_title": "Waste Adjustment and Bag Factorization", "step_text": "Total ordered volume includes waste factor: V_total = V_cy · (1 + waste/100). One 80lb bag yields ~0.60 cu ft, and one 60lb bag yields ~0.45 cu ft."}
        ],
        "faqs": [
            {"q": "When should I order ready-mix truck delivery vs buying bags?", "a": "Generally, if your project requires more than 1 cubic yard (approx. 45 to 60 bags of 80lb concrete), ordering a ready-mix concrete delivery truck is significantly faster, more consistent, and less labor-intensive."},
            {"q": "What thickness should a patio slab be?", "a": "A standard residential concrete patio or walkway should be 4 inches thick. For vehicle parking or heavy equipment, 5 to 6 inches with reinforcement rebar is recommended."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const th = getNum('thickness') / 12;
          const waste = 1 + (getNum('waste') / 100);
          const cuft = L * W * th * waste;
          const cuyd = cuft / 27;
          const bags80 = Math.ceil(cuft / 0.60);
          const bags60 = Math.ceil(cuft / 0.45);

          setDisp('cubic_yards', cuyd.toFixed(2) + ' cu yd');
          setDisp('cubic_feet', cuft.toFixed(1) + ' cu ft');
          setDisp('bags_80lb', bags80 + ' bags');
          setDisp('bags_60lb', bags60 + ' bags');
        """
    },
    {
        "slug": "paint-coverage",
        "category": "construction",
        "name": "Paint Coverage & Gallons Calculator",
        "description": "Calculate exact paint gallons and primer requirements for walls and ceilings minus window and door cutouts.",
        "hero_badge": "Painting & Coatings • Coverage Matrix",
        "formula_display": "Gallons = [(Total Wall Area - Cutouts) × Number of Coats] / 350 sq ft",
        "fields": [
            {"id": "room_length", "label": "Room Length", "default": 14, "suffix": "ft", "min": 1, "max": 100, "step": 1, "hint": "Room length in feet"},
            {"id": "room_width", "label": "Room Width", "default": 12, "suffix": "ft", "min": 1, "max": 100, "step": 1, "hint": "Room width in feet"},
            {"id": "ceiling_height", "label": "Ceiling Height", "default": 9, "suffix": "ft", "min": 6, "max": 20, "step": 0.5, "hint": "Height from floor to ceiling"},
            {"id": "doors", "label": "Number of Doors", "default": 2, "min": 0, "max": 10, "step": 1, "hint": "Standard doors subtract ~21 sq ft each"},
            {"id": "windows", "label": "Number of Windows", "default": 2, "min": 0, "max": 20, "step": 1, "hint": "Standard windows subtract ~15 sq ft each"},
            {"id": "coats", "label": "Number of Coats", "default": 2, "min": 1, "max": 4, "step": 1, "hint": "Two coats recommended for full coverage"}
        ],
        "metrics": [
            {"id": "gallons_needed", "label": "Paint Gallons Needed", "default_display": "2.4 gal (3 cans)", "highlight": True},
            {"id": "net_wall_area", "label": "Net Paintable Surface", "default_display": "396.0 sq ft"},
            {"id": "primer_needed", "label": "Primer Needed (1 Coat)", "default_display": "1.2 gal"},
            {"id": "total_coverage_area", "label": "Total Multi-Coat Area", "default_display": "792.0 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Gross Wall Surface Area", "step_text": "Total gross perimeter wall area is A_gross = 2 × (Length + Width) × Height."},
            {"step_title": "Cutout Deductions", "step_text": "Deduct window and door openings: A_cutouts = (doors × 21) + (windows × 15). Net paintable wall area is A_net = A_gross - A_cutouts."},
            {"step_title": "Gallon Consumption Model", "step_text": "One standard gallon covers approximately 350 to 400 square feet. Gallons required = (A_net × coats) / 350."}
        ],
        "faqs": [
            {"q": "How many square feet does 1 gallon of paint cover?", "a": "A standard gallon of latex interior paint covers between 350 and 400 square feet on smooth, primed walls. Textured or porous drywall may reduce coverage to 300 sq ft."},
            {"q": "Do I need primer if my paint includes primer?", "a": "For bare drywall, patched areas, or dramatic color shifts (e.g. dark red to white), a dedicated high-hide stain-blocking primer is strongly recommended."}
        ],
        "js_logic": """
          const L = getNum('room_length');
          const W = getNum('room_width');
          const H = getNum('ceiling_height');
          const doors = getNum('doors');
          const windows = getNum('windows');
          const coats = getNum('coats');

          const grossArea = 2 * (L + W) * H;
          const cutoutArea = (doors * 21) + (windows * 15);
          const netArea = Math.max(0, grossArea - cutoutArea);
          const totalArea = netArea * coats;
          const gallons = totalArea / 350;
          const cans = Math.ceil(gallons);
          const primer = netArea / 350;

          setDisp('gallons_needed', gallons.toFixed(1) + ' gal (' + cans + ' cans)');
          setDisp('net_wall_area', netArea.toFixed(1) + ' sq ft');
          setDisp('primer_needed', primer.toFixed(1) + ' gal');
          setDisp('total_coverage_area', totalArea.toFixed(1) + ' sq ft');
        """
    },
    {
        "slug": "flooring",
        "category": "construction",
        "name": "Flooring & Tile Quantity Calculator",
        "description": "Calculate hardwood planks, laminate, vinyl plank (LVP), and ceramic tile boxes with waste allowance.",
        "hero_badge": "Flooring Solutions • Waste & Box Matrix",
        "formula_display": "Total Ordered Sq Ft = Room Area × (1 + Waste Percentage / 100)",
        "fields": [
            {"id": "length", "label": "Room Length", "default": 18, "suffix": "ft", "min": 1, "max": 100, "step": 0.5, "hint": "Room length in feet"},
            {"id": "width", "label": "Room Width", "default": 14, "suffix": "ft", "min": 1, "max": 100, "step": 0.5, "hint": "Room width in feet"},
            {"id": "box_coverage", "label": "Coverage per Box", "default": 24, "suffix": "sq ft", "min": 5, "max": 60, "step": 0.5, "hint": "Manufacturer square feet per box"},
            {"id": "waste_pct", "label": "Waste Percentage", "default": 10, "suffix": "%", "min": 0, "max": 25, "step": 1, "hint": "10% for straight lay, 15% for herringbone/diagonal"}
        ],
        "metrics": [
            {"id": "boxes_needed", "label": "Total Boxes to Purchase", "default_display": "12 boxes", "highlight": True},
            {"id": "net_sqft", "label": "Net Room Area", "default_display": "252.0 sq ft"},
            {"id": "gross_sqft", "label": "Gross Ordered Area", "default_display": "277.2 sq ft"},
            {"id": "actual_coverage", "label": "Purchased Box Coverage", "default_display": "288.0 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Net Area Calculation", "step_text": "Room area A_net = Length × Width."},
            {"step_title": "Waste Allowance Integration", "step_text": "End cuts, mistakes, and awkward room borders require additional material: A_gross = A_net · (1 + waste/100)."},
            {"step_title": "Box Quantization", "step_text": "Flooring is sold strictly by whole unopened cartons: Boxes = ceil(A_gross / box_coverage)."}
        ],
        "faqs": [
            {"q": "Why is 10% waste recommended for flooring?", "a": "Planks cut at the end of every row often cannot be reused if the off-cut is shorter than the manufacturer minimum stagger length (typically 8 to 12 inches)."},
            {"q": "Should I keep extra boxes after installation?", "a": "Yes, always keep at least one full extra box of your dye lot and run number for future repairs due to water damage or heavy impacts."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const cov = getNum('box_coverage');
          const waste = 1 + (getNum('waste_pct') / 100);

          const net = L * W;
          const gross = net * waste;
          const boxes = Math.ceil(gross / (cov || 1));
          const actualCov = boxes * cov;

          setDisp('boxes_needed', boxes + ' boxes');
          setDisp('net_sqft', net.toFixed(1) + ' sq ft');
          setDisp('gross_sqft', gross.toFixed(1) + ' sq ft');
          setDisp('actual_coverage', actualCov.toFixed(1) + ' sq ft');
        """
    },
    {
        "slug": "drywall",
        "category": "construction",
        "name": "Drywall Sheet & Joint Compound Calculator",
        "description": "Calculate 4×8 and 4×12 drywall panels, joint compound buckets, drywall screws, and paper joint tape.",
        "hero_badge": "Drywall & Sheetrock • Wall & Ceiling Matrix",
        "formula_display": "Sheets = (Total Wall Area + Ceiling Area) / Sheet Area",
        "fields": [
            {"id": "length", "label": "Room Length", "default": 16, "suffix": "ft", "min": 1, "max": 100, "step": 1, "hint": "Room length in feet"},
            {"id": "width", "label": "Room Width", "default": 12, "suffix": "ft", "min": 1, "max": 100, "step": 1, "hint": "Room width in feet"},
            {"id": "height", "label": "Ceiling Height", "default": 8, "suffix": "ft", "min": 7, "max": 16, "step": 0.5, "hint": "Floor to ceiling height"},
            {"id": "sheet_size", "label": "Sheet Type (32 for 4×8, 48 for 4×12)", "default": 32, "suffix": "sq ft", "min": 32, "max": 48, "step": 16, "hint": "4×8 sheet = 32 sq ft; 4×12 sheet = 48 sq ft"}
        ],
        "metrics": [
            {"id": "sheets_needed", "label": "Drywall Sheets Needed", "default_display": "22 sheets", "highlight": True},
            {"id": "total_area", "label": "Total Surface (Walls + Ceiling)", "default_display": "640.0 sq ft"},
            {"id": "compound_pails", "label": "Joint Compound (4.5 Gal Pails)", "default_display": "2 pails"},
            {"id": "screws_count", "label": "Drywall Screws (1-1/4\")", "default_display": "704 screws (1.5 lbs)"}
        ],
        "proof_steps": [
            {"step_title": "Total Enclosing Envelope Area", "step_text": "Wall area = 2 × (L + W) × H. Ceiling area = L × W. Total area = Wall area + Ceiling area."},
            {"step_title": "Sheet Yield and Waste Factor", "step_text": "With a standard 10% cutting waste factor, Sheets = ceil[(Total Area × 1.10) / Sheet Size]."},
            {"step_title": "Fasteners and Mud Consumables", "step_text": "Drywall sheets require approximately 32 screws per 4×8 panel (~12\" edge and 16\" field spacing). Mud consumes ~0.053 gallons per square foot."}
        ],
        "faqs": [
            {"q": "Should I use 4×8 or 4×12 drywall panels?", "a": "4×12 panels produce 33% fewer butt joints, resulting in faster taping and smoother finishes. However, 4×12 panels are heavier (~75 lbs) and require two people to lift."},
            {"q": "Should drywall be installed horizontally or vertically on walls?", "a": "In residential construction, hanging panels horizontally across studs increases shear strength and places seams at a convenient 4-foot height for taping."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const H = getNum('height');
          const sheetSize = getNum('sheet_size') || 32;

          const wallArea = 2 * (L + W) * H;
          const ceilingArea = L * W;
          const totalArea = wallArea + ceilingArea;
          const sheets = Math.ceil((totalArea * 1.10) / sheetSize);
          const compoundGal = totalArea * 0.053;
          const pails = Math.ceil(compoundGal / 4.5);
          const screws = sheets * 32;

          setDisp('sheets_needed', sheets + ' sheets');
          setDisp('total_area', totalArea.toFixed(1) + ' sq ft');
          setDisp('compound_pails', pails + ' pails (' + compoundGal.toFixed(1) + ' gal)');
          setDisp('screws_count', screws + ' screws (~' + (screws / 450).toFixed(1) + ' lbs)');
        """
    },
    {
        "slug": "gravel",
        "category": "construction",
        "name": "Gravel & Crushed Stone Tonnage Calculator",
        "description": "Calculate cubic yards and metric/US tons of gravel, crush-and-run, or pea gravel for driveways, bases, and drainage.",
        "hero_badge": "Civil Engineering • Aggregate Tonnage Matrix",
        "formula_display": "Tons = [Cubic Yards × 1.4 Tons/cu yd]",
        "fields": [
            {"id": "length", "label": "Driveway / Area Length", "default": 50, "suffix": "ft", "min": 1, "max": 1000, "step": 1, "hint": "Length in feet"},
            {"id": "width", "label": "Driveway / Area Width", "default": 10, "suffix": "ft", "min": 1, "max": 100, "step": 0.5, "hint": "Width in feet"},
            {"id": "depth", "label": "Gravel Depth", "default": 4, "suffix": "in", "min": 1, "max": 24, "step": 0.5, "hint": "Compacted layer depth in inches"},
            {"id": "density", "label": "Aggregate Density", "default": 1.4, "suffix": "tons/yd³", "min": 1.1, "max": 1.8, "step": 0.05, "hint": "Crushed limestone ~1.4 tons/yd³"}
        ],
        "metrics": [
            {"id": "tons_needed", "label": "Gravel Required", "default_display": "8.64 tons", "highlight": True},
            {"id": "cubic_yards", "label": "Volume (Cubic Yards)", "default_display": "6.17 cu yd"},
            {"id": "cubic_feet", "label": "Volume (Cubic Feet)", "default_display": "166.7 cu ft"},
            {"id": "tandem_loads", "label": "Tandem Dump Truck Loads (~14t)", "default_display": "1 truckload"}
        ],
        "proof_steps": [
            {"step_title": "Geometric Volumetric Integral", "step_text": "V_cf = Length (ft) × Width (ft) × [Depth (in) / 12]. Cubic yards V_cy = V_cf / 27."},
            {"step_title": "Density Gravimetric Conversion", "step_text": "Aggregate tonnage: T = V_cy × Density. Dense graded aggregate typically weighs ~2,800 lbs per cubic yard (1.4 US tons)."},
            {"step_title": "Compaction Settling Variable", "step_text": "Vibrated crush-and-run aggregate settles approximately 15% to 20% under a plate compactor roller."}
        ],
        "faqs": [
            {"q": "How deep should a gravel driveway be?", "a": "A proper gravel driveway consists of 8 to 12 inches total: 4 to 6 inches of coarse #3 or #4 ballast base stone, followed by 4 inches of crushed stone (#57 or ABC crush-and-run)."},
            {"q": "How many tons of gravel fit in a tri-axle dump truck?", "a": "A standard tri-axle dump truck typically hauls 18 to 22 tons of aggregate, while a standard tandem dump truck carries 12 to 14 tons."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const D = getNum('depth') / 12;
          const dens = getNum('density') || 1.4;

          const cuft = L * W * D;
          const cuyd = cuft / 27;
          const tons = cuyd * dens;
          const trucks = Math.ceil(tons / 14);

          setDisp('tons_needed', tons.toFixed(2) + ' tons');
          setDisp('cubic_yards', cuyd.toFixed(2) + ' cu yd');
          setDisp('cubic_feet', cuft.toFixed(1) + ' cu ft');
          setDisp('tandem_loads', trucks + (trucks === 1 ? ' truckload' : ' truckloads'));
        """
    },
    {
        "slug": "mulch",
        "category": "construction",
        "name": "Mulch & Soil Volume Calculator",
        "description": "Calculate cubic yards and 2 cu ft / 3 cu ft bag counts of hardwood bark mulch or garden topsoil for landscape beds.",
        "hero_badge": "Landscaping • Landscape Mulch Matrix",
        "formula_display": "Cubic Yards = [Bed Area (sq ft) × Depth (in)] / 324",
        "fields": [
            {"id": "bed_area", "label": "Total Garden Bed Area", "default": 450, "suffix": "sq ft", "min": 10, "max": 10000, "step": 10, "hint": "Combined area of garden beds"},
            {"id": "mulch_depth", "label": "Mulch Depth", "default": 3, "suffix": "in", "min": 1, "max": 6, "step": 0.5, "hint": "2-3 inches recommended for weed control"}
        ],
        "metrics": [
            {"id": "cubic_yards", "label": "Bulk Mulch (Cubic Yards)", "default_display": "4.17 cu yd", "highlight": True},
            {"id": "bags_2cuft", "label": "Standard 2 cu ft Bags", "default_display": "57 bags"},
            {"id": "bags_3cuft", "label": "Large 3 cu ft Bags", "default_display": "38 bags"},
            {"id": "truck_beds", "label": "Pickup Truck Beds (~2 cu yd)", "default_display": "3 loads"}
        ],
        "proof_steps": [
            {"step_title": "Dimensional Divisor Derivation", "step_text": "One cubic yard = 27 cu ft = 27 × 12 = 324 board-feet. Therefore, 1 cubic yard covers exactly 324 square feet at 1 inch depth."},
            {"step_title": "Cubic Yardage Formula", "step_text": "Cubic Yards = (Area × Depth_inches) / 324."},
            {"step_title": "Retail Bag Equivalence", "step_text": "Since 1 cubic yard = 27 cubic feet: 2 cu ft bags = ceil(cuft / 2), and 3 cu ft bags = ceil(cuft / 3)."}
        ],
        "faqs": [
            {"q": "How deep should mulch be applied?", "a": "A 3-inch depth is optimal for suppressing weeds and retaining soil moisture. Mulch deeper than 4 inches can starve plant roots of oxygen and create fungal buildup."},
            {"q": "When is bulk mulch cheaper than bags?", "a": "Bulk delivery is typically economical when you need 3 or more cubic yards (approx. 40+ bags). Under 2 cubic yards, retail bagged mulch is often more convenient."}
        ],
        "js_logic": """
          const area = getNum('bed_area');
          const depth = getNum('mulch_depth');
          const cuyd = (area * depth) / 324;
          const cuft = cuyd * 27;
          const b2 = Math.ceil(cuft / 2);
          const b3 = Math.ceil(cuft / 3);
          const trucks = Math.ceil(cuyd / 2);

          setDisp('cubic_yards', cuyd.toFixed(2) + ' cu yd');
          setDisp('bags_2cuft', b2 + ' bags');
          setDisp('bags_3cuft', b3 + ' bags');
          setDisp('truck_beds', trucks + ' pickup loads');
        """
    },
    {
        "slug": "pavers",
        "category": "construction",
        "name": "Patio Paver & Polymeric Sand Calculator",
        "description": "Calculate stone pavers, bedding sand, crushed stone base, and joint sand requirements for patios and walkways.",
        "hero_badge": "Hardscaping • Paver & Base Solver",
        "formula_display": "Paver Units = Area (sq ft) / Paver Area (sq ft) × 1.10",
        "fields": [
            {"id": "length", "label": "Patio Length", "default": 20, "suffix": "ft", "min": 2, "max": 100, "step": 1, "hint": "Length of paver patio in feet"},
            {"id": "width", "label": "Patio Width", "default": 15, "suffix": "ft", "min": 2, "max": 100, "step": 1, "hint": "Width of paver patio in feet"},
            {"id": "paver_length", "label": "Paver Unit Length", "default": 8, "suffix": "in", "min": 4, "max": 24, "step": 1, "hint": "Paver length in inches"},
            {"id": "paver_width", "label": "Paver Unit Width", "default": 4, "suffix": "in", "min": 4, "max": 24, "step": 1, "hint": "Paver width in inches"}
        ],
        "metrics": [
            {"id": "pavers_count", "label": "Pavers to Order (10% Waste)", "default_display": "1,485 pavers", "highlight": True},
            {"id": "bedding_sand", "label": "1\" Bedding Sand (cu yd)", "default_display": "0.93 cu yd"},
            {"id": "base_gravel", "label": "4\" Crushed Base Gravel (tons)", "default_display": "5.19 tons"},
            {"id": "polymeric_sand", "label": "Polymeric Sand (50 lb Bags)", "default_display": "3 bags"}
        ],
        "proof_steps": [
            {"step_title": "Paver Surface Area", "step_text": "Single paver area A_p = (paver_length × paver_width) / 144 sq ft."},
            {"step_title": "Total Unit Count with Cutting Waste", "step_text": "Units = ceil[(Patio Area / A_p) × 1.10]. The 10% allowance covers perimeter split cutting."},
            {"step_title": "Sub-Base Stratification", "step_text": "ICPI standards mandate: 4 inches compacted road base gravel (#21A) + 1 inch uncompacted concrete sand bedding."}
        ],
        "faqs": [
            {"q": "Can I use beach sand or fine play sand for paver bedding?", "a": "No. Concrete sand (ASTM C33) has sharp, angular grains that lock together under compaction. Rounded play sand will wash out and cause sinking."},
            {"q": "How many 50 lb bags of polymeric sand do I need?", "a": "One 50 lb bag of polymeric joint sand covers approximately 75 to 100 square feet of standard pavers with narrow (1/8\" to 1/4\") joints."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const pL = getNum('paver_length');
          const pW = getNum('paver_width');

          const area = L * W;
          const paverAreaSqFt = (pL * pW) / 144;
          const units = Math.ceil((area / (paverAreaSqFt || 0.222)) * 1.10);
          const sandCuYd = (area * 1) / 324;
          const gravelTons = ((area * 4) / 324) * 1.4;
          const polyBags = Math.ceil(area / 85);

          setDisp('pavers_count', units.toLocaleString() + ' pavers');
          setDisp('bedding_sand', sandCuYd.toFixed(2) + ' cu yd');
          setDisp('base_gravel', gravelTons.toFixed(2) + ' tons');
          setDisp('polymeric_sand', polyBags + ' bags (50 lb)');
        """
    },
    {
        "slug": "sod-turf",
        "category": "construction",
        "name": "Sod & Turf Pallet Calculator",
        "description": "Calculate sod rolls, square feet, pallet counts, and soil prep requirements for instant lawn turfgrass.",
        "hero_badge": "Turfgrass • Pallet & Roll Matrix",
        "formula_display": "Pallets Needed = [Lawn Sq Ft × 1.05] / Pallet Sq Ft (Typically 450)",
        "fields": [
            {"id": "length", "label": "Lawn Length", "default": 80, "suffix": "ft", "min": 5, "max": 500, "step": 5, "hint": "Lawn length in feet"},
            {"id": "width", "label": "Lawn Width", "default": 40, "suffix": "ft", "min": 5, "max": 500, "step": 5, "hint": "Lawn width in feet"},
            {"id": "pallet_sqft", "label": "Sq Ft per Pallet", "default": 450, "suffix": "sq ft", "min": 400, "max": 500, "step": 10, "hint": "Standard pallet: 450-500 sq ft (50 rolls)"}
        ],
        "metrics": [
            {"id": "pallets_needed", "label": "Pallets to Order (5% Waste)", "default_display": "8 pallets", "highlight": True},
            {"id": "total_sqft", "label": "Total Lawn Surface Area", "default_display": "3,200.0 sq ft"},
            {"id": "sod_rolls", "label": "Individual Rolls (2' × 5')", "default_display": "336 rolls"},
            {"id": "estimated_weight", "label": "Approx. Pallet Weight", "default_display": "16,000 lbs (8.0 tons)"}
        ],
        "proof_steps": [
            {"step_title": "Surface Boundary Area", "step_text": "Net lawn area A = Length × Width."},
            {"step_title": "Cutting Waste Cushion", "step_text": "Add 5% for standard rectilinear lawns (or 10% for curved beds): A_order = A × 1.05."},
            {"step_title": "Pallet Yield Calculation", "step_text": "Pallets = ceil(A_order / pallet_coverage). A typical pallet contains 50 rolls (10 sq ft each = 500 sq ft) and weighs ~2,000 to 2,500 lbs."}
        ],
        "faqs": [
            {"q": "How quickly must fresh sod be installed after delivery?", "a": "Fresh sod should be installed within 24 to 48 hours of harvest. In temperatures exceeding 80°F, pallets heat up from internal composting and must be installed within 12 hours."},
            {"q": "How much does a pallet of sod weigh?", "a": "Depending on soil moisture content, one pallet weighs between 1,800 and 3,000 lbs. Do not attempt to haul a full pallet in a half-ton pickup truck without checking payload limits."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const pSqFt = getNum('pallet_sqft') || 450;

          const area = L * W;
          const gross = area * 1.05;
          const pallets = Math.ceil(gross / pSqFt);
          const rolls = Math.ceil(gross / 10);
          const weightTons = (pallets * 2200) / 2000;

          setDisp('pallets_needed', pallets + ' pallets');
          setDisp('total_sqft', area.toLocaleString() + ' sq ft');
          setDisp('sod_rolls', rolls.toLocaleString() + ' rolls');
          setDisp('estimated_weight', (pallets * 2200).toLocaleString() + ' lbs (' + weightTons.toFixed(1) + ' tons)');
        """
    },
    {
        "slug": "retaining-wall",
        "category": "construction",
        "name": "Retaining Wall Block & Backfill Calculator",
        "description": "Calculate retaining wall blocks, capstones, gravel drainage backfill, and perforated drain tile pipe.",
        "hero_badge": "Structural Masonry • Block & Drainage Matrix",
        "formula_display": "Blocks = [Wall Length (ft) × Wall Height (ft)] / Block Face Area (sq ft)",
        "fields": [
            {"id": "length", "label": "Wall Length", "default": 30, "suffix": "ft", "min": 4, "max": 200, "step": 1, "hint": "Total running length of the retaining wall"},
            {"id": "height", "label": "Exposed Wall Height", "default": 3, "suffix": "ft", "min": 1, "max": 10, "step": 0.5, "hint": "Exposed height above grade (add 1 buried course)"},
            {"id": "block_length", "label": "Block Face Length", "default": 12, "suffix": "in", "min": 8, "max": 18, "step": 1, "hint": "Length of block face in inches"},
            {"id": "block_height", "label": "Block Height", "default": 4, "suffix": "in", "min": 3, "max": 8, "step": 0.5, "hint": "Height of block in inches"}
        ],
        "metrics": [
            {"id": "blocks_needed", "label": "Total Retaining Blocks", "default_display": "315 blocks", "highlight": True},
            {"id": "cap_stones", "label": "Cap Stones (Linear Feet)", "default_display": "30 units (30 ft)"},
            {"id": "drainage_gravel", "label": "Drainage Gravel Backfill (12\" deep)", "default_display": "3.33 cu yd (4.66 tons)"},
            {"id": "drain_pipe", "label": "Perforated 4\" Drain Pipe", "default_display": "30 linear ft"}
        ],
        "proof_steps": [
            {"step_title": "Buried Base Course Consideration", "step_text": "Retaining walls require 1 course buried beneath finished grade for stability: Total Course Height = Height + (block_height / 12)."},
            {"step_title": "Block Face Yield", "step_text": "Block face area A_b = (block_length × block_height) / 144 sq ft. Total Blocks = ceil[(Wall Length × Total Height) / A_b] × 1.05."},
            {"step_title": "Hydrostatic Drainage Calculus", "step_text": "Retaining walls fail due to water pressure. A 12-inch clear gravel drainage chimney is placed behind the wall: V_gravel = Length × Height × 1.0 ft."}
        ],
        "faqs": [
            {"q": "When does a retaining wall require an engineer's stamp?", "a": "Most municipal building codes mandate a stamped civil engineering design for any retaining wall with an exposed height of 4 feet or higher (measured from bottom of footing)."},
            {"q": "What is geogrid and when is it necessary?", "a": "Geogrid is a high-tensile polyester mesh embedded between block courses extending back into compacted soil to reinforce walls over 3 to 4 feet in height."}
        ],
        "js_logic": """
          const L = getNum('length');
          const H = getNum('height');
          const bL = getNum('block_length');
          const bH = getNum('block_height');

          const buriedH = bH / 12;
          const totalH = H + buriedH;
          const blockFaceSqFt = (bL * bH) / 144;
          const totalArea = L * totalH;
          const blocks = Math.ceil((totalArea / (blockFaceSqFt || 0.333)) * 1.05);
          const caps = Math.ceil(L / (bL / 12));
          const gravelCuYd = (L * totalH * 1.0) / 27;
          const gravelTons = gravelCuYd * 1.4;

          setDisp('blocks_needed', blocks + ' blocks');
          setDisp('cap_stones', caps + ' units (' + L + ' ft)');
          setDisp('drainage_gravel', gravelCuYd.toFixed(2) + ' cu yd (' + gravelTons.toFixed(2) + ' tons)');
          setDisp('drain_pipe', L + ' linear ft');
        """
    },
    {
        "slug": "deck-framing",
        "category": "construction",
        "name": "Deck Framing & Joist Spacing Calculator",
        "description": "Calculate pressure-treated floor joists, rim joists, support beams, posts, and decking boards with standard 12\" or 16\" on-center spacing.",
        "hero_badge": "Carpentry & Framing • Deck Structural Matrix",
        "formula_display": "Joist Count = ceil[Deck Width (in) / On-Center Spacing (in)] + 1",
        "fields": [
            {"id": "deck_length", "label": "Deck Length (Along House Ledger)", "default": 16, "suffix": "ft", "min": 6, "max": 50, "step": 1, "hint": "Length along house wall"},
            {"id": "deck_projection", "label": "Deck Projection (Out from House)", "default": 12, "suffix": "ft", "min": 4, "max": 24, "step": 1, "hint": "Distance joists span outwards"},
            {"id": "joist_spacing", "label": "Joist Spacing (On-Center)", "default": 16, "suffix": "in", "min": 12, "max": 24, "step": 4, "hint": "16\" standard for wood; 12\" required for composite decking"},
            {"id": "board_width", "label": "Decking Board Width", "default": 5.5, "suffix": "in", "min": 3.5, "max": 7.5, "step": 0.5, "hint": "Standard 5/4×6 board measures 5.5 inches"}
        ],
        "metrics": [
            {"id": "joist_count", "label": "Floor Joists Required", "default_display": "13 joists (12 ft)", "highlight": True},
            {"id": "decking_boards", "label": "Surface Decking Boards", "default_display": "27 boards (16 ft)", "highlight": True},
            {"id": "support_posts", "label": "6×6 Support Posts (8' max span)", "default_display": "3 posts"},
            {"id": "deck_area", "label": "Deck Surface Area", "default_display": "192.0 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Joist Layout Algorithm", "step_text": "Joists run perpendicular to the ledger board. Number of joists = ceil[(Deck Length × 12) / Spacing] + 1 (for end rim joist)."},
            {"step_title": "Decking Board Quantity", "step_text": "Boards run parallel to the house across joists. Effective board width with 1/8\" gap = 5.625\". Boards = ceil[(Deck Projection × 12) / 5.625]."},
            {"step_title": "Beam Post Support Calculation", "step_text": "Drop beams require 6×6 support posts spaced no more than 8 feet apart under standard 50 psf total load."}
        ],
        "faqs": [
            {"q": "Why is 12-inch joist spacing needed for composite boards?", "a": "Composite decking (Trex, TimberTech) has higher flexibility than natural lumber. At 16\" spacing, composite boards will sag or feel bouncy under summer sun."},
            {"q": "What fasteners should be used with pressure-treated lumber?", "a": "Copper preservative chemicals (ACQ, MCQ) in modern pressure-treated wood corrode standard steel. Use hot-dipped galvanized or 304/316 grade stainless steel screws."}
        ],
        "js_logic": """
          const L = getNum('deck_length');
          const P = getNum('deck_projection');
          const space = getNum('joist_spacing') || 16;
          const bW = getNum('board_width') || 5.5;

          const joists = Math.ceil((L * 12) / space) + 1;
          const effBW = bW + 0.125;
          const boards = Math.ceil((P * 12) / effBW);
          const posts = Math.ceil(L / 8) + 1;
          const area = L * P;

          setDisp('joist_count', joists + ' joists (' + P + ' ft)');
          setDisp('decking_boards', boards + ' boards (' + L + ' ft)');
          setDisp('support_posts', posts + ' posts (6×6)');
          setDisp('deck_area', area.toFixed(1) + ' sq ft');
        """
    },
    {
        "slug": "fence-post",
        "category": "construction",
        "name": "Fence Post, Rail & Picket Calculator",
        "description": "Calculate 4×4 posts, 2×4 horizontal rails, dog-ear pickets, and quick-set concrete bags for privacy and picket fences.",
        "hero_badge": "Fencing Solutions • Post & Picket Matrix",
        "formula_display": "Posts = ceil[Fence Length / Post Spacing] + 1",
        "fields": [
            {"id": "fence_length", "label": "Total Fence Perimeter", "default": 120, "suffix": "ft", "min": 8, "max": 1000, "step": 8, "hint": "Total running length of fencing"},
            {"id": "post_spacing", "label": "Post Spacing (On-Center)", "default": 8, "suffix": "ft", "min": 6, "max": 10, "step": 1, "hint": "8 ft standard, 6 ft for high-wind zones"},
            {"id": "picket_width", "label": "Picket Face Width", "default": 5.5, "suffix": "in", "min": 3.5, "max": 6, "step": 0.5, "hint": "Standard 1×6 picket measures 5.5 inches wide"},
            {"id": "rails_per_section", "label": "Horizontal Rails per Section", "default": 3, "min": 2, "max": 4, "step": 1, "hint": "3 rails standard for 6ft privacy fence"}
        ],
        "metrics": [
            {"id": "posts_count", "label": "4×4 Posts Needed", "default_display": "16 posts", "highlight": True},
            {"id": "rails_count", "label": "2×4 Horizontal Rails", "default_display": "45 rails (8 ft)"},
            {"id": "pickets_count", "label": "Fence Pickets (5% Waste)", "default_display": "275 pickets"},
            {"id": "concrete_bags", "label": "Fast-Setting Concrete (50 lb)", "default_display": "32 bags (2 per hole)"}
        ],
        "proof_steps": [
            {"step_title": "Post Interval Derivation", "step_text": "Number of sections = ceil(Fence Length / Post Spacing). Number of posts = Sections + 1 (plus 1 additional post per gate)."},
            {"step_title": "Rail Count Formula", "step_text": "Total 2×4 rails = Sections × Rails per section."},
            {"step_title": "Picket Density Calculation", "step_text": "Pickets = ceil[(Fence Length × 12) / Picket Width] × 1.05 for solid privacy fencing."}
        ],
        "faqs": [
            {"q": "How deep should fence post holes be dug?", "a": "Fence post holes must be dug to a minimum depth of one-third the total post height (typically 24 to 36 inches), or below your local municipal frost line to prevent winter heaving."},
            {"q": "How many bags of concrete are needed per post?", "a": "For a standard 4×4 post in a 9-inch diameter hole, use two 50 lb bags of fast-setting concrete mix."}
        ],
        "js_logic": """
          const L = getNum('fence_length');
          const S = getNum('post_spacing') || 8;
          const pW = getNum('picket_width') || 5.5;
          const railsPerSec = getNum('rails_per_section') || 3;

          const sections = Math.ceil(L / S);
          const posts = sections + 1;
          const rails = sections * railsPerSec;
          const pickets = Math.ceil(((L * 12) / pW) * 1.05);
          const concrete = posts * 2;

          setDisp('posts_count', posts + ' posts');
          setDisp('rails_count', rails + ' rails (' + S + ' ft)');
          setDisp('pickets_count', pickets + ' pickets');
          setDisp('concrete_bags', concrete + ' bags (2/hole)');
        """
    },
    {
        "slug": "asphalt-driveway",
        "category": "construction",
        "name": "Asphalt Driveway Tonnage & Cost Calculator",
        "description": "Calculate hot mix asphalt (HMA) tonnage, square footage, and paving crew material costs for driveways and parking lots.",
        "hero_badge": "Civil Paving • Hot Mix Asphalt Matrix",
        "formula_display": "Asphalt Tons = [Area (sq ft) × Depth (in) × 110 lbs/sq yd/in] / 2,000",
        "fields": [
            {"id": "length", "label": "Driveway Length", "default": 60, "suffix": "ft", "min": 10, "max": 1000, "step": 5, "hint": "Length of driveway in feet"},
            {"id": "width", "label": "Driveway Width", "default": 12, "suffix": "ft", "min": 8, "max": 100, "step": 1, "hint": "Width of driveway in feet"},
            {"id": "depth", "label": "Compacted Asphalt Thickness", "default": 2.5, "suffix": "in", "min": 1.5, "max": 6, "step": 0.5, "hint": "2.5 to 3 inches typical for residential driveways"},
            {"id": "cost_per_ton", "label": "Hot Mix Cost per Ton", "default": 95, "prefix": "$", "min": 50, "max": 200, "step": 5, "hint": "Local asphalt plant FOB / delivered price"}
        ],
        "metrics": [
            {"id": "asphalt_tons", "label": "Hot Mix Asphalt Required", "default_display": "11.00 tons", "highlight": True},
            {"id": "surface_area", "label": "Surface Area", "default_display": "720.0 sq ft"},
            {"id": "material_cost", "label": "Estimated Material Cost", "default_display": "$1,045.00"},
            {"id": "dump_truck_loads", "label": "Tri-Axle Delivery Loads (~20t)", "default_display": "1 truckload"}
        ],
        "proof_steps": [
            {"step_title": "Square Yardage Transformation", "step_text": "Area in square yards: A_sy = (Length × Width) / 9."},
            {"step_title": "Asphalt Paving Density Constant", "step_text": "Compact hot mix asphalt weighs approximately 110 lbs per square yard per inch of thickness (145 lbs/cu ft)."},
            {"step_title": "Tonnage Derivation", "step_text": "Tons = (A_sy × Depth_in × 110) / 2000. Add 5% for edge tamping compaction margin."}
        ],
        "faqs": [
            {"q": "What is the minimum recommended asphalt thickness for a home driveway?", "a": "A residential driveway requires a minimum of 2.5 to 3 inches of compacted asphalt over a 6 to 8 inch compacted aggregate base (crush-and-run)."},
            {"q": "How long after paving can I park cars on new asphalt?", "a": "You can walk on new asphalt within 24 hours, but wait 3 to 5 full days before parking passenger vehicles, and avoid turning wheels while stationary."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const D = getNum('depth');
          const price = getNum('cost_per_ton') || 95;

          const sqft = L * W;
          const sqyd = sqft / 9;
          const tons = ((sqyd * D * 110) / 2000) * 1.05;
          const cost = tons * price;
          const loads = Math.ceil(tons / 20);

          setDisp('asphalt_tons', tons.toFixed(2) + ' tons');
          setDisp('surface_area', sqft.toFixed(1) + ' sq ft (' + sqyd.toFixed(1) + ' sq yd)');
          setDisp('material_cost', '$' + Math.round(cost).toLocaleString());
          setDisp('dump_truck_loads', loads + ' truckload');
        """
    },
    {
        "slug": "brick-mortar",
        "category": "construction",
        "name": "Brick & Mortar Quantity Calculator",
        "description": "Calculate modular, standard, and queen brick quantities plus Type N or Type S mortar bags for brick masonry walls.",
        "hero_badge": "Masonry Infrastructure • Brick & Mortar Matrix",
        "formula_display": "Modular Bricks = Wall Area (sq ft) × 6.85 Bricks/sq ft",
        "fields": [
            {"id": "wall_length", "label": "Wall Length", "default": 20, "suffix": "ft", "min": 2, "max": 200, "step": 1, "hint": "Length of brick wall in feet"},
            {"id": "wall_height", "label": "Wall Height", "default": 8, "suffix": "ft", "min": 1, "max": 30, "step": 0.5, "hint": "Height of brick wall in feet"},
            {"id": "brick_type", "label": "Bricks per Sq Ft (6.85 Modular, 5.76 Queen)", "default": 6.85, "min": 4.5, "max": 8, "step": 0.1, "hint": "Standard modular brick = 6.85 units/sq ft with 3/8\" joint"}
        ],
        "metrics": [
            {"id": "bricks_needed", "label": "Bricks to Order (5% Waste)", "default_display": "1,151 bricks", "highlight": True},
            {"id": "wall_area", "label": "Total Wall Face Area", "default_display": "160.0 sq ft"},
            {"id": "mortar_bags", "label": "80 lb Mortar Bags (Type N)", "default_display": "8 bags (1 per 140 bricks)"},
            {"id": "masonry_sand", "label": "Masonry Sand Required", "default_display": "0.77 tons"}
        ],
        "proof_steps": [
            {"step_title": "Wall Surface Calculation", "step_text": "Wall Face Area A = Wall Length × Wall Height."},
            {"step_title": "Brick Density with Standard 3/8\" Mortar Joint", "step_text": "A standard modular brick (3-5/8\" × 2-1/4\" × 7-5/8\") with 3/8\" joint yields 6.85 bricks per square foot: Bricks = ceil[A × 6.85 × 1.05]."},
            {"step_title": "Mortar Consumption Heuristic", "step_text": "One 80 lb bag of pre-mixed masonry mortar lays approximately 125 to 140 modular bricks."}
        ],
        "faqs": [
            {"q": "What is the difference between Type N and Type S mortar?", "a": "Type N mortar (medium strength, ~750 psi) is ideal for exterior above-grade brick veneer. Type S mortar (high strength, ~1,800 psi) is required for below-grade foundations or structural walls."},
            {"q": "How many bricks come on a standard delivery cube/pallet?", "a": "A standard brick pallet (cube) contains 500 to 525 modular bricks and weighs approximately 2,000 to 2,400 lbs."}
        ],
        "js_logic": """
          const L = getNum('wall_length');
          const H = getNum('wall_height');
          const rate = getNum('brick_type') || 6.85;

          const area = L * H;
          const bricks = Math.ceil(area * rate * 1.05);
          const bags = Math.ceil(bricks / 140);
          const sandTons = (bags * 80 * 3) / 2000;

          setDisp('bricks_needed', bricks.toLocaleString() + ' bricks');
          setDisp('wall_area', area.toFixed(1) + ' sq ft');
          setDisp('mortar_bags', bags + ' bags (80 lb)');
          setDisp('masonry_sand', sandTons.toFixed(2) + ' tons');
        """
    },
    {
        "slug": "lumber-board-feet",
        "category": "construction",
        "name": "Board Feet (FBM) & Lumber Price Calculator",
        "description": "Calculate board footage (FBM) and total pricing for rough-sawn and dimensional hardwood and softwood lumber.",
        "hero_badge": "Hardwood & Forestry • Board Foot Solver",
        "formula_display": "Board Feet = [Thickness (in) × Width (in) × Length (in)] / 144",
        "fields": [
            {"id": "thickness", "label": "Nominal Thickness", "default": 2, "suffix": "in", "min": 0.5, "max": 16, "step": 0.25, "hint": "Thickness in inches (4/4 = 1\", 8/4 = 2\")"},
            {"id": "width", "label": "Nominal Width", "default": 6, "suffix": "in", "min": 1, "max": 24, "step": 0.5, "hint": "Width in inches"},
            {"id": "length_ft", "label": "Board Length", "default": 10, "suffix": "ft", "min": 1, "max": 30, "step": 0.5, "hint": "Length in feet"},
            {"id": "quantity", "label": "Number of Pieces", "default": 15, "min": 1, "max": 5000, "step": 1, "hint": "Count of identical boards"},
            {"id": "price_per_bf", "label": "Price per Board Foot", "default": 5.25, "prefix": "$", "min": 0.5, "max": 50, "step": 0.25, "hint": "Lumberyard price per FBM"}
        ],
        "metrics": [
            {"id": "total_bf", "label": "Total Board Feet (FBM)", "default_display": "150.0 BF", "highlight": True},
            {"id": "single_bf", "label": "Board Feet per Piece", "default_display": "10.0 BF"},
            {"id": "total_cost", "label": "Total Lumber Cost", "default_display": "$787.50"},
            {"id": "linear_footage", "label": "Total Linear Footage", "default_display": "150.0 linear ft"}
        ],
        "proof_steps": [
            {"step_title": "Board Foot Volume Definition", "step_text": "One board foot equals 144 cubic inches (a 1-inch thick board measuring 12 inches wide by 12 inches long)."},
            {"step_title": "Dimensional Calculation with Length in Feet", "step_text": "BF = [Thickness (in) × Width (in) × Length (ft)] / 12."},
            {"step_title": "Monetary Tally", "step_text": "Total Board Feet = BF_single × Quantity. Total Order Price = Total Board Feet × Price per BF."}
        ],
        "faqs": [
            {"q": "What is the difference between nominal and actual lumber dimensions?", "a": "Nominal lumber is named before surfacing and kiln-drying. A nominal 2×4 actually measures 1.5\" × 3.5\". In rough-sawn hardwood lumber, board footage is computed using nominal rough dimensions."},
            {"q": "What does 4/4 and 8/4 mean in hardwood lumber?", "a": "Hardwood mills express thickness in quarters of an inch: 4/4 is 1 inch thick, 5/4 is 1.25 inches, 6/4 is 1.5 inches, and 8/4 is 2.0 inches thick."}
        ],
        "js_logic": """
          const T = getNum('thickness');
          const W = getNum('width');
          const L_ft = getNum('length_ft');
          const qty = getNum('quantity') || 1;
          const price = getNum('price_per_bf');

          const singleBF = (T * W * L_ft) / 12;
          const totalBF = singleBF * qty;
          const totalCost = totalBF * price;
          const totalLinear = L_ft * qty;

          setDisp('total_bf', totalBF.toFixed(1) + ' BF');
          setDisp('single_bf', singleBF.toFixed(1) + ' BF');
          setDisp('total_cost', '$' + totalCost.toFixed(2));
          setDisp('linear_footage', totalLinear.toFixed(1) + ' linear ft');
        """
    },
    {
        "slug": "roofing-shingles",
        "category": "construction",
        "name": "Roofing Shingles & Bundles Calculator",
        "description": "Calculate roofing squares, 3-tab and architectural shingle bundles, underlayment rolls, and roof pitch multiplier.",
        "hero_badge": "Roofing Systems • Pitch & Shingle Matrix",
        "formula_display": "Roofing Squares = [Footprint Sq Ft × Pitch Multiplier] / 100",
        "fields": [
            {"id": "footprint_area", "label": "Building Ground Footprint", "default": 2000, "suffix": "sq ft", "min": 200, "max": 15000, "step": 50, "hint": "Horizontal ground footprint including roof overhangs"},
            {"id": "pitch", "label": "Roof Slope (Rise per 12\" Run)", "default": 6, "suffix": "/12", "min": 2, "max": 18, "step": 1, "hint": "6/12 pitch = 6\" rise for every 12\" horizontal run"},
            {"id": "waste", "label": "Waste & Ridge Factor", "default": 12, "suffix": "%", "min": 5, "max": 25, "step": 1, "hint": "10-15% standard for hip/valley roofs"}
        ],
        "metrics": [
            {"id": "roofing_squares", "label": "Total Roofing Squares", "default_display": "25.0 squares", "highlight": True},
            {"id": "bundles_needed", "label": "Shingle Bundles (3/Square)", "default_display": "75 bundles"},
            {"id": "actual_surface_sqft", "label": "True Pitched Roof Area", "default_display": "2,236.1 sq ft"},
            {"id": "underlayment_rolls", "label": "Synthetic Felt Rolls (10 Sq/Roll)", "default_display": "3 rolls"}
        ],
        "proof_steps": [
            {"step_title": "Roof Pitch Pythagorean Multiplier", "step_text": "The pitch factor secant: M_pitch = √[1 + (pitch / 12)²]. For a 6/12 pitch, M_pitch = √(1 + 0.25) = 1.118."},
            {"step_title": "True Geometric Slope Area", "step_text": "True Area = Footprint × M_pitch. Order Area = True Area · (1 + waste/100)."},
            {"step_title": "Roofing Square and Bundle Quantization", "step_text": "One roofing square = 100 square feet. Architectural shingles pack 3 bundles per square: Bundles = Squares × 3."}
        ],
        "faqs": [
            {"q": "What is a 'square' in roofing?", "a": "A roofing square is a standard unit of measurement equal to exactly 100 square feet of roof surface."},
            {"q": "How many bundles of shingles make a square?", "a": "For almost all standard fiberglass and architectural shingles, exactly 3 bundles cover 1 square (100 sq ft). Heavy designer shingles may require 4 or 5 bundles per square."}
        ],
        "js_logic": """
          const foot = getNum('footprint_area');
          const pitch = getNum('pitch');
          const waste = 1 + (getNum('waste') / 100);

          const pitchFactor = Math.sqrt(1 + Math.pow(pitch / 12, 2));
          const trueArea = foot * pitchFactor;
          const grossArea = trueArea * waste;
          const squares = grossArea / 100;
          const bundles = Math.ceil(squares * 3);
          const underlay = Math.ceil(squares / 10);

          setDisp('roofing_squares', squares.toFixed(1) + ' squares');
          setDisp('bundles_needed', bundles + ' bundles');
          setDisp('actual_surface_sqft', trueArea.toFixed(1) + ' sq ft');
          setDisp('underlayment_rolls', underlay + ' rolls');
        """
    },
    {
        "slug": "ac-btu-tonnage",
        "category": "construction",
        "name": "HVAC Air Conditioner BTU & Tonnage Calculator",
        "description": "Calculate residential cooling BTU requirements and AC condenser tonnage based on square footage, ceiling height, and climate zone.",
        "hero_badge": "HVAC Engineering • Manual J Sizing Solver",
        "formula_display": "Cooling Tons = Total Required BTU / 12,000 BTU/ton",
        "fields": [
            {"id": "square_footage", "label": "Conditioned Home Area", "default": 2200, "suffix": "sq ft", "min": 200, "max": 8000, "step": 50, "hint": "Finished heated/cooled square footage"},
            {"id": "ceiling_height", "label": "Average Ceiling Height", "default": 9, "suffix": "ft", "min": 8, "max": 16, "step": 0.5, "hint": "Standard is 8 to 9 ft"},
            {"id": "climate_zone", "label": "Climate Zone (Zone 1 Hot to Zone 5 Cool)", "default": 3, "min": 1, "max": 5, "step": 1, "hint": "1: Deep South/TX/FL, 3: Mid-Atlantic, 5: Northern US"},
            {"id": "occupants", "label": "Number of Regular Occupants", "default": 4, "min": 1, "max": 12, "step": 1, "hint": "Each occupant adds ~400 BTU sensible/latent heat"}
        ],
        "metrics": [
            {"id": "condenser_tonnage", "label": "Recommended AC Tonnage", "default_display": "3.5 Tons", "highlight": True},
            {"id": "cooling_btu", "label": "Required Cooling Capacity", "default_display": "42,400 BTU/hr"},
            {"id": "cfm_airflow", "label": "Required Airflow (CFM)", "default_display": "1,400 CFM (400 CFM/Ton)"},
            {"id": "sensible_load", "label": "Volume Enclosure Multiplier", "default_display": "1.12× base load"}
        ],
        "proof_steps": [
            {"step_title": "Base Sensible Heat Load by Climate", "step_text": "Base load varies by zone: Zone 1 = 26 BTU/sqft, Zone 2 = 23 BTU/sqft, Zone 3 = 20 BTU/sqft, Zone 4 = 17 BTU/sqft, Zone 5 = 15 BTU/sqft."},
            {"step_title": "Height and Occupancy Corrections", "step_text": "BTU = [Area × Base_Rate × (Ceiling / 8)] + (Occupants × 400). Kitchen areas add 1,200 BTU."},
            {"step_title": "HVAC Tonnage Derivation", "step_text": "One ton of refrigeration equals 12,000 BTU/hr (heat required to melt 1 ton of ice in 24 hours): Tons = BTU / 12,000. Round to standard 0.5-ton increments."}
        ],
        "faqs": [
            {"q": "Can I install an oversized AC unit to cool my home faster?", "a": "No! Oversized AC units satisfy the thermostat too quickly, preventing adequate dehumidification. This leaves the home feeling clammy and causes indoor mold and compressor short-cycling."},
            {"q": "What tonnage does a 2,000 sq ft home require?", "a": "Most well-insulated 2,000 sq ft homes in moderate climates require a 3.0 to 3.5 ton central AC system."}
        ],
        "js_logic": """
          const sqft = getNum('square_footage');
          const H = getNum('ceiling_height');
          const zone = getNum('climate_zone') || 3;
          const occ = getNum('occupants') || 2;

          const rates = { 1: 26, 2: 23, 3: 20, 4: 17, 5: 15 };
          const baseRate = rates[zone] || 20;
          const rawBtu = (sqft * baseRate * (H / 8)) + (occ * 400) + 1200;
          const exactTons = rawBtu / 12000;
          const tons = Math.ceil(exactTons * 2) / 2; // round to nearest 0.5 ton
          const cfm = tons * 400;

          setDisp('condenser_tonnage', tons.toFixed(1) + ' Tons');
          setDisp('cooling_btu', Math.round(rawBtu).toLocaleString() + ' BTU/hr');
          setDisp('cfm_airflow', cfm.toLocaleString() + ' CFM');
          setDisp('sensible_load', (H / 8).toFixed(2) + '× height factor');
        """
    },
    {
        "slug": "heating-btu",
        "category": "construction",
        "name": "Heating BTU & Furnace Sizing Calculator",
        "description": "Calculate furnace heating output (BTU/hr) and thermal efficiency ratings based on regional design temperatures and insulation levels.",
        "hero_badge": "Thermal Systems • Furnace Sizing Matrix",
        "formula_display": "Furnace BTU = Home Area (sq ft) × Heating Factor (BTU/sq ft)",
        "fields": [
            {"id": "square_footage", "label": "Heated Square Footage", "default": 2200, "suffix": "sq ft", "min": 200, "max": 10000, "step": 50, "hint": "Finished living area"},
            {"id": "climate_severity", "label": "Winter Climate Zone (1 Mild to 5 Extreme Cold)", "default": 3, "min": 1, "max": 5, "step": 1, "hint": "1: Florida/Gulf (30 BTU), 3: Ohio/PA (45 BTU), 5: MN/ME (60 BTU)"},
            {"id": "efficiency_afue", "label": "Furnace AFUE Efficiency", "default": 96, "suffix": "%", "min": 80, "max": 98, "step": 1, "hint": "96% for high-efficiency condensing gas furnace"}
        ],
        "metrics": [
            {"id": "furnace_input_btu", "label": "Recommended Furnace Input", "default_display": "100,000 BTU/hr", "highlight": True},
            {"id": "output_heat_btu", "label": "Net Heat Output Delivered", "default_display": "99,000 BTU/hr"},
            {"id": "annual_fuel_use", "label": "Effective Efficiency Tier", "default_display": "Condensing 96% AFUE"},
            {"id": "btu_per_sqft", "label": "Specific Heating Density", "default_display": "45 BTU / sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Heating Degree Day Zone Classification", "step_text": "Zone 1 (Mild): 30 BTU/sqft; Zone 2 (Moderate): 35-40 BTU/sqft; Zone 3 (Cold): 45 BTU/sqft; Zone 4 (Very Cold): 50 BTU/sqft; Zone 5 (Sub-Zero): 60 BTU/sqft."},
            {"step_title": "Net Thermal Demand", "step_text": "Net Demand BTU_out = Area × Heating Factor."},
            {"step_title": "AFUE Efficiency Rating Adjustment", "step_text": "Furnaces are labeled by fuel input rate: Input BTU = Net Output BTU / (AFUE / 100)."}
        ],
        "faqs": [
            {"q": "What does AFUE stand for on a furnace?", "a": "AFUE stands for Annual Fuel Utilization Efficiency. A 96% AFUE rating means 96% of the fuel is converted into usable heat, while only 4% is lost through chimney exhaust."},
            {"q": "What happens if a furnace is too big for the house?", "a": "An oversized furnace will heat the house too rapidly and shut off before circulating heat evenly, resulting in extreme temperature swings between rooms and excessive wear on heat exchangers."}
        ],
        "js_logic": """
          const sqft = getNum('square_footage');
          const zone = getNum('climate_severity') || 3;
          const afue = (getNum('efficiency_afue') || 96) / 100;

          const factors = { 1: 30, 2: 38, 3: 45, 4: 52, 5: 60 };
          const factor = factors[zone] || 45;
          const netBtu = sqft * factor;
          const inputBtu = netBtu / afue;
          const roundedInput = Math.ceil(inputBtu / 10000) * 10000;

          setDisp('furnace_input_btu', roundedInput.toLocaleString() + ' BTU/hr');
          setDisp('output_heat_btu', Math.round(netBtu).toLocaleString() + ' BTU/hr');
          setDisp('annual_fuel_use', 'Condensing ' + Math.round(afue * 100) + '% AFUE');
          setDisp('btu_per_sqft', factor + ' BTU / sq ft');
        """
    },
    {
        "slug": "solar-sizing",
        "category": "construction",
        "name": "Solar Panel Array Sizing & kWh Calculator",
        "description": "Calculate solar panel system size (kW), required roof panels, daily energy generation, and utility offset.",
        "hero_badge": "Renewable Energy • Photovoltaic Matrix",
        "formula_display": "System Size (kW) = [Annual kWh / (Sun Hours × 365)] / Derate Factor",
        "fields": [
            {"id": "monthly_kwh", "label": "Monthly Electric Usage", "default": 1100, "suffix": "kWh", "min": 200, "max": 5000, "step": 50, "hint": "Average monthly kilowatt-hours from electric bill"},
            {"id": "sun_hours", "label": "Average Peak Daily Sun Hours", "default": 4.5, "suffix": "hrs/day", "min": 3, "max": 7, "step": 0.25, "hint": "US average is 4.0 to 5.5 peak sun hours"},
            {"id": "panel_wattage", "label": "Solar Panel Rating", "default": 400, "suffix": "watts", "min": 300, "max": 500, "step": 10, "hint": "Modern monocrystalline panel: 400W"},
            {"id": "offset_target", "label": "Target Electric Bill Offset", "default": 100, "suffix": "%", "min": 25, "max": 150, "step": 5, "hint": "Percentage of electric consumption to offset"}
        ],
        "metrics": [
            {"id": "system_size_kw", "label": "Recommended Array Size", "default_display": "9.43 kW DC", "highlight": True},
            {"id": "panel_count", "label": "Total Solar Panels Needed", "default_display": "24 panels (400W)", "highlight": True},
            {"id": "annual_production", "label": "Est. Annual Generation", "default_display": "13,200 kWh/yr"},
            {"id": "roof_area_needed", "label": "Required Unshaded Roof Area", "default_display": "432 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Daily Electrical Energy Consumption", "step_text": "Target annual energy = (Monthly kWh × 12) × (Offset% / 100). Daily demand E_daily = Annual kWh / 365."},
            {"step_title": "System Derate and Inverter Losses", "step_text": "DC-to-AC inverters, wiring resistance, and temperature degradation create an industry standard 0.80 derate factor: kW_DC = E_daily / (Peak Sun Hours × 0.80)."},
            {"step_title": "Panel Count and Roof Footprint", "step_text": "Panels = ceil[(kW_DC × 1000) / Panel Wattage]. Each modern 400W panel occupies approximately 18 square feet."}
        ],
        "faqs": [
            {"q": "What is a 'peak sun hour'?", "a": "A peak sun hour is not just daylight; it is an hour when solar irradiance reaches an intensity of 1,000 watts per square meter (1 kW/m²)."},
            {"q": "How much roof space does a 10 kW solar array take?", "a": "A 10 kW system typically uses 25 panels (at 400W each) and requires roughly 450 to 500 square feet of unshaded, south- or west-facing roof space."}
        ],
        "js_logic": """
          const moKwh = getNum('monthly_kwh');
          const sunH = getNum('sun_hours');
          const pWatt = getNum('panel_wattage') || 400;
          const offset = (getNum('offset_target') || 100) / 100;

          const annualKwh = moKwh * 12 * offset;
          const dailyKwh = annualKwh / 365;
          const systemKw = dailyKwh / (sunH * 0.80);
          const panels = Math.ceil((systemKw * 1000) / pWatt);
          const roofSqFt = panels * 18;

          setDisp('system_size_kw', systemKw.toFixed(2) + ' kW DC');
          setDisp('panel_count', panels + ' panels (' + pWatt + 'W)');
          setDisp('annual_production', Math.round(annualKwh).toLocaleString() + ' kWh/yr');
          setDisp('roof_area_needed', roofSqFt + ' sq ft');
        """
    },
    {
        "slug": "tankless-water-heater",
        "category": "construction",
        "name": "Tankless Water Heater GPM & Sizing Calculator",
        "description": "Calculate required Gallons Per Minute (GPM), incoming ground water temperature rise (ΔT), and heating capacity for on-demand water heaters.",
        "hero_badge": "Plumbing Engineering • Flow & Thermal Rise Matrix",
        "formula_display": "Required GPM = Sum of Concurrent Fixture Flow Rates",
        "fields": [
            {"id": "showers", "label": "Simultaneous Showers Running", "default": 2, "min": 0, "max": 5, "step": 1, "hint": "Standard shower consumes 2.0 to 2.5 GPM"},
            {"id": "sinks", "label": "Simultaneous Sinks / Faucets", "default": 2, "min": 0, "max": 6, "step": 1, "hint": "Bathroom/kitchen sink consumes 1.0 to 1.5 GPM"},
            {"id": "appliances", "label": "Dishwasher or Washing Machine", "default": 1, "min": 0, "max": 3, "step": 1, "hint": "Consumes ~1.5 to 2.0 GPM"},
            {"id": "inlet_temp", "label": "Incoming Ground Water Temp", "default": 50, "suffix": "°F", "min": 35, "max": 75, "step": 1, "hint": "35-45°F in North; 60-70°F in Deep South"}
        ],
        "metrics": [
            {"id": "peak_gpm", "label": "Peak Flow Demand (GPM)", "default_display": "7.5 GPM", "highlight": True},
            {"id": "temp_rise", "label": "Required Temperature Rise (ΔT)", "default_display": "70°F Rise (to 120°F)"},
            {"id": "gas_btu_input", "label": "Natural Gas Input Required", "default_display": "199,000 BTU/hr"},
            {"id": "electric_kw_draw", "label": "Electric Equivalent Draw", "default_display": "36 kW (150 Amps)"}
        ],
        "proof_steps": [
            {"step_title": "Peak Concurrent Flow Calculus", "step_text": "GPM_total = (showers × 2.0) + (sinks × 1.0) + (appliances × 1.5)."},
            {"step_title": "Thermal Rise Derivation", "step_text": "To deliver standard 120°F domestic hot water: ΔT = 120°F - Inlet Water Temp (°F)."},
            {"step_title": "Thermodynamic Heat Input", "step_text": "Water heating energy equation: BTU/hr = GPM × ΔT × 500 (since 1 gal water = 8.33 lbs, 8.33 × 60 = 500). Gas units assume 82% efficiency: BTU_in = BTU / 0.82."}
        ],
        "faqs": [
            {"q": "Can an electric tankless water heater supply a whole house in cold climates?", "a": "In northern regions where winter groundwater is 35°F to 45°F, electric tankless units struggle to provide more than 3 to 4 GPM unless the home has a massive 300A or 400A electrical service panel."},
            {"q": "What size gas line is needed for a gas tankless water heater?", "a": "High-output gas tankless units (199,000 BTU) typically require a dedicated 3/4-inch gas line directly from the meter rather than the 1/2-inch line used by conventional tank heaters."}
        ],
        "js_logic": """
          const sh = getNum('showers');
          const sk = getNum('sinks');
          const ap = getNum('appliances');
          const inlet = getNum('inlet_temp') || 50;

          const gpm = (sh * 2.0) + (sk * 1.0) + (ap * 1.5);
          const deltaT = Math.max(10, 120 - inlet);
          const rawBtu = gpm * deltaT * 500;
          const gasBtu = rawBtu / 0.82;
          const kwDraw = (gpm * deltaT * 0.147);

          setDisp('peak_gpm', gpm.toFixed(1) + ' GPM');
          setDisp('temp_rise', deltaT + '°F Rise (to 120°F)');
          setDisp('gas_btu_input', Math.round(gasBtu).toLocaleString() + ' BTU/hr');
          setDisp('electric_kw_draw', Math.round(kwDraw) + ' kW (~' + Math.round((kwDraw * 1000) / 240) + 'A @ 240V)');
        """
    },
    {
        "slug": "electricity-cost",
        "category": "construction",
        "name": "Electricity Cost & Appliance kWh Calculator",
        "description": "Calculate daily, monthly, and annual operating costs for any electrical appliance from wattage and local utility kWh rates.",
        "hero_badge": "Electrical Economics • kWh Cost Matrix",
        "formula_display": "Cost = [Watts × Hours Run / 1,000] × Utility Rate ($/kWh)",
        "fields": [
            {"id": "wattage", "label": "Appliance Wattage", "default": 1500, "suffix": "watts", "min": 1, "max": 15000, "step": 25, "hint": "Nameplate wattage on appliance label"},
            {"id": "hours_per_day", "label": "Daily Operating Hours", "default": 8, "suffix": "hrs/day", "min": 0.25, "max": 24, "step": 0.25, "hint": "Average hours running per 24-hour cycle"},
            {"id": "kwh_rate", "label": "Electric Utility Rate", "default": 0.16, "prefix": "$", "suffix": "/kWh", "min": 0.05, "max": 0.60, "step": 0.01, "hint": "US average is ~$0.16/kWh"}
        ],
        "metrics": [
            {"id": "monthly_cost", "label": "Monthly Electricity Cost", "default_display": "$57.60 / mo", "highlight": True},
            {"id": "annual_cost", "label": "Annual Electricity Cost", "default_display": "$700.80 / yr"},
            {"id": "daily_kwh", "label": "Daily Energy Consumption", "default_display": "12.0 kWh / day"},
            {"id": "monthly_kwh", "label": "Monthly Energy Consumption", "default_display": "360.0 kWh / mo"}
        ],
        "proof_steps": [
            {"step_title": "Kilowatt-Hour Integral", "step_text": "Energy consumption in kilowatt-hours: kWh_daily = (Watts × Daily Hours) / 1,000."},
            {"step_title": "Monthly and Annual Scaling", "step_text": "Monthly kWh = kWh_daily × 30. Annual kWh = kWh_daily × 365."},
            {"step_title": "Monetary Utility Assessment", "step_text": "Cost = Total kWh × Utility Rate ($/kWh)."}
        ],
        "faqs": [
            {"q": "How much electricity does a space heater use?", "a": "A standard 1,500-watt space heater running 8 hours a day consumes 12 kWh per day, costing approximately $1.92 per day or $57.60 per month at $0.16/kWh."},
            {"q": "What household appliances use the most electricity?", "a": "Central air conditioning and heat pumps, electric water heaters, electric clothes dryers, and EV chargers consume the vast majority of residential power."}
        ],
        "js_logic": """
          const W = getNum('wattage');
          const H = getNum('hours_per_day');
          const rate = getNum('kwh_rate');

          const dailyKwh = (W * H) / 1000;
          const monthlyKwh = dailyKwh * 30;
          const annualKwh = dailyKwh * 365;
          const moCost = monthlyKwh * rate;
          const yrCost = annualKwh * rate;

          setDisp('monthly_cost', '$' + moCost.toFixed(2) + ' / mo');
          setDisp('annual_cost', '$' + yrCost.toFixed(2) + ' / yr');
          setDisp('daily_kwh', dailyKwh.toFixed(1) + ' kWh / day');
          setDisp('monthly_kwh', monthlyKwh.toFixed(1) + ' kWh / mo');
        """
    },
    {
        "slug": "wire-gauge-drop",
        "category": "construction",
        "name": "Voltage Drop & Wire Gauge (AWG) Calculator",
        "description": "Calculate electrical voltage drop, percentage loss, and proper American Wire Gauge (AWG) conductor sizing for single-phase copper circuits.",
        "hero_badge": "Electrical Engineering • NEC Voltage Drop Matrix",
        "formula_display": "Voltage Drop (VD) = [2 × K × I × Length (ft)] / Circular Mils (CM)",
        "fields": [
            {"id": "circuit_voltage", "label": "Circuit Voltage", "default": 120, "suffix": "volts", "min": 12, "max": 480, "step": 12, "hint": "120V standard branch circuit, 240V for heavy equipment"},
            {"id": "load_amperes", "label": "Continuous Load Amperage", "default": 16, "suffix": "amps", "min": 1, "max": 200, "step": 1, "hint": "16A continuous on a 20A breaker (80% rule)"},
            {"id": "one_way_distance", "label": "One-Way Conductor Length", "default": 100, "suffix": "ft", "min": 10, "max": 1000, "step": 10, "hint": "Distance from panel to load"},
            {"id": "wire_gauge", "label": "Wire Gauge (12 for 12AWG, 10 for 10AWG)", "default": 12, "suffix": "AWG", "min": 0, "max": 14, "step": 2, "hint": "14 AWG (15A), 12 AWG (20A), 10 AWG (30A), 8 AWG (50A)"}
        ],
        "metrics": [
            {"id": "voltage_drop_volts", "label": "Total Voltage Drop", "default_display": "6.35 Volts", "highlight": True},
            {"id": "percentage_drop", "label": "Percentage Voltage Drop", "default_display": "5.29%", "highlight": True},
            {"id": "voltage_at_load", "label": "Voltage Delivered to Load", "default_display": "113.65 Volts"},
            {"id": "nec_compliance", "label": "NEC Rec. (<3% Branch Limit)", "default_display": "Fails 3% limit (Upsize to 10 AWG)"}
        ],
        "proof_steps": [
            {"step_title": "Ohm's Law for Long Run Conductors", "step_text": "Voltage Drop V_d = 2 × K × I × L / CM, where K = 12.9 ohms-cmil/ft for copper at 75°C, I is current in amps, L is one-way distance in feet, and CM is circular mils."},
            {"step_title": "Conductor Circular Mil Cross-Sections", "step_text": "14 AWG = 4,110 CM; 12 AWG = 6,530 CM; 10 AWG = 10,380 CM; 8 AWG = 16,510 CM; 6 AWG = 26,240 CM; 4 AWG = 41,740 CM."},
            {"step_title": "NEC Maximum Drop Recommendation", "step_text": "National Electrical Code (NEC) Section 210.19(A) recommends that voltage drop not exceed 3% on branch circuits and 5% total across feeder and branch combined."}
        ],
        "faqs": [
            {"q": "Why is high voltage drop dangerous?", "a": "Excessive voltage drop causes electric motors to overheat and burn out, dimming lights, sensitive electronic tripping, and wasted energy dissipated as heat inside wall conduits."},
            {"q": "When should I upsize from 12 AWG to 10 AWG on a 20A circuit?", "a": "Whenever a 120V 20A circuit run exceeds 70 to 80 feet, upsizing from 12 AWG to 10 AWG keeps voltage drop below the NEC recommended 3% threshold."}
        ],
        "js_logic": """
          const V = getNum('circuit_voltage');
          const I = getNum('load_amperes');
          const L = getNum('one_way_distance');
          const awg = getNum('wire_gauge');

          const cmTable = { 14: 4110, 12: 6530, 10: 10380, 8: 16510, 6: 26240, 4: 41740, 2: 66360, 0: 105600 };
          const cm = cmTable[awg] || 6530;
          const k = 12.9; // copper resistance constant
          const vd = (2 * k * I * L) / cm;
          const pct = (vd / V) * 100;
          const vLoad = V - vd;

          setDisp('voltage_drop_volts', vd.toFixed(2) + ' Volts');
          setDisp('percentage_drop', pct.toFixed(2) + '%');
          setDisp('voltage_at_load', vLoad.toFixed(2) + ' Volts');
          setDisp('nec_compliance', pct <= 3.0 ? 'Compliant (< 3% NEC limit)' : 'Exceeds 3% limit (Upsize wire gauge)');
        """
    },
    {
        "slug": "generator-sizing",
        "category": "construction",
        "name": "Generator Sizing & Starting Watts Calculator",
        "description": "Calculate running watts and surge (starting) watts for whole-home and portable emergency backup generators.",
        "hero_badge": "Emergency Power • Generator Sizing Matrix",
        "formula_display": "Generator Size = Total Running Watts + Largest Motor Surge Watts",
        "fields": [
            {"id": "refrigerator", "label": "Refrigerators & Freezers", "default": 2, "min": 0, "max": 4, "step": 1, "hint": "700 running watts, 2,200 starting surge watts each"},
            {"id": "sump_pump", "label": "Sump Pump (1/2 HP)", "default": 1, "min": 0, "max": 2, "step": 1, "hint": "1,050 running watts, 2,150 starting surge watts"},
            {"id": "well_pump", "label": "Deep Well Pump (1 HP)", "default": 0, "min": 0, "max": 1, "step": 1, "hint": "2,000 running watts, 4,000 starting surge watts"},
            {"id": "portable_heater", "label": "Baseboard / Space Heaters", "default": 1, "min": 0, "max": 3, "step": 1, "hint": "1,500 running watts each (no surge)"},
            {"id": "general_lighting", "label": "Lighting & Electronics Allowance", "default": 1200, "suffix": "watts", "min": 200, "max": 5000, "step": 100, "hint": "LED lights, TVs, Wi-Fi router, laptop chargers"}
        ],
        "metrics": [
            {"id": "recommended_generator", "label": "Minimum Generator Rating", "default_display": "7,500 Watts", "highlight": True},
            {"id": "running_watts", "label": "Continuous Running Watts", "default_display": "5,150 Watts"},
            {"id": "peak_surge_watts", "label": "Peak Starting Surge Load", "default_display": "6,650 Watts"},
            {"id": "fuel_runtime", "label": "Est. 50% Load Fuel Burn", "default_display": "~0.55 gal/hr gasoline"}
        ],
        "proof_steps": [
            {"step_title": "Inductive Motor Inrush Current", "step_text": "Compressors and pumps require 2 to 3 times their running power during the first 2 to 3 seconds of startup to establish magnetic rotor fields."},
            {"step_title": "Simultaneous Surge Rule", "step_text": "Calculate running load by summing all continuous devices. Then add only the SINGLE largest motor startup surge, since probability of multiple motors starting on the exact same millisecond is near zero."},
            {"step_title": "Safety Operating Headroom", "step_text": "Generators should not operate continuously at 100% capacity. Add a 20% safety margin: Generator kW = Peak Load × 1.20."}
        ],
        "faqs": [
            {"q": "Can a portable generator power a central air conditioner?", "a": "A typical 3-ton central AC requires 3,500 running watts but 10,000+ starting watts. To run on a portable generator under 10 kW, you must install an inductive soft-start kit on the AC compressor."},
            {"q": "What is the difference between an inverter generator and open-frame generator?", "a": "Inverter generators produce clean pure sine wave power (<3% Total Harmonic Distortion) safe for sensitive computers and TVs, and throttle engine speed to match electrical demand, saving fuel."}
        ],
        "js_logic": """
          const fridge = getNum('refrigerator');
          const sump = getNum('sump_pump');
          const well = getNum('well_pump');
          const heater = getNum('portable_heater');
          const general = getNum('general_lighting');

          const runFridge = fridge * 700;
          const runSump = sump * 1050;
          const runWell = well * 2000;
          const runHeater = heater * 1500;
          const totalRun = runFridge + runSump + runWell + runHeater + general;

          let maxSurge = 0;
          if (well > 0) maxSurge = Math.max(maxSurge, 2000);
          if (fridge > 0) maxSurge = Math.max(maxSurge, 1500);
          if (sump > 0) maxSurge = Math.max(maxSurge, 1100);

          const peakWatts = totalRun + maxSurge;
          const rated = Math.ceil((peakWatts * 1.20) / 500) * 500;

          setDisp('recommended_generator', rated.toLocaleString() + ' Watts (' + (rated / 1000).toFixed(1) + ' kW)');
          setDisp('running_watts', totalRun.toLocaleString() + ' Watts');
          setDisp('peak_surge_watts', peakWatts.toLocaleString() + ' Watts');
          setDisp('fuel_runtime', '~' + (rated / 13000).toFixed(2) + ' gal/hr gasoline @ 50% load');
        """
    },
    {
        "slug": "insulation-r-value",
        "category": "construction",
        "name": "Insulation R-Value & Batt Roll Calculator",
        "description": "Calculate thermal resistance R-value, fiberglass batt and roll quantities, and blow-in bag counts for attics and exterior walls.",
        "hero_badge": "Thermal Envelope • R-Value & Batt Matrix",
        "formula_display": "Total Batts = Total Cavity Area / Area per Batt",
        "fields": [
            {"id": "surface_area", "label": "Insulation Area", "default": 1200, "suffix": "sq ft", "min": 50, "max": 10000, "step": 50, "hint": "Attic floor or wall frame area"},
            {"id": "target_r_value", "label": "Target R-Value", "default": 38, "min": 13, "max": 60, "step": 1, "hint": "R-13/R-15 for 2×4 walls; R-38 to R-60 for attics"},
            {"id": "roll_coverage", "label": "Coverage per Roll / Package", "default": 48.9, "suffix": "sq ft", "min": 20, "max": 150, "step": 0.5, "hint": "Manufacturer roll square footage"}
        ],
        "metrics": [
            {"id": "packages_needed", "label": "Batt / Roll Packages Needed", "default_display": "25 rolls", "highlight": True},
            {"id": "required_thickness", "label": "Required Fiberglass Thickness", "default_display": "12.0 inches (R-38)"},
            {"id": "blow_in_bags", "label": "Alternative Loose-Fill Bags", "default_display": "31 bags (Attic)"},
            {"id": "energy_savings", "label": "Estimated Heat Loss Reduction", "default_display": "Up to 35% heating savings"}
        ],
        "proof_steps": [
            {"step_title": "Thermal Resistance Definition", "step_text": "R-value measures conductive heat flow resistance: R = ΔT / (Heat Flux Q). Higher R-values indicate greater thermal insulation."},
            {"step_title": "Fiberglass Thickness Equivalence", "step_text": "Standard fiberglass batt delivers approximately R-3.14 per inch of thickness: Thickness = Target R-Value / 3.14."},
            {"step_title": "Roll Package Quantization", "step_text": "Packages = ceil(Area / Roll Coverage). Add 5% for cavity end trimming."}
        ],
        "faqs": [
            {"q": "What R-value is recommended for an attic?", "a": "The US Department of Energy and International Energy Conservation Code (IECC) recommend R-38 to R-49 for moderate climates, and R-60 for cold northern zones."},
            {"q": "Can I install new insulation directly over old insulation?", "a": "Yes, as long as the old insulation is dry and free of mold or rodent contamination. Never use kraft-faced (vapor barrier) insulation on top of existing insulation; use unfaced batts or loose-fill blow-in."}
        ],
        "js_logic": """
          const area = getNum('surface_area');
          const rVal = getNum('target_r_value') || 38;
          const cov = getNum('roll_coverage') || 48.9;

          const rolls = Math.ceil((area * 1.05) / cov);
          const thickness = rVal / 3.14;
          const blowBags = Math.ceil((area * (rVal / 38) * 0.95) / 38);

          setDisp('packages_needed', rolls + ' rolls / packages');
          setDisp('required_thickness', thickness.toFixed(1) + ' inches (R-' + rVal + ')');
          setDisp('blow_in_bags', blowBags + ' bags loose-fill');
          setDisp('energy_savings', 'Up to 35% thermal savings');
        """
    },
    {
        "slug": "rebar-calculator",
        "category": "construction",
        "name": "Concrete Rebar Grid & Weight Calculator",
        "description": "Calculate rebar sticks, grid layout spacing, overlap splices, and steel weight for reinforced concrete slabs and footings.",
        "hero_badge": "Reinforced Concrete • Rebar Grid Solver",
        "formula_display": "Linear Feet = [(Length / Spacing + 1) × Width] + [(Width / Spacing + 1) × Length]",
        "fields": [
            {"id": "slab_length", "label": "Slab Length", "default": 30, "suffix": "ft", "min": 2, "max": 200, "step": 1, "hint": "Slab length in feet"},
            {"id": "slab_width", "label": "Slab Width", "default": 20, "suffix": "ft", "min": 2, "max": 200, "step": 1, "hint": "Slab width in feet"},
            {"id": "grid_spacing", "label": "Rebar Grid Spacing (On-Center)", "default": 18, "suffix": "in", "min": 6, "max": 36, "step": 2, "hint": "12\" to 18\" typical for residential concrete slabs"},
            {"id": "rebar_size", "label": "Rebar Bar Size (#3: 3/8\", #4: 1/2\", #5: 5/8\")", "default": 4, "min": 3, "max": 8, "step": 1, "hint": "#4 rebar (1/2\" diameter) is standard"}
        ],
        "metrics": [
            {"id": "rebar_sticks", "label": "20-Foot Rebar Sticks", "default_display": "45 sticks (20 ft)", "highlight": True},
            {"id": "linear_feet", "label": "Total Steel Linear Footage", "default_display": "880 linear ft"},
            {"id": "total_weight", "label": "Total Steel Rebar Weight", "default_display": "588 lbs (0.29 tons)"},
            {"id": "tie_wire", "label": "Rebar Wire Ties Needed", "default_display": "308 intersection ties"}
        ],
        "proof_steps": [
            {"step_title": "Bidirectional Orthogonal Grid Layout", "step_text": "Number of lengthwise bars = ceil[(Width × 12) / Spacing] + 1. Number of widthwise bars = ceil[(Length × 12) / Spacing] + 1."},
            {"step_title": "Lap Splice and Edge Clearance Allowance", "step_text": "ACI 318 requires a 30-bar-diameter lap splice (e.g. 15 inches for #4 rebar) whenever 20ft sticks are joined: Add 10% for lap splices."},
            {"step_title": "ASTM Weight per Foot Specifications", "step_text": "#3 rebar = 0.376 lbs/ft; #4 rebar = 0.668 lbs/ft; #5 rebar = 1.043 lbs/ft; #6 rebar = 1.502 lbs/ft."}
        ],
        "faqs": [
            {"q": "What height should rebar be positioned inside a 4-inch concrete slab?", "a": "Rebar must be positioned in the center or top third of the slab (approx. 2 inches off the subgrade) using plastic rebar chairs. Rebar laying flat on dirt provides zero structural reinforcement."},
            {"q": "Why is rebar needed in a concrete slab?", "a": "Concrete has high compressive strength but poor tensile strength. Steel rebar resists bending and tensile loads, preventing slab cracking and separation during soil shifting or vehicle loads."}
        ],
        "js_logic": """
          const L = getNum('slab_length');
          const W = getNum('slab_width');
          const S = getNum('grid_spacing') || 18;
          const bar = getNum('rebar_size') || 4;

          const numLengthBars = Math.ceil((W * 12) / S) + 1;
          const numWidthBars = Math.ceil((L * 12) / S) + 1;
          const rawFeet = (numLengthBars * L) + (numWidthBars * W);
          const totalFeet = rawFeet * 1.10; // 10% lap splice
          const sticks = Math.ceil(totalFeet / 20);
          const ties = numLengthBars * numWidthBars;

          const weights = { 3: 0.376, 4: 0.668, 5: 1.043, 6: 1.502, 7: 2.044, 8: 2.670 };
          const lbPerFt = weights[bar] || 0.668;
          const totalLbs = totalFeet * lbPerFt;

          setDisp('rebar_sticks', sticks + ' sticks (20 ft)');
          setDisp('linear_feet', Math.round(totalFeet) + ' linear ft');
          setDisp('total_weight', Math.round(totalLbs) + ' lbs (' + (totalLbs / 2000).toFixed(2) + ' tons)');
          setDisp('tie_wire', ties + ' intersection ties');
        """
    },
    {
        "slug": "gutter-sizing",
        "category": "construction",
        "name": "Rain Gutter & Downspout Sizing Calculator",
        "description": "Calculate roof drainage watershed, 5-inch vs 6-inch seamless K-style gutter capacity, and downspout count based on local rainfall intensity.",
        "hero_badge": "Stormwater Engineering • Gutter Capacity Matrix",
        "formula_display": "Drainage Area = Roof Area × Pitch Factor × Max Rainfall Rate (in/hr)",
        "fields": [
            {"id": "roof_length", "label": "Eave Gutter Length", "default": 45, "suffix": "ft", "min": 10, "max": 200, "step": 1, "hint": "Length of fascia board along roof eave"},
            {"id": "roof_width", "label": "Roof Width (Ridge to Eave)", "default": 20, "suffix": "ft", "min": 5, "max": 80, "step": 1, "hint": "Horizontal span draining into this gutter"},
            {"id": "rainfall_intensity", "label": "10-Year Max Rainfall Rate", "default": 5.5, "suffix": "in/hr", "min": 2, "max": 10, "step": 0.5, "hint": "US average: 4.0 to 6.5 inches/hr peak storm"},
            {"id": "roof_pitch", "label": "Roof Pitch Rise (/12)", "default": 6, "min": 2, "max": 16, "step": 1, "hint": "Pitch multiplier accounts for wind-driven rain velocity"}
        ],
        "metrics": [
            {"id": "gutter_profile", "label": "Recommended Gutter Size", "default_display": "6-Inch K-Style", "highlight": True},
            {"id": "downspouts_count", "label": "Downspouts Required", "default_display": "2 Downspouts (3×4\")", "highlight": True},
            {"id": "adjusted_area", "label": "Design Watershed Drainage Area", "default_display": "1,080 sq ft"},
            {"id": "peak_flow_rate", "label": "Peak Stormwater Discharge", "default_display": "61.9 GPM"}
        ],
        "proof_steps": [
            {"step_title": "Roof Watershed Area Adjustment", "step_text": "Roof drainage area A_d = Length × Width × Pitch Factor. Pitch factors: 4/12 = 1.05, 6/12 = 1.10, 8/12 = 1.20, 12/12 = 1.30."},
            {"step_title": "Rational Flow Method", "step_text": "Discharge Q = (Rainfall_in/hr × A_d) / 96.23 GPM."},
            {"step_title": "SMACNA Gutter Sizing Heuristic", "step_text": "Standard 5-inch K-style gutters handle up to 5,500 sq ft watershed with 3×4 downspouts. When watershed intensity exceeds 1,000 adjusted sq ft per 30ft run, 6-inch gutters prevent overshooting and foundation erosion."}
        ],
        "faqs": [
            {"q": "Should I choose 5-inch or 6-inch seamless gutters?", "a": "6-inch gutters hold 40% more water volume than 5-inch gutters and are significantly less prone to clogging from pine needles and leaves. Most modern homes benefit from 6-inch gutters paired with 3×4 downspouts."},
            {"q": "How far apart should downspouts be placed?", "a": "Downspouts should be installed every 30 to 40 linear feet of gutter run to prevent overflowing during heavy downpours."}
        ],
        "js_logic": """
          const L = getNum('roof_length');
          const W = getNum('roof_width');
          const rain = getNum('rainfall_intensity') || 5.5;
          const pitch = getNum('roof_pitch') || 6;

          const pitchFactor = 1 + (pitch * 0.02);
          const adjArea = L * W * pitchFactor;
          const gpm = (rain * adjArea) / 96.23;
          const profile = (adjArea > 900 || rain > 5.0) ? '6-Inch K-Style' : '5-Inch K-Style';
          const downspouts = Math.max(1, Math.ceil(L / 35));

          setDisp('gutter_profile', profile);
          setDisp('downspouts_count', downspouts + ' Downspouts (3×4")');
          setDisp('adjusted_area', Math.round(adjArea) + ' sq ft');
          setDisp('peak_flow_rate', gpm.toFixed(1) + ' GPM');
        """
    },
    {
        "slug": "excavation-trench",
        "category": "construction",
        "name": "Trench Excavation & Soil Swell Calculator",
        "description": "Calculate trench volume in cubic yards, bank cubic yards (BCY) vs loose cubic yards (LCY), and haul-off dump truck loads.",
        "hero_badge": "Earthwork & Excavation • Soil Swell Matrix",
        "formula_display": "Loose Volume (LCY) = Bank Volume (BCY) × (1 + Swell Factor / 100)",
        "fields": [
            {"id": "length", "label": "Trench Length", "default": 100, "suffix": "ft", "min": 5, "max": 2000, "step": 5, "hint": "Total length of trench excavation"},
            {"id": "width", "label": "Trench Width", "default": 2, "suffix": "ft", "min": 0.5, "max": 20, "step": 0.25, "hint": "Bucket width or trench width in feet"},
            {"id": "depth", "label": "Trench Depth", "default": 4, "suffix": "ft", "min": 1, "max": 20, "step": 0.5, "hint": "Depth in feet (OSHA mandates shoring over 5ft)"},
            {"id": "soil_swell", "label": "Soil Swell Factor", "default": 25, "suffix": "%", "min": 10, "max": 50, "step": 5, "hint": "Clay/dirt swells 20-30% when disturbed and uncompacted"}
        ],
        "metrics": [
            {"id": "bank_cuyd", "label": "In-Ground Volume (BCY)", "default_display": "29.63 cu yd", "highlight": True},
            {"id": "loose_cuyd", "label": "Excavated Loose Volume (LCY)", "default_display": "37.04 cu yd", "highlight": True},
            {"id": "truck_loads", "label": "10-Yard Dump Truck Hauls", "default_display": "4 truckloads"},
            {"id": "trench_sqft", "label": "Trench Bottom Surface", "default_display": "200.0 sq ft"}
        ],
        "proof_steps": [
            {"step_title": "Bank Cubic Yard (BCY) In-Situ Volume", "step_text": "Undisturbed compacted earth volume: V_BCY = [Length (ft) × Width (ft) × Depth (ft)] / 27."},
            {"step_title": "Soil Bulking and Swell Phenomenon", "step_text": "When soil is excavated, air voids are introduced. Loose Cubic Yards V_LCY = V_BCY · (1 + Swell% / 100)."},
            {"step_title": "Haul-Off Truck Capacity", "step_text": "Dump trucks are sized by loose payload volume: Truckloads = ceil(V_LCY / 10 cu yd)."}
        ],
        "faqs": [
            {"q": "What is soil swell factor?", "a": "Soil swell is the percentage volume expansion that occurs when dense, compacted natural earth is excavated and broken into loose particles. Dense clay typically swells 25% to 35%."},
            {"q": "When does OSHA require trench safety boxes or sloping?", "a": "OSHA safety standard 1926.652 mandates protective systems (sloping, shoring, or trench shields) for all trenches 5 feet or deeper, unless excavated entirely in stable solid rock."}
        ],
        "js_logic": """
          const L = getNum('length');
          const W = getNum('width');
          const D = getNum('depth');
          const swell = 1 + (getNum('soil_swell') / 100);

          const cuft = L * W * D;
          const bcy = cuft / 27;
          const lcy = bcy * swell;
          const trucks = Math.ceil(lcy / 10);
          const area = L * W;

          setDisp('bank_cuyd', bcy.toFixed(2) + ' cu yd');
          setDisp('loose_cuyd', lcy.toFixed(2) + ' cu yd');
          setDisp('truck_loads', trucks + ' truckloads');
          setDisp('trench_sqft', area.toFixed(1) + ' sq ft');
        """
    }
]
