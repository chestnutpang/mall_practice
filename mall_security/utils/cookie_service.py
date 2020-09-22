from sanic_session import Session, AIORedisSessionInterface

session = Session()


def session_init(app):
    session.init_app(app, interface=AIORedisSessionInterface(
        app.redis,
        cookie_name='msc',
        secure=False
    ))


class CookieSession:

    @classmethod
    def set_session(cls, user_id, request):
        request.ctx.session['user'] = user_id

    @classmethod
    def get_session(cls, request):
        return request.ctx.session.get('user')

    @classmethod
    def clear_session(cls, request):
        request.ctx.session.clear()
