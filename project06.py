# -----------------------------
# Project 06
# Title: Simple RAG Chain
# Description: Creates embeddings, stores them in a vector database,
#              retrieves the most relevant text for a user query,
#              and uses an LLM to answer using that context.
# -----------------------------

from langchain_groq import ChatGroq                # LLM wrapper
from langchain_huggingface import HuggingFaceEmbeddings  # Embedding model
from langchain_community.vectorstores import FAISS # Vector store for similarity search
from dotenv import load_dotenv                     # Load environment variables

load_dotenv()                                      # Load .env variables

# Sample knowledge base for retrieval
data = [
    "We're a team of 50 people, all working remotely",
    "We allow only 5 holidays per year",
    "You get bonus every 6 months"
]

# Create embedding model
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Build a FAISS vector store from the sample data
vectorstore = FAISS.from_texts(data, embeddings)

# Convert the vector store into a retriever for querying
retriever = vectorstore.as_retriever()

# User query to test retrieval
query = "How many leaves do you allow per year?"

# Retrieve the most relevant text chunk
results = retriever.invoke(query)
context = results[0].page_content                 # Extract the matched text

# Initialize LLM
llm = ChatGroq(model="llama-3.1-8b-instant")

# Ask the LLM to answer using retrieved context
response = llm.invoke(
    f"Using this context: {context}, answer the user query: {query}"
)

# Print the final answer
print(response.content.strip())
