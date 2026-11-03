/**
 * lib/math/chattel-vs-land-home.ts
 * OmniOperand Chattel Loan vs. Land-Home Modular Mortgage Comparative Engine
 *
 * Models:
 * - Chattel Personal Property Financing (Higher interest rate, shorter amortization, escalating park lot rent)
 * - Titled Real Property Modular/Manufactured Mortgage (Lower rate, 30-year amortization, land equity appreciation)
 * - 5-Year, 10-Year, and 30-Year Cumulative Interest & Equity Schedules
 * - Asset Depreciation (Personal Property on leased pad) vs. Appreciation (Land + Home Real Estate)
 * - Crossover Breakeven Year Analysis
 */

export interface ChattelTerms {
  interestRatePct: number; // e.g. 9.75%
  termYears: number; // e.g. 20
  downPaymentPct: number; // e.g. 10%
  monthlyLotRent: number; // e.g. $650/mo
  annualLotRentInflationPct?: number; // e.g. 3.5%
  annualHomeDepreciationPct?: number; // e.g. 2.0%
}

export interface LandHomeTerms {
  landCost: number; // e.g. $65,000
  interestRatePct: number; // e.g. 6.75%
  termYears: number; // e.g. 30
  downPaymentPct: number; // e.g. 5%
  annualPropertyTaxRatePct?: number; // e.g. 1.2%
  annualInsurance?: number; // e.g. $1,400
  annualAppreciationPct?: number; // e.g. 3.5%
}

export interface ChattelVsLandHomeInputs {
  manufacturedHomeCost: number; // e.g. $150,000
  chattel: ChattelTerms;
  landHome: LandHomeTerms;
}

export interface AmortizationSnapshot {
  year: number;
  remainingLoanBalance: number;
  cumulativeInterestPaid: number;
  cumulativeTotalOutlay: number;
  estimatedAssetValue: number;
  netEquity: number;
}

export interface ChattelVsLandHomeOutputs {
  chattelSummary: {
    homeCost: number;
    downPaymentAmount: number;
    financedPrincipal: number;
    monthlyPI: number;
    initialMonthlyLotRent: number;
    initialTotalMonthlyOutlay: number;
    lifetimeInterestPaid: number;
    snapshots: {
      year5: AmortizationSnapshot;
      year10: AmortizationSnapshot;
      year20: AmortizationSnapshot;
      year30: AmortizationSnapshot;
    };
  };
  landHomeSummary: {
    packageTotalCost: number;
    downPaymentAmount: number;
    financedPrincipal: number;
    monthlyPI: number;
    monthlyTaxesAndInsurance: number;
    initialTotalMonthlyOutlay: number;
    lifetimeInterestPaid: number;
    snapshots: {
      year5: AmortizationSnapshot;
      year10: AmortizationSnapshot;
      year20: AmortizationSnapshot;
      year30: AmortizationSnapshot;
    };
  };
  comparison: {
    monthlyPaymentDiffInitial: number; // LandHome - Chattel (positive means LandHome initially costs more)
    tenYearCumulativeOutlayDiff: number; // Chattel Outlay - LandHome Outlay
    tenYearNetEquityAdvantage: number; // LandHome Equity - Chattel Equity
    breakevenYear: number; // Year when LandHome net wealth surpasses Chattel
    recommendationSummary: string;
  };
}

