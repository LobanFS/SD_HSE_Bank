from datetime import date
from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.commands.operation_commands import (
    CreateOperation, CreateOperationHandler,
    UpdateOperation, UpdateOperationHandler,
    DeleteOperation, DeleteOperationHandler,
)
from src.finance.domain.enums import OperationType


class OperationFacade:
    def __init__(
        self,
        create_handler: CreateOperationHandler,
        update_handler: UpdateOperationHandler,
        delete_handler: DeleteOperationHandler,
        recorder: Recorder,
    ):
        self._create = timed(recorder, "Operation.Create")(create_handler.handle)
        self._update = timed(recorder, "Operation.Update")(update_handler.handle)
        self._delete = timed(recorder, "Operation.Delete")(delete_handler.handle)

    def create(
        self,
        id: str,
        type: OperationType,
        bank_account_id: str,
        date: date,
        category_id: str,
        amount: float,
        description: str | None = None,
    ):
        self._create(
            CreateOperation(
                id=id,
                type=type,
                bank_account_id=bank_account_id,
                date=date,
                category_id=category_id,
                amount=amount,
                description=description,
            )
        )

    def update(
        self,
        id: str,
        type: OperationType,
        bank_account_id: str,
        date: date,
        category_id: str,
        amount: float,
        description: str | None = None,
    ):
        self._update(
            UpdateOperation(
                id=id,
                type=type,
                bank_account_id=bank_account_id,
                date=date,
                category_id=category_id,
                amount=amount,
                description=description,
            )
        )

    def delete(self, id: str):
        self._delete(DeleteOperation(id=id))
