import subprocess
import os

def kill_chrome():
    try:
        # Kill Chrome processes using pkill
        subprocess.run(["pkill", "-f", "chrome"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Chrome: {e}")
    except FileNotFoundError:
        # Try killall as backup
        try:
            subprocess.run(["killall", "chrome"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Could not kill Chrome processes. They may not be running.")