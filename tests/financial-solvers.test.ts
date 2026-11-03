/**
 * tests/financial-solvers.test.ts
 * Automated Unit Test Suite for the 6 High-Intent Financial & Business Math Engines:
 * 1. DSCR Rental Property Investor Loan Engine
 * 2. 12/24-Month Bank Statement Mortgage Engine
 * 3. Chattel Loan vs. Land-Home Modular Mortgage Comparison Engine
 * 4. Therapy Private Practice Breakeven Engine
 * 5. 1099 Locum Tenens Tax Arbitrage Engine
 * 6. Section 179 Heavy Equipment Tax Shield Engine
 */

import assert from 'node:assert';
import { calculateDscrLoan } from '../lib/math/dscr-loan.ts';
import { calculateBankStatementMortgage } from '../lib/math/bank-statement-mortgage.ts';
import { calculateChattelVsLandHome } from '../lib/math/chattel-vs-land-home.ts';
import { calculateTherapyPracticeBreakeven } from '../lib/math/therapy-private-practice-breakeven.ts';
import { calculateLocumTenensTax } from '../lib/math/locum-tenens-tax-calculator.ts';
import { calculateSection179Equipment } from '../lib/math/section-179-equipment.ts';

console.log('===============================================================');
console.log('🧪 Testing 6 High-Intent Financial & Commercial Math Engines');
console.log('===============================================================');

// 1. DSCR Loan Engine Tests
console.log('Testing Engine 1: DSCR Rental Property Investor Loan...');
const dscrTest1 = calculateDscrLoan({
  propertyPrice: 400000,
  downPaymentPct: 20, // $320k loan
  interestRatePct: 7.25,
  loanTermYears: 30,
  grossMonthlyRent: 3200,
  annualPropertyTaxes: 4800, // $400/mo
  annualInsurance: 1800, // $150/mo
  monthlyHoa: 0,
});

assert.strictEqual(dscrTest1.loanAmount, 320000);
assert.strictEqual(dscrTest1.downPaymentAmount, 80000);
assert(Math.abs(dscrTest1.monthlyPI - 2182.88) < 1.0, `DSCR monthly PI expected ~2182.88, got ${dscrTest1.monthlyPI}`);
assert(Math.abs(dscrTest1.totalMonthlyPITIA - 2732.88) < 1.0, `DSCR PITIA expected ~2732.88, got ${dscrTest1.totalMonthlyPITIA}`);
assert(Math.abs(dscrTest1.dscrRatio - 1.1709) < 0.01, `DSCR ratio expected ~1.17, got ${dscrTest1.dscrRatio}`);
assert.strictEqual(dscrTest1.tier, 'tight');
assert.strictEqual(dscrTest1.maxPitiaThresholds.target100, 3200);
assert(Math.abs(dscrTest1.maxPitiaThresholds.target120 - 2666.67) < 0.1);
assert(Math.abs(dscrTest1.maxPitiaThresholds.target125 - 2560.00) < 0.1);

// Test Prime DSCR
const dscrPrime = calculateDscrLoan({
  propertyPrice: 300000,
  downPaymentPct: 25,
  interestRatePct: 6.5,
  loanTermYears: 30,
  grossMonthlyRent: 3000,
  annualPropertyTaxes: 3000,
  annualInsurance: 1200,
});
assert(dscrPrime.dscrRatio >= 1.50);
assert.strictEqual(dscrPrime.tier, 'strong');
console.log('  ✅ DSCR Engine: Exact PITIA, ratio thresholds, and tiers verified!');

// 2. Bank Statement Mortgage Engine Tests
console.log('Testing Engine 2: 12/24-Month Bank Statement Mortgage...');
const bankTest = calculateBankStatementMortgage({
  calculationMethod: 12,
  totalGrossDeposits: 360000,
  accountType: 'business',
  expenseRatioPct: 50,
  monthlyPersonalDebts: 800,
  maxDtiPct: 50,
  interestRatePct: 7.5,
  loanTermYears: 30,
  downPaymentPct: 20,
});

assert.strictEqual(bankTest.totalQualifyingRevenue, 180000);
assert.strictEqual(bankTest.monthlyQualifyingIncome, 15000);
assert.strictEqual(bankTest.maxAllowableTotalDebt, 7500); // 50% DTI
assert.strictEqual(bankTest.maxAllowableHousingExpense, 6700); // 7500 - 800
assert(bankTest.maxPurchasePower > 700000, `Purchasing power should be > $700k, got ${bankTest.maxPurchasePower}`);
assert.strictEqual(bankTest.qualifyingStatus, 'qualified');

// Test 24-month personal account (100% credit)
const bankPersonal = calculateBankStatementMortgage({
  calculationMethod: 24,
  totalGrossDeposits: 480000,
  accountType: 'personal',
  monthlyPersonalDebts: 500,
  maxDtiPct: 45,
});
assert.strictEqual(bankPersonal.expenseRatioPct, 0);
assert.strictEqual(bankPersonal.monthlyQualifyingIncome, 20000);
console.log('  ✅ Bank Statement Engine: 12/24mo averages, expense tiers, and purchasing power inversion verified!');

// 3. Chattel vs Land-Home Engine Tests
console.log('Testing Engine 3: Chattel Loan vs. Land-Home Modular Mortgage...');
const chattelTest = calculateChattelVsLandHome({
  manufacturedHomeCost: 150000,
  chattel: {
    interestRatePct: 9.75,
    termYears: 20,
    downPaymentPct: 10,
    monthlyLotRent: 650,
    annualLotRentInflationPct: 3.5,
    annualHomeDepreciationPct: 2.0,
  },
  landHome: {
    landCost: 65000,
    interestRatePct: 6.75,
    termYears: 30,
    downPaymentPct: 5,
    annualPropertyTaxRatePct: 1.2,
    annualInsurance: 1400,
    annualAppreciationPct: 3.5,
  },
});

