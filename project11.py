# -----------------------------
# Project 10
# Title: Agent with Short-Term Memory (Thread-Based)
# Description: Demonstrates an LLM agent that uses tools and maintains
#              short-term memory via thread-based checkpointing.
# -----------------------------

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv

load_dotenv()

#Step 1 : Tools
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the sum"""
    return a + b

@tool
def multiply_two_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return result"""
    return a * b

#Step 2: Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b")

#Step 3: Middleware to trim messages


#Step 4: Create agent with memory
agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_two_numbers],
    checkpointer=InMemorySaver(),
)

#Step 5: Thread config for short-term memory

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
        {"configurable": {"thread_id": "1"}}
    )
    print("User:", user_input)
    print("Agent:", result["messages"][-1].content)
    print("---")