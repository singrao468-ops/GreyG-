#!/bin/bash
# 🚀 Safe GitHub Auto Uploader (No Token Needed)
# Make sure you're logged in using: gh auth login

echo ""
echo "🚀 Starting secure upload to GitHub..."

# Stop on error
set -e

# Check login
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ You are not logged in to GitHub CLI. Run: gh auth login"
    exit 1
fi

# Git setup
cd "$(dirname "$0")" || exit
git add .
git commit -m "Auto update - $(date +"%a %b %d %H:%M:%S %Z %Y")" || echo "🟡 No new changes to commit"

# Push changes
echo "📤 Pushing to remote repository..."
if git push; then
    echo "✅ Upload complete!"
else
    echo "❌ Upload failed. Please check your internet or permissions."
fi

