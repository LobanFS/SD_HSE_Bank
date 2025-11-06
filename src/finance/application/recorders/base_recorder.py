from typing import Protocol

class Recorder(Protocol):
    def record(self, name: str, elapsed_ms: float, success: bool) -> None: ...