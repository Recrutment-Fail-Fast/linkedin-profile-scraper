#!/usr/bin/env python3
"""
Build Docker image with Chrome profile automatically included.
Reads Chrome configuration from .env file and builds the image.
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_chrome_config():
    """Get Chrome configuration from environment variables."""
    chrome_user_data_dir = os.getenv('CHROME_USER_DATA_DIR')
    chrome_profile_directory = os.getenv('CHROME_PROFILE_DIRECTORY', 'Default')
    
    if not chrome_user_data_dir:
        raise ValueError(
            "❌ CHROME_USER_DATA_DIR not found in .env file!\n"
            "Please add your Chrome profile path to .env file."
        )
    
    return chrome_user_data_dir, chrome_profile_directory

def validate_chrome_profile(user_data_dir, profile_directory):
    """Validate that the Chrome profile exists."""
    profile_path = Path(user_data_dir) / profile_directory
    
    if not Path(user_data_dir).exists():
        raise FileNotFoundError(f"❌ Chrome User Data directory not found: {user_data_dir}")
    
    if not profile_path.exists():
        available_profiles = [item.name for item in Path(user_data_dir).iterdir() 
                            if item.is_dir() and (item.name == "Default" or item.name.startswith("Profile "))]
        raise FileNotFoundError(
            f"❌ Chrome profile '{profile_directory}' not found in {user_data_dir}\n"
            f"Available profiles: {available_profiles}"
        )
    
    return profile_path

def build_docker_image(chrome_user_data_dir, chrome_profile_directory, image_tag="linkedin-scraper:latest"):
    """Build Docker image with Chrome profile included."""
    print("🐳 Building Docker image with Chrome profile...")
    print(f"📁 Chrome User Data Dir: {chrome_user_data_dir}")
    print(f"📂 Profile Directory: {chrome_profile_directory}")
    print(f"🏷️ Image Tag: {image_tag}")
    
    # Convert Windows paths to Unix-style for Docker build context
    if os.name == 'nt':  # Windows
        # Convert C:\Users\... to /c/Users/... for Docker
        unix_path = chrome_user_data_dir.replace('\\', '/').replace('C:', '/c')
        chrome_user_data_dir = unix_path
    
    # Build command
    cmd = [
        "docker", "build",
        "--build-arg", f"CHROME_USER_DATA_DIR={chrome_user_data_dir}",
        "--build-arg", f"CHROME_PROFILE_DIRECTORY={chrome_profile_directory}",
        "-t", image_tag,
        "."
    ]
    
    print(f"🔨 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ Docker image built successfully: {image_tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker build failed with exit code {e.returncode}")
        return False

def main():
    """Main function to build Docker image with Chrome profile."""
    print("🔧 Docker Build with Chrome Profile")
    print("=" * 50)
    
    try:
        # Get Chrome configuration
        chrome_user_data_dir, chrome_profile_directory = get_chrome_config()
        
        # Validate profile exists
        profile_path = validate_chrome_profile(chrome_user_data_dir, chrome_profile_directory)
        print(f"✅ Chrome profile found: {profile_path}")
        
        # Check for important files
        auth_files = ["Cookies", "Preferences", "Local Storage"]
        missing_files = []
        
        for file_name in auth_files:
            file_path = profile_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            print(f"⚠️  Warning: Some authentication files are missing: {missing_files}")
            print("This might indicate the profile hasn't been used much.")
            response = input("Continue anyway? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Build cancelled.")
                return
        
        # Get image tag from command line or use default
        image_tag = sys.argv[1] if len(sys.argv) > 1 else "linkedin-scraper:latest"
        
        # Build the image
        success = build_docker_image(chrome_user_data_dir, chrome_profile_directory, image_tag)
        
        if success:
            print("\n🎉 Success! Docker image built with Chrome profile included.")
            print(f"🚀 You can now run: docker run -p 8000:8000 {image_tag}")
            print("\n💡 Note: The Chrome profile is now embedded in the image.")
            print("To update the profile, rebuild the image after updating your Chrome data.")
        else:
            print("\n❌ Build failed. Check the errors above.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your .env file contains:")
        print("CHROME_USER_DATA_DIR=C:\\Users\\yourusername\\AppData\\Local\\Google\\Chrome\\User Data")
        print("CHROME_PROFILE_DIRECTORY=Default")

if __name__ == "__main__":
    main() 