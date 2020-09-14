import pymysql

db = None


class DBMysql:
    db = None
    cursor = None
    
    @classmethod
    def db_init(cls, *args):
        cls.db = pymysql.connect(*args)
        cls.cursor = cls.db.cursor()


if __name__ == '__main__':
    pymysql.connect('localhost', 'root', 'ghost2111', 'mall')
