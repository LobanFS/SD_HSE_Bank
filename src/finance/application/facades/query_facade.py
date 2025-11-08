from typing import Optional, List
from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.domain.entities import BankAccount, Category, Operation
from src.finance.domain.repositories import IRepository


class QueryFacade:
    def __init__(
        self,
        account_repo: IRepository[BankAccount],
        category_repo: IRepository[Category],
        operation_repo: IRepository[Operation],
        recorder: Recorder,
    ):
        self._accounts = account_repo
        self._categories = category_repo
        self._operations = operation_repo

        self.list_accounts = timed(recorder, "Query.ListAccounts")(self._list_accounts)
        self.list_categories = timed(recorder, "Query.ListCategories")(self._list_categories)
        self.list_operations = timed(recorder, "Query.ListOperations")(self._list_operations)
        self.get_account = timed(recorder, "Query.GetAccount")(self._get_account)
        self.get_category = timed(recorder, "Query.GetCategory")(self._get_category)
        self.get_operation = timed(recorder, "Query.GetOperation")(self._get_operation)

    def _list_accounts(self) -> List[BankAccount]:
        return self._accounts.list()

    def _list_categories(self) -> List[Category]:
        return self._categories.list()

    def _list_operations(self) -> List[Operation]:
        return self._operations.list()

    def _get_account(self, id: str) -> Optional[BankAccount]:
        return self._accounts.get(id)

    def _get_category(self, id: str) -> Optional[Category]:
        return self._categories.get(id)

    def _get_operation(self, id: str) -> Optional[Operation]:
        return self._operations.get(id)
