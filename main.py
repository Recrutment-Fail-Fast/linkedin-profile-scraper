from fastapi import FastAPI, HTTPException
import uvicorn
from agents.linkedin_to_profile_json import run_agent
from stores.prospect_store import prospect_store
from utils import kill_chrome
from models import Prospect
app = FastAPI()


@app.post("/api/v1/scrape_profile")
async def scrape_profile_endpoint(request: Prospect):
    try:
        prospect_store.prospect = {
            "id": request.id,
            "linkedin_url": request.linkedin_url
        }
        kill_chrome()
        await run_agent()
        return {"status": "success", "message": "Profile scraped and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
