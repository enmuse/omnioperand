/**
 * lib/math/locum-tenens-tax-calculator.ts
 * OmniOperand 1099 Travel Healthcare / Locum Tenens Tax Arbitrage Engine
 *
 * Implements IRS Tax Code Standards for Traveling Physicians, CRNAs, & Allied Providers:
 * - IRS Revenue Ruling 73-529 Tax Home & Duplicated Living Expense Substantiation
 * - GSA Per Diem Rule Non-Taxable Stipend Splits (Lodging + Meals/Incidentals)
 * - Self-Employment Tax (15.3% on 92.35% Net SE Income, SS Cap + Medicare Surtax)
 * - Section 401(k) Solo / SEP-IRA Tax Shield Deferral Modeling
 * - Progressive Federal & State Income Tax Arbitrage vs. Traditional W-2 Employment
 */

export interface LocumTenensInputs {
  w2BaseSalary: number; // e.g. $180,000
  locumHourlyRate: number; // e.g. $150/hr
  projectedBillableHours: number; // e.g. 1,600 hrs
  weeklyNonTaxableStipend: number; // e.g. $1,400/wk (GSA compliant)
  taxFilingStatus: 'single' | 'married'; // Single or Married Filing Jointly
  primaryHomeStateTaxRatePct?: number; // e.g. 5.0% flat or effective
  monthlyDuplicatedHousingExpense?: number; // e.g. $1,500/mo required for IRS tax home
  annualBusinessDeductions?: number; // e.g. $12,000 (CME, mileage, scrubs, health ins)
  solo401kContribution?: number; // Optional retirement shelter (up to $69,000)
}

export interface W2Breakdown {
  grossSalary: number;
  ficaTax: number;
  federalIncomeTax: number;
  stateIncomeTax: number;
  totalTax: number;
  netTakeHomePay: number;
  effectiveTaxRatePct: number;
}

export interface LocumBreakdown {
  grossHourlyEarnings: number;
  nonTaxablePerDiemTotal: number;
  totalGrossInflow: number;
  businessDeductions: number;
  duplicatedHousingExpense: number;
  netScheduleCProfit: number;
  seTax: {
    socialSecurity: number;
    medicare: number;
    additionalMedicare: number;
    total: number;
    deductibleHalf: number;
  };
  solo401kContribution: number;
  taxableIncome: number;
  federalIncomeTax: number;
  stateIncomeTax: number;
  totalTaxLiability: number;
  quarterlyEstimatedTaxPayment: number;
  trueNetAfterTaxTakeHome: number;
  effectiveTaxRatePct: number;
}

export interface LocumTenensOutputs {
  w2Model: W2Breakdown;
  locumModel: LocumBreakdown;
  arbitrage: {
    netTakeHomeDifference: number; // Locum Net - W2 Net
    percentageIncrease: number;
    annualPerDiemTaxShieldSavings: number; // Estimated tax avoided via tax-free stipends
    quarterlyTaxSchedule: {
      q1_Apr15: number;
      q2_Jun15: number;
      q3_Sep15: number;
      q4_Jan15: number;
    };
    summaryRecommendation: string;
  };
}

const SS_WAGE_CAP = 168600; // Social Security wage cap
const STANDARD_DED_SINGLE = 14600;
const STANDARD_DED_MARRIED = 29200;

