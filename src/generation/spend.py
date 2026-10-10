"""Conservative per-process API spend estimate and preflight cap.

Paid providers must configure their input/output rates explicitly. The request
is bounded with MAX_API_OUTPUT_TOKENS, then reserved against MAX_API_SPEND_USD
before it is sent. UTF-8 byte counts are used as a conservative token estimate
when provider usage is unavailable; reported spend is still an estimate.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass


class SpendLimitError(RuntimeError):
    """The next request is not allowed by the configured spend budget."""


@dataclass(frozen=True)
class Reservation:
    amount: float
    input_rate: float
    output_rate: float
    input_estimate: int
    output_limit: int


_lock = threading.RLock()
_estimated_spend = 0.0


def _positive_float(name: str, default: str | None = None) -> float:
    raw = os.getenv(name, default)
    if raw is None or not raw.strip():
        raise SpendLimitError(
            f"API request stopped before sending: set {name} to the provider's "
            "USD cost per 1M tokens (use 0 only for a confirmed free rate)."
        )
    try:
        value = float(raw)
    except ValueError as exc:
        raise SpendLimitError(f"API request stopped: {name} must be a number.") from exc
    if value < 0:
        raise SpendLimitError(f"API request stopped: {name} cannot be negative.")
    return value


def max_output_tokens() -> int:
    try:
        value = int(os.getenv("MAX_API_OUTPUT_TOKENS", "1024"))
    except ValueError as exc:
        raise SpendLimitError("API request stopped: MAX_API_OUTPUT_TOKENS must be an integer.") from exc
    if value < 1:
        raise SpendLimitError("API request stopped: MAX_API_OUTPUT_TOKENS must be positive.")
    return value


def reserve(messages: list[dict]) -> Reservation:
    """Reserve the worst-case estimate before one provider attempt."""
    global _estimated_spend
    input_rate = _positive_float("LLM_INPUT_COST_PER_1M_USD")
    output_rate = _positive_float("LLM_OUTPUT_COST_PER_1M_USD")
    output_limit = max_output_tokens()
    input_bytes = len(json.dumps(messages, ensure_ascii=False).encode("utf-8"))
    amount = (input_bytes * input_rate + output_limit * output_rate) / 1_000_000
    try:
        cap = float(os.getenv("MAX_API_SPEND_USD", "1.00"))
    except ValueError as exc:
        raise SpendLimitError("API request stopped: MAX_API_SPEND_USD must be a number.") from exc
    if cap < 0:
        raise SpendLimitError("API request stopped: MAX_API_SPEND_USD cannot be negative.")

    with _lock:
        if _estimated_spend + amount > cap:
            raise SpendLimitError(
                f"API spend cap ${cap:.2f} would be exceeded: estimated current spend "
                f"${_estimated_spend:.6f} + request reservation ${amount:.6f}. "
                "Request was stopped before it was sent. Raise the cap only after human approval."
            )
        _estimated_spend += amount
    return Reservation(amount, input_rate, output_rate, input_bytes, output_limit)


def settle(reservation: Reservation, usage, response_text: str) -> float:
    """Replace the reservation with an estimate based on provider usage, if present."""
    global _estimated_spend
    prompt_tokens = getattr(usage, "prompt_tokens", None) if usage is not None else None
    completion_tokens = getattr(usage, "completion_tokens", None) if usage is not None else None
    if not isinstance(prompt_tokens, int) or prompt_tokens < 0:
        prompt_tokens = reservation.input_estimate
    if not isinstance(completion_tokens, int) or completion_tokens < 0:
        completion_tokens = len(response_text.encode("utf-8"))
    actual_estimate = (
        prompt_tokens * reservation.input_rate + completion_tokens * reservation.output_rate
    ) / 1_000_000
    with _lock:
        _estimated_spend += actual_estimate - reservation.amount
        return _estimated_spend


def current_spend() -> float:
    with _lock:
        return _estimated_spend


def reset_spend() -> None:
    """Start a new CLI/evaluation run. Do not call between app user requests."""
    global _estimated_spend
    with _lock:
        _estimated_spend = 0.0


def configured_cap() -> float:
    try:
        return float(os.getenv("MAX_API_SPEND_USD", "1.00"))
    except ValueError as exc:
        raise SpendLimitError("MAX_API_SPEND_USD must be a number.") from exc

