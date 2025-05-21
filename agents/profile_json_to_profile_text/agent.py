import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from .system_prompt import system_prompt


# The user_input is expected to be a dictionary (e.g., profile_dict)
def profile_json_to_profile_text(user_input: dict):
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.3)

    # Convert the input dictionary to a JSON string
    # This string will be the actual input to the language model
    profile_json_string = json.dumps(user_input, indent=2)

    # Updated prompt template to use a placeholder for the human message
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        ("human", "{profile_data_as_json}") # Using a tuple with a placeholder
    ])

    # Using LangChain Expression Language (LCEL)
    chain = prompt_template | llm
    # Invoke the chain by providing the JSON string for the placeholder
    response = chain.invoke({"profile_data_as_json": profile_json_string})
    return response.content


    
