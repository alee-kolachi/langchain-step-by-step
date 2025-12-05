# -----------------------------
# Project 01
# Title: Simple LLM Invocation
# Description: Loads environment variables, initializes a Groq LLM model,
#              sends a prompt, and prints the model's response.
# -----------------------------

from langchain_groq import ChatGroq       # Import Groq LLM wrapper from LangChain
from dotenv import load_dotenv            # Import function to load environment variables

load_dotenv()                             # Load environment variables from .env file

# Initialize the Groq language model with the chosen model name
llm = ChatGroq(model="llama-3.1-8b-instant")

# Send a prompt to the model and store the response
result = llm.invoke("Hey who is the prime minister of paksitan")

# Print only the content portion of the model's response
print(result.content)
