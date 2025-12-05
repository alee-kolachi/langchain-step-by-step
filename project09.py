# -----------------------------
# Project 09
# Title: Simple Chat Agent
# Description: Creates a basic LLM-powered chat agent without tools or memory
#              and runs multiple user messages through it.
# -----------------------------

from langchain_groq import ChatGroq               # LLM wrapper
from langchain.agents import create_agent         # Create a simple agent
from langchain.messages import AIMessage          # Used to identify AI outputs
from dotenv import load_dotenv                    # Load .env variables

load_dotenv()                                     # Initialize environment

# Step 1: Initialize the language model
llm = ChatGroq(model="openai/gpt-oss-120b")

# Step 2: Create a basic agent with no tools or memory
agent = create_agent(
    model=llm,
    system_prompt="You are a helpful assistant. Answer questions naturally."
)

# Step 3: Sample conversation inputs
questions = [
    "Hello, how are you?",
    "Can you explain what LangChain is?",
    "Give me a joke."
]

# Loop through each question and get the final AI response
for q in questions:
    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    
    # The last message from the model is the assistant's final answer
    final_answer = result["messages"][-1].content

    print(f"Q: {q}\nA: {final_answer}\n")
