import json
import os
import time
from flask import request
from models import instansi as instansi_model, berkas_instansi as berkas_instansi_model
from flask_jwt_extended import get_jwt_identity
from validator import ValidateError, validate_create_instansi_errors
from lib import generate_filename as gfn, db

def get_all_instansi():
    current_user = get_jwt_identity()
    role = current_user["role"]
    q = request.args.get('q', None)
    if role == "admin":
        _instansi = instansi_model.fetchall(q=q)
        return _instansi, 200
    else:
        _instansi = instansi_model.fetch_by_email(current_user['email'])
        if(_instansi is None):
            return [{"msg": "Instansi tidak ditemukan"}], 404
        return _instansi, 200

def get_instansi_me():
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_user = current_user["id_user"]
    if(role == "admin"):
        return {"msg": "Anda tidak memiliki akses"}, 403
    instansi_ = instansi_model.fetch(id_user)
    if instansi_ is None:
        return {"msg": "Instansi tidak ditemukan"}, 404
    return instansi_, 200

def get_instansi(id):
    current_user = get_jwt_identity()
    role = current_user["role"]
    if(role == "admin"):
        instansi_ = instansi_model.fetch(id)
        if instansi_ is None:
            return {"msg": "Instansi tidak ditemukan"}, 404
        return instansi_, 200
    else:
        return {"msg": "Anda tidak memiliki akses"}, 403

def create_instansi():
    exist = instansi_model.fetch_by_email(request.form.get('email', None))
    if exist is not None:
        return {"msg": "Email sudah terdaftar"}, 400
    dl = 'static/neucertify/docs/' # Download location
    try:
        #  nama_instansi:
        # type: string
        # email:
        # type: string
        # password:
        # type: string
        # no_telp:
        # type: string
        # alamat:
        # type: string
        # nip:
        # type: string
        # berkas_pemerintah:
        # type: string
        # format: binary
        # ktp:
        # type: string
        # format: binary

        nama_instansi = request.form.get('nama_instansi', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        no_telp = request.form.get('no_telp', None)
        alamat = request.form.get('alamat', None)
        nomor_izin_pemerintah = request.form.get('nip', None)
        berkas_pemerintah = request.files.get('berkas_pemerintah', None)
        ktp = request.files.get('ktp', None)

        validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, berkas_pemerintah, ktp)

        # Generate File Name
        bp = gfn.generate(berkas_pemerintah.filename, "bp")
        ktp_ = gfn.generate(ktp.filename, "ktp")
        
        # Generate path location
        berkas_pemerintah_location = dl + bp + ".pdf"
        ktp_location = dl + ktp_ + ".jpg"

        id = instansi_model.create(
            nama_instansi = nama_instansi,
            email = email,
            password = password,
            no_telp = no_telp,
            alamat = alamat,
            nomor_izin_pemerintah = nomor_izin_pemerintah,
        )

        berkas_instansi_model.upload(
            berkas=berkas_pemerintah_location, 
            id_instansi=id, 
            ktp=ktp_location
        )

        berkas_pemerintah.save(berkas_pemerintah_location)
        ktp.save(ktp_location)

        return "", 201

    except ValidateError as e:
        return json.loads(str(e)), 422

def update_instansi():
    current_user = get_jwt_identity()
    id_user = current_user["id_user"]
    role = current_user["role"]
    # The current cannot editing another user
    if role == "user" and id_user != id:
        return {"msg": "Anda tidak memilki akses"}, 403

    try:
        nama_instansi = request.form.get('nama_instansi', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        no_telp = request.form.get('no_telp', None)
        alamat = request.form.get('alamat', None)
        nomor_izin_pemerintah = request.form.get('nip', None)
        file = request.files.get('cover', None)
        verified = request.form.get('verified', None)

        if role == "user":
            return {"msg": "Unauthorized"}, 403

        if verified not in ["true", "false"]:
            return {"msg": "Verified harus berupa true atau false"}, 422
        
        # validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, file)

        if file is not None:
            if file.content_type not in ["image/jpeg", "image/png"]:
                return {"msg": "Format file tidak didukung"}, 422

        old_cover = instansi_model.get_cover(id)

        if old_cover is not None:
            if os.path.exists(old_cover['cover']):
                old_cover = old_cover['cover']
                os.remove(old_cover)
        # Generate proper file name
        location = None

        if file is not None:
            filename = str(time.time()) + "_" +file.filename
            location = 'static/uploads/' + filename
            file.save(location)

        instansi_model.update(
            id = id,
            nama_instansi = nama_instansi,
            email = email,
            password = password,
            no_telp = no_telp,
            alamat = alamat,
            nomor_izin_pemerintah = nomor_izin_pemerintah,
            file = location,
            verified = verified
        )
        return "", 200

    except ValidateError as e:
        return json.loads(str(e)), 422    
    
def delete_instansi(id):
    current_user = get_jwt_identity()
    id_user = current_user["id_user"]
    role = current_user["role"]
    # The current cannot editing another user
    if role == "user" and id_user != id:
        return {"msg": "Anda tidak memilki akses"}, 403

    if(db.get_role(email=current_user["email"]) is None):
        return {"msg": "Anda tidak memiliki akses"}, 403

    berkas_instansi_model.delete(id)
    instansi_model.delete(id)