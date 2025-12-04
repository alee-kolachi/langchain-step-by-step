from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    query: str
    code: str


llm = ChatGroq(model="llama-3.1-8b-instant")

def run_code(code: str):
    """
    Execute Python code from a string and report success or errors.
    """
    try:
        exec(code, {})
        return {"success": True, "error": None}
    except Exception as e:
        return {"success": False, "error": str(e)}


# user_query = input("What python code do you want?")

# response = llm.invoke(f"Please create python code based on this user query: {user_query}")
# print(response)

graph = StateGraph(AgentState)

graph.add_node("run_code", run_code)

graph.add_edge(START, "run_code")
graph.add_edge("run_code", END)

workflow = graph.compile()

print(workflow)

