import calendar
import datetime

import jwt
from flask_restx import abort

from constant import SECRET, ALGO
from service.user_service import UserService


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    def get_by_name(self, name):
        return self.service.get_by_username(name)

    def generate_token(self, username, password, is_refresh=False):
        if None in [username, password]:
            abort(400)

        user = self.service.get_by_username(username)
        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.service.compare_paswords(user.password, password):
                raise abort(400)

        data = {'username': user.username,
                'role': user.role}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)
        d30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(d30.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {'access_token': access_token,
                'refresh_token': refresh_token}

    def approve_refresh_tokens(self, token):
        data = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGO])
        username = data.get('username')
        return self.generate_token(username, None, is_refresh=True)

