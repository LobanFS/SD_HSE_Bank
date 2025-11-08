from datetime import date
from src.UI.base import Screen
from src.UI.io import read_str, read_float_positive, choose_from, pause
from src.UI.table import print_table
from src.finance.application.facades.query_facade import QueryFacade
from src.finance.application.facades.operation_facade import OperationFacade
from src.finance.domain.enums import OperationType

class OperationsScreen(Screen):
    title = "Операции"

    def __init__(self, query: QueryFacade, operation: OperationFacade, go_back):
        self.q = query
        self.op = operation
        self._back = go_back

    def show(self) -> None:
        print("\n[Операции]")
        print("1. Список")
        print("2. Добавить")
        print("3. Изменить")
        print("4. Удалить")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    rows = self.q.list_operations()
                    print_table(rows, [
                        ("id","ID"), ("type","Тип"), ("bank_account_id","Счет"),
                        ("amount","Сумма"), ("date","Дата"), ("category_id","Категория"),
                        ("description","Описание")
                    ])
                    pause()
                case "2":
                    id_ = read_str("ID: ")
                    t = choose_from("Тип", ["income","expense"])
                    acc = read_str("ID счета: ")
                    cat = read_str("ID категории: ")
                    amt = read_float_positive("Сумма (>0): ")
                    desc = input("Описание (опционально): ").strip() or None
                    self.op.create(id_, OperationType(t), acc, date.today(), cat, amt, desc)
                    print("OK"); pause()
                case "3":
                    id_ = read_str("ID операции: ")
                    t = choose_from("Новый тип", ["income","expense"])
                    acc = read_str("ID счета: ")
                    cat = read_str("ID категории: ")
                    amt = read_float_positive("Новая сумма (>0): ")
                    desc = input("Описание (опционально): ").strip() or None
                    self.op.update(id_, OperationType(t), acc, date.today(), cat, amt, desc)
                    print("OK"); pause()
                case "4":
                    id_ = read_str("ID операции: ")
                    self.op.delete(id_); print("OK"); pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор."); pause()
        except Exception as e:
            print(f"Ошибка: {e}"); pause()
