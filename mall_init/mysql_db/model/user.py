from utils.mysql_tool import DbBase
from sqlalchemy import Column, VARCHAR, CHAR
import secrets
import string
SECRET_CHARS = string.ascii_lowercase + string.digits


class User:
    __tablename__ = 'user'
    # username = Column(VARCHAR(20))
    # phone = Column(CHAR(11))
    # mail = Column(VARCHAR(64))
    # password = Column(CHAR(64))
    # salt = Column(CHAR(64))

    def register(self, phone, password):
        sql = f'insert into {self.__tablename__} (phone, password) values("{phone}", "{password}")'


    def login(self, password):
        if self.password == password:
            return True

    def logout(self):
        pass

    def change_password(self, password):
        self.password = password
    
    def token_generate(self):
        pass
    

def salt_generate(size=48, chars=SECRET_CHARS):
    return ''.join(secrets.choice(chars) for _ in range(size))


# import sqlalchemy as sa
# tb1 = sa.Table()
# if __name__ == '__main__':
#