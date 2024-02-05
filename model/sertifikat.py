from psycopg2 import IntegrityError
from lib.db import conn
from psycopg2.errors import DatabaseError

def get_all_sertifikat():
    with conn.cursor() as cur:
        try:
            cur.execute("select s.id_sertifikat, p.nama_peserta, s.id_peserta from sertifikat s join peserta p on p.id_peserta = s.id_peserta")
            sertifikats = cur.fetchall()
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

def create_sertifikat():
    try:
        with conn.cursor() as cur:
            # Get the count of participants
            cur.execute("SELECT COUNT(*) FROM participants")
            num_participants = cur.fetchone()[0]

            # Fetch the IDs of all participants
            cur.execute("SELECT id_peserta FROM participants")
            participant_ids = cur.fetchall()

            if num_participants == 0:
                return False, "No participants found, cannot create certificates"

            # Generate and insert certificates for each participant
            for participant_id in participant_ids:
                # Generate a new certificate ID
                cur.execute("SELECT id_sertifikat FROM sertifikat ORDER BY id_sertifikat DESC LIMIT 1")
                latest_cert_id = cur.fetchone()
                if latest_cert_id:
                    updated_id = int(latest_cert_id[0][4:]) + 1
                else:
                    updated_id = 1
                new_id = f"SERT{updated_id}"

                # Insert the new certificate
                cur.execute("INSERT INTO sertifikat (id_sertifikat, id_peserta) VALUES (%s, %s)", (new_id, participant_id))
            
            conn.commit()
            return True, f"{num_participants} certificates created"
    except (DatabaseError, Exception) as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        return False, str(e)

def get_sertifikat_by_instansi(id:str, email:str):
    try:
        with conn.cursor() as cur:
            cur.execute("select s.id_sertifikat, p.nama_peserta from sertifikat s join peserta p on p.id_peserta = s.id_peserta join instansi i on i.id_instansi = p.id_instansi where i.id_instansi = %(id)s and i.email = %(email)s",{
                "id": id,
                "email": email
            })
            sertifikats = cur.fetchall()
            sertifikat_ = []
            for sertifikat in sertifikats:
                new_sertifikat = {
                    "id": sertifikat[0],
                    "nama_peserta": sertifikat[1]
                }
                sertifikat_.append(new_sertifikat)
            return sertifikat_
    except DatabaseError:
        conn.rollback()
        return None

