from datetime import date
from src.finance.domain.entities import Operation
from src.finance.domain.repositories import IRepository
from src.finance.domain.enums import OperationType

class AnalyticsService:
    def __init__(self, operation_repo: IRepository[Operation]):
        self._operations = operation_repo

    def diff_for_period(self, start: date, end: date) -> float:
        inc = exp = 0.0
        for op in self._operations.list():
            if not (start <= op.date <= end): continue
            if op.type == OperationType.INCOME: inc += op.amount
            else: exp += op.amount
        return inc - exp

    def by_category(self) -> dict[str, dict[str, float]]:
        grouped: dict[str, dict[str, float]] = {}

        for op in self._operations.list():
            if op.category_id not in grouped:
                grouped[op.category_id] = {"income": 0.0, "expense": 0.0}

            if op.type == OperationType.INCOME:
                grouped[op.category_id]["income"] += op.amount
            elif op.type == OperationType.EXPENSE:
                grouped[op.category_id]["expense"] += op.amount

        return grouped