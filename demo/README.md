# Demo – AI Agent Memory

Runnable demos for the [AI Agent Memory report](../LLM-Agent-Memory-Report.md): retrieval memory (D1), format of memory (D2), and evaluation flow (D3).

**Requirements:** Python 3.8+. Optional: `networkx` for graph demos (`pip install networkx`).

---

## D1 – Retrieval Memory

### Similarity-based (vector store)

In-memory vector store: add documents, embed (simple bag-of-words style), query with top-k.

```bash
python demo/retrieval/similarity_retrieval.py
```

### Graph / Key-value

Key-value store (dict) and optional graph (NetworkX): add nodes/edges or key-value pairs, retrieve by key or traversal.

```bash
python demo/retrieval/graph_or_kv_retrieval.py
```

### Tool call

Memory is accessed only through tools (e.g. `search_memory`, `get_preference`). A simulated agent chooses which tools to call for each user message; in practice an LLM would pick tools from a schema.

```bash
python demo/retrieval/tool_call_retrieval.py
```

### MCP server (for LM Studio)

Same tools exposed as an MCP server over stdio so you can attach them in LM Studio and let the model call tools.

1. **Install:** `pip install "mcp[cli]"` (Python 3.10+).
2. **Run server (optional test):**  
   `python demo/retrieval/mcp_memory_server.py`  
   (stdio; for LM Studio you do not run this yourself—LM Studio starts it.)
3. **Add in LM Studio:** Developer Settings → MCP → Add server. Example config:
   - **Command:** `python`
   - **Args:** `["/absolute/path/to/survey-memory-for-ggj/demo/retrieval/mcp_memory_server.py"]`  
   Or from repo root: args `["demo/retrieval/mcp_memory_server.py"]` and set working directory to the repo root.
   - **Transport:** stdio (default).

Tools provided: `search_memory_tool`, `get_preference_tool`, `list_preference_keys_tool`.

---

## D2 – Format of memory

### Explicit (free text, vector, graph)

Store the same content in three formats: free text (string), vector (embedding), graph (node/triple).

```bash
python demo/format/explicit_memory.py
```

### Personal vs System

Two namespaces: (1) user preferences / dialogue (personal), (2) reasoning / planning steps (system). Add and retrieve from each.

```bash
python demo/format/personal_vs_system.py
```

---

## D3 – Evaluation flow

Load a small NIAH-style benchmark (synthetic QA), feed context into memory, query, compare to ground truth. Metric: exact match. Output: accuracy and short report.

```bash
python demo/evaluation/run_eval.py
```

---

## Layout

```
demo/
  retrieval/
    similarity_retrieval.py   # D1 – vector store, add + query top-k
    graph_or_kv_retrieval.py  # D1 – graph or key-value
    tool_call_retrieval.py   # D1 – retrieval via tool call (search_memory, get_preference)
    mcp_memory_server.py    # D1 – MCP server (stdio) for LM Studio
  format/
    explicit_memory.py        # D2 – free text, vector, graph
    personal_vs_system.py      # D2 – personal vs system store
  evaluation/
    run_eval.py               # D3 – benchmark pipeline, accuracy
  README.md                    # This file
```
