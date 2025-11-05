from enum import Enum

class OperationType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"