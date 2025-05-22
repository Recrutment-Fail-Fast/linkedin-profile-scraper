from fastapi import FastAPI, HTTPException
import uvicorn
from agents.evaluate_prospect.agent import evaluate_prospect_agent
from agents.scrape_linkedin_profile.agent import scrape_linkedin_profile_agent
from stores.prospect import prospect_store
from utils import kill_chrome
from models import Prospect
app = FastAPI()


@app.post("/api/v1/evaluate_prospect")
async def evaluate_prospect_endpoint(request: Prospect):
    try:
        prospect_store.prospect = {
            "id": request.prospect_id,
            "linkedin_url": request.linkedin_url
        }
        kill_chrome()
        await scrape_linkedin_profile_agent()
        await evaluate_prospect_agent(request.prospect_evaluation_id)
        return {"status": "success", "message": "Profile scraped and evaluated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
