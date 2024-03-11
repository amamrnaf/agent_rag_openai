
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
import os
import openai

os.environ["OPENAI_API_KEY"] = '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'
os.environ["ANTHROPIC_API_KEY"] = "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"
os.environ["LANGCHAIN_API_KEY"] = 'ls__8d4ee31314974e8eb9d2c2247f1af642'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
openai.api_key = os.environ["OPENAI_API_KEY"]


# tokenizer = Anthropic().tokenizer
# Settings.tokenizer = tokenizer

# llm = Anthropic(model="claude-3-opus-20240229")

# llm = OpenAI(temperature=0.1,model="gpt-3.5-turbo")

llm = Ollama(model="llama2", request_timeout=30.0)