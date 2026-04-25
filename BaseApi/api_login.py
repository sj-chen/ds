from BaseApi.http_client import HttpClient
from BaseApi.response import ResponseWrapper


class User:
    def __init__(self, client: HttpClient):
        self.client = client

    def login(self, username, password ) -> ResponseWrapper:
        resp = self.client.post("/sso/login",data = {"username": username, "password": password})
        tokenhead = resp.get('data.tokenHead')
        token = resp.get('data.token')
        if tokenhead:
            self.client.setHeaders({'Authorization': tokenhead+token})
        return resp

    def get_user_info(self) -> ResponseWrapper:
        resp = self.client.get("/sso/info")
        return resp