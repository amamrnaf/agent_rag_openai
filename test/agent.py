from flask import Flask, request, jsonify
from sql_query import NL_2_SQL_fn
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from query_decomposition import generate_queries_decomposition
from pdf_query import process_question
from TIC_query import process_questionTIC

# from pdf_query import Pdf_tool
app = Flask(__name__)

NL_2_SQL_tool = FunctionTool.from_defaults(
    fn=NL_2_SQL_fn,
    description="useful for querying the customs database with natural language,you can decompose what you wanna learn from the database and ask a question at a time.DO NOT use a sql command"
)

Pdf_tool = FunctionTool.from_defaults(
    fn=process_question,
    description= "A comprehensive set of documents outlining the classification and specifications of various products, including chemicals and industrial goods, for the purpose of tariffs and regulations."
)

TIC_tool = FunctionTool.from_defaults(
    fn=process_questionTIC,
    description= "The document details moroccan domestic consumption tax (taxe intérieure de consommation TIC)."
)


agent = ReActAgent.from_tools([NL_2_SQL_tool,Pdf_tool,TIC_tool], llm=llm, verbose=True)
 
@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.json
    user_input = data.get('user_input', '') 
    
    if not user_input:
        return jsonify({'error': 'Please provide a user input'}), 400

    try:
        # Assuming agent.chat returns a string or a serializable object
        response = agent.chat(user_input)
        # Modify the response as needed to ensure JSON serializability
        # json_response = {'response': str(response)}
        return str(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
