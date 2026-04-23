from BaseApi.conftest import client
from BaseApi.http_client import HttpClient
from BaseApi.response import ResponseWrapper


class User:
    def __init__(self, client: HttpClient):
        self.client = client

    def login(self, username, password ) -> ResponseWrapper:
        resp = self.client.post("/sso/login",data = {"username": username, "password": password})
        print(resp.json)
        return resp