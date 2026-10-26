#!/usr/bin/env python3
"""
scripts/apply_email_rules.py
Verifies if omnioperand@gmail.com is verified, then sets up:
1. brandon@omnioperand.com -> omnioperand@gmail.com (Priority 1)
2. contact@omnioperand.com -> omnioperand@gmail.com (Priority 2)
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
    target_email = "omnioperand@gmail.com"
    print(f"Checking verification status of {target_email} in account {ACCOUNT_ID}...")
    
    dest_resp = cf_api(f"/accounts/{ACCOUNT_ID}/email/routing/addresses")
    destinations = dest_resp.get("result", [])
    target_rec = next((d for d in destinations if d.get("email") == target_email), None)
    
    if not target_rec:
        print(f"❌ Destination address {target_email} not found in Cloudflare account!")
        print("Adding it now...")
        add_resp = cf_api(f"/accounts/{ACCOUNT_ID}/email/routing/addresses", method="POST", data={"email": target_email})
        print(f"Result: {add_resp}")
        print("Please check omnioperand@gmail.com and click the verification link.")
        return False

    is_verified = bool(target_rec.get("verified"))
    print(f"Destination Address: {target_email}")
    print(f"Verified: {is_verified} (Timestamp: {target_rec.get('verified')})")
    
    if not is_verified:
        print("\n⏳ ACTION REQUIRED:")
        print(f"  The verification email has been sent by Cloudflare to '{target_email}'.")
        print("  1. Log into your omnioperand@gmail.com inbox.")
        print("  2. Open the email from Cloudflare and click the authorization link.")
        print("  3. Run this script again: python3 scripts/apply_email_rules.py")
        return False

    print("\n✅ Destination address is verified! Configuring custom routing rules...")
    rules_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules")
    existing_rules = rules_resp.get("result", [])

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
            print(f"Updating existing rule for {alias} (ID: {rule_id})...")
            up_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules/{rule_id}", method="PUT", data=rule_body)
            if up_resp.get("success"):
                print(f"  ✅ Updated rule '{rule_name}' for {alias} -> {target_email}")
            else:
                print(f"  ❌ Failed to update rule: {up_resp.get('errors')}")
        else:
            print(f"Creating new rule for {alias} -> {target_email}...")
            create_resp = cf_api(f"/zones/{ZONE_ID}/email/routing/rules", method="POST", data=rule_body)
            if create_resp.get("success"):
                print(f"  ✅ Created rule '{rule_name}' for {alias} -> {target_email}")
            else:
                print(f"  ❌ Failed to create rule: {create_resp.get('errors')}")

    print("\n🎉 Custom routing rules successfully applied!")
    return True

if __name__ == "__main__":
    main()
