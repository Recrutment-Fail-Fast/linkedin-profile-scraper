from pydantic import BaseModel, Field
from typing import Optional

class Prospect(BaseModel):
    prospect_id: str = Field(..., description="Unique identifier for the prospect")
    linkedin_url: str = Field(..., description="LinkedIn profile URL of the prospect") 
    prospect_evaluation_id: str = Field(..., description="Unique identifier for the evaluation process")

class EvaluationResponse(BaseModel):
    success: bool = Field(..., description="Whether the evaluation was successful")
    message: str = Field(..., description="Descriptive message about the evaluation result")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message describing what went wrong")
