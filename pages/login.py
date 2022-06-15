from playwright.sync_api import Page


class LoginPage:
    _signup = "text=Sign Up"

    # def __init__(self, impl_obj: page) -> None:
    #     super().__init__(impl_obj)
    def __init__(self, page: Page):
        self.page = page
        # pass

    def navigate(self):
        """Navigate to this page"""
        self.page.goto(self.path)
        self.page.eval_on_selector("iframe", 'el => el.setAttribute("hidden", "")')

    @property
    def path(self):
        """Returns url for the page"""
        return "/login"

    @property
    def user_name_field(self):
        """Returns the user_name field"""
        return self.page.wait_for_selector('input[type="username"]')

    @property
    def password_field(self):
        """Returns the password field"""
        return self.page.wait_for_selector('input[type="password"]')

    @property
    def log_in_button(self):
        """Returns the login button"""
        return self.page.wait_for_selector('button:has-text("Log In")')

    def login_user(self, user):
        """Log user into application"""
        self.user_name_field.fill(user["username"])
        self.password_field.fill(user["password"])
        self.log_in_button.click()
