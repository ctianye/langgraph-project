from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import interrupt
import time
from langgraph.types import Command

#这里使用装饰器来对其进行一个任务的定义，同时任务必须是在这几点中定义的，才能被工作流所使用：entrypoint, 其他的task,以及图的节点中
@task
def write_essay(topic: str) -> str:
    """Write an essay about the given topic."""
    time.sleep(1) # A placeholder for a long-running task.
    return f"An essay about topic: {topic}"

#使用entrypoint装饰器来定义，将这个函数装饰成一个入口点，这样就可以在外部调用这个函数来启动整个工作流
@entrypoint(checkpointer=InMemorySaver())
def workflow(topic: str) -> dict:
    """A simple workflow that writes an essay and asks for a review."""
    essay = write_essay("cat").result()
    is_approved = interrupt({
        # Any json-serializable payload provided to interrupt as argument.
        # It will be surfaced on the client side as an Interrupt when streaming data
        # from the workflow.
        "essay": essay, # The essay we want reviewed.
        # We can add any additional information that we need.
        # For example, introduce a key called "action" with some instructions.
        "action": "Please approve/reject the essay",
    })

    return {
        "essay": essay, # The essay that was generated
        "is_approved": is_approved, # Response from HIL
    }

# thread_id = str(uuid7())
config = {"configurable": {"thread_id": "1"}}
#因为前面使用装饰器后 这里成为一个入口，就可以使用stream_events来进行调用，stream_events是一个异步的调用方式，可以在执行过程中获取到中间结果
#同时也可以使用invoke来进行调用，invoke是一个同步的调用方式，执行完后才会返回结果
# stream = workflow.stream_events("cat", config, version="v3")
# _ = stream.output
#其实这里调用到interrupt后，就会返回一个中断的结果，这个中断的结果就是一个Interrupt对象，里面包含了中断的相关信息，比如中断的类型，中断的值，中断的时间等等
# print({"write_essay": stream.interrupts[0].value["essay"]})
# print({"__interrupt__": stream.interrupts})
# {'write_essay': 'An essay about topic: cat'}

res = workflow.invoke("cat", config, version="v3")
#在这里就可以继续让中断继续，同时因为装饰器task的存在，第二次的调用不会再次执行任务，可以通过打断点来判断
res2 = workflow.invoke(Command(resume="approve"), config, version="v3")

print(res)
print(res2)