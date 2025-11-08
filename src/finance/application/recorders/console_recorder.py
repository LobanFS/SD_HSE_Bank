from src.finance.application.recorders.base_recorder import Recorder

class ConsoleRecorder(Recorder):
    def record(self, name: str, elapsed_ms: float, success: bool) -> None:
        flag = "OK" if success else "FAIL"
        print(f"[metrics] {name}: {elapsed_ms:.2f} ms ({flag})")
