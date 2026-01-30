"""
D1 – Graph / Key-value retrieval demo.
Key-value store (dict) + optional graph (NetworkX) for nodes/edges; retrieve by key or traversal.
Run: python demo/retrieval/graph_or_kv_retrieval.py
"""

from __future__ import annotations

try:
    import networkx as nx
except ImportError:
    nx = None  # type: ignore

from typing import Any, Dict, List, Optional


class KeyValueMemory:
    """Simple key-value memory store (dict-backed)."""

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def keys(self) -> List[str]:
        return list(self._store.keys())


def demo_kv() -> None:
    print("Key-value retrieval\n")
    kv = KeyValueMemory()
    kv.set("user:theme", "dark")
    kv.set("user:language", "en")
    kv.set("last_topic", "retrieval memory")
    kv.set("session:turn_count", 5)

    for key in ["user:theme", "last_topic", "session:turn_count"]:
        print(f"  get({key!r}) -> {kv.get(key)!r}")
    print()


def demo_graph() -> None:
    if nx is None:
        print("Graph retrieval skipped (install networkx: pip install networkx)\n")
        return

    print("Graph retrieval (nodes = facts, edges = relations)\n")
    G = nx.DiGraph()
    G.add_node("user", type="entity", name="User")
    G.add_node("preference:theme", type="preference", value="dark")
    G.add_node("preference:layout", type="preference", value="compact")
    G.add_node("event:meeting", type="event", when="Tuesday 3pm")
    G.add_edge("user", "preference:theme", relation="has_preference")
    G.add_edge("user", "preference:layout", relation="has_preference")
    G.add_edge("user", "event:meeting", relation="scheduled")

    # Retrieve: neighbors of "user"
    neighbors = list(G.successors("user"))
    print("  Neighbors of 'user':", neighbors)
    for n in neighbors:
        attrs = G.nodes[n]
        print(f"    {n}: {attrs}")
    print("Done (graph).\n")


def main() -> None:
    print("Graph / Key-value retrieval (D1)\n")
    demo_kv()
    demo_graph()


if __name__ == "__main__":
    main()
