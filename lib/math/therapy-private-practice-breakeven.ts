/**
 * lib/math/therapy-private-practice-breakeven.ts
 * OmniOperand Private Practice Breakeven Engine: Cash-Pay vs. Insurance Credentialing
 *
 * Implements Practice Economics for Mental Health Counselors, Psychologists, & Therapists:
 * - Claim Denial & Delay Degradation Factor
 * - 3rd-Party Clearinghouse & Billing Service Fee Drag
 * - Unpaid Administrative & Prior Authorization Burden
 * - Clinical vs. Administrative Hours Opportunity Cost
 */

export interface TherapyPracticeInputs {
  targetAnnualNetIncome: number; // e.g. $120,000
  weeksWorkedPerYear: number; // e.g. 48
  cashSessionFee: number; // e.g. $150
  insuranceReimbursementRate: number; // e.g. $105
  claimDenialRatePct?: number; // e.g. 8%
  billingFeePct?: number; // e.g. 6%
  unpaidAdminMinsPerSession?: number; // e.g. 20 mins for insurance
  cashAdminMinsPerSession?: number; // e.g. 5 mins for cash
  fixedAnnualOverhead: number; // e.g. $14,000 (EHR, malpractice, office, accounting)
  clinicalMinutesPerSession?: number; // e.g. 50 mins
}

export interface ModelMetrics {
  effectiveRatePerSession: number;
  sessionsPerYear: number;
  sessionsPerWeek: number;
  clinicalHoursPerWeek: number;
  adminHoursPerWeek: number;
  totalWorkingHoursPerWeek: number;
  annualAdminHours: number;
  effectiveGrossHourlyEarnings: number; // Net revenue / total hours worked
}

export interface TherapyPracticeOutputs {
  targetTakeHomeIncome: number;
  fixedAnnualOverhead: number;
  totalRevenueRequired: number;
  weeksWorkedPerYear: number;
  cashModel: ModelMetrics;
  insuranceModel: ModelMetrics;
  comparison: {
    weeklyHourDifference: number; // Insurance weekly hours - Cash weekly hours
    annualUnpaidAdminHoursDifference: number; // Extra admin hours forced by insurance billing
    opportunityCostAnnual: number; // Unpaid admin hours valued at cash rate
    headlineSummary: string;
    effectiveHourlyDisparityPct: number; // How much higher cash hourly earnings are
  };
}

