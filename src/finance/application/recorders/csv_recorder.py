from pathlib import Path
import csv
from datetime import datetime, timezone
from src.finance.application.recorders.base_recorder import Recorder

class CsvRecorder(Recorder):
    def __init__(self, directory: str = "data"):
        base = Path(directory)
        if not base.is_absolute():
            base = Path(__file__).resolve().parents[4] / base
        base.mkdir(parents=True, exist_ok=True)
        self._path = base / "metrics.csv"
        self._ensure_header()

    def _ensure_header(self):
        if not self._path.exists():
            with self._path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["timestamp", "name", "elapsed_ms", "success"])

    def record(self, name: str, elapsed_ms: float, success: bool):
        ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        row = [ts, name, f"{elapsed_ms:.3f}", "1" if success else "0"]
        with open(self._path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)