export function calculateLocumTenensTax(inputs: LocumTenensInputs): LocumTenensOutputs {
  const isMarried = inputs.taxFilingStatus === 'married';
  const stdDed = isMarried ? STANDARD_DED_MARRIED : STANDARD_DED_SINGLE;
  const stateRate = Math.max(0, inputs.primaryHomeStateTaxRatePct ?? 5.0) / 100;

  // --- 1. W-2 Permanent Benchmark ---
  const w2Gross = Math.max(0, inputs.w2BaseSalary || 0);
  const w2FicaSS = Math.min(w2Gross, SS_WAGE_CAP) * 0.062;
  const w2FicaMed = w2Gross * 0.0145;
  const w2AddMedThreshold = isMarried ? 250000 : 200000;
  const w2AddMed = Math.max(0, w2Gross - w2AddMedThreshold) * 0.009;
  const w2FicaTotal = w2FicaSS + w2FicaMed + w2AddMed;

  const w2Taxable = Math.max(0, w2Gross - stdDed);
  const w2FedTax = computeFederalIncomeTax(w2Taxable, isMarried);
  const w2StateTax = w2Taxable * stateRate;
  const w2TotalTax = w2FicaTotal + w2FedTax + w2StateTax;
  const w2NetTakeHome = w2Gross - w2TotalTax;
  const w2EffectiveRate = w2Gross > 0 ? (w2TotalTax / w2Gross) * 100 : 0;

  // --- 2. 1099 Locum Tenens Model ---
  const hourlyRate = Math.max(0, inputs.locumHourlyRate || 0);
  const hours = Math.max(0, inputs.projectedBillableHours || 0);
  const grossHourly = hourlyRate * hours;

  const weeklyStipend = Math.max(0, inputs.weeklyNonTaxableStipend || 0);
  const weeksWorked = hours > 0 ? hours / 40 : 0;
  const totalPerDiem = weeklyStipend * weeksWorked;
  const totalGrossInflow = grossHourly + totalPerDiem;

  const busDeductions = Math.max(0, inputs.annualBusinessDeductions ?? 12000);
  const monthlyDupHousing = Math.max(0, inputs.monthlyDuplicatedHousingExpense ?? 1500);
  const annualDupHousing = monthlyDupHousing * 12;

  const netSchedC = Math.max(0, grossHourly - busDeductions);

  // Self-Employment Tax
  const netSeEarnings = netSchedC * 0.9235;
  const seSS = Math.min(netSeEarnings, SS_WAGE_CAP) * 0.124;
  const seMed = netSeEarnings * 0.029;
  const seAddMedThreshold = isMarried ? 250000 : 200000;
  const seAddMed = Math.max(0, netSeEarnings - seAddMedThreshold) * 0.009;
  const seTotal = seSS + seMed + seAddMed;
  const deductibleHalfSE = seTotal / 2;

  // Solo 401(k) Shelter (Optional, capped at $69,000)
  const maxPossibleSolo401k = Math.min(69000, 23000 + Math.max(0, (netSchedC - deductibleHalfSE) * 0.20));
  const solo401kChosen = Math.min(maxPossibleSolo401k, Math.max(0, inputs.solo401kContribution ?? 0));

  const locumTaxable = Math.max(0, netSchedC - deductibleHalfSE - solo401kChosen - stdDed);
  const locumFedTax = computeFederalIncomeTax(locumTaxable, isMarried);
  const locumStateTax = locumTaxable * stateRate;
  const locumTotalTax = seTotal + locumFedTax + locumStateTax;

  // True Net After-Tax Cash Flow = Inflows - Business Expenses - Duplicated Living - Taxes
  const trueNetTakeHome = (grossHourly - busDeductions - annualDupHousing - locumTotalTax) + totalPerDiem;
  const locumEffectiveRate = totalGrossInflow > 0 ? (locumTotalTax / totalGrossInflow) * 100 : 0;

  const quarterlyPayment = locumTotalTax / 4;

  // --- 3. Arbitrage Advantage & Summary ---
  const netDiff = trueNetTakeHome - w2NetTakeHome;
  const pctInc = w2NetTakeHome > 0 ? (netDiff / w2NetTakeHome) * 100 : 0;
  // Tax saved by receiving per diem tax-free rather than as taxable W-2/1099 income (~30% bracket)
  const perDiemTaxShield = totalPerDiem * 0.32;

  const summary = `1099 Locum Tenens delivers $${Math.round(netDiff).toLocaleString()} (${pctInc.toFixed(1)}%) higher annual take-home pay than a $${Math.round(w2Gross).toLocaleString()} W-2 position, primarily driven by $${Math.round(totalPerDiem).toLocaleString()} in tax-free per diem housing stipends.`;

  return {
    w2Model: {
      grossSalary: round2(w2Gross),
      ficaTax: round2(w2FicaTotal),
      federalIncomeTax: round2(w2FedTax),
      stateIncomeTax: round2(w2StateTax),
      totalTax: round2(w2TotalTax),
      netTakeHomePay: round2(w2NetTakeHome),
      effectiveTaxRatePct: round2(w2EffectiveRate),
    },
    locumModel: {
      grossHourlyEarnings: round2(grossHourly),
      nonTaxablePerDiemTotal: round2(totalPerDiem),
      totalGrossInflow: round2(totalGrossInflow),
      businessDeductions: round2(busDeductions),
      duplicatedHousingExpense: round2(annualDupHousing),
      netScheduleCProfit: round2(netSchedC),
      seTax: {
        socialSecurity: round2(seSS),
        medicare: round2(seMed),
        additionalMedicare: round2(seAddMed),
        total: round2(seTotal),
        deductibleHalf: round2(deductibleHalfSE),
      },
      solo401kContribution: round2(solo401kChosen),
      taxableIncome: round2(locumTaxable),
      federalIncomeTax: round2(locumFedTax),
      stateIncomeTax: round2(locumStateTax),
      totalTaxLiability: round2(locumTotalTax),
      quarterlyEstimatedTaxPayment: round2(quarterlyPayment),
      trueNetAfterTaxTakeHome: round2(trueNetTakeHome),
      effectiveTaxRatePct: round2(locumEffectiveRate),
    },
    arbitrage: {
      netTakeHomeDifference: round2(netDiff),
      percentageIncrease: round2(pctInc),
      annualPerDiemTaxShieldSavings: round2(perDiemTaxShield),
      quarterlyTaxSchedule: {
        q1_Apr15: round2(quarterlyPayment),
        q2_Jun15: round2(quarterlyPayment),
        q3_Sep15: round2(quarterlyPayment),
        q4_Jan15: round2(quarterlyPayment),
      },
      summaryRecommendation: summary,
    },
  };
}

function computeFederalIncomeTax(taxableIncome: number, isMarried: boolean): number {
  if (taxableIncome <= 0) return 0;

  const bracketsSingle = [
    { cap: 11600, rate: 0.10 },
    { cap: 47150, rate: 0.12 },
    { cap: 100525, rate: 0.22 },
    { cap: 191950, rate: 0.24 },
    { cap: 243725, rate: 0.32 },
    { cap: 609350, rate: 0.35 },
    { cap: Infinity, rate: 0.37 },
  ];

  const bracketsMarried = [
    { cap: 23200, rate: 0.10 },
    { cap: 94300, rate: 0.12 },
    { cap: 201050, rate: 0.22 },
    { cap: 383900, rate: 0.24 },
    { cap: 487450, rate: 0.32 },
    { cap: 731200, rate: 0.35 },
    { cap: Infinity, rate: 0.37 },
  ];

  const brackets = isMarried ? bracketsMarried : bracketsSingle;
  let tax = 0;
  let prevCap = 0;

  for (const b of brackets) {
    if (taxableIncome > prevCap) {
      const taxableInBracket = Math.min(taxableIncome - prevCap, b.cap - prevCap);
      tax += taxableInBracket * b.rate;
      prevCap = b.cap;
    } else {
      break;
    }
  }

  return tax;
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}
