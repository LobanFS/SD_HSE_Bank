
import csv, io
from src.finance.domain.visitors.base_export_visitor import ExportVisitor
from src.finance.domain.entities import BankAccount, Category, Operation

class CsvExportVisitor(ExportVisitor):
    def __init__(self):
        self._rows = []

    def visit_account(self, a: BankAccount) -> None:
        self._rows.append({
            "kind": "account", "id": a.id, "name": a.name, "balance": a.balance,
            "type": "", "bank_account_id": "", "amount": "", "date": "", "category_id": "", "description": ""
        })

    def visit_category(self, c: Category) -> None:
        self._rows.append({
            "kind": "category", "id": c.id, "name": c.name, "type": c.type.value,
            "balance": "", "bank_account_id": "", "amount": "", "date": "", "category_id": "", "description": ""
        })

    def visit_operation(self, o: Operation) -> None:
        self._rows.append({
            "kind": "operation", "id": o.id, "type": o.type.value, "bank_account_id": o.bank_account_id,
            "amount": o.amount, "date": o.date.isoformat(), "category_id": o.category_id,
            "description": o.description or "", "name": "", "balance": ""
        })

    def result(self) -> str:
        buf = io.StringIO()
        fieldnames = ["kind","id","name","balance","type","bank_account_id","amount","date","category_id","description"]
        writer = csv.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        for r in self._rows: writer.writerow(r)
        return buf.getvalue()