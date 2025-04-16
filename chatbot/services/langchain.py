from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from fastapi import WebSocket

from services.elasticsearch import product_search_tool


session_history = {}

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant. Use product search results to provide natural responses. Here are the prior messages: {messages}."),
        ("human", "{user_input}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini", streaming=True)
llm_with_tools = model.bind_tools([product_search_tool])
llm_chain = prompt | llm_with_tools


async def stream_response(user_input: str, ws: WebSocket, session_id: str ):

    if session_id not in session_history:
        session_history[session_id] = []
    
    history = session_history[session_id]
    history.append(HumanMessage(content=user_input))

    ai_msg = await llm_chain.ainvoke({"user_input": user_input, "messages": history})

    if ai_msg.tool_calls:
        await ws.send_text("calling tools")
        tool_msgs = await product_search_tool.abatch(ai_msg.tool_calls)
        history.extend([ai_msg, *tool_msgs])

    buffer = ""
    
    async for token in llm_chain.astream(
        {"user_input": user_input, "messages": history}
    ):
        await ws.send_text(token.content)
        buffer += token.content

    history.append(AIMessage(content=buffer))

