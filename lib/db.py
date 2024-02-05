import psycopg2
from dotenv import load_dotenv
import os
import bcrypt

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
    admin = None
    user = None
    try:
        cur.execute("SELECT * FROM admin WHERE email = %(email)s", {"email": email})
        admin = cur.fetchone()

        cur.execute("SELECT * FROM instansi WHERE email = %(email)s", {"email": email})
        user = cur.fetchone()

        if user is not None:
            if bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
                return user

        if admin is not None:
            if bcrypt.checkpw(password.encode("utf-8"), admin[2].encode("utf-8")):
                return admin

    except Exception as e:
        conn.rollback()
        print(f"Error occurred: {e}")
    finally:
        cur.close()
    if admin is not None:
        return admin
    return user


def get_role(email: str):
    cur = conn.cursor()
    admin = None
    user = None
    _admin = None
    _user = None
    try:
        cur.execute("SELECT * FROM admin WHERE email = %(email)s", {
            "email": email,
        })
        admin = cur.fetchone()

        if(admin is not None):
            _admin = "admin"

        cur.execute("SELECT * FROM instansi WHERE email = %(email)s", {
            "email": email,
        })
        user = cur.fetchone()

        if(user is not None):
            _user = "user"

        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
    finally:
        cur.close()
    if admin is not None:
        return _admin
    return _user
def get_id_user(email:str):
    cur = conn.cursor()
    user = None
    admin = None
    _admin = None
    _user = None
    try:
        cur.execute("SELECT id_admin FROM admin WHERE email = %(email)s", {
            "email": email,
        })

        admin = cur.fetchone()
        if(admin is not None):
            _admin = admin[0]

        cur.execute("SELECT id_instansi FROM instansi WHERE email = %(email)s", {
            "email": email,
        })

        user = cur.fetchone()
        if(user is not None):
            _user = user[0]

        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
    finally:
        cur.close()
    if admin is not None:
        return _admin
    return _user