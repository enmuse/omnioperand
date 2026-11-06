/**
 * lib/math/personal-injury-settlement.ts
 * OmniOperand Personal Injury Settlement Value & Multiplier Sizer
 *
 * Implements insurance industry claims adjuster and trial attorney valuation formulas:
 * - Special Damages (economic losses: medical bills, lost wages, out-of-pocket)
 * - General Damages (non-economic pain and suffering using 1.5x to 5.0x severity multiplier)
 * - Comparative negligence fault adjustments
 * - Pre-trial vs. Litigation attorney contingency fees (33.33% vs. 40%)
 * - Medical lien / subrogation holdbacks and Net Client In-Pocket Recovery
 */

export interface PersonalInjuryInputs {
  pastMedicalBills: number;
  futureMedicalCare?: number;
  lostWages: number;
  futureLostEarnings?: number;
  injurySeverityTier: 'minor' | 'moderate' | 'severe' | 'catastrophic';
  customMultiplier?: number; // e.g., 2.5
  plaintiffFaultPct?: number; // e.g., 10 for 10% comparative negligence
  attorneyFeePct?: number; // 33.33 for pre-trial, 40 for litigation
  medicalLiensHoldback?: number; // health insurance subrogation or hospital liens
}

export interface PersonalInjuryOutputs {
  totalEconomicSpecials: number;
  injuryMultiplier: number;
  painAndSufferingGeneralDamages: number;
  grossSettlementValue: number;
  comparativeFaultReduction: number;
  adjustedGrossSettlement: number;
  attorneyFeeAmount: number;
  medicalLiensPaid: number;
  netClientInPocketRecovery: number;
  clientTakeHomePercentage: number;
}

export function calculatePersonalInjury(inputs: PersonalInjuryInputs): PersonalInjuryOutputs {
  const pastMed = Math.max(0, inputs.pastMedicalBills || 0);
  const futureMed = Math.max(0, inputs.futureMedicalCare || 0);
  const lostWages = Math.max(0, inputs.lostWages || 0);
  const futureWages = Math.max(0, inputs.futureLostEarnings || 0);

  const totalEconomicSpecials = pastMed + futureMed + lostWages + futureWages;

  let defaultMultiplier = 2.0;
  switch (inputs.injurySeverityTier) {
    case 'minor':
      defaultMultiplier = 1.75; // soft-tissue, sprains, quick recovery
      break;
    case 'moderate':
      defaultMultiplier = 2.75; // fractures, disc herniation, injections
      break;
    case 'severe':
      defaultMultiplier = 4.0; // surgery, ligament tears, partial disability
      break;
    case 'catastrophic':
      defaultMultiplier = 5.0; // TBI, paralysis, permanent impairment
      break;
  }

  const injuryMultiplier = inputs.customMultiplier !== undefined && inputs.customMultiplier > 0
    ? inputs.customMultiplier
    : defaultMultiplier;

  const painAndSufferingGeneralDamages = totalEconomicSpecials * injuryMultiplier;
  const grossSettlementValue = totalEconomicSpecials + painAndSufferingGeneralDamages;

  const faultPct = Math.max(0, Math.min(100, inputs.plaintiffFaultPct ?? 0)) / 100;
  const comparativeFaultReduction = grossSettlementValue * faultPct;
  const adjustedGrossSettlement = Math.max(0, grossSettlementValue - comparativeFaultReduction);

  const feePct = Math.max(0, Math.min(50, inputs.attorneyFeePct ?? 33.333)) / 100;
  const attorneyFeeAmount = adjustedGrossSettlement * feePct;

  const liens = Math.max(0, inputs.medicalLiensHoldback ?? 0);
  const medicalLiensPaid = Math.min(liens, Math.max(0, adjustedGrossSettlement - attorneyFeeAmount));

  const netClientInPocketRecovery = Math.max(0, adjustedGrossSettlement - attorneyFeeAmount - medicalLiensPaid);
  const clientTakeHomePercentage = grossSettlementValue > 0
    ? (netClientInPocketRecovery / grossSettlementValue) * 100
    : 0;

  return {
    totalEconomicSpecials,
    injuryMultiplier,
    painAndSufferingGeneralDamages,
    grossSettlementValue,
    comparativeFaultReduction,
    adjustedGrossSettlement,
    attorneyFeeAmount,
    medicalLiensPaid,
    netClientInPocketRecovery,
    clientTakeHomePercentage
  };
}

