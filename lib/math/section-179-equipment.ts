/**
 * lib/math/section-179-equipment.ts
 * OmniOperand Section 179 Heavy Equipment Tax Shield & Cash-Flow Sizer
 *
 * Implements Internal Revenue Code (IRC) Section 179 & Section 168(k) Bonus Depreciation:
 * - Commercial Heavy Machinery (>6,000 lbs GVWR) vs. Heavy SUV vs. Light Passenger Vehicles
 * - Statutory Section 179 Cap ($1,220,000 limit / $3,050,000 phase-out threshold)
 * - Immediate Year 1 Tax Shield Cash Inversion
 * - Leveraged Equipment Financing "Cash-in-Pocket" Net Arbitrage Analysis
 * - 5-Year Amortization vs. Tax Write-Off Schedule
 */

export type EquipmentType = 'heavy_machinery' | 'heavy_suv' | 'light_vehicle';
export type FinancingMethod = 'loan' | 'cash';

export interface Section179Inputs {
  equipmentPurchasePrice: number; // e.g. $125,000
  equipmentType?: EquipmentType; // default 'heavy_machinery'
  financingMethod?: FinancingMethod; // default 'loan'
  downPaymentPct?: number; // default 10%
  loanInterestRatePct?: number; // default 8.5%
  loanTermMonths?: number; // default 60
  monthsActiveInYear1?: number; // default 6
  entityTaxBracketPct?: number; // default 35% (combined corporate/pass-through)
}

export interface YearScheduleItem {
  year: number;
  principalPaid: number;
  interestPaid: number;
  totalLoanPayment: number;
  taxDeduction: number;
  taxSavings: number;
  netAnnualCashFlow: number;
}

export interface Section179Outputs {
  purchasePrice: number;
  equipmentType: EquipmentType;
  equipmentTypeLabel: string;
  financingMethod: FinancingMethod;
  section179Deduction: number;
  bonusDepreciationDeduction: number;
  totalYear1Deduction: number;
  taxBracketPct: number;
  immediateYear1TaxSavings: number;
  financingMetrics: {
    downPaymentAmount: number;
    financedPrincipal: number;
    monthlyLoanPayment: number;
    year1LoanPayments: number;
    totalYear1CashOutlay: number;
    lifetimeLoanInterest: number;
  };
  netYear1CashFlow: number; // Tax Savings - Year 1 Cash Outlay ("Cash in Pocket")
  isCashPositiveInYear1: boolean;
  fiveYearSchedule: YearScheduleItem[];
  leadTakeawayHeadline: string;
}

const SECTION_179_CAP = 1220000; // 2024 statutory limit
const SECTION_179_PHASEOUT = 3050000;
const HEAVY_SUV_CAP = 30500;
const LUXURY_AUTO_CAP_YEAR1 = 20400;
const BONUS_DEPRECIATION_RATE = 0.60; // 60% phase-down rate for 2024

