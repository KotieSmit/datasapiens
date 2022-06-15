from playwright.sync_api import Page


class StatsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to this page"""
        self.page.goto(self.path)

    @property
    def path(self):
        """Returns url for the page"""
        return "/stats"

    @property
    def total_income(self):
        """Return total income value"""
        return self.page.wait_for_selector(
            'div:right-of(span:has-text("Total Income:"))'
        ).inner_text()

    @property
    def total_expense(self):
        """Return total expense value"""
        return self.page.wait_for_selector(
            'div:right-of(span:has-text("Total Expense:"))'
        ).inner_text()
