from pages.signup import SignupPage
from pages.login import LoginPage


class TestAccess:
    def test_sign_up(self, page: SignupPage):
        signup_page = SignupPage(page)
        signup_page.navigate()
        user = {"username": "Mo", "password": "!oj!1#"}
        signup_page.sign_up_user(user)
        assert "/login" in page.url

    def test_duplicate_sign_up(self, page: SignupPage):
        signup_page = SignupPage(page)
        signup_page.navigate()
        user = {"username": "Mo", "password": "!oj!1#"}
        signup_page.sign_up_user(user)
        signup_page.assert_duplicate_user_error()

    def test_login(self, page: LoginPage):
        login_page = LoginPage(page)
        login_page.navigate()
        user = {"username": "Mo", "password": "!oj!1#"}
        login_page.login_user(user)
        assert "/lists" in page.url
