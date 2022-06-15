from playwright.sync_api import Page


class SignupPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to this page"""
        self.page.goto(self.path)
        self.page.eval_on_selector("iframe", 'el => el.setAttribute("hidden", "")')

    @property
    def path(self):
        """Returns url for the page"""
        return "/signup"

    @property
    def user_name_field(self):
        return self.page.wait_for_selector('input[type="username"]')

    @property
    def password_1_field(self):
        """Returns the first password field for signup"""
        return self.page.wait_for_selector('input[type="password"] >> nth=0')

    @property
    def password_2_field(self):
        """Returns the second password field for signup"""
        return self.page.wait_for_selector('input[type="password"] >> nth=1')

    @property
    def sign_up_button(self):
        """Returns the signup submit button"""
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
