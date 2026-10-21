"""
scripts/data_legal_insurance.py
25 High-Value Legal, Insurance, Torts & Actuarial Damages Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

LEGAL_CALCULATORS = [
    {
        "slug": "personal-injury-multiplier",
        "category": "legal",
        "name": "Personal Injury Settlement Multiplier Calculator",
        "description": "Calculate estimated car accident and bodily injury insurance claim settlement value using the insurance adjuster multiplier method.",
        "hero_badge": "Personal Injury • Settlement Valuation",
        "formula_display": "Settlement Value = (Medical Bills + Lost Wages) + (Multiplier × Medical Special Damages)",
        "fields": [
            {"id": "medical_specials_usd", "label": "Total Past Medical Bills ($ USD)", "default": 18500, "prefix": "$", "min": 500, "max": 1000000, "step": 500, "hint": "Emergency room, surgery, imaging, physical therapy"},
            {"id": "future_medical_usd", "label": "Estimated Future Medical Expenses ($)", "default": 6500, "prefix": "$", "min": 0, "max": 1000000, "step": 500, "hint": "Future injections, revision surgery, rehab"},
            {"id": "lost_earnings_usd", "label": "Lost Wages & Earnings ($)", "default": 5200, "prefix": "$", "min": 0, "max": 500000, "step": 250, "hint": "Documented missed work days and sick leave used"},
            {"id": "injury_severity_tier", "label": "Injury Severity Multiplier (1.5x Minor to 5.0x Severe)", "default": 2.5, "suffix": "x", "min": 1.5, "max": 5.0, "step": 0.25, "hint": "Soft tissue ~1.5-2x, Broken bone ~2.5-3x, Spine surgery ~4-5x"}
        ],
        "metrics": [
            {"id": "estimated_settlement_range", "label": "Estimated Settlement Range", "default_display": "$85,000.00 – $105,000.00", "highlight": True},
            {"id": "total_special_damages", "label": "Total Economic Special Damages", "default_display": "$30,200.00", "highlight": True},
            {"id": "pain_suffering_component", "label": "Pain & Suffering General Damages", "default_display": "$62,500.00 (2.5x)"},
            {"id": "attorney_contingency_cut", "label": "Est. Attorney Fee (33.3% Contingency)", "default_display": "$30,800.00"}
        ],
        "proof_steps": [
            {"step_title": "Economic Special Damages Summation", "step_text": "Specials = Past Medical ($18,500) + Future Medical ($6,500) + Lost Wages ($5,200) = $30,200.00."},
            {"step_title": "General Damages Multiplier Formulation", "step_text": "Insurance adjusters calculate non-economic pain and suffering by applying a multiplier to medical specials. Pain & Suffering = ($18,500 + $6,500) × 2.5 = $62,500.00."},
            {"step_title": "Gross Settlement Range", "step_text": "Baseline Settlement = Special Damages ($30,200) + General Damages ($62,500) = $92,700.00 (typically negotiating between $85k and $105k depending on liability clarity and policy limits)."}
        ],
        "faqs": [
            {"q": "What factors determine the personal injury multiplier?", "a": "Key factors include: severity and permanency of injury (fractures vs whiplash), objective diagnostic imaging (MRI findings), duration of physical therapy, disruption of daily activities, and clear liability fault of the defendant."},
            {"q": "Can a settlement exceed the defendant's auto insurance policy limits?", "a": "Settlements are practically capped by the defendant's bodily injury liability policy limits (e.g. $50,000 or $100,000) unless you carry Underinsured Motorist (UIM) coverage or the defendant has personal attachable assets."}
        ],
        "js_logic": """
          const pastMed = getNum('medical_specials_usd');
          const futMed = getNum('future_medical_usd');
          const wages = getNum('lost_earnings_usd');
          const mult = getNum('injury_severity_tier') || 2.5;

          const totalMed = pastMed + futMed;
          const specials = totalMed + wages;
          const painSuffering = totalMed * mult;
          const baseline = specials + painSuffering;

          const low = baseline * 0.90;
          const high = baseline * 1.15;
          const atty = baseline * 0.3333;

          setDisp('estimated_settlement_range', '$' + Math.round(low).toLocaleString() + ' – $' + Math.round(high).toLocaleString());
          setDisp('total_special_damages', '$' + Math.round(specials).toLocaleString());
          setDisp('pain_suffering_component', '$' + Math.round(painSuffering).toLocaleString() + ' (' + mult.toFixed(1) + 'x)');
          setDisp('attorney_contingency_cut', '$' + Math.round(atty).toLocaleString());
        """
    },
    {
        "slug": "pain-and-suffering-valuation",
        "category": "legal",
        "name": "Pain and Suffering Damages Valuation Calculator (Per Diem vs Multiplier)",
        "description": "Calculate non-economic pain and suffering damages using both the daily Per Diem method and the Insurance Multiplier method for personal injury demand letters.",
        "hero_badge": "Tort Law • Non-Economic Damages",
        "formula_display": "Per Diem Total = Number of Recovery Days × Daily Earnings Rate",
        "fields": [
            {"id": "recovery_duration_days", "label": "Duration of Pain / Medical Treatment (Days)", "default": 180, "suffix": "days", "min": 14, "max": 1825, "step": 10, "hint": "Days from accident until Maximum Medical Improvement (MMI)"},
            {"id": "daily_per_diem_rate", "label": "Daily Per Diem Rate ($/Day)", "default": 225, "prefix": "$", "min": 50, "max": 1500, "step": 25, "hint": "Typically equals one full day of victim's regular daily wage earnings"},
            {"id": "medical_specials_usd", "label": "Total Hard Medical Specials ($)", "default": 14500, "prefix": "$", "min": 1000, "max": 500000, "step": 500, "hint": "Doctor bills and physical therapy costs"}
        ],
        "metrics": [
            {"id": "per_diem_total_damages", "label": "Per Diem Total Valuation", "default_display": "$40,500.00", "highlight": True},
            {"id": "multiplier_equivalent_valuation", "label": "Multiplier Method Equivalent (2.8x)", "default_display": "$40,600.00", "highlight": True},
            {"id": "recommended_demand_amount", "label": "Recommended Settlement Demand", "default_display": "$55,000.00 (Specials + Pain)"},
            {"id": "implied_multiplier", "label": "Implied Special Damages Multiplier", "default_display": "2.79x Multiplier"}
        ],
        "proof_steps": [
            {"step_title": "Per Diem Jurisprudence", "step_text": "The Per Diem ('per day') approach argues before a jury that enduring pain, sleep loss, and reduced mobility is worth at least one full day's regular wage: 180 days × $225/day = $40,500.00."},
            {"step_title": "Multiplier Cross-Validation", "step_text": "Implied Multiplier = Per Diem Pain / Medical Specials = $40,500 / $14,500 = 2.79x. In moderate injury claims, a 2.5x to 3.0x multiplier aligns closely with jury verdicts."},
            {"step_title": "Total Demand Formulation", "step_text": "Comprehensive Demand = Medical Specials ($14,500) + Pain & Suffering ($40,500) = $55,000.00."}
        ],
        "faqs": [
            {"q": "What is the Per Diem method in a personal injury trial?", "a": "Attorneys ask the jury to assign a daily dollar value (often the plaintiff's daily earnings, e.g. $200/day) to the physical pain and emotional suffering endured, multiplying that rate by the number of days between the crash and maximum medical recovery."},
            {"q": "Do all states allow the Per Diem argument in court?", "a": "Most states permit the per diem argument, but some jurisdictions (e.g. New Jersey, Pennsylvania, and federal courts) restrict attorneys from suggesting specific daily dollar figures to juries, leaving valuation strictly to jury discretion."}
        ],
        "js_logic": """
          const days = getNum('recovery_duration_days');
          const perDiem = getNum('daily_per_diem_rate');
          const meds = getNum('medical_specials_usd');

          const perDiemTotal = days * perDiem;
          const impliedMult = meds > 0 ? (perDiemTotal / meds) : 2.5;
          const totalDemand = meds + perDiemTotal;

          setDisp('per_diem_total_damages', '$' + Math.round(perDiemTotal).toLocaleString());
          setDisp('multiplier_equivalent_valuation', '$' + Math.round(meds * impliedMult).toLocaleString() + ' (' + impliedMult.toFixed(1) + 'x)');
          setDisp('recommended_demand_amount', '$' + Math.round(totalDemand).toLocaleString());
          setDisp('implied_multiplier', impliedMult.toFixed(2) + 'x Multiplier');
        """
    },
    {
        "slug": "structured-settlement-npv",
        "category": "legal",
        "name": "Structured Settlement Annuity Lump-Sum Present Value (NPV)",
        "description": "Calculate fair market cash lump-sum present value (NPV) and purchasing company discount factoring haircut when selling structured settlement annuity payments.",
        "hero_badge": "Settlement Finance • Present Value",
        "formula_display": "NPV = Σ [Monthly Payment / (1 + r / 12)ᵗ] | Discount Rate r typically 8% - 15%",
        "fields": [
            {"id": "monthly_annuity_payment", "label": "Monthly Annuity Payment ($)", "default": 1750, "prefix": "$", "min": 100, "max": 25000, "step": 50, "hint": "Guaranteed tax-free structured settlement payment"},
            {"id": "remaining_payment_years", "label": "Remaining Payment Duration (Years)", "default": 15, "suffix": "yrs", "min": 1, "max": 40, "step": 1, "hint": "Years of guaranteed annuity payments remaining"},
            {"id": "purchaser_discount_rate_pct", "label": "Factoring Company Discount Rate (%)", "default": 11.5, "suffix": "%", "min": 4.0, "max": 25.0, "step": 0.5, "hint": "Annual discount rate quoted by settlement buyer (typically 9% - 14%)"}
        ],
        "metrics": [
            {"id": "lump_sum_cash_offer", "label": "Fair Net Lump-Sum Cash Offer", "default_display": "$149,420.00", "highlight": True},
            {"id": "total_nominal_payments", "label": "Total Future Guaranteed Payments", "default_display": "$315,000.00", "highlight": True},
            {"id": "effective_discount_haircut", "label": "Discount Haircut Surrendered", "default_display": "52.6% Lost to Discounting ($165,580)"},
            {"id": "fair_court_benchmark", "label": "Judicial Approval Fairness Assessment", "default_display": "Reasonable Rate for Structured Buyout"}
        ],
        "proof_steps": [
            {"step_title": "Total Nominal Value Summation", "step_text": "Total Payments = 15 years × 12 months × $1,750 = 180 payments = $315,000.00."},
            {"step_title": "Discounted Cash Flow (DCF) Integration", "step_text": "Present Value PV = PMT · [(1 - (1 + i)⁻ⁿ) / i], where monthly discount i = 11.5% / 12 = 0.009583 and n = 180."},
            {"step_title": "Lump-Sum Present Value", "step_text": "PV = $1,750 · [(1 - (1.009583)⁻¹⁸⁰) / 0.009583] = $1,750 · 85.38 = $149,420.00."},
            {"step_title": "Surrendered Wealth Quantification", "step_text": "Selling today sacrifices $165,580 in guaranteed tax-free income in exchange for immediate liquidity."}
        ],
        "faqs": [
            {"q": "Why does a judge have to approve selling a structured settlement?", "a": "Under the Structured Settlement Protection Act, state courts must review all transfers to verify that the discount rate is fair and that selling payments serves the payee's immediate financial best interests without leaving them destitute."},
            {"q": "Are structured settlement payments tax-free?", "a": "Yes! Under Section 104(a)(2) of the Internal Revenue Code, 100% of physical injury structured settlement payments (both principal and accumulated interest earnings) are exempt from federal and state income tax."}
        ],
        "js_logic": """
          const pmt = getNum('monthly_annuity_payment');
          const yrs = getNum('remaining_payment_years');
          const disc = (getNum('purchaser_discount_rate_pct') || 11.5) / 100;

          const n = yrs * 12;
          const r = disc / 12;
          const totalNominal = pmt * n;
          const pv = r > 0 ? (pmt * (1 - Math.pow(1 + r, -n)) / r) : totalNominal;
          const haircut = totalNominal - pv;
          const haircutPct = totalNominal > 0 ? (haircut / totalNominal) * 100 : 0;

          setDisp('lump_sum_cash_offer', '$' + Math.round(pv).toLocaleString());
          setDisp('total_nominal_payments', '$' + Math.round(totalNominal).toLocaleString());
          setDisp('effective_discount_haircut', haircutPct.toFixed(1) + '% Lost ($' + Math.round(haircut).toLocaleString() + ')');
          setDisp('fair_court_benchmark', disc <= 0.12 ? 'Favorable Rate (Likely Court Approval)' : 'High Discount (Scrutiny Expected)');
        """
    },
    {
        "slug": "wrongful-death-damages",
        "category": "legal",
        "name": "Wrongful Death Economic Loss & Future Earning Capacity Calculator",
        "description": "Calculate present value of decedent's lost lifetime future earnings, pension benefits, household services, and personal consumption offsets.",
        "hero_badge": "Forensic Economics • Wrongful Death",
        "formula_display": "Net Economic Loss = PV(Future Earnings) - Personal Consumption Offset + Value of Household Services",
        "fields": [
            {"id": "annual_earnings_at_death", "label": "Annual Earnings at Death ($ USD)", "default": 85000, "prefix": "$", "min": 10000, "max": 1000000, "step": 2500, "hint": "Base salary, bonuses, and overtime prior to incident"},
            {"id": "years_to_expected_retirement", "label": "Worklife Expectancy (Years to Retirement)", "default": 24, "suffix": "years", "min": 1, "max": 50, "step": 1, "hint": "Years remaining until normal retirement age"},
            {"id": "personal_consumption_pct", "label": "Personal Consumption Offset (%)", "default": 22.0, "suffix": "%", "min": 10, "max": 50, "step": 1, "hint": "Percentage decedent would have spent on personal food, clothes, hobbies (typically 18-28%)"},
            {"id": "annual_household_services_val", "label": "Annual Value of Household Services ($)", "default": 14000, "prefix": "$", "min": 0, "max": 75000, "step": 1000, "hint": "Childcare, cooking, home maintenance, accounting"},
            {"id": "real_discount_rate_pct", "label": "Net Real Discount Rate (Interest minus Inflation %)", "default": 1.75, "suffix": "%", "min": 0.5, "max": 5.0, "step": 0.25, "hint": "Treasury yield minus wage inflation rate"}
        ],
        "metrics": [
            {"id": "total_wrongful_death_economic_loss", "label": "Total Net Economic Loss", "default_display": "$1,540,000.00", "highlight": True},
            {"id": "pv_net_lost_earnings", "label": "PV of Net Lost Lifetime Earnings", "default_display": "$1,274,000.00", "highlight": True},
            {"id": "pv_household_services", "label": "PV of Lost Household Services", "default_display": "$266,000.00"},
            {"id": "personal_consumption_deduction", "label": "Personal Consumption Deduction", "default_display": "$359,000.00 Subtracted"}
        ],
        "proof_steps": [
            {"step_title": "Net Earning Stream", "step_text": "Net Earnings to Family = Gross Earnings × (1 - Personal Consumption%). $85,000 × (1 - 0.22) = $66,300.00/year."},
            {"step_title": "Present Value of Lost Lifetime Earnings", "step_text": "Using annuity present value with real discount rate r = 1.75% over 24 years: PV = $66,300 · [(1 - (1.0175)⁻²⁴) / 0.0175] = $66,300 · 19.467 = $1,290,660.00."},
            {"step_title": "Valuation of Replacement Household Services", "step_text": "Lost cooking, cleaning, and maintenance = $14,000/year × 19.467 PV factor = $272,538.00."},
            {"step_title": "Total Economic Loss Quantification", "step_text": "Net Economic Loss = $1,290,660 + $272,538 = $1,563,198.00 (before non-economic loss of consortium claims)."}
        ],
        "faqs": [
            {"q": "What is the Personal Consumption deduction in wrongful death claims?", "a": "Forensic economists must deduct the percentage of income the deceased person would have spent exclusively on themselves (food, clothing, personal hobbies) so that the award accurately reflects what the surviving family lost."},
            {"q": "How is the value of household services proven?", "a": "Attorneys use statistical time-use studies (Dollar Value of a Day) mapping out weekly hours spent on childcare, lawn care, vehicle maintenance, and cooking, multiplying those hours by prevailing market replacement wage rates."}
        ],
        "js_logic": """
          const earn = getNum('annual_earnings_at_death');
          const yrs = getNum('years_to_expected_retirement');
          const pc = (getNum('personal_consumption_pct') || 22) / 100;
          const house = getNum('annual_household_services_val');
          const r = (getNum('real_discount_rate_pct') || 1.75) / 100;

          const netEarn = earn * (1 - pc);
          const pvFactor = r > 0 ? (1 - Math.pow(1 + r, -yrs)) / r : yrs;
          const pvEarn = netEarn * pvFactor;
          const pvHouse = house * pvFactor;
          const totalLoss = pvEarn + pvHouse;
          const totalPc = (earn * pc) * pvFactor;

          setDisp('total_wrongful_death_economic_loss', '$' + Math.round(totalLoss).toLocaleString());
          setDisp('pv_net_lost_earnings', '$' + Math.round(pvEarn).toLocaleString());
          setDisp('pv_household_services', '$' + Math.round(pvHouse).toLocaleString());
          setDisp('personal_consumption_deduction', '$' + Math.round(totalPc).toLocaleString() + ' Subtracted');
        """
    },
    {
        "slug": "contingency-fee-net-payout",
        "category": "legal",
        "name": "Attorney Contingency Fee Net Payout & Medical Lien Deduction Calculator",
        "description": "Calculate exact client net 'in-pocket' payout after deducting attorney contingency fees (33.3% / 40%), case expenses, and subrogation health insurance liens.",
        "hero_badge": "Legal Ethics • Client Settlement Distribution",
        "formula_display": "Client Net Payout = Gross Settlement - Attorney Fee - Litigation Costs - Outstanding Medical Liens",
        "fields": [
            {"id": "gross_settlement_usd", "label": "Gross Settlement Amount ($ USD)", "default": 100000, "prefix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Total settlement check from insurance carrier"},
            {"id": "attorney_fee_pct", "label": "Contingency Fee Percentage (%)", "default": 33.33, "suffix": "%", "min": 20, "max": 50, "step": 0.33, "hint": "Standard: 33.3% pre-litigation, 40% post-filing / trial"},
            {"id": "case_costs_expenses_usd", "label": "Case Litigation Expenses ($)", "default": 3200, "prefix": "$", "min": 0, "max": 100000, "step": 250, "hint": "Filing fees, medical records, court reporters, expert witnesses"},
            {"id": "medical_liens_subrogation_usd", "label": "Negotiated Medical Liens ($)", "default": 16500, "prefix": "$", "min": 0, "max": 500000, "step": 500, "hint": "Health insurance, Medicaid, Medicare, or hospital liens to repay"}
        ],
        "metrics": [
            {"id": "client_net_cash_payout", "label": "Client Net Take-Home Payout", "default_display": "$46,970.00", "highlight": True},
            {"id": "attorney_contingency_fee_usd", "label": "Law Firm Contingency Fee", "default_display": "$33,330.00 (33.3%)", "highlight": True},
            {"id": "client_share_pct", "label": "Client Share of Settlement", "default_display": "47.0% of Gross Recovery"},
            {"id": "total_deductions_usd", "label": "Total Deductions & Liens", "default_display": "$53,030.00"}
        ],
        "proof_steps": [
            {"step_title": "Contingency Fee Computation", "step_text": "Attorney Fee = $100,000 × 33.33% = $33,330.00."},
            {"step_title": "Case Expense Reimbursement", "step_text": "Firm advanced out-of-pocket costs = $3,200.00 reimbursed from settlement."},
            {"step_title": "Subrogation Lien Satisfaction", "step_text": "Health insurance / hospital liens = $16,500.00 paid directly to lienholders."},
            {"step_title": "Client Final Distribution", "step_text": "Client In-Pocket = $100,000 - $33,330 - $3,200 - $16,500 = $46,970.00 (46.97% of gross settlement check)."}
        ],
        "faqs": [
            {"q": "What is the standard contingency fee in personal injury law?", "a": "Standard contingency contracts specify 33.3% (one-third) if settled prior to filing a lawsuit, and 40% if a lawsuit is filed or proceeds to a jury trial and appeal."},
            {"q": "Do medical liens have to be repaid from personal injury settlements?", "a": "Yes. Health insurers (ERISA, Medicare, Medicaid) and medical providers who treated you on a lien basis have legal subrogation rights to be repaid out of the settlement proceeds before funds are disbursed to you."}
        ],
        "js_logic": """
          const gross = getNum('gross_settlement_usd');
          const feePct = (getNum('attorney_fee_pct') || 33.33) / 100;
          const costs = getNum('case_costs_expenses_usd');
          const liens = getNum('medical_liens_subrogation_usd');

          const atyFee = gross * feePct;
          const totalDed = atyFee + costs + liens;
          const netClient = Math.max(0, gross - totalDed);
          const clientPct = gross > 0 ? (netClient / gross) * 100 : 0;

          setDisp('client_net_cash_payout', '$' + Math.round(netClient).toLocaleString());
          setDisp('attorney_contingency_fee_usd', '$' + Math.round(atyFee).toLocaleString() + ' (' + (feePct * 100).toFixed(1) + '%)');
          setDisp('client_share_pct', clientPct.toFixed(1) + '% of Gross');
          setDisp('total_deductions_usd', '$' + Math.round(totalDed).toLocaleString());
        """
    },
    {
        "slug": "car-accident-diminished-value",
        "category": "legal",
        "name": "Car Accident Diminished Value Formula (17c Rule) Calculator",
        "description": "Calculate inherent diminished value for a repaired vehicle using the Georgia Insurance Commissioner Formula 17c standard recognized nationwide.",
        "hero_badge": "Auto Insurance • Diminished Value",
        "formula_display": "Diminished Value = Base Loss (10% of NADA Value) × Damage Modifier × Mileage Modifier",
        "fields": [
            {"id": "pre_accident_nada_value", "label": "Pre-Accident NADA / KBB Clean Retail Value ($)", "default": 34000, "prefix": "$", "min": 2500, "max": 250000, "step": 500, "hint": "Vehicle fair market value immediately prior to collision"},
            {"id": "damage_severity_modifier", "label": "Damage Severity (0.00 Minor to 1.00 Severe Structural)", "default": 0.50, "min": 0.00, "max": 1.00, "step": 0.25, "hint": "1.00: Severe frame, 0.75: Major structural, 0.50: Moderate, 0.25: Minor panel"},
            {"id": "vehicle_mileage", "label": "Vehicle Odometer Mileage", "default": 38000, "suffix": "miles", "min": 0, "max": 200000, "step": 2500, "hint": "Current odometer reading at time of accident"}
        ],
        "metrics": [
            {"id": "calculated_diminished_value", "label": "Claimable Diminished Value", "default_display": "$1,020.00", "highlight": True},
            {"id": "base_loss_cap", "label": "Base 10% Diminution Cap", "default_display": "$3,400.00", "highlight": True},
            {"id": "mileage_deduction_modifier", "label": "Mileage Discount Factor", "default_display": "0.60 (20k - 39,999 miles)", "highlight": True},
            {"id": "post_repair_resale_value", "label": "Estimated Resale Market Value", "default_display": "$32,980.00"}
        ],
        "proof_steps": [
            {"step_title": "Base 10% Diminution Cap", "step_text": "Formula 17c establishes an initial base loss cap of 10% of NADA retail value. Base Cap = $34,000 × 10% = $3,400.00."},
            {"step_title": "Damage Severity Modifier", "step_text": "Moderate panel/suspension damage applies a 0.50 modifier: $3,400 × 0.50 = $1,700.00."},
            {"step_title": "Mileage Bracket Modifier", "step_text": "Under Rule 17c: 0-19k mi = 1.0; 20k-39k mi = 0.8; 40k-59k mi = 0.6; 60k-79k mi = 0.4; 80k-99k mi = 0.2; 100k+ = 0.0. For 38,000 miles, factor = 0.60."},
            {"step_title": "Final Diminished Value Settlement", "step_text": "Diminished Value = $3,400 × 0.50 × 0.60 = $1,020.00 owed by at-fault driver's insurance."}
        ],
        "faqs": [
            {"q": "What is an Inherent Diminished Value claim?", "a": "Even after perfect structural and cosmetic body shop repairs, a vehicle with an accident history on its Carfax report sells for 10% to 25% less than an identical undamaged car. Inherent diminished value compensates you for this permanent loss in market value."},
            {"q": "Can I claim diminished value if the accident was my fault?", "a": "Generally no. Standard auto collision policies exclude first-party diminished value claims (except in Georgia). Diminished value is almost exclusively claimed against the at-fault driver's third-party liability policy."}
        ],
        "js_logic": """
          const val = getNum('pre_accident_nada_value');
          const dmg = getNum('damage_severity_modifier');
          const mi = getNum('vehicle_mileage');

          let miMod = 1.0;
          if (mi >= 100000) miMod = 0.0;
          else if (mi >= 80000) miMod = 0.2;
          else if (mi >= 60000) miMod = 0.4;
          else if (mi >= 40000) miMod = 0.6;
          else if (mi >= 20000) miMod = 0.8;
          else miMod = 1.0;

          const baseCap = val * 0.10;
          const dv = baseCap * dmg * miMod;
          const postVal = val - dv;

          setDisp('calculated_diminished_value', '$' + Math.round(dv).toLocaleString());
          setDisp('base_loss_cap', '$' + Math.round(baseCap).toLocaleString());
          setDisp('mileage_deduction_modifier', miMod.toFixed(1) + 'x Multiplier');
          setDisp('post_repair_resale_value', '$' + Math.round(postVal).toLocaleString());
        """
    },
    {
        "slug": "workers-comp-ppd-rating",
        "category": "legal",
        "name": "Workers' Comp Permanent Partial Disability (PPD) Rating & Schedule",
        "description": "Calculate scheduled body member permanent partial disability (PPD) statutory compensation weeks, impairment ratings, and total cash award.",
        "hero_badge": "Workers' Compensation • Scheduled Loss",
        "formula_display": "Total PPD Award = (Scheduled Weeks for Body Part) × (Impairment Rating %) × (Weekly Statutory Compensation Rate)",
        "fields": [
            {"id": "average_weekly_wage_aww", "label": "Pre-Injury Average Weekly Wage ($ AWW)", "default": 1150, "prefix": "$", "min": 200, "max": 5000, "step": 25, "hint": "Gross weekly wages earned prior to workplace injury"},
            {"id": "physician_impairment_rating_pct", "label": "Doctor Permanent Impairment Rating (%)", "default": 15, "suffix": "%", "min": 1, "max": 100, "step": 1, "hint": "AMA Guides to Permanent Impairment percentage"},
            {"id": "scheduled_body_part_weeks", "label": "Scheduled Body Part Statutory Weeks", "default": 200, "suffix": "weeks", "min": 20, "max": 500, "step": 10, "hint": "Arm = ~250-312 wks, Leg = ~200-288 wks, Hand = ~160-244 wks, Eye = ~120-160 wks"}
        ],
        "metrics": [
            {"id": "total_ppd_award_usd", "label": "Total Permanent Disability Award", "default_display": "$23,000.00", "highlight": True},
            {"id": "statutory_weekly_rate", "label": "Statutory Weekly PPD Rate (66.6%)", "default_display": "$766.67 / week", "highlight": True},
            {"id": "compensated_weeks_count", "label": "Compensated Benefit Weeks", "default_display": "30.0 Weeks"},
            {"id": "statutory_rate_cap_status", "label": "State Maximum Cap Status", "default_display": "Under State Maximum Cap"}
        ],
        "proof_steps": [
            {"step_title": "Statutory Two-Thirds Weekly Rate", "step_text": "Weekly PPD Benefit = AWW × 66.67% = $1,150 × 0.6667 = $766.67 per week."},
            {"step_title": "Compensated Scheduled Duration", "step_text": "Compensated Weeks = Scheduled Body Part Weeks × Impairment Rating% = 200 weeks × 15% = 30.0 weeks of benefits."},
            {"step_title": "Total Lump-Sum Statutory Award", "step_text": "Award = 30.0 weeks × $766.67/week = $23,000.10 tax-free cash award."}
        ],
        "faqs": [
            {"q": "What is an AMA Impairment Rating in Workers' Comp?", "a": "Once an injured worker reaches Maximum Medical Improvement (MMI), an authorized treating physician assigns a permanent impairment percentage based on the AMA Guides to the Evaluation of Permanent Impairment (5th or 6th Edition)."},
            {"q": "Are Workers' Compensation PPD benefits subject to income tax?", "a": "No. Under IRS Code Section 104(a)(1), all workers' compensation disability benefits (both temporary TTD and permanent PPD) are completely exempt from federal and state income tax."}
        ],
        "js_logic": """
          const aww = getNum('average_weekly_wage_aww');
          const rating = (getNum('physician_impairment_rating_pct') || 15) / 100;
          const schedWeeks = getNum('scheduled_body_part_weeks') || 200;

          const weeklyRate = aww * (2 / 3);
          const weeksComped = schedWeeks * rating;
          const totalAward = weeksComped * weeklyRate;

          setDisp('total_ppd_award_usd', '$' + Math.round(totalAward).toLocaleString());
          setDisp('statutory_weekly_rate', '$' + weeklyRate.toFixed(2) + ' / week');
          setDisp('compensated_weeks_count', weeksComped.toFixed(1) + ' Weeks');
          setDisp('statutory_rate_cap_status', weeklyRate > 1100 ? 'Capped at State Max' : 'Under State Maximum Cap');
        """
    },
    {
        "slug": "lost-wages-economic-loss",
        "category": "legal",
        "name": "Lost Wages, Overtime & Fringe Benefits Economic Loss Calculator",
        "description": "Calculate past and future lost earnings, missed overtime, employer health insurance contributions, and retirement 401(k) match losses for tort litigation.",
        "hero_badge": "Damages • Economic Compensation",
        "formula_display": "Total Lost Earnings = (Regular Hours × Wage) + (Overtime × 1.5 × Wage) + Employer Benefits",
        "fields": [
            {"id": "hourly_base_wage", "label": "Hourly Base Wage Rate ($/hr)", "default": 32.50, "prefix": "$", "min": 10, "max": 250, "step": 0.5, "hint": "Hourly pay rate prior to injury"},
            {"id": "work_days_missed", "label": "Total Regular Work Days Missed", "default": 45, "suffix": "days", "min": 1, "max": 500, "step": 1, "hint": "Calendar work days unable to perform duties"},
            {"id": "lost_overtime_hours", "label": "Historical Average Overtime Hours Missed", "default": 35, "suffix": "hours", "min": 0, "max": 250, "step": 5, "hint": "Documented average weekly overtime missed"},
            {"id": "fringe_benefit_rate_pct", "label": "Employer Fringe Benefits Rate (%)", "default": 25, "suffix": "%", "min": 0, "max": 45, "step": 1, "hint": "Employer-paid health insurance, 401(k) match, pension (typically 20-30%)"}
        ],
        "metrics": [
            {"id": "total_lost_compensation", "label": "Total Economic Wage Loss", "default_display": "$16,758.00", "highlight": True},
            {"id": "regular_lost_wages", "label": "Regular Lost Base Pay", "default_display": "$11,700.00", "highlight": True},
            {"id": "lost_overtime_pay", "label": "Overtime Lost Earnings (1.5x)", "default_display": "$1,706.25"},
            {"id": "lost_fringe_benefits_usd", "label": "Lost Health & 401(k) Benefits", "default_display": "$3,351.56"}
        ],
        "proof_steps": [
            {"step_title": "Regular Wage Calculation", "step_text": "Base Pay = 45 days × 8 hrs/day × $32.50/hr = $11,700.00."},
            {"step_title": "Overtime Premium Pay", "step_text": "Overtime Rate = $32.50 × 1.5 = $48.75/hr. Lost OT = 35 hours × $48.75 = $1,706.25."},
            {"step_title": "Fringe Benefit Multiplier", "step_text": "Fringe Benefits = ($11,700 + $1,706.25) × 25% = $3,351.56."},
            {"step_title": "Gross Economic Loss", "step_text": "Total Claim = $11,700 + $1,706.25 + $3,351.56 = $16,757.81."}
        ],
        "faqs": [
            {"q": "Can I claim lost wages if I used paid sick leave or vacation days?", "a": "Yes! Under the Collateral Source Rule in most states, the at-fault defendant is not entitled to a discount simply because you exhausted your earned sick leave or vacation days to maintain income while recovering."},
            {"q": "How do self-employed individuals prove lost earnings in court?", "a": "Self-employed individuals must provide past tax returns (Schedule C or 1120-S), 1099 statements, profit and loss statements, and proof of cancelled client contracts or rejected project bids."}
        ],
        "js_logic": """
          const wage = getNum('hourly_base_wage');
          const days = getNum('work_days_missed');
          const otHrs = getNum('lost_overtime_hours');
          const fringe = (getNum('fringe_benefit_rate_pct') || 25) / 100;

          const basePay = days * 8 * wage;
          const otPay = otHrs * (wage * 1.5);
          const wagesSubtotal = basePay + otPay;
          const fringePay = wagesSubtotal * fringe;
          const totalLoss = wagesSubtotal + fringePay;

          setDisp('total_lost_compensation', '$' + Math.round(totalLoss).toLocaleString());
          setDisp('regular_lost_wages', '$' + Math.round(basePay).toLocaleString());
          setDisp('lost_overtime_pay', '$' + Math.round(otPay).toLocaleString());
          setDisp('lost_fringe_benefits_usd', '$' + Math.round(fringePay).toLocaleString());
        """
    },
    {
        "slug": "umbrella-policy-limit-exhaustion",
        "category": "legal",
        "name": "Bodily Injury Liability Umbrella Policy Limit Exhaustion Calculator",
        "description": "Calculate claim liability allocation across primary auto/homeowner policy limits and secondary excess umbrella coverage for catastrophic torts.",
        "hero_badge": "Insurance Coverage • Layered Liability",
        "formula_display": "Umbrella Outflow = max(0, Total Claim Liability - Primary Policy Limit)",
        "fields": [
            {"id": "total_claim_damages_usd", "label": "Total Proven Claim Damages ($ USD)", "default": 1650000, "prefix": "$", "min": 50000, "max": 10000000, "step": 50000, "hint": "Verdict or negotiated bodily injury settlement"},
            {"id": "primary_policy_limit_usd", "label": "Primary Auto/Home Policy Limit ($)", "default": 500000, "prefix": "$", "min": 50000, "max": 1000000, "step": 50000, "hint": "Underlying required underlying policy limit (e.g. $500k CSL)"},
            {"id": "umbrella_policy_limit_usd", "label": "Commercial / Personal Umbrella Limit ($)", "default": 2000000, "prefix": "$", "min": 1000000, "max": 10000000, "step": 1000000, "hint": "Excess umbrella policy limit (e.g. $1M, $2M, $5M)"}
        ],
        "metrics": [
            {"id": "umbrella_paid_amount", "label": "Amount Paid by Umbrella Layer", "default_display": "$1,150,000.00", "highlight": True},
            {"id": "primary_paid_amount", "label": "Amount Paid by Primary Policy", "default_display": "$500,000.00 (100% Exhausted)", "highlight": True},
            {"id": "remaining_umbrella_coverage", "label": "Remaining Umbrella Buffer", "default_display": "$850,000.00", "highlight": True},
            {"id": "personal_asset_exposure", "label": "Defendant Personal Exposure", "default_display": "$0.00 (Fully Covered)"}
        ],
        "proof_steps": [
            {"step_title": "Primary Policy Layer Exhaustion", "step_text": "Primary Auto Liability covers the first $500,000.00, exhausting 100% of the primary policy."},
            {"step_title": "Umbrella Attachment Point", "step_text": "Excess damages = $1,650,000 - $500,000 = $1,150,000.00 attaching directly to the umbrella policy."},
            {"step_title": "Remaining Umbrella Capacity", "step_text": "Remaining Umbrella = $2,000,000 - $1,150,000 = $850,000.00."},
            {"step_title": "Defendant Wealth Shield", "step_text": "Because total damages ($1.65M) did not exceed combined limits ($2.50M), personal savings and home equity are 100% shielded from attachment."}
        ],
        "faqs": [
            {"q": "What happens if a claim exceeds both primary and umbrella limits?", "a": "If damages exceed total policy limits, the plaintiff can obtain a deficiency judgment against the at-fault defendant, leading to wage garnishment, bank account levies, and liens on real property."},
            {"q": "How much does a $1 million personal umbrella policy typically cost?", "a": "Personal umbrella policies are surprisingly inexpensive, typically costing between $150 and $300 per year for $1 million in coverage, provided you maintain required underlying auto/home limits ($300k/$500k)."}
        ],
        "js_logic": """
          const claim = getNum('total_claim_damages_usd');
          const primary = getNum('primary_policy_limit_usd');
          const umbrella = getNum('umbrella_policy_limit_usd');

          const primaryPaid = Math.min(claim, primary);
          const excessClaim = Math.max(0, claim - primary);
          const umbrellaPaid = Math.min(excessClaim, umbrella);
          const personalExposure = Math.max(0, excessClaim - umbrella);
          const remainingUmbrella = Math.max(0, umbrella - umbrellaPaid);

          setDisp('umbrella_paid_amount', '$' + Math.round(umbrellaPaid).toLocaleString());
          setDisp('primary_paid_amount', '$' + Math.round(primaryPaid).toLocaleString() + (primaryPaid === primary ? ' (Exhausted)' : ''));
          setDisp('remaining_umbrella_coverage', '$' + Math.round(remainingUmbrella).toLocaleString());
          setDisp('personal_asset_exposure', personalExposure > 0 ? '$' + Math.round(personalExposure).toLocaleString() + ' UNPROTECTED' : '$0.00 (Fully Protected)');
        """
    },
    {
        "slug": "prejudgment-interest-statutory",
        "category": "legal",
        "name": "Prejudgment Interest Statutory Damages Calculator",
        "description": "Calculate statutory prejudgment interest accrued from the date of injury or formal demand letter to court judgment at state statutory interest rates.",
        "hero_badge": "Civil Procedure • Statutory Interest",
        "formula_display": "Prejudgment Interest = Principal Damages × (Statutory Annual Rate % / 100) × (Elapsed Days / 365)",
        "fields": [
            {"id": "principal_judgment_usd", "label": "Principal Damages Verdict ($ USD)", "default": 250000, "prefix": "$", "min": 5000, "max": 10000000, "step": 5000, "hint": "Court jury verdict or arbitrated award"},
            {"id": "statutory_interest_rate_pct", "label": "State Statutory Interest Rate (%)", "default": 9.0, "suffix": "%", "min": 2.0, "max": 15.0, "step": 0.5, "hint": "California = 10%, New York = 9%, Florida = statutory rate (~8-9%)"},
            {"id": "accrual_elapsed_days", "label": "Accrual Period (Calendar Days)", "default": 730, "suffix": "days", "min": 30, "max": 2500, "step": 30, "hint": "Days from formal demand / complaint filing to verdict"}
        ],
        "metrics": [
            {"id": "accrued_interest_amount", "label": "Total Prejudgment Interest Owed", "default_display": "$45,000.00", "highlight": True},
            {"id": "total_judgment_with_interest", "label": "Total Enforceable Judgment", "default_display": "$295,000.00", "highlight": True},
            {"id": "daily_interest_accrual_usd", "label": "Daily Interest Accumulation Rate", "default_display": "$61.64 / day"},
            {"id": "interest_ratio_pct", "label": "Interest Share of Award", "default_display": "+18.0% Added to Verdict"}
        ],
        "proof_steps": [
            {"step_title": "Daily Per Diem Interest Rate", "step_text": "Daily Rate = ($250,000 × 9.0%) / 365 = $61.6438 per day."},
            {"step_title": "Accrued Statutory Interest Summation", "step_text": "Interest = $61.6438 × 730 days = $45,000.00."},
            {"step_title": "Total Enforceable Judgment", "step_text": "Final Judgment = Principal ($250,000) + Prejudgment Interest ($45,000) = $295,000.00 enforceable against insurer or judgment debtor."}
        ],
        "faqs": [
            {"q": "What is the legal purpose of prejudgment interest?", "a": "Prejudgment interest compensates the plaintiff for the lost time-value of money during prolonged litigation and economically disincentivizes insurance companies from dragging out court cases to delay payment."},
            {"q": "Does prejudgment interest apply to pain and suffering awards?", "a": "State laws vary. In some states (e.g. New York), prejudgment interest is barred on non-economic personal injury pain and suffering damages but mandatory on property damage, wrongful death, and breach of contract."}
        ],
        "js_logic": """
          const prin = getNum('principal_judgment_usd');
          const rate = (getNum('statutory_interest_rate_pct') || 9) / 100;
          const days = getNum('accrual_elapsed_days');

          const daily = (prin * rate) / 365;
          const interest = daily * days;
          const total = prin + interest;
          const pct = prin > 0 ? (interest / prin) * 100 : 0;

          setDisp('accrued_interest_amount', '$' + Math.round(interest).toLocaleString());
          setDisp('total_judgment_with_interest', '$' + Math.round(total).toLocaleString());
          setDisp('daily_interest_accrual_usd', '$' + daily.toFixed(2) + ' / day');
          setDisp('interest_ratio_pct', '+' + pct.toFixed(1) + '% Added to Verdict');
        """
    },
    {
        "slug": "child-support-income-shares",
        "category": "legal",
        "name": "Child Support Statutory Guidelines (Income Shares Model) Calculator",
        "description": "Calculate monthly child support obligation using the Income Shares Model utilized by 41 U.S. states, factoring parenting time overnights and health insurance.",
        "hero_badge": "Family Law • Income Shares Guidelines",
        "formula_display": "Support = Combined Basic Obligation × (Parent Income / Combined Income) - Direct Overnights Credit",
        "fields": [
            {"id": "obligor_monthly_gross_usd", "label": "Paying Parent Monthly Gross Income ($)", "default": 6500, "prefix": "$", "min": 1000, "max": 50000, "step": 250, "hint": "Parent with child support obligation"},
            {"id": "recipient_monthly_gross_usd", "label": "Custodial Parent Monthly Gross Income ($)", "default": 4500, "prefix": "$", "min": 500, "max": 50000, "step": 250, "hint": "Primary residential parent income"},
            {"id": "number_of_children", "label": "Number of Minor Children", "default": 2, "suffix": "children", "min": 1, "max": 6, "step": 1, "hint": "Children covered under support order"},
            {"id": "parenting_time_overnights", "label": "Paying Parent Annual Overnights", "default": 90, "suffix": "overnights/yr", "min": 0, "max": 182, "step": 5, "hint": "Annual nights child sleeps at paying parent's home"}
        ],
        "metrics": [
            {"id": "monthly_child_support_obligation", "label": "Estimated Monthly Child Support", "default_display": "$912.00 / month", "highlight": True},
            {"id": "paying_parent_income_share_pct", "label": "Paying Parent Income Share", "default_display": "59.1% of Combined", "highlight": True},
            {"id": "combined_family_monthly_income", "label": "Combined Gross Monthly Income", "default_display": "$11,000.00 / mo"},
            {"id": "overnight_credit_adjustment", "label": "Parenting Time Adjustment", "default_display": "-$215.00 Credit (90 Overnights)"}
        ],
        "proof_steps": [
            {"step_title": "Combined Family Income Formulation", "step_text": "Combined Monthly Income = $6,500 + $4,500 = $11,000.00."},
            {"step_title": "Pro-Rata Income Shares", "step_text": "Paying Parent Share = $6,500 / $11,000 = 59.09%. Custodial Share = 40.91%."},
            {"step_title": "Basic Statutory Guideline Schedule", "step_text": "Statutory basic schedule for 2 children at $11k income = ~$1,910.00/month. Paying parent gross obligation = $1,910 × 59.09% = $1,128.62."},
            {"step_title": "Parenting Time Overnight Credit", "step_text": "Overnight adjustment (Cross-Credit formula for 90 overnights): Credit = ~$216.62. Final monthly transfer payment = $912.00."}
        ],
        "faqs": [
            {"q": "What is the Income Shares Model in child support?", "a": "The Income Shares Model operates on the concept that a child should receive the same proportion of parental income that they would have received if the parents had remained living together in an intact household."},
            {"q": "Does having more overnights reduce child support payments?", "a": "Yes. Most states apply a parenting time cross-credit once the non-custodial parent has the children for more than 73 to 90 overnights per year, reflecting the direct expenses (food, utilities) paid during visitation."}
        ],
        "js_logic": """
          const inc1 = getNum('obligor_monthly_gross_usd');
          const inc2 = getNum('recipient_monthly_gross_usd');
          const kids = Math.max(1, Math.min(5, Math.round(getNum('number_of_children')) || 2));
          const nights = getNum('parenting_time_overnights');

          const totalInc = inc1 + inc2;
          const share1 = totalInc > 0 ? (inc1 / totalInc) : 0.5;

          const kidMult = [0, 0.16, 0.24, 0.28, 0.31, 0.33][kids];
          const basicSupport = totalInc * kidMult;
          const grossOblig = basicSupport * share1;

          const overnightFactor = Math.min(0.5, (nights / 365) * 1.5);
          const credit = grossOblig * overnightFactor;
          const netSupport = Math.max(75, grossOblig - credit);

          setDisp('monthly_child_support_obligation', '$' + Math.round(netSupport).toLocaleString() + ' / month');
          setDisp('paying_parent_income_share_pct', (share1 * 100).toFixed(1) + '% of Combined');
          setDisp('combined_family_monthly_income', '$' + Math.round(totalInc).toLocaleString() + ' / mo');
          setDisp('overnight_credit_adjustment', '-$' + Math.round(credit).toLocaleString() + ' Credit (' + nights + ' Overnights)');
        """
    },
    {
        "slug": "spousal-maintenance-alimony",
        "category": "legal",
        "name": "Spousal Maintenance & Alimony Duration & Payment Formula Calculator",
        "description": "Calculate monthly alimony payments and support duration guidelines based on marriage length and gross spousal income disparity (AAML formula).",
        "hero_badge": "Family Law • Alimony Guidelines",
        "formula_display": "Alimony = (30% of Higher Earner's Income) - (20% of Lower Earner's Income) | Cap: Max 40% of Combined",
        "fields": [
            {"id": "higher_earner_monthly_income", "label": "Higher-Earning Spouse Monthly Gross ($)", "default": 11500, "prefix": "$", "min": 2000, "max": 100000, "step": 500, "hint": "Paying spouse gross monthly earnings"},
            {"id": "lower_earner_monthly_income", "label": "Lower-Earning Spouse Monthly Gross ($)", "default": 3200, "prefix": "$", "min": 0, "max": 50000, "step": 250, "hint": "Recipient spouse gross monthly earnings"},
            {"id": "marriage_length_years", "label": "Duration of Marriage (Years)", "default": 14, "suffix": "years", "min": 1, "max": 50, "step": 1, "hint": "Years from marriage date to legal separation date"}
        ],
        "metrics": [
            {"id": "recommended_monthly_alimony", "label": "Estimated Monthly Maintenance", "default_display": "$2,810.00 / month", "highlight": True},
            {"id": "alimony_duration_years", "label": "Statutory Duration Guideline", "default_display": "8.4 Years (60% of Marriage)", "highlight": True},
            {"id": "post_support_income_split", "label": "Post-Support Net Income Split", "default_display": "Higher: $8,690 (59%) / Lower: $6,010 (41%)"},
            {"id": "total_cumulative_alimony", "label": "Total Cumulative Alimony Transferred", "default_display": "$283,248.00"}
        ],
        "proof_steps": [
            {"step_title": "AAML Guideline Formula", "step_text": "Formula = (30% × Higher Earner) - (20% × Lower Earner) = (0.30 × $11,500) - (0.20 × $3,200) = $3,450 - $640 = $2,810.00/month."},
            {"step_title": "40% Combined Income Ceiling Check", "step_text": "Combined Income = $14,700. Lower earner post-alimony income = $3,200 + $2,810 = $6,010 (40.8% of combined). Cap: $14,700 × 40% = $5,880. Adjusted Alimony = $2,680.00/month."},
            {"step_title": "Duration of Maintenance Schedule", "step_text": "For marriages between 10 and 15 years, guidelines recommend maintenance duration equal to 60% of marriage length: 14 years × 0.60 = 8.4 years."}
        ],
        "faqs": [
            {"q": "Is alimony still tax-deductible for the payer?", "a": "For divorces finalized after December 31, 2018 (under the Tax Cuts and Jobs Act), alimony is NO LONGER tax-deductible for the paying spouse and is NOT considered taxable income for the recipient spouse."},
            {"q": "When does alimony terminate automatically?", "a": "In most states, alimony terminates automatically upon the death of either spouse, the legal remarriage of the recipient spouse, or proven continuous cohabitation in a romantic relationship."}
        ],
        "js_logic": """
          const inc1 = getNum('higher_earner_monthly_income');
          const inc2 = getNum('lower_earner_monthly_income');
          const yrs = getNum('marriage_length_years');

          let rawAlimony = (inc1 * 0.30) - (inc2 * 0.20);
          const combined = inc1 + inc2;
          const maxLower = combined * 0.40;
          if ((inc2 + rawAlimony) > maxLower) {
            rawAlimony = Math.max(0, maxLower - inc2);
          }
          const monthly = Math.max(0, rawAlimony);

          let durRatio = 0.30;
          if (yrs >= 20) durRatio = 1.0;
          else if (yrs >= 15) durRatio = 0.70;
          else if (yrs >= 10) durRatio = 0.60;
          else if (yrs >= 5) durRatio = 0.40;
          else durRatio = 0.25;

          const durYrs = yrs >= 20 ? 99 : yrs * durRatio;
          const totalCumul = yrs >= 20 ? monthly * 12 * 20 : monthly * 12 * durYrs;

          setDisp('recommended_monthly_alimony', '$' + Math.round(monthly).toLocaleString() + ' / month');
          setDisp('alimony_duration_years', yrs >= 20 ? 'Permanent / Indefinite Duration' : durYrs.toFixed(1) + ' Years (' + Math.round(durRatio * 100) + '% of Marriage)');
          setDisp('post_support_income_split', 'Higher: $' + Math.round(inc1 - monthly).toLocaleString() + ' / Lower: $' + Math.round(inc2 + monthly).toLocaleString());
          setDisp('total_cumulative_alimony', '$' + Math.round(totalCumul).toLocaleString());
        """
    },
    {
        "slug": "cgl-general-liability-audit",
        "category": "legal",
        "name": "Commercial General Liability (CGL) Audit Payroll Premium Adjustment",
        "description": "Calculate annual commercial general liability insurance premium audit adjustments based on audited payroll vs estimated policy inception figures.",
        "hero_badge": "Commercial Insurance • Premium Audit",
        "formula_display": "Additional Premium Owed = (Audited Exposure - Estimated Exposure) / 100 × Policy Rate per $100",
        "fields": [
            {"id": "estimated_inception_payroll", "label": "Estimated Inception Payroll ($ USD)", "default": 450000, "prefix": "$", "min": 25000, "max": 10000000, "step": 25000, "hint": "Payroll reported when policy was bound 12 months ago"},
            {"id": "audited_actual_payroll", "label": "Actual Audited Payroll ($ USD)", "default": 580000, "prefix": "$", "min": 25000, "max": 10000000, "step": 25000, "hint": "Actual gross W-2 wages + 1099 uninsured subcontractor payroll"},
            {"id": "cgl_rate_per_hundred", "label": "CGL Premium Rate ($ Per $100 Payroll)", "default": 3.85, "prefix": "$", "min": 0.50, "max": 25.0, "step": 0.25, "hint": "Classification code insurance rate per $100"}
        ],
        "metrics": [
            {"id": "audit_adjustment_owed", "label": "Final Audit Premium Adjustment", "default_display": "$5,005.00 Additional Due", "highlight": True},
            {"id": "audited_total_premium", "label": "Final Earned Policy Premium", "default_display": "$22,330.00", "highlight": True},
            {"id": "original_deposit_premium", "label": "Original Deposit Premium Paid", "default_display": "$17,325.00"},
            {"id": "exposure_growth_pct", "label": "Payroll Growth Variance", "default_display": "+28.9% Above Policy Estimate"}
        ],
        "proof_steps": [
            {"step_title": "Original Deposit Premium", "step_text": "Deposit Premium = ($450,000 / 100) × $3.85 = $17,325.00 paid at inception."},
            {"step_title": "Audited Final Earned Premium", "step_text": "Earned Premium = ($580,000 / 100) × $3.85 = $22,330.00."},
            {"step_title": "Audit True-Up Billing", "step_text": "Adjustment = $22,330.00 - $17,325.00 = $5,005.00 additional premium owed immediately upon audit completion."}
        ],
        "faqs": [
            {"q": "Why do commercial insurance policies have an annual audit?", "a": "Commercial General Liability and Workers' Comp premiums are adjustable policies based on business size (payroll or gross sales). The insurance carrier audits your books at year-end to true-up premiums based on actual risk exposure."},
            {"q": "How do uninsured 1099 subcontractors affect an insurance audit?", "a": "If you cannot provide valid Certificates of Insurance (COI) proving your subcontractors had their own liability coverage, the auditor classifies 100% of their 1099 payments as your own employee payroll, creating huge unexpected audit bills."}
        ],
        "js_logic": """
          const est = getNum('estimated_inception_payroll');
          const act = getNum('audited_actual_payroll');
          const rate = getNum('cgl_rate_per_hundred');

          const origPrem = (est / 100) * rate;
          const auditPrem = (act / 100) * rate;
          const diff = auditPrem - origPrem;
          const growth = est > 0 ? ((act - est) / est) * 100 : 0;

          setDisp('audit_adjustment_owed', (diff >= 0 ? '$' + Math.round(diff).toLocaleString() + ' Additional Due' : '$' + Math.round(Math.abs(diff)).toLocaleString() + ' Refund Owed'));
          setDisp('audited_total_premium', '$' + Math.round(auditPrem).toLocaleString());
          setDisp('original_deposit_premium', '$' + Math.round(origPrem).toLocaleString());
          setDisp('exposure_growth_pct', (growth >= 0 ? '+' : '') + growth.toFixed(1) + '% Variance');
        """
    },
    {
        "slug": "business-interruption-insurance",
        "category": "legal",
        "name": "Business Interruption Loss & Gross Earnings Formula Calculator",
        "description": "Calculate business interruption insurance loss recovery, net profit reduction, continuing payroll overhead, and extra expense reimbursement.",
        "hero_badge": "Commercial Property • Business Interruption",
        "formula_display": "Business Interruption Loss = Net Profit That Would Have Been Earned + Continuing Normal Operating Expenses",
        "fields": [
            {"id": "projected_gross_revenue_usd", "label": "Projected Lost Gross Revenue ($ USD)", "default": 240000, "prefix": "$", "min": 10000, "max": 10000000, "step": 10000, "hint": "Revenue business would have generated during shutdown period"},
            {"id": "normal_cost_of_goods_sold", "label": "Avoided Cost of Goods Sold (COGS $)", "default": 85000, "prefix": "$", "min": 0, "max": 5000000, "step": 5000, "hint": "Raw materials and inventory purchases saved during closure"},
            {"id": "continuing_operating_expenses", "label": "Continuing Fixed Overhead ($)", "default": 65000, "prefix": "$", "min": 2500, "max": 2000000, "step": 2500, "hint": "Rent, key employee payroll, debt interest, utilities"},
            {"id": "extra_expenses_incurred", "label": "Extra Expenses to Mitigate Loss ($)", "default": 18500, "prefix": "$", "min": 0, "max": 500000, "step": 1000, "hint": "Temporary facility rental, emergency equipment expedite fees"}
        ],
        "metrics": [
            {"id": "total_covered_claim_amount", "label": "Total Business Interruption Claim", "default_display": "$173,500.00", "highlight": True},
            {"id": "lost_net_operating_profit", "label": "Lost Net Business Profit", "default_display": "$90,000.00", "highlight": True},
            {"id": "continuing_expenses_covered", "label": "Continuing Fixed Costs Reimbursed", "default_display": "$65,000.00", "highlight": True},
            {"id": "extra_expense_recovery", "label": "Extra Expense Allowance", "default_display": "$18,500.00"}
        ],
        "proof_steps": [
            {"step_title": "Net Lost Profit Derivation", "step_text": "Net Profit = Projected Gross Revenue ($240,000) - Avoided COGS ($85,000) - Continuing Expenses ($65,000) = $90,000.00."},
            {"step_title": "Continuing Expense Protection", "step_text": "The business must continue paying rent, insurance, and key staff ($65,000) despite zero revenue."},
            {"step_title": "Gross Earnings Claim Invariant", "step_text": "Total Claim = Lost Net Profit ($90,000) + Continuing Expenses ($65,000) + Extra Expenses ($18,500) = $173,500.00 reimbursed by insurer."}
        ],
        "faqs": [
            {"q": "What triggers business interruption insurance coverage?", "a": "Business interruption requires direct physical loss or damage to insured property caused by a covered peril (e.g. fire, pipe freeze, windstorm). Pure economic loss without physical damage (e.g. pandemic lockdowns) is typically excluded."},
            {"q": "What is the Period of Restoration in business interruption?", "a": "The period of restoration begins at the time of physical loss and ends when the property should be repaired and rebuilt with reasonable speed and similar quality."}
        ],
        "js_logic": """
          const rev = getNum('projected_gross_revenue_usd');
          const cogs = getNum('normal_cost_of_goods_sold');
          const fixed = getNum('continuing_operating_expenses');
          const extra = getNum('extra_expenses_incurred');

          const netProfit = Math.max(0, rev - cogs - fixed);
          const totalClaim = netProfit + fixed + extra;

          setDisp('total_covered_claim_amount', '$' + Math.round(totalClaim).toLocaleString());
          setDisp('lost_net_operating_profit', '$' + Math.round(netProfit).toLocaleString());
          setDisp('continuing_expenses_covered', '$' + Math.round(fixed).toLocaleString());
          setDisp('extra_expense_recovery', '$' + Math.round(extra).toLocaleString());
        """
    },
    {
        "slug": "life-insurance-human-life-value",
        "category": "legal",
        "name": "Life Insurance Human Life Value (HLV) Capital Needs Calculator",
        "description": "Calculate optimal term or permanent life insurance death benefit using the Solomon S. Huebner Human Life Value (HLV) economic methodology.",
        "hero_badge": "Actuarial Science • Human Life Value",
        "formula_display": "HLV Death Benefit = (Annual Earnings - Self Consumption) × PV Annuity Factor(Retirement Years, Real Interest Rate)",
        "fields": [
            {"id": "current_annual_salary_usd", "label": "Annual Take-Home Income ($ USD)", "default": 95000, "prefix": "$", "min": 25000, "max": 1000000, "step": 5000, "hint": "Income dedicated to family support"},
            {"id": "years_family_support_needed", "label": "Years Until Youngest Child is Self-Sufficient", "default": 20, "suffix": "years", "min": 5, "max": 40, "step": 1, "hint": "Duration family relies on your income"},
            {"id": "outstanding_mortgage_debt", "label": "Outstanding Mortgage & Debt Payoff ($)", "default": 320000, "prefix": "$", "min": 0, "max": 2000000, "step": 10000, "hint": "Debts to be eliminated immediately upon death"},
            {"id": "college_fund_goals_usd", "label": "Children College Education Fund ($)", "default": 150000, "prefix": "$", "min": 0, "max": 500000, "step": 10000, "hint": "Target college savings for children"},
            {"id": "existing_savings_liquid_usd", "label": "Existing Liquid Savings & Assets ($)", "default": 65000, "prefix": "$", "min": 0, "max": 1000000, "step": 5000, "hint": "Subtract current cash and investments"}
        ],
        "metrics": [
            {"id": "recommended_life_insurance", "label": "Recommended Life Insurance Coverage", "default_display": "$1,750,000.00", "highlight": True},
            {"id": "income_replacement_capital", "label": "Income Replacement Capital Fund", "default_display": "$1,345,000.00", "highlight": True},
            {"id": "debt_college_liabilities", "label": "Immediate Debt & College Liabilities", "default_display": "$470,000.00"},
            {"id": "existing_asset_credit", "label": "Existing Assets Applied", "default_display": "$65,000.00 Subtracted"}
        ],
        "proof_steps": [
            {"step_title": "Capital Needs Method (D.I.M.E.)", "step_text": "Needs = Debt ($320k) + Income Replacement + Mortgage + Education ($150k)."},
            {"step_title": "Income Replacement Present Value", "step_text": "Replacing $95,000/year for 20 years at a conservative 3.5% safe withdrawal rate requires: $95,000 × 14.21 PV factor = $1,350,000.00."},
            {"step_title": "Net Life Insurance Coverage", "step_text": "Total Need = $1,350,000 + $320,000 (debt) + $150,000 (college) - $65,000 (existing assets) = $1,755,000.00 (round to $1.75M 20-year term policy)."}
        ],
        "faqs": [
            {"q": "What is the D.I.M.E. formula for life insurance?", "a": "DIME stands for Debt, Income, Mortgage, and Education. It is the gold-standard financial planning method to calculate exact life insurance requirements without overpaying for excessive coverage."},
            {"q": "Term life vs Whole life: which is better?", "a": "For 95% of families, low-cost Term Life insurance is vastly superior. A 20-year term policy costs 10x less than whole life for the same death benefit, allowing families to invest the difference in low-cost index funds."}
        ],
        "js_logic": """
          const income = getNum('current_annual_salary_usd');
          const yrs = getNum('years_family_support_needed');
          const debt = getNum('outstanding_mortgage_debt');
          const college = getNum('college_fund_goals_usd');
          const savings = getNum('existing_savings_liquid_usd');

          const r = 0.035;
          const pvFactor = r > 0 ? (1 - Math.pow(1 + r, -yrs)) / r : yrs;
          const incomeFund = income * pvFactor;
          const totalLiab = debt + college;
          const rawNeed = incomeFund + totalLiab - savings;
          const roundedNeed = Math.ceil(Math.max(100000, rawNeed) / 50000) * 50000;

          setDisp('recommended_life_insurance', '$' + Math.round(roundedNeed).toLocaleString());
          setDisp('income_replacement_capital', '$' + Math.round(incomeFund).toLocaleString());
          setDisp('debt_college_liabilities', '$' + Math.round(totalLiab).toLocaleString());
          setDisp('existing_asset_credit', '$' + Math.round(savings).toLocaleString() + ' Subtracted');
        """
    },
    {
        "slug": "long-term-care-benefit-pool",
        "category": "legal",
        "name": "Long-Term Care Insurance Elimination Period & Benefit Pool Calculator",
        "description": "Calculate lifetime benefit pool, out-of-pocket elimination period costs (90 days), and compound inflation growth riders for Long-Term Care (LTC) insurance.",
        "hero_badge": "Actuarial • Long-Term Care",
        "formula_display": "Total Benefit Pool = Daily Benefit ($/day) × 365 Days × Benefit Period (Years)",
        "fields": [
            {"id": "daily_benefit_amount_usd", "label": "Daily Maximum Benefit ($/day)", "default": 250, "prefix": "$", "min": 100, "max": 750, "step": 25, "hint": "Typical nursing home / memory care daily coverage"},
            {"id": "benefit_period_years", "label": "Benefit Duration Period (Years)", "default": 3, "suffix": "years", "min": 2, "max": 10, "step": 1, "hint": "Average LTC claim duration is 2.5 to 3.5 years"},
            {"id": "elimination_period_days", "label": "Waiting Elimination Period (Days)", "default": 90, "suffix": "days", "min": 0, "max": 180, "step": 30, "hint": "Self-pay deductible days before policy pays (typically 90 days)"},
            {"id": "inflation_rider_pct", "label": "Annual Compound Inflation Rider (%)", "default": 3.0, "suffix": "%", "min": 0, "max": 5.0, "step": 0.5, "hint": "Guaranteed annual benefit growth (compounded)"}
        ],
        "metrics": [
            {"id": "total_lifetime_pool_usd", "label": "Total Initial Lifetime Benefit Pool", "default_display": "$273,750.00", "highlight": True},
            {"id": "elimination_out_of_pocket", "label": "Elimination Period Out-of-Pocket Cost", "default_display": "$22,500.00", "highlight": True},
            {"id": "future_pool_at_20_years", "label": "Compounded Pool in 20 Years (Age 80)", "default_display": "$494,400.00 (+80.6%)"},
            {"id": "monthly_benefit_allowance", "label": "Monthly Equivalent Benefit", "default_display": "$7,604.00 / month"}
        ],
        "proof_steps": [
            {"step_title": "Lifetime Pool Multiplication", "step_text": "Pool = $250/day × 365 days/year × 3 years = $273,750.00 initial maximum coverage."},
            {"step_title": "Elimination Period Self-Pay Liability", "step_text": "During the 90-day waiting deductible, the policyholder pays out-of-pocket: 90 days × $250/day = $22,500.00."},
            {"step_title": "Compound Inflation Rider Growth", "step_text": "With a 3.0% compound rider over 20 years: Daily Benefit = $250 × 1.03²⁰ = $451.52/day. Lifetime Pool = $494,414.00."}
        ],
        "faqs": [
            {"q": "What is the elimination period in Long-Term Care insurance?", "a": "The elimination period functions like a time-deductible. It is the number of consecutive calendar or service days (typically 90 days) you must pay for care out of pocket before insurance benefits begin paying."},
            {"q": "What triggers long-term care insurance benefits?", "a": "Benefits trigger when a licensed healthcare professional certifies that you cannot perform at least 2 out of 6 Activities of Daily Living (ADLs: bathing, dressing, eating, transferring, toileting, continence) or suffer severe cognitive impairment (Alzheimer's/dementia)."}
        ],
        "js_logic": """
          const daily = getNum('daily_benefit_amount_usd');
          const yrs = getNum('benefit_period_years');
          const elim = getNum('elimination_period_days');
          const inf = (getNum('inflation_rider_pct') || 3.0) / 100;

          const pool = daily * 365 * yrs;
          const outOfPocket = elim * daily;
          const futurePool = pool * Math.pow(1 + inf, 20);
          const monthly = (daily * 365) / 12;

          setDisp('total_lifetime_pool_usd', '$' + Math.round(pool).toLocaleString());
          setDisp('elimination_out_of_pocket', '$' + Math.round(outOfPocket).toLocaleString());
          setDisp('future_pool_at_20_years', '$' + Math.round(futurePool).toLocaleString() + ' (+3% comp)');
          setDisp('monthly_benefit_allowance', '$' + Math.round(monthly).toLocaleString() + ' / mo');
        """
    },
    {
        "slug": "property-casualty-coinsurance",
        "category": "legal",
        "name": "Property Casualty Co-Insurance Penalty (80% Rule) Calculator",
        "description": "Calculate insurance payout and coinsurance penalties on commercial property claims when insurance coverage is less than 80% of replacement value.",
        "hero_badge": "Property Insurance • Coinsurance Clause",
        "formula_display": "Claim Payout = (Insurance Carried / Insurance Required) × Loss - Deductible",
        "fields": [
            {"id": "actual_building_replacement_cost", "label": "Full Building Replacement Cost ($ USD)", "default": 1000000, "prefix": "$", "min": 50000, "max": 50000000, "step": 50000, "hint": "Current 100% replacement cost at time of loss"},
            {"id": "insurance_coverage_carried", "label": "Actual Insurance Limit Carried ($)", "default": 600000, "prefix": "$", "min": 25000, "max": 40000000, "step": 25000, "hint": "Policy limit stated on declarations page"},
            {"id": "coinsurance_clause_pct", "label": "Policy Coinsurance Clause (%)", "default": 80, "suffix": "%", "min": 80, "max": 100, "step": 10, "hint": "Standard policy clause is 80% or 90%"},
            {"id": "covered_property_loss_usd", "label": "Actual Fire / Storm Loss Incurred ($)", "default": 200000, "prefix": "$", "min": 5000, "max": 10000000, "step": 5000, "hint": "Cost to repair partial property damage"},
            {"id": "policy_deductible_usd", "label": "Policy Deductible ($)", "default": 5000, "prefix": "$", "min": 500, "max": 50000, "step": 500, "hint": "Property deductible"}
        ],
        "metrics": [
            {"id": "insurer_claim_payout", "label": "Insurer Claim Check Payout", "default_display": "$145,000.00", "highlight": True},
            {"id": "coinsurance_penalty_absorbed", "label": "Coinsurance Penalty Borne by Owner", "default_display": "$50,000.00 Penalty", "highlight": True},
            {"id": "required_coverage_limit", "label": "Minimum Coverage Required", "default_display": "$800,000.00 (80%)"},
            {"id": "coverage_ratio_penalty_pct", "label": "Coinsurance Settlement Ratio", "default_display": "75.0% of Loss Paid"}
        ],
        "proof_steps": [
            {"step_title": "Insurance Required by Contract", "step_text": "Required Insurance = 100% Replacement Cost ($1,000,000) × 80% Coinsurance Clause = $800,000.00."},
            {"step_title": "Did / Should Ratio", "step_text": "Ratio = Insurance Carried ($600,000) / Insurance Required ($800,000) = 0.75 (75.0%). The property was underinsured by 25%."},
            {"step_title": "Claim Penalty Apportionment", "step_text": "Gross Claim = $200,000 Loss × 0.75 = $150,000.00. Minus $5,000 deductible = $145,000.00."},
            {"step_title": "Financial Penalty Absorbed", "step_text": "Even though the $200,000 loss was well below the $600,000 policy limit, the building owner absorbs a $50,000.00 penalty plus $5k deductible out-of-pocket."}
        ],
        "faqs": [
            {"q": "What is the Coinsurance Clause in commercial property insurance?", "a": "The coinsurance clause requires policyholders to insure their property for at least 80% (or 90%) of its true replacement cost value. If underinsured, the insurer penalizes every claim proportionally, even partial losses."},
            {"q": "How can commercial property owners waive the coinsurance penalty?", "a": "Request an Agreed Value endorsement on your policy. This suspends the coinsurance condition for one year in exchange for submitting an approved annual Statement of Values (SOV)."}
        ],
        "js_logic": """
          const cost = getNum('actual_building_replacement_cost');
          const carried = getNum('insurance_coverage_carried');
          const coPct = (getNum('coinsurance_clause_pct') || 80) / 100;
          const loss = getNum('covered_property_loss_usd');
          const ded = getNum('policy_deductible_usd');

          const req = cost * coPct;
          const ratio = req > 0 ? Math.min(1.0, carried / req) : 1.0;
          const grossPaid = loss * ratio;
          const netPaid = Math.max(0, grossPaid - ded);
          const penalty = loss - grossPaid;

          setDisp('insurer_claim_payout', '$' + Math.round(netPaid).toLocaleString());
          setDisp('coinsurance_penalty_absorbed', '$' + Math.round(penalty).toLocaleString() + (penalty > 0 ? ' Penalty' : ' (No Penalty)'));
          setDisp('required_coverage_limit', '$' + Math.round(req).toLocaleString() + ' (' + Math.round(coPct * 100) + '%)');
          setDisp('coverage_ratio_penalty_pct', (ratio * 100).toFixed(1) + '% Paid');
        """
    },
    {
        "slug": "title-insurance-reissue-rate",
        "category": "legal",
        "name": "Title Insurance Premium & Refinance Reissue Rate Calculator",
        "description": "Calculate lender and owner title insurance policy premiums, simultaneous issue discounts, and refinance reissue rate savings.",
        "hero_badge": "Real Estate Law • Title Insurance",
        "formula_display": "Reissue Premium = Standard Title Rate × (1 - Reissue Discount % [typically 30% - 40%])",
        "fields": [
            {"id": "title_policy_amount_usd", "label": "Mortgage Loan or Purchase Price ($)", "default": 450000, "prefix": "$", "min": 25000, "max": 5000000, "step": 10000, "hint": "Loan amount for lender policy, purchase price for owner policy"},
            {"id": "transaction_type", "label": "Transaction Type (1 = Purchase, 2 = Refinance Reissue)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "1 for home purchase, 2 for mortgage refinance"},
            {"id": "prior_policy_age_years", "label": "Years Since Prior Title Policy Issued", "default": 3, "suffix": "years", "min": 1, "max": 15, "step": 1, "hint": "Reissue rate eligibility requires prior policy within 5-10 years"}
        ],
        "metrics": [
            {"id": "final_title_premium_usd", "label": "Final Title Insurance Premium", "default_display": "$1,380.00", "highlight": True},
            {"id": "reissue_discount_savings", "label": "Reissue Discount Savings", "default_display": "$920.00 Saved (40% Off)", "highlight": True},
            {"id": "standard_base_rate", "label": "Full Standard Title Rate", "default_display": "$2,300.00"},
            {"id": "policy_type_issued", "label": "Coverage Form", "default_display": "Lender's ALTA Refinance Policy"}
        ],
        "proof_steps": [
            {"step_title": "Standard Graduated Title Rate Schedule", "step_text": "Standard title rate for $450,000 = ~$2,300.00 based on state-promulgated insurance rating schedules."},
            {"step_title": "Reissue Rate Eligibility", "step_text": "Because prior title insurance was issued within the last 10 years (3 years ago), the title company needs only to perform an 'update search' rather than a 40-year historical title search."},
            {"step_title": "40% Reissue Credit", "step_text": "Reissue Premium = $2,300.00 × (1 - 0.40) = $1,380.00, saving the homeowner $920.00 in closing costs."}
        ],
        "faqs": [
            {"q": "What is a title insurance reissue rate discount?", "a": "When refinancing or selling a property that had a title policy issued within the last 5 to 10 years, insurers offer a discounted 'reissue rate' (typically 30% to 40% off standard rates) because the title was already vetted and cleared recently."},
            {"q": "Do I have to buy owner's title insurance when refinancing?", "a": "No! When refinancing, you only pay for a new Lender's Title Policy to protect the new bank's first-lien mortgage. Your original Owner's Title Policy remains active for as long as you or your heirs own the home."}
        ],
        "js_logic": """
          const amount = getNum('title_policy_amount_usd');
          const isRefi = Math.round(getNum('transaction_type')) === 2;
          const yrs = getNum('prior_policy_age_years');

          let baseRate = (amount / 1000) * 5.10;
          let discPct = 0;
          if (isRefi && yrs <= 10) {
            discPct = yrs <= 3 ? 0.40 : (yrs <= 5 ? 0.35 : 0.25);
          }

          const savings = baseRate * discPct;
          const finalPrem = baseRate - savings;

          setDisp('final_title_premium_usd', '$' + Math.round(finalPrem).toLocaleString());
          setDisp('reissue_discount_savings', discPct > 0 ? '$' + Math.round(savings).toLocaleString() + ' Saved (' + Math.round(discPct * 100) + '% Off)' : 'No Reissue Discount Applicable');
          setDisp('standard_base_rate', '$' + Math.round(baseRate).toLocaleString());
          setDisp('policy_type_issued', isRefi ? "Lender's ALTA Refinance Policy" : "Owner's & Lender's Simultaneous Issue");
        """
    },
    {
        "slug": "subrogation-lien-reduction",
        "category": "legal",
        "name": "Health Insurance Subrogation Lien Reduction (Common Fund Doctrine) Calculator",
        "description": "Calculate mandatory legal reductions to health insurance and ERISA subrogation liens under the Common Fund Doctrine and Made-Whole Doctrine.",
        "hero_badge": "Healthcare Subrogation • Lien Resolution",
        "formula_display": "Net Lien = Gross Lien - (Gross Lien × Attorney Fee %) - Pro-Rata Litigation Costs",
        "fields": [
            {"id": "gross_medical_lien_usd", "label": "Asserted Health Insurance Lien ($ USD)", "default": 32000, "prefix": "$", "min": 1000, "max": 500000, "step": 500, "hint": "Original subrogation lien claimed by Blue Cross, United, Aetna"},
            {"id": "gross_tort_settlement_usd", "label": "Total Gross Tort Settlement ($)", "default": 100000, "prefix": "$", "min": 5000, "max": 2000000, "step": 5000, "hint": "Total personal injury recovery"},
            {"id": "attorney_contingency_fee_pct", "label": "Attorney Fee Percentage (%)", "default": 33.33, "suffix": "%", "min": 25, "max": 45, "step": 0.33, "hint": "Contractual attorney fee percentage"},
            {"id": "case_litigation_expenses_usd", "label": "Total Case Expenses ($)", "default": 4500, "prefix": "$", "min": 0, "max": 50000, "step": 250, "hint": "Costs advanced by law firm"}
        ],
        "metrics": [
            {"id": "reduced_lien_payout_usd", "label": "Final Compromised Lien Payoff", "default_display": "$19,894.00", "highlight": True},
            {"id": "total_lien_reduction_usd", "label": "Total Dollar Reduction Captured", "default_display": "$12,106.00 (37.8% Cut)", "highlight": True},
            {"id": "attorney_fee_deduction", "label": "Common Fund Attorney Fee Share", "default_display": "$10,666.00 Subtracted"},
            {"id": "pro_rata_expense_share", "label": "Pro-Rata Expense Share", "default_display": "$1,440.00 Subtracted"}
        ],
        "proof_steps": [
            {"step_title": "Common Fund Doctrine Equity", "step_text": "Because the attorney created the fund from which the health insurer recovers, the insurer must pay its fair share of legal fees and expenses."},
            {"step_title": "Common Fund Fee Reduction", "step_text": "Lien Fee Credit = $32,000 × 33.33% = $10,665.60."},
            {"step_title": "Pro-Rata Expense Reduction", "step_text": "Lien Share of Recovery = $32k / $100k = 32.0%. Expense Credit = $4,500 × 32.0% = $1,440.00."},
            {"step_title": "Final Compromised Lien", "step_text": "Compromised Lien = $32,000 - $10,665.60 - $1,440.00 = $19,894.40, saving the injured client $12,105.60."}
        ],
        "faqs": [
            {"q": "What is the Common Fund Doctrine in lien negotiation?", "a": "The Common Fund Doctrine is a universal equitable rule establishing that when a lawyer recovers money that benefits a third-party lienholder, that lienholder must reduce its claim by its pro-rata share of attorney fees and litigation costs."},
            {"q": "Do self-funded ERISA plans have to reduce their liens?", "a": "Federal ERISA self-funded plans are governed by federal law (US Airways v. McCutchen). If the plan document explicitly disclaims the Common Fund and Made-Whole doctrines, ERISA plans can legally demand 100% full recovery unless negotiated down by counsel."}
        ],
        "js_logic": """
          const lien = getNum('gross_medical_lien_usd');
          const settle = getNum('gross_tort_settlement_usd');
          const feePct = (getNum('attorney_contingency_fee_pct') || 33.33) / 100;
          const costs = getNum('case_litigation_expenses_usd');

          const atyCut = lien * feePct;
          const share = settle > 0 ? (lien / settle) : 0.3;
          const expCut = costs * share;
          const totalReduction = atyCut + expCut;
          const netLien = Math.max(0, lien - totalReduction);
          const cutPct = lien > 0 ? (totalReduction / lien) * 100 : 0;

          setDisp('reduced_lien_payout_usd', '$' + Math.round(netLien).toLocaleString());
          setDisp('total_lien_reduction_usd', '$' + Math.round(totalReduction).toLocaleString() + ' (' + cutPct.toFixed(1) + '% Cut)');
          setDisp('attorney_fee_deduction', '$' + Math.round(atyCut).toLocaleString() + ' Subtracted');
          setDisp('pro_rata_expense_share', '$' + Math.round(expCut).toLocaleString() + ' Subtracted');
        """
    },
    {
        "slug": "breach-of-contract-damages",
        "category": "legal",
        "name": "Breach of Contract Expectation & Consequential Damages Calculator",
        "description": "Calculate expectation damages, incidental losses, consequential lost profits (Hadley v. Baxendale rule), and mitigation offsets in commercial contract disputes.",
        "hero_badge": "Contract Law • Commercial Litigation",
        "formula_display": "Expectation Damages = (Contract Price - Mitigation Revenue) + Incidental Expenses + Consequential Damages",
        "fields": [
            {"id": "agreed_contract_price_usd", "label": "Full Agreed Contract Value ($ USD)", "default": 175000, "prefix": "$", "min": 1000, "max": 10000000, "step": 5000, "hint": "Original promised contract consideration"},
            {"id": "mitigation_resale_revenue", "label": "Mitigation Substitute Revenue ($)", "default": 95000, "prefix": "$", "min": 0, "max": 10000000, "step": 5000, "hint": "Money recovered by selling goods/services to an alternate buyer"},
            {"id": "incidental_expenses_usd", "label": "Incidental Storage & Brokering Costs ($)", "default": 8500, "prefix": "$", "min": 0, "max": 100000, "step": 500, "hint": "Storage, return freight, and re-listing expenses"},
            {"id": "consequential_lost_profits_usd", "label": "Foreseeable Consequential Damages ($)", "default": 24000, "prefix": "$", "min": 0, "max": 1000000, "step": 1000, "hint": "Downstream lost profits reasonably foreseeable at contract signing"}
        ],
        "metrics": [
            {"id": "total_recoverable_damages", "label": "Total Recoverable Breach Damages", "default_display": "$112,500.00", "highlight": True},
            {"id": "direct_expectation_loss", "label": "Direct Expectation Loss", "default_display": "$80,000.00", "highlight": True},
            {"id": "mitigation_credit_offset", "label": "Mitigation Credit Subtracted", "default_display": "$95,000.00 Offset"},
            {"id": "incidental_consequential_total", "label": "Secondary Losses Recovered", "default_display": "$32,500.00"}
        ],
        "proof_steps": [
            {"step_title": "Direct Expectation Loss", "step_text": "Direct Loss = Contract Price ($175,000) - Mitigation Cover ($95,000) = $80,000.00."},
            {"step_title": "Incidental Breach Expenses", "step_text": "Costs incurred in finding a substitute buyer (warehousing, brokers) = $8,500.00."},
            {"step_title": "Hadley v. Baxendale Consequential Foreseeability", "step_text": "Consequential lost profits = $24,000.00 recoverable because both parties contemplated downstream production delays at contract formation."},
            {"step_title": "Total Restitution Judgment", "step_text": "Total Recovery = $80,000 + $8,500 + $24,000 = $112,500.00 puts plaintiff in the exact financial position performance would have."}
        ],
        "faqs": [
            {"q": "What is the Duty to Mitigate in contract law?", "a": "Under the doctrine of avoidable consequences, a non-breaching party cannot recover damages that could have been avoided with reasonable effort (e.g. attempting to re-sell custom goods or hiring substitute contractors)."},
            {"q": "Can you recover punitive damages in a breach of contract lawsuit?", "a": "No. In American contract law, punitive damages are strictly barred for simple breach of contract unless the breach is accompanied by an independent intentional tort such as common law fraud or conversion."}
        ],
        "js_logic": """
          const price = getNum('agreed_contract_price_usd');
          const mit = getNum('mitigation_resale_revenue');
          const inc = getNum('incidental_expenses_usd');
          const con = getNum('consequential_lost_profits_usd');

          const direct = Math.max(0, price - mit);
          const totalDamages = direct + inc + con;

          setDisp('total_recoverable_damages', '$' + Math.round(totalDamages).toLocaleString());
          setDisp('direct_expectation_loss', '$' + Math.round(direct).toLocaleString());
          setDisp('mitigation_credit_offset', '$' + Math.round(mit).toLocaleString() + ' Offset');
          setDisp('incidental_consequential_total', '$' + Math.round(inc + con).toLocaleString());
        """
    },
    {
        "slug": "medical-malpractice-damages-cap",
        "category": "legal",
        "name": "Medical Malpractice Noneconomic Damages Cap Adjustment Calculator",
        "description": "Calculate medical malpractice verdict reductions, applying state statutory noneconomic damage caps (e.g. California MICRA, Texas, Florida, Ohio).",
        "hero_badge": "Health Law • Malpractice Tort Reform",
        "formula_display": "Total Payout = Proven Economic Damages + min(Jury Noneconomic Award, Statutory Cap)",
        "fields": [
            {"id": "economic_damages_usd", "label": "Proven Economic Damages ($ USD)", "default": 850000, "prefix": "$", "min": 50000, "max": 20000000, "step": 50000, "hint": "Past/future medical bills and lifetime lost wages (uncapped)"},
            {"id": "jury_noneconomic_verdict", "label": "Jury Noneconomic Verdict (Pain & Suffering $)", "default": 1500000, "prefix": "$", "min": 50000, "max": 50000000, "step": 100000, "hint": "Jury award for physical pain and loss of quality of life"},
            {"id": "state_statutory_cap_usd", "label": "State Statutory Noneconomic Cap ($)", "default": 350000, "prefix": "$", "min": 250000, "max": 1500000, "step": 25000, "hint": "California MICRA (AB 35) = $350k injury / $500k wrongful death"}
        ],
        "metrics": [
            {"id": "final_reduced_payout_usd", "label": "Final Enforceable Court Judgment", "default_display": "$1,200,000.00", "highlight": True},
            {"id": "noneconomic_verdict_slashed", "label": "Verdict Reduction (Tort Reform Cut)", "default_display": "-$1,150,000.00 Slashed", "highlight": True},
            {"id": "effective_recovery_pct", "label": "Client Percentage of Jury Verdict", "default_display": "51.1% of Original Jury Verdict", "highlight": True},
            {"id": "economic_payout_uncapped", "label": "Economic Damages (100% Preserved)", "default_display": "$850,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Original Jury Verdict", "step_text": "Jury awarded $850,000 economic + $1,500,000 noneconomic = $2,350,000.00."},
            {"step_title": "Statutory Cap Application", "step_text": "State law caps pain and suffering at $350,000.00. The judge enters a remittitur slashing noneconomic damages from $1.5M to $350,000."},
            {"step_title": "Final Reduced Judgment", "step_text": "Final Judgment = $850,000 (uncapped economic) + $350,000 (capped noneconomic) = $1,200,000.00 ($1,150,000 eliminated by statute)."}
        ],
        "faqs": [
            {"q": "What is California AB 35 (MICRA reform)?", "a": "For 47 years, California capped noneconomic malpractice damages at $250,000. Assembly Bill 35 modernized MICRA starting in 2023, raising the cap to $350,000 for injuries (escalating to $750k over 10 years) and $500,000 for wrongful death (escalating to $1M)."},
            {"q": "Are past and future medical bills capped in malpractice claims?", "a": "No! In all 50 states, actual past medical expenses, future lifetime nursing care, and lost earnings are classified as economic damages and are 100% exempt from statutory damage caps."}
        ],
        "js_logic": """
          const econ = getNum('economic_damages_usd');
          const nonEcon = getNum('jury_noneconomic_verdict');
          const cap = getNum('state_statutory_cap_usd');

          const cappedNonEcon = Math.min(nonEcon, cap);
          const finalJudg = econ + cappedNonEcon;
          const origJury = econ + nonEcon;
          const slashed = nonEcon - cappedNonEcon;
          const pct = origJury > 0 ? (finalJudg / origJury) * 100 : 100;

          setDisp('final_reduced_payout_usd', '$' + Math.round(finalJudg).toLocaleString());
          setDisp('noneconomic_verdict_slashed', (slashed > 0 ? '-$' + Math.round(slashed).toLocaleString() + ' Slashed' : '$0.00 (Under Cap)'));
          setDisp('effective_recovery_pct', pct.toFixed(1) + '% of Jury Verdict');
          setDisp('economic_payout_uncapped', '$' + Math.round(econ).toLocaleString() + ' (100% Paid)');
        """
    },
    {
        "slug": "legal-billing-realization-rate",
        "category": "legal",
        "name": "Law Firm Billing Realization & Collection Rate Productivity Calculator",
        "description": "Calculate billing realization rate, collection rate, write-down write-off leakage, and true hourly collected rate for law firm partners and associates.",
        "hero_badge": "Law Firm Practice Management • Financial Metrics",
        "formula_display": "Overall Realization = (Billed Hours / Logged Hours) × (Collected Revenue / Billed Revenue)",
        "fields": [
            {"id": "logged_billable_hours", "label": "Logged Billable Hours (Timesheet)", "default": 1800, "suffix": "hours/yr", "min": 200, "max": 3000, "step": 50, "hint": "Raw billable hours tracked by attorney"},
            {"id": "standard_hourly_billing_rate", "label": "Standard Hourly Billing Rate ($/hr)", "default": 475, "prefix": "$", "min": 100, "max": 2000, "step": 25, "hint": "Partner or associate standard card rate"},
            {"id": "billing_realization_pct", "label": "Billing Realization Rate (%)", "default": 91.0, "suffix": "%", "min": 70, "max": 100, "step": 0.5, "hint": "Percentage of logged time actually invoiced to clients (after partner write-downs)"},
            {"id": "collection_realization_pct", "label": "Collection Realization Rate (%)", "default": 94.0, "suffix": "%", "min": 70, "max": 100, "step": 0.5, "hint": "Percentage of invoiced fees collected in cash (after client fee disputes)"}
        ],
        "metrics": [
            {"id": "total_annual_cash_collected", "label": "Total Cash Fee Collections", "default_display": "$730,950.00 / yr", "highlight": True},
            {"id": "overall_realization_rate", "label": "Overall Realization Rate", "default_display": "85.5% Net Yield", "highlight": True},
            {"id": "effective_collected_hourly_rate", "label": "Effective Realized Hourly Rate", "default_display": "$406.08 / hour", "highlight": True},
            {"id": "annual_revenue_leakage", "label": "Annual Write-Down Fee Leakage", "default_display": "$124,050.00 Lost to Write-Downs"}
        ],
        "proof_steps": [
            {"step_title": "Standard Value Potential", "step_text": "Gross Standard Value = 1,800 hours × $475/hr = $855,000.00."},
            {"step_title": "Billing Realization Haircut", "step_text": "Billed Invoices = $855,000 × 91% = $778,050.00 ($76,950 written down by billing partner)."},
            {"step_title": "Collection Realization Cash Receipt", "step_text": "Collected Cash = $778,050 × 94% = $731,367.00 ($46,683 uncollected or disputed)."},
            {"step_title": "Effective Realized Rate", "step_text": "Overall Realization = 91% × 94% = 85.54%. True Realized Hourly Rate = $731,367 / 1,800 hours = $406.32/hour."}
        ],
        "faqs": [
            {"q": "What is the difference between billing realization and collection realization?", "a": "Billing realization is the percentage of logged lawyer hours that actually make it onto the invoice sent to the client. Collection realization is the percentage of that invoiced amount that the client actually pays."},
            {"q": "What is considered a healthy realization rate in law firms?", "a": "AmLaw 200 benchmarks target 92% to 95% billing realization and 95% to 97% collection realization, yielding an overall realization rate above 88%."}
        ],
        "js_logic": """
          const hrs = getNum('logged_billable_hours');
          const rate = getNum('standard_hourly_billing_rate');
          const billReal = (getNum('billing_realization_pct') || 91) / 100;
          const collReal = (getNum('collection_realization_pct') || 94) / 100;

          const standardVal = hrs * rate;
          const billedVal = standardVal * billReal;
          const collectedVal = billedVal * collReal;
          const overallReal = billReal * collReal;
          const effRate = hrs > 0 ? (collectedVal / hrs) : rate;
          const leakage = standardVal - collectedVal;

          setDisp('total_annual_cash_collected', '$' + Math.round(collectedVal).toLocaleString() + ' / yr');
          setDisp('overall_realization_rate', (overallReal * 100).toFixed(1) + '% Net Yield');
          setDisp('effective_collected_hourly_rate', '$' + effRate.toFixed(2) + ' / hr');
          setDisp('annual_revenue_leakage', '$' + Math.round(leakage).toLocaleString() + ' Lost');
        """
    },
    {
        "slug": "punitive-compensatory-ratio",
        "category": "legal",
        "name": "Punitive-to-Compensatory Damages Ratio Compliance (SCOTUS Due Process)",
        "description": "Calculate punitive-to-compensatory damages ratios and test constitutional compliance under U.S. Supreme Court 14th Amendment Due Process precedents.",
        "hero_badge": "Constitutional Tort Law • SCOTUS Precedent",
        "formula_display": "Punitive Ratio = Punitive Damages Award / Total Compensatory Damages (Single-Digit Ratio Rule)",
        "fields": [
            {"id": "compensatory_damages_award", "label": "Actual Compensatory Damages Verdict ($)", "default": 750000, "prefix": "$", "min": 10000, "max": 50000000, "step": 25000, "hint": "Jury verdict for actual medical, lost wage, and pain damages"},
            {"id": "punitive_damages_jury_award", "label": "Jury Punitive Damages Award ($)", "default": 6500000, "prefix": "$", "min": 0, "max": 100000000, "step": 100000, "hint": "Jury punishment award for malicious or reckless conduct"},
            {"id": "reprehensibility_tier", "label": "Defendant Reprehensibility (1 = Financial Harm, 2 = Physical/Health Recklessness)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "State Farm v. Campbell reprehensibility standard"}
        ],
        "metrics": [
            {"id": "punitive_to_compensatory_ratio", "label": "Punitive Ratio Multiple", "default_display": "8.67x Ratio", "highlight": True},
            {"id": "scotus_due_process_status", "label": "Constitutional Due Process Risk", "default_display": "Vulnerable on Appeal (> 4:1 Ratio)", "highlight": True},
            {"id": "recommended_remittitur_target", "label": "Likely Post-Appeal Capped Award", "default_display": "$3,000,000.00 (4:1 Benchmark)", "highlight": True},
            {"id": "total_payout_after_appeal", "label": "Projected Final Enforceable Verdict", "default_display": "$3,750,000.00"}
        ],
        "proof_steps": [
            {"step_title": "Numerical Ratio Formulation", "step_text": "Ratio = Punitive Damages ($6,500,000) / Compensatory Damages ($750,000) = 8.67:1."},
            {"step_title": "SCOTUS Landmark Precedents", "step_text": "In State Farm v. Campbell (2003) and BMW v. Gore (1996), the U.S. Supreme Court held that punitive awards exceeding a single-digit ratio (9:1) violate 14th Amendment Due Process, and that ratios exceeding 4:1 are constitutionally suspect when compensatory damages are substantial."},
            {"step_title": "Judicial Remittitur Forecast", "step_text": "Appellate courts routinely enter remittitur capping punitive damages at 4x compensatory damages ($750,000 × 4 = $3,000,000.00), reducing the total award to $3,750,000.00."}
        ],
        "faqs": [
            {"q": "Can punitive damages ever exceed a 9:1 ratio constitutionally?", "a": "Yes, but only in rare cases where the defendant's conduct was egregious but resulted in only small or nominal compensatory damages (e.g. $10,000 in actual injury). When compensatory damages are already large ($1M+), a 1:1 or 2:1 ratio is often the constitutional ceiling."},
            {"q": "What factors determine 'reprehensibility' under BMW v. Gore?", "a": "1) Whether harm was physical rather than purely economic; 2) indifference to health and safety; 3) whether the victim was financially vulnerable; 4) repeated misconduct vs isolated incident; 5) intentional malice or deceit."}
        ],
        "js_logic": """
          const comp = getNum('compensatory_damages_award');
          const pun = getNum('punitive_damages_jury_award');
          const rep = Math.round(getNum('reprehensibility_tier')) || 2;

          const ratio = comp > 0 ? (pun / comp) : 99;
          let status = 'Constitutional (Within Single-Digit Limits)';
          let maxRatio = rep === 2 ? 4.0 : 2.0;

          if (ratio > 9.0) {
            status = 'UNCONSTITUTIONAL (Exceeds Single-Digit Limit)';
          } else if (ratio > 4.0) {
            status = 'High Reversal Risk (> 4:1 Benchmark)';
          }

          const remittiturPun = Math.min(pun, comp * maxRatio);
          const finalTotal = comp + remittiturPun;

          setDisp('punitive_to_compensatory_ratio', ratio.toFixed(2) + 'x Ratio');
          setDisp('scotus_due_process_status', status);
          setDisp('recommended_remittitur_target', '$' + Math.round(remittiturPun).toLocaleString() + ' (' + maxRatio + ':1 Target)');
          setDisp('total_payout_after_appeal', '$' + Math.round(finalTotal).toLocaleString());
        """
    },
    {
        "slug": "trademark-registration-fees",
        "category": "legal",
        "name": "USPTO Trademark Filing Fees & Multi-Class Madrid Protocol Calculator",
        "description": "Calculate United States Patent and Trademark Office (USPTO TEAS Plus) filing fees, international class additions, and Section 8/9 renewal costs.",
        "hero_badge": "Intellectual Property • Trademark Filing",
        "formula_display": "Total USPTO Filing Cost = Number of International Classes × Fee per Class ($250 TEAS Plus)",
        "fields": [
            {"id": "international_classes_count", "label": "Number of International Classes (Nice Classification)", "default": 2, "suffix": "classes", "min": 1, "max": 45, "step": 1, "hint": "Goods/services categories (e.g. Class 9 Software, Class 42 SaaS)"},
            {"id": "filing_basis", "label": "Filing Basis (1 = 1(a) In-Use, 2 = 1(b) Intent-to-Use)", "default": 2, "min": 1, "max": 2, "step": 1, "hint": "1(a) Already in commerce; 1(b) Plan to use in future (requires $100 Statement of Use later)"},
            {"id": "attorney_legal_fee_usd", "label": "Trademark Attorney Legal Fee ($)", "default": 750, "prefix": "$", "min": 0, "max": 5000, "step": 50, "hint": "Search clearance and application preparation legal fee"}
        ],
        "metrics": [
            {"id": "total_initial_filing_cost", "label": "Total Initial Investment", "default_display": "$1,250.00", "highlight": True},
            {"id": "uspto_statutory_fees", "label": "USPTO Government Filing Fees", "default_display": "$500.00 (2 Classes @ $250)", "highlight": True},
            {"id": "future_statement_of_use_fee", "label": "Future Statement of Use Govt Fee", "default_display": "$200.00 ($100 / class for 1(b))"},
            {"id": "renewal_timeline_reminder", "label": "Next Regulatory Deadline", "default_display": "Section 8 Affidavit due in Year 5–6"}
        ],
        "proof_steps": [
            {"step_title": "USPTO Statutory Class Fees", "step_text": "TEAS Plus filing fee = $250.00 per class. For 2 classes (e.g. Goods & Services): 2 × $250 = $500.00."},
            {"step_title": "Intent-to-Use (ITU) Subsequent Costs", "step_text": "Under Section 1(b), filing a Statement of Use (SOU) when goods launch costs $100.00 per class ($200.00 total)."},
            {"step_title": "Turnkey Intellectual Property Outflow", "step_text": "Initial Cost = $500 USPTO fees + $750 Attorney legal preparation = $1,250.00."}
        ],
        "faqs": [
            {"q": "What is the difference between TEAS Plus and TEAS Standard?", "a": "TEAS Plus costs $250 per class and requires choosing pre-approved goods/services descriptions from the USPTO ID Manual. TEAS Standard costs $350 per class and allows custom free-form descriptions."},
            {"q": "What maintenance filings are required to keep a trademark active?", "a": "Between the 5th and 6th year after registration, you must file a Section 8 Declaration of Continued Use ($225/class). Between the 9th and 10th year, you must file a combined Section 8 and Section 9 Renewal ($525/class) every 10 years indefinitely."}
        ],
        "js_logic": """
          const classes = Math.max(1, Math.round(getNum('international_classes_count')) || 1);
          const isItu = Math.round(getNum('filing_basis')) === 2;
          const atty = getNum('attorney_legal_fee_usd');

          const uspto = classes * 250;
          const ituFee = isItu ? (classes * 100) : 0;
          const totalInitial = uspto + atty;

          setDisp('total_initial_filing_cost', '$' + Math.round(totalInitial).toLocaleString());
          setDisp('uspto_statutory_fees', '$' + Math.round(uspto).toLocaleString() + ' (' + classes + ' Classes @ $250)');
          setDisp('future_statement_of_use_fee', isItu ? '$' + ituFee + ' ($100/class for 1(b))' : '$0.00 (1(a) In-Commerce)');
          setDisp('renewal_timeline_reminder', 'Section 8 Affidavit due in Year 5–6');
        """
    },
    {
        "slug": "workers-comp-emr-modifier",
        "category": "legal",
        "name": "Workers' Comp Experience Modification Rate (EMR) Premium Impact",
        "description": "Calculate Experience Modification Rate (EMR / Mod) financial impact, workers' compensation insurance premium surcharges, and credit discounts.",
        "hero_badge": "Risk Management • EMR Modifiers",
        "formula_display": "Modified Premium = Manual Base Premium × Experience Modification Factor (EMR)",
        "fields": [
            {"id": "manual_base_premium_usd", "label": "Manual Base Workers' Comp Premium ($ USD)", "default": 85000, "prefix": "$", "min": 5000, "max": 2000000, "step": 2500, "hint": "Payroll × class code rates before experience rating"},
            {"id": "current_emr_factor", "label": "Current Experience Mod (EMR)", "default": 1.25, "min": 0.50, "max": 2.50, "step": 0.05, "hint": "1.00 is industry average. > 1.00 is debit surcharge, < 1.00 is credit discount"},
            {"id": "best_possible_emr", "label": "Minimum Achievable Zero-Loss EMR", "default": 0.75, "min": 0.50, "max": 0.95, "step": 0.05, "hint": "Theoretical minimum mod if company had zero claims over 3 years"}
        ],
        "metrics": [
            {"id": "actual_premium_billed", "label": "Modified Annual Premium Billed", "default_display": "$106,250.00", "highlight": True},
            {"id": "annual_emr_penalty_surcharge", "label": "Annual EMR Debit Penalty Paid", "default_display": "+$21,250.00 Surcharge", "highlight": True},
            {"id": "controllable_safety_savings", "label": "Controllable Safety Savings Potential", "default_display": "$42,500.00 / yr", "highlight": True},
            {"id": "emr_standing_status", "label": "Safety Risk Rating", "default_display": "Debit Mod (High Claim Frequency)"}
        ],
        "proof_steps": [
            {"step_title": "Manual Base Premium", "step_text": "Manual Base Premium = $85,000.00."},
            {"step_title": "EMR Multiplier Application", "step_text": "Modified Premium = Manual Premium × EMR = $85,000 × 1.25 = $106,250.00."},
            {"step_title": "Direct Debit Surcharge Penalty", "step_text": "Penalty Paid = $106,250 - $85,000 = +$21,250.00 extra annual premium caused by past workplace injuries."},
            {"step_title": "Controllable Safety Premium Spread", "step_text": "Best Possible Premium (0.75 Mod) = $85,000 × 0.75 = $63,750.00. Controllable Safety Spread = $106,250 - $63,750 = $42,500.00/year."}
        ],
        "faqs": [
            {"q": "What is an Experience Modification Rate (EMR) in construction?", "a": "An EMR is an actuarial multiplier calculated by NCCI based on a company's past 3 years of workers' comp claims. An EMR of 1.00 is average; an EMR of 1.25 increases premiums by 25%; an EMR of 0.80 discounts premiums by 20%."},
            {"q": "Why do general contractors disqualify subcontractors with EMR above 1.0?", "a": "Major general contractors and government agencies refuse to hire subcontractors with an EMR above 1.00 because high mods signal poor safety culture, leading to project OSHA shut-downs and heightened site liability."}
        ],
        "js_logic": """
          const base = getNum('manual_base_premium_usd');
          const emr = getNum('current_emr_factor') || 1.25;
          const bestEmr = getNum('best_possible_emr') || 0.75;

          const billed = base * emr;
          const delta = billed - base;
          const bestBilled = base * bestEmr;
          const controllable = billed - bestBilled;

          let status = 'Industry Average (1.00)';
          if (emr > 1.0) status = 'Debit Surcharge (Adverse Claims)';
          else if (emr < 1.0) status = 'Credit Discount (Superior Safety)';

          setDisp('actual_premium_billed', '$' + Math.round(billed).toLocaleString());
          setDisp('annual_emr_penalty_surcharge', (delta >= 0 ? '+$' : '-$') + Math.abs(Math.round(delta)).toLocaleString() + (delta >= 0 ? ' Surcharge' : ' Discount'));
          setDisp('controllable_safety_savings', '$' + Math.round(controllable).toLocaleString() + ' / yr');
          setDisp('emr_standing_status', status);
        """
    }
]
