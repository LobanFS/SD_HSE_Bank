from src.UI.base import Screen
from src.UI.io import read_date, pause
from src.finance.application.facades.analytics_facade import AnalyticsFacade
from src.finance.application.facades.query_facade import QueryFacade
from src.UI.table import print_table

class AnalyticsScreen(Screen):
    title = "Аналитика"

    def __init__(self, analytics: AnalyticsFacade, query: QueryFacade, go_back):
        self.an = analytics
        self.q = query
        self._back = go_back

    def show(self) -> None:
        print("\n[Аналитика]")
        print("1. Разница доходы-расходы за период")
        print("2. Группировка по категориям (все операции)")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    start = read_date("Начало (YYYY-MM-DD): ")
                    end = read_date("Конец  (YYYY-MM-DD): ")
                    diff = self.an.diff_for_period(start, end)
                    print(f"Разница: {diff}")
                    pause()
                case "2":
                    g = self.an.by_category()
                    # Выведем как табличку: category_id, income, expense
                    rows = [{"category_id": k, "income": v["income"], "expense": v["expense"]} for k, v in g.items()]
                    print_table(rows, [("category_id","Категория"), ("income","Доход"), ("expense","Расход")])
                    pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор."); pause()
        except Exception as e:
            print(f"Ошибка: {e}"); pause()
