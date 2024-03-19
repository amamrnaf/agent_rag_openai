
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
import os
import openai
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.core import Settings
from llama_index.llms.replicate import Replicate


# Settings.embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")

os.environ["REPLICATE_API_TOKEN"] = "r8_JdicPBAHRT7nv3Db33v8TU7XQw2phYZ0nyKcy"
os.environ['COHERE_API_KEY'] = 'tz56cKLq6j4PdFKXEW9K9XGOF4spOnCHHENAaY8W'
os.environ["OPENAI_API_KEY"] = "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"
os.environ["ANTHROPIC_API_KEY"] = "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"
os.environ["LANGCHAIN_API_KEY"] = 'ls__8d4ee31314974e8eb9d2c2247f1af642'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
openai.api_key = os.environ["OPENAI_API_KEY"]


# tokenizer = Anthropic().tokenizer
# Settings.tokenizer = tokenizer

llm = Replicate(
    model="meta/llama-2-70b-chat",
    max_tokens=1024,
)

# llm = Anthropic(model="claude-3-opus-20240229")

# llm = OpenAI(temperature=0.1,model="gpt-4")

# llm = Ollama(model="llama2:70b", request_timeout=1000.0)
