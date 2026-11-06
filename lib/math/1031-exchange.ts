/**
 * lib/math/1031-exchange.ts
 * OmniOperand IRS §1031 Like-Kind Exchange & Boot Tax Sizer
 *
 * Implements Treasury Regulation §1.1031 criteria:
 * - Realized Gain vs. Recognized Gain
 * - Depreciation Recapture (§1250 at 25%)
 * - Federal Long-Term Capital Gains (20%) + NIIT (3.8%) + State Tax Rate
 * - Cash Boot & Mortgage Boot liability relief
 * - 45-day identification and 180-day exchange closing schedules
 */

export interface Exchange1031Inputs {
  relinquishedSalesPrice: number;
  relinquishedClosingCostsPct?: number; // e.g., 6 for 6%
  originalPurchaseBasis: number;
  capitalImprovements?: number;
  accumulatedDepreciation: number;
  relinquishedMortgagePayoff: number;
  replacementPurchasePrice: number;
  replacementNewMortgage: number;
  cashReceivedOut?: number;
  federalCapGainsPct?: number; // 20%
  niitTaxPct?: number; // 3.8%
  stateTaxPct?: number; // e.g., 5%
}

export interface Exchange1031Outputs {
  netSalesProceeds: number;
  adjustedTaxBasis: number;
  realizedGain: number;
  depreciationRecaptureTax: number;
  capitalGainsTax: number;
  totalTaxIfSoldOutright: number;
  mortgageBoot: number; // relief of debt without equal replacement
  cashBoot: number;
  totalTaxableBoot: number;
  recognizedGain: number; // lesser of realized gain or boot
  taxesDueCurrently: number;
  taxesDeferred1031: number;
  isFullExchange: boolean;
  identificationDeadlineDays: number;
  closingDeadlineDays: number;
}

export function calculate1031Exchange(inputs: Exchange1031Inputs): Exchange1031Outputs {
  const salePrice = Math.max(0, inputs.relinquishedSalesPrice || 0);
  const closingCosts = salePrice * (Math.max(0, inputs.relinquishedClosingCostsPct ?? 6) / 100);
  const netSalesProceeds = Math.max(0, salePrice - closingCosts);

  const purchaseBasis = Math.max(0, inputs.originalPurchaseBasis || 0);
  const improvements = Math.max(0, inputs.capitalImprovements || 0);
  const depreciation = Math.max(0, inputs.accumulatedDepreciation || 0);

  const adjustedTaxBasis = purchaseBasis + improvements - depreciation;
  const realizedGain = Math.max(0, netSalesProceeds - adjustedTaxBasis);

  const fedCapGains = Math.max(0, inputs.federalCapGainsPct ?? 20) / 100;
  const niit = Math.max(0, inputs.niitTaxPct ?? 3.8) / 100;
  const stateRate = Math.max(0, inputs.stateTaxPct ?? 5) / 100;

  // Depreciation recapture taxed at 25% + state
  const deprecTaxRate = 0.25 + stateRate;
  const capGainsTaxRate = fedCapGains + niit + stateRate;

  // Realized gain breakdown: depreciation portion vs remaining capital gain
  const taxableDeprecPortion = Math.min(depreciation, realizedGain);
  const taxableCapGainPortion = Math.max(0, realizedGain - taxableDeprecPortion);

  const depreciationRecaptureTax = taxableDeprecPortion * deprecTaxRate;
  const capitalGainsTax = taxableCapGainPortion * capGainsTaxRate;
  const totalTaxIfSoldOutright = depreciationRecaptureTax + capitalGainsTax;

  // Boot calculations
  const oldDebt = Math.max(0, inputs.relinquishedMortgagePayoff || 0);
  const newDebt = Math.max(0, inputs.replacementNewMortgage || 0);
  const mortgageBoot = Math.max(0, oldDebt - newDebt);
  const cashBoot = Math.max(0, inputs.cashReceivedOut || 0);

  const totalTaxableBoot = mortgageBoot + cashBoot;
  const recognizedGain = Math.min(realizedGain, totalTaxableBoot);

  // Blended tax rate on recognized boot
  const blendedTaxRate = realizedGain > 0 ? (totalTaxIfSoldOutright / realizedGain) : capGainsTaxRate;
  const taxesDueCurrently = recognizedGain * blendedTaxRate;
  const taxesDeferred1031 = Math.max(0, totalTaxIfSoldOutright - taxesDueCurrently);

  const isFullExchange = totalTaxableBoot === 0 && inputs.replacementPurchasePrice >= netSalesProceeds;

  return {
    netSalesProceeds,
    adjustedTaxBasis,
    realizedGain,
    depreciationRecaptureTax,
    capitalGainsTax,
    totalTaxIfSoldOutright,
    mortgageBoot,
    cashBoot,
    totalTaxableBoot,
    recognizedGain,
    taxesDueCurrently,
    taxesDeferred1031,
    isFullExchange,
    identificationDeadlineDays: 45,
    closingDeadlineDays: 180
  };
}
