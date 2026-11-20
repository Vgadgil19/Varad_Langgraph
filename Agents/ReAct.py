from langchain_openai import ChatOpenAI
from typing import TypedDict, Sequence, List, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, AIMessage,  HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2, max_tokens = 500)


class Agentstate(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a : int, b : int):
    """ This is the tool which adds two numbers"""
    return a + b

@tool
def mul(a : int, b : int):
    """ This is the tool which multiplies two numbers"""
    return a * b

@tool 
def sub(a : int, b : int):
    """ This is the tool which subreacts two numbers"""
    return a - b

tools = [add,sub, mul]
model = llm.bind_tools(tools=tools)
def model_call(state : Agentstate)->Agentstate:
    sys_prompt = SystemMessage(content= "You are my AI Assistant please answer my query to the best of your ability")
    response = model.invoke([sys_prompt] + state["messages"])
    return {"messages" : [response]}

def should_cont(state : Agentstate):
    messages = state["messages"]
    last_mess = messages[-1]
    if not last_mess.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(Agentstate)
graph.add_node("agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools_node", tool_node)
graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_cont,
    {
        "continue" : "tools_node",
        "end" : END
    },
)

graph.add_edge("tools_node", "agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1] 
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages" : [("user", "Add 2 numbers 48 + 56 and multiply the result with 6 also tell me one amazing fact about geopolitics.")]}
print_stream(app.stream(inputs, stream_mode="values"))  


