from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from dotenv import load_dotenv
from prompts import task, override_system_message, extend_planner_system_message
from models import Profile
from browser import browser
load_dotenv()

import asyncio

controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


initial_actions = [
	{'open_tab': {'url': 'https://www.linkedin.com/in/nicoll-fern%C3%A1ndez-90a350190/'}},
]

async def main():
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
		controller=controller,
		initial_actions=initial_actions,
		override_system_message=override_system_message,
		extend_planner_system_message=extend_planner_system_message
    )
    result = await agent.run()
    print(result.final_result())
    await browser.close()

asyncio.run(main())