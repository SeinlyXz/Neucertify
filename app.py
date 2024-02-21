from flask import Flask, request
from flask_cors import CORS
import controller.peserta as peserta_controller
import controller.acara as acara_controller
import controller.instansi as instansi_controller
import controller.sertifikat as sertifikat_controller
from lib.middleware import instansi_only, handle_validate
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
)
import lib.db as db
from datetime import timedelta
import dotenv
import os
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
    id_user = db.get_id_user(email=email)
    
    access_token = create_access_token(
        identity = {
            "email": email, # nanti dihapus
            "role": role,
            "id_user": id_user
        },
        expires_delta = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )
    return {"access_token": access_token}, 200

# ----------------- Instansi (Oke) -----------------

@app.get('/api/v1/instansi')
@jwt_required()
def get_all_instansi():
    return instansi_controller.get_all_instansi()

@app.get('/api/v1/instansi/me')
@jwt_required()
def get_instansi_me():
    return instansi_controller.get_instansi_me()

@app.get('/api/v1/instansi/<id>')
@jwt_required()
def get_instansi(id):
    return instansi_controller.get_instansi(id)

@app.post('/api/v1/instansi')
def create_instansi():
    return instansi_controller.create_instansi()

@app.put('/api/v1/instansi/<id>')
@jwt_required()
def update_instansi(id):
    return instansi_controller.update_instansi(id)

@app.delete('/api/v1/instansi/<id>')
@jwt_required()
def delete_instansi(id):
    return instansi_controller.delete_instansi(id)

# ----------------- Peserta -----------------
@app.get('/api/v1/peserta')
@jwt_required()
def get_all_peserta():
    return peserta_controller.get_all_peserta()

@app.get('/api/v1/peserta/<id>')
@jwt_required()
def get_peserta(id):
    return peserta_controller.get_peserta(id)

@app.post('/api/v1/peserta')
@jwt_required()
@handle_validate()
def create_peserta():
    return peserta_controller.create_peserta()

@app.put('/api/v1/peserta/<id>')
@jwt_required()
def update_peserta(id):
    return peserta_controller.update_peserta(id)

@app.delete('/api/v1/peserta/<id>')
def delete_peserta(id):
    return peserta_controller.delete_peserta(id)

# ----------------- Acara (Oke) -----------------
@app.get('/api/v1/acara')
@jwt_required()
def get_all_acara():
    return acara_controller.get_all_acara()

@app.get('/api/v1/acara/<id>')
@jwt_required()
def get_acara(id):
    return acara_controller.get_acara(id)

@app.post('/api/v1/acara')
@jwt_required()
@instansi_only("Hanya instansi yang dapat membuat acara")
@handle_validate()
def create_new_acara():
    return acara_controller.create_new_acara()

@app.put('/api/v1/acara/<id>')
@jwt_required()
@instansi_only("Hanya instansi yang dapat mengupdate acara")
@handle_validate()
def update_acara(id):
    return acara_controller.update_acara(id)

@app.delete('/api/v1/acara/<id>')
@jwt_required()
def delete_acara(id):
    return acara_controller.delete_acara(id)

# ----------------- Sertifikat -----------------
@app.get('/api/v1/sertifikat/generated')
@jwt_required()
def get_all_sertifikat():
    return sertifikat_controller.get_all_generated_sertifikat()

@app.get('/api/v1/sertifikat')
@jwt_required()
def get_all_sertifikat_by_instansi():
    return sertifikat_controller.get_all_sertifikat()

@app.get('/api/v1/sertifikat/<id>')
@jwt_required()
def get_sertifikat(id):
    return sertifikat_controller.get_sertifikat(id)

@app.post('/api/v1/sertifikat')
@jwt_required()
def create_sertifikat():
    return sertifikat_controller.create_sertifikat()

@app.post('/api/v1/sertifikat/generate')
@jwt_required()
def generate_sertifikat():
    return sertifikat_controller.generate_sertifikat()

@app.put('/api/v1/sertifikat/<id>')
@jwt_required()
def update_sertifikat(id):
    pass

@app.delete('/api/v1/sertifikat/<id>')
@jwt_required()
def delete_sertifikat(id):
    return sertifikat_controller.delete_sertifikat(id=id)

if __name__ == '__main__':
    app.run(debug=True)