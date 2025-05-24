from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from pydantic import BaseModel, Field
from services import supabase
from stores.prospect import prospect_store


from .prompts import construct_other_job_position_evaluation_prompt
from utils import get_other_job_positions

class OtherPositionEvaluationResult(BaseModel):
    is_fit: bool = Field(description="Whether the prospect is fit for the other job position.")
    llm_evaluation: str = Field(description="The textual evaluation from the LLM.")
    evaluated_position_id: str = Field(description="The ID of the job position that was evaluated.")

async def evaluate_prospect_for_other_positions(
    prospect_resume: str,
):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    output_parser = JsonOutputFunctionsParser(pydantic_schema=OtherPositionEvaluationResult)
    alternative_positions = get_other_job_positions()
    evaluation_prompt = construct_other_job_position_evaluation_prompt(alternative_positions)
    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=evaluation_prompt),
        ("human", "{prospect_resume}")
    ])
    evaluation_chain = chat_prompt | llm.bind_tools([OtherPositionEvaluationResult]) | output_parser
    evaluation_result = evaluation_chain.invoke({"prospect_resume": prospect_resume})

    if evaluation_result.is_fit:
        prospect_id = prospect_store.prospect["prospect_id"]
        supabase.table("prospect_evaluation").insert({
            "prospect_id": prospect_id,
            "job_position_id": evaluation_result.evaluated_position_id,
        }).execute()
        return evaluation_result.evaluated_position_id
    else:
        return None

            
