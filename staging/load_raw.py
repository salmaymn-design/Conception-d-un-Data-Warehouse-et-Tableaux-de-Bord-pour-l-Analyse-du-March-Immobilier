import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# تحميل .env
load_dotenv()

# تحديد المسار الصحيح للمشروع
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# مسار CSV
CSV_FILE = os.path.join(BASE_DIR, "data", "darkom_annonces.csv")

# الاتصال بقاعدة البيانات
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# قراءة CSV
df = pd.read_csv(CSV_FILE)

# إدخال البيانات
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO staging.staging_darkom (
            annonce_id,
            date_publication,
            titre,
            ville,
            quartier,
            type_bien,
            transaction,
            prix,
            surface,
            nb_chambres,
            nb_salles_bain,
            etage,
            annee_construction
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))

conn.commit()

cur.close()
conn.close()

print("✅ Data loaded successfully into staging")