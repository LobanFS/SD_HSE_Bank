from src.UI.base import Screen
from src.UI.io import read_str, choose_from, pause
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
        print("1. Импорт csv/json/yaml")
        print("2. Экспорт CSV")
        print("3. Экспорт JSON")
        print("4. Экспорт YAML")
        print("0. Назад")
        ch = input("Выберите: ").strip()
        try:
            match ch:
                case "1":
                    path = read_str("Путь к файлу: ")
                    self.imp.import_file(path)
                    print("OK")
                    pause()
                case "2":
                    path = read_str("Куда сохранить CSV: ")
                    self.exp.export_all("csv", path)
                    print("OK")
                    pause()
                case "3":
                    path = read_str("Куда сохранить JSON: ")
                    self.exp.export_all("json", path)
                    print("OK")
                    pause()
                case "4":
                    path = read_str("Куда сохранить YAML: ")
                    self.exp.export_all("yaml", path)
                    print("OK")
                    pause()
                case "0":
                    self._back()
                case _:
                    print("Неверный выбор.")
                    pause()
        except Exception as e:
            print(f"Ошибка: {e}")
            pause()
