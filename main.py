from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from dotenv import load_dotenv
load_dotenv()

import asyncio
from pydantic import BaseModel
from typing import List
class Profile(BaseModel):
    name: str
    title: str
    location: str





controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# main.py
# ...
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

prompt = """
Go to the profile of camila rivera and get the name, title and location
"""


initial_actions = [
	{'open_tab': {'url': 'https://www.linkedin.com/in/camila-rivera-arenas-68361b2aa/'}},
]

async def main():
    agent = Agent(
        task=prompt,
        llm=llm,
        browser=browser,
		controller=controller,
		initial_actions=initial_actions
    )
    result = await agent.run()
    print(result.final_result())
    await browser.close()

asyncio.run(main())