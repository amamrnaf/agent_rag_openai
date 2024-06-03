from sqlalchemy import MetaData, Table, create_engine
from llama_index.core import SQLDatabase

# This is a Read-only user do not change!!!!!
database_connection_string = 'mysql://aiuser:topnegoce@192.168.2.134/Adildb'
engine = create_engine(database_connection_string)

# Create a MetaData object
metadata = MetaData()

# Reflect the existing tables
codification_table = Table('codification', metadata, autoload_with=engine)
importers_table = Table('importers_info', metadata, autoload_with=engine)
exporters_table = Table('exporters_info', metadata, autoload_with=engine)
fournisseurs_table = Table('fournisseurs_info', metadata, autoload_with=engine)
clients_table = Table('clients_info', metadata, autoload_with=engine)
annual_export_table = Table('annual_export_info', metadata, autoload_with=engine)
annual_import_table = Table('annual_import_info', metadata, autoload_with=engine)
import_duty_table = Table('import_duty_info', metadata, autoload_with=engine)
document_required_table = Table('document_required_info', metadata, autoload_with=engine)


sql_database = SQLDatabase(engine)






