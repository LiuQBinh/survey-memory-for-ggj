"""
D2 – Personal vs System memory demo.
Two namespaces: (1) user preferences (personal), (2) reasoning steps (system). Add and retrieve from each.
Run: python demo/format/personal_vs_system.py
"""

from __future__ import annotations

import re
from typing import Any, Dict, List


class NamespaceStore:
    """Simple in-memory store per namespace (personal vs system)."""

    def __init__(self) -> None:
        self._data: List[Dict[str, Any]] = []

    def add(self, entry: Dict[str, Any]) -> None:
        self._data.append(entry)

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._data)

    def query(self, question: str) -> List[Dict[str, Any]]:
        """Retrieve entries that match any word in the question (simple keyword overlap)."""
        q_words = set(re.findall(r"\w+", question.lower()))
        out: List[Dict[str, Any]] = []
        for entry in self._data:
            text = " ".join(str(v).lower() for v in entry.values())
            entry_words = set(re.findall(r"\w+", text))
            if q_words & entry_words:
                out.append(entry)
        return out


def main() -> None:
    # Personal memory: what the user said or chose (user-facing)
    personal = NamespaceStore()
    personal.add({
        "what": "User said their name",
        "name": "Bình",
    })
    personal.add({
        "what": "User chose reminder time",
        "remind_at": "17:00",
        "note": "every day",
    })
    personal.add({
        "what": "Last exchange with user",
        "user": "Remind me to stand up at 5pm.",
        "agent": "I'll remind you at 17:00 every day.",
    })

    # System memory: how the agent reasoned (internal, not shown to user)
    system = NamespaceStore()
    system.add({
        "step": 1,
        "did": "Looked up user timezone",
        "result": "Asia/Ho_Chi_Minh",
    })
    system.add({
        "step": 2,
        "did": "Decided when to send reminder",
        "result": "17:00 local time",
    })
    system.add({
        "step": 3,
        "did": "Scheduled reminder in calendar",
        "result": "OK",
    })

    print("Personal vs System memory (D2)\n")
    print("Personal (what the user said / chose):")
    for e in personal.get_all():
        print(f"  {e}")
    print("\nSystem (how the agent reasoned internally):")
    for e in system.get_all():
        print(f"  {e}")

    # Ask and retrieve: simulate questions and show what is pulled from each store
    print("\n--- Ask and retrieve ---\n")
    questions = [
        "What is the user's name?",
        "When is the reminder?",
        "How did the agent decide the time?",
    ]
    for q in questions:
        print(f"Q: {q}")
        from_personal = personal.query(q)
        from_system = system.query(q)
        if from_personal:
            print("  From personal:", from_personal)
        if from_system:
            print("  From system:", from_system)
        if not from_personal and not from_system:
            print("  (no match)")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
