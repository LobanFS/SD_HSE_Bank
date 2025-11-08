from src.UI.base import Screen
from src.UI.io import read_str, pause
from src.UI.table import print_table
from src.finance.application.facades.query_facade import QueryFacade
from src.finance.application.facades.account_facade import AccountFacade

class AccountsScreen(Screen):
    title = "Аккаунты"

    def __init__(self, query: QueryFacade, account: AccountFacade, go_back):
        self.q = query
        self.acc = account
        self._back = go_back

    def show(self) -> None:
        print("\n[Аккаунты]")
        print("1. Список")
        print("2. Создать")
        print("3. Переименовать")
        print("4. Удалить")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    rows = self.q.list_accounts()
                    print_table(rows, [("id","ID"), ("name","Название"), ("balance","Баланс")])
                    pause()
                case "2":
                    id_ = read_str("ID: ")
                    name = read_str("Название: ")
                    bal = float(input("Начальный баланс (по умолчанию 0): ") or 0)
                    self.acc.create(id_, name, bal); print("OK"); pause()
                case "3":
                    id_ = read_str("ID: ")
                    new_name = read_str("Новое имя: ")
                    self.acc.rename(id_, new_name); print("OK"); pause()
                case "4":
                    id_ = read_str("ID: ")
                    self.acc.delete(id_); print("OK"); pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор."); pause()
        except Exception as e:
            print(f"Ошибка: {e}"); pause()
