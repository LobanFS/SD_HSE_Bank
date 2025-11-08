from typing import Protocol, TypeVar

T = TypeVar("T")

class Command(Protocol[T]):
    pass

class CommandHandler(Protocol[T]):
    def handle(self, cmd: Command[T]): ...


