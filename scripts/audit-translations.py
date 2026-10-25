#!/usr/bin/env python3
"""
scripts/audit-translations.py
Runs the Node.js Multilingual Localization Integrity Audit Engine.
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def main():
    js_script = REPO_ROOT / "scripts" / "audit-translations.js"
    res = subprocess.run(["node", str(js_script)], check=False)
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
