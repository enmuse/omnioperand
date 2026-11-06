/**
 * lib/math/commercial-real-estate-cap-rate.ts
 * OmniOperand Commercial Real Estate Cap Rate, NOI & Debt Yield Underwriting Engine
 *
 * Implements institutional commercial mortgage and equity syndication metrics:
 * - Gross Potential Rent (GPR) and Effective Gross Income (EGI)
 * - Net Operating Income (NOI) after operating expenses (OpEx)
 * - Capitalization Rate (Cap Rate) and valuation inversions
 * - Wholesale Debt Yield (NOI / Loan Amount) with standard 9.50% threshold
 * - Debt Service Coverage Ratio (DSCR) and Cash-on-Cash Return
 */

export interface CreCapRateInputs {
  purchasePrice: number;
  grossPotentialRentAnnual: number;
  otherIncomeAnnual?: number;
  vacancyLossPct?: number; // e.g., 5 for 5%
  operatingExpensesAnnual: number; // taxes, insurance, repairs, mgmt, reserves
  loanToValuePct?: number; // e.g., 70 for 70% LTV
  loanInterestRatePct?: number; // e.g., 6.75 for 6.75%
  amortizationYears?: number; // e.g., 25 or 30 years
}

export interface CreCapRateOutputs {
  purchasePrice: number;
  effectiveGrossIncome: number;
  netOperatingIncome: number;
  operatingExpenseRatioPct: number;
  capRatePct: number;
  loanAmount: number;
  equityRequired: number;
  annualDebtService: number;
  monthlyDebtService: number;
  debtYieldPct: number;
  dscr: number;
  netCashFlowAfterDebt: number;
  cashOnCashReturnPct: number;
  isDebtYieldAcceptable: boolean; // >= 9.5%
  isDscrAcceptable: boolean; // >= 1.25x
}

export function calculateCreCapRate(inputs: CreCapRateInputs): CreCapRateOutputs {
  const price = Math.max(0, inputs.purchasePrice || 0);
  const gpr = Math.max(0, inputs.grossPotentialRentAnnual || 0);
  const otherInc = Math.max(0, inputs.otherIncomeAnnual || 0);
  const vacancyRate = Math.max(0, Math.min(100, inputs.vacancyLossPct ?? 5)) / 100;

  const vacancyLoss = gpr * vacancyRate;
  const effectiveGrossIncome = gpr - vacancyLoss + otherInc;

  const opex = Math.max(0, inputs.operatingExpensesAnnual || 0);
  const netOperatingIncome = Math.max(0, effectiveGrossIncome - opex);

  const opexRatioPct = effectiveGrossIncome > 0 ? (opex / effectiveGrossIncome) * 100 : 0;
  const capRatePct = price > 0 ? (netOperatingIncome / price) * 100 : 0;

  const ltvPct = Math.max(0, Math.min(100, inputs.loanToValuePct ?? 70)) / 100;
  const loanAmount = price * ltvPct;
  const equityRequired = Math.max(0, price - loanAmount);

  const rate = Math.max(0, inputs.loanInterestRatePct ?? 6.75) / 100;
  const termYears = Math.max(1, inputs.amortizationYears ?? 25);
  const n = termYears * 12;
  const r = rate / 12;

  let monthlyDebtService = 0;
  if (loanAmount > 0) {
    if (r === 0) {
      monthlyDebtService = loanAmount / n;
    } else {
      const f = Math.pow(1 + r, n);
      monthlyDebtService = loanAmount * ((r * f) / (f - 1));
    }
  }

  const annualDebtService = monthlyDebtService * 12;
  const debtYieldPct = loanAmount > 0 ? (netOperatingIncome / loanAmount) * 100 : 0;
  const dscr = annualDebtService > 0 ? (netOperatingIncome / annualDebtService) : 0;

  const netCashFlowAfterDebt = netOperatingIncome - annualDebtService;
  const cashOnCashReturnPct = equityRequired > 0 ? (netCashFlowAfterDebt / equityRequired) * 100 : 0;

  return {
    purchasePrice: price,
    effectiveGrossIncome,
    netOperatingIncome,
    operatingExpenseRatioPct: opexRatioPct,
    capRatePct,
    loanAmount,
    equityRequired,
    annualDebtService,
    monthlyDebtService,
    debtYieldPct,
    dscr,
    netCashFlowAfterDebt,
    cashOnCashReturnPct,
    isDebtYieldAcceptable: debtYieldPct >= 9.5,
    isDscrAcceptable: dscr >= 1.25
  };
}
