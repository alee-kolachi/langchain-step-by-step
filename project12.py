"""
Project 12 — Agent + Pydantic Structured Output (Updated LangChain)

What this project demonstrates:
- Tool calling (fetch_weather)
- Modern structured output using PydanticOutputParser
- ChatGroq with latest LangChain agent API
"""

from dotenv import load_dotenv
import json
from typing import Optional
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import AIMessage

from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# ---------------------------------------------------------
# 1. Tool (Mock Weather API)
# ---------------------------------------------------------

@tool
def fetch_weather(city: str) -> str:
    """
    Mock weather tool. Returns JSON string with basic weather info.
    Replace this with a real API call if needed.
    """
    city_lower = city.lower()

    if "lahore" in city_lower:
        data = {"city": city, "temp_c": 28, "condition": "Cloudy"}
    elif "london" in city_lower:
        data = {"city": city, "temp_c": 12, "condition": "Rain"}
    else:
        data = {"city": city, "temp_c": 22, "condition": "Clear"}

    return json.dumps(data)


# ---------------------------------------------------------
# 2. Modern Structured Output using Pydantic
# ---------------------------------------------------------

class WeatherOutput(BaseModel):
    city: str = Field(..., description="The city requested")
    temp_c: int = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition")
    advice: str = Field(..., description="Short advice for the user")

parser = PydanticOutputParser(pydantic_object=WeatherOutput)


# ---------------------------------------------------------
# 3. Initialize latest LLM
# ---------------------------------------------------------

llm = ChatGroq(model="llama-3.1-8b-instant")


# ---------------------------------------------------------
# 4. Create Agent (LATEST API)
# ---------------------------------------------------------

system_prompt = f"""
You are a weather assistant.

When the user asks for weather:
- ALWAYS call the fetch_weather tool.
- You must ALWAYS reply with valid JSON.
No comments.
No explanations.
No extra text.
Only output in the following format:

{parser.get_format_instructions()}

Output must be valid JSON AND FOLLOWS THE FORMAT NOTHIGN ELSE REQUIRED.
"""

agent = create_agent(
    model=llm,
    tools=[fetch_weather],
    system_prompt=system_prompt
)


# ---------------------------------------------------------
# 5. Run Demo
# ---------------------------------------------------------

def run_demo():
    queries = [
        "What's the weather in Lahore today?",
        "Tell me weather for London with advice.",
        "Weather in Karachi please."
    ]

    for q in queries:
        print("\n" + "=" * 60)
        print("USER:", q)

        result = agent.invoke({"messages": [{"role": "user", "content": q}]})

        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        final = ai_messages[-1].content

        print("\nRaw model output:")
        print(final)

        # Parse into Pydantic object
        try:
            parsed = parser.parse(final)
            print("\nParsed structured output:")
            print(parsed.model_dump())
        except Exception as e:
            print("Parsing error:", e)

        print("=" * 60)


if __name__ == "__main__":
    run_demo()
