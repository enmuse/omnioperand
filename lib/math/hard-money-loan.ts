/**
 * lib/math/hard-money-loan.ts
 * OmniOperand Hard Money & Fix-and-Flip Bridge Loan Underwriting Engine
 *
 * Implements private lending underwriting standards:
 * - 70% ARV Maximum Allowable Offer (MAO) benchmark
 * - Dual underwriting caps: Loan-to-Cost (LTC up to 90%) vs. Loan-to-ARV (LTARV up to 75%)
 * - Origination points, monthly interest-only debt service, and holding costs
 * - Net investor flip profit and annualized cash-on-cash ROI
 */

export interface HardMoneyInputs {
  purchasePrice: number;
  rehabBudget: number;
  afterRepairValue: number;
  maxLtcPct?: number; // e.g., 90 for 90% of purchase + 100% rehab, or 85% total
  maxLtarvPct?: number; // e.g., 75 for 75%
  interestRatePct?: number; // e.g., 11.5 for 11.5%
  originationPointsPct?: number; // e.g., 2 for 2 points
  holdingPeriodMonths?: number; // e.g., 6 months
  sellingCostsPct?: number; // e.g., 6 for 6% of ARV
  otherMonthlyHoldingCosts?: number; // utilities, taxes, insurance e.g., $400/mo
}

export interface HardMoneyOutputs {
  afterRepairValue: number;
  seventyPercentMao: number; // ARV * 0.70 - Rehab
  totalProjectCost: number; // Purchase + Rehab
  loanAmount: number; // lesser of LTC cap and LTARV cap
  borrowerEquityRequired: number; // Total Project Cost - Loan Amount
  originationPointsAmount: number;
  monthlyInterestPayment: number;
  totalInterestPaid: number;
  totalHoldingCosts: number;
  sellingCosts: number;
  totalCapitalInvested: number;
  netFlipProfit: number;
  returnOnInvestmentPct: number;
  annualizedRoiPct: number;
  is70RuleMet: boolean;
}

export function calculateHardMoney(inputs: HardMoneyInputs): HardMoneyOutputs {
  const purchase = Math.max(0, inputs.purchasePrice || 0);
  const rehab = Math.max(0, inputs.rehabBudget || 0);
  const arv = Math.max(0, inputs.afterRepairValue || 0);
  const totalProjectCost = purchase + rehab;

  // 70% rule
  const seventyPercentMao = Math.max(0, (arv * 0.70) - rehab);
  const is70RuleMet = purchase <= seventyPercentMao;

  const ltcPct = Math.max(0, Math.min(100, inputs.maxLtcPct ?? 85)) / 100;
  const ltarvPct = Math.max(0, Math.min(100, inputs.maxLtarvPct ?? 75)) / 100;

  const maxLtcLoan = totalProjectCost * ltcPct;
  const maxLtarvLoan = arv * ltarvPct;
  const loanAmount = Math.min(maxLtcLoan, maxLtarvLoan);

  const borrowerEquityRequired = Math.max(0, totalProjectCost - loanAmount);

  const pointsPct = Math.max(0, inputs.originationPointsPct ?? 2) / 100;
  const originationPointsAmount = loanAmount * pointsPct;

  const rate = Math.max(0, inputs.interestRatePct ?? 11.5) / 100;
  const monthlyRate = rate / 12;
  const monthlyInterestPayment = loanAmount * monthlyRate;

  const months = Math.max(1, inputs.holdingPeriodMonths ?? 6);
  const totalInterestPaid = monthlyInterestPayment * months;

  const otherHolding = Math.max(0, inputs.otherMonthlyHoldingCosts ?? 400) * months;
  const totalHoldingCosts = totalInterestPaid + otherHolding;

  const sellingPct = Math.max(0, inputs.sellingCostsPct ?? 6) / 100;
  const sellingCosts = arv * sellingPct;

  const totalCapitalInvested = borrowerEquityRequired + originationPointsAmount + totalHoldingCosts;
  const totalExpenses = totalProjectCost + originationPointsAmount + totalHoldingCosts + sellingCosts;
  const netFlipProfit = arv - totalExpenses;

  const roiPct = totalCapitalInvested > 0 ? (netFlipProfit / totalCapitalInvested) * 100 : 0;
  const annualizedRoiPct = roiPct * (12 / months);

  return {
    afterRepairValue: arv,
    seventyPercentMao,
    totalProjectCost,
    loanAmount,
    borrowerEquityRequired,
    originationPointsAmount,
    monthlyInterestPayment,
    totalInterestPaid,
    totalHoldingCosts,
    sellingCosts,
    totalCapitalInvested,
    netFlipProfit,
    returnOnInvestmentPct: roiPct,
    annualizedRoiPct,
    is70RuleMet
  };
}
