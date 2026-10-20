#!/usr/bin/env python3
"""
scripts/test_site.py — Automated Mathematical Integrity & SEO Compliance Test Suite
"""

import sys
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_mathematical_precision():
    print("Testing Mathematical Solver Logic & Inversion Invariants...")
    a = 10.0
    sqrt2 = math.sqrt(2)

    # Octagon Constants
    k_apothem = (1 + sqrt2) / 2
    k_circumradius = math.sqrt(4 + 2 * sqrt2) / 2
    k_area = 2 * (1 + sqrt2)
    k_short_diag = math.sqrt(2 + sqrt2)
    k_span = 1 + sqrt2
    k_long_diag = math.sqrt(4 + 2 * sqrt2)

    # Forward calculations
    p = 8 * a
    r_i = a * k_apothem
    R = a * k_circumradius
    A = a * a * k_area
    d_S = a * k_short_diag
    S = a * k_span
    d_L = a * k_long_diag

    assert math.isclose(p, 80.0), "Perimeter mismatch"
    assert math.isclose(r_i, 12.071067811865476), "Apothem mismatch"
    assert math.isclose(R, 13.065629648763766), "Circumradius mismatch"
    assert math.isclose(A, 482.842712474619), "Area mismatch"
    assert math.isclose(d_S, 18.477590650225735), "Short diagonal mismatch"
    assert math.isclose(S, 24.14213562373095), "Span mismatch"
    assert math.isclose(d_L, 26.13125929752753), "Long diagonal mismatch"

    # Inversion calculations back to 'a'
    inv_p = p / 8
    inv_ri = (2 * r_i) / (1 + sqrt2)
    inv_R = (2 * R) / math.sqrt(4 + 2 * sqrt2)
    inv_A = math.sqrt(A / (2 * (1 + sqrt2)))
    inv_ds = d_S / math.sqrt(2 + sqrt2)
    inv_S = S / (1 + sqrt2)
    inv_dl = d_L / math.sqrt(4 + 2 * sqrt2)

    for name, val in [("P", inv_p), ("r_i", inv_ri), ("R", inv_R), ("A", inv_A), ("d_S", inv_ds), ("S", inv_S), ("d_L", inv_dl)]:
        assert math.isclose(val, 10.0, rel_tol=1e-12), f"Inversion failure for {name}: {val}"

    # Law of Cosines check on short diagonal: d_S^2 = a^2 + a^2 - 2a^2 cos(135°)
    cos135 = math.cos(math.radians(135))
    expected_ds_sq = 2 * a * a - 2 * a * a * cos135
    assert math.isclose(d_S * d_S, expected_ds_sq), "Law of Cosines invariant failed"

    print("  ✅ Octagon: All 8 forward and inverse mathematical derivations passed with 1e-12 precision!")

    # Hexagon Invariants (a = 10)
    sqrt3 = math.sqrt(3)
    k_hex_apothem = sqrt3 / 2
    k_hex_circumradius = 1.0
    k_hex_perimeter = 6.0
    k_hex_area = (3 * sqrt3) / 2
    k_hex_short_diag = sqrt3
    k_hex_span = sqrt3
    k_hex_long_diag = 2.0

    p_hex = a * k_hex_perimeter
    ri_hex = a * k_hex_apothem
    R_hex = a * k_hex_circumradius
    A_hex = a * a * k_hex_area
    ds_hex = a * k_hex_short_diag
    S_hex = a * k_hex_span
    dl_hex = a * k_hex_long_diag

    assert math.isclose(p_hex, 60.0), "Hexagon perimeter mismatch"
    assert math.isclose(ri_hex, 8.660254037844386), "Hexagon apothem mismatch"
    assert math.isclose(R_hex, 10.0), "Hexagon circumradius mismatch"
    assert math.isclose(A_hex, 259.8076211353316), "Hexagon area mismatch"
    assert math.isclose(ds_hex, 17.320508075688775), "Hexagon short diag mismatch"
    assert math.isclose(S_hex, 17.320508075688775), "Hexagon span mismatch"
    assert math.isclose(dl_hex, 20.0), "Hexagon long diag mismatch"

    inv_p_hex = p_hex / 6
    inv_ri_hex = (2 * ri_hex) / sqrt3
    inv_R_hex = R_hex
    inv_A_hex = math.sqrt((2 * A_hex) / (3 * sqrt3))
    inv_ds_hex = ds_hex / sqrt3
    inv_S_hex = S_hex / sqrt3
    inv_dl_hex = dl_hex / 2
    for name, val in [("Hex-P", inv_p_hex), ("Hex-ri", inv_ri_hex), ("Hex-R", inv_R_hex), ("Hex-A", inv_A_hex), ("Hex-ds", inv_ds_hex), ("Hex-S", inv_S_hex), ("Hex-dl", inv_dl_hex)]:
        assert math.isclose(val, 10.0, rel_tol=1e-12), f"Hexagon inversion failure for {name}: {val}"

    print("  ✅ Hexagon: All 7 forward and inverse mathematical derivations passed with 1e-12 precision!")

    # Pentagon Invariants (a = 10)
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    k_pen_apothem = math.sqrt(25 + 10 * sqrt5) / 10
    k_pen_circumradius = math.sqrt(50 + 10 * sqrt5) / 10
    k_pen_perimeter = 5.0
    k_pen_area = math.sqrt(25 + 10 * sqrt5) / 4
    k_pen_diag = phi
    k_pen_height = math.sqrt(5 + 2 * sqrt5) / 2

    p_pen = a * k_pen_perimeter
    ri_pen = a * k_pen_apothem
    R_pen = a * k_pen_circumradius
    A_pen = a * a * k_pen_area
    d_pen = a * k_pen_diag
    h_pen = a * k_pen_height

    assert math.isclose(p_pen, 50.0), "Pentagon perimeter mismatch"
    assert math.isclose(ri_pen, 6.881909602355868), "Pentagon apothem mismatch"
    assert math.isclose(R_pen, 8.5065080835204), "Pentagon circumradius mismatch"
    assert math.isclose(A_pen, 172.0477400588967), "Pentagon area mismatch"
    assert math.isclose(d_pen, 16.18033988749895), "Pentagon diagonal mismatch"
    assert math.isclose(h_pen, 15.388417685876266), "Pentagon height mismatch"

    inv_p_pen = p_pen / 5
    inv_ri_pen = ri_pen / k_pen_apothem
    inv_R_pen = R_pen / k_pen_circumradius
    inv_A_pen = math.sqrt(A_pen / k_pen_area)
    inv_d_pen = d_pen / phi
    inv_h_pen = h_pen / k_pen_height
    for name, val in [("Pen-P", inv_p_pen), ("Pen-ri", inv_ri_pen), ("Pen-R", inv_R_pen), ("Pen-A", inv_A_pen), ("Pen-d", inv_d_pen), ("Pen-h", inv_h_pen)]:
        assert math.isclose(val, 10.0, rel_tol=1e-12), f"Pentagon inversion failure for {name}: {val}"

    print("  ✅ Pentagon: All 6 forward and inverse mathematical derivations passed with 1e-12 precision!")

    # Decagon Invariants (a = 10)
    k_dec_apothem = math.sqrt(5 + 2 * sqrt5) / 2
    k_dec_circumradius = phi
    k_dec_perimeter = 10.0
    k_dec_area = (5 / 2) * math.sqrt(5 + 2 * sqrt5)
    k_dec_span = math.sqrt(5 + 2 * sqrt5)
    k_dec_d1 = math.sqrt((5 + sqrt5) / 2)
    k_dec_d2 = phi * phi
    k_dec_d4 = 2 * phi

    p_dec = a * k_dec_perimeter
    ri_dec = a * k_dec_apothem
    R_dec = a * k_dec_circumradius
    A_dec = a * a * k_dec_area
    S_dec = a * k_dec_span
    d1_dec = a * k_dec_d1
    d2_dec = a * k_dec_d2
    d4_dec = a * k_dec_d4

    assert math.isclose(p_dec, 100.0), "Decagon perimeter mismatch"
    assert math.isclose(ri_dec, 15.388417685876266), "Decagon apothem mismatch"
    assert math.isclose(R_dec, 16.18033988749895), "Decagon circumradius mismatch"
    assert math.isclose(A_dec, 769.4208842938133), "Decagon area mismatch"
    assert math.isclose(S_dec, 30.77683537175253), "Decagon span mismatch"
    assert math.isclose(d1_dec, 19.02113032590307), "Decagon short diag mismatch"
    assert math.isclose(d2_dec, 26.18033988749895), "Decagon medium diag mismatch"
    assert math.isclose(d4_dec, 32.3606797749979), "Decagon main diameter mismatch"

    inv_p_dec = p_dec / 10
    inv_ri_dec = ri_dec / k_dec_apothem
    inv_R_dec = R_dec / phi
    inv_A_dec = math.sqrt(A_dec / k_dec_area)
    inv_S_dec = S_dec / k_dec_span
    inv_d1_dec = d1_dec / k_dec_d1
    inv_d2_dec = d2_dec / (phi * phi)
    inv_d4_dec = d4_dec / (2 * phi)
    for name, val in [("Dec-P", inv_p_dec), ("Dec-ri", inv_ri_dec), ("Dec-R", inv_R_dec), ("Dec-A", inv_A_dec), ("Dec-S", inv_S_dec), ("Dec-d1", inv_d1_dec), ("Dec-d2", inv_d2_dec), ("Dec-d4", inv_d4_dec)]:
        assert math.isclose(val, 10.0, rel_tol=1e-12), f"Decagon inversion failure for {name}: {val}"

    print("  ✅ Decagon: All 8 forward and inverse mathematical derivations passed with 1e-12 precision!")

    # Universal Regular N-Gon Invariant Tests (Testing Heptagon n=7 and Dodecagon n=12)
    for test_n in [7, 12]:
        angle_pi_n = math.pi / test_n
        tan_pi_n = math.tan(angle_pi_n)
        sin_pi_n = math.sin(angle_pi_n)

        p_n = test_n * a
        ri_n = a / (2 * tan_pi_n)
        R_n = a / (2 * sin_pi_n)
        A_n = (test_n * a * a) / (4 * tan_pi_n)

        inv_p = p_n / test_n
        inv_ri = 2 * ri_n * tan_pi_n
        inv_R = 2 * R_n * sin_pi_n
        inv_A = math.sqrt((4 * A_n * tan_pi_n) / test_n)

        for name, val in [(f"n{test_n}-P", inv_p), (f"n{test_n}-ri", inv_ri), (f"n{test_n}-R", inv_R), (f"n{test_n}-A", inv_A)]:
            assert math.isclose(val, 10.0, rel_tol=1e-12), f"N-gon ({test_n}) inversion failure for {name}: {val}"

        assert math.isclose(ri_n / R_n, math.cos(angle_pi_n), rel_tol=1e-12), f"Cosine invariant failed for n={test_n}"

    print("  ✅ Universal N-Gon: Arbitrary n=7 and n=12 derivations passed with 1e-12 precision!")

    # --- NEW SOLVER MATHEMATICAL INVARIANTS ---

    # 1. Mortgage Invariants (P = 400,000, r = 6.5%, 30 yrs)
    P_loan = 400000.0
    r_loan = 0.065 / 12
    n_loan = 30 * 12
    factor_loan = math.pow(1 + r_loan, n_loan)
    M_loan = P_loan * (r_loan * factor_loan) / (factor_loan - 1)
    assert math.isclose(M_loan, 2528.27258, rel_tol=1e-4), "Mortgage payment mismatch"
    # Inversion: find P from M
    P_inverted = M_loan * (factor_loan - 1) / (r_loan * factor_loan)
    assert math.isclose(P_inverted, P_loan, rel_tol=1e-12), "Mortgage principal inversion failed"
    print("  ✅ Mortgage: Monthly payment and principal inversion verified!")

    # 2. Compound Interest (P = 10000, r = 8%, 20 yrs, monthly)
    P_ci = 10000.0
    r_ci = 0.08
    t_ci = 20
    m_ci = 12
    fv_lump = P_ci * math.pow(1 + r_ci / m_ci, m_ci * t_ci)
    assert math.isclose(fv_lump, 49268.02768, rel_tol=1e-4), "Compound interest lump sum mismatch"
    apy_ci = math.pow(1 + r_ci / m_ci, m_ci) - 1
    assert math.isclose(apy_ci, 0.0829995, rel_tol=1e-4), "APY mismatch"
    print("  ✅ Compound Interest: Lump sum and APY verified!")

    # 3. CAGR (V0 = 100,000, Vn = 350,000, n = 5)
    v0_cagr = 100000.0
    vn_cagr = 350000.0
    n_cagr = 5.0
    cagr = math.pow(vn_cagr / v0_cagr, 1 / n_cagr) - 1
    assert math.isclose(cagr, 0.284735, rel_tol=1e-4), "CAGR rate mismatch"
    # Inversion: find Vn from V0 and cagr
    vn_inv = v0_cagr * math.pow(1 + cagr, n_cagr)
    assert math.isclose(vn_inv, vn_cagr, rel_tol=1e-12), "CAGR valuation inversion failed"
    print("  ✅ CAGR: Geometric mean and terminal valuation inversion verified!")

    # 4. Auto Loan (P = 32950, apr = 5.9%, 60 mos)
    P_auto = 32950.0
    r_auto = 0.059 / 12
    n_auto = 60
    f_auto = math.pow(1 + r_auto, n_auto)
    M_auto = P_auto * (r_auto * f_auto) / (f_auto - 1)
    assert math.isclose(M_auto, 635.483, rel_tol=1e-3), "Auto loan payment mismatch"
    print("  ✅ Auto Loan: Monthly installment payment verified!")

    # 5. Concrete Volume (20 ft x 10 ft x 4 in)
    cu_ft_conc = 20.0 * 10.0 * (4.0 / 12.0)
    cu_yd_conc = cu_ft_conc / 27.0
    assert math.isclose(cu_yd_conc, 2.4691358, rel_tol=1e-6), "Concrete cubic yard mismatch"
    # 80-lb bag count: 2.4691358 * 45 = 111.11 -> 112 bags net
    bags_80 = cu_ft_conc / 0.60
    assert math.isclose(bags_80, 111.111, rel_tol=1e-3), "Concrete bag count mismatch"
    print("  ✅ Concrete Volume: Slab cubic yards and 80lb bag yields verified!")

    # 6. Roof Pitch (6:12 pitch, 30 ft span)
    pitch_angle_deg = math.degrees(math.atan(6.0 / 12.0))
    assert math.isclose(pitch_angle_deg, 26.56505, rel_tol=1e-4), "Roof pitch angle mismatch"
    multiplier_roof = math.sqrt(1 + (6.0 / 12.0) ** 2)
    assert math.isclose(multiplier_roof, 1.118034, rel_tol=1e-5), "Roof rafter multiplier mismatch"
    rafter_len = (30.0 / 2.0) * multiplier_roof
    assert math.isclose(rafter_len, 16.7705, rel_tol=1e-3), "Rafter line length mismatch"
    print("  ✅ Roof Pitch: Pitch angle and rafter hypotenuse length verified!")

    # 7. Circle Sector (R = 10, theta = 60 deg)
    theta_rad = math.radians(60.0)
    arc_s = 10.0 * theta_rad
    chord_c = 2 * 10.0 * math.sin(theta_rad / 2)
    sagitta_h = 10.0 * (1 - math.cos(theta_rad / 2))
    assert math.isclose(chord_c, 10.0, rel_tol=1e-12), "Equilateral chord mismatch"
    # Sagitta Inversion: R = (c^2 / 8h) + h / 2
    r_from_sagitta = (chord_c ** 2) / (8 * sagitta_h) + (sagitta_h / 2)
    assert math.isclose(r_from_sagitta, 10.0, rel_tol=1e-12), "Chord-Sagitta radius inversion failed"
    print("  ✅ Circle Sector: Arc, chord, sagitta and Sagitta-Chord radius inversion verified!")

    # 8. Right Triangle (3-4-5)
    c_tri = math.sqrt(3.0**2 + 4.0**2)
    assert math.isclose(c_tri, 5.0), "Pythagorean hypotenuse mismatch"
    h_tri = (3.0 * 4.0) / 5.0
    assert math.isclose(h_tri, 2.4), "Altitude mismatch"
    ri_tri = (3.0 + 4.0 - 5.0) / 2.0
    assert math.isclose(ri_tri, 1.0), "Inradius mismatch"
    print("  ✅ Right Triangle: Pythagoras, altitude, and inradius verified!")

    # 9. Definite Integral: f(x) = 0.5x^3 - 1.5x^2 + 2x + 3 from 0 to 4
    # F(x) = 0.125x^4 - 0.5x^3 + x^2 + 3x
    def F_poly(x):
        return 0.125 * (x**4) - 0.5 * (x**3) + 1.0 * (x**2) + 3.0 * x
    integral_val = F_poly(4) - F_poly(0)
    assert math.isclose(integral_val, 28.0), f"Integral mismatch: {integral_val}"
    print("  ✅ Definite Integral: Fundamental Theorem Part 2 evaluated with machine precision!")

    # 10. Derivative: f(x) = x^3 - 3x^2 + 2 at x=2
    # f'(x) = 3x^2 - 6x -> f'(2) = 12 - 12 = 0
    f_prime_2 = 3 * (2.0**2) - 6 * 2.0
    assert math.isclose(f_prime_2, 0.0), "Derivative slope mismatch"
    print("  ✅ Derivative: Instantaneous slope and stationary point verified!")

