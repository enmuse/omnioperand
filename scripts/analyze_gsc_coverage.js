#!/usr/bin/env node
/**
 * scripts/analyze_gsc_coverage.js
 * Pulls all queries and query+page mappings from Google Search Console,
 * checks our existing calculator inventory and HTML pages,
 * and analyzes query coverage to find missing calculators or intent gaps.
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

async function getAccessToken() {
  const jwt = createJWT(key.client_email, key.private_key, ['https://www.googleapis.com/auth/webmasters']);
  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: jwt
    }).toString()
  });
  const data = await tokenRes.json();
  if (!data.access_token) {
    throw new Error('Failed to get access token: ' + JSON.stringify(data));
  }
  return data.access_token;
}

// Find all existing HTML paths in the repository
function getAllExistingPages() {
  const pages = new Set();
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === '.wrangler') continue;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.name === 'index.html') {
        const rel = path.relative(REPO_ROOT, fullPath);
        const urlPath = '/' + rel.replace(/\/index\.html$/, '/').replace(/^index\.html$/, '');
        pages.add(urlPath);
      } else if (entry.name.endsWith('.html') && entry.name !== '404.html') {
        const rel = path.relative(REPO_ROOT, fullPath);
        pages.add('/' + rel);
      }
    }
  }
  walk(REPO_ROOT);
  return pages;
}

async function fetchGscData(accessToken, body) {
  const res = await fetch('https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent('sc-domain:omnioperand.com') + '/searchAnalytics/query', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + accessToken, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return await res.json();
}

async function main() {
  const token = await getAccessToken();
  const existingPages = getAllExistingPages();
  console.log(`Found ${existingPages.size} local pages/endpoints in repo.`);

  const today = new Date();
  const endDate = today.toISOString().split('T')[0];
  // 90 days back
  const startDate = new Date(today - 90 * 24 * 3600 * 1000).toISOString().split('T')[0];

  // 1. Fetch query + page dimensions
  console.log(`Fetching query+page data from ${startDate} to ${endDate}...`);
  const queryPageRes = await fetchGscData(token, {
    startDate,
    endDate,
    dimensions: ['query', 'page'],
    rowLimit: 25000
  });

  const queryPageRows = queryPageRes.rows || [];
  console.log(`Fetched ${queryPageRows.length} query-page combinations.`);

  // 2. Fetch all unique queries
  const queryRes = await fetchGscData(token, {
    startDate,
    endDate,
    dimensions: ['query'],
    rowLimit: 25000
  });
  const queryRows = queryRes.rows || [];
  console.log(`Fetched ${queryRows.length} unique queries.\n`);

  // Save raw data to JSON for deep analysis
  const outputPath = path.join(REPO_ROOT, 'data', 'gsc_full_report.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify({
    fetched_at: new Date().toISOString(),
    startDate,
    endDate,
    total_queries: queryRows.length,
    total_query_page_pairs: queryPageRows.length,
    queries: queryRows,
    query_pages: queryPageRows
  }, null, 2));

  console.log(`Saved full GSC raw data to ${outputPath}`);

  // Summary analysis
  console.log('\n========================================');
  console.log('ALL UNIQUE GSC QUERIES (Sorted by Impressions):');
  console.log('========================================');

  const sortedQueries = queryRows.sort((a, b) => b.impressions - a.impressions);
  for (let i = 0; i < sortedQueries.length; i++) {
    const q = sortedQueries[i];
    console.log(`${String(i + 1).padStart(3)}. [${String(q.impressions).padStart(4)} imp, ${String(q.clicks).padStart(2)} clk, pos ${q.position.toFixed(1).padStart(5)}] "${q.keys[0]}"`);
  }
}

main().catch(console.error);
