from langgraph.types import Command

from agent import app

initial_state = {
    "email_content": "I was charged twice for my subscription! This is urgent!",
}

config = {"configurable": {"thread_id": "customer_12"}}

res = app.invoke(initial_state,config)

human_response = Command(
    resume={
        "approved": True,
        "edited_response": "We sincerely apologize for the double charge. I've initiated an immediate refund...",
    }
)
res2 = app.invoke(human_response,config=config)
print(res2)