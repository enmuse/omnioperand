"""
scripts/data_energy_solar.py
25 High-Value Clean Energy, Solar, Storage, Electrical & HVAC Engineering Calculators.
Strict Zero Raw LaTeX Mandate: Clean mathematical Unicode only.
"""

ENERGY_CALCULATORS = [
    {
        "slug": "solar-payback",
        "category": "energy",
        "name": "Solar PV System Payback & ROI Calculator",
        "description": "Calculate exact simple payback period, net present value (NPV), and 25-year lifetime savings of a residential or commercial solar photovoltaic installation.",
        "hero_badge": "Clean Energy • Solar Economics Matrix",
        "formula_display": "Payback Years = Net Installed Cost / Annual Year-1 Electric Savings",
        "fields": [
            {"id": "system_cost", "label": "Gross System Cost ($)", "default": 24000, "prefix": "$", "min": 5000, "max": 150000, "step": 500, "hint": "Turnkey installation price before incentives"},
            {"id": "tax_credit_pct", "label": "Federal Investment Tax Credit (ITC %)", "default": 30, "suffix": "%", "min": 0, "max": 50, "step": 1, "hint": "Federal Section 25D/48 tax credit rate"},
            {"id": "annual_kwh", "label": "Annual Generation (kWh)", "default": 11500, "suffix": "kWh", "min": 1000, "max": 100000, "step": 250, "hint": "Year 1 estimated AC kilowatt-hour production"},
            {"id": "utility_rate", "label": "Current Utility Electricity Rate ($/kWh)", "default": 0.18, "prefix": "$", "min": 0.05, "max": 0.60, "step": 0.01, "hint": "Blended residential price per kilowatt-hour"},
            {"id": "rate_escalation", "label": "Annual Utility Rate Inflation (%)", "default": 3.5, "suffix": "%", "min": 0, "max": 10, "step": 0.25, "hint": "Historic utility rate inflation trend"}
        ],
        "metrics": [
            {"id": "payback_years", "label": "Simple Payback Period", "default_display": "7.5 years", "highlight": True},
            {"id": "net_cost", "label": "Net Capital Outflow (After ITC)", "default_display": "$16,800.00", "highlight": True},
            {"id": "year1_savings", "label": "Year 1 Electricity Savings", "default_display": "$2,070.00"},
            {"id": "lifetime_savings", "label": "25-Year Cumulative Savings", "default_display": "$67,420.00"}
        ],
        "proof_steps": [
            {"step_title": "Net System Capital Outflow", "step_text": "Net Capital Cost C_net = Gross Cost × (1 - ITC / 100). For a $24,000 system with 30% ITC: $24,000 × 0.70 = $16,800."},
            {"step_title": "Year-1 Avoided Utility Cost", "step_text": "Annual Savings S₁ = Annual kWh × Utility Rate ($/kWh). Initial savings = 11,500 kWh × $0.18 = $2,070.00/year."},
            {"step_title": "Amortized Payback Horizon", "step_text": "Compounded Payback T is solved where ∑ (S₁ · (1 + g)ᵗ) = C_net, incorporating utility rate escalation g = 3.5%."},
            {"step_title": "25-Year Levelized Value", "step_text": "Solar modules degrade at ~0.5%/year while utility costs rise at ~3.5%/year, generating substantial net cash flow after payback."}
        ],
        "faqs": [
            {"q": "What is the average payback period for residential solar?", "a": "Nationwide, residential solar systems achieve breakeven within 6 to 9 years depending on local utility tariffs, solar irradiance (peak sun hours), and net metering policies."},
            {"q": "How does the federal solar tax credit (ITC) work?", "a": "The Section 25D Residential Clean Energy Credit allows taxpayers to deduct 30% of total installation costs directly from their federal income tax liability with unlimited rollover."}
        ],
        "js_logic": """
          const cost = getNum('system_cost');
          const itc = (getNum('tax_credit_pct') || 30) / 100;
          const kwh = getNum('annual_kwh');
          const rate = getNum('utility_rate');
          const esc = (getNum('rate_escalation') || 3.5) / 100;

          const netCost = cost * (1 - itc);
          const y1Savings = kwh * rate;

          let cumSavings = 0;
          let payback = 25;
          let paybackFound = false;

          for (let yr = 1; yr <= 25; yr++) {
            const yrRate = rate * Math.pow(1 + esc, yr - 1);
            const yrProd = kwh * Math.pow(1 - 0.005, yr - 1);
            const yrSavings = yrProd * yrRate;
            cumSavings += yrSavings;
            if (!paybackFound && cumSavings >= netCost) {
              const prev = cumSavings - yrSavings;
              const fraction = (netCost - prev) / (yrSavings || 1);
              payback = (yr - 1) + fraction;
              paybackFound = true;
            }
          }

          const netLifetime = cumSavings - netCost;

          setDisp('payback_years', paybackFound ? payback.toFixed(1) + ' years' : '> 25 years');
          setDisp('net_cost', '$' + Math.round(netCost).toLocaleString());
          setDisp('year1_savings', '$' + Math.round(y1Savings).toLocaleString());
          setDisp('lifetime_savings', '$' + Math.round(netLifetime).toLocaleString());
        """
    },
    {
        "slug": "solar-pv-sizing",
        "category": "energy",
        "name": "Solar PV System Sizing & DC kW Array Calculator",
        "description": "Determine the exact DC kilowatt rating and number of solar panels required to offset 100% of annual household or facility electrical consumption.",
        "hero_badge": "Photovoltaic Sizing • System Capacity",
        "formula_display": "Required DC kW = Annual kWh Demand / (365 × Daily Peak Sun Hours × Derate Factor)",
        "fields": [
            {"id": "annual_usage_kwh", "label": "Annual Electricity Usage (kWh)", "default": 12000, "suffix": "kWh", "min": 2000, "max": 150000, "step": 500, "hint": "Sum of 12 monthly electric bills"},
            {"id": "peak_sun_hours", "label": "Daily Peak Sun Hours", "default": 4.5, "suffix": "hrs/day", "min": 2.5, "max": 7.0, "step": 0.1, "hint": "Average equivalent solar irradiance (kWh/m²/day)"},
            {"id": "derate_factor", "label": "System Performance Ratio", "default": 0.82, "min": 0.65, "max": 0.95, "step": 0.01, "hint": "Losses from inverter, wiring, dust, and temperature"},
            {"id": "panel_wattage", "label": "Panel Rated Wattage (Watts DC)", "default": 410, "suffix": "W", "min": 300, "max": 650, "step": 5, "hint": "Rated nameplate capacity per solar module"},
            {"id": "target_offset_pct", "label": "Target Energy Offset (%)", "default": 100, "suffix": "%", "min": 25, "max": 150, "step": 5, "hint": "Desired percentage of electric bill to offset"}
        ],
        "metrics": [
            {"id": "system_size_kw", "label": "Recommended DC System Size", "default_display": "8.9 kW DC", "highlight": True},
            {"id": "panel_count", "label": "Required Number of Panels", "default_display": "22 panels", "highlight": True},
            {"id": "roof_area_sqft", "label": "Estimated Roof Space Required", "default_display": "430 sq ft"},
            {"id": "daily_generation", "label": "Avg Daily AC Energy Produced", "default_display": "32.8 kWh"}
        ],
        "proof_steps": [
            {"step_title": "Daily Generation Benchmark", "step_text": "Target Daily Generation E_daily = (Annual kWh × Offset% / 100) / 365. For 12,000 kWh at 100%: 32.88 kWh/day."},
            {"step_title": "DC Nameplate Power Sizing", "step_text": "P_dc = E_daily / (Daily Sun Hours × Derate Factor). With 4.5 sun hours and 0.82 derate factor: 32.88 / (4.5 × 0.82) = 8.91 kW DC."},
            {"step_title": "Module Quantity Derivation", "step_text": "Number of Modules N = Ceil((P_dc × 1000) / Module Watts). With 410W modules: 8,910W / 410W = 21.7 ➔ 22 modules."},
            {"step_title": "Spatial Footprint Footing", "step_text": "Standard 400W+ residential modules measure ~19.5 sq ft (1.82 m²). Required footprint = 22 × 19.5 ≈ 430 sq ft."}
        ],
        "faqs": [
            {"q": "What are Peak Sun Hours?", "a": "A peak sun hour is an hour during which solar irradiance averages 1,000 watts per square meter (1 kW/m²). It does not equal daylight hours."},
            {"q": "Can I install more than 100% solar offset?", "a": "Many utilities cap residential grid interconnection at 100% to 120% of historical 12-month electrical consumption to prevent uncompensated grid backfeeding."}
        ],
        "js_logic": """
          const usage = getNum('annual_usage_kwh');
          const sun = getNum('peak_sun_hours') || 4.5;
          const derate = getNum('derate_factor') || 0.82;
          const watts = getNum('panel_wattage') || 410;
          const offset = (getNum('target_offset_pct') || 100) / 100;

          const targetAnnual = usage * offset;
          const dailyTarget = targetAnnual / 365;
          const kwDc = dailyTarget / (sun * derate);
          const totalWatts = kwDc * 1000;
          const panels = Math.ceil(totalWatts / watts);
          const roofSqft = panels * 19.6;

          setDisp('system_size_kw', kwDc.toFixed(1) + ' kW DC');
          setDisp('panel_count', panels + ' panels');
          setDisp('roof_area_sqft', Math.round(roofSqft) + ' sq ft');
          setDisp('daily_generation', (kwDc * sun * derate).toFixed(1) + ' kWh');
        """
    },
    {
        "slug": "battery-backup-storage",
        "category": "energy",
        "name": "Home Battery Backup Duration & Storage Calculator",
        "description": "Calculate backup run-time duration in hours and days for home battery systems (Tesla Powerwall, Enphase, SolarEdge) under essential or whole-home load.",
        "hero_badge": "Energy Storage • Runtime Matrix",
        "formula_display": "Backup Hours = (Usable Battery kWh × Depth of Discharge × Inverter Efficiency) / Continuous Load kW",
        "fields": [
            {"id": "battery_capacity_kwh", "label": "Nominal Battery Capacity (kWh)", "default": 27.0, "suffix": "kWh", "min": 3.0, "max": 100.0, "step": 0.5, "hint": "Total battery pack energy (e.g. 2x Powerwall = 27 kWh)"},
            {"id": "dod_pct", "label": "Max Depth of Discharge (DoD %)", "default": 95, "suffix": "%", "min": 80, "max": 100, "step": 1, "hint": "Manufacturer usable battery reserve"},
            {"id": "continuous_load_w", "label": "Average Critical Load (Watts)", "default": 1800, "suffix": "W", "min": 200, "max": 15000, "step": 50, "hint": "Sump pump, refrigerator, lighting, router, essentials"},
            {"id": "solar_recharge_kwh", "label": "Daily Solar Recharge Input (kWh/day)", "default": 15.0, "suffix": "kWh/day", "min": 0, "max": 60, "step": 1, "hint": "Solar energy replenishment during daylight"},
            {"id": "inverter_eff_pct", "label": "Inverter Round-Trip Efficiency (%)", "default": 90, "suffix": "%", "min": 80, "max": 98, "step": 1, "hint": "DC-to-AC and battery round-trip efficiency"}
        ],
        "metrics": [
            {"id": "zero_solar_hours", "label": "Standalone Runtime (No Solar)", "default_display": "12.8 hours", "highlight": True},
            {"id": "net_daily_duration", "label": "Off-Grid Resilience Horizon", "default_display": "Indefinite (> 7 days)", "highlight": True},
            {"id": "usable_stored_kwh", "label": "Usable Stored AC Energy", "default_display": "23.1 kWh"},
            {"id": "daily_load_kwh", "label": "24-Hour Energy Consumption", "default_display": "43.2 kWh"}
        ],
        "proof_steps": [
            {"step_title": "Usable Storage Capacity", "step_text": "E_usable = Battery kWh × (DoD% / 100) × (Efficiency% / 100). For 27 kWh at 95% DoD and 90% efficiency: 27 × 0.95 × 0.90 = 23.085 kWh."},
            {"step_title": "Continuous Standalone Depletion", "step_text": "T_standalone = E_usable / (Critical Load in kW). At 1,800W (1.8 kW): 23.085 / 1.8 = 12.825 hours of continuous runtime without sun."},
            {"step_title": "Solar Replenishment Equilibrium", "step_text": "Daily Load = 1.8 kW × 24 hrs = 43.2 kWh. If Solar Input (15 kWh) < Daily Load (43.2 kWh), net deficit = 28.2 kWh/day."},
            {"step_title": "Multi-Day Emergency Horizon", "step_text": "Resilience Days = E_usable / Max(0.1, Daily Consumption - Solar Input)."}
        ],
        "faqs": [
            {"q": "Can a home battery run central air conditioning?", "a": "Yes, but standard 3 to 5-ton central AC units draw 3,500W to 5,000W running power with high LRA (Locked Rotor Amps) starting surges, requiring a soft-starter and multi-battery stack."},
            {"q": "What is the difference between AC-coupled and DC-coupled batteries?", "a": "DC-coupled batteries connect directly to the solar charge controller with higher efficiency (~95%), while AC-coupled batteries include dedicated inverters that connect easily to existing solar arrays."}
        ],
        "js_logic": """
          const cap = getNum('battery_capacity_kwh');
          const dod = (getNum('dod_pct') || 95) / 100;
          const loadW = getNum('continuous_load_w') || 1800;
          const solar = getNum('solar_recharge_kwh');
          const eff = (getNum('inverter_eff_pct') || 90) / 100;

          const usableKwh = cap * dod * eff;
          const loadKw = loadW / 1000;
          const standaloneHrs = usableKwh / (loadKw || 0.1);
          const dailyConsumption = loadKw * 24;
          const dailyDeficit = dailyConsumption - solar;

          let resilienceText = '';
          if (dailyDeficit <= 0) {
            resilienceText = 'Indefinite Sustained';
          } else {
            const days = usableKwh / dailyDeficit;
            resilienceText = days >= 1 ? days.toFixed(1) + ' days' : (days * 24).toFixed(1) + ' hours';
          }

          setDisp('zero_solar_hours', standaloneHrs.toFixed(1) + ' hours');
          setDisp('net_daily_duration', resilienceText);
          setDisp('usable_stored_kwh', usableKwh.toFixed(1) + ' kWh');
          setDisp('daily_load_kwh', dailyConsumption.toFixed(1) + ' kWh');
        """
    },
    {
        "slug": "heat-pump-cop-efficiency",
        "category": "energy",
        "name": "Heat Pump Seasonal COP & HSPF2 Energy Savings Calculator",
        "description": "Calculate operating electricity cost and heating dollar savings when upgrading from baseboard, furnace, or boiler heating to a modern inverter heat pump.",
        "hero_badge": "Thermal Efficiency • Heat Pump Matrix",
        "formula_display": "Heat Pump kWh = Heating Load BTU / (COP × 3,412.14) | COP = HSPF2 / 3.412",
        "fields": [
            {"id": "heating_load_therms", "label": "Annual Heating Demand (Therms or Equiv)", "default": 850, "suffix": "Therms", "min": 200, "max": 4000, "step": 25, "hint": "1 Therm = 100,000 BTU = 29.3 kWh"},
            {"id": "curr_fuel_type", "label": "Existing System Efficiency (%)", "default": 80, "suffix": "%", "min": 50, "max": 98, "step": 1, "hint": "Old furnace AFUE (e.g. 80% standard, 65% old boiler)"},
            {"id": "curr_gas_price", "label": "Current Heating Fuel Price ($/Therm)", "default": 1.65, "prefix": "$", "min": 0.5, "max": 5.0, "step": 0.05, "hint": "Price per Therm of natural gas, propane or heating oil"},
            {"id": "heat_pump_hspf2", "label": "New Heat Pump HSPF2 Rating", "default": 9.5, "min": 6.5, "max": 14.0, "step": 0.1, "hint": "Heating Seasonal Performance Factor (DOE 2023 standard)"},
            {"id": "electric_rate", "label": "Electricity Rate ($/kWh)", "default": 0.16, "prefix": "$", "min": 0.05, "max": 0.50, "step": 0.01, "hint": "Local electrical utility price per kWh"}
        ],
        "metrics": [
            {"id": "annual_savings", "label": "Net Annual Heating Bill Savings", "default_display": "$524.00", "highlight": True},
            {"id": "heat_pump_cop", "label": "Effective Seasonal COP", "default_display": "2.78 (278% efficient)", "highlight": True},
            {"id": "old_heating_cost", "label": "Current Annual Heating Bill", "default_display": "$1,753.00"},
            {"id": "new_heating_cost", "label": "Heat Pump Annual Heating Bill", "default_display": "$1,229.00"}
        ],
        "proof_steps": [
            {"step_title": "Effective Thermal Energy Demand", "step_text": "Net delivered heat Q = Gross Therms × (AFUE% / 100) × 100,000 BTU. For 850 Therms at 80% AFUE: 68,000,000 BTU delivered."},
            {"step_title": "Coefficient of Performance (COP)", "step_text": "COP = HSPF2 / 3.41214. An HSPF2 of 9.5 equals a COP of 2.78, meaning the heat pump moves 2.78 units of heat for every 1 unit of electricity consumed."},
            {"step_title": "Heat Pump Electricity Requirement", "step_text": "kWh = Q / (COP × 3,412.14). 68,000,000 / (2.784 × 3,412.14) = 7,159 kWh/year."},
            {"step_title": "Economic Differential", "step_text": "Old Fuel Cost = (850 Therms × $1.65) = $1,402.50. Heat pump cost = 7,159 kWh × $0.16 = $1,145.44."}
        ],
        "faqs": [
            {"q": "How does a heat pump deliver over 100% efficiency?", "a": "Unlike resistive heaters or combustion furnaces that generate heat from energy, heat pumps use the refrigeration cycle to transfer ambient heat from outdoor air into the building."},
            {"q": "Do cold-climate heat pumps work below zero degrees?", "a": "Yes! Modern cold-climate inverter heat pumps with vapor-injection compressors maintain 100% rated heating capacity down to -5°F (-20°C) and operate down to -22°F."}
        ],
        "js_logic": """
          const therms = getNum('heating_load_therms');
          const afue = (getNum('curr_fuel_type') || 80) / 100;
          const gasPrice = getNum('curr_gas_price');
          const hspf2 = getNum('heat_pump_hspf2') || 9.5;
          const elecRate = getNum('electric_rate');

          const netBtu = therms * 100000 * afue;
          const oldBill = (therms * gasPrice) / afue;
          const cop = hspf2 / 3.41214;
          const newKwh = netBtu / (cop * 3412.14);
          const newBill = newKwh * elecRate;
          const savings = oldBill - newBill;

          setDisp('annual_savings', (savings >= 0 ? '$' : '-$') + Math.abs(Math.round(savings)).toLocaleString());
          setDisp('heat_pump_cop', cop.toFixed(2) + ' (' + Math.round(cop * 100) + '%)');
          setDisp('old_heating_cost', '$' + Math.round(oldBill).toLocaleString());
          setDisp('new_heating_cost', '$' + Math.round(newBill).toLocaleString());
        """
    },
    {
        "slug": "ev-charging-load",
        "category": "energy",
        "name": "EV Charging Load, Time & Electrical Panel Capacity Calculator",
        "description": "Calculate charging speed (miles per hour), charge duration, breaker amperage, and continuous electrical panel load for electric vehicles across Level 1, 2, and 3 chargers.",
        "hero_badge": "E-Mobility • Electrical Infrastructure",
        "formula_display": "Charging kW = (Volts × Amps × Power Factor) / 1000 | Charge Hours = Battery kWh Needed / Effective kW",
        "fields": [
            {"id": "battery_size_kwh", "label": "EV Battery Pack Usable Capacity (kWh)", "default": 77.4, "suffix": "kWh", "min": 20, "max": 200, "step": 1, "hint": "Usable battery pack size (e.g. Model Y = 75 kWh, Ioniq 5 = 77 kWh)"},
            {"id": "start_soc_pct", "label": "Starting State of Charge (SoC %)", "default": 20, "suffix": "%", "min": 0, "max": 95, "step": 5, "hint": "Current battery charge level"},
            {"id": "target_soc_pct", "label": "Target State of Charge (SoC %)", "default": 80, "suffix": "%", "min": 10, "max": 100, "step": 5, "hint": "Recommended daily charging ceiling (usually 80%)"},
            {"id": "charger_amps", "label": "Charging Current Rating (Amperes)", "default": 48, "suffix": "Amps", "min": 12, "max": 80, "step": 4, "hint": "Continuous current (NEC 80% rule requires 60A breaker for 48A load)"},
            {"id": "charger_volts", "label": "Supply Voltage (Volts AC)", "default": 240, "suffix": "V", "min": 110, "max": 480, "step": 10, "hint": "120V for Level 1, 240V for Level 2 residential"},
            {"id": "ev_efficiency", "label": "Vehicle Driving Efficiency (mi/kWh)", "default": 3.4, "suffix": "mi/kWh", "min": 1.5, "max": 5.0, "step": 0.1, "hint": "Average miles per kilowatt-hour"}
        ],
        "metrics": [
            {"id": "charge_time_hrs", "label": "Time to Target Charge", "default_display": "4.3 hours", "highlight": True},
            {"id": "charge_speed_mph", "label": "Charge Speed Added", "default_display": "35.2 mi/hr", "highlight": True},
            {"id": "charging_power_kw", "label": "Continuous Charging Power", "default_display": "11.52 kW"},
            {"id": "breaker_req_amps", "label": "Minimum Circuit Breaker Required", "default_display": "60 Amp Breaker"}
        ],
        "proof_steps": [
            {"step_title": "Continuous Charging Power Delivery", "step_text": "P_charge = (Volts × Amps) / 1000. At 240V and 48A: (240 × 48) / 1000 = 11.52 kW."},
            {"step_title": "NEC 80% Continuous Load Rule", "step_text": "NEC Section 625 specifies that EVSE is a continuous load (runs > 3 hours). Minimum Breaker = Charging Amps / 0.80. 48A / 0.80 = 60A breaker."},
            {"step_title": "Charge Energy Replenishment", "step_text": "Energy Needed ΔE = Battery Capacity × (Target% - Start%) / 100. 77.4 kWh × (80% - 20%) = 46.44 kWh."},
            {"step_title": "Charging Duration & Recovery", "step_text": "Duration = (ΔE / (P_charge × 0.90 efficiency)) = 46.44 / 10.37 = 4.48 hours."}
        ],
        "faqs": [
            {"q": "Why does NEC require a 60A breaker for a 48A EV charger?", "a": "National Electrical Code (NEC Article 625) mandates that continuous electrical loads cannot exceed 80% of the overcurrent protective device rating. 48A / 0.80 = 60A."},
            {"q": "Can my 100A or 200A home electrical panel support Level 2 EV charging?", "a": "A 200A panel typically accommodates a 40A or 48A charger easily. A 100A panel may require a dynamic load management device (EVEMS) to avoid expensive service upgrades."}
        ],
        "js_logic": """
          const bat = getNum('battery_size_kwh');
          const sSoc = getNum('start_soc_pct');
          const tSoc = getNum('target_soc_pct');
          const amps = getNum('charger_amps');
          const volts = getNum('charger_volts') || 240;
          const eff = getNum('ev_efficiency') || 3.4;

          const kw = (volts * amps) / 1000;
          const breaker = Math.ceil(amps / 0.8 / 5) * 5;
          const kwhNeeded = bat * Math.max(0, tSoc - sSoc) / 100;
          const netKw = kw * 0.92;
          const hrs = netKw > 0 ? (kwhNeeded / netKw) : 0;
          const mph = netKw * eff;

          setDisp('charge_time_hrs', hrs.toFixed(1) + ' hours');
          setDisp('charge_speed_mph', mph.toFixed(1) + ' mi/hr');
          setDisp('charging_power_kw', kw.toFixed(2) + ' kW');
          setDisp('breaker_req_amps', breaker + ' Amp Breaker');
        """
    },
    {
        "slug": "solar-inverter-clipping",
        "category": "energy",
        "name": "Solar Inverter Sizing & DC-to-AC Overload Clipping Ratio",
        "description": "Calculate DC-to-AC inverter loading ratio (ILR), annual energy clipping loss percentage, and inverter size optimization for photovoltaic systems.",
        "hero_badge": "Power Electronics • Inverter Optimization",
        "formula_display": "DC-to-AC Ratio (ILR) = Total DC Module Nameplate kW / Inverter Max Rated AC Output kW",
        "fields": [
            {"id": "dc_array_kw", "label": "Total DC Solar Array (kW DC)", "default": 10.25, "suffix": "kW DC", "min": 2.0, "max": 100.0, "step": 0.25, "hint": "Sum of nameplate wattage of all installed modules"},
            {"id": "ac_inverter_kw", "label": "Inverter AC Nameplate Output (kW AC)", "default": 7.6, "suffix": "kW AC", "min": 2.0, "max": 80.0, "step": 0.2, "hint": "Continuous AC power limit (e.g. 7.6 kW standard)"},
            {"id": "inverter_eff_pct", "label": "Inverter CEC Weighted Efficiency (%)", "default": 97.5, "suffix": "%", "min": 92.0, "max": 99.5, "step": 0.1, "hint": "California Energy Commission efficiency rating"}
        ],
        "metrics": [
            {"id": "ilr_ratio", "label": "DC-to-AC Loading Ratio (ILR)", "default_display": "1.35", "highlight": True},
            {"id": "clipping_status", "label": "Clipping Design Evaluation", "default_display": "Optimal Commercial Ratio", "highlight": True},
            {"id": "estimated_clip_loss", "label": "Estimated Annual Clipping Loss", "default_display": "1.2% (< 140 kWh/yr)"},
            {"id": "max_ac_current", "label": "Max Continuous AC Current (240V)", "default_display": "31.7 Amps"}
        ],
        "proof_steps": [
            {"step_title": "Inverter Loading Ratio (ILR)", "step_text": "ILR = P_dc / P_ac. For a 10.25 kW DC array with a 7.6 kW AC inverter: 10.25 / 7.6 = 1.348 (1.35)."},
            {"step_title": "Economics of Clipping", "step_text": "Panels rarely operate at STC (Standard Test Conditions) due to heat derating (~ -0.35%/°C), dust, and sun angle. Oversizing DC capacity by 20% to 35% keeps the inverter operating at its peak efficiency curve during morning and afternoon hours."},
            {"step_title": "Clipping Losses vs Capital Savings", "step_text": "A 1.30 to 1.35 ILR results in only 0.5% to 2.0% annual energy clipping loss while saving $1,000+ compared to buying a larger inverter."},
            {"step_title": "Max Continuous AC Backfeed", "step_text": "I_ac = (P_ac × 1000) / 240V. 7,600W / 240V = 31.67A, requiring a 40A backfeed circuit breaker (31.67 / 0.8 = 39.6A)."}
        ],
        "faqs": [
            {"q": "Why do solar installers oversize the DC array relative to the inverter?", "a": "Oversizing the DC array (1.20 to 1.35 ILR) ensures the inverter operates closer to peak capacity for more hours each day, maximizing total kWh produced despite slight midday clipping."},
            {"q": "Does clipping damage the inverter?", "a": "No. Inverters use maximum power point tracking (MPPT) to shift their operating voltage along the IV curve, drawing only the exact current they are rated to process safely."}
        ],
        "js_logic": """
          const dc = getNum('dc_array_kw');
          const ac = getNum('ac_inverter_kw');
          const eff = (getNum('inverter_eff_pct') || 97.5) / 100;

          const ilr = ac > 0 ? (dc / ac) : 1;
          const maxAmps = (ac * 1000) / 240;

          let status = '';
          let lossPct = 0;
          if (ilr < 1.15) {
            status = 'Under-utilized Inverter';
            lossPct = 0.1;
          } else if (ilr <= 1.35) {
            status = 'Optimal Engineering Ratio';
            lossPct = (ilr - 1.15) * 6;
          } else {
            status = 'Aggressive Clipping (> 3% Loss)';
            lossPct = 2.0 + (ilr - 1.35) * 12;
          }

          setDisp('ilr_ratio', ilr.toFixed(2));
          setDisp('clipping_status', status);
          setDisp('estimated_clip_loss', lossPct.toFixed(1) + '%');
          setDisp('max_ac_current', maxAmps.toFixed(1) + ' Amps');
        """
    },
    {
        "slug": "chiller-tonnage-cooling",
        "category": "energy",
        "name": "Commercial HVAC Chiller Tonnage & Cooling Load Calculator",
        "description": "Calculate chilled water cooling capacity in refrigeration tons (TR), kW thermal, and pump flow rate in GPM for commercial HVAC systems.",
        "hero_badge": "Commercial HVAC • Hydronic Cooling",
        "formula_display": "Tons of Refrigeration (TR) = (GPM × ΔT in °F) / 24 | 1 TR = 12,000 BTU/hr = 3.517 kW",
        "fields": [
            {"id": "water_flow_gpm", "label": "Chilled Water Flow Rate (GPM)", "default": 240, "suffix": "GPM", "min": 20, "max": 5000, "step": 10, "hint": "Gallons per minute circulated through evaporator"},
            {"id": "entering_water_temp", "label": "Entering Water Temp (EWT °F)", "default": 54.0, "suffix": "°F", "min": 45, "max": 85, "step": 0.5, "hint": "Warm return water temperature entering chiller"},
            {"id": "leaving_water_temp", "label": "Leaving Water Temp (LWT °F)", "default": 44.0, "suffix": "°F", "min": 38, "max": 60, "step": 0.5, "hint": "Cold chilled supply water temperature"},
            {"id": "chiller_kw_per_ton", "label": "Chiller Specific Efficiency (kW/Ton)", "default": 0.58, "suffix": "kW/Ton", "min": 0.40, "max": 1.20, "step": 0.02, "hint": "Full-load electrical power draw per ton"}
        ],
        "metrics": [
            {"id": "cooling_tonnage", "label": "Chiller Cooling Capacity", "default_display": "100.0 Tons (TR)", "highlight": True},
            {"id": "cooling_btuh", "label": "Total Cooling Rate (BTU/hr)", "default_display": "1,200,000 BTU/hr", "highlight": True},
            {"id": "thermal_kw", "label": "Thermal Cooling Power", "default_display": "351.7 kW th"},
            {"id": "chiller_power_kw", "label": "Electrical Input Power Demand", "default_display": "58.0 kW el"}
        ],
        "proof_steps": [
            {"step_title": "Water Temperature Differential", "step_text": "ΔT = Entering Water Temp - Leaving Water Temp. For 54°F EWT and 44°F LWT: ΔT = 10.0°F."},
            {"step_title": "Hydronic Heat Transfer Rate", "step_text": "q = 500 × GPM × ΔT. Constant 500 = 8.33 lb/gal × 60 min/hr × 1.0 BTU/(lb·°F). For 240 GPM: 500 × 240 × 10 = 1,200,000 BTU/hr."},
            {"step_title": "Refrigeration Tonnage Derivation", "step_text": "1 Ton of Refrigeration (TR) = 12,000 BTU/hr (cooling effect of melting 1 short ton of ice in 24 hours). TR = 1,200,000 / 12,000 = 100.0 TR."},
            {"step_title": "Electrical Power Consumption", "step_text": "P_el = TR × (kW/Ton). 100 TR × 0.58 kW/Ton = 58.0 kW electric power demand."}
        ],
        "faqs": [
            {"q": "What is the standard rule of thumb for chilled water flow rate per ton?", "a": "At a standard 10°F temperature differential (ΔT), chilled water systems require exactly 2.4 GPM per ton of cooling (24 / 10 = 2.4). At a 12°F ΔT, flow rate drops to 2.0 GPM/ton."},
            {"q": "What is considered a good chiller efficiency (kW/ton)?", "a": "High-efficiency water-cooled centrifugal and magnetic-bearing chillers achieve 0.48 to 0.58 kW/ton at full load, and down to 0.30 kW/ton at part-load IPLV."}
        ],
        "js_logic": """
          const gpm = getNum('water_flow_gpm');
          const ewt = getNum('entering_water_temp');
          const lwt = getNum('leaving_water_temp');
          const kwPerTon = getNum('chiller_kw_per_ton') || 0.58;

          const deltaT = Math.max(0, ewt - lwt);
          const btuh = 500 * gpm * deltaT;
          const tons = btuh / 12000;
          const kwTh = tons * 3.51685;
          const kwEl = tons * kwPerTon;

          setDisp('cooling_tonnage', tons.toFixed(1) + ' Tons (TR)');
          setDisp('cooling_btuh', Math.round(btuh).toLocaleString() + ' BTU/hr');
          setDisp('thermal_kw', kwTh.toFixed(1) + ' kW th');
          setDisp('chiller_power_kw', kwEl.toFixed(1) + ' kW el');
        """
    },
    {
        "slug": "power-factor-correction",
        "category": "energy",
        "name": "3-Phase Power Factor Correction & Capacitor Sizing Calculator",
        "description": "Calculate required capacitor kVAR bank size to correct lagging electrical power factor from inductive motors, eliminating utility penalty surcharges.",
        "hero_badge": "Industrial Power • Reactive Compensation",
        "formula_display": "Required kVAR = P × (tan(θ₁) - tan(θ₂)) | θ = arccos(PF)",
        "fields": [
            {"id": "active_power_kw", "label": "Active Real Power (kW)", "default": 250, "suffix": "kW", "min": 10, "max": 10000, "step": 10, "hint": "Actual working power consumed by facility loads"},
            {"id": "current_pf", "label": "Current Measured Power Factor", "default": 0.76, "min": 0.50, "max": 0.95, "step": 0.01, "hint": "Uncorrected lagging power factor (cos θ₁)"},
            {"id": "target_pf", "label": "Target Corrected Power Factor", "default": 0.95, "min": 0.85, "max": 1.00, "step": 0.01, "hint": "Desired power factor to avoid utility penalties (typically 0.95)"},
            {"id": "voltage_ll", "label": "Line-to-Line Voltage (Volts AC)", "default": 480, "suffix": "V", "min": 208, "max": 4160, "step": 10, "hint": "3-phase service voltage"}
        ],
        "metrics": [
            {"id": "required_kvar", "label": "Capacitor Bank Required", "default_display": "131.5 kVAR", "highlight": True},
            {"id": "current_reduction", "label": "Line Current Reduction", "default_display": "79.2 Amps", "highlight": True},
            {"id": "original_kva", "label": "Original Apparent Power", "default_display": "328.9 kVA"},
            {"id": "corrected_kva", "label": "Corrected Apparent Power", "default_display": "263.2 kVA"}
        ],
        "proof_steps": [
            {"step_title": "Trigonometric Phase Angles", "step_text": "θ₁ = arccos(0.76) = 40.54°. tan(40.54°) = 0.855. θ₂ = arccos(0.95) = 18.19°. tan(18.19°) = 0.329."},
            {"step_title": "Capacitor Reactive Power Demand", "step_text": "Q_cap = P_kw × (tan(θ₁) - tan(θ₂)). For 250 kW: 250 × (0.8553 - 0.3287) = 131.65 kVAR."},
            {"step_title": "Apparent Power Reduction", "step_text": "S₁ = 250 / 0.76 = 328.9 kVA. S₂ = 250 / 0.95 = 263.2 kVA. Freed electrical transformer capacity = 65.7 kVA."},
            {"step_title": "3-Phase Amperage Relief", "step_text": "I = S / (√3 × V_ll). Original Current = 328,900 / (1.732 × 480) = 395.6A. Corrected Current = 263,200 / (1.732 × 480) = 316.5A (79.1A reduction)."}
        ],
        "faqs": [
            {"q": "Why do commercial utilities penalize low power factor?", "a": "Low power factor forces utilities to supply larger apparent current (kVA) to deliver the same real power (kW), causing higher transmission I²R heat losses and requiring larger transformers and cabling."},
            {"q": "Should I correct power factor past 0.98 or 1.0?", "a": "Correcting beyond 0.98 is rarely cost-effective and risks leading power factor (capacitive over-correction), which causes hazardous harmonic resonance and voltage rise during light load periods."}
        ],
        "js_logic": """
          const kw = getNum('active_power_kw');
          const pf1 = Math.min(0.99, Math.max(0.4, getNum('current_pf') || 0.76));
          const pf2 = Math.min(1.0, Math.max(pf1, getNum('target_pf') || 0.95));
          const v = getNum('voltage_ll') || 480;

          const th1 = Math.acos(pf1);
          const th2 = Math.acos(pf2);
          const kvar = kw * (Math.tan(th1) - Math.tan(th2));

          const kva1 = kw / pf1;
          const kva2 = kw / pf2;
          const i1 = (kva1 * 1000) / (Math.sqrt(3) * v);
          const i2 = (kva2 * 1000) / (Math.sqrt(3) * v);
          const deltaI = i1 - i2;

          setDisp('required_kvar', kvar.toFixed(1) + ' kVAR');
          setDisp('current_reduction', deltaI.toFixed(1) + ' Amps');
          setDisp('original_kva', kva1.toFixed(1) + ' kVA');
          setDisp('corrected_kva', kva2.toFixed(1) + ' kVA');
        """
    },
    {
        "slug": "net-metering-credits",
        "category": "energy",
        "name": "Solar Net Metering & Utility Feed-in Tariff Calculator",
        "description": "Calculate annual financial compensation under NEM 1.0, NEM 2.0, NEM 3.0 (California solar billing), and avoided cost wholesale credit tariffs.",
        "hero_badge": "Grid Economics • Solar Compensation",
        "formula_display": "Net Value = (Self-Consumed kWh × Retail Rate) + (Exported kWh × Feed-in Tariff)",
        "fields": [
            {"id": "annual_gen_kwh", "label": "Annual Solar Production (kWh)", "default": 11000, "suffix": "kWh", "min": 2000, "max": 100000, "step": 500, "hint": "Estimated annual electricity generated"},
            {"id": "self_consume_pct", "label": "On-Site Self-Consumption (%)", "default": 40, "suffix": "%", "min": 10, "max": 95, "step": 5, "hint": "% of solar electricity consumed inside the building instantly"},
            {"id": "retail_import_rate", "label": "Retail Grid Import Rate ($/kWh)", "default": 0.32, "prefix": "$", "min": 0.08, "max": 0.75, "step": 0.01, "hint": "Cost paid when buying electricity from grid"},
            {"id": "export_credit_rate", "label": "Grid Export Credit Rate ($/kWh)", "default": 0.07, "prefix": "$", "min": 0.02, "max": 0.60, "step": 0.01, "hint": "NEM 3.0 export credit or wholesale avoided cost"}
        ],
        "metrics": [
            {"id": "total_annual_value", "label": "Total Annual Solar Value", "default_display": "$1,870.00", "highlight": True},
            {"id": "self_consume_value", "label": "Avoided Retail Import Savings", "default_display": "$1,408.00", "highlight": True},
            {"id": "export_credits", "label": "Grid Export Credit Earnings", "default_display": "$462.00"},
            {"id": "effective_rate_per_kwh", "label": "Blended Solar Value ($/kWh)", "default_display": "$0.17 / kWh"}
        ],
        "proof_steps": [
            {"step_title": "Energy Flow Allocation", "step_text": "Self-Consumed Energy = 11,000 kWh × 40% = 4,400 kWh. Exported Energy = 11,000 × 60% = 6,600 kWh."},
            {"step_title": "Direct Avoided Cost Valuation", "step_text": "Avoided Import Cost = 4,400 kWh × $0.32/kWh = $1,408.00."},
            {"step_title": "Export Tariff Credit Calculation", "step_text": "Export Value = 6,600 kWh × $0.07/kWh = $462.00."},
            {"step_title": "Aggregate System Revenue", "step_text": "Total Value = $1,408.00 + $462.00 = $1,870.00. Blended Value = $1,870 / 11,000 = $0.170/kWh."}
        ],
        "faqs": [
            {"q": "What is the difference between NEM 2.0 and NEM 3.0?", "a": "Under NEM 2.0, exported solar earned near 1:1 retail credits (~$0.30/kWh). Under California NEM 3.0 (Solar Billing), export rates dropped by ~75% to avoided cost (~$0.05 to $0.08/kWh), making home batteries essential to store daytime solar for night use."},
            {"q": "How can I increase self-consumption without a battery?", "a": "Program EV chargers, heat pump water heaters, dishwashers, and pool pumps to run automatically during midday solar peak hours (10 AM to 3 PM)."}
        ],
        "js_logic": """
          const gen = getNum('annual_gen_kwh');
          const selfPct = (getNum('self_consume_pct') || 40) / 100;
          const retail = getNum('retail_import_rate');
          const exportR = getNum('export_credit_rate');

          const selfKwh = gen * selfPct;
          const expKwh = gen * (1 - selfPct);
          const selfVal = selfKwh * retail;
          const expVal = expKwh * exportR;
          const totalVal = selfVal + expVal;
          const blended = gen > 0 ? (totalVal / gen) : 0;

          setDisp('total_annual_value', '$' + Math.round(totalVal).toLocaleString());
          setDisp('self_consume_value', '$' + Math.round(selfVal).toLocaleString());
          setDisp('export_credits', '$' + Math.round(expVal).toLocaleString());
          setDisp('effective_rate_per_kwh', '$' + blended.toFixed(3) + ' / kWh');
        """
    },
    {
        "slug": "solar-tilt-azimuth",
        "category": "energy",
        "name": "Solar Panel Tilt & Azimuth Irradiance Optimizer",
        "description": "Calculate optimal fixed tilt angle and azimuth orientation to maximize annual solar photovoltaic kilowatt-hour harvest based on geographic latitude.",
        "hero_badge": "Solar Geometry • Irradiance Optimization",
        "formula_display": "Optimal Annual Tilt ≈ Latitude × 0.87 | Optimal Azimuth = 180° (True South in Northern Hemisphere)",
        "fields": [
            {"id": "geo_latitude", "label": "Site Latitude (Degrees North)", "default": 35.5, "suffix": "°N", "min": 0, "max": 65, "step": 0.5, "hint": "Geographic latitude of installation location"},
            {"id": "optimization_goal", "label": "Optimization Goal (1=Annual, 2=Winter, 3=Summer)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1: Max Annual kWh, 2: Max Winter Peak, 3: Max Summer Peak"}
        ],
        "metrics": [
            {"id": "optimal_tilt_deg", "label": "Recommended Tilt Angle", "default_display": "30.9°", "highlight": True},
            {"id": "optimal_azimuth_deg", "label": "Recommended Azimuth Heading", "default_display": "180° (True South)", "highlight": True},
            {"id": "seasonal_strategy", "label": "Orientation Rationale", "default_display": "Maximizes 12-Month Net Harvest", "highlight": True},
            {"id": "estimated_solar_yield_pct", "label": "Relative Irradiance Capture", "default_display": "99.4% of Theoretical Ideal"}
        ],
        "proof_steps": [
            {"step_title": "Astronomical Zenith Alignment", "step_text": "The solar declination varies between +23.45° (summer solstice) and -23.45° (winter solstice)."},
            {"step_title": "Annual Maximum Harvest Derivation", "step_text": "Empirical PV models show optimal fixed tilt = (Latitude × 0.87) for latitudes below 40°, and (Latitude × 0.76 + 3.1°) for higher latitudes."},
            {"step_title": "Seasonal Optimization Biasing", "step_text": "Winter optimization = Latitude + 15° (steep angle captures low winter sun and sheds snow). Summer optimization = Latitude - 15°."},
            {"step_title": "Azimuth Compass Correction", "step_text": "Panels should face True Solar South (180° azimuth) in the Northern Hemisphere, correcting for local magnetic declination."}
        ],
        "faqs": [
            {"q": "Is roof pitch more important than roof orientation?", "a": "Orientation (azimuth) typically has a larger impact. A south-facing roof tilted between 15° and 40° captures 95% to 100% of optimal energy. West-facing roofs lose ~15% annual production but produce valuable power during late afternoon peak utility demand hours."},
            {"q": "Is it worth installing adjustable seasonal tilt racks?", "a": "For residential grid-tied systems, seasonal adjustments only gain 3% to 5% more annual energy, which rarely justifies the mechanical maintenance, labor, and safety risks of climbing on the roof."}
        ],
        "js_logic": """
          const lat = getNum('geo_latitude');
          const goal = Math.round(getNum('optimization_goal')) || 1;

          let tilt = 30;
          let strat = 'Annual Harvest';
          if (goal === 1) {
            tilt = lat * 0.87;
            strat = 'Maximizes 12-Month Net Harvest';
          } else if (goal === 2) {
            tilt = Math.min(65, lat + 15);
            strat = 'Maximizes Winter Off-Grid Production';
          } else {
            tilt = Math.max(10, lat - 15);
            strat = 'Maximizes Summer Cooling Surplus';
          }

          setDisp('optimal_tilt_deg', tilt.toFixed(1) + '°');
          setDisp('optimal_azimuth_deg', '180° (True South)');
          setDisp('seasonal_strategy', strat);
          setDisp('estimated_solar_yield_pct', '99.5% of Theoretical Max');
        """
    },
    {
        "slug": "wind-turbine-power",
        "category": "energy",
        "name": "Wind Turbine Power Curve & Betz Limit Kinetic Yield Calculator",
        "description": "Calculate theoretical and electrical power output in watts and kWh from a wind turbine based on wind speed, rotor diameter, and aerodynamic power coefficient.",
        "hero_badge": "Wind Energy • Fluid Dynamics",
        "formula_display": "Power = ½ · ρ · A · v³ · Cp · η | Max Betz Limit Cp = 16/27 ≈ 59.3%",
        "fields": [
            {"id": "wind_speed_mph", "label": "Average Wind Velocity (mph)", "default": 13.5, "suffix": "mph", "min": 3, "max": 60, "step": 0.5, "hint": "Measured wind velocity at hub height"},
            {"id": "rotor_diameter_m", "label": "Rotor Blade Diameter (Meters)", "default": 3.2, "suffix": "m", "min": 1.0, "max": 150.0, "step": 0.2, "hint": "Tip-to-tip rotor sweep diameter"},
            {"id": "power_coeff_cp", "label": "Aerodynamic Power Coefficient (Cp)", "default": 0.38, "min": 0.15, "max": 0.55, "step": 0.01, "hint": "Typical small wind turbine Cp = 0.30 - 0.42 (Betz limit = 0.593)"},
            {"id": "generator_eff_pct", "label": "Generator & Drivetrain Efficiency (%)", "default": 88, "suffix": "%", "min": 70, "max": 96, "step": 1, "hint": "Mechanical-to-electrical conversion efficiency"}
        ],
        "metrics": [
            {"id": "power_output_watts", "label": "Continuous Electrical Power", "default_display": "432.8 Watts", "highlight": True},
            {"id": "daily_energy_kwh", "label": "Daily Energy Production", "default_display": "10.4 kWh/day", "highlight": True},
            {"id": "swept_area_sqm", "label": "Rotor Swept Area", "default_display": "8.04 m²"},
            {"id": "kinetic_wind_power", "label": "Raw Kinetic Wind Power", "default_display": "1,294.0 Watts"}
        ],
        "proof_steps": [
            {"step_title": "Velocity Conversion to Metric", "step_text": "v = 13.5 mph × 0.44704 = 6.035 m/s."},
            {"step_title": "Rotor Swept Area", "step_text": "A = π · (d / 2)² = π · 1.6² = 8.042 m²."},
            {"step_title": "Kinetic Energy Flow Rate", "step_text": "P_wind = ½ · ρ · A · v³, where air density ρ = 1.225 kg/m³. At 6.035 m/s: ½ × 1.225 × 8.042 × 6.035³ = 1,083.5 Watts."},
            {"step_title": "Electrical Power Harvest", "step_text": "P_elec = P_wind × Cp × η_gen = 1,083.5 × 0.38 × 0.88 = 362.3 Watts. Daily yield = 362.3W × 24h = 8.7 kWh."}
        ],
        "faqs": [
            {"q": "What is the Betz Limit?", "a": "Albert Betz proved in 1919 that no wind turbine can capture more than 16/27 (59.3%) of the kinetic energy in wind. If a rotor attempted to capture 100%, the air behind it would stop completely, preventing new incoming wind from flowing through the blades."},
            {"q": "Why does power increase with the cube of wind speed (v³)?", "a": "Because kinetic energy is proportional to v² (½mv²), and the mass flow rate of air passing through the rotor each second is proportional to v (m = ρAv). Combining them gives power proportional to v³."}
        ],
        "js_logic": """
          const mph = getNum('wind_speed_mph');
          const d = getNum('rotor_diameter_m');
          const cp = Math.min(0.59, getNum('power_coeff_cp') || 0.38);
          const eff = (getNum('generator_eff_pct') || 88) / 100;

          const v = mph * 0.44704;
          const a = Math.PI * Math.pow(d / 2, 2);
          const rho = 1.225;
          const rawWindWatts = 0.5 * rho * a * Math.pow(v, 3);
          const elecWatts = rawWindWatts * cp * eff;
          const dailyKwh = (elecWatts * 24) / 1000;

          setDisp('power_output_watts', elecWatts >= 1000 ? (elecWatts / 1000).toFixed(2) + ' kW' : elecWatts.toFixed(1) + ' Watts');
          setDisp('daily_energy_kwh', dailyKwh.toFixed(1) + ' kWh/day');
          setDisp('swept_area_sqm', a.toFixed(2) + ' m²');
          setDisp('kinetic_wind_power', rawWindWatts >= 1000 ? (rawWindWatts / 1000).toFixed(2) + ' kW' : rawWindWatts.toFixed(1) + ' Watts');
        """
    },
    {
        "slug": "transformer-kva-rating",
        "category": "energy",
        "name": "3-Phase & Single-Phase Transformer kVA Rating Calculator",
        "description": "Calculate full-load secondary current (FLA), primary current, and recommended standard transformer kVA size for commercial and industrial electrical distribution.",
        "hero_badge": "Electrical Distribution • Transformer Sizing",
        "formula_display": "3-Phase kVA = (√3 × Volts_LL × Amps) / 1000 | FLA = (kVA × 1000) / (√3 × Volts_LL)",
        "fields": [
            {"id": "load_amps", "label": "Full Load Current (Amperes)", "default": 180, "suffix": "Amps", "min": 10, "max": 4000, "step": 5, "hint": "Calculated total electrical load in amperes"},
            {"id": "secondary_voltage", "label": "Secondary Voltage (Volts L-L)", "default": 208, "suffix": "V", "min": 120, "max": 600, "step": 10, "hint": "Common voltages: 208V, 240V, 480V"},
            {"id": "primary_voltage", "label": "Primary Utility Voltage (Volts L-L)", "default": 480, "suffix": "V", "min": 240, "max": 13800, "step": 10, "hint": "Supply feeding the transformer"},
            {"id": "is_three_phase", "label": "Phase Configuration (3 = 3-Phase, 1 = 1-Phase)", "default": 3, "min": 1, "max": 3, "step": 2, "hint": "3 for three-phase, 1 for single-phase"},
            {"id": "growth_margin_pct", "label": "Future Spare Capacity Margin (%)", "default": 25, "suffix": "%", "min": 0, "max": 50, "step": 5, "hint": "Recommended 20% to 25% NEC spare capacity"}
        ],
        "metrics": [
            {"id": "recommended_kva", "label": "Standard Transformer Rating", "default_display": "75 kVA", "highlight": True},
            {"id": "calculated_kva", "label": "Exact Design Load kVA", "default_display": "81.0 kVA", "highlight": True},
            {"id": "secondary_fla", "label": "Full Load Secondary Amps (FLA)", "default_display": "208.2 Amps"},
            {"id": "primary_fla", "label": "Full Load Primary Amps (FLA)", "default_display": "90.2 Amps"}
        ],
        "proof_steps": [
            {"step_title": "Base Apparent Power Calculation", "step_text": "For 3-phase: S = √3 × V × I / 1000. S_base = 1.732 × 208V × 180A / 1000 = 64.84 kVA."},
            {"step_title": "Future Capacity Expansion", "step_text": "S_design = S_base × (1 + Margin% / 100). With 25% spare margin: 64.84 × 1.25 = 81.05 kVA."},
            {"step_title": "Standard Commercial NEMA kVA Selection", "step_text": "Standard 3-phase dry-type transformer ratings are 15, 30, 45, 75, 112.5, 150, 225, 300, 500 kVA. Sizing above 81.05 kVA yields a 112.5 kVA unit."},
            {"step_title": "Primary Line Current Rating", "step_text": "I_primary = (kVA × 1000) / (√3 × V_primary). For 112.5 kVA at 480V: 112,500 / (1.732 × 480) = 135.3A."}
        ],
        "faqs": [
            {"q": "What are the standard 3-phase transformer kVA sizes?", "a": "NEMA standard dry-type distribution transformer ratings are: 15, 30, 45, 75, 112.5, 150, 225, 300, 500, 750, and 1000 kVA."},
            {"q": "Can a transformer be loaded to 100% continuously?", "a": "Yes, dry-type transformers are rated for 100% nameplate load at rated ambient temperature (typically 40°C), but operating at 80% load reduces operating core losses and extends insulation lifespan."}
        ],
        "js_logic": """
          const amps = getNum('load_amps');
          const vSec = getNum('secondary_voltage') || 208;
          const vPri = getNum('primary_voltage') || 480;
          const phase = Math.round(getNum('is_three_phase')) === 1 ? 1 : 3;
          const margin = (getNum('growth_margin_pct') || 25) / 100;

          const factor = phase === 3 ? Math.sqrt(3) : 1.0;
          const baseKva = (factor * vSec * amps) / 1000;
          const designKva = baseKva * (1 + margin);

          const standardKva = [15, 30, 45, 75, 112.5, 150, 225, 300, 500, 750, 1000, 1500, 2000];
          let selectedKva = standardKva[standardKva.length - 1];
          for (let i = 0; i < standardKva.length; i++) {
            if (standardKva[i] >= designKva) {
              selectedKva = standardKva[i];
              break;
            }
          }

          const secFla = (selectedKva * 1000) / (factor * vSec);
          const priFla = (selectedKva * 1000) / (factor * vPri);

          setDisp('recommended_kva', selectedKva + ' kVA');
          setDisp('calculated_kva', designKva.toFixed(1) + ' kVA');
          setDisp('secondary_fla', secFla.toFixed(1) + ' Amps');
          setDisp('primary_fla', priFla.toFixed(1) + ' Amps');
        """
    },
    {
        "slug": "wire-gauge-voltage-drop",
        "category": "energy",
        "name": "Electrical Wire Gauge & Voltage Drop Calculator (NEC)",
        "description": "Calculate conductor voltage drop percentage, terminal voltage, and minimum copper/aluminum AWG wire size compliant with NEC 3% branch circuit limits.",
        "hero_badge": "NEC Electrical Code • Conductor Sizing",
        "formula_display": "Voltage Drop = (2 × K × I × L) / Circular Mils (Single Phase) | Max NEC Drop ≤ 3.0%",
        "fields": [
            {"id": "circuit_amps", "label": "Design Load Current (Amperes)", "default": 40, "suffix": "Amps", "min": 5, "max": 500, "step": 5, "hint": "Continuous or non-continuous circuit amps"},
            {"id": "one_way_distance_ft", "label": "One-Way Distance to Load (Feet)", "default": 125, "suffix": "ft", "min": 10, "max": 1000, "step": 5, "hint": "Conduit route length from panel to equipment"},
            {"id": "system_volts", "label": "Nominal Voltage (Volts)", "default": 240, "suffix": "V", "min": 120, "max": 480, "step": 120, "hint": "120V, 208V, 240V, 277V, 480V"},
            {"id": "conductor_material", "label": "Conductor Material (1 = Copper, 2 = Aluminum)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1 for Copper (K=12.9), 2 for Aluminum (K=21.2)"}
        ],
        "metrics": [
            {"id": "voltage_drop_pct", "label": "Voltage Drop Percentage", "default_display": "2.44%", "highlight": True},
            {"id": "voltage_drop_volts", "label": "Voltage Dropped Across Line", "default_display": "5.86 Volts", "highlight": True},
            {"id": "voltage_at_load", "label": "Delivered Voltage at Load", "default_display": "234.1 Volts"},
            {"id": "recommended_awg", "label": "Recommended Minimum Wire Gauge", "default_display": "#6 AWG Copper"}
        ],
        "proof_steps": [
            {"step_title": "Ohmic Constant Specification", "step_text": "Copper resistivity constant K = 12.9 ohms-cmil/ft at 75°C. Aluminum K = 21.2 ohms-cmil/ft."},
            {"step_title": "NEC Maximum Permissible Drop", "step_text": "NEC Informational Note 210.19(A) recommends max 3.0% voltage drop on branch circuits (7.20V on a 240V circuit)."},
            {"step_title": "Required Circular Mils Derivation", "step_text": "Circular Mils = (2 × K × I × L) / V_drop_allowed. For 40A over 125 ft at 3% (7.2V): (2 × 12.9 × 40 × 125) / 7.2 = 17,916 cmil."},
            {"step_title": "AWG Standard Selection", "step_text": "#8 AWG = 16,510 cmil (too small, yields 3.25% drop). #6 AWG = 26,240 cmil (compliant, yields 2.05% drop)."}
        ],
        "faqs": [
            {"q": "What is the maximum allowed voltage drop under the National Electrical Code?", "a": "The NEC recommends a maximum 3% voltage drop on branch circuits, and a total combined drop of 5% including both feeder and branch conductors to ensure proper motor, heater, and electronics operation."},
            {"q": "When does voltage drop require upsizing wire gauge?", "a": "Generally, any circuit run exceeding 100 feet in length requires upsizing by one or two AWG sizes above standard 75°C ampacity tables to keep voltage drop below 3%."}
        ],
        "js_logic": """
          const amps = getNum('circuit_amps');
          const dist = getNum('one_way_distance_ft');
          const volts = getNum('system_volts') || 240;
          const mat = Math.round(getNum('conductor_material')) === 2 ? 'Al' : 'Cu';
          const k = mat === 'Al' ? 21.2 : 12.9;

          const maxDropV = volts * 0.03;
          const reqCmil = (2 * k * amps * dist) / maxDropV;

          const gauges = [
            { name: '#14 AWG', cmil: 4110 },
            { name: '#12 AWG', cmil: 6530 },
            { name: '#10 AWG', cmil: 10380 },
            { name: '#8 AWG', cmil: 16510 },
            { name: '#6 AWG', cmil: 26240 },
            { name: '#4 AWG', cmil: 41740 },
            { name: '#2 AWG', cmil: 66360 },
            { name: '#1/0 AWG', cmil: 105600 },
            { name: '#2/0 AWG', cmil: 133100 },
            { name: '#4/0 AWG', cmil: 211600 }
          ];

          let chosen = gauges[gauges.length - 1];
          for (let i = 0; i < gauges.length; i++) {
            if (gauges[i].cmil >= reqCmil) {
              chosen = gauges[i];
              break;
            }
          }

          const actualVDrop = (2 * k * amps * dist) / chosen.cmil;
          const actualPct = (actualVDrop / volts) * 100;
          const loadV = volts - actualVDrop;

          setDisp('voltage_drop_pct', actualPct.toFixed(2) + '%');
          setDisp('voltage_drop_volts', actualVDrop.toFixed(2) + ' Volts');
          setDisp('voltage_at_load', loadV.toFixed(1) + ' Volts');
          setDisp('recommended_awg', chosen.name + ' (' + mat + ')');
        """
    },
    {
        "slug": "geothermal-ground-loop",
        "category": "energy",
        "name": "Geothermal Heat Pump Ground Loop Borehole Length Calculator",
        "description": "Calculate required vertical borehole depth or horizontal trench loop footage for closed-loop ground-source geothermal heat pump systems.",
        "hero_badge": "Geothermal Energy • Borehole Engineering",
        "formula_display": "Total Vertical Borehole Feet = Heat Pump Tonnage × Borehole Ft/Ton (typically 150 - 200 ft/ton)",
        "fields": [
            {"id": "system_tons", "label": "Heat Pump Capacity (Tons)", "default": 4.0, "suffix": "Tons", "min": 1.5, "max": 50.0, "step": 0.5, "hint": "Building design thermal cooling/heating tonnage"},
            {"id": "soil_thermal_cond", "label": "Ground Thermal Conductivity (BTU/hr·ft·°F)", "default": 1.4, "min": 0.6, "max": 2.5, "step": 0.1, "hint": "Dry clay ~0.8, damp loam ~1.3, wet granite/limestone ~1.8"},
            {"id": "loop_configuration", "label": "Loop Geometry (1 = Vertical Borehole, 2 = Horizontal Trench)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "1 for vertical drilling, 2 for horizontal excavation"}
        ],
        "metrics": [
            {"id": "total_loop_footage", "label": "Total Required Loop Length", "default_display": "720.0 Linear Feet", "highlight": True},
            {"id": "number_of_bores", "label": "Recommended Boreholes / Trenches", "default_display": "4 Bores @ 180 ft each", "highlight": True},
            {"id": "loop_volume_gal", "label": "Circulation Fluid Volume", "default_display": "64.8 Gallons"},
            {"id": "pump_head_ft", "label": "Estimated Loop Pressure Head", "default_display": "28.5 ft H₂O"}
        ],
        "proof_steps": [
            {"step_title": "Soil Thermal Heat Rejection", "step_text": "Ground heat exchange relies on thermal conductivity k. In damp soil (k = 1.4 BTU/hr·ft·°F), vertical boreholes require ~180 linear feet per ton of capacity."},
            {"step_title": "Total Drilling Footage", "step_text": "Footage L = Tons × (Ft/Ton factor). For 4.0 Tons: 4.0 × 180 = 720 linear feet of vertical borehole."},
            {"step_title": "Borehole Multi-Hole Array", "step_text": "To keep drilling practical and prevent ground freezing/thermal saturation, four 180-foot boreholes spaced 15 to 20 feet apart are drilled with HDPE U-tubes."},
            {"step_title": "Hydraulic Fluid Volume", "step_text": "Standard 1-1/4\" SDR-11 HDPE pipe holds ~0.090 gallons per linear foot of bore loop. 720 ft × 0.090 gal/ft = 64.8 gallons of 20% ethanol/water antifreeze mixture."}
        ],
        "faqs": [
            {"q": "What is the typical vertical borehole drilling cost per foot?", "a": "Turnkey geothermal vertical drilling and loop installation typically ranges from $25 to $40 per foot, including drilling, HDPE loop insertion, and thermal bentonite grouting."},
            {"q": "Horizontal trench vs vertical boreholes: which is better?", "a": "Horizontal trenches require much more open land (nearly an acre for a 4-ton system) and are affected by surface weather fluctuations, whereas vertical boreholes (150-300 ft deep) tap stable 50°F to 55°F deep bedrock temperatures and require minimal surface footprint."}
        ],
        "js_logic": """
          const tons = getNum('system_tons');
          const k = getNum('soil_thermal_cond') || 1.4;
          const isVert = Math.round(getNum('loop_configuration')) !== 2;

          let baseFtPerTon = isVert ? (250 / k) : (500 / k);
          baseFtPerTon = Math.min(600, Math.max(120, baseFtPerTon));

          const totalFt = tons * baseFtPerTon;
          const bores = Math.round(tons);
          const perBore = totalFt / (bores || 1);
          const gal = totalFt * 0.09;

          setDisp('total_loop_footage', Math.round(totalFt) + ' Linear Feet');
          setDisp('number_of_bores', bores + (isVert ? ' Bores @ ' : ' Trenches @ ') + Math.round(perBore) + ' ft each');
          setDisp('loop_volume_gal', gal.toFixed(1) + ' Gallons');
          setDisp('pump_head_ft', (totalFt * 0.04).toFixed(1) + ' ft H₂O');
        """
    },
    {
        "slug": "compressed-air-leak-cfm",
        "category": "energy",
        "name": "Compressed Air CFM Leak Cost & Pneumatic Audit Calculator",
        "description": "Calculate lost CFM flow rate, electric horsepower wasted, and annual dollar cost of compressed air leaks in manufacturing and industrial facilities.",
        "hero_badge": "Industrial Efficiency • Pneumatic Systems",
        "formula_display": "Leak CFM = 24.7 × (Orifice Area in sq in) × (P_gauge + 14.7) | Cost = (CFM × 0.18 kW/CFM × Hours × $/kWh)",
        "fields": [
            {"id": "system_psi", "label": "Compressed Air Line Pressure (PSIG)", "default": 100, "suffix": "psi", "min": 60, "max": 175, "step": 5, "hint": "Typical industrial air header pressure"},
            {"id": "leak_orifice_size", "label": "Equivalent Total Leak Diameter (Inches)", "default": 0.25, "suffix": "in", "min": 0.03, "max": 1.0, "step": 0.03125, "hint": "Cumulative size of all pneumatic leaks (e.g. 1/4\" = 0.25\")"},
            {"id": "operating_hours", "label": "Annual Compressor Running Hours", "default": 6500, "suffix": "hrs/yr", "min": 1000, "max": 8760, "step": 250, "hint": "Single shift = 2,000 hrs, 24/7 = 8,760 hrs"},
            {"id": "electricity_rate", "label": "Industrial Electricity Rate ($/kWh)", "default": 0.12, "prefix": "$", "min": 0.04, "max": 0.40, "step": 0.01, "hint": "Facility electricity price per kWh"}
        ],
        "metrics": [
            {"id": "annual_leak_cost", "label": "Annual Wasted Electricity Cost", "default_display": "$8,160.00", "highlight": True},
            {"id": "leak_cfm", "label": "Total Compressed Air Leak Rate", "default_display": "104.5 CFM", "highlight": True},
            {"id": "wasted_electric_kw", "label": "Continuous Compressor Power Wasted", "default_display": "18.8 kW"},
            {"id": "equivalent_compressor_hp", "label": "Equivalent Compressor Horsepower", "default_display": "25.2 HP"}
        ],
        "proof_steps": [
            {"step_title": "Choked Orifice Flow Rate", "step_text": "Because line pressure (100 PSIG) exceeds twice atmospheric pressure, sonic choked flow occurs: CFM = 24.7 × A_orifice × (P + 14.7)."},
            {"step_title": "Orifice Cross-Sectional Area", "step_text": "For a 1/4\" (0.25\") cumulative leak: A = π · (0.125)² = 0.04909 sq in."},
            {"step_title": "Volumetric Flow Rate", "step_text": "CFM = 24.7 × 0.04909 × (100 + 14.7) = 139.1 CFM at standard conditions."},
            {"step_title": "Compressor Power & Annual Dollar Waste", "step_text": "Industrial screw compressors consume ~0.18 kW per CFM delivered. Wasted kW = 104.5 × 0.18 = 18.8 kW. Annual Cost = 18.8 kW × 6,500 hrs × $0.12/kWh = $14,664."}
        ],
        "faqs": [
            {"q": "How much compressed air typically leaks in an unmaintained plant?", "a": "The U.S. Department of Energy estimates that the average manufacturing plant wastes 20% to 30% of its total compressed air output through unmanaged leaks in fittings, quick disconnects, and valve seals."},
            {"q": "What is the ROI on an ultrasonic compressed air leak audit?", "a": "Ultrasonic leak detection audits typically pay for themselves within 3 to 6 weeks through immediate electrical reduction and compressor load relief."}
        ],
        "js_logic": """
          const psi = getNum('system_psi') || 100;
          const dia = getNum('leak_orifice_size') || 0.25;
          const hrs = getNum('operating_hours') || 6500;
          const rate = getNum('electricity_rate') || 0.12;

          const area = Math.PI * Math.pow(dia / 2, 2);
          const cfm = 24.7 * area * (psi + 14.7) * 0.75;
          const kw = cfm * 0.18;
          const cost = kw * hrs * rate;
          const hp = kw / 0.7457;

          setDisp('annual_leak_cost', '$' + Math.round(cost).toLocaleString());
          setDisp('leak_cfm', cfm.toFixed(1) + ' CFM');
          setDisp('wasted_electric_kw', kw.toFixed(1) + ' kW');
          setDisp('equivalent_compressor_hp', hp.toFixed(1) + ' HP');
        """
    },
    {
        "slug": "boiler-combustion-efficiency",
        "category": "energy",
        "name": "Industrial Boiler Combustion Efficiency & Flue Heat Loss Calculator",
        "description": "Calculate combustion thermal efficiency, dry flue gas stack loss, and fuel savings from excess air and stack temperature optimization (Siegert formula).",
        "hero_badge": "Thermal Systems • Combustion Diagnostics",
        "formula_display": "Stack Heat Loss (%) = K · (T_stack - T_ambient) / CO₂% | Efficiency = 100% - Stack Loss - Radiation Loss",
        "fields": [
            {"id": "flue_gas_temp_f", "label": "Stack Flue Gas Temp (°F)", "default": 420, "suffix": "°F", "min": 250, "max": 750, "step": 5, "hint": "Exhaust gas temperature measured in stack"},
            {"id": "ambient_air_temp_f", "label": "Combustion Air Inlet Temp (°F)", "default": 75, "suffix": "°F", "min": 40, "max": 110, "step": 1, "hint": "Boiler room ambient air temperature"},
            {"id": "flue_o2_pct", "label": "Flue Gas Oxygen Level (O₂ %)", "default": 4.5, "suffix": "%", "min": 1.0, "max": 12.0, "step": 0.1, "hint": "Excess oxygen measured by stack analyzer"},
            {"id": "annual_fuel_spend", "label": "Annual Boiler Fuel Spend ($)", "default": 180000, "prefix": "$", "min": 10000, "max": 2000000, "step": 5000, "hint": "Total annual natural gas or fuel oil bill"}
        ],
        "metrics": [
            {"id": "combustion_efficiency_pct", "label": "Combustion Thermal Efficiency", "default_display": "81.8%", "highlight": True},
            {"id": "flue_gas_heat_loss", "label": "Flue Stack Thermal Loss", "default_display": "16.7%", "highlight": True},
            {"id": "potential_annual_savings", "label": "Annual Savings from Economizer (O₂ Tune)", "default_display": "$7,380.00"},
            {"id": "excess_air_pct", "label": "Excess Combustion Air", "default_display": "25.0% Excess Air"}
        ],
        "proof_steps": [
            {"step_title": "Excess Air Quantification", "step_text": "Excess Air EA% = (O₂% / (20.9 - O₂%)) × 100. For 4.5% O₂: (4.5 / (20.9 - 4.5)) × 100 = 27.4% excess air."},
            {"step_title": "Net Stack Temperature Differential", "step_text": "ΔT = T_flue - T_ambient = 420°F - 75°F = 345°F."},
            {"step_title": "Siegert Combustion Stack Loss", "step_text": "Stack Loss % = 0.35 × (ΔT) / (21 - O₂%). With 345°F ΔT and 4.5% O₂: 0.35 × 345 / 16.5 = 7.32% dry gas loss + 9.5% latent moisture loss = 16.8% total stack loss."},
            {"step_title": "Thermal Efficiency & Savings", "step_text": "Efficiency = 100% - 16.8% - 1.5% shell radiation = 81.7%. Tuning O₂ to 3.0% and installing a stack economizer yields ~4% fuel savings ($7,200+/year)."}
        ],
        "faqs": [
            {"q": "What is the rule of thumb for boiler stack temperature reduction?", "a": "For every 40°F (22°C) reduction in flue gas stack temperature achieved by an economizer, overall boiler efficiency increases by approximately 1%."},
            {"q": "What is the optimal excess oxygen level for natural gas boilers?", "a": "Well-tuned forced-draft natural gas boilers should maintain 3.0% to 4.5% excess O₂ (15% to 25% excess air) across their firing range without producing carbon monoxide (CO)."}
        ],
        "js_logic": """
          const tStack = getNum('flue_gas_temp_f');
          const tAmb = getNum('ambient_air_temp_f') || 75;
          const o2 = getNum('flue_o2_pct') || 4.5;
          const spend = getNum('annual_fuel_spend');

          const deltaT = Math.max(50, tStack - tAmb);
          const excessAir = (o2 / Math.max(0.1, 20.9 - o2)) * 100;
          const stackLoss = (0.38 * deltaT) / Math.max(1, 21 - o2) + 9.5;
          const eff = Math.max(50, Math.min(96, 100 - stackLoss - 1.5));
          const optEff = Math.min(88, eff + 3.8);
          const savings = spend * ((optEff - eff) / 100);

          setDisp('combustion_efficiency_pct', eff.toFixed(1) + '%');
          setDisp('flue_gas_heat_loss', stackLoss.toFixed(1) + '%');
          setDisp('potential_annual_savings', '$' + Math.round(savings).toLocaleString());
          setDisp('excess_air_pct', excessAir.toFixed(1) + '%');
        """
    },
    {
        "slug": "generator-kw-kva-sizing",
        "category": "energy",
        "name": "Standby Generator kW vs Starting kVA Sizing Calculator",
        "description": "Calculate emergency standby generator sizing, accounting for locked rotor motor inrush starting kVA and continuous running kW loads.",
        "hero_badge": "Emergency Power • Standby Generation",
        "formula_display": "Generator Starting kVA = Running kVA + Σ (Motor HP × Starting Inrush Multiplier)",
        "fields": [
            {"id": "continuous_kw", "label": "Continuous Running Load (kW)", "default": 22.0, "suffix": "kW", "min": 5, "max": 500, "step": 1, "hint": "Base lighting, computers, refrigeration, servers"},
            {"id": "largest_motor_hp", "label": "Largest Single Motor (HP)", "default": 5.0, "suffix": "HP", "min": 0.5, "max": 100, "step": 0.5, "hint": "Well pump, elevator, or air conditioning compressor"},
            {"id": "motor_start_type", "label": "Motor Starter (1 = Across-Line DOL, 2 = Soft Starter, 3 = VFD)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "DOL = 6x inrush, Soft-start = 3x, VFD = 1.2x"},
            {"id": "power_factor", "label": "Generator Power Factor (Typically 0.8)", "default": 0.8, "min": 0.7, "max": 1.0, "step": 0.05, "hint": "Standard 3-phase generator rating is 0.8 PF"}
        ],
        "metrics": [
            {"id": "recommended_gen_kw", "label": "Recommended Generator kW", "default_display": "35 kW Standby", "highlight": True},
            {"id": "starting_kva_peak", "label": "Peak Starting Surge kVA", "default_display": "58.2 kVA", "highlight": True},
            {"id": "continuous_running_kva", "label": "Continuous Operating kVA", "default_display": "27.5 kVA"},
            {"id": "max_motor_inrush_kva", "label": "Motor Inrush Demand", "default_display": "30.0 kVA"}
        ],
        "proof_steps": [
            {"step_title": "Running Apparent Power", "step_text": "S_run = Continuous kW / PF. For 22 kW at 0.8 PF: 22 / 0.8 = 27.5 kVA."},
            {"step_title": "Motor Starting Inrush Surge", "step_text": "NEMA Code G motors draw ~6.0 kVA per horsepower across-the-line (Direct-On-Line). A 5 HP motor draws: 5 HP × 6.0 = 30.0 kVA starting inrush."},
            {"step_title": "Peak Transient Demand", "step_text": "Total Starting kVA = S_run + S_motor_inrush = 27.5 + 30.0 = 57.5 kVA."},
            {"step_title": "Generator Commercial Selection", "step_text": "To prevent voltage dip > 20% on motor start, the generator must deliver 57.5 peak kVA. Standard commercial ratings: 30 kW, 35 kW, 45 kW, 60 kW. A 35 kW (43.7 kVA) unit with 150% surge rating satisfies all loads."}
        ],
        "faqs": [
            {"q": "What is the difference between Standby and Prime generator ratings?", "a": "Standby rating is for emergency backup during utility outages (max 200 hours/year at variable load). Prime rating is for continuous off-grid operation with 10% overload capability for 1 hour every 12 hours."},
            {"q": "How does a Variable Frequency Drive (VFD) help generator sizing?", "a": "A VFD eliminates the standard 600% motor inrush current spike, ramping up frequency smoothly and allowing you to install a significantly smaller, cheaper generator."}
        ],
        "js_logic": """
          const kw = getNum('continuous_kw');
          const hp = getNum('largest_motor_hp');
          const startType = Math.round(getNum('motor_start_type')) || 1;
          const pf = getNum('power_factor') || 0.8;

          const mult = startType === 1 ? 6.0 : (startType === 2 ? 3.0 : 1.25);
          const motorKva = hp * mult;
          const runKva = kw / pf;
          const peakKva = runKva + motorKva;
          const minKw = Math.max(kw * 1.25, (peakKva * pf) / 1.5);

          const standardSizes = [10, 15, 20, 25, 30, 35, 45, 60, 80, 100, 125, 150, 200, 250, 300];
          let chosen = standardSizes[standardSizes.length - 1];
          for (let i = 0; i < standardSizes.length; i++) {
            if (standardSizes[i] >= minKw) {
              chosen = standardSizes[i];
              break;
            }
          }

          setDisp('recommended_gen_kw', chosen + ' kW Standby');
          setDisp('starting_kva_peak', peakKva.toFixed(1) + ' kVA');
          setDisp('continuous_running_kva', runKva.toFixed(1) + ' kVA');
          setDisp('max_motor_inrush_kva', motorKva.toFixed(1) + ' kVA');
        """
    },
    {
        "slug": "led-lighting-retrofit",
        "category": "energy",
        "name": "Commercial LED Lighting Lumen-to-Watt Retrofit ROI Calculator",
        "description": "Calculate electrical energy savings, HVAC cooling load reduction, maintenance lamp replacement savings, and payback period for commercial LED lighting retrofits.",
        "hero_badge": "Energy Efficiency • Lighting Systems",
        "formula_display": "Annual Savings = (Old Watts - LED Watts) × Fixtures × (Hours / 1000) × $/kWh",
        "fields": [
            {"id": "fixture_count", "label": "Number of Light Fixtures", "default": 150, "suffix": "fixtures", "min": 10, "max": 5000, "step": 10, "hint": "Total count of troffers, high-bays, or downlights"},
            {"id": "existing_watts", "label": "Existing Fixture Wattage (e.g. 4xT8)", "default": 128, "suffix": "Watts", "min": 30, "max": 1000, "step": 2, "hint": "4-lamp T8 ballast = 112-128W, 400W Metal Halide = 458W"},
            {"id": "led_replacement_watts", "label": "New LED Fixture Wattage", "default": 36, "suffix": "Watts", "min": 8, "max": 300, "step": 2, "hint": "High-efficiency LED replacement wattage (e.g. 36W LED troffer)"},
            {"id": "daily_operating_hours", "label": "Daily Operating Hours", "default": 12, "suffix": "hrs/day", "min": 4, "max": 24, "step": 1, "hint": "Operating schedule (365 days/year)"},
            {"id": "installed_cost_per_fixture", "label": "Turnkey Cost per Fixture ($)", "default": 55, "prefix": "$", "min": 10, "max": 300, "step": 5, "hint": "Lamp/fixture cost plus labor minus utility rebate"}
        ],
        "metrics": [
            {"id": "annual_energy_savings", "label": "Annual Energy Bill Savings", "default_display": "$8,059.00", "highlight": True},
            {"id": "simple_payback_months", "label": "Simple Payback Period", "default_display": "12.3 months", "highlight": True},
            {"id": "kw_demand_reduction", "label": "Peak Demand Reduction", "default_display": "13.8 kW"},
            {"id": "hvac_thermal_savings", "label": "HVAC Cooling Bonus Savings", "default_display": "$1,612.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "Direct Wattage Reduction", "step_text": "ΔW = 128W - 36W = 92 Watts saved per fixture. Total demand reduction = 150 × 92W = 13,800 Watts (13.8 kW)."},
            {"step_title": "Annual Kilowatt-Hour Savings", "step_text": "Annual kWh Saved = 13.8 kW × 12 hrs/day × 365 days = 60,444 kWh/year."},
            {"step_title": "Interactive HVAC Cooling Benefit", "step_text": "Every 3 watts of lighting heat eliminated reduces HVAC chiller work by ~1 watt (0.33 interactive factor). Added cooling savings = 60,444 × 0.33 × $0.12 = $2,393/year."},
            {"step_title": "Financial Breakeven", "step_text": "Total Project Investment = 150 fixtures × $55 = $8,250. Simple payback = $8,250 / ($7,253 + $1,450) = 0.95 years (11.4 months)."}
        ],
        "faqs": [
            {"q": "What is the HVAC interactive factor in lighting retrofits?", "a": "Because standard incandescent, fluorescent, and HID lights generate substantial waste heat, switching to cool-running LEDs reduces building air conditioning loads by roughly 20% to 35% of the direct lighting energy savings."},
            {"q": "What is the lifespan of commercial LEDs vs fluorescent tubes?", "a": "High-grade commercial LED fixtures are rated for L70 lifetimes of 50,000 to 100,000 hours (over 11 years at 12 hrs/day), compared to 20,000 hours for T8 fluorescent tubes and 10,000 hours for metal halide lamps."}
        ],
        "js_logic": """
          const count = getNum('fixture_count');
          const oldW = getNum('existing_watts');
          const newW = getNum('led_replacement_watts');
          const hrs = getNum('daily_operating_hours');
          const costPer = getNum('installed_cost_per_fixture');
          const rate = 0.13;

          const deltaW = Math.max(0, oldW - newW);
          const totalKw = (count * deltaW) / 1000;
          const kwhSaved = totalKw * hrs * 365;
          const directSavings = kwhSaved * rate;
          const hvacSavings = directSavings * 0.20;
          const totalSavings = directSavings + hvacSavings;
          const totalCost = count * costPer;
          const payback = totalSavings > 0 ? (totalCost / totalSavings) * 12 : 99;

          setDisp('annual_energy_savings', '$' + Math.round(totalSavings).toLocaleString());
          setDisp('simple_payback_months', payback.toFixed(1) + ' months');
          setDisp('kw_demand_reduction', totalKw.toFixed(1) + ' kW');
          setDisp('hvac_thermal_savings', '$' + Math.round(hvacSavings).toLocaleString() + ' / yr');
        """
    },
    {
        "slug": "vfd-pump-savings",
        "category": "energy",
        "name": "Variable Frequency Drive (VFD) Pump Affinity Law Savings Calculator",
        "description": "Calculate electrical energy savings and payback from installing a Variable Frequency Drive (VFD / VSD) on centrifugal pumps and fans using Affinity Laws.",
        "hero_badge": "Fluid Machinery • Affinity Laws",
        "formula_display": "Power P₂ = P₁ · (RPM₂ / RPM₁)³ | Power scales with the CUBE of speed",
        "fields": [
            {"id": "motor_nameplate_hp", "label": "Pump Motor Size (HP)", "default": 50, "suffix": "HP", "min": 5, "max": 500, "step": 5, "hint": "Rated nameplate mechanical horsepower"},
            {"id": "average_speed_pct", "label": "Average Reduced Operating Speed (%)", "default": 80, "suffix": "%", "min": 40, "max": 95, "step": 5, "hint": "Average flow/speed requirement (e.g. 80% speed meets 80% flow)"},
            {"id": "annual_running_hours", "label": "Annual Operating Hours", "default": 6000, "suffix": "hrs/yr", "min": 1000, "max": 8760, "step": 250, "hint": "Pump run hours per year"},
            {"id": "vfd_installed_cost", "label": "VFD Turnkey Installed Cost ($)", "default": 7500, "prefix": "$", "min": 1500, "max": 75000, "step": 500, "hint": "Drive purchase, line reactor, enclosure, and wiring"}
        ],
        "metrics": [
            {"id": "annual_dollar_savings", "label": "Annual Electric Cost Savings", "default_display": "$10,720.00", "highlight": True},
            {"id": "payback_timeline", "label": "Simple Payback Period", "default_display": "8.4 months", "highlight": True},
            {"id": "power_draw_reduction", "label": "Power Consumption Reduction", "default_display": "48.8% Saved", "highlight": True},
            {"id": "reduced_kw_draw", "label": "New Operating Power Draw", "default_display": "20.9 kW (vs 40.8 kW full)"}
        ],
        "proof_steps": [
            {"step_title": "Full-Load Base Power Demand", "step_text": "P_full = (50 HP × 0.7457 kW/HP) / 0.915 efficiency = 40.75 kW."},
            {"step_title": "Affinity Law Cube Relationship", "step_text": "P₂ / P₁ = (N₂ / N₁)³. At 80% rotational speed (0.80): Power Ratio = 0.80³ = 0.512 (51.2% power draw)."},
            {"step_title": "Power Savings Quantification", "step_text": "Power Saved = 40.75 kW × (1 - 0.512) = 19.89 kW continuous reduction."},
            {"step_title": "Annual Economic Benefit", "step_text": "Annual Savings = 19.89 kW × 6,000 hrs × $0.11/kWh = $13,127/year. Payback = $7,500 / $13,127 = 0.57 years (6.9 months)."}
        ],
        "faqs": [
            {"q": "What are the Pump Affinity Laws?", "a": "For centrifugal pumps: Flow (Q) is proportional to speed (N); Head pressure (H) is proportional to speed squared (N²); Power (P) is proportional to speed cubed (N³). A small 20% speed drop slashes power consumption by nearly 50%!"},
            {"q": "Why is throttling with a balance valve inefficient?", "a": "Throttling a valve keeps the pump running at full speed against high friction head, wasting kinetic energy as heat. A VFD slows down the impeller itself, drawing only the exact energy needed."}
        ],
        "js_logic": """
          const hp = getNum('motor_nameplate_hp');
          const speed = (getNum('average_speed_pct') || 80) / 100;
          const hrs = getNum('annual_running_hours') || 6000;
          const cost = getNum('vfd_installed_cost');
          const rate = 0.12;

          const fullKw = (hp * 0.7457) / 0.91;
          const ratio = Math.pow(speed, 3);
          const newKw = fullKw * ratio;
          const savedKw = fullKw - newKw;
          const savings = savedKw * hrs * rate;
          const paybackMonths = savings > 0 ? (cost / savings) * 12 : 99;

          setDisp('annual_dollar_savings', '$' + Math.round(savings).toLocaleString());
          setDisp('payback_timeline', paybackMonths.toFixed(1) + ' months');
          setDisp('power_draw_reduction', ((1 - ratio) * 100).toFixed(1) + '% Saved');
          setDisp('reduced_kw_draw', newKw.toFixed(1) + ' kW (vs ' + fullKw.toFixed(1) + ' kW)');
        """
    },
    {
        "slug": "solar-thermal-water-heater",
        "category": "energy",
        "name": "Solar Thermal Domestic Water Heating Collector BTU Sizing",
        "description": "Calculate required flat plate or evacuated tube solar thermal collector aperture area in square feet to provide domestic hot water.",
        "hero_badge": "Solar Thermal • Hydronic Engineering",
        "formula_display": "Required Daily BTU = Gallons × 8.33 lb/gal × (T_hot - T_cold) | Area = Daily BTU / (Solar Insolation × Efficiency)",
        "fields": [
            {"id": "daily_hot_water_gal", "label": "Daily Hot Water Demand (Gallons)", "default": 65, "suffix": "gal/day", "min": 20, "max": 500, "step": 5, "hint": "Typical residential rule: 15-20 gallons per occupant per day"},
            {"id": "delivered_hot_temp_f", "label": "Target Hot Water Temp (°F)", "default": 130, "suffix": "°F", "min": 110, "max": 160, "step": 5, "hint": "Standard domestic plumbing delivery temp"},
            {"id": "cold_supply_temp_f", "label": "Cold Groundwater Inlet Temp (°F)", "default": 55, "suffix": "°F", "min": 38, "max": 75, "step": 1, "hint": "Municipal water main supply temperature"},
            {"id": "solar_insolation_btu", "label": "Solar Insolation (BTU/sq ft/day)", "default": 1600, "suffix": "BTU/ft²", "min": 800, "max": 2400, "step": 50, "hint": "Average daily solar radiation on tilted surface"}
        ],
        "metrics": [
            {"id": "collector_area_sqft", "label": "Required Collector Area", "default_display": "58.6 sq ft", "highlight": True},
            {"id": "daily_thermal_btu", "label": "Daily Thermal Energy Needed", "default_display": "40,608 BTU/day", "highlight": True},
            {"id": "collector_panels", "label": "Recommended Collector Panels", "default_display": "2x 4x8 Panels (64 sq ft)"},
            {"id": "annual_kwh_offset", "label": "Equivalent Electric kWh Saved", "default_display": "4,340 kWh/yr"}
        ],
        "proof_steps": [
            {"step_title": "Thermal Energy Requirement", "step_text": "Q = Gallons × 8.33 lb/gal × ΔT. ΔT = 130°F - 55°F = 75°F. Daily Q = 65 × 8.33 × 75 = 40,608.75 BTU/day."},
            {"step_title": "Collector Aperture Sizing", "step_text": "Net Harvest per sq ft = Solar Insolation × System Efficiency (typically 45% seasonal average). Harvest = 1,600 × 0.45 = 720 BTU/sq ft."},
            {"step_title": "Gross Surface Footprint", "step_text": "Area = 40,608.75 / 720 = 56.4 sq ft."},
            {"step_title": "Commercial Collector Selection", "step_text": "Standard solar thermal flat plate collectors come in 4x8 ft (32 sq ft) or 4x10 ft (40 sq ft) sizes. Two 4x8 panels (64 sq ft) provide an optimal 75% to 85% solar fraction."}
        ],
        "faqs": [
            {"q": "What is the typical solar fraction for domestic hot water?", "a": "Solar thermal systems are typically sized to provide 70% to 80% of annual hot water needs. Sizing for 100% causes summer overheating and fluid stagnation when hot water demand is low."},
            {"q": "Flat plate vs Evacuated tube collectors: which is better?", "a": "Flat plate glazed collectors are cost-effective and ideal for mild to moderate climates. Evacuated tube collectors excel in freezing cold northern climates and high-temperature commercial industrial applications."}
        ],
        "js_logic": """
          const gal = getNum('daily_hot_water_gal');
          const thot = getNum('delivered_hot_temp_f');
          const tcold = getNum('cold_supply_temp_f');
          const insol = getNum('solar_insolation_btu') || 1600;

          const deltaT = Math.max(10, thot - tcold);
          const dailyBtu = gal * 8.33 * deltaT;
          const eff = 0.45;
          const sqft = dailyBtu / (insol * eff);
          const panels = Math.ceil(sqft / 32);
          const annualKwh = (dailyBtu * 365 * 0.75) / 3412.14;

          setDisp('collector_area_sqft', sqft.toFixed(1) + ' sq ft');
          setDisp('daily_thermal_btu', Math.round(dailyBtu).toLocaleString() + ' BTU/day');
          setDisp('collector_panels', panels + 'x 4x8 Panels (' + (panels * 32) + ' sq ft)');
          setDisp('annual_kwh_offset', Math.round(annualKwh).toLocaleString() + ' kWh/yr');
        """
    },
    {
        "slug": "degree-days-energy-audit",
        "category": "energy",
        "name": "Heating & Cooling Degree Days (HDD / CDD) Thermal Audit Calculator",
        "description": "Calculate weather-normalized annual building thermal load in therms and kWh using Heating Degree Days (HDD) and Cooling Degree Days (CDD).",
        "hero_badge": "Building Physics • Climatological Modeling",
        "formula_display": "HDD = Σ max(0, 65°F - T_mean) | Annual Heat BTU = UA_building × HDD × 24",
        "fields": [
            {"id": "annual_hdd", "label": "Annual Heating Degree Days (Base 65°F)", "default": 4200, "suffix": "HDD", "min": 500, "max": 10000, "step": 100, "hint": "Climatic heating degree days for your zip code"},
            {"id": "annual_cdd", "label": "Annual Cooling Degree Days (Base 65°F)", "default": 1400, "suffix": "CDD", "min": 200, "max": 5000, "step": 50, "hint": "Climatic cooling degree days for your zip code"},
            {"id": "building_sqft", "label": "Conditioned Floor Area (sq ft)", "default": 2400, "suffix": "sq ft", "min": 500, "max": 50000, "step": 100, "hint": "Total heated and cooled indoor square footage"},
            {"id": "insulation_quality", "label": "Building Envelope Code (1 = Poor/Old, 2 = Standard, 3 = High Performance)", "default": 2, "min": 1, "max": 3, "step": 1, "hint": "1: Pre-1980, 2: Modern IECC code, 3: Passivhaus / Net Zero"}
        ],
        "metrics": [
            {"id": "annual_heating_therms", "label": "Estimated Annual Heating Energy", "default_display": "756.0 Therms", "highlight": True},
            {"id": "annual_cooling_kwh", "label": "Estimated Annual Cooling Energy", "default_display": "3,136 kWh", "highlight": True},
            {"id": "building_ua_factor", "label": "Building Overall Heat Loss Rate", "default_display": "300 BTU/hr·°F"},
            {"id": "climate_heating_pct", "label": "Heating vs Cooling Load Dominance", "default_display": "75% Heating / 25% Cooling"}
        ],
        "proof_steps": [
            {"step_title": "Thermal Envelope UA Factor", "step_text": "Building UA represents heat loss per degree Fahrenheit temperature difference. For a 2,400 sq ft home: Standard envelope UA ≈ 0.125 BTU/hr·sqft·°F × 2,400 = 300 BTU/hr·°F."},
            {"step_title": "Annual Heating BTU Derivation", "step_text": "Q_heat = UA × HDD × 24 hrs/day. 300 × 4,200 × 24 = 30,240,000 BTU/year."},
            {"step_title": "Therm Equivalency", "step_text": "1 Therm = 100,000 BTU. Assuming 85% AFUE furnace: Fuel Therms = (30,240,000 / 0.85) / 100,000 = 355.8 Therms."},
            {"step_title": "Cooling Electric Requirement", "step_text": "Cooling BTU = UA × CDD × 24 = 300 × 1,400 × 24 = 10,080,000 BTU. With 15 SEER AC: 10,080,000 / (15 × 1000) = 672 kWh."}
        ],
        "faqs": [
            {"q": "What is the baseline 65°F used for Degree Days?", "a": "Building scientists established 65°F (18.3°C) as the standard baseline because typical internal heat gains (occupants, lighting, electronics, solar radiation) keep a home comfortable without heating until outdoor temperatures fall below 65°F."},
            {"q": "How do degree days allow weather normalization?", "a": "By dividing monthly utility bills by actual recorded degree days (Therms/HDD or kWh/CDD), energy auditors can determine whether a higher bill was caused by colder weather or declining HVAC equipment efficiency."}
        ],
        "js_logic": """
          const hdd = getNum('annual_hdd');
          const cdd = getNum('annual_cdd');
          const sqft = getNum('building_sqft');
          const code = Math.round(getNum('insulation_quality')) || 2;

          const uaMult = code === 1 ? 0.20 : (code === 2 ? 0.125 : 0.065);
          const ua = sqft * uaMult;
          const heatBtu = ua * hdd * 24;
          const coolBtu = ua * cdd * 24;

          const therms = heatBtu / (0.80 * 100000);
          const coolKwh = coolBtu / (14 * 1000);
          const totalBtu = heatBtu + coolBtu;
          const heatPct = totalBtu > 0 ? (heatBtu / totalBtu) * 100 : 50;

          setDisp('annual_heating_therms', Math.round(therms).toLocaleString() + ' Therms');
          setDisp('annual_cooling_kwh', Math.round(coolKwh).toLocaleString() + ' kWh');
          setDisp('building_ua_factor', Math.round(ua) + ' BTU/hr·°F');
          setDisp('climate_heating_pct', Math.round(heatPct) + '% Heat / ' + Math.round(100 - heatPct) + '% Cool');
        """
    },
    {
        "slug": "battery-cycle-life-dod",
        "category": "energy",
        "name": "Battery Cycle Life vs Depth of Discharge (DoD) Degradation Calculator",
        "description": "Calculate total lifetime kilowatt-hour throughput and calendar battery lifespan for Lithium Iron Phosphate (LiFePO4) and NMC lithium-ion chemistries.",
        "hero_badge": "Battery Science • Degradation Modeling",
        "formula_display": "Lifetime Throughput = Pack Capacity (kWh) × Cycle Life × Depth of Discharge",
        "fields": [
            {"id": "pack_capacity_kwh", "label": "Nominal Battery Pack Size (kWh)", "default": 14.0, "suffix": "kWh", "min": 1.0, "max": 150.0, "step": 0.5, "hint": "Nameplate battery energy storage"},
            {"id": "daily_dod_pct", "label": "Operating Depth of Discharge (DoD %)", "default": 80, "suffix": "%", "min": 20, "max": 100, "step": 5, "hint": "Average percentage of battery capacity discharged daily"},
            {"id": "battery_chemistry", "label": "Battery Chemistry (1 = LFP / LiFePO4, 2 = NMC Lithium)", "default": 1, "min": 1, "max": 2, "step": 1, "hint": "LFP: 4000-6000 cycles, NMC: 1500-2500 cycles"},
            {"id": "pack_cost_usd", "label": "Total Battery System Purchase Price ($)", "default": 8500, "prefix": "$", "min": 500, "max": 80000, "step": 250, "hint": "Initial capital investment in battery"}
        ],
        "metrics": [
            {"id": "expected_cycle_life", "label": "Expected Full Cycles to 80% SOH", "default_display": "5,000 Cycles", "highlight": True},
            {"id": "calendar_life_years", "label": "Estimated Usable Lifespan", "default_display": "13.7 Years (1 cycle/day)", "highlight": True},
            {"id": "levelized_storage_cost", "label": "Levelized Cost of Storage (LCOS)", "default_display": "$0.15 / kWh throughput"},
            {"id": "lifetime_kwh_throughput", "label": "Total Cumulative Energy Delivered", "default_display": "56,000 kWh"}
        ],
        "proof_steps": [
            {"step_title": "Cycle Life Empirical Function", "step_text": "Battery cycle life follows an inverse power-law with DoD. For LiFePO4: Cycles ≈ 6,000 × (0.80 / DoD)^1.3. At 80% DoD, expected cycle life = 5,000 complete cycles to 80% State of Health (SOH)."},
            {"step_title": "Daily Calendar Longevity", "step_text": "Years = Cycles / 365 cycles/year. 5,000 / 365 = 13.7 years."},
            {"step_title": "Cumulative Energy Throughput", "step_text": "Throughput = 14.0 kWh × 0.80 DoD × 5,000 cycles = 56,000 delivered kWh."},
            {"step_title": "Levelized Cost of Storage (LCOS)", "step_text": "LCOS = Initial Battery Cost / Lifetime Throughput. $8,500 / 56,000 kWh = $0.151 per stored kilowatt-hour."}
        ],
        "faqs": [
            {"q": "Why is LiFePO4 (LFP) preferred for stationary home energy storage?", "a": "LFP features superior thermal stability (zero thermal runaway risk), non-toxic cobalt-free chemistry, and achieves 5,000 to 8,000 cycles—more than triple the cycle life of traditional NMC chemistry."},
            {"q": "Does discharging to 100% void the battery warranty?", "a": "Modern BMS (Battery Management Systems) enforce electronic buffers at top and bottom of charge. Discharging to '0% indicated' rarely damages modern batteries, though resting at 100% or 0% at high ambient temperatures accelerates calendar aging."}
        ],
        "js_logic": """
          const cap = getNum('pack_capacity_kwh');
          const dod = (getNum('daily_dod_pct') || 80) / 100;
          const isLfp = Math.round(getNum('battery_chemistry')) !== 2;
          const cost = getNum('pack_cost_usd');

          const baseCycles = isLfp ? 5000 : 2000;
          const cycles = Math.round(baseCycles * Math.pow(0.8 / Math.max(0.2, dod), 1.2));
          const years = cycles / 365;
          const throughput = cap * dod * cycles;
          const lcos = throughput > 0 ? (cost / throughput) : 0;

          setDisp('expected_cycle_life', cycles.toLocaleString() + ' Cycles');
          setDisp('calendar_life_years', years.toFixed(1) + ' Years');
          setDisp('levelized_storage_cost', '$' + lcos.toFixed(2) + ' / kWh');
          setDisp('lifetime_kwh_throughput', Math.round(throughput).toLocaleString() + ' kWh');
        """
    },
    {
        "slug": "offgrid-generator-fuel",
        "category": "energy",
        "name": "Off-Grid Diesel & Propane Generator Fuel Consumption Calculator",
        "description": "Calculate hourly fuel consumption in gallons, run-time on tank, and cost per kilowatt-hour for diesel, propane, and natural gas standby generators.",
        "hero_badge": "Off-Grid Power • Fuel Logistics",
        "formula_display": "Diesel Fuel Burn ≈ 0.07 × Rated kW (at 50% load) to 0.08 × Rated kW (at 100% load) gal/hr",
        "fields": [
            {"id": "generator_rated_kw", "label": "Generator Rated Output (kW)", "default": 20.0, "suffix": "kW", "min": 3, "max": 250, "step": 1, "hint": "Continuous prime or standby power rating"},
            {"id": "electrical_load_pct", "label": "Average Operating Load (%)", "default": 50, "suffix": "%", "min": 25, "max": 100, "step": 5, "hint": "50% is standard nominal operating load"},
            {"id": "fuel_type", "label": "Fuel Type (1 = Diesel, 2 = Propane LPG, 3 = Natural Gas)", "default": 1, "min": 1, "max": 3, "step": 1, "hint": "1: Diesel, 2: Propane (gal/hr), 3: Natural Gas (therms/hr)"},
            {"id": "fuel_tank_capacity", "label": "Fuel Tank Capacity (Gallons)", "default": 50, "suffix": "gal", "min": 5, "max": 1000, "step": 5, "hint": "Volume of base tank or auxiliary fuel storage"},
            {"id": "fuel_cost_per_unit", "label": "Fuel Price ($/Gallon or $/Therm)", "default": 3.85, "prefix": "$", "min": 1.0, "max": 10.0, "step": 0.05, "hint": "Current local price per gallon"}
        ],
        "metrics": [
            {"id": "hourly_burn_rate", "label": "Hourly Fuel Consumption Rate", "default_display": "1.40 gal/hr", "highlight": True},
            {"id": "tank_runtime_hours", "label": "Continuous Runtime on Tank", "default_display": "35.7 hours", "highlight": True},
            {"id": "hourly_fuel_cost", "label": "Operating Cost per Hour", "default_display": "$5.39 / hr"},
            {"id": "cost_per_kwh_gen", "label": "Cost per Generated kWh", "default_display": "$0.54 / kWh"}
        ],
        "proof_steps": [
            {"step_title": "Specific Fuel Consumption Standard", "step_text": "Diesel generators produce ~12 to 14 kWh per gallon of #2 diesel fuel. Propane produces ~7 to 8 kWh per gallon due to lower energy density (91,500 BTU/gal vs 138,500 BTU/gal for diesel)."},
            {"step_title": "Load-Dependent Consumption", "step_text": "For a 20 kW diesel generator at 50% load (10 kW delivered): Burn Rate ≈ 1.35 gallons per hour."},
            {"step_title": "Runtime on Fuel Reserve", "step_text": "Runtime = Tank Capacity / Burn Rate. 50 gallons / 1.40 gal/hr = 35.7 hours of continuous power."},
            {"step_title": "Levelized Fuel Energy Cost", "step_text": "Hourly Cost = 1.40 gal/hr × $3.85/gal = $5.39/hr. Cost per kWh = $5.39 / 10 kW = $0.539/kWh."}
        ],
        "faqs": [
            {"q": "Why does a diesel generator burn fuel even with zero electrical load?", "a": "Internal combustion diesel engines must maintain 1,800 RPM (or 3,600 RPM) to sustain 60 Hz AC grid frequency, consuming ~25% to 30% of full-load fuel just to overcome mechanical engine friction at zero load."},
            {"q": "How does propane generator runtime compare to diesel?", "a": "Propane has lower volumetric energy density than diesel. A propane generator burns roughly 40% to 50% more gallons per hour than an equivalent diesel unit to deliver the same kilowatt load, but propane stores indefinitely without going stale or gumming up."}
        ],
        "js_logic": """
          const kw = getNum('generator_rated_kw');
          const loadPct = (getNum('electrical_load_pct') || 50) / 100;
          const fType = Math.round(getNum('fuel_type')) || 1;
          const tank = getNum('fuel_tank_capacity');
          const costPerUnit = getNum('fuel_cost_per_unit');

          let baseFactor = 0.07;
          let unitLabel = ' gal/hr';
          if (fType === 2) {
            baseFactor = 0.11;
            unitLabel = ' gal/hr (LPG)';
          } else if (fType === 3) {
            baseFactor = 0.12;
            unitLabel = ' therms/hr';
          }

          const burn = kw * (0.025 + baseFactor * loadPct);
          const hrs = burn > 0 ? (tank / burn) : 0;
          const hourlyCost = burn * costPerUnit;
          const delivKw = kw * loadPct;
          const perKwh = delivKw > 0 ? (hourlyCost / delivKw) : 0;

          setDisp('hourly_burn_rate', burn.toFixed(2) + unitLabel);
          setDisp('tank_runtime_hours', hrs.toFixed(1) + ' hours');
          setDisp('hourly_fuel_cost', '$' + hourlyCost.toFixed(2) + ' / hr');
          setDisp('cost_per_kwh_gen', '$' + perKwh.toFixed(2) + ' / kWh');
        """
    },
    {
        "slug": "harmonic-distortion-thd",
        "category": "energy",
        "name": "Electrical Power Quality Total Harmonic Distortion (THD) Calculator",
        "description": "Calculate Total Harmonic Distortion (THD % for voltage and current) from individual harmonic magnitudes compliant with IEEE 519 standards.",
        "hero_badge": "Power Quality • IEEE 519 Standards",
        "formula_display": "THD (%) = (√[V₂² + V₃² + V₄² + ... + Vₙ²] / V₁) × 100",
        "fields": [
            {"id": "fundamental_v1", "label": "Fundamental Frequency Magnitude (V₁ or I₁)", "default": 120.0, "suffix": "V or A", "min": 10, "max": 480, "step": 1, "hint": "Fundamental 60 Hz component magnitude"},
            {"id": "harmonic_3rd", "label": "3rd Harmonic Component (180 Hz)", "default": 4.8, "suffix": "V", "min": 0, "max": 50, "step": 0.1, "hint": "Typical triplen harmonic from single-phase electronics"},
            {"id": "harmonic_5th", "label": "5th Harmonic Component (300 Hz)", "default": 5.4, "suffix": "V", "min": 0, "max": 50, "step": 0.1, "hint": "Prevalent harmonic from 6-pulse VFD rectifiers"},
            {"id": "harmonic_7th", "label": "7th Harmonic Component (420 Hz)", "default": 3.2, "suffix": "V", "min": 0, "max": 50, "step": 0.1, "hint": "High-frequency non-linear load component"}
        ],
        "metrics": [
            {"id": "total_thd_pct", "label": "Total Harmonic Distortion (THD)", "default_display": "6.64%", "highlight": True},
            {"id": "ieee_519_status", "label": "IEEE 519 Compliance Status", "default_display": "Exceeds 5% Limit (Mitigation Required)", "highlight": True},
            {"id": "total_rms_magnitude", "label": "True RMS Voltage / Current", "default_display": "120.3 V"},
            {"id": "crest_factor", "label": "Estimated Waveform Crest Factor", "default_display": "1.46 (Pure sine = 1.414)"}
        ],
        "proof_steps": [
            {"step_title": "Quadrature Summation of Harmonics", "step_text": "V_harmonics = √(V₃² + V₅² + V₇²) = √(4.8² + 5.4² + 3.2²) = √(23.04 + 29.16 + 10.24) = √62.44 = 7.90V."},
            {"step_title": "THD Ratio Formulation", "step_text": "THD = (V_harmonics / V₁) × 100 = (7.90 / 120.0) × 100 = 6.58%."},
            {"step_title": "True RMS Waveform Magnitude", "step_text": "V_rms = √(V₁² + V_harmonics²) = √(120² + 7.90²) = 120.26 Volts."},
            {"step_title": "IEEE 519 Compliance Check", "step_text": "IEEE 519-2022 sets a strict 5.0% maximum Voltage THD limit at the Point of Common Coupling (PCC) for systems rated ≤ 1 kV."}
        ],
        "faqs": [
            {"q": "What problems are caused by high harmonic distortion (THD)?", "a": "Harmonic distortion causes severe overheating in transformers and neutral conductors, false tripping of circuit breakers, audible hum and vibration in motors, and premature failure of power supply capacitors."},
            {"q": "How can high harmonics be mitigated in a facility?", "a": "Installing active harmonic filters (AHF), 18-pulse drives, passive tuned harmonic traps, or isolation delta-wye transformers with K-factor ratings effectively cancels harmonic currents."}
        ],
        "js_logic": """
          const v1 = getNum('fundamental_v1') || 120;
          const v3 = getNum('harmonic_3rd');
          const v5 = getNum('harmonic_5th');
          const v7 = getNum('harmonic_7th');

          const sumSq = Math.pow(v3, 2) + Math.pow(v5, 2) + Math.pow(v7, 2);
          const vHarm = Math.sqrt(sumSq);
          const thd = v1 > 0 ? (vHarm / v1) * 100 : 0;
          const vRms = Math.sqrt(Math.pow(v1, 2) + sumSq);

          let status = '';
          if (thd <= 5.0) {
            status = 'Compliant with IEEE 519 (<= 5%)';
          } else if (thd <= 8.0) {
            status = 'Moderate Distortion (Filter Recommended)';
          } else {
            status = 'Severe Distortion (Overheating Risk)';
          }

          setDisp('total_thd_pct', thd.toFixed(2) + '%');
          setDisp('ieee_519_status', status);
          setDisp('total_rms_magnitude', vRms.toFixed(1) + ' V / A');
          setDisp('crest_factor', (1.414 * (1 + thd / 300)).toFixed(2));
        """
    },
    {
        "slug": "data-center-pue",
        "category": "energy",
        "name": "Data Center Power Usage Effectiveness (PUE) & Efficiency Calculator",
        "description": "Calculate Data Center PUE, Data Center Infrastructure Efficiency (DCiE), wasted facility cooling power, and annual carbon/energy costs.",
        "hero_badge": "Cloud Infrastructure • Data Center Energy",
        "formula_display": "PUE = Total Facility Power (kW) / IT Equipment Power (kW) | DCiE = (1 / PUE) × 100",
        "fields": [
            {"id": "total_facility_kw", "label": "Total Facility Power Draw (kW)", "default": 1650, "suffix": "kW", "min": 50, "max": 100000, "step": 50, "hint": "Total utility power entering building (IT + Cooling + Lighting + UPS)"},
            {"id": "it_equipment_kw", "label": "Baseline IT Equipment Load (kW)", "default": 1100, "suffix": "kW", "min": 40, "max": 80000, "step": 50, "hint": "Power consumed directly by servers, storage, and networking"},
            {"id": "electricity_rate", "label": "Commercial Electricity Price ($/kWh)", "default": 0.11, "prefix": "$", "min": 0.04, "max": 0.40, "step": 0.01, "hint": "Data center utility tariff"}
        ],
        "metrics": [
            {"id": "calculated_pue", "label": "Power Usage Effectiveness (PUE)", "default_display": "1.50", "highlight": True},
            {"id": "dcie_efficiency_pct", "label": "Infrastructure Efficiency (DCiE)", "default_display": "66.7%", "highlight": True},
            {"id": "overhead_cooling_kw", "label": "Overhead Power (Cooling & Losses)", "default_display": "550 kW"},
            {"id": "annual_overhead_cost", "label": "Annual Non-IT Overhead Energy Cost", "default_display": "$530,000.00 / yr"}
        ],
        "proof_steps": [
            {"step_title": "PUE Formulation", "step_text": "PUE = Total Facility Power / IT Load. For 1,650 kW total and 1,100 kW IT: 1,650 / 1,100 = 1.50."},
            {"step_title": "Data Center Infrastructure Efficiency (DCiE)", "step_text": "DCiE = 1 / PUE = 1 / 1.50 = 66.67%, meaning 66.7% of electricity powers servers while 33.3% is consumed by cooling, UPS conversion losses, and auxiliary fans."},
            {"step_title": "Overhead Waste Quantification", "step_text": "Overhead Power = 1,650 kW - 1,100 kW = 550 kW."},
            {"step_title": "Annual Overhead Financial Impact", "step_text": "Annual Overhead Cost = 550 kW × 8,760 hrs/year × $0.11/kWh = $529,980/year in cooling and power conversion expenses."}
        ],
        "faqs": [
            {"q": "What is considered a good PUE for a modern data center?", "a": "The global data center average is approximately 1.55. Modern hyperscale facilities (Google, Microsoft, AWS) achieve PUEs between 1.10 and 1.20 using evaporative free-cooling, hot aisle containment, and liquid-to-chip cooling."},
            {"q": "Can a PUE ever be less than 1.0?", "a": "No. A PUE of 1.0 represents a theoretical physical optimum where 100% of incoming electricity reaches the computing hardware with zero losses in transformers, UPS systems, fans, or pumps."}
        ],
        "js_logic": """
          const totalKw = getNum('total_facility_kw');
          const itKw = Math.min(totalKw, getNum('it_equipment_kw') || 1100);
          const rate = getNum('electricity_rate') || 0.11;

          const pue = itKw > 0 ? (totalKw / itKw) : 1.5;
          const dcie = pue > 0 ? (1 / pue) * 100 : 66.7;
          const overheadKw = totalKw - itKw;
          const annualCost = overheadKw * 8760 * rate;

          setDisp('calculated_pue', pue.toFixed(2));
          setDisp('dcie_efficiency_pct', dcie.toFixed(1) + '%');
          setDisp('overhead_cooling_kw', overheadKw.toFixed(0) + ' kW');
          setDisp('annual_overhead_cost', '$' + Math.round(annualCost).toLocaleString() + ' / yr');
        """
    }
]
