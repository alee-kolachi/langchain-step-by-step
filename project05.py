# -----------------------------
# Project 05
# Title: Vector Store Retrieval
# Description: Creates embeddings for documents, stores them in FAISS,
#              retrieves the most relevant document for a query,
#              and uses an LLM to generate a short explanation.
# -----------------------------

from langchain_groq import ChatGroq                 # LLM wrapper
from langchain_huggingface import HuggingFaceEmbeddings  # Embedding model
from langchain_community.vectorstores import FAISS  # Vector search library
from dotenv import load_dotenv                      # Environment loader

load_dotenv()                                       # Load environment variables

# Documents to store in the vector database
docs = [
    "LangChain helps build LLM applications.",
    "RAG improves LLM responses with external info.",
    "FAISS is a vector search library."
]

# Create text embeddings using a HuggingFace model
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
print(f"Embeddings: {embeddings}")                  # Debug output

# Store the documents in a FAISS vector index
vectorstore = FAISS.from_texts(docs, embeddings)
print(f"VectorStore: {vectorstore}")                # Debug output

# Retrieve the most relevant document for the query
retriever = vectorstore.as_retriever()
results = retriever.invoke("What is RAG")
context = results[0].page_content                  # Extract matched text
print(f"Context: {context}")                       # Debug output

# Ask the LLM for a short explanation using the retrieved context
llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke(
    f"Explain in short using this {context}"
).content.strip()

# Display the final explanation
print(response)
