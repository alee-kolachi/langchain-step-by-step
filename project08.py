# -----------------------------
# Project 08
# Title: Multi-Tool Agent (Add, Multiply, Retrieve)
# Description: Defines multiple tools (math + retrieval), sets up a tool-using LLM agent,
#              and processes several user queries using those tools.
# -----------------------------

from langchain_groq import ChatGroq                         # LLM wrapper
from langchain.tools import tool                            # Decorator to define tools
from langchain_huggingface import HuggingFaceEmbeddings     # Embedding model
from langchain_community.vectorstores import FAISS          # Vector database
from langchain.messages import AIMessage                    # For detecting AI responses
from langchain.agents import create_agent                   # Create tool-using agent
from typing import Any
from dotenv import load_dotenv                              # Load env variables

load_dotenv()                                                # Initialize environment

# Step 1 — Define tools

@tool
def add_numbers(a: int, b: int) -> int:
    """This function adds two numbers and returns the total result."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """This function multiplies two numbers and returns the result."""
    return a * b

# Sample company information for retrieval
docs = [
    "We're a team of 50 people, all working remotely",
    "We allow only 5 holidays per year",
    "You get bonus every 6 months"
]

# Build vector store for retrieval tool
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = FAISS.from_texts(docs, embeddings)

@tool
def retrieve_info(query: str) -> str:
    """Retrieves similar information from docs based on the given query."""
    results = vectorstore.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])

# Initialize LLM for the agent
llm = ChatGroq(model="openai/gpt-oss-120b")

# Create the agent with math + retrieval tools
agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_numbers, retrieve_info],
    system_prompt=(
        "You can add, multiply, or retrieve information from the knowledge base.\n"
        "You MUST use tools for math. Do not calculate yourself.\n"
        "You MUST retrieve information from vectorstore when the user asks about the company."
    )
)

# Questions for the agent to answer
questions = [
    "How much is 2+4",
    "What is 4*4",
    "A friend was asking me question that got me confused, he asked me how much are the total eggs in 5 days if one hen lays 5 eggs daily",
    "Explain our holiday policy at my company."
]

# Run each question through the agent
for question in questions:
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": question
        }]
    })
    
    # Extract the last AI message
    final_message = None
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            final_message = msg

    print(f"Question: {question}\nAnswer: {final_message.content}\n")
