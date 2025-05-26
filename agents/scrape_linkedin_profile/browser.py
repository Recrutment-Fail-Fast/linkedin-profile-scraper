from browser_use import BrowserSession, BrowserProfile

async def create_browser():
    """Create and return a started BrowserSession instance using existing Chrome profile."""
    try:

        browser_profile = BrowserProfile(
            cookies_file="cookies.json",
            headless=True,  # Set to False if you want to see the browser
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--remote-debugging-address=0.0.0.0",
            ],
            # Browser-use specific settings
            # wait_between_actions=0.5,
            # wait_for_network_idle_page_load_time=2.0,
            # highlight_elements=True,
            # viewport_expansion=500,
        )

        # Create browser session using the profile
        browser_session = BrowserSession(
            browser_profile=browser_profile,
        )
        
        # Start the browser session
        print("🚀 Starting browser session with existing profile...")
        await browser_session.start()
    
        print(f"✅ BrowserSession created and started successfully with existing profile")
        return browser_session

    except Exception as e:
        print(f"❌ Error creating browser session: {e}")
        import traceback
        traceback.print_exc()
        raise
