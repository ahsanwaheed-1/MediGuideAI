import os
from langchain_openai import ChatOpenAI
from src.prompts import NARRATIVE_CHAT_TEMPLATE

def get_llm(model_name: str = "gpt-4.1-nano", temperature: float = 0.0):
    """Initializes and returns the ChatOpenAI model."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=api_key,
        streaming=True
    )

def get_assessment_chain(llm):
    """Builds and returns a reusable LLMChain (LCEL) for assessment."""
    return NARRATIVE_CHAT_TEMPLATE | llm

def stream_narrative(llm, inputs: dict):
    """
    Generator that streams the output from the LLM.
    `inputs` should contain:
    - age, gender, conditions, medications, symptoms, duration, severity, notes, language
    - chat_history: List of BaseMessage objects
    """
    chain = get_assessment_chain(llm)
    for chunk in chain.stream(inputs):
        if chunk.content:
            yield chunk.content
