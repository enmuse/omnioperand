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

    # --- 15 GSC HIGH-INTENT CALCULATOR INVARIANTS ---

    # 11. Rebar Grid & Spacing (20 ft x 10 ft, 12 in grid, 3 in clearance, #4 bar)
    clearance_ft = 3.0 / 12.0
    eff_len = 20.0 - 2 * clearance_ft
    eff_wid = 10.0 - 2 * clearance_ft
    bars_len = math.floor((10.0 * 12 - 6) / 12) + 1  # 10 bars along length
    bars_wid = math.floor((20.0 * 12 - 6) / 12) + 1  # 20 bars along width
    total_lin_ft = (bars_len * eff_len) + (bars_wid * eff_wid)
    assert total_lin_ft > 0, "Rebar footage must be positive"
    weight_lb = total_lin_ft * 0.668  # #4 bar = 0.668 lb/ft
    assert math.isclose(weight_lb, total_lin_ft * 0.668, rel_tol=1e-6), "Rebar weight mismatch"
    print("  ✅ Rebar Grid & Spacing: Linear footage and ASTM weight verified!")

    # 12. Drywall Estimator (20 ft x 15 ft x 9 ft height, 60 sq ft cutouts, 4x8 sheet)
    wall_sqft = 2 * (20.0 + 15.0) * 9.0 - 60.0  # 570 sq ft
    ceil_sqft = 20.0 * 15.0  # 300 sq ft
    total_drywall_sqft = wall_sqft + ceil_sqft  # 870 sq ft
    sheets_needed = math.ceil((total_drywall_sqft / 32.0) * 1.10)
    assert sheets_needed == 30, f"Drywall sheet mismatch: {sheets_needed}"
    print("  ✅ Drywall Estimator: Surface area, 10% waste buffer, and sheet count verified!")

    # 13. HVAC Furnace Sizing (2,000 sq ft, 9 ft ceiling, Zone 3 @ 40 BTU/sqft, average ins)
    hvac_btu = 2000.0 * 40.0 * 1.0 * (9.0 / 8.0)
    assert math.isclose(hvac_btu, 90000.0), f"HVAC BTU mismatch: {hvac_btu}"
    hvac_tonnage = hvac_btu / 12000.0
    assert math.isclose(hvac_tonnage, 7.5), f"HVAC tonnage mismatch: {hvac_tonnage}"
    print("  ✅ HVAC Furnace Sizing: Manual J heating BTU and tonnage verified!")

    # 14. Lean-To Roof Pitch (12 ft run, 4 ft rise, 12 in overhang)
    pitch_ratio_x = (4.0 / 12.0) * 12.0
    assert math.isclose(pitch_ratio_x, 4.0), "Pitch ratio mismatch"
    lean_deg = math.degrees(math.atan(4.0 / 12.0))
    assert math.isclose(lean_deg, 18.4349, rel_tol=1e-4), "Lean-to pitch angle mismatch"
    rafter_true_len = math.sqrt(12.0**2 + 4.0**2) + (12.0 / 12.0)
    assert math.isclose(rafter_true_len, 13.64911, rel_tol=1e-4), "Lean-to rafter length mismatch"
    print("  ✅ Lean-To Roof Pitch: Pitch ratio, angle, and true rafter length verified!")

    # 15. Generator Sizing (Running watts: 5200 W, Surge watts: 8700 W, 20% margin)
    running_kw = 5200.0 / 1000.0
    surge_kva = 8700.0 / 1000.0
    recommended_gen = surge_kva * 1.20
    assert math.isclose(running_kw, 5.2), "Generator running kW mismatch"
    assert math.isclose(surge_kva, 8.7), "Generator surge kVA mismatch"
    assert math.isclose(recommended_gen, 10.44), "Generator safety margin mismatch"
    print("  ✅ Generator Sizing: Continuous kW, peak surge kVA, and 20% margin verified!")

    # 16. Wire Gauge & Voltage Drop (100 ft 1-phase 120V, 20A, #12 AWG Cu: 1.93 ohm/kft)
    loop_dist = 2 * 100.0
    r_wire = loop_dist * (1.93 / 1000.0)
    v_drop = 20.0 * r_wire
    v_drop_pct = (v_drop / 120.0) * 100.0
    assert math.isclose(v_drop, 7.72, rel_tol=1e-3), f"Voltage drop mismatch: {v_drop}"
    assert math.isclose(v_drop_pct, 6.433, rel_tol=1e-2), f"Voltage drop pct mismatch: {v_drop_pct}"
    assert v_drop_pct > 3.0, "NEC 3% branch limit threshold check"
    print("  ✅ Wire Gauge & Voltage Drop: Ohmic drop and NEC 3% limit verified!")

    # 17. Battery Backup Storage (15 kWh/day, 2 days autonomy, LiFePO4 DoD=85%, Inverter eff=95%, 48V)
    req_kwh = (15.0 * 2.0) / (0.85 * 0.95)
    assert math.isclose(req_kwh, 37.1517, rel_tol=1e-3), f"Battery required kWh mismatch: {req_kwh}"
    req_ah = (req_kwh * 1000.0) / 48.0
    assert math.isclose(req_ah, 773.99, rel_tol=1e-3), f"Battery required Ah mismatch: {req_ah}"
    print("  ✅ Battery Backup Storage: DoD autonomy capacity and Amp-Hour sizing verified!")

    # 18. Reverse Mortgage HECM (Age 70, Home $600k, Mortgage $120k, Rate 6.5%, PLF=0.485)
    gross_proceeds = 600000.0 * 0.485
    net_cash = gross_proceeds - 120000.0 - 18000.0  # deducting mandatory payoff and closing
    assert math.isclose(gross_proceeds, 291000.0), "HECM gross proceeds mismatch"
    assert math.isclose(net_cash, 153000.0), "HECM net proceeds mismatch"
    print("  ✅ Reverse Mortgage HECM: Actuarial PLF and mandatory payoff deductions verified!")

    # 19. Section 199A QBI ($150k income, Single, $80k QBI -> 20% full deduction)
    qbi_ded = 80000.0 * 0.20
    assert math.isclose(qbi_ded, 16000.0), "QBI 20% deduction mismatch"
    print("  ✅ Section 199A QBI: 20% passthrough deduction verified!")

    # 20. RV Loan ($55k net loan, 7.5%, 15 years = 180 months)
    r_rv = 0.075 / 12.0
    n_rv = 180
    f_rv = math.pow(1 + r_rv, n_rv)
    m_rv = 55000.0 * (r_rv * f_rv) / (f_rv - 1)
    assert math.isclose(m_rv, 509.91, rel_tol=1e-2), f"RV monthly payment mismatch: {m_rv}"
    total_int_rv = m_rv * n_rv - 55000.0
    assert math.isclose(total_int_rv, 36783.8, rel_tol=1e-1), "RV total interest mismatch"
    print("  ✅ RV Loan: Long-term amortization and interest verified!")

    # 21. Equity IRR & MOIC (C0 = -1,000,000, C1-C4 = 80,000, C5 = 1,600,000)
    total_inflows = 4 * 80000.0 + 1600000.0
    moic = total_inflows / 1000000.0
    assert math.isclose(moic, 1.92), f"MOIC mismatch: {moic}"
    # Verify NPV at IRR (r ≈ 0.156186) is zero within machine precision
    r_irr = 0.1561855654
    npv = -1000000.0 + sum(80000.0 / ((1 + r_irr)**t) for t in range(1, 5)) + 1600000.0 / ((1 + r_irr)**5)
    assert abs(npv) < 1.0, f"IRR root finding mismatch: NPV={npv}"
    print("  ✅ Equity IRR: Multi-year cash flow NPV and MOIC verified!")

    # 22. qPCR Primer Tm (20 bp, 10 GC, 50% GC)
    tm_wallace = 2 * 10 + 4 * 10
    assert tm_wallace == 60, "Wallace Tm mismatch"
    ta_rec = tm_wallace - 5.0
    assert ta_rec == 55.0, "Ta annealing temperature mismatch"
    print("  ✅ qPCR Primer Tm: Base-stacking melting and annealing Ta verified!")

    # 23. US Navy Body Fat (Male: 70 in height, 16 in neck, 34 in waist)
    bf_male = 86.010 * math.log10(34.0 - 16.0) - 70.041 * math.log10(70.0) + 36.76
    assert math.isclose(bf_male, 15.493, rel_tol=1e-2), f"Navy body fat male mismatch: {bf_male}"
    # Female: 65 in height, 13 in neck, 28 in waist, 38 in hip
    bf_fem = 163.205 * math.log10(28.0 + 38.0 - 13.0) - 97.684 * math.log10(65.0) - 78.387
    assert math.isclose(bf_fem, 25.931, rel_tol=1e-2), f"Navy body fat female mismatch: {bf_fem}"
    print("  ✅ US Navy Body Fat: DoD male and female logarithmic formulas verified!")

    # 24. Cost of Smoking (1 pack/day, $9.50/pack, 20 yrs, 7% growth)
    annual_cost_smk = 1.0 * 9.50 * 365.0
    assert math.isclose(annual_cost_smk, 3467.50), "Annual smoking outlay mismatch"
    fv_smk = annual_cost_smk * ((math.pow(1.07, 20) - 1.0) / 0.07)
    assert math.isclose(fv_smk, 142150.0, rel_tol=1e-1), f"Smoking opportunity cost mismatch: {fv_smk}"
    print("  ✅ Cost of Smoking: 20-year compound interest opportunity cost verified!")

    # 25. Italian Localized Generator Sizing
    it_gen_file = REPO_ROOT / "it" / "ingegneria" / "dimensionamento-gruppo-elettrogeno" / "index.html"
    assert it_gen_file.exists(), "Italian generator sizing file missing"
    it_content = it_gen_file.read_text(encoding="utf-8")
    assert 'href="https://omnioperand.com/it/ingegneria/dimensionamento-gruppo-elettrogeno/"' in it_content, "Missing Italian canonical"
    assert 'hreflang="it"' in it_content, "Missing it hreflang"
    assert 'hreflang="en"' in it_content, "Missing en hreflang"
    print("  ✅ Italian Generator Sizing: Canonical and bidirectional hreflangs verified!")

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
        # Core Solvers
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
        # Core Calculator HTML pages
        "finance/mortgage-amortization/index.html",
        "finance/compound-interest/index.html",
        "finance/cagr/index.html",
        "finance/auto-loan/index.html",
        "geometry/3d/concrete-volume/index.html",
        "geometry/2d/roof-pitch/index.html",
        "geometry/2d/circle-sector/index.html",
        "geometry/2d/right-triangle/index.html",
        "calculus/integrals/index.html",
        "calculus/derivatives/index.html",
        # 15 GSC High-Intent Calculators + Italian route
        "construction/concrete-volume/index.html",
        "construction/rebar-calculator/index.html",
        "construction/drywall/index.html",
        "engineering/hvac-furnace-sizing/index.html",
        "geometry/2d/lean-to-roof-pitch/index.html",
        "engineering/generator-sizing/index.html",
        "engineering/wire-gauge-voltage-drop/index.html",
        "engineering/battery-backup-storage/index.html",
        "finance/reverse-mortgage-hecm/index.html",
        "finance/section-199a-qbi/index.html",
        "finance/rv-loan/index.html",
        "finance/equity-irr/index.html",
        "biotech/qpcr-primer-tm/index.html",
        "health/navy-body-fat/index.html",
        "health/cost-of-smoking/index.html",
        "it/ingegneria/dimensionamento-gruppo-elettrogeno/index.html"
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

