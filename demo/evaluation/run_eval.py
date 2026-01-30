"""
D3 – Evaluation flow demo.
Load a small benchmark (NIAH-style or synthetic QA), feed context into memory, query, compare to ground truth.
Metric: exact match (or simulated LLM-as-Judge). Output: accuracy / short report.
Run: python demo/evaluation/run_eval.py
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Tuple


def simple_embed(text: str, dim: int = 64) -> List[float]:
    words = re.findall(r"\w+", text.lower())
    vec = [0.0] * dim
    for w in words:
        vec[hash(w) % dim] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine_sim(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


@dataclass
class Sample:
    """One QA sample: context (long text), question, ground-truth answer."""

    context: str
    question: str
    answer_gt: str


def make_synthetic_benchmark() -> List[Sample]:
    """Minimal NIAH-style benchmark: needle (fact) in haystack (context), question asks for needle."""
    return [
        Sample(
            context="Background paragraph. " * 20 + " The secret code is X7K9. " + "More filler. " * 20,
            question="What is the secret code?",
            answer_gt="X7K9",
        ),
        Sample(
            context="Meeting notes. " * 15 + " The deadline is Friday 5pm. " + "Other items. " * 15,
            question="When is the deadline?",
            answer_gt="Friday 5pm",
        ),
        Sample(
            context="Document. " * 10 + " The winner was Alice. " + "Rest of doc. " * 10,
            question="Who was the winner?",
            answer_gt="Alice",
        ),
    ]


def retrieve_answer(context: str, question: str, top_k: int = 3) -> str:
    """
    Simulated retrieval-based answer: embed context chunks and question, return best-matching chunk
    (or a simple substring match for the demo). For real pipeline, replace with LLM + memory.
    """
    # Chunk context by sentences (rough)
    chunks = [s.strip() for s in re.split(r"[.!?]+", context) if len(s.strip()) > 10]
    if not chunks:
        return ""
    q_emb = simple_embed(question)
    best_score = -1.0
    best_chunk = chunks[0]
    for c in chunks:
        c_emb = simple_embed(c)
        s = cosine_sim(q_emb, c_emb)
        if s > best_score:
            best_score = s
            best_chunk = c
    return best_chunk.strip()


def exact_match(pred: str, gt: str) -> bool:
    """Normalize and check if predicted answer contains ground truth (or equals)."""
    p = pred.lower().strip()
    g = gt.lower().strip()
    return g in p or p == g


def run_eval(samples: List[Sample]) -> Tuple[float, List[bool]]:
    """Run pipeline: for each sample, retrieve answer from context, compare to ground truth."""
    results: List[bool] = []
    for s in samples:
        pred = retrieve_answer(s.context, s.question)
        results.append(exact_match(pred, s.answer_gt))
    accuracy = sum(results) / len(results) if results else 0.0
    return accuracy, results


def main() -> None:
    print("Evaluation flow (D3)\n")
    benchmark = make_synthetic_benchmark()
    accuracy, results = run_eval(benchmark)

    print("Samples:")
    for i, (s, ok) in enumerate(zip(benchmark, results)):
        pred = retrieve_answer(s.context, s.question)
        print(f"  {i + 1}. Q: {s.question}")
        print(f"     GT: {s.answer_gt}  |  Pred: {pred[:50]}...  |  Match: {ok}")
    print(f"\nAccuracy (exact match): {accuracy:.2%} ({sum(results)}/{len(results)})")
    print("\nDone.")


if __name__ == "__main__":
    main()
