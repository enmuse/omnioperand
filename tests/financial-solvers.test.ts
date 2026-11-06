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
import { calculateSbaLoan } from '../lib/math/sba-loan.ts';
import { calculate1031Exchange } from '../lib/math/1031-exchange.ts';
import { calculateCostSegregation } from '../lib/math/cost-segregation.ts';
import { calculateHardMoney } from '../lib/math/hard-money-loan.ts';
import { calculateCreCapRate } from '../lib/math/commercial-real-estate-cap-rate.ts';
import { calculateStructuredSettlement } from '../lib/math/structured-settlement-lump-sum.ts';
import { calculateCommercialSolar } from '../lib/math/commercial-solar-tax-credit.ts';
import { calculateRdTaxCredit } from '../lib/math/rd-tax-credit.ts';
import { calculatePersonalInjury } from '../lib/math/personal-injury-settlement.ts';
import { calculateBusinessValuation } from '../lib/math/business-valuation-multiple.ts';

console.log('===============================================================');
console.log('🧪 Testing 16 High-Intent Financial & Commercial Math Engines');
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

// 7. SBA 7(a) & 504 Loan Tests
console.log('Testing Engine 7: SBA 7(a) & 504 Commercial Loan...');
const sba7aTest = calculateSbaLoan({
  loanProgram: '7a',
  totalProjectCost: 1000000,
  downPaymentPct: 10,
  primeRatePct: 8.5,
  lenderSpreadPct: 2.75,
  loanTermYears: 25,
  annualNetOperatingIncome: 150000,
});
assert.strictEqual(sba7aTest.financedAmount, 900000);
assert.strictEqual(sba7aTest.effectiveInterestRatePct, 11.25);
assert(sba7aTest.monthlyPrincipalAndInterest > 8500 && sba7aTest.monthlyPrincipalAndInterest < 9500);
assert(sba7aTest.dscr > 1.30);
assert.strictEqual(sba7aTest.isDscrApproved, true);

const sba504Test = calculateSbaLoan({
  loanProgram: '504',
  totalProjectCost: 2000000,
  primeRatePct: 7.5,
  cdcRatePct: 6.25,
  loanTermYears: 25,
  annualNetOperatingIncome: 250000,
});
assert.strictEqual(sba504Test.splitDetails?.seniorBankAmount, 1000000);
assert.strictEqual(sba504Test.splitDetails?.cdcDebentureAmount, 800000);
assert(sba504Test.dscr >= 1.25);
console.log('  ✅ SBA Commercial Loan Engine: 7(a) variable spread, 504 debenture split, and DSCR verified!');

// 8. 1031 Exchange Like-Kind Tax Sizer Tests
console.log('Testing Engine 8: IRS §1031 Like-Kind Exchange & Boot Tax Sizer...');
const exchangeTest = calculate1031Exchange({
  relinquishedSalesPrice: 1500000,
  relinquishedClosingCostsPct: 6,
  originalPurchaseBasis: 600000,
  capitalImprovements: 100000,
  accumulatedDepreciation: 250000,
  relinquishedMortgagePayoff: 500000,
  replacementPurchasePrice: 1600000,
  replacementNewMortgage: 600000,
  cashReceivedOut: 0,
});
assert.strictEqual(exchangeTest.adjustedTaxBasis, 450000); // 600k + 100k - 250k
assert.strictEqual(exchangeTest.netSalesProceeds, 1410000); // 1.5M - 90k
assert.strictEqual(exchangeTest.realizedGain, 960000); // 1.41M - 450k
assert.strictEqual(exchangeTest.totalTaxableBoot, 0);
assert.strictEqual(exchangeTest.taxesDueCurrently, 0);
assert(exchangeTest.taxesDeferred1031 > 250000);
assert.strictEqual(exchangeTest.isFullExchange, true);
console.log('  ✅ 1031 Exchange Engine: Adjusted basis, realized gain, depreciation recapture, and boot tax verified!');

