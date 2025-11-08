from src.UI.base import Screen
from src.UI.io import read_str, choose_from, pause
from src.UI.table import print_table
from src.finance.application.facades.query_facade import QueryFacade
from src.finance.application.facades.category_facade import CategoryFacade
from src.finance.domain.enums import CategoryType

class CategoriesScreen(Screen):
    title = "Категории"

    def __init__(self, query: QueryFacade, category: CategoryFacade, go_back):
        self.q = query
        self.cat = category
        self._back = go_back

    def show(self) -> None:
        print("\n[Категории]")
        print("1. Список")
        print("2. Создать")
        print("3. Переименовать")
        print("4. Удалить")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    rows = self.q.list_categories()
                    print_table(rows, [("id","ID"), ("type","Тип"), ("name","Название")])
                    pause()
                case "2":
                    id_ = read_str("ID: ")
                    name = read_str("Название: ")
                    t = choose_from("Тип", ["income","expense"])
                    self.cat.create(id_, CategoryType(t), name); print("OK"); pause()
                case "3":
                    id_ = read_str("ID: "); new_name = read_str("Новое имя: ")
                    self.cat.rename(id_, new_name); print("OK"); pause()
                case "4":
                    id_ = read_str("ID: ")
                    self.cat.delete(id_); print("OK"); pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор."); pause()
        except Exception as e:
            print(f"Ошибка: {e}"); pause()
