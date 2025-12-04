# project9_simple_chat.py

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

# Step 1: Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b")

# Step 2: Create a simple agent without tools or memory
agent = create_agent(
    model=llm,
    system_prompt="You are a helpful assistant. Answer questions naturally."
)

# Step 3: Sample conversation
questions = [
    "Hello, how are you?",
    "Can you explain what LangChain is?",
    "Give me a joke."
]

for q in questions:
    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    # Extract only the final AI answer
    final_answer = result["messages"][-1].content
    print(f"Q: {q}\nA: {final_answer}\n")
