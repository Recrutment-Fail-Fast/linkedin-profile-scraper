from browser_use import BrowserSession, BrowserProfile
from datetime import datetime, timedelta
from stores.prospect import prospect_store
import os
import uuid
from dotenv import load_dotenv


async def create_browser():
    """Create browser session with LinkedIn cookies and navigate to LinkedIn."""
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get LinkedIn cookie from environment variable
        li_at_cookie: str = os.getenv("L_AT_COOKIE")
        if not li_at_cookie:
            raise ValueError("L_AT_COOKIE is not set in .env file")
        
        # LinkedIn authentication cookie
        storage_state = {
            "cookies": [
                {
                    "name": "li_at",
                    "value": li_at_cookie,
                    "domain": ".linkedin.com",
                    "path": "/",
                    "expires": int((datetime.now() + timedelta(days=7)).timestamp()),
                    "secure": True,
                    "httpOnly": False,
                    "sameSite": "None"
                },
            ],
            "origins": [
                {
                    "origin": "https://www.linkedin.com",
                    "localStorage": []
                }
            ]
        }

        # Check if running in Docker
        is_docker = os.getenv("DOCKER", "false").lower() == "true"
        
        # Configure browser arguments based on environment
        browser_args = []
        if is_docker:
            browser_args = [
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI",
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--enable-automation",
                "--disable-default-apps",
                "--disable-sync",
                "--single-process",
                "--no-zygote",
                "--memory-pressure-off",
                "--remote-debugging-address=0.0.0.0",
                "--disable-setuid-sandbox",
            ]
        
        # Configure browser profile with cookies and other settings
        browser_profile = BrowserProfile(
            storage_state=storage_state,  # Pass LinkedIn cookies
            headless=is_docker,  # Set to False if you want to see the browser
            # user_data_dir="/tmp/chrome-profile" if is_docker else None,  # Use persistent directory in Docker
            chromium_sandbox=not is_docker,  # Disable sandbox in Docker
            args=browser_args,
        )

        # Create and start the browser session
        print("🚀 Starting browser session with LinkedIn cookies...")
        browser_session = BrowserSession(browser_profile=browser_profile)
        await browser_session.start()
        
        # Get the LinkedIn URL and navigate to it
        linkedin_url = prospect_store.prospect["linkedin_url"]
        page = await browser_session.get_current_page()
        await page.goto(linkedin_url)
        
        return browser_session
        
    except Exception as e:
        print(f"❌ Error creating browser session: {e}")
        import traceback
        traceback.print_exc()
        raise