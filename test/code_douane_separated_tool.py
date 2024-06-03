# All tools VectorIndex version
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
    ChatPromptTemplate,
)
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.core.tools import QueryEngineTool, ToolMetadata,FunctionTool
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
import llama_index.core
import json
from llm import llm

# with open('chemist_circ.json', 'r') as file:
#     data = json.load(file)

#     for item in data:
        
#         circular_number = item.get('circular_number', 'N/A')
#         date = item.get('date', 'N/A')
#         objet = item.get('objet', 'N/A')
#         reference = item.get('reference', 'N/A')
#         file_name = item.get('file', 'N/A')

       
              

def create_tools_for_chapters(json_file):
    tools = []
    with open(f"{json_file}.json", 'r') as file:
        data = json.load(file)

        for index,item in enumerate(data):
            title = item.get('title', 'N/A')
            file = item.get('file', 'N/A')
            # Load or generate index
            try:
                storage_context = StorageContext.from_defaults(
                    persist_dir=f"./code_douane_storage/{index}"
                )
                index = load_index_from_storage(storage_context)
            except:
                # Load data
                docs = SimpleDirectoryReader(
                    input_files=[f"./doaune_pdfs/{file}"]
                ).load_data()

                # Set context window and number of output tokens
                Settings.context_window = 4096
                Settings.num_output = 256

                # Build index
                index = VectorStoreIndex.from_documents(docs, transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=20)], llm=llm)

                # Persist index
                index.storage_context.persist(persist_dir=f"./circulaire_prod_chimie_store/{index}")

            # Define chat templates
            chat_text_qa_msgs = [
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content="Always answer the question, even if the context isn't helpful."
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=(
                        "Context below.\n"
                        "{context_str}\n"
                        "Given documents and context below, "
                        "answer the question: {query_str}\n"
                    ),
                ),
            ]

            # Simplify and condense messages for refinement template
            chat_refine_msgs = [
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content="Always answer the question, even if the context isn't helpful."
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=(
                        "Refine the original answer with more context below.\n"
                        "{context_msg}\n"
                        "Given new context, refine the original answer: {query_str}. "
                        "If context isn't useful, output the original answer.\n"
                        "Original Answer: {existing_answer}"
                    ),
                ),
            ]   

            text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
            refine_template = ChatPromptTemplate(chat_refine_msgs)
            # Query engine setup
            engine = index.as_query_engine(
                text_qa_template=text_qa_template,
                refine_template=refine_template,
                llm=llm,
                similarity_top_k=3,
            )

            # Tool definition
            tool = QueryEngineTool(
                query_engine=engine,
                metadata=ToolMetadata(
                    object =f"code de doaune",
                    description=(
                        f"tool sur {title}"
                    ),
                ),
            )
            
            tools.append(tool)

    return tools

# Create tools for the specified chapters
query_engine_tools = create_tools_for_chapters('chemist_circ')