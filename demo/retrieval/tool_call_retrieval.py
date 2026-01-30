"""
D1 – Retrieval via tool call demo.
Memory is accessed through tools (e.g. search_memory, get_preference) that an agent invokes
instead of querying a vector store or graph directly. Matches "Commands & Tools" in the report.
Run: python demo/retrieval/tool_call_retrieval.py
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

# ---------------------------------------------------------------------------
# Memory backend (same data as in other demos, but only reachable via tools)
# ---------------------------------------------------------------------------

MEMORY_FACTS: List[str] = [
    "User prefers dark mode and compact layout.",
    "Meeting scheduled for Tuesday 3pm with the design team.",
    "User asked for a summary of the last three conversations.",
]

PREFERENCES: Dict[str, Any] = {
    "theme": "dark",
    "language": "en",
    "layout": "compact",
}


# ---------------------------------------------------------------------------
# Tools: the only way to read memory (tool-call retrieval)
# ---------------------------------------------------------------------------

def search_memory(query: str, top_k: int = 3) -> List[str]:
    """
    Tool: search memory by keyword overlap. Agent calls this to retrieve relevant facts.
    """
    q_lower = set(query.lower().split())
    scored: List[tuple[str, int]] = []
    for fact in MEMORY_FACTS:
        words = set(fact.lower().split())
        score = len(q_lower & words)
        if score > 0:
            scored.append((fact, score))
    scored.sort(key=lambda x: -x[1])
    return [f for f, _ in scored[:top_k]]


def get_preference(key: str) -> Optional[Any]:
    """
    Tool: get a stored user preference by key. Agent calls this for theme, language, etc.
    """
    return PREFERENCES.get(key)


def list_preference_keys() -> List[str]:
    """Tool: list available preference keys (e.g. for discovery)."""
    return list(PREFERENCES.keys())


# ---------------------------------------------------------------------------
# Simulated agent: receives user message, decides which tools to call, uses results
# ---------------------------------------------------------------------------

TOOLS: Dict[str, Callable[..., Any]] = {
    "search_memory": search_memory,
    "get_preference": get_preference,
    "list_preference_keys": list_preference_keys,
}


def simulate_agent_tool_calls(user_message: str) -> List[tuple[str, Any]]:
    """
    Simulated agent: map user message to tool invocations (no real LLM).
    In practice, an LLM would choose tools from a schema and we would execute them.
    """
    calls: List[tuple[str, Any]] = []
    msg_lower = user_message.lower()

    if "prefer" in msg_lower or "theme" in msg_lower or "layout" in msg_lower or "interface" in msg_lower:
        keys = list_preference_keys()
        calls.append(("list_preference_keys", keys))
        for k in ["theme", "layout", "language"]:
            if k in keys:
                v = get_preference(k)
                calls.append((f"get_preference({k!r})", v))

    if "meeting" in msg_lower or "when" in msg_lower or "schedule" in msg_lower:
        results = search_memory(user_message, top_k=2)
        calls.append(("search_memory", results))

    if "summary" in msg_lower or "conversation" in msg_lower or "past" in msg_lower:
        results = search_memory(user_message, top_k=3)
        calls.append(("search_memory", results))

    # If no pattern matched, do a generic search
    if not calls:
        results = search_memory(user_message, top_k=2)
        calls.append(("search_memory", results))

    return calls


def main() -> None:
    print("Retrieval via tool call (D1)\n")
    print("Memory is only accessible through tools: search_memory, get_preference, list_preference_keys.\n")

    examples = [
        "What are the user's interface preferences?",
        "When is the design meeting?",
        "Give me a summary of past conversations.",
    ]

    for msg in examples:
        print(f"User: {msg}")
        calls = simulate_agent_tool_calls(msg)
        for tool_used, result in calls:
            print(f"  -> Tool: {tool_used}")
            print(f"     Result: {result}")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
