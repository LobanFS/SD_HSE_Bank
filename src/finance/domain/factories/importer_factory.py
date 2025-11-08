from pathlib import Path
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.importers.base_importer import BaseImporter
from src.finance.domain.importers.csv_importer import CsvImporter
from src.finance.domain.importers.csv_importer import CsvImporter
from src.finance.domain.importers.json_importer import JsonImporter
from src.finance.domain.importers.yaml_importer import YamlImporter

def importer_for(path: str, factory: EntityFactory) -> BaseImporter:
    ext = Path(path).suffix.lower()
    if ext == ".csv": return CsvImporter(factory)
    if ext == ".json": return JsonImporter(factory)
    if ext == ".yaml" or ext == ".yml": return YamlImporter(factory)
    raise ValueError(f"Неизвестный формат: {ext}")