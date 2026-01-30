# survey-memory-for-ggj

Runnable demos for the **AI Agent Memory** report: **D1** retrieval memory, **D2** format of memory, **D3** evaluation flow.

**Report (Notion):** [LLM memory](https://www.notion.so/ggjungle/LLM-memory-2f8cf7d9448880e6833aec61026996f8)

---

## Requirements

- Python 3.8+
- Optional: `networkx` for graph demos (`pip install networkx`)
- For MCP server: Python 3.10+, `pip install "mcp[cli]"`

---

## Demo

### D1 – Retrieval Memory

- **Similarity-based:** in-memory vector store, add + query top-k.  
  `python demo/retrieval/similarity_retrieval.py`

- **Graph / Key-value:** dict + optional NetworkX graph.  
  `python demo/retrieval/graph_or_kv_retrieval.py`

- **Tool call:** memory only via tools (`search_memory`, `get_preference`).  
  `python demo/retrieval/tool_call_retrieval.py`

- **MCP server (LM Studio):** same tools over stdio. In LM Studio add MCP server: command `python`, args `["demo/retrieval/mcp_memory_server.py"]`. Tools: `search_memory_tool`, `get_preference_tool`, `list_preference_keys_tool`.

### D2 – Format of memory

- **Explicit:** same content in free text, vector, graph.  
  `python demo/format/explicit_memory.py`

- **Personal vs System:** two namespaces (user preferences vs reasoning).  
  `python demo/format/personal_vs_system.py`

### D3 – Evaluation flow

- NIAH-style benchmark, exact match.  
  `python demo/evaluation/run_eval.py`

---

## Layout

```
demo/
  retrieval/   similarity_retrieval.py, graph_or_kv_retrieval.py,
               tool_call_retrieval.py, mcp_memory_server.py
  format/      explicit_memory.py, personal_vs_system.py
  evaluation/  run_eval.py
  README.md    (detailed demo doc)
```
