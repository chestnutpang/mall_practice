import peewee_async


class DBConn:
    db = None

    @classmethod
    def db_init(cls, app):
        cls.db = app.db = peewee_async.MySQLDatabase(
            app.server_config.mysql_db,
            host=app.server_config.mysql_host,
            port=app.server_config.mysql_port,
            user=app.server_config.mysql_user,
            password=app.server_config.mysql_password,
        )
        cls.db.connect()


def init_model():
    from model import User
    DBConn.db.create_tables([User])
