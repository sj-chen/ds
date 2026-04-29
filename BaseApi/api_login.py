from common.http_client import HttpClient
from common.response import ResponseWrapper


class User:
    def __init__(self, client: HttpClient):
        self.client = client

    def login(self, username, password, telephone='', pwd='') -> ResponseWrapper:
        resp = self.client.post("/sso/login",data = {"username": username, "password": password})
        tokenhead = resp.get('data.tokenHead')
        token = resp.get('data.token')
        if tokenhead:
            self.client.setHeaders({'Authorization': tokenhead+token})
            self.username = username
            self.password = password
            self.telephone = telephone
            self.pwd = pwd

        return resp

    def get_user_info(self) -> ResponseWrapper:
        resp = self.client.get("/sso/info")
        return resp

    def get_authcode(self, telephone) -> ResponseWrapper:
        resp = self.client.get(f"/sso/getAuthCode?telephone={telephone}")
        return resp

    def register_user(self, username, password, telephone, authCode ) -> ResponseWrapper:
        resp = self.client.post("/sso/register", data = {"username": username, "password": password,
                                                         "telephone": telephone,"authCode": authCode})
        return resp

    def update_password(self, telephone, password , authCode) -> ResponseWrapper:
        resp = self.client.post("/sso/updatePassword", data = {"telephone": telephone, "password": password, "authCode": authCode})
        return resp