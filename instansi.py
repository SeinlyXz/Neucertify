from psycopg2 import IntegrityError
from lib.db import conn
from psycopg2.errors import DatabaseError
import os

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

def get_cover(id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT cover FROM instansi WHERE id_instansi = %(id)s", {
                "id": id
            })
            cover = cur.fetchone()[0]

            if cover is None:
                return None

            # Convert tuple to dictionary
            cover_ = {
                "cover": cover
            }
        except DatabaseError:
            conn.rollback()
            return None
    return cover_

def update(id, nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, file):
    try:
        with conn.cursor() as cur:
            # Fetch existing data once
            cur.execute("SELECT id_instansi, nama_instansi, email, password, nomor_telp, alamat, cover, nomor_izin_pemerintah FROM instansi WHERE id_instansi = %(id)s", {"id": id})
            instansi_data = cur.fetchone()

            if not instansi_data:
                return None
            # Set default values if parameters are None
            nama_instansi = nama_instansi or instansi_data[1]
            email = email or instansi_data[2]
            password = password or instansi_data[3]
            no_telp = no_telp or instansi_data[4]
            alamat = alamat or instansi_data[5]
            file = file or instansi_data[6]
            nomor_izin_pemerintah = nomor_izin_pemerintah or instansi_data[7]

            cur.execute(
                "UPDATE instansi SET nama_instansi = %s, email = %s, password = %s, nomor_telp = %s, alamat = %s, cover = %s, nomor_izin_pemerintah = %s WHERE id_instansi = %s",
                (nama_instansi, email, password, no_telp, alamat, file, nomor_izin_pemerintah, id)
            )
            conn.commit()
            return True

    except IntegrityError:
        conn.rollback()
        return None  # Indicates a duplicate key violation

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
        return None
        
def delete(id):
    with conn.cursor() as cur:
        try:
            # Get cover path
            cur.execute("SELECT cover FROM instansi WHERE id_instansi = %(id)s", {"id": id})
            cover_path = cur.fetchone()[0]
            # Delete the cover file
            if os.path.exists(cover_path):
                os.remove(cover_path)

            cur.execute(
                "DELETE FROM instansi WHERE id_instansi = %s",
                (id,)
            )
            conn.commit()
            return True
        except IntegrityError:
            conn.rollback()
            return None  # Indicates a duplicate key violation
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
            return None
        
def fetch_by_email(email):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id_instansi, nama_instansi, alamat, cover, email FROM instansi WHERE email = %(email)s", {
                "email": email
            })
            instansi = cur.fetchone()

            if instansi is None:
                return None

            # Convert tuple to dictionary
            instansi_ = {
                "id": instansi[0],
                "nama_instansi": instansi[1],
                "alamat_instansi": instansi[2],
                "cover": instansi[3],
                "email": instansi[4]
            }
        except DatabaseError:
            conn.rollback()
            return None
    return instansi_