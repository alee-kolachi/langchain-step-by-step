"""Project 6 — Vector Store Retrieval

Goal: Use embeddings + FAISS for smarter retrieval."""

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

docs = [
    "LangChain helps build LLM applications.",
    "RAG improves LLM responses with external info.",
    "FAISS is a vector search library."
]

#Create Embeddings
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
print(f"Embeddings: {embeddings}")
vectorstore = FAISS.from_texts(docs, embeddings)
print(f"VectorStore: {vectorstore}")

#Retreieve
retriever = vectorstore.as_retriever()
results = retriever.invoke("What is RAG")
context = results[0].page_content
print(f"Context: {context}")


#Ask LLM
llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke(f"Explain in short using this {context}").content.strip()

print(response)

