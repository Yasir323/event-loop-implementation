from typing import TypeVar

T = TypeVar("T")


class EventResult:

    def __init__(self, key: str, result: T) -> None:
        self.key = key
        self.result = result
