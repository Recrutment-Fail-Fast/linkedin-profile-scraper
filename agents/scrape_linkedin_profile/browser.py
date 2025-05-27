from browser_use import BrowserSession, BrowserProfile
from datetime import datetime, timedelta
from stores.prospect import prospect_store
import os
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
                }
            ],
            "origins": []
        }
        
        # Configure browser profile with cookies and other settings
        browser_profile = BrowserProfile(
            headless=True,  # Set to False if you want to see the browser
            storage_state=storage_state,  # Pass LinkedIn cookies
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--remote-debugging-address=0.0.0.0",
            ]
        )

        # Create and start the browser session
        print("🚀 Starting browser session with LinkedIn cookies...")
        browser_session = BrowserSession(browser_profile=browser_profile)
        await browser_session.start()
        
        # Verify the browser context and cookies
        context = browser_session.browser_context
        if not context:
            raise RuntimeError("BrowserContext not available after browser_session.start()")
        
        linkedin_url = prospect_store.prospect["linkedin_url"]

        await browser_session.navigate_to(linkedin_url)
        
        return browser_session
        
    except Exception as e:
        print(f"❌ Error creating browser session: {e}")
        import traceback
        traceback.print_exc()
        raise