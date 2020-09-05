from elasticsearch_dsl import Document, Keyword, Text, Nested, connections
from es_model.es_product_attribute_value import EsProductAttributeValue


class EsProduct(Document):
    productSn = Keyword()

    brandName = Keyword()

    productCategoryName = Keyword()

    name = Text(analyzer="ik_max_word")
    subTitle = Text(analyzer="ik_max_word")
    keywords = Text(analyzer="ik_max_word")

    attrValueList = Nested(EsProductAttributeValue)

    class Index:
        name = 'pms'

    def add_attr_value(self, kwargs):
        product_attribute_value = EsProductAttributeValue(**kwargs)
        self.attrValueList.append(
            product_attribute_value
        )


if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    # connections.create_connection()
    EsProduct.init()
