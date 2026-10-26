#!/usr/bin/env node
/**
 * scripts/check_gsc_indexing.js
 * Queries Google Search Console API to report:
 * 1. Sitemaps submission & indexed counts reported by Google
 * 2. Total distinct pages actively ranking & receiving impressions in Google search results
 * 3. Recent 7-day impressions, clicks, and top indexed calculator URLs
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const ENV_FILE = path.join(REPO_ROOT, '.env');

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

const key = JSON.parse(fs.readFileSync(keyPath, 'utf8'));

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
  const b64 = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
  const unsigned = b64(header) + '.' + b64(payload);
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(unsigned);
  sign.end();
  return unsigned + '.' + sign.sign(privateKey, 'base64url');
}

async function run() {
  console.log('=========================================================');
  console.log('📊 Google Search Console Live Indexing & Coverage Audit');
  console.log('=========================================================');

  const jwt = createJWT(key.client_email, key.private_key, ['https://www.googleapis.com/auth/webmasters']);
  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: jwt
    }).toString()
  });

  const { access_token } = await tokenRes.json();
  const siteUrl = 'sc-domain:omnioperand.com';

  // 1. Check sitemaps status
  console.log('\n1️⃣ SITEMAPS COVERAGE (Reported by GSC):');
  const sitemapsRes = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/sitemaps`, {
    headers: { Authorization: 'Bearer ' + access_token }
  });
  const sitemapsData = await sitemapsRes.json();
  const sitemaps = sitemapsData.sitemap || [];
  
  let totalSubmitted = 0;
  let totalIndexed = 0;
  
  for (const s of sitemaps) {
    const contents = s.contents || [];
    for (const c of contents) {
      const sub = parseInt(c.submitted || '0', 10);
      const idx = parseInt(c.indexed || '0', 10);
      totalSubmitted += sub;
      totalIndexed += idx;
      console.log(`  • ${s.path.replace('https://omnioperand.com/', '')}: Submitted=${sub}, Indexed=${idx}`);
    }
    if (contents.length === 0) {
      console.log(`  • ${s.path.replace('https://omnioperand.com/', '')}: Pending Google processing (Last submitted: ${s.lastSubmitted || 'recently'})`);
    }
  }

  // 2. Query Search Analytics for all unique pages that have received impressions
  console.log('\n2️⃣ ACTIVELY INDEXED & SERVED PAGES (Search Performance Data):');
  // Domain launched Oct 20, 2026 (~6 days ago)
  const analyticsRes = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + access_token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      startDate: '2026-10-18',
      endDate: '2026-10-26',
      dimensions: ['page'],
      rowLimit: 5000
    })
  });

  const analyticsData = await analyticsRes.json();
  const pages = analyticsData.rows || [];
  console.log(`  Total unique pages indexed & ranking in search: ${pages.length}`);

  let totalImpressions = 0;
  let totalClicks = 0;
  pages.forEach(p => {
    totalImpressions += p.impressions;
    totalClicks += p.clicks;
  });

  console.log(`  Total Search Impressions (Past 6 Days): ${totalImpressions.toLocaleString()}`);
  console.log(`  Total Organic Clicks: ${totalClicks.toLocaleString()}`);

  console.log('\n3️⃣ TOP 20 INDEXED PAGES BY SEARCH VISIBILITY:');
  pages.slice(0, 20).forEach((p, i) => {
    const url = p.keys[0].replace('https://omnioperand.com', '');
    console.log(`  ${(i + 1).toString().padStart(2, ' ')}. ${url.padEnd(48, ' ')} | Imp: ${p.impressions.toString().padStart(4, ' ')} | Clicks: ${p.clicks} | Pos: ${p.position.toFixed(1)}`);
  });

  // Query by date to show growth trend
  const dateRes = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + access_token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      startDate: '2026-10-18',
      endDate: '2026-10-26',
      dimensions: ['date']
    })
  });
  const dateData = await dateRes.json();
  console.log('\n4️⃣ DAILY IMPRESSION TRAJECTORY (Past 7 Days):');
  (dateData.rows || []).forEach(d => {
    console.log(`  📅 ${d.keys[0]}: ${d.impressions} impressions, ${d.clicks} clicks`);
  });

  // 5. Sample URL Inspection API
  console.log('\n5️⃣ LIVE GOOGLE URL INSPECTION STATUS:');
  const sampleUrls = [
    'https://omnioperand.com/geometry/2d/shapes/octagon/',
    'https://omnioperand.com/construction/concrete-volume/',
    'https://omnioperand.com/finance/mortgage-amortization/',
    'https://omnioperand.com/agriculture/grain-bin-bushel-capacity/'
  ];

  for (const u of sampleUrls) {
    try {
      const inspectRes = await fetch('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + access_token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          inspectionUrl: u,
          siteUrl: siteUrl
        })
      });
      if (inspectRes.ok) {
        const d = await inspectRes.json();
        const res = d.inspectionResult?.indexStatusResult;
        console.log(`  🔍 ${u.replace('https://omnioperand.com', '')}`);
        console.log(`     Verdict: ${res?.verdict} | Coverage: ${res?.coverageState} | Crawled: ${res?.lastCrawlTime || 'Recently'}`);
      }
    } catch (e) {
      // Pass
    }
  }

  console.log('\n=========================================================');
}

run().catch(console.error);

