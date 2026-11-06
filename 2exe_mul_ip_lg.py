from langgraph.graph import StateGraph
from typing import TypedDict, List
import math

class Agentgraph(TypedDict):
    values : List[int]
    Name : str
    operation : str
    result : str

def custom_op(state : Agentgraph)->Agentgraph:
    """This node generates the string output as per given list of int and oepration to be performed"""
    if state["operation"] == "*":
        res = math.prod(state["values"]) 
            
    elif state["operation"] == "+":
        res = sum(state["values"])
    else:
        raise ValueError("Provide the correct operator '+' or '*'")
    
    state["result"]  = f"Hi {state["Name"]}, your answer is {res}"
    return state

graph = StateGraph(Agentgraph)
graph.add_node("custom_operation", custom_op)
graph.set_entry_point("custom_operation")
graph.set_finish_point("custom_operation")
app = graph.compile()

png_data = app.get_graph().draw_mermaid_png()
with open("graph3.png", "wb") as f:
    f.write(png_data)
result = app.invoke({"values" : [9,8,3,19,5,1], "Name" : "Varad", "operation" : "+"})
print(result["result"])
