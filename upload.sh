#!/bin/bash

# 🔰 Smart GitHub Auto Uploader
echo "🚀 Starting smart upload to GitHub..."

cd ~/grey_trading || exit 1

# Add all changes
git add .

# Detect changed files
CHANGED_FILES=$(git diff --cached --name-only)

if [ -z "$CHANGED_FILES" ]; then
  echo "⚡ No new changes to commit."
  exit 0
fi

# Commit with timestamp + file list
COMMIT_MESSAGE="Auto update - $(date '+%a %b %d %H:%M:%S %Z %Y') | Changed: $CHANGED_FILES"
git commit -m "$COMMIT_MESSAGE"

# Push changes
echo "📤 Pushing to remote repository..."
git push -u origin main

# Check push status
if [ $? -eq 0 ]; then
  echo "✅ Upload complete!"
  echo ""
  echo "🌐 View on GitHub: https://github.com/singrao468-ops/GreyG-"
else
  echo "❌ Upload failed. Check your GitHub connection."
fi

