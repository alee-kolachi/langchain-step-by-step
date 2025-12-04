"""Project 8 — Basic Tool Agent

Goal: Let LLM call a Python function."""

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers together."""
    return a+b

llm = ChatGroq(model="llama-3.1-8b-instant")
agent = create_agent(
    model=llm,
    tools=[add_numbers],
    system_prompt="You can use a tool to add two numbers."
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 2+45"
            }
        ]
    }
)

for msg in result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)

        