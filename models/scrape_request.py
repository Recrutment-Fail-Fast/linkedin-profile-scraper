from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    id: str