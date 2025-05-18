# Linkedin Profile Scraper

This project scrapes LinkedIn profiles using Playwright and integrates with Google AI and Supabase.

---

## Setup Instructions

### 1. Install `uv` (Python package manager)

Open PowerShell and run:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

---

### 2. Create a Virtual Environment

```powershell
uv venv
```

---

### 3. Activate the Virtual Environment

```powershell
.venv\Scripts\activate
```

---

### 4. Install Dependencies

```powershell
uv pip install requirements.txt
```

---

### 5. Install Playwright Browsers

```powershell
playwright install
```

---

### 6. Create a `.env` File

Add the following variables to your `.env` file:

```env
GOOGLE_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
CHROME_PATH=
CHROME_USER_DATA_DIR=
CHROME_PROFILE_DIRECTORY=
```

- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/).
- **SUPABASE_URL** and **SUPABASE_KEY**: Get from your Supabase project settings.

---

### 7. Configure Chrome

1. Open Chrome and go to: `chrome://version/`
2. Set `CHROME_PATH` in your `.env` to the **Executable Path** shown.
3. In `C:\Users\yourUser\`, create a folder for your Chrome environment (e.g., `C:\Users\anakin\ChromeTestEnvironment`).
4. Set `CHROME_USER_DATA_DIR` to this folder path.
5. Inside that folder, create another folder for your Chrome profile (e.g., `MyTestProfile`).
6. Set `CHROME_PROFILE_DIRECTORY` to this profile folder name.

---

### 8. Start Chrome with Remote Debugging

Replace paths and names as needed, then run in PowerShell:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\YourUserName\ChromeTestEnvironment" --profile-directory="MyTestProfile"
```

- Log in to your Chrome profile or create a new one.

---

### 9. Run the Project

Send a POST request to `/api/v1/scrape_profile` with the following JSON body:

```json
{
  "id": "some id (uuid)",
  "linkedin_url": "https://www.linkedin.com/in/obi-wan-kenobi/"
}
```

---

### 10. Expected Response

You should receive a response like:

```json
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
```

---

## Notes

- Make sure all environment variables are set correctly.
- For any issues, check your Chrome paths and profile settings.

---

