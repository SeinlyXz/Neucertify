import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="neucertifydb",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

def login(email: str, password: str):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM instansi WHERE email = %(email)s AND password = %(password)s", {
            "email": email,
            "password": password
        })
        user = cur.fetchone()
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
    finally:
        cur.close()
    return user