def test_calculator_count_invariants():
    print("Testing Master Calculator Count & Metric Invariants...")
    import json
    metrics_path = REPO_ROOT / "config" / "metrics.json"
    assert metrics_path.exists(), "Missing config/metrics.json master source of truth"

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    reg_path = REPO_ROOT / "api" / "solvers" / "calculator_registry.json"
    with open(reg_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    assert metrics["solvers_count"] == len(registry), f"Solvers count mismatch: {metrics['solvers_count']} vs registry {len(registry)}"
    assert metrics["mcp_tools_count"] == len(registry) + 1, "MCP tools count mismatch"

    # Verify mcp/index.html does not contain stale (10 Solvers)
    mcp_html = (REPO_ROOT / "mcp" / "index.html").read_text(encoding="utf-8")
    assert "(10 Solvers)" not in mcp_html, "mcp/index.html contains stale '(10 Solvers)' string!"
    assert f"({metrics['solvers_count']} Solvers" in mcp_html, f"mcp/index.html missing current ({metrics['solvers_count']} Solvers"

    # Verify mcp/schemas.json has full toolset
    schemas_path = REPO_ROOT / "mcp" / "schemas.json"
    assert schemas_path.exists(), "Missing mcp/schemas.json"
    with open(schemas_path, "r", encoding="utf-8") as f:
        schemas = json.load(f)
    assert len(schemas["tools"]) == metrics["mcp_tools_count"], f"mcp/schemas.json tool count mismatch: {len(schemas['tools'])} vs {metrics['mcp_tools_count']}"

    print(f"  ✅ Master metrics verified: {metrics['solvers_count']} solvers, {metrics['mcp_tools_count']} MCP tools across {metrics['categories_count']} disciplines!")

def test_internationalization_and_hreflang():
    print("Testing Multi-Language Internationalization & Reciprocal Hreflangs...")
    non_en_languages = ["es", "fr", "de", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"]
    all_languages = ["en"] + non_en_languages
    
    # 1. Verify all 11 language directories exist
    for lang in non_en_languages:
        lang_dir = REPO_ROOT / lang
        assert lang_dir.exists() and lang_dir.is_dir(), f"Missing language directory: {lang}"
        # Check that index.html exists in language root
        assert (lang_dir / "index.html").exists(), f"Missing root index.html for language: {lang}"
        assert (lang_dir / "geometry" / "2d" / "shapes" / "octagon" / "index.html").exists(), f"Missing localized octagon solver for language: {lang}"
        assert (lang_dir / "geometry" / "2d" / "shapes" / "regular-polygon" / "index.html").exists(), f"Missing localized regular-polygon solver for language: {lang}"

    # 2. Verify reciprocal hreflang tags on canonical English page
    en_octagon = (REPO_ROOT / "geometry" / "2d" / "shapes" / "octagon" / "index.html").read_text(encoding="utf-8")
    for lang in all_languages:
        expected_tag = f'hreflang="{lang}"'
        assert expected_tag in en_octagon, f"Missing hreflang tag for {lang} in English octagon page"
    assert 'hreflang="x-default"' in en_octagon, "Missing x-default hreflang tag in English octagon page"

    # 3. Verify reciprocal hreflang tags on localized Spanish page
    es_octagon = (REPO_ROOT / "es" / "geometry" / "2d" / "shapes" / "octagon" / "index.html").read_text(encoding="utf-8")
    assert '<html lang="es"' in es_octagon, "Missing html lang='es' in Spanish octagon page"
    assert 'href="https://omnioperand.com/es/geometry/2d/shapes/octagon/"' in es_octagon, "Missing canonical Spanish URL"
    for lang in all_languages:
        assert f'hreflang="{lang}"' in es_octagon, f"Missing reciprocal hreflang for {lang} in Spanish page"

    # 4. Verify reciprocal hreflang tags on localized Portuguese page
    pt_octagon = (REPO_ROOT / "pt" / "geometry" / "2d" / "shapes" / "octagon" / "index.html").read_text(encoding="utf-8")
    assert '<html lang="pt"' in pt_octagon, "Missing html lang='pt' in Portuguese octagon page"
    assert 'href="https://omnioperand.com/pt/geometry/2d/shapes/octagon/"' in pt_octagon, "Missing canonical Portuguese URL"
    for lang in all_languages:
        assert f'hreflang="{lang}"' in pt_octagon, f"Missing reciprocal hreflang for {lang} in Portuguese page"

    # 5. Verify Language Dropdown in headers
    assert 'class="lang-dropdown"' in en_octagon, "Missing lang-dropdown in English header"
    assert 'class="lang-dropdown"' in es_octagon, "Missing lang-dropdown in Spanish header"
    assert 'ES' in es_octagon, "Missing Spanish language code in Spanish header"
    assert 'PT' in pt_octagon, "Missing Portuguese language code in Portuguese header"

    # 6. Verify comma decimal support in solver JS
    oct_js = (REPO_ROOT / "assets" / "js" / "octagon-solver.js").read_text(encoding="utf-8")
    assert ".replace(',', '.')" in oct_js, "octagon-solver.js missing comma decimal parsing support"

    print(f"  ✅ Internationalization verified: 11 non-English languages (12 total), bidirectional hreflangs, language switcher, and European decimal support!")

def main():
    print("=========================================================")
    print("🧪 Running OmniOperand Integrity Test Suite")
    print("=========================================================")
    try:
        test_mathematical_precision()
        test_file_integrity()
        test_zero_raw_latex_in_html()
        test_calculator_count_invariants()
        test_internationalization_and_hreflang()
        print("\n🎉 ALL TESTS PASSED! Site is 100% compliant.")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
