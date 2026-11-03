/**
 * assets/js/therapy-practice-solver.js
 * OmniOperand Private Practice Breakeven Client Engine: Cash-Pay vs. Insurance Credentialing
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

  function solveTherapyPractice() {
    const targetNet = getNum('param-target_net_income', 120000);
    const weeks = Math.max(1, Math.min(52, getNum('param-weeks_worked', 48)));
    const cashFee = Math.max(1, getNum('param-cash_fee', 150));
    const insRate = Math.max(1, getNum('param-insurance_rate', 105));
    const denialPct = getNum('param-denial_rate', 8) / 100;
    const billingPct = getNum('param-billing_fee', 6) / 100;
    const insAdminMins = getNum('param-insurance_admin_mins', 20);
    const cashAdminMins = 5;
    const clinicalMins = 50;
    const overhead = getNum('param-fixed_overhead', 14000);

    const totalRevenueRequired = targetNet + overhead;

    // 1. Cash Model
    const cashEffectiveRate = cashFee;
    const cashSessionsYear = Math.ceil(totalRevenueRequired / cashEffectiveRate);
    const cashSessionsWeek = cashSessionsYear / weeks;
    const cashClinicalHoursWeek = (cashSessionsWeek * clinicalMins) / 60;
    const cashAdminHoursWeek = (cashSessionsWeek * cashAdminMins) / 60;
    const cashTotalHoursWeek = cashClinicalHoursWeek + cashAdminHoursWeek;
    const cashAnnualAdminHours = (cashSessionsYear * cashAdminMins) / 60;

    // 2. Insurance Model
    const insEffectiveRate = insRate * (1 - denialPct) * (1 - billingPct);
    const insSessionsYear = Math.ceil(totalRevenueRequired / Math.max(1, insEffectiveRate));
    const insSessionsWeek = insSessionsYear / weeks;
    const insClinicalHoursWeek = (insSessionsWeek * clinicalMins) / 60;
    const insAdminHoursWeek = (insSessionsWeek * insAdminMins) / 60;
    const insTotalHoursWeek = insClinicalHoursWeek + insAdminHoursWeek;
    const insAnnualAdminHours = (insSessionsYear * insAdminMins) / 60;

    // 3. Comparisons
    const extraHoursWeek = insTotalHoursWeek - cashTotalHoursWeek;
    const annualAdminDiff = insAnnualAdminHours - cashAnnualAdminHours;
    const opportunityCost = annualAdminDiff * cashFee;

    const headline = `You must work ${insTotalHoursWeek.toFixed(1)} hours/week on Insurance vs. ${cashTotalHoursWeek.toFixed(1)} hours/week on Cash to take home the exact same ${formatUSD(targetNet)} income.`;

    const headlineEl = document.getElementById('res-comparison_headline');
    if (headlineEl) headlineEl.innerText = headline;

    setMetric('res-cash_sessions_week', `${cashSessionsWeek.toFixed(1)} sessions/wk`);
    setMetric('res-ins_sessions_week', `${insSessionsWeek.toFixed(1)} sessions/wk`);
    setMetric('res-cash_hours_week', `${cashTotalHoursWeek.toFixed(1)} hrs/wk`);
    setMetric('res-ins_hours_week', `${insTotalHoursWeek.toFixed(1)} hrs/wk`);
    setMetric('res-extra_hours_week', `+${extraHoursWeek.toFixed(1)} hrs/wk`);
    setMetric('res-ins_effective_rate', `$${insEffectiveRate.toFixed(2)} / session`);
    setMetric('res-annual_admin_hours', `${Math.round(insAnnualAdminHours)} hrs / yr`);
    setMetric('res-unpaid_admin_diff', `${Math.round(annualAdminDiff)} unpaid hrs / yr`);
    setMetric('res-opportunity_cost', formatUSD(opportunityCost) + ' / yr');

    // Dynamic AI prompt generator sync
    const promptEl = document.getElementById('llm-prompt-display');
    if (promptEl) {
      promptEl.innerText = `[OmniOperand Mental Health Practice Economics Verification]
Target Take-Home Salary: $${targetNet.toLocaleString()} | Fixed Practice Overhead: $${overhead.toLocaleString()}
Total Gross Annual Revenue Needed: $${totalRevenueRequired.toLocaleString()} across ${weeks} active weeks
1. Cash-Pay Model:
   - Fee: $${cashFee}/session | Annual Sessions Needed: ${cashSessionsYear} (${cashSessionsWeek.toFixed(1)}/wk)
   - Weekly Hours: ${cashClinicalHoursWeek.toFixed(1)} clinical + ${cashAdminHoursWeek.toFixed(1)} admin = ${cashTotalHoursWeek.toFixed(1)} hrs/week
2. Insurance Credentialed Model:
   - Nominal Rate: $${insRate} | Denial Rate: ${(denialPct*100).toFixed(0)}% | Billing Fee: ${(billingPct*100).toFixed(0)}%
   - Effective Collected Rate: $${insEffectiveRate.toFixed(2)}/session | Annual Sessions Needed: ${insSessionsYear} (${insSessionsWeek.toFixed(1)}/wk)
   - Weekly Hours: ${insClinicalHoursWeek.toFixed(1)} clinical + ${insAdminHoursWeek.toFixed(1)} admin = ${insTotalHoursWeek.toFixed(1)} hrs/week
Outcome Disparity: Provider must work +${extraHoursWeek.toFixed(1)} additional hours/week on insurance (${Math.round(annualAdminDiff)} unpaid billing hours/year, generating $${Math.round(opportunityCost).toLocaleString()} in lost opportunity cost).`;
    }
  }

  function copySummary() {
    const headline = document.getElementById('res-comparison_headline')?.innerText || '';
    const adminDiff = document.getElementById('res-unpaid_admin_diff')?.innerText || '';
    const oppCost = document.getElementById('res-opportunity_cost')?.innerText || '';

    const text = `OmniOperand Therapy Private Practice Analysis:\n• ${headline}\n• Unpaid Admin Documentation Burden: ${adminDiff}\n• Annual Opportunity Cost: ${oppCost}\nSource: https://omnioperand.com/calculators/therapy-private-practice-breakeven/`;

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
    const calc = document.getElementById('therapy-practice-calculator');
    if (calc) {
      calc.querySelectorAll('input').forEach(el => {
        el.addEventListener('input', solveTherapyPractice);
        el.addEventListener('change', solveTherapyPractice);
      });

      const copyBtn = document.getElementById('btn-copy-summary');
      if (copyBtn) copyBtn.addEventListener('click', copySummary);

      const printBtn = document.getElementById('btn-print-pdf');
      if (printBtn) printBtn.addEventListener('click', () => window.print());

      solveTherapyPractice();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
