from playwright.sync_api import Page


class ListsPage:
    budget_name = None
    budget_entry_name = None

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to this page"""
        self.page.goto(self.path)
        self.page.eval_on_selector("iframe", 'el => el.setAttribute("hidden", "")')

    @property
    def path(self):
        """Returns url for the page"""
        return "/lists"

    @property
    def log_out_button(self):
        """Returns log out button"""
        return self.page.wait_for_selector('button:has-text("Log Out")')

    @property
    def budget_entry_list_bar(self):
        """Returns bar which contains a budget entry list item for the given 'budget_entry_name'"""
        try:
            return self.page.wait_for_selector(
                f'div div:has-text("{self.budget_entry_name}")', timeout=2000
            )
        except:
            return None

    @property
    def budget_entry_bar(self):
        """Horizontal bar containing the input field and the add button for adding a budget"""
        return self.page.wait_for_selector('div:below(:text("Add Budget"))')

    @property
    def budget_input(self):
        """Returns the budget input field"""
        return self.budget_entry_bar.wait_for_selector('input[type="text"]')

    @property
    def add_budget_button(self):
        return self.budget_entry_bar.wait_for_selector("button")

    @property
    def budget_list_panel(self):
        """Panel housing list of existing budgets"""
        try:
            return self.page.wait_for_selector(
                f'h3:has-text("{self.budget_name}")', timeout=1000
            ).wait_for_selector("xpath=../..")
        except:
            return None

    @property
    def budget_list_name(self):
        """Return the element with the given 'budget_name'"""
        return self.page.wait_for_selector(f'h3:has-text("{self.budget_name}")')

    @property
    def budget_list_delete_button(self):
        """Returns the delete button for the given"""
        return self.budget_list_panel.wait_for_selector("button")

    @property
    def add_entry_panel(self):
        """Returns the horizontal bar containing the add entry elements"""
        return self.page.wait_for_selector('div:below(h2:has-text("Add Entry"))')

    @property
    def add_entry_name_input(self):
        """Returns the name input field for adding new budget"""
        return self.add_entry_panel.wait_for_selector(
            'div:has-text("Entry Name") input'
        )

    @property
    def entry_value_input(self):
        """Returns the value input field for adding new budget"""
        return self.add_entry_panel.wait_for_selector('div:has-text("Amount") input')

    @property
    def budget_entry_delete_button(self):
        """Returns the delete button for a budget entry"""
        return self.budget_entry_list_bar.wait_for_selector("button")

    @property
    def entry_category_select(self):
        """Returns the category select element for adding new budget entry"""
        return self.add_entry_panel.wait_for_selector("select")

    @property
    def add_entry_negation_button(self):
        """Returns the + - button for adding new budget entry"""
        return self.add_entry_panel.wait_for_selector("button")

    @property
    def add_entry_add_button(self):
        """Returns the 'Add' button for adding new budget entry"""
        return self.add_entry_panel.wait_for_selector("button >> nth=1")

    def negation_button_state(self):
        """Determine the state of the +- button"""
        if (
            self.add_entry_panel.wait_for_selector("div[mode]").get_attribute("mode")
            == "0"
        ):
            return "+"
        return "-"

    def add_budget(self, budget_name):
        """Add new budget"""
        self.navigate()
        self.budget_input.fill(budget_name)
        self.add_budget_button.click()

    def assert_budget_added(self, budget_name):
        """Assert the budget was added"""
        assert self.page.wait_for_selector(f'h3:has-text("{budget_name}")').is_visible()

    def navigate_to_budget(self, budget_name):
        """Navigate to given budget"""
        self.budget_name = budget_name
        self.navigate()
        self.budget_list_name.click()

    def add_budget_entries(self, data):
        """Add budget entries form given list"""
        for entry in data:
            self.add_budget_entry(data[entry])

    def add_budget_entry(self, data):
        """Add single budget entry"""
        self.add_entry_name_input.fill(data["name"])
        self.entry_category_select.select_option(data["category"])
        if data["negation"] != self.negation_button_state():
            self.add_entry_negation_button.click()
        self.entry_value_input.fill(str(data["amount"]))
        self.add_entry_add_button.click()

    def assert_budget_entries(self, data):
        """Assert budget entries are visible"""
        for entry in data:
            self.budget_entry_name = entry
            category = data[entry]["category"]
            amount = f"{data[entry]['negation']} {str(data[entry]['amount'])}"
            self.budget_entry_list_bar.wait_for_selector(
                f'h3:has-text("{self.budget_entry_name}")'
            ).is_visible()
            self.budget_entry_list_bar.wait_for_selector(
                f'span:has-text("{category}")'
            ).is_visible()
            self.budget_entry_list_bar.wait_for_selector(
                f'div:has-text("{amount}")'
            ).is_visible()

    def delete_budget_entry(self, budget_entry_name):
        """Delete budget entry"""
        self.budget_entry_name = budget_entry_name
        self.budget_entry_delete_button.click()
        assert self.budget_entry_list_bar == None

    def delete_budget(self, budget_name):
        self.budget_name = budget_name
        self.budget_list_delete_button.click()
        assert self.budget_list_panel == None
