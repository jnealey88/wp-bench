"""Model interface leveraging LiteLLM providers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from litellm import completion, completion_cost
from litellm.utils import ModelResponse

from .config import ModelConfig


@dataclass
class GenerationResult:
    """Result from a model generation call with usage data."""

    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Optional[float] = None


class ModelInterface:
    """Thin wrapper over LiteLLM to keep prompts consistent."""

    def __init__(self, config: ModelConfig):
        self.config = config

    def generate(self, prompt: str) -> GenerationResult:
        """Generate a completion for the given prompt.

        Args:
            prompt: The user prompt to send to the model.

        Returns:
            GenerationResult with text and token usage data.
        """
        kwargs = {
            "model": self.config.name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.temperature,
            "timeout": self.config.request_timeout,
        }
        # Only add optional params if they're set
        if self.config.max_tokens is not None:
            kwargs["max_tokens"] = self.config.max_tokens
        if self.config.top_p is not None:
            kwargs["top_p"] = self.config.top_p
        if self.config.reasoning_effort:
            kwargs["reasoning_effort"] = self.config.reasoning_effort
        # Extended thinking for Claude models
        if self.config.extended_thinking and self.config.extended_thinking.enabled:
            kwargs["thinking"] = {
                "type": "enabled",
                "budget_tokens": self.config.extended_thinking.budget_tokens,
            }
        response: ModelResponse = completion(**kwargs)
        choice = response.choices[0]
        text = choice.message["content"]  # type: ignore[index]

        # Extract usage data with safe defaults
        usage = getattr(response, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
        completion_tokens = getattr(usage, "completion_tokens", 0) or 0
        total_tokens = getattr(usage, "total_tokens", 0) or 0

        # Estimate cost (may fail for some providers)
        cost = self._safe_estimate_cost(response)

        return GenerationResult(
            text=text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
        )

    def _safe_estimate_cost(self, response: ModelResponse) -> Optional[float]:
        """Safely estimate cost, returning None if not available."""
        try:
            return completion_cost(completion_response=response)
        except Exception:
            return None
