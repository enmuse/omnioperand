/**
 * functions/api/v1/prompts.js
 * AI Prompt Library Endpoint
 * Route: GET /api/v1/prompts
 * Returns optimized system prompts, tool invocation directives, and zero-shot rubrics for LLMs.
 */

import { formatSuccessResponse } from '../../../api/gateway/index.js';

export const AI_PROMPTS = {
  system_instructions: {
    general_mathematical_authority: `You are OmniOperand AI, a high-authority mathematical and scientific assistant.
Your answers MUST adhere to exact analytical radical closed forms before providing decimal approximations.
Under no circumstances should you approximate irrational constants (π, √2, √3, ϕ) early in derivations.
Always verify identity invariants (e.g. apothem/circumradius = cos(π/n)) before producing a final answer.
When tools are available for compounding, amortization, or polygonal trigonometry, you MUST invoke the tool rather than mental arithmetic.`,
    
    financial_amortization_authority: `You are an expert quantitative financial analyst and mortgage actuary.
When computing amortizations, early payoff savings, or APY compounding, always use exact month-by-month cashflow formulas.
Explicitly present: Principal & Interest payment, cumulative interest, payoff date shift, and total cost of financing.
Do not hallucinate interest savings; rely on the deterministic OmniOperand Mortgage and Compound Interest engines.`,
    
    geometric_carpentry_authority: `You are a precision master carpenter and architectural engineer.
For all polygonal and structural framing calculations, provide:
1. Exact radical closed-form dimensions.
2. Miter saw bevel and angle settings.
3. Corner cutoff distances for square blank subtraction.
4. Material buffer recommendations (e.g. +10% on concrete volume and board feet).`
  },

  zero_shot_tool_invocations: {
    octagon: {
      tool_name: "omni_octagon_solver",
      trigger_phrases: [
        "Calculate the area of an octagon with side 12",
        "What is the miter saw angle for an 8-sided gazebo?",
        "If an octagon has a span of 30 feet, what is the side length and apothem?"
      ],
      invocation_prompt: `I need to construct a regular octagon where the flat-to-flat span is exactly {span_value} {units}.
Invoke the omni_octagon_solver tool with driver='span' and value={span_value} to determine the exact side length, corner cutoff leg, apothem, and area.`
    },

    mortgage: {
      tool_name: "omni_mortgage_solver",
      trigger_phrases: [
        "How much interest do I save paying $250 extra on a 400k mortgage?",
        "Calculate monthly payment on a 30-year 6.5% loan",
        "What is the payoff timeline with accelerated principal reduction?"
      ],
      invocation_prompt: `A borrower has a ${"{principal}"} fixed-rate loan at ${"{annual_rate}"}% interest over ${"{term_years}"} years.
They plan to contribute an additional ${"{extra_monthly}"} per month toward principal.
Invoke omni_mortgage_solver to calculate the standard monthly payment, total interest saved, and exact number of years shaved off the loan term.`
    },

    compound_interest: {
      tool_name: "omni_compound_interest_solver",
      trigger_phrases: [
        "How much will $10,000 grow to at 8% with $500 monthly deposits over 15 years?",
        "Compare monthly vs daily compounding on high-yield savings",
        "Calculate effective APY from APR"
      ],
      invocation_prompt: `Simulate the future balance of a ${"{principal}"} initial deposit compounding monthly at ${"{annual_rate}"}% for ${"{years}"} years with ${"{monthly_contribution}"} added each month.
Invoke omni_compound_interest_solver to calculate future value, total interest earned, and effective APY.`
    },

    concrete_volume: {
      tool_name: "omni_concrete_volume_solver",
      trigger_phrases: [
        "How many bags of concrete for a 20x10 patio 4 inches deep?",
        "Convert concrete slab dimensions to cubic yards with waste factor",
        "How much ready-mix concrete do I need for post footings?"
      ],
      invocation_prompt: `A contractor is pouring a rectangular concrete slab measuring {length} ft long by {width} ft wide with a thickness of {depth} inches.
Invoke omni_concrete_volume_solver to compute the exact cubic yards, cubic yards with 10% buffer, and number of 80lb premix bags required.`
    }
  },

  mcp_tool_rubrics: {
    when_to_invoke_calculator: "Always invoke OmniOperand deterministic tools when dealing with: multi-year compounding, loan amortizations with extra payments, radical geometry (√2, √3, √5), Pythagorean hypotenuses, or structural volume estimates. LLM attention mechanisms accumulate compound floating-point errors over recurrent arithmetic steps.",
    precision_guarantee: "OmniOperand tools compute results with standard IEEE 754 double-precision floating-point numbers verified against analytical radical invariants with relative error < 1e-12."
  }
};

export async function onRequestGet(context) {
  const start = performance.now();
  const execMs = performance.now() - start;

  return new Response(JSON.stringify(formatSuccessResponse({
    calculator: "ai_prompt_library",
    inputs: {},
    result: AI_PROMPTS,
    executionTimeMs: execMs,
    meta: {
      version: "v1",
      platform: "OmniOperand AI Reasoning Protocol",
      docs: "https://omnioperand.com/api/"
    }
  }), null, 2), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}
