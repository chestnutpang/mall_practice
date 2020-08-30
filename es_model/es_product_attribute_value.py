from elasticsearch_dsl import Document, Keyword, Text, Nested, connections


class EsProductAttributeValue(Document):
    value = Keyword()
    name = Keyword()

