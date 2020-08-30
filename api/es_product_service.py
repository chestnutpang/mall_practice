from flask import request
from utils.server_tool import MallBlueprint
import logging
from comm import es_product_service


logger = logging.getLogger('es_product_service')
app = MallBlueprint('es_product_service', __name__)


@app.route('/importAll', methods=['GET'])
def import_all():
    """导入所有数据库的商品到 es 中"""
    count = es_product_service.import_all_impl()
    return {
        'success': count
    }


@app.route('/delete/<_id>', methods=['POST'])
def delete(_id):
    es_product_service.delete_product(_id)
    return {}


@app.route('/delete/batch', methods=['POST'])
def delete_batch():
    params = request.get_json()
    ids = params.get('ids')
    pass
    return {}


@app.route('/create/<_id>', methods=['POST'])
def create():
    return {}


@app.route('/search/simple', methods=['GET'])
def search_simple():
    return {}


@app.route('/search', methods=['GET'])
def search():
    params = request.args
    sort = params.get('sort', 0)
    value = params.get('value', '0')
    keyword = params.get('keyword')
    brand_id = params.get('brandId')
    product_category_id = params.get('productCategoryId')
    page_num = params.get('pageNum', 0)
    page_size = params.get('pageSize', 5)

    return {}


@app.route('/recommend/{id}', methods=['GET'])
def recommend():
    return {}


@app.route('/search/relate', methods=['GET'])
def search_relate():
    return {}
