from flask import request
from utils.server_tool import MallBlueprint
from utils.es_tool import es
import logging
import comm


logger = logging.getLogger('es_product_service')
app = MallBlueprint('es_product_service', __name__)


@app.route('/importAll')
def import_all():
    """导入所有数据库的商品到 es 中"""
    count = comm.import_all_impl()
    return {
        'success': count
    }



