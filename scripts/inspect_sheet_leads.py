#!/usr/bin/env python3
"""
scripts/inspect_sheet_leads.py — OmniOperand Live Leads Inspection Tool

Inspects incoming leads from:
1. Google Sheets (via LEADS_GOOGLE_SHEET_ID)
2. Local backup queue (data/leads/pending-leads.json)

Usage:
  python3 scripts/inspect_sheet_leads.py
"""

import os
import sys
import json
import urllib.request
import csv
import io
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"
LOCAL_LEADS_FILE = REPO_ROOT / "data" / "leads" / "pending-leads.json"

# Load environment
sheet_url = None
sheet_id = None
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("LEADS_GOOGLE_SHEET_URL="):
                sheet_url = line.split("=", 1)[1].strip('"\'')
            elif line.startswith("LEADS_GOOGLE_SHEET_ID="):
                sheet_id = line.split("=", 1)[1].strip('"\'')

def check_google_sheet(sid):
    if not sid:
        return None, "No LEADS_GOOGLE_SHEET_ID in .env"
    
    export_url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    try:
        import ssl
        ctx = ssl.create_default_context()
        try:
            import certifi
            ctx.load_verify_locations(certifi.where())
        except Exception:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(export_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = resp.read().decode("utf-8")
            reader = csv.reader(io.StringIO(data))
            rows = list(reader)
            return rows, None
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return None, "Google Sheet is private. To allow automated CLI checks, set General Access in the sheet to 'Anyone with the link: Viewer'."
        return None, f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return None, str(e)

def inspect_local_leads():
    if not LOCAL_LEADS_FILE.exists():
        return []
    try:
        with open(LOCAL_LEADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def main():
    print("=========================================================")
    print("📋 OmniOperand Live Leads Inspection Engine")
    print("=========================================================\n")
    
    print(f"🔗 Google Sheet: {sheet_url or 'Not Configured'}")
    
    rows, err = check_google_sheet(sheet_id)
    if err:
        print(f"⚠️  Google Sheet Status: {err}\n")
    else:
        print(f"✅ Google Sheet Status: Accessible")
        if len(rows) <= 1:
            print("   Rows recorded: 0 leads (sheet is initialized or has headers only)\n")
        else:
            headers = rows[0]
            leads = rows[1:]
            print(f"   Total Recorded Leads in Sheet: {len(leads)}\n")
            print("   Recent 5 Leads in Google Sheet:")
            for idx, r in enumerate(leads[-5:], 1):
                print(f"   [{idx}] " + " | ".join(r[:6]))
            print()

    local = inspect_local_leads()
    print(f"💾 Local Backup Leads: {len(local)} leads recorded in {LOCAL_LEADS_FILE.name}")
    if local:
        for idx, l in enumerate(local[-3:], 1):
            print(f"   [{idx}] {l.get('timestamp')} - {l.get('full_name')} ({l.get('property_value')}, {l.get('state_zip')})")
    
    print("\n=========================================================")

if __name__ == "__main__":
    main()
