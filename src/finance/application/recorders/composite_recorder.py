from typing import Iterable
from src.finance.application.recorders.base_recorder import Recorder

class CompositeRecorder(Recorder):
    def __init__(self, recorders: Iterable[Recorder]):
        self._recorders = list(recorders)

    def record(self, name: str, elapsed_ms: float, success: bool) -> None:
        for r in self._recorders:
            try:
                r.record(name, elapsed_ms, success)
            except Exception:
                pass
