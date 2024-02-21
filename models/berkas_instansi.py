from lib.db import conn
from psycopg2.errors import DatabaseError
import os

def upload(berkas:str, id_instansi:str, ktp:str):
    berkas = f"/{berkas}"
    ktp = f"/{ktp}"
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO berkas_instansi (path_berkas_pemerintah,id_instansi,path_ktp) VALUES (%(path_berkas)s, %(id_instansi)s, %(path_ktp)s)", {
                "path_berkas": berkas,
                "id_instansi": id_instansi,
                "path_ktp": ktp
            })
            conn.commit()
        except DatabaseError:
            conn.rollback()
            return None
        finally:
            cur.close()
    return True

def delete(id_instansi:str):
    with conn.cursor() as cur:
        try:
            # get the path of the berkas_instansi and ktp
            cur.execute("SELECT path_berkas_pemerintah, path_ktp FROM berkas_instansi WHERE id_instansi = %(id_instansi)s", {
                "id_instansi": id_instansi
            })
            berkas = cur.fetchone()
            
            if berkas is None:
                return None

            berkas_pemerintah = berkas[0]
            ktp = berkas[1]
            if berkas_pemerintah is not None and ktp is not None:
                # delete "/" from the path
                berkas_pemerintah = berkas_pemerintah[1:]
                ktp = ktp[1:]
                if os.path.exists(berkas_pemerintah) and os.path.exists(ktp):
                    print("File exists berkas instansi")
                    os.remove(berkas_pemerintah)
                    os.remove(ktp)
            # delete the record from the table
            cur.execute("DELETE FROM berkas_instansi WHERE id_instansi = %(id_instansi)s", {
                "id_instansi": id_instansi
            })
            conn.commit()
        except DatabaseError:
            conn.rollback()
            return None
        finally:
            cur.close()
    return True