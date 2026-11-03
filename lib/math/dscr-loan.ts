/**
 * lib/math/dscr-loan.ts
 * OmniOperand High-Precision DSCR Rental Property Investor Loan Engine
 *
 * Implements Non-QM Investor Underwriting Criteria:
 * - Debt Service Coverage Ratio: DSCR = Gross Monthly Rent / Total Monthly PITIA
 * - Exact Amortization & PITIA Escrow Sizing
 * - Maximum allowable PITIA threshold inversions for target DSCR benchmarks (1.00x, 1.20x, 1.25x)
 */

export interface DscrLoanInputs {
  propertyPrice: number;
  downPaymentPct: number; // e.g., 20 for 20%
  interestRatePct: number; // e.g., 7.25 for 7.25%
  loanTermYears: number; // e.g., 30
  grossMonthlyRent: number;
  annualPropertyTaxes: number;
  annualInsurance: number;
  monthlyHoa?: number;
}

export type DscrTier = 'deficit' | 'tight' | 'standard' | 'strong';

export interface DscrLoanOutputs {
  downPaymentAmount: number;
  loanAmount: number;
  monthlyPI: number;
  monthlyTaxes: number;
  monthlyInsurance: number;
  monthlyHoa: number;
  totalMonthlyPITIA: number;
  dscrRatio: number;
  monthlyCashFlow: number;
  annualCashFlow: number;
  maxPitiaThresholds: {
    target100: number; // Max PITIA for DSCR = 1.00x
    target120: number; // Max PITIA for DSCR = 1.20x
    target125: number; // Max PITIA for DSCR = 1.25x
  };
  tier: DscrTier;
  tierLabel: string;
  tierColor: string;
  isQualifiedStandard: boolean; // DSCR >= 1.20
  isQualifiedPrime: boolean; // DSCR >= 1.25
}

export function calculateDscrLoan(inputs: DscrLoanInputs): DscrLoanOutputs {
  const price = Math.max(0, inputs.propertyPrice || 0);
  const downPct = Math.max(0, Math.min(100, inputs.downPaymentPct ?? 20)) / 100;
  const ratePct = Math.max(0, inputs.interestRatePct ?? 7.25) / 100;
  const termYears = Math.max(1, Math.min(50, inputs.loanTermYears ?? 30));
  const rent = Math.max(0, inputs.grossMonthlyRent || 0);
  const taxes = Math.max(0, inputs.annualPropertyTaxes || 0);
  const insurance = Math.max(0, inputs.annualInsurance || 0);
  const hoa = Math.max(0, inputs.monthlyHoa || 0);

  const downPaymentAmount = price * downPct;
  const loanAmount = Math.max(0, price - downPaymentAmount);

  const n = termYears * 12;
  const r = ratePct / 12;

  let monthlyPI = 0;
  if (loanAmount > 0) {
    if (r === 0) {
      monthlyPI = loanAmount / n;
    } else {
      const factor = Math.pow(1 + r, n);
      monthlyPI = loanAmount * ((r * factor) / (factor - 1));
    }
  }

  const monthlyTaxes = taxes / 12;
  const monthlyInsurance = insurance / 12;
  const totalMonthlyPITIA = monthlyPI + monthlyTaxes + monthlyInsurance + hoa;

  const dscrRatio = totalMonthlyPITIA > 0 ? rent / totalMonthlyPITIA : 0;
  const monthlyCashFlow = rent - totalMonthlyPITIA;
  const annualCashFlow = monthlyCashFlow * 12;

  let tier: DscrTier = 'deficit';
  let tierLabel = 'Deficit / Negative Cash Flow (< 1.00x)';
  let tierColor = '#ef4444'; // Red

  if (dscrRatio >= 1.50) {
    tier = 'strong';
    tierLabel = 'Strong Prime DSCR (1.50x+)';
    tierColor = '#059669'; // Emerald
  } else if (dscrRatio >= 1.20) {
    tier = 'standard';
    tierLabel = 'Standard Qualified (1.20x–1.49x)';
    tierColor = '#10b981'; // Green
  } else if (dscrRatio >= 1.00) {
    tier = 'tight';
    tierLabel = 'Tight Coverage (1.00x–1.19x)';
    tierColor = '#f59e0b'; // Amber
  }

  const maxPitiaThresholds = {
    target100: rent > 0 ? rent / 1.0 : 0,
    target120: rent > 0 ? rent / 1.2 : 0,
    target125: rent > 0 ? rent / 1.25 : 0,
  };

  return {
    downPaymentAmount: round2(downPaymentAmount),
    loanAmount: round2(loanAmount),
    monthlyPI: round2(monthlyPI),
    monthlyTaxes: round2(monthlyTaxes),
    monthlyInsurance: round2(monthlyInsurance),
    monthlyHoa: round2(hoa),
    totalMonthlyPITIA: round2(totalMonthlyPITIA),
    dscrRatio: round4(dscrRatio),
    monthlyCashFlow: round2(monthlyCashFlow),
    annualCashFlow: round2(annualCashFlow),
    maxPitiaThresholds: {
      target100: round2(maxPitiaThresholds.target100),
      target120: round2(maxPitiaThresholds.target120),
      target125: round2(maxPitiaThresholds.target125),
    },
    tier,
    tierLabel,
    tierColor,
    isQualifiedStandard: dscrRatio >= 1.20,
    isQualifiedPrime: dscrRatio >= 1.25,
  };
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}

function round4(val: number): number {
  return Math.round(val * 10000) / 10000;
}
