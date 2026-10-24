#!/usr/bin/env python3
"""
scripts/export_pending_leads.py — Inspect & Export Backup Leads from OmniOperand

Usage:
  python3 scripts/export_pending_leads.py          # Displays summary and recent leads
  python3 scripts/export_pending_leads.py --csv    # Exports leads to data/leads/exported-leads.csv
"""

import sys
import json
import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEADS_FILE = REPO_ROOT / "data" / "leads" / "pending-leads.json"
CSV_FILE = REPO_ROOT / "data" / "leads" / "exported-leads.csv"

def inspect_leads(export_csv=False):
    if not LEADS_FILE.exists():
        print(f"No leads file found at: {LEADS_FILE}")
        return 0

    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error reading {LEADS_FILE}: {e}")
        return 1

    print("=========================================================")
    print("📋 OmniOperand Pending Leads Inspection Engine")
    print(f"Total Captured Leads: {len(leads)}")
    print(f"Backup Source: {LEADS_FILE}")
    print("=========================================================\n")

    if not leads:
        print("No pending leads currently in local storage.")
        return 0

    # Display recent 10 leads
    for idx, lead in enumerate(leads[-10:], 1):
        print(f"[{idx}] {lead.get('timestamp', 'N/A')}")
        print(f"    Lead ID:   {lead.get('lead_id', 'N/A')}")
        print(f"    Name:      {lead.get('full_name', 'N/A')}")
        print(f"    Email:     {lead.get('email', 'N/A')}")
        print(f"    Phone:     {lead.get('phone', 'N/A')}")
        print(f"    State/Zip: {lead.get('state_zip', 'N/A')}")
        print(f"    Vertical:  {lead.get('vertical', 'N/A')} ({lead.get('financing_model', 'N/A')})")
        print(f"    Property:  {lead.get('property_value', 'N/A')} (Down: {lead.get('down_payment', 'N/A')})")
        print(f"    Credit:    {lead.get('credit_tier', 'N/A')}")
        print("-" * 55)

    if export_csv:
        fieldnames = [
            "lead_id", "timestamp", "vertical", "financing_model",
            "full_name", "email", "phone", "state_zip",
            "credit_tier", "property_use", "property_value",
            "down_payment", "monthly_budget", "tcpa_consent", "source_url"
        ]
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for lead in leads:
                writer.writerow(lead)
        print(f"\n✅ Exported {len(leads)} leads to: {CSV_FILE}")

    return 0

if __name__ == "__main__":
    to_csv = "--csv" in sys.argv
    sys.exit(inspect_leads(export_csv=to_csv))