// 9. Cost Segregation & Bonus Depreciation Tests
console.log('Testing Engine 9: Cost Segregation & Bonus Depreciation...');
const costSegTest = calculateCostSegregation({
  purchasePrice: 2000000,
  landValuePct: 20, // $1.6M depreciable basis
  propertyType: 'commercial',
  fiveYearAssetPct: 15, // $240k
  fifteenYearAssetPct: 10, // $160k
  bonusDepreciationPct: 60,
  marginalTaxRatePct: 37,
});
assert.strictEqual(costSegTest.depreciableBasis, 1600000);
assert.strictEqual(costSegTest.fiveYearBasis, 240000);
assert.strictEqual(costSegTest.fifteenYearBasis, 160000);
assert(costSegTest.costSegYear1Depreciation > 250000);
assert(costSegTest.immediateYear1TaxSavings > 90000);
assert(costSegTest.roiMultipleOnStudy > 15);
console.log('  ✅ Cost Segregation Engine: 5/15-yr asset reclassification, bonus depreciation, and tax shield verified!');

// 10. Hard Money Bridge Loan Tests
console.log('Testing Engine 10: Hard Money & Fix-and-Flip Bridge Loan...');
const hardMoneyTest = calculateHardMoney({
  purchasePrice: 220000,
  rehabBudget: 60000,
  afterRepairValue: 420000,
  maxLtcPct: 85,
  maxLtarvPct: 75,
  interestRatePct: 11.5,
  originationPointsPct: 2,
  holdingPeriodMonths: 6,
});
assert.strictEqual(hardMoneyTest.totalProjectCost, 280000);
assert.strictEqual(hardMoneyTest.seventyPercentMao, 234000); // 420k * 0.70 - 60k
assert.strictEqual(hardMoneyTest.is70RuleMet, true);
assert(hardMoneyTest.netFlipProfit > 50000);
assert(hardMoneyTest.annualizedRoiPct > 80);
console.log('  ✅ Hard Money Engine: 70% ARV MAO, dual LTC/LTARV caps, interest-only carry, and ROI verified!');

// 11. Commercial Real Estate Cap Rate & Debt Yield Tests
console.log('Testing Engine 11: CRE Cap Rate, NOI & Debt Yield...');
const creTest = calculateCreCapRate({
  purchasePrice: 5000000,
  grossPotentialRentAnnual: 600000,
  otherIncomeAnnual: 25000,
  vacancyLossPct: 5,
  operatingExpensesAnnual: 225000,
  loanToValuePct: 70, // $3.5M loan
  loanInterestRatePct: 6.75,
  amortizationYears: 25,
});
assert.strictEqual(creTest.effectiveGrossIncome, 595000); // 600k - 30k + 25k
assert.strictEqual(creTest.netOperatingIncome, 370000); // 595k - 225k
assert(Math.abs(creTest.capRatePct - 7.4) < 0.01);
assert.strictEqual(creTest.loanAmount, 3500000);
assert(Math.abs(creTest.debtYieldPct - 10.57) < 0.1);
assert.strictEqual(creTest.isDebtYieldAcceptable, true);
assert(creTest.dscr > 1.25);
console.log('  ✅ CRE Cap Rate Engine: EGI, NOI, 7.4% cap rate, 10.57% debt yield, and DSCR verified!');

// 12. Structured Settlement Factoring Tests
console.log('Testing Engine 12: Structured Settlement & Annuity Lump-Sum Factoring...');
const settlementTest = calculateStructuredSettlement({
  monthlyPayment: 2500,
  remainingYears: 10,
  annualColaPct: 0,
  factoringDiscountRatePct: 12,
  administrativeFee: 2500,
});
assert.strictEqual(settlementTest.totalPaymentsCount, 120);
assert.strictEqual(settlementTest.nominalTotalFutureValue, 300000);
assert(settlementTest.grossPresentValue > 170000 && settlementTest.grossPresentValue < 180000);
assert(settlementTest.netCashLumpSumOffer > 170000);
assert(settlementTest.dollarDiscountSurrendered > 120000);
console.log('  ✅ Structured Settlement Engine: 120-payment monthly discounting, NPV, and factoring haircut verified!');

