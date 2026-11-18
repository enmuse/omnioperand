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
echo "🚀 Publishing omnioperand-mcp to public NPM registry..."
npm publish --access public
echo "🎉 Successfully published omnioperand-mcp!"
