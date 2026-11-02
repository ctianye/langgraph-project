from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint


@entrypoint(checkpointer=InMemorySaver())
def my_workflow(number: int, *, previous: Any = None) -> int:
    previous = previous or 0
    return number + previous

config = {
    "configurable": {
        "thread_id": "some_thread_id"
    }
}

#首先是传入一个number参数
my_workflow.invoke(1, config)  # 1 (previous was None)
#在第二次操作的时候，上一个previous的值就是上一次的返回值1，所以这里传入2的时候，previous就是1，所以返回值就是3
my_workflow.invoke(2, config)  # 3 (previous was 1 from the previous invocation)



@entrypoint(checkpointer=InMemorySaver())
def my_workflow(number: int, *, previous: Any = None) -> entrypoint.final[int, int]:
    previous = previous or 0
    # This will return the previous value to the caller, saving
    # 2 * number to the checkpoint, which will be used in the next invocation
    # for the `previous` parameter.
    return entrypoint.final(value=previous, save=2 * number)
#value返回给调用者，而save下次同 thread_id 运行时，作为 previous 参数回来，这是一个解耦的操作
config = {
    "configurable": {
        "thread_id": "1"
    }
}

my_workflow.invoke(3, config)  # 0 (previous was None)
my_workflow.invoke(1, config)  # 6 (previous was 3 * 2 from the previous invocation)