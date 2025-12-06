

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
    Simple mock tool that returns JSON weather data based on a city name.
    Real API integration can replace this function later.
    """
    city_lower = city.lower()

    # Basic branching to simulate different weather responses
    if "lahore" in city_lower:
        data = {"city": city, "temp_c": 28, "condition": "Cloudy"}
    elif "london" in city_lower:
        data = {"city": city, "temp_c": 12, "condition": "Rain"}
    else:
        # Default weather for unspecified cities
        data = {"city": city, "temp_c": 22, "condition": "Clear"}

    # Tools must always return strings (often JSON strings)
    return json.dumps(data)


# ---------------------------------------------------------
# 2. Modern Structured Output using Pydantic
# ---------------------------------------------------------

class WeatherOutput(BaseModel):
    """
    Defines the exact JSON structure the agent must return.
    The model enforces the fields and types in the final output.
    """
    city: str = Field(..., description="The city requested")
    temp_c: int = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition")
    advice: str = Field(..., description="Short advice for the user")

# Parser that turns model output into this structured Pydantic object
parser = PydanticOutputParser(pydantic_object=WeatherOutput)


# ---------------------------------------------------------
# 3. Initialize latest LLM
# ---------------------------------------------------------

# ChatGroq wrapper for Llama 3.1 model
llm = ChatGroq(model="llama-3.1-8b-instant")


# ---------------------------------------------------------
# 4. Create Agent (LATEST API)
# ---------------------------------------------------------

# System prompt that forces:
# - mandatory tool usage
# - mandatory JSON output
# - strict adherence to the Pydantic format
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

# Creates an agent with tool-calling capabilities and custom prompt
agent = create_agent(
    model=llm,
    tools=[fetch_weather],
    system_prompt=system_prompt
)


# ---------------------------------------------------------
# 5. Run Demo
# ---------------------------------------------------------

def run_demo():
    """
    Sends multiple sample queries to the agent, prints raw JSON output,
    then parses it into a Pydantic model for structured usage.
    """
    queries = [
        "What's the weather in Lahore today?",
        "Tell me weather for London with advice.",
        "Weather in Karachi please."
    ]

    for q in queries:
        print("\n" + "=" * 60)
        print("USER:", q)

        # Invoke agent with message-based input format
        result = agent.invoke({"messages": [{"role": "user", "content": q}]})

        # Extract only AI messages from agent output
        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        final = ai_messages[-1].content  # last AI message = final output

        print("\nRaw model output:")
        print(final)

        # Attempt to parse JSON using the Pydantic parser
        try:
            parsed = parser.parse(final)
            print("\nParsed structured output:")
            print(parsed.model_dump())
        except Exception as e:
            print("Parsing error:", e)

        print("=" * 60)


# Entry point
if __name__ == "__main__":
    run_demo()
