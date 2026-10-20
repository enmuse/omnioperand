/**
 * api/schemas/validation.js
 * Strict runtime input and payload validation using Zod schemas.
 * Ensures zero unexpected parameters, correct types, and enforced bounds.
 */

import { z } from 'zod';

export const OctagonInputSchema = z.object({
  driver: z.enum([
    'side', 'a', 'area', 'a_poly', 'perimeter', 'p',
    'apothem', 'inradius', 'r_i', 'circumradius', 'r',
    'span', 's', 'short_diagonal', 'd_s', 'long_diagonal', 'd_l'
  ]).default('side'),
  value: z.coerce.number().positive("Value must be strictly positive").default(10),
  precision: z.coerce.number().int().min(2).max(14).default(6),
  units: z.string().max(20).default('units')
});

export const RegularPolygonInputSchema = z.object({
  n: z.coerce.number().int().min(3, "Must have at least 3 sides").max(1000, "Maximum 1000 sides").default(8),
  driver: z.enum(['side', 'a', 'area', 'perimeter', 'apothem', 'inradius', 'circumradius', 'span']).default('side'),
  value: z.coerce.number().positive("Value must be strictly positive").default(10),
  precision: z.coerce.number().int().min(2).max(14).default(6),
  units: z.string().max(20).default('units')
});

export const MortgageInputSchema = z.object({
  principal: z.coerce.number().positive("Principal must be greater than zero").max(1e9).default(400000),
  annual_rate: z.coerce.number().min(0, "Rate cannot be negative").max(100, "Rate cannot exceed 100%").default(6.5),
  term_years: z.coerce.number().min(1, "Term must be at least 1 year").max(50, "Term cannot exceed 50 years").default(30),
  extra_monthly: z.coerce.number().min(0).max(1e7).default(0)
});

export const CompoundInterestInputSchema = z.object({
  principal: z.coerce.number().min(0).max(1e10).default(10000),
  annual_rate: z.coerce.number().min(0).max(500).default(7.0),
  years: z.coerce.number().positive().max(100).default(10),
  compound_frequency: z.coerce.number().int().refine(val => [1, 2, 4, 12, 365].includes(val), {
    message: "Compound frequency must be 1 (annually), 2 (semi-annually), 4 (quarterly), 12 (monthly), or 365 (daily)"
  }).default(12),
  monthly_contribution: z.coerce.number().min(0).max(1e8).default(500)
});

export const CagrInputSchema = z.object({
  initial_value: z.coerce.number().positive("Initial value must be positive").default(10000),
  final_value: z.coerce.number().nonnegative("Final value cannot be negative").default(25000),
  years: z.coerce.number().positive("Years must be positive").max(200).default(5)
});

export const AutoLoanInputSchema = z.object({
  vehicle_price: z.coerce.number().positive().max(1e7).default(35000),
  down_payment: z.coerce.number().min(0).max(1e7).default(5000),
  trade_in: z.coerce.number().min(0).max(1e7).default(2000),
  interest_rate: z.coerce.number().min(0).max(50).default(5.9),
  term_months: z.coerce.number().int().min(6).max(120).default(60),
  sales_tax_pct: z.coerce.number().min(0).max(30).default(6.0)
});

export const ConcreteVolumeInputSchema = z.object({
  shape: z.enum(['slab', 'footing', 'column', 'cylinder']).default('slab'),
  length: z.coerce.number().positive().default(20),
  width: z.coerce.number().positive().default(10),
  depth: z.coerce.number().positive().default(4), // inches
  diameter: z.coerce.number().positive().optional().default(12),
  height: z.coerce.number().positive().optional().default(8)
});

export const RoofPitchInputSchema = z.object({
  rise: z.coerce.number().positive().default(6),
  run: z.coerce.number().positive().default(12),
  building_run_feet: z.coerce.number().positive().default(16)
});

export const CircleSectorInputSchema = z.object({
  radius: z.coerce.number().positive().default(10),
  angle_deg: z.coerce.number().positive().max(360).default(60)
});

export const RightTriangleInputSchema = z.object({
  leg_a: z.coerce.number().positive().default(3),
  leg_b: z.coerce.number().positive().default(4)
});

// Auth & Key Management Schemas
export const CreateApiKeySchema = z.object({
  tier: z.enum(['free', 'pro', 'enterprise']).default('free'),
  name: z.string().min(2).max(100).default('Default Key'),
  email: z.string().email().optional()
});

// Lead Capture Schema
export const LeadCaptureSchema = z.object({
  email: z.string().email("A valid email address is required"),
  calculator: z.string().min(1),
  partner_id: z.string().optional().default('direct'),
  inputs: z.record(z.any()).optional().default({}),
  timestamp: z.string().optional()
});

export const VALIDATORS = {
  "octagon": OctagonInputSchema,
  "regular-polygon": RegularPolygonInputSchema,
  "mortgage": MortgageInputSchema,
  "compound-interest": CompoundInterestInputSchema,
  "cagr": CagrInputSchema,
  "auto-loan": AutoLoanInputSchema,
  "concrete-volume": ConcreteVolumeInputSchema,
  "roof-pitch": RoofPitchInputSchema,
  "circle-sector": CircleSectorInputSchema,
  "right-triangle": RightTriangleInputSchema
};