// 13. Commercial Solar ITC & MACRS Tests
console.log('Testing Engine 13: Commercial Solar ITC & MACRS Depreciation...');
const solarTest = calculateCommercialSolar({
  systemSizeKw: 150,
  installedCostPerWatt: 2.20,
  itcPercentage: 30,
  corporateTaxRatePct: 28,
  utilityRatePerKwh: 0.16,
});
assert.strictEqual(solarTest.totalSystemGrossCost, 330000);
assert.strictEqual(solarTest.federalItcCreditAmount, 99000); // 30% of $330k
assert.strictEqual(solarTest.macrsDepreciableBasis, 280500); // $330k - $49.5k (50% of ITC)
assert(solarTest.totalYear1TaxRelief > 110000);
assert(solarTest.simplePaybackPeriodYears < 6);
console.log('  ✅ Commercial Solar Engine: Section 48 ITC, 85% MACRS basis reduction, and solar payback verified!');

// 14. Federal R&D Tax Credit Tests
console.log('Testing Engine 14: Federal R&D Tax Credit (IRC §41)...');
const rdTest = calculateRdTaxCredit({
  w2EmployeeWages: 450000,
  usContractorExpenses: 100000, // 65% = $65k
  cloudSuppliesExpenses: 35000,
  priorYear1Qre: 200000,
  priorYear2Qre: 180000,
  priorYear3Qre: 160000,
  isQualifiedSmallBusiness: true,
});
assert.strictEqual(rdTest.totalCurrentQre, 550000); // 450k + 65k + 35k
assert.strictEqual(rdTest.priorThreeYearAverageQre, 180000);
assert.strictEqual(rdTest.baseAmountAsc, 90000); // 50% of 180k
assert.strictEqual(rdTest.incrementalQre, 460000);
assert(Math.abs(rdTest.federalCreditAmount - 64400) < 0.01);
assert(Math.abs(rdTest.maxPayrollTaxOffsetEligible - 64400) < 0.01);
console.log('  ✅ R&D Tax Credit Engine: 65% contractor rule, 14% ASC incremental formula, and QSB payroll offset verified!');

// 15. Personal Injury Settlement Multiplier Tests
console.log('Testing Engine 15: Personal Injury Settlement Value & Multiplier...');
const piTest = calculatePersonalInjury({
  pastMedicalBills: 35000,
  futureMedicalCare: 15000,
  lostWages: 10000,
  injurySeverityTier: 'moderate', // 2.75x multiplier
  plaintiffFaultPct: 10,
  attorneyFeePct: 33.333,
  medicalLiensHoldback: 12000,
});
assert.strictEqual(piTest.totalEconomicSpecials, 60000);
assert.strictEqual(piTest.injuryMultiplier, 2.75);
assert.strictEqual(piTest.painAndSufferingGeneralDamages, 165000); // 60k * 2.75
assert.strictEqual(piTest.grossSettlementValue, 225000);
assert.strictEqual(piTest.adjustedGrossSettlement, 202500); // 225k * 0.90
assert(piTest.netClientInPocketRecovery > 115000);
console.log('  ✅ Personal Injury Engine: Specials, 2.75x pain & suffering multiplier, fault reduction, and net client recovery verified!');

// 16. Business Valuation Multiple Tests
console.log('Testing Engine 16: Business Valuation & SDE Multiple Sizer...');
const valTest = calculateBusinessValuation({
  annualGrossRevenue: 1500000,
  netReportedProfit: 180000,
  ownerCompensationDraw: 140000,
  discretionaryPerksExpenses: 25000,
  depreciationAmortization: 35000,
  interestExpense: 10000,
  targetMultiple: 3.5,
});
assert.strictEqual(valTest.totalAddBacks, 210000);
assert.strictEqual(valTest.sellersDiscretionaryEarnings, 390000); // 180k + 210k
assert.strictEqual(valTest.estimatedMedianValuation, 1365000); // 390k * 3.5
assert(Math.abs(valTest.dealStructure.cashAtClosing70Pct - 955500) < 0.1);
assert(Math.abs(valTest.dealStructure.sellerNote15Pct - 204750) < 0.1);
console.log('  ✅ Business Valuation Engine: SDE recast add-backs, 3.5x multiple, and deal structure verified!');

console.log('\n🎉 ALL 16 FINANCIAL & COMMERCIAL MATH ENGINES PASSED 100% OF TESTS!');
console.log('===============================================================');
