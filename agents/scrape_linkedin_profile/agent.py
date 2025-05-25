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
    browser_session = None
    try:
        # Create browser session using existing Chrome profile
        print("🔄 Creating browser session with existing Chrome profile...")
        browser_session = await create_browser()
        
        # Create and run agent
        print("🤖 Creating browser agent...")
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session,
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
        # Clean up browser session if it was created
        if browser_session:
            try:
                print("🧹 Cleaning up browser session...")
                # Note: We might want to keep the session alive for reuse
                await browser_session.close()
                print("ℹ️ Browser session closed")
            except Exception as cleanup_error:
                print(f"⚠️ Error during browser cleanup: {cleanup_error}")
    