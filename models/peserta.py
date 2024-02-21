from lib.db import conn
from psycopg2.errors import DatabaseError

def get_all_peserta(q:str = None):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_peserta, nama_peserta, email, no_telp, hadir, id_instansi FROM peserta")
            pesertas = cur.fetchall()
            peserta_ = []
            for peserta in pesertas:
                new_peserta = {
                    "id_peserta": peserta[0],
                    "nama": peserta[1],
                    "email": peserta[2],
                    "no_telp": peserta[3],
                    "kehadiran": peserta[4],
                    "id_instansi": peserta[5]
                }
                peserta_.append(new_peserta)
            return peserta_
        except DatabaseError:
            conn.rollback()
            return None

def get_all_peserta_by_instansi(email: str, q:str = None):
    with conn.cursor() as cur:
        try:
            if q is not None:
                cur.execute("select p.id_peserta, p.nama_peserta, p.email, p.no_telp, p.hadir, p.id_instansi from peserta p join instansi i on i.id_instansi = p.id_instansi where i.email = %(email)s and (p.nama_peserta ilike %(query)s or p.email ilike %(query)s)", {
                    "email": email,
                    "query": f"%{q}%"
                })
            else:
                cur.execute("select p.id_peserta, p.nama_peserta, p.email, p.no_telp, p.hadir, p.id_instansi from peserta p join instansi i on i.id_instansi = p.id_instansi where i.email = %(email)s", {
                    "email": email
                })
            pesertas = cur.fetchall()
            peserta_ = []
            if len(pesertas) == 0:
                return None
            for peserta in pesertas:
                new_peserta = {
                    "id_peserta": peserta[0],
                    "nama": peserta[1],
                    # "email": peserta[2],
                    # "no_telp": peserta[3],
                    # "kehadiran": peserta[4],
                    # "id_instansi": peserta[5]
                }
                peserta_.append(new_peserta)
            return peserta_
        except DatabaseError:
            conn.rollback()
            return None

def create_peserta(nama:str, email:str, no_telp:str, id_instansi:str, nik:str, id_acara:str):
    with conn.cursor() as cur:
        try:
            # Get the last id_peserta which is PS stand for Peserta
            cur.execute("SELECT id_peserta FROM peserta ORDER BY id_peserta DESC LIMIT 1")
            last_id = cur.fetchone()
            if last_id is None:
                last_id = "PS000"
            else:
                last_id = last_id[0]
            last_id = last_id[2:]
            new_id = int(last_id) + 1
            new_id = "PS" + str(new_id).zfill(3)

            cur.execute("INSERT INTO peserta (id_peserta, nama_peserta, email, nik, no_telp, id_instansi, id_acara) VALUES (%(id_peserta)s, %(nama)s, %(email)s, %(nik)s, %(no_telp)s, %(id_instansi)s, %(id_acara)s)", {
                "id_peserta": new_id,
                "nama": nama,
                "email": email,
                "nik": nik,
                "no_telp": no_telp,
                "id_instansi": id_instansi,
                "id_acara": id_acara
            })
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False

def get_peserta_by_id(id:str, id_instansi:str = None):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_peserta, nama_peserta, email, no_telp, hadir, id_instansi FROM peserta WHERE id_peserta = %(id)s and id_instansi = %(id_instansi)s", {
                "id": id,
                "id_instansi": id_instansi
            })
            peserta = cur.fetchone()
            if peserta is None:
                return None
            new_peserta = {
                "id_peserta": peserta[0],
                "nama": peserta[1],
                "email": peserta[2],
                "no_telp": peserta[3],
                "kehadiran": peserta[4],
                "id_instansi": peserta[5]
            }
            return new_peserta
        except DatabaseError:
            conn.rollback()
            return None
        
def update_peserta(id:str, nama:str, email:str, no_telp:str, id_instansi:str, hadir:str):
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE peserta SET nama_peserta = %(nama)s, email = %(email)s, no_telp = %(no_telp)s, hadir = %(hadir)s WHERE id_peserta = %(id)s and id_instansi = %(id_instansi)s", {
                "id": id,
                "nama": nama,
                "email": email,
                "no_telp": no_telp,
                "id_instansi": id_instansi,
                "hadir": hadir
            })
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False