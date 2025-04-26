from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from rankingMachine import search_and_format
import sys


if "torch" in sys.modules:
    del sys.modules["torch.classes"]

# Setup Ollama LLM
llm = OllamaLLM(model="gemma3:4b")

# Prompt template
template = """You are a resume recommendation assistant. Please analyze these five documents step by step, document by document.
always remember to show the resume ID.
You are given search results of top resumes and must summarize or highlight key of all five resumes information for the user.
If the user request has notiong to do with the retrieved resume, dont show any resume information, just answer the request by yourself, like 
having a casual chat.

Resume Search Results:
{search_results}

User Request:
{question}

Answer: """
prompt = PromptTemplate(input_variables=["search_results", "question"], template=template)
chain = prompt | llm

def run_agent(query):
    resumes = search_and_format(query)
    return chain.invoke({"search_results": resumes, "question": query})
