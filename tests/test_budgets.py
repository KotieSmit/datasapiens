from xmlrpc.server import list_public_methods
from pages.lists import ListsPage
from pages.stats import StatsPage


class TestBudgets:

    budgets = {
        "Dev Team": {
            "Team event": {
                "name": "Team event",
                "amount": 1000,
                "category": "Entertainment",
                "negation": "-",
            },
            "Budget allocation": {
                "name": "Budget allocation",
                "amount": 1500,
                "category": "Other",
                "negation": "+",
            },
            "Team lunch": {
                "name": "Team lunch",
                "amount": 300,
                "category": "Food",
                "negation": "-",
            },
        },
        "HR": {
            "Office event for HR staff": {
                "name": "Office event for HR staff",
                "amount": 250,
                "category": "Entertainment",
                "negation": "-",
            },
            "Uber": {
                "name": "Uber",
                "amount": 20,
                "category": "Transport",
                "negation": "-",
            },
            "Budget allocation": {
                "name": "Budget allocation",
                "amount": 1000,
                "category": "Other",
                "negation": "+",
            },
        },
        "Delete this budget": {
            "plus_1": {
                "name": "plus_1",
                "amount": 10000,
                "category": "Entertainment",
                "negation": "+",
            },
            "minus_1": {
                "name": "minus_1",
                "amount": 100,
                "category": "Entertainment",
                "negation": "-",
            },
            "plus_2": {
                "name": "plus_2",
                "amount": 10000,
                "category": "Entertainment",
                "negation": "+",
            },
            "minus_2": {
                "name": "minus_2",
                "amount": 100,
                "category": "Entertainment",
                "negation": "-",
            },
        },
    }

    def test_adding_and_removing_budgets(self, page: ListsPage):
        lists_page = ListsPage(page)
        budget_name = "Dev Team"
        for budget_name in self.budgets.keys():
            lists_page.add_budget(budget_name)
            lists_page.assert_budget_added(budget_name)

    def test_add_budget_entries(self, page: ListsPage):
        lists_page = ListsPage(page)
        for key, budget in self.budgets.items():
            lists_page.navigate_to_budget(key)
            lists_page.add_budget_entries(budget)
            lists_page.assert_budget_entries(budget)

    def test_delete_budget_entry(self, page: ListsPage):
        lists_page = ListsPage(page)
        stats_page = StatsPage(page)
        stats_page.navigate()
        # Get values before deleting budget entries
        total_expense = int(stats_page.total_expense.replace(" ", ""))
        total_income = int(stats_page.total_income.replace(" ", ""))
        budget_entry_minus = self.budgets["Delete this budget"]["minus_1"]
        budget_entry_plus = self.budgets["Delete this budget"]["plus_1"]
        # Navigate to and delete a budget entry
        lists_page.navigate_to_budget("Delete this budget")
        lists_page.delete_budget_entry(budget_entry_minus["name"])
        lists_page.delete_budget_entry(budget_entry_plus["name"])

        # Assert that deleting a budget entry, take effect on totals
        stats_page.navigate()
        assert (
            int(stats_page.total_expense.replace(" ", "")) - total_expense
            == budget_entry_minus["amount"]
        )
        assert (
            total_income - int(stats_page.total_income.replace(" ", ""))
            == budget_entry_plus["amount"]
        )

    def test_delete_budget_with_entries(self, page: ListsPage):
        lists_page = ListsPage(page)
        stats_page = StatsPage(page)
        stats_page.navigate()
        # Get values before deleting budget entries
        total_expense = int(stats_page.total_expense.replace(" ", ""))
        total_income = int(stats_page.total_income.replace(" ", ""))
        budget_entry_minus = self.budgets["Delete this budget"]["minus_2"]
        budget_entry_plus = self.budgets["Delete this budget"]["plus_2"]
        # Navigate to and delete a budget entry
        lists_page.navigate()
        lists_page.delete_budget("Delete this budget")

        # Assert that deleting a budget entry, take effect on totals
        stats_page.navigate()
        assert (
            int(stats_page.total_expense.replace(" ", "")) - total_expense
            == budget_entry_minus["amount"]
        )
        assert (
            total_income - int(stats_page.total_income.replace(" ", ""))
            == budget_entry_plus["amount"]
        )
