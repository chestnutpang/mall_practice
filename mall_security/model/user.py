import secrets
import string
from functools import wraps
from utils.mysql_dbbase import BaseModel
import peewee
from utils.cookie_service import CookieSession


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    nickname = peewee.CharField()

    @classmethod
    async def register(cls, request, kwargs):
        res = cls.create(**kwargs)
        CookieSession.set_session(res.id, request)
        return res

    @classmethod
    async def login(cls, request, username, password):
        res = cls.select().where((cls.username == username) & (cls.password == password)).dicts().first()
        print(res)
        if res is not None:
            CookieSession.set_session(res.get('id'), request)
        return res
    
    @classmethod
    async def logout(cls, request):
        CookieSession.clear_session(request)

    @classmethod
    async def get_user_info(cls, request):
        user_id = CookieSession.get_session(request)
        res = {}
        if user_id is None:
            return res
        user = cls.get(user_id)
        res['username'] = user.username
        res['id'] = user.id
        res['nickname'] = user.nickname
        return res


SECRET_CHARS = string.ascii_lowercase + string.digits


def salt_generate(size=48, chars=SECRET_CHARS):
    return ''.join(secrets.choice(chars) for _ in range(size))


def nickname_generate():
    return f'用户{salt_generate(7)}'