export function calculateChattelVsLandHome(inputs: ChattelVsLandHomeInputs): ChattelVsLandHomeOutputs {
  const homeCost = Math.max(0, inputs.manufacturedHomeCost || 0);

  // --- 1. Chattel Calculation ---
  const cRate = Math.max(0, inputs.chattel.interestRatePct ?? 9.75) / 100;
  const cTerm = Math.max(1, Math.min(30, inputs.chattel.termYears ?? 20));
  const cDownPct = Math.max(0, Math.min(90, inputs.chattel.downPaymentPct ?? 10)) / 100;
  const initialLotRent = Math.max(0, inputs.chattel.monthlyLotRent ?? 650);
  const lotInflation = Math.max(0, inputs.chattel.annualLotRentInflationPct ?? 3.5) / 100;
  const cDepreciation = Math.max(0, inputs.chattel.annualHomeDepreciationPct ?? 2.0) / 100;

  const cDownPayment = homeCost * cDownPct;
  const cPrincipal = Math.max(0, homeCost - cDownPayment);
  const cMonthlyPI = calculateMonthlyPI(cPrincipal, cRate, cTerm);
  const cInitialTotalMonthly = cMonthlyPI + initialLotRent;

  // --- 2. Land-Home Calculation ---
  const landCost = Math.max(0, inputs.landHome.landCost ?? 65000);
  const lhPackageCost = homeCost + landCost;
  const lhRate = Math.max(0, inputs.landHome.interestRatePct ?? 6.75) / 100;
  const lhTerm = Math.max(1, Math.min(40, inputs.landHome.termYears ?? 30));
  const lhDownPct = Math.max(0, Math.min(90, inputs.landHome.downPaymentPct ?? 5)) / 100;
  const taxRate = Math.max(0, inputs.landHome.annualPropertyTaxRatePct ?? 1.2) / 100;
  const annualIns = Math.max(0, inputs.landHome.annualInsurance ?? 1400);
  const lhAppreciation = Math.max(0, inputs.landHome.annualAppreciationPct ?? 3.5) / 100;

  const lhDownPayment = lhPackageCost * lhDownPct;
  const lhPrincipal = Math.max(0, lhPackageCost - lhDownPayment);
  const lhMonthlyPI = calculateMonthlyPI(lhPrincipal, lhRate, lhTerm);
  const lhMonthlyEscrow = (lhPackageCost * taxRate + annualIns) / 12;
  const lhInitialTotalMonthly = lhMonthlyPI + lhMonthlyEscrow;

  // --- Month-by-month simulation for 30 years (360 months) ---
  let cBal = cPrincipal;
  let cCumInt = 0;
  let cCumOutlay = cDownPayment;

  let lhBal = lhPrincipal;
  let lhCumInt = 0;
  let lhCumOutlay = lhDownPayment;

  const cSnapshots: Record<number, AmortizationSnapshot> = {};
  const lhSnapshots: Record<number, AmortizationSnapshot> = {};

  let breakevenYear = 30;
  let breakevenFound = false;

  for (let m = 1; m <= 360; m++) {
    const yr = Math.ceil(m / 12);
    const yrFrac = m / 12;

    // Chattel step
    const currentLotRent = initialLotRent * Math.pow(1 + lotInflation, (m - 1) / 12);
    let cIntMo = 0;
    let cPrinMo = 0;
    if (m <= cTerm * 12 && cBal > 0) {
      cIntMo = cBal * (cRate / 12);
      cPrinMo = Math.min(cBal, cMonthlyPI - cIntMo);
      cBal = Math.max(0, cBal - cPrinMo);
      cCumInt += cIntMo;
      cCumOutlay += cMonthlyPI + currentLotRent;
    } else {
      cCumOutlay += currentLotRent; // After loan payoff, park rent continues forever!
    }

    // Land-Home step
    let lhIntMo = 0;
    let lhPrinMo = 0;
    if (m <= lhTerm * 12 && lhBal > 0) {
      lhIntMo = lhBal * (lhRate / 12);
      lhPrinMo = Math.min(lhBal, lhMonthlyPI - lhIntMo);
      lhBal = Math.max(0, lhBal - lhPrinMo);
      lhCumInt += lhIntMo;
      lhCumOutlay += lhMonthlyPI + lhMonthlyEscrow;
    } else {
      lhCumOutlay += lhMonthlyEscrow;
    }

    // Snapshot recordings at key milestone years: 5, 10, 20, 30
    if (m === 60 || m === 120 || m === 240 || m === 360) {
      const yearNum = m / 12;

      // Chattel asset value: manufactured home depreciates
      const cAssetVal = homeCost * Math.pow(1 - cDepreciation, yearNum);
      const cNetEq = Math.max(0, cAssetVal - cBal);
      cSnapshots[yearNum] = {
        year: yearNum,
        remainingLoanBalance: round2(cBal),
        cumulativeInterestPaid: round2(cCumInt),
        cumulativeTotalOutlay: round2(cCumOutlay),
        estimatedAssetValue: round2(cAssetVal),
        netEquity: round2(cNetEq),
      };

      // Land-Home asset value: package appreciates
      const lhAssetVal = lhPackageCost * Math.pow(1 + lhAppreciation, yearNum);
      const lhNetEq = Math.max(0, lhAssetVal - lhBal);
      lhSnapshots[yearNum] = {
        year: yearNum,
        remainingLoanBalance: round2(lhBal),
        cumulativeInterestPaid: round2(lhCumInt),
        cumulativeTotalOutlay: round2(lhCumOutlay),
        estimatedAssetValue: round2(lhAssetVal),
        netEquity: round2(lhNetEq),
      };
    }

    // Check Breakeven: when Land-Home Net Wealth (Equity - Cumulative Outlay) exceeds Chattel Net Wealth
    if (!breakevenFound && m % 12 === 0) {
      const currentYear = m / 12;
      const cAssetVal = homeCost * Math.pow(1 - cDepreciation, currentYear);
      const cNetWealth = Math.max(0, cAssetVal - cBal) - cCumOutlay;

      const lhAssetVal = lhPackageCost * Math.pow(1 + lhAppreciation, currentYear);
      const lhNetWealth = Math.max(0, lhAssetVal - lhBal) - lhCumOutlay;

      if (lhNetWealth > cNetWealth) {
        breakevenYear = currentYear;
        breakevenFound = true;
      }
    }
  }

  const tenYearOutlayDiff = cSnapshots[10].cumulativeTotalOutlay - lhSnapshots[10].cumulativeTotalOutlay;
  const tenYearEquityAdvantage = lhSnapshots[10].netEquity - cSnapshots[10].netEquity;

  let rec = `Buying land with a 30-year modular mortgage builds $${Math.round(tenYearEquityAdvantage).toLocaleString()} more equity over 10 years and avoids indefinite lot rent inflation.`;
  if (breakevenYear <= 5) {
    rec = `Strong Buy Land-Home: Breakeven occurs in Year ${breakevenYear}. Land appreciation rapidly offsets the higher initial package price.`;
  }

  return {
    chattelSummary: {
      homeCost: round2(homeCost),
      downPaymentAmount: round2(cDownPayment),
      financedPrincipal: round2(cPrincipal),
      monthlyPI: round2(cMonthlyPI),
      initialMonthlyLotRent: round2(initialLotRent),
      initialTotalMonthlyOutlay: round2(cInitialTotalMonthly),
      lifetimeInterestPaid: round2(cSnapshots[20].cumulativeInterestPaid),
      snapshots: {
        year5: cSnapshots[5],
        year10: cSnapshots[10],
        year20: cSnapshots[20],
        year30: cSnapshots[30],
      },
    },
    landHomeSummary: {
      packageTotalCost: round2(lhPackageCost),
      downPaymentAmount: round2(lhDownPayment),
      financedPrincipal: round2(lhPrincipal),
      monthlyPI: round2(lhMonthlyPI),
      monthlyTaxesAndInsurance: round2(lhMonthlyEscrow),
      initialTotalMonthlyOutlay: round2(lhInitialTotalMonthly),
      lifetimeInterestPaid: round2(lhSnapshots[30].cumulativeInterestPaid),
      snapshots: {
        year5: lhSnapshots[5],
        year10: lhSnapshots[10],
        year20: lhSnapshots[20],
        year30: lhSnapshots[30],
      },
    },
    comparison: {
      monthlyPaymentDiffInitial: round2(lhInitialTotalMonthly - cInitialTotalMonthly),
      tenYearCumulativeOutlayDiff: round2(tenYearOutlayDiff),
      tenYearNetEquityAdvantage: round2(tenYearEquityAdvantage),
      breakevenYear,
      recommendationSummary: rec,
    },
  };
}

function calculateMonthlyPI(principal: number, annualRate: number, termYears: number): number {
  if (principal <= 0) return 0;
  const n = termYears * 12;
  const r = annualRate / 12;
  if (r === 0) return principal / n;
  const f = Math.pow(1 + r, n);
  return principal * ((r * f) / (f - 1));
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}
