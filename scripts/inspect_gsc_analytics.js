#!/usr/bin/env node
/**
 * scripts/inspect_gsc_analytics.js
 * Analyzes live Google Search Console search performance data
 * to identify high-impression pages, striking-distance queries, and optimization targets.
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

async function main() {
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

  const today = new Date();
  const endDate = today.toISOString().split('T')[0];
  const startDate = new Date(today - 28 * 24 * 3600 * 1000).toISOString().split('T')[0];

  // 1. Overall stats
  const aggRes = await fetch('https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent('sc-domain:omnioperand.com') + '/searchAnalytics/query', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + access_token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ startDate, endDate })
  });
  const aggData = await aggRes.json();
  console.log('=== OVERALL GSC PERFORMANCE ===');
  if (aggData.rows && aggData.rows.length > 0) {
    const r = aggData.rows[0];
    console.log(`Total Clicks: ${r.clicks} | Total Impressions: ${r.impressions} | Average CTR: ${(r.ctr * 100).toFixed(2)}% | Average Position: ${r.position.toFixed(1)}`);
  }

  // 2. Top Pages
  const pagesRes = await fetch('https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent('sc-domain:omnioperand.com') + '/searchAnalytics/query', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + access_token, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      startDate,
      endDate,
      dimensions: ['page'],
      rowLimit: 100
    })
  });
  const pagesData = await pagesRes.json();
  const topPages = (pagesData.rows || []).sort((a, b) => b.impressions - a.impressions);
  console.log(`\n=== TOP PAGES BY IMPRESSIONS (${topPages.length} active pages) ===`);
  for (const p of topPages.slice(0, 25)) {
    console.log(`  ${String(p.impressions).padStart(4)} imp | ${p.clicks} clicks | pos ${p.position.toFixed(1).padStart(4)} | ${p.keys[0]}`);
  }

  // 3. Top Queries
  const queryRes = await fetch('https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent('sc-domain:omnioperand.com') + '/searchAnalytics/query', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + access_token, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      startDate,
      endDate,
      dimensions: ['query'],
      rowLimit: 100
    })
  });
  const queryData = await queryRes.json();
  const topQueries = (queryData.rows || []).sort((a, b) => b.impressions - a.impressions);
  console.log(`\n=== TOP QUERIES BY IMPRESSIONS (${topQueries.length} distinct queries) ===`);
  for (const q of topQueries.slice(0, 25)) {
    console.log(`  ${String(q.impressions).padStart(4)} imp | ${q.clicks} clicks | pos ${q.position.toFixed(1).padStart(4)} | ${q.keys[0]}`);
  }

  // 4. Striking distance queries (position <= 30)
  const striking = (queryData.rows || []).filter(q => q.position <= 30).sort((a, b) => a.position - b.position);
  console.log(`\n=== STRIKING DISTANCE QUERIES (Position <= 30) ===`);
  for (const s of striking) {
    console.log(`  Pos ${s.position.toFixed(1).padStart(4)} | ${String(s.impressions).padStart(3)} imp | ${s.clicks} clicks | "${s.keys[0]}"`);
  }
}

main().catch(console.error);
