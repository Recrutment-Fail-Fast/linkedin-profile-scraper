import subprocess

def kill_chrome():
    try:
        subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Chrome: {e}")
    except FileNotFoundError:
        print("PowerShell command not found. Please ensure it is in your PATH.")