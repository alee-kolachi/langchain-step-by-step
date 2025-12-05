# -----------------------------
# Project 02
# Title: LLM Tagline Generator
# Description: Loads environment variables, initializes a Groq LLM model,
#              generates a 1-line tagline for a given product, and prints it.
# -----------------------------

from langchain_groq import ChatGroq        # Import Groq LLM wrapper from LangChain
from dotenv import load_dotenv             # Import function to load environment variables

load_dotenv()                              # Load environment variables from .env file

# Initialize the Groq language model with the specified model name
llm = ChatGroq(model="llama-3.1-8b-instant")

# Invoke the model with a prompt requesting a short product tagline
response = llm.invoke("Give a 1-line tagline for 'Smartwatch'.")

# Extract the text content and remove any extra whitespace
tagline = response.content.strip()

# Display the final tagline
print(tagline)
