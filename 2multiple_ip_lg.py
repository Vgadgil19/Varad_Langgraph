from langgraph.graph import StateGraph
from typing import TypedDict, List

class AgentState(TypedDict):
    values : List[int]
    name : str
    result : str

def process_val(state : AgentState) -> AgentState:
    """ This function takes the values and name as input and calculate the sum and parse the sum with name"""
    
    state["result"] = f"Hi, {state["name"]} Your Sum : {sum(state["values"])}"
    return state

graph = StateGraph(AgentState)
graph.add_node("processing", process_val)
graph.set_entry_point("processing")
graph.set_finish_point("processing")
com = graph.compile()

png_data = com.get_graph().draw_mermaid_png()

with open("graph2.png", "wb") as f:
    f.write(png_data)

result = com.invoke({ "values" : {5,8,6,9,3,12},"name" : "Varad"})

print(result["result"])