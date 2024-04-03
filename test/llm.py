
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.replicate import Replicate
# from llama_index.llms.anthropic import Anthropic
import os
from llama_index.llms.huggingface import (
    HuggingFaceInferenceAPI,
    HuggingFaceLLM,
)
from typing import List, Optional
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.core import Settings
# import logging
# import sys

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# from IPython.display import Markdown, display

import llama_index.core

llama_index.core.set_global_handler("simple")
Settings.embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")

os.environ['COHERE_API_KEY'] = 'tz56cKLq6j4PdFKXEW9K9XGOF4spOnCHHENAaY8W'
# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "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"
os.environ["ANTHROPIC_API_KEY"] = "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"

HF_TOKEN: Optional[str] = os.getenv("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")
# tokenizer = Anthropic().tokenizer
# Settings.tokenizer = tokenizer

llm_sql = HuggingFaceInferenceAPI(
    model_name="MaziyarPanahi/sqlcoder-7b-Mistral-7B-Instruct-v0.2-slerp-GGUF"
)
# llm = Anthropic(model="claude-3-opus-20240229")

# llm = OpenAI(temperature=0.1,model="gpt-4")

llm = Ollama(model="mixtral",base_url="http://192.168.2.201:11434" ,request_timeout=300.0)

