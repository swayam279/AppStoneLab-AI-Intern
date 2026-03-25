import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()

model= ChatMistralAI(model='mistral-medium-2508')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages= state['messages']
    response= model.invoke(messages)
    
    return {'messages': [response]}

conn= sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpoint= SqliteSaver(conn= conn)

graph= StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot= graph.compile(checkpointer= checkpoint)

def retrieve_all_threads():
    
    all_threads= set()
    for cpt in checkpoint.list(None):
        all_threads.add(cpt.config['configurable']['thread_id'])
    
    return list(all_threads)