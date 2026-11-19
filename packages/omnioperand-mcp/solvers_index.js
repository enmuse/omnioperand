/**
 * api/solvers/index.js
 * OmniOperand Deterministic Multi-Domain Mathematical Solvers Engine
 * High-precision, zero-hallucination algebraic & radical calculations.
 */

const SQRT2 = Math.SQRT2;
const SQRT3 = Math.sqrt(3);

export function roundPrec(val, prec = 6) {
  if (typeof val !== 'number' || isNaN(val) || !isFinite(val)) return 0;
  const factor = Math.pow(10, prec);
  return Math.round((val + Number.EPSILON) * factor) / factor;
}

// ==========================================
// 1. REGULAR OCTAGON SOLVER
// ==========================================
export function solveOctagon(params = {}) {
  const driver = (params.driver || 'side').toLowerCase();
  let val = parseFloat(params.value ?? params.side ?? 10);
  if (isNaN(val) || val <= 0) val = 10;
  const prec = Math.min(14, Math.max(2, parseInt(params.precision ?? 6, 10)));
  const units = params.units || 'units';

  let a = val;
  switch (driver) {
    case 'side':
    case 'a':
      a = val;
      break;
    case 'area':
    case 'a_poly':
      a = Math.sqrt(val / (2 * (1 + SQRT2)));
      break;
    case 'perimeter':
    case 'p':
      a = val / 8;
      break;
    case 'apothem':
    case 'inradius':
    case 'r_i':
      a = (2 * val) / (1 + SQRT2);
      break;
    case 'circumradius':
    case 'r':
      a = (2 * val) / Math.sqrt(4 + 2 * SQRT2);
      break;
    case 'span':
    case 's':
      a = val / (1 + SQRT2);
      break;
    case 'short_diagonal':
    case 'd_s':
      a = val / Math.sqrt(2 + SQRT2);
      break;
    case 'long_diagonal':
    case 'd_l':
      a = val / Math.sqrt(4 + 2 * SQRT2);
      break;
  }

  const p = 8 * a;
  const r_i = (a * (1 + SQRT2)) / 2;
  const R = (a * Math.sqrt(4 + 2 * SQRT2)) / 2;
  const area = 2 * (1 + SQRT2) * a * a;
  const S = a * (1 + SQRT2);
  const d_S = a * Math.sqrt(2 + SQRT2);
  const d_L = a * Math.sqrt(4 + 2 * SQRT2);
  const corner_cut = a / SQRT2;

  return {
    calculator: "octagon",
    inputs: { driver, value: val, precision: prec, units },
    result: {
      side_length: roundPrec(a, prec),
      area: roundPrec(area, prec),
      perimeter: roundPrec(p, prec),
      apothem_inradius: roundPrec(r_i, prec),
      circumradius: roundPrec(R, prec),
      span_flat_to_flat: roundPrec(S, prec),
      short_diagonal: roundPrec(d_S, prec),
      long_diagonal: roundPrec(d_L, prec),
      corner_cutoff_leg: roundPrec(corner_cut, prec),
      interior_angle_deg: 135.0,
      exterior_angle_deg: 45.0,
      central_angle_deg: 45.0,
      sum_interior_deg: 1080.0
    },
    exact_radicals: {
      area: "2(1 + √2)a²",
      apothem: "[a(1 + √2)] / 2",
      circumradius: "[a√(4 + 2√2)] / 2",
      span: "a(1 + √2)",
      short_diagonal: "a√(2 + √2)",
      long_diagonal: "a√(4 + 2√2)",
      corner_cutoff: "a / √2"
    },
    units: { length: units, area: `${units}²` }
  };
}

