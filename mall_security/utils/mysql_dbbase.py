import peewee
from utils.mysql_tool import DBConn


class BaseModel(peewee.Model):
    class Meta:
        database = DBConn.db
