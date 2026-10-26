#!/usr/bin/env python3
"""
scripts/setup_email_routing.py
Automates Cloudflare Email Routing, SPF, DMARC, and MX records for omnioperand.com.
Target destination: omnioperand@gmail.com
Inbound aliases: brandon@omnioperand.com, contact@omnioperand.com
Outbound authorization: Cloudflare + Google SMTP (include:_spf.google.com)
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"

def load_env():
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

env = load_env()
TOKEN = env.get("CLOUD_FLARE_API_TOKEN") or env.get("CLOUD_FLARE_PAGES_API_TOKEN")
ACCOUNT_ID = env.get("CLOUDFLARE_ACCOUNT_ID", "2bbe914ca4d82460c51d668407bb3dbd")
ZONE_ID = env.get("CLOUDFLARE_ZONE_ID", "3c5297e2d6de7e4e858fd2679201e85d")

if not TOKEN:
    print("❌ Error: No Cloudflare API token found in .env")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def cf_api(endpoint, method="GET", data=None):
    url = f"https://api.cloudflare.com/client/v4{endpoint}"
    req_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            return json.loads(error_body)
        except Exception:
            return {"success": False, "status_code": e.code, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=========================================================")
    print("📧 Cloudflare Email Routing & Outbound SMTP Infrastructure")
    print("=========================================================\n")

    # Step A: Verify Zone
    print(f"Step A: Verifying Zone (ID: {ZONE_ID})...")
    zone_resp = cf_api(f"/zones/{ZONE_ID}")
    if not zone_resp.get("success"):
        print(f"❌ Failed to query zone: {zone_resp}")
        sys.exit(1)
    zone_name = zone_resp["result"]["name"]
    print(f"  ✅ Confirmed Zone: {zone_name} (Status: {zone_resp['result']['status']})")

    # Step B1: Destination Address (omnioperand@gmail.com)
    # Cloudflare accounts endpoint: /accounts/{account_id}/email/routing/addresses
    # or zone endpoint: /zones/{zone_id}/email/routing/destination_addresses
    print("\nStep B1: Checking Destination Addresses...")
    dest_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/destination_addresses")
    if not dest_resp.get("success"):
        # Try accounts endpoint
        print(f"  Trying account-level destination endpoint: /accounts/{ACCOUNT_ID}/email/routing/addresses")
        dest_resp = cf_api(f"/accounts/{ACCOUNT_ID}/email/routing/addresses")
        dest_endpoint = f"/accounts/{ACCOUNT_ID}/email/routing/addresses"
    else:
        dest_endpoint = f"/zones/{ZONE_ID}/email/routing/destination_addresses"

    destinations = dest_resp.get("result", [])
    print(f"  Existing destination addresses: {len(destinations)}")
    for d in destinations:
        print(f"    - {d.get('email')} (Verified: {d.get('verified', False)})")

    target_email = "omnioperand@gmail.com"
    existing_target = next((d for d in destinations if d.get("email") == target_email), None)

    if not existing_target:
        print(f"  Adding destination address {target_email}...")
        add_dest_resp = cf_api(dest_endpoint, method="POST", data={"email": target_email})
        print(f"  Response: {add_dest_resp}")
        if add_dest_resp.get("success"):
            print(f"  ✅ Added {target_email}. Verification email triggered!")
        else:
            print(f"  ⚠️ Could not add {target_email}: {add_dest_resp.get('errors')}")
    else:
        print(f"  ℹ️ {target_email} is already registered. (Verified: {existing_target.get('verified')})")

    # Step B2: Enable Email Routing on Zone
    print("\nStep B2: Checking Email Routing Status on Zone...")
    status_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/enabled")
    if status_resp.get("success") and status_resp.get("result", {}).get("enabled"):
        print(f"  ✅ Email routing is already ENABLED on {zone_name}.")
    else:
        print("  Enabling email routing on zone...")
        enable_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/enable", method="POST")
        print(f"  Result: {enable_resp.get('success', False)}")

    # Step B3: Routing Rules
    print("\nStep B3: Inspecting & Configuring Custom Routing Rules...")
    rules_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules")
    existing_rules = rules_resp.get("result", [])
    print(f"  Found {len(existing_rules)} existing rules:")
    for r in existing_rules:
        name = r.get("name")
        matchers = r.get("matchers", [])
        actions = r.get("actions", [])
        print(f"    Rule [{r.get('id')}]: '{name}' | Matchers: {matchers} | Actions: {actions} | Enabled: {r.get('enabled')}")

    rules_to_ensure = [
        {
            "name": "Forward Brandon to Gmail",
            "alias": "brandon@omnioperand.com",
            "priority": 1
        },
        {
            "name": "Forward Contact to Gmail",
            "alias": "contact@omnioperand.com",
            "priority": 2
        }
    ]

    for req_rule in rules_to_ensure:
        alias = req_rule["alias"]
        rule_name = req_rule["name"]
        prio = req_rule["priority"]

        # Check if a rule for this alias exists
        rule_match = None
        for r in existing_rules:
            for m in r.get("matchers", []):
                if m.get("field") == "to" and m.get("value") == alias:
                    rule_match = r
                    break
            if rule_match:
                break

        rule_body = {
            "name": rule_name,
            "enabled": True,
            "priority": prio,
            "matchers": [{"type": "literal", "field": "to", "value": alias}],
            "actions": [{"type": "forward", "value": [target_email]}]
        }

        if rule_match:
            rule_id = rule_match["id"]
            print(f"  Updating existing rule for {alias} (Rule ID: {rule_id}) to point to {target_email}...")
            up_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules/{rule_id}", method="PUT", data=rule_body)
            if up_resp.get("success"):
                print(f"  ✅ Updated rule for {alias} -> {target_email}")
            else:
                print(f"  ⚠️ Update failed: {up_resp.get('errors')}")
        else:
            print(f"  Creating new routing rule for {alias} -> {target_email}...")
            create_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules", method="POST", data=rule_body)
            if create_resp.get("success"):
                print(f"  ✅ Created rule '{rule_name}' for {alias} -> {target_email}")
            else:
                print(f"  ⚠️ Creation failed: {create_resp.get('errors')}")

    # Step C: DNS Records (MX, SPF, DMARC)
    print("\nStep C: Checking & Configuring DNS Records...")
    dns_resp = cf_api(f"/zones/{ZONE_ID}/dns_records?per_page=100")
    if not dns_resp.get("success"):
        print(f"❌ Failed to fetch DNS records: {dns_resp}")
        return

    dns_records = dns_resp.get("result", [])
    print(f"  Loaded {len(dns_records)} DNS records.")

    # 1. MX Records for Email Routing
    expected_mx = [
        {"content": "route1.mx.cloudflare.net", "priority": 92},
        {"content": "route2.mx.cloudflare.net", "priority": 55},
        {"content": "route3.mx.cloudflare.net", "priority": 39}
    ]

    current_mx = [r for r in dns_records if r.get("type") == "MX" and r.get("name") in ["omnioperand.com", "@"]]
    print(f"  Existing MX records ({len(current_mx)}):")
    for mx in current_mx:
        print(f"    - {mx.get('content')} (Priority: {mx.get('priority')}) [ID: {mx.get('id')}]")

    # If old or incorrect MX records exist that aren't the expected route*.mx.cloudflare.net, replace or clean them
    expected_hosts = {e["content"]: e["priority"] for e in expected_mx}
    for mx in current_mx:
        content = mx.get("content")
        prio = mx.get("priority")
        if content in expected_hosts:
            if prio != expected_hosts[content]:
                print(f"  Updating priority for {content} from {prio} to {expected_hosts[content]}...")
                cf_api(f"/zones/{ZONE_ID}/dns_records/{mx['id']}", method="PATCH", data={"priority": expected_hosts[content]})
            del expected_hosts[content]
        else:
            print(f"  ℹ️ Found non-standard or legacy MX record: {content} (Priority {prio})")

    for host, prio in expected_hosts.items():
        print(f"  Creating missing MX record: {host} (Priority {prio})...")
        rec_data = {
            "type": "MX",
            "name": "@",
            "content": host,
            "priority": prio,
            "ttl": 1
        }
        res = cf_api(f"/zones/{ZONE_ID}/dns_records", method="POST", data=rec_data)
        if res.get("success"):
            print(f"  ✅ Created MX record: {host}")
        else:
            print(f"  ⚠️ Error creating MX record: {res.get('errors')}")

    # 2. SPF Record (Allow Cloudflare + Google SMTP)
    target_spf = "v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all"
    current_spf = [r for r in dns_records if r.get("type") == "TXT" and "v=spf1" in r.get("content", "")]

    if current_spf:
        for spf_rec in current_spf:
            rec_id = spf_rec["id"]
            rec_content = spf_rec["content"]
            if rec_content == target_spf:
                print(f"  ✅ SPF record is already optimal: \"{rec_content}\"")
            else:
                print(f"  Updating SPF record from \"{rec_content}\" to \"{target_spf}\"...")
                up_res = cf_api(f"/zones/{ZONE_ID}/dns_records/{rec_id}", method="PUT", data={
                    "type": "TXT",
                    "name": "@",
                    "content": target_spf,
                    "ttl": 1
                })
                if up_res.get("success"):
                    print(f"  ✅ Successfully updated SPF record!")
                else:
                    print(f"  ⚠️ SPF update error: {up_res.get('errors')}")
    else:
        print(f"  Creating SPF record: \"{target_spf}\"...")
        res = cf_api(f"/zones/{ZONE_ID}/dns_records", method="POST", data={
            "type": "TXT",
            "name": "@",
            "content": target_spf,
            "ttl": 1
        })
        if res.get("success"):
            print(f"  ✅ Created SPF record successfully!")
        else:
            print(f"  ⚠️ SPF creation error: {res.get('errors')}")

    # 3. DMARC Record
    target_dmarc = "v=DMARC1; p=none; sp=none; aspf=r;"
    current_dmarc = [r for r in dns_records if r.get("type") == "TXT" and r.get("name", "").startswith("_dmarc")]

    if current_dmarc:
        for dmarc_rec in current_dmarc:
            rec_id = dmarc_rec["id"]
            rec_content = dmarc_rec["content"]
            print(f"  Existing DMARC record found: \"{rec_content}\"")
            if rec_content != target_dmarc:
                print(f"  Updating DMARC record to \"{target_dmarc}\"...")
                up_res = cf_api(f"/zones/{ZONE_ID}/dns_records/{rec_id}", method="PUT", data={
                    "type": "TXT",
                    "name": "_dmarc",
                    "content": target_dmarc,
                    "ttl": 1
                })
                if up_res.get("success"):
                    print(f"  ✅ Successfully updated DMARC record!")
                else:
                    print(f"  ⚠️ DMARC update error: {up_res.get('errors')}")
            else:
                print("  ✅ DMARC record is already exact match.")
    else:
        print(f"  Creating DMARC record for _dmarc: \"{target_dmarc}\"...")
        res = cf_api(f"/zones/{ZONE_ID}/dns_records", method="POST", data={
            "type": "TXT",
            "name": "_dmarc",
            "content": target_dmarc,
            "ttl": 1
        })
        if res.get("success"):
            print(f"  ✅ Created DMARC record successfully!")
        else:
            print(f"  ⚠️ DMARC creation error: {res.get('errors')}")

    print("\n=========================================================")
    print("🎉 Cloudflare Email Routing & DNS Automation Complete!")
    print("=========================================================")

if __name__ == "__main__":
    main()
