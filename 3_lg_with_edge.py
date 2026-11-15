from langgraph.graph import StateGraph
from typing import TypedDict, List

# create Agent state class
class Agentclass(TypedDict):
    name : str
    age : int
    skills : List[str]
    res : str

# Create nodes 1 to 3
def first_node(state : Agentclass) -> Agentclass:
    """This is first node which gives output as name"""
    state["res"] = f"Hi, {state['name']}!"
    return state
def second_node(state : Agentclass) -> Agentclass:
    """This is second node which gives output as name + age"""
    state["res"] = state["res"] + f" your are {state['age']} years old,"
    return state
def third_node(state : Agentclass)->Agentclass:
    """This is third node which gives output as name + age + skills"""
    # Formatted Str output ->
    skills = state["skills"]
    formatted_skills = ", ".join(skills[:-1]) + " and " + skills[-1]
    state["res"] = state["res"] + f" and your skills are {formatted_skills}!"
    return state

# create graph
graph = StateGraph(Agentclass)
# Add Nodes
graph.add_node("first node", first_node)
graph.add_node("second node",second_node)
graph.add_node("third node", third_node)
# Entry Point
graph.set_entry_point("first node")
# Add edges
graph.add_edge("first node", "second node")
graph.add_edge("second node", "third node")
# Finish Point
graph.set_finish_point("third node")
# Compile the graph
app = graph.compile()

# Print the graph
png_data = app.get_graph().draw_mermaid_png()

with open("graph4.png", "wb") as f:
    f.write(png_data)

# Invoke the graph and print results
result = app.invoke({"name":"varad", "age" : 23, "skills" : ["LLM", "Langchain", "Lanngraph", "DL", "ML"]})
print(result["res"])
