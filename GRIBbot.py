import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

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

