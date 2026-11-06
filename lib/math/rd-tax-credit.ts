/**
 * lib/math/rd-tax-credit.ts
 * OmniOperand Federal R&D Tax Credit (IRC Section 41) Estimator
 *
 * Implements Treasury Regulation §1.41 Alternative Simplified Credit (ASC) standards:
 * - Qualified Research Expenses (QRE): 100% W-2 wages, 65% US contractor costs, 100% cloud/supplies
 * - 3-Year historical average base amount calculation
 * - 14% ASC rate on incremental QRE (or 6% flat rate for new startups with no history)
 * - Section 41(h) Qualified Small Business (QSB) payroll tax offset election (up to $500,000)
 */

export interface RdTaxCreditInputs {
  w2EmployeeWages: number;
  usContractorExpenses: number; // 65% statutory qualification rule
  cloudSuppliesExpenses: number;
  priorYear1Qre?: number;
  priorYear2Qre?: number;
  priorYear3Qre?: number;
  isQualifiedSmallBusiness?: boolean; // gross receipts < $5M and under 5 years old
}

export interface RdTaxCreditOutputs {
  qualifiedWages: number;
  qualifiedContractors: number; // 65% of raw expenses
  qualifiedSupplies: number;
  totalCurrentQre: number;
  priorThreeYearAverageQre: number;
  baseAmountAsc: number; // 50% of 3-year average
  incrementalQre: number;
  federalCreditAmount: number;
  effectiveCreditRatePct: number;
  maxPayrollTaxOffsetEligible: number; // up to $500,000 for QSB
  isPayrollOffsetAllowed: boolean;
}

export function calculateRdTaxCredit(inputs: RdTaxCreditInputs): RdTaxCreditOutputs {
  const wages = Math.max(0, inputs.w2EmployeeWages || 0);
  const contractorsRaw = Math.max(0, inputs.usContractorExpenses || 0);
  const qualifiedContractors = contractorsRaw * 0.65; // IRC §41(b)(3) 65% rule
  const supplies = Math.max(0, inputs.cloudSuppliesExpenses || 0);

  const totalCurrentQre = wages + qualifiedContractors + supplies;

  const y1 = Math.max(0, inputs.priorYear1Qre || 0);
  const y2 = Math.max(0, inputs.priorYear2Qre || 0);
  const y3 = Math.max(0, inputs.priorYear3Qre || 0);

  const hasHistory = y1 > 0 || y2 > 0 || y3 > 0;
  const priorThreeYearAverageQre = hasHistory ? (y1 + y2 + y3) / 3 : 0;
  const baseAmountAsc = priorThreeYearAverageQre * 0.50;

  let federalCreditAmount = 0;
  if (hasHistory) {
    const incrementalQre = Math.max(0, totalCurrentQre - baseAmountAsc);
    federalCreditAmount = incrementalQre * 0.14; // 14% ASC rate
  } else {
    // 6% flat credit if no prior 3 years of QRE
    federalCreditAmount = totalCurrentQre * 0.06;
  }

  const effectiveCreditRatePct = totalCurrentQre > 0 ? (federalCreditAmount / totalCurrentQre) * 100 : 0;
  const isQsb = inputs.isQualifiedSmallBusiness ?? true;
  const maxPayrollTaxOffsetEligible = isQsb ? Math.min(500000, federalCreditAmount) : 0;

  return {
    qualifiedWages: wages,
    qualifiedContractors,
    qualifiedSupplies: supplies,
    totalCurrentQre,
    priorThreeYearAverageQre,
    baseAmountAsc,
    incrementalQre: Math.max(0, totalCurrentQre - baseAmountAsc),
    federalCreditAmount,
    effectiveCreditRatePct,
    maxPayrollTaxOffsetEligible,
    isPayrollOffsetAllowed: isQsb
  };
}

