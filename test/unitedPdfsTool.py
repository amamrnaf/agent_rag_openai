# Vectorindex version
import os.path
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage)
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings,ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.response_synthesizers import TreeSummarize
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.embeddings.openai import OpenAIEmbedding
import llama_index.core

llama_index.core.set_global_handler("simple")
def initialize_index():
    """Initialize or load the index."""
    PERSIST_DIR = "./storageDAGPDF"
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader("./ProcessedPDFs").load_data()
        Settings.context_window = 4096
        Settings.num_output = 256
        index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=20)], llm=llm)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    return index

def initialize_query_pipeline():

    """Initialize the query pipeline."""
    chat_text_qa_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                "Always answer the question, even if the context isn't helpful."
            ),
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(
                "Context information is below.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the provided documents and context information below, "
                "answer the question: {query_str}\n"
            ),
        ),
    ]

    text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
    retriever = index.as_retriever(similarity_top_k=5)
    reranker = CohereRerank()
    summarizer = TreeSummarize(llm=llm)

    p = QueryPipeline(verbose=False)
    p.add_modules(
        {
            "llm": llm,
            "prompt_tmpl": text_qa_template,
            "retriever": retriever,
            "summarizer": summarizer,
            "reranker": reranker,
        }
    )
    p.add_link("prompt_tmpl", "llm")
    p.add_link("llm", "retriever")
    p.add_link("retriever", "reranker", dest_key="nodes")
    p.add_link("llm", "reranker", dest_key="query_str")
    p.add_link("reranker", "summarizer", dest_key="nodes")
    p.add_link("llm", "summarizer", dest_key="query_str")
    return p

index = initialize_index()
query_pipeline = initialize_query_pipeline()

def Pdf_toolVectorIndex(user_question: str) -> str:
    """Process a user question and return the response."""
    context_str = "These documents detail the classification and specifications of diverse products, encompassing a range of items from chemicals to industrial goods, for tariff and regulatory purposes."
    response = query_pipeline.run(query_str=user_question, context_str=context_str)
    return response

Pdf_toolVector = FunctionTool.from_defaults(fn=Pdf_toolVectorIndex,description= "This tool provides access to a comprehensive set of documents outlining the classification and specifications of various products, including chemicals and industrial goods, for tariff and regulatory purposes. The content is embedded and stored in a vector store, enabling efficient retrieval and processing of user queries.")
