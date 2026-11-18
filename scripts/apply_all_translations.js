#!/usr/bin/env node
/**
 * scripts/apply_all_translations.js
 * Comprehensive Localization Orchestrator for OmniOperand
 *
 * Applies:
 * 1. COMMON_UI headers, footers, LLM badges and buttons across all 11 languages
 * 2. Specialized FAQs in HTML and JSON-LD for all 19 Batch 2 solvers
 * 3. Step-by-Step Proof derivations for all 18 geometry/statistics solvers
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { COMMON_UI } from './translations/common_ui.js';
import { GEOMETRY_2D } from './translations/geometry_2d.js';
import { GEOMETRY_3D } from './translations/geometry_3d.js';
import { STATISTICS } from './translations/statistics.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const LANGS = ["de", "es", "fr", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"];

const ALL_SOLVERS = {
  ...GEOMETRY_2D,
  ...GEOMETRY_3D,
  ...STATISTICS
};

export function runGlobalLocalization() {
  console.log("=========================================================");
  console.log("🚀 Running Global Mathematical Localization Across 11 Languages");
  console.log("=========================================================\n");

  let totalFilesProcessed = 0;
  let totalFaqsLocalized = 0;
  let totalProofsLocalized = 0;

  for (const lang of LANGS) {
    const langDir = path.join(REPO_ROOT, lang);
    if (!fs.existsSync(langDir)) continue;

    const ui = COMMON_UI[lang];
    let langFileCount = 0;

    function walkDir(dir) {
      const entries = fs.readdirSync(dir);
      for (const e of entries) {
        const full = path.join(dir, e);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
          walkDir(full);
        } else if (e === 'index.html') {
          const rel = path.relative(REPO_ROOT, full).replace(/\\/g, '/');
          let content = fs.readFileSync(full, 'utf8');
          let modified = false;

          // ==========================================================
          // 1. COMMON UI STRINGS REPLACEMENT
          // ==========================================================
          if (ui) {
            // Heading: Frequently Asked Questions
            if (content.includes("Frequently Asked Questions")) {
              content = content.replace(/Frequently Asked Questions/g, ui.faq_heading);
              modified = true;
            }
            // Heading: Calculated Output Metrics
            if (content.includes("Calculated Output Metrics")) {
              content = content.replace(/Calculated Output Metrics/g, ui.calc_output_metrics);
              modified = true;
            }
            // Heading: Artificial Intelligence & Prompt Integration
            if (content.includes("Artificial Intelligence & Prompt Integration")) {
              content = content.replace(/Artificial Intelligence & Prompt Integration/g, ui.ai_prompt_int);
              modified = true;
            }
            // Heading: Step-by-Step Mathematical Derivation
            if (content.includes("Step-by-Step Mathematical Derivation")) {
              content = content.replace(/Step-by-Step Mathematical Derivation/g, ui.step_by_step_proof);
              modified = true;
            }
            // LLM directive badge
            if (content.includes("LLM Directive & API Spec")) {
              content = content.replace(/LLM Directive & API Spec/g, ui.llm_directive_badge);
              modified = true;
            }
            // LLM prompt explanation text
            if (content.includes("Paste this verified mathematical prompt directly into ChatGPT")) {
              content = content.replace(/Paste this verified mathematical prompt directly into ChatGPT[^\n<]+/g, ui.llm_expl);
              modified = true;
            }
            // Copy buttons
            if (content.includes("Copy Prompt for AI")) {
              content = content.replace(/Copy Prompt for AI/g, ui.copy_prompt);
              modified = true;
            }
            if (content.includes("Copy API Endpoint")) {
              content = content.replace(/Copy API Endpoint/g, ui.copy_api);
              modified = true;
            }
            // Footer bottom verified notice
            if (content.includes("All mathematical proofs and calculations verified.") ||
                content.includes("All mathematical proofs and calculations rigorously verified")) {
              content = content.replace(/© 2026 OmniOperand\.\s*All mathematical proofs and calculations (?:rigorously )?verified\./g, ui.footer_verified);
              modified = true;
            }
            if (content.includes("Hosted on Cloudflare Edge • Pure Client-Side Math") ||
                content.includes("Hosted on Cloudflare Edge Network • Built with Zero External Dependencies")) {
              content = content.replace(/Hosted on Cloudflare Edge(?: Network)? • (?:Pure Client-Side Math|Built with Zero External Dependencies)/g, ui.footer_hosting);
              modified = true;
            }
            // Feature checkmarks
            if (content.includes("<span>✓ Standardized for <code>llms.txt</code></span>")) {
              content = content.replace(/<span>✓ Standardized for <code>llms\.txt<\/code><\/span>/g, `<span>${ui.tag_llms}</span>`);
              content = content.replace(/<span>✓ Exact Radical Form & Closed Formulas<\/span>/g, `<span>${ui.tag_exact}</span>`);
              content = content.replace(/<span>✓ Machine-Readable Edge API<\/span>/g, `<span>${ui.tag_api}</span>`);
              modified = true;
            }
          }

          // ==========================================================
          // 2. SOLVER-SPECIFIC FAQS & PROOFS
          // ==========================================================
          for (const [solverKey, solverData] of Object.entries(ALL_SOLVERS)) {
            // Check if this file belongs to this solver
            // e.g. rel === "no/geometry/ellipse/index.html" and solverKey === "geometry/ellipse"
            if (rel.includes(solverKey)) {
              // 2A. LOCALIZED FAQS
              if (solverData.faqs && solverData.faqs[lang]) {
                const localizedFaqs = solverData.faqs[lang];

                // Replace in HTML body:
                // Find all faq-item occurrences
                const faqItemRegex = /<div class="faq-item(?: open)?">\s*<div class="faq-question">\s*<span>([^<]+)<\/span>\s*<span class="faq-icon">\+<\/span>\s*<\/div>\s*<div class="faq-answer">([\s\S]*?)<\/div>\s*<\/div>/g;
                let itemIndex = 0;
                content = content.replace(faqItemRegex, (match, oldQ, oldA) => {
                  if (itemIndex < localizedFaqs.length) {
                    const newFaq = localizedFaqs[itemIndex++];
                    totalFaqsLocalized++;
                    return `<div class="faq-item">
          <div class="faq-question">
            <span>${newFaq.q}</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-answer">
            ${newFaq.a}
          </div>
        </div>`;
                  }
                  return match;
                });

                // Replace in JSON-LD Schema:
                // Find FAQPage mainEntity Questions
                const jsonLdFaqRegex = /\{\s*"@type":\s*"Question",\s*"name":\s*"([^"]+)",\s*"acceptedAnswer":\s*\{\s*"@type":\s*"Answer",\s*"text":\s*"([^"]+)"\s*\}\s*\}/g;
                let schemaIndex = 0;
                content = content.replace(jsonLdFaqRegex, (match, oldQ, oldA) => {
                  if (schemaIndex < localizedFaqs.length) {
                    const newFaq = localizedFaqs[schemaIndex++];
                    const escapedA = newFaq.a.replace(/"/g, '\\"');
                    const escapedQ = newFaq.q.replace(/"/g, '\\"');
                    return `{\n          "@type": "Question",\n          "name": "${escapedQ}",\n          "acceptedAnswer": {\n            "@type": "Answer",\n            "text": "${escapedA}"\n          }\n        }`;
                  }
                  return match;
                });

                modified = true;
              }

              // 2B. LOCALIZED PROOFS
              if (solverData.proofs && solverData.proofs[lang]) {
                const localizedProofs = solverData.proofs[lang];

                const proofStepRegex = /<div class="proof-step">\s*<div class="step-num">(\d+)<\/div>\s*<div class="step-content">\s*<strong>([^<]+)<\/strong>\s*<p>([\s\S]*?)<\/p>\s*<\/div>\s*<\/div>/g;
                let proofIndex = 0;
                content = content.replace(proofStepRegex, (match, stepNum, oldTitle, oldBody) => {
                  if (proofIndex < localizedProofs.length) {
                    const newProof = localizedProofs[proofIndex++];
                    totalProofsLocalized++;
                    return `<div class="proof-step">
            <div class="step-num">${stepNum}</div>
            <div class="step-content">
              <strong>${newProof.title}</strong>
              <p>${newProof.body}</p>
            </div>
          </div>`;
                  }
                  return match;
                });

                modified = true;
              }
            }
          }

          if (modified) {
            fs.writeFileSync(full, content, 'utf8');
            langFileCount++;
            totalFilesProcessed++;
          }
        }
      }
    }

    walkDir(langDir);
    console.log(`  • /${lang}/: ${langFileCount} files updated with localized UI, FAQs, and proofs.`);
  }

  console.log(`\n🎉 Localization sweep completed!`);
  console.log(`   - Total Files Updated: ${totalFilesProcessed}`);
  console.log(`   - Total FAQs Localized: ${totalFaqsLocalized}`);
  console.log(`   - Total Proof Steps Localized: ${totalProofsLocalized}\n`);
}

runGlobalLocalization();

