from sqlalchemy import MetaData, Table, create_engine
from llama_index.core import SQLDatabase


# Assuming you already have an SQLAlchemy engine (e.g., from your Flask app)
# Replace 'your_database_connection_string' with your actual connection string
database_connection_string = 'mysql://root:@192.168.2.134/Adildb'
engine = create_engine(database_connection_string)

# Create a MetaData object
metadata = MetaData()

# Reflect the existing tables
codification_table = Table('codification', metadata, autoload_with=engine)
importers_table = Table('importers', metadata, autoload_with=engine)
exporters_table = Table('exporters', metadata, autoload_with=engine)
fournisseurs_table = Table('fournisseurs', metadata, autoload_with=engine)
clients_table = Table('clients', metadata, autoload_with=engine)
annual_export_table = Table('annual_export', metadata, autoload_with=engine)
annual_import_table = Table('annual_import', metadata, autoload_with=engine)
import_duty_table = Table('import_duty', metadata, autoload_with=engine)
document_required_table = Table('document_required', metadata, autoload_with=engine)

included_tables=["codification","importers","exporters","import_duty","clients","document_required","annual_import","annual_export","fournisseurs"]

sql_database = SQLDatabase(engine)






