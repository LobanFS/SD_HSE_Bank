from dependency_injector import containers, providers
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.account_repo import InMemoryAccountRepo
from src.finance.infrastructure.in_memory_repos.category_repo import InMemoryCategoryRepo
from src.finance.infrastructure.in_memory_repos.operation_repo import InMemoryOperationRepo
from src.finance.application.commands.account_commands import CreateAccountHandler, RenameAccountHandler, DeleteAccountHandler
from src.finance.application.commands.category_commands import CreateCategoryHandler, RenameCategoryHandler, DeleteCategoryHandler
from src.finance.application.commands.operation_commands import CreateOperationHandler, UpdateOperationHandler, DeleteOperationHandler
from src.finance.application.facades.account_facade import AccountFacade
from src.finance.application.facades.category_facade import CategoryFacade
from src.finance.application.facades.operation_facade import OperationFacade
from src.finance.application.facades.analytics_facade import AnalyticsFacade
from src.finance.application.facades.import_facade import ImportFacade
from src.finance.application.facades.export_facade import ExportFacade
from src.finance.application.services.analytics_service import AnalyticsService
from src.finance.application.facades.query_facade import QueryFacade
from src.finance.application.recorders.csv_recorder import CsvRecorder
from src.finance.application.recorders.console_recorder import ConsoleRecorder
from src.finance.application.recorders.composite_recorder import CompositeRecorder

class Container(containers.DeclarativeContainer):
    #синглетоны
    factory = providers.Singleton(EntityFactory)
    csv_recorder     = providers.Singleton(CsvRecorder, directory="data")
    console_recorder = providers.Singleton(ConsoleRecorder)

    #репозитории
    account_repo = providers.Singleton(InMemoryAccountRepo)
    category_repo = providers.Singleton(InMemoryCategoryRepo)
    operation_repo = providers.Singleton(InMemoryOperationRepo)

    # компоновщик
    recorder = providers.Singleton(
        CompositeRecorder,
        recorders=providers.List(csv_recorder, console_recorder),
    )
    # хендлеры
    create_account_handler = providers.Factory(
        CreateAccountHandler,
        repo=account_repo,
        factory=factory,
    )
    rename_account_handler = providers.Factory(
        RenameAccountHandler,
        repo=account_repo,
    )
    delete_account_handler = providers.Factory(
        DeleteAccountHandler,
        repo=account_repo,
    )

    create_category_handler = providers.Factory(
        CreateCategoryHandler,
        repo=category_repo,
        factory=factory,
    )
    rename_category_handler = providers.Factory(
        RenameCategoryHandler,
        repo=category_repo,
    )
    delete_category_handler = providers.Factory(
        DeleteCategoryHandler,
        category_repo=category_repo,
        operation_repo=operation_repo,
    )

    create_operation_handler = providers.Factory(
        CreateOperationHandler,
        operation_repo=operation_repo,
        account_repo=account_repo,
        category_repo=category_repo,
        factory=factory,
    )
    update_operation_handler = providers.Factory(
        UpdateOperationHandler,
        operation_repo=operation_repo,
        account_repo=account_repo,
        category_repo=category_repo,
        factory=factory,
    )
    delete_operation_handler = providers.Factory(
        DeleteOperationHandler,
        operation_repo=operation_repo,
        account_repo=account_repo,
    )

    # сервисы
    analytics_service = providers.Factory(
        AnalyticsService,
        operation_repo=operation_repo,
    )

    # фасады
    query_facade = providers.Factory(
        QueryFacade,
        account_repo=account_repo,
        category_repo=category_repo,
        operation_repo=operation_repo,
        recorder=recorder,
    )

    account_facade = providers.Factory(
        AccountFacade,
        create_handler=create_account_handler,
        rename_handler=rename_account_handler,
        delete_handler=delete_account_handler,
        recorder=recorder,
    )
    category_facade = providers.Factory(
        CategoryFacade,
        create_handler=create_category_handler,
        rename_handler=rename_category_handler,
        delete_handler=delete_category_handler,
        recorder=recorder,
    )

    operation_facade = providers.Factory(
        OperationFacade,
        create_handler=create_operation_handler,
        update_handler=update_operation_handler,
        delete_handler=delete_operation_handler,
        recorder=recorder,
    )
    analytics_facade = providers.Factory(
        AnalyticsFacade,
        service=analytics_service,
        recorder=recorder,
    )

    import_facade = providers.Factory(
        ImportFacade,
        factory=factory,
        account_repo=account_repo,
        category_repo=category_repo,
        operation_repo=operation_repo,
    )

    export_facade = providers.Factory(
        ExportFacade,
        account_repo=account_repo,
        category_repo=category_repo,
        operation_repo=operation_repo,
        recorder=recorder,
    )