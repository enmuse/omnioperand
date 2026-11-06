/**
 * lib/math/cost-segregation.ts
 * OmniOperand Cost Segregation & Bonus Depreciation Tax Savings Engine
 *
 * Implements IRS Cost Segregation Audit Techniques Guide (ATG) standards:
 * - Asset reclassification into 5-year (personal property) and 15-year (land improvements)
 * - IRC §168(k) bonus depreciation acceleration vs. 27.5-year / 39-year MACRS straight-line
 * - First-year incremental tax write-off and Net Present Value (NPV) of tax timing arbitrage
 */

export interface CostSegInputs {
  purchasePrice: number;
  landValuePct?: number; // e.g., 20 for 20%
  propertyType: 'residential' | 'commercial'; // 27.5 vs 39 years
  fiveYearAssetPct?: number; // e.g., 14 for 14%
  fifteenYearAssetPct?: number; // e.g., 10 for 10%
  bonusDepreciationPct?: number; // e.g., 60 for 60%
  marginalTaxRatePct?: number; // e.g., 37 for 37%
  discountRatePct?: number; // for NPV, e.g., 8 for 8%
}

export interface CostSegOutputs {
  totalPurchasePrice: number;
  landValue: number;
  depreciableBasis: number;
  fiveYearBasis: number;
  fifteenYearBasis: number;
  structuralBasis: number;
  straightLineYear1Depreciation: number;
  costSegYear1Depreciation: number;
  incrementalYear1Deduction: number;
  immediateYear1TaxSavings: number;
  npvTaxBenefit: number;
  roiMultipleOnStudy: number; // assuming ~$4,500 typical engineering study fee
}

export function calculateCostSegregation(inputs: CostSegInputs): CostSegOutputs {
  const price = Math.max(0, inputs.purchasePrice || 0);
  const landPct = Math.max(0, Math.min(100, inputs.landValuePct ?? 20)) / 100;
  const landValue = price * landPct;
  const depreciableBasis = Math.max(0, price - landValue);

  const fivePct = Math.max(0, Math.min(50, inputs.fiveYearAssetPct ?? 14)) / 100;
  const fifteenPct = Math.max(0, Math.min(50, inputs.fifteenYearAssetPct ?? 10)) / 100;

  const fiveYearBasis = depreciableBasis * fivePct;
  const fifteenYearBasis = depreciableBasis * fifteenPct;
  const structuralBasis = Math.max(0, depreciableBasis - fiveYearBasis - fifteenYearBasis);

  const bonusPct = Math.max(0, Math.min(100, inputs.bonusDepreciationPct ?? 60)) / 100;
  const taxRate = Math.max(0, inputs.marginalTaxRatePct ?? 37) / 100;
  const discountRate = Math.max(0, inputs.discountRatePct ?? 8) / 100;

  const recoveryYears = inputs.propertyType === 'residential' ? 27.5 : 39.0;
  // Half-year convention for standard straight-line: ~1/recoveryYears * 0.5 or mid-month
  const straightLineYear1Depreciation = (depreciableBasis / recoveryYears) * (11.5 / 12); // mid-month average

  // Cost Seg Year 1 Depreciation:
  // 5-year bonus + remaining standard 5-year half-year (20%)
  const fiveBonus = fiveYearBasis * bonusPct;
  const fiveRemaining = fiveYearBasis - fiveBonus;
  const fiveStandardYr1 = fiveRemaining * 0.20; // 200% DB half-year

  // 15-year bonus + remaining standard 15-year half-year (5%)
  const fifteenBonus = fifteenYearBasis * bonusPct;
  const fifteenRemaining = fifteenYearBasis - fifteenBonus;
  const fifteenStandardYr1 = fifteenRemaining * 0.05; // 150% DB half-year

  // Structural portion straight-line Year 1
  const structuralYr1 = (structuralBasis / recoveryYears) * (11.5 / 12);

  const costSegYear1Depreciation = fiveBonus + fiveStandardYr1 + fifteenBonus + fifteenStandardYr1 + structuralYr1;
  const incrementalYear1Deduction = Math.max(0, costSegYear1Depreciation - straightLineYear1Depreciation);
  const immediateYear1TaxSavings = incrementalYear1Deduction * taxRate;

  // NPV timing benefit over 10-year holding period
  // Front-loading tax shield vs steady straight-line: approximate discounted delta
  const npvTaxBenefit = immediateYear1TaxSavings * (1 / (1 + discountRate * 0.5));
  const estimatedStudyCost = 4500;
  const roiMultipleOnStudy = immediateYear1TaxSavings > 0 ? (immediateYear1TaxSavings / estimatedStudyCost) : 0;

  return {
    totalPurchasePrice: price,
    landValue,
    depreciableBasis,
    fiveYearBasis,
    fifteenYearBasis,
    structuralBasis,
    straightLineYear1Depreciation,
    costSegYear1Depreciation,
    incrementalYear1Deduction,
    immediateYear1TaxSavings,
    npvTaxBenefit,
    roiMultipleOnStudy
  };
}

