from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()


def simple_chain():
    prompt = PromptTemplate(
        template="Generate 2 interesting facts about {facts}",
        input_variables=["facts"]
    )

    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()

    chain = prompt | llm | parser
    output = chain.invoke({"facts": "black people in early era"})

    print(output)


def sequential_chain():
    prompt1 = PromptTemplate(
        template="Generate a detailed report on {topic}",
        input_variables=["topic"]
    )

    prompt2 = PromptTemplate(
        template="Generate a 4 pointer summary from the following text:\n {text}",
        input_variables=["text"]
    )
    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()

    chain = prompt1 | llm | parser | prompt2 | llm | parser

    print(chain.invoke({"topic": "Unemployement in Pakistan"}))


def parallel_chain():
    llm_1 = ChatGroq(model="llama-3.1-8b-instant")
    llm_2 = ChatGroq(model="llama-3.1-8b-instant")

    prompt1 = PromptTemplate(
        template="Generate short and simple notes from the following: \n {text}",
        input_variables=["text"]
    )


    prompt2 = PromptTemplate(
        template="Generate 4 short question from the following text: \n {text}",
        input_variables=["text"]
    )

    prompt3 = PromptTemplate(
        template="Merge the provided notes and quiz into the single document.\n notes -> {notes}, quiz -> {quiz}",
        input_variables=["notes", "quiz"]
    )

    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "notes": prompt1 | llm_1 | parser,
        "quiz": prompt2 | llm_2 | parser
    })

    merge_chain = prompt3 | llm_1 | parser

    chain = parallel_chain | merge_chain

    text = """
Black is a racial classification of people, usually a political and skin color-based category for specific populations with a mid- to dark brown complexion. Often in countries with socially based systems of racial classification in the Western world, the term "black" is used to describe persons who are perceived as darker-skinned in contrast to other populations. It is most commonly used for people of sub-Saharan African ancestry, Indigenous Australians, Melanesians, and Negritos, though it has been applied in many contexts to other groups, and is no indicator of any close ancestral relationship whatsoever. However, not all people considered "black" have dark skin and often additional phenotypical characteristics are relevant, such as certain facial and hair-texture features. Indigenous African societies do not use the term black as a racial identity outside of influences brought by Western cultures.

Contemporary anthropologists and other scientists, while recognizing the reality of biological variation between different human populations, regard the concept of a "Black race" as social construct.[1] Different societies apply different criteria regarding who is classified "black", and these social constructs have changed over time. In a number of countries, societal variables affect classification as much as skin color, and the social criteria for "blackness" vary. Some perceive the term 'black' as a derogatory, outdated, reductive or otherwise unrepresentative label, and as a result neither use nor define it, especially in African countries with little to no history of colonial racial segregation.[2]

In the anglosphere, the term can carry a variety of meanings depending on the country. While the term "person of color" is commonly used and accepted in the United States,[3] the near-sounding term "colored person" is considered highly offensive, except in South Africa, where it is a descriptor for a person of mixed race. In other regions such as Australia and Melanesia, settlers applied the adjective "black" to the indigenous population. It was universally regarded as highly offensive in Australia until the 1960s and 1970s. "Black" was generally not used as a noun, but rather as an adjective qualifying some other descriptor (e.g. "black ****"). As desegregation progressed after the 1967 referendum, some Indigenous Australians adopted the term, following the American fashion, but it remains problematic.[4]
"""
    resutls = chain.invoke({"text": text})

    print (resutls)

def conditional_chain():

    class Feedback(BaseModel):
        sentiment: Literal["positive", "negative"] = Field(description="Give the sentiment of the feedback.")

    llm = ChatGroq(model="llama-3.1-8b-instant")
    parser = StrOutputParser()
    parser2 = PydanticOutputParser(pydantic_object=Feedback)

    prompt1 = PromptTemplate(
        template="Classify the sentiment of the following feeback text into positive or negative:\n{feedback}\n{format_instructions}",
        input_variables=["feedback"],
        partial_variables={"format_instructions": parser2.get_format_instructions()}
    )

    classifier_chain = prompt1 | llm | parser2

    prompt2 = PromptTemplate(
        template="Write an appropriate response to this positive feedback:\n{feedback}",
        input_variables=["feedback"]
    )

    prompt3 = PromptTemplate(
        template="Write an appropriate response to this negative feedback:\n{feedback}",
        input_variables=["feedback"]
    )

    branch_chain = RunnableBranch(
        (lambda x:x.sentiment == "positive", prompt2 | llm | parser),
        (lambda x:x.sentiment == "negative", prompt3 | llm | parser),
        RunnableLambda(lambda x: "Could not find sentiment")
        
    )

    chain = classifier_chain | branch_chain
    result = chain.invoke({"feedback": "This is very terrible device that is neither working nor charging."})
    print(result)




conditional_chain()
