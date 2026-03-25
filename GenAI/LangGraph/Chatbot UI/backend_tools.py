import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import BaseMessage
from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph  # noqa: F401
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

model= ChatMistralAI(model='mistral-medium-2508')

# Tools --------------------------------------------------------------------------------------------------------------------

search_tool= DuckDuckGoSearchRun(region= "us-en")

@tool
def calculator(a: float, b: float) -> float:
    """ 
    It is compulsary to use this tool whenever any calculations are to be performed.
    """
    add= a + b
    return {'a':a, 'b':b, 'result': add}

tools= [search_tool, calculator]

model_with_tools= model.bind_tools(tools)

# --------------------------------------------------------------------------------------------------------------------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages= state['messages']
    response= model_with_tools.invoke(messages)
    
    return {'messages': [response]}

tool_node= ToolNode(tools)

conn= sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpoint= SqliteSaver(conn= conn)

graph= StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot= graph.compile(checkpointer= checkpoint)

def retrieve_all_threads():
    
    all_threads= set()
    for cpt in checkpoint.list(None):
        all_threads.add(cpt.config['configurable']['thread_id'])
    
    return list(all_threads)
