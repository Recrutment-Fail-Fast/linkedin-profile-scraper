#!/usr/bin/env python3
"""
Script to copy your existing Chrome profile to the Docker volume.
This allows the LinkedIn scraper to use your saved logins and cookies.
Uses environment variables from .env file for Chrome configuration.
"""

import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_chrome_config_from_env():
    """Get Chrome configuration from environment variables."""
    chrome_path = os.getenv('CHROME_PATH')
    chrome_user_data_dir = os.getenv('CHROME_USER_DATA_DIR')
    chrome_profile_directory = os.getenv('CHROME_PROFILE_DIRECTORY', 'Default')
    
    if not chrome_user_data_dir:
        raise ValueError(
            "❌ CHROME_USER_DATA_DIR not found in .env file!\n"
            "Please add the following to your .env file:\n"
            "CHROME_USER_DATA_DIR=C:\\Users\\yourusername\\AppData\\Local\\Google\\Chrome\\User Data\n"
            "CHROME_PROFILE_DIRECTORY=Default\n"
            "CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )
    
    return {
        'chrome_path': chrome_path,
        'user_data_dir': Path(chrome_user_data_dir),
        'profile_directory': chrome_profile_directory
    }

def validate_chrome_profile(user_data_dir, profile_directory):
    """Validate that the Chrome profile exists and contains expected files."""
    profile_path = user_data_dir / profile_directory
    
    if not user_data_dir.exists():
        raise FileNotFoundError(f"❌ Chrome User Data directory not found: {user_data_dir}")
    
    if not profile_path.exists():
        available_profiles = [item.name for item in user_data_dir.iterdir() 
                            if item.is_dir() and (item.name == "Default" or item.name.startswith("Profile "))]
        raise FileNotFoundError(
            f"❌ Chrome profile '{profile_directory}' not found in {user_data_dir}\n"
            f"Available profiles: {available_profiles}"
        )
    
    # Check for important authentication files
    auth_files = ["Cookies", "Preferences", "Local Storage"]
    missing_files = []
    
    for file_name in auth_files:
        file_path = profile_path / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"⚠️  Warning: Some authentication files are missing: {missing_files}")
        print("This might indicate the profile hasn't been used much or is corrupted.")
    
    return profile_path

