
from typing import Any, List


class Stack:
    def __init__(self) -> None:
        self.items: List[Any] = []

    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self) -> None:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self) -> Any:
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def __str__(self) -> str:
        return str(self.items)
