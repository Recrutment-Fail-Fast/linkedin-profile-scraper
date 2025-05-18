from initial_actions import get_initial_actions
from prompts import task, override_system_message, extend_planner_system_message
from models import Profile
from browser import browser
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from utils.prospects import store_scraped_profile
from dotenv import load_dotenv

load_dotenv()

controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.0)


async def run_agent():
    agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
		controller=controller,
		initial_actions=get_initial_actions(),
		override_system_message=override_system_message,
		extend_planner_system_message=extend_planner_system_message
    )
    result = await agent.run()
    await browser.close()
    store_scraped_profile(result)