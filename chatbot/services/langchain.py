import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, chain
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from fastapi import WebSocket


today = datetime.datetime.today().strftime("%D")
prompt = ChatPromptTemplate(
    [
        ("system", f"You are a helpful assistant. The date today is {today}."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini", streaming=True)
search_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
)


llm_with_tools = model.bind_tools([search_tool])
llm_chain = prompt | llm_with_tools

history = []


@chain
def tool_chain(user_input: str, config: RunnableConfig):
    history.append(HumanMessage(content=user_input))

    ai_msg = llm_chain.invoke({"user_input": user_input}, config=config)
    if ai_msg.tool_calls:
        yield "searching in www \n \n "
        tool_msgs = search_tool.batch(ai_msg.tool_calls, config=config)
        history.extend([ai_msg, *tool_msgs])

    bufer = ""

    for token in llm_chain.stream(
        {"user_input": user_input, "messages": history}, config=config
    ):
        yield token.content
        bufer = bufer + token.content
    history.append(AIMessage(content=bufer))


async def stream_response(user_input: str, ws: WebSocket):
    tokens = tool_chain.stream(user_input)

    for token in tokens:
        await ws.send_text(token)
