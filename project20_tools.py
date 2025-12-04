from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
#print(search_tool.invoke("recent news of pakistan?"))


from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(..., description="The first number in the function")
    b: int = Field(..., description="The second number in the function")

def multiply(a: int, b: int) -> int:
    return a * b

multiply_tool = StructuredTool.from_function(
    func=multiply,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)

#print(multiply_tool)
#print(multiply_tool.invoke({"a":3, "b":5}))


############
from langchain.tools import BaseTool
from typing import Type

class MultiplyInput(BaseModel):
    a: int = Field(..., description="The first number in the function")
    b: int = Field(..., description="The second number in the function")

class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"

    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, a: int, b: int) -> int:
        return a * b
    
multiply_tool = MultiplyTool()
#print(multiply_tool)
#print(multiply_tool.invoke({"a": 55, "b": 10}))



##################
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return the product"""
    return a * b

llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tool = llm.bind_tools([multiply_tool])

query = HumanMessage("How much is 6 when multiplied by 6")
messages = [query]
#print(messages)

result = llm_with_tool.invoke("How much is 6 when multiplied by 6")
messages.append(result)
#print(messages)
tool_result = multiply_numbers.invoke(result.tool_calls[0])
messages.append(tool_result)
print(messages)

print(llm_with_tool.invoke(messages))