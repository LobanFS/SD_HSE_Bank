from typing import Optional
from dataclasses import dataclass, replace
from datetime import date
from src.finance.domain.entities import Operation, BankAccount, Category
from src.finance.domain.enums import OperationType
from src.finance.domain.repositories import IRepository
from src.finance.domain.factories.entity_factory import EntityFactory

@dataclass
class CreateOperation:
    id: str
    type: OperationType
    bank_account_id: str
    date: date
    amount: float
    category_id: str
    description: Optional[str] = None

class CreateOperationHandler:
    def __init__(
        self,
        operation_repo: IRepository[Operation],
        account_repo: IRepository[BankAccount],
        category_repo: IRepository[Category],
        factory: EntityFactory,
    ):
        self._operation_repo = operation_repo
        self._account_repo = account_repo
        self._category_repo = category_repo
        self._factory = factory

    def handle(self, cmd: CreateOperation) -> None:
        account = self._account_repo.get(cmd.bank_account_id)
        if account is None:
            raise ValueError(f"BankAccount {cmd.bank_account_id} not found")

        if self._category_repo.get(cmd.category_id) is None:
            raise ValueError(f"Category {cmd.category_id} not found")

        if self._operation_repo.get(cmd.id) is not None:
            raise ValueError(f"Operation with id={cmd.id} already exists")

        op = self._factory.create_operation(
            id=cmd.id,
            type=cmd.type,
            bank_account_id=cmd.bank_account_id,
            amount=cmd.amount,
            date=cmd.date,
            category_id=cmd.category_id,
            description=cmd.description,
        )

        self._operation_repo.add(op)

        delta = cmd.amount if cmd.type == OperationType.INCOME else -cmd.amount
        updated_account = replace(account, balance=account.balance + delta)
        self._account_repo.update(updated_account)
