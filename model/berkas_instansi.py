from lib.db import conn
from psycopg2.errors import DatabaseError

def upload(berkas:str, id_instansi:str, ktp:str):
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO berkas_instansi (path_berkas,id_instansi,path_ktp) VALUES (%(path_berkas)s, %(id_instansi)s, %(path_ktp)s)", {
                "path_berkas": berkas,
                "id_instansi": id_instansi,
                "path_ktp": ktp
            })
            conn.commit()
        except DatabaseError:
            conn.rollback()
            return None
    return True