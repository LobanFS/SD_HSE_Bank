from src.UI.base import Screen
from src.UI.io import read_str, pause
from src.finance.application.facades.import_facade import ImportFacade
from src.finance.application.facades.export_facade import ExportFacade

class IOScreen(Screen):
    title = "Импорт/Экспорт"

    def __init__(self, imp: ImportFacade, exp: ExportFacade, go_back):
        self.imp = imp
        self.exp = exp
        self._back = go_back

    def show(self) -> None:
        print("\n[Импорт/Экспорт]")
        print("1. Импорт CSV")
        print("2. Экспорт CSV")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    path = read_str("Путь к CSV: ")
                    self.imp.import_file(path); print("OK"); pause()
                case "2":
                    path = read_str("Куда сохранить CSV: ")
                    self.exp.export_all("csv", path); print("OK"); pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор."); pause()
        except Exception as e:
            print(f"Ошибка: {e}"); pause()
