import csv, io
from typing import Any
from src.finance.domain.importers.base_importer import BaseImporter

class CsvImporter(BaseImporter):
    def _parse(self, raw: str) -> dict[str, Any]:
        accounts, categories, operations = [], [], []
        reader = csv.DictReader(io.StringIO(raw))
        for row in reader:
            kind = (row.get("kind") or "").lower()
            if kind == "account":
                accounts.append({
                    "id": row["id"],
                    "name": row["name"],
                    "balance": float(row.get("balance") or 0),
                })
            elif kind == "category":
                categories.append({
                    "id": row["id"],
                    "type": row["type"],
                    "name": row["name"],
                })
            elif kind == "operation":
                operations.append({
                    "id": row["id"],
                    "type": row["type"],
                    "bank_account_id": row["bank_account_id"],
                    "amount": float(row["amount"]),
                    "date": row["date"],
                    "category_id": row["category_id"],
                    "description": row.get("description") or None,
                })
        return {"accounts": accounts, "categories": categories, "operations": operations}
