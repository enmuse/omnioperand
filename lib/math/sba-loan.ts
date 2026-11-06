/**
 * lib/math/sba-loan.ts
 * OmniOperand SBA 7(a) & SBA 504 Commercial Loan Underwriting Engine
 *
 * Implements standard U.S. Small Business Administration (SBA) criteria:
 * - SBA 7(a): Variable rate (Prime + spread), guaranty fees (up to 3.75%), monthly amortization
 * - SBA 504: 50/40/10 split (Senior Bank 50%, CDC Debenture 40%, Borrower Equity 10%)
 * - Blended interest rate, monthly debt service, and minimum DSCR required (1.15x - 1.25x)
 */

export interface SbaLoanInputs {
  loanProgram: '7a' | '504';
  totalProjectCost: number;
  downPaymentPct?: number; // e.g., 10 for 10%
  primeRatePct?: number; // e.g., 8.5 for 8.5%
  lenderSpreadPct?: number; // e.g., 2.75% for 7(a)
  loanTermYears?: number; // 10 years (working cap/equip) or 25 years (real estate)
  annualNetOperatingIncome?: number; // for DSCR sizing
  cdcRatePct?: number; // for 504 debenture (typically lower fixed rate ~6.5%)
}

export interface SbaLoanOutputs {
  loanProgram: '7a' | '504';
  totalProjectCost: number;
  downPaymentAmount: number;
  financedAmount: number;
  sbaGuaranteeFee: number;
  effectiveInterestRatePct: number;
  monthlyPrincipalAndInterest: number;
  annualDebtService: number;
  dscr: number;
  isDscrApproved: boolean; // DSCR >= 1.15
  tierLabel: string;
  splitDetails?: {
    seniorBankAmount: number;
    seniorBankMonthlyPI: number;
    cdcDebentureAmount: number;
    cdcDebentureMonthlyPI: number;
  };
}

export function calculateSbaLoan(inputs: SbaLoanInputs): SbaLoanOutputs {
  const cost = Math.max(0, inputs.totalProjectCost || 0);
  const downPct = Math.max(0, Math.min(100, inputs.downPaymentPct ?? 10)) / 100;
  const downPaymentAmount = cost * downPct;
  const financedAmount = Math.max(0, cost - downPaymentAmount);
  const termYears = Math.max(1, Math.min(30, inputs.loanTermYears ?? 25));
  const n = termYears * 12;
  const noi = Math.max(0, inputs.annualNetOperatingIncome || 0);

  let guaranteeFee = 0;
  let effectiveRatePct = 0;
  let monthlyPI = 0;
  let splitDetails: SbaLoanOutputs['splitDetails'];

  if (inputs.loanProgram === '7a') {
    const prime = Math.max(0, inputs.primeRatePct ?? 8.5);
    const spread = Math.max(0, inputs.lenderSpreadPct ?? 2.75);
    effectiveRatePct = prime + spread;
    const r = effectiveRatePct / 100 / 12;

    // SBA 7(a) Guaranty Fee Tiers
    if (financedAmount <= 150000) {
      guaranteeFee = financedAmount * 0.0;
    } else if (financedAmount <= 700000) {
      guaranteeFee = financedAmount * 0.0277;
    } else if (financedAmount <= 1000000) {
      guaranteeFee = financedAmount * 0.0327;
    } else {
      guaranteeFee = financedAmount * 0.0375;
    }

    if (financedAmount > 0) {
      if (r === 0) {
        monthlyPI = financedAmount / n;
      } else {
        const factor = Math.pow(1 + r, n);
        monthlyPI = financedAmount * ((r * factor) / (factor - 1));
      }
    }
  } else {
    // SBA 504: 50% Senior Bank, 40% CDC, 10% Borrower Equity
    const seniorBankAmount = cost * 0.50;
    const cdcDebentureAmount = cost * 0.40;
    const bankRate = Math.max(0, inputs.primeRatePct ?? 7.50) / 100 / 12;
    const cdcRate = Math.max(0, inputs.cdcRatePct ?? 6.25) / 100 / 12;

    const fBank = Math.pow(1 + bankRate, n);
    const bankMonthlyPI = seniorBankAmount * ((bankRate * fBank) / (fBank - 1));

    const fCdc = Math.pow(1 + cdcRate, n);
    const cdcMonthlyPI = cdcDebentureAmount * ((cdcRate * fCdc) / (fCdc - 1));

    monthlyPI = bankMonthlyPI + cdcMonthlyPI;
    const blendedRate = (seniorBankAmount * (inputs.primeRatePct ?? 7.50) + cdcDebentureAmount * (inputs.cdcRatePct ?? 6.25)) / financedAmount;
    effectiveRatePct = blendedRate;

    // CDC fee ~2.15% financed into debenture
    guaranteeFee = cdcDebentureAmount * 0.0215;

    splitDetails = {
      seniorBankAmount,
      seniorBankMonthlyPI: bankMonthlyPI,
      cdcDebentureAmount,
      cdcDebentureMonthlyPI: cdcMonthlyPI
    };
  }

  const annualDebtService = monthlyPI * 12;
  const dscr = annualDebtService > 0 ? (noi / annualDebtService) : 0;
  const isDscrApproved = dscr >= 1.15;

  let tierLabel = 'Sub-Standard (< 1.15x DSCR)';
  if (dscr >= 1.50) {
    tierLabel = 'Strong Coverage (1.50x+)';
  } else if (dscr >= 1.25) {
    tierLabel = 'Standard Bank Approval (1.25x+)';
  } else if (dscr >= 1.15) {
    tierLabel = 'Minimum SBA Eligible (1.15x–1.24x)';
  }

  return {
    loanProgram: inputs.loanProgram,
    totalProjectCost: cost,
    downPaymentAmount,
    financedAmount,
    sbaGuaranteeFee: guaranteeFee,
    effectiveInterestRatePct: effectiveRatePct,
    monthlyPrincipalAndInterest: monthlyPI,
    annualDebtService,
    dscr,
    isDscrApproved,
    tierLabel,
    splitDetails
  };
}
