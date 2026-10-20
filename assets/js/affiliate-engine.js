/**
 * assets/js/affiliate-engine.js
 * OmniOperand Contextual Monetization & Affiliate Recommendation Engine
 * Evaluates live calculation thresholds and dynamically injects high-intent partner CTAs.
 * Safeguards Core Web Vitals with CLS-prevented responsive ad containers.
 */

(function () {
  'use strict';

  // Fallback inline partner config (ensures zero external latency or blocking)
  const AFFILIATE_DATA = {
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
        id: "ready_mix",
        name: "Ready-Mix Dispatch",
        badge: "Pro Contractor Tip",
        headline: "Large Pour (>3 cu yds): Order Ready-Mix Delivery Instead of 150+ Bags",
        cta: "Get Instant Concrete Truck Quote",
        url: "https://www.homedepot.com/c/concrete_supplies?ref=omnioperand",
        disclosure: "Hand-mixing more than 50 bags risks cold joints and structural failure.",
        check: (inputs, res) => (res.cu_yards >= 3.0) || (res.bags_80lb >= 120)
      }
    ],

    roof_pitch: [
      {
        id: "modernize_roofing",
        name: "Modernize Home Services",
        badge: "Vetted Roofers",
        headline: "Compare Top Local Roofing Contractors & Material Warranties",
        cta: "Get 3 Free Estimates",
        url: "https://modernize.com/roofing?ref=omnioperand",
        disclosure: "Free estimates with no obligation. All contractors are verified.",
        check: (inputs, res) => true
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
    ]
  };

  class AffiliateEngine {
    constructor() {
      this.activePartner = null;
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
      this.setupAdPlaceholders();
      this.bindCalculatorTarget();
    }

    getCategoryFromPage() {
      const path = window.location.pathname.toLowerCase();
      if (path.includes('mortgage')) return 'mortgage';
      if (path.includes('auto-loan')) return 'auto_loan';
      if (path.includes('compound-interest') || path.includes('cagr')) return 'compound_interest';
      if (path.includes('concrete')) return 'concrete_volume';
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
      return list[0]; // fallback to first partner in category
    }

    injectPartnerCard(container, partner) {
      if (!container || !partner) return;
      if (container.getAttribute('data-active-partner') === partner.id) return;

      container.setAttribute('data-active-partner', partner.id);
      container.innerHTML = `
        <div class="omni-affiliate-card">
          <div class="omni-affiliate-top">
            <span class="omni-affiliate-badge">${partner.badge}</span>
            <span class="omni-affiliate-partner-name">${partner.name}</span>
          </div>
          <h4 class="omni-affiliate-headline">${partner.headline}</h4>
          <div class="omni-affiliate-action-row">
            <a href="${partner.url}" target="_blank" rel="noopener sponsored" class="omni-affiliate-btn">
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
      }
    }

    bindCalculatorTarget() {
      // Run initial check
      this.evaluate();

      // Listen for custom calculation events if fired by solvers
      window.addEventListener('omni:calculated', (e) => {
        if (e.detail) {
          this.evaluate(e.detail.inputs || {}, e.detail.results || {});
        }
      });
    }

    // CLS-Safe Ad Slot Placeholders
    setupAdPlaceholders() {
      const adSlots = document.querySelectorAll('.omni-ad-slot');
      if (!adSlots || adSlots.length === 0) return;

      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const slot = entry.target;
              observer.unobserve(slot);
              this.hydrateAdSlot(slot);
            }
          });
        }, { rootMargin: '200px' });

        adSlots.forEach(slot => observer.observe(slot));
      } else {
        adSlots.forEach(slot => this.hydrateAdSlot(slot));
      }
    }

    hydrateAdSlot(slot) {
      // If ad script is not present, fall back to house promo / affiliate partner
      const cat = this.getCategoryFromPage() || 'geometry';
      const partner = this.findMatchingPartner(cat) || AFFILIATE_DATA.geometry[0];

      if (!slot.querySelector('.omni-affiliate-card') && !slot.hasAttribute('data-ad-filled')) {
        slot.setAttribute('data-ad-filled', 'true');
        slot.innerHTML = `
          <div class="omni-ad-fallback">
            <span class="omni-ad-tag">SPONSORED PARTNER</span>
            <div class="omni-ad-fallback-content">
              <strong>${partner.name}:</strong> ${partner.headline}
            </div>
            <a href="${partner.url}" target="_blank" rel="noopener sponsored" class="omni-ad-fallback-cta">
              ${partner.cta} →
            </a>
          </div>
        `;
      }
    }
  }

  // Instantiate globally
  window.OmniAffiliateEngine = new AffiliateEngine();
})();
