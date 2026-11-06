/**
 * assets/js/hard-money-loan-solver.js
 * OmniOperand Hard Money & Fix-and-Flip Bridge Loan Client Engine
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

  function solveHardMoney() {
    const purchase = getNum('param-purchase_price', 220000);
    const rehab = getNum('param-rehab_budget', 60000);
    const arv = getNum('param-after_repair_value', 420000);
    const maxLtcPct = getNum('param-max_ltc_pct', 85) / 100;
    const maxLtarvPct = getNum('param-max_ltarv_pct', 75) / 100;
    const rate = getNum('param-interest_rate', 11.5) / 100;
    const pointsPct = getNum('param-points_pct', 2) / 100;
    const months = Math.max(1, getNum('param-holding_months', 6));
    const sellingCostsPct = getNum('param-selling_costs_pct', 6) / 100;
    const otherHoldingMonthly = getNum('param-other_holding_monthly', 400);

    const totalProjectCost = purchase + rehab;
    const mao70 = Math.max(0, (arv * 0.70) - rehab);
    const is70Met = purchase <= mao70;

    const maxLtcLoan = totalProjectCost * maxLtcPct;
    const maxLtarvLoan = arv * maxLtarvPct;
    const loanAmount = Math.min(maxLtcLoan, maxLtarvLoan);

    const borrowerEquity = Math.max(0, totalProjectCost - loanAmount);
    const pointsAmount = loanAmount * pointsPct;
    const monthlyInterest = loanAmount * (rate / 12);
    const totalInterest = monthlyInterest * months;
    const totalOtherHolding = otherHoldingMonthly * months;
    const totalHolding = totalInterest + totalOtherHolding;
    const sellingCosts = arv * sellingPct;

    const totalInvested = borrowerEquity + pointsAmount + totalHolding;
    const totalAllCosts = totalProjectCost + pointsAmount + totalHolding + sellingCosts;
    const netProfit = arv - totalAllCosts;

    const roiPct = totalInvested > 0 ? (netProfit / totalInvested) * 100 : 0;
    const annualizedRoiPct = roiPct * (12 / months);

    const badgeEl = document.getElementById('res-mao_badge');
    if (badgeEl) {
      if (is70Met) {
        badgeEl.innerText = 'Passes 70% ARV Rule';
        badgeEl.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
        badgeEl.style.color = '#34d399';
      } else {
        badgeEl.innerText = `Exceeds 70% MAO by $${Math.round(purchase - mao70).toLocaleString()}`;
        badgeEl.style.backgroundColor = 'rgba(239, 68, 68, 0.15)';
        badgeEl.style.color = '#ef4444';
      }
    }

    setMetric('res-net_flip_profit', (netProfit >= 0 ? '+' : '') + formatUSD(netProfit));
    setMetric('res-roi_pct', formatDec(roiPct, 1) + '%');
    setMetric('res-annualized_roi', formatDec(annualizedRoiPct, 1) + '% Ann.');
    setMetric('res-loan_amount', formatUSD(loanAmount));
    setMetric('res-borrower_equity', formatUSD(borrowerEquity));
    setMetric('res-monthly_interest', formatUSD(monthlyInterest) + '/mo');
    setMetric('res-mao_70', formatUSD(mao70));
    setMetric('res-total_invested', formatUSD(totalInvested));

    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Hard Money & Fix-and-Flip Underwriting Verification]
Acquisition Price: $${purchase.toLocaleString()} | Rehab Budget: $${rehab.toLocaleString()} (Total Cost: $${totalProjectCost.toLocaleString()})
After-Repair Value (ARV): $${arv.toLocaleString()}
70% Rule Maximum Allowable Offer (MAO): $${Math.round(mao70).toLocaleString()} (${is70Met ? 'MET' : 'EXCEEDED'})
Financed Loan Amount: $${Math.round(loanAmount).toLocaleString()} (Cap: Min(LTC $${Math.round(maxLtcLoan).toLocaleString()}, LTARV $${Math.round(maxLtarvLoan).toLocaleString()}))
Borrower Out-of-Pocket Cash: $${Math.round(borrowerEquity).toLocaleString()} + Points: $${Math.round(pointsAmount).toLocaleString()}
Holding Period: ${months} Months @ ${(rate * 100).toFixed(2)}% Interest-Only ($${monthlyInterest.toFixed(2)}/mo)
Total Holding & Selling Costs: $${Math.round(totalHolding + sellingCosts).toLocaleString()}
Net Real Estate Flip Profit: $${Math.round(netProfit).toLocaleString()}
Cash-on-Cash ROI: ${roiPct.toFixed(1)}% (${annualizedRoiPct.toFixed(1)}% Annualized)`;
    }
  }

  function copySummary() {
    const profit = document.getElementById('res-net_flip_profit')?.innerText || 'N/A';
    const roi = document.getElementById('res-roi_pct')?.innerText || 'N/A';
    const loan = document.getElementById('res-loan_amount')?.innerText || 'N/A';
    const arv = document.getElementById('param-after_repair_value')?.value || '0';

    const text = `OmniOperand Hard Money Loan Analysis:\n• Projected ARV: $${Number(arv).toLocaleString()}\n• Financed Loan: ${loan}\n• Net Flip Profit: ${profit}\n• Cash-on-Cash ROI: ${roi}\nSource: https://omnioperand.com/calculators/hard-money-loan/`;

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
    const calc = document.getElementById('hard-money-loan-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveHardMoney);
        el.addEventListener('change', solveHardMoney);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveHardMoney();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
