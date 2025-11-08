from typing import Optional
from dataclasses import dataclass
from datetime import date
from src.finance.domain.entities import Operation, BankAccount, Category
from src.finance.domain.enums import OperationType
from src.finance.domain.repositories import IRepository
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.errors import NotFoundError
from src.finance.application.commands.op_common import OperationCommon

@dataclass
class CreateOperation:
    id: str
    type: OperationType
    bank_account_id: str
    date: date
    amount: float
    category_id: str
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateOperation:
    id: str
    type: OperationType
    bank_account_id: str
    amount: float
    date: date
    category_id: str
    description: str | None = None


@dataclass(frozen=True)
class DeleteOperation:
    id: str

class CreateOperationHandler(OperationCommon):
    def __init__(
        self,
        operation_repo: IRepository[Operation],
        account_repo: IRepository[BankAccount],
        category_repo: IRepository[Category],
        factory: EntityFactory,
    ):
        super().__init__(operation_repo, account_repo, category_repo)
        self._factory = factory
    def handle(self, cmd: CreateOperation) -> None:
        account = self._get_account(cmd.bank_account_id)
        check = self._get_category_checked(cmd.category_id, cmd.type)
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
        self._apply_delta(account, self._delta(cmd.type, cmd.amount))

class UpdateOperationHandler(OperationCommon):
    def __init__(
        self,
        operation_repo: IRepository[Operation],
        account_repo: IRepository[BankAccount],
        category_repo: IRepository[Category],
        factory: EntityFactory,
    ):
        super().__init__(operation_repo, account_repo, category_repo)
        self._factory = factory
    def handle(self, cmd: UpdateOperation) -> None:
        old = self._operation_repo.get(cmd.id)
        if old is None:
            raise NotFoundError(f"Operation {cmd.id} not found")
        old_acc = self._get_account(old.bank_account_id)
        new_acc = self._get_account(cmd.bank_account_id)
        check = self._get_category_checked(cmd.category_id, cmd.type)
        self._apply_delta(old_acc, -self._delta(old.type, old.amount))
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
        self._apply_delta(new_acc, self._delta(cmd.type, cmd.amount))

class DeleteOperationHandler(OperationCommon):
    def __init__(
        self,
        operation_repo: IRepository[Operation],
        account_repo: IRepository[BankAccount],
    ):
        super().__init__(operation_repo, account_repo, category_repo=None)

    def handle(self, cmd: DeleteOperation) -> None:
        old = self._operation_repo.get(cmd.id)
        if old is None:
            raise NotFoundError(f"Operation {cmd.id} not found")
        acc = self._get_account(old.bank_account_id)
        self._apply_delta(acc, -self._delta(old.type, old.amount))
        self._operation_repo.remove(cmd.id)