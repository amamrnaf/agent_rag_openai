from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.core.query_pipeline import QueryPipeline,InputComponent
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os
from llama_index.core import (
    VectorStoreIndex,
    Settings
)
from llm import llm,parser


PERSIST_DIR = "./storageDoauneCode"
if not os.path.exists(PERSIST_DIR):
    file_extractor = {".pdf": parser}
    reader = SimpleDirectoryReader("./pdff", file_extractor=file_extractor)
    documents = reader.load_data()
    Settings.context_window = 4096
    Settings.num_output = 256
    index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=20)], llm=llm)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

retriever = index.as_retriever(similarity_top_k=5)
reranker = CohereRerank()
summarizer = TreeSummarize(llm=llm)

# define query pipeline
p = QueryPipeline(verbose=True)
p.add_modules(
    {
        "input":InputComponent(),
        # "prompt":prompt_tmpl,
        "retriever": retriever,
        "llm":llm,
        "summarizer": summarizer,
        "reranker": reranker,
    }
)


p.add_link("input", "retriever")
p.add_link("retriever", "reranker", dest_key="nodes")
p.add_link("input", "reranker", dest_key="query_str")
p.add_link("reranker", "summarizer", dest_key="nodes")
p.add_link("input", "summarizer", dest_key="query_str")


def coude_douane_tool(user_question: str) -> str:
    """Process a user question and return the response."""
   
    response = p.run(query=user_question)
    return response

