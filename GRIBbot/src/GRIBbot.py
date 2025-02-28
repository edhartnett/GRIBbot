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

    from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # List of PDFs to process
    #pdf_files = ["GRIB2-for-DUMMIES.pdf", "WMO-306-v-I-2-2023_en.pdf"] 
    pdf_files = ["GRIB2-for-DUMMIES.pdf"] 

    # Websites to ingest
    web_pages = [
        "https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/",
        "https://noaa-emc.github.io/NCEPLIBS-g2c/",
        "https://noaa-emc.github.io/NCEPLIBS-g2/",
    ]

    # Load and combine all documents
    all_documents = []

    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        all_documents.extend(documents)

    # Load web pages
    for page_url in web_pages:
        loader = WebBaseLoader(page_url)
        documents = loader.load()
        for doc in documents:
            doc.metadata["source"] = page_url  # Track source URL
        all_documents.extend(documents)
    
    # Split all documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(all_documents)    # Step 1: Load PDF file

    # Step 3: Use HuggingFace embeddings (you can choose a different embedding model if needed)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Step 4: Store embeddings into a FAISS vector database
    vector_store = FAISS.from_documents(docs, embedding_model)

    # Optional: Save the FAISS index to disk for later use
    vector_store.save_local("faiss_index")

    print("PDFs and websites have been processed and stored in FAISS vector store.")
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

    from langchain.chat_models import init_chat_model

    model = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")
    # messages = [
    #     SystemMessage("Translate the following from English into Italian"),
    #     HumanMessage("hi!"),
    # ]

    # print(model.invoke(messages))
    # print("done")


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
    # query = "Hi! I'm Bob."

    # input_messages = [HumanMessage(query)]
    # output = app.invoke({"messages": input_messages}, config)
    # output["messages"][-1].pretty_print()  # output contains all messages in state

    # query = "What's my name?"

    # input_messages = [HumanMessage(query)]
    # output = app.invoke({"messages": input_messages}, config)
    # output["messages"][-1].pretty_print()
    prompt = """
    You are a helpful assistant. You answer questions about GRIB and 
    other data formats. For any other kind of question, you reply that 
    you only answer questions about GRIB.\n Use the following context to answer 
    the question:\n {context}\n Answer this question:\n {text} 
    """
    pn.extension()
    def get_response(contents, user, instance):
        # Perform similarity search on the vector store using the user's question
        retrieved_docs = vector_store.similarity_search(contents, k=5)

        # Combine the content of retrieved documents into a context string
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        input_messages = [HumanMessage(prompt.format(context=context, text=contents))]
        #print(input_messages)
        output = app.invoke({"messages": input_messages}, config)
        response = output["messages"][-1].content
        return response

    intro = "I am a chatbot that can answer questions the GRIB data format."
    chat_bot = pn.chat.ChatInterface(callback=get_response)
    chat_bot.send(intro, user="Assistant", respond=False)
    chat_bot.show()
    chat_bot.servable()
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

            