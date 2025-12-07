# Import necessary modules from LangChain and other libraries
from langchain_community.document_loaders import TextLoader  # Loader for plain text files
from langchain_groq import ChatGroq  # Groq LLM integration
from langchain_core.output_parsers import StrOutputParser  # Parses LLM output as string
from langchain_core.prompts import PromptTemplate  # Allows template-based prompts
from langchain_community.document_loaders import PyPDFLoader  # Loader for PDF files
from langchain_community.document_loaders import DirectoryLoader  # Loader for directories of files
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load environment variables from .env file
load_dotenv()

# Function to demonstrate loading a text file and generating a summary using ChatGroq
def text_loader():
    # Initialize a text loader to read a specific text file
    loader = TextLoader(
        file_path="docs/abc.txt",  # Path to text file
        encoding='utf-8'  # File encoding
    )

    # Define a prompt template for summarization
    prompt = PromptTemplate(
        template="Write summary of the follwoing: \n {text}",  # Template with a placeholder for text
        input_variables=["text"]  # Variable name used in template
    )

    # Initialize the LLM (Large Language Model) from Groq
    llm = ChatGroq(model="llama-3.1-8b-instant")  # Using LLaMA 3.1 8B instant model

    # Initialize output parser to convert LLM output into string
    parser = StrOutputParser()

    # Load documents from the text file
    docs = loader.load()

    # Print type of loaded documents and first document's details
    print(type(docs))           # Should be a list of Document objects
    print(type(docs[0]))        # Each item is a Document
    print(docs[0].metadata)     # Metadata of first document (like source, page number)
    print(docs[0].page_content) # Actual content of the document

    # Create a processing chain: prompt -> LLM -> output parser
    chain = prompt | llm | parser

    # Invoke the chain on the text content of the first document
    print(chain.invoke({"text": docs[0].page_content}))

# Function to demonstrate loading a PDF file
def pdf_loader():
    # Initialize PDF loader with path to a PDF file
    loader = PyPDFLoader(
        file_path="docs/nke-10k-2023.pdf"
    )

    # Load the PDF into a list of Document objects
    docs = loader.load()

    # Print the number of pages/documents loaded
    print(len(docs))

# Function to demonstrate loading all files in a directory
def directory_loader():
    # Initialize DirectoryLoader to load all files recursively
    loader = DirectoryLoader(
        path="docs",  # Directory path
        glob="**/*",  # Glob pattern to match all files
        # Use PDF loader for .pdf files, TextLoader for everything else
        loader_cls=lambda p: PyPDFLoader(p) if p.endswith(".pdf") else TextLoader(p)
    )

    # Load all documents from the directory
    docs = loader.load()

    # Print the total number of documents loaded
    print(len(docs))
