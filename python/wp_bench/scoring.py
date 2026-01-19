"""Score aggregation utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Any, Dict, List, Optional


@dataclass
class ScoreBreakdown:
    knowledge: float = 0.0
    correctness: float = 0.0
    quality: float = 0.0
    weights: Dict[str, float] = field(
        default_factory=lambda: {"knowledge": 0.3, "correctness": 0.4, "quality": 0.3}
    )

    def overall(self) -> float:
        total = 0.0
        for key, weight in self.weights.items():
            total += getattr(self, key, 0.0) * weight
        return round(total, 4)


class ScoreAggregator:
    def __init__(self) -> None:
        self.knowledge_scores: List[float] = []
        self.correctness_scores: List[float] = []
        self.quality_scores: List[float] = []

    def add_execution(self, correctness: float, quality: float | None = None) -> None:
        self.correctness_scores.append(correctness)
        if quality is not None:
            self.quality_scores.append(quality)

    def add_knowledge(self, score: float) -> None:
        self.knowledge_scores.append(score)

    def finalize(self) -> ScoreBreakdown:
        breakdown = ScoreBreakdown()
        if self.knowledge_scores:
            breakdown.knowledge = mean(self.knowledge_scores)
        if self.correctness_scores:
            breakdown.correctness = mean(self.correctness_scores)
        if self.quality_scores:
            breakdown.quality = mean(self.quality_scores)
        else:
            breakdown.quality = 0.0
        return breakdown


@dataclass
class TokenUsage:
    """Token counts from a single model call."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
        )


@dataclass
class UsageSummary:
    """Aggregated usage statistics for a benchmark run."""

    total_tokens: TokenUsage = field(default_factory=TokenUsage)
    estimated_cost_usd: Optional[float] = None
    num_calls: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt_tokens": self.total_tokens.prompt_tokens,
            "completion_tokens": self.total_tokens.completion_tokens,
            "total_tokens": self.total_tokens.total_tokens,
            "estimated_cost_usd": (
                round(self.estimated_cost_usd, 6)
                if self.estimated_cost_usd is not None
                else None
            ),
            "num_calls": self.num_calls,
        }


class UsageAggregator:
    """Aggregates token usage and cost across multiple model calls."""

    def __init__(self) -> None:
        self.total_tokens = TokenUsage()
        self.total_cost: float = 0.0
        self.num_calls: int = 0
        self._has_cost_data: bool = True

    def add(self, usage: TokenUsage, cost: Optional[float] = None) -> None:
        self.total_tokens = self.total_tokens + usage
        self.num_calls += 1
        if cost is not None:
            self.total_cost += cost
        else:
            self._has_cost_data = False

    def finalize(self) -> UsageSummary:
        return UsageSummary(
            total_tokens=self.total_tokens,
            estimated_cost_usd=self.total_cost if self._has_cost_data else None,
            num_calls=self.num_calls,
        )