export function calculateTherapyPracticeBreakeven(inputs: TherapyPracticeInputs): TherapyPracticeOutputs {
  const targetNet = Math.max(0, inputs.targetAnnualNetIncome || 0);
  const overhead = Math.max(0, inputs.fixedAnnualOverhead || 0);
  const totalRevenueRequired = targetNet + overhead;

  const weeks = Math.max(1, Math.min(52, inputs.weeksWorkedPerYear ?? 48));
  const cashFee = Math.max(1, inputs.cashSessionFee || 150);
  const insRate = Math.max(1, inputs.insuranceReimbursementRate || 105);
  const denialRate = Math.max(0, Math.min(50, inputs.claimDenialRatePct ?? 8)) / 100;
  const billingFee = Math.max(0, Math.min(30, inputs.billingFeePct ?? 6)) / 100;

  const insAdminMins = Math.max(0, inputs.unpaidAdminMinsPerSession ?? 20);
  const cashAdminMins = Math.max(0, inputs.cashAdminMinsPerSession ?? 5);
  const clinicalMins = Math.max(15, inputs.clinicalMinutesPerSession ?? 50);

  // --- 1. Cash-Pay Model ---
  const cashEffectiveRate = cashFee;
  const cashSessionsYear = Math.ceil(totalRevenueRequired / cashEffectiveRate);
  const cashSessionsWeek = cashSessionsYear / weeks;
  const cashClinicalHoursWeek = (cashSessionsWeek * clinicalMins) / 60;
  const cashAdminHoursWeek = (cashSessionsWeek * cashAdminMins) / 60;
  const cashTotalHoursWeek = cashClinicalHoursWeek + cashAdminHoursWeek;
  const cashAnnualAdminHours = (cashSessionsYear * cashAdminMins) / 60;
  const cashEffectiveHourly = cashTotalHoursWeek > 0 ? (totalRevenueRequired / (cashTotalHoursWeek * weeks)) : 0;

  // --- 2. Insurance In-Network Model ---
  // Effective rate incorporates lost revenue from claim denials/clawbacks and third-party billing costs
  const insEffectiveRate = insRate * (1 - denialRate) * (1 - billingFee);
  const insSessionsYear = Math.ceil(totalRevenueRequired / Math.max(1, insEffectiveRate));
  const insSessionsWeek = insSessionsYear / weeks;
  const insClinicalHoursWeek = (insSessionsWeek * clinicalMins) / 60;
  const insAdminHoursWeek = (insSessionsWeek * insAdminMins) / 60;
  const insTotalHoursWeek = insClinicalHoursWeek + insAdminHoursWeek;
  const insAnnualAdminHours = (insSessionsYear * insAdminMins) / 60;
  const insEffectiveHourly = insTotalHoursWeek > 0 ? (totalRevenueRequired / (insTotalHoursWeek * weeks)) : 0;

  // --- 3. Comparison Metrics ---
  const weeklyHourDifference = insTotalHoursWeek - cashTotalHoursWeek;
  const annualAdminHoursDiff = insAnnualAdminHours - cashAnnualAdminHours;
  const opportunityCostAnnual = annualAdminHoursDiff * cashFee;
  const hourlyDisparityPct = insEffectiveHourly > 0 ? ((cashEffectiveHourly - insEffectiveHourly) / insEffectiveHourly) * 100 : 0;

  const headlineSummary = `You must work ${insTotalHoursWeek.toFixed(1)} hours/week on Insurance vs. ${cashTotalHoursWeek.toFixed(1)} hours/week on Cash to take home the exact same $${Math.round(targetNet).toLocaleString()} income.`;

  return {
    targetTakeHomeIncome: round2(targetNet),
    fixedAnnualOverhead: round2(overhead),
    totalRevenueRequired: round2(totalRevenueRequired),
    weeksWorkedPerYear: weeks,
    cashModel: {
      effectiveRatePerSession: round2(cashEffectiveRate),
      sessionsPerYear: cashSessionsYear,
      sessionsPerWeek: round2(cashSessionsWeek),
      clinicalHoursPerWeek: round2(cashClinicalHoursWeek),
      adminHoursPerWeek: round2(cashAdminHoursWeek),
      totalWorkingHoursPerWeek: round2(cashTotalHoursWeek),
      annualAdminHours: round2(cashAnnualAdminHours),
      effectiveGrossHourlyEarnings: round2(cashEffectiveHourly),
    },
    insuranceModel: {
      effectiveRatePerSession: round2(insEffectiveRate),
      sessionsPerYear: insSessionsYear,
      sessionsPerWeek: round2(insSessionsWeek),
      clinicalHoursPerWeek: round2(insClinicalHoursWeek),
      adminHoursPerWeek: round2(insAdminHoursWeek),
      totalWorkingHoursPerWeek: round2(insTotalHoursWeek),
      annualAdminHours: round2(insAnnualAdminHours),
      effectiveGrossHourlyEarnings: round2(insEffectiveHourly),
    },
    comparison: {
      weeklyHourDifference: round2(weeklyHourDifference),
      annualUnpaidAdminHoursDifference: round2(annualAdminHoursDiff),
      opportunityCostAnnual: round2(opportunityCostAnnual),
      headlineSummary,
      effectiveHourlyDisparityPct: round2(hourlyDisparityPct),
    },
  };
}

function round2(val: number): number {
  return Math.round(val * 100) / 100;
}
