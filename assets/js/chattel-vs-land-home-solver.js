/**
 * assets/js/chattel-vs-land-home-solver.js
 * OmniOperand Chattel Loan vs. Land-Home Modular Mortgage Comparison Engine
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

  function calculatePI(principal, annualRate, termYears) {
    if (principal <= 0) return 0;
    const n = termYears * 12;
    const r = annualRate / 12;
    if (r === 0) return principal / n;
    const f = Math.pow(1 + r, n);
    return principal * ((r * f) / (f - 1));
  }

  function solveComparison() {
    const homeCost = getNum('param-home_cost', 150000);
    const landCost = getNum('param-land_cost', 65000);

    // Chattel terms
    const cRate = getNum('param-chattel_rate', 9.75) / 100;
    const cTerm = getNum('param-chattel_term', 20);
    const cDownPct = getNum('param-chattel_down_pct', 10) / 100;
    const initialLotRent = getNum('param-chattel_lot_rent', 650);
    const lotInflation = 0.035; // 3.5% annual park rent escalation
    const cDepreciation = 0.02; // 2% annual personal property depreciation

    // Real property terms
    const lhPackage = homeCost + landCost;
    const lhRate = getNum('param-real_rate', 6.75) / 100;
    const lhTerm = getNum('param-real_term', 30);
    const lhDownPct = getNum('param-real_down_pct', 5) / 100;
    const lhTaxRate = 0.012; // 1.2% property taxes
    const lhAnnualIns = 1400;
    const lhAppreciation = 0.035; // 3.5% real estate appreciation

    // Down payments & loan amounts
    const cDown = homeCost * cDownPct;
    const cPrincipal = Math.max(0, homeCost - cDown);
    const cMonthlyPI = calculatePI(cPrincipal, cRate, cTerm);
    const cInitialTotalMonthly = cMonthlyPI + initialLotRent;

    const lhDown = lhPackage * lhDownPct;
    const lhPrincipal = Math.max(0, lhPackage - lhDown);
    const lhMonthlyPI = calculatePI(lhPrincipal, lhRate, lhTerm);
    const lhMonthlyEscrow = (lhPackage * lhTaxRate + lhAnnualIns) / 12;
    const lhInitialTotalMonthly = lhMonthlyPI + lhMonthlyEscrow;

    // Simulate 120 months (10 years) & 360 months (30 years)
    let cBal = cPrincipal;
    let cCumInt = 0;
    let cCumOutlay = cDown;

    let lhBal = lhPrincipal;
    let lhCumInt = 0;
    let lhCumOutlay = lhDown;

    let cInt10 = 0, lhInt10 = 0;
    let cOutlay10 = 0, lhOutlay10 = 0;
    let cEquity10 = 0, lhEquity10 = 0;
    let breakevenYear = 30;
    let breakevenFound = false;

    for (let m = 1; m <= 360; m++) {
      const currentLotRent = initialLotRent * Math.pow(1 + lotInflation, (m - 1) / 12);

      // Chattel step
      if (m <= cTerm * 12 && cBal > 0) {
        const intMo = cBal * (cRate / 12);
        const prinMo = Math.min(cBal, cMonthlyPI - intMo);
        cBal = Math.max(0, cBal - prinMo);
        cCumInt += intMo;
        cCumOutlay += cMonthlyPI + currentLotRent;
      } else {
        cCumOutlay += currentLotRent;
      }

      // Land-Home step
      if (m <= lhTerm * 12 && lhBal > 0) {
        const intMo = lhBal * (lhRate / 12);
        const prinMo = Math.min(lhBal, lhMonthlyPI - intMo);
        lhBal = Math.max(0, lhBal - prinMo);
        lhCumInt += intMo;
        lhCumOutlay += lhMonthlyPI + lhMonthlyEscrow;
      } else {
        lhCumOutlay += lhMonthlyEscrow;
      }

      if (m === 120) {
        cInt10 = cCumInt;
        lhInt10 = lhCumInt;
        cOutlay10 = cCumOutlay;
        lhOutlay10 = lhCumOutlay;
        const cVal10 = homeCost * Math.pow(1 - cDepreciation, 10);
        cEquity10 = Math.max(0, cVal10 - cBal);
        const lhVal10 = lhPackage * Math.pow(1 + lhAppreciation, 10);
        lhEquity10 = Math.max(0, lhVal10 - lhBal);
      }

      // Check Breakeven Year
      if (!breakevenFound && m % 12 === 0) {
        const yr = m / 12;
        const cVal = homeCost * Math.pow(1 - cDepreciation, yr);
        const cNetWealth = Math.max(0, cVal - cBal) - cCumOutlay;

        const lhVal = lhPackage * Math.pow(1 + lhAppreciation, yr);
        const lhNetWealth = Math.max(0, lhVal - lhBal) - lhCumOutlay;

        if (lhNetWealth > cNetWealth) {
          breakevenYear = yr;
          breakevenFound = true;
        }
      }
    }

    setMetric('res-chattel_initial_monthly', formatUSD(cInitialTotalMonthly) + '/mo');
    setMetric('res-land_home_initial_monthly', formatUSD(lhInitialTotalMonthly) + '/mo');
    setMetric('res-chattel_pi', formatUSD(cMonthlyPI));
    setMetric('res-land_home_pi', formatUSD(lhMonthlyPI));
    setMetric('res-chattel_lot_rent', formatUSD(initialLotRent) + '/mo');
    setMetric('res-land_home_escrow', formatUSD(lhMonthlyEscrow) + '/mo');

    setMetric('res-chattel_10yr_interest', formatUSD(cInt10));
    setMetric('res-land_home_10yr_interest', formatUSD(lhInt10));
    setMetric('res-chattel_10yr_outlay', formatUSD(cOutlay10));
    setMetric('res-land_home_10yr_outlay', formatUSD(lhOutlay10));

    setMetric('res-chattel_10yr_equity', formatUSD(cEquity10));
    setMetric('res-land_home_10yr_equity', formatUSD(lhEquity10));

    const equityAdvantage = lhEquity10 - cEquity10;
    setMetric('res-10yr_equity_advantage', '+' + formatUSD(equityAdvantage));
    setMetric('res-breakeven_year', `Year ${breakevenYear}`);

    // Update breakeven badge text
    const beBadge = document.getElementById('res-breakeven_badge');
    if (beBadge) {
      beBadge.innerText = `Breakeven: Year ${breakevenYear} • Net Wealth Crossover`;
    }

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Manufactured Home Financing Comparative Analysis]
Manufactured Home Cost: $${homeCost.toLocaleString()} | Private Land Cost: $${landCost.toLocaleString()}
1. Chattel Personal Property on Leased Lot:
   - Initial Loan: $${Math.round(cPrincipal).toLocaleString()} @ ${(cRate*100).toFixed(2)}% (${cTerm} Yrs)
   - Monthly Installment: $${cMonthlyPI.toFixed(2)} P&I + $${initialLotRent.toFixed(2)} Lot Rent = $${cInitialTotalMonthly.toFixed(2)}/mo
   - 10-Year Cumulative Interest: $${Math.round(cInt10).toLocaleString()} | 10-Year Outlay: $${Math.round(cOutlay10).toLocaleString()}
   - 10-Year Net Equity (at 2% annual depreciation): $${Math.round(cEquity10).toLocaleString()}
2. Land-Home Modular Mortgage (Home + Land Owned):
   - Package Price: $${lhPackage.toLocaleString()} | Loan: $${Math.round(lhPrincipal).toLocaleString()} @ ${(lhRate*100).toFixed(2)}% (${lhTerm} Yrs)
   - Monthly Installment: $${lhMonthlyPI.toFixed(2)} P&I + $${lhMonthlyEscrow.toFixed(2)} Taxes/Ins = $${lhInitialTotalMonthly.toFixed(2)}/mo
   - 10-Year Cumulative Interest: $${Math.round(lhInt10).toLocaleString()} | 10-Year Outlay: $${Math.round(lhOutlay10).toLocaleString()}
   - 10-Year Net Equity (at 3.5% real estate appreciation): $${Math.round(lhEquity10).toLocaleString()}
Comparative Crossover: Land-Home builds $${Math.round(equityAdvantage).toLocaleString()} more equity over 10 years, breaking even in Year ${breakevenYear}.`;
    }
  }

  function copySummary() {
    const chattelMo = document.getElementById('res-chattel_initial_monthly')?.innerText || '$0';
    const landHomeMo = document.getElementById('res-land_home_initial_monthly')?.innerText || '$0';
    const eqAdv = document.getElementById('res-10yr_equity_advantage')?.innerText || '$0';
    const be = document.getElementById('res-breakeven_year')?.innerText || 'Year 5';

    const text = `OmniOperand Chattel vs Land-Home Mortgage Analysis:\n• Chattel Monthly: ${chattelMo}\n• Land-Home Package Monthly: ${landHomeMo}\n• 10-Year Land-Home Equity Advantage: ${eqAdv}\n• Breakeven Crossover: ${be}\nSource: https://omnioperand.com/calculators/chattel-vs-land-home/`;

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
    const calc = document.getElementById('chattel-land-home-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveComparison);
        el.addEventListener('change', solveComparison);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveComparison();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
