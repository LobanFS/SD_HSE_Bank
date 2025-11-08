import json
from typing import Any
from src.finance.domain.importers.base_importer import BaseImporter

class JsonImporter(BaseImporter):
    def _parse(self, raw: str) -> dict[str, Any]:
        return json.loads(raw)
