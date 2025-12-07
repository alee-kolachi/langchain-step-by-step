"""
FULL LANGCHAIN + GROQ + RAG TUTORIAL PROJECT
--------------------------------------------

This file demonstrates:

1. Loading environment variables
2. Basic LLM call
3. Chains with output parsers
4. Pydantic structured output
5. Prompt templates
6. Loading & splitting PDFs
7. Creating embeddings
8. Creating a Chroma vectorstore
9. Retriever-based RAG pipeline
10. Final structured output example

All code is simplified & production-ready.
"""

from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field

# LangChain imports
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_classic.schema.runnable import RunnablePassthrough

# RAG components
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# --------------------------------------------------------------------
# 1. Environment Setup
# --------------------------------------------------------------------
load_dotenv()  # loads your .env file so GROQ_API_KEY is available


# --------------------------------------------------------------------
# 2. Initialize LLM (Groq)
# --------------------------------------------------------------------
llm = ChatGroq(model="llama-3.1-8b-instant")


# --------------------------------------------------------------------
# 3. Basic LLM Call
# --------------------------------------------------------------------
def basic_example():
    print("\n=== BASIC LLM CALL ===")
    response = llm.invoke("What is the capital of India?")
    print(response.content)


# --------------------------------------------------------------------
# 4. Simple Chain (LLM → String Parser)
# --------------------------------------------------------------------
def simple_chain_example():
    print("\n=== SIMPLE CHAIN (LLM | PARSER) ===")
    parser = StrOutputParser()
    chain = llm | parser
    print(chain.invoke("Give me a 3-line review of any smartphone."))


# --------------------------------------------------------------------
# 5. Structured Output Using Pydantic
# --------------------------------------------------------------------
class MobileReview(BaseModel):
    phone_model: str = Field(..., description="Name of the phone")
    pros: str = Field(..., description="Positive points")
    features: List[str] = Field(..., description="Features list")


def structured_output_example():
    print("\n=== STRUCTURED OUTPUT EXAMPLE ===")
    structured_llm = llm.with_structured_output(MobileReview)

    review_text = """
    The Samsung Galaxy S23 has an excellent display, long battery life,
    fast performance and a great camera. Wireless charging works well,
    and the design is premium.
    """

    result = structured_llm.invoke(review_text)
    print(result)


# --------------------------------------------------------------------
# 6. Prompt Template Example
# --------------------------------------------------------------------
def prompt_example():
    print("\n=== PROMPT TEMPLATE EXAMPLE ===")

    template = ChatPromptTemplate([
        ("system", "You respond in exactly 2 lines."),
        ("human", "Explain {topic}")
    ])

    chain = template | llm | StrOutputParser()
    print(chain.invoke({"topic": "programming"}))


# --------------------------------------------------------------------
# 7. RAG PIPELINE (PDF → Split → Embed → Retrieve → Answer)
# --------------------------------------------------------------------
def rag_pipeline_example():
    print("\n=== RAG PIPELINE EXAMPLE ===")

    # 1) Load PDF
    loader = PyPDFLoader("pdf/nke-10k-2023.pdf")
    documents = loader.load()

    # 2) Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    splits = splitter.split_documents(documents)

    # 3) Embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4) Create vectorstore
    vectorstore = Chroma.from_documents(
        collection_name="my_collection",
        embedding=embeddings,
        documents=splits,
        persist_directory="./chroma_db"
    )

    # 5) Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # Helper to convert docs → string
    def doc2str(docs):
        return "\n\n".join(d.page_content for d in docs)

    # 6) RAG prompt
    template = """
    Use the context to answer the question.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(template)

    # 7) RAG Chain
    rag_chain = (
        {
            "context": retriever | doc2str,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print(rag_chain.invoke("What industry is most competitive according to this report?"))


# --------------------------------------------------------------------
# 8. Final Example (Pydantic Structured Output With Prompt)
# --------------------------------------------------------------------
class Output(BaseModel):
    sentiment: str = Field(description="Positive or negative?")
    thing: str = Field(description="What is being reviewed?")


def final_structured_example():
    print("\n=== FINAL STRUCTURED OUTPUT WITH TEMPLATE ===")

    parser = PydanticOutputParser(pydantic_object=Output)

    prompt = PromptTemplate.from_template(
        "Give me a short review about {topic}\n\nFormat as:\n{format_instructions}"
    )

    # insert format instructions automatically
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser
    result = chain.invoke({"topic": "iPhone"})
    print(result)


# --------------------------------------------------------------------
# RUN EVERYTHING (Tutorial Flow)
# --------------------------------------------------------------------
if __name__ == "__main__":
    basic_example()
    simple_chain_example()
    structured_output_example()
    prompt_example()
    rag_pipeline_example()
    final_structured_example()

