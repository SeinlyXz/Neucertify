from flask import Flask, request, jsonify
from flask_cors import CORS
import instansi
import json
import random
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
)
import lib.db as db
from datetime import timedelta
import dotenv
import os
from validator import validate_create_instansi_errors, ValidateError
dotenv.load_dotenv()


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)
CORS(app)


@app.route('/auth/v1/login', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if db.login(email=email, password=password) is None:
        return {"msg": "Email atau password salah"}, 401
    access_token = create_access_token(
        identity=email,
        expires_delta=app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )
    return {"access_token": access_token}, 200


@app.get('/api/v1/instansi')
@jwt_required()
def get_all_instansi():
    q = request.args.get('q')
    if q is None:
        data = instansi.fetchall()
    data = instansi.fetchall(q=q)
    return data, 200

@app.get('/api/v1/instansi/<id>')
@jwt_required()
def get_instansi(id):
    instansi_ = instansi.fetch(id)
    if instansi_ is None:
        return {"msg": "Instansi tidak ditemukan"}, 404
    return instansi_, 200

@app.post('/api/v1/instansi')
@jwt_required()
def create_instansi():
    try:
        nama_instansi = request.form.get('nama_instansi', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        no_telp = request.form.get('no_telp', None)
        alamat = request.form.get('alamat', None)
        nomor_izin_pemerintah = request.form.get('nip', None)
        file = request.files.get('cover', None)

        validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, file)

        # Generate random string for file name
        random_string = "".join([chr(random.randint(97, 122)) for _ in range(10)])
        filename = random_string + file.filename

        location = 'static/uploads/' + filename
        instansi.create(
            nama_instansi = nama_instansi,
            email = email,
            password = password,
            no_telp = no_telp,
            alamat = alamat,
            nomor_izin_pemerintah = nomor_izin_pemerintah,
            file = location
        )

        file.save(location)

        return "", 201

    except ValidateError as e:
        return json.loads(str(e)), 422

if __name__ == '__main__':
    app.run(debug=True)
