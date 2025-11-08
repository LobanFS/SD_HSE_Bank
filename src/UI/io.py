from datetime import date

def read_str(prompt: str) -> str:
    s = input(prompt).strip()
    while s == "":
        s = input("Не может быть пустым, повторите: ").strip()
    return s

def read_float_positive(prompt: str) -> float:
    while True:
        try:
            raw = input(prompt).strip()
            val = float(raw)
            if val <= 0:
                print("Введите положительное число.")
                continue
            return val
        except ValueError:
            print("Неверный формат числа. Повторите.")

def read_date(prompt: str) -> date:
    while True:
        try:
            return date.fromisoformat(input(prompt).strip())
        except Exception:
            print("Неверная дата, формат YYYY-MM-DD.")

def choose_from(prompt: str, options: list[str]) -> str:
    while True:
        v = input(f"{prompt} {options}: ").strip().lower()
        if v in options:
            return v
        print("Неверный выбор.")

def pause():
    input("\nНажмите Enter для продолжения...")
