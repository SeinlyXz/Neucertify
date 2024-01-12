from psycopg2 import IntegrityError
from lib.db import conn
from psycopg2.errors import DatabaseError
from collections import OrderedDict

def fetchall(q=None):
    with conn.cursor() as cur:
        try:
            if q is not None:
                cur.execute("SELECT id_instansi, nama_instansi, alamat, cover, email FROM instansi WHERE nama_instansi ILIKE %(nama_instansi)s", {
                    "nama_instansi": f"%{q}%"
                })
            else:
                cur.execute("SELECT id_instansi, nama_instansi, alamat, cover, email FROM instansi")

            instansis = cur.fetchall()

            # Convert tuple to dictionary
            instansi_ = []
            for instansi in instansis:
                new_instansi = {
                    "id": instansi[0],
                    "nama_instansi": instansi[1],
                    "alamat_instansi": instansi[2],
                    "cover": instansi[3],
                    "email": instansi[4]
                }
                instansi_.append(new_instansi)
        except DatabaseError:
            conn.rollback()
            return None

    return instansi_

def fetch(id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_instansi, nama_instansi, alamat, cover FROM instansi WHERE id_instansi = %(id)s", {
                "id": id
            })
            instansi = cur.fetchone()

            if instansi is None:
                return None

            # Convert tuple to dictionary
            instansi_ = {
                "id": instansi[0],
                "nama_instansi": instansi[1],
                "alamat_instansi": instansi[2],
                "cover": instansi[3]
            }
        except DatabaseError:
            conn.rollback()
            return None
    return instansi_

def create(nama_instansi:str, email: str, password: str, no_telp: str, alamat: str, nomor_izin_pemerintah: str, file:str):
    # Example kode instansi: MA Ali Maksum -> MAL
    kode_instansi = "".join([x[0] for x in nama_instansi.split(" ")])

    with conn.cursor() as cur:
        try:
            # Get the latest numeric part of id_instansi
            cur.execute("SELECT MAX(CAST(SUBSTRING(id_instansi FROM 5) AS INTEGER)) FROM instansi")
            latest_numeric_part = cur.fetchone()[0]

            # Increment the numeric part
            new_numeric_part = 1 if latest_numeric_part is None else latest_numeric_part + 1

            # Create the new id_instansi
            id_instansi = f'INST{new_numeric_part}'

            cur.execute(
                "INSERT INTO instansi (id_instansi, nama_instansi, email, password, nomor_telp, alamat, cover, nomor_izin_pemerintah, kode_instansi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (id_instansi, nama_instansi, email, password, no_telp, alamat, file, nomor_izin_pemerintah, kode_instansi)
            )
            conn.commit()
            return id_instansi
        except IntegrityError:
            conn.rollback()
            return None  # Indicates a duplicate key violation
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
            return None