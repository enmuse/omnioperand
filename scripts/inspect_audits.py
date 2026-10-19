#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_env():
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

def inspect_audits(url, strategy="mobile"):
    load_env()
    api_key = os.environ.get("PAGESPEED_API_KEY", "")
    query_parts = [
        f"url={urllib.parse.quote(url)}",
        f"strategy={strategy}",
        "category=performance",
        "category=accessibility",
        "category=best-practices",
        "category=seo"
    ]
    if api_key:
        query_parts.append(f"key={api_key}")

    api_url = f"https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?{'&'.join(query_parts)}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "OmniOperand-PageSpeed-Check/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
        audits = data.get("lighthouseResult", {}).get("audits", {})
        categories = data.get("lighthouseResult", {}).get("categories", {})

        print(f"=== {url} ({strategy}) ===")
        for cat_name, cat in categories.items():
            print(f"Category: {cat_name.upper()} = {int(cat.get('score', 0) * 100)}")
            for audit_ref in cat.get("auditRefs", []):
                audit_id = audit_ref.get("id")
                audit = audits.get(audit_id, {})
                score = audit.get("score")
                if score is not None and score < 1.0:
                    title = audit.get("title")
                    display = audit.get("displayValue", "")
                    weight = audit_ref.get("weight")
                    print(f"   ❌ [{cat_name}] {audit_id} (weight {weight}): {title} -> {display}")

if __name__ == "__main__":
    inspect_audits("https://omnioperand.com/geometry/2d/shapes/octagon/", "mobile")
