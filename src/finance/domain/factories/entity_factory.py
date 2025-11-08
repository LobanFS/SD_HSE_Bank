from src.finance.domain.entities import BankAccount, Category, Operation
from src.finance.domain.enums import CategoryType, OperationType
from datetime import date

class EntityFactory:
    _instance = None

    def create_account(self, id: str, name: str, balance: float = 0.0) -> BankAccount:
        return BankAccount(id=id, name=name, balance=balance)

    def create_category(self, id: str, type: CategoryType, name: str) -> Category:
        return Category(id=id, type=type, name=name)

    def create_operation(self, id: str, type: OperationType,
                         bank_account_id: str, amount: float,
                         date: date, category_id: str, description: str | None = None) -> Operation:
        if amount <= 0:
            raise ValueError("Сумма операции должна быть положительной")
        return Operation(id=id, type=type, bank_account_id=bank_account_id,
                         amount=amount, date=date, category_id=category_id,
                         description=description)



