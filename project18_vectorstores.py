from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.schema import Document
from dotenv import load_dotenv

load_dotenv()

model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

doc1 = Document(
    page_content="Hello, my name is Ali Kolachi",
    metadata={"type":"name"}
)

doc2 = Document(
    page_content="Hello, my age is 26",
    metadata={"type":"age"}
)

docs = [doc1, doc2]

vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="db/chroma_db",
    collection_name="personal_data"
)

vector_store.add_documents(docs)
results = vector_store.similarity_search(
    query="how old am i?",
    k=1
)
print(results)