// ==========================================
// 2. UNIVERSAL REGULAR POLYGON SOLVER (n=3..1000)
// ==========================================
export function solveRegularPolygon(params = {}) {
  let n = parseInt(params.n ?? 8, 10);
  if (isNaN(n) || n < 3) n = 3;
  if (n > 1000) n = 1000;

  const driver = (params.driver || 'side').toLowerCase();
  let val = parseFloat(params.value ?? params.side ?? 10);
  if (isNaN(val) || val <= 0) val = 10;
  const prec = Math.min(14, Math.max(2, parseInt(params.precision ?? 6, 10)));
  const units = params.units || 'units';

  const halfCentral = Math.PI / n;
  const tanHalf = Math.tan(halfCentral);
  const sinHalf = Math.sin(halfCentral);

  let a = val;
  switch (driver) {
    case 'side':
    case 'a':
      a = val;
      break;
    case 'area':
      a = Math.sqrt((4 * val * tanHalf) / n);
      break;
    case 'perimeter':
      a = val / n;
      break;
    case 'apothem':
    case 'inradius':
      a = 2 * val * tanHalf;
      break;
    case 'circumradius':
      a = 2 * val * sinHalf;
      break;
    case 'span':
      a = (n % 2 === 0) ? 2 * val * tanHalf : val / ((1 + Math.cos(halfCentral)) / (2 * sinHalf));
      break;
  }

  const p = n * a;
  const r_i = a / (2 * tanHalf);
  const R = a / (2 * sinHalf);
  const area = 0.5 * n * a * r_i;
  const intAngle = ((n - 2) * 180) / n;
  const extAngle = 360 / n;
  const diagonalsCount = (n * (n - 3)) / 2;

  return {
    calculator: "regular-polygon",
    inputs: { n, driver, value: val, precision: prec, units },
    result: {
      sides_count: n,
      side_length: roundPrec(a, prec),
      area: roundPrec(area, prec),
      perimeter: roundPrec(p, prec),
      apothem_inradius: roundPrec(r_i, prec),
      circumradius: roundPrec(R, prec),
      interior_angle_deg: roundPrec(intAngle, prec),
      exterior_angle_deg: roundPrec(extAngle, prec),
      central_angle_deg: roundPrec(extAngle, prec),
      diagonals_count: diagonalsCount,
      sum_interior_angles_deg: (n - 2) * 180
    },
    exact_radicals: {
      apothem: "a / [2 tan(π/n)]",
      circumradius: "a / [2 sin(π/n)]",
      area: "[n · a²] / [4 tan(π/n)]"
    },
    units: { length: units, area: `${units}²` }
  };
}

// ==========================================
// 3. MORTGAGE AMORTIZATION SOLVER
// ==========================================
export function solveMortgage(params = {}) {
  const P = Math.max(0, parseFloat(params.principal ?? 400000));
  const annualRate = Math.max(0, parseFloat(params.annual_rate ?? params.rate ?? 6.5));
  const years = Math.max(1, parseFloat(params.term_years ?? params.years ?? 30));
  const extraMonthly = Math.max(0, parseFloat(params.extra_monthly ?? 0));
  const prec = 2;

  const r = (annualRate / 100) / 12;
  const n = Math.round(years * 12);

  let monthlyPayment = 0;
  if (r === 0) {
    monthlyPayment = P / n;
  } else {
    const factor = Math.pow(1 + r, n);
    monthlyPayment = P * (r * factor) / (factor - 1);
  }

  const standardTotalPaid = monthlyPayment * n;
  const standardTotalInterest = standardTotalPaid - P;

  // Payoff schedule simulation with extra payments
  let balance = P;
  let totalInterestWithExtra = 0;
  let totalPaidWithExtra = 0;
  let monthsWithExtra = 0;
  const effectiveMonthly = monthlyPayment + extraMonthly;

  while (balance > 0.01 && monthsWithExtra < n + 1200) {
    monthsWithExtra++;
    const interestMonth = balance * r;
    let principalMonth = effectiveMonthly - interestMonth;
    if (principalMonth > balance) {
      principalMonth = balance;
    }
    balance -= principalMonth;
    totalInterestWithExtra += interestMonth;
    totalPaidWithExtra += (principalMonth + interestMonth);
  }

  const interestSaved = Math.max(0, standardTotalInterest - totalInterestWithExtra);
  const monthsSaved = Math.max(0, n - monthsWithExtra);
  const yearsSaved = roundPrec(monthsSaved / 12, 1);

  return {
    calculator: "mortgage",
    inputs: {
      principal: P,
      annual_rate: annualRate,
      term_years: years,
      extra_monthly: extraMonthly
    },
    result: {
      monthly_principal_and_interest: roundPrec(monthlyPayment, prec),
      total_monthly_payment: roundPrec(effectiveMonthly, prec),
      total_standard_payment: roundPrec(standardTotalPaid, prec),
      total_standard_interest: roundPrec(standardTotalInterest, prec),
      scheduled_payoff_months: n,
      actual_payoff_months: monthsWithExtra,
      interest_saved: roundPrec(interestSaved, prec),
      time_saved_years: yearsSaved,
      total_paid_with_extra: roundPrec(totalPaidWithExtra, prec)
    },
    units: { currency: "USD" }
  };
}

