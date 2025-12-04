"""Project 6 — Simple RAG Chain

Goal: Combine retrieval + LLM into one flow."""

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

data = [
    "We're a team of 50 people, all working remotely",
    "We allow only 5 holidays per year",
    "You get bonus every 6 months"
]

#Create embeddings
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = FAISS.from_texts(data, embeddings)
retriever = vectorstore.as_retriever()

#user query
query = "How many leaves do you allow per year?"
results = retriever.invoke(query)
context = results[0].page_content

#llm answer
llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke(f"Using this context: {context}, answer the user query: {query}")
print(response.content.strip())