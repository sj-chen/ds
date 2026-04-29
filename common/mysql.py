import pymysql
from common.file import load_setting
import pymysql.cursors
import logging
import time
setting = load_setting()

class LoggingCursor(pymysql.cursors.Cursor):
    def __init__(self, connection):
        super().__init__(connection)
        # 使用与测试框架统一的 logger，方便在同一个日志文件查看
        self.logger = logging.getLogger('api_test')

    def execute(self, query, args=None):
        start = time.perf_counter()
        try:
            result = super().execute(query, args)
            elapsed = time.perf_counter() - start
            self.logger.debug(f"[SQL] {query} | Args: {args} | Time: {elapsed:.6f}s")
            return result
        except Exception:
            elapsed = time.perf_counter() - start
            self.logger.error(f"[SQL FAILED] {query} | Args: {args} | Time: {elapsed:.6f}s")
            raise

class MysqlDb:
    def __init__(self) :
        connect = pymysql.connect(
            host = setting['mysql']['MYSQL_HOST'],
            port = int(setting['mysql']['MYSQL_PORT']),
            user = setting['mysql']['MYSQL_USER'],
            passwd = setting['mysql']['MYSQL_PASSWD'],
            database = setting['mysql']['MYSQL_DB'],
            autocommit = True,
            cursorclass = LoggingCursor
        )
        self.__cursor = connect.cursor()


    @property
    def cursor(self):
        return self.__cursor

    def close(self):
        self.__cursor.close()



    def execute(self, sql, params=None) :
        self.sql, self.params = sql, params
        self.__cursor.execute(sql, params)
        self.result = self.__cursor.fetchone()
        return self.result

    def fetchone(self):
        return self.__cursor.fetchone()

    def assert_exists(self, code) -> "MysqlDb":
        if code == 200 and self.result is None:
            AssertionError(f"[SQL] {self.sql} | Args: {self.params} | result: {self.result}")
        if code == 500 and self.result is not None:
            AssertionError(f"[SQL] {self.sql} | Args: {self.params} | result: {self.result}")
        return self

