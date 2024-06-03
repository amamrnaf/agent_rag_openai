from flask import Flask, request, jsonify
from llm import llm
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from doc_required_tool import DocsRequired
from Taxes_tool import ImportDuties
from sql_query import NL2SQLfn
from codification_tool import PositionTarifaire
from prompt import new_tmpl
from code_douane_tool import coude_douane_tool
app = Flask(__name__)


NL2SQLtool = FunctionTool.from_defaults(
    fn=NL2SQLfn,
    description="useful for questionning with natural language about a database importers/exporters,suppliers/clients,yearly imports/exports,the database is in FRENCH"
)

DocsRequiredtool = FunctionTool.from_defaults(
    fn=DocsRequired,
    description="useful for asking an engine of required decuments for importing a specific product with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY"
)

taxesTool = FunctionTool.from_defaults(
    fn=ImportDuties,
    description="useful for asking an engine for datas on DI,TVA and TPI of specific product with NATURAL LANGUAGE IN FRENCH,DO NOT USE A SQL QUERY"
)

positiontarifairetool = FunctionTool.from_defaults(
    fn=PositionTarifaire,
    description="useful for questionning with natural language about a database on HS(poistion tarifaire) codification,name,category and the chapter it belongs to."
)

douane_tool = FunctionTool.from_defaults(
    fn=coude_douane_tool,
    description="useful for searching through morrocan dahirs and law on customs and regulations."
)

agent = ReActAgent.from_tools(
        tools=[NL2SQLtool,taxesTool,DocsRequiredtool,positiontarifairetool], 
        llm=llm, 
        verbose=True,
        )
agent.update_prompts(
    {"agent_worker:system_prompt": new_tmpl}
)
 
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
