from browser_use import Browser, BrowserConfig

def create_browser():
    """Create and return a Browser instance with proper error handling."""
    try:
        chrome_path = "/root/.cache/ms-playwright/chromium-1169/chrome-linux/chrome"
        chrome_user_data_dir = "/tmp/chrome-profile"
        chrome_profile_directory = "Default"
        debug_port = 9223

        browser = Browser(
            config=BrowserConfig(
                browser_binary_path=chrome_path,
                chrome_remote_debugging_port=debug_port,
                extra_browser_args=[
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-software-rasterizer",
                    "--disable-extensions",
                    "--disable-background-networking",
                    "--remote-debugging-address=0.0.0.0",
                    f"--remote-debugging-port={debug_port}",
                    f"--user-data-dir={chrome_user_data_dir}",
                    f"--profile-directory={chrome_profile_directory}"
                ]
            )
        )
    
        print(f"✅ Browser created successfully. Type: {type(browser)}")
        return browser

    except Exception as e:
        print(f"❌ Error creating browser: {e}")
        import traceback
        traceback.print_exc()
        raise
