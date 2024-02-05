import json

def validate_todo_input(todo, is_done):
    errors = []

    if not todo:
        errors.append("todo is required")

    if not is_done:
        errors.append("is_done is required")
    elif is_done not in ["0", "1"]:
        errors.append("is_done must be 0 or 1")

    return errors

class ValidateError(Exception):
    def __init__(self, errors):
        super().__init__(errors)

def validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, berkas_pemerintah, ktp):
    errors = []

    if not nama_instansi:
        errors.append("nama_instansi is required")

    if not email:
        errors.append("email is required")

    if not password:
        errors.append("password is required")

    if not no_telp:
        errors.append("no_telp is required")

    if not alamat:
        errors.append("alamat is required")

    if not nomor_izin_pemerintah:
        errors.append("nomor_izin_pemerintah is required")

    if not berkas_pemerintah:
        errors.append("berkas_pemerintah is required")

    if not ktp:
        errors.append("ktp is required")

    if berkas_pemerintah.content_type not in ["application/pdf"]:
        errors.append("berkas_pemerintah must be pdf")

    if ktp is not None:
        if ktp.content_type not in ["image/img", "image/png", "image/jpg", "image/jpeg"]:
            errors.append("ktp must be img, png, jpg, or jpeg")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))

def validate_create_peserta_error(nama, email, no_telp, id_instansi, nik, id_acara):
    errors = []

    if not nama:
        errors.append("nama is required")

    if not email:
        errors.append("email is required")

    if not no_telp:
        errors.append("no_telp is required")

    if not id_instansi:
        errors.append("id_instansi is required")

    if not nik:
        errors.append("nik is required")

    if not id_acara:
        errors.append("id_acara is required")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))
    
def validate_create_acara_error(acara, keterangan):
    errors = []

    if not acara:
        errors.append("acara is required")

    if not keterangan:
        errors.append("keterangan is required")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))