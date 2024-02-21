from flask import request
from models import peserta as peserta_model
from flask_jwt_extended import get_jwt_identity
from validator import validate_create_peserta_error

def get_all_peserta():
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        _peserta = peserta_model.get_all_peserta()
        return _peserta, 200
    else:
        q = request.args.get('q', None)
        _peserta = peserta_model.get_all_peserta_by_instansi(current_user['email'], q=q)
        if _peserta is None:
            return [{"msg": "Peserta tidak ditemukan"}], 404
        return _peserta, 200
    # return peserta_model.get_all_peserta()

def get_peserta(id):
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        _peserta = peserta_model.get_peserta_by_id(id)
        if(_peserta is None):
            return {"msg": "Peserta tidak ditemukan"}, 404
        return _peserta, 200
    
    _peserta = peserta_model.get_peserta_by_id(id=id, id_instansi=current_user["id_user"])
    if(_peserta is None):
        return {"msg": "Peserta tidak ditemukan"}, 404
    return _peserta, 200

def create_peserta():
    current_user = get_jwt_identity()
    _email_instansi = current_user["email"]
    id_instansi = current_user["id_user"]
    role = current_user["role"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat peserta"}, 403
    
    nama = request.form.get('nama', None)
    email = request.form.get('email', None)
    no_telp = request.form.get('no_telp', None)
    nik = request.form.get('nik', None)
    id_acara = request.form.get('id_acara', None)
    validate_create_peserta_error(nama, email, no_telp, _email_instansi, nik, id_acara)
    peserta_model.create_peserta(
        nama=nama,
        email=email,
        no_telp=no_telp,
        id_instansi=id_instansi,
        nik=nik,
        id_acara=id_acara
    )
    return "", 201

def update_peserta(id:str):
    current_user = get_jwt_identity()
    _email_instansi = current_user["email"]
    role = current_user["role"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat peserta"}, 403
    nama = request.form.get('nama', None)
    email = request.form.get('email', None)
    no_telp = request.form.get('no_telp', None)
    nik = request.form.get('nik', None)
    id_acara = request.form.get('id_acara', None)
    validate_create_peserta_error(nama, email, no_telp, _email_instansi, nik, id_acara)
    peserta_model.update_peserta(
        id=id,
        nama=nama,
        email=email,
        no_telp=no_telp,
        nik=nik,
        id_acara=id_acara
    )
    return "", 200

def delete_peserta(id:str):
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat peserta"}, 403
    peserta_model.delete_peserta(id)
    return "", 200