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
	{'open_tab': {'url': 'https://www.linkedin.com/in/nicole-murillo-fonseca-1b53582b3/'}},
    {'scroll_down': {'amount': 1000}}

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
    pre_parsed_data = result.final_result()
    await browser.close()
    data: Profile = Profile.model_validate_json(pre_parsed_data)
    print(data)

asyncio.run(main())