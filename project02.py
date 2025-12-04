from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
response = llm.invoke("Give a 1-line tagline for 'Smartwatch'.")
tagline = response.content.strip()
print(tagline)