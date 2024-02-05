from lib.db import conn
from psycopg2.errors import DatabaseError

def get_all_peserta():
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

def get_all_peserta_by_instansi(email: str):
    with conn.cursor() as cur:
        try:
            cur.execute("select p.id_peserta, p.nama_peserta, p.email, p.no_telp, p.hadir, p.id_instansi from peserta p join instansi i on i.id_instansi = p.id_instansi where i.email = %(email)s", {
                "email": email
            })
            pesertas = cur.fetchall()
            peserta_ = []
            if peserta_ is None:
                return None
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

def create_peserta(nama:str, email:str, no_telp:str, id_instansi:str, nik:str, id_acara:str):
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO peserta (nama_peserta, email, no_telp, id_instansi) VALUES (%(nama)s, %(email)s, %(no_telp)s, %(id_instansi)s)", {
                "nama": nama,
                "email": email,
                "no_telp": no_telp,
                "id_instansi": id_instansi
            })
            conn.commit()
            return True
        except DatabaseError:
            conn.rollback()
            return False

def get_peserta_by_id(id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_peserta, nama_peserta, email, no_telp, hadir, id_instansi FROM peserta WHERE id_peserta = %(id)s", {
                "id": id
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