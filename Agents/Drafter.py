from langchain_openai import  ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END,START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, BaseMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.graph import add_messages
from typing import Annotated, TypedDict, List, Sequence
load_dotenv()

doc_con = " "

class AgentClass(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content : str)->str:
    """ This tool adds the text provided as input to this tool to document"""
    
    global doc_con
    doc_con = content
    return f"The doc has been updated successfully! Current content is : {doc_con}"

@tool
def save_doc(filename : str)->str:
    """ This tool saves the doc to the text file and finishes the process!
    Args :
        filename : Name of the file
    """
    global doc_con
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"
    try :
        with open (filename, 'w') as f:
            f.write(doc_con)
            print(f"The file has been saved as : {filename}")
            return f"The file has been saved as : {filename}"
    except Exception as e:
        return f"Error saving the file : {str(e)}"


tools = [update, save_doc]

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2, max_tokens = 500).bind_tools(tools)

def our_agent(state : AgentClass)->AgentClass:

    sys_prompt = SystemMessage(content=f""" You are a drafter and helpful writing assistant. You are going to help user update and  modify the documents. 
If user wants to update the document, use update tool with complete updated content.
If user is satisfied with the document and doesn't want any further updation, use save_doc tool to save the document.
Make sure to always show the current document state after modifications. 
Current document content is : {doc_con}""")
    
    if not state['messages']:
        user_input = "I'm ready to help you with document updation. What would like to create?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("What would you like to do with doc?")
        print(f"\n USER : {user_input}")
        user_message = HumanMessage(content=user_input)
        
    all_message = [sys_prompt]
    all_message.extend(state['messages'])
    all_message.append(user_message)
    
    # print(type(all_message))
    # print(type(all_message[0]))
    
    response = llm.invoke(all_message)
    
    print(f"\n AI Response : {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"Using Tools : {[tc['name'] for tc in response.tool_calls]}")
    return {"messages" : [user_message, response]}


def should_cont(state : AgentClass)->AgentClass:
    """ This funnction / node decides whether to continue or end the conversation"""
    messages = state['messages']
    
    if not messages:
        return "continue"
    for messages in reversed(messages):
        if isinstance(messages, ToolMessage) and "saved" in messages.content.lower() and "document" in messages.content.lower():
            return "end"
    return "continue"

def print_mess(messages):
    """ This node prints the messages in proper format"""
    if not messages:
        return
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"Tool Result : {message.content}")

graph = StateGraph(AgentClass)
graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools) )
graph.add_edge("agent", "tools")
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "tools", 
    should_cont,
    {
        "continue" : "agent",
        "end" : END,
    },
)

app = graph.compile()

png_data = app.get_graph().draw_mermaid_png()
with open("drafter.png", "wb") as f:
    f.write(png_data)

def run_doc_agent():
    print("-----DRAFTER-----")
    state = {"messages" : []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_mess(step["messages"])
            
    print("-----DRAFTER FINISHED-----")
    
if __name__ == "__main__":
    run_doc_agent()
            
        