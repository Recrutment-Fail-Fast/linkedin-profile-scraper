from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, validator
from utils import get_evaluation_criteria_and_prospect_profile, store_score_and_evaluation
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from .system_prompt import construct_evaluation_criteria_system_prompt


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

    result = await get_evaluation_criteria_and_prospect_profile(prospect_evaluation_id)

    evaluation_criteria = result["evaluation_criteria"]
    prospect_profile = result["profile_text"]
    system_prompt_content = construct_evaluation_criteria_system_prompt(evaluation_criteria)  # Renamed to avoid conflict
    # Updated prompt template to use a placeholder for the human message
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt_content),
        ("human", "{prospect_profile}") # Using a tuple with a placeholder
    ])

    # Instantiate the parser
    output_parser = JsonOutputFunctionsParser(pydantic_schema=EvaluationOutput)

    # Bind the Pydantic model to the LLM and create the chain
    chain = prompt_template | llm.bind_tools([EvaluationOutput]) | output_parser
    # Invoke the chain by providing the JSON string for the placeholder
    response = chain.invoke({"prospect_profile": prospect_profile})
    store_score_and_evaluation(
        llm_score=response['llm_score'],
        llm_evaluation=response['llm_evaluation'],
        prospect_evaluation_id=prospect_evaluation_id
    )

    return response
    
