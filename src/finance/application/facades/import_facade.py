from pathlib import Path
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.factories.importer_factory import importer_for
from src.finance.domain.repositories import IRepository
from src.finance.domain.entities import BankAccount, Category, Operation
from src.finance.domain.errors import AlreadyExistsError
from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder

class ImportFacade:
    def __init__(self,
                 factory: EntityFactory,
                 account_repo: IRepository[BankAccount],
                 category_repo: IRepository[Category],
                 operation_repo: IRepository[Operation],
                 recorder: Recorder):
        self._factory = factory
        self._acc_repo, self._cat_repo, self._op_repo = account_repo, category_repo, operation_repo
        self._import_timed = timed(recorder, "Import.File")(self._import_impl)

    def import_file(self, file_path: str) -> None:
        self._import_timed(file_path)

    def _import_impl(self, file_path: str) -> None:
        raw = Path(file_path).read_text(encoding="utf-8")
        imp = importer_for(file_path, self._factory)
        accounts, categories, operations = imp.import_data(raw)

        for account in accounts:
            try:
                self._acc_repo.add(account)
            except AlreadyExistsError:
                pass

        for category in categories:
            try:
                self._cat_repo.add(category)
            except AlreadyExistsError:
                pass

        for operation in operations:
            try:
                self._op_repo.add(operation)
            except AlreadyExistsError:
                pass
