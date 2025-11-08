from dataclasses import replace
from src.finance.domain.entities import Operation, BankAccount, Category
from src.finance.domain.enums import OperationType
from src.finance.domain.repositories import IRepository
from src.finance.domain.errors import NotFoundError


class OperationCommon:
    def __init__(
        self,
        operation_repo: IRepository[Operation],
        account_repo: IRepository[BankAccount],
        category_repo: IRepository[Category] | None,
    ):
        self._operation_repo = operation_repo
        self._account_repo = account_repo
        self._category_repo = category_repo

    @staticmethod
    def _delta(type_: OperationType, amount: float) -> float:
        return amount if type_ == OperationType.INCOME else -amount

    def _get_account(self, id_: str) -> BankAccount:
        acc = self._account_repo.get(id_)
        if acc is None:
            raise NotFoundError(f"BankAccount {id_} not found")
        return acc

    def _get_category_checked(self, id_: str, op_type: OperationType) -> Category:
        if not self._category_repo:
            raise RuntimeError("Category repository not provided")
        cat = self._category_repo.get(id_)
        if cat is None:
            raise NotFoundError(f"Category {id_} not found")
        if cat.type != op_type:
            raise ValueError("Operation type and category type must match")
        return cat

    def _apply_delta(self, account: BankAccount, delta: float) -> None:
        self._account_repo.update(replace(account, balance=account.balance + delta))
