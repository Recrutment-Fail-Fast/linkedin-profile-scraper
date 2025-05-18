from pydantic import BaseModel

class Prospect(BaseModel):
    id: str
    linkedin_url: str
