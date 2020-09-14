from es_model import EsProduct
from utils.es_tool import ESConn
from service.sql import es_product_query
from elasticsearch import helpers
from utils.gevent_pool import gevent_pool
import copy


# 导入全部商品
def import_all_impl():
    count = get_product_bulk()
    return count


product_es_bulk = {
    '_index': 'pms',
    '_type': 'doc',
    '_source': None
}


def get_product_bulk(_id=None):
    pms_map = {}
    for product, attr in es_product_query(_id):
        if pms_map.get(product.get('id')) is None:
            pms = EsProduct(**product)
            pms.meta.id = product.get('id')
        else:
            pms = pms_map.get(product.get('id'))
        pms.add_attr_value(attr)
        pms_map[product.get('id')] = pms
    count = 0
    for pms in pms_map.values():
        pms.save()
        count += 1
    return count

def save_product_bulk(bulk_list):
    helpers.bulk(ESConn.es, bulk_list)



'''
def get_product_list(_id=None):
    """
    SQL 语句:
    select
            p.id id,
            p.product_sn productSn,
            p.brand_id brandId,
            p.brand_name brandName,
            p.product_category_id productCategoryId,
            p.product_category_name productCategoryName,
            p.pic pic,
            p.name name,
            p.sub_title subTitle,
            p.price price,
            p.sale sale,
            p.new_status newStatus,
            p.recommand_status recommandStatus,
            p.stock stock,
            p.promotion_type promotionType,
            p.keywords keywords,
            p.sort sort,
            pav.id attr_id,
            pav.value attr_value,
            pav.product_attribute_id attr_product_attribute_id,
            pa.type attr_type,
            pa.name attr_name
        from pms_product p
        left join pms_product_attribute_value pav on p.id = pav.product_id
        left join pms_product_attribute pa on pav.product_attribute_id= pa.id
        where delete_status = 0 and publish_status = 1 group by id;
    """
    product_query = db.session.query(p.id.label('_id'), p.product_sn.label('productSn'), p.brand_id.label('brandId'),
                                     p.brand_name.label('brandName'), p.product_category_id.label('productCategoryId'),
                                     p.product_category_name.label('productCategoryName'), p.pic,
                                     p.name, p.sub_title.label('subTitle'), p.price, p.sale,
                                     p.new_status.label('newStatus'), p.recommand_status.label('recommendStatus'),
                                     p.stock, p.promotion_type.label('promotionType'),
                                     p.keywords.label('keywords'),
                                     p.sort,
                                     pav.id.label('attr_id'), pav.value.label('attr_value'),
                                     pav.product_attribute_id.label('attr_product_attribute_id'),
                                     func.group_concat(pa.type).label('attr_type'),
                                     func.group_concat(pa.name).label('attr_name')) \
        .filter(p.delete_status == 0, p.publish_status == 1).join(pav, p.id == pav.product_id) \
        .join(pa, pav.product_attribute_id == pa.id)
    if _id is not None:
        product_list = product_query.filter(p.id == _id).all()
    else:
        product_list = product_query.all()
    product_map = {}
    for product in product_list:
        if product[0] in product_map:
            es_product = product_map[product[0]]
        else:
            es_product = EsProduct(data_to_dict(product.keys[:-5], product[:-5]))
        es_product.add_attr_value(data_to_dict(product.keys[-5:], product[-5:]))
        product_map[product[0]] = es_product

    for product in product_map.values():
        yield product


def get_product(_id):
    es_product = EsProduct.get(_id)
    return es_product


def delete_product(_id):
    es_product = EsProduct.get(_id)
    es_product.delete()


def create_product_by_id(_id):
    product_list = get_product_list(_id)
    es_product = None
    for product in product_list:
        if es_product is None:
            es_product = EsProduct(data_to_dict(product.keys[:-5], product[:-5]))
        es_product.add_attr_value(data_to_dict(product.keys[-5:], product[-5:]))
    es_product.save()
'''


def recommend_product(_id):
    es_product = EsProduct.get(_id)
    es_product.update(recommendStatus=1)


def search_product(search_param):
    product_search = EsProduct.search().query("match", **search_param)
    res = product_search.execute()
    print(res)
    return {}
