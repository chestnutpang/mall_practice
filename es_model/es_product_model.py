from utils.es_tool import ESControl


class EsProduct:
    name = 'product'

    @classmethod
    @ESControl.mall_index_create
    def create(cls, body, params=None, headers=None):
        return cls.name, f"{body.get('id')}_{body.get('brandId')}" \
                         f"_{body.get('attr_id')}_{body.get('attr_product_attribute_id')}"

