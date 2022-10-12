import base64
import hashlib
import hmac

from constant import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.users_dao import UserDAO


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        password = data.get('password')
        data["password"] = self.get_hash_hard(password)
        print(data["password"])
        return self.dao.create(data)

    def update(self, data, uid):
        return self.dao.update(data, uid)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_by_username(self, name):
        return self.dao.get_by_name(name)

    def get_hash_hard(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def get_hash_easy(self, password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def compare_paswords(self, hash_pass, password):
        return hmac.compare_digest(
            base64.b64decode(hash_pass),
            hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS))
