from pathlib import Path
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.importers.base_importer import BaseImporter
from src.finance.domain.importers.csv_importer import CsvImporter
from src.finance.domain.importers.csv_importer import CsvImporter
from src.finance.domain.importers.json_importer import JsonImporter
from src.finance.domain.importers.yaml_importer import YamlImporter
from src.finance.domain.resolvers.import_resolvers import CsvResolver, JsonResolver, YamlResolver
def importer_for(path: str, factory: EntityFactory) -> BaseImporter:
    chain = CsvResolver(factory, JsonResolver(factory, YamlResolver(factory)))
    importer = chain.resolve(path)
    if importer is None:
        raise ValueError(f"Неизвестный формат файла: {Path(path).suffix.lower()}")
    return importer