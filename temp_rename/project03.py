from langchain_groq import ChatGroq
from langchain.tools import tool, BaseTool, InjectedToolArg
from pydantic import BaseModel, Field
from typing import Type, Annotated
from langchain.messages import HumanMessage
import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

class ConverterInput(BaseModel):
    base_currency: str = Field(..., description="base currency to convert from")
    target_currency: str = Field(..., description="target currency to convert to")

class ConverterTool(BaseTool):
    name: str = "get_conversion_factor"
    description: str = "This tool fetches the currency conversion factor between a given base currency and a target currency"
    args_schema: Type[BaseModel] = ConverterInput

    def _run(self, base_currency: str, target_currency: str) -> float:
        CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
        url = f"https://api.freecurrencyapi.com/v1/latest?apikey={CURRENCY_API_KEY}&base_currency={base_currency}&currencies={target_currency}"
        response = requests.get(url)
        data = response.json()["data"]
        print("Data", data)
        return data

@tool
def convert(base_currency_value: int, conversion_factor: Annotated[float, InjectedToolArg]) -> float:
    """Given a currency conversion rate, this function calculates the target currency value from the given base currency value"""
    return base_currency_value * conversion_factor

get_conversion_factor = ConverterTool()

llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tool = llm.bind_tools([get_conversion_factor, convert])

messages = [HumanMessage("What is the conversion factor between USD and EUR, based on that Convert 100 USD to EUR")]
ai_message = llm_with_tool.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    print("Tool call", tool_call)
    if tool_call['name'] == "get_conversion_factor":
        tool_message_1 = get_conversion_factor.invoke(tool_call)
        conversion_rate = json.loads(tool_message_1.content)[tool_call["args"]["target_currency"]]
        messages.append(tool_message_1)
    if tool_call["name"] == "convert":
        tool_call['args']['conversion_rate'] = conversion_rate
        tool_message_2 = convert.invoke(tool_call)
        messages.append(tool_message_2)

print(messages)
print(llm_with_tool.invoke(messages).content)