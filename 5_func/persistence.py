from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.runtime import Runtime

checkpointer = InMemorySaver()
store = InMemoryStore()

def mock_llm(state: MessagesState,runtime:Runtime):
#通过打印状态 我们可以看见同一个线程的情况下，状态是会被保存下来的，这样就可以在下一次调用的时候继续使用上一次的状态，而不是重新开始
    #print(state)
    store = runtime.store
#第一次第一个线程get时其实是没有memories，但是第二个线程get时是有memories的，因为第一个线程已经put了，所以第二个线程就可以获取到
    print(store.get(("memories",), "user_bob"))
    store.put(("memories",), "user_bob", {"memory": "User's name is Bob"})
    return {"messages": [{"role": "ai", "content": "hello world"}]}


builder = StateGraph(MessagesState)
builder.add_node("llm", mock_llm)
builder.add_edge(START, "llm")
builder.add_edge("llm", END)

graph = builder.compile(checkpointer=checkpointer, store=store)

result = graph.invoke(
    {"messages": [{"role": "user", "content": "Hi, my name is Bob."}]},
    {"configurable": {"thread_id": "thread-1"}},
)

result = graph.invoke(
    {"messages": [{"role": "user", "content": "hello"}]},
    {"configurable": {"thread_id": "thread-2"}},
)