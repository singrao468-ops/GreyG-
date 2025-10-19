#!/bin/bash

echo "🚀 Starting smart upload to GitHub..."

cd ~/grey_trading || exit 1

# Add all changes
git add .

# Find changed files for better commit message
CHANGED_FILES=$(git diff --cached --name-only)

if [ -z "$CHANGED_FILES" ]; then
  echo "⚡ No new changes to commit."
  exit 0
fi

# Create readable commit message
COMMIT_MESSAGE="Auto update - $(date '+%a %b %d %H:%M:%S %Z %Y') | Changed: $CHANGED_FILES"

# Commit changes
git commit -m "$COMMIT_MESSAGE"

# Push changes
echo "📤 Pushing to remote repository..."
git push -u origin main

if [ $? -eq 0 ]; then
  echo "✅ Upload complete!"
else
  echo "❌ Upload failed. Check your GitHub connection."
fi

