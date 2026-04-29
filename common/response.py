import requests


class ResponseWrapper:
    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def json(self):
        return self._response.json()

    @property
    def text(self):
        return self._response.text
    @property
    def headers(self):
        return self._response.headers

    def get(self, json_path: str ,default=None):
        data = self.json
        keys = json_path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default

        return data

    def assert_status(self, expected_status) -> "ResponseWrapper":
        if self.status_code != expected_status:
            raise AssertionError(f'Expected status {expected_status} but got {self.status_code}')
        return self

    def assert_code(self, code:int ) -> "ResponseWrapper":
        if self.get('code') != code:
            raise AssertionError(f'Expected code {code} but got {self.get("code")}')
        return self

    def assert_message(self, message) :
        if self.get('message') != message:
            raise AssertionError(f'Expected message {message} but got {self.get("message")}')
        return self

    def assert_success(self) -> "ResponseWrapper":
        return self.assert_status(200)

    def assert_data(self, key, value) -> "ResponseWrapper":
        if self.get(key) != value :
            raise AssertionError(f'Expected value {value} but got {self.get(key)}')
        return self

    def assert_data_key(self, key) -> "ResponseWrapper":
        if not self.get(key):
            raise AssertionError(f'Expected key {key} but got {self.get(key)}')
        return self

    def assert_not_data_key(self, key) -> "ResponseWrapper":
        if self.get(key):
            raise AssertionError(f'Don\'t expected key {key} but got {self.get(key)}')
        return self

