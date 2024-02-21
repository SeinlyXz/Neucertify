
from flask import request
from flask_jwt_extended import get_jwt_identity
from models import sertifikat as sertifikat_model, peserta as peserta_model

def get_all_sertifikat():
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_instansi = current_user["id_user"]
    if role == "admin":
        _sertifikat = sertifikat_model.get_all_sertifikat(id_instansi=id_instansi)
        if _sertifikat is None:
            return [{"msg": "Sertifikat tidak ditemukan"}], 404
        return _sertifikat, 200
    else:
        _sertifikat = sertifikat_model.get_sertifikat_by_instansi(id=id_instansi, email=current_user['email'])
        if _sertifikat is None:
            return [{"msg": "Sertifikat tidak ditemukan"}], 404
        return _sertifikat, 200

def get_all_generated_sertifikat():
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_instansi = current_user["id_user"]
    if role == "admin":
        _sertifikat = sertifikat_model.get_all_generated_sertifikat()
        if _sertifikat is None:
            return [{"msg": "Sertifikat tidak ditemukan"}], 404
        return _sertifikat, 200
    else:
        _sertifikat = sertifikat_model.get_sertifikat_by_instansi(id=id_instansi, email=current_user['email'])
        if _sertifikat is None:
            return [{"msg": "Sertifikat tidak ditemukan"}], 404
        return _sertifikat, 200
    
def get_sertifikat(id):
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        _sertifikat = sertifikat_model.get_sertifikat(id)
        return _sertifikat, 200
    else:
        _sertifikat = sertifikat_model.get_detail_sertifikat(id_sertifikat=id, id_instansi=current_user['id_user'])
        if(_sertifikat is None):
            return {"msg": "Sertifikat belum memiliki peserta"}, 404
        return _sertifikat, 200
    
def create_sertifikat():
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_instansi = current_user["id_user"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat sertifikat"}, 403
    
    id_acara = request.form.get('id_acara', None)
    exist = sertifikat_model.create_sertifikat(id_instansi=id_instansi, id_acara=id_acara)
    if not exist:
        return {"msg": "Sertifikat sudah dibuat atau acara tidak ditemukan"}, 400
    return "", 201

def generate_sertifikat():
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_instansi = current_user["id_user"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat sertifikat"}, 403
    
    id_acara = request.form.get('id_acara', None)
    waktu = request.form.get('waktu', None)
    id_sertifikat = request.form.get('id_sertifikat', None)
    ok = sertifikat_model.generate_sertifikat(id_instansi=id_instansi, id_acara=id_acara, waktu=waktu, id_serfitikat=id_sertifikat)
    if not ok:
        return {"msg": "Peserta tidak ditemukan"}, 400
    return "", 201

def delete_sertifikat(id):
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat menghapus sertifikat"}, 403
    ok = sertifikat_model.delete_sertifikat(id_sertifikat=id)
    if not ok:
        return {"msg": "Sertifikat tidak ditemukan"}, 404
    return "", 204