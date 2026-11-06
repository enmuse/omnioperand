/**
 * lib/math/structured-settlement-lump-sum.ts
 * OmniOperand Structured Settlement & Annuity Lump-Sum Factoring Engine
 *
 * Implements IRC §5891 and State Structured Settlement Protection Act standards:
 * - Court-approved discounting of guaranteed periodic payments
 * - Present Value (NPV) using market factoring discount rates (9% - 18%)
 * - Cost of immediate liquidity vs. holding guaranteed tax-free annuity cash flows
 */

export interface StructuredSettlementInputs {
  monthlyPayment: number;
  remainingYears: number; // e.g., 10 years
  annualColaPct?: number; // Cost of Living Adjustment, e.g., 0% or 3%
  factoringDiscountRatePct?: number; // e.g., 12 for 12%
  administrativeFee?: number; // e.g., $2,500
}

export interface StructuredSettlementOutputs {
  totalPaymentsCount: number;
  nominalTotalFutureValue: number;
  grossPresentValue: number;
  netCashLumpSumOffer: number;
  dollarDiscountSurrendered: number;
  effectivePayoutPercentage: number; // Cash received / Nominal total
  breakEvenReinvestmentRatePct: number;
}

export function calculateStructuredSettlement(inputs: StructuredSettlementInputs): StructuredSettlementOutputs {
  const pmt = Math.max(0, inputs.monthlyPayment || 0);
  const years = Math.max(0.5, Math.min(40, inputs.remainingYears || 10));
  const totalMonths = Math.round(years * 12);

  const colaPct = Math.max(0, inputs.annualColaPct ?? 0) / 100;
  const discountRate = Math.max(0.01, (inputs.factoringDiscountRatePct ?? 12) / 100);
  const monthlyDiscount = discountRate / 12;
  const adminFee = Math.max(0, inputs.administrativeFee ?? 2500);

  let nominalTotal = 0;
  let grossPresentValue = 0;

  for (let m = 1; m <= totalMonths; m++) {
    const yearIndex = Math.floor((m - 1) / 12);
    const adjustedPmt = pmt * Math.pow(1 + colaPct, yearIndex);
    nominalTotal += adjustedPmt;

    // Discount to present
    const pv = adjustedPmt / Math.pow(1 + monthlyDiscount, m);
    grossPresentValue += pv;
  }

  const netCashLumpSumOffer = Math.max(0, grossPresentValue - adminFee);
  const dollarDiscountSurrendered = Math.max(0, nominalTotal - netCashLumpSumOffer);
  const effectivePayoutPercentage = nominalTotal > 0 ? (netCashLumpSumOffer / nominalTotal) * 100 : 0;

  return {
    totalPaymentsCount: totalMonths,
    nominalTotalFutureValue: nominalTotal,
    grossPresentValue,
    netCashLumpSumOffer,
    dollarDiscountSurrendered,
    effectivePayoutPercentage,
    breakEvenReinvestmentRatePct: inputs.factoringDiscountRatePct ?? 12
  };
}

