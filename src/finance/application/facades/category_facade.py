from src.finance.application.decorators.timing import timed
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.commands.category_commands import (
    CreateCategory, CreateCategoryHandler,
    RenameCategory, RenameCategoryHandler,
    DeleteCategory, DeleteCategoryHandler,
)
from src.finance.domain.enums import CategoryType


class CategoryFacade:
    def __init__(
        self,
        create_handler: CreateCategoryHandler,
        rename_handler: RenameCategoryHandler,
        delete_handler: DeleteCategoryHandler,
        recorder: Recorder,
    ):
        self._create = timed(recorder, "Category.Create")(create_handler.handle)
        self._rename = timed(recorder, "Category.Rename")(rename_handler.handle)
        self._delete = timed(recorder, "Category.Delete")(delete_handler.handle)

    def create(self, id: str, type: CategoryType, name: str):
        self._create(CreateCategory(id=id, type=type, name=name))

    def rename(self, id: str, new_name: str):
        self._rename(RenameCategory(id=id, new_name=new_name))

    def delete(self, id: str):
        self._delete(DeleteCategory(id=id))