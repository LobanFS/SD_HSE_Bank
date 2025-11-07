from dependency_injector import containers, providers
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.account_repo import InMemoryAccountRepo
from src.finance.infrastructure.in_memory_repos.category_repo import InMemoryCategoryRepo
from src.finance.infrastructure.in_memory_repos.operation_repo import InMemoryOperationRepo
from src.finance.application.recorders.csv_recorder import CsvRecorder
from src.finance.application.commands.account_commands import CreateAccountHandler
from src.finance.application.commands.category_commands import CreateCategoryHandler
from src.finance.application.commands.operation_commands import CreateOperationHandler
from src.finance.application.facades.account_facade import AccountFacade
from src.finance.application.facades.category_facade import CategoryFacade
from src.finance.application.facades.operation_facade import OperationFacade
from src.finance.application.facades.analytics_facade import AnalyticsFacade
from src.finance.application.facades.import_facade import ImportFacade
from src.finance.application.facades.export_facade import ExportFacade
from src.finance.application.services.analytics_service import AnalyticsService
from src.finance.infrastructure.export.csv_export_visitor import CsvExportVisitor

class Container(containers.DeclarativeContainer):
    #синглетоны
    factory = providers.Singleton(EntityFactory)
    recorder = providers.Singleton(CsvRecorder, directory="data")

    #репозитории
    account_repo = providers.Singleton(InMemoryAccountRepo)
    category_repo = providers.Singleton(InMemoryCategoryRepo)
    operation_repo = providers.Singleton(InMemoryOperationRepo)

    # хендлеры
    create_account_handler = providers.Factory(
        CreateAccountHandler,
        repo=account_repo,
        factory=factory,
    )
    create_category_handler = providers.Factory(
        CreateCategoryHandler,
        repo=category_repo,
        factory=factory,
    )
    create_operation_handler = providers.Factory(
        CreateOperationHandler,
        operation_repo=operation_repo,
        account_repo=account_repo,
        category_repo=category_repo,
        factory=factory,
    )

    # сервисы
    analytics_service = providers.Factory(
        AnalyticsService,
        operation_repo=operation_repo,
    )

    # фасады
    account_facade = providers.Factory(
        AccountFacade,
        handler=create_account_handler,
        recorder=recorder,
    )
    category_facade = providers.Factory(
        CategoryFacade,
        handler=create_category_handler,
        recorder=recorder,
    )
    operation_facade = providers.Factory(
        OperationFacade,
        handler=create_operation_handler,
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