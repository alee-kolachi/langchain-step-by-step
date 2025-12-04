from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from dotenv import load_dotenv

load_dotenv()

def text_loader():
    loader = TextLoader(
        file_path="docs/abc.txt",
        encoding='utf-8'
    )

    prompt = PromptTemplate(
        template="Write summary of the follwoing: \n {text}",
        input_variables=["text"]
    )

    llm = ChatGroq(model="llama-3.1-8b-instant")

    parser = StrOutputParser()

    docs = loader.load()

    print(type(docs))
    print(type(docs[0]))
    print(docs[0].metadata)
    print(docs[0].page_content)


    chain = prompt | llm | parser

    print(chain.invoke({"text": docs[0].page_content}))

def pdf_loader():
    loader = PyPDFLoader(
        file_path="docs/nke-10k-2023.pdf"
    )

    docs = loader.load()
    print(len(docs))

def directory_loader():
    loader = DirectoryLoader(
        path="docs",
        glob="**/*",
        loader_cls= lambda p: PyPDFLoader(p) if p.endswith(".pdf") else TextLoader(p)
    )

    docs = loader.load()

    print(len(docs))

