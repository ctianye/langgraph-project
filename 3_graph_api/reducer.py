from typing import Annotated
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Overwrite
from typing_extensions import TypedDict

#当注释掉后 默认为覆盖的情况
def append_strings(left: list[str], right: list[str]) -> list[str]:
    """Combine the existing state value (left) with a node update (right)."""
    return left + right


class State(TypedDict):
    tags: Annotated[list[str], append_strings]  # Use the append_strings function to combine lists

def node_1(state: State) -> State:
    return {"tags": ["2"]}

#这样的话就是先是1，然后变为[1,2],同时又经过node2 然后因为overwrite就变成[]了
def node_2(state: State) -> State:
    return {"tags": Overwrite([])}

graph = StateGraph(State)
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

graph = graph.compile()

res = graph.invoke({"tags": ["1"]})

print(res)  #如果有 append_strings函数时，{'tags': ['1', '2']}，默认覆盖为 {'tags': ['2']}