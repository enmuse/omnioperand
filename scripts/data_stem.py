"""
scripts/data_stem.py
26 High-Precision STEM, Geometry, Physics & Statistical Mechanics Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

STEM_CALCULATORS = [
    {
        "slug": "ellipse",
        "category": "geometry",
        "name": "Ellipse Area, Perimeter & Eccentricity Calculator",
        "description": "Calculate exact ellipse area, Ramanujan high-precision perimeter approximation, semi-axes, focal distance, and orbital eccentricity.",
        "hero_badge": "Conic Sections • Ramanujan Elliptic Matrix",
        "formula_display": "Area = π · a · b | Perimeter ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], where h = (a - b)² / (a + b)²",
        "fields": [
            {"id": "semi_major", "label": "Semi-Major Axis (a)", "default": 10, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Half the longest diameter"},
            {"id": "semi_minor", "label": "Semi-Minor Axis (b)", "default": 6, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Half the shortest diameter (b ≤ a)"}
        ],
        "metrics": [
            {"id": "ellipse_area", "label": "Exact Ellipse Area", "default_display": "188.4956 units²", "highlight": True},
            {"id": "ramanujan_perimeter", "label": "Perimeter (Ramanujan II)", "default_display": "51.0540 units", "highlight": True},
            {"id": "linear_eccentricity", "label": "Focal Distance (c = √(a² - b²))", "default_display": "8.0000 units"},
            {"id": "first_eccentricity", "label": "Orbital Eccentricity (e = c/a)", "default_display": "0.8000 (Elliptic)"}
        ],
        "proof_steps": [
            {"step_title": "Affine Stretching Area Integral", "step_text": "An ellipse x²/a² + y²/b² = 1 is the linear transformation of a unit circle x² + y² = 1 stretched by factor a horizontally and b vertically: Area = ∫∫ dx dy = π · a · b."},
            {"step_title": "Ramanujan's Second Perimeter Formula", "step_text": "Because the exact perimeter requires an incomplete elliptic integral of the second kind E(e), Srinivasa Ramanujan formulated the famously accurate closed-form approximation: P ≈ π(a + b)[1 + 3h / (10 + √(4 - 3h))], where h = (a - b)² / (a + b)²."},
            {"step_title": "Foci and Orbital Eccentricity", "step_text": "Linear focal distance c = √(a² - b²). First eccentricity e = c / a = √(1 - b²/a²). When e = 0, the ellipse collapses to a perfect circle; as e ➔ 1, it elongates into a parabola."}
        ],
        "faqs": [
            {"q": "Why is there no simple closed-form formula for the perimeter of an ellipse?", "a": "Unlike a circle where curvature is constant, an ellipse's curvature varies continuously. Integrating the arc length differential ds = √[dx² + dy²] yields a non-elementary elliptic integral that cannot be expressed with basic algebraic functions."},
            {"q": "What is the error of Ramanujan's second perimeter formula?", "a": "Ramanujan's second approximation has an extraordinary maximum relative error of less than 0.0015% even for extremely flattened ellipses with eccentricity near 1."}
        ],
        "js_logic": """
          let a = getNum('semi_major');
          let b = getNum('semi_minor');
          if (b > a) { const tmp = a; a = b; b = tmp; }

          const area = Math.PI * a * b;
          const h = Math.pow(a - b, 2) / Math.pow(a + b, 2);
          const perim = Math.PI * (a + b) * (1 + (3 * h) / (10 + Math.sqrt(4 - (3 * h))));
          const c = Math.sqrt(Math.max(0, Math.pow(a, 2) - Math.pow(b, 2)));
          const e = a > 0 ? (c / a) : 0;

          setDisp('ellipse_area', area.toFixed(4) + ' units²');
          setDisp('ramanujan_perimeter', perim.toFixed(4) + ' units');
          setDisp('linear_eccentricity', c.toFixed(4) + ' units');
          setDisp('first_eccentricity', e.toFixed(4) + (e === 0 ? ' (Circle)' : ' (Elliptic)'));
        """
    },
    {
        "slug": "trapezoid",
        "category": "geometry",
        "name": "Trapezoid Area, Median & Perimeter Calculator",
        "description": "Calculate trapezoid (trapezium) area, midline median, perimeter, and diagonal lengths from base lengths, height, and side legs.",
        "hero_badge": "Planar Geometry • Trapezoid Solver",
        "formula_display": "Area = ½(Base a + Base b) · Height | Median = ½(a + b)",
        "fields": [
            {"id": "base_a", "label": "Parallel Base a", "default": 12, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Top parallel base"},
            {"id": "base_b", "label": "Parallel Base b", "default": 20, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Bottom parallel base"},
            {"id": "height", "label": "Perpendicular Height (h)", "default": 8, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Perpendicular distance between bases"},
            {"id": "leg_c", "label": "Left Leg (c)", "default": 8.94, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.1, "hint": "Left non-parallel side"},
            {"id": "leg_d", "label": "Right Leg (d)", "default": 8.94, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.1, "hint": "Right non-parallel side"}
        ],
        "metrics": [
            {"id": "trapezoid_area", "label": "Trapezoid Area", "default_display": "128.0000 units²", "highlight": True},
            {"id": "midline_median", "label": "Midline Median (m)", "default_display": "16.0000 units", "highlight": True},
            {"id": "total_perimeter", "label": "Total Perimeter", "default_display": "49.8800 units"},
            {"id": "trapezoid_type", "label": "Symmetry Classification", "default_display": "Isosceles Trapezoid"}
        ],
        "proof_steps": [
            {"step_title": "Triangulation Area Proof", "step_text": "Partitioning the trapezoid along a diagonal divides it into two triangles with identical altitude h and respective bases a and b: Area = ½ · a · h + ½ · b · h = ½(a + b)h."},
            {"step_title": "Midline Theorem", "step_text": "The median connecting the midpoints of non-parallel legs is parallel to both bases with length exactly equal to their arithmetic mean: m = ½(a + b). Hence, Area = m · h."},
            {"step_title": "Boundary Perimeter", "step_text": "Perimeter P = a + b + c + d."}
        ],
        "faqs": [
            {"q": "What is an isosceles trapezoid?", "a": "An isosceles trapezoid is a trapezoid where the two non-parallel legs are congruent (c = d), base angles are equal, and both internal diagonals have equal length."},
            {"q": "What is the difference between a trapezoid and a trapezium?", "a": "In American English, a trapezoid has at least one pair of parallel sides. In British English, this shape is called a trapezium, while a trapezoid refers to a quadrilateral with no parallel sides."}
        ],
        "js_logic": """
          const a = getNum('base_a');
          const b = getNum('base_b');
          const h = getNum('height');
          const c = getNum('leg_c');
          const d = getNum('leg_d');

          const m = (a + b) / 2;
          const area = m * h;
          const perim = a + b + c + d;
          const isIso = Math.abs(c - d) < 0.05;

          setDisp('trapezoid_area', area.toFixed(4) + ' units²');
          setDisp('midline_median', m.toFixed(4) + ' units');
          setDisp('total_perimeter', perim.toFixed(4) + ' units');
          setDisp('trapezoid_type', isIso ? 'Isosceles Trapezoid (c = d)' : 'Scalene Trapezoid');
        """
    },
    {
        "slug": "rhombus",
        "category": "geometry",
        "name": "Rhombus Area, Side & Diagonals Calculator",
        "description": "Calculate rhombus area, perimeter, side length, incircle radius, and internal angles from intersecting diagonals d₁ and d₂.",
        "hero_badge": "Equilateral Quadrilateral • Rhombus Matrix",
        "formula_display": "Area = ½(d₁ · d₂) | Side a = ½√(d₁² + d₂²)",
        "fields": [
            {"id": "diag_1", "label": "Diagonal 1 (d₁)", "default": 16, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "First internal diagonal"},
            {"id": "diag_2", "label": "Diagonal 2 (d₂)", "default": 12, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Second internal diagonal"}
        ],
        "metrics": [
            {"id": "rhombus_area", "label": "Rhombus Area", "default_display": "96.0000 units²", "highlight": True},
            {"id": "side_length", "label": "Side Length (a)", "default_display": "10.0000 units", "highlight": True},
            {"id": "rhombus_perimeter", "label": "Total Perimeter (4a)", "default_display": "40.0000 units"},
            {"id": "inradius", "label": "Incircle Radius (r)", "default_display": "4.8000 units"}
        ],
        "proof_steps": [
            {"step_title": "Orthogonal Bisection Property", "step_text": "The diagonals of a rhombus bisect each other at right angles (90°), creating 4 congruent right triangles with legs d₁/2 and d₂/2."},
            {"step_title": "Pythagorean Side Derivation", "step_text": "By the Pythagorean theorem on each quadrant triangle: a² = (d₁/2)² + (d₂/2)² = (d₁² + d₂²) / 4, yielding a = ½√(d₁² + d₂²)."},
            {"step_title": "Diagonal Area Proof", "step_text": "Sum of four right triangles: Area = 4 × [½ · (d₁/2) · (d₂/2)] = ½(d₁ · d₂). Inradius r = (d₁ · d₂) / [2√(d₁² + d₂²)]."}
        ],
        "faqs": [
            {"q": "Is every square a rhombus?", "a": "Yes! A square is a special equilateral rhombus where both diagonals are equal (d₁ = d₂) and all four internal angles are right angles (90°)."},
            {"q": "Can you calculate rhombus area with side and angle?", "a": "Yes. If you know side length a and internal angle θ, Area = a² · sin(θ)."}
        ],
        "js_logic": """
          const d1 = getNum('diag_1');
          const d2 = getNum('diag_2');

          const area = 0.5 * d1 * d2;
          const a = 0.5 * Math.sqrt(Math.pow(d1, 2) + Math.pow(d2, 2));
          const perim = 4 * a;
          const r = a > 0 ? (area / (2 * a)) : 0;

          setDisp('rhombus_area', area.toFixed(4) + ' units²');
          setDisp('side_length', a.toFixed(4) + ' units');
          setDisp('rhombus_perimeter', perim.toFixed(4) + ' units');
          setDisp('inradius', r.toFixed(4) + ' units');
        """
    },
    {
        "slug": "parallelogram",
        "category": "geometry",
        "name": "Parallelogram Area & Diagonals Calculator",
        "description": "Calculate parallelogram area, perimeter, internal diagonals, and heights using base, side, and acute internal angle.",
        "hero_badge": "Affine Geometry • Parallelogram Matrix",
        "formula_display": "Area = Base · Height = a · b · sin(θ)",
        "fields": [
            {"id": "side_a", "label": "Base Side (a)", "default": 14, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Length of horizontal base"},
            {"id": "side_b", "label": "Adjacent Side (b)", "default": 9, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Length of adjacent slant side"},
            {"id": "angle_deg", "label": "Internal Angle (θ)", "default": 60, "suffix": "degrees", "min": 5, "max": 175, "step": 1, "hint": "Angle between sides a and b"}
        ],
        "metrics": [
            {"id": "para_area", "label": "Parallelogram Area", "default_display": "109.1169 units²", "highlight": True},
            {"id": "altitude_h", "label": "Perpendicular Height (h)", "default_display": "7.7942 units"},
            {"id": "diagonal_p", "label": "Long Diagonal (p)", "default_display": "20.0749 units", "highlight": True},
            {"id": "diagonal_q", "label": "Short Diagonal (q)", "default_display": "12.3693 units"}
        ],
        "proof_steps": [
            {"step_title": "Trigonometric Altitude and Area", "step_text": "Altitude h = b · sin(θ). Therefore: Area = a · h = a · b · sin(θ)."},
            {"step_title": "Law of Cosines for Diagonals", "step_text": "Diagonal p opposite obtuse angle (180° - θ): p = √[a² + b² + 2ab cos(θ)]. Diagonal q opposite acute angle θ: q = √[a² + b² - 2ab cos(θ)]."},
            {"step_title": "Parallelogram Law (Apollonius Identity)", "step_text": "Fundamental vector invariant: p² + q² = 2(a² + b²). The sum of squares of the diagonals equals the sum of squares of all four sides."}
        ],
        "faqs": [
            {"q": "What is the Parallelogram Law?", "a": "The Parallelogram Law states that for any parallelogram, p² + q² = 2(a² + b²). In linear algebra and functional analysis, this identity proves whether a normed vector space is an inner product space (Hilbert space)."},
            {"q": "When does a parallelogram have maximum area?", "a": "For fixed side lengths a and b, area is maximized when sin(θ) = 1 (θ = 90°), meaning the parallelogram becomes a rectangle."}
        ],
        "js_logic": """
          const a = getNum('side_a');
          const b = getNum('side_b');
          const thetaDeg = getNum('angle_deg');
          const thetaRad = (thetaDeg * Math.PI) / 180;

          const h = b * Math.sin(thetaRad);
          const area = a * h;
          const p = Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2) + (2 * a * b * Math.cos(thetaRad)));
          const q = Math.sqrt(Math.max(0, Math.pow(a, 2) + Math.pow(b, 2) - (2 * a * b * Math.cos(thetaRad))));

          setDisp('para_area', area.toFixed(4) + ' units²');
          setDisp('altitude_h', h.toFixed(4) + ' units');
          setDisp('diagonal_p', p.toFixed(4) + ' units');
          setDisp('diagonal_q', q.toFixed(4) + ' units');
        """
    },
    {
        "slug": "kite",
        "category": "geometry",
        "name": "Kite Geometry & Area Calculator",
        "description": "Calculate kite area, perimeter, side pairs, and internal diagonal lengths from perpendicular diagonal axes.",
        "hero_badge": "Deltoid Geometry • Kite Area Matrix",
        "formula_display": "Area = ½(d₁ · d₂) | Perimeter = 2(a + b)",
        "fields": [
            {"id": "diag_1", "label": "Longitudinal Diagonal (d₁)", "default": 18, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Symmetry axis diagonal"},
            {"id": "diag_2", "label": "Transverse Diagonal (d₂)", "default": 10, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Perpendicular cross diagonal"},
            {"id": "top_offset", "label": "Upper Diagonal Split (d₁_top)", "default": 4, "suffix": "units", "min": 0.1, "max": 500, "step": 0.5, "hint": "Distance from top vertex to diagonal intersection"}
        ],
        "metrics": [
            {"id": "kite_area", "label": "Kite Surface Area", "default_display": "90.0000 units²", "highlight": True},
            {"id": "side_a", "label": "Top Side Pair (a)", "default_display": "6.4031 units"},
            {"id": "side_b", "label": "Bottom Side Pair (b)", "default_display": "14.8661 units"},
            {"id": "kite_perimeter", "label": "Total Perimeter", "default_display": "42.5384 units", "highlight": True}
        ],
        "proof_steps": [
            {"step_title": "Orthodiagonal Quadrilateral Area Theorem", "step_text": "Because the diagonals of a kite intersect at right angles (90°), its area is identical to half the bounding rectangle: Area = ½(d₁ · d₂)."},
            {"step_title": "Pythagorean Pair Formulation", "step_text": "Let d₂ be bisected into two equal halves (d₂/2). Top sides: a = √[(d₁_top)² + (d₂/2)²]. Bottom sides: b = √[(d₁ - d₁_top)² + (d₂/2)²]."},
            {"step_title": "Perimeter Sum", "step_text": "Perimeter P = 2(a + b)."}
        ],
        "faqs": [
            {"q": "What is the geometric definition of a kite?", "a": "A kite is a quadrilateral with reflection symmetry across a diagonal, having two distinct pairs of adjacent, equal-length sides."},
            {"q": "Can a kite be a cyclic quadrilateral?", "a": "A kite is cyclic (can be inscribed in a circle) if and only if its two opposite non-vertex angles are right angles (90°), in which case it is called a right kite."}
        ],
        "js_logic": """
          const d1 = getNum('diag_1');
          const d2 = getNum('diag_2');
          const d1Top = getNum('top_offset') || (d1 / 3);

          const d1Bot = Math.max(0.1, d1 - d1Top);
          const halfD2 = d2 / 2;
          const a = Math.sqrt(Math.pow(d1Top, 2) + Math.pow(halfD2, 2));
          const b = Math.sqrt(Math.pow(d1Bot, 2) + Math.pow(halfD2, 2));
          const area = 0.5 * d1 * d2;
          const perim = 2 * (a + b);

          setDisp('kite_area', area.toFixed(4) + ' units²');
          setDisp('side_a', a.toFixed(4) + ' units');
          setDisp('side_b', b.toFixed(4) + ' units');
          setDisp('kite_perimeter', perim.toFixed(4) + ' units');
        """
    },
    {
        "slug": "cylinder",
        "category": "geometry",
        "name": "Cylinder Volume & Surface Area Calculator",
        "description": "Calculate cylinder volume, lateral curved surface area, total surface area, and base perimeter from radius and height.",
        "hero_badge": "Solid Geometry • Cylinder Volumetric Matrix",
        "formula_display": "Volume = π · r² · h | Total Surface Area = 2πr(r + h)",
        "fields": [
            {"id": "radius", "label": "Cylinder Radius (r)", "default": 5, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius of circular base"},
            {"id": "height", "label": "Height (h)", "default": 12, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Cylinder altitude"}
        ],
        "metrics": [
            {"id": "cylinder_volume", "label": "Cylinder Volume", "default_display": "942.4778 units³", "highlight": True},
            {"id": "lateral_area", "label": "Lateral Curved Surface Area", "default_display": "376.9911 units²"},
            {"id": "total_surface_area", "label": "Total Surface Area (Caps + Body)", "default_display": "534.0708 units²", "highlight": True},
            {"id": "base_circumference", "label": "Base Perimeter / Circumference", "default_display": "31.4159 units"}
        ],
        "proof_steps": [
            {"step_title": "Cavalieri's Volumetric Principle", "step_text": "The volume of a right circular cylinder is the product of its circular base area and its perpendicular height: V = A_base · h = (π · r²) · h."},
            {"step_title": "Unrolled Net Lateral Area", "step_text": "Unrolling the curved lateral boundary yields a flat rectangle with width equal to base circumference 2πr and height h: A_lateral = 2π · r · h."},
            {"step_title": "Total Enclosed Boundary", "step_text": "Summing the lateral wall plus top and bottom circular caps: A_total = 2πrh + 2(πr²) = 2πr(r + h)."}
        ],
        "faqs": [
            {"q": "What cylinder dimensions maximize volume for a given surface area?", "a": "For a closed cylinder of fixed surface area, volume is maximized when height equals diameter (h = 2r). This geometric ratio minimizes thermal loss and material cost."},
            {"q": "How do you calculate liquid volume in a partially filled horizontal cylinder?", "a": "Calculating liquid volume in a horizontal tank requires finding the area of the circular segment filled with fluid: A_segment = r² · arccos[(r - d)/r] - (r - d)√(2rd - d²), multiplied by length L."}
        ],
        "js_logic": """
          const r = getNum('radius');
          const h = getNum('height');

          const vol = Math.PI * Math.pow(r, 2) * h;
          const lat = 2 * Math.PI * r * h;
          const tot = 2 * Math.PI * r * (r + h);
          const circ = 2 * Math.PI * r;

          setDisp('cylinder_volume', vol.toFixed(4) + ' units³');
          setDisp('lateral_area', lat.toFixed(4) + ' units²');
          setDisp('total_surface_area', tot.toFixed(4) + ' units²');
          setDisp('base_circumference', circ.toFixed(4) + ' units');
        """
    },
    {
        "slug": "cone",
        "category": "geometry",
        "name": "Right Circular Cone Volume & Slant Height Calculator",
        "description": "Calculate cone volume, slant height, lateral area, total surface area, and base cone angle from radius and vertical height.",
        "hero_badge": "Conical Geometry • Right Cone Matrix",
        "formula_display": "Volume = ⅓ · π · r² · h | Slant Height s = √(r² + h²)",
        "fields": [
            {"id": "radius", "label": "Base Radius (r)", "default": 6, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius of circular base"},
            {"id": "height", "label": "Vertical Height (h)", "default": 8, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Height from apex to base center"}
        ],
        "metrics": [
            {"id": "cone_volume", "label": "Cone Volume", "default_display": "301.5929 units³", "highlight": True},
            {"id": "slant_height", "label": "Slant Height (s)", "default_display": "10.0000 units", "highlight": True},
            {"id": "lateral_surface_area", "label": "Lateral Surface Area", "default_display": "188.4956 units²"},
            {"id": "total_surface_area", "label": "Total Surface Area", "default_display": "301.5929 units²"}
        ],
        "proof_steps": [
            {"step_title": "Calculus Solid of Revolution Integral", "step_text": "Revolving the line y = (r/h)x from x = 0 to h around the x-axis: V = π ∫₀ʰ (r/h)² x² dx = π(r²/h²) · [h³ / 3] = ⅓ · π · r² · h. Exactly one-third of the circumscribed cylinder volume."},
            {"step_title": "Pythagorean Slant Height", "step_text": "The apex, center, and perimeter form a right triangle: s = √(r² + h²)."},
            {"step_title": "Sector Unrolling for Lateral Area", "step_text": "The unrolled lateral surface forms a circular sector with radius s and arc length 2πr: A_lateral = π · r · s. Total Area = πrs + πr² = πr(s + r)."}
        ],
        "faqs": [
            {"q": "Why is the volume of a cone exactly one-third of a cylinder?", "a": "As proved rigorously by Eudoxus and Archimedes via exhaustion (and modern triple integration), any cone or pyramid with base area B and height h has volume V = ⅓ · B · h, regardless of base shape."},
            {"q": "What is the angle of repose in conical granular piles?", "a": "When dry aggregate (sand, gravel, grain) pours from a conveyor into a conical pile, internal friction limits the slope angle θ = arctan(h/r), known as the material's natural angle of repose (~34° for gravel)."}
        ],
        "js_logic": """
          const r = getNum('radius');
          const h = getNum('height');

          const s = Math.sqrt(Math.pow(r, 2) + Math.pow(h, 2));
          const vol = (1 / 3) * Math.PI * Math.pow(r, 2) * h;
          const lat = Math.PI * r * s;
          const tot = Math.PI * r * (s + r);

          setDisp('cone_volume', vol.toFixed(4) + ' units³');
          setDisp('slant_height', s.toFixed(4) + ' units');
          setDisp('lateral_surface_area', lat.toFixed(4) + ' units²');
          setDisp('total_surface_area', tot.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "sphere",
        "category": "geometry",
        "name": "Sphere Volume & Surface Area Calculator",
        "description": "Calculate exact sphere volume, surface area, radius, diameter, and circumscribed cylinder ratio using Archimedes' theorem.",
        "hero_badge": "Spherical Geometry • Archimedean Sphere Matrix",
        "formula_display": "Volume = 4/3 · π · r³ | Surface Area = 4 · π · r²",
        "fields": [
            {"id": "radius", "label": "Sphere Radius (r)", "default": 7, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Distance from center to surface"}
        ],
        "metrics": [
            {"id": "sphere_volume", "label": "Sphere Volume", "default_display": "1,436.7550 units³", "highlight": True},
            {"id": "surface_area", "label": "Surface Area", "default_display": "615.7522 units²", "highlight": True},
            {"id": "diameter", "label": "Diameter (2r)", "default_display": "14.0000 units"},
            {"id": "cylinder_ratio", "label": "Archimedean Cylinder Ratio", "default_display": "Exact 2:3 Volume Ratio"}
        ],
        "proof_steps": [
            {"step_title": "Archimedes' Masterpiece: On the Sphere and Cylinder", "step_text": "Archimedes proved in 225 BC that a sphere inscribed inside a cylinder has exactly two-thirds the volume and two-thirds the surface area of the cylinder: V_sphere = ⅔ · V_cylinder = ⅔ · (πr² · 2r) = 4/3 · π · r³."},
            {"step_title": "Surface Area Derivative", "step_text": "The derivative of volume with respect to radius equals the surface area: dV/dr = d/dr(4/3 π r³) = 4πr²."},
            {"step_title": "Isoperimetric Supremacy", "step_text": "Among all three-dimensional shapes enclosing a given volume, the sphere possesses the absolute minimum surface area, minimizing surface tension energy."}
        ],
        "faqs": [
            {"q": "Why is the sphere surface area exactly four times its great circle area?", "a": "A great circle has area πr². Archimedes showed that wrapping the sphere's surface tightly onto a flat plane equals exactly four great circles: 4 × πr² = 4πr²."},
            {"q": "What was carved on Archimedes' tombstone?", "a": "Archimedes considered his proof of the 2:3 ratio of the volume and surface area of an inscribed sphere to its bounding cylinder his greatest achievement, requesting that a sphere inscribed in a cylinder be sculpted onto his tombstone."}
        ],
        "js_logic": """
          const r = getNum('radius');

          const vol = (4 / 3) * Math.PI * Math.pow(r, 3);
          const sa = 4 * Math.PI * Math.pow(r, 2);
          const d = 2 * r;

          setDisp('sphere_volume', vol.toFixed(4) + ' units³');
          setDisp('surface_area', sa.toFixed(4) + ' units²');
          setDisp('diameter', d.toFixed(4) + ' units');
          setDisp('cylinder_ratio', 'Exact 2:3 Volume Ratio (V_cyl = ' + (vol * 1.5).toFixed(1) + ')');
        """
    },
    {
        "slug": "torus",
        "category": "geometry",
        "name": "Torus Volume & Surface Area (Donut) Calculator",
        "description": "Calculate donut torus volume and surface area using Pappus's Centroid Theorems from major radius R and minor radius r.",
        "hero_badge": "Topology & Solids • Pappus Toroid Matrix",
        "formula_display": "Volume = 2π² · R · r² | Surface Area = 4π² · R · r",
        "fields": [
            {"id": "major_radius", "label": "Major Radius (R)", "default": 10, "suffix": "units", "min": 1, "max": 1000, "step": 0.5, "hint": "Distance from center of hole to center of tube (R > r)"},
            {"id": "minor_radius", "label": "Minor Radius (r)", "default": 3, "suffix": "units", "min": 0.1, "max": 500, "step": 0.25, "hint": "Radius of the revolving tube cross-section"}
        ],
        "metrics": [
            {"id": "torus_volume", "label": "Torus Volume", "default_display": "1,776.5288 units³", "highlight": True},
            {"id": "torus_surface_area", "label": "Total Surface Area", "default_display": "1,184.3525 units²", "highlight": True},
            {"id": "hole_diameter", "label": "Inner Hole Diameter (2(R - r))", "default_display": "14.0000 units"},
            {"id": "outer_diameter", "label": "Outer Outer Diameter (2(R + r))", "default_display": "26.0000 units"}
        ],
        "proof_steps": [
            {"step_title": "Pappus's First Centroid Theorem (Volume)", "step_text": "Volume equals cross-sectional area multiplied by the distance traveled by its geometric centroid: Area_circle = πr². Centroid path = 2πR. Therefore: V = (πr²) · (2πR) = 2π² · R · r²."},
            {"step_title": "Pappus's Second Centroid Theorem (Surface Area)", "step_text": "Surface area equals perimeter of cross-section multiplied by distance traveled by its centroid: Perimeter = 2πr. Centroid path = 2πR. Therefore: A = (2πr) · (2πR) = 4π² · R · r."},
            {"step_title": "Ring Torus Geometric Condition", "step_text": "When R > r, the torus forms a standard ring torus with an open central aperture; when R = r, it forms a horn torus touching at the origin; when R < r, it is a spindle torus self-intersecting internally."}
        ],
        "faqs": [
            {"q": "What is the genus of a torus in topology?", "a": "In topology, a torus has genus 1 (possessing exactly one through-hole). It is topologically distinct from a sphere (genus 0) and cannot be continuously deformed into a sphere without cutting."},
            {"q": "Why are nuclear fusion reactors (tokamaks) shaped like a torus?", "a": "A torus has no boundaries or ends, allowing strong magnetic field lines to twist continuously without leaky end-caps, stably confining ultra-hot hydrogen plasma."}
        ],
        "js_logic": """
          let R = getNum('major_radius');
          let r = getNum('minor_radius');
          if (r > R) { const tmp = R; R = r; r = tmp; }

          const vol = 2 * Math.pow(Math.PI, 2) * R * Math.pow(r, 2);
          const sa = 4 * Math.pow(Math.PI, 2) * R * r;
          const innerD = 2 * (R - r);
          const outerD = 2 * (R + r);

          setDisp('torus_volume', vol.toFixed(4) + ' units³');
          setDisp('torus_surface_area', sa.toFixed(4) + ' units²');
          setDisp('hole_diameter', innerD.toFixed(4) + ' units');
          setDisp('outer_diameter', outerD.toFixed(4) + ' units');
        """
    },
    {
        "slug": "triangular-prism",
        "category": "geometry",
        "name": "Triangular Prism Volume & Surface Area Calculator",
        "description": "Calculate triangular prism volume, lateral face area, base area, and total surface area from triangular base dimensions and prism length.",
        "hero_badge": "Polyhedral Geometry • Triangular Prism Matrix",
        "formula_display": "Volume = Base Area · Length | Total Area = 2 · Base Area + (a + b + c) · Length",
        "fields": [
            {"id": "base_width", "label": "Triangular Base Width (b)", "default": 8, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Base edge of triangular face"},
            {"id": "base_height", "label": "Triangular Base Height (h)", "default": 6, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Perpendicular height of triangular face"},
            {"id": "prism_length", "label": "Prism Length (L)", "default": 15, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Extrusion length of prism"}
        ],
        "metrics": [
            {"id": "prism_volume", "label": "Prism Volume", "default_display": "360.0000 units³", "highlight": True},
            {"id": "base_face_area", "label": "Single Triangle Base Area", "default_display": "24.0000 units²"},
            {"id": "lateral_surface", "label": "Lateral Rectangular Wall Area", "default_display": "336.0000 units²"},
            {"id": "total_surface", "label": "Total Surface Area (Walls + Ends)", "default_display": "384.0000 units²", "highlight": True}
        ],
        "proof_steps": [
            {"step_title": "Uniform Cross-Section Volumetric Extrusion", "step_text": "The volume of any right prism equals the area of its base polygon multiplied by its length: A_base = ½ · b · h. Volume V = A_base · L = ½ · b · h · L."},
            {"step_title": "Lateral Wall Area", "step_text": "Assuming an isosceles triangular cross-section with slanted leg s = √[(b/2)² + h²], the perimeter is P_base = b + 2s. Lateral Area = P_base · L."},
            {"step_title": "Total Closed Net", "step_text": "Total Area = (2 × A_base) + Lateral Area."}
        ],
        "faqs": [
            {"q": "What is the optical dispersion property of an equilateral glass prism?", "a": "Isaac Newton proved in 1666 that a triangular glass prism refracts white sunlight into its constituent spectral colors because the refractive index of glass varies inversely with wavelength (Snell's Law dispersion)."},
            {"q": "How many vertices, edges, and faces does a triangular prism have?", "a": "A triangular prism has 5 faces (2 triangular bases + 3 rectangular sides), 9 edges, and 6 vertices, satisfying Euler's polyhedral formula V - E + F = 6 - 9 + 5 = 2."}
        ],
        "js_logic": """
          const b = getNum('base_width');
          const h = getNum('base_height');
          const L = getNum('prism_length');

          const baseArea = 0.5 * b * h;
          const vol = baseArea * L;
          const s = Math.sqrt(Math.pow(b / 2, 2) + Math.pow(h, 2));
          const perim = b + (2 * s);
          const lat = perim * L;
          const tot = (2 * baseArea) + lat;

          setDisp('prism_volume', vol.toFixed(4) + ' units³');
          setDisp('base_face_area', baseArea.toFixed(4) + ' units²');
          setDisp('lateral_surface', lat.toFixed(4) + ' units²');
          setDisp('total_surface', tot.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "pyramid",
        "category": "geometry",
        "name": "Square Pyramid Volume & Slant Height Calculator",
        "description": "Calculate square and rectangular pyramid volume, lateral slant height, lateral face area, and total surface area.",
        "hero_badge": "Pyramidal Geometry • Square Pyramid Matrix",
        "formula_display": "Volume = ⅓ · a² · h | Slant Height s = √[h² + (a/2)²]",
        "fields": [
            {"id": "base_side", "label": "Square Base Side (a)", "default": 10, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Edge length of square base"},
            {"id": "vertical_height", "label": "Vertical Height (h)", "default": 12, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Height from apex to base center"}
        ],
        "metrics": [
            {"id": "pyramid_volume", "label": "Pyramid Volume", "default_display": "400.0000 units³", "highlight": True},
            {"id": "slant_height", "label": "Lateral Face Slant Height (s)", "default_display": "13.0000 units", "highlight": True},
            {"id": "lateral_surface", "label": "Lateral Triangular Face Area", "default_display": "260.0000 units²"},
            {"id": "total_surface", "label": "Total Surface Area (Base + Faces)", "default_display": "360.0000 units²"}
        ],
        "proof_steps": [
            {"step_title": "Pyramidal Volume Proof", "step_text": "Three congruent pyramids assemble exactly into a cube or square prism of identical base and height: Volume = ⅓ · a² · h."},
            {"step_title": "Lateral Face Altitude via Pythagorean Theorem", "step_text": "The vertical height h, apothem of base a/2, and slant height s form a right triangle: s = √[h² + (a/2)²]."},
            {"step_title": "Four Triangular Faces Net", "step_text": "Lateral Area = 4 × [½ · a · s] = 2 · a · s. Total Area = a² + 2as."}
        ],
        "faqs": [
            {"q": "What are the dimensions of the Great Pyramid of Giza?", "a": "The Great Pyramid of Giza originally had a base side of ~230.3 meters (~755.6 ft) and a height of ~146.6 meters (~481 ft), yielding a volume of ~2.59 million cubic meters."},
            {"q": "What is the difference between slant height and pyramid height?", "a": "Vertical height is the perpendicular altitude from the apex straight down to the base center. Slant height is the altitude running along the sloping surface of an exterior triangular face to the edge midpoint."}
        ],
        "js_logic": """
          const a = getNum('base_side');
          const h = getNum('vertical_height');

          const s = Math.sqrt(Math.pow(h, 2) + Math.pow(a / 2, 2));
          const vol = (1 / 3) * Math.pow(a, 2) * h;
          const lat = 2 * a * s;
          const tot = Math.pow(a, 2) + lat;

          setDisp('pyramid_volume', vol.toFixed(4) + ' units³');
          setDisp('slant_height', s.toFixed(4) + ' units');
          setDisp('lateral_surface', lat.toFixed(4) + ' units²');
          setDisp('total_surface', tot.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "frustum-cone",
        "category": "geometry",
        "name": "Frustum of a Cone (Truncated Cone) Calculator",
        "description": "Calculate volume, lateral surface area, slant height, and total surface area of a truncated cone (frustum) from base radii and height.",
        "hero_badge": "Truncated Solids • Conical Frustum Matrix",
        "formula_display": "Volume = ⅓ · π · h · (R² + Rr + r²) | Slant Height s = √[h² + (R - r)²]",
        "fields": [
            {"id": "bottom_radius", "label": "Bottom Base Radius (R)", "default": 8, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Radius of larger circular base"},
            {"id": "top_radius", "label": "Top Base Radius (r)", "default": 4, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius of smaller circular top base"},
            {"id": "frustum_height", "label": "Frustum Height (h)", "default": 10, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Vertical distance between parallel bases"}
        ],
        "metrics": [
            {"id": "frustum_volume", "label": "Frustum Volume", "default_display": "1,172.8613 units³", "highlight": True},
            {"id": "slant_height", "label": "Slant Height (s)", "default_display": "10.7703 units"},
            {"id": "lateral_surface", "label": "Lateral Surface Area", "default_display": "406.0270 units²", "highlight": True},
            {"id": "total_surface", "label": "Total Surface Area", "default_display": "657.3697 units²"}
        ],
        "proof_steps": [
            {"step_title": "Subtractive Conical Calculus", "step_text": "A frustum is formed by subtracting a small cone of height h₁ from a full cone of height h₂ = h + h₁. By similar triangles, r/R = h₁ / (h + h₁). Integrating slices: V = ⅓ · π · h · (R² + Rr + r²)."},
            {"step_title": "Slant Pythagorean Relation", "step_text": "The difference in radii (R - r) forms the base of a right triangle with altitude h: Slant Height s = √[h² + (R - r)²]."},
            {"step_title": "Lateral Surface Sector Difference", "step_text": "Lateral Area A_lat = π(R + r)s. Total Area = A_lat + πR² + πr²."}
        ],
        "faqs": [
            {"q": "What everyday objects are shaped as conical frustums?", "a": "Buckets, paper coffee cups, lampshades, plant pots, and cooling towers for power plants are all engineered as conical frustums."},
            {"q": "How does a frustum volume compare to a simple cylinder?", "a": "A cylinder with average radius r_avg = (R + r)/2 underestimates true frustum volume because volumetric growth scales quadratically (r²). The frustum volume formula accurately captures this non-linear cross-sectional expansion."}
        ],
        "js_logic": """
          let R = getNum('bottom_radius');
          let r = getNum('top_radius');
          if (r > R) { const tmp = R; R = r; r = tmp; }
          const h = getNum('frustum_height');

          const s = Math.sqrt(Math.pow(h, 2) + Math.pow(R - r, 2));
          const vol = (1 / 3) * Math.PI * h * (Math.pow(R, 2) + (R * r) + Math.pow(r, 2));
          const lat = Math.PI * (R + r) * s;
          const tot = lat + (Math.PI * Math.pow(R, 2)) + (Math.PI * Math.pow(r, 2));

          setDisp('frustum_volume', vol.toFixed(4) + ' units³');
          setDisp('slant_height', s.toFixed(4) + ' units');
          setDisp('lateral_surface', lat.toFixed(4) + ' units²');
          setDisp('total_surface', tot.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "frustum-pyramid",
        "category": "geometry",
        "name": "Frustum of a Pyramid (Truncated Pyramid) Calculator",
        "description": "Calculate volume, slant height, and surface area of a truncated square pyramid from top base a₁, bottom base a₂, and height.",
        "hero_badge": "Ancient Egyptian Geometry • Moscow Papyrus Matrix",
        "formula_display": "Volume = ⅓ · h · (A₁ + A₂ + √(A₁ · A₂))",
        "fields": [
            {"id": "bottom_side", "label": "Bottom Square Side (a₁)", "default": 12, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Side length of lower base"},
            {"id": "top_side", "label": "Top Square Side (a₂)", "default": 6, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Side length of upper base"},
            {"id": "frustum_height", "label": "Frustum Height (h)", "default": 9, "suffix": "units", "min": 0.5, "max": 1000, "step": 0.5, "hint": "Vertical distance between bases"}
        ],
        "metrics": [
            {"id": "pyramid_frustum_vol", "label": "Frustum Volume", "default_display": "756.0000 units³", "highlight": True},
            {"id": "face_slant_height", "label": "Lateral Face Slant Height (s)", "default_display": "9.4868 units"},
            {"id": "trapezoid_faces_area", "label": "4 Lateral Trapezoid Faces", "default_display": "341.5260 units²", "highlight": True},
            {"id": "total_surface_area", "label": "Total Surface Area", "default_display": "521.5260 units²"}
        ],
        "proof_steps": [
            {"step_title": "The Moscow Mathematical Papyrus (Problem 14)", "step_text": "Dating to 1850 BC, Problem 14 in the Egyptian Moscow Papyrus provides the exact modern formula: V = ⅓ · h · (a₁² + a₁a₂ + a₂²)."},
            {"step_title": "Geometric Mean Base Cross-Section", "step_text": "For any truncated pyramid with top area A₂ and bottom area A₁: Volume V = ⅓ · h · [A₁ + A₂ + √(A₁ · A₂)]."},
            {"step_title": "Lateral Trapezoidal Faces", "step_text": "Each of the 4 lateral faces is an isosceles trapezoid with bases a₁ and a₂ and altitude s = √[h² + ((a₁ - a₂)/2)²]. Lateral Area = 4 × [½(a₁ + a₂)s] = 2(a₁ + a₂)s."}
        ],
        "faqs": [
            {"q": "Why is the Moscow Papyrus Problem 14 so historically famous?", "a": "It is widely considered the pinnacle of ancient Egyptian mathematics, proving that ancient geometers knew the exact non-trivial formula for a truncated pyramid millennia before calculus was formalized."},
            {"q": "What structures use truncated pyramid geometry?", "a": "Mayan and Aztec step pyramids (such as El Castillo at Chichen Itza), obelisk pedestals, and concrete civil bridge piers."}
        ],
        "js_logic": """
          let a1 = getNum('bottom_side');
          let a2 = getNum('top_side');
          if (a2 > a1) { const tmp = a1; a1 = a2; a2 = tmp; }
          const h = getNum('frustum_height');

          const s = Math.sqrt(Math.pow(h, 2) + Math.pow((a1 - a2) / 2, 2));
          const A1 = Math.pow(a1, 2);
          const A2 = Math.pow(a2, 2);
          const vol = (1 / 3) * h * (A1 + A2 + Math.sqrt(A1 * A2));
          const lat = 2 * (a1 + a2) * s;
          const tot = lat + A1 + A2;

          setDisp('pyramid_frustum_vol', vol.toFixed(4) + ' units³');
          setDisp('face_slant_height', s.toFixed(4) + ' units');
          setDisp('trapezoid_faces_area', lat.toFixed(4) + ' units²');
          setDisp('total_surface_area', tot.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "ellipsoid",
        "category": "geometry",
        "name": "Ellipsoid Volume & Surface Area Calculator",
        "description": "Calculate ellipsoid volume and surface area using the Knud Thomsen p-norm approximation formula from semi-axes a, b, and c.",
        "hero_badge": "Triaxial Geometry • Ellipsoid Volumetric Solver",
        "formula_display": "Volume = 4/3 · π · a · b · c | Surface Area ≈ 4π · [((ab)^p + (ac)^p + (bc)^p) / 3]^(1/p), p ≈ 1.6075",
        "fields": [
            {"id": "axis_a", "label": "Semi-Axis a", "default": 8, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius along x-axis"},
            {"id": "axis_b", "label": "Semi-Axis b", "default": 5, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius along y-axis"},
            {"id": "axis_c", "label": "Semi-Axis c", "default": 3, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius along z-axis"}
        ],
        "metrics": [
            {"id": "ellipsoid_volume", "label": "Exact Ellipsoid Volume", "default_display": "502.6548 units³", "highlight": True},
            {"id": "thomsen_surface", "label": "Surface Area (Knud Thomsen)", "default_display": "339.7371 units²", "highlight": True},
            {"id": "geometric_mean_radius", "label": "Geometric Mean Radius", "default_display": "4.9324 units"},
            {"id": "ellipsoid_type", "label": "Ellipsoid Classification", "default_display": "Triaxial Scalene (a ≠ b ≠ c)"}
        ],
        "proof_steps": [
            {"step_title": "Ellipsoid Volume Integral", "step_text": "Subjecting the unit sphere x² + y² + z² ≤ 1 to the linear stretch matrix diag(a, b, c): V = 4/3 · π · a · b · c. This formula is exact for all ellipsoids."},
            {"step_title": "Knud Thomsen Surface Area Formula", "step_text": "Because exact surface area requires incomplete elliptic integrals of the first and second kind, Knud Thomsen devised the formula: Area ≈ 4π · [((ab)ᵖ + (ac)ᵖ + (bc)ᵖ) / 3]^(1/p), where optimal parameter p = ln(3)/ln(2) ≈ 1.6075."},
            {"step_title": "Bound on Relative Error", "step_text": "Thomsen's formula bounds maximum relative error to less than 1.061% over all possible triaxial geometries."}
        ],
        "faqs": [
            {"q": "What is the shape of planet Earth?", "a": "Due to centrifugal forces from axial rotation, Earth is not a perfect sphere but an oblate spheroid (an ellipsoid with a = b = 6,378.1 km at the equator and c = 6,356.8 km at the poles)."},
            {"q": "What is the difference between a prolate and oblate ellipsoid?", "a": "A prolate spheroid (football shape) has a = b < c (elongated along its polar axis). An oblate spheroid (flattened disk) has a = b > c."}
        ],
        "js_logic": """
          const a = getNum('axis_a');
          const b = getNum('axis_b');
          const c = getNum('axis_c');

          const vol = (4 / 3) * Math.PI * a * b * c;
          const p = 1.6075;
          const term = (Math.pow(a * b, p) + Math.pow(a * c, p) + Math.pow(b * c, p)) / 3;
          const sa = 4 * Math.PI * Math.pow(term, 1 / p);
          const rMean = Math.cbrt(a * b * c);

          let classification = 'Triaxial Scalene (a ≠ b ≠ c)';
          if (a === b && b === c) classification = 'Perfect Sphere (a = b = c)';
          else if (a === b && c < a) classification = 'Oblate Spheroid (a = b > c)';
          else if (a === b && c > a) classification = 'Prolate Spheroid (a = b < c)';

          setDisp('ellipsoid_volume', vol.toFixed(4) + ' units³');
          setDisp('thomsen_surface', sa.toFixed(4) + ' units²');
          setDisp('geometric_mean_radius', rMean.toFixed(4) + ' units');
          setDisp('ellipsoid_type', classification);
        """
    },
    {
        "slug": "arc-length",
        "category": "geometry",
        "name": "Arc Length, Sector Area & Chord Calculator",
        "description": "Calculate circular arc length (s), sector area, segment area, and chord length from circle radius and central angle (degrees or radians).",
        "hero_badge": "Trigonometry • Circular Arc & Sector Matrix",
        "formula_display": "Arc Length s = r · θ (rad) = [π · r · θ°] / 180° | Sector Area = ½ · r² · θ",
        "fields": [
            {"id": "circle_radius", "label": "Circle Radius (r)", "default": 10, "suffix": "units", "min": 0.1, "max": 1000, "step": 0.5, "hint": "Radius of circle"},
            {"id": "central_angle_deg", "label": "Central Angle (θ in Degrees)", "default": 60, "suffix": "degrees", "min": 1, "max": 360, "step": 1, "hint": "Angle subtended at center"}
        ],
        "metrics": [
            {"id": "arc_length_val", "label": "Arc Length (s)", "default_display": "10.4720 units", "highlight": True},
            {"id": "sector_area_val", "label": "Sector Area (Pie Slice)", "default_display": "52.3599 units²", "highlight": True},
            {"id": "chord_length_val", "label": "Chord Length (c)", "default_display": "10.0000 units"},
            {"id": "segment_area_val", "label": "Segment Area (Between Arc & Chord)", "default_display": "9.0586 units²"}
        ],
        "proof_steps": [
            {"step_title": "Radian Definition and Arc Length", "step_text": "One radian is defined as the central angle subtending an arc equal in length to the circle's radius. Converting degrees to radians: θ_rad = θ° · (π / 180°). Arc Length s = r · θ_rad."},
            {"step_title": "Sector Area Derivation", "step_text": "Sector area is proportional to the fraction of the full circle: Area_sector = (θ° / 360°) · πr² = ½ · r² · θ_rad."},
            {"step_title": "Chord Length and Segment Area", "step_text": "Bisecting the isosceles triangle formed by the radius arms yields chord length: c = 2r · sin(θ / 2). Circular Segment Area = Area_sector - Area_triangle = ½ · r² · (θ_rad - sin θ_rad)."}
        ],
        "faqs": [
            {"q": "What is the difference between a circular sector and a circular segment?", "a": "A circular sector is a pie-slice shape bounded by two radius lines and an arc. A circular segment is the smaller region between a straight chord line and the circular arc."},
            {"q": "Why are angles measured in radians in calculus?", "a": "In calculus, using radians preserves simple derivatives such as d/dx(sin x) = cos x. If measured in degrees, an extra unwieldy factor of π/180 appears in every trigonometric derivative and integral."}
        ],
        "js_logic": """
          const r = getNum('circle_radius');
          const deg = getNum('central_angle_deg');

          const rad = (deg * Math.PI) / 180;
          const s = r * rad;
          const sector = 0.5 * Math.pow(r, 2) * rad;
          const chord = 2 * r * Math.sin(rad / 2);
          const triArea = 0.5 * Math.pow(r, 2) * Math.sin(rad);
          const segment = Math.max(0, sector - triArea);

          setDisp('arc_length_val', s.toFixed(4) + ' units');
          setDisp('sector_area_val', sector.toFixed(4) + ' units²');
          setDisp('chord_length_val', chord.toFixed(4) + ' units');
          setDisp('segment_area_val', segment.toFixed(4) + ' units²');
        """
    },
    {
        "slug": "projectile-motion",
        "category": "physics",
        "name": "Projectile Motion & Ballistic Trajectory Calculator",
        "description": "Calculate ballistic flight trajectory, maximum apogee height, total hang time, and horizontal ground range under gravitational acceleration.",
        "hero_badge": "Classical Kinematics • Ballistic Vector Matrix",
        "formula_display": "Range R = [v₀² · sin(2θ)] / g | Max Height H = [v₀² · sin²(θ)] / (2g)",
        "fields": [
            {"id": "velocity_v0", "label": "Initial Launch Velocity (v₀)", "default": 45, "suffix": "m/s", "min": 1, "max": 5000, "step": 1, "hint": "Muzzle or launch velocity in meters per second"},
            {"id": "launch_angle", "label": "Launch Angle (θ)", "default": 45, "suffix": "degrees", "min": 1, "max": 89, "step": 1, "hint": "Angle above horizontal (45° maximizes range in vacuum)"},
            {"id": "initial_height", "label": "Initial Release Height (y₀)", "default": 0, "suffix": "meters", "min": 0, "max": 1000, "step": 1, "hint": "Elevation of launch platform above ground"}
        ],
        "metrics": [
            {"id": "max_range", "label": "Total Horizontal Range", "default_display": "206.42 meters", "highlight": True},
            {"id": "max_height", "label": "Maximum Altitude (Apogee)", "default_display": "51.61 meters", "highlight": True},
            {"id": "flight_time", "label": "Total Hang Time", "default_display": "6.49 seconds"},
            {"id": "impact_velocity", "label": "Terminal Impact Velocity", "default_display": "45.00 m/s (162.0 km/h)"}
        ],
        "proof_steps": [
            {"step_title": "Orthogonal Vector Velocity Decomposition", "step_text": "Horizontal velocity: v_x = v₀ · cos(θ). Vertical velocity: v_y = v₀ · sin(θ). In vacuum kinematics, horizontal velocity remains constant (a_x = 0)."},
            {"step_title": "Apogee Altitude and Vertical Ascent Time", "step_text": "At maximum height, vertical velocity drops to zero (v_y = 0): t_apex = (v₀ sin θ) / g. Peak height H = y₀ + (v₀² sin² θ) / 2g."},
            {"step_title": "Quadratic Ground Impact Time", "step_text": "Solving y(t) = y₀ + (v₀ sin θ)t - ½gt² = 0 for positive root t_impact yields total flight duration. Range R = v_x · t_impact."}
        ],
        "faqs": [
            {"q": "Why is 45 degrees the optimal launch angle for maximum range?", "a": "Because horizontal range is proportional to sin(2θ). The sine function achieves its maximum value of 1.0 at 90°, so 2θ = 90° implies θ = 45° in an ideal vacuum without aerodynamic drag."},
            {"q": "How does air resistance change the optimal launch angle?", "a": "Aerodynamic atmospheric drag dissipates kinetic energy continuously over distance, shifting the optimal launch angle for baseballs, golf balls, and artillery down to 32° to 38°."}
        ],
        "js_logic": """
          const v0 = getNum('velocity_v0');
          const deg = getNum('launch_angle');
          const y0 = getNum('initial_height');
          const g = 9.80665;

          const rad = (deg * Math.PI) / 180;
          const vx = v0 * Math.cos(rad);
          const vy = v0 * Math.sin(rad);

          // Quadratic formula for flight time: -0.5*g*t^2 + vy*t + y0 = 0
          const a = -0.5 * g;
          const b = vy;
          const c = y0;
          const disc = Math.pow(b, 2) - (4 * a * c);
          const t = (-b - Math.sqrt(Math.max(0, disc))) / (2 * a);

          const range = vx * t;
          const hMax = y0 + (Math.pow(vy, 2) / (2 * g));
          const vyImpact = vy - (g * t);
          const vImpact = Math.sqrt(Math.pow(vx, 2) + Math.pow(vyImpact, 2));

          setDisp('max_range', range.toFixed(2) + ' meters (' + (range * 3.28084).toFixed(1) + ' ft)');
          setDisp('max_height', hMax.toFixed(2) + ' meters (' + (hMax * 3.28084).toFixed(1) + ' ft)');
          setDisp('flight_time', t.toFixed(2) + ' seconds');
          setDisp('impact_velocity', vImpact.toFixed(2) + ' m/s (' + (vImpact * 3.6).toFixed(1) + ' km/h)');
        """
    },
    {
        "slug": "kinetic-energy",
        "category": "physics",
        "name": "Kinetic Energy & Linear Momentum Calculator",
        "description": "Calculate translational kinetic energy (Joules, ft-lbs), linear momentum, and relativistic velocity inversions from mass and velocity.",
        "hero_badge": "Newtonian Mechanics • Kinetic Energy Matrix",
        "formula_display": "Kinetic Energy E_k = ½ · m · v² | Momentum p = m · v",
        "fields": [
            {"id": "mass_kg", "label": "Object Mass (m)", "default": 80, "suffix": "kg", "min": 0.001, "max": 1000000, "step": 1, "hint": "Mass in kilograms (1 kg = 2.205 lbs)"},
            {"id": "velocity_ms", "label": "Velocity (v)", "default": 25, "suffix": "m/s", "min": 0.1, "max": 100000, "step": 1, "hint": "Speed in meters per second (25 m/s = 56 mph)"}
        ],
        "metrics": [
            {"id": "kinetic_joules", "label": "Kinetic Energy", "default_display": "25,000.0 Joules (25.0 kJ)", "highlight": True},
            {"id": "foot_pounds", "label": "Imperial Work (Foot-Pounds)", "default_display": "18,439.1 ft-lbs"},
            {"id": "momentum_val", "label": "Linear Momentum (p)", "default_display": "2,000.0 kg·m/s", "highlight": True},
            {"id": "tnt_equivalent", "label": "TNT Chemical Energy Equivalent", "default_display": "5.98 grams of TNT"}
        ],
        "proof_steps": [
            {"step_title": "Work-Energy Theorem Derivation", "step_text": "Work done on a mass is the line integral of force: W = ∫ F dx = ∫ (m · dv/dt) dx = m ∫ v dv = ½ · m · v²."},
            {"step_title": "Quadratic Velocity Scaling", "step_text": "Because velocity is squared, doubling vehicle speed quadruples (4×) required braking distance and collision impact energy."},
            {"step_title": "Momentum Relationship", "step_text": "Linear momentum p = mv. Kinetic energy can be expressed via momentum as E_k = p² / (2m). 1 Joule = 0.737562 ft-lbs."}
        ],
        "faqs": [
            {"q": "Why does braking distance quadruple when speed doubles?", "a": "Brakes perform mechanical work against kinetic energy (W = F · d = ½mv²). Since kinetic energy scales quadratically with velocity (v²), doubling your speed from 30 mph to 60 mph multiplies kinetic energy by 4, requiring 4 times the stopping distance."},
            {"q": "When does relativistic kinetic energy become necessary?", "a": "Classical Newtonian kinetic energy (½mv²) is accurate for speeds below ~10% the speed of light. Above 0.1c, Einstein's relativistic equation E_k = (γ - 1)mc² must be used to account for Lorentz factor γ."}
        ],
        "js_logic": """
          const m = getNum('mass_kg');
          const v = getNum('velocity_ms');

          const ke = 0.5 * m * Math.pow(v, 2);
          const p = m * v;
          const ftlbs = ke * 0.737562;
          const tntGrams = ke / 4184; // 1g TNT = 4184 Joules

          setDisp('kinetic_joules', ke.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' Joules (' + (ke / 1000).toFixed(2) + ' kJ)');
          setDisp('foot_pounds', Math.round(ftlbs).toLocaleString() + ' ft-lbs');
          setDisp('momentum_val', p.toFixed(1) + ' kg·m/s');
          setDisp('tnt_equivalent', tntGrams.toFixed(2) + ' grams of TNT');
        """
    },
    {
        "slug": "ohms-law",
        "category": "physics",
        "name": "Ohm's Law & Electrical Power (PIVR) Calculator",
        "description": "Calculate Voltage (V), Current (I), Resistance (R), and Electrical Power (P) with bidirectional four-quadrant PIVR inversions.",
        "hero_badge": "Electromagnetism • Four-Quadrant Ohm's Wheel",
        "formula_display": "V = I · R | Power P = V · I = I² · R = V² / R",
        "fields": [
            {"id": "voltage_v", "label": "Voltage (V)", "default": 120, "suffix": "volts", "min": 0.1, "max": 100000, "step": 1, "hint": "Electrical potential difference"},
            {"id": "resistance_r", "label": "Resistance (R)", "default": 15, "suffix": "ohms (Ω)", "min": 0.01, "max": 1000000, "step": 0.5, "hint": "Circuit electrical resistance"}
        ],
        "metrics": [
            {"id": "current_amps", "label": "Current Draw (I)", "default_display": "8.000 Amperes", "highlight": True},
            {"id": "power_watts", "label": "Power Dissipated (P)", "default_display": "960.00 Watts", "highlight": True},
            {"id": "power_hp", "label": "Mechanical Horsepower", "default_display": "1.29 HP (746 W/HP)"},
            {"id": "conductance_siemens", "label": "Electrical Conductance (G = 1/R)", "default_display": "0.0667 Siemens"}
        ],
        "proof_steps": [
            {"step_title": "Drude Electron Conduction Model", "step_text": "Discovered experimentally by Georg Ohm in 1827: Current I through a conductor between two points is directly proportional to voltage V and inversely proportional to resistance R: I = V / R."},
            {"step_title": "Joule Heating and Thermodynamic Power", "step_text": "Joule's first law defines electrical power dissipation: P = V · I. Substituting Ohm's law yields P = (IR) · I = I²R = V² / R."},
            {"step_title": "Four-Quadrant PIVR Matrix Invariant", "step_text": "Given any two known variables among {P, I, V, R}, all remaining parameters are resolved through twelve deterministic algebraic substitutions."}
        ],
        "faqs": [
            {"q": "What is the difference between AC impedance and DC resistance?", "a": "In direct current (DC) circuits, resistance R opposes electron flow. In alternating current (AC) circuits, total opposition is termed impedance Z = √(R² + X²), where reactance X accounts for inductive coils and capacitors."},
            {"q": "Why does doubling voltage quadruple power in a fixed resistance?", "a": "Because power scales with voltage squared: P = V² / R. If voltage across a heating element doubles from 120V to 240V, heat output increases by a factor of 4."}
        ],
        "js_logic": """
          const V = getNum('voltage_v');
          const R = getNum('resistance_r');

          const I = R > 0 ? (V / R) : 0;
          const P = V * I;
          const hp = P / 745.7;
          const G = R > 0 ? (1 / R) : 0;

          setDisp('current_amps', I.toFixed(3) + ' Amperes');
          setDisp('power_watts', P.toFixed(2) + ' Watts (' + (P / 1000).toFixed(3) + ' kW)');
          setDisp('power_hp', hp.toFixed(2) + ' HP');
          setDisp('conductance_siemens', G.toFixed(4) + ' Siemens (mho)');
        """
    },
    {
        "slug": "density-mass-volume",
        "category": "physics",
        "name": "Density, Mass & Volume Calculator",
        "description": "Calculate material density (ρ), total mass, and displacement volume with bidirectional inversions and material reference library.",
        "hero_badge": "Continuum Mechanics • Density Invariant Matrix",
        "formula_display": "Density ρ = Mass / Volume | Mass = ρ · Volume | Volume = Mass / ρ",
        "fields": [
            {"id": "mass_val", "label": "Mass (m)", "default": 19.3, "suffix": "kg", "min": 0.001, "max": 1000000, "step": 0.1, "hint": "Mass of the material"},
            {"id": "volume_val", "label": "Volume (V)", "default": 0.001, "suffix": "m³", "min": 0.00001, "max": 10000, "step": 0.0001, "hint": "1 m³ = 1,000 Liters = 1,000,000 cm³"}
        ],
        "metrics": [
            {"id": "density_kgm3", "label": "Calculated Density (ρ)", "default_display": "19,300 kg/m³ (19.3 g/cm³)", "highlight": True},
            {"id": "specific_gravity", "label": "Specific Gravity (Relative to Water)", "default_display": "19.30 (Pure Gold)", "highlight": True},
            {"id": "density_imperial", "label": "Imperial Density", "default_display": "1,204.8 lbs / cu ft"},
            {"id": "buoyancy_fate", "label": "Buoyancy Behavior in Fresh Water", "default_display": "Sinks (Negative Buoyancy)"}
        ],
        "proof_steps": [
            {"step_title": "Continuum Intensive Property", "step_text": "Density ρ = dm / dV. Unlike mass and volume which are extensive variables, density is an intensive physical property invariant to sample quantity."},
            {"step_title": "Specific Gravity and Buoyancy", "step_text": "Specific Gravity SG = ρ_substance / ρ_H2O (at 4°C, where ρ_water = 1,000 kg/m³ = 1.0 g/cm³)."},
            {"step_title": "Archimedes' Buoyancy Principle", "step_text": "An object submerged in fluid experiences an upward buoyant force equal to the weight of the displaced fluid: F_buoyant = ρ_fluid · V · g. If SG < 1.0, the object floats; if SG > 1.0, it sinks."}
        ],
        "faqs": [
            {"q": "What is the densest naturally occurring element on Earth?", "a": "Osmium is the densest naturally occurring element, with a density of 22,590 kg/m³ (22.59 g/cm³), narrowly surpassing iridium (22.56 g/cm³)."},
            {"q": "Why does ice float on liquid water?", "a": "Water exhibits a rare density anomaly: hydrogen bonding creates an open hexagonal crystalline lattice when freezing, causing solid ice (density ~917 kg/m³) to expand and float in liquid water (density ~1,000 kg/m³)."}
        ],
        "js_logic": """
          const m = getNum('mass_val');
          const V = getNum('volume_val');

          const rho = V > 0 ? (m / V) : 0;
          const gcm3 = rho / 1000;
          const sg = rho / 1000;
          const lbCuFt = rho * 0.062428;

          setDisp('density_kgm3', Math.round(rho).toLocaleString() + ' kg/m³ (' + gcm3.toFixed(2) + ' g/cm³)');
          setDisp('specific_gravity', sg.toFixed(2) + (Math.abs(sg - 19.3) < 0.5 ? ' (~Gold)' : (Math.abs(sg - 7.8) < 0.5 ? ' (~Steel)' : '')));
          setDisp('density_imperial', lbCuFt.toFixed(1) + ' lbs / cu ft');
          setDisp('buoyancy_fate', sg < 1.0 ? 'Floats (Positive Buoyancy)' : 'Sinks (Negative Buoyancy)');
        """
    },
    {
        "slug": "quadratic-formula",
        "category": "calculus",
        "name": "Quadratic Formula & Parabola Vertex Calculator",
        "description": "Calculate real and complex roots, discriminant (Δ = b² - 4ac), and vertex coordinates of any quadratic equation ax² + bx + c = 0.",
        "hero_badge": "Algebraic Analysis • Quadratic Discriminant Matrix",
        "formula_display": "Roots x = [-b ± √(b² - 4ac)] / (2a) | Discriminant Δ = b² - 4ac",
        "fields": [
            {"id": "coeff_a", "label": "Quadratic Coefficient (a)", "default": 2, "min": -1000, "max": 1000, "step": 0.5, "hint": "Must be non-zero (a ≠ 0)"},
            {"id": "coeff_b", "label": "Linear Coefficient (b)", "default": -4, "min": -1000, "max": 1000, "step": 0.5, "hint": "Coefficient of x"},
            {"id": "coeff_c", "label": "Constant Term (c)", "default": -6, "min": -1000, "max": 1000, "step": 0.5, "hint": "y-intercept constant"}
        ],
        "metrics": [
            {"id": "root_x1", "label": "Root x₁", "default_display": "x₁ = 3.0000", "highlight": True},
            {"id": "root_x2", "label": "Root x₂", "default_display": "x₂ = -1.0000", "highlight": True},
            {"id": "discriminant_val", "label": "Discriminant (Δ = b² - 4ac)", "default_display": "Δ = 64.0000 (Two Real Roots)"},
            {"id": "parabola_vertex", "label": "Parabola Vertex (h, k)", "default_display": "(1.0000, -8.0000)"}
        ],
        "proof_steps": [
            {"step_title": "Completing the Square Proof", "step_text": "Dividing ax² + bx + c = 0 by a yields x² + (b/a)x = -c/a. Adding (b/2a)² to both sides: [x + b/2a]² = (b² - 4ac) / 4a². Taking square roots yields the iconic formula x = [-b ± √(b² - 4ac)] / 2a."},
            {"step_title": "Discriminant Root Characterization", "step_text": "If Δ > 0: Two distinct real roots. If Δ = 0: Exactly one repeated real root (tangent to x-axis). If Δ < 0: Two conjugate complex roots x = -b/2a ± i√(4ac - b²) / 2a."},
            {"step_title": "Vertex Calculus Extrema", "step_text": "Differentiating dy/dx = 2ax + b = 0 gives the vertex axis of symmetry: h = -b / (2a), and minimum/maximum value k = c - b² / (4a)."}
        ],
        "faqs": [
            {"q": "What does a negative discriminant mean geometrically?", "a": "A negative discriminant (Δ < 0) means the parabola's vertex lies above the x-axis (if opening upward) or below the x-axis (if opening downward), so the curve never intersects the x-axis in real space."},
            {"q": "What are Vieta's formulas for quadratics?", "a": "Vieta's formulas state that the sum of roots equals -b/a (x₁ + x₂ = -b/a) and the product of roots equals c/a (x₁ · x₂ = c/a)."}
        ],
        "js_logic": """
          const a = getNum('coeff_a') || 1;
          const b = getNum('coeff_b');
          const c = getNum('coeff_c');

          const disc = Math.pow(b, 2) - (4 * a * c);
          const h = -b / (2 * a);
          const k = c - (Math.pow(b, 2) / (4 * a));

          if (disc > 0) {
            const x1 = (-b + Math.sqrt(disc)) / (2 * a);
            const x2 = (-b - Math.sqrt(disc)) / (2 * a);
            setDisp('root_x1', 'x₁ = ' + x1.toFixed(4));
            setDisp('root_x2', 'x₂ = ' + x2.toFixed(4));
            setDisp('discriminant_val', 'Δ = ' + disc.toFixed(4) + ' (Two Distinct Real Roots)');
          } else if (disc === 0) {
            const x = -b / (2 * a);
            setDisp('root_x1', 'x = ' + x.toFixed(4));
            setDisp('root_x2', 'Repeated Root');
            setDisp('discriminant_val', 'Δ = 0 (One Repeated Real Root)');
          } else {
            const real = (-b / (2 * a)).toFixed(4);
            const imag = (Math.sqrt(-disc) / (2 * Math.abs(a))).toFixed(4);
            setDisp('root_x1', real + ' + ' + imag + 'i');
            setDisp('root_x2', real + ' - ' + imag + 'i');
            setDisp('discriminant_val', 'Δ = ' + disc.toFixed(4) + ' (Two Complex Conjugate Roots)');
          }

          setDisp('parabola_vertex', '(' + h.toFixed(4) + ', ' + k.toFixed(4) + ') ' + (a > 0 ? 'Min' : 'Max'));
        """
    },
    {
        "slug": "standard-deviation",
        "category": "statistics",
        "name": "Standard Deviation & Variance Calculator",
        "description": "Calculate sample and population standard deviation, variance, arithmetic mean, and sum of squared deviations for statistical datasets.",
        "hero_badge": "Statistical Inference • Variance & Dispersion Matrix",
        "formula_display": "Sample s = √[∑(xᵢ - x̄)² / (n - 1)] | Population σ = √[∑(xᵢ - μ)² / N]",
        "fields": [
            {"id": "val_1", "label": "Value 1", "default": 12, "min": -10000, "max": 10000, "step": 1, "hint": "Data point 1"},
            {"id": "val_2", "label": "Value 2", "default": 18, "min": -10000, "max": 10000, "step": 1, "hint": "Data point 2"},
            {"id": "val_3", "label": "Value 3", "default": 24, "min": -10000, "max": 10000, "step": 1, "hint": "Data point 3"},
            {"id": "val_4", "label": "Value 4", "default": 30, "min": -10000, "max": 10000, "step": 1, "hint": "Data point 4"},
            {"id": "val_5", "label": "Value 5", "default": 36, "min": -10000, "max": 10000, "step": 1, "hint": "Data point 5"}
        ],
        "metrics": [
            {"id": "sample_sd", "label": "Sample Standard Deviation (s)", "default_display": "9.4868", "highlight": True},
            {"id": "population_sd", "label": "Population Standard Deviation (σ)", "default_display": "8.4853", "highlight": True},
            {"id": "arithmetic_mean", "label": "Arithmetic Mean (x̄)", "default_display": "24.0000"},
            {"id": "sample_variance", "label": "Sample Variance (s²)", "default_display": "90.0000"}
        ],
        "proof_steps": [
            {"step_title": "Mean Centering Transformation", "step_text": "The sample mean x̄ = (1/n) ∑ xᵢ. Deviations from mean dᵢ = xᵢ - x̄."},
            {"step_title": "Bessel's Correction for Unbiased Variance", "step_text": "Dividing by n underestimates population variance because deviations are calculated from the sample mean rather than true population mean μ. Bessel's correction divides by (n - 1) degrees of freedom to yield an unbiased estimator: s² = ∑ dᵢ² / (n - 1)."},
            {"step_title": "Standard Deviation Metric", "step_text": "Standard deviation s = √(s²) returns dispersion back to original measurement units."}
        ],
        "faqs": [
            {"q": "When should I use sample standard deviation vs population standard deviation?", "a": "Use sample standard deviation (n - 1) whenever your dataset is a sample representing a larger population. Use population standard deviation (N) only when your data represents 100% of the entire target population."},
            {"q": "What is the 68-95-99.7 empirical rule?", "a": "For a normal bell-curve distribution, approximately 68.27% of observations fall within ±1 standard deviation of the mean, 95.45% fall within ±2 standard deviations, and 99.73% fall within ±3 standard deviations."}
        ],
        "js_logic": """
          const vals = [
            getNum('val_1'),
            getNum('val_2'),
            getNum('val_3'),
            getNum('val_4'),
            getNum('val_5')
          ];

          const n = vals.length;
          const sum = vals.reduce((a, b) => a + b, 0);
          const mean = sum / n;
          const ss = vals.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0);

          const sVar = ss / (n - 1);
          const pVar = ss / n;
          const sSd = Math.sqrt(sVar);
          const pSd = Math.sqrt(pVar);

          setDisp('sample_sd', sSd.toFixed(4));
          setDisp('population_sd', pSd.toFixed(4));
          setDisp('arithmetic_mean', mean.toFixed(4));
          setDisp('sample_variance', sVar.toFixed(4) + ' (Pop: ' + pVar.toFixed(4) + ')');
        """
    },
    {
        "slug": "z-score",
        "category": "statistics",
        "name": "Z-Score & Standard Normal Distribution Calculator",
        "description": "Calculate standard score z, cumulative probability P(Z < z), two-tailed p-value, and percentile rank in a standard normal distribution.",
        "hero_badge": "Gaussian Statistics • Standard Normal Matrix",
        "formula_display": "z = (x - μ) / σ | Φ(z) = ½ · [1 + erf(z / √2)]",
        "fields": [
            {"id": "raw_score", "label": "Raw Value (x)", "default": 85, "min": -10000, "max": 10000, "step": 1, "hint": "Observed test score or data point"},
            {"id": "population_mean", "label": "Population Mean (μ)", "default": 70, "min": -10000, "max": 10000, "step": 1, "hint": "Average value of distribution"},
            {"id": "std_deviation", "label": "Standard Deviation (σ)", "default": 10, "min": 0.001, "max": 1000, "step": 0.5, "hint": "Spread of distribution (σ > 0)"}
        ],
        "metrics": [
            {"id": "z_score_val", "label": "Standard Score (z)", "default_display": "+1.5000", "highlight": True},
            {"id": "percentile_rank", "label": "Percentile Rank P(X < x)", "default_display": "93.32%", "highlight": True},
            {"id": "p_value_two_tail", "label": "Two-Tailed Probability p-value", "default_display": "0.1336"},
            {"id": "t_score_equiv", "label": "T-Score Equivalent (50 + 10z)", "default_display": "65.00"}
        ],
        "proof_steps": [
            {"step_title": "Standardization Normalization", "step_text": "The z-score measures how many standard deviations a raw observation x lies above or below the mean: z = (x - μ) / σ."},
            {"step_title": "Gaussian Cumulative Distribution Function", "step_text": "Cumulative probability Φ(z) = (1 / √2π) ∫₋∞ᶻ e^(-t²/2) dt = ½[1 + erf(z / √2)], where erf is the Gauss error function."},
            {"step_title": "Hypothesis Testing Benchmark", "step_text": "In two-tailed hypothesis testing, |z| ≥ 1.96 corresponds to p ≤ 0.05 (statistical significance), and |z| ≥ 2.576 corresponds to p ≤ 0.01."}
        ],
        "faqs": [
            {"q": "What does a negative z-score indicate?", "a": "A negative z-score indicates that the data point is below the distribution mean. For example, z = -1.5 means the value is 1.5 standard deviations below average."},
            {"q": "What percentage of data falls above z = 2.0?", "a": "Because Φ(2.0) = 0.9772 (97.72% below), exactly 2.28% of observations in a normal distribution fall above z = +2.0."}
        ],
        "js_logic": """
          const x = getNum('raw_score');
          const mu = getNum('population_mean');
          const sigma = getNum('std_deviation') || 1;

          const z = (x - mu) / sigma;

          // Approximation of error function erf(x)
          function erf(val) {
            const t = 1.0 / (1.0 + 0.3275911 * Math.abs(val));
            const poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
            const ans = 1.0 - poly * Math.exp(-val * val);
            return val >= 0 ? ans : -ans;
          }

          const phi = 0.5 * (1 + erf(z / Math.SQRT2));
          const pTwo = 2 * (1 - 0.5 * (1 + erf(Math.abs(z) / Math.SQRT2)));
          const tScore = 50 + (10 * z);

          setDisp('z_score_val', (z >= 0 ? '+' : '') + z.toFixed(4));
          setDisp('percentile_rank', (phi * 100).toFixed(2) + '%');
          setDisp('p_value_two_tail', pTwo.toFixed(4));
          setDisp('t_score_equiv', tScore.toFixed(2));
        """
    },
    {
        "slug": "permutations-combinations",
        "category": "statistics",
        "name": "Permutations & Combinations (nPr & nCr) Calculator",
        "description": "Calculate factorials, permutations (ordered nPr), and combinations (unordered binomial coefficients nCr) with exact integer precision.",
        "hero_badge": "Combinatorics • Discrete Math Matrix",
        "formula_display": "nPr = n! / (n - r)! | nCr = n! / [r! · (n - r)!]",
        "fields": [
            {"id": "total_n", "label": "Total Elements (n)", "default": 10, "min": 1, "max": 65, "step": 1, "hint": "Total pool size (n ≥ r)"},
            {"id": "sample_r", "label": "Subset Chosen (r)", "default": 3, "min": 0, "max": 65, "step": 1, "hint": "Number of elements chosen"}
        ],
        "metrics": [
            {"id": "combinations_ncr", "label": "Combinations nCr (Order Does Not Matter)", "default_display": "120", "highlight": True},
            {"id": "permutations_npr", "label": "Permutations nPr (Order Matters)", "default_display": "720", "highlight": True},
            {"id": "factorial_n", "label": "Factorial n!", "default_display": "3,628,800"},
            {"id": "multiplicity_factor", "label": "Permutation Expansion (r!)", "default_display": "6 (r! arrangements)"}
        ],
        "proof_steps": [
            {"step_title": "Fundamental Counting Principle", "step_text": "Selecting r elements in order from n items yields n choices for the first, (n - 1) for the second, ..., down to (n - r + 1): nPr = n! / (n - r)!."},
            {"step_title": "Symmetry and Division of Redundancy", "step_text": "If order is irrelevant, each group of r items can be arranged in r! identical ways: nCr = nPr / r! = n! / [r! · (n - r)!]."},
            {"step_title": "Pascal's Recurrence Identity", "step_text": "Binomial coefficients satisfy Pascal's rule: nCr = (n-1)C(r-1) + (n-1)Cr, mapping directly to rows of Pascal's Triangle."}
        ],
        "faqs": [
            {"q": "What is the key difference between permutations and combinations?", "a": "Order matters in permutations (e.g., a locker combination lock is actually a permutation, where 1-2-3 is distinct from 3-2-1). Order does NOT matter in combinations (e.g., lottery numbers or poker hands)."},
            {"q": "Why is 0! equal to 1?", "a": "By definition, there is exactly one way to arrange zero objects (the empty set). Defining 0! = 1 also preserves algebraic consistency in formulas like nPn = n! / 0! = n!."}
        ],
        "js_logic": """
          let n = Math.round(getNum('total_n'));
          let r = Math.round(getNum('sample_r'));
          if (r > n) r = n;

          function fact(k) {
            let res = 1;
            for (let i = 2; i <= k; i++) res *= i;
            return res;
          }

          function nPr(nVal, rVal) {
            let res = 1;
            for (let i = 0; i < rVal; i++) res *= (nVal - i);
            return res;
          }

          const pVal = nPr(n, r);
          const rFact = fact(r);
          const cVal = pVal / rFact;
          const nFact = n <= 20 ? fact(n).toLocaleString() : fact(n).toExponential(4);

          setDisp('combinations_ncr', Math.round(cVal).toLocaleString());
          setDisp('permutations_npr', Math.round(pVal).toLocaleString());
          setDisp('factorial_n', nFact);
          setDisp('multiplicity_factor', rFact.toLocaleString() + ' (r! arrangements)');
        """
    },
    {
        "slug": "bayes-theorem",
        "category": "statistics",
        "name": "Bayes' Theorem & Conditional Probability Calculator",
        "description": "Calculate posterior probability P(A|B), prior odds, likelihood ratio, and diagnostic true/false positive rates using Bayes' rule.",
        "hero_badge": "Epistemology & Probability • Bayesian Update Matrix",
        "formula_display": "P(A|B) = [P(B|A) · P(A)] / P(B)",
        "fields": [
            {"id": "prior_prob", "label": "Prior Probability P(A)", "default": 0.01, "min": 0.0001, "max": 0.999, "step": 0.005, "hint": "Base rate prevalence (e.g. 1% disease rate in population)"},
            {"id": "true_positive", "label": "Sensitivity / True Positive P(B|A)", "default": 0.95, "min": 0.50, "max": 1.0, "step": 0.01, "hint": "Test accuracy when condition is present"},
            {"id": "false_positive", "label": "False Positive Rate P(B|¬A)", "default": 0.05, "min": 0.001, "max": 0.50, "step": 0.005, "hint": "Test positive when condition is absent"}
        ],
        "metrics": [
            {"id": "posterior_prob", "label": "Posterior Probability P(A|B)", "default_display": "16.10% (Positive Predictive Value)", "highlight": True},
            {"id": "marginal_p_b", "label": "Total Evidence Probability P(B)", "default_display": "0.0590 (5.90% test positive)"},
            {"id": "bayes_factor", "label": "Likelihood Ratio / Bayes Factor", "default_display": "19.00× Evidence Strength", "highlight": True},
            {"id": "base_rate_fallacy", "label": "Base Rate Weighting", "default_display": "83.9% of positive results are false alarms"}
        ],
        "proof_steps": [
            {"step_title": "Conditional Probability Definition", "step_text": "Joint probability P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A). Equating both sides yields Bayes' Theorem: P(A|B) = [P(B|A) · P(A)] / P(B)."},
            {"step_title": "Law of Total Probability", "step_text": "The marginal evidence probability partitions across mutually exclusive hypotheses: P(B) = P(B|A) · P(A) + P(B|¬A) · P(¬A), where P(¬A) = 1 - P(A)."},
            {"step_title": "Base Rate Fallacy Resolution", "step_text": "When prior probability P(A) is very low (e.g. rare disease or rare defect), even a test with 95% sensitivity produces predominantly false positive signals."}
        ],
        "faqs": [
            {"q": "What is the Base Rate Fallacy?", "a": "The base rate fallacy is the cognitive error of judging conditional probability without factoring in background prior probability. If a rare disease affects 1 in 1,000 people, a 95% accurate test will still be wrong over 95% of the time on a positive result."},
            {"q": "How is Bayes' theorem used in machine learning and AI?", "a": "Bayesian inference powers spam filters, medical diagnostic AI, Markov Chain Monte Carlo (MCMC) simulations, and Kalman filters in autonomous vehicle navigation by continuously updating probabilities as new evidence arrives."}
        ],
        "js_logic": """
          const pA = getNum('prior_prob');
          const pBgivenA = getNum('true_positive');
          const pBgivenNotA = getNum('false_positive');

          const pNotA = 1 - pA;
          const pB = (pBgivenA * pA) + (pBgivenNotA * pNotA);
          const pAgivenB = pB > 0 ? ((pBgivenA * pA) / pB) : 0;
          const bayesFactor = pBgivenNotA > 0 ? (pBgivenA / pBgivenNotA) : 0;
          const falseAlarm = (1 - pAgivenB) * 100;

          setDisp('posterior_prob', (pAgivenB * 100).toFixed(2) + '% (PPV)');
          setDisp('marginal_p_b', pB.toFixed(4) + ' (' + (pB * 100).toFixed(2) + '% test positive)');
          setDisp('bayes_factor', bayesFactor.toFixed(2) + '× Evidence Strength');
          setDisp('base_rate_fallacy', falseAlarm.toFixed(1) + '% of positive results are false alarms');
        """
    },
    {
        "slug": "matrix-multiplication",
        "category": "calculus",
        "name": "2×2 Matrix Determinant & Inverse Calculator",
        "description": "Calculate 2×2 matrix determinant det(A), matrix trace, matrix inverse A⁻¹, characteristic polynomial, and eigenvalues.",
        "hero_badge": "Linear Algebra • Matrix Determinant Matrix",
        "formula_display": "det(A) = ad - bc | A⁻¹ = [1 / det(A)] · [ [d, -b], [-c, a] ]",
        "fields": [
            {"id": "elem_a", "label": "Element a (Row 1, Col 1)", "default": 4, "min": -1000, "max": 1000, "step": 0.5, "hint": "Top-left entry"},
            {"id": "elem_b", "label": "Element b (Row 1, Col 2)", "default": 7, "min": -1000, "max": 1000, "step": 0.5, "hint": "Top-right entry"},
            {"id": "elem_c", "label": "Element c (Row 2, Col 1)", "default": 2, "min": -1000, "max": 1000, "step": 0.5, "hint": "Bottom-left entry"},
            {"id": "elem_d", "label": "Element d (Row 2, Col 2)", "default": 6, "min": -1000, "max": 1000, "step": 0.5, "hint": "Bottom-right entry"}
        ],
        "metrics": [
            {"id": "matrix_det", "label": "Determinant det(A)", "default_display": "10.0000 (Invertible)", "highlight": True},
            {"id": "matrix_trace", "label": "Matrix Trace tr(A)", "default_display": "10.0000"},
            {"id": "inverse_row1", "label": "Inverse Row 1 [d/det, -b/det]", "default_display": "[0.6000, -0.7000]", "highlight": True},
            {"id": "inverse_row2", "label": "Inverse Row 2 [-c/det, a/det]", "default_display": "[-0.2000, 0.4000]"}
        ],
        "proof_steps": [
            {"step_title": "Geometric Area Scaling Factor", "step_text": "The determinant of a 2×2 matrix represents the signed factor by which area scales under the linear transformation: det(A) = ad - bc."},
            {"step_title": "Cramer's Rule Adjugate Matrix Inversion", "step_text": "By the adjugate matrix formula: A⁻¹ = (1 / det A) · adj(A) = (1 / (ad - bc)) · [ [d, -b], [-c, a] ]."},
            {"step_title": "Singular Matrix Non-Invertibility", "step_text": "If det(A) = 0, the transformation collapses two-dimensional space onto a line or point; hence the matrix is singular and no inverse exists."}
        ],
        "faqs": [
            {"q": "What does a zero determinant mean physically?", "a": "A zero determinant means the linear transformation squashes space into a lower dimension (e.g., flattening an area into a line), meaning information is permanently lost and the operation cannot be reversed."},
            {"q": "What are eigenvalues in linear algebra?", "a": "Eigenvalues λ are scalar multipliers where multiplying the matrix by eigenvector v merely stretches or compresses v without changing its spatial direction: A · v = λ · v."}
        ],
        "js_logic": """
          const a = getNum('elem_a');
          const b = getNum('elem_b');
          const c = getNum('elem_c');
          const d = getNum('elem_d');

          const det = (a * d) - (b * c);
          const tr = a + d;

          setDisp('matrix_det', det.toFixed(4) + (det !== 0 ? ' (Invertible)' : ' (Singular)'));
          setDisp('matrix_trace', tr.toFixed(4));

          if (Math.abs(det) > 1e-9) {
            const i11 = d / det;
            const i12 = -b / det;
            const i21 = -c / det;
            const i22 = a / det;
            setDisp('inverse_row1', '[' + i11.toFixed(4) + ', ' + i12.toFixed(4) + ']');
            setDisp('inverse_row2', '[' + i21.toFixed(4) + ', ' + i22.toFixed(4) + ']');
          } else {
            setDisp('inverse_row1', 'Undefined');
            setDisp('inverse_row2', 'Matrix is Singular (det = 0)');
          }
        """
    },
    {
        "slug": "pendulum-period",
        "category": "physics",
        "name": "Simple Pendulum Period & Harmonic Frequency Calculator",
        "description": "Calculate pendulum period (T), natural frequency (Hz), angular frequency (rad/s), and local gravitational acceleration (g).",
        "hero_badge": "Harmonic Oscillations • Pendulum Dynamics Matrix",
        "formula_display": "Period T = 2π · √(L / g) | Frequency f = 1 / T",
        "fields": [
            {"id": "pendulum_length", "label": "Pendulum Length (L)", "default": 1.0, "suffix": "meters", "min": 0.05, "max": 100, "step": 0.05, "hint": "Distance from pivot to center of mass"},
            {"id": "gravity_g", "label": "Gravitational Acceleration (g)", "default": 9.80665, "suffix": "m/s²", "min": 1, "max": 30, "step": 0.1, "hint": "9.80665 on Earth, 1.62 on Moon, 3.72 on Mars"}
        ],
        "metrics": [
            {"id": "period_seconds", "label": "Oscillation Period (T)", "default_display": "2.0061 seconds", "highlight": True},
            {"id": "frequency_hz", "label": "Natural Frequency (f)", "default_display": "0.4985 Hz (cycles/sec)", "highlight": True},
            {"id": "angular_frequency", "label": "Angular Frequency (ω = √(g/L))", "default_display": "3.1316 rad/s"},
            {"id": "seconds_pendulum_length", "label": "Length for Exact 2-Sec Period", "default_display": "0.9936 meters (~39.1 inches)"}
        ],
        "proof_steps": [
            {"step_title": "Torque Restoring Differential Equation", "step_text": "Net restoring torque τ = -m · g · L · sin(θ). For small angles (θ < 15°), sin(θ) ≈ θ (first-order Taylor series approximation), yielding linear differential equation: d²θ/dt² + (g/L)θ = 0."},
            {"step_title": "Simple Harmonic Motion Solution", "step_text": "Angular frequency ω = √(g / L). Period T = 2π / ω = 2π · √(L / g)."},
            {"step_title": "Mass Invariance of Gravitational Pendulums", "step_text": "Galileo Galilei discovered in 1581 that period T is completely independent of the pendulum bob's mass, confirming the equivalence principle between inertial and gravitational mass."}
        ],
        "faqs": [
            {"q": "What is a 'seconds pendulum'?", "a": "A seconds pendulum is a pendulum whose period is precisely 2 seconds (1 second for each swing from left to right). On Earth's surface, a seconds pendulum has a length of almost exactly 0.994 meters (~39.1 inches)."},
            {"q": "How does a Foucault pendulum prove Earth rotates?", "a": "Because a pendulum maintains its plane of oscillation in an inertial reference frame, the plane appears to rotate relative to Earth's surface at an angular speed of 360° · sin(latitude) per day, providing direct empirical proof of planetary rotation."}
        ],
        "js_logic": """
          const L = getNum('pendulum_length');
          const g = getNum('gravity_g') || 9.80665;

          const omega = Math.sqrt(g / (L || 1));
          const T = (2 * Math.PI) / omega;
          const f = 1 / T;
          const secL = g / Math.pow(Math.PI, 2);

          setDisp('period_seconds', T.toFixed(4) + ' seconds');
          setDisp('frequency_hz', f.toFixed(4) + ' Hz');
          setDisp('angular_frequency', omega.toFixed(4) + ' rad/s');
          setDisp('seconds_pendulum_length', secL.toFixed(4) + ' meters (~' + (secL * 39.3701).toFixed(1) + ' in)');
        """
    }
]
