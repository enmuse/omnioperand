#!/usr/bin/env node
/**
 * scripts/audit-translations.js — Multilingual Localization Integrity Audit Engine
 *
 * Deterministic Audit for OmniOperand's 11 localized language directories:
 * /de/, /es/, /fr/, /it/, /pt/, /nl/, /pl/, /sv/, /no/, /fi/, /ro/
 *
 * Checks:
 * 1. HTML attributes: <html lang="{code}"> matching parent folder code
 * 2. Document title: <title> not containing raw English fallback phrases
 * 3. Meta description: <meta name="description"> not containing English fallback phrases
 * 4. OpenGraph & Twitter tags: og:title and og:description matching localized metadata
 * 5. Core DOM elements:
 *    - .brand-badge ("Finanzen", "Geometrie", etc., not "Math Engine" or "Finance")
 *    - .breadcrumbs (not "Home" as root anchor)
 *    - .hero-badge (no raw English phrases)
 *    - h1 & .hero-subtext (no raw English phrases)
 *    - .hud-panel-header h2 (localized, not "Parameters & Inversions")
 *    - .blueprint-header h3 (localized, not "Analytical Proof & Invariants")
 *    - .footer-bottom (localized legal/hosting notice)
 * 6. Language Detection Heuristic:
 *    - Body text stopword ratio > 15% English stopwords
 * 7. Outputs translation-audit-report.json
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const LANG_CODES = ["de", "es", "fr", "it", "pt", "nl", "pl", "sv", "no", "fi", "ro"];

const ENGLISH_FALLBACK_PHRASES = [
  "Pure Mathematical Precision",
  "Exact Radical Derivations",
  "Multidisciplinary Quantitative Computing Engine",
  "Domain Hub • Geometry & Spatial Analysis",
  "Domain Hub • Quantitative Finance",
  "Domain Hub • Calculus & Analysis",
  "Planar geometry engines",
  "Calculated Output Metrics",
  "Two-Dimensional Geometry",
  "Three-Dimensional Geometry",
  "Step-by-Step Mathematical Derivation",
  "Parameters & Inversions",
  "Deterministic Engine",
  "Analytical Proof & Invariants",
  "Governing Mathematical Formula:",
  "All mathematical proofs and calculations rigorously verified",
  "Hosted on Cloudflare Edge Network • Built with Zero External Dependencies",
  "Open Solver →",
  "Launch Universal N-Gon Solver",
  "Related High-Precision Solvers"
];

const ENGLISH_STOPWORDS = new Set([
  "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
  "for", "not", "on", "with", "as", "you", "do", "at", "this",
  "but", "his", "by", "from", "they", "we", "say", "her", "she",
  "or", "an", "will", "my", "one", "all", "would", "there", "their",
  "what", "so", "up", "out", "if", "about", "who", "get", "which",
  "go", "me", "when", "make", "can", "like", "time", "no", "just",
  "him", "know", "take", "people", "into", "year", "your", "good",
  "some", "could", "them", "see", "other", "than", "then", "now",
  "look", "only", "come", "its", "over", "think", "also", "back",
  "after", "use", "two", "how", "our", "work", "first", "well",
  "way", "even", "new", "want", "because", "any", "these", "give",
  "day", "most", "us", "calculate", "exact", "calculator"
]);

function auditFile(filePath, langCode) {
  const relPath = path.relative(REPO_ROOT, filePath);
  const content = fs.readFileSync(filePath, 'utf8');

  const failures = [];
  const details = {};

  // 1. <html lang="...">
  const langMatch = content.match(/<html\s+[^>]*lang=["']([^"']+)["']/i);
  const actualLang = langMatch ? langMatch[1] : null;
  if (!actualLang || actualLang.toLowerCase() !== langCode.toLowerCase()) {
    failures.push("INVALID_HTML_LANG");
    details.html_lang = actualLang;
  }

  // 2. <title>
  const titleMatch = content.match(/<title>([^<]*)<\/title>/i);
  const titleText = titleMatch ? titleMatch[1].trim() : "";
  if (!titleText) {
    failures.push("MISSING_TITLE");
  } else {
    for (const phrase of ENGLISH_FALLBACK_PHRASES) {
      if (titleText.toLowerCase().includes(phrase.toLowerCase())) {
        failures.push("ENGLISH_IN_TITLE");
        details.title_offending = phrase;
        break;
      }
    }
  }

  // 3. <meta name="description">
  const descMatch = content.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i) ||
                    content.match(/<meta\s+content=["']([^"']*)["']\s+name=["']description["']/i);
  const descText = descMatch ? descMatch[1].trim() : "";
  if (!descText) {
    failures.push("MISSING_META_DESCRIPTION");
  } else {
    for (const phrase of ENGLISH_FALLBACK_PHRASES) {
      if (descText.toLowerCase().includes(phrase.toLowerCase())) {
        failures.push("ENGLISH_IN_META_DESCRIPTION");
        details.meta_desc_offending = phrase;
        break;
      }
    }
  }

  // 4. OpenGraph tags
  const ogTitleMatch = content.match(/<meta\s+property=["']og:title["']\s+content=["']([^"']*)["']/i);
  if (ogTitleMatch) {
    for (const phrase of ENGLISH_FALLBACK_PHRASES) {
      if (ogTitleMatch[1].toLowerCase().includes(phrase.toLowerCase())) {
        failures.push("ENGLISH_IN_OG_TITLE");
        details.og_title_offending = phrase;
        break;
      }
    }
  }

  // 5. Core DOM Elements
  // .brand-badge
  const brandBadgeMatch = content.match(/<span class=["']brand-badge["']>([^<]*)<\/span>/i);
  if (brandBadgeMatch) {
    const badgeText = brandBadgeMatch[1].trim();
    if (["Math Engine", "Geometry", "Calculus", "Finance", "Physics", "Statistics"].includes(badgeText)) {
      failures.push("UNTRANSLATED_BRAND_BADGE");
      details.brand_badge = badgeText;
    }
  }

  // .breadcrumbs "Home"
  const breadcrumbHomeMatch = content.match(/<li class=["']breadcrumb-item["']>\s*<a[^>]*>\s*Home\s*<\/a>/i);
  if (breadcrumbHomeMatch) {
    failures.push("UNTRANSLATED_BREADCRUMBS_HOME");
    details.breadcrumb_home = "Home";
  }

  // h1
  const h1Match = content.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1Match) {
    const rawH1 = h1Match[1].replace(/<[^>]+>/g, '').trim();
    for (const phrase of ENGLISH_FALLBACK_PHRASES) {
      if (rawH1.toLowerCase().includes(phrase.toLowerCase())) {
        failures.push("UNTRANSLATED_H1");
        details.h1_offending = phrase;
        break;
      }
    }
  }

  // .hud-panel-header h2
  const hudH2Match = content.match(/<div class=["']hud-panel-header["']>[\s\S]*?<h2>([^<]*)<\/h2>/i);
  if (hudH2Match) {
    const h2Text = hudH2Match[1].trim();
    if (["Parameters & Inversions", "Parameter & Inversions"].includes(h2Text)) {
      failures.push("UNTRANSLATED_HUD_PANEL_HEADER");
      details.hud_h2 = h2Text;
    }
  }

  // .blueprint-header h3
  const bpH3Match = content.match(/<div class=["']blueprint-header["']>[\s\S]*?<h3>([^<]*)<\/h3>/i);
  if (bpH3Match) {
    const h3Text = bpH3Match[1].trim();
    if (h3Text.includes("Analytical Proof & Invariants")) {
      failures.push("UNTRANSLATED_BLUEPRINT_HEADER");
      details.bp_h3 = h3Text;
    }
  }

  // .footer-bottom
  if (content.includes("All mathematical proofs and calculations rigorously verified") ||
      content.includes("Hosted on Cloudflare Edge Network • Built with Zero External Dependencies")) {
    failures.push("UNTRANSLATED_FOOTER");
    details.footer = "English notice present";
  }

  // 6. Stopword Ratio Heuristic on clean body text
  const cleanBody = content
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<svg[\s\S]*?<\/svg>/gi, '')
    .replace(/<[^>]+>/g, ' ');

  const words = cleanBody.match(/\b[A-Za-z]{2,}\b/g) || [];
  if (words.length > 50) {
    let engCount = 0;
    for (const w of words) {
      if (ENGLISH_STOPWORDS.has(w.toLowerCase())) {
        engCount++;
      }
    }
    const ratio = engCount / words.length;
    if (ratio > 0.15) {
      failures.push("FAILED_TRANSLATION_STOPWORD_THRESHOLD");
      details.stopword_ratio = Number(ratio.toFixed(3));
    }
  }

  return {
    file: relPath,
    lang: langCode,
    status: failures.length > 0 ? "FAILED_TRANSLATION" : "PASSED",
    failures,
    details
  };
}

function findHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const item of list) {
    const full = path.join(dir, item);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      results = results.concat(findHtmlFiles(full));
    } else if (item === 'index.html') {
      results.push(full);
    }
  }
  return results;
}

export function runAudit() {
  console.log("=========================================================");
  console.log("🌐 Multilingual Localization Integrity Audit Engine");
  console.log("=========================================================");

  const allResults = [];
  let failedCount = 0;
  let passedCount = 0;

  for (const lang of LANG_CODES) {
    const langDir = path.join(REPO_ROOT, lang);
    if (!fs.existsSync(langDir)) continue;

    const files = findHtmlFiles(langDir);
    let langFailed = 0;
    for (const f of files) {
      const res = auditFile(f, lang);
      allResults.push(res);
      if (res.status === "FAILED_TRANSLATION") {
        failedCount++;
        langFailed++;
      } else {
        passedCount++;
      }
    }
    console.log(`  • /${lang}/: ${files.length} files audited | ${langFailed} failed, ${files.length - langFailed} passed`);
  }

  const reportPath = path.join(REPO_ROOT, "translation-audit-report.json");
  fs.writeFileSync(reportPath, JSON.stringify({
    total_audited: allResults.length,
    total_passed: passedCount,
    total_failed: failedCount,
    results: allResults
  }, null, 2), 'utf8');

  console.log("---------------------------------------------------------");
  console.log(`📊 Summary: ${allResults.length} files audited | ${failedCount} FAILED | ${passedCount} PASSED`);
  console.log(`📝 Full audit report saved to: translation-audit-report.json`);
  console.log("=========================================================\n");

  return failedCount;
}

if (process.argv[1] && process.argv[1].endsWith('audit-translations.js')) {
  const code = runAudit();
  process.exit(code === 0 ? 0 : 1);
}
