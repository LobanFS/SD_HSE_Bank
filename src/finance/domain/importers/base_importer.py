from abc import ABC, abstractmethod
from typing import Any
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.enums import OperationType, CategoryType
from datetime import date

class BaseImporter(ABC):
    def __init__(self, factory: EntityFactory):
        self.factory = factory

    def import_data(self, raw: str) -> tuple[list, list, list]:
        payload = self._parse(raw)
        payload = self._validate(payload)
        accounts, categories, operations = self._to_domain(payload)
        return accounts, categories, operations

    @abstractmethod
    def _parse(self, raw: str) -> dict[str, Any]: ...

    def _to_domain(self, payload: dict[str, Any]) -> tuple:
        accounts = []
        categories = []
        operations = []

        for account in payload["accounts"]:
            accounts.append(self.factory.create_account(**account))

        for category in payload["categories"]:
            category = dict(category)
            category["type"] = CategoryType[category["type"]]
            categories.append(self.factory.create_category(**category))

        for operation in payload["operations"]:
            operation = dict(operation)
            operation["type"] = OperationType[operation["type"]]
            operation["date"] = date.fromisoformat(operation["date"])
            operations.append(self.factory.create_operation(**operation))

        return accounts, categories, operations

    @staticmethod
    def _validate(payload: dict[str, Any]) -> dict[str, Any]:
        def clean(records, required: list[str]):
            valid = []
            for rec in records:
                if all(rec.get(k) not in (None, "") for k in required):
                    valid.append(rec)
            return valid

        payload["accounts"] = clean(payload["accounts"], ["id", "name"])
        payload["categories"] = clean(payload["categories"], ["id", "name", "type"])
        payload["operations"] = clean(payload["operations"], ["id", "type", "amount", "bank_account_id", "category_id", "date"])

        return payload







