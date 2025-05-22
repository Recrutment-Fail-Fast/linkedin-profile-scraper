from pydantic import BaseModel

class Prospect(BaseModel):
    prospect_id: str
    linkedin_url: str
    prospect_evaluation_id: str
