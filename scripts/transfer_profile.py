#!/usr/bin/env python3
"""
Script to transfer Chrome profile data from local Windows to Docker volume.
This allows you to reuse your authenticated LinkedIn session in Docker.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def copy_windows_profile_to_docker():
    """Copy Chrome profile from Windows to Docker volume."""
    
    # Get Windows Chrome profile path from environment variables
    windows_chrome_user_data_dir = os.environ.get("WINDOWS_CHROME_USER_DATA_DIR")
    windows_chrome_profile_directory = os.environ.get("WINDOWS_CHROME_PROFILE_DIRECTORY", "Default")
    
    if not windows_chrome_user_data_dir:
        print("❌ WINDOWS_CHROME_USER_DATA_DIR environment variable not set!")
        print("Please add WINDOWS_CHROME_USER_DATA_DIR to your .env file.")
        print("Example: WINDOWS_CHROME_USER_DATA_DIR=C:/Users/juans/ChromeTestEnvironment")
        return False
    
    windows_profile_path = Path(windows_chrome_user_data_dir) / windows_chrome_profile_directory
    
    if not windows_profile_path.exists():
        print(f"❌ Windows profile not found at: {windows_profile_path}")
        print("Please update the WINDOWS_CHROME_USER_DATA_DIR and WINDOWS_CHROME_PROFILE_DIRECTORY in your .env file.")
        return False
    
    print(f"📁 Found Windows profile at: {windows_profile_path}")
    
    # Create temporary directory to stage profile data
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_profile = Path(temp_dir) / "Default"
        
        print(f"📦 Copying profile to temporary location...")
        shutil.copytree(windows_profile_path, temp_profile)
        
        # Important files for authentication persistence
        auth_files = [
            "Cookies",
            "Local Storage",
            "Session Storage",
            "Preferences", 
            "History",
            "Login Data",
            "Web Data"
        ]
        
        print("🔍 Checking for authentication files:")
        for file_name in auth_files:
            file_path = temp_profile / file_name
            if file_path.exists():
                if file_path.is_file():
                    size = file_path.stat().st_size
                    print(f"  ✅ {file_name}: {size} bytes")
                else:
                    file_count = len(list(file_path.rglob('*'))) if file_path.is_dir() else 0
                    print(f"  ✅ {file_name}: {file_count} files")
            else:
                print(f"  ❌ {file_name}: Not found")
        
        # Create docker-compose command to copy profile
        print(f"\n🐳 Starting container to copy profile data...")
        
        # Start container temporarily to copy data
        cmd = [
            "docker-compose", "run", "--rm", 
            "-v", f"{temp_dir}:/tmp/source",
            "linkedin-scraper",
            "cp", "-r", "/tmp/source/Default/", "/tmp/chrome-profile/"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Profile data copied successfully to Docker volume!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to copy profile: {e}")
            print(f"Error output: {e.stderr}")
            return False

def verify_docker_profile():
    """Verify that the profile was copied correctly to Docker."""
    
    cmd = [
        "docker-compose", "run", "--rm",
        "linkedin-scraper",
        "ls", "-la", "/tmp/chrome-profile/Default/"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\n📋 Docker profile contents:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to verify profile: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Chrome Profile Transfer Tool")
    print("=" * 50)
    
    # Step 1: Copy profile
    if copy_windows_profile_to_docker():
        # Step 2: Verify copy
        verify_docker_profile()
        print("\n✅ Profile transfer complete!")
        print("You can now start your Docker container and it should use your authenticated session.")
    else:
        print("\n❌ Profile transfer failed!")
        print("Please check the error messages above and try again.") 