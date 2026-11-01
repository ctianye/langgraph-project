from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class InputState(TypedDict):
    user_input: str


class OutputState(TypedDict):
    graph_output: str


class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str


class PrivateState(TypedDict):
    bar: str


def node_1(state: InputState) -> OverallState:
    # Write to OverallState
    return {"foo": state["user_input"] + " name","chengjianhao":"taiqiangle","graph_output":"chengjianhao"}
#这里的chengjianhao字段其实就不会被识别到,但是graph_output是会被识别到的，因为它在OverallState里面有这个字段，那么就会接收这个字段，会起到过滤的作用


def node_2(state: OverallState) -> PrivateState:
    # Read from OverallState, write to PrivateState
    return {"bar": state["foo"] + " is","chengjianhao":"taiqiangle","graph_output":"chengjianhao"}
#这里的graph_output也不会被识别到，因为其privatestate里面没有这个字段，那么就不会接收这个字段，会起到过滤的作用

def node_3(state: PrivateState) -> OutputState:
    # Read from PrivateState, write to OutputState
    return {"graph_output": state["bar"] + " Lance"}

#对于这个的graph传递的schema（模式），也就是说在里面传入的像字典一样的是什么内容和字段，比如说
#overallstate就是整个图中所存在的，inputshcema就是传入的，那么就是要指定到这个字段，如果说额外再的话，其是不会识别的，可以进行调试验证
builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
res = graph.invoke({"user_input": "My"})

print(res)

# {'graph_output': 'My name is Lance'}