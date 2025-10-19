#!/bin/bash

# 🚀 Grey Market App - GitHub Auto Upload Script

# 🧠 यहां अपना GitHub Token डालो (मुझे मत बताना!)
GITHUB_TOKEN=" "

# 🏷️ Repository का नाम
REPO_URL="https://$GITHUB_TOKEN@github.com/singrao468-ops/GreyG-_GMP.git"

echo "🚀 Starting upload to GitHub..."

cd ~/grey_trading || exit

# Git setup
git init >/dev/null 2>&1
git add .
git commit -m "Auto update - $(date)" >/dev/null 2>&1

# Remote सेट करो (पुराना हटाओ)
git remote remove origin >/dev/null 2>&1
git remote add origin "$REPO_URL"

git branch -M main

echo "📤 Pushing to remote repository..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Upload successful!"
else
    echo "❌ Upload failed. Check your GitHub token or repo name."
fi

