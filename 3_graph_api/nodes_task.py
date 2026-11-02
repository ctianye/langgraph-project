from typing import NotRequired

import requests
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    urls: list[str]
    results: NotRequired[list[str]]

#使用装饰器来进行任务的定义，任务的作用就是能够在完成一个任务后及时的对其进行检查点的存储，避免中断后的重新执行
@task
def _make_request(url: str):
    """Make a request."""
    return requests.get(url).text[:100]


def call_api(state: State):
    """Example node that makes API requests as checkpointed tasks."""
    futures = [_make_request(url) for url in state["urls"]]
    results = [f.result() for f in futures]
    return {"results": results}


builder = StateGraph(State)
builder.add_node("call_api", call_api)
builder.add_edge(START, "call_api")
builder.add_edge("call_api", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}

res = graph.invoke({"urls": ["https://www.baidu.com"]}, config)

print(res)