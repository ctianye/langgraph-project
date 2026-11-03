from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.chat_models import init_chat_model
import os

model = init_chat_model("openai:sensenova-6.8-flash-lite",
    api_key=os.getenv("SENSENOVA_API_KEY", "your-api-key-here"),
    base_url="https://token.sensenova.cn/v1",)

def llm(state: MessagesState):
    ai_msg = model.invoke(state["messages"])
    return {"messages": [ai_msg]}

graph = StateGraph(MessagesState)
graph.add_node(llm)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)
graph = graph.compile()

stream = graph.stream_events({
    "messages": [{"role": "user", "content": "What is 42 * 17?"}],
}, version="v3")

for val in stream.values:
    print(val, end="", flush=True)

final_state = stream.output