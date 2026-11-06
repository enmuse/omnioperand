/**
 * assets/js/1031-exchange-solver.js
 * OmniOperand IRS §1031 Like-Kind Exchange & Boot Tax Client Engine
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

  function solve1031() {
    const salePrice = getNum('param-sales_price', 1500000);
    const closingCostsPct = getNum('param-closing_costs_pct', 6) / 100;
    const purchaseBasis = getNum('param-original_basis', 600000);
    const improvements = getNum('param-improvements', 100000);
    const depreciation = getNum('param-depreciation', 250000);
    const oldDebt = getNum('param-relinquished_debt', 500000);
    const newPrice = getNum('param-replacement_price', 1600000);
    const newDebt = getNum('param-replacement_debt', 600000);
    const cashOut = getNum('param-cash_boot', 0);

    const netSalesProceeds = Math.max(0, salePrice - (salePrice * closingCostsPct));
    const adjustedBasis = purchaseBasis + improvements - depreciation;
    const realizedGain = Math.max(0, netSalesProceeds - adjustedBasis);

    const fedCapGains = 0.20;
    const niit = 0.038;
    const stateTax = 0.05;

    const deprecTaxRate = 0.25 + stateTax;
    const capGainsTaxRate = fedCapGains + niit + stateTax;

    const taxableDeprec = Math.min(depreciation, realizedGain);
    const taxableCapGain = Math.max(0, realizedGain - taxableDeprec);

    const totalOutrightTax = (taxableDeprec * deprecTaxRate) + (taxableCapGain * capGainsTaxRate);

    const mortgageBoot = Math.max(0, oldDebt - newDebt);
    const totalBoot = mortgageBoot + cashOut;
    const recognizedGain = Math.min(realizedGain, totalBoot);

    const blendedRate = realizedGain > 0 ? (totalOutrightTax / realizedGain) : capGainsTaxRate;
    const taxesDueCurrently = recognizedGain * blendedRate;
    const taxesDeferred = Math.max(0, totalOutrightTax - taxesDueCurrently);

    const badgeEl = document.getElementById('res-exchange_badge');
    if (badgeEl) {
      if (totalBoot === 0 && newPrice >= netSalesProceeds) {
        badgeEl.innerText = '100% Tax-Deferred Full Exchange';
        badgeEl.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
        badgeEl.style.color = '#34d399';
      } else {
        badgeEl.innerText = `Partial Exchange ($${Math.round(totalBoot).toLocaleString()} Boot)`;
        badgeEl.style.backgroundColor = 'rgba(245, 158, 11, 0.15)';
        badgeEl.style.color = '#f59e0b';
      }
    }

    setMetric('res-taxes_deferred', formatUSD(taxesDeferred));
    setMetric('res-taxes_due', formatUSD(taxesDueCurrently));
    setMetric('res-realized_gain', formatUSD(realizedGain));
    setMetric('res-adjusted_basis', formatUSD(adjustedBasis));
    setMetric('res-total_boot', formatUSD(totalBoot));
    setMetric('res-net_proceeds', formatUSD(netSalesProceeds));
    setMetric('res-outright_tax', formatUSD(totalOutrightTax));

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand IRS §1031 Exchange Underwriting Verification]
Relinquished Property Sale Price: $${salePrice.toLocaleString()} (Net: $${Math.round(netSalesProceeds).toLocaleString()})
Adjusted Tax Basis: $${Math.round(adjustedBasis).toLocaleString()} (Purchase: $${purchaseBasis.toLocaleString()} + Impr: $${improvements.toLocaleString()} - Deprec: $${depreciation.toLocaleString()})
Total Realized Gain: $${Math.round(realizedGain).toLocaleString()}
Tax if Sold Outright: $${Math.round(totalOutrightTax).toLocaleString()} (Deprec Recapture: $${Math.round(taxableDeprec * deprecTaxRate).toLocaleString()} + Cap Gains: $${Math.round(taxableCapGain * capGainsTaxRate).toLocaleString()})
Replacement Property: $${newPrice.toLocaleString()} (Debt: $${newDebt.toLocaleString()})
Taxable Boot (Mortgage + Cash): $${Math.round(totalBoot).toLocaleString()}
Resulting Immediate Tax: $${Math.round(taxesDueCurrently).toLocaleString()} | Taxes 1031 Deferred: $${Math.round(taxesDeferred).toLocaleString()}
Deadlines: 45 Days to Identify | 180 Days to Close`;
    }
  }

  function copySummary() {
    const deferred = document.getElementById('res-taxes_deferred')?.innerText || 'N/A';
    const due = document.getElementById('res-taxes_due')?.innerText || 'N/A';
    const gain = document.getElementById('res-realized_gain')?.innerText || 'N/A';
    const sale = document.getElementById('param-sales_price')?.value || '0';

    const text = `OmniOperand 1031 Exchange Analysis:\n• Relinquished Sale: $${Number(sale).toLocaleString()}\n• Total Realized Gain: ${gain}\n• Taxes Deferred (§1031): ${deferred}\n• Immediate Tax Due: ${due}\nSource: https://omnioperand.com/calculators/1031-exchange/`;

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
    const calc = document.getElementById('1031-exchange-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solve1031);
        el.addEventListener('change', solve1031);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solve1031();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
