#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def inspect_details(url):
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")
    
    api_key = os.environ.get("PAGESPEED_API_KEY", "")
    api_url = f"https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url={urllib.parse.quote(url)}&strategy=mobile&category=accessibility&category=seo&key={api_key}"
    
    req = urllib.request.Request(api_url, headers={"User-Agent": "OmniOperand-PageSpeed-Check/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
        audits = data.get("lighthouseResult", {}).get("audits", {})

        for aid in ["color-contrast", "heading-order", "label-content-name-mismatch", "robots-txt"]:
            audit = audits.get(aid, {})
            print(f"=== Audit: {aid} (Score: {audit.get('score')}) ===")
            details = audit.get("details", {})
            for item in details.get("items", []):
                print("   Node:", item.get("node", {}).get("snippet"))
                print("   Explanation:", item.get("node", {}).get("explanation") or item.get("subItems", {}))
                if aid == "robots-txt":
                    print("   Line:", item.get("lineNumber"), "Rule:", item.get("rule"), "Error:", item.get("error"))

if __name__ == "__main__":
    inspect_details("https://omnioperand.com/geometry/2d/shapes/octagon/")
