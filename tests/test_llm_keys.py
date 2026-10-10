"""Key pool: rotation, failover on 429/401, shared cache. No network: the client is faked."""

import json

import pytest

from src.generation import llm


class FakeError(Exception):
    def __init__(self, status):
        super().__init__(f"status {status}")
        self.status_code = status


def fake_client_factory(behaviour, calls):
    """behaviour: key -> status code to raise, or None to answer."""
    class Client:
        def __init__(self, key):
            self.key = key
            self.chat = self
            self.completions = self

        def create(self, **kwargs):
            calls.append(self.key)
            status = behaviour.get(self.key)
            if status:
                raise FakeError(status)
            msg = type("M", (), {"content": json.dumps({"key": self.key})})
            return type("R", (), {"choices": [type("C", (), {"message": msg})]})
    return lambda key, base_url: Client(key)


@pytest.fixture(autouse=True)
def setup(monkeypatch, tmp_path):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_MODEL", "some/model")
    monkeypatch.setenv("LLM_API_KEYS", "key-aaaa1111, key-bbbb2222, key-cccc3333")
    monkeypatch.delenv("LLM_KEY_STRATEGY", raising=False)
    monkeypatch.setattr(llm, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(llm, "_next_key", 0)
    monkeypatch.setattr(llm, "_rest_until", {})
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)


def msgs(text):
    return [{"role": "user", "content": text}]


def test_round_robin_spreads_calls(monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "_make_client", fake_client_factory({}, calls))
    for i in range(4):
        llm.complete(msgs(f"q{i}"), use_cache=False)
    assert calls == ["key-aaaa1111", "key-bbbb2222", "key-cccc3333", "key-aaaa1111"]


def test_rate_limited_key_is_skipped_and_same_context_resent(monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "_make_client", fake_client_factory({"key-aaaa1111": 429}, calls))
    out = json.loads(llm.complete(msgs("same question"), use_cache=False))
    assert out["key"] == "key-bbbb2222" and calls == ["key-aaaa1111", "key-bbbb2222"]
    llm.complete(msgs("next"), use_cache=False)  # key 1 is resting, so it is not tried again
    assert "key-aaaa1111" not in calls[2:]


def test_invalid_key_never_retried_and_all_bad_raises(monkeypatch):
    calls = []
    behaviour = {"key-aaaa1111": 401, "key-bbbb2222": 401, "key-cccc3333": 401}
    monkeypatch.setattr(llm, "_make_client", fake_client_factory(behaviour, calls))
    with pytest.raises(RuntimeError, match="all 3 key"):
        llm.complete(msgs("q"), use_cache=False)
    assert len(calls) == 3  # each bad key tried once, then it stops


def test_failover_always_starts_with_first_key(monkeypatch):
    monkeypatch.setenv("LLM_KEY_STRATEGY", "failover")
    calls = []
    monkeypatch.setattr(llm, "_make_client", fake_client_factory({}, calls))
    llm.complete(msgs("a"), use_cache=False)
    llm.complete(msgs("b"), use_cache=False)
    assert calls == ["key-aaaa1111", "key-aaaa1111"]


def test_cache_is_shared_by_all_keys(monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "_make_client", fake_client_factory({}, calls))
    first = llm.complete(msgs("cached?"))
    second = llm.complete(msgs("cached?"))
    assert first == second and len(calls) == 1


def test_single_key_still_works(monkeypatch):
    monkeypatch.delenv("LLM_API_KEYS")
    monkeypatch.setenv("LLM_API_KEY", "only-key-9999")
    calls = []
    monkeypatch.setattr(llm, "_make_client", fake_client_factory({}, calls))
    llm.complete(msgs("q"), use_cache=False)
    assert calls == ["only-key-9999"]


def test_mask_hides_key():
    assert llm.mask("sk-or-v1-abcdef123456") == "...3456"
