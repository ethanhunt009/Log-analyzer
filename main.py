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
    agent.update_suricata_rule_tool,
]

def init():
    load_dotenv()
    filterwarnings("ignore")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)


CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE_NAME = "chathistory"
COLLECTION_NAME = "chat"
SESSION_ID = "session_1"

chat_history = MongoDBChatMessageHistory(
    connection_string = CONNECTION_STRING,
    database_name = DATABASE_NAME,
    collection_name = COLLECTION_NAME,
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
    user_input = input("read the suricata log file and check for any anomaly or error, if you find the need to update the suricata rules then update it, and create a report of this. Only read the new log, do not read alread read ones, are you clear about this? then it is okay")
    while True:
        response = call_gemini(user_input)
        print(f"Response: {response}")
        time.wait(1000*60*5)
        end = time.time() 
        print(f"Time taken: {end - start} seconds")
        
chat()