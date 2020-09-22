from flask import request
from utils.server_tool import MallBlueprint
import logging
from service import es_product_service


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
    """根据id删除商品"""
    res = es_product_service.delete_product(_id)
    return {
        'count': res
    }


@app.route('/get/<_id>', methods=['GET'])
def get(_id):
    return es_product_service.get_product(_id)


@app.route('/delete/batch', methods=['POST'])
def delete_batch():
    """根据id批量删除商品"""
    count = es_product_service.delete_product_batch()
    return {
        'count': count
    }


@app.route('/create/<_id>', methods=['POST'])
def create(_id):
    """根据id创建商品"""
    if not isinstance(_id, int):
        raise ValueError
    res = es_product_service.get_product_bulk(_id)
    return {
        'count': res
    }


@app.route('/search/simple', methods=['GET'])
def search_simple():
    """简单搜索"""

    res = es_product_service.search_product_simple()
    return {
        'res': res
    }


@app.route('/search', methods=['GET'])
def search():
    """综合搜索、筛选、排序"""
    
    res = es_product_service.search_product()
    return {}


@app.route('/recommend/<_id>', methods=['POST'])
def recommend(_id):
    """根据商品id推荐商品"""
    es_product_service.recommend_product(_id)
    return {}


@app.route('/search/relate', methods=['GET'])
def search_relate():
    """获取搜索的相关品牌、分类及筛选属性"""
    return {}
