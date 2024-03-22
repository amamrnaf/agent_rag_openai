from sqlalchemy import create_engine, MetaData, Table, Column, String, text

# Define the database connection
engine = create_engine('mysql://root:@192.168.2.134/Adildb')

# Create a metadata object
metadata = MetaData()

# Define the columns for importers_info table
importers_info_columns = [
    Column('name', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the importers_info table schema
importers_info = Table(
    'importers_info',
    metadata,
    *importers_info_columns
)

# Define the columns for exporters_info table
exporters_info_columns = [
    Column('name', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the exporters_info table schema
exporters_info = Table(
    'exporters_info',
    metadata,
    *exporters_info_columns
)
# Define the columns for clients_info table
clients_info_columns = [
    Column('name', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the clients_info table schema
clients_info = Table(
    'clients_info',
    metadata,
    *clients_info_columns
)

# Define the columns for fournisseurs_info table
fournisseurs_info_columns = [
    Column('name', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the fournisseurs_info table schema
fournisseurs_info = Table(
    'fournisseurs_info',
    metadata,
    *fournisseurs_info_columns
)

document_required_info_columns = [
    Column('document_number', String(255)),
    Column('document_name', String(255)),
    Column('libelle_d_extrait', String(255)),
    Column('issuer', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the documents_required_info table schema
document_required_info = Table(
    'document_required_info',
    metadata,
    *document_required_info_columns
)

annual_import_info_columns = [
    Column('year', String(255)),
    Column('weight', String(255)),
    Column('value', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the annual_import_info table schema
annual_import_info = Table(
    'annual_import_info',
    metadata,
    *annual_import_info_columns
)

# Define the columns for annual_export_info table
annual_export_info_columns = [
    Column('year', String(255)),
    Column('weight', String(255)),
    Column('value', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the annual_export_info table schema
annual_export_info = Table(
    'annual_export_info',
    metadata,
    *annual_export_info_columns
)

# Define the columns for accord_convention_info table
accord_convention_info_columns = [
    Column('country', String(255)),
    Column('agreement', String(255)),
    Column('di_percentage', String(255)),
    Column('tpi_percentage', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the accord_convention_info table schema
accord_convention_info = Table(
    'accord_convention_info',
    metadata,
    *accord_convention_info_columns
)

import_duty_info_columns = [
    Column('DI', String(255)),
    Column('TPI', String(255)),
    Column('TVA', String(255)),
    Column('code', String(10)),
    Column('designation', String(1000)),
    Column('category', String(1000))
]

# Define the import_duty_info table schema
import_duty_info = Table(
    'import_duty_info',
    metadata,
    *import_duty_info_columns
)

metadata.create_all(engine)

# Construct the SELECT statement for importers_info table
stmt_importers_info = text("""
    SELECT importers.name AS name, importers.code AS code,
           codification.name AS designation, codification.category AS category
    FROM importers
    JOIN codification ON importers.code = codification.code
""")

# Construct the SELECT statement for exporters_info table
stmt_exporters_info = text("""
    SELECT exporters.name AS name, exporters.code AS code,
           codification.name AS designation, codification.category AS category
    FROM exporters
    JOIN codification ON exporters.code = codification.code
""")

stmt_clients = text("""
    SELECT clients.country AS country, clients.value AS value,
           clients.weight AS weight, clients.code AS code,
           codification.name AS designation, codification.category AS category
    FROM clients
    JOIN codification ON clients.code = codification.code
""")

stmt_fournisseurs = text("""
    SELECT fournisseurs.country AS country, fournisseurs.value AS value,
           fournisseurs.weight AS weight, fournisseurs.code AS code,
           codification.name AS designation, codification.category AS category
    FROM fournisseurs
    JOIN codification ON fournisseurs.code = codification.code
""")

stmt_document_required = text("""
    SELECT document_required.document_number AS document_number,
           document_required.document_name AS document_name,
           document_required.libelle_d_extrait AS libelle_d_extrait,
           document_required.issuer AS issuer,
           document_required.code AS code,
           codification.name AS designation, codification.category AS category
    FROM document_required
    JOIN codification ON document_required.code = codification.code
""")

stmt_annual_import = text("""
    SELECT annual_import.year AS year, annual_import.weight AS weight,
           annual_import.value AS value, annual_import.code AS code,
           codification.name AS designation, codification.category AS category
    FROM annual_import
    JOIN codification ON annual_import.code = codification.code
""")

stmt_annual_export = text("""
    SELECT annual_export.year AS year, annual_export.weight AS weight,
           annual_export.value AS value, annual_export.code AS code,
           codification.name AS designation, codification.category AS category
    FROM annual_export
    JOIN codification ON annual_export.code = codification.code
""")

stmt_accord_convention = text("""
    SELECT accord_convention.country AS country,
           accord_convention.agreement AS agreement,
           accord_convention.di_percentage AS di_percentage,
           accord_convention.tpi_percentage AS tpi_percentage,
           accord_convention.code AS code,
           codification.name AS designation, codification.category AS category
    FROM accord_convention
    JOIN codification ON accord_convention.code = codification.code
""")

stmt_import_duty =text("""
    SELECT import_duty.DI AS DI,
       import_duty.TPI AS TPI,
       import_duty.TVA AS TVA,
       import_duty.code AS code,
       codification.name AS designation,
       codification.category AS category
    FROM import_duty
    JOIN codification ON import_duty.code = codification.code;
""")
# Connect to the database
with engine.connect() as connection:

    try:
        # Begin a transaction
        trans = connection.begin()
        # connection.execute(importers_info.delete())

        # # Delete rows from exporters_info table
        # connection.execute(exporters_info.delete())
        
        # # Delete rows from clients_info table
        # connection.execute(clients_info.delete())

        # # Delete rows from fournisseurs_info table
        # connection.execute(fournisseurs_info.delete())
        
        # # Delete rows from document_required_info table
        # connection.execute(document_required_info.delete())
        
        # # Delete rows from annual_import_info table
        # connection.execute(annual_import_info.delete())
        
        # # Delete rows from annual_export_info table
        # connection.execute(annual_export_info.delete())
        
        # # Delete rows from accord_convention_info table
        # connection.execute(accord_convention_info.delete())
        # trans.commit()

        # # Begin another transaction
        # trans = connection.begin()

        # result_importers_info = connection.execute(stmt_importers_info)
        # for row in result_importers_info.fetchall():
        #     query = text("INSERT INTO importers_info (name, code, designation, category) VALUES (:name, :code, :designation, :category)")
        #     connection.execute(query, {"name": row[0], "code": row[1], "designation": row[2], "category": row[3]})
        
        # # Commit the transaction
        # trans.commit()

        # # Begin another transaction
        # trans = connection.begin()

        # # Insert rows into exporters_info table
        # result_exporters_info = connection.execute(stmt_exporters_info)
        # for row in result_exporters_info.fetchall():
        #     query = text("INSERT INTO exporters_info (name, code, designation, category) VALUES (:name, :code, :designation, :category)")
        #     connection.execute(query, {"name": row[0], "code": row[1], "designation": row[2], "category": row[3]})
        # trans.commit()
        # trans = connection.begin()

        # result_clients = connection.execute(stmt_clients)
        # for row in result_clients.fetchall():
        #     query = text("INSERT INTO clients_info (name, code, designation, category) VALUES (:name, :code, :designation, :category)")
        #     connection.execute(query, {"name": row[0], "code": row[1], "designation": row[4], "category": row[5]})
        #  # Commit the transaction
        # trans.commit()
        # trans = connection.begin()

    
        # # Insert rows into fournisseurs_info table
        # result_fournisseurs = connection.execute(stmt_fournisseurs)
        # for row in result_fournisseurs.fetchall():
        #     query = text("INSERT INTO fournisseurs_info (name, code, designation, category) VALUES (:name, :code, :designation, :category)")
        #     connection.execute(query, {"name": row[0], "code": row[1], "designation": row[4], "category": row[5]})
        #  # Commit the transaction
        # trans.commit()
        # trans = connection.begin()

        # # Insert rows into document_required_info table
        # result_document_required = connection.execute(stmt_document_required)
        # for row in result_document_required.fetchall():
        #     query = text("INSERT INTO document_required_info (document_number, document_name, libelle_d_extrait, issuer, code, designation, category) VALUES (:document_number, :document_name, :libelle_d_extrait, :issuer, :code, :designation, :category)")
        #     connection.execute(query, {"document_number": row[0], "document_name": row[1], "libelle_d_extrait": row[2], "issuer": row[3], "code": row[4], "designation": row[5], "category": row[6]})
        #  # Commit the transaction
        # trans.commit()
        # trans = connection.begin()

        # # Insert rows into annual_import_info table
        # result_annual_import = connection.execute(stmt_annual_import)
        # for row in result_annual_import.fetchall():
        #     query = text("INSERT INTO annual_import_info (year, weight, value, code, designation, category) VALUES (:year, :weight, :value, :code, :designation, :category)")
        #     connection.execute(query, {"year": row[0], "weight": row[1], "value": row[2], "code": row[3], "designation": row[4], "category": row[5]})
        #  # Commit the transaction
        # trans.commit()
        # trans = connection.begin()

        # # Insert rows into annual_export_info table
        # result_annual_export = connection.execute(stmt_annual_export)
        # for row in result_annual_export.fetchall():
        #     query = text("INSERT INTO annual_export_info (year, weight, value, code, designation, category) VALUES (:year, :weight, :value, :code, :designation, :category)")
        #     connection.execute(query, {"year": row[0], "weight": row[1], "value": row[2], "code": row[3], "designation": row[4], "category": row[5]})
        #  # Commit the transaction
        # trans.commit()
        # trans = connection.begin()

        # Insert rows into accord_convention_info table
        # result_accord_convention = connection.execute(stmt_accord_convention)
        # for row in result_accord_convention.fetchall():
        #     query = text("INSERT INTO accord_convention_info (country, agreement, di_percentage, tpi_percentage, code, designation, category) VALUES (:country, :agreement, :di_percentage, :tpi_percentage, :code, :designation, :category)")
        #     connection.execute(query, {"country": row[0], "agreement": row[1], "di_percentage": row[2], "tpi_percentage": row[3], "code": row[4], "designation": row[5], "category": row[6]})
        # trans.commit()
        # trans = connection.begin()

        # result_import_duty = connection.execute(stmt_import_duty)
        # for row in result_import_duty.fetchall():
        #     query = text("INSERT INTO import_duty_info (DI, TPI, TVA, code, designation, category) VALUES (:DI, :TPI, :TVA, :code, :designation, :category)")
        #     connection.execute(query, {"DI": row[0],"TPI": row[1],"TVA": row[2],"code": row[3],"designation": row[4],"category": row[5]})
        # # Commit the transaction
        trans.commit()
    
    except Exception as e:
        # Rollback the transaction in case of error
        trans.rollback()
        print(f"An error occurred: {e}")
    
