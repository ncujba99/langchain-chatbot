import asyncio
import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from fastapi import WebSocket


@tool
async def search_tool(query: str):
    """Elastic search query"""
    print(query)
    await asyncio.sleep(100)
    return {"status": ""}

# Store session-based chat history
session_history = {}

today = datetime.datetime.today().strftime("%D")
prompt = ChatPromptTemplate(
    [
        ("system", f"You are a helpful assistant. The date today is {today}."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini", streaming=True)
llm_with_tools = model.bind_tools([search_tool])
llm_chain = prompt | llm_with_tools


async def tool_chain(user_input: str, session_id: str):
    if session_id not in session_history:
        session_history[session_id] = []
    
    history = session_history[session_id]
    history.append(HumanMessage(content=user_input))

    ai_msg = await llm_chain.ainvoke({"user_input": user_input})

    if ai_msg.tool_calls:
        yield "searching in www \n \n "
        tool_msgs = await search_tool.abatch(ai_msg.tool_calls)
        history.extend([ai_msg, *tool_msgs])

    buffer = ""
    
    async for token in llm_chain.astream(
        {"user_input": user_input, "messages": history}
    ):
        yield token.content
        buffer += token.content

    history.append(AIMessage(content=buffer))

async def stream_response(user_input: str, ws: WebSocket, session_id: str ):
    await ws.send_text(f"Session ID: {session_id}")
    async for token in tool_chain(user_input, session_id):
        await ws.send_text(token)