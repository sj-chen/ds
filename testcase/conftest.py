import pymysql
import pytest
import redis
from BaseApi.api_login import User
from DataFactory.user_factory import UserFactory
from common.encrypt import Encrypt
from common.http_client import HttpClient
from common.log import setup_logging
from common.file import load_setting, load_data
import bcrypt

from common.mysql import MysqlDb
from common.redis import RedisClient


@pytest.fixture(scope='session')
def config():
    pass

# @pytest.fixture(scope='session')
# def load_dataa(filename):
#     return load_data(filename)

@pytest.fixture(scope='session')
def setting() -> dict:
    return load_setting()

@pytest.fixture(scope="session")
def client(setup_logging):
    c = HttpClient("http://192.168.1.49:8085", logger=setup_logging)
    yield c
    c.close()

@pytest.fixture(scope="session")
def redis_client():
    r = RedisClient()
    yield r
    r.close()

@pytest.fixture(scope="session")
def encrypt():
    yield Encrypt()

@pytest.fixture(scope="session")
def db():
    db = MysqlDb()
    db.execute("delete from ums_member where username like 'test_%'")
    yield db
    db.close()

@pytest.fixture(scope="function")
def user_unlogin(client) :
    u = User(client)
    old_headers = client.session.headers.copy()   # 假设 client.headers 是字典
    yield u
    client.setHeaders(old_headers)

@pytest.fixture(scope="function")
def user_one(client, user_factory) :
    username, password, telephone, pwd = user_factory.create_user()
    u = User(client)
    u.login(username, password, telephone, pwd)
    yield u
    # user_factory.delete_user(username)

@pytest.fixture(scope="session")
def user(client, user_factory) :
    username, password, telephone, pwd = user_factory.create_user()
    u = User(client)
    u.login(username, password, telephone, pwd)
    yield u

@pytest.fixture(scope="session")
def user_factory(db) :
    return UserFactory(db)

