#!/usr/bin/env python3
"""
scripts/check_pagespeed.py — Query Google PageSpeed Insights API for Mobile & Desktop Lighthouse scores
"""

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

def check_pagespeed(url, strategy="mobile"):
    api_key = os.environ.get("PAGESPEED_API_KEY", "")
    params = {
        "url": url,
        "strategy": strategy,
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }
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
    
    print(f"📡 Querying Google PageSpeed ({strategy.upper()}) for: {url} ...")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "OmniOperand-PageSpeed-Check/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            categories = data.get("lighthouseResult", {}).get("categories", {})
            perf = int(categories.get("performance", {}).get("score", 0) * 100)
            a11y = int(categories.get("accessibility", {}).get("score", 0) * 100)
            bp = int(categories.get("best-practices", {}).get("score", 0) * 100)
            seo = int(categories.get("seo", {}).get("score", 0) * 100)

            audits = data.get("lighthouseResult", {}).get("audits", {})
            fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")
            lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
            tbt = audits.get("total-blocking-time", {}).get("displayValue", "N/A")
            cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
            speed_index = audits.get("speed-index", {}).get("displayValue", "N/A")

            # Collect opportunities/diagnostics if score < 100
            issues = []
            for audit_key in ["render-blocking-resources", "unused-css-rules", "unused-javascript", "modern-image-formats", "uses-responsive-images"]:
                audit = audits.get(audit_key)
                if audit and audit.get("score") is not None and audit.get("score") < 1.0:
                    title = audit.get("title")
                    savings = audit.get("displayValue", "")
                    issues.append(f"{title}: {savings}")

            return {
                "url": url,
                "strategy": strategy,
                "performance": perf,
                "accessibility": a11y,
                "best_practices": bp,
                "seo": seo,
                "fcp": fcp,
                "lcp": lcp,
                "tbt": tbt,
                "cls": cls,
                "speed_index": speed_index,
                "issues": issues
            }
    except Exception as e:
        print(f"❌ Error querying PageSpeed API: {e}")
        return None

def main():
    load_env()
    urls_to_test = [
        "https://omnioperand.com/",
        "https://omnioperand.com/geometry/2d/shapes/octagon/"
    ]
    
    results = []
    for u in urls_to_test:
        for st in ["desktop", "mobile"]:
            res = check_pagespeed(u, st)
            if res:
                results.append(res)
                print(f"   📊 Scores ({st.upper()}): Perf: {res['performance']}/100 | A11y: {res['accessibility']}/100 | Best Practices: {res['best_practices']}/100 | SEO: {res['seo']}/100")
                print(f"   ⚡ Web Vitals: FCP={res['fcp']}, LCP={res['lcp']}, TBT={res['tbt']}, CLS={res['cls']}")
                if res['issues']:
                    print(f"   ⚠️ Opportunities: {', '.join(res['issues'])}")
            print()

    print("=========================================================")
    print("PAGE SPEED SUMMARY:")
    for r in results:
        badge = "🟢 100/100" if r['performance'] == 100 else f"🟡 {r['performance']}/100"
        print(f"{badge} | {r['strategy'].upper():<7} | Perf: {r['performance']}/100 | A11y: {r['accessibility']}/100 | SEO: {r['seo']}/100 | {r['url']}")
    print("=========================================================")

if __name__ == "__main__":
    main()
