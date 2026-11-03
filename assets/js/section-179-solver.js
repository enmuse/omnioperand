/**
 * assets/js/section-179-solver.js
 * OmniOperand Section 179 Heavy Equipment Tax Shield & Cash-Flow Client Engine
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

  function solveSection179() {
    const price = getNum('param-equipment_price', 125000);
    const eqTypeEl = document.querySelector('input[name="equipment_type"]:checked');
    const eqType = eqTypeEl ? eqTypeEl.value : 'heavy_machinery';

    const methodEl = document.querySelector('input[name="financing_method"]:checked');
    const isLoan = methodEl ? methodEl.value === 'loan' : true;

    const downPct = isLoan ? getNum('param-down_payment_pct', 10) / 100 : 1.0;
    const ratePct = getNum('param-interest_rate', 8.5) / 100;
    const termMonths = getNum('param-loan_term_months', 60);
    const activeMonths = getNum('param-months_active_yr1', 6);
    const taxBracket = getNum('param-tax_bracket', 35) / 100;

    // Toggle financing input fields visibility/disabled
    const loanFields = document.querySelectorAll('.loan-only-field');
    loanFields.forEach(f => {
      f.style.opacity = isLoan ? '1' : '0.4';
      const inp = f.querySelector('input');
      if (inp) inp.disabled = !isLoan;
    });

    // 1. Section 179 & Bonus Depreciation limits
    const sec179Cap = 1220000;
    const suvCap = 30500;
    const luxuryCarCap = 20400;

    let sec179Deduction = 0;
    let bonusDepreciation = 0;

    if (eqType === 'heavy_machinery') {
      sec179Deduction = Math.min(price, sec179Cap);
      const remainingBasis = Math.max(0, price - sec179Deduction);
      bonusDepreciation = remainingBasis * 0.60;
    } else if (eqType === 'heavy_suv') {
      sec179Deduction = Math.min(price, suvCap);
      const remainingBasis = Math.max(0, price - sec179Deduction);
      bonusDepreciation = remainingBasis * 0.60;
    } else {
      sec179Deduction = Math.min(price, luxuryCarCap);
      bonusDepreciation = 0;
    }

    const totalYear1Deduction = sec179Deduction + bonusDepreciation;
    const immediateTaxSavings = totalYear1Deduction * taxBracket;

    // 2. Financing Outlay
    let downPaymentAmount = 0;
    let financedPrincipal = 0;
    let monthlyPayment = 0;
    let year1LoanPayments = 0;
    let totalYear1CashOutlay = 0;

    if (!isLoan) {
      totalYear1CashOutlay = price;
    } else {
      downPaymentAmount = price * downPct;
      financedPrincipal = Math.max(0, price - downPaymentAmount);

      const r = ratePct / 12;
      if (r === 0) {
        monthlyPayment = financedPrincipal / termMonths;
      } else {
        const f = Math.pow(1 + r, termMonths);
        monthlyPayment = financedPrincipal * ((r * f) / (f - 1));
      }

      year1LoanPayments = monthlyPayment * activeMonths;
      totalYear1CashOutlay = downPaymentAmount + year1LoanPayments;
    }

    // Net Year 1 Cash Flow: Tax Savings minus Outlay ("Cash in Pocket")
    const netYear1CashFlow = immediateTaxSavings - totalYear1CashOutlay;
    const isCashPositive = netYear1CashFlow > 0;

    setMetric('res-immediate_tax_savings', formatUSD(immediateTaxSavings));
    setMetric('res-year1_cash_outlay', formatUSD(totalYear1CashOutlay));
    setMetric('res-net_cash_flow', (netYear1CashFlow >= 0 ? '+' : '') + formatUSD(netYear1CashFlow));
    setMetric('res-total_deduction', formatUSD(totalYear1Deduction));
    setMetric('res-sec179_deduction', formatUSD(sec179Deduction));
    setMetric('res-bonus_depreciation', formatUSD(bonusDepreciation));
    setMetric('res-monthly_payment', formatUSD(monthlyPayment) + '/mo');
    setMetric('res-down_payment', formatUSD(downPaymentAmount) + ` (${(downPct * 100).toFixed(0)}%)`);

    const cashFlowEl = document.getElementById('res-net_cash_flow');
    if (cashFlowEl) {
      cashFlowEl.style.color = isCashPositive ? 'var(--accent-emerald, #10b981)' : '#f59e0b';
    }

    const badgeEl = document.getElementById('res-cash_pocket_badge');
    if (badgeEl) {
      if (isCashPositive) {
        badgeEl.innerText = `+$${Math.round(netYear1CashFlow).toLocaleString()} Net Cash-in-Pocket Year 1`;
        badgeEl.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
        badgeEl.style.color = '#34d399';
      } else {
        badgeEl.innerText = `Net Outlay: $${Math.round(Math.abs(netYear1CashFlow)).toLocaleString()} in Year 1`;
        badgeEl.style.backgroundColor = 'rgba(245, 158, 11, 0.15)';
        badgeEl.style.color = '#f59e0b';
      }
    }

    // 5-Year Schedule Generation
    const tableBody = document.getElementById('sched-table-body');
    if (tableBody) {
      tableBody.innerHTML = '';
      let bal = financedPrincipal;
      const rMo = ratePct / 12;

      for (let y = 1; y <= 5; y++) {
        const moCount = y === 1 ? activeMonths : 12;
        let prinY = 0;
        let intY = 0;

        if (isLoan && bal > 0) {
          for (let m = 0; m < moCount; m++) {
            if (bal <= 0) break;
            const intMo = bal * rMo;
            const prinMo = Math.min(bal, monthlyPayment - intMo);
            bal = Math.max(0, bal - prinMo);
            prinY += prinMo;
            intY += intMo;
          }
        }

        const loanPmts = y === 1 ? downPaymentAmount + (prinY + intY) : (prinY + intY);
        const taxDed = y === 1 ? totalYear1Deduction + intY : intY;
        const taxSav = taxDed * taxBracket;
        const netFlow = taxSav - loanPmts;

        const row = document.createElement('tr');
        row.innerHTML = `
          <td style="padding:8px 12px; font-weight:700;">Year ${y}</td>
          <td style="padding:8px 12px;">${formatUSD(loanPmts)}</td>
          <td style="padding:8px 12px; color:#38bdf8;">${formatUSD(taxDed)}</td>
          <td style="padding:8px 12px; color:#34d399;">${formatUSD(taxSav)}</td>
          <td style="padding:8px 12px; font-weight:700; color:${netFlow >= 0 ? '#34d399' : '#cbd5e1'};">${(netFlow >= 0 ? '+' : '') + formatUSD(netFlow)}</td>
        `;
        tableBody.appendChild(row);
      }
    }

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Section 179 Equipment Tax Shield Verification]
Equipment Purchase Price: $${price.toLocaleString()} (${eqType})
Entity Tax Bracket: ${(taxBracket * 100).toFixed(0)}%
Section 179 Deduction: $${Math.round(sec179Deduction).toLocaleString()} | Bonus Depreciation: $${Math.round(bonusDepreciation).toLocaleString()}
Total Year 1 Tax Deduction: $${Math.round(totalYear1Deduction).toLocaleString()}
Immediate Cash Tax Savings: $${Math.round(immediateTaxSavings).toLocaleString()}
Financing Mode: ${isLoan ? `Commercial Loan (${(ratePct*100).toFixed(2)}%, ${termMonths} Mos)` : 'Cash Purchase'}
Year 1 Financing Outlay: $${Math.round(downPaymentAmount).toLocaleString()} down + $${Math.round(year1LoanPayments).toLocaleString()} payments = $${Math.round(totalYear1CashOutlay).toLocaleString()}
Net Year 1 Arbitrage ("Cash in Pocket"): ${(netYear1CashFlow >= 0 ? '+' : '')}$${Math.round(netYear1CashFlow).toLocaleString()}`;
    }
  }

  function copySummary() {
    const savings = document.getElementById('res-immediate_tax_savings')?.innerText || '$0';
    const outlay = document.getElementById('res-year1_cash_outlay')?.innerText || '$0';
    const netFlow = document.getElementById('res-net_cash_flow')?.innerText || '$0';
    const price = document.getElementById('param-equipment_price')?.value || '0';

    const text = `OmniOperand Section 179 Heavy Equipment Analysis:\n• Equipment Price: $${Number(price).toLocaleString()}\n• Immediate Year 1 Tax Shield Savings: ${savings}\n• Year 1 Financing Outlay: ${outlay}\n• Net Year 1 Cash-in-Pocket Benefit: ${netFlow}\nSource: https://omnioperand.com/calculators/section-179-equipment/`;

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
    const calc = document.getElementById('section-179-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveSection179);
        el.addEventListener('change', solveSection179);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveSection179();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
