import time
from typing import Callable
from src.finance.application.recorders.base_recorder import Recorder

def timed(recorder: Recorder , scenario: str | None = None):
    def decorate(handler : Callable):
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            success = True
            try:
                res = handler(*args, **kwargs)
                return res
            except Exception:
                success = False
                raise
            finally:
                elapsed = (time.perf_counter() - t0) * 1000
                name = scenario or handler.__name__
                recorder.record(name, elapsed, success)
        return wrapper
    return decorate
