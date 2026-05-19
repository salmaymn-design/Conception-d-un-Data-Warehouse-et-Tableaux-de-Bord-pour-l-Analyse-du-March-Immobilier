import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# ==================================================
# CONNECTION
# ==================================================

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ==================================================
# LOAD CLEAN DATA
# ==================================================

df = pd.read_sql("SELECT * FROM clean.clean_darkom", engine)

print("Data loaded:", len(df))

# ==================================================
# 1. DIM VILLE
# ==================================================

dim_ville = df[['ville']].drop_duplicates().reset_index(drop=True)
dim_ville['id_ville'] = dim_ville.index + 1

# ==================================================
# 2. DIM TYPE BIEN
# ==================================================

dim_type = df[['type_bien']].drop_duplicates().reset_index(drop=True)
dim_type['id_type_bien'] = dim_type.index + 1

# ==================================================
# 3. DIM TRANSACTION
# ==================================================

dim_transaction = df[['transaction']].drop_duplicates().reset_index(drop=True)
dim_transaction['id_transaction'] = dim_transaction.index + 1

# ==================================================
# 4. DIM TEMPS
# ==================================================

dim_temps = df[['date_publication','annee_publication','mois_publication','trimestre_publication']].drop_duplicates()
dim_temps = dim_temps.reset_index(drop=True)
dim_temps['id_temps'] = dim_temps.index + 1

# ==================================================
# 5. FACT TABLE
# ==================================================

fact = df.copy()

# merge dimensions

fact = fact.merge(dim_ville, on='ville', how='left')
fact = fact.merge(dim_type, on='type_bien', how='left')
fact = fact.merge(dim_transaction, on='transaction', how='left')
fact = fact.merge(dim_temps, on=[
    'date_publication',
    'annee_publication',
    'mois_publication',
    'trimestre_publication'
], how='left')

# ==================================================
# SELECT FACT COLUMNS
# ==================================================

fact_table = fact[[
    'annonce_id',
    'id_ville',
    'id_type_bien',
    'id_transaction',
    'id_temps',
    'prix',
    'surface',
    'prix_m2',
    'nb_chambres',
    'nb_salles_bain',
    'etage',
    'annee_construction',
    'age_bien',
    'categorie_prix',
    'categorie_surface'
]]

# ==================================================
# LOAD INTO POSTGRES (BI SCHEMA)
# ==================================================

dim_ville.to_sql("dim_ville", engine, schema="bi_schema", if_exists="replace", index=False)
dim_type.to_sql("dim_type_bien", engine, schema="bi_schema", if_exists="replace", index=False)
dim_transaction.to_sql("dim_transaction", engine, schema="bi_schema", if_exists="replace", index=False)
dim_temps.to_sql("dim_temps", engine, schema="bi_schema", if_exists="replace", index=False)

fact_table.to_sql("fact_annonces", engine, schema="bi_schema", if_exists="replace", index=False)

# ==================================================
# RESULT
# ==================================================

print("DATA WAREHOUSE CREATED SUCCESSFULLY 🚀")

print("Fact rows:", len(fact_table))
print("Dimensions created:")
print("Ville:", len(dim_ville))
print("Type Bien:", len(dim_type))
print("Transaction:", len(dim_transaction))
print("Temps:", len(dim_temps))