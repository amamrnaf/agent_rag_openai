from flask import Flask, request, jsonify
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from unitedPdfsTool import Pdf_toolVector
from seperatedPdfsTool import query_engine_tools
from TICTool import TIC_tool
from doc_required_tool import DocsRequired
from Taxes_tool import ImportDuties
from sql_query import NL2SQLfn
from codification_tool import PositionTarifaire

app = Flask(__name__)


NL2SQLtool = FunctionTool.from_defaults(
    fn=NL2SQLfn,
    description="useful for asking an engine of trade data (imports,suppliers,...) with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY,the tool queries one table at a time so you may have to split your inqueries"
)

DocsRequiredtool = FunctionTool.from_defaults(
    fn=DocsRequired,
    description="useful for asking an engine of required decuments for importing a specific product with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY,the tool queries one table that are associated to a hs code or a name"
)

taxestool = FunctionTool.from_defaults(
    fn=ImportDuties,
    description="useful for asking an engine for datas on DI,TVA and TPI of specific product with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY,the tool queries one table that are associated to a HS code or a name"
)

positiontarifairetool = FunctionTool.from_defaults(
    fn=PositionTarifaire,
    description="useful for asking an engine of datas on HS(poistion tarifaire) codification,name,category and the chapter it belongs to with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY."
)

agent = ReActAgent.from_tools([NL2SQLtool,taxestool,DocsRequiredtool,positiontarifairetool,Pdf_toolVector,TIC_tool], llm=llm, verbose=True)
 
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
