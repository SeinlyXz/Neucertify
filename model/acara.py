from lib.db import conn
from psycopg2.errors import DatabaseError

def get_all_acara():
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM acara a JOIN detail_acara da ON a.id_acara = da.id_acara JOIN instansi i ON i.id_instansi = da.id_instansi")
            acaras = cur.fetchall()
            acara_ = []
            for acara in acaras:
                new_acara = {
                    "id_acara": acara[0],
                    "nama_acara": acara[1],
                    "keterangan": acara[2],
                    "id_instansi": acara[4]
                }
                acara_.append(new_acara)
            return acara_
        except DatabaseError:
            conn.rollback()
            return None
        
def get_all_acara_by_instansi(email:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM acara a JOIN detail_acara da ON a.id_acara = da.id_acara JOIN instansi i ON i.id_instansi = da.id_instansi WHERE i.email = %(email)s", {
                "email": email
            })
            acaras = cur.fetchall()
            acara_ = []
            for acara in acaras:
                new_acara = {
                    "id_acara": acara[0],
                    "nama_acara": acara[1],
                    "keterangan": acara[2],
                    "id_instansi": acara[4]
                }
                acara_.append(new_acara)
        except DatabaseError:
            conn.rollback()
            return None
        
def create_acara(acara:str, keterangan:str, id_instansi:str):
    with conn.cursor() as cur:
        try:
            # Find latest id_acara
            cur.execute("SELECT id_acara FROM acara ORDER BY id_acara DESC LIMIT 1")
            id_acara = cur.fetchone()[0]
            id_acara_ = "ACR"+str(int(id_acara[3:])+1)
            
            # Generate KD Acara
            kd_acara = keterangan.upper()[:3]

            # Insert into acara
            cur.execute("INSERT INTO acara (id_acara, acara, keterangan, id_instansi, kd_acara) VALUES (%(id_acara)s, %(acara)s, %(keterangan)s, %(id_instansi)s,%(kd_acara)s)", {
                "id_acara": id_acara_,
                "acara": acara,
                "keterangan": keterangan,
                "id_instansi": id_instansi,
                "kd_acara": kd_acara
            })
            conn.commit()
            return id_acara_
        except DatabaseError:
            conn.rollback()
            return None