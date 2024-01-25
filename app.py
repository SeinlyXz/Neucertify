import time
from flask import Flask, request
from flask_cors import CORS
import model.instansi as instansi
import model.berkas_instansi as berkas_instansi
import model.peserta as peserta
import lib.generate_filename as gfn
import json
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity
)
import lib.db as db
from datetime import timedelta
import dotenv
import os
from validator import validate_create_instansi_errors, validate_create_peserta_error, ValidateError
dotenv.load_dotenv()
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/neucertify.json'  # Our API url (can of course be a local resource)
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)
CORS(app)
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
)
app.register_blueprint(swaggerui_blueprint)


@app.post('/auth/v1/login')
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    
    if db.login(email=email, password=password) is None:
        return {"msg": "Email atau password salah"}, 401
    role = db.get_role(email=email)
    access_token = create_access_token(
        identity = {
            "email": email,
            "role": role
        },
        expires_delta = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )
    return {"access_token": access_token}, 200

# ----------------- Instansi -----------------

@app.get('/api/v1/instansi')
@jwt_required()
def get_all_instansi():
    current_user = get_jwt_identity()
    role = current_user["role"]
    print(role)
    q = request.args.get('q')
    if q is None:
        if role == "admin":
            data = instansi.fetchall()
        else:
            data = instansi.fetch_by_email(current_user["email"])

    if role == "admin":
        data = instansi.fetchall(q=q)
    else:
        data = instansi.fetch_by_email(current_user["email"])
    return data, 200

@app.get('/api/v1/instansi/<id>')
@jwt_required()
def get_instansi(id):
    instansi_ = instansi.fetch(id)
    if instansi_ is None:
        return {"msg": "Instansi tidak ditemukan"}, 404
    return instansi_, 200

@app.post('/api/v1/instansi')
def create_instansi():
    dl = 'static/neucertify/docs/'
    try:
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
        bp = gfn(berkas_pemerintah.filename)
        ktp_ = gfn(ktp.filename)

        # Generate path location
        berkas_pemerintah_location = dl + bp
        ktp_location = dl + ktp_

        id = instansi.create(
            nama_instansi = nama_instansi,
            email = email,
            password = password,
            no_telp = no_telp,
            alamat = alamat,
            nomor_izin_pemerintah = nomor_izin_pemerintah,
        )

        berkas_instansi.upload(
            berkas=berkas_pemerintah, 
            id_instansi=id, 
            ktp=ktp
        )

        bp.save(berkas_pemerintah_location)
        ktp_.save(ktp_location)

        return "", 201

    except ValidateError as e:
        return json.loads(str(e)), 422

@app.put('/api/v1/instansi/<id>')
@jwt_required()
def update_instansi(id):
    current_user = get_jwt_identity()
    _current_user = current_user["email"]

    # The current cannot editing another user
    if instansi.check_current_user(email=_current_user) is None or current_user["role"] != "admin":
        return {"msg": "Anda tidak memiliki akses"}, 403

    try:
        nama_instansi = request.form.get('nama_instansi', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        no_telp = request.form.get('no_telp', None)
        alamat = request.form.get('alamat', None)
        nomor_izin_pemerintah = request.form.get('nip', None)
        file = request.files.get('cover', None)

        # validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, file)

        if file is not None and file.content_type not in ["image/jpeg", "image/png"]:
            return {"msg": "Format file tidak didukung"}, 422

        old_cover = instansi.get_cover(id)
        if old_cover['cover'] is not None:
            if os.path.exists(old_cover['cover']):
                old_cover = old_cover['cover']
                os.remove(old_cover)
        # Generate proper file name
        location = None

        if file is not None:
            filename = str(time.time()) + "_" +file.filename
            location = 'static/uploads/' + filename
            file.save(location)

        instansi.update(
            id = id,
            nama_instansi = nama_instansi,
            email = email,
            password = password,
            no_telp = no_telp,
            alamat = alamat,
            nomor_izin_pemerintah = nomor_izin_pemerintah,
            file = location
        )
        return "", 200

    except ValidateError as e:
        return json.loads(str(e)), 422    

@app.delete('/api/v1/instansi/<id>')
@jwt_required()
def delete_instansi(id):
    current_user = get_jwt_identity()
    _current_user = current_user["email"]

    # The current cannot editing another user
    if instansi.check_current_user(email=_current_user) is None or current_user["role"] != "admin":
        return {"msg": "Unauthorized"}, 403
    
    try:
        instansi.delete(id)
    except Exception as e:
        print(e)
        return {"msg": "Terjadi kesalahan"}, 500
    return "", 200


# ----------------- Peserta -----------------
@app.get('/api/v1/peserta')
@jwt_required()
def get_all_peserta():
    current_user = get_jwt_identity()
    role = current_user["role"]
    if role == "admin":
        _peserta = peserta.get_all_peserta()
        return _peserta, 200
    else:
        _peserta = peserta.get_all_peserta_by_instansi(current_user['email'])
        if(_peserta is None):
            return {"msg": "Peserta tidak ditemukan"}, 404
        return _peserta, 200

@app.get('/api/v1/peserta/<id>')
@jwt_required()
def get_peserta(id):
    pass

@app.post('/api/v1/peserta')
@jwt_required()
def create_peserta():
    current_user = get_jwt_identity()
    _email_instansi = current_user["email"]
    role = current_user["role"]
    if role == "admin":
        return {"msg": "Hanya instansi yang dapat membuat peserta"}, 403
    try:
        nama = request.form.get('nama', None)
        email = request.form.get('email', None)
        no_telp = request.form.get('no_telp', None)
        nik = request.form.get('nik', None)
        id_acara = request.form.get('id_acara', None)
        validate_create_peserta_error(nama, email, no_telp, _email_instansi, nik, id_acara)
        peserta.create_peserta(
            nama=nama,
            email=email,
            no_telp=no_telp,
            id_instansi=_email_instansi,
            nik=nik,
            id_acara=id_acara
        )
        return "", 201
    except Exception as e:
        print(e)
        return {"msg": "Terjadi kesalahan"}, 500

@app.put('/api/v1/peserta/<id>')
@jwt_required()
def update_peserta(id):
    pass

@app.delete('/api/v1/peserta/<id>')
def delete_peserta(id):
    pass


# ----------------- Sertifikat -----------------
@app.get('/api/v1/sertifikat')
@jwt_required()
def get_all_sertifikat():
    pass

@app.get('/api/v1/sertifikat/<id>')
@jwt_required()
def get_sertifikat(id):
    pass

@app.post('/api/v1/sertifikat')
@jwt_required()
def create_sertifikat():
    pass

@app.put('/api/v1/sertifikat/<id>')
@jwt_required()
def update_sertifikat(id):
    pass

@app.delete('/api/v1/sertifikat/<id>')
@jwt_required
def delete_sertifikat(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)