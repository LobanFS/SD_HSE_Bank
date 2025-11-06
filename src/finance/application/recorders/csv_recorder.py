import csv, os
from datetime import datetime
from .base_recorder import Recorder

class CsvRecorder(Recorder):
    def __init__(self, directory: str = "data"):
        self._dir = directory
        os.makedirs(self._dir, exist_ok=True)
        self._path = os.path.join(self._dir, "metrics.csv")
        self._ensure_header()

    def _ensure_header(self):
        if not os.path.exists(self._path):
            with open(self._path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["timestamp", "name", "elapsed_ms", "success"])

    def record(self, name: str, elapsed_ms: float, success: bool):
        row = [
            datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            name,
            f"{elapsed_ms:.3f}",
            "1" if success else "0"
        ]
        with open(self._path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)