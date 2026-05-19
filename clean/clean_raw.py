import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime

# =========================
# CONFIG
# =========================
load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df = pd.read_sql("SELECT * FROM staging.staging_darkom", engine)

print("Lignes initiales :", len(df))

# =========================
# CLEANING NA
# =========================
df = df.replace(r'^\s*$', np.nan, regex=True)
df = df.replace(["NaN", "nan", "NULL", "null"], np.nan)

# =========================
# DUPLICATES
# =========================
print("Doublons :", df.duplicated('annonce_id').sum())
df = df.drop_duplicates('annonce_id')

# =========================
# MISSING VALUES
# =========================
df.fillna({
    'quartier': 'Inconnu',
    'type_bien': 'Appartement',
    'transaction': 'Vente',
    'nb_chambres': 0,
    'nb_salles_bain': 0,
    'etage': 0,
    'ville': 'Inconnu',
    'annee_construction': datetime.now().year
}, inplace=True)

# =========================
# TYPES
# =========================
df['date_publication'] = pd.to_datetime(df['date_publication'], errors='coerce')
df = df.dropna(subset=['date_publication'])

cols_num = ['prix','surface','nb_chambres','nb_salles_bain','etage','annee_construction']
df[cols_num] = df[cols_num].apply(pd.to_numeric, errors='coerce')
df = df.dropna(subset=['prix','surface'])



# =========================
# OUTLIERS FILTER (IQR)
# =========================

def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

# appliquer IQR sur les colonnes numériques importantes
for col in ['prix', 'surface', 'nb_chambres']:
    df = remove_outliers_iqr(df, col)


# =========================
# STANDARDIZATION
# =========================
df['ville'] = df['ville'].str.strip().str.title()

df['type_bien'] = df['type_bien'].str.lower().map({
    'appartement':'Appartement',
    'villa':'Villa',
    'terrain':'Terrain',
    'bureau':'Bureau'
}).fillna('Autre')

df['transaction'] = df['transaction'].str.lower().map({
    'vente':'Vente',
    'location':'Location'
}).fillna('Autre')

# =========================
# FEATURES
# =========================
df['prix_m2'] = np.where(df['surface'] > 0, df['prix']/df['surface'], np.nan)

year = datetime.now().year
df['age_bien'] = np.where(df['annee_construction'] <= year, year - df['annee_construction'], np.nan)

df['categorie_prix'] = pd.cut(
    df['prix'],
    bins=[0,300000,800000,2000000,1e12],
    labels=['Economique','Moyen','Haut Standing','Luxe']
)

df['categorie_surface'] = pd.cut(
    df['surface'],
    bins=[0,80,150,1e12],
    labels=['Petit','Moyen','Grand']
)

# =========================
# TIME DIMENSIONS
# =========================
df['annee_publication'] = df['date_publication'].dt.year
df['mois_publication'] = df['date_publication'].dt.month
df['trimestre_publication'] = df['date_publication'].dt.quarter

# =========================
# LOAD CLEAN LAYER
# =========================
df.to_sql('clean_darkom', engine, schema='clean', if_exists='replace', index=False)

print("Clean layer OK ✔")
print("Final rows :", len(df))
print("NULL restants :\n", df.isnull().sum())