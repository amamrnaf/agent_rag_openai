
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.replicate import Replicate
import os
from llama_index.llms.huggingface import (
    HuggingFaceInferenceAPI,
    HuggingFaceLLM,
)
from typing import List, Optional
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.core import Settings
import llama_index.core
from llama_parse import LlamaParse  #

llama_index.core.set_global_handler("simple")
Settings.embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")

HF_TOKEN: Optional[str] = os.getenv("")
os.environ['COHERE_API_KEY'] = ''
# os.environ["OPENAI_API_KEY"] = ""
# os.environ["OPENAI_API_KEY"] = ""
# os.environ["OPENAI_API_KEY"] = ""

parser = LlamaParse(
    api_key="llx-szNf94dIOrNKPkZQV0TzHWdUJQzU7XYciavl2H7iHmz9FN9W",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown"  # "markdown" and "text" are available
)

# llm = HuggingFaceLLM(
#     model_name="CohereForAI/c4ai-command-r-plus"
# )


# llm = OpenAI(temperature=0.1,model="gpt-4")

llm = Ollama(model="mixtral",base_url="http://192.168.2.201:11434" ,request_timeout=300.0)
llm_sql = Ollama(model="command-r:latest",base_url="http://192.168.2.201:11434" ,request_timeout=300.0)

