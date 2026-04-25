import dataclasses

import pytest
import allure
from common.file import load_data
data = load_data('user.yaml')

@dataclasses.dataclass
class TestLoginUserCase:
    name: str
    username: str
    password: str
    expect_code: int
    expect_msg: str

def to_login_user_case(raw_data: list[dict]) -> list[type[TestLoginUserCase]]:
    cases = []
    for item in raw_data:
        cases.append(TestLoginUserCase(
            name=item['name'],
            username=item['username'],
            password=item['password'],
            expect_code=item['expect_code'],
            expect_msg=item['expect_msg']
        ))
    return cases


@allure.feature("用戶")
class TestLogin:
    @pytest.mark.parametrize('case', to_login_user_case(data['test_login_user']), ids = lambda c: c.name  )
    @allure.story("登录")
    def test_login_user(self, case: TestLoginUserCase, db, user_unlogin):
        res = user_unlogin.login(case.username, case.password)
        res.assert_success().assert_code(case.expect_code).assert_message(case.expect_msg)
    #
    # @pytest.mark.parametrize('username, password', data['test_login_user'])
    # @allure.story("个人信息")
    # def test_info(self,username, password, db, user):
    #     res = user.get_user_info()
    #     res.assert_success().assert_code(code).assert_message(message)