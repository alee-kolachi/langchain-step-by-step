# -----------------------------
# Project 04
# Title: Mini Knowledge Base
# Description: Stores a few text snippets, performs a manual check to find
#              the relevant one based on a query, and then uses an LLM
#              to generate a simple explanation.
# -----------------------------

# Small set of documents acting as a basic knowledge base
docs = [
    "LangChain helps build LLM applications.",
    "RAG improves LLM responses with external info.",
    "FAISS is a vector search library."
]

# User query
query = "What is LangChain?"

# Manual retrieval: check each document for the keyword
for doc in docs:
    if "LangChain" in doc:
        context = doc      # Select the matching document
        break

from langchain_groq import ChatGroq          # LLM wrapper
from dotenv import load_dotenv               # Load environment variables

load_dotenv()                                # Load .env file variables

# Initialize the language model
llm = ChatGroq(model="llama-3.1-8b-instant")

# Ask the LLM to explain using the selected context
response = llm.invoke(
    f"Based on this info: {context}, explain LangChain simply."
)

# Print the answer
print(response.content.strip())
