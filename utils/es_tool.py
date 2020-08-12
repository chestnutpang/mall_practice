import elasticsearch
from functools import wraps


class ESConn:
    es = None

    @classmethod
    def init(cls, es_host, es_port):
        cls.es = elasticsearch.Elasticsearch(
            f'{es_host}:{es_port}',
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniff_timeout=60
        )


index = 'mall'


class ESControl:
    @classmethod
    def mall_index_create(cls, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            doc_type, _id = func(*args, **kwargs)
            print(doc_type, args, kwargs)
            # ESConn.es.create(index, _id, body, doc_type, params, headers)
            res = ESConn.es.create(index, _id, body=kwargs, doc_type=doc_type)
            return res
        return wrapped

    @classmethod
    def mall_index_search(cls, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            res = ESConn.es.search

    # @classmethod
    # def mall_index_create(cls, *args, **kwargs):
    #     res = ESConn.es.create(index, *args, **kwargs)
    #     return res

    # @classmethod
    # def mall_index_create_batch(cls, func):
    #     @wraps(func)
    #     def wrapped(*args, **kwargs):
    #         _id = func(*args, **kwargs)
    #         # ESConn.es.create(index, _id, body, doc_type, params, headers)
    #         res = ESConn.es.create(index, _id, *args, **kwargs)
    #         return res
    #     return wrapped

