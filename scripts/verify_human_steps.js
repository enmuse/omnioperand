import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const envFile = path.join(REPO_ROOT, '.env');
const env = {};
if (fs.existsSync(envFile)) {
  const content = fs.readFileSync(envFile, 'utf8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
      const idx = trimmed.indexOf('=');
      const k = trimmed.slice(0, idx).trim();
      const v = trimmed.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
      env[k] = v;
    }
  }
}

async function verifyStripe() {
  console.log('\n========================================');
  console.log('1. VERIFYING STRIPE API KEY & ACCOUNT');
  console.log('========================================');
  const stripeKey = env.STRIPE_SECRET_KEY;
  if (!stripeKey) {
    console.log('❌ STRIPE_SECRET_KEY is missing from .env');
    return;
  }
  const maskedKey = stripeKey.slice(0, 8) + '...' + stripeKey.slice(-4);
  console.log(`Stripe Key Present: ${maskedKey}`);
  console.log(`Key Type: ${stripeKey.startsWith('rk_live') ? 'Live Restricted Key' : stripeKey.startsWith('sk_live') ? 'Live Secret Key' : 'Test Key'}`);

  try {
    const accRes = await fetch('https://api.stripe.com/v1/account', {
      headers: { Authorization: `Bearer ${stripeKey}` }
    });
    const accData = await accRes.json();
    if (accRes.ok) {
      console.log('✅ Account Connected:');
      console.log(`   - ID: ${accData.id}`);
      console.log(`   - Business Name: ${accData.business_profile?.name || 'N/A'}`);
      console.log(`   - Statement Descriptor: ${accData.settings?.payments?.statement_descriptor || accData.business_profile?.statement_descriptor || 'N/A'}`);
      console.log(`   - Support Email: ${accData.business_profile?.support_email || 'N/A'}`);
      console.log(`   - Payouts Enabled: ${accData.payouts_enabled}`);
      console.log(`   - Charges Enabled: ${accData.charges_enabled}`);
    } else {
      console.log(`⚠️ Note on Account Read: ${accData.error?.message}`);
    }

    const prodRes = await fetch('https://api.stripe.com/v1/products?limit=10', {
      headers: { Authorization: `Bearer ${stripeKey}` }
    });
    const prodData = await prodRes.json();
    if (prodRes.ok) {
      console.log(`✅ Products Accessible (${prodData.data.length} found):`);
      for (const p of prodData.data) {
        console.log(`   - Product: "${p.name}" (ID: ${p.id}, Active: ${p.active})`);
      }
    } else {
      console.log(`❌ Products Read Error: ${prodData.error?.message}`);
    }

    const priceRes = await fetch('https://api.stripe.com/v1/prices?limit=10', {
      headers: { Authorization: `Bearer ${stripeKey}` }
    });
    const priceData = await priceRes.json();
    if (priceRes.ok) {
      console.log(`✅ Prices Configured (${priceData.data.length} found):`);
      for (const pr of priceData.data) {
        const amt = pr.unit_amount ? `$${(pr.unit_amount / 100).toFixed(2)}` : 'Custom';
        const interval = pr.recurring ? `/${pr.recurring.interval}` : '';
        console.log(`   - Price: ${amt}${interval} (ID: ${pr.id}, Product: ${pr.product}, Active: ${pr.active})`);
      }
    }
  } catch (err) {
    console.log(`❌ Stripe API connection failed: ${err.message}`);
  }
}

async function verifyCloudflareEmail() {
  console.log('\n========================================');
  console.log('2. VERIFYING CLOUDFLARE EMAIL ROUTING');
  console.log('========================================');
  const token = env.CLOUD_FLARE_API_TOKEN || env.CLOUD_FLARE_PAGES_API_TOKEN;
  const accountId = env.CLOUDFLARE_ACCOUNT_ID || '2bbe914ca4d82460c51d668407bb3dbd';
  const zoneId = env.CLOUDFLARE_ZONE_ID || '3c5297e2d6de7e4e858fd2679201e85d';

  if (!token) {
    console.log('❌ Cloudflare API token missing from .env');
    return;
  }

  const headers = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json'
  };

  try {
    // 1. Check destination addresses
    const destRes = await fetch(`https://api.cloudflare.com/client/v4/accounts/${accountId}/email/routing/addresses`, { headers });
    const destData = await destRes.json();
    console.log('Cloudflare Account Destination Addresses:');
    if (destData.result) {
      for (const d of destData.result) {
        console.log(`   - Email: ${d.email} | Verified: ${d.verified ? '✅ YES (' + d.verified + ')' : '❌ NO'}`);
      }
    } else {
      console.log('   Error reading destinations:', destData.errors);
    }

    // 2. Check zone email routing settings
    const zoneEmailRes = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/email/routing`, { headers });
    const zoneEmailData = await zoneEmailRes.json();
    if (zoneEmailData.result) {
      console.log(`Zone Email Routing Enabled: ${zoneEmailData.result.enabled ? '✅ YES' : '❌ NO'} (Status: ${zoneEmailData.result.status})`);
    }

    // 3. Check zone email routing rules
    const rulesRes = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/email/routing/rules`, { headers });
    const rulesData = await rulesRes.json();
    console.log('Zone Email Routing Custom Rules:');
    if (rulesData.result) {
      for (const r of rulesData.result) {
        const matchStr = r.matchers?.map(m => `${m.field}=${m.value}`).join(', ');
        const actionStr = r.actions?.map(a => `${a.type} -> ${a.value?.join?.(',') || a.value}`).join(', ');
        console.log(`   - Rule: "${r.name}" | Active: ${r.enabled ? '✅' : '❌'} | Match: [${matchStr}] | Action: [${actionStr}]`);
      }
    } else {
      console.log('   Error reading rules:', rulesData.errors);
    }

    // 4. Check DNS MX and SPF records
    const dnsRes = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/dns_records?type=MX`, { headers });
    const dnsData = await dnsRes.json();
    console.log('DNS MX Records:');
    if (dnsData.result) {
      for (const rec of dnsData.result) {
        console.log(`   - MX: ${rec.content} (Priority: ${rec.priority})`);
      }
    }

    const txtRes = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/dns_records?type=TXT`, { headers });
    const txtData = await txtRes.json();
    console.log('DNS SPF & DMARC Records:');
    if (txtData.result) {
      for (const rec of txtData.result) {
        if (rec.content.includes('spf') || rec.name.startsWith('_dmarc')) {
          console.log(`   - TXT (${rec.name}): ${rec.content}`);
        }
      }
    }
  } catch (err) {
    console.log(`❌ Cloudflare API verification failed: ${err.message}`);
  }
}

async function verifyLeadWebhook() {
  console.log('\n========================================');
  console.log('3. VERIFYING LEAD PIPELINE & WEBHOOK');
  console.log('========================================');
  const webhookUrl = env.LEAD_WEBHOOK_URL;
  console.log(`Lead Webhook URL: ${webhookUrl ? webhookUrl.slice(0, 30) + '...' : 'EMPTY'}`);
  console.log(`Google Sheet URL: ${env.LEADS_GOOGLE_SHEET_URL ? 'Configured ✅' : 'EMPTY'}`);
  console.log(`Google Sheet ID: ${env.LEADS_GOOGLE_SHEET_ID ? env.LEADS_GOOGLE_SHEET_ID : 'EMPTY'}`);
}

async function run() {
  await verifyStripe();
  await verifyCloudflareEmail();
  await verifyLeadWebhook();
  console.log('\n========================================');
  console.log('VERIFICATION COMPLETE');
  console.log('========================================\n');
}

run();