// ==========================================
// 4. COMPOUND INTEREST SOLVER
// ==========================================
export function solveCompoundInterest(params = {}) {
  const P = Math.max(0, parseFloat(params.principal ?? 10000));
  const ratePct = parseFloat(params.annual_rate ?? params.rate ?? 7.0);
  const years = Math.max(0.1, parseFloat(params.years ?? 10));
  const freq = parseInt(params.compound_frequency ?? params.compound_freq ?? 12, 10); // 12 = monthly
  const monthlyContrib = Math.max(0, parseFloat(params.monthly_contribution ?? 500));
  const prec = 2;

  const r = ratePct / 100;
  const apy = Math.pow(1 + r / freq, freq) - 1;

  // Monthly iterative compound model for precision matching deposit flows
  let balance = P;
  let totalDeposits = P;
  const totalMonths = Math.round(years * 12);
  const monthlyRate = Math.pow(1 + r / freq, freq / 12) - 1;

  for (let m = 1; m <= totalMonths; m++) {
    balance = balance * (1 + monthlyRate) + monthlyContrib;
    totalDeposits += monthlyContrib;
  }

  const totalInterestEarned = balance - totalDeposits;

  return {
    calculator: "compound-interest",
    inputs: {
      principal: P,
      annual_rate: ratePct,
      years,
      compound_frequency: freq,
      monthly_contribution: monthlyContrib
    },
    result: {
      future_value: roundPrec(balance, prec),
      total_principal_invested: roundPrec(totalDeposits, prec),
      total_interest_earned: roundPrec(totalInterestEarned, prec),
      effective_apy_percentage: roundPrec(apy * 100, 3)
    },
    units: { currency: "USD" }
  };
}

// ==========================================
// 5. CAGR (COMPOUND ANNUAL GROWTH RATE)
// ==========================================
export function solveCagr(params = {}) {
  const initial = Math.max(0.0001, parseFloat(params.initial_value ?? 10000));
  const finalVal = Math.max(0, parseFloat(params.final_value ?? 25000));
  const years = Math.max(0.01, parseFloat(params.years ?? 5));
  const prec = 4;

  const cagr = Math.pow(finalVal / initial, 1 / years) - 1;
  const totalGrowth = finalVal - initial;
  const totalReturnPct = (totalGrowth / initial) * 100;

  return {
    calculator: "cagr",
    inputs: { initial_value: initial, final_value: finalVal, years },
    result: {
      cagr_percentage: roundPrec(cagr * 100, prec),
      cagr_decimal: roundPrec(cagr, 6),
      total_growth_amount: roundPrec(totalGrowth, 2),
      total_return_percentage: roundPrec(totalReturnPct, 2),
      growth_multiple: roundPrec(finalVal / initial, 3)
    },
    units: { return: "%", currency: "USD" }
  };
}

