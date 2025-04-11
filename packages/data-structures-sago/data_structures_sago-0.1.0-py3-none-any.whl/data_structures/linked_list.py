

"""
Module linked_list.py
Implementation of a singly linked list
"""

from typing import Optional, Any


class Node:
    """
    Represents a node in the list.
    """

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[Node] = None


class LinkedList:
    """
    Class to manipulate a simply linked list.
    """

    def __init__(self):
        self.head: Optional[Node] = None

    def is_empty(self) -> bool:
        return self.head is None

    def append(self, data: Any) -> None:
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data: Any) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data: Any) -> None:
        if self.is_empty():
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next and current.next.data != data:
            current = current.next

        if current.next:
            current.next = current.next.next

    def find(self, data: Any) -> bool:
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def __str__(self) -> str:
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements)

    def traverse(self):
        """
        Traverses the linked list and prints the data of each node.
        """
        if self.is_empty():
            print("The list is empty.")
            return

        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
