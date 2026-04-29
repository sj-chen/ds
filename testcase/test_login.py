import pytest
import allure
from models.user import *
from common.file import load_data, to_cases
data = load_data('user.yaml')

@pytest.fixture(scope='class', autouse=True)
def create_regrister_user(db, user_factory):
    cases = to_cases(TestRegister, data['test_register'])
    expectd_case: TestRegister
    for case in cases:
        if case.name == "已存在用户注册":
            user_factory.create_user(case.username)
    yield
    # db.execute("delete from ums_member where username like %s", ("test_%"))



@allure.feature("用戶")
class TestLogin:
    @pytest.mark.parametrize('case', to_cases(TestLoginUser, data['test_login_user']), ids = lambda c: c.name)
    @allure.story("登录")
    def test_login_user(self, case, db, user_unlogin):
        res = user_unlogin.login(case.username, case.password)
        res.assert_success().assert_code(case.expect_code).assert_message(case.expect_msg)

    @pytest.mark.parametrize('case', to_cases(TestInfo, data['test_info']), ids=lambda c: c.name)
    @allure.story("个人信息")
    def test_info(self, case, db, user):
        res = user.get_user_info()
        (res.assert_success().assert_code(case.expect_code).
         assert_message(case.expect_msg).assert_not_data_key('data.password').
         assert_data('data.username', case.username))

    @pytest.mark.parametrize('case', to_cases(TestRegister, data['test_register']), ids=lambda c: c.name)
    @allure.story("注册用户")
    def test_register_user(self, case, redis_client: redis.Redis, user_unlogin, db):
        getauthcode_resp = user_unlogin.get_authcode(case.telephone)
        # print(getauthcode_resp.status_code, getauthcode_resp.json)
        authcode = redis_client.get(f"mall:ums:authCode:{case.telephone}")
        authcode = authcode.strip().strip('"').strip("'")
        res = user_unlogin.register_user(case.username, case.password, case.telephone, authcode)
        # print(res.status_code, res.json)

    @pytest.mark.parametrize('case', to_cases(TestUpdatePassword, data['test_update_password']), ids=lambda c: c.name)
    def test_update_password(self, case, db, user_one, redis_client, encrypt):
        user_one.get_authcode(user_one.telephone)
        authCode = redis_client.getAuth(user_one.telephone)
        telephone = user_one.telephone
        if case.telephone is not None:
            telephone = case.telephone
        if case.authCode is not None:
            authCode = case.authCode
        res = user_one.update_password(telephone, case.password, authCode)
        result = db.execute("select password from ums_member where username=%s", (user_one.username))
        check_password = encrypt.check_password(case.password, result[0])
        assert check_password is (case.expect_code == 200)
        res.assert_success().assert_code(case.expect_code).assert_message(case.expect_msg)
