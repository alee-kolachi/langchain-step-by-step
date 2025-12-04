"""Project 4 — Mini Knowledge Base

Goal: Store a few text snippets and retrieve manually."""

docs = [
    "LangChain helps build LLM applications.",
    "RAG improves LLM responses with external info.",
    "FAISS is a vector search library."
]

query = "What is LangChain?"

for doc in docs:
    if "LangChain" in doc:
        context = doc
        break

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke(f"Based on this info: {context}, Explain langchain simply.")

print(response.content.strip())