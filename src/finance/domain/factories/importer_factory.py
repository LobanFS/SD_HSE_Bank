from pathlib import Path
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.importers.base_importer import BaseImporter
from src.finance.domain.importers.csv_importer import CsvImporter

def importer_for(path: str, factory: EntityFactory) -> BaseImporter:
    ext = Path(path).suffix.lower()
    if ext == ".csv": return CsvImporter(factory)
    raise ValueError(f"Неизвестный формат: {ext}")