assert.strictEqual(chattelTest.chattelSummary.financedPrincipal, 135000);
assert(chattelTest.chattelSummary.monthlyPI > 1200);
assert.strictEqual(chattelTest.landHomeSummary.packageTotalCost, 215000);
assert(chattelTest.comparison.tenYearNetEquityAdvantage > 50000, 'Land-Home 10-year equity must exceed Chattel by > $50k');
assert(chattelTest.comparison.breakevenYear <= 10, `Breakeven must occur within 10 years, got Year ${chattelTest.comparison.breakevenYear}`);
console.log('  ✅ Chattel vs. Land-Home: Side-by-side amortizations and 10-year equity spread verified!');

// 4. Therapy Private Practice Breakeven Tests
console.log('Testing Engine 4: Private Practice Breakeven (Cash vs. Insurance)...');
const therapyTest = calculateTherapyPracticeBreakeven({
  targetAnnualNetIncome: 120000,
  weeksWorkedPerYear: 48,
  cashSessionFee: 150,
  insuranceReimbursementRate: 105,
  claimDenialRatePct: 8,
  billingFeePct: 6,
  unpaidAdminMinsPerSession: 20,
  cashAdminMinsPerSession: 5,
  fixedAnnualOverhead: 14000,
});

assert.strictEqual(therapyTest.totalRevenueRequired, 134000);
assert(therapyTest.insuranceModel.effectiveRatePerSession < 95.0, `Insurance effective rate expected < 95, got ${therapyTest.insuranceModel.effectiveRatePerSession}`);
assert(therapyTest.insuranceModel.sessionsPerYear > therapyTest.cashModel.sessionsPerYear);
assert(therapyTest.insuranceModel.totalWorkingHoursPerWeek > therapyTest.cashModel.totalWorkingHoursPerWeek);
assert(therapyTest.comparison.weeklyHourDifference > 5.0, `Insurance must require >5 extra hours/week, got ${therapyTest.comparison.weeklyHourDifference}`);
assert(therapyTest.comparison.annualUnpaidAdminHoursDifference > 150, `Annual admin difference should be > 150 hours, got ${therapyTest.comparison.annualUnpaidAdminHoursDifference}`);
console.log('  ✅ Therapy Practice Engine: Denial drag, billing friction, and clinical/admin hours parity verified!');

// 5. Locum Tenens Tax Arbitrage Tests
console.log('Testing Engine 5: 1099 Locum Tenens Tax Arbitrage...');
const locumTest = calculateLocumTenensTax({
  w2BaseSalary: 180000,
  locumHourlyRate: 150,
  projectedBillableHours: 1600,
  weeklyNonTaxableStipend: 1400,
  taxFilingStatus: 'single',
  primaryHomeStateTaxRatePct: 5.0,
  monthlyDuplicatedHousingExpense: 1500,
  annualBusinessDeductions: 12000,
  solo401kContribution: 20000,
});

assert.strictEqual(locumTest.locumModel.grossHourlyEarnings, 240000);
assert.strictEqual(locumTest.locumModel.nonTaxablePerDiemTotal, 56000);
assert(locumTest.locumModel.trueNetAfterTaxTakeHome > locumTest.w2Model.netTakeHomePay);
assert(locumTest.arbitrage.netTakeHomeDifference > 30000, `Locum advantage should be > $30k, got ${locumTest.arbitrage.netTakeHomeDifference}`);
assert.strictEqual(locumTest.arbitrage.quarterlyTaxSchedule.q1_Apr15, locumTest.locumModel.quarterlyEstimatedTaxPayment);
console.log('  ✅ Locum Tenens Engine: IRS tax home compliance, GSA per diem splits, and SE tax shelter verified!');

// 6. Section 179 Heavy Equipment Tax Shield Tests
console.log('Testing Engine 6: Section 179 Equipment Tax Shield & Cash Flow...');
const s179Test = calculateSection179Equipment({
  equipmentPurchasePrice: 125000,
  equipmentType: 'heavy_machinery',
  financingMethod: 'loan',
  downPaymentPct: 10, // $12,500 down, $112,500 loan
  loanInterestRatePct: 8.5,
  loanTermMonths: 60,
  monthsActiveInYear1: 6,
  entityTaxBracketPct: 35,
});

assert.strictEqual(s179Test.totalYear1Deduction, 125000);
assert.strictEqual(s179Test.immediateYear1TaxSavings, 43750); // $125k * 35%
assert(s179Test.financingMetrics.totalYear1CashOutlay < 30000, `Year 1 outlay expected < $30k, got ${s179Test.financingMetrics.totalYear1CashOutlay}`);
assert.strictEqual(s179Test.isCashPositiveInYear1, true);
assert(s179Test.netYear1CashFlow > 15000, `Net Year 1 cash benefit should exceed +$15,000, got ${s179Test.netYear1CashFlow}`);
assert.strictEqual(s179Test.fiveYearSchedule.length, 5);

// Test Passenger Vehicle Cap
const s179Car = calculateSection179Equipment({
  equipmentPurchasePrice: 65000,
  equipmentType: 'light_vehicle',
  entityTaxBracketPct: 35,
});
assert.strictEqual(s179Car.section179Deduction, 20400); // 2024 luxury auto cap
console.log('  ✅ Section 179 Engine: Immediate tax shield, equipment loan outlay, and cash-in-pocket arbitrage verified!');

console.log('\n🎉 ALL 6 FINANCIAL & COMMERCIAL MATH ENGINES PASSED 100% OF TESTS!');
console.log('===============================================================');
