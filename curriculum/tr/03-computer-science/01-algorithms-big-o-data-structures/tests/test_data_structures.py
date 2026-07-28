import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "src" / "data_structures.py"
SPEC = importlib.util.spec_from_file_location("data_structures", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

Stack = MODULE.Stack
BoundedQueue = MODULE.BoundedQueue
SinglyLinkedList = MODULE.SinglyLinkedList
SessionStore = MODULE.SessionStore


def test_stack_is_lifo() -> None:
    stack = Stack()
    stack.push("first")
    stack.push("second")
    assert stack.pop() == "second"
    assert stack.peek() == "first"


def test_stack_rejects_empty_pop() -> None:
    with pytest.raises(IndexError):
        Stack().pop()


def test_bounded_queue_is_fifo() -> None:
    queue = BoundedQueue(2)
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2


def test_bounded_queue_enforces_capacity() -> None:
    queue = BoundedQueue(1)
    queue.enqueue("request")
    with pytest.raises(OverflowError):
        queue.enqueue("overflow")


def test_linked_list_prepend_and_find() -> None:
    linked = SinglyLinkedList()
    linked.prepend(1)
    linked.prepend(2)
    assert list(linked) == [2, 1]
    assert linked.find(1)
    assert not linked.find(3)


def test_session_store_lifecycle() -> None:
    store = SessionStore()
    store.set("session-1", "user-1")
    assert store.get("session-1") == "user-1"
    assert store.remove("session-1")
    assert store.get("session-1") is None
