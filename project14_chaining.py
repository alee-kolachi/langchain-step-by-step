"""
LANGCHAIN TUTORIAL — ADVANCED CHAINS
------------------------------------

This file demonstrates the following concepts using:
Groq Llama-3.1 + LangChain Runnables

1. Simple chain
2. Sequential chain
3. Parallel chain (RunnableParallel)
4. Conditional branching chain (RunnableBranch)

Each example has clear comments for tutorial purposes.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()  # Load API keys


# -------------------------------------------------------------------
# 1. SIMPLE CHAIN
# -------------------------------------------------------------------
def simple_chain():
    """
    Basic prompt → LLM → text parser chain.
    """

    prompt = PromptTemplate(
        template="Generate 2 interesting facts about {facts}",
        input_variables=["facts"]
    )

    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()

    chain = prompt | llm | parser

    output = chain.invoke({"facts": "black people in early era"})
    print("\n----- SIMPLE CHAIN -----")
    print(output)


# -------------------------------------------------------------------
# 2. SEQUENTIAL CHAIN
# -------------------------------------------------------------------
def sequential_chain():
    """
    Step-by-step pipeline:
      1. Generate a long report
      2. Summarize that report in 4 bullet points
    """

    prompt1 = PromptTemplate(
        template="Generate a detailed report on: {topic}",
        input_variables=["topic"]
    )

    prompt2 = PromptTemplate(
        template="Generate a 4 point summary from this text:\n{text}",
        input_variables=["text"]
    )

    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()

    # Pipeline: REPORT → SUMMARY
    chain = prompt1 | llm | parser | prompt2 | llm | parser

    print("\n----- SEQUENTIAL CHAIN -----")
    print(chain.invoke({"topic": "Unemployment in Pakistan"}))


# -------------------------------------------------------------------
# 3. PARALLEL CHAIN
# -------------------------------------------------------------------
def parallel_chain():
    """
    Run two chains in parallel:
        - notes generator
        - question generator
    Then merge outputs.
    """

    llm_1 = ChatGroq(model="llama-3.1-8b-instant")
    llm_2 = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()

    prompt_notes = PromptTemplate(
        template="Generate short and simple notes from this text:\n{text}",
        input_variables=["text"]
    )

    prompt_quiz = PromptTemplate(
        template="Generate 4 short questions from this text:\n{text}",
        input_variables=["text"]
    )

    prompt_merge = PromptTemplate(
        template="Merge the notes and quiz into one document.\n\nNOTES:\n{notes}\n\nQUIZ:\n{quiz}",
        input_variables=["notes", "quiz"]
    )

    # Parallel execution (RunnableParallel)
    parallel = RunnableParallel({
        "notes": prompt_notes | llm_1 | parser,
        "quiz":  prompt_quiz  | llm_2 | parser
    })

    # Merge stage
    merge_chain = prompt_merge | llm_1 | parser

    # Full pipeline
    chain = parallel | merge_chain

    text = """
Black is a racial classification of people based on skin tone, commonly used in
Western societies. The term varies widely by culture, context, and history. It 
is considered a social construct by modern anthropologists.
    """

    print("\n----- PARALLEL CHAIN -----")
    result = chain.invoke({"text": text})
    print(result)


# -------------------------------------------------------------------
# 4. CONDITIONAL CHAIN (RunnableBranch)
# -------------------------------------------------------------------
def conditional_chain():
    """
    Branching pipeline:
        1. Classify sentiment using Pydantic structured output
        2. If positive → generate positive reply
           If negative → generate negative reply
           Otherwise → fallback
    """

    class Feedback(BaseModel):
        sentiment: Literal["positive", "negative"] = Field(
            description="Sentiment of feedback"
        )

    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser_text = StrOutputParser()
    parser_json = PydanticOutputParser(pydantic_object=Feedback)

    # Step 1: classify sentiment
    prompt_classifier = PromptTemplate(
        template=(
            "Classify the sentiment of this feedback as positive or negative:\n"
            "{feedback}\n\n"
            "{format_instructions}"
        ),
        input_variables=["feedback"],
        partial_variables={"format_instructions": parser_json.get_format_instructions()}
    )

    classifier_chain = prompt_classifier | llm | parser_json

    # Step 2: conditional branches
    prompt_positive = PromptTemplate(
        template="Write a professional response to this positive feedback:\n{feedback}",
        input_variables=["feedback"]
    )

    prompt_negative = PromptTemplate(
        template="Write a professional response to this negative feedback:\n{feedback}",
        input_variables=["feedback"]
    )

    # Branch logic
    branch = RunnableBranch(
        (lambda x: x.sentiment == "positive", prompt_positive | llm | parser_text),
        (lambda x: x.sentiment == "negative", prompt_negative | llm | parser_text),
        RunnableLambda(lambda x: "Could not detect sentiment.")
    )

    chain = classifier_chain | branch

    feedback_text = "This is a terrible device. It doesn't work and won't charge."
    result = chain.invoke({"feedback": feedback_text})

    print("\n----- CONDITIONAL CHAIN -----")
    print(result)


# -------------------------------------------------------------------
# RUN ANY CHAIN YOU WANT
# -------------------------------------------------------------------
if __name__ == "__main__":
    simple_chain()
    sequential_chain()
    parallel_chain()
    conditional_chain()

