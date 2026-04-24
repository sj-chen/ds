import pymysql
import pytest

from BaseApi.api_login import User
from BaseApi.http_client import HttpClient
from BaseApi.log import setup_logging
from common.file import load_setting, load_data


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

@pytest.fixture(scope="function")
def db(setting):
    connect = pymysql.connect(
        host = setting['mysql']['MYSQL_HOST'],
        port = int(setting['mysql']['MYSQL_PORT']),
        user = setting['mysql']['MYSQL_USER'],
        passwd = setting['mysql']['MYSQL_PASSWD'],
        database = setting['mysql']['MYSQL_DB'],
    )
    cursor = connect.cursor()
    # cursor.execute('select * from oms_order where member_id = 11')

    yield cursor
    cursor.close()

@pytest.fixture(scope="class")
def user_api(client) :
    u = User(client)
    yield u
