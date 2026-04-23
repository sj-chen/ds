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

    def get(self, json_path: str ,default=None):
        data = self.json
        keys = json_path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default

        return data

    def assert_status(self, expected_status):
        if self.status_code != int(expected_status):
            raise AssertionError(f'Expected status {expected_status} but got {self.status_code}')
        return self

    def assert_code(self, code:str ):
        if self.get('code') != int(code):
            raise AssertionError(f'Expected status {code} but got {self.status_code}')
        return self

    def assert_message(self, message):
        if self.get('message') != message:
            raise AssertionError(f'Expected message {message} but got {self.get("message")}')
        return self

    def assert_success(self):
        return self.assert_status(200)