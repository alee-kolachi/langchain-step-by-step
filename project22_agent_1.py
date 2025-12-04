from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

search = DuckDuckGoSearchRun()
prompt = hub.pull("hwchase17/react")


agent = create_react_agent(
    llm=llm,
    tools=[search],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[search],
    verbose=True
)

print(agent_executor.invoke({"input": "Give me latest news about the capital of Pakistan in 3 points?"}))