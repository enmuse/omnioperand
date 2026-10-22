/**
 * functions/api/clinical-triage.js
 * Cloudflare Pages Function: POST /api/clinical-triage
 * Deterministic Telehealth Psychiatric Triage & Statutory Medication Router
 */

const FPA_STATES = new Set(['VT', 'ME', 'MA', 'NY', 'CO', 'WA', 'OR', 'NM', 'MN', 'AZ', 'NV']);

export async function onRequestPost(context) {
  try {
    let body = {};
    const ct = context.request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      body = await context.request.json();
    } else {
      const form = await context.request.formData();
      body = Object.fromEntries(form.entries());
    }

    const state = String(body.patient_state || "NC").trim().toUpperCase();
    const complaint = String(body.primary_complaint || "depression_mdd");
    const phqScores = Array.isArray(body.phq9_scores) ? body.phq9_scores : [2, 2, 3, 2, 1, 1, 1, 0, 0];
    const q9Score = parseInt(body.phq9_q9 ?? phqScores[8] ?? 0);
    const gad7 = parseInt(body.gad7_score || 11);
    const meds = String(body.current_medications || "").toLowerCase();

    // 1. Critical Q9 Crisis Interlock
    const crisisActive = q9Score > 0;

    // 2. PHQ-9 & GAD-7 Total Scoring
    const phqTotal = phqScores.reduce((a, b) => a + (parseInt(b) || 0), 0);
    let phqSeverity = "Mild";
    if (phqTotal >= 20) phqSeverity = "Severe";
    else if (phqTotal >= 15) phqSeverity = "Moderately Severe";
    else if (phqTotal >= 10) phqSeverity = "Moderate";
    else if (phqTotal < 5) phqSeverity = "Minimal";

    let gad7Severity = "Mild";
    if (gad7 >= 15) gad7Severity = "Severe";
    else if (gad7 >= 10) gad7Severity = "Moderate";
    else if (gad7 < 5) gad7Severity = "Minimal";

    // 3. Controlled Substance & Ryan Haight Act Check (21 U.S.C. § 829(e))
    const isScheduleII = meds.includes('adderall') || meds.includes('vyvanse') || meds.includes('methylphenidate') || meds.includes('ritalin') || meds.includes('dexedrine');
    const isScheduleIV = meds.includes('xanax') || meds.includes('klonopin') || meds.includes('ativan') || meds.includes('valium') || meds.includes('alprazolam') || meds.includes('clonazepam');

    const controlledDetected = isScheduleII || isScheduleIV;
    let ryanHaightNotice = "No controlled substances reported. Routine non-controlled psychiatric medication management eligible for direct telehealth evaluation.";
    if (controlledDetected) {
      ryanHaightNotice = "Controlled substance reported (" + (isScheduleII ? "Schedule II Stimulant" : "Schedule IV Sedative") + "). Under Ryan Haight Act (21 U.S.C. § 829(e)) and DEA telemedicine rules, prescription requires an active federal PHE telemedicine waiver or verified in-person collaborative examination.";
    }

    // 4. State Licensure & Practice Authority
    const isFpa = FPA_STATES.has(state);
    const practiceAuthority = isFpa ? "Full Practice Authority (FPA - Independent Prescribing)" : "Collaborative Practice / Supervisory Agreement Required";

    return new Response(JSON.stringify({
      success: true,
      tool: "psychiatric_clinical_triage",
      patient_state: state,
      primary_complaint: complaint,
      crisis_override: crisisActive,
      emergency_protocol: crisisActive ? {
        active: true,
        alert: "EMERGENCY: Thoughts of self-harm reported. Routine telehealth disabled.",
        crisis_lifeline: "Dial or Text 988 (Available 24/7, Free, Confidential)",
        crisis_text_line: "Text HOME to 741741"
      } : { active: false },
      psychometrics: {
        phq9_total: phqTotal,
        phq9_severity: phqSeverity,
        phq9_q9_suicide_score: q9Score,
        gad7_total: gad7,
        gad7_severity: gad7Severity
      },
      statutory_compliance: {
        state: state,
        practice_authority: practiceAuthority,
        ryan_haight_act: {
          controlled_substance_detected: controlledDetected,
          class: isScheduleII ? "Schedule II" : (isScheduleIV ? "Schedule IV" : "Non-Controlled"),
          statutory_notice: ryanHaightNotice
        }
      },
      estimated_costs_usd: {
        intake_evaluation_cpt99205: 295,
        followup_med_management_cpt99214: 145,
        estimated_commercial_copay: 35
      },
      dispatch_endpoint: "/api/leads"
    }, null, 2), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    return new Response(JSON.stringify({ success: false, error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
