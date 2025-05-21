from browser_use import Browser, BrowserConfig
import os
from dotenv import load_dotenv

load_dotenv()

chrome_path: str = os.environ.get("CHROME_PATH")
chrome_user_data_dir: str = os.environ.get("CHROME_USER_DATA_DIR")
chrome_profile_directory: str = os.environ.get("CHROME_PROFILE_DIRECTORY")

browser = Browser(
    config=BrowserConfig(
        browser_binary_path=chrome_path,
        chrome_remote_debugging_port=9223,
        extra_browser_args=[
            f"--user-data-dir={chrome_user_data_dir}",
            f"--profile-directory={chrome_profile_directory}"
        ]
    )
)