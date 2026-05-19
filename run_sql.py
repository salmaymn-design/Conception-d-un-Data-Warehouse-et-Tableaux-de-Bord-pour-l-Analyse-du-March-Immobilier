import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

with open("init.sql", "r", encoding="utf-8") as file:
    sql = file.read()

cur.execute(sql)
conn.commit()

cur.close()
conn.close()

print("✅ SQL executed successfully")