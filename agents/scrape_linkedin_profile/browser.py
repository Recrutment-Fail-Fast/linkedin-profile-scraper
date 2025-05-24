from browser_use import Browser, BrowserConfig
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_browser():
    """Create and return a Browser instance with proper error handling."""
    try:
        chrome_path: str = os.environ.get("CHROME_PATH")
        chrome_user_data_dir: str = os.environ.get("CHROME_USER_DATA_DIR")
        chrome_profile_directory: str = os.environ.get("CHROME_PROFILE_DIRECTORY")
        debug_port = 9223

        # Docker-friendly browser args
        docker_args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--headless=new",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-ipc-flooding-protection",
            "--enable-automation",
            "--remote-debugging-address=0.0.0.0"
        ]

        base_args = [
            f"--user-data-dir={chrome_user_data_dir}",
            f"--profile-directory={chrome_profile_directory}",
            "--disable-blink-features=AutomationControlled",
            "--no-default-browser-check",
            "--no-first-run",
            "--disable-default-apps",
            "--disable-extensions-except",
            "--disable-plugins-discovery",
            "--allow-running-insecure-content"
        ]

        extra_args = base_args + docker_args

        # Initialize browser with proper configuration
        browser_config = BrowserConfig(
            browser_binary_path=chrome_path,
            chrome_remote_debugging_port=debug_port,
            extra_browser_args=extra_args,
        )

        browser_instance = Browser(config=browser_config)
        print(f"✅ Browser created successfully. Type: {type(browser_instance)}")
        return browser_instance
        
    except Exception as e:
        print(f"❌ Error creating browser: {e}")
        import traceback
        traceback.print_exc()
        raise

# Create browser instance
browser = create_browser()