# -----------------------------
# Project 10
# Title: Agent with Short-Term Memory (Thread-Based)
# Description: Demonstrates an LLM agent that uses tools and maintains
#              short-term memory via thread-based checkpointing.
# -----------------------------

from langchain_groq import ChatGroq                     # LLM wrapper
from langchain.tools import tool                        # Tool decorator
from langchain.agents import create_agent               # Agent factory
from langchain.agents.middleware import before_model    # Message middleware (optional trimming)
from langchain.messages import RemoveMessage            # Used for message deletion
from langgraph.checkpoint.memory import InMemorySaver   # In-memory checkpoint store
from langchain_core.runnables import RunnableConfig     # Config for threaded execution
from dotenv import load_dotenv                          # Load environment variables

load_dotenv()                                            # Initialize env variables

# Step 1: Define tools

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the sum"""
    return a + b

@tool
def multiply_two_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return result"""
    return a * b

# Step 2: Initialize the language model
llm = ChatGroq(model="openai/gpt-oss-120b")

# Step 3: Middleware placeholder (not trimming anything here)
# You could implement trimming logic if needed.

# Step 4: Create the agent with memory enabled via InMemorySaver
agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_two_numbers],
    checkpointer=InMemorySaver(),  # Enables short-term, thread-based memory
)

# Step 5: Thread configuration for memory
# Memory persists within this thread ID
thread_config = {"configurable": {"thread_id": "1"}}

# Step 6: Multi-turn conversation
conversation = [
    "Hi, my name is Alice.",
    "Please add 7 + 5.",
    "Now multiply that result by 3.",
    "What was my name again?",
]

for user_input in conversation:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        thread_config
    )
    
    # The agent's latest response is the last message
    reply = result["messages"][-1].content

    print("User:", user_input)
    print("Agent:", reply)
    print("---")
