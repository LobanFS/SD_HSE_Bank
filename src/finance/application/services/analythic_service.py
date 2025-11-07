from datetime import date
from collections import defaultdict
from src.finance.infrastructure.in_memory_repos.operation_repo import InMemoryOperationRepo
from src.finance.domain.enums import OperationType

class AnalyticsService:
    def __init__(self, operation_repo: InMemoryOperationRepo):
        self._operations = operation_repo

    def diff_for_period(self, start: date, end: date) -> float:
        inc = exp = 0.0
        for op in self._operations.list():
            if not (start <= op.date <= end): continue
            if op.type == OperationType.INCOME: inc += op.amount
            else: exp += op.amount
        return inc - exp

    def by_category(self):
        groupped = {}
        for operation in self._operations.list():
            if operation.type not in groupped:
                groupped[operation.category_id] = {
                    "income" : 0,
                    "expense" : 0
                }
            if operation.type == OperationType.INCOME:
                groupped[operation.category_id]["income"] += operation.amount
            if operation.type == OperationType.EXPENSE:
                groupped[operation.category_id]["expense"] += operation.amount
        return groupped