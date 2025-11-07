from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.commands.operation_commands import CreateOperation, CreateOperationHandler
from src.finance.domain.enums import  OperationType
from datetime import date

class OperationFacade:
    def __init__(self, handler: CreateOperationHandler, recorder: Recorder):
        self._create = timed(recorder, "Create operation")(handler.handle)

    def create(self, id: str, type: OperationType, bank_account_id: str, date: date,
               category_id: str, amount: float = 0.0, description: str | None = None):
        self._create(CreateOperation(id=id, type=type,
                                                 bank_account_id=bank_account_id,
                                                 date=date, amount=amount,
                                                 category_id=category_id, description=description))
