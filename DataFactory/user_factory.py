import random
from pymysql.cursors import Cursor
from common.encrypt import Encrypt
import uuid

# from common.mysql import mysqldb


class UserFactory:
    def __init__(self, db: Cursor):
        self.db = db

    def __phone(self):
        prefix = ['13', '15', '16', '17', '18', '19']
        suffix = ''.join(str(random.randint(0,9))  for _ in range(9))
        phone = f'{random.choice(prefix)}{suffix}'
        return phone

    def __trace_id(self) -> uuid.UUID:
        return uuid.uuid4()


    def create_user(self, username = None, password = "123456"):
        if username is None:
            trace_id = self.__trace_id().hex[-5:]
            username = f'test_{trace_id}'
        pwd = Encrypt.hash_password(password)
        telephone = self.__phone()
        self.db.execute("insert into ums_member (username,password,phone) values(%s,%s,%s)",(username, pwd, telephone))
        return username, password, telephone, pwd

    def delete_user(self, username):
        self.db.execute("delete from ums_member where username = %s", (username))