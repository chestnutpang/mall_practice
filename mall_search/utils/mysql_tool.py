import pymysql

db = None


class DBMysql:
    db = None
    cursor = None
    
    @classmethod
    def db_init(cls, *args):
        cls.db = pymysql.connect(*args)
        cls.cursor = cls.db.cursor()