export function calculateSection179Equipment(inputs: Section179Inputs): Section179Outputs {
  const price = Math.max(0, inputs.equipmentPurchasePrice || 0);
  const eqType: EquipmentType = inputs.equipmentType || 'heavy_machinery';
  const method: FinancingMethod = inputs.financingMethod || 'loan';
  const taxBracket = Math.max(0, Math.min(60, inputs.entityTaxBracketPct ?? 35)) / 100;

  // --- 1. Statutory Deduction Calculation ---
  let sec179Deduction = 0;
  let bonusDepreciation = 0;
  let eqTypeLabel = 'Heavy Machinery & Commercial Yellow Iron (>6,000 lbs)';

  if (eqType === 'heavy_machinery') {
    // 100% eligible up to $1,220,000 cap
    const allowable179 = Math.max(0, SECTION_179_CAP - Math.max(0, price - SECTION_179_PHASEOUT));
    sec179Deduction = Math.min(price, allowable179);
    const remainingBasis = Math.max(0, price - sec179Deduction);
    bonusDepreciation = remainingBasis * BONUS_DEPRECIATION_RATE;
  } else if (eqType === 'heavy_suv') {
    eqTypeLabel = 'Heavy SUV / Crossover (6,000–14,000 lbs GVWR)';
    sec179Deduction = Math.min(price, HEAVY_SUV_CAP);
    const remainingBasis = Math.max(0, price - sec179Deduction);
    bonusDepreciation = remainingBasis * BONUS_DEPRECIATION_RATE;
  } else {
    eqTypeLabel = 'Light Passenger Vehicle (<6,000 lbs GVWR - Luxury Auto Limit)';
    sec179Deduction = Math.min(price, LUXURY_AUTO_CAP_YEAR1);
    bonusDepreciation = 0; // Capped by Section 280F
  }

  const totalYear1Deduction = sec179Deduction + bonusDepreciation;
  const immediateYear1TaxSavings = totalYear1Deduction * taxBracket;

  // --- 2. Financing & Cash Outlay Calculation ---
  const downPct = Math.max(0, Math.min(100, inputs.downPaymentPct ?? 10)) / 100;
  const ratePct = Math.max(0, inputs.loanInterestRatePct ?? 8.5) / 100;
  const termMonths = Math.max(12, Math.min(120, inputs.loanTermMonths ?? 60));
  const activeMonthsYr1 = Math.max(1, Math.min(12, inputs.monthsActiveInYear1 ?? 6));

  let downPaymentAmount = 0;
  let financedPrincipal = 0;
  let monthlyPayment = 0;
  let year1LoanPayments = 0;
  let totalYear1CashOutlay = 0;
  let lifetimeInterest = 0;

  if (method === 'cash') {
    totalYear1CashOutlay = price;
  } else {
    downPaymentAmount = price * downPct;
    financedPrincipal = Math.max(0, price - downPaymentAmount);

    const r = ratePct / 12;
    if (r === 0) {
      monthlyPayment = financedPrincipal / termMonths;
    } else {
      const f = Math.pow(1 + r, termMonths);
      monthlyPayment = financedPrincipal * ((r * f) / (f - 1));
    }

    year1LoanPayments = monthlyPayment * activeMonthsYr1;
    totalYear1CashOutlay = downPaymentAmount + year1LoanPayments;
    lifetimeInterest = monthlyPayment * termMonths - financedPrincipal;
  }

  // Net Year 1 Cash Flow: Tax Savings minus Year 1 Outlay
  const netYear1CashFlow = immediateYear1TaxSavings - totalYear1CashOutlay;
  const isCashPositive = netYear1CashFlow > 0;

  // --- 3. 5-Year Schedule ---
  const schedule: YearScheduleItem[] = [];
  let remainingBal = financedPrincipal;
  const rMo = ratePct / 12;

  for (let y = 1; y <= 5; y++) {
    const monthsInYr = y === 1 ? activeMonthsYr1 : 12;
    let prinY = 0;
    let intY = 0;

    if (method === 'loan' && remainingBal > 0) {
      for (let m = 0; m < monthsInYr; m++) {
        if (remainingBal <= 0) break;
        const intMo = remainingBal * rMo;
        const prinMo = Math.min(remainingBal, monthlyPayment - intMo);
        remainingBal = Math.max(0, remainingBal - prinMo);
        prinY += prinMo;
        intY += intMo;
      }
    }

    const totalPmts = y === 1 ? downPaymentAmount + (prinY + intY) : prinY + intY;
    const taxDed = y === 1 ? totalYear1Deduction + intY : intY; // Year 1 takes upfront write-off; subsequent years write off interest
    const taxSav = taxDed * taxBracket;
    const netCf = taxSav - totalPmts;

    schedule.push({
      year: y,
      principalPaid: round2(prinY),
      interestPaid: round2(intY),
      totalLoanPayment: round2(totalPmts),
      taxDeduction: round2(taxDed),
      taxSavings: round2(taxSav),
      netAnnualCashFlow: round2(netCf),
    });
  }

  let takeaway = `Section 179 generates $${Math.round(immediateYear1TaxSavings).toLocaleString()} in cash tax savings, requiring only $${Math.round(totalYear1CashOutlay).toLocaleString()} in Year 1 financing outlay.`;
  if (isCashPositive) {
    takeaway = `Net Cash-Positive Arbitrage: You pocket +$${Math.round(netYear1CashFlow).toLocaleString()} in immediate net cash during Year 1 after covering all down payment and equipment loan payments.`;
  }

  return {
    purchasePrice: round2(price),
    equipmentType: eqType,
    equipmentTypeLabel: eqTypeLabel,
    financingMethod: method,
    section179Deduction: round2(sec179Deduction),
    bonusDepreciationDeduction: round2(bonusDepreciation),
    totalYear1Deduction: round2(totalYear1Deduction),
    taxBracketPct: round2(taxBracket * 100),
    immediateYear1TaxSavings: round2(immediateYear1TaxSavings),
    financingMetrics: {
      downPaymentAmount: round2(downPaymentAmount),
      financedPrincipal: round2(financedPrincipal),
      monthlyLoanPayment: round2(monthlyPayment),
      year1LoanPayments: round2(year1LoanPayments),
      totalYear1CashOutlay: round2(totalYear1CashOutlay),
      lifetimeLoanInterest: round2(lifetimeInterest),
    },
    netYear1CashFlow: round2(netYear1CashFlow),
    isCashPositiveInYear1: isCashPositive,
    fiveYearSchedule: schedule,
    leadTakeawayHeadline: takeaway,
  };
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}
