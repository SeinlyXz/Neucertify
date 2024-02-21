from psycopg2 import IntegrityError
from lib.db import conn
from psycopg2.errors import DatabaseError

def get_all_generated_sertifikat():
    with conn.cursor() as cur:
        try:
            cur.execute("select s.id_sertifikat, p.nama_peserta, s.id_peserta from sertifikat s join peserta p on p.id_peserta = s.id_peserta")
            sertifikats = cur.fetchall()
            if len(sertifikats) == 0:
                return None
            sertifikat_ = []
            for sertifikat in sertifikats:
                new_sertifikat = {
                    "id": sertifikat[0],
                    "nama_peserta": sertifikat[1],
                    "id_peserta": sertifikat[2]
                }
                sertifikat_.append(new_sertifikat)
            return sertifikat_
        except DatabaseError:
            conn.rollback()
            return None

def get_all_sertifikat(id_instansi:str):
    with conn.cursor() as cur:
        try:
            cur.execute("select * from sertifikat s where id_instansi = %(id_instansi)s",{
                "id_instansi": id_instansi
            })
            sertifikats = cur.fetchall()
            if len(sertifikats) == 0:
                return None
            sertifikat_ = []
            for sertifikat in sertifikats:
                new_sertifikat = {
                    "id": sertifikat[0],
                    "nama_peserta": sertifikat[1],
                    "id_peserta": sertifikat[2]
                }
                sertifikat_.append(new_sertifikat)
            return sertifikat_
        except DatabaseError:
            conn.rollback()
            return None

def get_sertifikat(id):
    with conn.cursor() as cur:
        try:
            cur.execute("select s.id_sertifikat, p.nama_peserta from sertifikat s join peserta p on p.id_peserta = s.id_peserta where s.id_peserta = %(id)s",{
                "id": id
            })
            sertifikat = cur.fetchone()
            data = {
                "id": sertifikat[0],
                "nama_peserta": sertifikat[1]
            }
            return data
        except DatabaseError:
            conn.rollback()
            return None


def generate_sertifikat(id_acara:str, waktu:str, id_instansi:str, id_serfitikat:str):
    try:
        with conn.cursor() as cur:
            cur.execute("select p.id_peserta, p.nama_peserta, p.id_acara, da.link_acara from peserta p join acara a on a.id_acara = p.id_acara join detail_acara da on da.id_acara = a.id_acara where p.id_instansi = %(id_instansi)s and p.id_acara = %(id_acara)s",{
                "id_instansi": id_instansi,
                "id_acara": id_acara
            })
            pesertas = cur.fetchall()
            if len(pesertas) == 0:
                return False
            peserta_ids = []
            for peserta in pesertas:
                list_peserta = {
                    "id_peserta": peserta[0],
                    "nama_peserta": peserta[1],
                    "id_acara": peserta[2],
                    "link": peserta[3]
                }
                peserta_ids.append(list_peserta)
            print(peserta_ids[0]["link"])
            for peserta_id in peserta_ids:
                cur.execute("insert into detail_sertifikat (link, id_sertifikat, waktu, id_peserta) values (%(link)s,%(id_sertifikat)s,%(waktu)s,%(id_peserta)s)",{
                    "id_sertifikat": id_serfitikat,
                    "id_peserta": peserta_id["id_peserta"],
                    "link": peserta_id["link"],
                    "waktu": waktu
                })
            conn.commit()
            return True, f"Sertifikat berhasil dibuat untuk {len(peserta_ids)} peserta."
    except (DatabaseError, Exception) as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        return False, str(e)


def create_sertifikat(id_instansi:str, id_acara:str):
    try:
        with conn.cursor() as cur:
            # get the last id_sertifikat
            cur.execute("select id_sertifikat from sertifikat order by id_sertifikat desc limit 1")
            last_id = cur.fetchone()
            if last_id is None:
                last_id = "SERT000"
            else:
                last_id = last_id[0]
            last_id = last_id[4:]
            new_id = int(last_id) + 1
            new_id = "SERT" + str(new_id).zfill(3)

            # Check if the acara is exist using where id_instansi and id_acara
            cur.execute("select id_acara from acara where id_instansi = %(id_instansi)s and id_acara = %(id_acara)s",{ 
                "id_instansi": id_instansi,
                "id_acara": id_acara
            })

            acara = cur.fetchone()
            if acara is None:
                return False

            cur.execute("insert into sertifikat(id_sertifikat, id_acara, id_instansi) values (%(id_sertifikat)s, %(id_acara)s, %(id_instansi)s)",{
                "id_sertifikat": new_id,
                "id_acara": id_acara,
                "id_instansi": id_instansi
            })
            conn.commit()
            return True
    except (DatabaseError, Exception) as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        return False, str(e)


def get_sertifikat_by_instansi(id:str, email:str):
    try:
        with conn.cursor() as cur:
            cur.execute("select * from sertifikat s where id_instansi = %(id_instansi)s",{
                "id_instansi": id,
            })
            sertifikats = cur.fetchall()
            if len(sertifikats) == 0:
                return None
            sertifikat_ = []
            for sertifikat in sertifikats:
                new_sertifikat = {
                    "id_sertifikat": sertifikat[0],
                }
                sertifikat_.append(new_sertifikat)
            return sertifikat_
    except DatabaseError:
        conn.rollback()
        return None
    
def get_detail_sertifikat(id_sertifikat:str, id_instansi):
    try:
        with conn.cursor() as cur:
            cur.execute("select s.id_sertifikat, p.nama_peserta, s.link, s.waktu from detail_sertifikat s join peserta p on p.id_peserta = s.id_peserta join instansi i on i.id_instansi = p.id_instansi where i.id_instansi = %(id_instansi)s and s.id_sertifikat = %(id_sertifikat)s",{
                "id_sertifikat": id_sertifikat,
                "id_instansi": id_instansi
            })
            sertifikats = cur.fetchall()
            if len(sertifikats) == 0:
                return None
            sertifikat_ = []
            for sertifikat in sertifikats:
                new_sertifikat = {
                    "id": sertifikat[0],
                    "nama_peserta": sertifikat[1],
                    "link": sertifikat[2],
                    "waktu": sertifikat[3]
                }
                sertifikat_.append(new_sertifikat)
            return sertifikat_
    except DatabaseError:
        conn.rollback()
        return None

def delete_sertifikat(id_sertifikat:str):
    try:
        with conn.cursor() as cur:
            cur.execute("delete from sertifikat where id_sertifikat = %(id_sertifikat)s",{
                "id_sertifikat": id_sertifikat
            })
            conn.commit()
            return True
    except DatabaseError:
        conn.rollback()
        return False
