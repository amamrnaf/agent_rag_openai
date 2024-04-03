from flask import Flask, request, jsonify
from sql_query import qp
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from query_decomposition import generate_queries_decomposition
from unitedPdfsTool import Pdf_toolVector
from seperatedPdfsTool import query_engine_tools
from TICTool import TIC_tool
# from pdf_query import Pdf_tool
app = Flask(__name__)


def NL_2_SQL_fn(input):
    response = qp.run(query=input)
    return response

NL_2_SQL_tool = FunctionTool.from_defaults(
    fn=NL_2_SQL_fn,
    description="useful for querying a database of doaune numbers(imports,exports,...) with natural language,the tool queries one table at a time so you may have to split your inqueries,DO NOT use a sql command"
)
agent = ReActAgent.from_tools([NL_2_SQL_tool,Pdf_toolVector, *query_engine_tools, TIC_tool], llm=llm, verbose=True)
 
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
