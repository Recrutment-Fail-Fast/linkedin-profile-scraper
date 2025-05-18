




irm https://astral.sh/uv/install.ps1 | iex


uv venv   

.venv\Scripts\activate  

uv install browser-use       

playwright install

chrome://version/


## Troubleshooting Chrome Remote Debugging Connection Issues

If you encounter `ERR_CONNECTION_REFUSED` when your script (using `browser-use` or Playwright) tries to connect to Chrome's remote debugging port (e.g., `http://localhost:9223/json`), it means Chrome launched but didn't activate its debugging service on that port.

This often happens when attempting to use an existing Chrome profile that might have conflicting states, settings, or lock files.

**Key Solution: Use a Dedicated Clean Profile for Automation**

The most reliable solution is to configure `browser-use` to launch Chrome with a dedicated, clean user data directory and profile. This isolates the automated browser session from your regular browsing profiles.

**Steps:**

1.  **Ensure ALL Chrome Instances are Closed:** Before running your script, use Task Manager (Ctrl+Shift+Esc) to terminate every `chrome.exe` process. This is crucial as existing Chrome instances can interfere with how new ones are launched with debugging flags.

run Stop-Process -Name chrome -Force in powershell

or tasklist /FI "IMAGENAME eq chrome.exe" if you want to verify any chrome instance is running


2.  **Configure `browser-use` in your Python script:**
    Modify your `Browser` initialization to specify a `browser_binary_path`, a `chrome_remote_debugging_port`, and `extra_browser_args` to define a new user data directory and profile for automation.

    ```python
    from browser_use import Browser, BrowserConfig

    # ... other imports and setup ...

    chrome_executable_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Adjust if your path is different
    # Define a new, clean directory for this automation's user data
    automation_user_data_dir = "C:\\Users\\YourUserName\\AutomationChromeProfile" # IMPORTANT: Replace YourUserName
    automation_profile_name = "AutomationProfile" # You can name this profile anything

    browser = Browser(
        config=BrowserConfig(
            browser_binary_path=chrome_executable_path,
            chrome_remote_debugging_port=9223,  # Or any other available port
            extra_browser_args=[
                f"--user-data-dir={automation_user_data_dir}",
                f"--profile-directory={automation_profile_name}"
            ]
        )
    )

    # ... rest of your agent and script logic ...
    ```

    *   **`browser_binary_path`**: Path to your `chrome.exe`.
    *   **`chrome_remote_debugging_port`**: The port for debugging (e.g., 9223).
    *   **`automation_user_data_dir`**: Choose a path for a *new* folder where Chrome will store data for this automation. **Replace `YourUserName` with your actual Windows username.** It's best if this directory does not overlap with your standard Chrome user data directory.
    *   **`automation_profile_name`**: A name for the profile within the `automation_user_data_dir` (e.g., "AutomationProfile", "MyScraperProfile").

3.  **Run Your Script:** `browser-use` will now launch Chrome using these settings, creating a fresh profile in the specified location, which should reliably enable the remote debugging interface.

**Manual Test (If `browser-use` still fails to connect):**

If direct configuration in `browser-use` still leads to issues (which is less likely with the above setup), you can manually test if Chrome can launch with debugging on a new profile:

*   Close all Chrome instances (Task Manager).
*   Open PowerShell or CMD and run (adjust paths and port as needed):
    ```powershell
    & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\YourUserName\ChromeTestEnvironment" --profile-directory="MyTestProfile"
    ```
*   Then, try to access `http://localhost:9223/json` in a different browser. If you see JSON data, Chrome launched correctly with debugging. If not, the issue is with how Chrome itself is launching, possibly due to deeper system conflicts or Chrome installation issues.

**Old Commands (For historical reference or manual launching with existing profiles - use with caution due to potential issues):**

```powershell
# Example: Launching with the main User Data and specifying a profile (can be problematic if the profile is in a bad state)
# & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\juans\AppData\Local\Google\Chrome\User Data" --profile-directory="Profile 9"

# Example: Launching with a specific profile directory directly (can also be problematic)
# & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\juans\AppData\Local\Google\Chrome\User Data\Profile 4"
```


{
  "name": "Jane Doe",
  "title": "Senior Data Scientist at OpenAI",
  "location": "San Francisco, CA, United States",
  "about": "Experienced Data Scientist with a demonstrated history of working in AI and machine learning. Passionate about solving real-world problems using data.",
  "skills": [
    "Machine Learning",
    "Python",
    "Data Analysis",
    "Deep Learning"
  ],
  "experience": [
    {
      "job_positions": [
        {
          "title": "Senior Data Scientist",
          "location": "San Francisco, CA",
          "description": "Leading AI model development and deployment for natural language processing tasks.",
          "start_date": "2021-06",
          "end_date": "Present",
          "skills": [
            "Natural Language Processing",
            "Python",
            "TensorFlow"
          ]
        },
        {
          "title": "Data Scientist",
          "location": "New York, NY",
          "description": "Developed predictive models and automated analytics pipelines.",
          "start_date": "2018-01",
          "end_date": "2021-05",
          "skills": [
            "Predictive Modeling",
            "SQL",
            "Scikit-Learn"
          ]
        }
      ],
      "start_date": "2018-01",
      "end_date": "Present"
    }
  ],
  "education": [
    {
      "school": "Stanford University",
      "degree": "Master of Science in Computer Science",
      "start_date": "2015-09",
      "end_date": "2017-06"
    },
    {
      "school": "University of California, Berkeley",
      "degree": "Bachelor of Science in Statistics",
      "start_date": "2011-09",
      "end_date": "2015-05"
    }
  ],
  "top_voices": [
    {
      "name": "Andrew Ng",
      "title": "Founder at DeepLearning.AI",
      "followers": 2100000
    },
    {
      "name": "Cassie Kozyrkov",
      "title": "Chief Decision Scientist at Google",
      "followers": 1200000
    }
  ],
  "languages": [
    {
      "language": "English",
      "level": "Native"
    },
    {
      "language": "Spanish",
      "level": "Professional Working Proficiency"
    }
  ]
}
