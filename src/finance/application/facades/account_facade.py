from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.commands.account_commands import CreateAccount, CreateAccountHandler

class AccountFacade:
    def __init__(self, handler: CreateAccountHandler, recorder: Recorder):
        self._create = timed(recorder, "Create account")(handler.handle)

    def create(self, id: str, name: str, balance: float = 0.0):
        self._create(CreateAccount(id=id, name=name, balance=balance))
    