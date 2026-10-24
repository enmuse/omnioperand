/**
 * assets/js/affiliate-engine.js
 * OmniOperand Contextual Monetization & High-Intent Conversion Engine
 * Evaluates live calculation thresholds and dynamically injects high-intent partner CTAs.
 * Safeguards Core Web Vitals with zero layout shift and verified nofollow sponsored links.
 */

(function () {
  'use strict';

  // Inline verified partner configuration (zero external latency or blocking)
  const AFFILIATE_DATA = {
    heloc: [
      {
        id: "heloc_rates",
        type: "heloc_card",
        url: "https://omnioperand.com/go/heloc-rates",
        check: () => true
      }
    ],

    construction: [
      {
        id: "contractor_dispatch",
        type: "construction_dispatch",
        url: "/dispatch/",
        check: () => true
      }
    ],

    mortgage: [
      {
        id: "lending_tree",
        name: "LendingTree",
        badge: "Top Refinance Network",
        headline: "Compare Verified Mortgage Lenders & Lock Lower Rates",
        cta: "See My Rates (Free)",
        url: "https://www.lendingtree.com/mortgage/?ref=omnioperand",
        disclosure: "NMLS #1130. Rates updated daily across 500+ top lenders.",
        check: (inputs, res) => (inputs.principal >= 150000) || (res.monthly_payment >= 1500)
      },
      {
        id: "rocket_mortgage",
        name: "Rocket Mortgage",
        badge: "Refinance Specialist",
        headline: "High Cumulative Interest: Save Up to $340/Mo by Refinancing",
        cta: "Calculate Refi Savings",
        url: "https://www.rocketmortgage.com/?ref=omnioperand",
        disclosure: "Equal Housing Lender. Savings based on credit qualification.",
        check: (inputs, res) => (res.total_interest >= 100000) || (inputs.rate >= 6.0)
      }
    ],

    auto_loan: [
      {
        id: "autopay",
        name: "AutoPay",
        badge: "Auto Refinance Leader",
        headline: "Lower Your Auto Loan Rate by Up to 3.5%",
        cta: "Check My Auto Rate",
        url: "https://www.autopay.com/?ref=omnioperand",
        disclosure: "Average borrower saves $1,400 over the remaining loan term.",
        check: (inputs, res) => (inputs.rate >= 5.0) || (res.total_interest >= 2500)
      }
    ],

    compound_interest: [
      {
        id: "marcus",
        name: "Marcus by Goldman Sachs",
        badge: "High-Yield Cash",
        headline: "Earn 4.40% APY on Your Cash Reserves — 10x National Average",
        cta: "Open High-Yield Savings",
        url: "https://www.marcus.com/?ref=omnioperand",
        disclosure: "Member FDIC. Maximize compounding with daily interest crediting.",
        check: (inputs, res) => (inputs.principal >= 2500)
      },
      {
        id: "vanguard",
        name: "Vanguard",
        badge: "Index Investing",
        headline: "Accelerate Compounding with 0.03% Expense Ratio Index Funds",
        cta: "Explore Low-Cost ETFs",
        url: "https://investor.vanguard.com/?ref=omnioperand",
        disclosure: "Investments subject to market risk. Past performance does not guarantee future results.",
        check: (inputs, res) => (res.future_value >= 25000)
      }
    ],

    concrete_volume: [
      {
        id: "contractor_dispatch",
        type: "construction_dispatch",
        url: "/dispatch/",
        check: () => true
      }
    ],

    roof_pitch: [
      {
        id: "contractor_dispatch",
        type: "construction_dispatch",
        url: "/dispatch/",
        check: () => true
      }
    ],

    geometry: [
      {
        id: "rockler_tools",
        name: "Rockler Woodworking & Hardware",
        badge: "Precision Tools",
        headline: "Digital Angle Finders & Miter Gauges for Flawless Polygonal Joinery",
        cta: "Shop Precision Tools",
        url: "https://www.rockler.com/?ref=omnioperand",
        disclosure: "Engineered for 22.5° octagon and 30° hexagon airtight joints.",
        check: () => true
      }
    ],

    islamic_finance: [
      {
        id: "guidance_residential",
        name: "Guidance Residential",
        badge: "Shariah Leader",
        headline: "Pre-Qualify for AAOIFI-Compliant Declining Balance Home Financing",
        cta: "Check Shariah Rates",
        url: "https://www.guidanceresidential.com/?ref=omnioperand",
        disclosure: "NMLS #8317. Strict Diminishing Musharaka co-ownership with zero compounding interest.",
        check: () => true
      },
      {
        id: "uif_corp",
        name: "UIF Corporation",
        badge: "AAOIFI Compliant",
        headline: "Nationwide Murabaha & Ijara Residential Financing",
        cta: "See UIF Financing",
        url: "https://www.myuif.com/?ref=omnioperand",
        disclosure: "Endorsed by leading North American Islamic Jurisprudence & Fatwa Councils.",
        check: () => true
      }
    ],

    itin_mortgage: [
      {
        id: "new_american_funding_itin",
        name: "New American Funding",
        badge: "Top ITIN Lender",
        headline: "Check ITIN Mortgage Rates & Down Payment Options (No SSN Required)",
        cta: "View ITIN Rates",
        url: "https://www.newamericanfunding.com/mortgage-loans/itin-loans/?ref=omnioperand",
        disclosure: "Equal Housing Lender. NMLS #6606. Accepts consular cards, ITIN letters, and W-2/1099.",
        check: () => true
      }
    ],

    credit_card_payoff: [
      {
        id: "consolidation_zero_apr",
        name: "LendingTree Balance Transfer",
        badge: "Interest Elimination",
        headline: "Warning: High Cumulative Interest Detected. Compare 0% APR Balance Transfer Cards",
        cta: "Compare 0% APR Cards",
        url: "https://www.lendingtree.com/credit-cards/balance-transfer/?ref=omnioperand",
        disclosure: "Save hundreds in interest charges by consolidating high-rate balances at 0% intro APR.",
        check: (inputs, res) => (inputs.interest_rate >= 18.0) || (res.total_interest >= 1000)
      }
    ]
  };

  class AffiliateEngine {
    constructor() {
      this.init();
    }

    init() {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => this.setup());
      } else {
        this.setup();
      }
    }

    setup() {
      this.bindCalculatorTarget();
    }

    getCategoryFromPage() {
      const path = window.location.pathname.toLowerCase();
      if (path.includes('islamic') || path.includes('musharaka') || path.includes('murabaha') || path.includes('ijara')) return 'islamic_finance';
      if (path.includes('itin')) return 'itin_mortgage';
      if (path.includes('credit-card') || path.includes('payoff') || path.includes('debt')) return 'credit_card_payoff';
      if (path.includes('heloc')) return 'heloc';
      if (path.includes('mortgage')) return 'mortgage';
      if (path.includes('auto-loan')) return 'auto_loan';
      if (path.includes('compound-interest') || path.includes('cagr')) return 'compound_interest';
      if (path.includes('/construction/') || path.includes('concrete') || path.includes('excavation') || path.includes('grading') || path.includes('retaining-wall') || path.includes('asphalt') || path.includes('deck') || path.includes('roofing') || path.includes('gravel') || path.includes('mulch') || path.includes('pavers')) return 'construction';
      if (path.includes('roof-pitch')) return 'roof_pitch';
      if (path.includes('geometry') || path.includes('shape') || path.includes('octagon')) return 'geometry';
      return null;
    }

    findMatchingPartner(category, inputs = {}, results = {}) {
      const list = AFFILIATE_DATA[category];
      if (!list || list.length === 0) return null;

      for (const p of list) {
        try {
          if (typeof p.check === 'function' && p.check(inputs, results)) {
            return p;
          }
        } catch (_) {}
      }
      return list[0];
    }

    injectPartnerCard(container, partner) {
      if (!container || !partner) return;
      if (container.getAttribute('data-active-partner') === partner.id && container.children.length > 0) return;

      container.setAttribute('data-active-partner', partner.id);

      if (partner.type === 'heloc_card') {
        container.innerHTML = `
<div class="contextual-action-card" style="background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.25); border-radius:10px; padding:1.25rem; margin-top:1.25rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap;">
    <div>
      <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; color:#38bdf8; font-weight:700; margin-bottom:0.25rem;">Verified Rate Comparison</div>
      <div style="font-size:0.95rem; font-weight:700; color:#fff;">Compare Live HELOC Rates for Your $<span id="rec-draw-balance">75,000</span> Balance</div>
      <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.2rem;">Lending partners offer fixed-rate draw conversions with zero closing costs.</div>
    </div>
    <a href="${partner.url}" rel="nofollow sponsored" target="_blank" class="btn-primary" style="padding:0.6rem 1.25rem; font-size:0.88rem;">
      View Top Rates →
    </a>
  </div>
</div>`;
        return;
      }

      if (partner.type === 'construction_dispatch') {
        container.innerHTML = `
<div class="contractor-dispatch-callout" style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:10px; padding:1.25rem; margin-top:1.25rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap;">
    <div>
      <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; color:#34d399; font-weight:700; margin-bottom:0.25rem;">Equipment & Crew Dispatch</div>
      <div style="font-size:0.95rem; font-weight:700; color:#fff;">Need Machine Execution for This Project?</div>
      <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.2rem;">Connect with verified regional equipment operators and heavy civil crews.</div>
    </div>
    <a href="${partner.url}" class="btn-secondary" style="padding:0.6rem 1.25rem; font-size:0.88rem; border-color:rgba(16,185,129,0.4); color:#6ee7b7;">
      Request Local Crew Dispatch →
    </a>
  </div>
</div>`;
        return;
      }

      container.innerHTML = `
        <div class="omni-affiliate-card">
          <div class="omni-affiliate-top">
            <span class="omni-affiliate-badge">${partner.badge}</span>
            <span class="omni-affiliate-partner-name">${partner.name}</span>
          </div>
          <h4 class="omni-affiliate-headline">${partner.headline}</h4>
          <div class="omni-affiliate-action-row">
            <a href="${partner.url}" target="_blank" rel="nofollow sponsored" class="omni-affiliate-btn">
              <span>${partner.cta}</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </a>
            <span class="omni-affiliate-disclosure">${partner.disclosure}</span>
          </div>
        </div>
      `;
    }

    evaluate(inputs = {}, results = {}) {
      const cat = this.getCategoryFromPage();
      if (!cat) return;

      const partner = this.findMatchingPartner(cat, inputs, results);
      if (!partner) return;

      const target = document.getElementById('affiliate-recommendation-target');
      if (target) {
        this.injectPartnerCard(target, partner);

        // Update dynamic balance if present
        const balanceEl = document.getElementById('rec-draw-balance');
        if (balanceEl) {
          const val = inputs.line_amount || inputs.principal || document.getElementById('param-line_amount')?.value;
          if (val) {
            const num = parseFloat(String(val).replace(/[^0-9.-]+/g, ''));
            if (!isNaN(num)) {
              balanceEl.innerText = Math.round(num).toLocaleString();
            }
          }
        }
      }
    }

    bindCalculatorTarget() {
      this.evaluate();

      window.addEventListener('omni:calculated', (e) => {
        if (e.detail) {
          this.evaluate(e.detail.inputs || {}, e.detail.results || {});
        }
      });
    }
  }

  // Global instantiate
  window.OmniAffiliateEngine = new AffiliateEngine();
})();
