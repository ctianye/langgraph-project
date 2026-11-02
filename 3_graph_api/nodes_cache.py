import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy


class State(TypedDict):
    x: int
    result: int


builder = StateGraph(State)


def expensive_node(state: State) -> dict[str, int]:
    # expensive computation
    time.sleep(2)
    return {"result": state["x"] * 2}

#开启内存缓存，设置缓存策略为3秒，意思是说在3秒内再次调用这个节点时，就会直接从缓存中获取结果，而不会重新执行这个节点的逻辑
builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=3))
#这个地方和前面的start，end是一样的
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())

print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}}]
#这里的stream_mode='updates'是指在执行节点时，会返回节点的更新结果，而不是最终的结果，这样可以在节点执行过程中获取到中间结果，然后还有其他的一些参数，具体可以看stream_mode的文档说明
print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}, '__metadata__': {'cached': True}}]