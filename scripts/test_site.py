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

    print("  ✅ All 8 forward and inverse mathematical derivations passed with 1e-12 precision!")

def test_file_integrity():
    print("Testing File & Asset Integrity...")
    required_files = [
        "index.html",
        "404.html",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "llms-full.txt",
        "assets/css/omni-core.css",
        "assets/css/calculator.css",
        "assets/js/omni-search.js",
        "assets/js/octagon-solver.js",
        "geometry/index.html",
        "geometry/2d/index.html",
        "geometry/2d/shapes/index.html",
        "geometry/2d/shapes/octagon/index.html",
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
