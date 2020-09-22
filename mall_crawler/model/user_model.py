import secrets
import string
from utils.mysql_tool import DbBase, db
from sqlalchemy.orm import aliased



class User:
    __tablename__ = 'user'
    username = Column(VARCHAR(20))
    phone = Column(CHAR(11))
    mail = Column(VARCHAR(64))
    password = Column(CHAR(64))
    salt = Column(CHAR(64))
