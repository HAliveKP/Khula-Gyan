import pytest

from src.generation import llm
from src.generation.spend import SpendLimitError, current_spend, reset_spend


def test_api_call_is_stopped_before_provider_when_estimate_exceeds_cap(monkeypatch, tmp_path):
    reset_spend()
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("LLM_API_KEY", "not-a-real-key")
    monkeypatch.setenv("LLM_INPUT_COST_PER_1M_USD", "100")
    monkeypatch.setenv("LLM_OUTPUT_COST_PER_1M_USD", "100")
    monkeypatch.setenv("MAX_API_SPEND_USD", "0.001")
    monkeypatch.setenv("MAX_API_OUTPUT_TOKENS", "100")
    monkeypatch.setattr(llm, "CACHE_DIR", tmp_path)
    called = False

    def provider_must_not_be_called(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("provider was called despite the cap")

    monkeypatch.setattr(llm, "_make_client", provider_must_not_be_called)
    with pytest.raises(SpendLimitError, match="stopped before it was sent"):
        llm.complete([{"role": "user", "content": "Test request"}], use_cache=False)
    assert called is False
    assert current_spend() == 0
    reset_spend()


def test_paid_call_fails_closed_without_cost_rates(monkeypatch):
    monkeypatch.setenv("LLM_INPUT_COST_PER_1M_USD", "")
    monkeypatch.setenv("LLM_OUTPUT_COST_PER_1M_USD", "")
    with pytest.raises(SpendLimitError, match="set LLM_INPUT_COST_PER_1M_USD"):
        from src.generation.spend import reserve
        reserve([{"role": "user", "content": "Test"}])

