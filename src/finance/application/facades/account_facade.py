from src.finance.application.commands.account_commands import (
    CreateAccount, CreateAccountHandler,
    RenameAccount, RenameAccountHandler,
    DeleteAccount, DeleteAccountHandler,
)
from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
class AccountFacade:
    def __init__(
        self,
        create_handler: CreateAccountHandler,
        rename_handler: RenameAccountHandler,
        delete_handler: DeleteAccountHandler,
        recorder: Recorder,
    ):
        self._create = timed(recorder, "Account.Create")(create_handler.handle)
        self._rename = timed(recorder, "Account.Rename")(rename_handler.handle)
        self._delete = timed(recorder, "Account.Delete")(delete_handler.handle)

    def create(self, id: str, name: str, balance: float = 0.0):
        self._create(CreateAccount(id=id, name=name, balance=balance))

    def rename(self, id: str, new_name: str):
        self._rename(RenameAccount(id=id, new_name=new_name))

    def delete(self, id: str):
        self._delete(DeleteAccount(id=id))