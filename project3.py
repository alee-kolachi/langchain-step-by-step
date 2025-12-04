"""Project 4 — Two-Step Chain

Goal: Run one output into another prompt."""

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
tagline = llm.invoke("Give 1 line tagline for my new product i.e Hair Oil")

explanation = llm.invoke(f"Explain why this tagline is effective: {tagline}").content.strip()

print("Tagline:", tagline)
print("Explanation:", explanation)