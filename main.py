from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import uvicorn
from agents.evaluate_prospect.agent import evaluate_prospect_agent
from agents.scrape_linkedin_profile.agent import scrape_linkedin_profile_agent
from stores.prospect import prospect_store
from utils import kill_chrome
from models import Prospect, EvaluationResponse, ErrorResponse

app = FastAPI(
    title="LinkedIn Profile Scraper & Prospect Evaluator",
    description="API for scraping LinkedIn profiles and evaluating prospects for job positions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.post(
    "/api/v1/evaluate_prospect",
    response_model=EvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate a prospect for a job position",
    description="""
    This endpoint scrapes a LinkedIn profile and evaluates the prospect against specific job criteria.
    
    The process includes:
    1. Scraping the LinkedIn profile data
    2. Evaluating the prospect against job requirements
    3. Returning success/failure with descriptive message
    
    If the prospect doesn't meet the main job requirements, the system will attempt to find 
    alternative positions that might be a better fit.
    """,
    responses={
        200: {
            "description": "Evaluation completed successfully",
            "model": EvaluationResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful evaluation",
                            "value": {
                                "success": True,
                                "message": "Prospect is fit for the job"
                            }
                        },
                        "no_fit": {
                            "summary": "Prospect not suitable",
                            "value": {
                                "success": False,
                                "message": "Prospect is not fit for the job and no other position found"
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error in request data",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error during evaluation process",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error occurred during LinkedIn profile scraping or evaluation"
                    }
                }
            }
        }
    },
    tags=["Prospect Evaluation"]
)
async def evaluate_prospect_endpoint(
    request: Prospect
) -> EvaluationResponse:
    """
    Evaluate a prospect for a specific job position.
    
    Args:
        request: Prospect data containing LinkedIn URL and evaluation IDs
        
    Returns:
        EvaluationResponse: Result of the evaluation process
        
    Raises:
        HTTPException: If evaluation process fails
    """
    try:
        prospect_store.prospect = {
            "prospect_id": request.prospect_id,
            "linkedin_url": request.linkedin_url
        }
        kill_chrome()
        await scrape_linkedin_profile_agent()
        result = await evaluate_prospect_agent(request.prospect_evaluation_id)
        return EvaluationResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Evaluation process failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
