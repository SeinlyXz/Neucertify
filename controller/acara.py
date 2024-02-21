from flask import request
from models import acara as acara_model
from flask_jwt_extended import get_jwt_identity
from validator import validate_create_acara_error

def get_all_acara():
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        _acara = acara_model.get_all_acara()
        return _acara, 200
    elif role == "user":
        _acara = acara_model.get_all_acara_by_instansi(current_user['email'])
        if _acara is None:
            return [{"msg": "Acara tidak ditemukan atau anda belum membuat acara"}], 404
        return _acara, 200
    else:
        return {"msg": "Anda tidak memiliki akses"}, 403

def get_acara(id):
    current_user = get_jwt_identity()
    id_user = current_user["id_user"]
    print(id_user, id)
    _acara = acara_model.get_acara_by_id(id, id_user=id_user)

    if _acara is None:
        return {"msg": "Acara tidak ditemukan"}, 404
    return _acara, 200

def create_new_acara():
    nama_acara = request.form.get('acara', None)
    keterangan = request.form.get('keterangan', None)

    current_user = get_jwt_identity()
    id_user = current_user["id_user"]

    if acara_model.check_is_verified(id_user) is None:
        return {"msg": "Anda belum terverifikasi"}, 403
    
    validate_create_acara_error(nama_acara, keterangan)

    id_acara = acara_model.create_acara(acara=nama_acara, keterangan=keterangan, id_instansi=id_user)
    acara_model.create_detail_acara(id_acara)
    return "", 201

def update_acara(id:str):
    current_user = get_jwt_identity()
    id_user = current_user["id_user"]

    nama_acara = request.form.get('acara', None)
    keterangan = request.form.get('keterangan', None)
    link = request.form.get('link', None)
    status = request.form.get('status', None)

    if status not in ["true", "false"]:
        return {"msg": "Status harus berupa true atau false"}, 422

    update_status = acara_model.update_acara(id_acara=id, acara=nama_acara, keterangan=keterangan, id_instansi=id_user)

    if update_status is None:
        return {"msg": "Acara tidak ditemukan"}, 404
    
    acara_model.update_detail_acara(id_acara=id, link=link, status=status)

    return "", 200

def delete_acara(id:str):
    current_user = get_jwt_identity()
    role = current_user["role"]
    id_user = current_user["id_user"]

    if role == "admin":
        return {"msg": "Hanya instansi yang dapat menghapus acara"}, 403
    
    if acara_model.delete_acara(id_acara=id, id_instansi=id_user) is False:
        return {"msg": "Acara tidak ditemukan"}, 404
    
    return "", 200