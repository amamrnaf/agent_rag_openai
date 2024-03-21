from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from llama_index.core.agent import ReActAgent

# Decomposition
template = """You are a helpful assistant that generates multiple sub-questions related to an input question for Moroccan customs. 
The objective is to break down the input into a set of sub-problems / sub-questions that can be answered individually and are as straightforward as possible. 
Generate several search queries relevant to: {question}
Output (3 queries):"""


prompt_decomposition = ChatPromptTemplate.from_template(template)

# LLM
llm = ChatOpenAI(temperature=0)

# Chain
generate_queries_decomposition = ( prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n")))
