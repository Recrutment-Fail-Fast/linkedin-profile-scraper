#!/bin/bash
# Script to copy Chrome profile during Docker build
# Usage: copy_chrome_profile_docker.sh <chrome_user_data_dir> <profile_directory>

set -e

CHROME_USER_DATA_DIR="$1"
PROFILE_DIRECTORY="$2"

if [ -z "$CHROME_USER_DATA_DIR" ] || [ -z "$PROFILE_DIRECTORY" ]; then
    echo "❌ Usage: $0 <chrome_user_data_dir> <profile_directory>"
    exit 1
fi

echo "🔧 Copying Chrome profile during Docker build..."
echo "📁 Source: $CHROME_USER_DATA_DIR/$PROFILE_DIRECTORY"
echo "📁 Target: /tmp/chrome-profile/"

# Check if source profile exists
if [ ! -d "$CHROME_USER_DATA_DIR/$PROFILE_DIRECTORY" ]; then
    echo "❌ Chrome profile not found: $CHROME_USER_DATA_DIR/$PROFILE_DIRECTORY"
    echo "Available profiles:"
    ls -la "$CHROME_USER_DATA_DIR" 2>/dev/null | grep "^d" | grep -E "(Default|Profile)" || echo "No profiles found"
    exit 1
fi

# Copy the profile
echo "📋 Copying profile files..."
cp -r "$CHROME_USER_DATA_DIR/$PROFILE_DIRECTORY"/* /tmp/chrome-profile/ 2>/dev/null || {
    echo "⚠️ Some files couldn't be copied (this is normal for locked files)"
}

# Check for important authentication files
echo "🔍 Checking for authentication files:"
AUTH_FILES=("Cookies" "Local Storage" "Session Storage" "Preferences" "Login Data" "Web Data")

for file in "${AUTH_FILES[@]}"; do
    if [ -e "/tmp/chrome-profile/$file" ]; then
        if [ -f "/tmp/chrome-profile/$file" ]; then
            size=$(stat -c%s "/tmp/chrome-profile/$file" 2>/dev/null || echo "unknown")
            echo "  ✅ $file: $size bytes"
        else
            count=$(find "/tmp/chrome-profile/$file" -type f 2>/dev/null | wc -l)
            echo "  ✅ $file: $count files"
        fi
    else
        echo "  ❌ $file: Not found"
    fi
done

# Set proper permissions
chmod -R 755 /tmp/chrome-profile/
echo "✅ Chrome profile copied successfully!" 