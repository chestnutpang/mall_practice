from elasticsearch_dsl import InnerDoc, Keyword


class EsProductAttributeValue(InnerDoc):
    value = Keyword()
    name = Keyword()
