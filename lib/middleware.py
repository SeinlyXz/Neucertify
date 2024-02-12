from functools import wraps
import json
from flask_jwt_extended import get_jwt_identity

from validator import ValidateError


def instansi_only(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            role = current_user.get("role")

            if role != "user":
                return {"msg": message}, 403

            return func(*args, **kwargs)
        return wrapper
    return decorator

# def admin_only(message):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             current_user = get_jwt_identity()
#             role = current_user.get("role")

#             if role != "admin":
#                 return {"msg": message}, 403

#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

def handle_validate():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidateError as e:
                return json.loads(str(e)), 422
        return wrapper
    return decorator