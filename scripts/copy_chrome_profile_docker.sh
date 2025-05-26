#!/bin/bash
# Script to copy and verify Chrome profile data within a Docker image.
# Usage: copy_chrome_profile_docker.sh <source_profile_data_path_in_image> <target_profile_path_in_image>

set -e

SOURCE_PROFILE_DATA_PATH="$1"
TARGET_PROFILE_PATH="$2"

if [ -z "$SOURCE_PROFILE_DATA_PATH" ] || [ -z "$TARGET_PROFILE_PATH" ]; then
    echo "❌ Usage: $0 <source_profile_data_path_in_image> <target_profile_path_in_image>"
    exit 1
fi

echo "🔧 Processing Chrome profile data within Docker image..."
echo "📁 Source (already in image): $SOURCE_PROFILE_DATA_PATH"
echo "🎯 Target (final location in image): $TARGET_PROFILE_PATH"

# Check if source data exists (it should have been copied by Dockerfile COPY)
if [ ! -d "$SOURCE_PROFILE_DATA_PATH" ]; then
    echo "❌ Source profile data not found at internal path: $SOURCE_PROFILE_DATA_PATH"
    echo "This is unexpected. Ensure Dockerfile correctly copied data before running this script."
    # List contents of /tmp to help debug
    ls -la /tmp
    exit 1
fi

# Ensure target directory exists (though Dockerfile should create it)
if [ ! -d "$TARGET_PROFILE_PATH" ]; then
    echo "ℹ️ Target directory $TARGET_PROFILE_PATH does not exist. Creating it."
    mkdir -p "$TARGET_PROFILE_PATH"
fi

# Copy the profile data from the source (e.g., /tmp/staging_area) to the final target path
# The `.` after SOURCE_PROFILE_DATA_PATH ensures contents are copied, not the directory itself
echo "📋 Copying profile files from $SOURCE_PROFILE_DATA_PATH to $TARGET_PROFILE_PATH..."
cp -r "$SOURCE_PROFILE_DATA_PATH"/. "$TARGET_PROFILE_PATH/" 2>/dev/null || {
    echo "⚠️ Some files couldn't be copied from $SOURCE_PROFILE_DATA_PATH to $TARGET_PROFILE_PATH. This might be okay for some files (e.g. lockfiles if they were somehow included), but check if essential files are present."
}

# Check for important authentication files in the final target location
echo "🔍 Checking for authentication files in $TARGET_PROFILE_PATH:"
AUTH_FILES=("Cookies" "Local Storage" "Preferences" "Login Data" "Web Data") # Removed "Session Storage" as it's often problematic and less critical for persistence

for file in "${AUTH_FILES[@]}"; do
    full_file_path="$TARGET_PROFILE_PATH/$file"
    if [ -e "$full_file_path" ]; then
        if [ -f "$full_file_path" ]; then
            size=$(stat -c%s "$full_file_path" 2>/dev/null || echo "unknown_size")
            echo "  ✅ $file: Found (File, Size: $size bytes)"
        elif [ -d "$full_file_path" ]; then
            count=$(find "$full_file_path" -type f 2>/dev/null | wc -l)
            echo "  ✅ $file: Found (Directory, $count files)"
        else
            echo "  ✅ $file: Found (Type unknown)"
        fi
    else
        echo "  ⚠️  $file: Not found in $TARGET_PROFILE_PATH. This might impact authentication."
    fi
done

# Set proper permissions for the final profile directory
chmod -R 777 "$TARGET_PROFILE_PATH/" # Changed to 777 for broader compatibility inside container
echo "✅ Chrome profile processed and placed at $TARGET_PROFILE_PATH." 