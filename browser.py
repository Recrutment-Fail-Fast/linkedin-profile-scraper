from browser_use import Browser, BrowserConfig

browser = Browser(
    config=BrowserConfig(
        browser_binary_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        chrome_remote_debugging_port=9223,
        extra_browser_args=[
            "--user-data-dir=C:\\Users\\juans\\ChromeTestEnvironment",
            "--profile-directory=MyTestProfile"
        ]
    )
)