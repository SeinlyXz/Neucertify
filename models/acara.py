from lib.db import conn
from psycopg2 import DatabaseError

def get_all_acara():
    with conn.cursor() as cur:
        try:
            cur.execute("select id_acara, acara, keterangan, id_instansi from acara a")
            acaras = cur.fetchall()
            acara_ = []
            for acara in acaras:
                new_acara = {
                    "id_acara": acara[0],
                    "nama_acara": acara[1],
                    "keterangan": acara[2],
                    "id_instansi": acara[3]
                }
                acara_.append(new_acara)
            conn.commit()
            return acara_
        except DatabaseError:
            conn.rollback()
            return None
        
def get_all_acara_by_instansi(email:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM acara a JOIN instansi i ON i.id_instansi = a.id_instansi WHERE i.email = %(email)s", {
                "email": email
            })
            acaras = cur.fetchall()

            if len(acaras) == 0:
                return None

            acara_ = []
            for acara in acaras:
                new_acara = {
                    "id_acara": acara[0],
                    "nama_acara": acara[1],
                    "keterangan": acara[2],
                    "id_instansi": acara[3]
                }
                acara_.append(new_acara)
            return acara_
        except DatabaseError:
            conn.rollback()
            return None

def get_acara_by_id(id_acara:str, id_user:str = None):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT a.id_acara, a.acara, a.keterangan, da.status, da.link_acara, a.kd_acara FROM acara a full JOIN detail_acara da ON a.id_acara = da.id_acara JOIN instansi i ON i.id_instansi = a.id_instansi where a.id_acara = %(id_acara)s and a.id_instansi = %(id_instansi)s", {
                "id_acara": id_acara,
                "id_instansi": id_user
            })
            acara = cur.fetchone()

            if acara == None:
                return None
            
            new_acara = {
                "id_acara": acara[0],
                "nama_acara": acara[1],
                "keterangan": acara[2],
                "status": acara[3],
                "link_acara": acara[4],
                "kd_acara": acara[5],
                "id_instansi": id_user,
            }
            return new_acara
        except DatabaseError:
            conn.rollback()
            return None

def check_is_verified(id_user:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM instansi WHERE id_instansi = %(id_instansi)s and verified = 'true'", {
                "id_instansi": id_user
            })
            acara = cur.fetchone()

            if acara is None:
                return None
            
            conn.commit()
        except DatabaseError:
            conn.rollback()
            return None
    return True

def create_acara(acara:str, keterangan:str, id_instansi:str):
    with conn.cursor() as cur:
        try:
            # Find latest id_acara
            cur.execute("SELECT id_acara FROM acara ORDER BY id_acara DESC LIMIT 1")
            id_acara = cur.fetchone()
            if id_acara == None:
                id_acara_ = "ACR1"
            else:
                _id_acara = str(id_acara[0])
                id_acara_ = "ACR"+str(int(_id_acara[3:])+1)
            
            # Generate KD Acara
            kd_acara = acara.upper()[:3]

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

def create_detail_acara(id_acara:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_detail_acara FROM detail_acara ORDER BY id_detail_acara DESC LIMIT 1")
            id_detail_acara = cur.fetchone()

            if id_detail_acara == None:
                id_detail_acara_ = "DTL1"
            else:
                _id_detail_acara = str(id_detail_acara[0])
                # id_acara_ = "DTL"+str(int(_id_detail_acara[3:])+1)
                id_detail_acara_ = "DTL"+str(int(_id_detail_acara[3:])+1)

            # Use on development only
            link = "https://meet.google.com/abc-123-xyz"
            # ------------------------
            cur.execute("INSERT INTO detail_acara (id_detail_acara, link_acara, id_acara) VALUES (%(id_detail_acara)s, %(id_acara)s, %(link_acara)s)", {
                "link_acara": link,
                "id_detail_acara": id_detail_acara_,
                "id_acara": id_acara
            })
            conn.commit()
            return id_detail_acara_
        except DatabaseError:
            conn.rollback()
            return None

def update_acara(id_acara:str, acara:str, keterangan:str, id_instansi:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT a.acara, a.keterangan, a.id_instansi, a.kd_acara FROM acara a WHERE a.id_acara = %(id_acara)s and a.id_instansi = %(id_instansi)s", {
                "id_acara": id_acara,
                "id_instansi": id_instansi
            })
            acara_ = cur.fetchone()

            if acara_ is None:
                return None

            acara = acara or acara_[0]
            keterangan = keterangan or acara_[1]
            id_instansi = id_instansi or acara_[2]
            kd_acara = acara.upper()[:3] or acara_[3]

            cur.execute("UPDATE acara SET acara = %(acara)s, keterangan = %(keterangan)s, kd_acara = %(kd_acara)s WHERE id_acara = %(id_acara)s", {
                "acara": acara,
                "keterangan": keterangan,
                "id_acara": id_acara,
                "kd_acara": kd_acara
            })
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False
        
def update_detail_acara(id_acara:str, status:str, link:str):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_acara, status, link_acara FROM detail_acara WHERE id_acara = %(id_acara)s", {
                "id_acara": id_acara
            })
            detail_acara_ = cur.fetchone()

            if detail_acara_ == None:
                return False
            
            status = status or detail_acara_[1]
            link = link or detail_acara_[2]

            cur.execute("UPDATE detail_acara SET status = %(status)s, link_acara = %(link)s WHERE id_acara = %(id_acara)s", {
                "status": status,
                "link": link,
                "id_acara": id_acara
            })
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False
        
def delete_acara(id_acara:str, id_instansi:str):
    with conn.cursor() as cur:
        try:
            cur.execute("DELETE FROM acara WHERE id_acara = %(id_acara)s and id_instansi = %(id_instansi)s", {
                "id_acara": id_acara,
                "id_instansi": id_instansi
            })

            if cur.rowcount == 0:
                return False
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False