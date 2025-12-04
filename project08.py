"""Project 8 — Multi-Tool Agent (Add + Multiply + Retrieve)"""

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.messages import AIMessage
from langchain.agents import create_agent
from typing import Any
from dotenv import load_dotenv

load_dotenv()

#Step1. Defining tools

@tool
def add_numbers(a: int, b: int) -> int:
    """This function adds two numbers and returns the total result."""
    return a+b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """This function multiply two numbers and return the total result."""
    return a*b

docs = [
    "We're a team of 50 people, all working remotely",
    "We allow only 5 holidays per year",
    "You get bonus every 6 months"
]

model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = FAISS.from_texts(docs, embeddings)

@tool
def retrieve_info(query: str) -> str:
    """Retreieves similar information from docs as per given query"""
    results = vectorstore.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])

#Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b")

#Create tool agent
agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_numbers, retrieve_info],
    system_prompt="""You can add, multiply, or retrieve information from the knowledge base to answer the user
                    You MUST use tools for math. You MUST NOT answer math yourself.
                    You MUST retrieve information from vectorstore when the user asks about the company."""
)

#Ask the agent
questions = [
    "How much is 2+4",
    "What is 4*4",
    "A friend was asking me question that got me confused, he asked me how much are the total eggs in 5 days if one hen lays 5 eggs daily",
    "Explain our holiday policy at my company."
]

for question in questions:
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": question
        }]
    })
    #Clean AI output
    final_message = None
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            final_message = msg  # overwrite until last one

    print(f"Question: {question}\nAnswer: {final_message.content}")
