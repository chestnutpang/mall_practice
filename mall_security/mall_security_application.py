import sanic
from sanic import response
from config import ServerConfig
from utils.mysql_tool import DBConn, init_model
from utils.redis_tool import RedisConn
from utils.cookie_service import session_init
app = sanic.Sanic(__name__)


def register_buleprint(app):
    import controller
    app.blueprint(controller.auth.bp)

    @app.route('/')
    async def index(request):
        return response.text('good')


@app.listener('before_server_start')
async def init_ext(app, loop):
    DBConn.db_init(app)
    await RedisConn.redis_init(app, loop)
    init_model()
    session_init(app)
    register_buleprint(app)


if __name__ == '__main__':
    app.server_config = ServerConfig
    app.run(debug=True)
