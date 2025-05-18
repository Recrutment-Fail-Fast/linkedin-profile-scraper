from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from dotenv import load_dotenv
from initial_actions import initial_actions
from prompts import task, override_system_message, extend_planner_system_message
from models.models import Profile
from browser import browser
import asyncio

load_dotenv()


controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.0)


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