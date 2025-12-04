"""Project 11 — Conversation Summary Memory

Goal: Automatically summarize old messages when context gets too long,
      keeping only the summary + recent messages.
"""

from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage, AIMessage
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# Step 1: Define Tools
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the sum"""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return result"""
    return a * b

# Step 2: Initialize LLM with tools
llm = ChatGroq(model="llama-3.1-8b-instant")
tools = [add_numbers, multiply_numbers]
llm_with_tools = llm.bind_tools(tools)

# Step 3: Define State with Summary
class State(MessagesState):
    summary: str  # Store conversation summary

# Step 4: Define the chatbot node
def call_model(state: State):
    """Main chatbot node that processes user input"""
    summary = state.get("summary", "")
    
    # If we have a summary, add it as context
    if summary:
        system_msg = SystemMessage(
            content=f"Summary of conversation so far: {summary}"
        )
        messages = [system_msg] + state["messages"]
    else:
        messages = state["messages"]
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Step 5: Route after model
def route_after_model(state: State) -> Literal["tools", "summarize", END]:
    """Route to tools if called, check summarization if not"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If tools were called, route to tools
    if last_message.tool_calls:
        return "tools"
    
    # Otherwise, check if we need to summarize (threshold: 5 messages)
    # This ensures we summarize BEFORE important info gets deleted
    if len(messages) > 5:
        return "summarize"
    
    return END

# Step 7: Summarization node
def summarize_conversation(state: State):
    """Summarize the conversation and remove old messages"""
    summary = state.get("summary", "")
    
    # Create prompt based on whether summary exists
    if summary:
        summary_prompt = (
            f"Previous summary: {summary}\n\n"
            "Extend the summary by including new information from the messages above. "
            "Preserve ALL important details from the previous summary AND add any new information "
            "like names, preferences, calculations, or facts. Do not lose any critical information:"
        )
    else:
        summary_prompt = (
            "Create a concise summary of the conversation above. "
            "Include ALL important details like:\n"
            "- Person's name if mentioned\n"
            "- Their preferences or interests\n"
            "- Any calculations or results\n"
            "- Key facts discussed"
        )
    
    # Get summary from LLM
    messages = state["messages"] + [HumanMessage(content=summary_prompt)]
    response = llm.invoke(messages)
    
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    
    return {"summary": response.content, "messages": delete_messages}

# Step 8: Build the graph
builder = StateGraph(State)

# Add nodes
builder.add_node("chatbot", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_node("summarize", summarize_conversation)

# Add edges
builder.add_edge(START, "chatbot")

# Route from chatbot based on tool calls and message count
builder.add_conditional_edges(
    "chatbot",
    route_after_model,
    {"tools": "tools", "summarize": "summarize", END: END}
)

# After tools execute, go back to chatbot
builder.add_edge("tools", "chatbot")

# After summarize, end
builder.add_edge("summarize", END)

# Compile with memory
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Step 9: Multi-turn conversation with summarization
conversation = [
    "Hi, my name is Alice.",
    "Please add 7 + 5.",
    "Now multiply that result by 3.",
    "I also love coding in Python.",
    "What programming languages do you know?",
    "Can you add 10 + 20 for me?",
    "What was my name again?",  # This should use the summary
]

config = {"configurable": {"thread_id": "1"}}

print("=" * 60)
print("CONVERSATION WITH SUMMARY MEMORY")
print("=" * 60)

for user_input in conversation:
    result = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config
    )
    
    # Get the last AI message
    ai_messages = [m for m in result['messages'] if isinstance(m, AIMessage)]
    last_ai_msg = ai_messages[-1] if ai_messages else None
    
    print(f"\nUser: {user_input}")
    if last_ai_msg:
        print(f"Agent: {last_ai_msg.content}")
    
    # Show summary if it was just created
    if result.get("summary"):
        print(f"[Summary created/updated]")
    print("-" * 60)

# Step 10: Check final state
final_state = graph.get_state(config)
print("\n" + "=" * 60)
print("FINAL STATE")
print("=" * 60)
print(f"\nMessages in memory: {len(final_state.values['messages'])}")
print(f"\nFull Summary:\n{final_state.values.get('summary', 'No summary yet')}")