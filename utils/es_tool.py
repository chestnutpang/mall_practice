from elasticsearch_dsl import connections


class ESConn:
    es = None

    @classmethod
    def init(cls, es_host, es_port):
        connections.create_connection(hosts=[f'{es_host}:{es_port}'])


