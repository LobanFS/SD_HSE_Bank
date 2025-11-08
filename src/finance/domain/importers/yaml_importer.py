import yaml
from typing import Any
from src.finance.domain.importers.base_importer import BaseImporter

class YamlImporter(BaseImporter):
    def _parse(self, raw: str) -> dict[str, Any]:
        return yaml.safe_load(raw) or {"accounts": [], "categories": [], "operations": []}
