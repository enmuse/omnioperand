#!/usr/bin/env python3
"""
scripts/deploy.py — Cloudflare Pages Programmatic Deployer for OmniOperand

Deploys the static site to Cloudflare Pages project 'omnioperand'.
Reads CLOUD_FLARE_PAGES_API_TOKEN or CLOUD_FLARE_API_TOKEN from .env.
"""

import os
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"
PROJECT_NAME = "omnioperand"
DEFAULT_ACCOUNT_ID = "2bbe914ca4d82460c51d668407bb3dbd"

def load_env_token():
    """Extracts Cloudflare API token from .env file."""
    if not ENV_FILE.exists():
        return ""
    tokens = {}
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CLOUD_FLARE_PAGES_API_TOKEN="):
                tokens["pages"] = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("CLOUD_FLARE_API_TOKEN="):
                tokens["standard"] = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("CLOUDFLARE_ACCOUNT_ID="):
                tokens["account"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return tokens

def deploy_pages():
    tokens = load_env_token()
    token = tokens.get("pages") or tokens.get("standard")
    account_id = tokens.get("account") or DEFAULT_ACCOUNT_ID

    if not token:
        print("❌ Error: No Cloudflare API token found in .env")
        sys.exit(1)

    print("=========================================================")
    print("⛅ Cloudflare Pages Deployer: OmniOperand")
    print(f"Project Name: {PROJECT_NAME}")
    print(f"Account ID: {account_id}")
    print(f"Deploy Directory: {REPO_ROOT}")
    print("=========================================================\n")

    env = os.environ.copy()
    env["CLOUDFLARE_API_TOKEN"] = token
    env["CLOUDFLARE_ACCOUNT_ID"] = account_id

    cmd = [
        "npx", "--yes", "wrangler", "pages", "deploy",
        str(REPO_ROOT),
        f"--project-name={PROJECT_NAME}",
        "--branch=main",
        "--commit-dirty=true"
    ]

    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
        print(res.stdout)
        if res.returncode == 0:
            print(f"\n✨ Successfully deployed OmniOperand!")
            print(f"🔗 Edge URL: https://{PROJECT_NAME}.pages.dev")
            print(f"🌐 Custom Domain: https://omnioperand.com")
            return True
        else:
            print(f"⚠️ Deployment error:\n{res.stderr}")
            return False
    except Exception as e:
        print(f"❌ Deploy subprocess exception: {e}")
        return False

if __name__ == "__main__":
    deploy_pages()
