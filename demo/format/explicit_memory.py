"""
D2 – Explicit memory demo.
Store the same content in three formats: free text (string), vector (embedding), graph (node/triple).
Run: python demo/format/explicit_memory.py
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Tuple

try:
    import networkx as nx
except ImportError:
    nx = None  # type: ignore


def simple_embed(text: str, dim: int = 64) -> List[float]:
    """Simple deterministic embedding (hash-based bag-of-words)."""
    words = re.findall(r"\w+", text.lower())
    vec = [0.0] * dim
    for w in words:
        vec[hash(w) % dim] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def main() -> None:
    content = "User prefers dark mode and compact layout for the dashboard."

    # 1. Free text
    free_text = content
    print("Explicit memory – same content in three formats\n")
    print("1. Free text (string):")
    print(f"   {free_text}\n")

    # 2. Vector (embedding)
    vector = simple_embed(content)
    print("2. Vector (embedding):")
    print(f"   dim={len(vector)}, sample: [{vector[0]:.3f}, {vector[1]:.3f}, ...]\n")

    # 3. Graph (node or triple)
    if nx is not None:
        G = nx.DiGraph()
        G.add_node("fact_1", type="preference", text=content[:50] + "...")
        G.add_node("subject", label="User")
        G.add_node("object", label="dark mode, compact layout")
        G.add_edge("subject", "fact_1", relation="has_preference")
        G.add_edge("fact_1", "object", relation="refers_to")
        print("3. Graph (nodes + edges):")
        for u, v, d in G.edges(data=True):
            print(f"   ({u}) --[{d.get('relation', '')}]--> ({v})")
        print(f"   Node 'fact_1' text: {G.nodes['fact_1'].get('text', '')}\n")
    else:
        # Fallback: triple as dict
        triple = {"subject": "User", "predicate": "prefers", "object": "dark mode, compact layout"}
        print("3. Graph (triple as dict, networkx not installed):")
        print(f"   {triple}\n")

    print("Done.")


if __name__ == "__main__":
    main()
