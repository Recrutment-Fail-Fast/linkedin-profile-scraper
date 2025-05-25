# Chrome Profile Setup for LinkedIn Scraper

This guide explains how to configure the LinkedIn scraper to use your existing Chrome profile, allowing it to reuse your saved logins and cookies.

## 🎯 Goal

Instead of logging into LinkedIn every time, the scraper will use your existing Chrome profile with saved authentication data.

## 📋 Prerequisites

1. Google Chrome installed on your system
2. You must be logged into LinkedIn in your Chrome browser
3. Docker and Docker Compose installed
4. Your Chrome profile path information

## 🚀 Setup Steps

### Step 1: Configure Environment Variables

Create or update your `.env` file with your Chrome configuration:

```env
# Chrome Configuration
CHROME_USER_DATA_DIR=C:\Users\yourusername\AppData\Local\Google\Chrome\User Data
CHROME_PROFILE_DIRECTORY=Default
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

**How to find your Chrome profile path:**

1. **Windows**: 
   - Open Chrome and go to `chrome://version/`
   - Look for "Profile Path" - copy everything before the profile name
   - Example: `C:\Users\juans\AppData\Local\Google\Chrome\User Data`

2. **macOS**:
   - Profile path: `~/Library/Application Support/Google/Chrome`

3. **Linux**:
   - Profile path: `~/.config/google-chrome`

**Profile Directory Options:**
- `Default` - Your main Chrome profile
- `Profile 1`, `Profile 2`, etc. - Additional profiles

### Step 2: Copy Your Chrome Profile

Run the profile copy script:

```bash
python scripts/copy_chrome_profile.py
```

The script will:
- Read your Chrome configuration from `.env`
- Validate that the profile exists
- Check for important authentication files
- Copy your profile to the Docker volume
- Preserve cookies, login data, and other authentication files

### Step 3: Verify Profile Copy

The script will show which authentication files were found:
- ✅ Cookies: Contains your login sessions
- ✅ Login Data: Saved passwords
- ✅ Local Storage: Website data
- ✅ Session Storage: Active sessions

### Step 4: Test the Scraper

Start your Docker container:
```bash
docker-compose up -d
```

Run the scraper - it should now skip LinkedIn login!

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CHROME_USER_DATA_DIR` | Path to Chrome's User Data directory | `C:\Users\juans\AppData\Local\Google\Chrome\User Data` |
| `CHROME_PROFILE_DIRECTORY` | Profile folder name within User Data | `Default` or `Profile 1` |
| `CHROME_PATH` | Path to Chrome executable (optional) | `C:\Program Files\Google\Chrome\Application\chrome.exe` |

### Finding Your Profile Directory

To find which profile you use for LinkedIn:

1. Open Chrome and go to `chrome://settings/people`
2. Note which profile you use for LinkedIn
3. The profile names correspond to folder names:
   - First profile: `Default`
   - Second profile: `Profile 1`
   - Third profile: `Profile 2`
   - etc.

### Docker Volume Mapping

Your profile is copied to the Docker volume `chrome-data` which is mounted at `/tmp/chrome-profile` inside the container.

## 🔍 Troubleshooting

### Environment Variable Errors

If you get "CHROME_USER_DATA_DIR not found" error:
1. Make sure your `.env` file exists in the project root
2. Check that the variable names are exactly as shown above
3. Use double backslashes (`\\`) in Windows paths

### Profile Not Found

If you get "Chrome profile not found" error:
1. Verify the `CHROME_USER_DATA_DIR` path exists
2. Check that `CHROME_PROFILE_DIRECTORY` matches an actual folder
3. Run the script to see available profiles

### Profile Lock Issues

If you get "profile in use" errors:
1. Close ALL Chrome windows before copying the profile
2. Make sure no other Chrome processes are running
3. Restart the Docker container: `docker-compose restart`

### Authentication Not Working

If you still need to log in:
1. Verify the profile was copied correctly
2. Check that the Cookies file exists and has data
3. Make sure you're using the correct profile directory

## 🔄 Updating Your Profile

To update your profile with new login data:
1. Log into any new services in your regular Chrome
2. Close Chrome completely
3. Run the copy script again to update the Docker volume

## 🛡️ Security Notes

- Your profile data is only accessible within the Docker container
- The profile is stored in a Docker volume, not directly on the host filesystem
- Consider using a dedicated Chrome profile for scraping activities

## 📝 Example .env Configuration

```env
# Chrome Configuration for LinkedIn Scraper
CHROME_USER_DATA_DIR=C:\Users\juans\ChromeTestEnvironment
CHROME_PROFILE_DIRECTORY=MyTestProfile
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

# Other environment variables
GOOGLE_API_KEY=your_api_key_here
```

## 📝 Manual Alternative

If the script doesn't work, you can manually copy your profile:

1. Find your Chrome profile directory
2. Copy the entire profile folder
3. Use `docker cp` to copy it to the container:
   ```bash
   docker cp /path/to/your/profile/. container_name:/tmp/chrome-profile/
   ```

## ✅ Verification

To verify your profile is working:
1. Check the scraper logs for "Using existing Chrome profile"
2. The scraper should navigate to LinkedIn without showing login prompts
3. You should see your LinkedIn homepage/feed instead of the login page 