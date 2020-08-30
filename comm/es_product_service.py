from sqlalchemy import func

from model import *
from utils.mysql_tool import data_to_dict
from es_model import EsProduct


# 导入全部商品
def import_all_impl():
    count = 0
    for product in get_product_list():
        create_product(product)
        count += 1
    return count


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
                                     func.group_concat(p.keywords).label('keywords'),
                                     p.sort,
                                     pav.id.label('attr_id'), pav.value.label('attr_value'),
                                     pav.product_attribute_id.label('attr_product_attribute_id'),
                                     func.group_concat(pa.type).label('attr_type'),
                                     func.group_concat(pa.name).label('attr_name')) \
        .filter(p.delete_status == 0, p.publish_status == 1).join(pav, p.id == pav.product_id) \
        .join(pa, pav.product_attribute_id == pa.id) \
        .group_by(p.id)
    if _id is not None:
        product_list = product_query.filter(p.id == _id).all()
    else:
        product_list = product_query.all()

    for product in product_list:
        yield product


def delete_product(_id):
    es_product = EsProduct(_id)
    es_product.delete(id=_id)


def create_product_by_id(_id):
    pass


def create_product(product):
    es_product = EsProduct(**data_to_dict(product.keys(), product))
    es_product.save()
