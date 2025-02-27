import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
import panel as pn


# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_API_KEY"] = getpass.getpass()



class GRIBbot:
    def __init__(self):
        print("GRIBbot initialized")
 
    def main(self):
        print("GRIBbot main")

if __name__=="__main__":
    gribbot = GRIBbot()
    gribbot.main()
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

    from langchain.chat_models import init_chat_model

    model = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")
    messages = [
        SystemMessage("Translate the following from English into Italian"),
        HumanMessage("hi!"),
    ]

    print(model.invoke(messages))
    print("done")


    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)


    # Define the function that calls the model
    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}


    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "abc123"}}
    query = "Hi! I'm Bob."

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state

    query = "What's my name?"

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()

    pn.extension()

    pn.panel("Hello World").servable()
    # while True:
    # # Get what the user wants to say
    #     user_input = input("You: ")
        
    #     # Check if the user wants to leave
    #     if user_input.lower() == 'quit':
    #         print("Goodbye!")
    #         break
    #     input_messages = [HumanMessage(user_input)]
    #     output = app.invoke({"messages": input_messages}, config)
    #     output["messages"][-1].pretty_print()

        # for chunk, metadata in app.stream(
        #     {"messages": input_messages, "language": "English"},
        #     config,
        #     stream_mode="messages",
        # ):
        #     if isinstance(chunk, AIMessage):  # Filter to just model responses
        #         print(chunk.content)

            