from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).parents[1] / "src" / "structures.py"
spec = importlib.util.spec_from_file_location("structures", MODULE_PATH)
assert spec and spec.loader
structures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(structures)

BinarySearchTree = structures.BinarySearchTree
Graph = structures.Graph
PriorityQueue = structures.PriorityQueue


def test_binary_search_tree_insert_contains_and_inorder() -> None:
    tree = BinarySearchTree()
    for value in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        tree.insert(value)

    assert tree.contains(7)
    assert not tree.contains(2)
    assert tree.inorder() == [1, 3, 4, 6, 7, 8, 10, 13, 14]
    assert tree.level_order() == [8, 3, 10, 1, 6, 14, 4, 7, 13]


def test_priority_queue_uses_priority_then_insertion_order() -> None:
    queue = PriorityQueue()
    queue.push("batch", priority=3)
    queue.push("online-a", priority=1)
    queue.push("online-b", priority=1)

    assert queue.pop() == "online-a"
    assert queue.pop() == "online-b"
    assert queue.pop() == "batch"


def test_graph_bfs_and_dfs() -> None:
    graph = Graph(directed=False)
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    graph.add_edge("b", "d")

    assert graph.bfs("a") == ["a", "b", "c", "d"]
    assert graph.dfs("a") == ["a", "b", "d", "c"]


def test_topological_sort_respects_dependencies() -> None:
    graph = Graph()
    graph.add_edge("load", "validate")
    graph.add_edge("validate", "train")
    graph.add_edge("train", "evaluate")

    assert graph.topological_sort() == ["load", "validate", "train", "evaluate"]


def test_topological_sort_detects_cycle() -> None:
    graph = Graph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "a")

    try:
        graph.topological_sort()
    except ValueError as error:
        assert "cycle" in str(error)
    else:
        raise AssertionError("cycle should raise ValueError")
