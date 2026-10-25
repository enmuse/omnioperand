import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def submit_urls():
    js_script = REPO_ROOT / "scripts" / "submit_indexnow.js"
    if js_script.exists():
        res = subprocess.run(["node", str(js_script)], check=False)
        return res.returncode == 0
    return False

if __name__ == "__main__":
    submit_urls()
