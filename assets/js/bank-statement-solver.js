/**
 * assets/js/bank-statement-solver.js
 * OmniOperand 12/24-Month Bank Statement Loan Client Engine
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

  function solveBankStatement() {
    const methodEl = document.querySelector('input[name="calc_method"]:checked');
    const months = methodEl ? parseInt(methodEl.value, 10) : 12;

    const accountTypeEl = document.querySelector('input[name="account_type"]:checked');
    const isPersonal = accountTypeEl ? accountTypeEl.value === 'personal' : false;

    const deposits = getNum('param-gross_deposits', 360000);
    const customExpensePct = getNum('param-expense_ratio', isPersonal ? 0 : 50);
    const expenseRatioPct = isPersonal ? 0 : Math.max(0, Math.min(100, customExpensePct));

    // Update expense ratio display if disabled or changed
    const expenseInput = document.getElementById('param-expense_ratio');
    if (expenseInput && isPersonal) {
      expenseInput.value = 0;
      expenseInput.disabled = true;
    } else if (expenseInput) {
      expenseInput.disabled = false;
    }

    const monthlyDebts = getNum('param-monthly_debts', 800);
    const maxDtiPct = getNum('param-max_dti', 50) / 100;
    const ratePct = getNum('param-interest_rate', 7.5) / 100;
    const termYears = getNum('param-loan_term_years', 30);
    const downPct = getNum('param-down_payment_pct', 20) / 100;

    const totalQualifyingRevenue = deposits * (1 - expenseRatioPct / 100);
    const monthlyQualifyingIncome = totalQualifyingRevenue / months;
    const benchmarkTaxReturn = monthlyQualifyingIncome * 0.38; // Typical net taxable write-down

    const maxAllowableTotalDebt = monthlyQualifyingIncome * maxDtiPct;
    const maxAllowableHousingExpense = Math.max(0, maxAllowableTotalDebt - monthlyDebts);

    const r = ratePct / 12;
    const n = termYears * 12;
    const m1 = r > 0 ? (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) : (1 / n);
    const e1 = 0.015 / 12; // 1.5% annual tax + ins factor

    const kPrice = (1 - downPct) * m1 + e1;
    let maxPurchasePower = 0;
    let maxLoanAmount = 0;
    let downPaymentAmount = 0;
    let estMonthlyPI = 0;

    if (kPrice > 0 && maxAllowableHousingExpense > 0) {
      maxPurchasePower = maxAllowableHousingExpense / kPrice;
      maxLoanAmount = maxPurchasePower * (1 - downPct);
      downPaymentAmount = maxPurchasePower * downPct;
      estMonthlyPI = maxLoanAmount * m1;
    }

    setMetric('res-qualifying_monthly_income', formatUSD(monthlyQualifyingIncome));
    setMetric('res-tax_return_comparison', formatUSD(benchmarkTaxReturn));
    setMetric('res-max_purchase_power', formatUSD(maxPurchasePower));
    setMetric('res-max_loan_amount', formatUSD(maxLoanAmount));
    setMetric('res-down_payment_needed', formatUSD(downPaymentAmount) + ` (${(downPct * 100).toFixed(0)}%)`);
    setMetric('res-max_housing_expense', formatUSD(maxAllowableHousingExpense) + '/mo');
    setMetric('res-total_debt_limit', formatUSD(maxAllowableTotalDebt) + '/mo');
    setMetric('res-estimated_monthly_pi', formatUSD(estMonthlyPI));

    const advantageMultiplier = benchmarkTaxReturn > 0 ? (monthlyQualifyingIncome / benchmarkTaxReturn).toFixed(1) : '2.6';
    setMetric('res-advantage_ratio', `${advantageMultiplier}x Borrowing Advantage`);

    // DTI Gauge calculation
    const dtiBar = document.getElementById('dti-gauge-fill');
    if (dtiBar) {
      dtiBar.style.width = `${Math.min(100, (maxDtiPct * 100))}%`;
    }

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Bank Statement Loan Underwriting Verification]
Calculation Method: ${months}-Month Average (${isPersonal ? 'Personal Checking' : 'Business Checking'})
Total Gross Bank Deposits: $${deposits.toLocaleString()}
Expense Ratio: ${expenseRatioPct}% | Total Qualifying Revenue: $${Math.round(totalQualifyingRevenue).toLocaleString()}
Monthly Qualifying Income: $${Math.round(monthlyQualifyingIncome).toLocaleString()}/mo (vs. $${Math.round(benchmarkTaxReturn).toLocaleString()}/mo tax return benchmark)
Existing Monthly Personal Debts: $${monthlyDebts.toLocaleString()}/mo
Max Allowable DTI: ${(maxDtiPct * 100).toFixed(0)}% | Max Allowable Housing PITIA: $${Math.round(maxAllowableHousingExpense).toLocaleString()}/mo
Target Loan Parameters: ${(ratePct * 100).toFixed(2)}% APR, ${termYears} Yrs, ${(downPct * 100).toFixed(0)}% Down
Maximum Backsolved Home Purchasing Power: $${Math.round(maxPurchasePower).toLocaleString()}
Max Loan Amount: $${Math.round(maxLoanAmount).toLocaleString()} | Down Payment: $${Math.round(downPaymentAmount).toLocaleString()}`;
    }
  }

  function copySummary() {
    const income = document.getElementById('res-qualifying_monthly_income')?.innerText || '$0';
    const power = document.getElementById('res-max_purchase_power')?.innerText || '$0';
    const pitia = document.getElementById('res-max_housing_expense')?.innerText || '$0';
    const deposits = document.getElementById('param-gross_deposits')?.value || '0';

    const text = `OmniOperand Bank Statement Mortgage Analysis:\n• Gross Deposits: $${Number(deposits).toLocaleString()}\n• Monthly Qualifying Income: ${income}\n• Max Home Purchasing Power: ${power}\n• Max Allowable Housing PITIA: ${pitia}\nSource: https://omnioperand.com/calculators/bank-statement-mortgage/`;

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
    const calc = document.getElementById('bank-statement-calculator');
    if (calc) {
      calc.querySelectorAll('input, select').forEach(el => {
        el.addEventListener('input', solveBankStatement);
        el.addEventListener('change', solveBankStatement);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveBankStatement();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
