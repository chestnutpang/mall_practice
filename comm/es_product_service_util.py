from model import *
from utils.es_tool import ESConn
from utils.mysql_tool import data_to_dict
import es_model


def import_all_impl():
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
        where delete_status = 0 and publish_status = 1
    """

    product_list = db.session.query(p.id.label('id'), p.product_sn.label('productSn'), p.brand_id.label('brandId'),
                                    p.brand_name.label('brandName'), p.product_category_id.label('productCategoryId'),
                                    p.product_category_name.label('productCategoryName'), p.pic,
                                    p.name, p.sub_title.label('subTitle'), p.price, p.sale,
                                    p.new_status.label('newStatus'), p.recommand_status.label('recommendStatus'),
                                    p.stock, p.promotion_type.label('promotionType'), p.keywords, p.sort,
                                    pav.id.label('attr_id'), pav.value.label('attr_value'),
                                    pav.product_attribute_id.label('attr_product_attribute_id'),
                                    pa.type.label('attr_type'), pa.name.label('attr_name'))\
        .filter(p.delete_status == 0, p.publish_status == 1).join(pav, p.id == pav.product_id) \
        .join(pa, pav.product_attribute_id == pa.id)\
        .all()
    index = 0
    for product in product_list:
        index += 1
        doc = data_to_dict(product.keys(), product)
        res = es_model.EsProduct.create(_id=index, body=doc)
        print(res)
    return len(product_list)
