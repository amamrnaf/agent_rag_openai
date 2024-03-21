from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import VectorStoreIndex,PromptTemplate
from sql_database_connection import sql_database, engine
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse 
from llama_index.core.retrievers import SQLRetriever
from typing import List
from llm import llm
from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    InputComponent,
)



# set Logging to DEBUG for more detailed outputs
table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
(SQLTableSchema(
        table_name="codification",
        context_str="This table stores information about douane position tarifaire with their respective codes, names, and categories. Each entry represents a unique code associated with a specific douane position, providing details about the corresponding name and category."
)),
(SQLTableSchema(
        table_name="importers",
        context_str="This table contains information about importers, including their names, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique importer, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="exporters",
    context_str="This table stores information about exporters, including their names, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique exporter, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="document_required",
    context_str="This table contains information about required documents, including document numbers, names, libelle d'extrait, issuers, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique document requirement, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="import_duty",
    context_str="This table records information about import duties, including Duty Import (DI), Taxe Provisoire d'Importation (TPI), Taxe sur la Valeur Ajoutée (TVA), the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique set of import duty details, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="annual_import",
    context_str="This table contains information about annual imports, including the year, weight in kg, value in dh, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique set of import data for a specific year, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="annual_export",
    context_str="This table contains information about annual exports, including the year, weight in kg, value in dh, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique set of export data for a specific year, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="clients",
    context_str="This table stores information about clients, including the country, value in dh, weight in kg, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique client record, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="fournisseurs",
    context_str="This table stores information about fournisseurs (suppliers), including the country, value in dh, weight in kg, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique supplier record, linked to a specific codification entry through the 'codification_id' foreign key."
)),
(SQLTableSchema(
    table_name="accord_convention",
    context_str="This table stores information about accords and conventions, including the country, agreement details, DI percentage, TPI percentage, the corresponding douane position tarifaire codes ('code'), and the unique codification entry they are associated with. Each entry represents a unique record for an accord or convention, linked to a specific codification entry through the 'codification_id' foreign key."
)),
]  # add a SQLTableSchema for each table

obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)

obj_retriever = obj_index.as_retriever(similarity_top_k=3)

query_engine = SQLTableRetrieverQueryEngine(
    sql_database, obj_index.as_retriever(similarity_top_k=1)
)

sql_retriever = SQLRetriever(sql_database)

def get_table_context_str(table_schema_objs: List[SQLTableSchema]):
    """Get table context string."""
    context_strs = []
    for table_schema_obj in table_schema_objs:
        table_info = sql_database.get_single_table_info(
            table_schema_obj.table_name
        )
        if table_schema_obj.context_str:
            table_opt_context = " The table description is: "
            table_opt_context += table_schema_obj.context_str
            table_info += table_opt_context

        context_strs.append(table_info)
    return "\n\n".join(context_strs)

table_parser_component = FnComponent(fn=get_table_context_str)

def parse_response_to_sql(response: ChatResponse) -> str:
    """Parse response to SQL."""
    response = response.message.content
    sql_query_start = response.find("SQLQuery:")
    if sql_query_start != -1:
        response = response[sql_query_start:]
        # TODO: move to removeprefix after Python 3.9+
        if response.startswith("SQLQuery:"):
            response = response[len("SQLQuery:") :]
    sql_result_start = response.find("SQLResult:")
    if sql_result_start != -1:
        response = response[:sql_result_start]
    return response.strip().strip("```").strip()

sql_parser_component = FnComponent(fn=parse_response_to_sql)

text2sql_prompt_template = """Given an input question, first create a syntactically correct {dialect} query to run. Then, examine the results of the query and return the answer. Order the results by a relevant column to provide the most interesting examples from the database.

Avoid querying for all columns from a specific table; only request a few relevant columns based on the question. Ensure the use of column names present in the schema description, and do not query for non-existent columns. Pay attention to the placement of columns in their respective tables, and qualify column names with the table name when necessary. Use the 'CAST' function to treat strings as numbers for numerical columns .

Follow the format below, with each element on a separate line:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only utilize tables listed below:
{schema}

Question: {query_str}
SQLQuery: """

templatee= PromptTemplate(text2sql_prompt_template)

text2sql_prompt = templatee.partial_format(
    dialect=engine.dialect.name
)
response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results without any limitations. Ensure that the full set of relevant information is included in your answer.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {context_str}\n"
    "Response: "
)
response_synthesis_prompt = PromptTemplate(
    response_synthesis_prompt_str,
)


qp = QP(
    modules={
        "input": InputComponent(),
        "table_retriever": obj_retriever,
        "table_output_parser": table_parser_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_output_parser": sql_parser_component,
        "sql_retriever": sql_retriever,
        "response_synthesis_prompt": response_synthesis_prompt,
        "response_synthesis_llm": llm,
    },
    verbose=True,
)

qp.add_chain(["input", "table_retriever", "table_output_parser"])
qp.add_link("input", "text2sql_prompt", dest_key="query_str")
qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
qp.add_chain(
    ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
)
qp.add_link(
    "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
)
qp.add_link(
    "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
)
qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
qp.add_link("response_synthesis_prompt", "response_synthesis_llm")  





