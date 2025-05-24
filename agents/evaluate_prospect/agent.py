from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, validator
from agents.other_job_position_evaluation.agent import evaluate_prospect_for_other_positions
from utils import get_job_evaluation_data, store_score_and_evaluation
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from .system_prompt import construct_evaluation_criteria_system_prompt
from models import EvaluationResponse


class EvaluationOutput(BaseModel):
    llm_score: float = Field(
        description="The score assigned by the LLM. Must be between 0 and 1 with exactly two decimal places.",
        ge=0.0,
        le=1.0
    )
    llm_evaluation: str = Field(description="The textual evaluation from the LLM.")
    
    @validator('llm_score')
    def validate_decimal_places(cls, v):
        # Check if score has exactly two decimal places
        str_v = str(v)
        if '.' in str_v:
            decimal_part = str_v.split('.')[1]
            if len(decimal_part) != 2:
                raise ValueError('llm_score must have exactly two decimal places')
        else:
            # If it's a whole number, format it with two decimal places
            v = float(f"{v:.2f}")
        return v

# The user_input is expected to be a dictionary (e.g., profile_dict)
async def evaluate_prospect_agent(prospect_evaluation_id: str):
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.3)
    output_parser = JsonOutputFunctionsParser(pydantic_schema=EvaluationOutput)


    initial_job_data = get_job_evaluation_data(prospect_evaluation_id)
    
    evaluation_criteria = initial_job_data["evaluation_criteria"]
    prospect_profile = initial_job_data["profile_text"]
    job_score_threshold = initial_job_data["llm_score_threshold"]


    try:
        system_prompt_content = construct_evaluation_criteria_system_prompt(evaluation_criteria)
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt_content),
            ("human", "{prospect_profile}") # Using a tuple with a placeholder
        ])

        chain = prompt_template | llm.bind_tools([EvaluationOutput]) | output_parser
        evaluation = chain.invoke({"prospect_profile": prospect_profile})

        store_score_and_evaluation(
            llm_score=evaluation["llm_score"],
            llm_evaluation=evaluation["llm_evaluation"],
            prospect_evaluation_id=prospect_evaluation_id
        )

        if evaluation["llm_score"] < job_score_threshold:
            other_position_id = await evaluate_prospect_for_other_positions(
                prospect_resume=prospect_profile,
            )
            if other_position_id:
                await evaluate_prospect_agent(prospect_evaluation_id=other_position_id)
            else:
                return EvaluationResponse(
                    success=False, 
                    message="Prospect is not fit for the job and no other position found"
                )
        else:
            return EvaluationResponse(
                success=True, 
                message="Prospect is fit for the job"
            )



    except Exception as e:
        print(f"Error storing initial evaluation for prospect_evaluation_id {prospect_evaluation_id}: {e}")
    
