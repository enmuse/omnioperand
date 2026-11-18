#!/usr/bin/env bash
# scripts/publish_mcp.sh — Helper to publish omnioperand-mcp to NPM
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../packages/omnioperand-mcp" && pwd)"
cd "$DIR"

echo "========================================================="
echo "📦 OmniOperand MCP NPM Publisher"
echo "Package Directory: $DIR"
echo "========================================================="

if ! npm whoami >/dev/null 2>&1; then
  echo "⚠️ You are not currently logged in to npm."
  echo "👉 Please run: npm login"
  echo "Then re-run this script: bash scripts/publish_mcp.sh"
  exit 1
fi

USER=$(npm whoami)
echo "👤 Logged in as: $USER"

OTP_FLAG=""
if [ -n "$1" ]; then
  echo "🔑 Using provided 2FA OTP code: $1"
  OTP_FLAG="--otp=$1"
fi

echo "🚀 Publishing omnioperand-mcp to public NPM registry..."
if npm publish --access public $OTP_FLAG; then
  echo ""
  echo "========================================================="
  echo "🎉 Successfully published omnioperand-mcp to NPM!"
  echo "🌐 Verify on registry: https://www.npmjs.com/package/omnioperand-mcp"
  echo "⚡ Run anywhere via npx: npx -y omnioperand-mcp"
  echo "========================================================="
else
  echo ""
  echo "========================================================="
  echo "⚠️ NPM Publish encountered an authorization / 2FA gate."
  echo ""
  echo "Option A (Quickest with Authenticator App):"
  echo "  Get the 6-digit code from your authenticator app and run:"
  echo "  bash scripts/publish_mcp.sh <6-DIGIT-OTP>"
  echo "  (e.g.: bash scripts/publish_mcp.sh 847291)"
  echo ""
  echo "Option B (Automated Token - Recommended for CI & no OTP prompts):"
  echo "  1. Visit: https://www.npmjs.com/settings/omnioperand/tokens"
  echo "  2. Click 'Generate New Token' -> Choose 'Classic Token' -> 'Automation'"
  echo "  3. In terminal, run:"
  echo "     npm set //registry.npmjs.org/:_authToken=npm_YOUR_TOKEN"
  echo "  4. Re-run: bash scripts/publish_mcp.sh"
  echo "========================================================="
  exit 1
fi
