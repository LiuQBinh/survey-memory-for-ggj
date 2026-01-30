"""
D1 – MCP server for retrieval via tool call.
Exposes search_memory, get_preference, list_preference_keys as MCP tools over stdio.
Use in LM Studio: add this server with command `python` and args `[path/to/mcp_memory_server.py]`.
Requires: pip install "mcp[cli]"
Run directly: python demo/retrieval/mcp_memory_server.py
"""

from __future__ import annotations

from typing import Any, List, Optional

# ---------------------------------------------------------------------------
# Memory backend (same as tool_call_retrieval.py; only reachable via MCP tools)
# ---------------------------------------------------------------------------

MEMORY_FACTS: List[str] = [
    "User prefers dark mode and compact layout.",
    "Meeting scheduled for Tuesday 3pm with the design team.",
    "User asked for a summary of the last three conversations.",
]

PREFERENCES: dict[str, Any] = {
    "theme": "dark",
    "language": "en",
    "layout": "compact",
}


def search_memory(query: str, top_k: int = 3) -> List[str]:
    """Search memory by keyword overlap. Returns relevant stored facts."""
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
    """Get a stored user preference by key (e.g. theme, language, layout)."""
    return PREFERENCES.get(key)


def list_preference_keys() -> List[str]:
    """List available preference keys for discovery."""
    return list(PREFERENCES.keys())


# ---------------------------------------------------------------------------
# MCP server (FastMCP, stdio for LM Studio)
# ---------------------------------------------------------------------------

def _create_mcp():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(
        "Memory (retrieval demo)",
        instructions="Tools to read agent memory: search facts, get user preferences, or list preference keys.",
        json_response=True,
    )

    @mcp.tool()
    def search_memory_tool(query: str, top_k: int = 3) -> List[str]:
        """Search memory by keyword. Use for questions about past events, meetings, or conversations."""
        return search_memory(query, top_k=top_k)

    @mcp.tool()
    def get_preference_tool(key: str) -> Any:
        """Get one user preference by key. Call list_preference_keys first to see available keys (e.g. theme, language, layout)."""
        value = get_preference(key)
        return value if value is not None else "(not set)"

    @mcp.tool()
    def list_preference_keys_tool() -> List[str]:
        """List all preference keys. Use before get_preference to know which keys to request."""
        return list_preference_keys()

    return mcp


def main() -> None:
    mcp = _create_mcp()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
