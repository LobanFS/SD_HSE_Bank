import yaml
from src.finance.domain.visitors.base_export_visitor import ExportVisitor
from src.finance.domain.entities import BankAccount, Category, Operation

class YamlExportVisitor(ExportVisitor):
    def __init__(self):
        self._data = {"accounts": [], "categories": [], "operations": []}

    def visit_account(self, a: BankAccount) -> None:
        self._data["accounts"].append({"id": a.id, "name": a.name, "balance": a.balance})

    def visit_category(self, c: Category) -> None:
        self._data["categories"].append({"id": c.id, "name": c.name, "type": c.type.value})

    def visit_operation(self, o: Operation) -> None:
        self._data["operations"].append({
            "id": o.id, "type": o.type.value, "bank_account_id": o.bank_account_id,
            "amount": o.amount, "date": o.date.isoformat(), "category_id": o.category_id,
            "description": o.description or ""
        })

    def result(self) -> str:
        return yaml.safe_dump(self._data, allow_unicode=True, sort_keys=False)
