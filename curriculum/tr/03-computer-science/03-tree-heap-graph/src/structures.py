from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from typing import Generic, Hashable, TypeVar

T = TypeVar("T")
NodeT = TypeVar("NodeT", bound=Hashable)


@dataclass
class TreeNode(Generic[T]):
    value: T
    left: TreeNode[T] | None = None
    right: TreeNode[T] | None = None


class BinarySearchTree(Generic[T]):
    def __init__(self) -> None:
        self.root: TreeNode[T] | None = None

    def insert(self, value: T) -> None:
        if self.root is None:
            self.root = TreeNode(value)
            return

        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = TreeNode(value)
                    return
                current = current.right
            else:
                return

    def contains(self, value: T) -> bool:
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

    def inorder(self) -> list[T]:
        result: list[T] = []

        def visit(node: TreeNode[T] | None) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node.value)
            visit(node.right)

        visit(self.root)
        return result

    def level_order(self) -> list[T]:
        if self.root is None:
            return []
        result: list[T] = []
        queue: deque[TreeNode[T]] = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, T]] = []
        self._sequence = 0

    def push(self, item: T, priority: int) -> None:
        heapq.heappush(self._heap, (priority, self._sequence, item))
        self._sequence += 1

    def pop(self) -> T:
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)[2]

    def __len__(self) -> int:
        return len(self._heap)


class Graph(Generic[NodeT]):
    def __init__(self, directed: bool = True) -> None:
        self.directed = directed
        self.adjacency: dict[NodeT, set[NodeT]] = {}

    def add_node(self, node: NodeT) -> None:
        self.adjacency.setdefault(node, set())

    def add_edge(self, source: NodeT, target: NodeT) -> None:
        self.add_node(source)
        self.add_node(target)
        self.adjacency[source].add(target)
        if not self.directed:
            self.adjacency[target].add(source)

    def bfs(self, start: NodeT) -> list[NodeT]:
        if start not in self.adjacency:
            return []
        visited = {start}
        queue: deque[NodeT] = deque([start])
        order: list[NodeT] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.adjacency[node], key=str):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: NodeT) -> list[NodeT]:
        if start not in self.adjacency:
            return []
        visited: set[NodeT] = set()
        order: list[NodeT] = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            stack.extend(
                reversed(sorted(self.adjacency[node], key=str))
            )
        return order

    def topological_sort(self) -> list[NodeT]:
        if not self.directed:
            raise ValueError("topological sort requires a directed graph")

        indegree = {node: 0 for node in self.adjacency}
        for neighbors in self.adjacency.values():
            for neighbor in neighbors:
                indegree[neighbor] += 1

        queue: deque[NodeT] = deque(
            sorted((node for node, degree in indegree.items() if degree == 0), key=str)
        )
        order: list[NodeT] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.adjacency[node], key=str):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.adjacency):
            raise ValueError("graph contains a cycle")
        return order


if __name__ == "__main__":
    tree = BinarySearchTree[int]()
    for number in [8, 3, 10, 1, 6, 14]:
        tree.insert(number)
    print("BST inorder:", tree.inorder())

    tasks = PriorityQueue[str]()
    tasks.push("batch-report", priority=3)
    tasks.push("online-inference", priority=1)
    print("Next task:", tasks.pop())

    pipeline = Graph[str]()
    pipeline.add_edge("load", "validate")
    pipeline.add_edge("validate", "train")
    pipeline.add_edge("train", "evaluate")
    print("Pipeline order:", pipeline.topological_sort())
