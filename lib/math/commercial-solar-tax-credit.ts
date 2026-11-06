/**
 * lib/math/commercial-solar-tax-credit.ts
 * OmniOperand Commercial Solar ITC Tax Credit & MACRS Accelerated Depreciation Engine
 *
 * Implements Inflation Reduction Act (IRA) Section 48 & MACRS 5-Year Property criteria:
 * - 30% Base Investment Tax Credit (ITC) + optional 10% energy community bonus
 * - Depreciable basis adjustment (100% - 50% of ITC = 85% basis)
 * - 5-year MACRS depreciation schedule (Yr 1: 20%, Yr 2: 32%, Yr 3: 19.2%, Yr 4: 11.52%, Yr 5: 11.52%, Yr 6: 5.76%)
 * - Bonus depreciation acceleration, annual solar electricity generation, and net payback period
 */

export interface CommercialSolarInputs {
  systemSizeKw: number; // e.g., 100 kW
  installedCostPerWatt?: number; // e.g., $2.40 / watt
  itcPercentage?: number; // e.g., 30 for 30% (or 40% with energy community bonus)
  corporateTaxRatePct?: number; // e.g., 28 for 28% (federal 21% + state 7%)
  annualSunHoursPerYear?: number; // e.g., 1400 kWh / kW
  utilityRatePerKwh?: number; // e.g., $0.16 / kWh
  annualRateEscalationPct?: number; // e.g., 3%
}

export interface CommercialSolarOutputs {
  systemSizeKw: number;
  totalSystemGrossCost: number;
  federalItcCreditAmount: number;
  macrsDepreciableBasis: number; // 85% of gross cost
  macrsTaxShieldTotal: number;
  year1MacrsDeduction: number;
  year1MacrsTaxSavings: number;
  totalYear1TaxRelief: number; // ITC + Year 1 MACRS tax savings
  netSystemCostAfterTaxes: number;
  year1ElectricSavings: number;
  simplePaybackPeriodYears: number;
  twentyFiveYearSavings: number;
}

export function calculateCommercialSolar(inputs: CommercialSolarInputs): CommercialSolarOutputs {
  const kw = Math.max(1, inputs.systemSizeKw || 100);
  const costPerWatt = Math.max(0.5, inputs.installedCostPerWatt ?? 2.40);
  const totalCost = kw * 1000 * costPerWatt;

  const itcPct = Math.max(0, Math.min(60, inputs.itcPercentage ?? 30)) / 100;
  const itcCreditAmount = totalCost * itcPct;

  // IRS rule: basis reduced by half of ITC
  const basisReduction = itcCreditAmount * 0.50;
  const macrsBasis = Math.max(0, totalCost - basisReduction);

  const taxRate = Math.max(0, inputs.corporateTaxRatePct ?? 28) / 100;
  const macrsTaxShieldTotal = macrsBasis * taxRate;

  // Year 1 standard MACRS 5-year half-year convention is 20%
  const year1MacrsDeduction = macrsBasis * 0.20;
  const year1MacrsTaxSavings = year1MacrsDeduction * taxRate;

  const totalYear1TaxRelief = itcCreditAmount + year1MacrsTaxSavings;
  const netSystemCostAfterTaxes = Math.max(0, totalCost - itcCreditAmount - macrsTaxShieldTotal);

  const sunHours = Math.max(500, inputs.annualSunHoursPerYear ?? 1400);
  const annualKwh = kw * sunHours;
  const electricRate = Math.max(0.01, inputs.utilityRatePerKwh ?? 0.16);
  const year1ElectricSavings = annualKwh * electricRate;

  const annualEscalation = Math.max(0, inputs.annualRateEscalationPct ?? 3) / 100;

  // Simple payback: net out of pocket cost / annual electric savings
  const simplePaybackPeriodYears = year1ElectricSavings > 0 ? (netSystemCostAfterTaxes / year1ElectricSavings) : 0;

  // 25-year cumulative electric savings
  let twentyFiveYearSavings = 0;
  let currentRate = electricRate;
  for (let y = 1; y <= 25; y++) {
    // 0.5% annual solar panel degradation
    const degradedKwh = annualKwh * (1 - (y - 1) * 0.005);
    twentyFiveYearSavings += degradedKwh * currentRate;
    currentRate *= (1 + annualEscalation);
  }

  return {
    systemSizeKw: kw,
    totalSystemGrossCost: totalCost,
    federalItcCreditAmount: itcCreditAmount,
    macrsDepreciableBasis: macrsBasis,
    macrsTaxShieldTotal,
    year1MacrsDeduction,
    year1MacrsTaxSavings,
    totalYear1TaxRelief,
    netSystemCostAfterTaxes,
    year1ElectricSavings,
    simplePaybackPeriodYears,
    twentyFiveYearSavings
  };
}
