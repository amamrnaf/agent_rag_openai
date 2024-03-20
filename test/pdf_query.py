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

def initialize_index():
    """Initialize or load the index."""
    PERSIST_DIR = "./storageDAG"
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader("./content").load_data()
        Settings.context_window = 4096
        Settings.num_output = 256
        llm =  OpenAI(
            temperature=0.2,
            model="gpt-3.5-turbo",
            context_window=Settings.context_window,
            num_output=Settings.num_output
        )
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

def process_question(user_question: str) -> str:
    """Process a user question and return the response."""
    context_str = "The document delineates regulations concerning chapter 29 for HS codificationsthat starts with 29."
    response = query_pipeline.run(query_str=user_question, context_str=context_str)
    return response

# # Example usage:
# user_question = input("Please input your question: ")
# response = process_question(user_question)
# print(response)


Pdf_tool = FunctionTool.from_defaults(fn=process_question,description= "Useful for searching for regulations concerning chapters 27(COMBUSTIBLES MINERAUX, HUILES MINERALES ET PRODUITS DE LEUR DISTILLATION; MATIERES BITUMINEUSES; CIRES MINERALES),28(PRODUITS DES INDUSTRIES CHIMIQUES OU DES INDUSTRIES CONNEXES),29(PRODUITS CHIMIQUES ORGANIQUES).")