import hashlib

from dao.model.user import User


class UserDAO:

    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_name(self, name):
        return self.session.query(User).filter(User.username == name).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        new = User(**data)
        self.session.add(new)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()



    def update(self, data, uid):
        user = self.get_one(uid)
        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.session.add(user)
        self.session.commit()

    def get_hash(self):
        return hashlib.md5(self.dao.encode('utf-8')).hexdigest()
