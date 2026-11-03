/**
 * lib/math/bank-statement-mortgage.ts
 * OmniOperand 12/24-Month Bank Statement Loan Engine for 1099 & Self-Employed Borrowers
 *
 * Implements Non-QM Underwriting Criteria:
 * - 12-Month vs. 24-Month Qualifying Bank Deposit Analysis
 * - Standard 50% Expense Ratio vs. CPA Attestation Letter vs. 100% Personal Account Credit
 * - Residual Income & Max Allowable Debt-to-Income (DTI: 45%–50%) Thresholds
 * - Algebraic Inversion of Maximum Purchasing Power from Allowable Front/Back-End Ratios
 */

export interface BankStatementInputs {
  calculationMethod: 12 | 24; // 12 or 24 months
  totalGrossDeposits: number;
  accountType: 'business' | 'personal';
  expenseRatioPct?: number; // e.g. 50% default for business, 0% for personal
  monthlyPersonalDebts: number; // Car loans, student debt, credit cards
  maxDtiPct?: number; // Default 50% Non-QM ceiling
  interestRatePct?: number; // e.g. 7.5%
  loanTermYears?: number; // e.g. 30
  downPaymentPct?: number; // e.g. 20%
  annualTaxInsuranceRatePct?: number; // e.g. 1.5% of purchase price
}

export interface BankStatementOutputs {
  calculationPeriodMonths: number;
  totalGrossDeposits: number;
  expenseRatioPct: number;
  totalQualifyingRevenue: number;
  monthlyQualifyingIncome: number;
  benchmarkTaxReturnIncome: number; // Estimated typical taxable net income after write-offs
  incomeAdvantageRatio: number; // Factor by which qualifying income exceeds tax return net
  maxAllowableTotalDebt: number; // Monthly income * Max DTI
  monthlyPersonalDebts: number;
  maxAllowableHousingExpense: number; // PITIA allowance
  maxPurchasePower: number; // Backsolved maximum home purchase price
  maxLoanAmount: number;
  requiredDownPayment: number;
  estimatedMonthlyPI: number;
  estimatedMonthlyTaxesAndInsurance: number;
  actualDti: number;
  qualifyingStatus: 'qualified' | 'constrained' | 'disqualified';
  qualifyingStatusMessage: string;
}

export function calculateBankStatementMortgage(inputs: BankStatementInputs): BankStatementOutputs {
  const months = inputs.calculationMethod === 24 ? 24 : 12;
  const deposits = Math.max(0, inputs.totalGrossDeposits || 0);
  const isPersonal = inputs.accountType === 'personal';

  // Default expense ratio: 0% for personal account (100% deposits qualify), 50% for business
  let expensePct = inputs.expenseRatioPct !== undefined
    ? Math.max(0, Math.min(100, inputs.expenseRatioPct))
    : (isPersonal ? 0 : 50);

  const monthlyDebts = Math.max(0, inputs.monthlyPersonalDebts || 0);
  const maxDtiPct = Math.max(10, Math.min(60, inputs.maxDtiPct ?? 50));
  const ratePct = Math.max(0, inputs.interestRatePct ?? 7.5) / 100;
  const termYears = Math.max(1, Math.min(40, inputs.loanTermYears ?? 30));
  const downPct = Math.max(0, Math.min(90, inputs.downPaymentPct ?? 20)) / 100;
  const taxInsRatePct = Math.max(0, inputs.annualTaxInsuranceRatePct ?? 1.5) / 100;

  const totalQualifyingRevenue = deposits * (1 - expensePct / 100);
  const monthlyQualifyingIncome = totalQualifyingRevenue / months;

  // Typical self-employed borrowers write down net income to ~30-40% of revenue on tax returns
  const benchmarkTaxReturnIncome = monthlyQualifyingIncome * 0.38;
  const incomeAdvantageRatio = benchmarkTaxReturnIncome > 0
    ? monthlyQualifyingIncome / benchmarkTaxReturnIncome
    : 1;

  const maxAllowableTotalDebt = monthlyQualifyingIncome * (maxDtiPct / 100);
  const maxAllowableHousingExpense = Math.max(0, maxAllowableTotalDebt - monthlyDebts);

  // Backsolve Maximum Purchase Price from allowable housing expense (PITIA)
  const r = ratePct / 12;
  const n = termYears * 12;
  const m1 = r > 0 ? (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) : (1 / n);
  const e1 = taxInsRatePct / 12; // Monthly escrow per dollar of price

  // Housing expense per dollar of purchase price: (1 - downPct)*m1 + e1
  const kPrice = (1 - downPct) * m1 + e1;

  let maxPurchasePower = 0;
  let maxLoanAmount = 0;
  let requiredDownPayment = 0;
  let estimatedMonthlyPI = 0;
  let estimatedMonthlyTaxesAndInsurance = 0;

  if (kPrice > 0 && maxAllowableHousingExpense > 0) {
    maxPurchasePower = maxAllowableHousingExpense / kPrice;
    maxLoanAmount = maxPurchasePower * (1 - downPct);
    requiredDownPayment = maxPurchasePower * downPct;
    estimatedMonthlyPI = maxLoanAmount * m1;
    estimatedMonthlyTaxesAndInsurance = maxPurchasePower * e1;
  }

  let qualifyingStatus: 'qualified' | 'constrained' | 'disqualified' = 'qualified';
  let qualifyingStatusMessage = 'Fully Qualified for Wholesale Non-QM Bank Statement Program';

  if (monthlyQualifyingIncome <= 0 || maxAllowableHousingExpense <= 0) {
    qualifyingStatus = 'disqualified';
    qualifyingStatusMessage = 'Disqualified: Existing monthly personal debts exceed maximum allowable DTI ceiling';
  } else if (monthlyDebts / (monthlyQualifyingIncome || 1) > 0.35) {
    qualifyingStatus = 'constrained';
    qualifyingStatusMessage = 'Constrained: Personal debt obligations restrict maximum purchasing power';
  }

  return {
    calculationPeriodMonths: months,
    totalGrossDeposits: round2(deposits),
    expenseRatioPct: round2(expensePct),
    totalQualifyingRevenue: round2(totalQualifyingRevenue),
    monthlyQualifyingIncome: round2(monthlyQualifyingIncome),
    benchmarkTaxReturnIncome: round2(benchmarkTaxReturnIncome),
    incomeAdvantageRatio: round2(incomeAdvantageRatio),
    maxAllowableTotalDebt: round2(maxAllowableTotalDebt),
    monthlyPersonalDebts: round2(monthlyDebts),
    maxAllowableHousingExpense: round2(maxAllowableHousingExpense),
    maxPurchasePower: round2(maxPurchasePower),
    maxLoanAmount: round2(maxLoanAmount),
    requiredDownPayment: round2(requiredDownPayment),
    estimatedMonthlyPI: round2(estimatedMonthlyPI),
    estimatedMonthlyTaxesAndInsurance: round2(estimatedMonthlyTaxesAndInsurance),
    actualDti: round2(maxDtiPct),
    qualifyingStatus,
    qualifyingStatusMessage,
  };
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}
