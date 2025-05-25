from agents.scrape_linkedin_profile.browser import create_browser
from .initial_actions import get_initial_actions
from .prompts import task, override_system_message, extend_planner_system_message
from models import Profile
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from utils.store_scraped_profile import store_scraped_profile
from dotenv import load_dotenv

load_dotenv()

controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)


async def scrape_linkedin_profile_agent():
    """Scrape LinkedIn profile using browser automation agent."""
    try:
        # Create browser instance
        
        # Create and run agent
        print("🤖 Creating browser agent...")
        agent = Agent(
            task=task,
            llm=llm,
            browser=create_browser(),
            controller=controller,
            initial_actions=get_initial_actions(),
            override_system_message=override_system_message,
            extend_planner_system_message=extend_planner_system_message
        )
        
        print("▶️ Running browser agent...")
        result = await agent.run()
        
        # Store the scraped profile
        print("💾 Storing scraped profile...")
        result = store_scraped_profile(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error in scrape_linkedin_profile_agent: {e}")
        raise
    finally:
        # Always close browser if it was created
        if browser_instance:
            try:
                print("🔒 Closing browser...")
                await browser_instance.close()
            except Exception as e:
                print(f"Warning: Error closing browser: {e}")
    