from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List

class AgentState(TypedDict):
    num1 : int
    num2 : int
    num3 : int
    num4 : int
    finalnum1 : int
    finalnum2 : int
    op1 : str
    op2 : str
    res : str

def add1(state : AgentState)->AgentState:
    """This node adds first 2 nums"""
    state["finalnum1"] = state["num1"] + state["num2"]
    return state

def sub1(state : AgentState)->AgentState:
    """This node subtracts first 2 nums"""
    state["finalnum1"] = state["num1"] - state["num2"]
    return state

def add2(state : AgentState)->AgentState:
    """This node adds next 2 nums"""
    state["finalnum2"] = state["num3"] + state["num4"]
    return state

def sub2(state : AgentState)->AgentState:
    """This node subtracts next 2 nums"""
    state["finalnum2"] = state["num3"] - state["num4"]
    return state

def next_node_decider1(state : AgentState)->AgentState:
    """This node decides whether to perform addition or subtraction for first set of inputs"""
    if state["op1"] == "+":
        return "add_op1"
    elif state["op1"] == "-":
        return "sub_op1"

def next_node_decider2(state : AgentState)->AgentState:
    """This node decides whether to perform addition or subtraction for next set of inputs"""
    if state["op2"] == "+":
        return "add_op2"
    elif state["op2"] == "-":
        return "sub_op2"

def last_node(state : AgentState) -> AgentState:
    """ this node returns output in proper string format"""
    state["res"] = f"As per given inputs, {state["num1"]} {state["op1"]} {state["num2"]} = {state["finalnum1"]} whereas, {state["num3"]} {state["op2"]} {state["num4"]} = {state["finalnum2"]} "
    return state
    
    
graph  = StateGraph(AgentState)
graph.add_node("add1", add1)
graph.add_node("sub1", sub1)
graph.add_node("router", lambda state : state)
graph.add_node("add2", add2)
graph.add_node("sub2", sub2)
graph.add_node("res", last_node)
graph.add_node("router2", lambda state : state)
graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    next_node_decider1,
    {
        "add_op1" : "add1",
        "sub_op1" : "sub1"
    }
)
graph.add_edge("add1", "router2")
graph.add_edge("sub1", "router2")

graph.add_conditional_edges(
    "router2",
    next_node_decider2,
    {
        "add_op2" : "add2",
        "sub_op2" : "sub2"
    }
)

graph.add_edge("add2", "res")
graph.add_edge("sub2", "res")
graph.add_edge("res", END)

app = graph.compile()

get_png = app.get_graph().draw_mermaid_png()
with open("graph5.png", "wb") as f:
    f.write(get_png)

result = app.invoke({"num1" : 6, "num2" : 3, "num3":9, "num4" : 7, "finalnum1" : 0, "finalnum2" : 0,"op1" : "+", "op2" : "-"})
print(result["res"])

