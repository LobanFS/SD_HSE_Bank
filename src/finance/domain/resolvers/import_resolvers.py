from __future__ import annotations
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.domain.importers.base_importer import BaseImporter
from src.finance.domain.importers.csv_importer import CsvImporter
from src.finance.domain.importers.json_importer import JsonImporter
from src.finance.domain.importers.yaml_importer import YamlImporter

class ImporterResolver(ABC):
    def __init__(self, factory: EntityFactory, nxt: Optional["ImporterResolver"] = None):
        self._factory = factory
        self._next = nxt

    def resolve(self, path: str) -> Optional[BaseImporter]:
        res = self._try_resolve(path)
        if res is not None:
            return res
        return self._next.resolve(path) if self._next else None

    @abstractmethod
    def _try_resolve(self, path: str) -> Optional[BaseImporter]: ...


class CsvResolver(ImporterResolver):
    def _try_resolve(self, path: str) -> Optional[BaseImporter]:
        return CsvImporter(self._factory) if Path(path).suffix.lower() == ".csv" else None

class JsonResolver(ImporterResolver):
    def _try_resolve(self, path: str) -> Optional[BaseImporter]:
        return JsonImporter(self._factory) if Path(path).suffix.lower() == ".json" else None

class YamlResolver(ImporterResolver):
    def _try_resolve(self, path: str) -> Optional[BaseImporter]:
        return YamlImporter(self._factory) if Path(path).suffix.lower() in (".yaml", ".yml") else None