def copy_profile_to_docker(source_profile_path, profile_name):
    """Copy Chrome profile to Docker volume."""
    print(f"📋 Copying Chrome profile '{profile_name}' to Docker volume...")
    
    # Create a temporary directory to stage the profile
    temp_dir = Path("/tmp/chrome_profile_staging")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Copy the profile to temp directory
        temp_profile_path = temp_dir / profile_name
        if temp_profile_path.exists():
            shutil.rmtree(temp_profile_path)
        
        print(f"📁 Copying from: {source_profile_path}")
        print(f"📁 Copying to: {temp_profile_path}")
        
        shutil.copytree(source_profile_path, temp_profile_path)
        
        # Important files for authentication persistence
        auth_files = [
            "Cookies", "Local Storage", "Session Storage", "Preferences", 
            "History", "Login Data", "Web Data", "Network Action Predictor",
            "Top Sites", "Bookmarks", "Favicons"
        ]
        
        print("\n🔍 Checking for important authentication files:")
        for file_name in auth_files:
            file_path = temp_profile_path / file_name
            if file_path.exists():
                if file_path.is_file():
                    size = file_path.stat().st_size
                    print(f"  ✅ {file_name}: {size} bytes")
                else:
                    file_count = len(list(file_path.rglob('*'))) if file_path.is_dir() else 0
                    print(f"  ✅ {file_name}: {file_count} files")
            else:
                print(f"  ❌ {file_name}: Not found")
        
        # Use Docker to copy the profile to the volume
        print(f"\n🐳 Copying profile to Docker volume...")
        
        # First, ensure the container is running
        result = subprocess.run(
            ["docker-compose", "ps", "-q", "linkedin-scraper"],
            capture_output=True, text=True, cwd=Path.cwd()
        )
        
        if not result.stdout.strip():
            print("🚀 Starting Docker container...")
            subprocess.run(["docker-compose", "up", "-d"], cwd=Path.cwd())
        
        # Copy the profile to the Docker volume
        cmd = [
            "docker-compose", "exec", "-T", "linkedin-scraper",
            "sh", "-c", f"rm -rf /tmp/chrome-profile/* && mkdir -p /tmp/chrome-profile"
        ]
        subprocess.run(cmd, cwd=Path.cwd())
        
        # Copy files using docker cp
        container_name = subprocess.run(
            ["docker-compose", "ps", "-q", "linkedin-scraper"],
            capture_output=True, text=True, cwd=Path.cwd()
        ).stdout.strip()
        
        if container_name:
            cmd = [
                "docker", "cp", f"{temp_profile_path}/.", f"{container_name}:/tmp/chrome-profile/"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Profile copied successfully to Docker volume!")
                
                # Verify the copy
                verify_cmd = [
                    "docker-compose", "exec", "-T", "linkedin-scraper",
                    "ls", "-la", "/tmp/chrome-profile/"
                ]
                verify_result = subprocess.run(verify_cmd, capture_output=True, text=True, cwd=Path.cwd())
                print(f"\n📁 Files in Docker volume:")
                print(verify_result.stdout)
                
                return True
            else:
                print(f"❌ Failed to copy profile: {result.stderr}")
                return False
        else:
            print("❌ Could not find running container")
            return False
            
    except Exception as e:
        print(f"❌ Error copying profile: {e}")
        return False
    finally:
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def main():
    """Main function to copy Chrome profile using environment variables."""
    print("🔧 Chrome Profile Copier for LinkedIn Scraper")
    print("📋 Using configuration from .env file")
    print("=" * 50)
    
    try:
        # Get Chrome configuration from environment variables
        config = get_chrome_config_from_env()
        
        print(f"📁 Chrome User Data Dir: {config['user_data_dir']}")
        print(f"📂 Profile Directory: {config['profile_directory']}")
        if config['chrome_path']:
            print(f"🌐 Chrome Path: {config['chrome_path']}")
        
        # Validate the profile exists
        source_profile_path = validate_chrome_profile(
            config['user_data_dir'], 
            config['profile_directory']
        )
        
        print(f"✅ Chrome profile found: {source_profile_path}")
        
        # Check if Chrome is running
        print(f"\n⚠️  IMPORTANT: Please close all Chrome windows before proceeding!")
        print(f"This prevents profile lock conflicts during copying.")
        
        # Check for running Chrome processes
        try:
            import psutil
            chrome_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc.info)
            
            if chrome_processes:
                print(f"⚠️  Found {len(chrome_processes)} running Chrome process(es):")
                for proc in chrome_processes[:3]:  # Show first 3
                    print(f"  - PID {proc['pid']}: {proc['name']}")
                if len(chrome_processes) > 3:
                    print(f"  ... and {len(chrome_processes) - 3} more")
                print("\nPlease close Chrome completely before continuing.")
        except ImportError:
            print("(Install psutil to check for running Chrome processes)")
        
        input("\nPress Enter when Chrome is closed...")
        
        # Copy the profile
        success = copy_profile_to_docker(source_profile_path, config['profile_directory'])
        
        if success:
            print("\n🎉 Success! Your Chrome profile has been copied to the Docker volume.")
            print("🔐 The LinkedIn scraper will now use your saved logins and cookies.")
            print(f"📂 Profile used: {config['profile_directory']}")
            print("\n📝 Next steps:")
            print("1. Make sure your Docker container is running: docker-compose up -d")
            print("2. Test the scraper - it should skip login steps!")
        else:
            print("\n❌ Failed to copy Chrome profile. Please check the errors above.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your .env file contains:")
        print("CHROME_USER_DATA_DIR=C:\\Users\\yourusername\\AppData\\Local\\Google\\Chrome\\User Data")
        print("CHROME_PROFILE_DIRECTORY=Default")
        print("CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

if __name__ == "__main__":
    main()

    # Local Chrome Configuration (for development)

    # example:
    # CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
    # CHROME_USER_DATA_DIR=C:\\Users\\juans\\ChromeTestEnvironment
    # CHROME_PROFILE_DIRECTORY=MyTestProfile