from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

users_ns = Namespace('users')


@users_ns.route('/')
class UserView(Resource):
    def get(self):
        all_users = user_service.get_all()
        return UserSchema(many=True).dump(all_users)

    def post(self):
        data = request.json
        user_service.create(data)
        return 'Created', 201


@users_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return UserSchema().dump(user)

    def put(self, uid):
        try:
            data = request.json
            user_service.update(data, uid)
            return 'Edited', 204

        except Exception as e:
            return f'Error {e}', 404

    def delete(self, uid):
        user_service.delete(uid)
        return 'Deleted', 204
