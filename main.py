from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from dotenv import load_dotenv
load_dotenv()

import asyncio
from pydantic import BaseModel
from typing import List
# Define the output format as a Pydantic model
class Profile(BaseModel):
    name: str
    title: str
    location: str



class Posts(BaseModel):
	posts: List[Profile]


controller = Controller(output_model=Posts)
llm = ChatOpenAI(model="gpt-4o")

browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # For Windows
    #     chrome_remote_debugging_port=9223, # Use a specific, non-default, non-zero port
    #     # For MAC, an example path would be: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    #     # For Linux, an example path would be: '/usr/bin/google-chrome'
    #     extra_browser_args=[
    #         '--user-data-dir=C:\\Users\\juans\\AppData\\Local\\Google\\Chrome\\User Data', # Corrected path
    #         '--profile-directory=Default',
    #         # '--remote-debugging-port=0'  # Removed from here
    #     ]
    )   
)
initial_actions = [
	{'open_tab': {'url': 'https://www.linkedin.com/in/camila-rivera-arenas-68361b2aa/'}},
]

async def main():
    agent = Agent(
        task="go to camila's Linkedin and get the name and title",
        llm=llm,
        browser=browser,
		controller=controller,
		initial_actions=initial_actions
    )
    result = await agent.run()
    print(result.final_result())
    await browser.close()

asyncio.run(main())