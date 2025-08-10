from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import time
from warnings import filterwarnings
import agent 
from langchain.agents import initialize_agent, AgentType

tool_list  =[
    agent.suricata_tool,
    agent.report_anomaly_tool,
    agent.report_error_tool,
    agent.update_suricata_tool,
]

def init():
    load_dotenv()
    filterwarnings("ignore")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)


CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE_NAME = "LOG"
COLLECTION_NAME = "LOGGING"
SESSION_ID = "session_1"

chat_history = MongoDBChatMessageHistory(
    connection_string = CONNECTION_STRING,
    database = DATABASE_NAME,
    collection = COLLECTION_NAME,
    session_id = SESSION_ID,
    create_index=True,
)

gemini_agent = initialize_agent(
    tools=tool_list,
    llm=init(),
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    chat_history=chat_history,
)


def call_gemini(query: str):
    """Call the Gemini agent with a query"""
    try:
        response = gemini_agent.run(query)
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def chat():
    start=time.time()
    user_input = input("Enter your query: ")
    while user_input.lower() != "exit":
        response = call_gemini(user_input)
        print(f"Response: {response}")
        user_input = input("Enter your query: ")
        end = time.time() 
        print(f"Time taken: {end - start} seconds")
        
chat()