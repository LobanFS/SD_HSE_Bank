from typing import Callable
from src.UI.base import Screen
from src.UI.io import pause

class HomeScreen(Screen):
    title = "HSE Bank — главное меню"

    def __init__(
        self,
        go_accounts: Callable[[], None],
        go_categories: Callable[[], None],
        go_operations: Callable[[], None],
        go_analytics: Callable[[], None],
        go_io: Callable[[], None],
        exit_app: Callable[[], None],
    ):
        self._go_accounts = go_accounts
        self._go_categories = go_categories
        self._go_operations = go_operations
        self._go_analytics = go_analytics
        self._go_io = go_io
        self._exit = exit_app

    def show(self) -> None:
        print("\n========== HSE BANK ==========")
        print("1. Аккаунты")
        print("2. Категории")
        print("3. Операции")
        print("4. Аналитика")
        print("5. Импорт/Экспорт")
        print("0. Выход")
        print("==============================")
        ch = input("Выберите пункт: ").strip()
        match ch:
            case "1": self._go_accounts()
            case "2": self._go_categories()
            case "3": self._go_operations()
            case "4": self._go_analytics()
            case "5": self._go_io()
            case "0": self._exit()
            case _:   print("Неверный выбор."); pause()
