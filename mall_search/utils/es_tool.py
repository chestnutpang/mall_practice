from elasticsearch_dsl import connections
import es_model


class RegisterModel:
    model_list = []

    @classmethod
    def register(cls):
        cls.model_list.append(es_model.EsProduct)

    @classmethod
    def get_model_list(cls):
        cls.register()
        return cls.model_list


class ESConn:
    es = None

    @classmethod
    def init(cls, es_host, es_port):
        cls.es = connections.create_connection(hosts=[f'{es_host}:{es_port}'])
        cls.register_model()

    @classmethod
    def register_model(cls):
        for model in RegisterModel.get_model_list():
            model.init()

