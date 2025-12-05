# -----------------------------
# Project 07
# Title: Basic Tool Agent
# Description: Defines a simple Python tool, allows an LLM agent to call it,
#              and prints the final AI response.
# -----------------------------

from langchain_groq import ChatGroq                    # LLM wrapper
from langchain.tools import tool                       # Decorator to turn functions into tools
from langchain.agents import create_agent              # Creates an agent that can use tools
from langchain.messages import AIMessage               # Message class to identify AI output
from dotenv import load_dotenv                         # Load environment variables

load_dotenv()                                           # Load .env settings

# Define a simple tool that adds two integers
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b

# Initialize the LLM
llm = ChatGroq(model="llama-3.1-8b-instant")

# Create an agent that knows it can use the add_numbers tool
agent = create_agent(
    model=llm,
    tools=[add_numbers],
    system_prompt="You can use a tool to add two numbers."
)

# Run the agent with a user query
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

# Extract and print only the AI messages from the result
for msg in result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)
