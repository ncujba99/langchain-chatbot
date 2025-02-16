from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableConfig, chain
# from langchain_core.messages import HumanMessage, AIMessage

# from langchain_core.runnables import RunnableConfig, chain

from fastapi import WebSocket


from langchain_ollama import ChatOllama

from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field



from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


model = ChatOllama(
    model="deepseek-r1:8b",
    base_url="http://ollama:11434",
    streaming=True,
    temperature=0.1
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{user_input}"),
        ("placeholder", "{messages}")
    ]
)

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return "unable to recive a response"


app = create_react_agent(
    model=model, 
    tools=[search],
    checkpointer=MemorySaver(),
    prompt=prompt
)



def tool_chain(user_input: str):

    for token in app.stream(
        {"user_input": user_input},
            config={"configurable": {"thread_id": 42}}
    ):
        yield token


async def stream_response(user_input: str, ws: WebSocket):    
    for token in tool_chain(user_input):
        await ws.send_text(token)
