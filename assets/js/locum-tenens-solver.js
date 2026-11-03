/**
 * assets/js/locum-tenens-solver.js
 * OmniOperand 1099 Travel Healthcare / Locum Tenens Tax Arbitrage Client Engine
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

  function computeFedTax(taxable, isMarried) {
    if (taxable <= 0) return 0;
    const brackets = isMarried
      ? [
          { cap: 23200, rate: 0.10 },
          { cap: 94300, rate: 0.12 },
          { cap: 201050, rate: 0.22 },
          { cap: 383900, rate: 0.24 },
          { cap: 487450, rate: 0.32 },
          { cap: 731200, rate: 0.35 },
          { cap: Infinity, rate: 0.37 },
        ]
      : [
          { cap: 11600, rate: 0.10 },
          { cap: 47150, rate: 0.12 },
          { cap: 100525, rate: 0.22 },
          { cap: 191950, rate: 0.24 },
          { cap: 243725, rate: 0.32 },
          { cap: 609350, rate: 0.35 },
          { cap: Infinity, rate: 0.37 },
        ];

    let tax = 0;
    let prev = 0;
    for (let i = 0; i < brackets.length; i++) {
      const b = brackets[i];
      if (taxable > prev) {
        const chunk = Math.min(taxable - prev, b.cap - prev);
        tax += chunk * b.rate;
        prev = b.cap;
      } else break;
    }
    return tax;
  }

  function solveLocumTax() {
    const w2Gross = getNum('param-w2_salary', 180000);
    const hourly = getNum('param-locum_hourly_rate', 150);
    const hours = getNum('param-billable_hours', 1600);
    const weeklyStipend = getNum('param-weekly_stipend', 1400);

    const statusEl = document.querySelector('input[name="filing_status"]:checked');
    const isMarried = statusEl ? statusEl.value === 'married' : false;
    const stdDed = isMarried ? 29200 : 14600;
    const stateRate = getNum('param-state_tax_rate', 5.0) / 100;
    const monthlyDupHousing = getNum('param-duplicated_housing', 1500);
    const annualDupHousing = monthlyDupHousing * 12;
    const busDeductions = getNum('param-business_deductions', 12000);
    const solo401k = getNum('param-solo_401k', 20000);

    // 1. W-2 Calculation
    const ssCap = 168600;
    const w2SS = Math.min(w2Gross, ssCap) * 0.062;
    const w2Med = w2Gross * 0.0145;
    const w2AddMedThresh = isMarried ? 250000 : 200000;
    const w2AddMed = Math.max(0, w2Gross - w2AddMedThresh) * 0.009;
    const w2Fica = w2SS + w2Med + w2AddMed;

    const w2Taxable = Math.max(0, w2Gross - stdDed);
    const w2Fed = computeFedTax(w2Taxable, isMarried);
    const w2State = w2Taxable * stateRate;
    const w2TotalTax = w2Fica + w2Fed + w2State;
    const w2NetTakeHome = w2Gross - w2TotalTax;

    // 2. 1099 Locum Tenens Calculation
    const grossHourly = hourly * hours;
    const weeksWorked = hours > 0 ? hours / 40 : 0;
    const nonTaxablePerDiem = weeklyStipend * weeksWorked;
    const totalGrossInflow = grossHourly + nonTaxablePerDiem;

    const netSchedC = Math.max(0, grossHourly - busDeductions);
    const seEarnings = netSchedC * 0.9235;
    const seSS = Math.min(seEarnings, ssCap) * 0.124;
    const seMed = seEarnings * 0.029;
    const seAddMed = Math.max(0, seEarnings - w2AddMedThresh) * 0.009;
    const totalSeTax = seSS + seMed + seAddMed;
    const dedHalfSe = totalSeTax / 2;

    const maxSolo401k = Math.min(69000, 23000 + Math.max(0, (netSchedC - dedHalfSe) * 0.20));
    const effectiveSolo401k = Math.min(maxSolo401k, solo401k);

    const locumTaxable = Math.max(0, netSchedC - dedHalfSe - effectiveSolo401k - stdDed);
    const locumFed = computeFedTax(locumTaxable, isMarried);
    const locumState = locumTaxable * stateRate;
    const locumTotalTax = totalSeTax + locumFed + locumState;

    const trueNetTakeHome = (grossHourly - busDeductions - annualDupHousing - locumTotalTax) + nonTaxablePerDiem;
    const quarterlyTax = locumTotalTax / 4;
    const netAdvantage = trueNetTakeHome - w2NetTakeHome;
    const perDiemShieldSavings = nonTaxablePerDiem * 0.32;

    setMetric('res-w2_net_takehome', formatUSD(w2NetTakeHome));
    setMetric('res-locum_net_takehome', formatUSD(trueNetTakeHome));
    setMetric('res-net_arbitrage_diff', (netAdvantage >= 0 ? '+' : '') + formatUSD(netAdvantage));
    setMetric('res-per_diem_tax_shield', formatUSD(perDiemShieldSavings));
    setMetric('res-non_taxable_stipends', formatUSD(nonTaxablePerDiem));
    setMetric('res-total_locum_tax', formatUSD(locumTotalTax));
    setMetric('res-se_tax_total', formatUSD(totalSeTax));
    setMetric('res-quarterly_payment', formatUSD(quarterlyTax) + ' / quarter');

    // Quarterly dates
    setMetric('res-q1_payment', formatUSD(quarterlyTax));
    setMetric('res-q2_payment', formatUSD(quarterlyTax));
    setMetric('res-q3_payment', formatUSD(quarterlyTax));
    setMetric('res-q4_payment', formatUSD(quarterlyTax));

    const diffEl = document.getElementById('res-net_arbitrage_diff');
    if (diffEl) {
      diffEl.style.color = netAdvantage >= 0 ? 'var(--accent-emerald, #10b981)' : '#ef4444';
    }

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Locum Tenens Tax Arbitrage Verification]
W-2 Permanent Benchmark: $${w2Gross.toLocaleString()} Gross -> $${Math.round(w2TotalTax).toLocaleString()} Total Tax -> $${Math.round(w2NetTakeHome).toLocaleString()} Net Take-Home
1099 Healthcare Locum Model:
- Hourly Rate: $${hourly}/hr × ${hours} Billable Hours = $${Math.round(grossHourly).toLocaleString()} Gross Hourly
- Non-Taxable Per Diem Stipend: $${weeklyStipend}/wk × ${weeksWorked.toFixed(1)} Wks = $${Math.round(nonTaxablePerDiem).toLocaleString()} Tax-Free
- Total 1099 Inflow: $${Math.round(totalGrossInflow).toLocaleString()}
- Schedule C Deductions: $${busDeductions.toLocaleString()} | Duplicated Housing: $${annualDupHousing.toLocaleString()}
- Self-Employment Tax: $${Math.round(totalSeTax).toLocaleString()} | Solo 401(k) Shelter: $${Math.round(effectiveSolo401k).toLocaleString()}
- Total Annual Tax (SE + Fed + State): $${Math.round(locumTotalTax).toLocaleString()} (Quarterly: $${Math.round(quarterlyTax).toLocaleString()})
- True Net After-Tax Cash Flow: $${Math.round(trueNetTakeHome).toLocaleString()}
Annual Arbitrage Advantage: +$${Math.round(netAdvantage).toLocaleString()} higher take-home pay via 1099 locum structure.`;
    }
  }

  function copySummary() {
    const w2Net = document.getElementById('res-w2_net_takehome')?.innerText || '$0';
    const locumNet = document.getElementById('res-locum_net_takehome')?.innerText || '$0';
    const diff = document.getElementById('res-net_arbitrage_diff')?.innerText || '$0';
    const perDiem = document.getElementById('res-non_taxable_stipends')?.innerText || '$0';
    const qtr = document.getElementById('res-quarterly_payment')?.innerText || '$0';

    const text = `OmniOperand Locum Tenens Tax Arbitrage Analysis:\n• W-2 Net Take-Home: ${w2Net}\n• 1099 Locum Net Take-Home: ${locumNet}\n• Net Arbitrage Advantage: ${diff}\n• Tax-Free Per Diem Total: ${perDiem}\n• Estimated Quarterly Tax Payment: ${qtr}\nSource: https://omnioperand.com/calculators/locum-tenens-tax-calculator/`;

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
    const calc = document.getElementById('locum-tenens-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveLocumTax);
        el.addEventListener('change', solveLocumTax);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveLocumTax();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
