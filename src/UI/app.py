from src.UI.base import MenuLoop
from src.UI.screens.home import HomeScreen
from src.UI.screens.accounts import AccountsScreen
from src.UI.screens.categories import CategoriesScreen
from src.UI.screens.operations import OperationsScreen
from src.UI.screens.analytics import AnalyticsScreen
from src.UI.screens.io_screen import IOScreen

def run(container):
    acc = container.account_facade()
    cat = container.category_facade()
    op  = container.operation_facade()
    an  = container.analytics_facade()
    imp = container.import_facade()
    exp = container.export_facade()
    q   = container.query_facade()

    loop_holder = {}

    def go_home():
        loop_holder["loop"].set_screen(home)

    def go_accounts():
        loop_holder["loop"].set_screen(accounts)

    def go_categories():
        loop_holder["loop"].set_screen(categories)

    def go_operations():
        loop_holder["loop"].set_screen(operations)

    def go_analytics():
        loop_holder["loop"].set_screen(analytics)

    def go_io():
        loop_holder["loop"].set_screen(io_screen)

    def exit_app():
        loop_holder["loop"].stop()

    home = HomeScreen(go_accounts, go_categories, go_operations, go_analytics, go_io, exit_app)
    accounts = AccountsScreen(q, acc, go_home)
    categories = CategoriesScreen(q, cat, go_home)
    operations = OperationsScreen(q, op, go_home)
    analytics = AnalyticsScreen(an, q, go_home)
    io_screen = IOScreen(imp, exp, go_home)

    loop = MenuLoop(home)
    loop_holder["loop"] = loop
    loop.run()
