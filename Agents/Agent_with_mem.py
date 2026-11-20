from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import List, TypedDict, Union
from dotenv import load_dotenv

load_dotenv()

class Chatbot(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2, max_tokens = 500)

def process(state : Chatbot)->Chatbot:
    """ This node will solve the user queries and generate the AI responses!"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\n AI : {response.content}")
    # print(state["messages"])
    return state

graph = StateGraph(Chatbot)
graph.add_node("pr", process)
graph.add_edge(START, "pr")
graph.add_edge("pr", END)
agent = graph.compile()

message_hist = []
query = input("Enter : ")
while query != "exit":
    message_hist.append(HumanMessage(content=query))
    result = agent.invoke({"messages" : message_hist})
    message_hist = result["messages"]
    query = input("Enter : ") 

