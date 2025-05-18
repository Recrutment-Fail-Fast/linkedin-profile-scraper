from fastapi import FastAPI, HTTPException
import uvicorn
from stores.prospect_store import prospect_store
from utils import get_prospect_to_scrape, run_agent
from utils import kill_chrome
from models import ScrapeRequest
app = FastAPI()


@app.post("/api/v1/scrape_profile")
async def scrape_profile_endpoint(request: ScrapeRequest):
    try:
        prospect_store.prospect = get_prospect_to_scrape(request.id)
        kill_chrome()
        await run_agent()
        return {"status": "success", "message": "Profile scraped and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
