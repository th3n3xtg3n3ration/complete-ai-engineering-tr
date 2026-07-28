"""Foundational data structures used in the lesson exercises."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """A small LIFO stack backed by a Python list."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)


class BoundedQueue(Generic[T]):
    """A FIFO queue with an explicit capacity limit."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        if len(self._items) >= self._capacity:
            raise OverflowError("queue capacity reached")
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)


@dataclass(slots=True)
class Node(Generic[T]):
    value: T
    next: Node[T] | None = None


class SinglyLinkedList(Generic[T]):
    """A singly linked list supporting O(1) prepend."""

    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self._size = 0

    def prepend(self, value: T) -> None:
        self.head = Node(value=value, next=self.head)
        self._size += 1

    def find(self, value: T) -> bool:
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def __iter__(self) -> Iterator[T]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        return self._size


class SessionStore:
    """A tiny hash-table-backed session store."""

    def __init__(self) -> None:
        self._sessions: dict[str, str] = {}

    def set(self, session_id: str, user_id: str) -> None:
        if not session_id or not user_id:
            raise ValueError("session_id and user_id must be non-empty")
        self._sessions[session_id] = user_id

    def get(self, session_id: str) -> str | None:
        return self._sessions.get(session_id)

    def remove(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None


if __name__ == "__main__":
    queue = BoundedQueue[str](capacity=2)
    queue.enqueue("request-1")
    queue.enqueue("request-2")
    print(queue.dequeue())