// ==========================================
// 6. AUTO LOAN FINANCING SOLVER
// ==========================================
export function solveAutoLoan(params = {}) {
  const price = Math.max(0, parseFloat(params.vehicle_price ?? 35000));
  const down = Math.max(0, parseFloat(params.down_payment ?? 5000));
  const tradeIn = Math.max(0, parseFloat(params.trade_in ?? 2000));
  const ratePct = Math.max(0, parseFloat(params.interest_rate ?? 5.9));
  const termMonths = Math.max(6, parseInt(params.term_months ?? 60, 10));
  const taxPct = Math.max(0, parseFloat(params.sales_tax_pct ?? 6.0));
  const prec = 2;

  const taxableAmount = Math.max(0, price - tradeIn);
  const salesTax = taxableAmount * (taxPct / 100);
  const loanPrincipal = Math.max(0, price + salesTax - down - tradeIn);

  const r = (ratePct / 100) / 12;
  let monthlyPayment = 0;
  if (r === 0) {
    monthlyPayment = loanPrincipal / termMonths;
  } else {
    const factor = Math.pow(1 + r, termMonths);
    monthlyPayment = loanPrincipal * (r * factor) / (factor - 1);
  }

  const totalPayments = monthlyPayment * termMonths;
  const totalInterest = totalPayments - loanPrincipal;
  const totalVehicleCost = totalPayments + down + tradeIn;

  return {
    calculator: "auto-loan",
    inputs: {
      vehicle_price: price,
      down_payment: down,
      trade_in: tradeIn,
      interest_rate: ratePct,
      term_months: termMonths,
      sales_tax_pct: taxPct
    },
    result: {
      loan_amount: roundPrec(loanPrincipal, prec),
      monthly_payment: roundPrec(monthlyPayment, prec),
      sales_tax_amount: roundPrec(salesTax, prec),
      total_interest_paid: roundPrec(totalInterest, prec),
      total_payments: roundPrec(totalPayments, prec),
      total_vehicle_cost: roundPrec(totalVehicleCost, prec)
    },
    units: { currency: "USD" }
  };
}

// ==========================================
// 7. CONCRETE VOLUME & BAG YIELDS SOLVER
// ==========================================
export function solveConcreteVolume(params = {}) {
  const shape = (params.shape || 'slab').toLowerCase();
  const prec = 3;

  let lengthFt = parseFloat(params.length ?? 20);
  let widthFt = parseFloat(params.width ?? 10);
  let depthInches = parseFloat(params.depth ?? params.thickness ?? 4);

  let volumeCuFt = 0;
  if (shape === 'column' || shape === 'cylinder') {
    const diameterInches = parseFloat(params.diameter ?? 12);
    const heightFt = parseFloat(params.height ?? lengthFt ?? 8);
    const radiusFt = (diameterInches / 12) / 2;
    volumeCuFt = Math.PI * radiusFt * radiusFt * heightFt;
  } else {
    // slab or footing
    const depthFt = depthInches / 12;
    volumeCuFt = lengthFt * widthFt * depthFt;
  }

  const cuYards = volumeCuFt / 27;
  const cuYardsWithBuffer = cuYards * 1.10; // +10% standard buffer
  const bags60 = Math.ceil(volumeCuFt / 0.45);
  const bags80 = Math.ceil(volumeCuFt / 0.60);

  return {
    calculator: "concrete-volume",
    inputs: { shape, length_ft: lengthFt, width_ft: widthFt, depth_in: depthInches },
    result: {
      volume_cubic_feet: roundPrec(volumeCuFt, prec),
      volume_cubic_yards: roundPrec(cuYards, prec),
      volume_cubic_yards_with_10pct_buffer: roundPrec(cuYardsWithBuffer, prec),
      premix_60lb_bags_needed: bags60,
      premix_80lb_bags_needed: bags80
    },
    units: { volume: "cubic yards", bags: "bags" }
  };
}

// ==========================================
// 8. ROOF PITCH & RAFTER LENGTH SOLVER
// ==========================================
export function solveRoofPitch(params = {}) {
  const rise = Math.max(0.1, parseFloat(params.rise ?? 6));
  const run = Math.max(0.1, parseFloat(params.run ?? 12));
  const runFt = parseFloat(params.building_run_feet ?? params.span ?? 16);
  const prec = 3;

  const slope = rise / run;
  const angleRad = Math.atan(slope);
  const angleDeg = (angleRad * 180) / Math.PI;
  const pitchMultiplier = Math.sqrt(1 + slope * slope);
  const rafterLengthFt = runFt * pitchMultiplier;

  return {
    calculator: "roof-pitch",
    inputs: { rise, run, building_run_feet: runFt },
    result: {
      pitch_ratio: `${roundPrec(rise, 1)}:12`,
      slope_decimal: roundPrec(slope, prec),
      pitch_angle_degrees: roundPrec(angleDeg, 2),
      pitch_multiplier: roundPrec(pitchMultiplier, 4),
      rafter_length_feet: roundPrec(rafterLengthFt, 2)
    },
    units: { angle: "degrees", length: "feet" }
  };
}

