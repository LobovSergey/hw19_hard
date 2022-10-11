import jwt
from flask import request, abort

from constant import ALGO, SECRET


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(404)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, SECRET, algorithms=ALGO)

        except Exception:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(404)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        role = None

        try:
            data = jwt.decode(token, SECRET, algorithms=ALGO)
            role = data.get('role')

        except Exception:
            abort(401)

        if role != 'admin':
            abort(401)

        return func(*args, **kwargs)

    return wrapper
