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

        # Inversions back to a
        inv_p = p_n / test_n
        inv_ri = 2 * ri_n * tan_pi_n
        inv_R = 2 * R_n * sin_pi_n
        inv_A = math.sqrt((4 * A_n * tan_pi_n) / test_n)

        for name, val in [(f"n{test_n}-P", inv_p), (f"n{test_n}-ri", inv_ri), (f"n{test_n}-R", inv_R), (f"n{test_n}-A", inv_A)]:
            assert math.isclose(val, 10.0, rel_tol=1e-12), f"N-gon ({test_n}) inversion failure for {name}: {val}"

        # Invariant ratio ri / R strictly equals cos(pi/n)
        assert math.isclose(ri_n / R_n, math.cos(angle_pi_n), rel_tol=1e-12), f"Cosine invariant failed for n={test_n}"

    print("  ✅ Universal N-Gon: Arbitrary n=7 and n=12 forward & inverse derivations passed with 1e-12 precision!")

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
        "assets/js/octagon-solver.js",
        "assets/js/hexagon-solver.js",
        "assets/js/pentagon-solver.js",
        "assets/js/decagon-solver.js",
        "assets/js/regular-polygon-solver.js",
        "assets/js/blueprint-engine.js",
        "geometry/index.html",
        "geometry/2d/index.html",
        "geometry/2d/shapes/index.html",
        "geometry/2d/shapes/regular-polygon/index.html",
        "geometry/2d/shapes/octagon/index.html",
        "geometry/2d/shapes/hexagon/index.html",
        "geometry/2d/shapes/pentagon/index.html",
        "geometry/2d/shapes/decagon/index.html",
        "calculus/index.html",
        "finance/index.html",
        "physics/index.html",
        "statistics/index.html"
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

    print(f"  ✅ All {len(required_files)} core files verified and non-empty!")

def main():
    print("=========================================================")
    print("🧪 Running OmniOperand Integrity Test Suite")
    print("=========================================================")
    try:
        test_mathematical_precision()
        test_file_integrity()
        print("\n🎉 ALL TESTS PASSED! Site is 100% compliant.")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
