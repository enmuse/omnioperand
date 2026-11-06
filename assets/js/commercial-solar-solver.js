/**
 * assets/js/commercial-solar-solver.js
 * OmniOperand Commercial Solar ITC & MACRS Depreciation Client Engine
 */

(function () {
  'use strict';

  function getNum(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback !== undefined ? fallback : 0;
    const clean = String(el.value).replace(/[^0-9.-]+/g, '');
    const val = parseFloat(clean);
    return isNaN(val) ? (fallback !== undefined ? fallback : 0) : val;
  }

  function setMetric(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
  }

  function formatUSD(val) {
    return '$' + Math.round(val).toLocaleString('en-US');
  }

  function formatDec(val, dec) {
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  function solveSolar() {
    const kw = Math.max(1, getNum('param-system_size_kw', 100));
    const costPerWatt = Math.max(0.5, getNum('param-cost_per_watt', 2.40));
    const itcPct = getNum('param-itc_pct', 30) / 100;
    const taxRate = getNum('param-corporate_tax_rate', 28) / 100;
    const sunHours = getNum('param-sun_hours_annual', 1400);
    const electricRate = getNum('param-utility_rate', 0.16);

    const totalCost = kw * 1000 * costPerWatt;
    const itcAmount = totalCost * itcPct;

    const macrsBasis = Math.max(0, totalCost - (itcAmount * 0.50));
    const macrsTotalShield = macrsBasis * taxRate;
    const year1MacrsDeduction = macrsBasis * 0.20;
    const year1MacrsSavings = year1MacrsDeduction * taxRate;

    const year1TotalTaxRelief = itcAmount + year1MacrsSavings;
    const netSystemCost = Math.max(0, totalCost - itcAmount - macrsTotalShield);

    const annualKwh = kw * sunHours;
    const year1Savings = annualKwh * electricRate;
    const paybackYears = year1Savings > 0 ? (netSystemCost / year1Savings) : 0;

    let cumulative25Yr = 0;
    let rate = electricRate;
    for (let y = 1; y <= 25; y++) {
      cumulative25Yr += annualKwh * (1 - (y - 1) * 0.005) * rate;
      rate *= 1.03;
    }

    setMetric('res-year1_tax_relief', formatUSD(year1TotalTaxRelief));
    setMetric('res-itc_credit_amount', formatUSD(itcAmount));
    setMetric('res-macrs_depreciable_basis', formatUSD(macrsBasis));
    setMetric('res-net_system_cost', formatUSD(netSystemCost));
    setMetric('res-payback_years', formatDec(paybackYears, 1) + ' Years');
    setMetric('res-total_system_cost', formatUSD(totalCost));
    setMetric('res-year1_electric_savings', formatUSD(year1Savings) + '/yr');
    setMetric('res-25yr_savings', formatUSD(cumulative25Yr));

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Commercial Solar Underwriting Verification]
Commercial System Capacity: ${kw} kW DC @ $${costPerWatt.toFixed(2)}/Watt (Gross Turnkey: $${totalCost.toLocaleString()})
Federal Section 48 ITC Credit (${(itcPct * 100).toFixed(0)}%): $${Math.round(itcAmount).toLocaleString()}
Adjusted MACRS 5-Year Depreciable Basis (85%): $${Math.round(macrsBasis).toLocaleString()}
Year 1 MACRS Half-Year Depreciation (20%): $${Math.round(year1MacrsDeduction).toLocaleString()} (Tax Shield @ ${(taxRate * 100).toFixed(0)}%: $${Math.round(year1MacrsSavings).toLocaleString()})
Immediate Year 1 Combined Tax Relief: $${Math.round(year1TotalTaxRelief).toLocaleString()}
Net Capital Investment Post-Tax Shields: $${Math.round(netSystemCost).toLocaleString()} (${((netSystemCost / totalCost) * 100).toFixed(1)}% of Gross)
Annual Solar Production: ${Math.round(annualKwh).toLocaleString()} kWh/yr @ $${electricRate.toFixed(2)}/kWh
Projected Simple Capital Payback: ${paybackYears.toFixed(1)} Years (25-Yr Cumulative Energy Savings: $${Math.round(cumulative25Yr).toLocaleString()})`;
    }
  }

  function copySummary() {
    const relief = document.getElementById('res-year1_tax_relief')?.innerText || 'N/A';
    const netCost = document.getElementById('res-net_system_cost')?.innerText || 'N/A';
    const payback = document.getElementById('res-payback_years')?.innerText || 'N/A';
    const kw = document.getElementById('param-system_size_kw')?.value || '0';

    const text = `OmniOperand Commercial Solar Analysis:\n• System Size: ${kw} kW\n• Year 1 Tax Shield (ITC + MACRS): ${relief}\n• Net Capital Outlay: ${netCost}\n• Simple Payback: ${payback}\nSource: https://omnioperand.com/calculators/commercial-solar-tax-credit/`;

    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('btn-copy-summary');
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = '<span>✓ Summary Copied!</span>';
        setTimeout(() => { btn.innerHTML = orig; }, 2000);
      }
    });
  }

  function init() {
    const calc = document.getElementById('commercial-solar-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveSolar);
        el.addEventListener('change', solveSolar);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveSolar();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
