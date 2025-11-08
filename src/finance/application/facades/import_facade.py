from pathlib import Path
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.factories.importer_factory import importer_for
from src.finance.domain.repositories import IRepository
from src.finance.domain.entities import BankAccount, Category, Operation
class ImportFacade:
    def __init__(self, factory: EntityFactory,
                 account_repo: IRepository[BankAccount],
                 category_repo: IRepository[Category],
                 operation_repo: IRepository[Operation]):
        self._factory = factory
        self._acc_repo, self._cat_repo, self._op_repo = account_repo, category_repo, operation_repo

    def import_file(self, file_path: str) -> None:
        raw = Path(file_path).read_text(encoding="utf-8")
        imp = importer_for(file_path, self._factory)
        accounts, categories, operations = imp.import_data(raw)

        for account in accounts:   self._acc_repo.safe_add(account)
        for category in categories: self._cat_repo.safe_add(category)
        for operation in operations: self._op_repo.safe_add(operation)
