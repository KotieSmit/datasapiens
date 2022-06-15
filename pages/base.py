from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(self.path)

    @property
    def path(self):
        return "/lists"

    @property
    def user_name_field(self):
        return self.page.wait_for_selector('input[type="username"]')

    @property
    def password_1_field(self):
        return self.page.wait_for_selector('input[type="password"] >> nth=0')

    @property
    def password_2_field(self):
        return self.page.wait_for_selector('input[type="password"] >> nth=1')

    @property
    def sign_up_button(self):
        return self.page.wait_for_selector('button:has-text("Sign Up")')

    def assert_duplicate_user_error(self):
        """Assert the duplicate user error is displayed"""
        assert self.page.is_visible("text=Username is already taken.")

    def sign_up_user(self, user):
        """Sign up user, if 'password_2' is supplied it will be used for repeat password, else the given password will be used for both password fields"""
        self.user_name_field.fill(user["username"])
        self.password_1_field.fill(user["password"])
        self.password_2_field.fill(getattr(user, "password_2", user["password"]))
        self.sign_up_button.click()
