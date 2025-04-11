

"""
Module queue.py
This module contains the implementation of a Queue in Python.
"""

from typing import Any, List


class Queue:
    def __init__(self) -> None:
        """
        Initializes a new, empty queue.
        """
        self.items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the end of the queue.
        Args:
        item: The item to add.
        """
        self.items.append(item)

    def dequeue(self) -> Any:
        """
        Checks out and returns the item to the front of the queue (first in, first out).

        Returns:
        The removed item.

        Stakes:
        IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)  # pop(0) remove the first item

    def peek(self) -> Any:
        """
        Returns the item to the front of the queue without removing it.

        Returns:
        The first item in the queue, or None if the queue is empty.
        """
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
        True if the queue contains no items, False otherwise. 
        """
        return len(self.items) == 0

    def __str__(self) -> str:
        """
        Returns a string representation of the queue.
        """
        return str(self.items)
