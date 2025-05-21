from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from .system_prompt import system_prompt

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.3)

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt), # System message defined here
    HumanMessage(content="{input}")
])

# Using LangChain Expression Language (LCEL)
chain = prompt_template | llm

def profile_json_to_profile_text(user_input):
    response = chain.invoke({
        "input": user_input
    })
    return response.content


    
