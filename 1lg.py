from typing import Dict, TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display 

class StateAgent(TypedDict):
    Name : str

def compliment_node(state : StateAgent) -> StateAgent:
    """ It is a node that adds the input name to the compliment message!"""
    
    state["Name"] = state["Name"] + "," + "you are doing amazing job learning Langgraph!"
    return state

graph = StateGraph(StateAgent)

graph.add_node("compliment", compliment_node)
graph.set_entry_point("compliment")
graph.set_finish_point("compliment")
app = graph.compile()

# img = display(Image(app.get_graph().draw_mermaid_png()))
png_data = app.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_data)
    
 
result = app.invoke({'Name' : "Varad"})
print(result)


