from flask import request
from utils.server_tool import MallBlueprint
import logging

logger = logging.getLogger('user')
app = MallBlueprint('user', __name__)


@app.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    logger.debug(f'{params}')
    return {}

