from dataclasses import dataclass
from typing_extensions import TypedDict

from langgraph.graph import StateGraph,END, START
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig

class State(TypedDict):
    input: str
    results: str

@dataclass
class Context:
    user_id: str

builder = StateGraph(State, context_schema=Context)

def plain_node(state: State):
    return state

#通过runtime可以获取context里面的的内容，这里context里面是user_id
def node_with_runtime(state: State, runtime: Runtime[Context],config:RunnableConfig):
    print("In node: ", runtime.context.user_id)
    return {"results": f"Hello, {state['input']}!"}

#而线程id是通过config中获取的，也就是其config来获取,这里是新版本 直接可以用runtime.execution_info.thread_id来进行获取
def node_with_execution_info(state: State, runtime: Runtime):
    print("In node with thread_id: ", runtime.execution_info.thread_id)
    return {"results": f"Hello, {state['input']}!"}


builder.add_node("plain_node", plain_node)
builder.add_node("node_with_runtime", node_with_runtime)
builder.add_node("node_with_execution_info", node_with_execution_info)
builder.add_edge(START, "plain_node")
builder.add_edge("plain_node", "node_with_runtime")
builder.add_edge("node_with_runtime", "node_with_execution_info")
builder.add_edge("node_with_execution_info", END)

graph = builder.compile()

res = graph.invoke({"input":"你好！"}, context=Context(user_id="u_123456"),config = {"configurable": {"thread_id": "customer_12"}})
print(res)