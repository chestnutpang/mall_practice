from utils.mysql_tool import DBMysql


sql_query = """
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


def es_product_query(_id=None):
    if _id is None:
        query = sql_query
    else:
        query = sql_query + f'and p.id = {_id}'

    DBMysql.cursor.execute(query)
    results = DBMysql.cursor.fetchall()
    desc = list(map(lambda x: x[0], DBMysql.cursor.description))
    for result in results:
        product = data_to_dict(desc[:-5], result[:-5])
        attr = data_to_dict(desc[-5:], result[-5:])
        yield product, attr


def data_to_dict(keys, values):
    result = {}
    for i in range(len(keys)):
        result[keys[i]] = values[i]
    return result


if __name__ == '__main__':
    import pymysql
    db = pymysql.connect('localhost', 'root', 'ghost2111', 'mall')
    db_cursor = db.cursor()
    res = es_product_query()
    print(db_cursor.description)
    print('>>>>')
    for r in res:
        print(r)