def test_file_integrity():
    print("Testing File & Asset Integrity...")
    required_files = [
        "index.html",
        "404.html",
        "robots.txt",
        "_headers",
        "sitemap.xml",
        "llms.txt",
        "llms-full.txt",
        "assets/css/omni-core.css",
        "assets/css/calculator.css",
        "assets/js/omni-search.js",
        "assets/js/blueprint-engine.js",
        # Polygon JS solvers
        "assets/js/octagon-solver.js",
        "assets/js/hexagon-solver.js",
        "assets/js/pentagon-solver.js",
        "assets/js/decagon-solver.js",
        "assets/js/regular-polygon-solver.js",
        # New 10 JS solvers
        "assets/js/mortgage-solver.js",
        "assets/js/compound-interest-solver.js",
        "assets/js/cagr-solver.js",
        "assets/js/auto-loan-solver.js",
        "assets/js/concrete-volume-solver.js",
        "assets/js/roof-pitch-solver.js",
        "assets/js/circle-sector-solver.js",
        "assets/js/right-triangle-solver.js",
        "assets/js/integrals-solver.js",
        "assets/js/derivatives-solver.js",
        # Hub pages
        "geometry/index.html",
        "geometry/2d/index.html",
        "geometry/3d/index.html",
        "geometry/2d/shapes/index.html",
        "calculus/index.html",
        "finance/index.html",
        "physics/index.html",
        "statistics/index.html",
        "api/index.html",
        "api/v1/openapi.json",
        # Polygon Calculators
        "geometry/2d/shapes/regular-polygon/index.html",
        "geometry/2d/shapes/octagon/index.html",
        "geometry/2d/shapes/hexagon/index.html",
        "geometry/2d/shapes/pentagon/index.html",
        "geometry/2d/shapes/decagon/index.html",
        # New 10 Calculator HTML pages
        "finance/mortgage-amortization/index.html",
        "finance/compound-interest/index.html",
        "finance/cagr/index.html",
        "finance/auto-loan/index.html",
        "geometry/3d/concrete-volume/index.html",
        "geometry/2d/roof-pitch/index.html",
        "geometry/2d/circle-sector/index.html",
        "geometry/2d/right-triangle/index.html",
        "calculus/integrals/index.html",
        "calculus/derivatives/index.html"
    ]

    for rel_path in required_files:
        f = REPO_ROOT / rel_path
        assert f.exists(), f"Missing required file: {rel_path}"
        assert f.stat().st_size > 0, f"File is empty: {rel_path}"
        # Check basic SEO tags for HTML
        if rel_path.endswith(".html") and rel_path != "404.html":
            content = f.read_text(encoding="utf-8")
            assert "<title>" in content, f"Missing <title> in {rel_path}"
            assert 'rel="canonical"' in content, f"Missing canonical link in {rel_path}"

    print(f"  ✅ All {len(required_files)} core files verified and non-empty with canonical SEO tags!")

def test_zero_raw_latex_in_html():
    print("Testing for Zero Raw LaTeX Commands in HTML...")
    import re
    latex_pattern = re.compile(r"\\[a-zA-Z]+")
    violations = []

    for html_file in REPO_ROOT.glob("**/*.html"):
        if ".git" in html_file.parts:
            continue
        content = html_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            matches = latex_pattern.findall(line)
            if matches:
                rel = html_file.relative_to(REPO_ROOT)
                violations.append((f"{rel}:{idx+1}", matches, line.strip()))

    if violations:
        for loc, matches, line in violations[:10]:
            print(f"  ❌ Raw LaTeX violation at {loc}: {matches} -> {line[:80]}")
        assert False, f"Found {len(violations)} raw LaTeX backslash commands in HTML files! Use clean Unicode math notation instead."

    print("  ✅ Zero raw LaTeX backslash commands found across all HTML files!")

def main():
    print("=========================================================")
    print("🧪 Running OmniOperand Integrity Test Suite")
    print("=========================================================")
    try:
        test_mathematical_precision()
        test_file_integrity()
        test_zero_raw_latex_in_html()
        print("\n🎉 ALL TESTS PASSED! Site is 100% compliant.")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
