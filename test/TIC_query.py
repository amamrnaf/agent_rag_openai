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

def initialize_index():
    """Initialize or load the index."""
    PERSIST_DIR = "./storageTIC"
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader("./contentTIC").load_data()
        Settings.context_window = 4096
        Settings.num_output = 256
        embed_model = OpenAIEmbedding(embed_batch_size=42)
        Settings.embed_model = embed_model
        llm =  OpenAI(
            temperature=0.2,
            model="gpt-4",
            context_window=Settings.context_window,
            num_output=Settings.num_output
        )
        index = VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)], llm=llm, embed_model=embed_model)
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

    retriever = index.as_retriever(similarity_top_k=3)
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

def process_questionTIC(user_question: str) -> str:
    """Process a user question and return the response."""
    context_str = "The document is a Moroccan legal decree from October 9, 1977, outlining tax rates and regulations for various goods subject to domestic consumption taxes."
    response = query_pipeline.run(query_str=user_question, context_str=context_str)
    return response

TIC_tool = FunctionTool.from_defaults(fn=process_questionTIC,description= "The document details moroccan domestic consumption tax (taxe intérieure de consommation TIC).")