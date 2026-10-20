#!/usr/bin/env python3
"""
scripts/submit_gsc.py
Submits the canonical sitemap to Google Search Console via the Webmasters API
using the service account credentials from API Keys directory.
"""

import sys
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

REPO_ROOT = Path(__file__).resolve().parent.parent

KEY_PATH = Path("/Users/brandonpersonal/Documents/Git/API Keys/charged-mission-148214-3ffdbf10b0bd.json")
SITEMAP_URL = "https://omnioperand.com/sitemap.xml"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

def submit_to_gsc():
    if not KEY_PATH.exists():
        print(f"❌ Key file not found at: {KEY_PATH}")
        return False

    print("🔑 Authenticating with Google Search Console service account...")
    credentials = service_account.Credentials.from_service_account_file(
        str(KEY_PATH), scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=credentials)

    print("📡 Querying verified sites in Search Console...")
    try:
        sites_resp = service.sites().list().execute()
        entries = sites_resp.get("siteEntry", [])
        print(f"Found {len(entries)} registered site entries in Search Console:")
        
        target_site = None
        for entry in entries:
            url = entry.get("siteUrl", "")
            perm = entry.get("permissionLevel", "")
            print(f"  • {url} (Permission: {perm})")
            if "omnioperand.com" in url:
                target_site = url

        if not target_site:
            # Try both domain and URL-prefix formats
            candidates = ["sc-domain:omnioperand.com", "https://omnioperand.com/"]
        else:
            candidates = [target_site]

        success = False
        for site in candidates:
            print(f"\n🚀 Attempting sitemap submission for site: '{site}'...")
            try:
                service.sitemaps().submit(
                    siteUrl=site,
                    feedpath=SITEMAP_URL
                ).execute()
                print(f"🎉 SUCCESS! Sitemap {SITEMAP_URL} successfully submitted to GSC for '{site}'!")
                success = True
                break
            except HttpError as e:
                err_data = json.loads(e.content.decode("utf-8")) if e.content else {}
                msg = err_data.get("error", {}).get("message", str(e))
                print(f"⚠️ GSC API Response for '{site}': {msg}")

        return success

    except HttpError as e:
        print(f"❌ Search Console API error: {e}")
        return False

if __name__ == "__main__":
    submit_to_gsc()
