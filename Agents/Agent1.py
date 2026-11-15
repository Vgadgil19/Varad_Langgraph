from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import List, TypedDict
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2, max_tokens = 500)

class AgentState(TypedDict):
    messages : List[HumanMessage]

def process(state : AgentState)->AgentState:
    response = llm.invoke(state["messages"])
    print(f"\n AI : {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("pr", process)
graph.add_edge(START, "pr")
graph.add_edge("pr", END)
agent = graph.compile()

query = input("Enter : ")
while query != "Exit":
    agent.invoke({"messages" : [HumanMessage(content=query)]})
    query = input("Enter : ")