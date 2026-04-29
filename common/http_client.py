import logging
from logging import Logger

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from common.response import ResponseWrapper


class HttpClient:
    def __init__(self, host, logger: Logger ):
        self.host = host
        self.session = requests.Session()
        self._retry()
        self.logger = logger

    def get(self, url) -> ResponseWrapper:
        url = self.host + url
        self.logger.debug(f"GET {url}")
        print("====+++++++++++++++")
        print(self.session.headers)
        resp = None
        try:
            resp = self.session.get(url)
        except requests.exceptions.RequestException as e:
            self.logger.error(e)

        # if resp is None or self.check(resp):
        #     return resp
        print(resp.request.url, resp.request.headers, resp.request.body)
        return ResponseWrapper(resp)

    def post(self, url, data) -> ResponseWrapper:
        url = self.host + url
        self.logger.debug(f"POST {url}")
        logging.getLogger("urllib3").setLevel(logging.DEBUG)

        resp = self.session.post(url, data=data)
        print(resp.request.url, resp.request.headers, resp.request.body)
        # if not self.check(resp):
        #     resp = self.session.post(url, data=data)
        return ResponseWrapper(resp)


    def _retry(self) :
        retry_strategy = Retry(
            total= 3,
            backoff_factor=2,
            status_forcelist=(404,500,502,503,504),
            allowed_methods=frozenset(("GET","POST",)),
            raise_on_status=False  # 即使响应状态码非200，也不在Retry层抛出异常，交给业务代码处理
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        # 将适配器挂载到 http 和 https 的请求上
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)


    def check(self, res: requests.Response) :
        if res.status_code == 401:
            self.logger.info("401 Unauthorized")
            # login()
            return False
        return True


    def close(self):
        self.session.close()

    def setHeaders(self, headers):
        self.session.headers.clear()
        self.session.headers.update(headers)