import elasticsearch


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


if __name__ == '__main__':
    es = elasticsearch.Elasticsearch()
    print(es.get())
