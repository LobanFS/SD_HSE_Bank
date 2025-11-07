from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.commands.category_commands import CreateCategory, CreateCategoryHandler
from src.finance.domain.enums import CategoryType


class CategoryFacade:
    def __init__(self, handler: CreateCategoryHandler, recorder: Recorder):
        self._create = timed(recorder, "Create category")(handler.handle)

    def create(self, id: str, type: CategoryType, name: str):
        self._create(CreateCategory(id=id, type=type, name=name))
