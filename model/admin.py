from psycopg2 import IntegrityError
from lib.db import conn
from psycopg2.errors import DatabaseError

def create(email: str, password: str):
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO admin (email, password) VALUES (%(email)s, %(password)s)", {
                "email": email,
                "password": password
            })
            conn.commit()
        except IntegrityError:
            conn.rollback()
            raise ("Email sudah terdaftar")
        except DatabaseError:
            conn.rollback()
            raise ("Terjadi kesalahan pada database")
    return True

def get_user(email: str, password: str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT email, password FROM admin WHERE email = %(email)s AND password = %(password)s", {
                "email": email,
                "password": password
            })
            user = cur.fetchone()
            if user is None:
                return None
            user_ = {
                "email": user[0],
                "password": user[1]
            }
        except DatabaseError:
            conn.rollback()
            return None
    return user_