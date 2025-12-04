import sys
import os
from pathlib import Path
import hashlib

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_classic.schema import Document
from dotenv import load_dotenv

load_dotenv()


def create_chroma_db():
    model_name = "all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="db/rag_chroma_db",
        collection_name="documents"
    )
    return vector_store

def split_document(document):
    print(document)
    doc = ""
    path = Path("docs") / document
    with open(path, "r") as f:
        doc = f.readlines()
    doc = "\n".join(doc)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100,
    )
    if document.endswith(".txt"):
        return splitter.split_text(doc)
    elif document.endswith(".pdf"):
        doc_obj = Document(page_content=doc)
        return splitter.split_documents(documents=doc)

def save_into_db(splits, vector_store):
    for i, split in enumerate(splits):
        vector_store.add_texts([split], ids=[f"doc_{i}"])
    return vector_store

def list_documents():
    files = os.listdir("docs")
    return files

def select_document():
    
    files = list_documents()
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    index = int(input("Please select document from its index"))
    print(f"You've chosen document with index: {index}")

    chosen_document = files[index-1]
    chatbot(chosen_document)


def chatbot(document: str):

    print()
    print("="*60)
    question = input("Please start asking questions now about this document. Type X to exit")
    if question.lower() == "x":
        sys.exit()
    else:
        vector_store = create_chroma_db()
        splits = split_document(document)
        vector_store = save_into_db(splits, vector_store)
        llm = ChatGroq(model="llama-3.1-8b-instant")
        prompt = PromptTemplate(
            template="You'll be given a query and a context, please look at the context and answer the query based on context. Important: If you cannot find answer, tell us that without giving incorrect answer.\nquery: {query} and context: {context}",
            input_variables=["query", "context"]
        )
        parser = StrOutputParser()

        model_name = "all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        query_embedding = embeddings.embed_query(question)
        
        retriever = vector_store.as_retriever() 
        results = retriever.invoke(question)
        context = results[0].page_content

        formatted_prompt = prompt.format(query=question, context=context)
        
        response = llm.invoke(formatted_prompt)
        response_text = parser.invoke(response)
        print("\nAnswer:", response_text)
        print("="*60)



            

        

    


def main():

    print()
    print("1. List Uploaded Documents")
    print("2. Select a Document")
    print("X. Exit")

    choice = input("Enter> ")

    match choice:
        case "1":
            files = list_documents()
            print(files)
            main()
        case "2":
            select_document()
        case "X" | "x":
            sys.exit()

if __name__ == "__main__":
    print("="*60)
    print("WELCOME TO FINANCIAL REPORT ANALYZER")
    print("="*60)
    main()