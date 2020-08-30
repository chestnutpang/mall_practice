from elasticsearch_dsl import Document, Keyword, Text, Nested, connections


class EsProduct(Document):
    productSn = Keyword()

    brandName = Keyword()

    productCategoryName = Keyword()

    name = Text(analyzer="ik_max_word")
    subTitle = Text(analyzer="ik_max_word")
    keywords = Text(analyzer="ik_max_word")

    attrValueList = Nested()

    class Index:
        name = 'pms'



if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    # connections.create_connection()
    EsProduct.init()
