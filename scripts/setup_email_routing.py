#!/usr/bin/env python3
"""
scripts/setup_email_routing.py — Cloudflare Free Email Routing Automator for OmniOperand
Configures incoming email forwarding from:
  - contact@omnioperand.com -> brandonpassmore@gmail.com
  - partners@omnioperand.com -> brandonpassmore@gmail.com
  - catch-all (*@omnioperand.com) -> brandonpassmore@gmail.com

Cloudflare Email Routing is 100% free.
"""

import os
import sys
import json
import ssl
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"

DESTINATION_EMAIL = "brandonpassmore@gmail.com"
DOMAIN = "omnioperand.com"

def load_env():
    env = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def make_request(url, method="GET", data=None, token=""):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return None, json.loads(err_body)
        except Exception:
            return None, {"error": err_body, "status": e.code}
    except Exception as e:
        return None, {"error": str(e)}

def ensure_dns_records(zone_id, token):
    print("1. Verifying DNS MX and SPF records on omnioperand.com...")
    dns_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    res, err = make_request(dns_url, method="GET", token=token)
    if err:
        print(f"  ⚠️ Could not query DNS records: {err}")
        return False
    
    existing = res.get("result", [])
    existing_mx = [r["content"].lower() for r in existing if r["type"] == "MX"]
    existing_spf = [r["content"] for r in existing if r["type"] == "TXT" and "spf" in r["content"].lower()]

    needed_mx = [
        ("isaac.mx.cloudflare.net", 11),
        ("linda.mx.cloudflare.net", 9),
        ("amir.mx.cloudflare.net", 73)
    ]

    for server, prio in needed_mx:
        if server.lower() not in existing_mx:
            payload = {
                "type": "MX",
                "name": DOMAIN,
                "content": server,
                "priority": prio,
                "ttl": 1
            }
            res_mx, err_mx = make_request(dns_url, method="POST", data=payload, token=token)
            if not err_mx:
                print(f"  ✅ Added MX record: {server} (priority {prio})")
            else:
                print(f"  ⚠️ Could not add MX {server}: {err_mx}")
        else:
            print(f"  ✅ MX record active: {server} (priority {prio})")

    if not existing_spf:
        payload = {
            "type": "TXT",
            "name": DOMAIN,
            "content": "v=spf1 include:_spf.mx.cloudflare.net ~all",
            "ttl": 1
        }
        res_spf, err_spf = make_request(dns_url, method="POST", data=payload, token=token)
        if not err_spf:
            print("  ✅ Added SPF TXT record.")
        else:
            print(f"  ⚠️ Could not add SPF TXT record: {err_spf}")
    else:
        print("  ✅ SPF TXT record active.")
    return True

def check_destination_verification(account_id, token):
    dest_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/email/routing/addresses"
    res, err = make_request(dest_url, method="GET", token=token)
    if err:
        print(f"  ⚠️ Could not check destination addresses: {err}")
        return False
    for addr in res.get("result", []):
        if addr.get("email") == DESTINATION_EMAIL:
            verified = addr.get("verified")
            if verified:
                return True
            return False
    return False

def add_destination(account_id, token):
    dest_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/email/routing/addresses"
    res, err = make_request(dest_url, method="POST", data={"email": DESTINATION_EMAIL}, token=token)
    if err:
        if "already exists" in str(err):
            print(f"  ℹ️ {DESTINATION_EMAIL} is registered in Account.")
        else:
            print(f"  ⚠️ Destination registration notice: {err}")
    else:
        print(f"  ✅ Registered {DESTINATION_EMAIL} with Cloudflare.")

def configure_rules(zone_id, token):
    print("\n3. Creating forwarding rules for contact@, partners@, and catch-all...")
    rules_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules"
    
    # Check existing rules
    res, err = make_request(rules_url, method="GET", token=token)
    existing_rules = {}
    if res and res.get("result"):
        for r in res["result"]:
            existing_rules[r.get("name")] = r.get("id")

    rules_to_create = [
        {"name": "Forward Contact", "match": f"contact@{DOMAIN}"},
        {"name": "Forward Partners", "match": f"partners@{DOMAIN}"}
    ]
    for r in rules_to_create:
        if r["name"] in existing_rules:
            print(f"  ✅ Rule '{r['name']}' already exists.")
            continue
        payload = {
            "name": r["name"],
            "enabled": True,
            "matchers": [
                {
                    "type": "literal",
                    "field": "to",
                    "value": r["match"]
                }
            ],
            "actions": [
                {
                    "type": "forward",
                    "value": [DESTINATION_EMAIL]
                }
            ]
        }
        res_r, err_r = make_request(rules_url, method="POST", data=payload, token=token)
        if err_r:
            print(f"  ⚠️ Could not create rule for {r['match']}: {err_r}")
        else:
            print(f"  ✅ Forwarding rule created: {r['match']} -> {DESTINATION_EMAIL}")

    # Catch-all rule
    catch_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules/catch_all"
    catch_payload = {
        "name": "Catch-all Forwarding",
        "enabled": True,
        "matchers": [
            {
                "type": "all"
            }
        ],
        "actions": [
            {
                "type": "forward",
                "value": [DESTINATION_EMAIL]
            }
        ]
    }
    res_c, err_c = make_request(catch_url, method="PUT", data=catch_payload, token=token)
    if err_c:
        print(f"  ⚠️ Catch-all notice: {err_c}")
    else:
        print(f"  ✅ Catch-all rule active: *@omnioperand.com -> {DESTINATION_EMAIL}")

def main():
    print("=========================================================")
    print("📧 Cloudflare Free Email Routing Setup: OmniOperand")
    print(f"Target Destination: {DESTINATION_EMAIL}")
    print(f"Domain: {DOMAIN}")
    print("=========================================================\n")

    env = load_env()
    token = env.get("CLOUD_FLARE_API_TOKEN") or env.get("CLOUD_FLARE_PAGES_API_TOKEN")
    account_id = env.get("CLOUDFLARE_ACCOUNT_ID", "2bbe914ca4d82460c51d668407bb3dbd")
    zone_id = env.get("CLOUDFLARE_ZONE_ID", "3c5297e2d6de7e4e858fd2679201e85d")

    if not token:
        print("❌ Error: No Cloudflare API token found in .env")
        sys.exit(1)

    # 1. DNS Records
    ensure_dns_records(zone_id, token)

    # 2. Destination Address
    print(f"\n2. Verifying destination address {DESTINATION_EMAIL}...")
    add_destination(account_id, token)
    is_verified = check_destination_verification(account_id, token)
    
    if not is_verified:
        print("\n⏳ ACTION REQUIRED IN GMAIL:")
        print(f"  Cloudflare has sent a verification email to: {DESTINATION_EMAIL}")
        print("  Please open Gmail, click 'Verify email address', and then rerun this script.")
        print("  (Cloudflare will not allow forwarding rules until you verify destination ownership).")
        return False
    else:
        print(f"  ✅ Destination {DESTINATION_EMAIL} is verified and active!")

    # 3. Forwarding Rules
    configure_rules(zone_id, token)
    print("\n🎉 Email Routing setup is 100% complete!")
    return True

if __name__ == "__main__":
    main()
