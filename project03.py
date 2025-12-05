# -----------------------------
# Project 03
# Title: Two-Step LLM Chain
# Description: Generates a tagline for a product, then feeds that tagline
#              into a second prompt to get an explanation.
# -----------------------------

from langchain_groq import ChatGroq        # Import Groq LLM wrapper from LangChain
from dotenv import load_dotenv             # Import function for environment variables

load_dotenv()                              # Load environment variables from .env file

# Initialize the Groq language model
llm = ChatGroq(model="llama-3.1-8b-instant")

# First prompt: ask the model to generate a 1-line tagline
tagline = llm.invoke("Give 1 line tagline for my new product i.e Hair Oil")

# Second prompt: explain why the generated tagline works
# Note: .content is used to extract raw text from the LLM response
explanation = llm.invoke(
    f"Explain why this tagline is effective: {tagline.content}"
).content.strip()

# Print the results
print("Tagline:", tagline.content)
print("Explanation:", explanation)
