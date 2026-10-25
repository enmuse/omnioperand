#!/usr/bin/env node
/**
 * scripts/submit_gsc.js
 * Submits all canonical sitemaps (index, monolithic, domain, and localized)
 * to Google Search Console via the Webmasters API using Service Account JWT.
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const REPO_ROOT = path.resolve(__dirname, '..');
const ENV_FILE = path.join(REPO_ROOT, '.env');

// Read service account key path from .env or fallback
let keyPath = '/Users/brandonpersonal/Documents/Git/API Keys/charged-mission-148214-3ffdbf10b0bd.json';

if (fs.existsSync(ENV_FILE)) {
  const envContent = fs.readFileSync(ENV_FILE, 'utf8');
  for (const line of envContent.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('GSC_SERVICE_ACCOUNT_KEY_FILE=')) {
      keyPath = trimmed.split('=', 2)[1].replace(/^["']|["']$/g, '');
    }
  }
}

if (!fs.existsSync(keyPath)) {
  console.error(`❌ GSC Service Account key file not found at: ${keyPath}`);
  process.exit(1);
}

const key = JSON.parse(fs.readFileSync(keyPath, 'utf8'));

// Generate RS256 JWT
function createJWT(clientEmail, privateKey, scopes) {
  const header = { alg: 'RS256', typ: 'JWT' };
  const now = Math.floor(Date.now() / 1000);
  const payload = {
    iss: clientEmail,
    scope: scopes.join(' '),
    aud: 'https://oauth2.googleapis.com/token',
    exp: now + 3600,
    iat: now
  };

  const base64UrlEncode = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
  const unsignedToken = `${base64UrlEncode(header)}.${base64UrlEncode(payload)}`;

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(unsignedToken);
  sign.end();
  const signature = sign.sign(privateKey, 'base64url');
  return `${unsignedToken}.${signature}`;
}

async function getAccessToken() {
  const jwt = createJWT(key.client_email, key.private_key, ['https://www.googleapis.com/auth/webmasters']);
  const params = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion: jwt
  });

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Failed to obtain Google OAuth2 token: ${errText}`);
  }

  const data = await res.json();
  return data.access_token;
}

const SITEMAPS_TO_SUBMIT = [
  'https://omnioperand.com/sitemap-index.xml',
  'https://omnioperand.com/sitemap.xml',
  'https://omnioperand.com/sitemap-en.xml',
  'https://omnioperand.com/sitemap-engineering.xml',
  'https://omnioperand.com/sitemap-finance.xml',
  'https://omnioperand.com/sitemap-es.xml',
  'https://omnioperand.com/sitemap-fr.xml',
  'https://omnioperand.com/sitemap-de.xml',
  'https://omnioperand.com/sitemap-it.xml',
  'https://omnioperand.com/sitemap-pt.xml',
  'https://omnioperand.com/sitemap-nl.xml',
  'https://omnioperand.com/sitemap-pl.xml',
  'https://omnioperand.com/sitemap-sv.xml',
  'https://omnioperand.com/sitemap-no.xml',
  'https://omnioperand.com/sitemap-fi.xml',
  'https://omnioperand.com/sitemap-ro.xml'
];

async function main() {
  console.log('=========================================================');
  console.log('📡 Google Search Console Sitemap Submission Engine');
  console.log('=========================================================');
  console.log(`🔑 Authenticating service account: ${key.client_email}`);

  const token = await getAccessToken();
  console.log('✅ Service account authenticated with Google Search Console API.');

  // Find verified site for omnioperand.com
  const sitesRes = await fetch('https://www.googleapis.com/webmasters/v3/sites', {
    headers: { Authorization: `Bearer ${token}` }
  });
  const sitesData = await sitesRes.json();
  const entries = sitesData.siteEntry || [];

  let targetSite = null;
  for (const entry of entries) {
    if (entry.siteUrl && entry.siteUrl.includes('omnioperand.com')) {
      targetSite = entry.siteUrl;
      console.log(`📍 Found verified property: ${entry.siteUrl} (Permission: ${entry.permissionLevel})`);
      break;
    }
  }

  if (!targetSite) {
    targetSite = 'sc-domain:omnioperand.com';
    console.log(`⚠️ Defaulting to target property: ${targetSite}`);
  }

  console.log(`\n🚀 Submitting ${SITEMAPS_TO_SUBMIT.length} sitemaps to property: '${targetSite}'...`);

  let successCount = 0;
  for (const sitemapUrl of SITEMAPS_TO_SUBMIT) {
    const putUrl = `https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(targetSite)}/sitemaps/${encodeURIComponent(sitemapUrl)}`;
    try {
      const resp = await fetch(putUrl, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` }
      });

      if (resp.status === 204 || resp.ok) {
        console.log(`  ✅ Successfully submitted: ${sitemapUrl}`);
        successCount++;
      } else {
        const body = await resp.text();
        console.warn(`  ⚠️ Warning (${resp.status}) for ${sitemapUrl}: ${body}`);
      }
    } catch (err) {
      console.error(`  ❌ Failed for ${sitemapUrl}:`, err.message);
    }
  }

  console.log(`\n📊 Submission Summary: ${successCount}/${SITEMAPS_TO_SUBMIT.length} sitemaps successfully sent to GSC!`);

  // Query updated sitemaps status
  console.log(`\n🔍 Verifying registered sitemaps in Search Console for '${targetSite}'...`);
  const statusRes = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(targetSite)}/sitemaps`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (statusRes.ok) {
    const statusData = await statusRes.json();
    const sitemaps = statusData.sitemap || [];
    console.log(`Total sitemaps registered in GSC: ${sitemaps.length}`);
    for (const sm of sitemaps) {
      const path = sm.path;
      const lastSub = sm.lastSubmitted || 'N/A';
      const warnings = sm.warnings || '0';
      const errors = sm.errors || '0';
      const pending = sm.isPending ? '⏳ Pending' : '✅ Processed';
      console.log(`  • ${path} | Status: ${pending} | Submitted: ${lastSub} | Warnings: ${warnings} | Errors: ${errors}`);
    }
  }

  console.log('=========================================================\n');
}

main().catch(err => {
  console.error('Fatal GSC submission error:', err);
  process.exit(1);
});
