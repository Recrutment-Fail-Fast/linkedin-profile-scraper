from browser_use import BrowserSession, BrowserProfile

async def create_browser():
    """Create and return a started BrowserSession instance using existing Chrome profile."""
    try:
        chrome_path = "/root/.cache/ms-playwright/chromium-1169/chrome-linux/chrome"
        
        # Use your existing Chrome profile directory
        # This should point to your actual Chrome profile with saved logins
        chrome_user_data_dir = "/tmp/chrome-profile"  # This will be mounted from host
        chrome_profile_directory = "Default"  # or "Profile 1", "Profile 2", etc.
        debug_port = 9223

        print(f"🔧 Using existing Chrome profile: {chrome_user_data_dir}/{chrome_profile_directory}")

        # Create browser profile with configuration to use existing profile
        browser_profile = BrowserProfile(
            executable_path=chrome_path,
            user_data_dir=chrome_user_data_dir,
            profile_directory=chrome_profile_directory,
            headless=True,  # Set to False if you want to see the browser
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--remote-debugging-address=0.0.0.0",
                f"--remote-debugging-port={debug_port}",
                # Remove profile-related args since they're handled by BrowserProfile
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
            keep_alive=True,  # Keep alive to maintain session state
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
