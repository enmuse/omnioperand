#!/usr/bin/env node
/**
 * scripts/submit_indexnow.js
 * Submits all canonical URLs to the IndexNow protocol across search engines
 * (Bing, IndexNow.org, Yandex, Seznam) for immediate crawling.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const REPO_ROOT = path.resolve(__dirname, '..');
const ENV_FILE = path.join(REPO_ROOT, '.env');
const SITEMAP_FILE = path.join(REPO_ROOT, 'sitemap.xml');

// 1. Load IndexNow credentials from .env
let indexNowKey = '8a2f3e4b5c6d7e8f9a0b1c2d3e4f5a6b';
let host = 'omnioperand.com';
let keyLocation = `https://${host}/${indexNowKey}.txt`;

if (fs.existsSync(ENV_FILE)) {
  const envContent = fs.readFileSync(ENV_FILE, 'utf8');
  for (const line of envContent.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('INDEXNOW_KEY=')) {
      indexNowKey = trimmed.split('=', 2)[1].replace(/^["']|["']$/g, '');
    } else if (trimmed.startsWith('INDEXNOW_KEY_LOCATION=')) {
      keyLocation = trimmed.split('=', 2)[1].replace(/^["']|["']$/g, '');
    }
  }
}

// 2. Parse all <loc> URLs from sitemap.xml
if (!fs.existsSync(SITEMAP_FILE)) {
  console.error(`❌ sitemap.xml not found at: ${SITEMAP_FILE}`);
  process.exit(1);
}

const sitemapContent = fs.readFileSync(SITEMAP_FILE, 'utf8');
const urlMatches = sitemapContent.match(/<loc>(.*?)<\/loc>/g) || [];
const urls = urlMatches.map(m => m.replace(/<\/?loc>/g, '').trim());

if (urls.length === 0) {
  console.error('❌ No URLs found in sitemap.xml');
  process.exit(1);
}

const ENDPOINTS = [
  { name: 'IndexNow Global (api.indexnow.org)', url: 'https://api.indexnow.org/indexnow' },
  { name: 'Microsoft Bing (www.bing.com)', url: 'https://www.bing.com/indexnow' },
  { name: 'Yandex (yandex.com)', url: 'https://yandex.com/indexnow' },
  { name: 'Seznam (search.seznam.cz)', url: 'https://search.seznam.cz/indexnow' }
];

async function submitToIndexNow() {
  console.log('=========================================================');
  console.log('⚡ IndexNow Multi-Engine Instant Push Engine');
  console.log('=========================================================');
  console.log(`📦 Loaded ${urls.length} URLs from sitemap.xml`);
  console.log(`🔑 IndexNow Key: ${indexNowKey}`);
  console.log(`📍 Key Location: ${keyLocation}`);
  console.log(`🌐 Host: ${host}\n`);

  const payload = {
    host: host,
    key: indexNowKey,
    keyLocation: keyLocation,
    urlList: urls
  };

  const bodyData = JSON.stringify(payload);

  for (const endpoint of ENDPOINTS) {
    console.log(`🚀 Dispatching ${urls.length} URLs to ${endpoint.name}...`);
    try {
      const resp = await fetch(endpoint.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'User-Agent': 'OmniOperand-IndexNow/2.0'
        },
        body: bodyData
      });

      const text = await resp.text();
      if (resp.status === 200 || resp.status === 202) {
        console.log(`  🎉 SUCCESS! [HTTP ${resp.status}] Accepted by ${endpoint.name}`);
        if (text) {
          console.log(`     Response: ${text.trim()}`);
        }
      } else {
        console.warn(`  ⚠️ Response [HTTP ${resp.status}] from ${endpoint.name}: ${text.trim()}`);
      }
    } catch (err) {
      console.error(`  ❌ Failed dispatching to ${endpoint.name}:`, err.message);
    }
  }

  console.log('\n=========================================================');
  console.log('✨ IndexNow dispatch batch completed across search engines!');
  console.log('=========================================================\n');
}

submitToIndexNow().catch(err => {
  console.error('Fatal IndexNow error:', err);
  process.exit(1);
});