// ==========================================
// 9. CIRCLE SECTOR, CHORD & SAGITTA SOLVER
// ==========================================
export function solveCircleSector(params = {}) {
  const r = Math.max(0.001, parseFloat(params.radius ?? params.r ?? 10));
  const thetaDeg = Math.max(0.01, Math.min(360, parseFloat(params.angle_deg ?? params.theta ?? 60)));
  const prec = 4;

  const thetaRad = (thetaDeg * Math.PI) / 180;
  const arcLength = r * thetaRad;
  const chordLength = 2 * r * Math.sin(thetaRad / 2);
  const sagitta = r * (1 - Math.cos(thetaRad / 2));
  const sectorArea = 0.5 * r * r * thetaRad;

  return {
    calculator: "circle-sector",
    inputs: { radius: r, angle_deg: thetaDeg },
    result: {
      radius: roundPrec(r, prec),
      central_angle_deg: roundPrec(thetaDeg, 2),
      arc_length: roundPrec(arcLength, prec),
      chord_length: roundPrec(chordLength, prec),
      sagitta_height: roundPrec(sagitta, prec),
      sector_area: roundPrec(sectorArea, prec)
    },
    exact_radicals: {
      arc_length: "r · θ_rad",
      chord_length: "2r · sin(θ / 2)",
      sagitta: "r[1 - cos(θ / 2)]",
      sector_area: "½ r² θ_rad"
    },
    units: { length: "units", area: "units²" }
  };
}

// ==========================================
// 10. RIGHT TRIANGLE SOLVER
// ==========================================
export function solveRightTriangle(params = {}) {
  const a = Math.max(0.001, parseFloat(params.leg_a ?? params.a ?? 3));
  const b = Math.max(0.001, parseFloat(params.leg_b ?? params.b ?? 4));
  const prec = 4;

  const c = Math.sqrt(a * a + b * b);
  const area = 0.5 * a * b;
  const perimeter = a + b + c;
  const altitude = (a * b) / c;
  const inradius = (a + b - c) / 2;
  const angleADeg = Math.atan(a / b) * (180 / Math.PI);
  const angleBDeg = 90 - angleADeg;

  return {
    calculator: "right-triangle",
    inputs: { leg_a: a, leg_b: b },
    result: {
      leg_a: roundPrec(a, prec),
      leg_b: roundPrec(b, prec),
      hypotenuse_c: roundPrec(c, prec),
      area: roundPrec(area, prec),
      perimeter: roundPrec(perimeter, prec),
      altitude_to_hypotenuse: roundPrec(altitude, prec),
      inradius: roundPrec(inradius, prec),
      angle_alpha_deg: roundPrec(angleADeg, 2),
      angle_beta_deg: roundPrec(angleBDeg, 2)
    },
    exact_radicals: {
      hypotenuse: "√(a² + b²)",
      area: "½ · a · b",
      altitude: "(a · b) / c",
      inradius: "(a + b - c) / 2"
    },
    units: { length: "units", area: "units²" }
  };
}

// Master Calculator Registry Map
export const CALCULATOR_REGISTRY = {
  "octagon": solveOctagon,
  "regular-polygon": solveRegularPolygon,
  "mortgage": solveMortgage,
  "compound-interest": solveCompoundInterest,
  "cagr": solveCagr,
  "auto-loan": solveAutoLoan,
  "concrete-volume": solveConcreteVolume,
  "roof-pitch": solveRoofPitch,
  "circle-sector": solveCircleSector,
  "right-triangle": solveRightTriangle
};
