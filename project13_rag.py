# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.output_parsers import StrOutputParser

# load_dotenv()

# llm = ChatGroq(model="llama-3.1-8b-instant")
# parser = StrOutputParser()

# #results = llm.invoke("What is the captial of india")
# #output_parser = parser.invoke(results)
# #print(results)
# #print(output_parser)

# #Simple chain
# #chain = llm | parser
# #print(chain.invoke("Give me a 10 line mobile review."))

# from typing import List
# from pydantic import BaseModel, Field

# class MobileReview(BaseModel):
#     phone_model: str= Field(..., description="Name of the mobile")
#     pros: str = Field(..., description="Positive points about the mobile")
#     features: List[str] = Field(..., description="Features of the mobile phone.")

# review_text = """
# I've been using the Samsung Galaxy S23 for a few weeks now, and I'm thoroughly impressed. 
# The phone's large 6.8-inch display is vibrant and perfect for watching movies or browsing the web.
# The battery life is excellent, lasting me a full day and a half with moderate use.
# I've also been using the phone's camera, which takes high-quality photos and videos.
# The phone's performance is lightning-fast, thanks to its powerful processor.
# The phone's design is sleek and stylish, with a premium feel to it.
# One of my favorite features is the phone's wireless charging capability.
# I've also been using the phone's fingerprint scanner, which is fast and secure.
# Overall, I'm very happy with my purchase and would recommend the Samsung Galaxy S23 to anyone in the market for a new phone.
# Its price is a bit steep, but the phone's features and performance make it well worth the investment.
# """

# structured_llm = llm.with_structured_output(MobileReview)
# #output = structured_llm.invoke(review_text)
# #print(output)

# from langchain_core.prompts import ChatPromptTemplate
# prompt = ChatPromptTemplate.from_template("Give me review about {topic}")


# chain = prompt | structured_llm
# #output = chain.invoke({"topic": "iphone 16"})
# #print(output)

# from langchain_core.messages import HumanMessage, SystemMessage
# system_message = SystemMessage(content="You're a helpful assistant")
# human_message = HumanMessage(content="Tell me about programming")

# template = ChatPromptTemplate([
#     ("system", "Youre a helpful assistant, always answering in 2 lines."),
#     ("human", "Tell me about {topic}")
# ])

# chain = llm | parser
# #prompt = template.invoke({"topic": "programming"})
# #print(chain.invoke(prompt))





# from langchain_community.document_loaders import PyPDFLoader
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langgraph.checkpoint.memory import InMemorySaver
# from dotenv import load_dotenv

# load_dotenv()

# file_path = "pdf/nke-10k-2023.pdf"
# loader = PyPDFLoader(file_path=file_path)
# document = loader.load()
# print(len(document))

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )

# splits = text_splitter.split_documents(document)
# print(len(splits))

# model_name = "all-MiniLM-L6-v2"
# embeddings = HuggingFaceEmbeddings(model_name=model_name)

# document_embeddings = embeddings.embed_documents([split.page_content for split in splits])

# vectorstore = Chroma.from_documents(
#     collection_name="my_collection",
#     embedding=embeddings,
#     documents=splits,
#     persist_directory="./chroma_db"
# )

# retriever = vectorstore.as_retriever(search_kwargs={"k":2})
# retriever.invoke("what is the most competitive industry in the world.")

# from langchain_core.prompts import ChatPromptTemplate
# template = """
# Answer the question based on the following context:
# Context: {context}
# Question: {question}
# Answer:
# """

# prompt = ChatPromptTemplate.from_template(template)

# from langchain_classic.schema.runnable import RunnablePassthrough

# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()} | prompt
# )

# rag_chain.invoke("what is the most competitive industry in the world.")

# def doc2str(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# rag_chain = (
#     {"context": retriever | doc2str, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | parser
# )

# checkpointer = InMemorySaver()



from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

prompt = PromptTemplate.from_template("Give me short review about {topic}\n\nFormat your answer as:\n{format_instructions}")

llm = ChatGroq(model="llama-3.1-8b-instant")

class Output(BaseModel):
    sentiment: str = Field(description="Is the review postive or negative")
    thing: str = Field(description="What is review about? About what thing/product?")

parser = PydanticOutputParser(pydantic_object=Output)
prompt = prompt.partial(format_instructions=parser.get_format_instructions())


chain = prompt | llm | parser
result = chain.invoke({"topic": "iphone"})
print(result)