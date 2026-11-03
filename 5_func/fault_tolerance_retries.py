from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import RetryPolicy

def mock_llm(state: MessagesState):
    print("hello")
    #在有些错误中，是触发重试策略的，同时在网络中只有5XX的错误才会触发重试策略，其他的错误不会触发重试策略
    #raise ValueError
    raise ConnectionError("Connection error occurred")
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
#在添加节点时可定义重试策略，max_attempts表示最大尝试次数，默认是1，也就是不重试
#然后在RetryPolicy中还可以定义其他的参数，比如backoff_factor，表示每次重试的间隔时间，单位是秒，默认是0，也就是不等待
graph.add_node(mock_llm,retry_policy=RetryPolicy(max_attempts=3),)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

res = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

print(res)