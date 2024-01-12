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

def validate_create_instansi_errors(nama_instansi, email, password, no_telp, alamat, nomor_izin_pemerintah, file):
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

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))