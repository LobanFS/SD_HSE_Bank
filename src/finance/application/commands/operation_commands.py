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

        category = self._category_repo.get(cmd.category_id)
        if category is None:
            raise ValueError(f"Category {cmd.category_id} not found")
        if category.type.value != cmd.type.value:
            raise ValueError("Operation type and category type must match")


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

@dataclass(frozen=True)
class UpdateOperation:
    id: str
    type: OperationType
    bank_account_id: str
    amount: float
    date: date
    category_id: str
    description: str | None = None


class UpdateOperationHandler:
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

    def handle(self, cmd: UpdateOperation) -> None:
        old = self._operation_repo.get(cmd.id)
        if old is None:
            raise ValueError(f"Operation {cmd.id} not found")

        old_account = self._account_repo.get(old.bank_account_id)
        if old_account is None:
            raise ValueError(f"BankAccount {old.bank_account_id} not found")

        new_account = self._account_repo.get(cmd.bank_account_id)
        if new_account is None:
            raise ValueError(f"BankAccount {cmd.bank_account_id} not found")

        category = self._category_repo.get(cmd.category_id)
        if category is None:
            raise ValueError(f"Category {cmd.category_id} not found")
        if category.type.value != cmd.type.value:
            raise ValueError("Operation type and category type must match")

        old_delta = old.amount if old.type == OperationType.INCOME else -old.amount
        self._account_repo.update(replace(old_account, balance=old_account.balance - old_delta))

        new_op = self._factory.create_operation(
            id=cmd.id,
            type=cmd.type,
            bank_account_id=cmd.bank_account_id,
            amount=cmd.amount,
            date=cmd.date,
            category_id=cmd.category_id,
            description=cmd.description,
        )
        self._operation_repo.update(new_op)

        new_account = self._account_repo.get(cmd.bank_account_id)
        assert new_account is not None
        new_delta = cmd.amount if cmd.type == OperationType.INCOME else -cmd.amount
        self._account_repo.update(replace(new_account, balance=new_account.balance + new_delta))

@dataclass(frozen=True)
class DeleteOperation:
    id: str

class DeleteOperationHandler:
    def __init__(self, operation_repo: IRepository[Operation], account_repo: IRepository[BankAccount]):
        self._operation_repo = operation_repo
        self._account_repo = account_repo

    def handle(self, cmd: DeleteOperation) -> None:
        operation = self._operation_repo.get(cmd.id)
        if operation is None:
            raise ValueError(f"Operation {cmd.id} not found")

        account = self._account_repo.get(operation.bank_account_id)
        if account is None:
            raise ValueError(f"BankAccount {operation.bank_account_id} not found")

        delta = operation.amount if operation.type == OperationType.INCOME else -operation.amount
        self._account_repo.update(replace(account, balance=account.balance - delta))

        self._operation_repo.remove(cmd.id)
