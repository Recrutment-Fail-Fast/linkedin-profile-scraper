import subprocess
import os
import psutil
import glob
import shutil

def kill_chrome():
    """
    Kill Chrome processes in a Docker-compatible way and clean up profile directories.
    Uses psutil for cross-platform process management.
    """
    killed_processes = 0
    
    try:
        # Method 1: Use psutil to find and kill Chrome processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_info = proc.info
                proc_name = proc_info['name'].lower() if proc_info['name'] else ''
                proc_cmdline = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                
                # Check if this is a Chrome/Chromium process
                if any(chrome_name in proc_name for chrome_name in ['chrome', 'chromium']) or \
                   any(chrome_name in proc_cmdline.lower() for chrome_name in ['chrome', 'chromium', 'playwright']):
                    
                    print(f"Killing Chrome process: PID {proc_info['pid']}, Name: {proc_name}")
                    proc.terminate()
                    killed_processes += 1
                    
                    # Wait a bit for graceful termination
                    try:
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        # Force kill if it doesn't terminate gracefully
                        proc.kill()
                        print(f"Force killed Chrome process: PID {proc_info['pid']}")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process might have already been terminated or we don't have access
                continue
                
    except Exception as e:
        print(f"Error using psutil to kill Chrome: {e}")
        
        # Method 2: Fallback to subprocess methods for Unix-like systems
        try:
            # Try pkill if available
            result = subprocess.run(["pkill", "-f", "chrome"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("Successfully killed Chrome processes using pkill")
            elif result.returncode == 1:
                print("No Chrome processes found to kill (pkill)")
            else:
                print(f"pkill returned code {result.returncode}: {result.stderr}")
                
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"pkill failed: {e}")
            
            # Method 3: Try killall as final fallback
            try:
                result = subprocess.run(["killall", "chrome"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("Successfully killed Chrome processes using killall")
                elif result.returncode == 1:
                    print("No Chrome processes found to kill (killall)")
                else:
                    print(f"killall returned code {result.returncode}: {result.stderr}")
                    
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                print(f"killall failed: {e}")
    
    # Clean up temporary Chrome profile directories (but preserve the main profile)
    cleanup_temp_chrome_profiles()
    
    if killed_processes > 0:
        print(f"Successfully killed {killed_processes} Chrome process(es)")
    else:
        print("No Chrome processes found to kill")

def cleanup_temp_chrome_profiles():
    """Clean up temporary Chrome profile directories to prevent lock conflicts."""
    try:
        # Find all chrome-profile-* directories in /tmp (temporary profiles)
        temp_profile_dirs = glob.glob("/tmp/chrome-profile-*")
        cleaned_dirs = 0
        
        for profile_dir in temp_profile_dirs:
            try:
                if os.path.exists(profile_dir):
                    shutil.rmtree(profile_dir)
                    cleaned_dirs += 1
                    print(f"Cleaned up temporary profile directory: {profile_dir}")
            except Exception as e:
                print(f"Failed to clean up {profile_dir}: {e}")
        
        # Also clean up any lock files in the main profile directory
        main_profile = "/tmp/chrome-profile"
        if os.path.exists(main_profile):
            try:
                # Remove lock files but keep the profile data
                lock_files = [
                    "SingletonLock", "SingletonSocket", "SingletonCookie"
                ]
                for lock_file in lock_files:
                    lock_path = os.path.join(main_profile, lock_file)
                    if os.path.exists(lock_path):
                        os.remove(lock_path)
                        print(f"Removed lock file: {lock_file}")
                        
                # Also check for profile-specific lock files
                for item in os.listdir(main_profile):
                    item_path = os.path.join(main_profile, item)
                    if os.path.isdir(item_path):
                        profile_lock = os.path.join(item_path, "SingletonLock")
                        if os.path.exists(profile_lock):
                            os.remove(profile_lock)
                            print(f"Removed profile lock: {item}/SingletonLock")
                            
            except Exception as e:
                print(f"Failed to clean up lock files in main profile: {e}")
        
        if cleaned_dirs > 0:
            print(f"Successfully cleaned up {cleaned_dirs} temporary Chrome profile director(ies)")
        else:
            print("No temporary Chrome profile directories found to clean up")
            
    except Exception as e:
        print(f"Error during profile cleanup: {e}")