from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import TimeoutPolicy
import asyncio
from langgraph.types import RetryPolicy

async def mock_llm(state: MessagesState):
    print("hello")
    await asyncio.sleep(3)  # Simulate a long-running task that exceeds the timeout
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
#还可以以timedelta传入一个数字（秒等），或者TimeoutPolicy对象来设置独立的运行和空闲限制
#然后可以以timeout来触发RetryPolicy的重试策略，timeout表示在这个时间内没有返回结果，就会触发重试策略
graph.add_node(mock_llm,retry_policy=RetryPolicy(max_attempts=3), timeout=2)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

asyncio.run(graph.ainvoke({"messages": [{"role": "user", "content": "hi!"}]}))