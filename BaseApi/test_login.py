import pytest
import allure
from common.file import load_data

data = load_data('user.yaml')

@allure.feature("用戶")
class TestLogin:
    @pytest.mark.parametrize('username, password,code,message', data['test_login_user'])
    @allure.story("登录")
    def test_login_user(self, username, password, code, message, db, user_unlogin):
        res = user_unlogin.login(username, password)
        res.assert_success().assert_code(code).assert_message(message)

    @pytest.mark.parametrize('username, password,code,message', data['test_login_user'])
    @allure.story("个人信息")
    def test_info(self,username, password,code,message, db, user):
        res = user.get_user_info()
        res.assert_success().assert_code(code).assert_message(message)