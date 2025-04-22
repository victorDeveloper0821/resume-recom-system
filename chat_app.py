from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from rankingMachine import search_and_format
import sys


if "torch" in sys.modules:
    del sys.modules["torch.classes"]

# Setup Ollama LLM
llm = OllamaLLM(model="gemma3:1b")

# Prompt template
template = """You are a resume recommendation assistant.
You are given search results of top resumes and must summarize or highlight key of all five resumes information for the user.
Please remember to show the resume ID.

Resume Search Results:
{search_results}

User Request:
{question}

Answer:"""
prompt = PromptTemplate(input_variables=["search_results", "question"], template=template)
chain = prompt | llm

def run_agent(query):
    resumes = search_and_format(query)
    return chain.invoke({"search_results": resumes, "question": query})
