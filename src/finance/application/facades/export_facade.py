from pathlib import Path
from typing import Literal
from src.finance.infrastructure.in_memory_repos.operation_repo import InMemoryOperationRepo
from src.finance.infrastructure.in_memory_repos.account_repo import InMemoryAccountRepo
from src.finance.infrastructure.in_memory_repos.category_repo import InMemoryCategoryRepo
from src.finance.domain.visitors.base_export_visitor import ExportVisitor
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.decorators.timing import timed
from src.finance.infrastructure.export.csv_export_visitor import CsvExportVisitor

Format = Literal["csv"]

class ExportFacade:
    def __init__(self,
                 account_repo: InMemoryAccountRepo,
                 category_repo: InMemoryCategoryRepo,
                 operation_repo: InMemoryOperationRepo,
                 recorder: Recorder):
        self._account_repo, self._category_repo, self._operation_repo = account_repo, category_repo, operation_repo
        self._export_all_timed = timed(recorder, "Export.All")(self._export_all_impl)

    def _make_visitor(self, fmt: Format) -> ExportVisitor:
        if fmt == "csv":  return CsvExportVisitor()

    def _export_all_impl(self, fmt: Format, out_path: str) -> str:
        visitor = self._make_visitor(fmt)

        for account in self._account_repo.list(): visitor.visit_account(account)
        for category in self._category_repo.list(): visitor.visit_category(category)
        for operation in self._operation_repo.list():  visitor.visit_operation(operation)
        content = visitor.result()
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return str(p)

    def export_all(self, fmt: Format, out_path: str) -> str:
        return self._export_all_timed(fmt, out_path)