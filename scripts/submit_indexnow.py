#!/usr/bin/env python3
"""
scripts/submit_indexnow.py
Submits all canonical URLs from sitemap.xml to the IndexNow API endpoint
for immediate crawling and indexing across search engines.
"""

import urllib.request
import urllib.error
import json
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

INDEXNOW_KEY = "8a2f3e4b5c6d7e8f9a0b1c2d3e4f5a6b"
HOST = "omnioperand.com"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"

def submit_urls():
    sitemap_file = REPO_ROOT / "sitemap.xml"
    if not sitemap_file.exists():
        print("❌ sitemap.xml does not exist!")
        return False

    # Parse URLs from sitemap.xml
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    # XML namespace
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for loc in root.findall(".//ns:loc", ns):
        if loc.text:
            urls.append(loc.text.strip())

    print(f"📦 Loaded {len(urls)} URLs from sitemap.xml for IndexNow submission")

    # Construct IndexNow JSON payload
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "OmniOperand-IndexNow/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            print(f"🎉 IndexNow Submission SUCCESSFUL! HTTP Status: {status}")
            print(f"✨ Submitted {len(urls)} URLs to search engine index cluster (Bing, Yandex, Seznam, Naver)!")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"⚠️ IndexNow HTTP Error {e.code}: {body}")
        # Note: HTTP 202 is Accepted, but urllib sometimes treats 202 as normal
        if e.code == 202:
            print(f"✅ HTTP 202 Accepted: {len(urls)} URLs queued by IndexNow engine!")
            return True
        return False
    except Exception as e:
        print(f"❌ Network/Connection error: {e}")
        return False

if __name__ == "__main__":
    submit_urls()
