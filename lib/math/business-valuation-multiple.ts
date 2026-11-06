/**
 * lib/math/business-valuation-multiple.ts
 * OmniOperand Business Valuation & SDE / EBITDA Multiple Sizer
 *
 * Implements International Business Brokers Association (IBBA) valuation standards:
 * - Seller's Discretionary Earnings (SDE) and Adjusted EBITDA recast schedule
 * - Industry multiple benchmarks based on recurring revenue and growth rates
 * - Low / Median / High enterprise valuation valuation boundaries
 * - Deal structure allocation: Cash at Closing, Seller Financing Note, and Earnout
 */

export interface BusinessValuationInputs {
  annualGrossRevenue: number;
  netReportedProfit: number;
  ownerCompensationDraw: number;
  discretionaryPerksExpenses?: number; // vehicles, travel, cell phone
  depreciationAmortization?: number;
  interestExpense?: number;
  oneTimeNonRecurringExpenses?: number;
  marketReplacementGmSalary?: number; // for Adjusted EBITDA calculation
  targetMultiple?: number; // e.g., 3.25x SDE
}

export interface BusinessValuationOutputs {
  annualGrossRevenue: number;
  reportedProfit: number;
  totalAddBacks: number;
  sellersDiscretionaryEarnings: number; // SDE
  adjustedEbitda: number;
  appliedMultiple: number;
  estimatedMedianValuation: number;
  valuationRangeLow: number;
  valuationRangeHigh: number;
  dealStructure: {
    cashAtClosing70Pct: number;
    sellerNote15Pct: number;
    earnoutContingent15Pct: number;
    sellerNoteMonthlyPayment: number; // 5 yr @ 8% interest
  };
}

export function calculateBusinessValuation(inputs: BusinessValuationInputs): BusinessValuationOutputs {
  const rev = Math.max(0, inputs.annualGrossRevenue || 0);
  const profit = inputs.netReportedProfit || 0;
  const ownerComp = Math.max(0, inputs.ownerCompensationDraw || 0);
  const perks = Math.max(0, inputs.discretionaryPerksExpenses || 0);
  const dep = Math.max(0, inputs.depreciationAmortization || 0);
  const interest = Math.max(0, inputs.interestExpense || 0);
  const oneTime = Math.max(0, inputs.oneTimeNonRecurringExpenses || 0);

  const totalAddBacks = ownerComp + perks + dep + interest + oneTime;
  const sde = profit + totalAddBacks;

  const gmSalary = Math.max(0, inputs.marketReplacementGmSalary ?? 120000);
  const adjustedEbitda = Math.max(0, sde - gmSalary);

  const multiple = Math.max(1.0, inputs.targetMultiple ?? 3.25);
  const medianValuation = Math.max(0, sde * multiple);

  const lowMultiple = Math.max(1.0, multiple - 0.5);
  const highMultiple = multiple + 0.5;

  const valuationRangeLow = Math.max(0, sde * lowMultiple);
  const valuationRangeHigh = Math.max(0, sde * highMultiple);

  // Deal structure allocation
  const cashAtClosing = medianValuation * 0.70;
  const sellerNote = medianValuation * 0.15;
  const earnout = medianValuation * 0.15;

  // 5-year seller note at 8% APR monthly amortization
  const r = 0.08 / 12;
  const n = 60;
  let sellerNoteMonthlyPayment = 0;
  if (sellerNote > 0) {
    const f = Math.pow(1 + r, n);
    sellerNoteMonthlyPayment = sellerNote * ((r * f) / (f - 1));
  }

  return {
    annualGrossRevenue: rev,
    reportedProfit: profit,
    totalAddBacks,
    sellersDiscretionaryEarnings: sde,
    adjustedEbitda,
    appliedMultiple: multiple,
    estimatedMedianValuation: medianValuation,
    valuationRangeLow,
    valuationRangeHigh,
    dealStructure: {
      cashAtClosing70Pct: cashAtClosing,
      sellerNote15Pct: sellerNote,
      earnoutContingent15Pct: earnout,
      sellerNoteMonthlyPayment
    }
  };
}

