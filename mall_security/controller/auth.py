from sanic import Blueprint
from service import auth_service
from model.user import User
from sanic.response import json

bp = Blueprint('auth', url_prefix='/auth')


bp.route('/register/phone', methods=['POST'])(auth_service.register)

bp.route('/login/phone', methods=['POST'])(auth_service.login)

bp.route('/logout', methods=['POST'])(auth_service.logout)

bp.route('/user_info')(auth_service.user_info)


@bp.route('/test')
async def test(request):
    from utils.mysql_tool import DBConn
    # print(User.Meta.database)
    res = User.login(username='dffff', password='adas')
    return json({})

